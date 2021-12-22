# 文件3：M7_Vocabulary_Richness#词汇丰富度评估
# 函数名：Richness
# 输入：词频字典
# 返回：得分
from nltk.corpus import stopwords


def Richness(Dict_Occur, my_num, lang):
    score3_0 = 25
    delta = 3
    stoplist = stopwords.words('english')

    word = []
    for key,value in Dict_Occur.items():
        if key not in stoplist:
            word.append(key)
    word_num = len(word)
    total_num = 0
    # print(Dict_Occur)
    # for key, value in Dict_Occur.items():
    #     if key not in stoplist:
    #         total_num = total_num + value
    total_num=my_num
    ratio = word_num/total_num

    if lang == 'cn':
        evaluation_0 = "词汇丰富度较高!"
        if ratio < 0.7:
            if ratio > 0.6:
                score3_0 = score3_0 - delta
                evaluation_0 = "词汇丰富度偏低,可尝试同义词替换或灵活使用短语。在学习中注意词汇的积累。"
            else:
                if ratio > 0.5:
                    score3_0 = score3_0 - 2 * delta
                    evaluation_0 = "词汇丰富度低,可尝试同义词替换或灵活使用短语。在学习中注意词汇的积累。"
                else:
                    score3_0 = score3_0 - 3 * delta
                    evaluation_0 = "词汇丰富度过低,可尝试同义词替换或灵活使用短语。在学习中注意词汇的积累。"
        evaluation3_0 = "您的单词丰富度得分为" + str(score3_0)+"分," + evaluation_0
    elif lang == 'en':
        evaluation_0 = "rich vocabulary!"
        if ratio < 0.7:
            if ratio > 0.6:
                score3_0 = score3_0 - delta
                evaluation_0 = "vocabulary richness is a little low, try synonyms substitution or use phrases flexibly. Pay attention to the accumulation of vocabulary in learning."
            else:
                if ratio > 0.5:
                    score3_0 = score3_0 - 2 * delta
                    evaluation_0 = "vocabulary richness is low, try synonym substitution or flexible use of phrases. Pay attention to the accumulation of vocabulary in learning."
                else:
                    score3_0 = score3_0 - 3 * delta
                    evaluation_0 = "vocabulary richness is too low, try synonym substitution or flexible use of phrases. Pay attention to the accumulation of vocabulary in learning"
        evaluation3_0 = "Your score of vocabulary richness is " + str(score3_0)+", " + evaluation_0

    return score3_0, evaluation3_0
