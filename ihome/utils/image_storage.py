# -*- coding:utf-8 -*-
# 七牛云图片上传成功辉返回一个存储图片的key
import qiniu

access_key = "yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"  #两个key都是账号提供的
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW"
bucket_name = 'ihome'
# 拼接访问全路径 ： http://oyucyko3w.bkt.clouddn.com/FtEAyyPRhUT8SU3f5DNPeejBjMV5


def upload_image(image_data):
     # 提供的qiniu.Auth()  方法传入access_key,secret_key  获取链接对象
    q = qiniu.Auth(access_key,secret_key)
     # 通过对象的upload_token()方法获取token
    token = q.upload_token(bucket_name)
     # 上传图片方法qiniu.put_data（token，key，image_data）
     # key不传会自动返回key   ret存储了key，  'key':图片  status_code = 200 就是上传成功
     # info包含存储。错误信息
    ret, info = qiniu.put_data(token, None, image_data)

    if 200 == info.status_code:
        return ret.get('key') # 获取图片key信息
    else:
        raise Exception('图片上传失败')

# if __name__ == '__main__':
#     with open('/home/python/Flast/Ihome/ihome/static/images/home02.jpg','rb') as f:
#         key = upload_image(f.read())
#         print (key)