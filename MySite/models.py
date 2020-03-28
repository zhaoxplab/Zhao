"""
这个是ORM
"""
from flask_sqlalchemy import SQLAlchemy

# 先实例化一个db
db = SQLAlchemy()


# 舔狗语录
class Quotations(db.Model):
    __tablename__ = 'flatter'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # 内容
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建时间

    def __repr__(self):
        return '<CreateTime %r>' % self.create_time
