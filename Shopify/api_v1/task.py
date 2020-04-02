from flask_restful import Resource
from flask import request, jsonify, current_app
from ..models import db, Tasks


class Task(Resource):
    def __init__(self):
        pass

    def get(self, t_status=None):
        if t_status == '1':  # 查询所有已完成
            result_ob = Tasks.query.filter(Tasks.status == t_status).all()
        elif t_status == '0':  # 查询所有未完成
            result_ob = Tasks.query.filter(Tasks.status == t_status).all()
        else:
            result_ob = Tasks.query.all()
        tasks = []
        for res in result_ob:
            task = dict()
            task['t_id'] = res.id
            task['domain'] = res.domain
            task['status'] = res.status
            tasks.append(task)
        result = dict()
        result['msg'] = 'success'
        result['data'] = tasks
        return jsonify(result)
        pass

    def post(self):
        """
        接收一个domain，和status(任务状态)默认'0'，未完成
        :return:
        """
        json_data = request.get_json(force=True)
        task_list = json_data['tasks']
        for task in task_list:
            domain = task['domain']
            status = task['status']
            data = Tasks(
                domain=domain,
                status=status
            )
            db.session.add(data)
        try:
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            db.session.rollback()  # 回滚
            current_app.logger.error(e)
            return jsonify({'msg': 'error'})
        pass

    def delete(self):
        """
        把任务标记为已完成状态
        """
        json_data = request.get_json(force=True)
        if json_data['domain']:
            url = json_data['domain']
            result_ob = Tasks.query.filter(Tasks.domain == url).first_or_404(description=f'{url} 任务不存在')
        else:
            return jsonify({'msg': 404})
        result_ob.status = '1'
        # 提交修改
        try:
            db.session.commit()
            return jsonify({'msg': f'{url}已完成'})
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'msg': 400})

    def put(self):
        """
        实现不了，2020年4月2日14:02:15，改个锤子
        :return:
        """
        return jsonify({'msg': 403})

        # json_data = request.get_json(force=True)
        # if json_data:
        #     url = json_data['domain']
        #     status = json_data['status']
        #     result_ob = Tasks.query.filter(Tasks.domain == url).first_or_404(description=f'{url} 任务不存在')
        # else:
        #     return jsonify({'msg': 404})
        # result_ob.status = status
        # # 提交修改
        # try:
        #     db.session.commit()
        #     return jsonify({'msg': f'{url}已完成'})
        # except Exception as e:
        #     current_app.logger.error(e)
        #     return jsonify({'msg': 400})
        # pass
