# -*- coding: utf-8 -*-
import qrcode
import random
import string

from modules import database
import config


def create_token(user_creator):
    db = database.Connection()
    # создание токена
    user_id = ''.join(random.choice('0123456789') for i in range(15))
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for i in range(12))
    list_us = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x",
               "c",
               "v", "b", "n", "m"]

    num_chars_start = random.randint(5, 10)
    num_chars_finish = random.randint(5, 10)
    start = ''.join(random.choices(list_us, k=num_chars_start))
    finish = ''.join(random.choices(list_us, k=num_chars_finish))
    user_id_en = ''
    for digit in str(user_id):
        num_to_add = num_chars_start + int(digit)
        if num_to_add > 9:
            num_to_add -= 10
        user_id_en += str(num_to_add)
    user_name_en = ''
    for char in username:
        index = list_us.index(char)
        new_index = (index + num_chars_finish) % len(list_us)
        user_name_en += list_us[new_index]
    finish_message = start + 'z' + user_id_en + 'v' + user_name_en + 'x' + finish
    # Создать QR-код с зашифрованными данными
    qr = qrcode.QRCode()
    qr_href = config.TG_HREF + finish_message
    qr.add_data(qr_href.encode())
    qr.make(fit=True)
    # Сохранение QR-кода как картинку
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")

    db.add_new_toke(finish_message, user_creator)  # добавление в бд токена и имя пользователя создавшего токен

    return finish_message
