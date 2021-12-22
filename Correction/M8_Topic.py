import re,math
from gensim import models
import base64
import joblib
# import matplotlib.pyplot as plt  # 绘制图像的模块
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt  # 绘制图像的模块


def port_stem(doc_test,wnl):
    texts_out = []
    for i in range(len(doc_test)):
        texts_out.append(wnl.stem(doc_test[i]))
    return texts_out


def preprocss(lists,wnl,stop_words):
    texts_out=[]
    for strr in lists:
        mystrr = re.sub(r'[\'+\’: ,./!?\[\]\"#@`8765412309%\<\>=^*&$;-]', ' ', strr)
        filestr=mystrr.lower().split()
        texts_out.extend(filestr)
    guodu=[]
    for word in texts_out:
        if (word not in stop_words) and (len(word) > 2):guodu.append(word)
    texts_out=[]
    for i in range(len(guodu)):texts_out.append(wnl.stem(guodu[i]))

    return texts_out


def get_topic_words(corpus,lda):
    topic = lda.get_document_topics(corpus,minimum_probability=0)
    topic = sorted(topic, key=lambda weight: weight[1], reverse=True)
    return topic


def mycosine(topic,titletopic):
    length=min(len(topic),len(titletopic))
    sum=0
    sq1=0
    sq2=0
    for i in range(length):
        sum += topic[i][0] * titletopic[i][0]
        sq1 += pow(topic[i][0], 2)
        sq2 += pow(titletopic[i][0], 2)
    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)),3)
    except ZeroDivisionError:
        result = 0.0
    if result==0:
        result=1
    return result


def simlary(doc_test,title_test,pre_M8):
    wnl = pre_M8[1]
    lda = pre_M8[3]
    dictionary = pre_M8[4]

    doc_test=port_stem(doc_test,wnl)
    texts=[]
    texts.insert(0,doc_test)
    title_test=port_stem(title_test,wnl)
    texts.insert(0,title_test)
    corpus=[dictionary.doc2bow(line) for line in texts]
    titletopic=get_topic_words(corpus[0],lda)
    topic = get_topic_words(corpus[1],lda)
    return topic,titletopic,mycosine(topic,titletopic)


def score(similarity, engagement, lang):
    comment1, score1 = engagement
    level = -1

    if lang == 'cn':
        if similarity > 0.865:
            score = 100
            comment = "完美切题,做的不错!"
            level = 2
        elif similarity > 0.845:
            score = 80
            comment = "文章主题和题干切合度一般,建议进一步向主题靠拢."
            level = 1
        elif similarity > 0.806:
            score = 60
            comment = "文章主题偏离题干要求较严重,建议修正."
            level = 1
        else:
            score = 50
            comment = "文章主题严重偏离题干要求,务必修正!"
            level = 0
    elif lang == 'en':
        if similarity > 0.865:
            score = 100
            comment = "The theme of your essay is rather relevant to the theme of model essay. Well done! "
            level = 2
        elif similarity > 0.845:
            score = 80
            comment = "The theme of your essay is a little relevant to the theme of model essay. You'd better make your essay more relevant."
            level = 1
        elif similarity > 0.806:
            score = 60
            comment = "The theme of your essay diverges from the theme of model essay. You'd better revise your essay. "
            level = 1
        else:
            score = 50
            comment = "The theme of your essay diverges greatly from the theme of model essay. Please revise your essay! "
            level = 0

    score = int(score * 0.9 + score1 * 0.1 + 0.5)
    comment = comment+comment1
    return score, comment, level


def engagement(topic, lang):
    num = 0
    for word in topic:
        if word[1] > 0.35:
            num += 1
    if lang == 'cn':
        if num > 3:
            comment = '主题分布分散,可能会令人疑惑.'
            score = 80
        else:
            comment = '主题分布集中,做的不错!'
            score = 100
    elif lang == 'en':
        if num > 3:
            comment = 'Theme is scattered and can be confusing.'
            score = 80
        else:
            comment = 'Theme in concentration. Well done!'
            score = 100

    return comment, score


