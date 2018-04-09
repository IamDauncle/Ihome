# -*- coding:utf-8 -*-
from ihome.utils.response_code import RET
from . import api
from ihome.utils.common import login_required
from flask import Flask,jsonify,request,json,current_app,g
from ihome.models import House,Order
import datetime
from ihome import db


# 定义提交订单接口

@api.route('/orders',methods = ['POST'])
@login_required
def set_order():
    '''
    该接口是作为提交订单作用
    获取house_id,为该house_id的房源创建一个order数据

    1判断登陆
    2.获取参数
    3.参数校验 --数据完整性  --房屋是否存在  --参数格式
    4.判断该时间是否存在订单
    5.创建订单
    6.提交数据库
    7.返回响应
    '''

    # 1.获取参数
    json_dict = request.json
    house_id = json_dict.get('house_id')
    start_date_str = json_dict.get('start_date')
    end_date_str = json_dict.get('end_date')

    # 2.校验参数
    # 校验参数完整性
    if not all([house_id,start_date_str,end_date_str]):
        return jsonify(errno=RET. PARAMERR , errmsg=u'参数不完整')
    # 校验参数格式
    try:
        house_id = int(house_id)  # 校验house_id参数格式,并转换成int类型
        # 校验时间格式并将字符串格式转换成事件格式
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        if end_date < start_date:
            return jsonify(errno=RET.PARAMERR , errmsg=u'无效时间段')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. PARAMERR, errmsg=u'参数格式有误')

        # 校验提交订单的房源是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'房屋数据获取失败')

    if not house:
        return jsonify(errno=RET.PARAMERR , errmsg=u'房源不存在')

    # 4.判断订单是否冲突
    try:
        conflict_orders = Order.query.filter(Order.house_id == house_id,Order.end_date>start_date,end_date>Order.begin_date).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR , errmsg=u'数据查询失败')
    if conflict_orders:
        return jsonify(errno=RET.PARAMERR , errmsg=u'该时间已有订单存在')


    # 5.创建订单
    order= Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date-start_date).days
    order.house_price = house.price
    order.amount = house.price * (end_date-start_date).days
    # order.status = 'WAIT_ACCEPT'  #  默认是WAIT_ACCEPT  可以不用写
    house.order_count += 1  # 需要将房屋的销量添加

    # 6.提交数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DBERR, errmsg=u'保存数据失败')

    # 7.返回响应
    return jsonify(errno=RET. OK, errmsg=u'创建订单成功')





















    pass