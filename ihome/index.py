# -*- coding:utf-8 -*-

from flask import Blueprint

# 创建蓝图
aip = Blueprint('aip',__name__)



# 使用蓝图注册路由
@aip.route("/",methods=['POST','GET'])
def index():

    return 'll'
