#!/usr/bin/env python3
# import argparse
import random

from telebot import apihelper

from config import bot
from helpers import yt_link_check
from meta import Answers, States
from audio import TgAudio
from server import serv_start
from sqlworker import (alt_bool, check_state, get_user, listener,
                       register_dude, set_column)

apihelper.proxy = {'https':'socks5://127.0.0.1:8123'}

# parser = argparse.ArgumentParser()
# parser.add_argument("-t", help="run without server, using different creds")
# args = parser.parse_args()

bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def start(m):
    user = get_user(m.chat.id)

    if not user:
        bot.send_message(m.chat.id, Answers.start)
        register_dude(m)
        return

    state = user.curr_state

    if state == States.start:
        bot.send_message(m.chat.id, 'Старт уже запущен был')

    elif state == States.asking_for_stuff:
        bot.send_message(m.chat.id, 'whops')

    elif state == States.asking_bass_pwr:
        bot.send_voice(m.chat.id, Answers.hm)

@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, Answers.reset)
    set_column(message.chat.id, state=States.start)

@bot.message_handler(commands=["transform", "random"])
def change_transform_state(m):
    user = get_user(m.chat.id)

    if not user:
        register_dude(m)
        user = get_user(m.chat.id)

    if m.text == '/transform':
        state = alt_bool(m.chat.id, transform=True)
        service = Answers.random_tags

    elif m.text == '/random':
        state = alt_bool(m.chat.id, random=True)
        service = Answers.random_bass

    if state:
        action = Answers.turn_on
    else:
        action = Answers.turn_off

    bot.send_message(m.chat.id, f"{action} {service}")

@bot.message_handler(commands=["delete"])
def delete_user(m):
    del m

@bot.message_handler(commands=["info"])
def user_man(message):
    bot.send_message(message.chat.id, Answers.info)

@bot.message_handler(func=lambda m: check_state(m.chat.id, States.start))
def cmd_reset(message):
    bot.send_message(message.chat.id, Answers.after_start)
    set_column(message.chat.id, States.asking_for_stuff)

@bot.message_handler(content_types=['audio', 'voice'])
def get_audio(m):
    """
    React on sended audio or voice
    """
    user = get_user(m.chat.id)
    bot.send_message(m.chat.id, Answers.got_it)
    try:
        audio = TgAudio.from_message(m)
    except:
        bot.send_audio(m.chat.id, Answers.too_much)

    if audio.content_type == 'audio':
        audio.transform_eyed3 = user.transform_eyed3

    if user.random_bass:
        random_power = random.randint(5, 10) #nosec
        bot.send_message(m.chat.id, f'пилю бас, сила: {random_power}')
        audio.bass_boost(random_power) # nosec
        bot.send_audio(m.chat.id, audio.open_bass())

    else:
        bot.send_message(m.chat.id, Answers.num_range)

    set_column(m.chat.id,
               state=States.asking_bass_pwr,
               last_src=audio.src_path)

# @bot.message_handler(content_types=['voice'])
# def get_voice(m):
#     
#     user = get_user(m.chat.id)
#     try:
#         voice = TgAudio.from_message(m)
#     except: # TODO tgapiexception вроде
#         bot.send_message(m.chat.id, Answers.too_much)

#     if user.random_bass:
#         random_power = random.randint(20, 21) # nosec
#         voice.bass_boost(random_power)
#         bot.send_message(m.chat.id, f'Сила: {random_power}')
#         bot.send_voice(m.chat.id, voice.open_bass())

#     else:
#         bot.send_message(m.chat.id, Answers.how_many)
#         set_column(m.chat.id, state=States.asking_bass_pwr)

@bot.message_handler(func=lambda m: check_state(m.chat.id, States.asking_bass_pwr))
def asking_for_bass_v(m):
    user = get_user(m.chat.id)
    if not m.text.isdigit():
        bot.send_message(m.chat.id, Answers.numbers_needed)

    elif int(m.text) < 1 or int(m.text) > 100:
        bot.send_message(m.chat.id, Answers.num_range)

    else:
        audio = TgAudio.from_local(m)
        audio.transform_eyed3 = user.transform_eyed3
        audio.bass_boost(int(m.text))
        if audio.content_type == 'audio':
            bot.send_audio(m.chat.id, audio.open_bass())
        else:
            bot.send_voice(m.chat.id, audio.open_bass)

# @bot.message_handler(func=lambda message: sqlworker.get_current_state(message.chat.id) == States.ASKING_FOR_BASS_POWER_AUDIO)
# def asking_for_bass_a(message):# Не DRY, Стыдно...
#     mcfn = './stuff/' + str(message.chat.id)

#     if not message.text.isdigit():
#         bot.send_message(message.chat.id, 'Цифра нужна, братан')
#         return

#     elif int(message.text) < 1 or int(message.text) > 100:
#         bot.send_message(message.chat.id, 'От 1 до 100, братан')

#     else:
#         convert_to(mcfn + '_audio',mcfn + '_audio.mp3')

#         tags = eyed3.load(mcfn + '_audio.mp3') #Смотрю че там по исходным id3 тэгам
#         convert_to(mcfn + '_audio',mcfn + '_dwnld.wav')

#         bass(message.text, mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
#         convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')

#         if sqlworker.is_transform(message.chat.id):
#             transform_tag(tags, mcfn + '_send.mp3')

#         audio = open(mcfn + '_send.mp3', 'rb')
#         bot.send_audio(message.chat.id, audio)
#         sqlworker.set_state(message.chat.id, States.ASKING_FOR_DOWNLOAD)

@bot.message_handler(content_types=['text'])
def answer_with_info(message):
    this_is_yt_link = yt_link_check(message.text)
    if this_is_yt_link:
        bot.send_message(message.chat.id, 'yt_link detec')
        return
    bot.send_message(message.chat.id, Answers.got_text)

bot.polling(none_stop=True)
# serv_start(bot)
