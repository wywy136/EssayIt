import paramiko
import os
import M4_Correct
# 实验室版本
import time


def Grammar_Correction(Spell_corrected_context):  # 服务器读取(默认参数为1本地-实验室,参数为0云服务器, 参数为2：全部操作都在实验室服务器 )

    print("=============M4 GEC Model Running=============")

    M4_start_time = time.time()
    # os.system('python ../Correction/shell.py')
    # 10.22: Correct函数返回修改语法错误之后的句子，list类型
    new_grammar = M4_Correct.Correct(Spell_corrected_context)
    # ori_grammar = Spell_corrected_context

    print("new_grammar,",time.time() - M4_start_time)
    # # 读取改语法前后的句子
    # print("=============M4 Following Processing=============")
    # f = open('../Correction/M4_M5_Data/test.error.sent')
    # ori_grammar = f.read()
    # f.close()
    # f = open('../Correction/M4_M5_Data/corrected.sent')
    # new_grammar = f.read()
    # f.close()
    with open('../Correction/M4_M5_Data/ourprd_withoutrule', 'w') as prd:
        # for i in new_grammar:
        #     prd.write(i + '\n')
        prd.write('\n'.join(new_grammar))
    print('have written')
    print(time.time() - M4_start_time)
    # ———————————Rule1:对模型的'分割操作进行修正———————————
    print("=============M4 Following Process=============")
    for i in range(len(new_grammar)):
        new_grammar[i] = new_grammar[i].replace("s ' ", "s' ")
        new_grammar[i] = new_grammar[i].replace(" 's", "'s")
        new_grammar[i] = new_grammar[i].replace(" n't", "n't")
        new_grammar[i] = new_grammar[i].replace(" 've", "'ve")
        new_grammar[i] = new_grammar[i].replace(" 'm", "'m")
        # 新发现的补充规则
        new_grammar[i] = new_grammar[i].replace("U . S .", "U.S.")

    with open('../Correction/M4_M5_Data/ourprd_withrule', 'w') as prd:
        # for i in new_grammar:
        #     prd.write(i + '\n')
        prd.write('\n'.join(new_grammar))

    # f = open('../Correction/M4_M5_Data/corrected.sent', 'w')
    # f.write(new_grammar)
    # f.close()

    # a = ori_grammar.split('\n')
    # if a[-1] == '':
    #     del a[-1]
    # b = new_grammar.split('\n')
    # if b[-1] == '':
    #     del b[-1]

    return new_grammar


if __name__ == '__main__':
    context = open('./M4_M5_Data/fce.test.src').read()
    gui_left_content = context.split('\n')
    Grammar_corrected_context = Grammar_Correction(gui_left_content)
