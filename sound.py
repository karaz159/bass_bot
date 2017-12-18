from pysndfx import AudioEffectsChain as af
import telebot as tb
from datetime import datetime
from os import system as sys
from config import token as TOKEN
from time import sleep

def bass(how_many,inn,outt):
    apply_af = af().lowshelf(how_many)
    apply_af(inn, outt)
    print ('BASS done')

def write_log(log):
    time = datetime.now()
    a_time = ('[' + str(time.hour) + ':' + str(time.minute) + '] ')
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

def convert_to(inn, out):# необходимо понять как вставлять в sys переменные
    sys('ffmpeg -y -loglevel quiet -i '+ inn + ' ' + out) #Конвертирую inn в ваф файл для дальнейшей работы

bot = tb.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'че пацаны, бассбуст?')

@bot.message_handler(content_types=['audio'])
def get_audio(message, nigga):
    bot.send_message(message.chat.id, 'эт аудио, инфа 100')
    if download_file(message, 'new_file.mp3'):
        print('downloaded!')
        convert_to('new_file.mp3','dwnld.wav')
        bass(50, 'dwnld.wav', 'bass.wav')# out is bass.wav
        convert_to('bass.wav','send.mp3')
        audio = open('send.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    else:
        bot.send_message(message.chat.id, 'Файлик слишком большой, прости, золотце')

@bot.message_handler(content_types=['voice'])
def get_voice(message):
    bot.send_message(message.chat.id, 'эт войс, я погромист, меня не обманешь')
    if download_file(message, 'new_voice.ogg'):
        print('downloaded!')
        convert_to('new_voice.ogg', 'new_voice.wav')
        bass(100, 'new_voice.wav', 'new_voiceb.wav')
        convert_to('new_voiceb.wav', 'send.ogg')
    else:
        bot.send_message(message.chat.id, 'СЛИШКОМ много болтовни, телеграм не позволяет скачать')
    voice = open('send.ogg', 'rb')
    bot.send_voice(message.chat.id, voice)
bot.polling()
