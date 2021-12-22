
sys.path.append('./M4_Error_Location')
import copy
import sys
import os
import time
import string
import threading
import multiprocessing
import M2_Preprocess as M2
import M3_SpellCorrection_Body as M3_Body
import M4_Grammar_Correction as M4
import M5
import M6_passive
import M6_declarative
import M6_compound
import M6_complex
import M6_eva
from stanfordcorenlp import StanfordCoreNLP
import M7_Vocabulary_Division  # 对分句进行分词
import M7_Vocabulary_Word_Distribution  # 词频,下标统计
import M7_Vocabulary_Richness  # 单词丰富度
import M7_Vocabulary_Replace0  # 替换使用次数过多的词
import M7_Vocabulary_Replace1  # 替换低级词汇为更高级近义词
import M7_Vocabulary_Count  # 文章字数是否合格
import M7_Vocabulary_Get_Score  # 计算总分
import M7_Vocabulary_ProcessDict  # 词形还原
import M8_Topic  # 主题评估
import M10_Phrase  # 短语识别
import M9_Htmlautomaker  # parallel自动生成


# 并行化函数
class MyProcess(multiprocessing.Process):
    def __init__(self, func, args=()):
        super(MyProcess, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result   # 如果子线程不使用join方法，此处可能会报没有self.result的错误


def process(args):
    print('Multicore!')
    (context, pre_M5, pre_M6, pre_M8, pre_M10, weight) = args
    # # 评测语法模块F0.5用
    # gui_left_content = context.split('\n')
    # Grammar_corrected_context = M4.Grammar_Correction(gui_left_content)

    # 界面显示·左
    gui_left_content = M2.Preprocess_Para(context)

    # 转化预加载参数
    nlp = StanfordCoreNLP('../Correction/StanfordCoreNLP')
    fw = pre_M6[1]
    fw_pre = pre_M6[2]
    fw_depend = pre_M6[3]
    fw_pos = pre_M6[4]
    level = pre_M6[5]

    # print('fw_pre', fw_pre)
    fw_num = 0
    for i in fw_pre:
        temp = i.split(' ')
        for j in temp:
            if not ((j in string.punctuation) | (j == ' ')):
                fw_num += 1
    # print('fw_num', fw_num)

    # # F0.5test_without_Spell
    # Grammar_corrected_context = M4.Grammar_Correction(gui_left_content)

    print("=============Now Process Inception=============")
    start_time = time.time()
    print(time.time() - start_time)

    stn_seped = []
    for para in gui_left_content:
        for stn in para:
            stn_seped.append(stn)

    # print(str(stn_seped))

    my_num = 0
    for i in stn_seped:
        temp = i.split(' ')
        for j in temp:
            if not ((j in string.punctuation) | (j == ' ')):
                my_num += 1
    # print(my_num)
    spell_corrected_context = copy.deepcopy(stn_seped)

    # # M6 Sentence_Level
    print("=============M6 Loading and Using StanfordCoreNLP=============")
    print(time.time() - start_time)
    # nlp = StasnfordCoreNLP('../Correction/StanfordCoreNLP')
    nlp_depend = []  # nlp依存
    nlp_pos = []  # nlp标注
    for sent in spell_corrected_context:
        nlp_depend.append(nlp.dependency_parse(sent))
        nlp_pos.append(nlp.pos_tag(sent))

    print("=============M6 Classifying Sentence Pattern=============")
    print(time.time() - start_time)
    # print(level)
    # print(spell_corrected_context)
    M6_res = M6_eva.eva(spell_corrected_context, nlp_depend, nlp_pos, fw_pre, fw_depend, fw_pos, level)
    stat_sentence_passratio = float(int(M6_res[0][0]) / 100)  # 被动句比例
    stat_sentence_subjratio = 1 - stat_sentence_passratio  # 主动局比例
    stat_sentence_pararatio = float(int(M6_res[2][0]) / 100)  # 并列句比例
    stat_sentence_compratio = float(int(M6_res[3][0]) / 100)  # 复合句比例
    stat_sentence_simpratio = 1 - stat_sentence_pararatio - stat_sentence_compratio  # 简单句比例
    # print(stat_sentence_passratio)

    # M7
    print("=============M7 Generating Vocabulary Return=============")
    print(time.time() - start_time)
    word_seped = M7_Vocabulary_Division.Division(spell_corrected_context)
    dict_occur = M7_Vocabulary_Word_Distribution.Word_Distribution_Occur(word_seped)
    dict_index = M7_Vocabulary_Word_Distribution.Word_Distribution_Index(word_seped)
    process, processraw = M7_Vocabulary_ProcessDict.Processdict(word_seped)

    score3_3, eva3_3 = M7_Vocabulary_Count.Count(fw_num, my_num)
    score3_0, eva3_0 = M7_Vocabulary_Richness.Richness(dict_occur, my_num)
    score3_1, eva3_1, eva_list_3_1 = M7_Vocabulary_Replace0.Replace0(processraw)
    score3_2, eva3_2, eva_list = M7_Vocabulary_Replace1.Replace1(process, processraw, int(level) - 1)
    M7_score = int(M7_Vocabulary_Get_Score.Get_Score(score3_3, score3_1, score3_2, score3_0))
    M7_eva = [eva3_3, eva3_0, eva3_1, eva3_2]
    # print(len(eva_list))
    
    # M8 Topic
    print("=============M8 Generating Topic Return=============")
    print(time.time() - start_time)
    # M8
    st = spell_corrected_context  # 学生文章
    M8_score, M8_eva, M8_level, base64_stu,base64_fw = M8_Topic.call_on(st, fw_pre, pre_M8)
    stat_topic_level = M8_level

    # M3 Misspell
    print("=============M3 Checking Spell Errors=============")
    print(time.time() - start_time)

    # threads_for_spell = []
    # nthreads = 3
    # num_per_thread = len(stn_seped) // nthreads + 1
    #
    # for i in range(nthreads):
    #     p = MyProcess(M3_Body.main, args=(stn_seped[i * num_per_thread:(i + 1) * num_per_thread],
    #                   spell_corrected_context[i * num_per_thread:(i + 1) * num_per_thread], 1,
    #                   nlp_pos[i * num_per_thread:(i + 1) * num_per_thread]))
    #     threads_for_spell.append(p)
    #
    #
    # for i in range(nthreads):
    #     threads_for_spell[i].start()
    #
    # for i in range(nthreads):
    #     threads_for_spell[i].join()
    #
    # for i in range(nthreads):
    #     threads_for_spell[i].run()
    #
    # M3_res = [0, [], [], [], [], [], [], []]
    # res1 = [0, [], [], [], [], [], [], []]
    # res2 = [0, [], [], [], [], [], [], []]
    # res3 = [0, [], [], [], [], [], [], []]
    # res_from_single_process = [res1, res2, res3]
    # for i in range(nthreads):
    #     temp = threads_for_spell[i].get_result()
    #     res_from_single_process[i][0] += temp[0]
    #     for j in range(1, 8):
    #         for item in temp[j]:
    #             res_from_single_process[i][j].append(item)
    # M3_res[0] = res1[0] + res2[0] + res3[0]
    # for i in range(nthreads):
    #     for j in range(1, 8):
    #         for item in res_from_single_process[i][j]:
    #             if j == 1:
    #                 item += i * num_per_thread
    #             M3_res[j].append(item)

    M3_res = M3_Body.main(stn_seped, spell_corrected_context, 1, nlp_pos)
    wrongsent = M3_res[1]  # 错误句子下标
    pos_word = M3_res[2]  # 错误单词下标
    mis_spedded_word = M3_res[3]  # 错误单词
    sgted_word = M3_res[4]  # 建议替换单词
    Spell_corrected_context = M3_res[7]

    # M4 Grammar
    print("=============M4 Now=============")
    print(time.time() - start_time)
    # 10.22修改：
    # Grammar_corrected_context就是改完语法之后的句子，list型，和Spell_corrected_context对应
    # 代替原来 os.system('python ../Correction/shell.py') 做的事
    Grammar_corrected_context = M4.Grammar_Correction(Spell_corrected_context)

    print("=============M5 GEC Error Classifying=============")
    print(time.time() - start_time)

    lines_in_m2, lines_in_corrected, lines_in_source = M5.M5_Run_Scripts(Spell_corrected_context,
                                                                         Grammar_corrected_context,
                                                                         pre_M5)

    M5_res = M5.M5_Locate_Classify(wrongsent, pos_word, mis_spedded_word, sgted_word,
                                   lines_in_m2, lines_in_corrected, lines_in_source, my_num)

    suggestion = M5_res[0]
    spell_score = M5_res[1]
    grammar_score = M5_res[2]
    statistic = M5_res[3]
    stat_misspell_num = int(statistic[0].split(': ')[1])
    stat_nounerr_num = int(statistic[1].split(': ')[1])
    stat_verberr_num = int(statistic[2].split(': ')[1])
    stat_other_num = int(statistic[3].split(': ')[1])

    print("=============M10 Phrase=============")
    print(time.time() - start_time)
    phrase_string = pre_M10[0]
    meaning = pre_M10[1]
    knowledge = pre_M10[2]
    example = pre_M10[3]
    M10_res = M10_Phrase.Main(phrase_string, meaning, knowledge, example, Spell_corrected_context)

    print("=============Displaying on Browser=============")
    print(time.time() - start_time)

    M9_res = M9_Htmlautomaker.automaker(gui_left_content, suggestion, statistic, spell_score, grammar_score, M6_res, M7_score, M7_eva, M8_score, M8_eva, eva_list, context, weight, base64_stu, base64_fw, M10_res, word_seped)


    print("=============Now Process Completed=============")
    print(time.time() - start_time)

    # 教师端选项卡3：学生整体信息统计所需参数整理如下

    # stat_misspell_num  # 拼写错误数量,int
    # stat_nounerr_num  # 名词错误数量,int
    # stat_verberr_num  # 动词错误数量,int
    # stat_other_num  # 其他错误数量,int
    #
    # stat_sentence_pararatio  # 并列句比例,float
    # stat_sentence_compratio  # 复合句比例,float
    # stat_sentence_simpratio  # 简单句比例,float
    #
    # stat_sentence_passratio  # 被动句比例,float
    # stat_sentence_subjratio  # 主动句比例,float
    #
    # stat_topic_level  # 主题切合度等级标号,int,0 - 严重偏题，1 - 轻微偏题，2 - 完美切题

    stat_teacher = [[stat_misspell_num, stat_nounerr_num, stat_verberr_num, stat_other_num],
                    [stat_sentence_pararatio, stat_sentence_compratio, stat_sentence_simpratio],
                    [stat_sentence_passratio, stat_sentence_subjratio],
                    [stat_topic_level],
                    [spell_score, grammar_score, M7_score, M6_res[4], M8_score,
                     int((spell_score*weight[0]+grammar_score*weight[1]+M7_score*weight[2]+M6_res[4]*weight[3]+M8_score*weight[4])/sum(weight)+0.5)]]
    return M9_res, stat_teacher


def process_test(context, nlp_in):
    # 特殊处理:段尾:
    context = context.replace(":\r\n", ': ')

    # 转化预加载参数
    nlp = nlp_in
    # fw = pre_M6[1]
    # fw_pre = pre_M6[2]
    # fw_depend = pre_M6[3]
    # fw_pos = pre_M6[4]
    # level = pre_M6[5]

    print("=============Now Process Inception=============")
    start_time = time.time()
    print(time.time() - start_time)
    stn_seped = M2.Preprocess(context)
    # copy_context = copy.deepcopy(context)
    spell_corrected_context = copy.deepcopy(stn_seped)

    # # # M6 Sentence_Level
    # print("=============M6 Loading and Using StanfordCoreNLP=============")
    # print(time.time() - start_time)
    nlp_depend = []  # nlp依存
    nlp_pos = []  # nlp标注
    for sent in spell_corrected_context:
        nlp_depend.append(nlp.dependency_parse(sent))
        nlp_pos.append(nlp.pos_tag(sent))
    #
    # print("=============M6 Classifying Sentence Pattern=============")
    # print(time.time() - start_time)
    # # # 权重
    # print(level)
    # print(spell_corrected_context)
    # M6_res = M6_eva.eva(spell_corrected_context, nlp_depend, nlp_pos, fw_pre, fw_depend, fw_pos, level)

    # # M7
    # print("=============M7 Generating Vocabulary Return=============")
    # print(time.time() - start_time)
    # word_seped = M7_Vocabulary_Division.Division(spell_corrected_context)
    # dict_occur = M7_Vocabulary_Word_Distribution.Word_Distribution_Occur(word_seped)
    # dict_index = M7_Vocabulary_Word_Distribution.Word_Distribution_Index(word_seped)
    #
    # num = 150  # 输入词数(临时)
    # score3_3, eva3_3 = M7_Vocabulary_Count.Count(num, dict_occur)
    # score3_0, eva3_0 = M7_Vocabulary_Richness.Richness(dict_occur)
    # score3_1, eva3_1 = M7_Vocabulary_Replace0.Replace0(dict_occur)
    # score3_2, eva3_2, eva_list = M7_Vocabulary_Replace1.Replace1(dict_occur, dict_index, int(level) - 1)
    # M7_score = int(M7_Vocabulary_Get_Score.Get_Score(score3_3, score3_1, score3_2, score3_0))
    # M7_eva = [eva3_3, eva3_0, eva3_1, eva3_2]
    #
    # print("=============M8 Generating Topic Return=============")
    # print(time.time() - start_time)
    # # M8
    # st = spell_corrected_context  # 学生文章
    # M8_score, M8_eva, base64_stu, base64_fw = M8_Topic.call_on(st, fw_pre, pre_M8)
    # # topic = M8_Topic.predict_topic(doc_test=f)
    # # # print('topic', topic)
    # # file = "challenge"  # 主题
    # # titletopic = M8_Topic.predict_topic(doc_test = file)
    # # # print(file, titletopic)
    # # M8_score, M8_eva = M8_Topic.topicscore(topic, titletopic)
    # # # print(M8_score, M8_eva)

    print("=============M3 Checking Spell Errors=============")
    print(time.time() - start_time)

    threads_for_spell = []
    nthreads = 3
    num_per_thread = len(stn_seped) // nthreads + 1

    for i in range(nthreads):
        p = MyProcess(M3_Body.main, args=(stn_seped[i * num_per_thread:(i + 1) * num_per_thread],
                      spell_corrected_context[i * num_per_thread:(i + 1) * num_per_thread], 1,
                      nlp_pos[i * num_per_thread:(i + 1) * num_per_thread]))
        threads_for_spell.append(p)
        # print('part1.', i)
    # print('sym1')
    for i in range(nthreads):
        threads_for_spell[i].start()
    # print('sym2')
    for i in range(nthreads):
        threads_for_spell[i].join()
    # print('sym3')
    for i in range(nthreads):
        threads_for_spell[i].run()
    #     print('part2.', i)
    # print('sym4')
    M3_res = [0, [], [], [], [], [], [], []]
    res1 = [0, [], [], [], [], [], [], []]
    res2 = [0, [], [], [], [], [], [], []]
    res3 = [0, [], [], [], [], [], [], []]
    res_from_single_process = [res1, res2, res3]
    for i in range(nthreads):
        temp = threads_for_spell[i].get_result()
        res_from_single_process[i][0] += temp[0]
        for j in range(1, 8):
            for item in temp[j]:
                res_from_single_process[i][j].append(item)
    M3_res[0] = res1[0] + res2[0] + res3[0]
    for i in range(nthreads):
        for j in range(1, 8):
            for item in res_from_single_process[i][j]:
                if j == 1:
                    item += i * num_per_thread
                M3_res[j].append(item)

    print("+++++++++++")
    print(M3_res)

    wrongsent = M3_res[1]  # 错误句子下标

    pos_word = M3_res[2]  # 错误单词下标

    mis_spedded_word = M3_res[3]  # 错误单词

    sgted_word = M3_res[4]  # 建议替换单词

    Spell_corrected_context = M3_res[7]

    print("=============M4 Now=============")
    print(time.time() - start_time)
    # 10.22修改：
    # Grammar_corrected_context就是改完语法之后的句子，list型，和Spell_corrected_context对应
    # 代替原来 os.system('python ../Correction/shell.py') 做的事
    Grammar_corrected_context = M4.Grammar_Correction(Spell_corrected_context)

    print("=============M5 GEC Error Classifying=============")
    print(time.time() - start_time)
    # os.system('/opt/anaconda/envs/wangyu_pytorch1.x/bin/python ../Correction/M5_Error_Location/parallel_to_m2.py -orig ../Correction/M4_M5_Data/test.error.sent '
    #           '-cor ../Correction/M4_M5_Data/corrected.sent -out ../Correction/M4_M5_Data/src_prd')
    # 10.22
    # 传入M5.M5_Run_Scripts时，不带'\n'
    # 代替原来 os.system()
    lines_in_m2, lines_in_corrected, lines_in_source = M5.M5_Run_Scripts(Spell_corrected_context,
                                                                         Grammar_corrected_context,
                                                                         pre_M5)

    M5_res = M5.M5_Locate_Classify(wrongsent, pos_word, mis_spedded_word, sgted_word,
                                   lines_in_m2, lines_in_corrected, lines_in_source)

    suggestion = M5_res[0]
    spell_score = M5_res[1]
    grammar_score = M5_res[2]
    statistic = M5_res[3]

    # print("=============Displaying on Browser=============")
    # print(time.time() - start_time)
    # content = M2.Preprocess_Para(context)  # 界面显示·左
    #
    # M9_res = M9_Htmlautomaker.automaker(content, suggestion, statistic, spell_score, grammar_score, M6_res, M7_score, M7_eva, M8_score, M8_eva, eva_list, context, weight, base64_stu, base64_fw)
    #
    # print("=============Now Process Completed=============")
    # print(time.time() - start_time)
    # return M9_res


if __name__ == '__main__':
    path = '../Correction/M1_M3_Data/M1_context.txt'
    context = M2.Load('../Correction/M1_M3_Data/M1_context.txt')
    nlp = StanfordCoreNLP('../Correction/StanfordCoreNLP')
    process_test(context, nlp)
    # print([context])
    print(res)
