"""
提取规则api
增删改查
"""
from flask_restful import Resource
from flask import request, jsonify, current_app
from ..models import db, Rules


class Rule(Resource):
    def __init__(self):
        pass

    def get(self, rule_id=None, rule_name=None):
        """
        获取所有解析规则
        :return:
        """
        if rule_id:
            result_ob = Rules.query.filter(Rules.id == rule_id).first_or_404(description=f'{rule_id} 不存在')
        elif rule_name:
            result_ob = Rules.query.filter(Rules.theme == rule_name).first_or_404(description=f'{rule_name} 不存在')
        else:
            result_ob = Rules.query.all()
            rules = []
            for res in result_ob:
                all_rules = dict()
                all_rules['theme'] = res.theme
                all_rules['rule'] = res.rules
                all_rules['describe'] = res.describe
                rules.append(all_rules)
            result = dict()
            result['msg'] = 'success'
            result['rules'] = rules
            return jsonify(result)
        result = dict()
        result['theme'] = result_ob.theme
        result['rules'] = result_ob.rules
        result['describe'] = result_ob.describe
        return jsonify({'msg': 'success', 'data': result})
    d = {
        'msg': 'success',
        'data': {
            'theme': '模板',
            'rules': {
                "page": "页码",
                "goods_link": "商品链接",
                "goods_name": "商品标题",
                "goods_price": "商品价格",
                "goods_norms": "商品属性",
                "goods_value": "商品属性值",
                "img_links": "图片链接"
            },
            'describe': '描述'
        }
    }

    def post(self):
        """
        接收三个参数
        :param theme: 主题名
        :param rules: 解析规则
        :param describe: 描述
        :return:
        request_body = {
                "theme": "Debut",
                "rules":{
                    "page": "/html/body/div[3]/main/div/div/div/ul[2]/li[2]/text()",
                    "goods_link": "//div[@id='Collection']/ul/li/div/a/@href",
                    "goods_name": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[1]/h1/text()",
                    "goods_price": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[1]/div/dl/div[1]/div[1]/dd/span/text()",
                    "goods_norms": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[2]/p/span/strong/text()",
                    "goods_value": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[2]/p/span/text()",
                    "img_links": "//div[contains(@class,'thumbnails-wrapper')]/ul/li/a/@href"
                },
                "describe":"Debut主题"
            }
        """
        json_data = request.get_json(force=True)
        # print(json_data)
        theme = json_data.get('theme')
        rules = json_data.get('rules')
        describe = json_data.get('describe')
        data = Rules(
            theme=theme,
            rules=rules,
            describe=describe
        )
        db.session.add(data)
        try:
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            db.session.rollback()  # 回滚
            current_app.logger.error(e)
            return jsonify({'msg': 'error'})

    def delete(self, rule_id=None, rule_name=None):
        """
        :param rule_id: 规则id
        :param rule_name: 规则名
        :return:
        """
        if rule_id:
            Rules.query.filter(Rules.id == rule_id).delete()
        elif rule_name:
            Rules.query.filter(Rules.theme == rule_name).delete()
        else:
            return jsonify({'msg': 400})
        try:
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'msg': 'error'})

    def put(self, rule_id=None, rule_name=None):
        """
        修改
        :param rule_id:
        :param rule_name:
        :return:
        """
        json_data = request.get_json(force=True)  # 获取修改的数据，2020年3月30日10:33:13
        theme = json_data.get('theme')
        rules = json_data.get('rules')
        describe = json_data.get('describe')
        if rule_id:
            result_ob = Rules.query.filter(Rules.id == rule_id).first_or_404(description=f'{rule_id} 不存在')
        elif rule_name:
            result_ob = Rules.query.filter(Rules.theme == rule_name).first_or_404(description=f'{rule_name} 不存在')
        else:
            return jsonify({'msg': 404})
        # 修改数据
        result_ob.theme = theme
        result_ob.rules = rules
        result_ob.describe = describe
        # 提交修改
        try:
            db.session.commit()
            return jsonify(json_data)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'msg': 400})
