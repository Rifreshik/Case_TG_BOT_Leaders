import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, filters, CallbackQueryHandler, \
    MessageHandler
from handlers import start, button_callback, handle_support_request
from config import BOT_TOKEN, INPUT_SUPPORT_REQUEST
from models import create_base

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def init_db(self):
    await create_base()


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(init_db).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INPUT_SUPPORT_REQUEST: [
                CallbackQueryHandler(button_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_support_request)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)

    logger.info("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()