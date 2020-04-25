"""
Module that represents
metadata of DUDES in db
States and Answers
"""
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class States:
    start = 'start'
    asking_for_stuff = 'asking_for_stuff'
    asking_bass_pwr = 'asking_bass_pwr'

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
