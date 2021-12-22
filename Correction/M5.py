import numpy as np
import sys
sys.path.append('../Correction/M5_Error_Location/')
import parallel_to_m2_Test as Para

symbol2type_cn = {"M:ADJ": "形容词缺失", "M:ADV": "副词缺失", "M:CONJ": "连词缺失",
               "M:DET": "限定词缺失", "M:NOUN": "名词缺失", "M:PART": "小品词缺失",
               "M:PREP": "介词缺失", "M:PRON": "代词缺失", "M:PUNCT": "标点符号缺失",
               "M:VERB": "动词缺失", "M:CONTR": "缩写缺失", "M:OTHER": "缺失错误",
               "M:NOUN:POSS": "名词所有格缺失", "M:VERB:FORM": "动词形式缺失", "M:VERB:TENSE": "动词时态缺失",
               "U:ADJ": "形容词冗余", "U:ADV": "副词冗余", "U:CONJ": "连词冗余",
               "U:DET": "限定词冗余", "U:NOUN": "名词冗余", "U:PART": "小品词冗余",
               "U:PREP": "介词冗余", "U:PRON": "代词冗余", "U:PUNCT": "标点冗余",
               "U:VERB": "动词冗余", "U:CONTR": "缩写冗余", "U:OTHER": "冗余错误",
               "U:NOUN:POSS": "名词所有格冗余", "U:VERB:FORM": "动词形式冗余", "U:VERB:TENSE": "动词时态冗余",
               "R:ADJ": "形容词使用错误", "R:ADV": "副词使用错误", "R:CONJ": "连词使用错误",
               "R:DET": "限定词使用错误", "R:NOUN": "名词使用错误", "R:PART": "小品词使用错误",
               "R:PREP": "介词使用错误", "R:PRON": "代词使用错误", "R:PUNCT": "标点使用错误",
               "R:VERB": "动词使用错误", "R:CONTR": "缩写使用错误", "R:MORPH": "词形错误",
               "R:ORTH": "正规用词错误", "R:OTHER": "用词错误", "R:SPELL": "拼写错误",
               "R:WO": "单词排列顺序错误", "R:ADJ:FORM": "形容词比较级/最高级错误", "R:NOUN:INFL": "名词单复数形式错误",
               "R:NOUN:NUM": "名词单复数误用", "R:NOUN:POSS": "名词所有格误用", "R:VERB:FORM": "动词形式误用",
               "R:VERB:INFL": "动词过去式拼写错误", "R:VERB:SVA": "主谓一致错误", "R:VERB:TENSE": "动词时态误用"
               }

symbol2type_en = {"M:ADJ": "Missing Adjective", "M:ADV": "Missing Adverb", "M:CONJ": "Missing Conjunction",
               "M:DET": "Missing Determiner", "M:NOUN": "Missing Noun", "M:PART": "Missing Particle",
               "M:PREP": "Missing Prepostion", "M:PRON": "Missing Pronoun", "M:PUNCT": "Missing Punctuation",
               "M:VERB": "Missing Verb", "M:CONTR": "Missing Abbreviation", "M:OTHER": "Missing some words",
               "M:NOUN:POSS": "Missing Possessive Case", "M:VERB:FORM": "Missing Werb Form", "M:VERB:TENSE": "Missing Werb Tense",
               "U:ADJ": "Unnecessary Adjective", "U:ADV": "Unnecessary Adverb", "U:CONJ": "Unnecessary Conjunction",
               "U:DET": "Unnecessary Determiner", "U:NOUN": "Unnecessary Noun", "U:PART": "Unnecessary Particle",
               "U:PREP": "Unnecessary Prepostion", "U:PRON": "Unnecessary Pronoun", "U:PUNCT": "Unnecessary Punctuation",
               "U:VERB": "Unnecessary Verb", "U:CONTR": "Unnecessary Abbreviation", "U:OTHER": "Unnecessary words",
               "U:NOUN:POSS": "Unnecessary Possessive Case", "U:VERB:FORM": "Unnecessary Werb Form", "U:VERB:TENSE": "Unnecessary Werb Tense",
               "R:ADJ": "Wrong usage of Adjective", "R:ADV": "Wrong usage of Adverb", "R:CONJ": "Wrong usage of Conjunction",
               "R:DET": "Wrong usage of Determiner", "R:NOUN": "Wrong usage of None", "R:PART": "Wrong usage of Particle",
               "R:PREP": "Wrong usage of Preposition", "R:PRON": "Wrong usage of Pronoun", "R:PUNCT": "Wrong usage of Punctuation",
               "R:VERB": "Wrong usage of Verb", "R:CONTR": "Wrong usage of Abbreviation", "R:MORPH": "Wrong Morphology",
               "R:ORTH": "Wrong words", "R:OTHER": "Wrong words", "R:SPELL": "Spelling errors",
               "R:WO": "Wrong word order", "R:ADJ:FORM": "Wrong Form of Adjective", "R:NOUN:INFL": "Wrong Inflation of Noun",
               "R:NOUN:NUM": "Wrong Word Num", "R:NOUN:POSS": "Wrong Possessive Case", "R:VERB:FORM": "Wrong Verb Form",
               "R:VERB:INFL": "Wrong Verb Inflation", "R:VERB:SVA": "Wrong Subjective Agreement", "R:VERB:TENSE": "Wrong Verb Tense"
               }


