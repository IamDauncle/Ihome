# -*- coding:utf-8 -*-


from flask import Blueprint

# 创建蓝图
# 配合RESTful设计方式,需要在url加入api,又使用版本控制模块  需要加前缀 /api/1.0  url_prefix指定url前缀
aip = Blueprint('aip',__name__,url_prefix='/api/1.0')

from ihome.api_1_0 import index
