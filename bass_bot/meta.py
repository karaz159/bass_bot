"""
Module that represents
metadata of DUDES in db
"""
from pysndfx import AudioEffectsChain as af
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
import eyed3

import subprocess
import ffmpeg
from config import BASS_PATH, CONVERT_PATH, DOWNLOAD_PATH
from helpers import download, prepare_file
from helpers import leet_translate

BASE = declarative_base()

class States:
    start = 'start'
    asking_for_stuff = 'asking_for_stuff'
    got_voice = 'got_voice'
    got_audio = 'got_audio'
    asking_bass_pwr_mp3 = 'asking_bass_pwr_mp3'
    asking_bass_pwr_voice = 'asking_bass_pwr_voice'

class Dude(BASE):
    """
    Main dude sqlalchemy class
    """
    __tablename__ = "dudes"

    user_id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, unique=True)
    user_name = Column(String, nullable=False)
    first_name = Column(String)
    curr_state = Column(String, server_default=States.start)
    random_bass = Column(Boolean, default=False)
    transform_eyed3 = Column(Boolean, default=True)
    last_message_date = Column(DateTime, server_default=func.now())
    first_message_date = Column(DateTime, server_default=func.now())
    last_source = Column(String, unique=True)

class TgAudio: # Замена на filepath
    def __init__(self, m):
        self.sender_id = str(m.chat.id)
        self.type = 'voice' if m.voice else 'audio'
        if m.audio:
            self.performer = m.audio.performer
            self.title = m.audio.title
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}.mp3'
        else:
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}.ogg'
        self.src_path = f'{DOWNLOAD_PATH}{self.sender_id}_{self.type}'
        self.wav_path = f'{CONVERT_PATH}{self.sender_id}_{self.type}.wav'
        self.bass_path = f'{BASS_PATH}{self.sender_id}_{self.type}.wav'
        download(m, self.src_path)
        self.transform_eyed3 = False

    @classmethod
    def from_local(cls, tg_user_id):
        pass

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


class LocalAudio(TgAudio):
    pass

class Answers:
    got_text = 'Мне нужна голосовуха либо аудиозапись, братан /info'
    started_already = "Я посвятил тебя уже во все, что можно, братан"
    shit_happend = ("Хм, что то пошло не так, на твоем бы месте"
                    "я бы рассказал автору как ты этого добился")
    #hm = open('./stuff/voice.ogg', 'rb')
    start = 'че пацаны, бассбуст? Краткий тутор доступен через /info'
    reset = "Восстанавливаю стандартные значения"
    turn_on = "Включаю"
    turn_off = "Отключаю"
    random_bass = "рандомный басс"
    random_tags = "рандомные тэги"
    info = ("Все, что нужно, так это бросить "
            "мне аудиофайл или голосовуху\n"
            "Так же возможно менять поведение "
            "бота командами \n/random \n/transform")
    after_start = "Все, что нужно, так это бросить мне аудиофайл или голосовуху"
    got_it = 'Принял'
    too_much = 'Слишком много всякого, не могу скачать'
    numbers_needed = 'Цифра нужна, братан'
    num_range = 'От 1 до 100, братан'
    how_many = 'Скок бассу, брах'
