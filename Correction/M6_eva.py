import M6_passive
import M6_declarative
import M6_compound
import M6_complex


def eva_cn(spell_corrected_context, xs_depend, xs_pos, standard, fw_depend, fw_pos, stu_id):
    xs_pass_rate = M6_passive.passive(spell_corrected_context, xs_depend, xs_pos)
    fw_pass_rate = M6_passive.passive(standard, fw_depend, fw_pos)
    xs_decl_rate = M6_declarative.declarative(spell_corrected_context, xs_depend, xs_pos)
    fw_decl_rate = M6_declarative.declarative(standard, fw_depend, fw_pos)
    xs_compound_rate = M6_compound.compound(spell_corrected_context, xs_depend, xs_pos)
    fw_compound_rate = M6_compound.compound(standard, fw_depend, fw_pos)
    xs_complex_rate1, xs_complex_rate2 = M6_complex.complex(spell_corrected_context, xs_depend, xs_pos)
    fw_complex_rate1, fw_complex_rate2 = M6_complex.complex(standard, fw_depend, fw_pos)

    if (stu_id == 4) | (stu_id == 5):  # 10, tag == 四级或六级
        pj_pass_rate = 8.41  # 11，平均比例
        pj_decl_rate = 90.66
        pj_compound_rate = 41.88
        pj_complex_rate1 = 48.38
        pj_complex_rate2 = 27.95
    elif (stu_id == 2) | (stu_id == 3):  # 中学
        pj_pass_rate = 6.3
        pj_decl_rate = 91.36
        pj_compound_rate = 37.87
        pj_complex_rate1 = 40.86
        pj_complex_rate2 = 35.17
    else:  # 小学
        pj_pass_rate = 0.97
        pj_decl_rate = 89.52
        pj_compound_rate = 28.1
        pj_complex_rate1 = 34.74
        pj_complex_rate2 = 47.69

    bz_pass_rate = round((fw_pass_rate + pj_pass_rate) / 2, 2)  # 12，用来评分的标准比例
    bz_decl_rate = round((fw_decl_rate + pj_decl_rate) / 2, 2)
    bz_compound_rate = round((fw_compound_rate + pj_compound_rate) / 2, 2)
    bz_complex_rate1 = round((fw_complex_rate1 + pj_complex_rate1) / 2, 2)
    bz_complex_rate2 = round((fw_complex_rate2 + pj_complex_rate2) / 2, 2)

    cha1 = abs(bz_pass_rate - xs_pass_rate)  # 与标准的偏差
    score1 = round(20 - 0.2 * cha1, 2)
    if cha1 <= 2:
        sug1 = '被动语法掌握较好'
    elif (cha1 > 2) & (bz_pass_rate < xs_pass_rate):
        sug1 = '本文主动句较少，可能不利于文章意思的传达'
    elif (cha1 > 2) & (bz_pass_rate > xs_pass_rate):
        sug1 = '被动句出现较少，可适当添加被动句型'

    cha2 = abs(bz_decl_rate - xs_decl_rate)
    score2 = round(15 - 0.15 * cha2, 2)
    if cha2 <= 1:
        sug2 = '文章句子层次丰富，情感充沛'
    elif (cha2 > 1) & (bz_decl_rate < xs_decl_rate):
        sug2 = '陈述句过多，建议增加疑问句、感叹句、祈使句提高句子丰富度'
    elif (cha2 > 1) & (bz_decl_rate > xs_decl_rate):
        sug2 = '本文陈述句较少，可能不利于文章意思的传达'

    cha3 = abs(bz_compound_rate - xs_compound_rate)
    score3 = round(20 - 0.2 * cha3, 2)
    if cha3 <= 3:
        sug3 = '文章结构严谨，有效地使用了语句间的衔接成分'
    elif (cha3 > 3) & (bz_compound_rate < xs_compound_rate):
        sug3 = '文中过渡词和衔接词过多'
    elif (cha3 > 3) & (bz_compound_rate > xs_compound_rate):
        sug3 = '文中过渡词和衔接词较少，建议增加衔接词汇的积累,使行文更加流畅'

    cha4 = abs(bz_complex_rate1 - xs_complex_rate1)
    cha5 = abs(bz_complex_rate2 - xs_complex_rate2)
    score4 = round((25 - 0.25 * cha4) + (20 - 0.2 * cha5), 2)
    if cha5 <= 6:
        if cha4 <= 6:
            sug4 = '句式变化多样，句型使用较好'
        elif (cha4 > 6) & (bz_complex_rate1 < xs_complex_rate1):
            sug4 = '复合句型掌握较好，句法方面做的很棒'
        elif (cha4 > 6) & (bz_complex_rate1 > xs_complex_rate1):
            sug4 = '句式有一定的变化，若适当增加一些从句的使用，文章会取得更好的成绩'
    elif cha5 > 6:
        if cha4 <= 6 & (bz_complex_rate2 < xs_complex_rate2):
            sug4 = '文章简单句过多，建议增加复合句的使用'
        elif cha4 <= 6 & (bz_complex_rate2 > xs_complex_rate2):
            sug4 = '句式变化多样，句型使用较好'
        elif cha4 > 6 & (bz_complex_rate1 < xs_complex_rate1):
            sug4 = '复合句型掌握较好，句法方面做的很棒'
        elif cha4 > 6 & (bz_complex_rate1 > xs_complex_rate1) & (bz_complex_rate2 < xs_complex_rate2):
            sug4 = '文章简单句过多，建议增加复合句的使用'
        elif cha4 > 6 & (bz_complex_rate1 > xs_complex_rate1) & (bz_complex_rate2 < xs_complex_rate2):
            sug4 = '复合句使用不太熟练，注意在平时练习中多加积累'

    score = int(score1 + score2 + score3 + score4 + 0.5)
    m6_pass = [xs_pass_rate, score1, sug1]  # 主被动
    m6_decl = [xs_decl_rate, score2, sug2]  # 陈述
    m6_comp1 = [xs_compound_rate, score3, sug3]  # 并列
    m6_comp2 = [xs_complex_rate1, xs_complex_rate2, score4, sug4]  # 复合rate1，简单rate2

    m6_res = [m6_pass, m6_decl, m6_comp1, m6_comp2, score]
    return m6_res


