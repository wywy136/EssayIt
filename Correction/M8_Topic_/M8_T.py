import re,math
from nltk.stem import WordNetLemmatizer,PorterStemmer
from gensim import models
from stop_words import get_stop_words
import base64
import joblib
#from wordcloud import WordCloud
#import matplotlib.pyplot as plt  # 绘制图像的模块


def port_stem(doc_test, wnl):
    texts_out = []
    for i in range(len(doc_test)):
        # texts_out.append(port.stem(doc_test[i]))
        texts_out.append(wnl.lemmatize(doc_test[i]))
    return texts_out


def preprocss(lists):
    en_stop = get_stop_words('en')
    en_stop.extend(
        ['from', 're', 'edu', 's', 'ed', 'in', 'at', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    texts_out=[]
    for strr in lists:
        mystrr = re.sub(r'[\'\’: ,./!?\"#@;-]', ' ', strr)
        filestr=mystrr.lower().split()
        texts_out.extend(filestr)
    guodu=[]
    for word in texts_out:
        if (word not in en_stop) and (len(word) > 2):
            guodu.append(word)
    return guodu


def text_vec(doc, vec):
    exten=[]
    for word in doc:
        if word not in vec:
            exten.extend([word])
        else:
            exten.extend([x[0] for x in vec.most_similar(word,topn=5)])
    return exten


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


def simlary(doc_test,title_test, pre_M8):
    wnl = pre_M8[1]
    lda = pre_M8[3]
    dictionary = pre_M8[4]
    vec = pre_M8[5]

    doc_test = text_vec(doc_test, vec)
    doc_test = port_stem(doc_test, wnl)
    texts = []
    texts.insert(0, doc_test)
    # print(title_test)
    title_test = text_vec(title_test, vec)
    # print('title_test',title_test)
    title_test = port_stem(title_test, wnl)
    texts.insert(0, title_test)
    corpus = [dictionary.doc2bow(line) for line in texts]
    # corpus_tidff = models.TfidfModel(corpus)[corpus]
    # topic=get_topic_words(corpus_tidff[0])
    # titletopic = get_topic_words(corpus_tidff[1])
    # pprint(corpus_tidff)
    topic = get_topic_words(corpus[0], lda)
    titletopic = get_topic_words(corpus[1], lda)
    return topic, titletopic, mycosine(topic, titletopic)


def get_topic_words(corpus, lda):
    topic = lda.get_document_topics(corpus)
    # topic=lda.top_topics(dictionary=dictionary,corpus=corpus,topn=20)
    # print(topic)
    topic = sorted(topic, key=lambda weight: weight[1], reverse=True)
    # print(topic)
    return topic


def score(similarity, engagement):
    comment1, score1 = engagement
    level = -1
    if similarity > 0.88:
        score = 100
        comment = "The theme of your essay is rather relevant to the theme of model essay. Well Done!"
        level = 2
    elif similarity > 0.6:
        score = 80
        comment = "The theme of your essay diverges slightly from the theme of model essay. "
        level = 1
    elif similarity > 0:
        score = 60
        comment = "The theme of your essay diverges from the theme of model essay. You have better revise your essay."
        level = 1
    else:
        score = 50
        comment = "The theme of your essay diverges significantly from the theme of model essay. Please revise!"
        level = 0
    score = int(score * 0.9 + score1 * 0.1 + 0.5)
    comment = comment+comment1
    return score, comment, level


def word_to_cloud(words, word_cloud):
    word = (" ".join(words))
    # print('word_to_cloud',word)
    wordcloud = word_cloud.generate(word)
    return wordcloud
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()


def engagement(topic):
    num = 0
    for word in topic:
        if word[1] > 0.2:
            num += 1
    if num > 4:
        comment = 'Theme in divergence. Others may get confused!'
        score = 80
    else:
        comment = 'Theme in concentration. Well Done! '
        score = 100
    return comment, score


# def _split_sentences(texts):
#     splitstr = '.!?。！？;'
#     start = 0
#     index = 0  # 每个字符的位置
#     sentences = []
#     for text in texts:
#         if text in splitstr:  # 检查标点符号下一个字符是否还是标点
#             sentences.append(texts[start:index + 1])  # 当前标点符号位置
#             start = index + 1  # start标记到下一句的开头
#         index += 1
#     if start < len(texts):
#         sentences.append(texts[start:])  # 这是为了处理文本末尾没有标
#     return sentences
# 
#
def call_on(sentence, fw, pre_M8):
    word_cloud = pre_M8[0]
    doc = preprocss(sentence)
    fanwen = preprocss(fw)
    topic, titletopic, sim = simlary(doc, fanwen, pre_M8)
    engage = engagement(topic)

    # print(str(doc))
    # print(str(fanwen))

    # word_to_cloud(doc, word_cloud).to_file('../Web/static/img/M8_stu.png')
    # word_to_cloud(fanwen, word_cloud).to_file('../Web/static/img/M8_fw.png')

    stu = open("../Web/static/img/M8_stu.png", 'rb')
    base64_stu = 'data:image/png;base64,' + base64.b64encode(stu.read()).decode()
    fw = open("../Web/static/img/M8_fw.png", 'rb')
    base64_fw = 'data:image/png;base64,' + base64.b64encode(fw.read()).decode()

    s, c, level = score(sim, engage)

    return s, c, level, base64_stu, base64_fw
