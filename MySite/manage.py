"""
先导入相关的类，注意模型要全部导入过来，即使代码中并没有显式地使用它们。
然后传入app或db来构建Manager和Migrate两个类的实例，
最后将MigrateCommand的命令加入到manager中。
#################################################################################
此时我们假设要更新模型的结构，在models.py的User模型结尾添加一行代码test = db.Column(db.Integer)，
然后点击PyCharm下方的Terminal，自动进入到了虚拟环境的命令行中，输入python manage.py db init来初始化，
这一步主要是建立数据库迁移相关的文件和文件夹，只是在第一次需要使用。
接着依次使用python manage.py db migrate和python manage.py db upgrade，
待运行完成
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .utils import create_app, db
from .models import Quotations

# migrate = Migrate(app=create_app(), db=db)
migrate = Migrate(app=create_app())

manager = Manager(app=create_app())
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
