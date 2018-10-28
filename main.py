#!/usr/bin/env python3
from pysndfx import AudioEffectsChain as af
import telebot as tb
from datetime import datetime
from os import system as sys
from os import remove as rm
import tekst, eyed3, cherrypy, argparse, sqlworker, sqlite3
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument("-t", help="run without server, using different creds")
args = parser.parse_args()

if args.t:
    import config2 as config
else:
    import config

def transform_tag(tags, final_name):
    sartist =tekst.transform(tags.tag.artist)
    stitle = tekst.transform(tags.tag.title)
    fille = eyed3.load(final_name)# ставлю свои тэги
    fille.tag.artist = sartist
    fille.tag.title = stitle
    fille.tag.save()


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

bot = tb.TeleBot(config.token)
bot.set_update_listener(listener)
hm = open('./stuff/voice.ogg', 'rb')
WEBHOOK_HOST = '178.32.56.22'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem' # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

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
    print ("the state is", state)
    if state == config.States.ASKING_FOR_DOWNLOAD:
        bot.send_message(message.chat.id, "Я посвятил тебя уже во все, что можно, братан")

    elif state == config.States.GOT_AUDIO:
        bot.send_message(message.chat.id, "Хм, что то пошло не так, на твоем бы месте я бы рассказал автору как ты этого добился")

    elif state == config.States.GOT_VOICE:
        bot.send_message(message.chat.id, "Хм, что то пошло не так, на твоем бы месте я бы рассказал автору как ты этого добился")
    elif state == config.States.ASKING_FOR_BASS_POWER_AUDIO:
        bot.send_voice(message.chat.id, hm)

    elif state == config.States.START:
        print("it is done")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, 'че пацаны, бассбуст? Краткий тутор доступен через /info')
        sqlworker.register_dude(message)

@bot.message_handler(commands=["random"])
def change_random_state(message):
    print (sqlworker.is_random(message.chat.id))
    if sqlworker.is_random(message.chat.id):
        bot.send_message(message.chat.id, "Отключаю рандомный басс!")
        sqlworker.set_random(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "Включаю рандомный басс!")
        sqlworker.set_random(message.chat.id, 1)

@bot.message_handler(commands=["transform"])
def change_transform_state(message):
    if sqlworker.is_transform(message.chat.id):
        bot.send_message(message.chat.id, "Отключаю рандомные тэги!")
        sqlworker.set_transform(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "Включаю рандомные тэги!")
        sqlworker.set_transform(message.chat.id, 1)

@bot.message_handler(commands=["info"])
def user_man(message):
    #tutor = open('./stuff/pic/tutor.mp4', 'rb')
    bot.send_message(message.chat.id, "Все, что нужно, так это бросить мне аудиофайл или голосовуху\nТак же возможно менять поведение бота командами /random /transform")
    #bot.send_video(message.chat.id, tutor)

@bot.message_handler(func=lambda message: sqlworker.get_current_state(message.chat.id) == config.States.START)
def cmd_reset(message):
    print("got 0")
    bot.send_message(message.chat.id, "Все, что нужно, так это бросить мне аудиофайл или голосовуху")
    sqlworker.set_state(message.chat.id, config.States.ASKING_FOR_DOWNLOAD)

@bot.message_handler(content_types=['audio'])
def get_audio(message):
    mcfn = './stuff/' + str(message.chat.first_name)
    bot.send_message(message.chat.id, 'эт аудио, инфа 100, Сейчас скачаю')
    if download_file(message, mcfn + '_audio'):
        print('downloaded!')
        if sqlworker.is_random(message.chat.id):
            print("yup, random")
            convert_to(mcfn + '_audio',mcfn + '_audio.mp3')
            tags = eyed3.load(mcfn + '_audio.mp3')
            convert_to(mcfn + '_audio',mcfn + '_dwnld.wav')
            bass(randint(25,100), mcfn + '_dwnld.wav', mcfn + '_dwnldb.wav')
            convert_to(mcfn + '_dwnldb.wav', mcfn + '_send.mp3')
            if sqlworker.is_transform(message.chat.id):
                transform_tag(tags, mcfn + '_send.mp3')
            else:
                tags_send = eyed3.load(mcfn + '_send.mp3')
                tags_send.tag.artist = tags.tag.artist
                tags_send.tag.title = tags.tag.title
                tags_send.tag.save()
            #tags.tag.save()
            audio = open(mcfn + '_send.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)

        else:
            bot.send_message(message.chat.id, 'Скок басу? 1-100')
            sqlworker.set_state(message.chat.id, config.States.ASKING_FOR_BASS_POWER_AUDIO)
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
        if sqlworker.is_random(message.chat.id):
            print("yup, random")
            bass(randint(25,100), mcfn + '_voice.wav', mcfn + '_voiceb.wav')
            convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
            voice = open(mcfn + '_send.ogg', 'rb')
            bot.send_voice(message.chat.id, voice)
        else:
            bot.send_message(message.chat.id, 'Скок басу? 1-100')
            sqlworker.set_state(message.chat.id, config.States.ASKING_FOR_BASS_POWER_VOICE)
    else:
        bot.send_message(message.chat.id, 'СЛИШКОМ много болтовни, телеграм не позволяет скачать')
###########################################################################################################
@bot.message_handler(func=lambda message: sqlworker.get_current_state(message.chat.id) == config.States.ASKING_FOR_BASS_POWER_VOICE)
def asking_for_bass_v(message):
    mcfn = './stuff/' + str(message.chat.first_name)

    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Цифра нужна, братан')

    elif int(message.text) < 1 or int(message.text) > 100:
        bot.send_message(message.chat.id, 'От 1 до 100, братан')

    else:
        print(message.text)
        bass(message.text, mcfn + '_voice.wav', mcfn + '_voiceb.wav')
        convert_to(mcfn + '_voiceb.wav', mcfn + '_send.ogg')
        voice = open(mcfn + '_send.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
        sqlworker.set_state(message.chat.id, config.States.ASKING_FOR_DOWNLOAD)


@bot.message_handler(func=lambda message: sqlworker.get_current_state(message.chat.id) == config.States.ASKING_FOR_BASS_POWER_AUDIO)
def asking_for_bass_a(message):# Не DRY, Стыдно...
    mcfn = './stuff/' + str(message.chat.first_name)

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
        sqlworker.set_state(message.chat.id, config.States.ASKING_FOR_DOWNLOAD)

#    bot.remove_webhook()

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
if args.t:
    print("yup, got test")
    bot.polling()
else:
    print ("omg")
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    certificate=open(WEBHOOK_SSL_CERT, 'r'))
    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
