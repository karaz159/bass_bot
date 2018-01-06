import random
def transform(word):
    shit  = ''
    for i in word.lower():
        if i == 'а': # РУССКАЯ БЛЯТЬ!
            shit += random.choice(('@', 'A','а'))
        elif i == 'б':
            shit += random.choice(('B','8','Б'))
        elif i == 'в':
            shit += random.choice(('V','В'))
        elif i == 'г':
            shit += random.choice(('G','Г'))
        elif i == 'д':
            shit += random.choice(('D','d','д','Д','t'))
        elif i == 'е':
            shit += random.choice(('3','E'))
        elif i == 'ж':
            shit += random.choice(('J','ZH'))
        elif i == 'з':
            shit += random.choice(('ZZ','Z'))
        elif i == 'и':
            shit += random.choice(('I', 'i'))
        elif i == 'й':
            shit += random.choice(('I','i'))
        elif i == 'к':
            shit += random.choice(('k','K'))
        elif i == 'л':
            shit += random.choice(('LL','L', 'l'))
        elif i == 'м':
            shit += random.choice(('М','ММ'))
        elif i == 'н':
            shit += random.choice(('н','Н'))
        elif i == 'о':
            shit += random.choice(('О','0'))
        elif i == 'п':
            shit += random.choice(('P','5'))
        elif i == 'р':
            shit += random.choice(('r','R'))
        elif i == 'с':
            shit += random.choice(('С','с','S','$','$$'))
        elif i == 'т':
            shit += random.choice(('Т','т','t'))
        elif i == 'у':
            shit += random.choice(('у','Y'))
        elif i == 'ф':
            shit += random.choice(('F','Ф'))
        elif i == 'х':
            shit += random.choice(('Х','H'))
        elif i == 'ц':
            shit += random.choice(('Ц','С'))
        elif i == 'ч':
            shit += random.choice(('Ч','CH','cH'))
        elif i == 'ш':
            shit += random.choice(('SH','sH','Sh','Ш'))
        elif i == 'щ':
            shit += random.choice(('SH','sH','Sh','Щ'))
        elif i == 'ъ':
            shit += random.choice(('Б','Ъ','ь','ъ'))
        elif i == 'ы':
            shit += random.choice(('bi','Ы'))
        elif i == 'ь':
            shit += random.choice(('Б','Ъ','ь','ъ'))
        elif i == 'э':
            shit += random.choice(('Э','э'))
        elif i == 'ю':
            shit += random.choice(('ю','Ю'))
        elif i == 'я':
            shit += random.choice(('я','Я'))
#АНГЛИЦКИЙ
        elif i == 'a':
            shit += random.choice((i,'@','A'))
        elif i == 'b':
            shit += random.choice((i,'8','B'))
        elif i == 'c':
            shit += random.choice((i,'CC','C'))
        elif i == 'd':
            shit += random.choice((i,'D','t'))
        elif i == 'e':
            shit += random.choice((i,'E','3'))
        elif i == 'f':
            shit += random.choice((i,'F'))
        elif i == 'g':
            shit += random.choice((i,'G'))
        elif i == 'h':
            shit += random.choice((i,'H'))
        elif i == 'i':
            shit += random.choice((i,'I'))
        elif i == 'j':
            shit += random.choice((i,'J'))
        elif i == 'k':
            shit += random.choice((i,'K'))
        elif i == 'l':
            shit += random.choice((i,'L'))
        elif i == 'm':
            shit += random.choice((i,'M'))
        elif i == 'n':
            shit += random.choice((i,'N'))
        elif i == 'o':
            shit += random.choice((i,'O','0'))
        elif i == 'p':
            shit += random.choice((i,'P','5'))
        elif i == 'r':
            shit += random.choice((i,'R'))
        elif i == 's':
            shit += random.choice((i,'S','$$','$'))
        elif i == 't':
            shit += random.choice((i,'T'))
        elif i == 'u':
            shit += random.choice((i,'U'))
        elif i == 'v':
            shit += random.choice((i,'V'))
        elif i == 'w':
            shit += random.choice((i,'W'))
        elif i == 'x':
            shit += random.choice((i,'X','XX'))
        elif i == 'y':
            shit += random.choice((i,'Y'))
        elif i == 'z':
            shit += random.choice((i,'Z'))
        else:
            shit += i
    return shit
