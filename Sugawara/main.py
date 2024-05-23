# -*- coding: utf-8 -*-

import telebot
from telebot import types

from modules import database
import config


bot = telebot.TeleBot(config.TG_TOKEN)
db = database.Connection(dbname=config.CON_DB['dbname'], user=config.CON_DB['user'], host=config.CON_DB['host'],
                         password=config.CON_DB['password'], port=config.CON_DB['port'])


def check_privilege_user(data):
    print(12)
    """
    'chat': {'id': 687807958, 'first_name': 'Денис', 'last_name': 'Кузнецов', 'username': 'Sugawara_Kou',
    'type': 'private'}, 'date': 1716217440, 'text': 'sdad'}}
    Проверка пользователй
    Если это новый пользователь, то и автоматическая регистрация
    по ключу
    'https://t.me/Latlon_v2_info_bot?start=' + tg_token.encoder(user_id=user_id, privilege=level)
    """
    return


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Авторизация пользователей
    """
    # res = db.check_user(message.chat.id)
    # if not res:
    #     return
    # else:
    #     res = 1
    if message.chat.id == config.TG_ADMIN_USER_ID:
        db.registration_user(message.chat)
        bot.send_message(message.chat.id, "Привет админ ✌️")


@bot.message_handler(commands=['add_user'])
def add_user(message):
    """
    Добавление пользователя
    """
    # bot.send_message(message.chat.id, "add user")
    img = open('QR_code/1.jpg', 'rb')
    db.add_token()
    bot.send_photo(message.chat.id, img,)
    bot.send_message(message.chat.id, "href")


@bot.message_handler(commands=['del_user'])
def delete_user(message):
    """
    Удалить пользователя
    """
    res = db.check_user(user_id=message.chat.id)
    if len(res) > 0 and res[0]['privilege'] == 0:
        keyboard = types.InlineKeyboardMarkup()
        users = db.get_users(user_id=message.chat.id)
        for i in users:
            keyboard.add(types.InlineKeyboardButton(i['username'], callback_data=i['user_id']))

        bot.send_message(message.chat.id, "Выберите пользователя", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "У вас нет прав(")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    db.del_user(call.data)
    bot.send_message(call.from_user.id, "Пользователь удален")
    bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(commands=['list_courses'])
def list_courses(message):
    """
    Посмотреть список курсов
    """
    bot.send_message(message.chat.id, "list courses")


@bot.message_handler(commands=['search_courses'])
def search_courses(message):
    """
    Найти курс
    """
    bot.send_message(message.chat.id, "search courses")


@bot.message_handler(commands=['help'])
def help_message(message):
    """
    Описание всех возможностей бота
    """
    res = db.check_user(user_id=message.chat.id)
    if len(res) > 0 and res[0]['privilege'] == 1:
        msg = """
        /help - Описание доступных функций
        /search_courses - найти курс
        /list_courses - Cписок курсов
        """
        bot.send_message(message.chat.id, msg)
    elif len(res) > 0 and res[0]['privilege'] == 1:
        msg = """
        /help - Описание доступных функций
        /search_courses - найти курс
        /list_courses - Cписок курсов
        /del_user - Удалить пользователя
        /add_user - Добавить пользователя
        """
        bot.send_message(message.chat.id, msg)


bot.infinity_polling(none_stop=True)
