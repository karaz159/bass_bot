from random import randint

from telebot.types import Message

from data import Answers
from helpers import this_is_downloadable_link
from models import States


def setup_handlers(bot):
    @bot.message_handler(commands=['start'])
    @bot.db.provide_session
    def start(m, session):
        user = bot.db.get_user(m, session)
        state = user.curr_state

        if state == States.start:
            bot.send_message(m.chat.id, Answers.start)
        elif state == States.asking_for_stuff:
            bot.send_message(m.chat.id, 'whoops')
        elif state == States.asking_bass_pwr:
            if getattr(Answers, 'hm'):
                bot.send_voice(m.chat.id, Answers.hm)

    @bot.message_handler(commands=['reset'])
    @bot.db.provide_session
    def reset(message, session):
        bot.send_message(message.chat.id, Answers.reset)
        dude = bot.db.get_user(message, session)
        dude.curr_state = States.start

    @bot.message_handler(commands=["transform"])
    @bot.db.provide_session
    def change_transform_state(message, session):
        dude = bot.db.get_user(message, session=session)
        dude.transform_eyed3 = not dude.transform_eyed3
        action = Answers.turn_on if dude.transform_eyed3 else Answers.turn_off
        bot.send_message(message.chat.id, f"{action} transform!")

    @bot.message_handler(commands=["random"])
    @bot.db.provide_session
    def change_random_state(message, session):
        dude = bot.db.get_user(message, session=session)
        dude.random_bass = not dude.random_bass
        action = Answers.turn_on if dude.random_bass else Answers.turn_off
        bot.send_message(message.chat.id, f"{action} random!")

    @bot.message_handler(commands=["delete"])
    @bot.db.provide_session
    def delete_user(message, session):
        dude = bot.db.get_user(message, session=session)
        bot.send_message(message.chat.id, 'Thanks for using bot, bye!')
        session.delete(dude)

    @bot.message_handler(commands=["info"])
    def user_man(message):
        bot.send_message(message.chat.id, Answers.info)

    @bot.message_handler(func=lambda m: bot.db.check_state(message=m, state=States.downloading))
    def downloading_stuff(message):
        bot.send_message(message.chat.id, Answers.downloading)

    @bot.message_handler(func=lambda m: bot.db.check_state(message=m, state=States.boosting))
    def boost_stuff(message):
        bot.send_message(message.chat.id, Answers.boosting)

    @bot.message_handler(content_types=['audio', 'voice'])
    @bot.db.provide_session
    def get_audio(m, session, yt_link=None):
        """
        React on sent audio or voice
        """
        dude = bot.db.get_user(m, session=session)
        dude.curr_state = States.downloading
        session.commit()
        bot.send_message(m.chat.id, Answers.got_it)
        if yt_link:
            try:
                bot.send_chat_action(m.chat.id, 'record_video')
                audio = bot.audio.from_yt(m, yt_link)
            except ValueError:
                bot.send_message(m.chat.id, 'Слишком большой видос, 10 минут макс')
                dude.curr_state = States.asking_bass_pwr
                return
        else:
            bot.send_chat_action(m.chat.id, 'record_audio')
            audio = bot.audio.from_message(m)

        if audio.content_type == 'audio':
            audio.transform_eyed3 = dude.transform_eyed3

        if dude.random_bass:
            random_power = randint(5, 50)  # nosec
            dude.curr_state = States.boosting
            session.commit()
            bot.send_message(m.chat.id, f'пилю бас, сила: {random_power}')
            audio.bass_boost(random_power)  # nosec
            bot.send_audio(m.chat.id, audio.open_bass())
        else:
            bot.send_message(m.chat.id, Answers.num_range)

        dude.curr_state = States.asking_bass_pwr
        dude.last_src = str(audio)

    @bot.message_handler(func=lambda m: bot.db.check_state(message=m, state=States.asking_bass_pwr))
    @bot.db.provide_session
    def asking_for_bass(m: Message, session):
        user = bot.db.get_user(m, session=session)
        if this_is_downloadable_link(m.text):
            get_audio(m, yt_link=m.text, session=session)
            return

        if not m.text.isdigit():
            bot.send_message(m.chat.id, Answers.numbers_needed)
            return
        elif int(m.text) < 1 or int(m.text) > 100:
            bot.send_message(m.chat.id, Answers.num_range)
            return

        try:
            audio = bot.audio.from_local(m)
        except FileNotFoundError:
            bot.send_message(m.chat.id, Answers.file_lost)
            return

        if audio.content_type == 'audio':
            audio.transform_eyed3 = user.transform_eyed3

        user.curr_state = States.boosting
        session.commit()
        audio.bass_boost(int(m.text))

        if audio.content_type == 'audio':
            bot.send_audio(m.chat.id, audio.open_bass())
        else:
            bot.send_voice(m.chat.id, audio.open_bass())

        user.curr_state = States.asking_bass_pwr

    @bot.message_handler(func=lambda m: bot.db.check_state(message=m, state=States.start))
    @bot.db.provide_session
    def after_start(message, session):
        bot.send_message(message.chat.id, Answers.after_start)
        dude = bot.db.get_user(message, session=session)
        dude.curr_state = States.asking_for_stuff

    @bot.message_handler(func=lambda m: this_is_downloadable_link(m.text))
    @bot.db.provide_session
    def got_yt_link(message, session):
        get_audio(message, session, message.text)

    @bot.message_handler()
    def got_text(message):
        bot.send_message(message.chat.id, Answers.got_text)
