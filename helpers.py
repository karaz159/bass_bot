"""
helpers file that contain useful features
"""
import sqlworker
import sys

class States:
    START = '0'  # Начало нового диалога
    ASKING_FOR_DOWNLOAD = '1'
    GOT_VOICE = '2'
    GOT_AUDIO = '3'
    ASKING_FOR_BASS_POWER_AUDIO = '4'
    ASKING_FOR_BASS_POWER_VOICE = '5'


class Answers:
    got_text = 'Мне нужна голосовуха либо аудиозапись, братан /info'
    started_already = "Я посвятил тебя уже во все, что можно, братан"
    shit_happend = ("Хм, что то пошло не так, на твоем бы месте"
                    "я бы рассказал автору как ты этого добился")
    hm = open('./stuff/voice.ogg', 'rb')
    start = 'че пацаны, бассбуст? Краткий тутор доступен через /info'
    reset = "Восстанавливаю стандартные значения"
    turn_on = "Отключаю"
    turn_off = "Включаю"
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


def user_started(message):
    return sqlworker.get_current_state(message.chat.id) == States.START

def download_video(link):
    pass

def check_asking(m):
    voice = sqlworker.get_current_state(m.chat.id) == States.ASKING_FOR_BASS_POWER_VOICE
    audio = sqlworker.get_current_state(m.chat.id) == States.ASKING_FOR_BASS_POWER_AUDIO
    return audio or voice

def convert_to(inn, out):
    sys('ffmpeg -y -loglevel quiet -i '+ inn + ' ' + out)