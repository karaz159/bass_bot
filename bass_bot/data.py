class Answers:  # TODO middleware
    start = 'Hello there! Ready to boost your stuff, use /info for more details'
    reset = "Resetting your state back to normal"
    file_lost = "Damn, i've lost your file, can you send me another one?"
    got_document = "Sorry, but for now i don't support docs"

    turn_on = "Turning on"
    turn_off = "Turning off"
    random_bass = "random bass"
    random_tags = "random audio tags"
    info = ("All you need is to pass me some audio or voice \n"
            "Also you can change the way i behave with your stuff\n"
            "Try /random /transform !")
    got_text = info
    after_start = info
    numbers_needed = 'Please feed me some numbers from 0 to 100'
    num_range = 'I can accept numbers from 0 to 100'
    downloading = 'Downloading things, please wait'
    boosting = 'Boosting things, please wait'
    bye = 'Thanks for using bot, hope to see you soon. bye!'
    large_video = 'Video is larger than expected! 10 minutes max!'
    yt_failed = 'Something bad happend with youtube download ;c, check other video, please!'
    making_bass_with_power = 'Making your bass with power:'

    try:
        hm = open('./hm.ogg', 'rb')
    except FileNotFoundError:
        pass


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
    'z': z,
    'hz': hz
}
