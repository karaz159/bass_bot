#!/usr/bin/env python3
from pysndfx import AudioEffectsChain as af
import telebot as tb
from datetime import datetime
from os import system as sys
from os import remove as rm
from time import sleep
import dbworker, config, tekst, eyed3, cherrypy
from random import randint
from config import token as TOKEN
#необходимо добавить пакет sysargv для тест режима

def bass(inn,outt):
    apply_af = af().lowshelf(randint(25,100))
    apply_af(inn, outt)
    print ('BASS done')

def write_log(log):
    time = datetime.now()
    a_time = ('[' + str(time.day) + '.' + str(time.month) + '.' + str(time.year) + ' ' + str(time.hour) + ':' + str(time.minute) + '] ')
    TF = open('log.txt', 'a', encoding = 'utf-8')
    TF.write(a_time + log + '\n')
    TF.close()

def listener(messages):#достаточно полезная вещь, можно использовать как лог
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            write_log(str(m.chat.first_name) + " (" + str(m.chat.id) + "): " + m.text)

        elif m.content_type == 'audio':
            write_log(str(m.chat.first_name) + ' ('+ str(m.chat.id) + ') '+ 'sended audio')

        elif m.content_type == 'voice':
            write_log(str(m.chat.first_name) + ' ('+ str(m.chat.id) + ') '+ 'sended voice')

def download_file(message, name):
    mcfn = './stuff/' + str(message.chat.first_name)
    try:
        if message.content_type == 'audio':
            file_info = bot.get_file(message.audio.file_id)

        elif message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(name, 'wb') as new_file: #необходимо получить имя файла
            new_file.write(downloaded_file)

        return True

    except tb.apihelper.ApiException:
        return False

def convert_to(inn, out):
    sys('ffmpeg -y -loglevel quiet -i '+ inn + ' ' + out) #Конвертирую inn в ваф файл для дальнейшей работы

###########################################################################################################
bot = tb.TeleBot(TOKEN)
bot.set_update_listener(listener)
hm = open('voice.ogg', 'rb')
###########################################################################################################

WEBHOOK_HOST = '178.32.56.221'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem' # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

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
##########################################################################################################
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'че пацаны, бассбуст? Краткий тутор доступен через /info')
    dbworker.set_state(message.chat.id, config.States.S_START.value)
###########################################################################################################
@bot.message_handler(commands=["info"])
def cmd_reset(message):
    tutor = open('./pic/tutor.mp4', 'rb')
    bot.send_message(message.chat.id, "Все, что нужно, так это бросить мне аудиофайл или голосовуху")
    bot.send_video(message.chat.id, tutor)
###########################################################################################################
@bot.message_handler(content_types=['audio'])
def get_audio(message):
    mcfn = './stuff/' + str(message.chat.first_name)
    bot.send_message(message.chat.id, 'эт аудио, инфа 100, Сейчас скачаю')
    if download_file(message, mcfn + '_audio'):
        print('downloaded!')
        mcfn = './stuff/' + str(message.chat.first_name)
        convert_to(mcfn + '_audio',mcfn + '_audio.mp3')
        fille = eyed3.load(mcfn + '_audio.mp3') #Смотрю че там по исходным id3 тэгам
        sartist =tekst.transform(fille.tag.artist)
        stitle = tekst.transform(fille.tag.title)
        convert_to(mcfn + '_audio',mcfn + '_dwnld.wav')
        bass(mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
        convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')
        fille = eyed3.load(mcfn + '_send.mp3')# ставлю свои тэги
        fille.tag.artist = sartist
        fille.tag.title = stitle
        fille.tag.save()
        audio = open(mcfn + '_send.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    else:
        bot.send_message(message.chat.id, 'Файлик слишком большой, прости, золотце')
###########################################################################################################
@bot.message_handler(content_types=['voice'])
def get_voice(message):
    mcfn = './stuff/' + str(message.chat.first_name)
    bot.send_message(message.chat.id, 'эт войс, я погромист, меня не обманешь')
    if download_file(message, mcfn+'_voice.ogg'):
        print('downloaded!')
        convert_to(mcfn + '_voice.ogg', mcfn + '_voice.wav')
        bass(mcfn + '_voice.wav', mcfn + '_voiceb.wav')
        convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
        voice = open(mcfn + '_send.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
    else:
        bot.send_message(message.chat.id, 'СЛИШКОМ много болтовни, телеграм не позволяет скачать')
###########################################################################################################
@bot.message_handler(func=lambda message: dbworker.get_current_state(message) == config.States.S_ASKING_FOR_BASS_POWER_AUDIO.value)
def asking_for_bass_a(message):# Не DRY, Стыдно...
    tries = 0
    mcfn = './stuff/' + str(message.chat.first_name)
    convert_to(mcfn + '_audio',mcfn + '_audio.mp3')
    fille = eyed3.load(mcfn + '_audio.mp3') #Смотрю че там по исходным id3 тэгам
    sartist =tekst.transform(fille.tag.artist)
    stitle = tekst.transform(fille.tag.title)
    convert_to(mcfn + '_audio',mcfn + '_dwnld.wav')
    bass(message.text, mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
    convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')
    fille = eyed3.load(mcfn + '_send.mp3')# ставлю свои тэги
    fille.tag.artist = sartist
    fille.tag.title = stitle
    fille.tag.save()
    audio = open(mcfn + '_send.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)
    dbworker.set_state(message.chat.id, config.States.S_ASKING_FOR_DOWNLOAD.value)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
