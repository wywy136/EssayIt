# M3_SpellCorrection_Word.py 查字典修正
import re
import string
import M3_SpellCorrection_Ngram as Ng
import time


# 函数dic，读取字典到数组中，并根据ADD来更新词典
def dic():
    d = set()

    f = open('../Correction/dic/ALL-FIN(slow).txt', 'r', encoding='utf-8', errors='ignore')
    rr = f.readline()
    rr = rr.strip()
    while rr != '':
        if rr not in d:
            d.add(rr)
        rr = f.readline()
        rr = rr.strip()

    f_add = open('../Correction/dic/ADD.txt', 'r', encoding='utf-8', errors='ignore')
    rr = f_add.readline()
    rr = rr.strip()
    while rr != '':
        if rr not in d:
            d.add(rr)
        rr = f_add.readline()
        rr = rr.strip()

    f.close()
    f_add.close()
    # w = open('../Correction/dic/ALL-FIN.txt', 'w', encoding='utf-8', errors='ignore')
    # for i in d:
    #     w.write(i+'\n')
    # print('Dic is OK!')

    return d


global DIC_SUM
DIC_SUM = dic()
print()


def words0(text):
    return re.findall('[A-z]+', text)
# 提取单词列表


def known(word):  # 求交集
    return set(word).intersection(set(DIC_SUM))
# 返回在词典中的词


def words(text):
    return re.findall('[a-z]+', text.lower())
# 化小写,去标点


def edits1(word):
    if word in '?!.,'"":
        return word
    else:
        n = len(word)
        alphabet = "'abcdefghijklmnopqrstuvwxyz"
        return set([word[0:i]+word[i+1:] for i in range(n)] +                      # 删
                   [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] +  # 移
                   [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] +  # 换
                   [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])   # 插
# 生成编辑距离为1的词


def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))
# 生成编辑距离为2的词(为进行缩减,只选其中正确的词汇,即NWORDS中的)
# 递归调用了edits1函数


def correct(word, s, ns_pos, ners_tag, k, switch):
    global DIC_SUM

    # print('before:', word)

    if word == 'th':
        return 'the'

    if word in "\"\'":
        return word

    # 含()''""的情况
    if (word[0] == '(') & (word[-1] == ')'):
        return word
    if (word[0] == '"') & (word[-1] == '"'):
        return word
    if (word[0] == "'") & (word[-1] == "'"):
        return word
    if (word[0] == '(') or (word[0] == "'") or (word[0] == '"'):
        word = ''.join(list(word).pop(0))
    if (word[-1] == ')') or (word[-1] == "'") or (word[-1] == '"'):
        word = ''.join(list(word).pop(-1))

    # ."的情况
    if word == '."':
        return word

    if (word[0] == '$') or (word[0] == '￥'):  # 钱,跳过
        return word

    # 所有格的情况
    if ('\'s' in word) or ('s\'' in word):
        return word

    # print('before dic:', word)

    # 跳过标点、首位数字(小数点+比例+1st…)、字典匹配词(包括大小写)
    if (word in string.punctuation) or (word[0] in '1234567890') or (word in DIC_SUM):
        return word

    # print('after dic:', word)

    # 首词的情况
    if k == 0:
        # 若首字母大写
        if word[0] in 'ABCDEFGHIGKLMNOPQRSTUVWXYZ':
            if (word in DIC_SUM) or (word.lower() in DIC_SUM):
                # print(word.lower())
                return word
        # 若首字母未大写,则先按照正常流程,视该词是否在词典中,返回最适合词,再将其大写

    else:
        if (word in DIC_SUM) or (word.lower() in DIC_SUM):
            return word

    # 标注为专有名词的情况
    if (ns_pos[k][1] == 'NNP') or (ns_pos[k][1] == 'NNPS'):  # 专有名词/命名实体不做处理
        return word

    # 识别为命名实体的情况
    if k in ners_tag:
        print('NERS')
        return word

    print('rest:', word)

    if len(word) < 3:
        candidates = known([word]) or known(edits1(word)) or [word]
    else:
        candidates = known([word]) or known(edits1(word)) or known(edits2(word)) or [word]

    print('rest:', word)

    if switch == 1:
        pass
        # print(k)
        # print(word, candidates)

    # 不存在编辑距离2以内的词或只有1个,返回这个词
    if len(candidates) == 1:
        # print(candidates)
        for i in candidates:
            return i

    # 计算Ngram
    p0 = 0
    for i in candidates:
        s[k] = i  # 换上这个单词
        p1 = Ng.p_ngram(s, k)
        # print(s)
        # print('%s =' % i, p1)
        # print(p1)  # testsent
        # print(i)  # testsent
        if p1 > p0:
            p0 = p1
            word = i  # 替换成概率较大的词
    return word
# 返回在单词组s中,最可能出现的word;k是单词的下标


def keep(o, a):
    o = re.sub('[^a-zA-Z]', '', o)
    if o.isupper():
        return a.upper()
    elif o.istitle():
        return a.capitalize()
    else:
        return a
# 在字符串a中,保留字符串o的全大写/大写开头
