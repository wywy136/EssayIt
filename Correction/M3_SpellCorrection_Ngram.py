# M3_SpellCorrection_Ngram.py 巴赫的Ngram模块
import re
import string
import operator
import time


def cleanText(input):
    input = re.sub(r'<[^{}]*>', '', input)  # 去除包含在……}中的内容
    input = re.sub(r'{[^{}]*}', '', input)
    input = re.sub(u"\\[.*?]", '', input)
    input = re.sub(r'[^a-zA-Z0-9\s]', '', input)
    input = re.sub(r"[^A-Za-z]", " ", input)
    input = re.sub('\[[0-9]*\]', "", input)  # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input)  # 把连续多个空格替换成一个空格
    input = input.lower()  # 变小写
    # input = bytes(input)#.encode('utf-8')
    # 把内容转换成utf-8格式以消除转义字符
    # input = input.decode("ascii", "ignore")
    return input


def cleanInput(input):
    cleanInput = []
    input = input.split(' ')  # 以空格为分隔符，返回列
    for item in input:
        item = item.strip(string.punctuation)  # string.punctuation获取所有标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):  # 找出单词，包括i,a等单个单词
            cleanInput.append(item)
    return cleanInput


def getNgrams(input, n):
    input = cleanInput(input)
    input = transdigit(input)
    output = {}
    for i in range(len(input) - n + 1):
        ngramTemp = " ".join(input[i:i + n])
        if ngramTemp not in output:
            output[ngramTemp] = 1
        else:
            output[ngramTemp] += 1
    return output


def transdigit(clean):
    for i in range(len(clean)):
        if clean[i][0] in '1234567890':  # 诸如1.2、3:5、21th
            clean[i] = 'NUM'
    return clean


