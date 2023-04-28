

from flask import Flask#从flask包中导入Flask类
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)#将Flask类的实例 赋值给名为 app 的变量。这个实例成为app包的成员。
app.config.from_object(Config)

db = SQLAlchemy(app)#数据库对象
migrate = Migrate(app,db) #迁移


# print(app.config['SECRET_KEY'])

#print('等会谁（哪个包或模块）在使用我：',__name__)

from app import routes,models


