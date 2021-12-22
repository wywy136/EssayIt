# 被动句
def passive(sentence, nlp_depend, nlp_pos):
    total = len(sentence)
    judge = 0
    for i in range(total):
        flag = 0  # 被动的标志;一旦为1,即被动,不用接着判断了
        temp = nlp_depend[i]

        for j in temp:
            if 'nsubjpass' in j:  # 陈述式被动
                flag = 1
                judge += 1
                break

        if flag == 0:  # 不是陈述被动
            temp = sentence[i].strip('\n').strip('.?,!').lower().split(' ')
            if sentence[i].strip('\n').endswith('?'):  # 结尾[?](疑问句)
                k = 0
                for k in range(len(temp)):
                    if temp[k] in ['am', 'is', 'are', 'be', 'was', 'were', 'been', 'being']:
                        pos = nlp_pos[i]
                        while k < min(len(temp)-1, k+4):  # be后4个单词/句长以内
                            k += 1
                            if pos[k][1] in ['VBD', 'VBN']:  # 疑问式被动·be
                                flag = 1
                                judge += 1
                                break

                    # 如果疑问句中有2重被动,判断出1重后直接break,不做多余的事
                    if flag == 1:
                        break

            # need doing类型;此处就不考虑need doing的疑问句形式了,没见过
            elif ('need' in temp) or ('needs' in temp) or ('needed' in temp):
                for k in range(len(temp)):
                    if temp[k] in ['need', 'needs', 'needed']:
                        if k < len(temp):  # need不位于句尾
                            if temp[k+1].endswith('ing'):
                                flag = 1
                                judge += 1
                                break

    rate = round(100*judge/total, 2)
    return rate
