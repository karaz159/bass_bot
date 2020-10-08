#!/usr/bin/env python3
from config import sys_log, SERVER_FLAG
from server import serv_start
from app import bot

if __name__ == "__main__":
    if SERVER_FLAG:
        serv_start(bot)
        sys_log.info('Running in server mode')
    else:
        bot.remove_webhook()
        sys_log.info('Running in poll mode')
        bot.polling(none_stop=True)
