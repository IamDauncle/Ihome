# -*- coding:utf-8 -*-



from . import api
from ihome.models import Area
from flask import request,current_app,jsonify,g,session
from ihome.utils.response_code import RET
from ihome import redis_store,db
from ihome import constants
from ihome.utils.common import login_required
from ihome.models import House,Facility,HouseImage,Order
from ihome.utils.image_storage import upload_image
import datetime





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

 # 如果发布时，有选择设备，就把选择的设备添加到house.facilities 属性保存
    if facilities:
        try:
            house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET. DBERR , errmsg=u'数据查询失败')



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






# 定义上传房屋图片接口
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


    # 将图片存入HouseImage
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = house_image_key

    # 设置首页显示的房源默认图片
    house.index_image_url = house_image_key

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR , errmsg=u'图片数据保存失败')

    # 5.拼接访问图片的url
    house_image_url = constants.QINIU_DOMIN_PREFIX + house_image_key

    return jsonify(errno=RET. OK , errmsg=u'OK',data = {'house_image_url':house_image_url})





# 定义首页推荐房屋
@api.route('/houses/index')
def get_index_house():
    '''
    该接口是给首页显示最新房源
    从数据库查询出时间最新的五组数据，使用order_by()排序，desc（）选择倒序，limit（）获取数据条数
    由于查询获取的数据是query数据对象，需要转成可以传递的json格式，字典或者列表获
    遍历查询得到的数据聚合对象，去除每个对象的数据信息，添加至列表
    接口需要的模型数据都封装在models，需要时调用获取
    '''

    #1. 获取房屋照片最新5张数据
    try:
        houses =House.query.order_by(House.create_time.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.  DBERR, errmsg=u'获取数据失败')
    if not houses:
        return jsonify(errno=RET.NODATA  , errmsg=u'数据不存在')

    # 2.构造数据
    # images_list = []
    # for house in houses:
    #     images_list.append(house.to_basic_dict())


    houses_list = [house.to_basic_dict() for house in houses]
    # 3.返回响应
    return jsonify(errno=RET. OK , errmsg=u'OK',data = {'houses_list':houses_list})




# 定义房源详细信息接口
@api.route('/houses/<int:house_id>')
def get_house_info(house_id):
    '''
    该接口用于显示房源的详细信息 分两部分 house-detail-tmpl  house-image-tmpl
    获取该房屋的信息---to_full_dict()
    构造响应数据----需要传入登陆用户的id用于前端获取判断是否是房屋房主
    放回响应
    '''

    #1.获取参数
    # 2.校验参数---路由转换器已经匹配int了，
    # 3.获取数据
    #4.构造响应json
    # 5.返回响应

   # 3.获取数据
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DBERR , errmsg=u'房源数据获取失败')

    if not house_id:
        return jsonify(errno=RET.NODATA  , errmsg=u'数据不存在')

    # 房源详细信息
    house_data_dict = house.to_full_dict()

    current_app.logger.debug(house_data_dict['img_urls'])
    current_app.logger.debug(house.images)

    # 获取登陆用户的id 判断是否是登陆用户  不是登陆用户返回-1

    login_user_id = session.get('user_id',-1)



    return jsonify(errno=RET. OK , errmsg=u'ok',data = {'house_data_dict':house_data_dict,'login_user_id':login_user_id})







# 定义获取房屋搜索显示接口
# [('sk', u'new'), ('ed', u''), ('sd', u''), ('p', u'1'), ('aid', u'')]
@api.route('/houses/search')
def get_houses_search():
    '''
    该视图是显示房屋搜索结果列表的页面
    需要根据传入的参数进行多层的条件筛选
    如果搜索没有他传入搜索条件,则是显示全部房源列表

    将得到的筛选得到的搜索列表结果进行排序判断
    根据排序要求,就行排序显示

    将排序的结果进行分页展示

    '''

    # 1.获取参数
    sk = request.args.get('sk')  # 排序方式  new ,booking,price-inc,price-des
    aid = request.args.get('aid')  # 城区
    start_date = request.args.get('sd') # 开始时间
    end_date = request.args.get('ed') # 离开时间
    p = request.args.get('p') # 分页页码



    # 2.参数校验
    try:
        p = int(p)
        if start_date:  # 如果有选择开始时间  进行校验
            start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        if end_date:   # 如果有选择结束时间  进行校验
            end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR  , errmsg=u'数据有误')



    try:  # 整个都是对数据的获取过程
    # 3.筛选

        # 创建一个中间变量,来进行筛选结果的存储获取,过度.
        house_query = House.query

        if aid:  # 城区筛选
            house_query = house_query.filter(House.area_id == aid)



        # 获取时间冲突的订单
        conflict_orders = []
        if start_date and end_date:  # 时间筛选
            conflict_orders = Order.query.filter(end_date > Order.begin_date, start_date < Order.end_date).all()
        elif start_date:
            conflict_orders = Order.query.filter(start_date < Order.end_date).all()
        elif end_date:
            conflict_orders = Order.query.filter(end_date > Order.begin_date).all()


        if conflict_orders:
        # 遍历冲突订单,获取冲突订单的houser_id
            in_order_houser = [order.house_id for order in conflict_orders]

            # 筛选出时间冲突的展示列表
            house_query = house_query.filter(House.id.notin_(in_order_houser))

        # 4.经过两步的筛选后,进行排序的判断   new ,booking,price-inc,price-des

        if sk == 'booking':  # 按订单数从多到少排序
            house_query = house_query.order_by(House.orders.desc())
        elif sk == 'price-inc':  # 按价格从低到高排序
            house_query = house_query.order_by(House.price.asc())
        elif sk == 'price-des':  # 按价格从高到底排序
            house_query = house_query.order_by(House.price.desc())
        else:
            house_query = house_query.order_by(House.create_time.desc())


        # 将进行排序的结果进行分页

        paginates = house_query.paginate(p,constants.HOME_PAGE_MAX_HOUSES,False)

        # 获取分页总数
        pages = paginates.page

        # 获取当前分页数据
        houses = paginates.items
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR  , errmsg=u'数据操作失败')

    # 获取房屋数据
    house_detail_list = [house.to_basic_dict() for house in houses]

    # 构造响应数据
    response_data = {
        'pages':pages,
        'house_detail_list':house_detail_list
    }

    return jsonify(errno=RET. OK , errmsg=u'列表获取成功',data = response_data)









