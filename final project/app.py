from operator import ge
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
from datetime import timedelta 
import re
from sqlalchemy import distinct 


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

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

class douban(db.Model):
    __tablename__ = 'douban'
    title_Chinese = db.Column(db.Text,primary_key=True)
    title_English = db.Column(db.Text,db.ForeignKey('IMDB.title'))
    rate = db.Column(db.Text)
    director = db.Column(db.Text)
    country = db.Column(db.Text)
    year = db.Column(db.Text)
    genre = db.Column(db.Text)

class IMDB(db.Model):
    __tablename__ = 'IMDB'
    title = db.Column(db.Text, db.ForeignKey('douban.title_English'))
    n_title = db.Column(db.Text)
    id = db.Column(db.Text,primary_key=True)
    image = db.Column(db.Text)

class rate(db.Model):
    __tablename__ = 'rate'
    r_title = db.Column(db.Text)
    #r_id = db.Column(db.Text,db.ForeignKey('IMDB.id'))
    r_id = db.Column(db.Text,primary_key=True)
    imdb =  db.Column(db.Integer)
    MTC = db.Column(db.Integer)
    rottenTomatoes = db.Column(db.Integer)

class details(db.Model):
    __tablename__ = 'details'
    i_title = db.Column(db.Text)
    #r_id = db.Column(db.Text,db.ForeignKey('IMDB.id'))
    i_id = db.Column(db.Text,primary_key=True)
    plot =  db.Column(db.Text)
    images = db.Column(db.Text)
 

class User(db.Model, UserMixin):#用户类（没有表名所以不是表？）
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)#主键
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    comments = db.relationship('Comment', backref='writer', lazy='dynamic')#设置映射关系
    
    #不用定义那一堆函数？


class Comment(db.Model):#评论类
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    comment_body = db.Column(db.Text)
    comment_writer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exp_date = db.Column(db.String)
    tomovie = db.Column(db.String)

