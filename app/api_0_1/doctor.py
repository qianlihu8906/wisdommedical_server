from flask import jsonify,request
from . import api
from .authentication import verify_access_token
from .errors import bad_request
from ..models import User,Doctor,App,Ship,Family,Role,Sex,db
from datetime import datetime

@api.route('/doctor/create',methods=['POST'])
@verify_access_token
def doctor_create():
    doctor_name = request.json.get('doctor_name')
    passwd = request.json.get('passwd')
    phone = request.json.get('phone')
    descp = request.json.get('descp')
    birthday = request.json.get('birthday')
    sex = request.json.get('sex')
    pic = request.json.get('pic') 

    birthday = datetime.strptime(birthday,"%Y-%m-%d")

    if not doctor_name or not passwd or not phone or not descp or not birthday or not sex:
        return bad_request(40010)
    doctor = Doctor.query.filter_by(doctor_name = doctor_name).first()
    if doctor is not None:
        return bad_request(40006)
    User.new_doctor(doctor_name,passwd,phone,birthday,sex,descp,pic)
    return bad_request(0)

@api.route('/doctor/update',methods=['POST'])
@verify_access_token
def doctor_update():
    doctor_name = request.json.get('doctor_name')
    passwd = request.json.get('passwd')
    phone = request.json.get('phone')
    descp = request.json.get('descp')
    pic = request.json.get('pic')

    if not doctor_name:
        return bad_request(40010)
    doctor = Doctor.query.filter_by(doctor_name=doctor_name).first()
    if not doctor:
        return bad_request(40007)
    if passwd is not None:
        doctor.passwd=passwd
    if phone is not None:
        doctor.phone = phone
    if descp is not None:
        doctor.descp = descp
    if pic is not None:
        doctor.pic = pic

    return bad_request(0)

@api.route('/doctor/get',methods=["POST"])
@verify_access_token
def doctor():
    doctor_name = request.json.get('doctor_name')
    passwd  = request.json.get('passwd')

    if not doctor_name:
        return bad_request(40010)
    user = User.query.filter_by(username=doctor_name,role=Role.DOCTOR).first()
    if user is None:
        return bad_request(40007)
    if passwd != user.passwd:
        return bad_request(40012)
    doctor = Doctor.query.filter_by(doctor_name=doctor_name).first()
    if doctor is None:
        return bad_request(40006)

    return jsonify(doctor.to_json())

@api.route('/doctor/getpic',methods=["POST"])
@verify_access_token
def doctor_getpic():
    doctor_name = request.json.get('doctor_name')

    if not doctor_name:
        return bad_request(40010)
    user = User.query.filter_by(username=doctor_name,role=Role.DOCTOR).first()
    if user is None:
        return bad_request(40007)
    doctor = Doctor.query.filter_by(doctor_name=doctor_name).first()
    if doctor is None:
        return bad_request(40006)

    return jsonify(doctor.to_json())

@api.route('/doctor/all')
@verify_access_token
def doctor_all():
    doctors = Doctor.query.order_by(Doctor.id).all()
    count = len(doctors)
    
    return jsonify({'count':count,'doctors':[doctor.to_json() for doctor in doctors]})

@api.route('/doctor/family',methods=["POST"])
@verify_access_token
def doctor_family():
    doctor_name = request.json.get('doctor_name')

    if not doctor_name:
        return bad_request(40010)

    ships = Ship.query.filter_by(doctor_name=doctor_name).order_by(Ship.id).all()

    familys = [Family.query.filter_by(family_name=ship.family_name).first().to_json() for ship in ships]

    return jsonify({'count':len(familys),'familys':familys})
