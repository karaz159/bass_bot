"""
helpers file that contain useful features
"""
from random import choice

import youtube_dl
from config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD
from data import ALPHABET


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


def download(self, message, name):
    """
    downloads mp3 or voice via bot
    """
    if message.audio:
        file_info = self.get_file(message.audio.file_id)
    else:
        file_info = self.get_file(message.voice.file_id)

    downloaded_file = self.download_file(file_info.file_path)

    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)

    return name


def is_supported(link):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(link) and e.IE_NAME != 'generic':
            return True
    return False


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def leet_translate(word):
    """
    transforms any word to cringe
    """
    cringe = ''
    if word:
        for character in word.lower():
            bad_character = ALPHABET.get(character)
            if bad_character:
                cringe += choice(bad_character)  # nosec
            else:
                cringe += character
    else:
        cringe = choice(ALPHABET.hz)  # nosec
    return cringe


def get_db_dsn(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db_name=DB_NAME):
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
