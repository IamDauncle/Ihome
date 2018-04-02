# -*- coding:utf-8 -*-
# 发送短信验证码


from . import api

@api.route('/passwords')
def register():
    # 1.获取参数,手机号,密码,用户短信验证码,uuid
    # 2.判断参数完整性
    # 3.获取服务器存储的短信验证码,比较两个验证码
    # 4.验证码相同就创建新用户---添加数据,保存数据
    # 5.返回结果


    pass

