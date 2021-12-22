# 并列句
def compound(sentence, nlp_depend, nlp_pos):
    total = len(sentence)
    judge = 0

    for i in range(0, total):
        flag = 0
        temp1 = nlp_depend[i]
        temp2 = sentence[i].lower().split(' ')

        for j in temp1:
            if ('cc' in j) or ('cc:preconj' in j):
                flag = 1
                judge += 1
                break

        if temp2[0] in ['although']:
            flag = 1
            judge += 1
        else:
            for k in range(0, len(temp2)):
                if temp2[k] in ['rather', 'while']:
                    flag = 1
                    judge += 1
                    break
                elif (temp2[k] in [',']) & (k != len(temp2)-1):
                    if temp2[k+1] in ['else', 'otherwise', 'yet', 'still', 'however', 'for', 'hence', 'so']:
                        flag = 1
                        judge += 1
                        break

    rate = round(100 * judge / total, 2)
    return rate