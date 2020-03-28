from flask_restful import Resource
from flask import request, jsonify, current_app
from ..models import db, Quotations


class Flatter(Resource):
    def __init__(self):
        pass

    def get(self, flatter_id=None):
        # data = request.get_json(force=True)
        if flatter_id:
            result_ob = Quotations.query.filter(Quotations.id == flatter_id).first()
            result = dict()
            result['content'] = result_ob.content
            return jsonify(result)
        else:
            result_ob = Quotations.query.all()
            contents = []
            for res in result_ob:
                all_content = dict()
                all_content['fid'] = res.id
                all_content['content'] = res.content
                contents.append(all_content)
            result = dict()
            result['msg'] = 'success'
            result['data'] = contents
            return jsonify(result)
        # return jsonify({'msg': 'success'})
        pass

    def post(self):
        json_data = request.get_json(force=True)
        data = json_data.get('content')  # 获取内容
        content = Quotations(
            content=data
        )
        # 提交到数据库
        db.session.add(content)
        try:
            db.session.commit()
            return jsonify({'msg': 'success', 'body': data})
        except Exception as e:
            db.session.rollback()  # 回滚
            current_app.logger.error(e)
        pass

    def delete(self):
        pass

    def put(self):
        pass
