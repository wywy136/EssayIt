# 复合句
def complex(sentence, nlp_depend, nlp_pos):
    total = len(sentence)
    judge1 = 0  # 复合句
    judge2 = 0  # 简单句
    num = 0

    for i in range(0, total):
        num += 1
        flag1 = 0  # 简单句
        flag2 = 0  # 复合句
        temp1 = nlp_depend[i]
        temp2 = sentence[i].split(' ')
        t = len(temp2)
        for iii in range(t):
            if temp2[t-1-iii] == '':
                temp2.pop(t-1-iii)

        for j in temp1:
            if ('advcl' in j) or ('expl' in j) or('csubj' in j) or('csubjpass' in j) or('xsubj' in j) or('mark' in j):
                # 状语从句,状语从句，从句的主要动词
                flag2 = 1
                judge1 += 1
                break
            if ('cc' in j) or ('cc:preconj' in j):
                flag1 = 1
                break
            if temp2[0] in ['Although']:
                flag1 = 1
                break

            for p in range(0, len(temp2)):
                if temp2[p] in ['rather', 'while']:
                    flag1 = 1
                    break
                elif (temp2[p] in [',']) & (p < len(temp2)-1):
                    if temp2[p + 1] in ['else', 'otherwise', 'yet', 'still', 'however', 'for', 'hence', 'so']:
                        flag1 = 1
                        break
        if flag2 == 0:
            pos = nlp_pos[i]

            for k in range(0, len(temp2)):
                if temp2[k] in ['that', 'whether']:
                    if (temp2[0] in ['It']) or(temp2[0] in ['Is'] and temp2[0] in ['Is']):
                        flag2 = 1
                        judge1 += 1
                        break
                    elif temp2[k-1] in ['it'] and (k != 0):
                        flag2 = 1
                        judge1 += 1
                        break
                if pos[k][1] in ['WRB', 'WP', 'WP$', 'WDT']:
                    if pos[k-1][1] in ['NN'] and (k != 0):
                        flag2 = 1
                        judge1 += 1
                        break
            if flag2 == 0:  # 不是复合句
                if flag1 == 0:  # 不是并列句
                    judge2 += 1  # 是简单句

    rate1 = round(100 * judge1 / total, 2)  # 复合句
    rate2 = round(100 * judge2 / total, 2)  # 简单句
    return rate1, rate2
