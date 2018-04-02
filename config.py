# -*- coding:utf-8 -*-
import logging
import redis


# 进行项目配置
class Config(object):
    DEBUG = True
    # 指定sql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/ihome'
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

    LOGGIONG_LEVEL = logging.DEBUG



# 适应不同环境条件下的项目配置,使用工厂设计

class DevelopmentConfig(Config):
    """创建调试环境下的配置类"""
    # 我们的爱家租房的房型，调试模式的配置和Config一致，所以pass
    LOGGIONG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """创建线上环境下的配置类"""

    # 重写有差异性的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.72.77:3306/iHome'
    DEBUG = False
    LOGGIONG_LEVEL = logging.warn


class UnittestConfig(Config):
    """单元测试的配置"""

    # 重写有差异性的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome_testcast_07'
    LOGGIONG_LEVEL = logging.DEBUG


# 准备工厂设计模式的原材料
configs =  {
    'default_config':Config,
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'unittest':UnittestConfig
}