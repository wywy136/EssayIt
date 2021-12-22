#文件7：M7_Vocabulary_Get_Score#计算总分
#函数名：Get_Score
#输入：单词丰富度得分，单词使用次数得分，单词高级程度得分，字数得分
#返回：总分
def Get_Score(a,b,c,d):
    score_3=a+b+c+d
    # score3="您在单词评估模块的总得分为："+str(score_3)+"分"
    score3 = str(score_3)
    return score3