def M5_Locate_Classify_cn(spellmis_stnindex, spellmis_wordindex, mis_spelled_word, suggested_word,
                          lines_in_m2, lines_in_corrected, lines_in_source, my_num):

    # file1 = open("../Correction/M4_M5_Data/src_prd")
    # file2 = open("../Correction/M4_M5_Data/corrected.sent")
    # file3 = open("../Correction/M4_M5_Data/test.error.sent")
    #
    # lines_in_m2 = file1.readlines()
    # lines_in_corrected = file2.readlines()
    # lines_in_source = file3.readlines()

    final = []
    statistic = {"拼写错误": 0,
                 "语法错误-名词": 0,
                 "语法错误-动词": 0,
                 "语法错误-其它": 0,
                 }

    stn_index = -1
    for i in range(len(lines_in_m2)):

        if lines_in_m2[i][0] == "S":

            stn_error = []
            stn_index += 1

            for k in range(len(spellmis_stnindex)):
                if stn_index == spellmis_stnindex[k]:
                    single_error = np.zeros(3)
                    single_error = single_error.tolist()
                    single_error[0] = [spellmis_wordindex[k]]
                    single_error[1] = "拼写错误。建议替换为" + suggested_word[k]
                    single_error[2] = mis_spelled_word[k]
                    stn_error.append(single_error)

                    statistic["拼写错误"] += 1

            for j in range(len(lines_in_m2)):

                if len(lines_in_m2[j + i + 1]) == 1:
                    break
                else:
                    single_error = np.zeros(3)
                    single_error = single_error.tolist()
                    pos = lines_in_m2[j + i + 1].split("|||")[0]
                    pos_s = int(pos.split()[1])
                    pos_e = int(pos.split()[2])
                    if lines_in_m2[j + i + 1].split("|||")[1] == 'noop':
                        break
                    else:
                        single_error[0] = [(num + pos_s) for num in range(pos_e - pos_s + 1)]

                        type = symbol2type_cn[lines_in_m2[j + i + 1].split("|||")[1]]

                        if lines_in_m2[j + i + 1].split("|||")[1].split(":")[1] == "NOUN":
                            statistic["语法错误-名词"] += 1
                        elif lines_in_m2[j + i + 1].split("|||")[1].split(":")[1] == "VERB":
                            statistic["语法错误-动词"] += 1
                        else:
                            statistic["语法错误-其它"] += 1

                        suggestion = ""
                        if lines_in_m2[j + i + 1].split("|||")[1].split(":")[0] == 'M':
                            suggestion = "建议添加" + lines_in_m2[j + i + 1].split("|||")[2]
                        elif lines_in_m2[j + i + 1].split("|||")[1].split(":")[0] == 'U':
                            deleted_words = ""
                            for t in range(pos_e - pos_s):
                                deleted_words += " "
                                deleted_words += lines_in_source[stn_index].split()[pos_s + t]
                            suggestion = "建议删除" + deleted_words
                        elif lines_in_m2[j + i + 1].split("|||")[1].split(":")[0] == 'R':
                            supplanted_words = ""
                            for t in range(pos_e - pos_s):
                                supplanted_words += " "
                                supplanted_words += lines_in_source[stn_index].split()[pos_s + t]
                            suggestion = "建议将" + supplanted_words + "替换为" + lines_in_m2[j + i + 1].split("|||")[2]

                        corrected = lines_in_corrected[stn_index].replace("\n", '')

                        single_error[1] = type + "。" + suggestion + "。修改结果：" + corrected
                        single_error[2] = lines_in_source[stn_index].split()[pos_s]

                stn_error.append(single_error)

            final.append(stn_error)
            # if i == 15:
            #     print(stn_error)

            statistic_return = []
            for errortype, num in statistic.items():
                statistic_return.append(errortype + ': ' + str(num))

    # 扣分部分:看总次数,考虑错误占比进行扣分
    # 扣分标准(暂定)
    # 200词
    # Spell: 0-3处 3分/处 3-6处 4分/处 6-10处 5分/处 大于10处 6分/处
    # Grammar: 0-3处 2分/处 3-6处 3分/处 6-10处 4分/处 大于10处 5分/处

    if statistic["拼写错误"]/my_num > 9/200:
        spell_score = max(0, int(100-statistic["拼写错误"]*(200/my_num)*6+0.5))
    elif statistic["拼写错误"]/my_num > 6/200:
        spell_score = max(0, int(100-statistic["拼写错误"]*(200/my_num)*5+0.5))
    elif statistic["拼写错误"]/my_num > 3/200:
        spell_score = max(0, int(100-statistic["拼写错误"]*(200/my_num)*4+0.5))
    else:
        spell_score = max(0, int(100-statistic["拼写错误"]*(200/my_num)*3+0.5))

    grammar_error_num = statistic["语法错误-名词"] + statistic["语法错误-动词"] + statistic["语法错误-其它"]
    if grammar_error_num/my_num > 9/200:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*5+0.5))
    elif grammar_error_num/my_num > 6/200:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*4+0.5))
    elif grammar_error_num/my_num > 3/200:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*3+0.5))
    else:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*2+0.5))

    return final, spell_score, grammar_score, statistic_return


