"""
Module describes audio class
allowing to set eyed3 tags, add dcb to bass, etc
"""
import os
import time

import eyed3
import ffmpeg

from config import BASS_PATH, DOWNLOAD_PATH
from helpers import download, download_video, leet_translate
from sqlworker import get_user


class TgAudio:  # Замена на filepath
    """
    Main TgAudio class
    """
    def __init__(self, sender_id, src_path, content_type,
                 performer=None, title=None, update_tags=False):
        # TODO to many logic in init?
        self.sender_id = sender_id
        self.content_type = content_type

        if self.content_type == 'audio':
            self.performer = performer
            self.title = title
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}B.mp3'
        else:
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}B.ogg'
        self.src_path = src_path
        self.transform_eyed3 = False
        if update_tags:
            ll = eyed3.load(self.src_path)
            ll.tag.artist = self.performer
            ll.tag.title = self.title
            ll.tag.save()

    @classmethod
    def from_message(cls, m):
        """
        Make this class from message,
        just pass message from tg
        """
        src_path = f'{DOWNLOAD_PATH}{m.chat.id}.mp3' if m.audio else f'{DOWNLOAD_PATH}{m.chat.id}.ogg'

        download(m, src_path)

        if m.audio:
            return cls(sender_id=m.chat.id,
                       src_path=src_path,
                       content_type=m.content_type,
                       performer=m.audio.performer,
                       title=m.audio.title)

        return cls(sender_id=m.chat.id,
                   src_path=src_path,
                   content_type=m.content_type)

    @classmethod
    def from_local(cls, m):
        """
        Make this class from local audio
        """
        user = get_user(m.chat.id)
        src = user.last_source

        if not os.path.exists(src):
            raise FileNotFoundError

        if src.endswith('mp3'):
            tags = eyed3.load(src).tag
            return cls(sender_id=m.chat.id,
                       src_path=user.last_source,
                       content_type='audio',
                       performer=tags.artist if tags else '',
                       title=tags.title if tags else '')

        return cls(m.chat.id, src, 'voice')

    @classmethod
    def from_yt(cls, m, link):
        """
        Makes class out of youtube video
        """
        src_path = f'{DOWNLOAD_PATH}{m.chat.id}'

        try:
            os.remove(f'{src_path}.mp3')
            os.remove(f'{src_path}.mp4')

        except FileNotFoundError:
            pass

        meta = download_video(link, src_path)
        src_path += '.mp3'
        title = meta['alt_title'] if meta['alt_title'] else meta['title']
        time.sleep(3)

        return cls(sender_id=m.chat.id, src_path=src_path,
                   content_type='audio', performer=meta['uploader'],
                   title=title, update_tags=True)

    def save_tags(self):
        """
        Updates mp3 tags using
        eyed3 lib
        """
        loaded_audio = eyed3.load(self.bass_done_path)
        loaded_audio.tag.artist = self.performer
        loaded_audio.tag.title = self.title
        loaded_audio.tag.save()

    def transform_tag(self):
        """
        gets title and performer from self
        and transforms them using leet_translate func
        """
        self.title = leet_translate(self.title)
        self.performer = leet_translate(self.performer)
        self.save_tags()

    def bass_boost(self, how_many):
        """
        Adds some dcb to loaded audio
        """
        stream = ffmpeg.input(self.src_path)
        stream = stream.audio.filter("bass", g=how_many)
        ffmpeg.output(stream, self.bass_done_path).overwrite_output().run()

        if self.transform_eyed3:
            self.transform_tag()

    def open_bass(self):
        """
        Returns opened in bytes audio
        """
        return open(self.bass_done_path, 'rb')
