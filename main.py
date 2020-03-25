#!/usr/bin/env python3
import argparse
from datetime import datetime
from random import randint

import cherrypy
import eyed3
import telebot as tb
from pysndfx import AudioEffectsChain as af
from telebot import apihelper

import config2 as config
import sqlworker
import tekst
from helpers import (Answers, States, check_asking, convert_to, download_video,
                     user_started, download_file, listener, Audio)

apihelper.proxy = {'https':'socks5://127.0.0.1:5555'}

LOG_FILE = 'log.txt'

answer = Answers
parser = argparse.ArgumentParser()
parser.add_argument("-t", help="run without server, using different creds")
args = parser.parse_args()

bot = tb.TeleBot(config.token)
bot.set_update_listener(listener)

# REWRITE TO CONFIG
# if args.t:
#     import config2 as config
# else:
#     import config
#     WEBHOOK_HOST = '178.32.56.221'
#     WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
#     WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

#     WEBHOOK_SSL_CERT = './webhook_cert.pem' # Путь к сертификату
#     WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

#     WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
#     WEBHOOK_URL_PATH = "/%s/" % (config.token)

def transform_tag(tags, final_name):
    sartist = tekst.transform(tags.tag.artist)
    stitle = tekst.transform(tags.tag.title)
    fille = eyed3.load(final_name)# ставлю свои тэги
    fille.tag.artist = sartist
    fille.tag.title = stitle
    fille.tag.save()

def bass(how_many, inn, outt):
    apply_af = af().lowshelf(how_many)
    apply_af(inn, outt)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = tb.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=['start'])
def start(message):
    state = sqlworker.get_current_state(message.chat.id)

    if state == States.ASKING_FOR_DOWNLOAD:
        bot.send_message(message.chat.id, Answers.started_already)

    elif state == States.GOT_AUDIO:
        bot.send_message(message.chat.id, Answers.shit_happend)

    elif state == States.GOT_VOICE:
        bot.send_message(message.chat.id, Answers.shit_happend)

    elif state == States.ASKING_FOR_BASS_POWER_AUDIO:
        bot.send_voice(message.chat.id, Answers.hm)

    else:
        bot.send_message(message.chat.id, Answers.start)
        sqlworker.register_dude(message)

@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, Answers.reset)
    sqlworker.reset_dude(message.chat.id)

@bot.message_handler(commands=["random"])
def change_random_state(message):
    if sqlworker.is_random(message.chat.id):
        bot.send_message(message.chat.id,
                         f'{Answers.turn_off} {Answers.random_bass}')

        sqlworker.set_random(message.chat.id, 0)

    else:
        bot.send_message(message.chat.id,
                         f"{Answers.turn_on} {Answers.random_bass}")
        sqlworker.set_random(message.chat.id, 1)

@bot.message_handler(commands=["transform"])
def change_transform_state(message):
    if sqlworker.is_transform(message.chat.id):
        bot.send_message(message.chat.id,
                         f"{Answers.turn_off} {Answers.random_tags}")
        sqlworker.set_transform(message.chat.id, 0)

    else:
        bot.send_message(message.chat.id,
                         f'{Answers.turn_on} {Answers.random_tags}')
        sqlworker.set_transform(message.chat.id, 1)


@bot.message_handler(commands=["info"])
def user_man(message):
    bot.send_message(message.chat.id, Answers.info)


@bot.message_handler(func=lambda m: sqlworker.get_current_state(m.chat.id) == States.START) # пиздеец
def cmd_reset(message):
    bot.send_message(message.chat.id, Answers.after_start)
    sqlworker.set_state(message.chat.id, States.ASKING_FOR_DOWNLOAD)


