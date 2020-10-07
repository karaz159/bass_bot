#!/usr/bin/env python3
"""
main module with all bot commands
"""
import random

from config import bot, log, SERVER_FLAG
from helpers import yt_link_check
from models import Answers, States
from server import serv_start
from sqlworker import alt_bool, check_state, get_user, listener, register_dude, set_column

bot.set_update_listener(listener)


if __name__ == "__main__":
    if SERVER_FLAG:
        serv_start()
        log.info('Running in server mode')
    else:
        bot.remove_webhook()
        log.info('Running in poll mode')
        bot.polling(none_stop=True)
