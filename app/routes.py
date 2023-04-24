from flask import render_template

from app import app#从app包中导入 app这个实例

#2个路由
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



