#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-
from flask import current_app

from ihome.libs.ytx_SDK.CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a216da8627648690162852228720504'

#主帐号Token
accountToken= '8894cced59de4689a7bbae1929f798dd'

#应用Id
appId='8a216da8627648690162852228d3050b'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id



# 使用框架自带的函数发送信息的话,没发送一条会创建一个对象,这样就消耗内存
# 自定义发送短信的单例
class CCP(object):

    def __new__(cls, *args, **kwargs):
    # 单例的创建,
        if not hasattr(cls,'_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)

        return cls._instance



    def send_template_sms(self,to, datas, tempId):
    # 发短信的函数

# 发送短信返回的结果  发送成功或返回'000000'        sendTemplateSMS(to, datas, tempId)--发送短信
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # 对结果进行判断
        current_app.logger.debug(result)

    # {'templateSMS': {'smsMessageSid': '8c881d5eefc64947a8418cff2044cd9e', 'dateCreated': '20180403121400'},
    #  'statusCode': '000000'}

        if result['statusCode'] == '000000':
            return 1
        else:
            return 0



