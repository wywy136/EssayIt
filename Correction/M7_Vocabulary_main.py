# 主函数：M7_Vocabulary_main
# 总输入：从键盘输入自己的英语水平等级（1.小学 2.初中 3.高中 4.大学四级 5.大学六级）/作文要求的字数
# 总输出：Richness，Replace0，Replace1，Count，Get_Score的所有返回值
import M7_Vocabulary_Open  # 打开文件 分句分词
import M7_Vocabulary_Word_Distribution  # 词频,下标统计
import M7_Vocabulary_Richness  # 单词丰富度
import M7_Vocabulary_Replace0  # 替换使用次数过多的词
import M7_Vocabulary_Replace1  # 替换低级词汇为更高级近义词
import M7_Vocabulary_Count  # 文章字数是否合格
import M7_Vocabulary_Get_Score  # 计算总分


if __name__ == "__main__":
    word_seped = M7_Vocabulary_Open.Open()

    print("请输入您的词汇水平：1.小学 2.初中 3.高中 4.大学四级 5.大学六级")
    level=input()
    print("请输入作文要求的字数：")
    num=input()

    dict_occur=M7_Vocabulary_Word_Distribution.Word_Distribution_Occur(word_seped)
    dict_index=M7_Vocabulary_Word_Distribution.Word_Distribution_Index(word_seped)

    # Richness，Replace0，Replace1，Count函数返回值是一个元组，[0]是int类型的score，[1]是字符串类型的evaluation.
    print(M7_Vocabulary_Count.Count(num, dict_occur)[1])
    print(M7_Vocabulary_Richness.Richness(dict_occur)[1])
    print(M7_Vocabulary_Replace0.Replace0(dict_occur)[1])
    print(M7_Vocabulary_Replace1.Replace1(dict_occur,dict_index,int(level)-1)[1])

    print(M7_Vocabulary_Get_Score.Get_Score(
        (M7_Vocabulary_Count.Count(num,dict_occur)[0]),
        (M7_Vocabulary_Replace0.Replace0(dict_occur)[0]),
        (M7_Vocabulary_Replace1.Replace1(dict_occur,dict_index,int(level)-1)[0]),
        (M7_Vocabulary_Richness.Richness(dict_occur)[0])
    )
    )
