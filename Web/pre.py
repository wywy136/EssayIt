# M2_Preprocess.py 输入文本、切分句子、标点转化等预处理工作
# 暂时没做issue的处理函数
import re
import string


def Load(path):  # 从.txt文件中读取文章;这起始应该是M1return回的参数;raw文章即可,格式在后续步骤处理
    f = open(path)
    return f.read()


def Preprocess(context):
    # 洗去多余的句首空格、n空格、换行符、全角字符,并确保标点后有空格(数目不重要,后期可以过滤掉)作为分词/句标准;对:.这类数字标点要特殊考虑

    # 洗去多余的句首空格、n空格
    context = re.sub('  +', ' ', context)
    context = context.strip(' ')

    # 洗去换行符
    context = context.replace("\r\n", ' ')
    context = context.replace("\r", ' ')
    context = context.replace("\n", ' ')

    # 洗去全角字符
    context = context.replace("‘", "'")  # 可能是don't类，不作为依据
    context = context.replace("’", "'")  # 可能是don't类，不作为依据
    context = context.replace("“", '"')
    context = context.replace("”", '"')
    context = context.replace("？", '?')
    context = context.replace("！", '!')
    context = context.replace("。", '.')  # 可能是小数点，需要匹配空格切分
    context = context.replace("，", ',')
    context = context.replace("：", ':')  # 可能是比分，不作为依据
    context = context.replace("；", ';')
    context = context.replace("（", '(')
    context = context.replace("）", ')')
    context = context.replace("''", '"')

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
    for i in range(0, len(context)):
        context_clean.append(context[i])
        if (context[i] == '.') & (i != 0) & (i != len(context)-1):
            if not ((context[i-1].isdigit()) & (context[i+1].isdigit())):  # 并非小数点
                context_clean.append(' ')
        elif (context[i] == ':') & (i != 0) & (i != len(context)-1):
            if not ((context[i-1].isdigit()) & (context[i+1].isdigit())):  # 并非比例
                context_clean.append(' ')
    context_clean = ''.join(context_clean)
    context_clean = re.sub(' +', ' ', context_clean)  # 多个空格->1个空格

    # 先按. 分句;再在句内用? /! /… 分句;其它标点不作为分句标准
    stn_seped = []

    # 分句并补回split函数去掉的标点
    context_clean = context_clean.split('. ')
    for i1 in context_clean:
        if i1 == '':
            continue
        if i1[-1] != '.':  # 最后1句的遗漏
            i1 += '.'  # 补上'.'

        i1 = i1.split('! ')
        for i2 in i1:
            if i2[-1] != '.':
                i2 += '!'
            i2 = i2.split('? ')
            for i3 in i2:
                if (i3[-1] != '.') & (i3[-1] != '!'):
                    i3 += '?'
                i3 = i3.split('… ')
                for i4 in i3:
                    if (i4[-1] != '.') & (i4[-1] != '!') & (i4[-1] != '?'):
                        i4 += '…'
                    if (i4 == '') or ((len(i4) == 1) & (i4 in string.punctuation)):
                        continue
                    stn_seped.append(i4)
    # 此时每句的末尾必然带标点

    # 将标点用空格隔开,不与单词粘连
    for i in range(0, len(stn_seped)):
        k = 0
        while k < len(stn_seped[i]):
            if k == len(stn_seped[i]) - 1:  # 末尾元素
                stn_seped[i] = list(stn_seped[i])
                stn_seped[i].insert(k, ' ')
                k += 1
                stn_seped[i] = ''.join(stn_seped[i])
                break

            # 空格隔开标点,不考虑连字符-和括号()和单引号',括号在单词检错时要先去掉,再去查字典
            if (stn_seped[i][k] in string.punctuation) & (stn_seped[i][k] != '-') \
                    & (stn_seped[i][k] != '(') & (stn_seped[i][k] != ')') & (stn_seped[i][k] != '\''):
                if not ((stn_seped[i][k] == '.' or stn_seped[i][k] == ':') &
                        (stn_seped[i][k + 1].isdigit() & stn_seped[i][k - 1].isdigit())):  # 非数字、非比分情况
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
        para_seped_fin.append(Preprocess(para_seped[i]))
    # n段-k句

    return para_seped_fin


if __name__ == '__main__':
    context = Load('../Correction/M1_M3_Data/M1_context.txt')
    # for i in Preprocess(context, 0):
    #     print(i)
    # print()
    # for i in Preprocess(context, 1):
    #     print(i)
    # print()
    print(Preprocess_Para(context))
