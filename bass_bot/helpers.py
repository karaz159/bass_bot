"""
helpers file that contain useful features
"""
import re
from random import choice

import youtube_dl

from config import bot
from models import hz, ALPHABET

def yt_link_check(link):
    first = re.search("(https?:\/\/[w.y]+outube.com\/watch\?v=[^\s]+)", link)
    second = re.search("(https?:\/\/[w.y]+outu.be\/[^\s]+)", link)
    return first or second

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_video(link, path):
    path += '.mp4'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(link, download=False)
        if meta['duration'] > 600:
            raise ValueError
        ydl.download([link])
    return meta


def download(message, name):
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


def leet_translate(word):
    '''
    transforms any word to cringe
    '''
    shit = ''
    if word:
        for character in word.lower():
            bad_character = ALPHABET.get(character)
            if bad_character:
                shit += choice(bad_character) # nosec
            else:
                shit += character
    else:
        shit = choice(hz) # nosec
    return shit
