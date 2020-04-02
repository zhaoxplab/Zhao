"""
公用
"""
from flask import Flask
# 导入models
from ..models import db
# 导入api
from ..api_v1 import api, rule, parse, task, shopify, spider
# 导蓝图
from ..api_v1 import api_bp


def add_api():
    api.add_resource(rule.Rule, '/api/rules', '/api/rules/<int:rule_id>', '/api/rules/<string:rule_name>')
    api.add_resource(parse.Parse, '/api/parse')
    api.add_resource(task.Task, '/api/tasks', '/api/tasks/<string:t_status>')
    api.add_resource(shopify.Shopify, '/api/shopifys')
    api.add_resource(spider.Spider, '/api/spider', '/api/spider/<string:func>')
    pass


def add_blueprint(app):
    """
    添加蓝图
    :param app:
    :return:
    """
    app.register_blueprint(api_bp)
    pass


def create_app():
    app = Flask(__name__)

    # 初始化orm
    # SQLAlchemy注册
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:100798@47.97.166.98:3306/yzz?charset=utf8mb4'
    # 设置数据库追踪信息，压制警告
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    # api.init_app需要写在add_api()之后
    add_api()
    api.init_app(app)

    # 注册蓝图
    add_blueprint(app)
    return app
