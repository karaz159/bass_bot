from classes import BassBot
from config import TOKEN
from helpers import get_db_dsn
from models import BASE

bot = BassBot(TOKEN, get_db_dsn(), BASE)

