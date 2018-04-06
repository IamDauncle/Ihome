# -*- coding:utf-8 -*-

# 定义获取静态资源的路由转换器
import functools

from flask import session,jsonify,g
from werkzeug.routing import BaseConverter

# 自定义路由转换器类
from ihome.utils.response_code import RET


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*args):
        # 重写init方法,可以写正则匹配规则

        super(RegexConverter, self).__init__(url_map)

        self.regex = args[0]



# 自定义用户登陆装饰器

def login_required(func,*args,**kwargs):

    @functools.wraps(func)
    def wrapper(*args,**kwargs):

        user_id = session.get('user_id')

        if not user_id:
            return jsonify(errno=RET. SESSIONERR, errmsg=u'用户未登陆')
        else:
            g.user_id = user_id
            return func(*args,**kwargs)

    return wrapper










