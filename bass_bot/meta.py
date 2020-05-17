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
    downloading = 'downloading'
    boosting = 'boosting'

class Dude(BASE):
    """
    Main dude sqlalchemy class
    """
    __tablename__ = "dudes"

    user_id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, unique=True)
    user_name = Column(String)
    first_name = Column(String)
    curr_state = Column(String, server_default=States.start)
    random_bass = Column(Boolean, default=False)
    transform_eyed3 = Column(Boolean, default=True)
    last_message_date = Column(DateTime, server_default=func.now())
    first_message_date = Column(DateTime, server_default=func.now())
    last_source = Column(String, unique=True)

class Answers:
    file_lost = 'Йоу, потерялся твой файл, можешь еще раз скинуть?'
    got_text = 'Мне нужна голосовуха либо аудиозапись, братан /info'
    started_already = "Я посвятил тебя уже во все, что можно, братан"
    shit_happend = ("Хм, что то пошло не так, на твоем бы месте"
                    "я бы рассказал автору как ты этого добился")
    hm = open('./hm.ogg', 'rb')
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
    downloading = 'Мой чувак, качаю вещи'
    boosting = 'Мой чувак, бустаю вещи'

a = ('@', 'A', 'а')
b = ('B', '8', 'Б')
c = ('С', 'с', 'S', '$', '$$')
d = ('D', 'd', 'д', 'Д', 't')
e = ('3', 'E')
f = ('F', 'Ф')
g = ('G', 'Г')
h = ('Х', 'H')
i = ('I', 'i', 'И', 'и')
k = ('k', 'K')
l = ('LL', 'L', 'l')
m = ('М', 'ММ')
n = ('н', 'Н')
o = ('О', '0')
r = ('r', 'R')
t = ('Ͳ', 'Т', 'т', 't')
v = ('V', 'В', 'v', 'в')
z = ('ZZ', 'Z', 'z', 'З', 'з')
hz = ('N3т', 'NE Y@sNo', '<UнKn0wн>', '4eг0')

ALPHABET = {
    'а': a,
    'б': b,
    'в': v,
    'г': ('G', 'Г'),
    'д': d,
    'е': e,
    'ж': ('J', 'ZH', 'ж', 'Ж'),
    'з': z,
    'и': i,
    'й': i,
    'к': k,
    'л': l,
    'м': m,
    'н': n,
    'о': o,
    'п': ('P', '5'),
    'р': r,
    'с': c,
    'т': t,
    'у': ('у', 'Y'),
    'ф': f,
    'х': h,
    'ц': ('Ц', 'С'),
    'ч': ('Ч', 'CH', 'cH'),
    'ш': ('SH', 'sH', 'Sh', 'Ш'),
    'щ': ('SH', 'sH', 'Sh', 'Щ'),
    'ъ': ('Б', 'Ъ', 'ь', 'ъ'),
    'ы': ('bi', 'Ы'),
    'ь': ('Б', 'Ъ', 'ь', 'ъ'),
    'э': ('Э', 'э'),
    'ю': ('ю', 'Ю'),
    'я': ('я', 'Я'),
    'a': a,
    'b': b,
    'c': c,
    'd': d,
    'e': e,
    'f': f,
    'g': g,
    'h': h,
    'i': i,
    'j': ('j', 'J'),
    'k': k,
    'l': l,
    'm': m,
    'n': n,
    'o': o,
    'p': ('P', '5'),
    'r': r,
    's': ('S', '$$', '$'),
    't': t,
    'u': ('u', 'U'),
    'v': v,
    'w': ('w', 'W'),
    'x': ('x', 'X', 'XX'),
    'y': ('y', 'Y'),
    'z': z
}
