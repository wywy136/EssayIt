from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import math
import heapq


def Load_Phrase(lang):
    if lang == 'cn':
        with open('./phrase_cn.txt', 'r', encoding='utf-8') as f:
            all = f.readlines()
    elif lang == 'en':
        with open('./phrase_en.txt', 'r', encoding='utf-8') as f:
            all = f.readlines()

    phrase = []
    meaning = []
    knowledge = []
    flag = 0
    knowledge_temp = ''
    for line in all:
        line = line.strip('\n')
        if flag == 1:
            flag = 0
            knowledge_temp = str(line)
            continue
        if len(line) == 0:
            flag = 1
            continue
        phrase.append(line.split(' ')[0:-1])
        meaning.append(line.split(' ')[-1])
        knowledge.append(knowledge_temp)

    phrase_string = []
    for phrase_one in phrase:
        string = ''
        for word in phrase_one:
            string += word
            string += ' '
        phrase_string.append(string)

    return phrase_string, meaning, knowledge


def softmax(score):
    total = 0
    for s in score:
        total += math.exp(s / 100)
    prob = []
    for s in score:
        prob.append(math.exp(s / 100) / total)
    one = 0
    for p in prob:
        one += p
    return prob


def findmax(prob, topk=3):
    max_num_index = map(prob.index, heapq.nlargest(topk, prob))
    return list(max_num_index)


def Main(phrase_list, meaning_list, knowledge_list, example_list, passage, wnd=6, move=2, threshold=65):
    ret_phr = []
    ret_mng = []
    ret_knw = []
    ret_exp = []
    for sentence in passage:
        score = []
        length = len(sentence.split(' '))
        topk = []
        if length <= wnd:
            for phrase in phrase_list:
                score.append(fuzz.token_set_ratio(sentence, phrase))
                prob = softmax(score)
                topk = findmax(prob, topk=3)
        else:
            part_test = ''
            start = 0
            end = start + wnd
            while end <= length:
                for i in range(wnd):
                    part_test += sentence.split(' ')[i + start]
                    part_test += ' '
                for phrase in phrase_list:
                    score.append(fuzz.ratio(part_test, phrase))
                start += move
                end += move
                prob = softmax(score)
                topk.append(findmax(prob, topk=1)[0])
                score = []
                part_test = ''

        final_phr = []
        final_score = []
        for index in topk:
            phr = phrase_list[index]
            final_phr.append(phr)
        for phr in final_phr:
            final_score.append(fuzz.token_set_ratio(sentence, phr))

        for i in range(len(final_score)):
            if final_score[i] >= threshold:
                ret_phr.append(final_phr[i])

    ret_phr = list(set(ret_phr))
    for phr in ret_phr:
        # ret_phr.append(phr)
        index = phrase_list.index(phr)
        ret_mng.append(meaning_list[index])
        ret_knw.append(knowledge_list[index])
        ret_exp.append(example_list[index])

    # 同维度list 短语/中文/语法知识
    return ret_phr, ret_mng, ret_knw, ret_exp


if __name__ == '__main__':
    p, m, k = Load_Phrase('cn')
    passage = ['Write a response in which you disuss the extent to which you agree or disagree with the recommendation and explain your reasoning for the position you take.']
    r1, r2, r3 = Main(p, m, k, passage)
    print(r1, r2, r3)
