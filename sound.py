from pysndfx import AudioEffectsChain as af
import telebot as tb
from datetime import datetime
from os import system as sys
from config import token as TOKEN

def bass(how_many):
    apply_af = af().lowshelf(how_many)
    infile = 'dwnld.wav'
    outfile = 'bass.wav'
    apply_af(infile, outfile)
    print ('done')

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

bot = tb.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'че пацаны, бассбуст?')

@bot.message_handler(content_types=['audio'])
def get_audio(message):
    bot.send_message(message.chat.id, 'эт аудио, инфа 100')
    bot.download_file('sound.mp3')
    sys('mpg123 -w dwnld.wav sound.mp3') #Конвертирую в ваф файл для дальнейшей работы
    bass(50)
    audio = open('bass.wav' 'rb')
    bot.send_audio(message.chat.id, audio)

@bot.message_handler(content_types=['voice'])
def get_voice(message):
    bot.send_message(message.chat.id, 'эт войс, я погромист, меня не обманешь')
    bot.get_file('sound.ogg')

bot.polling()
