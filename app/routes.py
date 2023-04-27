from flask import render_template, flash, redirect, url_for

from app import app#从app包中导入 app这个实例

from app.forms import LoginForm

#主页路由
@app.route('/')
@app.route('/index')
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
	login_form = LoginForm()
	if login_form.validate_on_submit():
		flash('login requested for user{},remember_me{}'.format(login_form.username.data,login_form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html',title = 'login',form = login_form)






