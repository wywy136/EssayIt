# -*- coding:utf-8 -*-
import copy
import string


def automaker(content, sugg, statistic, spell_score, grammar_score, M6_res, M7_score, M7_eva, M8_score, M8_eva,
              eva_list, context, weight, base64_stu, base64_fw, M10_res, word_seped, lang):
    # print('M7_Vol_eva')
    # print(eva_list)

    if lang == 'cn':
        content_len = len(content)  # 段数

        words = []  # 单个词
        for i in range(content_len):
            words.append([])
            for j in content[i]:
                temp = j.strip(' ').strip('\n').split(' ')
                words[i].append(temp)
                for k in range(len(words[i][-1])):
                    words[i][-1][k] = words[i][-1][k].replace('"', '&quot;')
                    words[i][-1][k] = words[i][-1][k].replace("'", '&apos;')
                    words[i][-1][k] = words[i][-1][k].replace(".  ", ':')  # 承接M2的:段尾处理

        sugg_grammar_word = []
        sugg_spell_word = []  # 按句分条建议,区分spell与grammar,对grammar去尾防重叠
        for i in range(len(sugg)):
            sugg_grammar_word.append([])
            sugg_spell_word.append([])
            for j in sugg[i]:
                if j[1].startswith('拼'):
                    sugg_spell_word[i].append([j[0], j[1]])
                else:  # 语法
                    if len(j[0]) > 1:  # 同一处标记词数>1,则删去后一个
                        j[0].pop()
                    sugg_grammar_word[i].append([j[0], j[1]])
        # print(sugg_grammar_word)
        # print(sugg_spell_word)

        stext_s1 = '<div class="spellwrong" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_s2 = '" data-content="'
        stext_s3 = '">'

        stext_g1 = '<div class="grammarwrong" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_g2 = '" data-content="'
        stext_g3 = '">'

        stext_v1_0 = '<div class="vocabulary0" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_v1_1 = '<div class="vocabulary1" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_v1 = [stext_v1_0, stext_v1_1]
        stext_v2 = '" data-content="'
        stext_v3 = '">'

        stext_n = '<div class="normalword">'
        etext = '</div>'

        cumsum_sent = 0
        words_sum = []  # 无分段版本,用于Vocabulary
        words_sum_lower = []  # 无分段+全小写版本,用于Vocabulary
        para_id = []  # 分段序号,用于Vocabulary插入<br><br>

        Spell = []  # Spell分立版,不用配套</div>

        Grammar = []  # Grammar分立版

        word_id = 0
        word_para = []  # 用于分段的词下标

        for i in range(len(words)):  # 段
            para_id.append(cumsum_sent)
            word_para.append(word_id)
            for j in range(len(words[i])):  # 句
                words_sum.append(words[i][j])
                words_sum_lower.append(words[i][j])
                # Spell
                # print(str(words[i]))
                # print(len(words[i]))
                # print(str(sugg_spell_word))
                # print(len(sugg_spell_word))
                # print(cumsum_sent)
                if sugg_spell_word[cumsum_sent] == []:  # 无拼写错误的句子
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        Spell.append(temp)
                        word_id += 1
                else:  # 有拼写错误的句子
                    temp_id = []
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        temp_id.append(temp)
                        word_id += 1
                    for p in sugg_spell_word[cumsum_sent]:  # 生成每条建议
                        # print(p)
                        # print(temp_id)
                        temp_id[p[0][0]] = ''  # 将对应html文本重置

                        p[1] = p[1].replace("'", '&apos;')
                        p[1] = p[1].replace('"', '&quot;')  # 防引号匹配导致错位

                        sent_split = p[1].split('。')
                        temp_id[p[0][-1]] = stext_s1 + sent_split[0] + stext_s2 + sent_split[1]\
                                            + stext_s3 + words[i][j][p[0][0]]
                    for x in temp_id:
                        Spell.append(x)

                # Grammar
                if sugg_grammar_word[cumsum_sent] == []:
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        Grammar.append(temp)
                else:
                    temp_id = []
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        temp_id.append(temp)
                    for p in sugg_grammar_word[cumsum_sent]:  # 每条建议
                        # print(p)
                        p[1] = p[1].replace("'", '&apos;')
                        p[1] = p[1].replace('"', '&quot;')  # 防引号匹配导致错位

                        sent_split = p[1].split('。')

                        for q in p[0]:
                            temp_id[q] = ''  # 将对应html文本重置
                            temp_id[q] = stext_g1 + sent_split[0] + stext_g2 + sent_split[1] + '<br>' \
                                         + sent_split[2] + stext_g3 + words[i][j][q]
                    for x in temp_id:
                        Grammar.append(x)

                cumsum_sent += 1

        # print(words_sum_lower)
        for i in range(len(words_sum_lower)):
            for j in range(len(words_sum_lower[i])):
                words_sum_lower[i][j] = words_sum_lower[i][j].lower()

        # Vocabulary
        voca_sum = copy.deepcopy(words_sum)
        for i in range(len(voca_sum)):
            for j in range(len(voca_sum[i])):
                voca_sum[i][j] = stext_n + words_sum[i][j] + etext

        # print(words_sum)
        voca_var = ['高频用词,建议替换', '低级用词,建议替换']
        for x in range(len(eva_list)):
            temp = ''
            for i in range(len(eva_list[x][2])):
                if i % 2 == 0:
                    eva_list[x][2][i] = str(eva_list[x][2][i])
                    eva_list[x][2][i] = eva_list[x][2][i].replace("'", '&apos;')
                    eva_list[x][2][i] = eva_list[x][2][i].replace('"', '&quot;')
                    temp += eva_list[x][2][i] + ': '
                else:
                    for j in range(len(eva_list[x][2][i])):
                        eva_list[x][2][i][j] = str(eva_list[x][2][i][j])
                        eva_list[x][2][i][j] = eva_list[x][2][i][j].replace("'", '&apos;')
                        eva_list[x][2][i][j] = eva_list[x][2][i][j].replace('"', '&quot;')
                        temp += eva_list[x][2][i][j] + ' / '
                    temp += '<br>'

                stn_id = eva_list[x][1][0]  # stn_id是句子标号,x是当前eva标号
                sugg_word_id = words_sum_lower[stn_id].index(word_seped[eva_list[x][1][0]][eva_list[x][1][1]].lower())  # 对句中词的定位有分歧,但对句的定位不会错,故在句中找词
                type_id = int(eva_list[x][-1])
                voca_sum[stn_id][sugg_word_id] = stext_v1[type_id] + voca_var[type_id] + stext_v2 + temp + stext_v3 + \
                                                 words_sum[stn_id][sugg_word_id] + etext

        para_id.pop(0)  # 删去第一个,也就是0
        word_para.pop(0)
        # print('eva_list', eva_list)
        # ---------------------------输出-------------------------------
        Spell_sum = ''
        for i in range(len(Spell)):
            Spell[i] = list(Spell[i])
            Spell[i].insert(4, ' id="w'+str(i)+'"')
            Spell[i] = "".join(Spell[i])

            # 防止I have a dream .情况(由此处的空格决定)
            if i < len(Spell)-1:
                if Spell[i+1][-1] in ",:.!?;":
                    Spell_sum += Spell[i] + etext
                    # print('in', Spell[i+1])
                else:
                    Spell_sum += Spell[i] + etext + ' '
                    # print('out', Spell[i+1])
            else:
                Spell_sum += Spell[i] + etext + ' '

            if (i+1) in word_para:
                Spell_sum += '<br><br>'

        Grammar_sum = ''
        for i in range(len(Grammar)):
            Grammar[i] = list(Grammar[i])
            Grammar[i].insert(4, ' id="w'+str(i)+'"')
            Grammar[i] = "".join(Grammar[i])

            # 防止I have a dream .情况
            if i < len(Grammar)-1:
                if Grammar[i+1][-1] in ",:.!?;":
                    Grammar_sum += Grammar[i] + etext
                else:
                    Grammar_sum += Grammar[i] + etext + ' '
            else:
                Grammar_sum += Grammar[i] + etext + ' '

            if (i+1) in word_para:
                Grammar_sum += '<br><br>'

        Vocabulary_sum = ''
        word_id = 0
        for i in range(len(voca_sum)):
            for j in range(len(voca_sum[i])):
                voca_sum[i][j] = list(voca_sum[i][j])
                voca_sum[i][j].insert(4, ' id="w' + str(word_id) + '"')
                voca_sum[i][j] = "".join(voca_sum[i][j])
                word_id += 1

                # 防止I have a dream .情况
                if j < len(voca_sum[i])-1:
                    if voca_sum[i][j+1][-7] in ",:.!?;":
                        Vocabulary_sum += voca_sum[i][j]
                    else:
                        Vocabulary_sum += voca_sum[i][j] + ' '
                else:
                    Vocabulary_sum += voca_sum[i][j] + ' '

            if (i+1) in para_id:
                Vocabulary_sum += '<br><br>'

        # print(Spell_sum)
        # print(Grammar_sum)
        # print(Vocabulary_sum)

        scores = [str(spell_score), str(grammar_score), str(M7_score), str(M6_res[4]), str(M8_score),
                  str(int((spell_score*weight[0] + grammar_score*weight[1] + M7_score*weight[2] + M6_res[4]*weight[3]
                           + M8_score*weight[4]) / sum(weight) + 0.5))]

        M7 = M7_eva[0] + '<br>' + M7_eva[1] + '<br>' + M7_eva[2] + '<br>' + M7_eva[3]

        M6 = '被动句比率:' + str(M6_res[0][0]) + '%' + '    '
        M6 += '主被动得分:' + str(M6_res[0][1]) + '<br>'
        M6 += M6_res[0][-1] + '<br>'
        M6 += '陈述句比率:' + str(M6_res[1][0]) + '%' + '    '
        M6 += '陈述句得分:' + str(M6_res[1][1]) + '<br>'
        M6 += M6_res[1][-1] + '<br>'
        M6 += '并列句比率:' + str(M6_res[2][0]) + '%' + '    '
        M6 += '并列句得分:' + str(M6_res[2][1]) + '<br>'
        M6 += M6_res[2][-1] + '<br>'
        M6 += '复合句比率:' + str(M6_res[3][0]) + '%' + '    '
        M6 += '简单句比率:' + str(M6_res[3][1]) + '%' + '    '
        M6 += '简单/复合句得分:' + str(M6_res[3][2]) + '<br>'
        M6 += M6_res[3][-1]

        M8 = M8_eva
        eva = [M7, M6, M8]

        # 短语知识
        phrase_found = '下列固定搭配在您的文章中被检测到了可能的使用，请确认并强化它们的正确用法:<br><br>'
        for i in range(len(M10_res[0])):
            phrase_found += M10_res[0][i] + '<br>'
            phrase_found += M10_res[1][i] + '<br>'
            phrase_found += '语法知识: ' + M10_res[2][i] + '<br>'
            phrase_found += '例句: ' + M10_res[3][i] + '<br>'
            phrase_found += '<br>'

        # 统计饼状图
        pie = []
        stat_len = len(statistic)
        error_type = []
        error_num = []
        for id in range(stat_len):
            temp = statistic[id].split(':')
            error_type.append(temp[0])
            error_num.append(int(temp[1]))
        error_sum = sum(error_num)
        for id in range(stat_len):
            if error_sum != 0:
                pie.append([error_type[id], round(100 * error_num[id] / error_sum, 1)])
            else:
                pie.append([error_type[id], 0])
        # print(pie)

        # 规范性警告
        warning = [0, 0, 0]  # 连续多空格/使用了全角标点/不规范字符(如ﬁ/ﬃ)
        if '  ' in context:
            warning[0] = 1
        for punc in ['，', '。', '？', '！', '“', '”', '‘', '’', '：', '；', '（', '）', '、', '《', '》']:
            if punc in context:
                warning[1] = 1
                break
        if ('ﬁ' in context) | ('ﬃ' in context):
            warning[2] = 1
        # print("warning =", warning)

        # 词云base64转码
        stu_cloud = '<img id="stu_cloud" style="max-width:280px;max-height:280px;float:left" ' + 'src="' + base64_stu + '"></img>'
        fw_cloud = '<img id="fw_cloud" style="max-width:280px;max-height:280px;float:right" ' + 'src="' + base64_fw + '"></img>'
        # cloud = '<img id="fw_cloud" style="max-width:280px;max-height:280px;float:right" ' + 'src="' + base64_ + '"></img>'
        # return word_id, Spell_sum, Grammar_sum, Vocabulary_sum, scores, eva, phrase_found, pie, warning, cloud

    elif lang == 'en':
        content_len = len(content)  # 段数

        words = []  # 单个词
        for i in range(content_len):
            words.append([])
            for j in content[i]:
                temp = j.strip(' ').strip('\n').split(' ')
                words[i].append(temp)
                for k in range(len(words[i][-1])):
                    words[i][-1][k] = words[i][-1][k].replace('"', '&quot;')
                    words[i][-1][k] = words[i][-1][k].replace("'", '&apos;')
                    words[i][-1][k] = words[i][-1][k].replace(".  ", ':')  # 承接M2的:段尾处理

        sugg_grammar_word = []
        sugg_spell_word = []  # 按句分条建议,区分spell与grammar,对grammar去尾防重叠
        for i in range(len(sugg)):
            sugg_grammar_word.append([])
            sugg_spell_word.append([])
            for j in sugg[i]:
                if j[1].startswith('S'):
                    sugg_spell_word[i].append([j[0], j[1]])
                else:  # 语法
                    if len(j[0]) > 1:  # 同一处标记词数>1,则删去后一个
                        j[0].pop()
                    sugg_grammar_word[i].append([j[0], j[1]])
        # print(sugg_grammar_word)
        # print(sugg_spell_word)

        stext_s1 = '<div class="spellwrong" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_s2 = '" data-content="'
        stext_s3 = '">'

        stext_g1 = '<div class="grammarwrong" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_g2 = '" data-content="'
        stext_g3 = '">'

        stext_v1_0 = '<div class="vocabulary0" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_v1_1 = '<div class="vocabulary1" data-container="body" data-toggle="popover" data-placement="bottom" data-html="true" title="'
        stext_v1 = [stext_v1_0, stext_v1_1]
        stext_v2 = '" data-content="'
        stext_v3 = '">'

        stext_n = '<div class="normalword">'
        etext = '</div>'

        cumsum_sent = 0
        words_sum = []  # 无分段版本,用于Vocabulary
        words_sum_lower = []  # 无分段+全小写版本,用于Vocabulary
        para_id = []  # 分段序号,用于Vocabulary插入<br><br>

        Spell = []  # Spell分立版,不用配套</div>

        Grammar = []  # Grammar分立版

        word_id = 0
        word_para = []  # 用于分段的词下标

        for i in range(len(words)):  # 段
            para_id.append(cumsum_sent)
            word_para.append(word_id)
            for j in range(len(words[i])):  # 句
                words_sum.append(words[i][j])
                words_sum_lower.append(words[i][j])
                # Spell
                # print(str(words[i]))
                # print(len(words[i]))
                # print(str(sugg_spell_word))
                # print(len(sugg_spell_word))
                # print(cumsum_sent)
                if sugg_spell_word[cumsum_sent] == []:  # 无拼写错误的句子
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        Spell.append(temp)
                        word_id += 1
                else:  # 有拼写错误的句子
                    temp_id = []
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        temp_id.append(temp)
                        word_id += 1
                    for p in sugg_spell_word[cumsum_sent]:  # 生成每条建议
                        # print(p)
                        # print(temp_id)
                        temp_id[p[0][0]] = ''  # 将对应html文本重置

                        p[1] = p[1].replace("'", '&apos;')
                        p[1] = p[1].replace('"', '&quot;')  # 防引号匹配导致错位

                        sent_split = p[1].split('.')
                        temp_id[p[0][-1]] = stext_s1 + sent_split[0] + stext_s2 + sent_split[1] \
                                            + stext_s3 + words[i][j][p[0][0]]
                    for x in temp_id:
                        Spell.append(x)

                # Grammar
                if sugg_grammar_word[cumsum_sent] == []:
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        Grammar.append(temp)
                else:
                    temp_id = []
                    for k in range(len(words[i][j])):  # 词
                        temp = stext_n + words[i][j][k]
                        temp_id.append(temp)
                    for p in sugg_grammar_word[cumsum_sent]:  # 每条建议
                        # print(p)
                        p[1] = p[1].replace("'", '&apos;')
                        p[1] = p[1].replace('"', '&quot;')  # 防引号匹配导致错位

                        sent_split = p[1].split('.')

                        for q in p[0]:
                            temp_id[q] = ''  # 将对应html文本重置
                            temp_id[q] = stext_g1 + sent_split[0] + stext_g2 + sent_split[1] + '<br>' \
                                         + sent_split[2] + stext_g3 + words[i][j][q]
                    for x in temp_id:
                        Grammar.append(x)

                cumsum_sent += 1

        # print(words_sum_lower)
        for i in range(len(words_sum_lower)):
            for j in range(len(words_sum_lower[i])):
                words_sum_lower[i][j] = words_sum_lower[i][j].lower()

        # Vocabulary
        voca_sum = copy.deepcopy(words_sum)
        for i in range(len(voca_sum)):
            for j in range(len(voca_sum[i])):
                voca_sum[i][j] = stext_n + words_sum[i][j] + etext

        # print(words_sum)
        voca_var = ['High frequency, replace it', 'Low-level, replace it']
        for x in range(len(eva_list)):
            temp = ''
            for i in range(len(eva_list[x][2])):
                if i % 2 == 0:
                    eva_list[x][2][i] = str(eva_list[x][2][i])
                    eva_list[x][2][i] = eva_list[x][2][i].replace("'", '&apos;')
                    eva_list[x][2][i] = eva_list[x][2][i].replace('"', '&quot;')
                    temp += eva_list[x][2][i] + ': '
                else:
                    for j in range(len(eva_list[x][2][i])):
                        eva_list[x][2][i][j] = str(eva_list[x][2][i][j])
                        eva_list[x][2][i][j] = eva_list[x][2][i][j].replace("'", '&apos;')
                        eva_list[x][2][i][j] = eva_list[x][2][i][j].replace('"', '&quot;')
                        temp += eva_list[x][2][i][j] + ' / '
                    temp += '<br>'

                stn_id = eva_list[x][1][0]  # stn_id是句子标号,x是当前eva标号
                sugg_word_id = words_sum_lower[stn_id].index(
                    word_seped[eva_list[x][1][0]][eva_list[x][1][1]].lower())  # 对句中词的定位有分歧,但对句的定位不会错,故在句中找词
                type_id = int(eva_list[x][-1])
                voca_sum[stn_id][sugg_word_id] = stext_v1[type_id] + voca_var[type_id] + stext_v2 + temp + stext_v3 + \
                                                 words_sum[stn_id][sugg_word_id] + etext

        para_id.pop(0)  # 删去第一个,也就是0
        word_para.pop(0)
        # print('eva_list', eva_list)
        # ---------------------------输出-------------------------------
        Spell_sum = ''
        for i in range(len(Spell)):
            Spell[i] = list(Spell[i])
            Spell[i].insert(4, ' id="w' + str(i) + '"')
            Spell[i] = "".join(Spell[i])

            # 防止I have a dream .情况(由此处的空格决定)
            if i < len(Spell) - 1:
                if Spell[i + 1][-1] in ",:.!?;":
                    Spell_sum += Spell[i] + etext
                    # print('in', Spell[i+1])
                else:
                    Spell_sum += Spell[i] + etext + ' '
                    # print('out', Spell[i+1])
            else:
                Spell_sum += Spell[i] + etext + ' '

            if (i + 1) in word_para:
                Spell_sum += '<br><br>'

        Grammar_sum = ''
        for i in range(len(Grammar)):
            Grammar[i] = list(Grammar[i])
            Grammar[i].insert(4, ' id="w' + str(i) + '"')
            Grammar[i] = "".join(Grammar[i])

            # 防止I have a dream .情况
            if i < len(Grammar) - 1:
                if Grammar[i + 1][-1] in ",:.!?;":
                    Grammar_sum += Grammar[i] + etext
                else:
                    Grammar_sum += Grammar[i] + etext + ' '
            else:
                Grammar_sum += Grammar[i] + etext + ' '

            if (i + 1) in word_para:
                Grammar_sum += '<br><br>'

        Vocabulary_sum = ''
        word_id = 0
        for i in range(len(voca_sum)):
            for j in range(len(voca_sum[i])):
                voca_sum[i][j] = list(voca_sum[i][j])
                voca_sum[i][j].insert(4, ' id="w' + str(word_id) + '"')
                voca_sum[i][j] = "".join(voca_sum[i][j])
                word_id += 1

                # 防止I have a dream .情况
                if j < len(voca_sum[i]) - 1:
                    if voca_sum[i][j+1][-7] in ",:.!?;":
                        Vocabulary_sum += voca_sum[i][j]
                    else:
                        Vocabulary_sum += voca_sum[i][j] + ' '
                else:
                    Vocabulary_sum += voca_sum[i][j] + ' '

            if (i + 1) in para_id:
                Vocabulary_sum += '<br><br>'

        # print(Spell_sum)
        # print(Grammar_sum)
        # print(Vocabulary_sum)

        scores = [str(spell_score), str(grammar_score), str(M7_score), str(M6_res[4]), str(M8_score),
                  str(int((spell_score * weight[0] + grammar_score * weight[1] + M7_score * weight[2] + M6_res[4] *
                           weight[3]
                           + M8_score * weight[4]) / sum(weight) + 0.5))]

        M7 = M7_eva[0] + '<br>' + M7_eva[1] + '<br>' + M7_eva[2] + '<br>' + M7_eva[3]

        M6 = 'Passive sentence ratio: ' + str(M6_res[0][0]) + '%' + '    '
        M6 += 'Active and passive score: ' + str(M6_res[0][1]) + '<br>'
        M6 += M6_res[0][-1] + '<br>'
        M6 += 'Statement ratio: ' + str(M6_res[1][0]) + '%' + '    '
        M6 += 'Statement score: ' + str(M6_res[1][1]) + '<br>'
        M6 += M6_res[1][-1] + '<br>'
        M6 += 'Syntactic ratio: ' + str(M6_res[2][0]) + '%' + '    '
        M6 += 'Syntactic score: ' + str(M6_res[2][1]) + '<br>'
        M6 += M6_res[2][-1] + '<br>'
        M6 += 'Compound sentence ratio: ' + str(M6_res[3][0]) + '%' + '    '
        M6 += 'Simple sentence ratio: ' + str(M6_res[3][1]) + '%' + '    '
        M6 += 'Simple/Compound sentence ratio: ' + str(M6_res[3][2]) + '<br>'
        M6 += M6_res[3][-1]

        M8 = M8_eva
        eva = [M7, M6, M8]

        # 短语知识
        phrase_found = 'The following fixed combinations have been detected in your essay. Please confirm and strengthen their correct usage:<br><br>'
        for i in range(len(M10_res[0])):
            phrase_found += M10_res[0][i] + '<br>'
            # phrase_found += M10_res[1][i] + '<br>'
            phrase_found += 'Grammar knowledge: ' + M10_res[2][i] + '<br>'
            phrase_found += 'Example sentence: ' + M10_res[3][i] + '<br>'
            phrase_found += '<br>'

        # 统计饼状图
        pie = []
        stat_len = len(statistic)
        error_type = []
        error_num = []
        for id in range(stat_len):
            temp = statistic[id].split(':')
            error_type.append(temp[0])
            error_num.append(int(temp[1]))
        error_sum = sum(error_num)
        for id in range(stat_len):
            if error_sum != 0:
                pie.append([error_type[id], round(100 * error_num[id] / error_sum, 1)])
            else:
                pie.append([error_type[id], 0])
        # print(pie)

        # 规范性警告
        warning = [0, 0, 0]  # 连续多空格/使用了全角标点/不规范字符(如ﬁ/ﬃ)
        if '  ' in context:
            warning[0] = 1
        for punc in ['，', '。', '？', '！', '“', '”', '‘', '’', '：', '；', '（', '）', '、', '《', '》']:
            if punc in context:
                warning[1] = 1
                break
        if ('ﬁ' in context) | ('ﬃ' in context):
            warning[2] = 1
        # print("warning =", warning)

        # 词云base64转码
        stu_cloud = '<img id="stu_cloud" style="max-width:280px;max-height:280px;float:left" ' + 'src="' + base64_stu + '"></img>'
        fw_cloud = '<img id="fw_cloud" style="max-width:280px;max-height:280px;float:right" ' + 'src="' + base64_fw + '"></img>'
        # cloud = '<img id="fw_cloud" style="max-width:280px;max-height:280px;float:right" ' + 'src="' + base64_ + '"></img>'
        # return word_id, Spell_sum, Grammar_sum, Vocabulary_sum, scores, eva, phrase_found, pie, warning, cloud

    return word_id, Spell_sum, Grammar_sum, Vocabulary_sum, scores, eva, phrase_found, pie, warning, stu_cloud, fw_cloud
