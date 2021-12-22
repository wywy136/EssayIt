# M3_SpellCorrection_Sum.py 整合包
import copy
import M2_Preprocess as M2
import M3_SpellCorrection_Body as Bo

# 1显示相近词;0不显示相近词


def Wrongnum(res):
    return res[0]


def Wrongsent(res):
    return res[1]


def Pos0(res):
    return res[2]


def Mis_spedded_word(res):
    return res[3]


def Sgted_word(res):
    return res[4]


def Ori(res):
    return res[5]


def New(res):
    return res[6]


def Spell_corrected_context(res):
    return res[7]


if __name__ == '__main__':
    context = M2.Load('../Correction/M1_M3_Data/M1_context.txt')
    stn_seped = M2.Preprocess(context)
    spell_corrected_context = copy.deepcopy(stn_seped)

    res = Bo.main(stn_seped, spell_corrected_context)
    print('wrongnum', res[0])  # 共计错误个数
    print('wrongsent', res[1])  # 错误句子下标
    print('pos0', res[2])  # 错误单词下标
    print('mis_spedded_word', res[3])  # 错误单词
    print('sgted_word', res[4])  # 建议替换单词
    print('ori', res[5])  # 原错句
    print('new', res[6])  # 新改句
    print('spell_corrected_context', res[7])  # 全词替换+无错词句子

    # 传至M3
    f = open('../Correction/M4_M5_Data/test.error.sent', 'w')
    for i in res[7]:
        f.write(i)
        f.write('\n')
    f.close()
