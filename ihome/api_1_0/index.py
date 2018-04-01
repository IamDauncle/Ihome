# -*- coding:utf-8 -*-

from ihome.api_1_0 import aip


# 使用蓝图注册路由
@aip.route("/",methods=['POST','GET'])
def index():

    return 'll'