class Missing(db.Model):#未收录电影
    __tablename__ = 'missing'
    title = db.Column(db.String, primary_key=True)


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
    email = StringField("邮箱Email", validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)], render_kw={"placeholder": "example@gmail.com"})
    password = PasswordField("密码Password", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder":  "Password"})
    submit = SubmitField("Login")

class NewCommentForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=25)], render_kw={"placeholder": "Title"})
    comment_body = TextAreaField("Comment Body", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder":  "Comment Body"})
    #exp_date = StringField("Expected Completion Date", validators=[InputRequired(), Length(max=8)], render_kw={"placeholder":  "DD/MM/YY"})
    submit = SubmitField("Submit")

'''
class SearchForm(FlaskForm):
    search_content=StringField("Search Content",render_kw={"placeholder": "电影名称"})
    submit = SubmitField("Submit")
'''
################################################################################################################

def check_user(current_user):
    user = User.query.filter_by(id = current_user.get_id()).first()
    if user:
        return True
    else:
        return False
################################################################################################################

df = pd.read_csv("upcomingMovies.csv")#,delimiter="\t"
mdic = df.to_dict('records')
#print(mdic)

@app.route("/", methods=['GET','POST'] )
def index():
    print(current_user)
    user = User.query.filter_by(id = current_user.get_id()).first()
    print(user)

    if request.method == "POST":
        print(request.form["searchInput"])
        return redirect(url_for('searchList',movie=request.form["searchInput"]))

    
    if not user:
        print('not user')
        return render_template('index.html',user_login = False,entries = mdic)
    else:
        print('have user')
        user_name = User.query.filter_by(id = current_user.get_id()).first()
        user_name = user_name.username
        print(user_name)
        return render_template('index.html',user_login = True,username=user_name,entries = mdic)



@app.route("/innerList/<string:type>")
def innerList(type):
    movie= db.session.query(douban.title_Chinese,IMDB.n_title,douban.director,douban.country,douban.year,douban.genre,douban.rate,rate.imdb,rate.rottenTomatoes,IMDB.image)\
    .join(IMDB,douban.title_English==IMDB.title)\
    .join(rate,IMDB.id==rate.r_id)\
    .filter(douban.genre==type)

    df2 = pd.DataFrame(movie, columns=['title','n_title','director','district','year','genre','douban_rate','imdb_rate','rT_rate','image'])
    #print(df2)
    mlist= df2.to_dict('records')

    return render_template('innerList.html',entries = mlist)

genre=['太空歌剧','太空冒险','社会科幻','机器人','赛博格','时空旅行','超人类','未来恐惧']
year=['2020s','2010s','2000s','1990s','1980s','1970s','1960s','其他']

@app.route("/movies/<first>/<second>")
def movies(first,second):
    if first == 'genre':
        tags = genre
        movie= db.session.query(douban.title_Chinese,IMDB.n_title,douban.director,douban.country,douban.year,douban.genre,douban.rate,rate.imdb,rate.rottenTomatoes,IMDB.image)\
        .join(IMDB,douban.title_English==IMDB.title)\
        .join(rate,IMDB.id==rate.r_id)\
        .filter(douban.genre==second).order_by(-douban.year)

        df2 = pd.DataFrame(movie, columns=['title','n_title','director','district','year','genre','douban_rate','imdb_rate','rT_rate','image'])
        #print(df2)
        mlist= df2.to_dict('records')
    else:
        tags = year
        y = second.rstrip('s')
        movie= db.session.query(douban.title_Chinese,IMDB.n_title,douban.director,douban.country,douban.year,douban.genre,douban.rate,rate.imdb,rate.rottenTomatoes,IMDB.image)\
            .join(IMDB,douban.title_English==IMDB.title)\
            .join(rate,IMDB.id==rate.r_id)\
            .filter(douban.year >=y).filter(douban.year <=str(int(y)+10)).order_by(douban.year)

        df2 = pd.DataFrame(movie, columns=['title','n_title','director','district','year','genre','douban_rate','imdb_rate','rT_rate','image'])
        #print(df2)
        mlist= df2.to_dict('records')
    return render_template('movieList.html',entries = mlist,user_login=check_user(current_user),tags=tags,type=first,title=second)

@app.route("/searchList/<movie>")
def searchList(movie):
    got_movie= db.session.query(douban.title_Chinese,IMDB.n_title,douban.director,douban.country,douban.year,douban.genre,douban.rate,rate.imdb,rate.rottenTomatoes,IMDB.image)\
    .join(IMDB,douban.title_English==IMDB.title)\
    .join(rate,IMDB.id==rate.r_id)\
    .filter(douban.title_Chinese.like("%"+movie+"%"))

    df2 = pd.DataFrame(got_movie, columns=['title','n_title','director','district','year','genre','douban_rate','imdb_rate','rT_rate','image'])
    mlist= df2.to_dict('records')
    print(mlist)
    if not mlist:
        new_missing = Missing(title=movie)
        db.session.merge(new_missing)
        db.session.commit()
    return render_template('searchList.html',entries = mlist,user_login=check_user(current_user))
    #return render_template('searchList.html',user_login=check_user(current_user))

@app.route("/movieInfo/<movie>",methods=['GET','POST'])
def movieInfo(movie):
    #print(movie)
    got_movie= db.session.query(douban.title_Chinese,IMDB.n_title,douban.director,douban.country,douban.year,douban.genre,douban.rate,rate.imdb,rate.rottenTomatoes,IMDB.image,details.plot,details.images)\
    .join(IMDB,douban.title_English==IMDB.title)\
    .join(rate,IMDB.id==rate.r_id)\
    .join(details,IMDB.id==details.i_id)\
    .filter(douban.title_Chinese.like("%"+movie+"%"))
    #.filter(douban.title_Chinese==movie)

    df2 = pd.DataFrame(got_movie, columns=['title','n_title','director','district','year','genre','douban_rate','imdb_rate','rT_rate','image','plot','images'])
    #print(df2)
    mInfo= df2.to_dict('records')

    mInfo[0]['images']=re.findall(r"'(.*?)'", mInfo[0]['images'])

    #got_comment=Comment.query.filter_by(tomovie=movie).all()
    got_comment = db.session.query(Comment.title,Comment.comment_body,User.username).join(User, Comment.comment_writer==User.id).filter(Comment.tomovie==movie)

    #print(got_comment)


    form = NewCommentForm()

    #影评输入
    #if form.validate_on_submit():
    if request.method == "POST":#!!!!!注意这里换了    
        print(form.title.data,form.comment_body.data,current_user,movie)
        new_comment = Comment(title=form.title.data, comment_body=form.comment_body.data, writer=current_user,tomovie=movie)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('movieInfo', movie= movie))
    else:
        return render_template('movieInfo.html',entries = mInfo,form=form,comments = got_comment,user_login=check_user(current_user))

@app.route('/login', methods=['GET','POST'])
def login():#用户登录视图
    form = LoginForm()#前文定义的登录表单
    #if form.validate_on_submit():#如果用户完整提交login表单
    if request.method == "POST":#上面那个不知道为什么老是无法判定完成所以换这个，但这个有隐患
      print('get submit')
      #首先先试着从数据库中中找找有没有这个用户
      #第一个username是User类里的属性；.first()返回找到的第一行
      #这个User是直接链接了数据库的user表？
      user = User.query.filter_by(email=form.email.data).first()
      print('!!!!!!!!!!submit!!!!!!!!!!!!')
      print('1111111',user)
      if user:#如果用户存在
          #而且密文密码验证通过
          print("user exist")
          if bcrypt.check_password_hash(user.password, form.password.data):
              print(user)
              login_user(user)#则调用flask_login库里的login_user函数加载用户，并创建用户session
              #此时页面重定向到view_notes（）视图页面
              print('!!!!!!!!right!!!!!!!!!!!!!')
              return redirect(url_for("index"))
          flash("Wrong Password, please try again.")
  
      flash("User does not exist, or invalid username or password.")
    #没有提交榜单就正常显示页面
    return render_template('login.html', title="Login", form=form)


@app.route('/register', methods=['GET','POST'])
def register():#用户注册视图
    print('I am here')
    form = RegisterForm()#前文定义的注册表单
    print('Creat RegisterForm')
    #if form.validate_on_submit():#如果用户完整提交表单
    if request.method == "POST":#上面那个不知道为什么老是无法判定完成所以换这个，但这个有隐患
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


@app.route('/pricing', methods=['GET','POST'])
def pricing():

    return render_template('pricing.html')



if __name__ == '__main__':
    app.run(debug=True)