#所有模型文件，数据库对应的类
from datetime import datetime

from app import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),index = True,unique = True)
    email = db.Column(db.String(120),index = True,unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref = 'author',lazy = 'dynamic')  #反向引用backref，可以从文章找回用户 #lazy = 'dynamic'

    def __repr__(self):
        return'<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index = True,default = datetime.utcnow) #电脑默认时间default = datetime.utcnow
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return'<Post {}>'.format(self.body)
