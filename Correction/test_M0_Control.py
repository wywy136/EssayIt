import copy
import sys
import os
sys.path.append('./M4_Error_Location')
import M2_Preprocess as M2
import M3_SpellCorrection_Body as M3_Body
import M3_SpellCorrection_Sum as M3_Sum
import M4_Grammar_Correction as M4
import M5
import M6_passive
import M6_declarative
import M6_compound
import M6_complex
from stanfordcorenlp import StanfordCoreNLP
import M7_Vocabulary_Division  # 对分句进行分词
import M7_Vocabulary_Word_Distribution  # 词频,下标统计
import M7_Vocabulary_Richness  # 单词丰富度
import M7_Vocabulary_Replace0  # 替换使用次数过多的词
import M7_Vocabulary_Replace1  # 替换低级词汇为更高级近义词
import M7_Vocabulary_Count  # 文章字数是否合格
import M7_Vocabulary_Get_Score  # 计算总分
import M8_Topic  # 主题评估
import M9_Htmlautomaker  # parallel自动生成


def process(context):
    stn_seped = M2.Preprocess(context)
    copy_context = copy.deepcopy(context)
    spell_corrected_context = copy.deepcopy(stn_seped)

    # # # M6 Sentence_Level
    # nlp = StanfordCoreNLP('../Correction/StanfordCoreNLP')
    # nlp_depend = []  # nlp依存
    # nlp_pos = []  # nlp标注
    # for sent in spell_corrected_context:
    #     nlp_depend.append(nlp.dependency_parse(sent))
    #     nlp_pos.append(nlp.pos_tag(sent))
    #
    # # 权重
    # pass_w, decl_w, comp1_w, comp2_w = [1, 2, 3, 4]
    #
    # M6_pass = M6_passive.passive(spell_corrected_context, nlp_depend, nlp_pos)
    # # M6_pass[0] = '被动句比率:'+str(M6_pass[0])+'%'
    # # M6_pass[1] = '主被动得分:' + str(M6_pass[1])
    # # print('被动句比率', M6_pass[0], '%')
    # # print('主被动得分', M6_pass[1])
    # # print(M6_pass[2])
    #
    # M6_decl = M6_declarative.declarative(spell_corrected_context, nlp_depend, nlp_pos)
    # # M6_decl[0] = '陈述句比率:'+str(M6_decl[0])+'%'
    # # M6_decl[1] = '陈述句得分:' + str(M6_decl[1])
    # # print('陈述句比率', M6_decl[0], '%')
    # # print('陈述句得分', M6_decl[1])
    # # print(M6_decl[2])
    #
    # M6_comp1 = M6_compound.compound(spell_corrected_context, nlp_depend, nlp_pos)
    # # M6_comp1[0] = '并列句比率:'+str(M6_comp1[0])+'%'
    # # M6_comp1[1] = '并列句得分:' + str(M6_comp1[1])
    # # print('并列句比率', M6_comp1[0], '%')
    # # print('并列句得分', M6_comp1[1])
    # # print(M6_comp1[2])
    #
    # M6_comp2 = M6_complex.complex(spell_corrected_context, nlp_depend, nlp_pos)
    # # M6_comp2[0] = '复合句比率:'+str(M6_decl[0])+'%'
    # # M6_comp2[1] = '简单句比率:' + str(M6_decl[1])+'%'
    # # M6_comp2[2] = '简单/复合句得分:' + str(M6_decl[2])
    # # print('复合句比率', M6_comp2[0], '%')
    # # print('简单句比率', M6_comp2[1], '%')
    # # print('简单/复合句得分', M6_comp2[2])
    # # print(M6_comp2[3])
    #
    # # int+0.5四舍五入
    # M6_total = int(0.5+100*(M6_pass[1]*pass_w+M6_decl[1]*decl_w+M6_comp1[1]*comp1_w
    #                         +M6_comp2[2]*comp2_w)/(pass_w*20+decl_w*15+comp1_w*20+comp2_w*45))
    # # print('Total =', M6_total)
    #
    # M6_res = [M6_pass, M6_decl, M6_comp1, M6_comp2, M6_total]

    # M7
    word_seped = M7_Vocabulary_Division.Division(spell_corrected_context)
    dict_occur = M7_Vocabulary_Word_Distribution.Word_Distribution_Occur(word_seped)
    dict_index = M7_Vocabulary_Word_Distribution.Word_Distribution_Index(word_seped)

    num = 150  # 输入词数(临时)
    level = 3  # 作者学习水平(临时)
    score3_3, eva3_3 = M7_Vocabulary_Count.Count(num, dict_occur)
    score3_0, eva3_0 = M7_Vocabulary_Richness.Richness(dict_occur)
    score3_1, eva3_1 = M7_Vocabulary_Replace0.Replace0(dict_occur)
    score3_2, eva3_2 = M7_Vocabulary_Replace1.Replace1(dict_occur, dict_index, int(level) - 1)
    M7_score = int(M7_Vocabulary_Get_Score.Get_Score(score3_3, score3_1, score3_2, score3_0))
    M7_eva = [eva3_3, eva3_0, eva3_1, eva3_2]

    # M8
    f = spell_corrected_context  # 文章
    topic = M8_Topic.predict_topic(doc_test=f)
    # print('topic', topic)
    file = "challenge"  # 主题
    titletopic = M8_Topic.predict_topic(doc_test = file)
    # print(file, titletopic)
    M8_score, M8_eva = M8_Topic.topicscore(topic, titletopic)
    # print(M8_score, M8_eva)

    M3_res = M3_Body.main(stn_seped, spell_corrected_context, 1)
    wrongnum = M3_Sum.Wrongnum(M3_res)  # 共计错误个数
    wrongsent = M3_Sum.Wrongsent(M3_res)  # 错误句子下标
    pos_word = M3_Sum.Pos0(M3_res)  # 错误单词下标
    mis_spedded_word = M3_Sum.Mis_spedded_word(M3_res)  # 错误单词
    sgted_word = M3_Sum.Sgted_word(M3_res)  # 建议替换单词
    ori = M3_Sum.Ori(M3_res)  # 原错句
    new = M3_Sum.New(M3_res)  # 新改句
    Spell_corrected_context = M3_Sum.Spell_corrected_context(M3_res)

    # 将拼写改后的句子写入文件
    f = open('../Correction/M4_M5_Data/test.error.sent', 'w')
    for i in Spell_corrected_context:
        f.write(i)
        f.write('\n')
    f.close()

    # 服务器传输
    # 上传改单词句-(调用模型)-下载改语法句
    # (默认参数为1本地-实验室,参数为0云服务器)
    M4.Grammar_Correction(2)
    # os.system('python ../Correction/shell.py')

    os.system('/opt/anaconda/envs/wangyu_pytorch1.x/bin/python ../Correction/M5_Error_Location/parallel_to_m2.py -orig ../Correction/M4_M5_Data/test.error.sent '
              '-cor ../Correction/M4_M5_Data/corrected.sent -out ../Correction/M4_M5_Data/src_prd')

    M5_res = M5.M5_Locate_Classify(wrongsent, pos_word, mis_spedded_word, sgted_word)
    suggestion = M5_res[0]
    spell_score = M5_res[1]
    grammar_score = M5_res[2]
    statistic = M5_res[3]

    content = M2.Preprocess_Para(context)  # 界面显示·左

    M9_Htmlautomaker.automaker(content, suggestion, statistic, spell_score, grammar_score, 'M6_res', M7_score, M7_eva, M8_score, M8_eva)

    return suggestion, spell_score, grammar_score, statistic,\
           content, M6_res, M7_score, M7_eva, M8_score, M8_eva


if __name__ == '__main__':
    path = '../Correction/M1_M3_Data/M1_context.txt'
    context = M2.Load('../Correction/M1_M3_Data/M1_context.txt')
    res = process(context)
    # print([context])
    # print(res)
