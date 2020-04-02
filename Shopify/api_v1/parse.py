from flask_restful import Resource
from flask import request, jsonify, current_app
from ..utils.gt import GetTheme
from ..models import db, Rules


class Parse(Resource):
    def __init__(self):
        pass

    def get(self):
        pass

    def post(self):
        """
        数据格式
        request_body = {
            'url': ['url_1', 'url_2', 'url3']
        }
        :return: response_body = {
            'data': [
                {
                    'link': 'url_1',
                    'theme': 'theme_1'
                },
                {
                    'link': 'url_2',
                    'theme': 'theme_2'
                },
            ]
        }
        """
        json_data = request.get_json(force=True)
        urls = json_data['url']
        get_theme = GetTheme(urls=urls)  # 实例化是传入url_list
        result = get_theme.run()  # 返回
        return jsonify({'data': result})