def draw(doc, fanwen, pre_M8, lang):
    topic, titletopic, sim = simlary(doc, fanwen, pre_M8)
    engage = engagement(topic, lang)
    s, c, level = score(sim, engage, lang)

    x = range(24)
    y_test = [0] * 24
    y_train = [0] * 24
    for i in range(len(topic)):
        y_train[titletopic[i][0]] = titletopic[i][1]
        y_test[topic[i][0]] = topic[i][1]

    plt.ylim(0, 1)
    # index_ls = ['\n'+'Diet', 'Family', '\n'+'System', 'Traffic', '\n'+'Success', 'Religion', '\n'+'Media', 'Person', '\n'+'Product',
    #             '\n'+'\n'+'Books&reading', 'Computer', '\n'+'Gift', 'Work', '\n'+'Life', 'Celebrity', '\n'+'\n'+'Country', '\n'+'Game',
    #             'Law', '\n'+'Sports', '\n'+'\n'+'Rules&Prestige', 'Interest', '\n'+'File&program', 'Festival',
    #             '\n'+'\n'+'School&teaching']
    if lang == 'cn':
        plt.plot(x, y_test, marker='*', label='你的文章')
        # plt.xticks(x,index_ls) ## 可以设置坐标字
        # plt.tick_params(labelsize=6)
        plt.legend(fontsize='x-large')
        plt.title("你的文章")
        plt.xlabel('主题')
        plt.ylabel('概率')
        c += "<br><br>PS:27个主题如下:<br>饮食,家庭,系统,交通,成功,宗教,媒体,独处,产品,书籍和阅读,科技,礼物,工作,生活,名人,国家,游戏,法律,运动,规则,兴趣,文化,节日,教育,身边人物,道德,活动"
    elif lang == 'en':
        plt.plot(x, y_test, marker='*', label='Your Essay')
        # plt.xticks(x,index_ls) ## 可以设置坐标字
        # plt.tick_params(labelsize=6)
        plt.legend(fontsize='x-large')
        plt.title("Your Essay")
        plt.xlabel('Themes')
        plt.ylabel('Probability')
        c += "<br><br>PS: The specific contents of 27 topics are as follows:<br>Catering culture, Famil, System, Traffic, Success, Religion, Media, Person, Product, Books&Reading, Computer, Gift, Work, Life, Celebrity, Country, Games, Law, Sports, Rules&Reputation, Interest, File&Program, Festival, School&Teaching, People around，Morality，Activity"

    plt.savefig("../Web/static/img/M8_stu.png")
    plt.clf()
    plt.ylim(0, 1)
    plt.plot(x, y_train, marker='.', label='model_essay')
    # index_ls = ['\n'+'Diet', 'Family', '\n'+'System', 'Traffic', '\n'+'Success', 'Religion', '\n'+'Media', 'Person', '\n'+'Product',
    #             '\n'+'\n'+'Books&reading', 'Computer', '\n'+'Gift', 'Work', '\n'+'Life', 'Celebrity', '\n'+'Country', '\n'+'\n'+'Game',
    #             'Law', '\n'+'Sports', '\n'+'\n'+'Rules&Prestige', 'Interest', '\n'+'File&program', 'Festival',
    #             '\n'+'\n'+'School&teaching']
    plt.legend(fontsize='x-large')
    # plt.xticks(x,index_ls) ## 可以设置坐标字
    # plt.tick_params(labelsize=6)
    plt.title("Model Essay")
    plt.xlabel('Themes')
    plt.ylabel('Probability')
    plt.savefig("../Web/static/img/M8_fw.png")
    stu = open("../Web/static/img/M8_stu.png", 'rb')
    base64_stu= 'data:image/png;base64,' + base64.b64encode(stu.read()).decode()
    fw = open("../Web/static/img/M8_fw.png", 'rb')
    base64_fw = 'data:image/png;base64,' + base64.b64encode(fw.read()).decode()
    return s, c, level, base64_stu, base64_fw


def call_on(sentence, fw, pre_M8, lang):
    wnl = pre_M8[1]
    stop_words=pre_M8[5]
    # word_cloud = pre_M8[0]
    doc = preprocss(sentence,wnl,stop_words)
    fanwen = preprocss(fw,wnl,stop_words)
    return draw(doc,fanwen,pre_M8, lang)
    # topic, titletopic, sim = simlary(doc, fanwen, pre_M8)
    # engage = engagement(topic)

    # word_to_cloud(doc, word_cloud).to_file('../Web/static/img/M8_stu.png')
    # word_to_cloud(fanwen, word_cloud).to_file('../Web/static/img/M8_fw.png')

    # stu = open("../Web/static/img/M8_stu.png", 'rb')
    # base64_stu = 'data:image/png;base64,' + base64.b64encode(stu.read()).decode()
    # fw = open("../Web/static/img/M8_fw.png", 'rb')
    # base64_fw = 'data:image/png;base64,' + base64.b64encode(fw.read()).decode()

    # s, c, level = score(sim, engage)

    # return s, c, level, base64_stu, base64_fw