def training1(input):
    summ1 = 0
    ngrams1 = getNgrams(input, 1)
    sortedNGrams1 = sorted(ngrams1.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(len(sortedNGrams1)):
        summ1 = summ1 + sortedNGrams1[i][1] + 1

    # global NWORDS
    # NWORDS = defaultdict(list)
    # for (key, value) in sortedNGrams1:
    #     NWORDS[key] = value

    numlist1 = []
    for i in range(len(sortedNGrams1)):
        numlist1.append((sortedNGrams1[i][1] + 1) / summ1)
    return sortedNGrams1, numlist1, summ1


def training(input):
    # sortedGrams1, numlist1, summ1= training1(input)
    summ = 0
    ngrams = getNgrams(input, 2)
    sortedNGrams = sorted(ngrams.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(len(sortedNGrams)):
        summ = summ + sortedNGrams[i][1] + 1
    numlist = []
    for i in range(len(sortedNGrams)):
        # for j in range(len(sortedGrams1)):
        #     temp = sortedNGrams[i][0].split(' ')
        #     if sortedGrams1[j][0] == temp[0]:
        numlist.append((sortedNGrams[i][1] + 1) / summ)  # (sortedNGrams[i][1]+1)/(sortedGrams1[j][1]+1))

    return sortedNGrams, numlist, summ


# 计算二元搭配的条件概率
def calprobability(archive1, prob1, summ1, archive, prob, summ, w1, w2):
    pro = 0
    # 搭配存在的情况下
    for i in range(len(archive)):
        if archive[i][-1][0] == w1 and archive[i][-1][1] == w2:
            for m in range(len(archive1)):
                if w1 == archive1[m][0]:
                    pro = prob[i] / prob1[m]
                    # if __name__ == '__main__':
                    #     print('正常', w2, '|', w1, pro)
                    return pro

    return newpro[0]
    # if pro == 0:
    #     if w1 in words:
    #         pro = newpro[0]  # 最小搭配条件概率
    #         # pro = (1/summ)/prob1[i]
    #         if __name__ == '__main__':
    #             print('异常1', w2, '|', w1, pro)
    #         return pro
    #
    # # 搭配不存在
    # if pro == 0:
    #     pro = newpro[0]  # 最小搭配条件概率
    #     if __name__ == '__main__':
    #         print('异常2', w2, '|', w1, pro)

    return pro


def p_ngram(sentence, number):
    cleanInput = []
    # print('sentence_ngram=', sentence)
    for item in sentence:
        item = item.strip(string.punctuation)  # string.punctuation获取所有标点符号
        cleanInput.append(item)
    if number == 0:
        w1 = cleanInput[number]
        w2 = cleanInput[number + 1]
        w3 = cleanInput[number + 2]
    else:
        if number + 1 == len(cleanInput):
            w3 = cleanInput[number]
            w2 = cleanInput[number - 1]
            w1 = cleanInput[number - 2]
        else:
            w2 = cleanInput[number]
            w3 = cleanInput[number + 1]
            w1 = cleanInput[number - 1]
    # return w1,w2,w3

    p1 = calprobability(archive1, prob1, summ1, archive, prob, summ, w1, w2)
    p2 = calprobability(archive1, prob1, summ1, archive, prob, summ, w2, w3)
    return p1 * p2


# # 以下为训练结果保存代码,仅在第1次调用
# content = open("M1_M3_Data/W14-1713.txt", encoding='UTF-8').read()  # open中的是txt训练样本
# archive, prob, summ = training(content)  # data为TXT格式即可
# archive1, prob1, summ1 = training1(content)
# print()
# f = open('M1_M3_Data/archine.txt', 'w', encoding='UTF-8')
# i = 0
# for i in range(len(archive)):
#     f.write(archive[i][0].replace('\n', ' '))
#     f.write('|||')
#     f.write(str(prob[i]).replace('\n', ' '))
#     f.write('|||')
#     f.write(str(archive[i][1]))
#     f.write('\n')
# f.write(str(summ))
# f.close()
#
# f1 = open('M1_M3_Data/archine1.txt', 'w', encoding='UTF-8')
# i = 0
# for i in range(len(archive1)):
#     f1.write(archive1[i][0].replace('\n', ' '))
#     f1.write('|||')
#     f1.write(str(prob1[i]).replace('\n', ' '))
#     f1.write('|||')
#     f1.write(str(archive1[i][1]))
#     f1.write('\n')
# f1.write(str(summ1))
# f1.close()

# test
print("M3_N_gram_test:")
test_time = time.time()

# 调用训练所得结果
f = open('../Correction/M1_M3_Data/archine.txt', encoding='UTF-8')
r = f.readlines()
i = 0
archive = []
prob = []
times = []
summ = 0
for i in range(len(r)-1):
    temp = r[i].strip('\n').split('|||')
    archive.append([temp[0], temp[1]])
    times.append(float(temp[2]))
    prob.append(float(temp[1]))
summ = int(r[i+1])
f.close()

# 训练补充语句1:增添split
for i in range(len(archive)):
    temp = archive[i][0].split(' ')
    archive[i].append(temp)

f = open('../Correction/M1_M3_Data/archine1.txt', encoding='UTF-8')
r = f.readlines()
i = 0
archive1 = []
prob1 = []
time1 = []
summ1 = 0
for i in range(len(r)-1):
    temp = r[i].strip('\n').split('|||')
    archive1.append([temp[0], temp[1], temp[2]])
    time1.append(float(temp[2]))
    prob1.append(float(temp[1]))
summ1 = int(r[i+1])

# 训练补充语句2:建立单词set
words = set()
for i in range(len(archive1)):
    words.add(archive[i][0])

k = 5
old = []
new = []
newpro = []
old.append(len(archive1)*(len(archive1)-1)/2-len(archive))
for i in range(k+1):  # 1-5
    old.append(times.count(i+1))
# print('old', old)
new.append(old[1]/old[0])
for i in range(1, k+1):  # 1-5
    new.append(((i+1)*old[i+1]/old[i]-i*(k+1)*old[k+1]/old[1])/(1-(k+1)*old[k+1]/old[1]))
for i in range(0, k+1):  # 0-5
    newpro.append(new[i] / summ)
# print('new', new)
# print('summ', summ)
# print('newpro', newpro)
for i in range(len(times)):
    if times[i] == 1:
        prob[i] = newpro[1]
    elif times[i] == 2:
        prob[i] = newpro[2]
    elif times[i] == 3:
        prob[i] = newpro[3]
    elif times[i] == 4:
        prob[i] = newpro[4]
    elif times[i] == 5:
        prob[i] = newpro[5]

# test
print("M3_N_gram_test:final")
print(time.time() - test_time)


if __name__ == '__main__':
    sentence1 = 'I am a good student in my class.'  # 待求句子
    sentence2 = "I am a best student in my class."
    sentence3 = "I am oh good student in my class."
    ans1 = p_ngram(sentence1.split(' '), 2)
    ans2 = p_ngram(sentence2.split(' '), 2)
    ans3 = p_ngram(sentence3.split(' '), 2)
    print(sentence1, ans1)
    print(sentence2, ans2)
    print(sentence3, ans3)


    # # a|b 的概率集
    # prolist = []
    # pro = 0
    # 搭配存在的情况下
