
import subprocess

import eyed3
import ffmpeg
from pysndfx import AudioEffectsChain as af

from config import BASS_PATH, DOWNLOAD_PATH
from helpers import download, leet_translate, prepare_file
from sqlworker import get_user

class TgAudio: # Замена на filepath
    def __init__(self, sender_id, src_path, content_type,
                 performer=None, title=None):
        self.sender_id = sender_id
        self.content_type = content_type
        if self.content_type == 'audio':
            self.performer = performer
            self.title = title
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}.mp3'
        else:
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}.ogg'
        self.src_path = src_path
        self.transform_eyed3 = False

    @classmethod
    def from_message(cls, m):
        src_path = f'{DOWNLOAD_PATH}{m.chat.id}.{m.content_type}'
        download(m, src_path)
        if m.audio:
            return cls(m.chat.id,
                       src_path,
                       m.content_type,
                       performer=m.audio.performer,
                       title=m.audio.title)
        return cls(m.chat.id, src_path, m.content_type)

    @classmethod
    def from_local(cls, m):
        user = get_user(m.chat.id)
        src = user.last_source
        if src.endswith('audio'):
            tags = eyed3.load(src).tag
            return cls(m.chat.id,
                       user.last_source,
                       'audio',
                       performer=tags.artist,
                       title=tags.title)
        return cls(m.chat.id, src, 'voice')

    def save_tags(self):
        '''
        Updates mp3 tags using
        eyed3 lib
        '''
        ll = eyed3.load(self.bass_done_path)
        ll.tag.artist = self.performer
        ll.tag.title = self.title
        ll.tag.save()

    def transform_tag(self):
        '''
        gets title and performer from self
        and transforms them using leet_translate func
        '''
        self.title = leet_translate(self.title)
        self.performer = leet_translate(self.performer)
        self.save_tags()

    def bass_boost(self, how_many):
        strint = f'ffmpeg -y -i {self.src_path} -af bass=g={str(how_many)}:f=110:w=0.7 {self.bass_done_path}'
        subprocess.call(strint, shell=True)
        if self.transform_eyed3:
            self.transform_tag()

    def bass_boost_legacy(self, how_many):
        prepare_file(self.src_path, self.wav_path)
        apply_af = af().lowshelf(how_many)
        apply_af(self.wav_path, self.bass_path)
        prepare_file(self.bass_path, self.bass_done_path)
        if self.transform_eyed3:
            self.transform_tag()

    def open_bass(self):
        return open(self.bass_done_path, 'rb')
