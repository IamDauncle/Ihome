# -*- coding:utf-8 -*-

from ihome.api_1_0 import api
from ihome.utils.SMS import CCP

# 使用蓝图注册路由
@api.route("/ll",methods=['POST','GET'])
def index():
    res = CCP().send_template_sms('18318050479', ['170711', '5'], '1')
    return 'll'
