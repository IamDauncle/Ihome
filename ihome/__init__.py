# -*- coding:utf-8 -*-


import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import configs

from ihome.utils.common import RegexConverter
import logging
from logging.handlers import RotatingFileHandler



db = SQLAlchemy() # 先创建一个db对象,供调用,再在创建app的工厂函数内部绑定app
redis_store = None





def setuploggin(loggin_leve):
#-- ----固定添加日志------
    # 设置日志的记录等级
    logging.basicConfig(level=loggin_leve)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)





def get_app(config_type):

    # 创建app
    app = Flask(__name__)

    setuploggin(configs[config_type].LOGGIONG_LEVEL)

    # 创建配置加载
    app.config.from_object(configs[config_type])
    # 创建连接sql的对象
    # db = SQLAlchemy(app)
    db.init_app(app) # db对象进行app绑定
    # 创建redis的使用对象
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_type].REDIS_HOST,port=configs[config_type].REDIS_PORT)
    # 创建csrf对象
    # CSRFProtect(app)
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