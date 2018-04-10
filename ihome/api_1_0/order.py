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
    该接口是作为提交订单作用   创建订单
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


    # 6.提交数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR, errmsg=u'保存数据失败')

    # 7.返回响应
    return jsonify(errno=RET. OK, errmsg=u'创建订单成功')






@api.route('/orders')
@login_required
def get_order():
    '''
    该接口是用于显示订单的.--客户订单,我的订单
    /api/1.0/orders?role=   client  landlord

    1.判断登陆
    2.获取参数
    3.校验参数
    4.根据用户身份查询订单
    5.构造响应数据
    6.返回响应
    '''

    # 获取参数
    role = request.args.get('role')
    # 参数校验
    if not role:
        return jsonify(errno=RET. PARAMERR, errmsg=u'数据不能为空')
    if not role in ['client','landlord']:
        return jsonify(errno=RET. PARAMERR, errmsg=u'参数有误')

    if role == 'client':   # 租客的订单
        try:
            orders = Order.query.order_by(Order.create_time.desc()).filter(Order.user_id == g.user_id).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR , errmsg=u'订单数据查询错误')

    else:   # 我出租的订单   获取订单中,order的house_id是我的房源的id的订单
        try:
            houses = House.query.filter(House.user_id == g.user_id).all()
            houses_id = [house.id for house in houses]
            orders = Order.query.order_by(Order.create_time.desc()).filter(Order.house_id.in_(houses_id)).all()

        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET. DBERR, errmsg=u'订单数据查询失败')

    # if not orders:  # 如果没有订单 下面的遍历就不会遍历,是[].
    #     return jsonify(errno=RET. NODATA, errmsg=u'赞无订单')


    # 构造响应数据

    orders_dict_list = [order.to_dict() for order in orders]

    return jsonify(errno=RET. OK, errmsg=u'OK',data = orders_dict_list)




@api.route('/orders/<int:order_id>',methods = ['PUT'])
@login_required
def set_order_status(order_id):
    '''
    /api/1.0/orders/3?action=accept
    该接口用于操作接单和拒接----修改order_status
    /order/order_id?action = ---accept    ---reject

    1判断登陆
    2.获取参数  --action  --order_Id   --reason
    3.参数校验   --accept    ---reject
    4.根据action 进行修改order_status
    5.如果是reject  需要添加拒接理由到评论字段
    6.提交数据库
    7.返回响应
    '''

    # 获取参数
    action = request.args.get('action')

    if not action in ['accept','reject']:
        return jsonify(errno=RET.PARAMERR , errmsg=u'缺少参数')



    try:
        order = Order.query.filter(Order.id == order_id,Order.status == 'WAIT_ACCEPT').first()
        # order = Order.query.filter(Order.id == order_id, Order.status == 'WAIT_ACCEPT',Order.house.user_id ==g.user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR , errmsg=u'订单查询失败')
    if not order:
        return jsonify(errno=RET.NODATA , errmsg=u'订单不存在')

    # 判断登陆用户是否为房主
    login_user_id = g.user_id
    house_user_id = order.house.user_id
    if login_user_id != house_user_id:
        return jsonify(errno=RET.USERERR, errmsg=u'非房主不可接单')

    if action == 'accept':  # 接单
        # 查询到订单,如果是接单..修改status订单的为待评价
        order.status = 'WAIT_COMMENT'
        # 接单后,将房源的销量加1
        order.house.order_count += 1
    else:
        # 获取拒单理由
        reason = request.json.get('reason')
        order.status = 'REJECTED'
        order.comment = reason

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR , errmsg=u'订单状态修改失败')

    return jsonify(errno=RET.OK , errmsg=u'OK')






@api.route('/orders/<order_id>/comment',methods = ['POST'])
@login_required
def set_comment(order_id):
    """
    客户评论接口



    """

    # 获取参数
    comment = request.json.get('comment')

    if not comment:
        return jsonify(errno=RET.PARAMERR , errmsg=u'评论不能为空')


    try:
        order = Order.query.filter(Order.id == order_id,Order.status == 'WAIT_COMMENT',Order.user_id == g.user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR , errmsg=u'查询数据失败')

    if not order:
        return jsonify(errno=RET. NODATA, errmsg=u'订单不存在')


    order.comment = comment
    order.status = 'COMPLETE'


    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR, errmsg=u'添加评论失败')


    return jsonify(errno=RET. OK, errmsg=u'OK')










