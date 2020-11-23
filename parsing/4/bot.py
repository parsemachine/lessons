# -*- coding: utf-8 -*-
import datetime
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from main import OUT_FILENAME, OUT_XLSX_FILENAME


# TOKEN Telegram-бота, получить можно у @BotFather
TELEGRAM_TOKEN = ''


def start_handler(update, context):
    text = 'Привет! Выбери, в каком формате прислать парсинг?'
    keyboard = [
        [InlineKeyboardButton(text='Получить JSON', callback_data='get_json'), ],
        [InlineKeyboardButton(text='Получить XLSX', callback_data='get_xlsx'), ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=text, reply_markup=markup)


def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    filenames = {
        'get_json': OUT_FILENAME,
        'get_xlsx': OUT_XLSX_FILENAME,
    }
    filename = filenames.get(query.data)
    if filename:
        modified_at = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d %H:%M:%S')
        caption = 'Результат парсинга от {}.'.format(modified_at)
        with open(filename, 'rb') as f:
            context.bot.send_document(query.message.chat.id, document=f, caption=caption)


updater = Updater(TELEGRAM_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

updater.start_polling()
updater.idle()
