# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config





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