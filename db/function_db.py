import psycopg2

from data.config import *




#***********************************АДМИНКА********************************************


async def verify_admin(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM all_admin WHERE chat_id = '{id}';")
        a = cur.fetchall()
        return a


async def select_admin():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM all_admin;")
        a = cur.fetchall()
        return a


async def make_admin(name, chat_id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"INSERT INTO all_admin (name, chat_id) VALUES ('{name}', '{chat_id}');")
        connection.commit()


async def delete_admin (id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    if id != 1087882216:
        with connection.cursor() as cur:
            cur.execute(
                    f"DELETE FROM all_admin WHERE chat_id = '{id}';")
            connection.commit()



# Жалобы на профиль
async def check_claims(selected):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    try:
        with connection.cursor() as cur:
            cur.execute(f"SELECT * FROM check_claim LIMIT 50;")
            a = cur.fetchall()
            if len(a) == 0:
                return 'empty'
            return a[selected]
    except:
        return 'empty'

async def insert_claims(text, quilty, noquilty):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f" INSERT INTO check_claim (problem, quilty, not_quilty) VALUES ('{text}', '{quilty}', '{noquilty}');")
        connection.commit()


async def delete_claims (id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(
                f"DELETE FROM check_claim WHERE quilty = '{id}';")
        connection.commit()



# Общие жалобы-пожелания
async def insert_wishes(message, chat_id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(
            f" INSERT INTO wishes (message, chat_id) VALUES ('{message}', {chat_id});")
        connection.commit()

async def check_wishes(selected):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    try:
        with connection.cursor() as cur:
            cur.execute(
                f"SELECT * FROM wishes LIMIT 50;")
            a = cur.fetchall()
            return a[selected]
    except:
        return 'empty'


async def delete_wishes(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(
            f"DELETE FROM wishes WHERE id = {id};")
        connection.commit()


# Остальные функции
async def collect_statistic():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(
            f"SELECT * FROM statistic WHERE id = 1;")
        a = cur.fetchall()
        cur.execute("SELECT * FROM check_claim;")
        b = cur.fetchall()
        cur.execute("SELECT * FROM wishes;")
        c = cur.fetchall()
        text = [
            'СТАТИСТИКА\n',
            f'👤 Общее кол-во пользователей: {a[0][1]}\n',
            f'😴 Кол-во спящих пользователей: {a[0][2]}\n',
            f'❌ Жалоб на анкеты: {len(b)}\n',
            f'⚠️Общие жалобы пожелания: {len(c)}'
        ]
        return text


async def delete_block_user (some, id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        if some == 'delete':
            cur.execute(
                f"DELETE FROM main_profil WHERE indx = '{id}';")
            cur.execute(f"DELETE FROM check_claim WHERE quilty = '{id}';")
            cur.execute(f"DELETE FROM wishes WHERE chat_id = '{id}';")
            connection.commit()
        elif some == 'block':
            # cur.execute(
            #     f"DELETE FROM main_profil WHERE indx = '{id}';")
            cur.execute(
                f"DELETE FROM check_claim WHERE quilty = '{id}';")
            cur.execute(
                    f"UPDATE main_profil SET ind4 = False WHERE indx = '{id}';")
            cur.execute(
                f"INSERT INTO blocked_users (chat_id) VALUES ('{id}');")
            connection.commit()
        elif some == 'unblock':
            cur.execute(
                f"DELETE FROM blocked_users WHERE chat_id = '{id}';")
            cur.execute(
                f"UPDATE main_profil SET ind4 = True WHERE indx = '{id}';")
            connection.commit()


async def activate_users():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(
            f"UPDATE main_profil SET ind4 = true, stop_searching = null WHERE now() - stop_searching > INTERVAL '15 DAY' ;")
        cur.execute('UPDATE statistic SET sleep_user = 0 WHERE id = 1')
        connection.commit()


async def admin_default(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"UPDATE main_profil SET ind1 = 0, ind2 = 0 WHERE indx = '{id}';")
        connection.commit()



# ********************************ПОИСК_ПРОФИЛЕЙ**************************88


async def send_profil(id):

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

        cur.execute(f"UPDATE main_profil SET last_activity = now() WHERE indx = '{id}'")
        connection.commit()
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
        b = ',\n'
        cur.execute(f"UPDATE main_profil SET {table} = '{a[0][0]}{b}{value}' WHERE indx = '{id}';")
        connection.commit()


async def send_search_db(id, disease, index_of_search):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    selected = []
    list_already_added = ('some', f'{id}',)
    bots_chat_id = ['1087882216']
    with connection.cursor() as cur:
        for item in disease:
            cur.execute(f"SELECT * FROM main_profil WHERE disease LIKE '%{item}%' AND indx NOT IN {list_already_added} AND ind4 = TRUE "
                        f"ORDER BY last_activity DESC LIMIT 200;")
            a = cur.fetchall()

            for i in a:
                selected.append(i)
                if i[11] not in bots_chat_id:
                    list_already_added = list_already_added + (f'{i[11]}',)

        if len(selected) - int(index_of_search) <= 1:
            cur.execute(f"UPDATE main_profil SET ind1 = '{int(index_of_search) + 1}', ind2 = '{len(selected)}', ind3 = 1 WHERE indx = '{id}';")
            connection.commit()
        else:
            cur.execute(f"UPDATE main_profil SET ind1 = '{int(index_of_search) + 1}', ind2 = '{len(selected)}' WHERE indx = '{id}';")
            connection.commit()

        return selected[int(index_of_search)]


async def reset_search(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"UPDATE main_profil SET ind1 = '0', ind3 = '0' WHERE indx = '{id}';")
        connection.commit()


async def stop_searching(happen, id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    if happen == True:
        with connection.cursor() as cur:
            cur.execute(f"UPDATE main_profil SET ind4 = true, stop_searching = null WHERE indx = '{id}'")
            cur.execute('UPDATE statistic SET sleep_user = sleep_user - 1 WHERE id = 1')
            connection.commit()
    else:
        with connection.cursor() as cur:
            cur.execute(f"UPDATE main_profil SET ind4 = {happen}, stop_searching = now() WHERE indx = '{id}'")
            cur.execute('UPDATE statistic SET sleep_user = sleep_user + 1 WHERE id = 1')
            connection.commit()


async def update_activity(id):

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()

    with connection.cursor() as cur:
        cur.execute(f"UPDATE main_profil SET last_activity = now() WHERE indx = '{id}'")
        connection.commit()





# ********************************ОСТАЛЬНОЕ**********************************

async def send_db_sick(table):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        global v
        v = cur.execute(f"SELECT * FROM sick_f WHERE ind1 = '{table}' ORDER BY ind2;")
        a = cur.fetchall()
        return a


async def verify_user(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM main_profil WHERE indx = '{id}';")
        already_registered = cur.fetchall()

        cur.execute(f"SELECT * FROM blocked_users WHERE chat_id = '{id}';")
        blocked = cur.fetchall()

        # bots = ['1087882216']

        if blocked:
            return 'blocked'
        elif already_registered:
            # if already_registered[0][11] in bots:
            #     return True
            return 'already_registered'
        else:
            return True

async def insert_login_web(chat_id, passw, phone):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    with connection.cursor() as cur:
        cur.execute(f"INSERT INTO login_web (chat_id, passw, phone) VALUES ('{chat_id}', '{passw}', '{phone}');")
        connection.commit()
