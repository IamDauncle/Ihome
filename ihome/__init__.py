# -*- coding:utf-8 -*-

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import configs


from ihome.utils.common import RegexConverter

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
    # 注册自定义路由转换器,添加至框架的路由转换器字典集
    # 're'为转换器使用的名称    converters={ 're':RegexConverter}
    app.url_map.converters['re'] = RegexConverter

    # 在app注册蓝图   蓝图注册需要放在后面
    from ihome.api_1_0 import api  # 为了能让redis_stoer在顶部导入,蓝图导入需要这样写
    app.register_blueprint(api)
    # 注册 静态文件蓝图
    from web_html import static_blue
    app.register_blueprint(static_blue)



    return app