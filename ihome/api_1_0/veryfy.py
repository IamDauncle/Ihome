# -*- coding:utf-8 -*-
import re

from ihome import constants
from . import api
from flask import request,current_app,jsonify,make_response
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store,constants
from ihome.utils.response_code import RET
import random
from ihome.utils.SMS import CCP


@api.route('/image_code')
def get_image_code():
    # 获取图片验证码  get请求

    # 1.获取uuid作为存储验证码的key  "image:uuid" : image_code
    uuid = request.args.get('uuid')
    last_uuid = request.args.get('last_uuid')
    if not uuid:
        return jsonify(errno=RET.PARAMERR, errmsg=u'缺少参数')

    # 2.生成图片验证码
    name,text,image = captcha.generate_captcha()

    # 3.redis存储图片验证码
    # 拼接redis存储的key

    redis_key = 'image:%s' %uuid
    try:
        if last_uuid: # 如果存在上一个的uuid
            redis_store.delete(last_uuid)  # 删除多余的uuid
                        # key      lavue     过期时间
        redis_store.set(redis_key,text,constants.IMAGE_CODE_REDIS_EXPIRES)  # 设置redis缓存
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR , errmsg=u'验证码保存失败')


    # 4.返回图片验证码
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response



# 定义发送短信验证码的视图
@api.route('/sms_code',methods=['POST'])
def send_sms_code():
    # 1.获取参数---手机号码,uuid,输入的图片验证码
    # 2.判断数据完整性
    # 3.获取存储的图片验证码,'image:uuid':code    进行比较
    # 4.如果两个验证码相同,生成短信验证码
    # 5.短信验证码保存在reids数据库
    # 6.发送短信验证码
    # 7.根据返回结果响应

   # 1.获取参数
    json_dict = request.json # 直接获取json数据的字典
    mobile = json_dict.get('mobile')
    uuid = json_dict.get('uuid')
    client_image_code = json_dict.get('imagecode')

    # 2.判断数据的完整性  数据的有效性校验
    if not all([mobile,uuid,client_image_code]):
        jsonify(errno=RET.DATAERR  , errmsg=u'缺少必要数据')

        # 判断手机号码
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        jsonify(errno=RET.DATAERR, errmsg=u'手机号码不合法')

    # 3.获取存储的图片code  拼接key
    image_key = 'image:%s' %uuid
    try:
        server_image_code = redis_store.get(image_key)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. NODATA , errmsg=u'图片验证码本地获取失败')

    if not server_image_code:
        return jsonify(errno=RET.NODATA, errmsg='验证码不存在')


    # 4.判断验证码是否一致
    if server_image_code.lower() != client_image_code.lower():
        return jsonify(errno=RET. DATAERR , errmsg=u'验证码不正确')

    # 生成短信验证码
    sms_code = '%06s' %random.randint(0,999999)
    current_app.logger.error(sms_code)
    # # 5.发送短信到用户
    # time = str(constants.SMS_CODE_REDIS_EXPIRES/60)
    # res = CCP().send_template_sms(mobile,[sms_code,time],'1')
    # if res != 1:
    #     return jsonify(errno=RET.THIRDERR  , errmsg=u'短信发送失败')


    # 6.存储短信验证码到redis

    sms_sky = 'sms:%s' %mobile
    try:
        redis_store.set(sms_sky,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DBERR , errmsg=u'短信验证码存储失败')



    return jsonify(errno=RET. OK, errmsg=u'短信发送成功')









