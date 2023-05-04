from urllib import request

from flask import render_template, flash, redirect, url_for,request
from flask_wtf import form
from werkzeug.urls import url_parse

from app import app, db  # 从app包中导入 app这个实例

from app.forms import LoginForm, RegistrationForm

from flask_login import current_user, login_user, login_required,UserMixin
from app.models import User,Post

from flask_login import logout_user #退出登录
#主页路由
@app.route('/')
@app.route('/index')
@login_required  #装饰器，一开始直接进入登陆页面
#1个视图函数
def index():
	user = {'username':'scott'}
	#模拟的评论数据
	posts = [
		{
			'author':{'username':'John'},
			'body':'Beautiful day Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'Beautiful day so cool'
		}
	]
	return render_template('index.html',user = user,posts = posts)



#登录路由
@app.route('/loginqqq',methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	login_form = LoginForm()
	if login_form.validate_on_submit():
		user = User.query.filter_by(username = login_form.username.data).first()
		if user is None or not user.check_password(login_form.password.data):
			flash('Invalid username or password')
		login_user(user,remember = login_form.remember_me.data)

		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '': #阻止从本网页跳转到别的网页
			next_page = url_for('index')
		return redirect(next_page)

		# return redirect(next_pages)
	return render_template('login.html',title = 'login',form = login_form)

#用户退出
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


#注册
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:  #如果已经登陆了
		return redirect(url_for('index'))
	form = RegistrationForm() #创建注册表单
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data) #如果提交成功了，就创建一个用户对象
		user.set_password(form.password.data)
		db.session.add(user) #加进数据库
		db.session.commit() #加进数据库
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)






