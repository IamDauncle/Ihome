# -*- coding:utf-8 -*-
import re

from ihome import db
from ihome.utils.response_code import RET
from ihome.api_1_0 import api
from ihome.utils.common import login_required
from flask import request,g,current_app,jsonify,session
from ihome.utils.image_storage import upload_image
from ihome.models import User
from ihome import constants



# 展示个人信息接口 用于修改页和个人主页
@api.route('/users')
@login_required
def show_user_info():
    # 显示客人信息接口
    # 1.判断登陆
    # 2.获取用户信息
    # 3.查询用户显示信息
    # 4.响应展示信息

    # 2.获取用户信息
    # user_id = g.user_id
    user_id = session['user_id']
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DBERR , errmsg=u'数据查询失败')
    if not user:
        return jsonify(errno=RET. USERERR , errmsg=u'用户名或密码不存在')

        # 3.查询用户显示信息
    # response_data = {
    #     'avatar_url': constants.QINIU_DOMIN_PREFIX + (self.avatar_url if self.avatar_url else ""),
    #     'name': self.name,
    #     'mobile': self.mobile,
    #     'user_id': self.id
    # }

    # 调用封装在models的用户信息数据函数
    context = user.to_dict()

    return jsonify(errno=RET. OK , errmsg=u'数据查询成功',data=context)




# 定义上传图片接口
@api.route('/users/avatar',methods=['POST'])
@login_required
def upload_avatar():
    # 用户上传头像的接口
# # 1.判断登陆状态
# # 2.接受上传头像图片，
    try:
        image_file = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='头像参数错误')
# # 3.调用七牛云接口
    try:
        image_key = upload_image(image_file)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传头像失败')
# # 4.将返回的存储图片key存储 avatar_url
    user_id = session['user_id']
    # user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e :
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR  , errmsg=u'用户查询失败')
    if not user:
        return jsonify(errno=RET.USERERR , errmsg=u'用户不存在或密码错误')
    user.avatar_url = image_key
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.roolback()
        return jsonify(errno=RET. DBERR , errmsg=u'头像图片保存失败')
# # 5.拼接浏览器渲染图片路径
    avatar_image_user = constants.QINIU_DOMIN_PREFIX + image_key


# # 6.返回json
    return jsonify(errno=RET. OK , errmsg=u'头像上传成功',data = avatar_image_user)




# 定义修改名字接口
@api.route('/users/name', methods=['PUT'])
@login_required
def change_name():
    # -----修改名字接口-----
    # 1.判断登陆
    # 2.获取参数
    json_dict = request.json
    name = json_dict.get('name')
# 3.校验参数
    if not all([name]):
        return jsonify(errno=RET. PARAMERR , errmsg=u'数据不完整')
    # user_id = g.user_id
    user_id = session['user_id']
    try:
        user = User.query.get(user_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg=u'获取数据失败')
    if not user:
        return jsonify(errno=RET.USERERR  , errmsg=u'用户不存在或密码不对')

# 4.存储数据
    user.name = name
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR , errmsg=u'数据保存失败')

    try:
        session['user_name'] = name
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. UNKOWNERR , errmsg=u'session修改失败')

# 5.返回响应json
    return jsonify(errno=RET. OK , errmsg=u'名称修改成功')



# 定义提交实名认证接口
@api.route('/users/auth',methods=['POST'])
@login_required
def set_user_auth():
    # 1.判断登陆
    # 2.接受参数   --id_card  --real_name
    # 3.参数校验   --是否完整  --身份证的校验  --姓名校验
    # 4.查询用户信息
    # 5.添加认证信息到属性
    # 6.返回响应


# 2.接受参数   --id_card  --real_name
    json_dict = request.json
    id_card = json_dict.get('id_card')
    real_name = json_dict.get('real_name')

    # 3.参数校验   --是否完整  --
    if not all([id_card,real_name]):
        return jsonify(errno=RET.PARAMERR  , errmsg=u'数据不完整')
    # 判断身份证
    # red = r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$'
    # if not re.match(red,id_card):
    #     return jsonify(errno=RET.ROLEERR  , errmsg=u'身份证格式有误')
    # # 姓名校验

    # 4.查询用户信息
    user_id = session['user_id']
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET. DBERR , errmsg=u'数据查询失败')
    if not user:
        return jsonify(errno=RET. USERERR , errmsg=u'用户名或密码不正确')


    user.id_card = id_card
    user.real_name = real_name
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET. DBERR , errmsg=u'数据存储失败')
    return jsonify(errno=RET. OK , errmsg=u'实名认证成功')





# 显示实名认证接口
@api.route('/users/auth')
@login_required
def show_user_auth():
    # 1.判断登陆

# 4.查询用户信息 判断是否存在用户
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR  , errmsg=u'用户数据获取失败')

    if not user:
        return jsonify(errno=RET.USERERR  , errmsg=u'用户名不存在或密码错误')
# 5.查询显示数据 --real_name --id_card
    context = user.arth_to_dict()
# 6.返回响应
    return jsonify(errno=RET.OK  , errmsg=u'实名认证信息获取成功',data = {'user_arth':context})