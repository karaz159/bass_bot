from random import choice

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
hz = ('N3т', 'NE Y@sNo', '<UнKn0wн>', '4eг0')

ALPHABET = {
    'а': a,
    'б': b,
    'в': ('V', 'В'),
    'г': ('G', 'Г'),
    'д': d,
    'е': e,
    'ж': ('J', 'ZH'),
    'з': ('ZZ', 'Z', 'З', 'з'),
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
    'v': ('v', 'V'),
    'w': ('w', 'W'),
    'x': ('x', 'X', 'XX'),
    'y': ('y', 'Y'),
    'z': ('z', 'Z')
}

def transform(word):
    '''
    transforms any word to cringe
    '''
    shit = ''
    if word:
        for character in word.lower():
            try:
                shit += choice(ALPHABET[character]) # nosec
            except KeyError:
                shit += character
    else:
        shit = choice(hz) # nosec
    return shit