def M5_Locate_Classify_en(spellmis_stnindex, spellmis_wordindex, mis_spelled_word, suggested_word,
                          lines_in_m2, lines_in_corrected, lines_in_source, my_num):

    # file1 = open("../Correction/M4_M5_Data/src_prd")
    # file2 = open("../Correction/M4_M5_Data/corrected.sent")
    # file3 = open("../Correction/M4_M5_Data/test.error.sent")
    #
    # lines_in_m2 = file1.readlines()
    # lines_in_corrected = file2.readlines()
    # lines_in_source = file3.readlines()

    final = []
    statistic = {"Spell error": 0,
                 "Grammar error-noun": 0,
                 "Grammar error-verb": 0,
                 "Grammar error-others": 0,
                 }

    stn_index = -1
    for i in range(len(lines_in_m2)):

        if lines_in_m2[i][0] == "S":

            stn_error = []
            stn_index += 1

            for k in range(len(spellmis_stnindex)):
                if stn_index == spellmis_stnindex[k]:
                    single_error = np.zeros(3)
                    single_error = single_error.tolist()
                    single_error[0] = [spellmis_wordindex[k]]
                    single_error[1] = "Spell error. Suggest replace it with " + suggested_word[k]
                    single_error[2] = mis_spelled_word[k]
                    stn_error.append(single_error)

                    statistic["Spell error"] += 1

            for j in range(len(lines_in_m2)):

                if len(lines_in_m2[j + i + 1]) == 1:
                    break
                else:
                    single_error = np.zeros(3)
                    single_error = single_error.tolist()
                    pos = lines_in_m2[j + i + 1].split("|||")[0]
                    pos_s = int(pos.split()[1])
                    pos_e = int(pos.split()[2])
                    if lines_in_m2[j + i + 1].split("|||")[1] == 'noop':
                        break
                    else:
                        single_error[0] = [(num + pos_s) for num in range(pos_e - pos_s + 1)]

                        type = symbol2type_en[lines_in_m2[j + i + 1].split("|||")[1]]

                        if lines_in_m2[j + i + 1].split("|||")[1].split(":")[1] == "NOUN":
                            statistic["Grammar error-noun"] += 1
                        elif lines_in_m2[j + i + 1].split("|||")[1].split(":")[1] == "VERB":
                            statistic["Grammar error-verb"] += 1
                        else:
                            statistic["Grammar error-others"] += 1

                        suggestion = ""
                        if lines_in_m2[j + i + 1].split("|||")[1].split(":")[0] == 'M':
                            suggestion = "Suggest add " + lines_in_m2[j + i + 1].split("|||")[2]
                        elif lines_in_m2[j + i + 1].split("|||")[1].split(":")[0] == 'U':
                            deleted_words = ""
                            for t in range(pos_e - pos_s):
                                deleted_words += " "
                                deleted_words += lines_in_source[stn_index].split()[pos_s + t]
                            suggestion = "Suggest delete " + deleted_words
                        elif lines_in_m2[j + i + 1].split("|||")[1].split(":")[0] == 'R':
                            supplanted_words = ""
                            for t in range(pos_e - pos_s):
                                supplanted_words += " "
                                supplanted_words += lines_in_source[stn_index].split()[pos_s + t]
                            suggestion = "Suggest replace " + supplanted_words + " with " + lines_in_m2[j + i + 1].split("|||")[2]

                        corrected = lines_in_corrected[stn_index].replace("\n", '')

                        single_error[1] = type + ". " + suggestion + ". Result after modified: " + corrected
                        single_error[2] = lines_in_source[stn_index].split()[pos_s]

                stn_error.append(single_error)

            final.append(stn_error)
            # if i == 15:
            #     print(stn_error)

            statistic_return = []
            for errortype, num in statistic.items():
                statistic_return.append(errortype + ': ' + str(num))

    # 扣分部分:看总次数,考虑错误占比进行扣分
    # 扣分标准(暂定)
    # 200词
    # Spell: 0-3处 3分/处 3-6处 4分/处 6-10处 5分/处 大于10处 6分/处
    # Grammar: 0-3处 2分/处 3-6处 3分/处 6-10处 4分/处 大于10处 5分/处

    if statistic["Spell error"]/my_num > 9/200:
        spell_score = max(0, int(100-statistic["Spell error"]*(200/my_num)*6+0.5))
    elif statistic["Spell error"]/my_num > 6/200:
        spell_score = max(0, int(100-statistic["Spell error"]*(200/my_num)*5+0.5))
    elif statistic["Spell error"]/my_num > 3/200:
        spell_score = max(0, int(100-statistic["Spell error"]*(200/my_num)*4+0.5))
    else:
        spell_score = max(0, int(100-statistic["Spell error"]*(200/my_num)*3+0.5))

    grammar_error_num = statistic["Grammar error-noun"] + statistic["Grammar error-verb"] + statistic["Grammar error-others"]
    if grammar_error_num/my_num > 9/200:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*5+0.5))
    elif grammar_error_num/my_num > 6/200:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*4+0.5))
    elif grammar_error_num/my_num > 3/200:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*3+0.5))
    else:
        grammar_score = max(0, int(100-grammar_error_num*(200/my_num)*2+0.5))

    return final, spell_score, grammar_score, statistic_return


def M5_Run_Scripts(Spell_corrected_context, Grammar_corrected_context, M5):

    lines_in_m2 = Para.main(Spell_corrected_context, Grammar_corrected_context, M5)
    lines_in_corrected = Grammar_corrected_context
    lines_in_source = Spell_corrected_context

    return lines_in_m2, lines_in_corrected, lines_in_source


if __name__ == '__main__':
    # spellmis_stnindex = [0, 1]
    # spellmis_wordindex = [1, 1]
    # suggested_word = ['haha', 'hehe']
    # mis_spelled_word = ['mis1', 'mis2']
    #
    # f, s, g, c = M5_Locate_Classify(spellmis_stnindex, spellmis_wordindex, mis_spelled_word, suggested_word)
    # print(f)

    with open('/home/wangyu/wy/Correction/M4_M5_Data/test.error.sent', 'r') as f1:
        Spell_corrected_context = f1.readlines()

    with open('/home/wangyu/wy/Correction/M4_M5_Data/corrected.sent', 'r') as f2:
        Grammar_corrected_context = f2.readlines()

    lines_in_m2, lines_in_corrected, lines_in_source = M5_Run_Scripts(Spell_corrected_context, Grammar_corrected_context)

    print(lines_in_m2)
