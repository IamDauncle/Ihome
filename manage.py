# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_wtf.csrf import CSRFProtect
from flask_session import Session




# 进行项目配置
class Config(object):
    DEBUG = True
    # 指定sql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.182.129:3306/ihome'
    # 指定数据库操作跟踪模式
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis的ip,端口
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 设置签名
    SECRET_KEY = '9NEV6yqPDkPpCOd03813wYl16DpWynvI+EFZl/ZXGyoRAkBUeDMra0GcSjwgg9Tw'

    # 配置session
    SESSION_TYPE = 'redis' # 配置session的存储方式
    SESSION_REDIS = redis.StrictRedis(host = REDIS_HOST,port = REDIS_PORT) #指定存储session的redis
    SESSION_USE_SIGNER = True  # 开启session签名模式,不以明文显示
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 设置session的过期时间



# 创建app
app = Flask(__name__)
# 创建配置加载
app.config.from_object(Config)
# 创建连接sql的对象
db = SQLAlchemy(app)
# 创建redis的使用对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 创建csrf对象
CSRFProtect(app)
# 创建session对象
Session(app)
# 创建脚本管理器对象
manage = Manager(app)
# 将app与数据库迁移关联
Migrate(app,db)
# 添加迁移数据库脚本
manage.add_command('db',MigrateCommand)








@app.route("/",methods=['POST','GET'])
def index():
    return 'll'



if __name__ == '__main__':
    # manage.run()
    app.run(debug=True)