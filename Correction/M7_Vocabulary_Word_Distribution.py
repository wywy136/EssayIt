# 文件2：M7_Vocabulary_Word_Distribution#词频统计
# 函数名：
# Word_Distribution_Occur
# Word_Distribution_Index
# 输入：分好句段的二维列表
# 返回：key为单词，value为词频的字典/key为单词，value为单词所在句子下标的字典


def Word_Distribution_Occur(word_seped):
    list1 = sum(word_seped, [])
    # print(list1)
    dict_occur = {}
    dict_occur = dict_occur.fromkeys(list1)
    word_list1 = list(dict_occur.keys())
    for i in word_list1:
        dict_occur[i] = list1.count(i)
    return dict_occur


def Word_Distribution_Index(word_seped):
    dict_index = {}
    for i in range(len(word_seped)):
        for j in range(len(word_seped[i])):
            dict_index.setdefault(word_seped[i][j], []).append(i)
    return dict_index
