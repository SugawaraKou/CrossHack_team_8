# -*- coding: utf-8 -*-

import telebot
from telebot import types

from modules import database
from src import tg_token_user
import config


bot = telebot.TeleBot(config.TG_TOKEN)
db = database.Connection(dbname=config.CON_DB['dbname'], user=config.CON_DB['user'], host=config.CON_DB['host'],
                         password=config.CON_DB['password'], port=config.CON_DB['port'])


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Авторизация пользователей
    """
    try:
        msg = str(message.text).split(' ')[1]
    except:
        msg = 'f'

    if db.check_token(msg):
        db.del_token(msg)
        try:
            db.registration_user(message.chat)
        except:
            pass

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton(text='/Найти_курс')
    button2 = types.KeyboardButton(text='/Cписок_курсов')
    keyboard.add(button1, button2)

    if message.chat.id in config.TG_ADMIN_USER_ID:
        button3 = types.KeyboardButton(text='/Удалить_пользователя')
        button4 = types.KeyboardButton(text='/Добавить_пользователя')
        keyboard.add(button3, button4)
        bot.send_message(message.chat.id, "Привет админ ✌️", reply_markup=keyboard)
    elif message.chat.id == db.check_user_id(message.chat.id):
        bot.send_message(message.chat.id, "Привет пользователь ✌️", reply_markup=keyboard)


@bot.message_handler(commands=['Добавить_пользователя'])
def add_user(message):
    """
    Добавление пользователя
    """
    if message.chat.id in config.TG_ADMIN_USER_ID:
        user_token = tg_token_user.create_token(message.chat.username)
        img = open('qr_code.png', 'rb')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Ссылка', url=config.TG_HREF+user_token))
        bot.send_photo(message.chat.id, img, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "У вас нет прав(")


@bot.message_handler(commands=['Удалить_пользователя'])
def delete_user(message):
    """
    Удалить пользователя
    """
    if message.chat.id in config.TG_ADMIN_USER_ID:
        keyboard = types.InlineKeyboardMarkup()
        users = db.get_users(user_id=message.chat.id)
        for i in users:
            keyboard.add(types.InlineKeyboardButton(i['username'], callback_data=i['user_id']))

        bot.send_message(message.chat.id, "Выберите пользователя", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "У вас нет прав(")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Обработка для удаления пользователей и отображения списка учебных материалов
    """
    if call.message.text == 'Выберите пользователя':
        db.del_user(call.data)
        bot.send_message(call.from_user.id,
                         f'Пользователь <b>{call.message.reply_markup.keyboard[0][0].text}</b> удален',
                         parse_mode='html')
    else:
        if call.data == 'regulations_ooip':
            bot.answer_callback_query(call.id, 'ОБРАТИТЕ ВНИМАНИЕ ! логин и пароль к  Conbiz доменные. Если вы не зарегестрированы на ресуре то обратитесь к отделу DevOps для добавления вас на Conbiz.', show_alert=True)
            for i in db.get_list_materials(call.data):
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('Ссылка', url=i['href']))
                bot.send_message(call.from_user.id, i['name'] + '\n' + i['description'], reply_markup=keyboard)
        elif call.data == 'crosstalks':
            for i in db.get_list_materials(call.data):
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('Ссылка', url=i['href']))
                bot.send_message(call.from_user.id, i['date'] + '\n' + i['subject'] + '\n' + i['speaker'], reply_markup=keyboard)
        elif call.data == 'courses':
            bot.answer_callback_query(call.id, 'Для создания аккаунта на платформе moodle, восстановления пароля, или доступа к курсам обратитесь в отдел ОиР.', show_alert=True)
            bot.send_message(call.from_user.id, 'Для этого: \n1. Ознакомьтесь с инструкцией создания обращений в ООиР http://conbiz.lan:8090/pages/viewpage.action?pageId=96633293 \n2. При заполнении обращения укажите в поле "Краткое описание обращения": ФИО, почту и название курсов к которым нужен доступ. \n3. После подачи обращения сотрудник отдела ОИР уведомит вас о выдаче доступа к курсам (и отправит данные новой учетной записи при ее отсутствии)')
            for i in db.get_list_materials(call.data):
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('Ссылка', url=i['href']))
                bot.send_message(call.from_user.id, i['description'] + '\n' + i['status'], reply_markup=keyboard)
        elif call.data == 'book':
            for i in db.get_list_materials(call.data):
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('Ссылка', url=i['href']))
                bot.send_message(call.from_user.id, i['name'], reply_markup=keyboard)
        elif call.data == 'seful_materials':
            pass

    bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(commands=['Cписок_курсов'])
def list_courses(message):
    """
    Посмотреть список курсов
    """
    if message.chat.id in config.TG_ADMIN_USER_ID or int(message.chat.id) == db.get_id_user(message.chat.id)['user_id']:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Регламент ООиР', callback_data='regulations_ooip'))
        keyboard.add(types.InlineKeyboardButton('CrossTalks', callback_data='crosstalks'))
        keyboard.add(types.InlineKeyboardButton('Курсы', callback_data='courses'))
        keyboard.add(types.InlineKeyboardButton('Книги', callback_data='book'))
        keyboard.add(types.InlineKeyboardButton('Полезные материалы', callback_data='seful_materials'))
        bot.send_message(message.chat.id, 'Выберите тип:', reply_markup=keyboard)


@bot.message_handler(commands=['Найти_курс'])
def search_courses(message):
    """
    Найти курс
    """
    if message.chat.id in config.TG_ADMIN_USER_ID or int(message.chat.id) == db.get_id_user(message.chat.id)['user_id']:
        bot.send_message(message.chat.id, 'Введите запрос')
        bot.register_next_step_handler(message, data_search)


def data_search(message):
    for i in db.data_search(message.text):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Ссылка', url=i['href']))
        bot.send_message(message.chat.id, i['name'], reply_markup=keyboard)


bot.infinity_polling(none_stop=True)
