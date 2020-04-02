from flask_restful import Resource
import asyncio
from flask import request, jsonify, current_app
from ..models import db, Tasks
from ..utils.reptile import Reptile


class Spider(Resource):
    def __init__(self):
        self.task = []
        pass

    def post(self, func=None):
        if func == 'start':
            result_ob = Tasks.query.filter(Tasks.status == '0').all()
            for res in result_ob:
                worm = Reptile(domain=res.domain)
                worm.run()
                task_ob = Tasks.query.filter(Tasks.domain == res.domain).first()
                task_ob.status = '1'
                try:
                    db.session.commit()
                    return jsonify({'msg': f'{res.domain} 任务完成'})
                except Exception as e:
                    current_app.logger.error(e)
                    return jsonify({'msg': 'error'})
        elif func == 'stop':
            return jsonify({'msg': '尚未提供此功能'})
        else:
            return jsonify({'msg': 403})
            pass
