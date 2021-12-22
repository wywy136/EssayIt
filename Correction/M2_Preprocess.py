# M2_Preprocess.py 输入文本、切分句子、标点转化等预处理工作
import re
import string
from nltk.tokenize import sent_tokenize


def Load(path):  # 从.txt文件中读取文章;这起始应该是M1return回的参数;raw文章即可,格式在后续步骤处理
    f = open(path)
    return f.read()


def Preprocess(context):
    # 洗去多余的句首空格、n空格、换行符、全角字符,并确保标点后有空格(数目不重要,后期可以过滤掉)作为分词/句标准;对:.这类数字标点要特殊考虑

    # 洗去多余的句首空格、n空格
    context = re.sub('  +', ' ', context)
    context = context.strip(' ')

    # 洗去全角字符
    context = context.replace("‘", "'")
    context = context.replace("’", "'")
    context = context.replace("“", '"')
    context = context.replace("”", '"')
    context = context.replace("？", '?')
    context = context.replace("！", '!')
    context = context.replace("。", '.')
    context = context.replace("，", ',')
    context = context.replace("：", ':')
    context = context.replace("；", ';')
    context = context.replace("（", '(')
    context = context.replace("）", ')')
    context = context.replace("''", '"')

    # 洗去bug字符
    context = context.replace('.?', '?')
    context = context.replace('".', '."')
    context = context.replace('ﬁ', 'fi')
    context = context.replace('ﬃ', 'ffi')

    # 添加易遗漏的区分空格
    context = context.replace("(", ' (')
    context = context.replace(")", ') ')
    context = context.replace(",", ', ')
    context = context.replace("?", '? ')
    context = context.replace('"', ' " ')
    context = context.replace("!", '! ')
    context = context.replace("…", '… ')
    context = context.replace("——", ' — ')  # 这是破折号—，连字符是-
    string.punctuation += '—'

    context_clean = []

    # 在非小数点/比例的.后+空格
    for i in range(len(context)):
        context_clean.append(context[i])
        if (context[i] == '.') & (i != 0) & (i != len(context)-1):
            if not ((context[i-1].isdigit()) & (context[i+1].isdigit())):  # 并非小数点
                context_clean.append(' ')
        elif (context[i] == ':') & (i != 0) & (i != len(context)-1):
            if not ((context[i-1].isdigit()) & (context[i+1].isdigit())):  # 并非比例
                context_clean.append(' ')
    context_clean = ''.join(context_clean)
    context_clean = re.sub(' +', ' ', context_clean)  # 多个空格->1个空格

    stn_seped = sent_tokenize(context_clean)

    # 将标点用空格隔开,不与单词粘连
    for i in range(len(stn_seped)):
        k = 0
        while k < len(stn_seped[i]):
            if k == len(stn_seped[i]) - 1:  # 末尾元素
                if stn_seped[i][-1] != '"':
                    stn_seped[i] = list(stn_seped[i])
                    stn_seped[i].insert(k, ' ')
                    k += 1
                    stn_seped[i] = ''.join(stn_seped[i])
                    break
                else:  # ."情况
                    stn_seped[i] = list(stn_seped[i])
                    stn_seped[i].insert(k-1, ' ')
                    k += 1
                    stn_seped[i] = ''.join(stn_seped[i])
                    break

            # 空格隔开标点,不考虑连字符-和括号()和单引号',括号在单词检错时要先去掉,再去查字典
            if (stn_seped[i][k] in string.punctuation) & (stn_seped[i][k] != '-') \
                    & (stn_seped[i][k] != '(') & (stn_seped[i][k] != ')') & (stn_seped[i][k] != '\''):
                if not ((stn_seped[i][k] == '.' or stn_seped[i][k] == ':') &
                        (stn_seped[i][k + 1].isdigit() & stn_seped[i][k - 1].isdigit())):  # 非数字、比分情况
                    stn_seped[i] = list(stn_seped[i])
                    stn_seped[i].insert(k, ' ')
                    k += 1
                    stn_seped[i] = ''.join(stn_seped[i])
            k += 1
        stn_seped[i] = re.sub(' +', ' ', stn_seped[i])

    return stn_seped


def Preprocess_Para(context):  # 分段函数
    context = context.replace("\r\n", '\n')
    context = context.replace("\r", '\n')
    para_seped_0 = context.split('\n')
    para_seped = []
    for i in range(0, len(para_seped_0)):
        if para_seped_0[i] == '':
            continue
        para_seped.append(para_seped_0[i])
    # n段
    para_seped_fin = []
    for i in range(0, len(para_seped)):
        temp = Preprocess(para_seped[i])
        para_seped_fin.append(temp)

    return para_seped_fin


if __name__ == '__main__':
    # context = Load('../Correction/M1_M3_Data/M1_context.txt')
    context = 'Surely many of us have expressed the following sentiment, or some variation on it, during our daily commutes to work: "People are getting so stupid these days!"'
    # for i in Preprocess(context, 0):
    #     print(i)
    # print()
    # for i in Preprocess(context, 1):
    #     print(i)
    # print()
    print(Preprocess_Para(context))
