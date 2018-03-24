from vedis import Vedis
import config
import telebot as tb
import config

bot = tb.TeleBot(config.token)

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id,message):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError:  # Если такого ключа почему-то не оказалось
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
