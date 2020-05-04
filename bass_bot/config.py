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

WEBHOOK_HOST = ''
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)


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