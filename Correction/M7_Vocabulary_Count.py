def Count(fw_num, my_num, lang):
    if lang == 'cn':
        total = "范文单词数量是"+str(fw_num)+","+"您的作文单词数量是"+str(my_num)
        score3_3 = 25
        evaluation_3 = ",字数基本符合要求!"
        if (abs(fw_num-my_num)/fw_num) > 0.1:
            score3_3 = int(25-62.5*((abs(fw_num-my_num)/fw_num)-0.1))  # 这里分数向下取整了
            if score3_3 < 0:
                score3_3 = 0
            if 17 <= score3_3 < 25:
                if my_num < fw_num:
                    evaluation_3 = ",字数较少,可适当丰富文章内容"
                else:
                    evaluation_3 = ",字数较多,可适当删减文章篇幅"
            elif 9 <= score3_3 < 17:
                if my_num < fw_num:
                    evaluation_3 = ",字数少,建议丰富文章内容"
                else:
                    evaluation_3 = ",字数多,建议删减文章篇幅"
            else:
                if my_num < fw_num:
                    evaluation_3 = ",字数过少,看来您需要好好丰富一下文章内容了"
                else:
                    evaluation_3 = ",字数过多,看来您需要对文章篇幅做较大的删减了"
        evaluation1_3 = "您的字数得分为"+str(score3_3)+"分, "+total+evaluation_3
    elif lang == 'en':
        total = "The word count of model essay is " + str(fw_num) + "," + " your word count is " + str(my_num)
        score3_3 = 25
        evaluation_3 = ", your word basically meets the requirement!"
        if (abs(fw_num - my_num) / fw_num) > 0.1:
            score3_3 = int(25 - 62.5 * ((abs(fw_num - my_num) / fw_num) - 0.1))  # 这里分数向下取整了
            if score3_3 < 0:
                score3_3 = 0
            if 17 <= score3_3 < 25:
                if my_num < fw_num:
                    evaluation_3 = ", the number of words is a little small, and the content of the article can be appropriately enriched"
                else:
                    evaluation_3 = ", the number of words is a little large, and the content of the article can be appropriately reduced"
            elif 9 <= score3_3 < 17:
                if my_num < fw_num:
                    evaluation_3 = ", the number of words is small, and the content of the article should be enriched"
                else:
                    evaluation_3 = ", the number of words is large, and the content of the article should be reduced"
            else:
                if my_num < fw_num:
                    evaluation_3 = ", the number of words is too small, and the content of the article should be enriched greatly"
                else:
                    evaluation_3 = ", the number of words is too large, and the content of the article should be reduced greatly"
        evaluation1_3 = "Your word count score is " + str(score3_3) + ", " + total + evaluation_3

    return score3_3, evaluation1_3