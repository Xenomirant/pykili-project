import random, sys, secrets, string, json, os
from zxcvbn import zxcvbn
rus_alph='йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
eng_alph='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
rus_vows='ёуеыаоэяию'
rus_cons='йцкнгшщзхъфвпрлджчсмтьб'
eng_cons='qwrtypsdfghjklzxcvbnm'
eng_vows='euioa'

def ins_word():
    word=input('Введите кодовое слово на кириллице или латинице: ')

    return word

def get_lang(word):
    rus_count=0
    eng_count=0
    for i in range(len(word)):
        for j in range(len(rus_alph)):
            if word[i]==rus_alph[j]:
                rus_count += 1

    for i in range(len(word)):
        for j in range(len(eng_alph)):
            if word[i]==eng_alph[j]:
                eng_count += 1

    if eng_count==len(word):
        lang='eng'
    if rus_count==len(word):
        lang='rus'
    if (rus_count!=len(word)) and (eng_count!=len(word)):
        sys.exit('Ошибка! Введите слово повторно')

    return lang

def get_chars(word, lang):
    word=word.lower()
    chars=list(word)
    cons=[]
    vows=[]
    if lang=='rus':
        for i in range(len(word)):
            if chars[i] in rus_cons:
                cons.append(chars[i])
            elif chars[i] in rus_vows:
                vows.append(chars[i])
    if lang=='eng':
        for i in range(len(word)):
            if chars[i] in eng_cons:
                cons.append(chars[i])
            elif chars[i] in eng_vows:
                vows.append(chars[i])
    if len(vows)==0 or len(cons)==0:
        sys.exit('Ошибка! Введите слово повторно')
    return cons,vows

def change(cons, vows, lang):
    password=''
    r_num = -1
    vows_=vows
    cons_=cons
    if (len(vows_)==1) and (lang=='rus'):
        vows_.append(secrets.choice(rus_vows))
    if (len(vows_)==1) and (lang=='eng'):
        vows_.append(secrets.choice(eng_vows))
    r_num=secrets.randbits(1)
    if (len(vows_)==2) and (r_num==0) and (lang=='rus'):
        vows_.append(secrets.choice(rus_vows))
    elif (len(vows_)==2) and (r_num==1) and (lang=='rus'):
        vows_.append(secrets.choice(rus_vows))
        vows_.append(secrets.choice(rus_vows))
    if (len(vows_)==2) and (r_num==0) and (lang=='eng'):
        vows_.append(secrets.choice(eng_vows))
    elif (len(vows_)==2) and (r_num==1) and (lang=='eng'):
        vows_.append(secrets.choice(eng_vows))
        vows_.append(secrets.choice(eng_vows))
    if len(vows)>1:
        r_num=secrets.randbits(1)
        if r_num==0:
            password=password+secrets.choice(vows_)
            vows_.remove(password[-1])
        r_num=secrets.randbits(1)
        for i in range(len(word)+1):
            if (r_num==0) and (len(cons_)!=1):
                password=password+secrets.choice(cons_)
                cons_.remove(password[-1])
            elif (r_num==1) and (len(cons_)>2):
                for i in range(2):
                    password=password+secrets.choice(cons_)
                    cons_.remove(password[-1])
            if (len(vows_)==1) and (len(cons_)==1):
                break
            if len(vows_)>1:
                password=password+secrets.choice(vows_)
                vows_.remove(password[-1])
        password=password+cons_[0]
        cons_.remove(password[-1])
        password=password+vows_[0]
        vows_.remove(password[-1])
    chars=list(password)
    for i in range(len(chars)):
        r_num=secrets.randbits(1)
        if r_num==0:
            chars[i] = chars[i].upper()
    password=''.join(chars)
    r_num=secrets.randbits(1)
    if (r_num==0):
        password=''.join(secrets.choice(string.punctuation) for i in range(secrets.randbits(2)))+password
    elif (r_num==1):
        password=password+''.join(secrets.choice(string.punctuation) for i in range(secrets.randbits(2)))
    return password

def find_min(data):
    res=data[0]
    res_num=0
    for i in range(len(data)):
        if data[i]<res:
            res=data[i]
            res_num=i
    return res, res_num

pass_count=input('введите колличество желаемых паролей: ')
passlist=[]
passlist_res=[]
if not pass_count.isdigit():
    sys.exit('Ошибка! Введите число')
for i in range(int(pass_count)):
    passlist_res.append(0)
    passlist.append(0)
word=ins_word()
lang=get_lang(word)
min=find_min(passlist_res)
elem_count=0
for i in range(1000):
    cons, vows = get_chars(word, lang)
    password = change(cons, vows, lang)
    results=zxcvbn(password, user_inputs=word)
    if elem_count < len(passlist_res):
        passlist_res[elem_count]=int(results['guesses'])
        passlist[elem_count]=(password, json.dumps(results, ensure_ascii=False, indent=4, default=str))
        elem_count = elem_count + 1
        continue
    min, min_i=find_min(passlist_res)
    if int(results['guesses'])>min:
        passlist_res[min_i]=int(results['guesses'])
        passlist[min_i]=(password, json.dumps(results, ensure_ascii=False, indent=4, default=str))

res = [[ i for i, j in passlist],[ j for i, j in passlist]]
for i in range(len(passlist)):
    print(res[0][i])
    print(res[1][i])
os.system('pause')


