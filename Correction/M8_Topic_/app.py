#####
sys.path.append('/root/code_4999/wy/Correction')
import multiprocessing as mp
import pickle
# pre
import pre
import sys
# M0
from M0_Control import process
# M2
from M2_Preprocess import Preprocess_Para
# M5
import spacy
import random
import os
from nltk.stem.lancaster import LancasterStemmer
import toolbox
# M6
import xlrd
from stanfordcorenlp import StanfordCoreNLP
# M8
from nltk.stem import WordNetLemmatizer, PorterStemmer
from gensim import models
import joblib
import matplotlib as mpl

import matplotlib.pyplot as plt  # 绘制图像的模块

# from wordcloud import WordCloud

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
mpl.use('Agg')

# --------------------------preload--------------------------
# M5
lang = spacy.load("en")
stemmer = LancasterStemmer()
gb_spell = toolbox.loadDictionary("../Correction/M5_Error_Location/resources/en_GB-large.txt")
tag_map = toolbox.loadTagMap("../Correction/M5_Error_Location/resources/en-ptb_map")
pre_M5 = [lang, stemmer, gb_spell, tag_map]

# M6
pre_M6 = []
pre_M6.append('temp')  # 代替[0]的临时变量
Stan = StanfordCoreNLP('../Correction/StanfordCoreNLP')
# pre_M6.append(Stan)

# M8
# word_cloud = WordCloud(background_color="white", width=1000, height=880,max_words=15)
word_cloud = []
# wnl = WordNetLemmatizer()  # 词形还原
wnl = PorterStemmer()
# lda = models.LdaModel.load('../Correction/lda_diction_lemm_tfidf_3000_26_5.model')
lda = models.LdaModel.load('../Correction/M8_Topic_/lda_diction_lemm_tfidf_3000_3_24_5.model')
dictionary = joblib.load('../Correction/M8_Topic_/diction_lda.dict')
# vec = models.Word2Vec.load('../Correction/word2vec_200.w2v')
filee = open('../Correction/M8_Topic_/stwords.txt', 'r', encoding='utf-8')
stop_words = filee.read()
stop_words = stop_words.split('\n')
pre_M8 = [word_cloud, wnl, 'port', lda, dictionary, stop_words]

with open('../Correction/phrase.txt', 'r', encoding='utf-8') as f:
    all = f.readlines()

phrase = []
meaning = []
knowledge = []
example = []
flag = 0
knowledge_temp = ''
for line in all:
    line = line.strip('\n')
    if flag == 1:
        flag = 0
        knowledge_temp = str(line)
        continue
    if len(line) == 0:
        flag = 1
        continue
    phrase.append(line.split('\t')[0].split(' ')[0:-1])
    meaning.append(line.split('\t')[0].split(' ')[-1])
    example.append(line.split('\t')[-1])
    knowledge.append(knowledge_temp)

phrase_string = []
for phrase_one in phrase:
    string = ''
    for word in phrase_one:
        string += word
        string += ' '
    phrase_string.append(string)

pre_M10 = [phrase_string, meaning, knowledge, example]

