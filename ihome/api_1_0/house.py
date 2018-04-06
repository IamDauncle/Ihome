# -*- coding:utf-8 -*-



from . import api
from ihome.models import Area
from flask import request,current_app,jsonify
from ihome.utils.response_code import RET





# 定义城区显示接口
@api.route('/areas')
def get_areas():

    # 1.查找出所以城区信息
    try:
        areas = Area.query.all() # 这是 一个模型对象集合列表
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR  , errmsg=u'城区数据查询失败')

    # 2.封装响应数据
    areas_list = []
    for area in areas:
        areas_list.append(area)

    # 3.响应
    return jsonify(errno=RET. OK , errmsg=u'城区数据查询成功',data = {'areas_list':areas_list})
