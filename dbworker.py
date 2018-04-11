from vedis import Vedis
import config, pickle
import telebot as tb

bot = tb.TeleBot(config.token)

def conservate(user):
    db = open('./stuff/users.dat', 'wb+')
    users = pickle.load(db)
    users.append(user)
    pickle.dump(users, db)
    db.close()

def users_base():
    try:
        db = open('./stuff/users.dat', 'rb')
        users = pickle.load(db)
        db.close()
        return users

    except FileNotFoundError:
        bot.send_message(config.karaz159, 'DATABASE NOT FOUND BOUYSSSSS', disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None)
        return config.karaz159
# Пытаемся узнать из базы «состояние» пользователя
=======
def get_current_state(message):
    with Vedis(config.db_file) as db:
        try:
            return db[message.chat.id]
        except KeyError:  # Если такого ключа почему-то не оказалось
            bot.forward_message(config.karaz159, message.chat.id, message.message_id)
            conservate(message.chat.id)
            bot.forward_message(config.karaz159, message.chat.id, message.message_id)
            return config.States.S_START.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            print('something went wrong')
            #тут желательно как-то обработать ситуацию
            return False