print("Pre is OK!")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(10))
    is_teacher = db.Column(db.SmallInteger, default=0)
    article = db.relationship("Article", backref="user")
    c0 = db.Column(db.Integer, default=0)
    c1 = db.Column(db.Integer, default=0)
    c2 = db.Column(db.Integer, default=0)
    c3 = db.Column(db.Integer, default=0)
    c4 = db.Column(db.Integer, default=0)
    code = db.Column(db.Integer, default=0)

    def __init__(self, name, password, is_teacher, code):
        self.name = name
        self.password = password
        self.is_teacher = is_teacher
        self.code = code


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    level = db.Column(db.Integer, default=0)

    stat_misspell_num = db.Column(db.Integer, default=0)  # 拼写错误数量,int
    stat_nounerr_num = db.Column(db.Integer, default=0)  # 名词错误数量,int
    stat_verberr_num = db.Column(db.Integer, default=0)  # 动词错误数量,int
    stat_other_num = db.Column(db.Integer, default=0)  # 其他错误数量,int
    stat_sentence_pararatio = db.Column(db.Float, default=0)  # 并列句比例,float
    stat_sentence_compratio = db.Column(db.Float, default=0)  # 复合句比例,float
    stat_sentence_simpratio = db.Column(db.Float, default=0)  # 简单句比例,float
    stat_sentence_passratio = db.Column(db.Float, default=0)  # 被动句比例,float
    stat_sentence_subjratio = db.Column(db.Float, default=0)  # 主动句比例,float
    stat_topic_level = db.Column(db.Integer, default=0)  # 主题切合度等级标号,int,0 - 严重偏题，1 - 轻微偏题，2 - 完美切题

    score_1 = db.Column(db.Integer, default=0)
    score_2 = db.Column(db.Integer, default=0)
    score_3 = db.Column(db.Integer, default=0)
    score_4 = db.Column(db.Integer, default=0)
    score_5 = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)


    def __init__(self, title, content, level):
        self.title = title
        self.content = content
        self.level = level


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST':
        if len(form.password.data) <6:
            flash('密码长度必须大于6')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        users = User.query.all()
        if len(users) == 0:
            return redirect(url_for('user_info_notFound'))
        for i in users:
            if i.name == username:
                if i.password == password:
                    if i.is_teacher == 0:
                        return redirect(url_for('user_info', username=username))
                    else:
                        return redirect(url_for('test', username= username))
                else:
                    return redirect(url_for('user_info_failed'))
        return render_template('user_info_notFound.html')
    return render_template('login.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        is_teacher = request.values.get("character")
        code = request.values.get("valid_code")
        print(is_teacher == "0")
        verify_code = ''.join(random.sample(['Z','Y','X','W','V','U','T','S','R','Q','P','O','N','M','L','K','J','I','H','G','F','E','D','C','B','A','1','2',
                                             '3','4','5','6','7','8','9','0'], 6))
     
        if is_teacher == "1":
            code = verify_code.lower()
            user = User(username, password, is_teacher, code)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('test', username=username))
        if is_teacher == "0":
            if (User.query.filter(User.code == code.lower()).first() == None):
                return "验证码无对应老师"
            else:
                current_teacher = User.query.filter(User.code == code.lower()).first()
                if len(current_teacher.article) != 0:
                    user = User(username, password, is_teacher, code)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('user_info', username=username))
                else:
                    user = User(username, password, is_teacher, code)
                    db.session.add(user)
                    db.session.commit()
                    return "未发布作业"
    return render_template('sign.html', form=form)


@app.route("/teacher_info/<string:username>", methods=['GET', 'POST'])
# 登录成功后跳转至这里
def teacher_info(username):
    current_user = User.query.filter(User.name == username).first()
    code = current_user.code
    print(current_user.name)
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            level = request.values.get("level") #难度分级
            current_user.c0 = request.values.get("criteria_0")
            current_user.c1 = request.values.get("criteria_1")
            current_user.c2 = request.values.get("criteria_2")
            current_user.c3 = request.values.get("criteria_3")
            current_user.c4 = request.values.get("criteria_4")
            article = Article(request.form['title'], request.form['content'], level)
            total_words = len(article.content.split())  # 单词数量
            current_user.article.append(article)
            db.session.add_all([current_user, article])
            db.session.commit()
            flash('Record was successfully added')
            return "Successfully uploaded"
            # redirect(url_for('Judge', content=article.content))
    return render_template('content_.html', code=code.upper())


