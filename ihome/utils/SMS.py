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

#
# class Dl():
#
#
#     def __new__(cls, *args, **kwargs):
#
#         cls._price = None
#         if not cls._price:
#             cls._price = super(Dl, cls).__new__(cls, *args, **kwargs)
#             # 可以在这给对象进行属性或其他设置
#             return cls._price
#
# class DLl():
#
#     def __new__(cls, *args, **kwargs):
#
#         if not hasattr(cls,'_price'):
#             cls._price = super(Dl, cls).__new__(cls, *args, **kwargs)
#             return cls._price
#









#
# 单例的实现.定义一个类的私有属性赋值为None,该属性用于作为接受返回的事例对象.
#     class CCP(object)
    # _instance = None
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
    #      或 cls._instance = object.__new__(cls, *args, **kwargs)
    #     return cls._instance

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
    #
    #         # 初始化REST SDK
    #         cls._instance.rest = REST(serverIP, serverPort, softVersion)
    #         cls._instance.rest.setAccount(accountSid, accountToken)
    #         cls._instance.rest.setAppId(appId)
    #
    #     return cls._instance


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






    # def send_template_sms(self, to, datas, tempId):
    #     """真正发送短信的方法
    #     返回值：如果是1,表示云通讯向我们发送短信是成功的，如果是0，表示失败
    #     """
    #
    #     # result : 是云通信告诉开发者的结果信息
    #     result = self.rest.sendTemplateSMS(to, datas, tempId)
    #
    #     # return的结果值，是开发者告诉用户短信是否发送成功
    #     if result.get('statusCode') == '000000':
    #         return 1
    #     else:
    #         return 0
















# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
    
   
#sendTemplateSMS(手机号码,内容数据,模板Id)