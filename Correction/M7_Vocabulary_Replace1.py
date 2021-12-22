from nltk.corpus import stopwords
import M7_Vocabulary_SynonymDict
import M7_Vocabulary_Replace0
import math


def pos_match(p, definition):
    definition = definition[0:4]
    if definition == p:
        return True
    else:
        return False


def Replace1(processed, processedraw, i, lang):
    num = len(sum(processedraw, []))
    stoplist = stopwords.words('english')
    evaluation1_2_key = []
    evaluation1_2_position = []
    evaluation1_2_replace = []
    evaluation1_2_symbol = []
    symbolist = []
    dict_list = [[], [], [], [], []]  # 导入五个词典

    dict_00 = []
    with open('../Correction/level-dic/dict00.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_00.append(ip.strip("\n"))
    file.close()

    dict_0 = []
    with open('../Correction/level-dic/dict0.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_0.append(ip.strip("\n"))
    file.close()
    dict_list[0] = dict_0

    dict_1 = []
    with open('../Correction/level-dic/dict1.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_1.append(ip.strip("\n"))
    file.close()
    dict_list[1] = dict_1

    dict_2 = []
    with open('../Correction/level-dic/dict2.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_2.append(ip.strip("\n"))
    file.close()
    dict_list[2] = dict_2

    dict_3 = []
    with open('../Correction/level-dic/dict3.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_3.append(ip.strip("\n"))
    file.close()
    dict_list[3] = dict_3

    dict_4 = []
    with open('../Correction/level-dic/dict4.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_4.append(ip.strip("\n"))
    file.close()
    dict_list[4] = dict_4

    dict_v = []
    with open('../Correction/level-dic/dict_v_adj_adv.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_v.append(ip.strip("\n"))
    file.close()

    most_100 = []
    with open('../Correction/level-dic/most_100_raw.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                most_100.append(ip.strip("\n"))
    file.close()

    sum_list = []
    sum_list1 = []
    for p in range(0, i):
        sum_list = sum_list + dict_list[p]
    for p in dict_00:
        sum_list.append(p)
    lowerlist = sum_list
    for p in range(i, 5):
        sum_list1 = sum_list1 + dict_list[p]
    higherlist = sum_list1

    excesslist = M7_Vocabulary_Replace0.Replace0(processedraw, lang)[2]
    for i in range(len(processed)):
        for j in processed[i]:
            if j[0] in excesslist:
                symbol = []
                symbol.append(j[0])
                symbol.append(str(0))
                evaluation1_2_symbol.append(symbol)

    for i in range(len(processed)):
        for j in processed[i]:
            if j[0] not in stoplist and j[0] in dict_v and j[0] in most_100 and j[0] in lowerlist:
                symbol = []
                symbol.append(j[0])
                symbol.append(str(1))
                evaluation1_2_symbol.append(symbol)
    for i in evaluation1_2_symbol:
        symbolist.append(i[0])

    for i in range(len(processed)):
        for p in processed[i]:
            if p[0] in symbolist and p[0] in dict_v:
                    listnotall = []
                    lemmadict = M7_Vocabulary_SynonymDict.lemmas(p[0])
                    for k,v in lemmadict.items():
                        if pos_match(str(p[1]), str(k)):
                            listnotall.append(str(k))
                            listnotall.append(list(v))
                    if len(listnotall) > 0:
                        evaluation1_2_key.append(p[0])
                        position = []
                        position.append(i)
                        position.append(processed[i].index(p))
                        evaluation1_2_position.append(position)
                        evaluation1_2_replace.append(listnotall)
    leng=0
    finalnum = []
    for i in evaluation1_2_symbol:
        if i[1] == "1" and i[0] not in finalnum:
            finalnum.append(i[0])
            leng = leng+1
    score3_2 = math.ceil(25-float(150/num)*leng)
    if score3_2 < 0:
        score3_2 = 0
    length = len(evaluation1_2_key)
    eva_list = [[] for row in range(length)]
    for i in range(length):
        if evaluation1_2_key[i] in excesslist:
          eva_list[i].append(evaluation1_2_key[i])
          eva_list[i].append(evaluation1_2_position[i])
          eva_list[i].append(evaluation1_2_replace[i])
          eva_list[i].append("0")
        else :
          eva_list[i].append(evaluation1_2_key[i])
          eva_list[i].append(evaluation1_2_position[i])
          eva_list[i].append(evaluation1_2_replace[i])
          eva_list[i].append("1")

    if lang == 'cn':
        eva = "您的单词高级程度得分为" + str(score3_2) + "分"
    elif lang == 'en':
        eva = "Your score of high level vocabulary is " + str(score3_2)
    return score3_2, eva, eva_list
