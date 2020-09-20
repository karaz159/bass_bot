#!/usr/bin/env python3
"""
main module with all bot commands
"""
import random

from config import bot, log, SERVER_FLAG
from helpers import yt_link_check
from meta import Answers, States
from audio import TgAudio
from server import serv_start
from sqlworker import alt_bool, check_state, get_user, listener, register_dude, set_column

bot.set_update_listener(listener)


@bot.message_handler(commands=['start'])
def start(m):
    user = get_user(m.chat.id)

    if not user:
        bot.send_message(m.chat.id, Answers.start)
        return

    state = user.curr_state

    if state == States.start:
        bot.send_message(m.chat.id, 'Старт уже запущен был')

    elif state == States.asking_for_stuff:
        bot.send_message(m.chat.id, 'whops')

    elif state == States.asking_bass_pwr:
        if getattr(Answers, 'hm'):
            bot.send_voice(m.chat.id, Answers.hm)


@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, Answers.reset)
    set_column(message.chat.id, state=States.start)


@bot.message_handler(commands=["transform", "random"])
def change_transform_state(m):
    if m.text == '/transform':
        state = alt_bool(m.chat.id, transform=True)
        service = Answers.random_tags

    elif m.text == '/random':
        state = alt_bool(m.chat.id, random=True)
        service = Answers.random_bass

    if state:
        action = Answers.turn_on
    else:
        action = Answers.turn_off

    bot.send_message(m.chat.id, f"{action} {service}")


@bot.message_handler(commands=["delete"])
def delete_user(m):
    pass  # TODO


@bot.message_handler(commands=["info"])
def user_man(message):
    bot.send_message(message.chat.id, Answers.info)


@bot.message_handler(func=lambda m: check_state(m.chat.id, States.downloading))
def downloading_stuff(message):
    bot.send_message(message.chat.id, Answers.downloading)


@bot.message_handler(func=lambda m: check_state(m.chat.id, States.boosting))
def boost_stuff(message):
    bot.send_message(message.chat.id, Answers.boosting)


@bot.message_handler(content_types=['audio', 'voice'])
def get_audio(m, yt_link=None):
    """
    React on sended audio or voice
    """
    user = get_user(m.chat.id)
    bot.send_message(m.chat.id, Answers.got_it)
    set_column(m.chat.id, state=States.downloading)

    if yt_link:
        try:
            bot.send_chat_action(m.chat.id, 'record_video')
            audio = TgAudio.from_yt(m, yt_link)
        except ValueError:
            bot.send_message(m.chat.id, 'Слишком большой видос, 10 минут макс')
            set_column(m.chat.id, state=States.asking_bass_pwr)
            return
    else:
        bot.send_chat_action(m.chat.id, 'record_audio')
        audio = TgAudio.from_message(m)

    if audio.content_type == 'audio':
        audio.transform_eyed3 = user.transform_eyed3

    if user.random_bass:
        random_power = random.randint(5, 50)  # nosec
        set_column(m.chat.id, state=States.boosting)
        bot.send_message(m.chat.id, f'пилю бас, сила: {random_power}')
        audio.bass_boost(random_power)  # nosec
        bot.send_audio(m.chat.id, audio.open_bass())

    else:
        bot.send_message(m.chat.id, Answers.num_range)

    set_column(m.chat.id,
               state=States.asking_bass_pwr,
               last_src=audio.src_path)


@bot.message_handler(func=lambda m: check_state(m.chat.id, States.asking_bass_pwr))
def asking_for_bass(m):
    user = get_user(m.chat.id)
    this_is_yt_link = yt_link_check(m.text)
    if this_is_yt_link:
        get_audio(m, yt_link=this_is_yt_link[0])
        return

    if not m.text.isdigit():
        bot.send_message(m.chat.id, Answers.numbers_needed)

    elif int(m.text) < 1 or int(m.text) > 100:
        bot.send_message(m.chat.id, Answers.num_range)

    else:
        try:
            audio = TgAudio.from_local(m)
        except FileNotFoundError:
            bot.send_message(m.chat.id, Answers.file_lost)

        else:
            if audio.content_type == 'audio':
                audio.transform_eyed3 = user.transform_eyed3

            set_column(m.chat.id, state=States.boosting)
            audio.bass_boost(int(m.text))

            if audio.content_type == 'audio':
                bot.send_audio(m.chat.id, audio.open_bass())

            else:
                bot.send_voice(m.chat.id, audio.open_bass())

            set_column(m.chat.id, state=States.asking_bass_pwr)


@bot.message_handler(func=lambda m: check_state(m.chat.id, States.start))
def after_start(message):
    bot.send_message(message.chat.id, Answers.after_start)
    set_column(message.chat.id, States.asking_for_stuff)


@bot.message_handler(content_types=['text'])
def answer_with_info(message):
    this_is_yt_link = yt_link_check(message.text)

    if this_is_yt_link:
        get_audio(message, yt_link=this_is_yt_link[0])

    else:
        bot.send_message(message.chat.id, Answers.got_text)


if __name__ == "__main__":
    if SERVER_FLAG:
        serv_start()
        log.info('Running in server mode')
    else:
        bot.remove_webhook()
        log.info('Running in poll mode')
        bot.polling(none_stop=True)
