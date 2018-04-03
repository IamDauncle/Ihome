# -*- coding:utf-8 -*-

from ihome.utils.response_code import RET
from . import api
from flask import jsonify,request,current_app
from ihome import redis_store, db
from ihome.models import User

@api.route('/passwords',methods=['POST'])
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

    # 3.获取服务器存储的短信验证码   拼接key
    sms_key = 'sms%s' %mobile
    try:
        sms_code_server = redis_store.get(sms_key)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. NODATA , errmsg=u'找不到验证码')

    if not sms_code_server:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码不存在')

    # 4.判断短信验证码是否一致
    if sms_code_server != sms_code_client:
        jsonify(errno=RET.DATAERR  , errmsg=u'短信验证码不正确')

    # 5.验证码相同就创建新用户

    user = User()
    user.name = mobile
    user.mobile = mobile
    user.password_hash = psw
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR , errmsg=u'用户创建失败')


    return jsonify(errno=RET.OK , errmsg=u'用户创建成功')






