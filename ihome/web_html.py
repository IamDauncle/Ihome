# -*- coding:utf-8 -*-

# 因为静态资源默认从讲台目录static目录下去寻找,可以就使得url累赘
# 定义一个用来获取静态资源的视图

# 创建蓝图

from flask import Blueprint,current_app

static_blue = Blueprint('static_blue',__name__)

@static_blue.route('/<file_name>')
def get_static_html(file_name):
    # 获取静态资源的视图
    # 静态资源访问  /static/html/index.html
    # 需求1.输入index.html直接访问
    #     2.访问/时,为index.html
    #     3.获取图标


    # 判断输入
    if not file_name:  #如果访问'/'
        file_name = 'index.html'

    if file_name != 'favicon.ico': # 如果访问的不是图标   是favicon.ico就直接从static取了
        file_name = 'html/%s' %file_name   # 无论是'/'还是其他html页面,都在这里拼接


    # current_app是应用上下文
    # send_static_file()是在静态资源static中获取传入的路径资源
    # 所以,send_static_file() 默认会在传入的路径前面拼接上'/static/'
    return current_app.send_static_file(file_name)





