# -*- coding: utf-8 -*-

import psycopg2
from datetime import datetime
import pytz


class Connection:
    def __init__(self, dbname='crosshack', user='sugawara', host='localhost', password='1qw23er4', port='5432'):

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

    def execute(self, query):
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

    def check_user(self, user_id):
        self.execute(f'select privilege from cross_users where user_id={user_id}')
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def get_users(self, user_id):
        self.execute(f'select user_id, username from cross_users where user_id != {user_id}')
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result

    def del_user(self, user_id):
        self.execute(f'delete from cross_users where user_id={user_id}')
        self.connection.commit()

    def registration_user(self, data):
        query = self.cursor.mogrify('insert into cross_users values (%s, %s, %s, %s, 0)',
                                    (data.id, data.username, data.first_name, data.last_name))
        self.execute(query)
        self.connection.commit()

    def add_token(self, data=None):
        # query = self.cursor.mogrify('insert into cross_users values (%s, %s, %s, %s, 0)',
        #                             (data.id, data.username, data.first_name, data.last_name))
        self.execute(f"insert into token_life values (12344, "
                     f"{int(datetime.now(pytz.timezone('Europe/Moscow')).timestamp())}, 'ttt')")
        self.connection.commit()

    def del_token(self, token):
        self.execute(f"delete from token_life where token_user={token}")
        self.connection.commit()

    def get_tokens(self):
        self.execute('select token_user, timestamp from token_life')
        result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  self.cursor.fetchall()]
        return result
