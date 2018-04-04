# -*- coding:utf-8 -*-

from . import api
from ihome.utils.common import login_required



# @api.route('/user/avatar',methods = ['POST'])
# @login_required
# def upload_avatar():
#     # 用户上传头像的接口
# # 1.判断登陆状态
# # 2.接受上传头像图片，
# # 3.调用七牛云接口
# # 4.将返回的存储图片key存储 avatar_url
# # 5.拼接浏览器渲染图片路径
# # 6.返回json