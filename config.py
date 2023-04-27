import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')or'you will never guss'   #os环境变量 加密字符串

