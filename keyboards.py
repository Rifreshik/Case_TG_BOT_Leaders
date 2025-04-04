from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import EMOJI

def create_main_menu():
    buttons = [
        [InlineKeyboardButton(f"{EMOJI['support']} Запрос на поддержку", callback_data='support')],
        [InlineKeyboardButton(f"{EMOJI['requests']} Просмотр заявок", callback_data='view_requests')],
    ]
    return InlineKeyboardMarkup(buttons)

def create_back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data='back')]])