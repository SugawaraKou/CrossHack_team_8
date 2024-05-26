# -*- coding: utf-8 -*-

import psycopg2
from datetime import datetime
import pytz


class Connection:
    def __init__(self, dbname='crosshack', user='sugawara', host='localhost', password='1qw23er4', port='5432'):
        # подключение к бд
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password
        self.port = port

        self.connection = psycopg2.connect(
            database=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def execute(self, query):  # запрос к бд, если нет соединения (отвалилась бд), то переподключиться
        try:
            self.cursor.execute(query)
        except Exception as e:
            self.connection = psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
        return False

    def check_token(self, token):  # проверка токена
        self.execute(f"select * from token_life where token_user='{token}'")
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def get_users(self, user_id):  # получение списка пользователей
        self.execute(f"select * from cross_users where user_id != {user_id}")
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def get_id_user(self, user_id):  # получение списка пользователй по id
        self.execute(f"select * from cross_users where user_id = {user_id}")
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result[0]

    def check_user_id(self, user_id):  # проверка пользователя
        self.execute(f"select user_id from cross_users where user_id = {user_id}")
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        try:
            return result[0]['user_id']
        except:
            return False

    def del_user(self, user_id):  # удаление пользователя
        self.execute(f'delete from cross_users where user_id={user_id}')
        self.connection.commit()

    def registration_user(self, data):  # регистрация пользователя
        query = self.cursor.mogrify('insert into cross_users values (%s, %s, %s, %s)',
                                    (data.id, data.username, data.first_name, data.last_name))
        self.execute(query)
        self.connection.commit()

    def del_token(self, token):  # удаление токена
        self.execute(f"delete from token_life where token_user='{token}'")
        self.connection.commit()

    def get_tokens(self):  # получение токена
        self.execute('select token_user, timestamp from token_life')
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def get_list_materials(self, name_materials):  # получение списка материалов
        self.execute(f'select * from {name_materials}')
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def add_new_toke(self, token, user_creator):  # добавление ноаого токена
        self.execute(f"insert into token_life values ('{token}', "
                     f"{datetime.now(pytz.timezone('Europe/Moscow')).timestamp()}, '{user_creator}')")
        self.connection.commit()

    def get_crosstalks(self):
        self.execute('select * from crosstalks')
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def data_search(self, st):  # поиск
        self.execute(f"select * from book where name like '%{st}%'")
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]

        self.execute(f"select * from courses where description like '%{st}%' or status like '%{st}%'")
        result2 = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]

        self.execute(f"select * from crosstalks where subject like '%{st}%' or speaker like '%{st}%'")
        result3 = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]

        self.execute(f"select * from regulations_ooip where name like '%{st}%' or description like '%{st}%'")
        result4 = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]

        for i in result2:
            result.append({'name': i['description'] + '\n' + i['status'], 'href': i['href']})
        for i in result3:
            result.append({'name': i['subject'] + '\n' + i['speaker'], 'href': i['href']})
        for i in result4:
            result.append({'name': i['name'] + '\n' + i['description'], 'href': i['href']})

        return result

    # test
    def add_data_in_regulations_ooip(self, data):
        self.execute(f"insert into regulations_ooip values ('{data[0]}', '{data[1]}', '{data[2]}')")
        self.connection.commit()

    def add_data_in_crosstalks(self, data):
        self.execute(f"insert into crosstalks values ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')")
        self.connection.commit()

    def add_data_in_books(self, data):
        self.execute(f"insert into book values ('{data[0]}', '{data[1]}')")
        self.connection.commit()
