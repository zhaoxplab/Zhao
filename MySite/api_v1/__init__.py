# api文件
from flask import Blueprint
from flask_restful import Api

# 蓝图的名字
api_bp = Blueprint('api', __name__)
# api名字
api = Api()
