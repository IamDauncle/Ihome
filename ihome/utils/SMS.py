#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  


from ihome.libs.ytx_SDK.CCPRestSDK import REST

import ConfigParser

#���ʺ�
accountSid= '8a216da8627648690162852228720504'

#���ʺ�Token
accountToken= '8894cced59de4689a7bbae1929f798dd'

#Ӧ��Id
appId='8a216da8627648690162852228d3050b'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿� 
serverPort='8883'

#REST�汾��
softVersion='2013-12-26'

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id



# ʹ�ÿ���Դ��ĺ���������Ϣ�Ļ�,û����һ���ᴴ��һ������,�����������ڴ�
# �Զ��巢�Ͷ��ŵĵ���
class CCP(object):

    def __new__(cls, *args, **kwargs):
    # �����Ĵ���,
        if not hasattr(cls,'_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # ��ʼ��REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)

        return cls._instance


    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
    #
    #         # ��ʼ��REST SDK
    #         cls._instance.rest = REST(serverIP, serverPort, softVersion)
    #         cls._instance.rest.setAccount(accountSid, accountToken)
    #         cls._instance.rest.setAppId(appId)
    #
    #     return cls._instance


    def send_template_sms(self,to, datas, tempId):
    # �����ŵĺ���

# ���Ͷ��ŷ��صĽ��  ���ͳɹ��򷵻�'000000'        sendTemplateSMS(to, datas, tempId)--���Ͷ���
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # �Խ�������ж�

        if result == '000000':
            return 1
        else:
            return 0



    # def send_template_sms(self, to, datas, tempId):
    #     """�������Ͷ��ŵķ���
    #     ����ֵ�������1,��ʾ��ͨѶ�����Ƿ��Ͷ����ǳɹ��ģ������0����ʾʧ��
    #     """
    #
    #     # result : ����ͨ�Ÿ��߿����ߵĽ����Ϣ
    #     result = self.rest.sendTemplateSMS(to, datas, tempId)
    #
    #     # return�Ľ��ֵ���ǿ����߸����û������Ƿ��ͳɹ�
    #     if result.get('statusCode') == '000000':
    #         return 1
    #     else:
    #         return 0
















# def sendTemplateSMS(to,datas,tempId):
#
#
#     #��ʼ��REST SDK
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
    
   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)