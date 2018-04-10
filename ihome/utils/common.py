# -*- coding:utf-8 -*-

# 定义获取静态资源的路由转换器
import functools

from flask import session,jsonify,g
from werkzeug.routing import BaseConverter
from functools import wraps

# 自定义路由转换器类
from ihome.utils.response_code import RET


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*args):
        # 重写init方法,可以写正则匹配规则

        super(RegexConverter, self).__init__(url_map)

        self.regex = args[0]



# 自定义用户登陆装饰器
def login_required(func):
    # 自定义装饰器必须必须要用@wraps()来装饰函数,
    # 这样是为了消除自定义装饰器对被装饰的函数 __name__属性的修改
    @wraps(func)
    def wrapper(*args,**kwargs):   # 登陆判断的实现的逻辑部分
        user_id = session.get('user_id') # 在session中获取user_id
        if not user_id:  # 获取不到就没登陆
            return jsonify(errno=RET. SESSIONERR, errmsg=u'用户未登陆')
        else: # 如果登陆,使用g变量保存user_id,可以在应用中使用
            g.user_id = user_id
            return func(*args,**kwargs)
    return wrapper












