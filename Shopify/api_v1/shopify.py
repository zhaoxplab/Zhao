from flask_restful import Resource
from flask import request, jsonify, current_app
from ..models import db, Shopifys


class Shopify(Resource):
    def __init__(self):
        pass

    def get(self):
        pass

    def post(self):
        json_data = request.get_json(force=True)
        tittle = json_data.get('tittle')
        price = json_data.get('price')
        domain = json_data.get('domain')
        link = json_data.get('link')
        sku = json_data.get('sku')
        specs = json_data.get('specs')
        img_link = json_data.get('img_link')
        data = Shopifys(
            tittle=tittle,
            price=price,
            domain=domain,
            link=link,
            sku=sku,
            specs=specs,
            img_link=img_link
        )
        db.session.add(data)
        try:
            db.session.commit()
            return json_data({'msg': 'success'})
        except Exception as e:
            db.session.rollback()  # 回滚
            current_app.logger.error(e)
            return jsonify({'msg': 'error'})
        pass

    def delete(self):
        pass

    def put(self):
        pass
