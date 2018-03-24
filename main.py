#!/usr/bin/env python3
from pysndfx import AudioEffectsChain as af
import telebot as tb
from datetime import datetime
from os import system as sys
from config import token as TOKEN
from time import sleep
import dbworker, config, tekst, eyed3, cherrypy

def bass(how_many,inn,outt):

    apply_af = af().lowshelf(how_many)
    apply_af(inn, outt)
    print ('BASS done')

def write_log(log):
    time = datetime.now()
    a_time = ('[' + str(time.day) + '.' + str(time.month) + '.' + str(time.year) + ' ' + str(time.hour) + ':' + str(time.minute) + '] ')
    TF = open('log.txt', 'a', encoding = 'utf-8')
    TF.write(a_time + log + '\n')
    TF.close()

#def report_an-update():
#    try:
#        update = open('report.txt', mode='r', encoding='utf-8')
#        for user in
######WIP Need to replace vedis? other bot


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

hm = open('voice.ogg', 'rb')
###########################################################################################################
bot = tb.TeleBot(TOKEN)
bot.set_update_listener(listener)
###########################################################################################################
WEBHOOK_HOST = '46.173.214.150'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
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
    state = dbworker.get_current_state(message.chat.id, message)
    if state == config.States.S_ASKING_FOR_DOWNLOAD.value:
        bot.send_message(message.chat.id, "Я посвятил тебя уже во все, что можно, братан")

    elif state == config.States.S_GOT_AUDIO.value:
        bot.send_message(message.chat.id, "Хм, что то пошло не так, на твоем бы месте я бы рассказал автору как ты этого добился")

    elif state == config.States.S_GOT_VOICE.value:
        bot.send_message(message.chat.id, "Хм, что то пошло не так, на твоем бы месте я бы рассказал автору как ты этого добился")

    elif state == config.States.S_ASKING_FOR_BASS_POWER_AUDIO.value:
        bot.send_voice(message.chat.id, hm)

    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, 'че пацаны, бассбуст? Краткий тутор доступен через /info')
        dbworker.set_state(message.chat.id, config.States.S_START.value)
###########################################################################################################
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Начнем заново, че пацаны, бассбуст?")
    dbworker.set_state(message.chat.id, config.States.S_START.value)
###########################################################################################################
@bot.message_handler(commands=["info"])
def cmd_reset(message):
    tutor = open('./pic/tutor.mp4', 'rb')
    bot.send_message(message.chat.id, "Все, что нужно, так это бросить мне аудиофайл или голосовуху")
    bot.send_video(message.chat.id, tutor)
###########################################################################################################
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def user_manual(message):
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    bot.send_message(message.chat.id, "Все, что тебе нужно, так это кинуть голосовуху или аудиозапись")
    dbworker.set_state(message.chat.id, config.States.S_ASKING_FOR_DOWNLOAD.value)
###########################################################################################################
@bot.message_handler(content_types=['audio'])
def get_audio(message):
    mcfn = './stuff/' + str(message.chat.first_name)
    bot.send_message(message.chat.id, 'эт аудио, инфа 100, Сейчас скачаю')
    if download_file(message, mcfn + '_audio'):
        print('downloaded!')
        dbworker.set_state(message.chat.id, config.States.S_GOT_AUDIO)
        bot.send_message(message.chat.id, 'Скок басу? 1-100')
        dbworker.set_state(message.chat.id, config.States.S_ASKING_FOR_BASS_POWER_AUDIO.value)

    else:
        bot.send_message(message.chat.id, 'Файлик слишком большой, прости, золотце')
###########################################################################################################
@bot.message_handler(content_types=['voice'])
def get_voice(message):
    mcfn = './stuff/' + str(message.chat.first_name)
    bot.send_message(message.chat.id, 'эт войс, я погромист, меня не обманешь')
    if download_file(message, mcfn+'_voice.ogg'):
        print('downloaded!')
        dbworker.set_state(message.chat.id, config.States.S_GOT_VOICE)
        convert_to(mcfn + '_voice.ogg', mcfn + '_voice.wav')
        bot.send_message(message.chat.id, 'Скок басу? 1-100')
        dbworker.set_state(message.chat.id, config.States.S_ASKING_FOR_BASS_POWER_VOICE.value)

    else:
        bot.send_message(message.chat.id, 'СЛИШКОМ много болтовни, телеграм не позволяет скачать')
###########################################################################################################
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ASKING_FOR_BASS_POWER_VOICE.value)
def asking_for_bass_v(message):
    mcfn = './stuff/' + str(message.chat.first_name)
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Цифра нужна, братан')

    if int(message.text) < 1 or int(message.text) > 100:
        bot.send_message(message.chat.id, 'От 1 до 100, братан')

    else:
        print(message.text)
        bass(message.text, mcfn + '_voice.wav', mcfn + '_voiceb.wav')
        convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
        voice = open(mcfn + '_send.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
        dbworker.set_state(message.chat.id, config.States.S_ASKING_FOR_DOWNLOAD.value)
###########################################################################################################
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ASKING_FOR_BASS_POWER_AUDIO.value)
def asking_for_bass_a(message):# Не DRY, Стыдно...
    tries = 0
    mcfn = './stuff/' + str(message.chat.first_name)
    if tries > 2:#Необходимо намутить свои автоматы которые будут вмещать сколь угодно состояний для пользователя
        bot.send_message(message.chat.id, 'ну ты ебан?')
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Цифра нужна, братан')
        tries += 1
        return
    if int(message.text) < 1 or int(message.text) > 100:
        bot.send_message(message.chat.id, 'От 1 до 100, братан')
        tries += 1
    else:
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
