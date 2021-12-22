# 文件4：M7_Vocabulary_Replace0#替换使用次数过多的词
# 函数名：Replace0
# 输入：key为单词，value为词频的词典
# 返回：得分，建议修改的单词列表
from nltk.corpus import stopwords


def Word_Distribution_Occur(word_seped):
    list1=sum(word_seped,[])
    dict_occur={}
    dict_occur=dict_occur.fromkeys(list1)
    word_list1=list(dict_occur.keys())
    for i in word_list1:
        dict_occur[i]=list1.count(i)
    return dict_occur


def Replace0(word_seped, lang):
     dict_v = []
     with open('../Correction/level-dic/dict_v_adj_adv.txt', 'r', encoding='utf-8')as file:
        for ip in file.readlines():
            if ip != None:
                dict_v.append(ip.strip("\n"))
     file.close()
     Dict_Occur = Word_Distribution_Occur(word_seped)
     evaluation1_1_list=[]
     total_num = 0
     for key, value in Dict_Occur.items():
         total_num = total_num + value
     threshold=int(4*(total_num/150))
     stoplist=stopwords.words('english')
     score3_1=25
     delta=3
     for key,value in Dict_Occur.items():
         if key not in stoplist and key.lower() not in stoplist and key in dict_v:
                 if value > threshold and score3_1 > 0:
                     evaluation1_1_list.append(key)
                     score3_1 = score3_1-delta

     if lang == 'cn':
         if len(evaluation1_1_list) == 0:
             evaluation_1 = ["您的单词使用次数得分为" + str(score3_1) + "分,没有大量重复使用的情况"]
         else:
             evaluation_1 = ["您的单词使用次数得分为" + str(score3_1) + "分,",
                             ','.join(evaluation1_1_list) + "使用次数过多，建议替换"]
     elif lang == 'en':
         if len(evaluation1_1_list) == 0:
             evaluation_1 = ["Your score of word frequency is " + str(score3_1) + ", no words use frequently"]
         else:
             evaluation_1 = ["Your score of word frequency is " + str(score3_1) + ", ",
                             ', '.join(evaluation1_1_list) + " use frequently, you'd better replace it/them"]

     evaluation1_1 = ' '.join(evaluation_1)
     return score3_1, evaluation1_1, evaluation1_1_list
