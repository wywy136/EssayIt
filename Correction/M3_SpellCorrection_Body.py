# M3_SpellCorrection_Body.py 主体执行及笔者测试
import nltk
import copy
import time
# 以下文件仅在单个调试时加入,本身都已经糅入了Control函数
import M2_Preprocess as Pre  # 输入文本、切分句子、标点转化等预处理工作
import M3_SpellCorrection_Word as Wo


def main(stn_seped, spell_corrected_context, switch=1, nlp_pos=[]):
    # 参数说明
    # stn_seped 切分好的句子
    # spell_corrected_context 原本也是切分好的句子,但还用来储存返回的全词替换的句子
    # switch 控制相近编辑距离单词显示;默认1为显示
    wrongnum = 0  # 共计错误个数
    wrongsent = []  # 错词句子下标
    ws = 0  # 错词句子起始下标
    pos0 = []  # 错误单词在句中位置
    mis_spedded_word = []  # 错词
    sgted_word = []  # 建议替换单词

    ori = []  # 原错句
    new = []  # 新改句

    # print("-------")
    # print(stn_seped)
    # print("-------")

    for gr in range(0, len(stn_seped)):
        os = stn_seped[gr].split()  # 修改前的单词组(含标点)
        ps = copy.deepcopy(os)  # 修改后的单词组(含标点)
        # t2 = time.time()
        # ns_pos = nltk.pos_tag(ps)
        ns_pos = nlp_pos[gr]
        ners = nltk.ne_chunk(ns_pos)  # 对含大小写的文本进行命名实体识别
        # t3 = time.time()
        # print('nltk=', t3-t2)
        ners_tag = []  # 识别单词下标
        i = 0
        k = 0
        while i < len(ners):
            if type(ners[i]) != tuple:
                for j in ners[i]:
                    ners_tag.append(k)
                    k += 1
            else:
                k += 1
            i += 1
        # t4 = time.time()
        for i in range(0, len(ps)):
            temp = Wo.correct(ps[i], ps, ns_pos, ners_tag, i, switch)
            # if i == 7:
            #     print("double")
            ps[i] = Wo.keep(os[i], temp)  # 根据字典修正单词,保留大小写

            if os[i][0] == '(':
                ps[i] = '(' + ps[i]
            if os[i][0] == '\'':
                ps[i] = '\'' + ps[i]
            if os[i][-1] == ')':
                ps[i] = ps[i] + ')'
            if os[i][-1] == '\'':
                ps[i] = ps[i] + '\''

            if ps[i] != os[i]:  # 判断有错
                wrongnum += 1  # 共计错误个数
                wrongsent.append(ws)  # 错词句子下标
                pos0.append(i)  # 错误单词在句中位置
                mis_spedded_word.append(os[i])  # 错词

                if i == 0:  # 首词错了
                    ps[i] = ps[i].title()
                    sgted_word.append(ps[i])  # 建议替换单词(含大小写)
                else:
                    sgted_word.append(ps[i])  # 建议替换单词

            else:  # 判断没错(但实际上还可能有首字母大小写错误)
                if (i == 0) & (os[0][0] in 'abcdefghijklmnopqrstuvwxyz'):  # 首词首字母大小写错了
                    wrongnum += 1  # 共计错误个数
                    wrongsent.append(ws)  # 错词句子下标
                    pos0.append(i)  # 错误单词在句中位置
                    mis_spedded_word.append(os[i])  # 错词
                    ps[i] = ps[i].title()
                    sgted_word.append(ps[i])  # 建议替换单词(含大小写)
        # t5 = time.time()
        # print('editdis', t5-t4)
        ws += 1  # 当前句子下标
    # 生成1对1的单一拼写错误句子对(不对spell_corrected_context做修改)
    for i in range(0, len(wrongsent)):
        ori.append(spell_corrected_context[wrongsent[i]])
        ex_sent = spell_corrected_context[wrongsent[i]].split()
        ex_sent[pos0[i]] = sgted_word[i]  # 换单词
        new.append(' '.join(ex_sent))

    # print('ori', ori)
    # print('new', new)

    # 循环替换spell_corrected_context中的错词,最终得到全词替换的无错词原文分句spell_corrected_context
    for i in range(0, len(wrongsent)):
        ex_sent = spell_corrected_context[wrongsent[i]].split()
        ex_sent[pos0[i]] = sgted_word[i]
        spell_corrected_context[wrongsent[i]] = ' '.join(ex_sent)
        # 破折号的后处理/承接M2
        spell_corrected_context[wrongsent[i]] = spell_corrected_context[wrongsent[i]].replace("—", '——')

    # print('spell_corrected_context', spell_corrected_context)

    return wrongnum, wrongsent, pos0, mis_spedded_word, sgted_word, ori, new, spell_corrected_context


# if __name__ == '__main__':
#     context = Pre.Load('../Correction/M1_M3_Data/M1_context.txt')
#     stn_seped = Pre.Preprocess(context)
#     spell_corrected_context = copy.deepcopy(stn_seped)
#     res = main(stn_seped, spell_corrected_context)
#     print(res)
