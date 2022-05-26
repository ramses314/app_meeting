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
            'ind1 VARCHAR(100),'
            'ind2 VARCHAR(100),'
            'ind3 VARCHAR(100)'
            ');'
        )
        connection.commit()

except Exception as _ex:
    print(['kmlmmlm'], _ex)

finally:
    pass
    if connection:
        connection.close()
        print('[INFO] PostgreSQL closed')


async def send_db_sick(table):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()
        with connection.cursor() as cur:
            global v
            v = cur.execute(f'SELECT * FROM sick_{table};')
            return cur.fetchall()

    except Exception as _ex:
        print(['kmlmmlm'], _ex)

    finally:
        pass

    return cur.fetchall()



async def send_profil(id):
    # try:
    #     connection = psycopg2.connect(
    #         host=host,
    #         user=user,
    #         password=password,
    #         database=db_name
    #     )
    #
    #     cursor = connection.cursor()
    #     with connection.cursor() as cur:
    #         global v
    #         v = cur.execute(f'SELECT * FROM main_profil WHERE indx = "{id}";')
    #         return cur.fetchall()
    #
    # except Exception as _ex:
    #     print(['kmlmmlm'], _ex)
    #
    # finally:
    #     pass
    # # a = cur.fetchall()
    # # print(a, cur.fetchall())
    # return cur.fetchall()

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()

    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM main_profil WHERE indx = '{id}';")
        a = cur.fetchall()
        return a



async def update_profil(table, value, id):

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    cursor = connection.cursor()

    with connection.cursor() as cur:
        cur.execute(
            f"UPDATE main_profil SET {table} = '{value}' WHERE indx = '{id}';"
        )
        connection.commit()

async def update_profil_add(table, value, id):

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    cursor = connection.cursor()



    with connection.cursor() as cur:
        cur.execute(f"SELECT disease FROM main_profil WHERE indx = '{id}';")
        a = cur.fetchall()
        print(2222, a, 4444, cur.fetchall)
        b = ',\n'
        cur.execute(f"UPDATE main_profil SET {table} = '{a[0][0]}{b}{value}' WHERE indx = '{id}';")
        connection.commit()


async def send_search_db(id, disease):

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()

    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM main_profil WHERE disease IN {tuple(disease)};")
        a = cur.fetchall()
        return a