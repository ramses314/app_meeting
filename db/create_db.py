import random
from random import randint

import psycopg2

from data.config import *


try:
    connection = psycopg2.connect(
        host = host,
        user = user,
        password = password,
        database = db_name
    )

    cursor = connection.cursor()

    with connection.cursor() as cur:
        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS sick_f '
        #     '(id SERIAL PRIMARY KEY,'
        #     'name VARCHAR(100),'
        #     'ind1 VARCHAR(70),'
        #     'ind2 VARCHAR(70)'
        #     ');'
        # )
        # connection.commit()

        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS sick_crazy '
        #     '(id SERIAL PRIMARY KEY,'
        #     'name VARCHAR(100),'
        #     'ind1 VARCHAR(70),'
        #     'ind2 VARCHAR(70)'
        #     ');'
        # )
        # connection.commit()
        #
        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS check_claim '
        #     '(id SERIAL PRIMARY KEY,'
        #     'problem TEXT,'
        #     'quilty INTEGER NOT NULL,'
        #     'not_quilty INTEGER NOT NULL'
        #     ');'
        # )
        # connection.commit()
        #
        cur.execute(
            'CREATE TABLE IF NOT EXISTS statistic '
            '(id SERIAL PRIMARY KEY,'
            'all_user INTEGER default 0,'
            'sleep_user INTEGER default 0'
            ');'
        )
        connection.commit()

        cur.execute(
            'CREATE TABLE IF NOT EXISTS login_web'
            '(id SERIAL PRIMARY KEY,'
            'chat_id INTEGER default 0,'
            'passw VARCHAR(10) default 0,'
            'phone VARCHAR(30)'
            ');'
        )
        connection.commit()

        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS Wishes '
        #     '(id SERIAL PRIMARY KEY,'
        #     'message TEXT,'
        #     'chat_id INTEGER,'
        #     'ind1 VARCHAR(80)'
        #     ');'
        # )
        # connection.commit()

        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS blocked_users '
        #     '(id SERIAL PRIMARY KEY,'
        #     'chat_id INTEGER,'
        #     'ind1 VARCHAR(80)'
        #     ');'
        # )
        # connection.commit()

        cur.execute(
            'CREATE TABLE IF NOT EXISTS main_profil '
            '(id SERIAL PRIMARY KEY,'
            'name VARCHAR(100),'
            'age INTEGER,'
            'country VARCHAR(100),'
            'city VARCHAR(100),'
            'gender VARCHAR(100),'
            'personality VARCHAR(100),'
            'disease VARCHAR(100),'
            'pain VARCHAR(100),'
            'photo VARCHAR(100),'
            'phone VARCHAR(100),'
            'indx VARCHAR(100),'
            'indy VARCHAR(100),'
            'ind1 INTEGER default 0,'
            'ind2 INTEGER default 0,'
            'ind3 INTEGER default 0,'
            'ind4 BOOLEAN NOT NULL DEFAULT TRUE,'
            'created_at DATE not null default current_date,'
            'stop_searching DATE,'
            'last_activity DATE not null default current_date'
            ');'
        )
        connection.commit()

        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS profil_stop_searching '
        #     '(id SERIAL PRIMARY KEY,'
        #     'name VARCHAR(100),'
        #     'age INTEGER,'
        #     'country VARCHAR(100),'
        #     'city VARCHAR(100),'
        #     'gender VARCHAR(100),'
        #     'personality VARCHAR(100),'
        #     'disease VARCHAR(100),'
        #     'pain VARCHAR(100),'
        #     'photo VARCHAR(100),'
        #     'phone VARCHAR(100),'
        #     'indx VARCHAR(100),'
        #     'indy VARCHAR(100),'
        #     'ind1 INTEGER default 0,'
        #     'ind2 INTEGER default 0,'
        #     'ind3 INTEGER default 0,'
        #     'created_at DATE not null default current_date,'
        #     'last_activity timestamp not null default current_timestamp,'
        #     ');'
        # )
        # connection.commit()
        #
        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS all_admin'
        #     '(id SERIAL PRIMARY KEY,'
        #     'name VARCHAR(100),'
        #     'chat_id INTEGER,'
        #     'indx VARCHAR(100),'
        #     'indy VARCHAR(100),'
        #     'ind1 VARCHAR(100),'
        #     'ind2 VARCHAR(100),'
        #     'ind3 VARCHAR(100)'
        #     ');'
        # )
        # connection.commit()
        print(26)

except Exception as _ex:
    pass

finally:
    if connection:
        connection.close()
        # print('[INFO] PostgreSQL closed')

