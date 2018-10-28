#!/usr/bin/python3
import config #bleh
import sqlite3
import telebot as tb
from datetime import datetime

bot = tb.TeleBot(config.token)
conn = sqlite3.connect('./stuff/db.sql')
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM boys")
except sqlite3.OperationalError:
    cursor.execute("""CREATE TABLE boys
          (id integer, username text, first_name text, state text,
          is_random integer, is_transform integer, last_date text, first_date text)
           """)
    conn.commit()
    bot.send_message(config.karaz159, 'there was some error with db, created new') # is there any other way to keep me in touch about this?
conn.close()

def show_db():
    boys = []
    try:
        for row in cursor.execute("SELECT username FROM boys"):
            boys += row
        return boys
    except sqlite3.OperationalError:
        return "some error accured"


def register_dude(message):
    print("registring")
    curr_time = datetime.now().strftime("%I:%M%p on %B %d, %Y")
    REGISTER_VALUES = (str(message.chat.id), message.chat.username, message.chat.first_name, '0', '0', '1', curr_time, curr_time)
    sql = ''' INSERT INTO BOYS VALUES (?,?,?,?,?,?,?,?)'''
    print(REGISTER_VALUES)
    conn = sqlite3.connect('./stuff/db.sql')
    cursor = conn.cursor()
    cursor.execute(sql, REGISTER_VALUES)
    conn.commit()
    #cursor.executemany("INSERT INTO boys VALUES (?,?,?,?,?,?,?,?)", REGISTER_VALUES)
    conn.close()

def get_current_state(user_id): #sqlite3 variant
    #print('showing current state')
    conn = sqlite3.connect('./stuff/db.sql')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT state FROM boys WHERE id = " + str(user_id))
        return cursor.fetchone()[0]
    except (IndexError, TypeError): # Если такого ключа почему-то не оказалось
        return "nope"
    conn.close()## Пытаемся узнать из базы «состояние» пользователя

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    conn = sqlite3.connect('./stuff/db.sql')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE boys SET state = " + value + " WHERE id = " + str(user_id))
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print('something went wrong')
        #тут желательно как-то обработать ситуацию
        return False
    conn.close()

def is_random(user_id):
    try:
        conn = sqlite3.connect('./stuff/db.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT is_random FROM boys WHERE id = " + str(user_id))
        return cursor.fetchone()[0]
    except sqlite3.OperationalError:
        print('something went wrong')
        #тут желательно как-то обработать ситуацию
        return False
    conn.close()

def set_random(user_id, value):
    try:
        conn = sqlite3.connect('./stuff/db.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE boys SET is_random = " + str(value) + " WHERE id = " + str(user_id))
        conn.commit()
    except sqlite3.OperationalError:
        print('something went wrong')
        #тут желательно как-то обработать ситуацию
    conn.close()

def is_transform(user_id):
    try:
        conn = sqlite3.connect('./stuff/db.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT is_transform FROM boys WHERE id = " + str(user_id))
        return cursor.fetchone()[0]
    except sqlite3.OperationalError:
        print('something went wrong')
        #тут желательно как-то обработать ситуацию
        return False
    conn.close()

def set_transform(user_id, value):
    try:
        conn = sqlite3.connect('./stuff/db.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE boys SET is_transform = " + str(value) + " WHERE id = " + str(user_id))
        conn.commit()
    except sqlite3.OperationalError:
        print('something went wrong')
        #тут желательно как-то обработать ситуацию
    conn.close()
