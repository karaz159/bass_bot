from os import getenv, makedirs, path
import logging
import telebot as tb

TOKEN = getenv('TOKEN')
assert TOKEN

DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')
DB_USER = getenv('DB_USER', 'postgres')
DB_PASSWORD = getenv("DB_PASSWORD", 'password')
DB_NAME = getenv('DB', 'postgres')
LOG = getenv('LOG', 'INFO')
SERVER_FLAG = getenv('SERVER_FLAG', None)
DOWNLOAD_PATH = getenv('DOWNLOAD_PATH', '/opt/bass/download/')
BASS_PATH = getenv('BASS_PATH', "/opt/bass/boosted/")
LOG_PATH = getenv('LOG_FOLDER', '/var/log/bass_bot/')

DB_DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

WH_HOST = getenv('WH_HOST', '')
WH_PORT = int(getenv("WH_PORT", "8443"))
WH_LISTEN = getenv('WH_LISTEN', '0.0.0.0')
WH_SSL_CERT = getenv("SSL_CERT", '/certs/WH_cert.pem')
WH_SSL_PRIV = getenv('SSL_PRIV', '/certs/WH_pkey.pem')
WH_URL_BASE = "https://%s:%s" % (WH_HOST, WH_PORT)
WH_URL_PATH = "/%s/" % (TOKEN)

pathes = (DOWNLOAD_PATH, BASS_PATH, LOG_PATH)
for folder in pathes:
    if not path.exists(folder):
        makedirs(folder)

log = logging.getLogger('bass_boost')
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')

info_file_handler = logging.FileHandler(f'{LOG_PATH}info.log')
error_file_handler = logging.FileHandler(f'{LOG_PATH}error.log')
info_file_handler.setFormatter(formatter)
info_file_handler.setLevel(logging.INFO)
error_file_handler.setFormatter(formatter)
error_file_handler.setLevel(logging.ERROR)

log.addHandler(info_file_handler)
log.addHandler(error_file_handler)
log.setLevel(LOG)

bot = tb.TeleBot(TOKEN)
