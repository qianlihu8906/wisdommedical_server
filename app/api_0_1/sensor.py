from flask import jsonify,request,current_app,url_for
from . import api 
from .authentication import verify_access_token
from .errors import bad_request
from ..models import Family,Member,Sensor,App,db
import json
from datetime import datetime

@api.route('/sensor/create',methods=['POST'])
@verify_access_token
def sensor_create():

    member_id = request.json.get('member_id')
    sensor_type = request.json.get('sensor_type')
    sensor_data = request.json.get('sensor_data')

    if not member_id or not sensor_type or not sensor_data:
        return bad_request(40010)
    
    member = Member.query.filter_by(id=member_id).first()
    if not member:
        return bad_request(40005)

    sensor = Sensor(member=member,sensor_data=json.dumps(sensor_data),sensor_type=sensor_type)
    db.session.add(sensor)

    return bad_request(0)


@api.route('/sensor/get',methods=["POST"])
@verify_access_token
def sensor_get():
    member_id = request.json.get('member_id')
    sensor_type = request.json.get('sensor_type')

    if not member_id or not sensor_type:
        return bad_request(40010)
    
    member = Member.query.filter_by(id = member_id).first()
    if not member:
        return bad_request(40005)

    sensors = Sensor.query.filter_by(member=member,sensor_type=sensor_type).order_by(Sensor.timestamp).all()
    count = len(sensors)
    return jsonify({'count':count,'sensors':[sensor.to_json() for sensor in sensors]})

@api.route('/sensor/get_one')
@verify_access_token
def sensor_get_one():
    pass
