#####
import sys
sys.path.append('../Correction')

# M0
from M0_Control_Test import process
# M5
import spacy
import os
from nltk.stem.lancaster import LancasterStemmer
import scripts.toolbox as toolbox
# M6
from stanfordcorenlp import StanfordCoreNLP

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(10))
    article = db.relationship("Article", backref="user")

    def __init__(self, name, password):
        self.name = name
        self.password = password

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST':
        if len(form.password.data) < 8:
            flash('密码长度必须大于8')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        users = User.query.all()
        for i in users:
            if i.name == username:
                if i.password == password:
                    return redirect(url_for('user_info', username=username))
                else:
                    return redirect(url_for('user_info_failed'))
        return render_template('user_info_notFound.html')
    return render_template('login.html', form=form)

@app.route('/sign_up', methods=['GET','POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_info', username=username))
    return render_template('sign.html', form=form)


@app.route("/user_info/<string:username>", methods=['GET', 'POST'])
# 登录成功后跳转至这里
def user_info(username):
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            current_user = User.query.filter(User.name == username).first()
            article = Article(request.form['title'], request.form['content'])
            current_user.article.append(article)
            db.session.add_all([current_user, article])
            db.session.commit()

            # --------------------------preload--------------------------
            # M5
            lang = spacy.load("en")
            stemmer = LancasterStemmer()
            gb_spell = toolbox.loadDictionary("../Correction/M5_Error_Location/resources/en_GB-large.txt")
            tag_map = toolbox.loadTagMap("../Correction/M5_Error_Location/resources/en-ptb_map")
            M5 = [lang, stemmer, gb_spell, tag_map]

            # M6
            M6 = StanfordCoreNLP('../Correction/StanfordCoreNLP')

            suggestion, spell_score, grammar_score, statistic, content, \
            M6_res, M7_score, M7_eva, M8_score, M8_eva = process(article.content, M5, M6)

            flash('Record was successfully added')
            return render_template('autoparallel.html')
            # redirect(url_for('Judge', content=article.content))
    return render_template('content.html')



#@app.route("/user_info_success/<string:username>")
#def user_info_success(username):
    #'<h1>Welcome,%s!</h1>'% username


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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')
    # ,host='0.0.0.0'
