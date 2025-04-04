from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from config import GROUP_CHAT_ID, EMOJI, INPUT_SUPPORT_REQUEST
from keyboards import create_main_menu, create_back_button
from models import SupportRequest, async_session
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n"
        "Я - бот поддержки. Чем могу помочь?\n"
        "Выберите действие из меню ниже:"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=create_main_menu())
    else:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=create_main_menu())

    return INPUT_SUPPORT_REQUEST


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'support':
        await query.edit_message_text(
            f"{EMOJI['support']} Введите ваши данные в формате:\n"
            "ФИО, Статус (полуфиналист/финалист/победитель), "
            "Сезон (1-5), Контакты (телефон и Telegram)\n\n"
            "Пример:\n"
            "Иванов Иван Иванович, финалист, 3, +79161234567 @username",
            reply_markup=create_back_button()
        )
        return INPUT_SUPPORT_REQUEST

    elif query.data == 'view_requests':
        async with async_session() as session:
            result = await session.execute(select(SupportRequest))
            requests = result.scalars().all()

        if requests:
            requests_text = "\n\n".join([
                f"📅 {req.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"👤 {req.full_name} ({req.status}, сезон {req.season})\n"
                f"📞 {req.contacts}\n"
                f"📝 {req.request_text[:50]}..."
                for req in requests
            ])
            await query.edit_message_text(
                f"{EMOJI['requests']} <b>Последние заявки:</b>\n\n{requests_text}",
                parse_mode='HTML',
                reply_markup=create_back_button()
            )
        else:
            await query.edit_message_text(
                f"{EMOJI['warning']} На данный момент нет активных заявок.",
                reply_markup=create_back_button()
            )
        return INPUT_SUPPORT_REQUEST

    elif query.data == 'back':
        return await start(update, context)


async def handle_support_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text
        user = update.message.from_user

        # Парсинг введенных данных
        parts = [part.strip() for part in user_input.split(',')]
        if len(parts) < 4:
            raise ValueError("Неверный формат данных")

        full_name, status, season, *contacts = parts
        contacts = ', '.join(contacts)

        # Сохранение в базу данных
        async with async_session() as session:
            new_request = SupportRequest(
                user_id=user.id,
                username=user.username,
                full_name=full_name,
                status=status,
                season=int(season),
                contacts=contacts,
                request_text=user_input
            )
            session.add(new_request)
            await session.commit()

        # Отправка в группу поддержки
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=(
                f"🆘 <b>Новый запрос от {full_name}</b>\n"
                f"👤 Статус: {status} (сезон {season})\n"
                f"📞 Контакты: {contacts}\n"
                f"📝 Полный текст:\n{user_input}"
            ),
            parse_mode='HTML'
        )

        await update.message.reply_text(
            f"{EMOJI['success']} Заявка оформлена! Ожидайте связи с дежурным.",
            reply_markup=create_main_menu()
        )

    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {e}")
        await update.message.reply_text(
            f"{EMOJI['error']} Ошибка формата данных! Используйте формат:\n"
            "ФИО, Статус, Сезон, Контакты\n\n"
            "Пример:\n"
            "Иванов Иван Иванович, финалист, 3, +79161234567 @username",
            reply_markup=create_main_menu()
        )

    return INPUT_SUPPORT_REQUEST