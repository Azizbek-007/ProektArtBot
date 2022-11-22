from sqlite3 import Error
import sqlite3
from time import ctime
from xlsxwriter.workbook import Workbook

def post_sql_query(sql_query):
    with sqlite3.connect('my.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        phone TEXT,
                        reg_date TEXT);'''

    post_sql_query(users_query)
create_tables()

def create_category_name():
    sql = '''CREATE TABLE "menu" (
	"id"	INTEGER,
	"name"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    post_sql_query(sql)
create_category_name()

def create_messages_tabel():
    sql = '''CREATE TABLE "messages" (
	"id"	INTEGER,
	"category_id"	INTEGER NOT NULL,
	"text"	TEXT,
	"photo"	TEXT
);'''
    post_sql_query(sql)
create_messages_tabel()

def create_category_tabele():
    sql = '''CREATE TABLE "category" (
	"id"	INTEGER,
	"menu_id"	INTEGER NOT NULL,
	"name"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    post_sql_query(sql)

create_category_name()

def register_user(user, username, first_name, last_name):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ' \
                             f'({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
        post_sql_query(insert_to_db_query)

def get_phone_number(user_id):
    user = f'select phone from USERS where user_id = {user_id};'
    result = post_sql_query(user)[0][0]
    if result == None: return False
    return True

def update_phone_number(user_id, phone_number):
    sql = f"update USERS set phone='{phone_number}' where user_id={user_id}"
    post_sql_query(sql)

def get_users():
    sql = "select * from USERS"
    result = post_sql_query(sql)
    return result

def menu():
    sql = "select * from menu"
    result = post_sql_query(sql)
    return result

def by_menu(name):
    sql = f"select * from menu where name='{name}'"
    result = post_sql_query(sql)
    return result

def get_xls():
    workbook = Workbook('users.xlsx')
    worksheet = workbook.add_worksheet()

    conn=sqlite3.connect('my.db')
    c=conn.cursor()
    c.execute("select * from USERS")
    mysel=c.execute("select * from USERS")
    f1=workbook.add_format({'bold':True, 'border':1, 'border_color': 'black', 'align':'center'})
    f2=workbook.add_format({'border':1, 'border_color':'black', 'align':'center'})
    worksheet.write_row('A1', ['user_id', 'username', 'firstname', 'lastname', 'phone', 'created_at'], f1)
    for i, row in enumerate(mysel):
        i+=1
        worksheet.write(i, 0, row[0], f2)
        worksheet.write(i, 1, row[1], f2)
        worksheet.write(i, 2, row[2], f2)
        worksheet.write(i, 3, row[3], f2)
        worksheet.write(i, 4, row[4], f2)
        worksheet.write(i, 5, row[5], f2)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('A:A', 12)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 25)
    workbook.close()

get_xls()
def get_user(user_id):
    sql = f"select * from USERS where user_id='{user_id}'"
    result = post_sql_query(sql)
    return result

def users_count():
    sql = "SELECT count(*) from USERS;"
    result = post_sql_query(sql)
    return result

def get_category(name):
    sql = f'select * from category where name="{name}"'
    result = post_sql_query(sql)
    return result

def get_message(cate_id):
    sql = f'select * from messages where category_id={cate_id}'
    result = post_sql_query(sql)
    print(result)
    return result

def by_message(id):
    sql = f"select * from messages where id={id}"
    result = post_sql_query(sql)
    return result

def delete_message(id):
    sql = f'DELETE FROM messages WHERE id={id};'
    post_sql_query(sql)

def delete_category(id):
    sql = f'DELETE FROM category WHERE id={id};'
    post_sql_query(sql)

def create_category(menu_id, text):
    sql = f'INSERT INTO category (menu_id, name) VALUES ' \
                             f'({menu_id}, "{text}");'
    post_sql_query(sql)

def menu_in_menu(menu_id):
    sql = f"select * from category where menu_id={menu_id}"
    result = post_sql_query(sql)
    return result

def create_message(category_id, text, photo):
    sql = f'INSERT INTO messages (category_id, text, photo) VALUES ' \
                             f'({category_id}, "{text}", "{photo}");'
    post_sql_query(sql)