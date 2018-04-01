# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import configs
from ihome.index import aip

db = SQLAlchemy() # 先创建一个db对象,供调用,再在创建app的工厂函数内部绑定app
redis_store = None

def get_app(config_type):

    # 创建app
    app = Flask(__name__)
    # 创建配置加载
    app.config.from_object(configs[config_type])
    # 创建连接sql的对象
    # db = SQLAlchemy(app)
    db.init_app(app) # db对象进行app绑定
    # 创建redis的使用对象
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_type].REDIS_HOST,port=configs[config_type].REDIS_PORT)
    # 创建csrf对象
    CSRFProtect(app)
    # 创建session对象
    Session(app)

    # 在app注册蓝图
    app.register_blueprint(aip)
    return app