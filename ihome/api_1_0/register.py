# -*- coding:utf-8 -*-
# 发送短信验证码
from ihome.utils.response_code import RET
from . import api
from flask import jsonify,request,current_app
from ihome import redis_store

@api.route('/passwords')
def register():
    # 1.获取参数,手机号,密码,用户短信验证码,uuid
    # 2.判断参数完整性
    # 3.获取服务器存储的短信验证码,比较两个验证码
    # 4.验证码相同就创建新用户---添加数据,保存数据
    # 5.返回结果



    # 1.获取参数
    json_dict = request.json  #获取前端传递的json数据转换成字典类型数据
    mobile = json_dict.get('mobile') # 获取手机号码
    psw = json_dict.get('psw') # 获取密码
    uuid = json_dict.get('uuid')
    sms_code_client = json_dict.get('sms_code_client')

    # 2.判断完整性
    if not all([mobile,psw,uuid,sms_code_client]):
        jsonify(errno=RET.DATAERR, errmsg=u'数据不完整')


    # 判断手机号码的有效性



    # if not sever_sms_code != sms_code_client:




    pass

