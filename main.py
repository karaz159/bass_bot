#!/usr/bin/env python3
import argparse

import telebot as tb
from telebot import apihelper

from config import TOKEN
from helpers import transform_eyed3, yt_link_check
from meta import Answers, States, TgAudio
from server import serv_start
from sqlworker import check_state, get_user, register_dude, set_bool, set_state

apihelper.proxy = {'https':'socks5://127.0.0.1:8123'}

answer = Answers
parser = argparse.ArgumentParser()
parser.add_argument("-t", help="run without server, using different creds")
args = parser.parse_args()

def listener(m):
    pass

bot = tb.TeleBot(TOKEN)
bot.set_update_listener(listener)
# bot.set_update_listener() # LOGGER

def transform_tag(tags, final_name):
    sartist = transform_eyed3(tags.tag.artist)
    stitle = transform_eyed3(tags.tag.title)
    fille = eyed3.load(final_name)# ставлю свои тэги
    fille.tag.artist = sartist
    fille.tag.title = stitle
    fille.tag.save()



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
        bot.send_message(m.chat.id, Answers.started_already)

    elif state == States.got_audio:
        bot.send_message(m.chat.id, Answers.shit_happend)

    elif state == States.got_voice:
        bot.send_message(m.chat.id, Answers.shit_happend)

    elif state == States.asking_bass_pwr_mp3:
        bot.send_voice(m.chat.id, Answers.hm)

@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, Answers.reset)
    set_state(message.chat.id, States.start)

@bot.message_handler(commands=["transform", "random"]) # TODO Такое, мб есть другой метод?
def change_transform_state(m):
    user = get_user(m.chat.id)

    if not user:
        register_dude(m)
        user = get_user(m.chat.id)

    if m.text == '/transform':
        state = set_bool(m.chat.id, 'transform')
        service = Answers.random_tags

    elif m.text == '/random':
        state = set_bool(m.chat.id, 'random')
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

@bot.message_handler(func=lambda m: check_state(m, States.start))
def cmd_reset(message):
    bot.send_message(message.chat.id, Answers.after_start)
    set_state(message.chat.id, States.asking_for_stuff)

@bot.message_handler(content_types=['audio'])
def get_audio(m):
    user = get_user(m.chat.id)
    audio = TgAudio(bot, m)

    if user.transform:
        audio.transform_eyed3()

    if user.random:
        audio.bass_boost(random_pwr=True)
        bot.send_audio(m.chat.id, audio.open_bass())
# def get_audio(message):
#     mcfn = f'{config.download_path}{str(message.chat.id)}'
#     bot.send_message(message.chat.id, Answers.got_it)
#     audio = Audio(message.audio)
#     if download_file(bot, message, mcfn + '_audio'):

#         if sqlworker.is_random(message.chat.id):
#             tags = eyed3.load(mcfn + '_audio.mp3')
#             convert_to(mcfn + '_audio', mcfn + '_dwnld.wav')
#             bass(randint(25, 100), mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
#             convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')

#             if sqlworker.is_transform(message.chat.id):
#                 transform_tag(tags, mcfn + '_send.mp3')

#             else:
#                 tags_send = eyed3.load(mcfn + '_send.mp3')
#                 tags_send.tag.artist = tags.tag.artist
#                 tags_send.tag.title = tags.tag.title
#                 tags_send.tag.save()
#             audio = open(mcfn + '_send.mp3', 'rb')
#             bot.send_audio(message.chat.id, audio)

#         else:
#             bot.send_message(message.chat.id, Answers.num_range)
#             sqlworker.set_state(message.chat.id, States.ASKING_FOR_BASS_POWER_AUDIO)
#     else:
#         bot.send_message(message.chat.id, Answers.too_much)

# @bot.message_handler(content_types=['voice'])
# def get_voice(message):
#     mcfn = './stuff/' + str(message.chat.id)
#     bot.send_message(message.chat.id, Answers.got_it)
#     if download_file(bot, message, f"{mcfn}_voice.ogg"):
#         convert_to(mcfn + '_voice.ogg', mcfn + '_voice.wav')

#         if sqlworker.is_random(message.chat.id):
#             bass(randint(25,100), mcfn + '_voice.wav', mcfn + '_voiceb.wav')
#             convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
#             voice = open(mcfn + '_send.ogg', 'rb')
#             bot.send_voice(message.chat.id, voice)

#         else:
#             bot.send_message(message.chat.id, 'Скок басу? 1-100')
#             sqlworker.set_state(message.chat.id, States.ASKING_FOR_BASS_POWER_VOICE)
#     else:
#         bot.send_message(message.chat.id, Answers.too_much)



# @bot.message_handler(func=lambda m: sqlworker.get_current_state(m.chat.id) == States.ASKING_FOR_BASS_POWER_VOICE)
# def asking_for_bass_v(message):
#     mcfn = './stuff/' + str(message.chat.id)

#     if not message.text.isdigit():
#         bot.send_message(message.chat.id, Answers.numbers_needed)

#     elif int(message.text) < 1 or int(message.text) > 100:
#         bot.send_message(message.chat.id, Answers.num_range)

#     else:
#         bass(message.text, mcfn + '_voice.wav', mcfn + '_voiceb.wav')
#         convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
#         voice = open(mcfn + '_send.ogg', 'rb')
#         bot.send_voice(message.chat.id, voice)
#         sqlworker.set_state(message.chat.id, States.ASKING_FOR_DOWNLOAD)


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
    bot.send_message(message.chat.id, answer.got_text)

bot.polling()
# serv_start(bot)
