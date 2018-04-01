# -*- coding:utf-8 -*-

# 定义获取静态资源的路由转换器


from werkzeug.routing import BaseConverter

# 自定义路由转换器类
class RegexConverter(BaseConverter):
    def __init__(self,url_map,*args):
        # 重写init方法,可以写正则匹配规则

        super(RegexConverter, self).__init__(url_map)

        self.regex = args[0]
