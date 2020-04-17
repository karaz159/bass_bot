"""
Module that represents
metadata of DUDES in db
"""
import random

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, func
from helpers import transform_eyed3 as t3
from helpers import download, prepare_file
from config import DOWNLOAD_PATH, CONVERT_PATH
from pysndfx import AudioEffectsChain as af

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
    last_voice_source = Column(String, unique=True)
    last_mp3_source = Column(String, unique=True)



class TgAudio():
    def __init__(self, bot, m):
        self.sender_id = str(m.chat.id)
        self.mime_type = m.audio.mime_type
        self.performer = m.audio.performer
        self.title = m.audio.title
        self.duration = m.audio.duration
        self.src_path = f'{DOWNLOAD_PATH}{self.sender_id}_audio'
        self.wav_path = f'{CONVERT_PATH}{self.sender_id}.wav'
        self.bass_path = None
        download(bot, m, self.src_path)
        prepare_file(self.src_path, self.wav_path)
        self.downloaded = True
        self.converted = True
        self.boosted = False

    def transform_eyed3(self):
        self.title = t3(self.title)
        self.performer = t3(self.performer)

    def bass_boost(self, random_pwr=False):
        if random_pwr:
            how_many = random.randint(1, 100) # nosec
        apply_af = af().lowshelf(how_many)
        apply_af(self.wav_path, self.bass_path)
        self.boosted = True

    def open_bass(self):
        if self.boosted:
            return open(self.bass_path)
        raise ValueError('Bass not boosted!')

    # @performer.setter
    # def perfromer(self, a):
        # pass

class LocalAudio(TgAudio):
    pass


class Answers:
    got_text = 'Мне нужна голосовуха либо аудиозапись, братан /info'
    started_already = "Я посвятил тебя уже во все, что можно, братан"
    shit_happend = ("Хм, что то пошло не так, на твоем бы месте"
                    "я бы рассказал автору как ты этого добился")
    hm = open('./stuff/voice.ogg', 'rb')
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
