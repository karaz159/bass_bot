from classes import BassBot
from config import TOKEN
from helpers import get_db_dsn
from models import BASE
from telebot import apihelper

apihelper.RETRY_ON_ERROR = True

bot = BassBot(TOKEN, get_db_dsn(), BASE)
