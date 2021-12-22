# 陈述句
def declarative(sentence, nlp_depend, nlp_pos):
    total = len(sentence)
    judge = 0
    for i in range(0, total):
        flag = 0
        temp = sentence[i].strip('\n').strip('.?,!').lower().split(' ')
        punc = sentence[i].strip('\n')[-1]
        # 包括了基本疑问句和感叹句的形式
        if (temp[0] in ['what', 'who', 'whom', 'where', 'which', 'when', 'whose', 'why', 'how',
                        'can', 'could', 'will', 'would', 'must', 'may', 'might', 'shall', 'should',
                        'am', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did'])\
                & (punc in ["!", "?"]):
            flag = 1
            judge += 1

        else:
            pos = nlp_pos[i]
            # 包括了反义疑问句的形式
            for j in range(0, len(pos)):
                if pos[j][0] == "n't":
                    if (j < len(pos)-1) & (j > 1):
                        if (pos[j-2][0] == ',') & (pos[j+1][1] == 'PRP'):  # 反义疑问句
                            flag = 1
                            judge += 1
                            break
                elif pos[j][0] in ["can", "could", "will", "would", "must", "may", "might",
                                   "shall", "should", "am", "is", "are", "was", "were",
                                   "have", "has", "had", "do", "does", "did"]:
                    if (j < len(pos) - 1) & (j > 0):
                        if (pos[j-1][0] == ',') & (pos[j+1][1] == 'PRP'):  # 反义疑问句
                            flag = 1
                            judge += 1
                            break

            if flag == 0:
                # 包括了祈使句的形式
                # Let、无主语、动词原形、Don't
                if (temp[0] in ["don't", "let", "let's", "please", "no"]) or (temp[-1] == "please"):
                    flag = 1
                    judge += 1
                else:
                    # 若句中无'nsubj', "nsubjpass"则认为是祈使句
                    stru = nlp_depend[i]
                    time = 0  # nsubj出现次数
                    for j in stru:
                        if j[0] in ['nsubj', "nsubjpass"]:
                            time += 1

                    # 还需要排除there should/must/... be的情况,实测
                    for k in range(0, len(temp)):
                        if temp[k] == 'there':
                            while k < min(len(temp)-1, k+2):  # be后2个单词/句长以内
                                k += 1
                                if temp[k] == 'be':
                                    time += 1
                                    break

                    if time == 0:
                        flag = 1
                        judge += 1

    judge = total - judge  # 陈述句个数;之前的judge是非陈述句个数
    rate = round(100*judge/total, 2)

    return rate