@app.route("/user_info/<string:username>", methods=['GET', 'POST'])
# 登录成功后跳转至这里
def user_info(username):
    if request.method == 'POST':
        # if not request.form['title'] or not request.form['content']:
        #     flash('Please enter all the fields', 'error')
        if not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            current_user = User.query.filter(User.name == username).first()
            article = Article('title', request.form['content'], 0)
            total_words = len(article.content.split())  # 单词数量
            code = current_user.code.lower()
            current_teacher = User.query.filter(User.code == code).first()
            print(current_teacher.name)
            current_user_criteria = [current_teacher.c0, current_teacher.c1, current_teacher.c2, current_teacher.c3, current_teacher.c4]
            # current_title = current_teacher.article[0].title
            current_content = current_teacher.article[-1].content
            current_level = current_teacher.article[-1].level

            # M8
            tag = current_level
            fw = current_content
            fw_pre = pre.Preprocess(fw)
            fw_depend = []  # nlp依存
            fw_pos = []  # nlp标注
            for sent in fw_pre:
                fw_depend.append(Stan.dependency_parse(sent))
                fw_pos.append(Stan.pos_tag(sent))
            pre_M6.append(fw)
            pre_M6.append(fw_pre)
            pre_M6.append(fw_depend)
            pre_M6.append(fw_pos)
            pre_M6.append(tag)

            # M9
            M9_context = str(article.content)
            # pre_M6_pseudo = [1, 2, 3]
            process_args = (M9_context, pre_M5, pre_M6, pre_M8, pre_M10, current_user_criteria)
            # print(type(current_user_criteria))
            serial = pickle.dumps(process_args)
            pool = mp.Pool()
            after_process = pool.map(process, (process_args,))
            (M9_res, stat_teacher) = after_process[0]
            # M9_res, stat_teacher = process(article.content, pre_M5, pre_M6, pre_M8, pre_M10, current_user_criteria)

            # 存储统计信息
            article.stat_misspell_num, article.stat_nounerr_num, article.stat_verberr_num, article.stat_other_num = stat_teacher[0]
            article.stat_sentence_pararatio, article.stat_sentence_compratio, article.stat_sentence_simpratio = stat_teacher[1]
            article.stat_sentence_passratio, article.stat_sentence_subjratio = stat_teacher[2]
            article.stat_topic_level = stat_teacher[3][0]
            article.score_1, article.score_2, article.score_3, article.score_4, article.score_5, article.total_score= stat_teacher[4]

            current_user.article.append(article)
            db.session.add_all([current_user, article])
            db.session.commit()
            word_id = M9_res[0]
            Spell_sum = M9_res[1]
            Grammar_sum = M9_res[2]
            Vocabulary_sum = M9_res[3]
            scores = M9_res[4]
            eva = M9_res[5]
            phrase_found = M9_res[6]
            pie = M9_res[7]
            warning = M9_res[8]
            stu_cloud = M9_res[9]
            fw_cloud = M9_res[10]

            flash('Record was successfully added')
            pool.close()
            pool.join()
            return render_template('parallel.html', word_id=word_id, Spell_sum=Spell_sum, Grammar_sum=Grammar_sum,
                                   Vocabulary_sum=Vocabulary_sum, scores=scores, eva=eva, phrase_found=phrase_found,
                                   pie=pie, warning=warning, stu_cloud=stu_cloud, fw_cloud=fw_cloud)

            # test = '<div>111</div>'
            # return render_template('test.html', test=test)
            redirect(url_for('Judge', content=article.content))

    # 当前用户历史数据
    havehist = 0  # 有历史为1,无为0
    current_user = User.query.filter(User.name == username).first()
    code = current_user.code
    current_students = User.query.filter(User.code == code.upper()).all()
    current_teachers = User.query.filter(User.code == code.lower()).all()
    title = current_teachers[-1].article[-1].title #"I have a dream."
    scores = []
    for i in range(len(current_students)):
        if current_students[i].name == current_user.name:
            scores.append([])
            if len(current_students[i].article) == 0:  # 没有历史
                scores[i] = []
            else:
                havehist = 1
                for j in range(len(current_students[i].article)):
                    temp = current_students[i].article[j]
                    scores[i].append([temp.content, temp.score_1, temp.score_2, temp.score_3, temp.score_4, temp.score_5, temp.total_score])

    return render_template('content.html', havehist=havehist, scores=scores, title=title)



# @app.route("/user_info_success/<string:username>")
# def user_info_success(username):
    # '<h1>Welcome,%s!</h1>'% username


@app.route("/user_info_failed")
def user_info_failed():
    return '<h1>Please check your password!</h1>'
@app.route("/user_info_notFound")
def user_info_notFound():
    return '<h1>Please sign up first</h1>'


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            article = Article(request.form['title'], request.form['content'])
            db.session.add(article)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('index'))
    return render_template('content.html')


