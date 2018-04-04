# -*- coding:utf-8 -*-
import re

from ihome.utils.response_code import RET
from . import api
from flask import jsonify,request,current_app,session,g
from ihome import redis_store, db
from ihome.models import User
from ihome.utils.common import login_required



@api.route('/users',methods=['POST'])
def register():
    # 注册视图

    # 1.获取参数,手机号,密码,用户短信验证码,uuid
    # 2.判断参数完整性
    # 3.获取服务器存储的短信验证码,比较两个验证码
    # 4.验证码相同就创建新用户---添加数据,保存数据
    # 5.返回结果



    # 1.获取参数
    json_dict = request.json  #获取前端传递的json数据转换成字典类型数据
    mobile = json_dict.get('mobile') # 获取手机号码
    psw = json_dict.get('password') # 获取密码
    # uuid = json_dict.get('uuid')
    sms_code_client = json_dict.get('sms_code')

    # 2.判断完整性
    if not all([mobile,psw,sms_code_client]):
        jsonify(errno=RET.DATAERR, errmsg=u'数据不完整')


    # 判断手机号码的有效性

    # if User.query.filter(User.mobile == mobile).first():
    #     return jsonify(errno=RET.DATAEXIST, errmsg='用户已经存在')

    user = None
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.debug(e)
    if user:
        return jsonify(errno=RET. USERERR , errmsg=u'该手机号已注册')


    # 3.获取服务器存储的短信验证码   拼接key
    sms_key = 'sms:%s' %mobile
    try:
        sms_code_server = redis_store.get(sms_key)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. NODATA , errmsg=u'找不到验证码')

    if not sms_code_server:
        return jsonify(errno=RET.NODATA, errmsg=u'短信验证码不存在')

    # 4.判断短信验证码是否一致
    if sms_code_server != sms_code_client:
        jsonify(errno=RET.DATAERR  , errmsg=u'短信验证码不正确')

    # 5.验证码相同就创建新用户

    user = User()
    user.name = mobile
    user.mobile = mobile
    # user.password_hash = psw
    user.password = psw  # 这里是设置了一个password属性来接受明文密码  然后在models进行加密

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR , errmsg=u'用户创建失败')


    return jsonify(errno=RET.OK , errmsg=u'用户创建成功')



@api.route('/users_info')
def chek_user():
    mobile = request.args.get('mobile')

    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'数据查询错误')
    if user is None:
        return jsonify(errno=RET.OK, errmsg=u'该手机号有效')
    return jsonify(errno=RET.DATAEXIST , errmsg=u'该手机号已注册')



@api.route('/sessions',methods = ['POST'])
def logint():
    #    """实现用户的登陆接口---设置用户session"""
    # # 1.获取参数--手机号mobile--密码psw
    json_dict = request.json
    mobile = json_dict.get('mobile')
    psw = json_dict.get('password')
    # # 2.参数的判断
    # 判断数据完整
    if not all([psw,mobile]):
        return jsonify(errno=RET.PARAMERR  , errmsg=u'参数不完整')
        # 判断手机号码
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=u'缺少参数')
    # # 3.获取用户信息--验证密码
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DBERR, errmsg=u'获取用户数据失败')
    if not user:
        return jsonify(errno=RET.USERERR , errmsg=u'密码或用户不正确')

    if not user.check_passworf(psw):
        return jsonify(errno=RET.PWDERR  , errmsg=u'密码或用户不正确')

    # # 4.设置session
    try:
        session['user_id'] = user.id
        session[mobile] = user.mobile
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DATAERR , errmsg=u'session登陆状态保存失败')
    # # 5.返回结果

    return jsonify(errno=RET.OK  , errmsg=u'登陆成功')

