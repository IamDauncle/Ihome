# -*- coding:utf-8 -*-
from ihome import db
from ihome.utils.response_code import RET
from . import api
from ihome.utils.common import login_required
from flask import request,g,current_app,jsonify
from ihome.utils.image_storage import upload_image
from ihome.models import User
from ihome.constants import QINIU_DOMIN_PREFIX




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
    user_id = g.user_id
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
    avatar_image_user = QINIU_DOMIN_PREFIX + image_key


# # 6.返回json
    return jsonify(errno=RET. OK , errmsg=u'头像上传成功',data = avatar_image_user)