@app.route("/test/<string:username>", methods=['GET', 'POST'])
# 选项卡2测试
def test(username):
    current_user = User.query.filter(User.name == username).first()
    code = current_user.code
    print(current_user.name)
    current_students = User.query.filter(User.code == code.upper()).all()
    names = []
    article_info = []  # 每一篇文章统计信息
    scores = []
    pie_1 = []
    pie_2 = []
    pie_3 = []
    pie_4 = []
    pie_id_1 = ["拼写错误", "名词错误", "动词错误", "其他错误"]
    pie_id_2 = ["并列句", "复合句", "简单句"]
    pie_id_3 = ["被动句", "主动句"]
    pie_id_4 = ["严重偏题", "轻微偏题", "完美切题"]
    pie_number_1 = [0, 0, 0, 0]
    pie_number_2 = [0, 0, 0]
    pie_number_3 = [0, 0]
    pie_number_4 = [0, 0, 0]
    print(current_students)
    for i in range(len(current_students)):
        names.append(current_students[i].name)
        article_info.append([])
        scores.append([])
        if len(current_students[i].article) == 0:
            scores[i] = []
            # article_info[i]= [[0,0,0,0],[0,0,0],[0,0],[0]]
        else:
            for j in range(len(current_students[i].article)):
                temp = current_students[i].article[j]
                scores[i].append(
                    [temp.content, temp.score_1, temp.score_2, temp.score_3, temp.score_4, temp.score_5,
                     temp.total_score])
                if temp.stat_topic_level == 0:
                    pie_number_4[0] += 1
                if temp.stat_topic_level == 1:
                    pie_number_4[1] += 1
                if temp.stat_topic_level == 2:
                    pie_number_4[2] += 1
                pie_number_1[0] += temp.stat_misspell_num
                pie_number_1[1] += temp.stat_nounerr_num
                pie_number_1[2] += temp.stat_verberr_num
                pie_number_1[3] += temp.stat_other_num
                pie_number_2[0] += temp.stat_sentence_pararatio
                pie_number_2[1] += temp.stat_sentence_compratio
                pie_number_2[2] += temp.stat_sentence_simpratio
                pie_number_3[0] += temp.stat_sentence_passratio
                pie_number_3[1] += temp.stat_sentence_subjratio

    pie_sum_1 = pie_number_1[0] + pie_number_1[1]+ pie_number_1[2]+ pie_number_1[3]
    pie_sum_2 = pie_number_2[0] + pie_number_2[1] + pie_number_2[2]
    pie_sum_3 = pie_number_3[0] + pie_number_3[1]
    pie_sum_4 = pie_number_4[0] + pie_number_4[1] + pie_number_4[2]
    if pie_sum_1 == 0:
        pie_sum_1 = 0.001
    if pie_sum_2 == 0:
        pie_sum_2 = 0.001
    if pie_sum_3 == 0:
        pie_sum_3 = 0.001
    if pie_sum_4 == 0:
        pie_sum_4 = 0.001
    for i in range(len(pie_number_1)):
        pie_1.append([pie_id_1[i], round(100 * pie_number_1[i] / pie_sum_1, 1)])
    for i in range(len(pie_number_2)):
        pie_2.append([pie_id_2[i], round(100 * pie_number_2[i] / pie_sum_2, 1)])
    for i in range(len(pie_number_3)):
        pie_3.append([pie_id_3[i], round(100 * pie_number_3[i] / pie_sum_3, 1)])
    for i in range(len(pie_number_4)):
        pie_4.append([pie_id_4[i], round(100 * pie_number_4[i] / pie_sum_4, 1)])

                # article_info[i].append([])
                # article_info[i][j].append(temp.content)
                # article_info[i][j].append([temp.stat_misspell_num, temp.stat_nounerr_num, temp.stat_verberr_num, temp.stat_other_num])
                # article_info[i][j].append([temp.stat_sentence_pararatio, temp.stat_sentence_compratio, temp.stat_sentence_simpratio])
                # article_info[i][j].append([temp.stat_sentence_passratio, temp.stat_sentence_subjratio])
                # article_info[i][j].append([temp.stat_topic_level])
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            level = request.values.get("level")  # 难度分级
            current_user.c0 = request.values.get("criteria_0")
            current_user.c1 = request.values.get("criteria_1")
            current_user.c2 = request.values.get("criteria_2")
            current_user.c3 = request.values.get("criteria_3")
            current_user.c4 = 100 - int(current_user.c0) - int(current_user.c1) - int(current_user.c2) - int(current_user.c3)
            article = Article(request.form['title'], request.form['content'], level)
            total_words = len(article.content.split())  # 单词数量
            current_user.article.append(article)
            db.session.add_all([current_user, article])
            db.session.commit()
            flash('Record was successfully added')
            return "Successfully uploaded"
    print(pie_1)
    return render_template('new_parallel.html', names=names, length=len(names), code=code.upper(), scores=scores, pie_1=pie_1, pie_2=pie_2, pie_3=pie_3, pie_4=pie_4)#article_info = article_info)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=4999)
