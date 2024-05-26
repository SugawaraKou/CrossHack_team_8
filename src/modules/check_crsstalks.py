# -*- coding: utf-8 -*-
"""
ПАвтоматическая отправка пользователям о новом материале
"""

from datetime import datetime
import pytz
import time
import telebot
from telebot import types

import database
from src import config


db = database.Connection()
bot = telebot.TeleBot(config.TG_TOKEN)

rec = db.get_crosstalks()
for i in rec:
    if (int(datetime.strptime(i['date'], '%d.%m.%Y').timestamp()) ==
            datetime.now(pytz.timezone('Europe/Moscow')).timestamp()):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(i['subject'] + '\n' + i['speaker'], uel=i['href']))
        for user in db.get_users(0):
            bot.send_message(user['user_id'], 'Уже сегодня', reply_markup=keyboard)

    time.sleep(86400)
