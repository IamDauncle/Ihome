# -*- coding:utf-8 -*-

from ihome.api_1_0 import api


# 使用蓝图注册路由
@api.route("/",methods=['POST','GET'])
def index():

    return 'll'
