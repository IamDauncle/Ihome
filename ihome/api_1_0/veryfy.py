# # -*- coding:utf-8 -*-
#
# # 验证视图
#
# from ihome.api_1_0 import api
# from ihome.utils.captcha.captcha import captcha
# from flask import make_response
#
#
#
#
# @api.route('/image_codes')
# def get_image_code():
#     # 定义生成验证码图片的视图
#
#     # 框架生成验证码图片   text为文字信息,image为图片
#     name, text, image = captcha.generate_captcha()
#
#     resposne = make_response(image)
#     resposne.headers['Content-Type'] = 'image/jpg'
#     return resposne
#     # return image







# -*- coding:utf-8 -*-
# 图片验证码和短信验证码


from . import api
from flask import request,current_app,jsonify,make_response
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store,constants
from ihome.utils.response_code import RET




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

















#
# from . import api
# from ihome.utils.captcha.captcha import captcha
# from flask import request, make_response, jsonify, abort, current_app
# from ihome import redis_store
# from ihome import constants
# from ihome.utils.response_code import RET
#
#     """提供图片验证码
#     1.接受请求，获取uuid
#     2.生成图片验证码
#     3.使用UUID存储图片验证码内容到redis
#     4.返回图片验证码
#     """

    #
    # # 1.接受请求，获取uuid
    # uuid = request.args.get('uuid')
    # last_uuid = request.args.get('last_uuid')
    # if not uuid:
    #     abort(403)
    #     # return jsonify(errno=RET.PARAMERR, errmsg=u'缺少参数')
    #
    # # 2.生成验证码:text是验证码的文字信息，image验证码的图片信息
    # name, text, image = captcha.generate_captcha()
    #
    # # 3.使用UUID存储图片验证码内容到redis
    # try:
    #     if last_uuid:
    #         # 上次的uuid还存在，删除上次的uuid对应的记录
    #         redis_store.delete('ImageCode:' + last_uuid)
    #
    #     # 保存本次需要记录的验证码数据
    #     redis_store.set('ImageCode:' + uuid, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    # except Exception as e:
    #     print e
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg=u'保存验证码失败')
    #
    # # 4.返回图片验证码
    # resposne = make_response(image)
    # resposne.headers['Content-Type'] = 'image/jpg'
    # return resposne
