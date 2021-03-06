from flask import Flask, render_template, redirect, request
from flask_login import login_required, logout_user, login_user, LoginManager, current_user
from future.backports.datetime import datetime

from data import db_session
from data.category import Category
from data.message import Message
from data.subcategory import Subcategory
from data.topic import Topic
# from flask_ngrok import run_with_ngrok
from data.user import User
from forms.message import MessageForm
from forms.topic import TopicForm
from forms.user import RegisterForm
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
# run_with_ngrok(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    category = db_sess.query(Category)
    subcategory = db_sess.query(Subcategory)
    return render_template("index.html", category=category, subcategory=subcategory)


@app.route("/subcategory/<name>")
def subcategory_name(name):
    db_sess = db_session.create_session()
    subcategory = db_sess.query(Subcategory).filter(Subcategory.name == name).first()
    topic = db_sess.query(Topic).filter(Topic.subcategory_id == subcategory.id)
    return render_template("subcategory.html", topic=topic, subcategory=subcategory)


@app.route("/subcategory/<name>/topic/<name1>", methods=['GET', 'POST'])
def topic_name(name, name1):
    db_sess = db_session.create_session()
    subcategory = db_sess.query(Subcategory).filter(Subcategory.name == name).first()
    topic = db_sess.query(Topic).filter(Topic.subcategory_id == subcategory.id, Topic.name == name1).first()
    message = db_sess.query(Message).filter(Message.topic_id == topic.id).all()
    authors = {topic.creator: db_sess.query(User).filter(User.id == topic.creator).first().name}
    for i in message:
        authors[i.author] = db_sess.query(User).filter(User.id == i.author).first().name
    if request.method == "POST":
        for i in message:
            try:
                request.form[str(i.id)]
            except Exception:
                pass
            else:
                i.like += 1
            db_sess.commit()
    return render_template("topic.html", topic=topic, message=message, subcategory=subcategory, authors=authors)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="???????????????????????? ?????????? ?????? ????????????",
                               form=form)
    return render_template('login.html', title='??????????????????????', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="???????????? ???? ??????????????????")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="?????????? ???????????????????????? ?????? ????????")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='??????????????????????', form=form)


@app.route('/subcategory/<subc>/topic',  methods=['GET', 'POST'])
@login_required
def add_topic(subc):
    form = TopicForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        topic = Topic()
        topic.name = form.name.data
        topic.text = form.text.data
        topic.time = datetime.now()
        sc = db_sess.query(Subcategory).filter(Subcategory.name == subc).first()
        topic.subcategory_id = sc.id
        topic.user = current_user
        current_user.topic.append(topic)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/subcategory/{subc}')
    return render_template('add_topic.html', title='???????????????????? ????????',
                           form=form)


@app.route('/subcategory/<subc>/topic/<topic>/message',  methods=['GET', 'POST'])
@login_required
def add_message(subc, topic):
    form = MessageForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        message = Message()
        message.text = form.text.data
        message.time = datetime.now()
        message.topic_id = db_sess.query(Topic).filter(Topic.name == topic).first().id
        message.author = current_user
        current_user.message.append(message)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/subcategory/{subc}/topic/{topic}')
    return render_template('add_message.html', title='???????????????????? ??????????????????',
                           form=form)


@app.route("/in_work")
def in_work():
    return '???????????????? ?????????????????? ?? ????????????'


if __name__ == '__main__':
    db_session.global_init("db/forum.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
