"""
这个是ORM
"""
from flask_sqlalchemy import SQLAlchemy

# 先实例化一个db
db = SQLAlchemy()


class Rules(db.Model):
    __tablename__ = 'rules'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    theme = db.Column(db.String(64), nullable=False, comment='主题')
    rules = db.Column(db.JSON, nullable=False, comment='解析规则')
    describe = db.Column(db.String(255), comment='描述')
    create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建时间')

    def __repr__(self):
        return '<Theme Name %r>' % self.theme


class Shopifys(db.Model):
    __tablename__ = 'shopify'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    tittle = db.Column(db.String(255), nullable=False, comment='标题')
    price = db.Column(db.String(64), nullable=False, comment='价格')
    domain = db.Column(db.String(255), comment='域名')
    link = db.Column(db.String(255), unique=True, nullable=False, comment='商品链接')
    sku = db.Column(db.JSON, nullable=False, comment='sku')
    specs = db.Column(db.JSON, nullable=False, comment='规格')
    img_link = db.Column(db.JSON, comment='图片链接')
    update_time = db.Column(db.TIMESTAMP, nullable=False, comment='修改时间')

    def __repr__(self):
        return '<Goods Name %r>' % self.tittle


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    domain = db.Column(db.String(255), unique=True, nullable=False, comment='域名')
    status = db.Column(db.Enum('1', '0'), server_default='0')
    create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建时间')

    def __repr__(self):
        return '<Theme Name %r>' % self.theme
