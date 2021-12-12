import pandas as pd
from flask import Flask, render_template, redirect, url_for, session, flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import DateTimeField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import email_validator

app = Flask(__name__)


bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'c1155c6a351e49eba15c00ce577b259e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment.db'
db = SQLAlchemy(app)

login_manager = LoginManager()#实例化登录管理对象
login_manager.init_app(app)#初始化应用
login_manager.login_view = "login"#设置用户登录视图函数（验证失败时要跳转的画面）   
################################################################################################################

@login_manager.user_loader#加载用户时需要做的事情
def load_user(user_id):
    return User.query.get(int(user_id))#从数据库中得到用户数据返回一个用户实例


class User(db.Model, UserMixin):#用户类（没有表名所以不是表？）
    #没有 __tablename__所以表名跟类名相同？
    id = db.Column(db.Integer, primary_key=True)#主键
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    notes = db.relationship('Note', backref='writer', lazy='dynamic')#设置映射关系
    
    #不用定义那一堆函数？


class Note(db.Model):#笔记类
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    note_body = db.Column(db.Text)
    note_writer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exp_date = db.Column(db.String)


class RegisterForm(FlaskForm):#注册表单类
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)], render_kw={"placeholder": "example@gmail.com"})
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "********"})
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        print(username.data,'validate username')
        existing_user_username = User.query.filter_by(username=username.data).first()
        print('1111',existing_user_username)
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

    def validate_email(self, email):
        print(email.data,'validate email')
        existing_user_email = User.query.filter_by(email=email.data).first()
        print('2222',existing_user_email)
        if existing_user_email:
            raise ValidationError("That email address belongs to different user. Please choose a different one.")



class LoginForm(FlaskForm):#登录表单类
    username = StringField("用户名Username", validators=[InputRequired(), Length(max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("密码Password", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder":  "Password"})
    submit = SubmitField("Login")

class NewNoteForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=25)], render_kw={"placeholder": "Title"})
    note_body = TextAreaField("Note Body", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder":  "Note Body"})
    exp_date = StringField("Expected Completion Date", validators=[InputRequired(), Length(max=8)], render_kw={"placeholder":  "DD/MM/YY"})
    submit = SubmitField("Add Note")

################################################################################################################

@app.route("/")
def index():
    print(current_user)
    user = User.query.filter_by(id = current_user.get_id()).first()
    print(user)
    if not user:
        print('not user')
        return render_template('index.html',user_login = False)
    else:
        print('have user')
        user_name = User.query.filter_by(id = current_user.get_id()).first()
        user_name = user_name.username
        print(user_name)
        return render_template('index.html',user_login = True,username=user_name)
        

@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/movies")
def movies():
    df = pd.read_csv("base_info.csv",delimiter="\t")
    list = df.to_dict('records')
    return render_template('movies.html', entries = list)

@app.route('/login', methods=['GET','POST'])
def login():#用户登录视图
    form = LoginForm()#前文定义的登录表单
    if form.validate_on_submit():#如果用户完整提交login表单
        #首先先试着从数据库中中找找有没有这个用户
        #第一个username是User类里的属性；.first()返回找到的第一行
        #这个User是直接链接了数据库的user表？
        user = User.query.filter_by(username=form.username.data).first()
        print('!!!!!!!!!!submit!!!!!!!!!!!!')
        if user:#如果用户存在
            #而且密文密码验证通过
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)#则调用flask_login库里的login_user函数加载用户，并创建用户session
                #此时页面重定向到view_notes（）视图页面
                print('!!!!!!!!right!!!!!!!!!!!!!')
                return redirect(url_for("view_notes"))
            flash("Wrong Password, please try again.")
    
        flash("User does not exist, or invalid username or password.")
    #没有提交榜单就正常显示页面
    return render_template('login.html', title="Login", form=form)


@app.route('/register', methods=['GET','POST'])
def register():#用户注册视图
    print('I am here')
    form = RegisterForm()#前文定义的注册表单
    print('Creat RegisterForm')
    if form.validate_on_submit():#如果用户完整提交表单
    #if request.method == "POST":#上面那个不知道为什么老是无法判定完成所以换这个，但这个有隐患
        print('!!!!!!!!!!!!!successfully submit!!!!!!!!!!!!!!!')
        hashed_password = bcrypt.generate_password_hash(form.password.data)#加密密码
        #实例化一个新用户
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,admin=0)
        db.session.add(new_user)#将新用户写入数据库
        db.session.commit()
        print('successfully commit!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout', methods=["GET","POST"])
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))

@app.route('/new-note', methods=['GET','POST'])
@login_required#保护route
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
    #if request.method == "POST":#!!!!!注意这里换了
        new_note = Note(title=form.title.data, note_body=form.note_body.data, writer=current_user,exp_date=form.exp_date.data)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('view_notes'))
    return render_template('new_note.html', title='New Note', form=form)

@app.route('/my-notes', methods=['GET','POST'])
@login_required
def view_notes():
    #print(current_user.get_id())
    user = User.query.filter_by(id = current_user.get_id()).first()
    if user.admin:#判断用户是否为admin
        notes = Note.query.all()
        return render_template('my_notes.html', notes=notes, title='All Tasks',admin = user.admin)
    else:
        notes = Note.query.filter_by(writer=current_user).all()#这里的writer是flaskform的属性
        return render_template('my_notes.html', notes=notes, title='My Tasks')

@app.route('/upload-note/<int:note_id>', methods=['GET',"POST"])
@login_required
def upload_note(note_id):#更新任务内容
    note = Note.query.get_or_404(note_id)#获取原数据
    form = NewNoteForm()
    if form.validate_on_submit():
    #if request.method == "POST":#!!!!!注意这里换了
        note.title=form.title.data
        note.note_body=form.note_body.data
        note.writer=current_user
        note.exp_date=form.exp_date.data

        db.session.commit()
        return redirect(url_for('view_notes'))
    else:
        form.title.data=note.title
        form.note_body.data=note.note_body
        form.exp_date.data=note.exp_date

        return render_template('new_note.html', title='Upload Task', form=form)

@app.route('/delete-note/<int:note_id>', methods=['GET',"POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('view_notes'))

@app.route('/discussion', methods=['GET','POST'])
def discussion():

    notes = Note.query.all()
    return render_template('discussion.html', notes=notes, title='Discussion')



if __name__ == '__main__':
    app.run(debug=True)