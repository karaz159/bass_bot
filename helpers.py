"""
helpers file that contain useful features
"""
import re

from random import choice
from os import system as sys

import config


def yt_link_check(link):
    return re.search("(https?:\/\/[w.y]+outube.com\/watch\?v=[^\s]+)", link)

def download_video(link):
    pass


def prepare_file(inn, out):
    sys(f'ffmpeg -y -loglevel quiet -i {inn} {out}') # nosec

def download(bot, message, name):
    """
    downloads mp3 or voice via bot
    """
    if message.audio:
        file_info = bot.get_file(message.audio.file_id)
    else:
        file_info = bot.get_file(message.voice.file_id)

    downloaded_file = bot.download_file(file_info.file_path)

    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)

    return name


def transform_eyed3(word):
    '''
    transforms any word to cringe
    '''
    shit = ''
    if word:
        for character in word.lower():
            try:
                shit += choice(config.ALPHABET[character]) # nosec
            except KeyError:
                shit += character
    else:
        shit = choice(config.hz) # nosec
    return shit
