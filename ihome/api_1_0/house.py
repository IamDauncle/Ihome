# -*- coding:utf-8 -*-



from . import api
from ihome.models import Area
from flask import request,current_app,jsonify
from ihome.utils.response_code import RET
from ihome import redis_store
from ihome import constants





# 定义城区显示接口
@api.route('/areas')
def get_areas():

    # 将城区显示存储为redis缓存
    try:
        areas_list = redis_store.get('Areas')
        if areas_list:
            return jsonify(errno=RET.OK, errmsg=u'城区数据查询成功', data={'areas_list': areas_list})
    except Exception as e:
        current_app.logger.error(e)


    # 1.查找出所以城区信息
    try:  # 获取所有相关的城区数据对象
        areas = Area.query.all() # 这是 一个模型对象集合列表
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR  , errmsg=u'城区数据查询失败')

    # 2.封装响应数据
    areas_list = []    # 这个列表就是作为响应数据的装有城区数据对象的列表数据
    for area in areas:   #在所有城区数据信息对象遍历出每个城区的数据对象，再调用封装好的显示信息函数
        areas_list.append(area.to_dict())

    try:  # 将数据缓存在redis
        redis_store.set('Areas',areas_list,constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)


    # 3.响应
    return jsonify(errno=RET. OK , errmsg=u'城区数据查询成功',data = {'areas_list':areas_list})