@bot.message_handler(content_types=['audio'])
def get_audio(message):
    mcfn = f'{config.download_path}{str(message.chat.id)}'
    bot.send_message(message.chat.id, Answers.got_it)
    audio = Audio(message.audio)
    if download_file(bot, message, mcfn + '_audio'):

        if sqlworker.is_random(message.chat.id):
            tags = eyed3.load(mcfn + '_audio.mp3')
            convert_to(mcfn + '_audio', mcfn + '_dwnld.wav')
            bass(randint(25, 100), mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
            convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')

            if sqlworker.is_transform(message.chat.id):
                transform_tag(tags, mcfn + '_send.mp3')

            else:
                tags_send = eyed3.load(mcfn + '_send.mp3')
                tags_send.tag.artist = tags.tag.artist
                tags_send.tag.title = tags.tag.title
                tags_send.tag.save()
            audio = open(mcfn + '_send.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)

        else:
            bot.send_message(message.chat.id, Answers.num_range)
            sqlworker.set_state(message.chat.id, States.ASKING_FOR_BASS_POWER_AUDIO)
    else:
        bot.send_message(message.chat.id, Answers.too_much)

@bot.message_handler(content_types=['voice'])
def get_voice(message):
    mcfn = './stuff/' + str(message.chat.id)
    bot.send_message(message.chat.id, Answers.got_it)
    if download_file(bot, message, f"{mcfn}_voice.ogg"):
        convert_to(mcfn + '_voice.ogg', mcfn + '_voice.wav')
        
        if sqlworker.is_random(message.chat.id):
            bass(randint(25,100), mcfn + '_voice.wav', mcfn + '_voiceb.wav')
            convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
            voice = open(mcfn + '_send.ogg', 'rb')
            bot.send_voice(message.chat.id, voice)

        else:
            bot.send_message(message.chat.id, 'Скок басу? 1-100')
            sqlworker.set_state(message.chat.id, States.ASKING_FOR_BASS_POWER_VOICE)
    else:
        bot.send_message(message.chat.id, Answers.too_much)



@bot.message_handler(func=lambda m: sqlworker.get_current_state(m.chat.id) == States.ASKING_FOR_BASS_POWER_VOICE)
def asking_for_bass_v(message):
    mcfn = './stuff/' + str(message.chat.id)

    if not message.text.isdigit():
        bot.send_message(message.chat.id, Answers.numbers_needed)

    elif int(message.text) < 1 or int(message.text) > 100:
        bot.send_message(message.chat.id, Answers.num_range)

    else:
        bass(message.text, mcfn + '_voice.wav', mcfn + '_voiceb.wav')
        convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
        voice = open(mcfn + '_send.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
        sqlworker.set_state(message.chat.id, States.ASKING_FOR_DOWNLOAD)


@bot.message_handler(func=lambda message: sqlworker.get_current_state(message.chat.id) == States.ASKING_FOR_BASS_POWER_AUDIO)
def asking_for_bass_a(message):# Не DRY, Стыдно...
    mcfn = './stuff/' + str(message.chat.id)

    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Цифра нужна, братан')
        return

    elif int(message.text) < 1 or int(message.text) > 100:
        bot.send_message(message.chat.id, 'От 1 до 100, братан')

    else:
        convert_to(mcfn + '_audio',mcfn + '_audio.mp3')

        tags = eyed3.load(mcfn + '_audio.mp3') #Смотрю че там по исходным id3 тэгам
        convert_to(mcfn + '_audio',mcfn + '_dwnld.wav')

        bass(message.text, mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
        convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')

        if sqlworker.is_transform(message.chat.id):
            transform_tag(tags, mcfn + '_send.mp3')

        audio = open(mcfn + '_send.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        sqlworker.set_state(message.chat.id, States.ASKING_FOR_DOWNLOAD)

@bot.message_handler(content_types=['text'])
def answer_with_info(message):
    bot.send_message(message.chat.id, answer.got_text)

bot.polling()

# else:
#     cherrypy.config.update({'server.socket_host': WEBHOOK_LISTEN,
#                             'server.socket_port': WEBHOOK_PORT,
#                             'server.ssl_module': 'builtin',
#                             'server.ssl_certificate': WEBHOOK_SSL_CERT,
#                             'server.ssl_private_key': WEBHOOK_SSL_PRIV})

#     bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                     certificate=open(WEBHOOK_SSL_CERT, 'r'))

#     cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
