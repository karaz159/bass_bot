"""
helpers file that contain useful features
"""
from random import choice

import youtube_dl
from config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD, YT_LOGIN, YT_PASSWORD, sys_log
from data import ALPHABET
from pathlib import Path


def download_video(link, path: Path):
    ydl_opts = {
        'username': YT_LOGIN,
        'password': YT_PASSWORD,
        'format': 'bestaudio/best',
        'outtmpl': str(path.with_suffix('.mp4')),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
    }

    if '&' in link:
        link = link.split('&')[0]

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(link, download=False)
        sys_log.info(f'Meta - {meta}\n'
                     f'duration - {meta.get("duration", "NONE")}')
        if not meta.get('duration'):
            sys_log.error('Can`t get meta duration!')
        if meta['duration'] > 600:
            raise ValueError

        ydl.download([link])
    return meta


def this_is_downloadable_link(link):
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
        cringe = choice(ALPHABET['hz'])  # nosec
    return cringe


def get_db_dsn(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db_name=DB_NAME):
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
