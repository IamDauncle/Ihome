# -*- coding:utf-8 -*-


from ihome import db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from ihome import get_app



app = get_app('default_config')
# 创建脚本管理器对象
manage = Manager(app)
# 将app与数据库迁移关联
Migrate(app,db)
# 添加迁移数据库脚本
manage.add_command('db',MigrateCommand)






if __name__ == '__main__':
    manage.run()
    # app.run(debug=True)