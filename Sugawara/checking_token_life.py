# -*- coding: utf-8 -*-
"""
Модуль для удаления токена по истечению определенного времени
"""

from datetime import datetime
import time
import pytz

from modules import database
import config

db = database.Connection()

while True:
    rec = db.get_tokens()
    for i in rec:
        if i['timestamp'] + config.LIFE_TG_TOKEN <= int(datetime.now(pytz.timezone('Europe/Moscow')).timestamp()):
            db.del_token(i['token_user'])

    time.sleep(10)
