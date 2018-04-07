# -*- coding:utf-8 -*-



from . import api
from ihome.models import Area
from flask import request,current_app,jsonify,g
from ihome.utils.response_code import RET
from ihome import redis_store,db
from ihome import constants
from ihome.utils.common import login_required
from ihome.models import House,Facility
from ihome.utils.image_storage import upload_image





# 定义城区显示接口
@api.route('/areas')
def get_areas():

    # 将城区显示存储为redis缓存
    try:
        areas_list = redis_store.get('Areas')
        if areas_list:
            return jsonify(errno=RET.OK, errmsg=u'城区数据查询成功', data=eval({'areas_list': areas_list}))
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



# 房屋发布接口
@api.route('/houses',methods=['POST'])
@login_required
def pub_house():
    # 1.判断登陆状态
    # 2.获取参数 --13个
    # 3.对数据进行校验  --完整性校验 --价钱有效性校验
    # 4.保存数据对象属性
    # 5.提交数据操作
    # 6.响应


# 2.获取参数 --13个
    json_dict = request.json

    title = json_dict.get('title') # 标题
    price = json_dict.get('price') # 价钱--分
    address = json_dict.get('address')
    area_id = json_dict.get('area_id')
    room_count = json_dict.get('room_count')
    acreage = json_dict.get('acreage') # 房屋面积
    unit = json_dict.get('unit')
    capacity = json_dict.get('capacity')
    beds = json_dict.get('beds')
    deposit = json_dict.get('deposit') # 房屋押金
    min_days = json_dict.get('min_days')
    max_days = json_dict.get('max_days')
    # 配置物品有可能都不配，所以不放在all（）里面判断
    facilities = json_dict.get('facility')  # 配置的物品复选框列表类型传入 【2,4,6】

    # ---数据完整性判断---
    if not all([title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET. PARAMERR , errmsg=u'信息填写不完整')

    # ---1.对于价钱这类存在浮点数，或者数字的数据，需要进行校验数据有效性校验，防止传入字符等---
    # ---2.对于浮点数的数据存储，需要将浮点数转化为整数进行存储。如价钱，使用价钱×100.以分为单位，进行整数存储---
    # ---3.浮点数存在精度问题，所以输出存数不使用浮点数存储---

    try: # 先试转成浮点数，可以转说明不是字符串
        price = int(float(price)*100)
        acreage = int(float(acreage)*100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. PARAMERR , errmsg=u'数据格式不正确')
# 4.保存数据对象属性
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
 # 查询出被选中的设施模型对象
    house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()

    # 4.保存到数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='发布新房源失败')

    # 5.响应结果                              传入house_id 是为了埋在html，给别的接口获取数据
    return jsonify(errno=RET.OK, errmsg='发布新房源成功', data={'house_id':house.id})







@api.route('/houses/image',methods = ['POST'])
@login_required
def set_house_image():
    # 1.判断登陆
    # 2.获取上传图片数据,房屋id
    # 3.调用七牛云
    # 4.存储返回的存储照片的key
    # 5.拼接访问图片的url
    # 6.返回响应


    # 2.获取上传图片数据

    try:
        house_image = request.files.get('house_image')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR  , errmsg=u'获取图片失败')

    house_id = request.form.get('house_id')
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少必传参数')

    # 3.调用七牛云
    house_image_key = upload_image(house_image)

    # 4.存储返回的存储照片的key
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR  , errmsg=u'获取房屋数据失败')

    if not house:
        return jsonify(errno=RET. NODATA , errmsg=u'房屋信息不存在')

    house.index_image_url = house_image_key

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR , errmsg=u'图片数据保存失败')

    # 5.拼接访问图片的url
    house_image_url = constants.QINIU_DOMIN_PREFIX + house_image_key

    return jsonify(errno=RET. OK , errmsg=u'OK',data = {'house_image_url':house_image_url})