def eva_en(spell_corrected_context, xs_depend, xs_pos, standard, fw_depend, fw_pos, stu_id):
    xs_pass_rate = M6_passive.passive(spell_corrected_context, xs_depend, xs_pos)
    fw_pass_rate = M6_passive.passive(standard, fw_depend, fw_pos)
    xs_decl_rate = M6_declarative.declarative(spell_corrected_context, xs_depend, xs_pos)
    fw_decl_rate = M6_declarative.declarative(standard, fw_depend, fw_pos)
    xs_compound_rate = M6_compound.compound(spell_corrected_context, xs_depend, xs_pos)
    fw_compound_rate = M6_compound.compound(standard, fw_depend, fw_pos)
    xs_complex_rate1, xs_complex_rate2 = M6_complex.complex(spell_corrected_context, xs_depend, xs_pos)
    fw_complex_rate1, fw_complex_rate2 = M6_complex.complex(standard, fw_depend, fw_pos)

    if (stu_id == 4) | (stu_id == 5):  # 10, tag == 四级或六级
        pj_pass_rate = 8.41  # 11，平均比例
        pj_decl_rate = 90.66
        pj_compound_rate = 41.88
        pj_complex_rate1 = 48.38
        pj_complex_rate2 = 27.95
    elif (stu_id == 2) | (stu_id == 3):  # 中学
        pj_pass_rate = 6.3
        pj_decl_rate = 91.36
        pj_compound_rate = 37.87
        pj_complex_rate1 = 40.86
        pj_complex_rate2 = 35.17
    else:  # 小学
        pj_pass_rate = 0.97
        pj_decl_rate = 89.52
        pj_compound_rate = 28.1
        pj_complex_rate1 = 34.74
        pj_complex_rate2 = 47.69

    bz_pass_rate = round((fw_pass_rate + pj_pass_rate) / 2, 2)  # 12，用来评分的标准比例
    bz_decl_rate = round((fw_decl_rate + pj_decl_rate) / 2, 2)
    bz_compound_rate = round((fw_compound_rate + pj_compound_rate) / 2, 2)
    bz_complex_rate1 = round((fw_complex_rate1 + pj_complex_rate1) / 2, 2)
    bz_complex_rate2 = round((fw_complex_rate2 + pj_complex_rate2) / 2, 2)

    cha1 = abs(bz_pass_rate - xs_pass_rate)  # 与标准的偏差
    score1 = round(20 - 0.2 * cha1, 2)
    if cha1 <= 2:
        sug1 = 'Good command of passive grammar'
    elif (cha1 > 2) & (bz_pass_rate < xs_pass_rate):
        sug1 = 'There are fewer active sentences in this article, which may be detrimental to the meaning of the article'
    elif (cha1 > 2) & (bz_pass_rate > xs_pass_rate):
        sug1 = 'There are rare passive sentences, and passive sentence patterns can be added appropriately'

    cha2 = abs(bz_decl_rate - xs_decl_rate)
    score2 = round(15 - 0.15 * cha2, 2)
    if cha2 <= 1:
        sug2 = 'The article sentence level is rich, the emotion is abundant'
    elif (cha2 > 1) & (bz_decl_rate < xs_decl_rate):
        sug2 = 'There are too many statements, it is suggested to add interrogative sentence, exclamatory sentence and imperative sentence to improve sentence richness'
    elif (cha2 > 1) & (bz_decl_rate > xs_decl_rate):
        sug2 = 'There are fewer statements in this article, which may be detrimental to the meaning of the article'

    cha3 = abs(bz_compound_rate - xs_compound_rate)
    score3 = round(20 - 0.2 * cha3, 2)
    if cha3 <= 3:
        sug3 = 'The structure of the paper is strict and the cohesion between sentences is used effectively'
    elif (cha3 > 3) & (bz_compound_rate < xs_compound_rate):
        sug3 = 'There are too many transition words and cohesion words in the text'
    elif (cha3 > 3) & (bz_compound_rate > xs_compound_rate):
        sug3 = 'There are fewer transition words and cohesive words in the text. It is recommended to increase the accumulation of cohesive words to make the text more fluent'

    cha4 = abs(bz_complex_rate1 - xs_complex_rate1)
    cha5 = abs(bz_complex_rate2 - xs_complex_rate2)
    score4 = round((25 - 0.25 * cha4) + (20 - 0.2 * cha5), 2)
    if cha5 <= 6:
        if cha4 <= 6:
            sug4 = 'The sentence pattern is varied, and the sentence pattern is used well'
        elif (cha4 > 6) & (bz_complex_rate1 < xs_complex_rate1):
            sug4 = 'Good command of compound sentence patterns, good at syntax'
        elif (cha4 > 6) & (bz_complex_rate1 > xs_complex_rate1):
            sug4 = 'There are some changes in sentence patterns. If some clauses are added appropriately, the article will get better results'
    elif cha5 > 6:
        if cha4 <= 6 & (bz_complex_rate2 < xs_complex_rate2):
            sug4 = 'The article is too many simple sentences, it is suggested to increase the use of compound sentences'
        elif cha4 <= 6 & (bz_complex_rate2 > xs_complex_rate2):
            sug4 = 'The sentence pattern is varied, and the sentence pattern is used well'
        elif cha4 > 6 & (bz_complex_rate1 < xs_complex_rate1):
            sug4 = 'Good command of compound sentences and great syntax'
        elif cha4 > 6 & (bz_complex_rate1 > xs_complex_rate1) & (bz_complex_rate2 < xs_complex_rate2):
            sug4 = 'The article is too many simple sentences, it is suggested to increase the use of compound sentences'
        elif cha4 > 6 & (bz_complex_rate1 > xs_complex_rate1) & (bz_complex_rate2 < xs_complex_rate2):
            sug4 = 'The use of compound sentences is not very skilled, pay attention to accumulate more in the usual practice'

    score = int(score1 + score2 + score3 + score4 + 0.5)
    m6_pass = [xs_pass_rate, score1, sug1]  # 主被动
    m6_decl = [xs_decl_rate, score2, sug2]  # 陈述
    m6_comp1 = [xs_compound_rate, score3, sug3]  # 并列
    m6_comp2 = [xs_complex_rate1, xs_complex_rate2, score4, sug4]  # 复合rate1，简单rate2

    m6_res = [m6_pass, m6_decl, m6_comp1, m6_comp2, score]
    return m6_res
