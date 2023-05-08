#所有模型文件，数据库对应的类
from datetime import datetime
from hashlib import md5

import self as self
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#关注模型，建立多对多的关系，建立一个表格，里面两个外键
followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')), #user的外键，关注你的
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))  #user的外键，你关注的
)





#用户模型
class User(UserMixin,db.Model): #UserMixin继承UserMixin里面的四个属性
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),index = True,unique = True)
    email = db.Column(db.String(120),index = True,unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref = 'author',lazy = 'dynamic')  #反向引用backref，可以从文章找回用户 #lazy = 'dynamic'
    about_me = db.Column(db.String(140)) #关于我
    last_seen = db.Column(db.DateTime, default=datetime.utcnow) #上次登录时间
    #关注模型
    followed = db.relationship(      #自链接
        'User',
        secondary = followers,  #关系表
        primaryjoin = (followers.c.follower_id == id),  #左边是follower_id
        secondaryjoin = (followers.c.followed_id == id),#右边是followed_id
        backref = db.backref('followers',lazy = 'dynamic'),#反向引用
        lazy = 'dynamic'




    )
    #关注模型
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    #帖子模型
    # join()多表连接，#filter过滤，order_by排序; 11节46:30
    # def followed_posts(self):
    #     return Post.qurry.join(
    #         followers,
    #         (followers.c.followed_id == Post.user_id)
    #     ).filter(
    #         followers.c.follower_id == self.id
    #     ).order_by(
    #         Post.timestamp.desc() #按时间降序排列
    #     )

    def followed_posts(self):
        followed = Post.qurry.join(
            followers,
            (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())




    # 头像
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    #密码
    def set_password(self,password):
        self.password_hash = generate_password_hash(password) #生成一个哈希加密

    def check_password(self,password):
        return check_password_hash(self.password_hash,password) #检查密码，返回True说明对

    def __repr__(self):
        return '<User {}>'.format(self.username)



#推文模型
class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index = True,default = datetime.utcnow) #电脑默认时间default = datetime.utcnow
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


    def __repr__(self):
        return'<Post {}>'.format(self.body)




