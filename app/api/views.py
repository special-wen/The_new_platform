#coding=utf-8
from . import api
from flask import current_app,jsonify,request
import json,datetime
from app.models import Interviewer,Record


@api.route('/signin', methods=['GET'])
def get_signin_list():
    s = current_app.config['WAIT_LIST']
    lists = []
    for i in s:
        lists.append((i.id,i.name,))
    data = {
        'total': len(s),
        'data': lists,
    }
    return jsonify(data)


@api.route('/signin', methods=['POST'])
def add_signin():
    stu_num = request.json.get('stu_num')
    inter = Interviewer.select().where(Interviewer.classes == str(datetime.datetime.now().year) and
                               Interviewer.stu_num == stu_num).first()
    if inter: #学号正确
        if inter not in current_app.config['WAIT_LIST']: #不在等待队列
            if not Record.select().where(Record.interviewer == inter and
                   Record.big_num == current_app.config['NOW_TIMES']).first():
                current_app.config['WAIT_LIST'].append(inter)
                status = True
                msg = '签到成功'

            else:
                status = False
                msg = '已参加过本轮面试，无需重复签到'
        else:
            status = False
            msg = '已在等待队列'
    else:
        status = False
        msg = '没有找到对应的应聘者'

    return jsonify({'msg':msg,'status':status})

@api.route('/interviewer')
def interviewer():
    stu_num = request.args.get('stu_num')
    inter = Interviewer.select().where(Interviewer.stu_num == stu_num and
                               Interviewer.classes == datetime.datetime.now().year).first()
    if inter:
        return jsonify({'status':True,'data':inter.to_json()})
    else:
        return jsonify({'msg':'找不到信息','status':False})