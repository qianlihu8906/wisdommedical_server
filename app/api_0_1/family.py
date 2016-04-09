from flask import jsonify,request,current_app,url_for
from datetime import datetime
from . import api
from .authentication import verify_access_token
from .errors import bad_request
from ..models import User,Family,Member,Doctor,Ship,App,Sensor,Role,Sex,db
from sqlalchemy import desc

@api.route('/family/create',methods=['POST'])
@verify_access_token
def family_create():
    family_name = request.json.get('family_name')
    passwd = request.json.get('passwd')
    phone = request.json.get('phone')
    address = request.json.get('address')
    
    descp = request.json.get('descp') or ""
    pic = request.json.get('pic')  or ""


    if not family_name or not passwd or not phone or not address:
        return bad_request(40010)

    family = Family.query.filter_by(family_name=family_name).first()
    if family is not None:
        return bad_request(40003)
    User.new_family(family_name,passwd,phone,address,descp,pic)
    return bad_request(0)

@api.route('/family/get',methods=["POST"])
@verify_access_token
def family_get():
    family_name = request.json.get('family_name')
    passwd = request.json.get('passwd')
    if family_name is None or passwd is None:
        return bad_request(40010)
    user = User.query.filter_by(username=family_name,role=Role.FAMILY).first()
    if user is None:
        return bad_request(40004)
    if passwd != user.passwd:
        return bad_request(40012)
    family = Family.query.filter_by(family_name=family_name).first()
    if family is None:
        return bad_request(40004)
    return jsonify(family.to_json())
        
@api.route('/family/update',methods=["POST"])
@verify_access_token
def family_update():
    family_name = request.json.get('family_name')
    passwd = request.json.get('passwd')
    phone = request.json.get('phone')
    address = request.json.get('address')
    descp = request.json.get('descp')
    pic = request.json.get('pic')

    if not family_name:
        return bad_request(40010)
    family = Family.query.filter_by(family_name=family_name).first()
    if family is None:
        return bad_request(40004)
    if passwd is not None:
        family.passwd = passwd
    if phone is not None:
        family.phone = phone
    if address is not None:
        family.address = address
    if descp is not None:
        family.descp = descp
    if pic is not None:
        family.pic = pic

    return bad_request(0)

@api.route('/family/doctor/add',methods=["POST"])
@verify_access_token
def family_doctor_add():
    family_name =   request.json.get("family_name");
    doctor_name =   request.json.get("doctor_name");

    if not family_name or not doctor_name:
        return bad_request(40010)
    family = Family.query.filter_by(family_name=family_name).first()
    if not family:
        return bad_request(40004)
    doctor = Doctor.query.filter_by(doctor_name=doctor_name).first()
    if not doctor:
        return bad_request(40007)
    ship = Ship.query.filter_by(family_name=family_name,doctor_name=doctor_name).first()
    if ship is not None:
        return bad_request(40014)

    ship = Ship(family_name=family.family_name,doctor_name=doctor.doctor_name)
    db.session.add(ship)

    return bad_request(0)

@api.route('/family/doctor',methods=["POST"])
@verify_access_token
def family_doctor():
    family_name = request.json.get('family_name')

    if not family_name:
        return bad_request(40010)
    family = Family.query.filter_by(family_name=family_name).first()
    if not family:
        return bad_request(40004)
    ships = Ship.query.filter_by(family_name =family.family_name).all()
    count = len(ships)
    doctors = [Doctor.query.filter_by(doctor_name=ship.doctor_name).first().to_json() for ship in ships]

    return jsonify({'count':count,'doctors':doctors})

@api.route('/family/member/create',methods=['POST'])
@verify_access_token
def family_member_create():
    family_name = request.json.get('family_name')
    nickname = request.json.get('nickname')
    phone = request.json.get('phone')
    birthday = request.json.get('birthday') 
    sex = request.json.get('sex')
    weight = request.json.get('weight')
    height = request.json.get('height')
    pic = request.json.get('pic')

    birthday = datetime.strptime(birthday,"%Y-%m-%d")

    if not family_name or not nickname or not phone or not birthday or not sex or not weight or not height:
        return bad_request(40010)
    family = Family.query.filter_by(family_name=family_name).first()
    if not family:
        return bad_request(40004)

    members = family.members.all()
    if members is not None:
        for member in members:
            if member.nickname == nickname:
                return bad_request(40013)
    member = Member(family=family,nickname=nickname,phone=phone,birthday=birthday,sex=sex,weight=weight,height=height,pic=pic)
    db.session.add(member)
    return bad_request(0)

@api.route('/family/member/all',methods=["POST"])
@verify_access_token
def family_member_all():
    family_name = request.json.get('family_name')
    
    if not family_name:
        return bad_request(40010)
    family = Family.query.filter_by(family_name=family_name).first()
    if not family:
        return bad_request(40004)
    
    members = family.members.order_by(Member.id).all()

    return jsonify({'count':len(members),'members':[member.to_json() for member in members]})

@api.route('/family/member/all/sensor',methods=["POST"])
@verify_access_token
def family_member_all_sensor():
    family_name = request.json.get('family_name')
    if not family_name:
        return bad_request(40010)
    family = Family.query.filter_by(family_name=family_name).first()
    if not family:
        return bad_request(40004)

    members = family.members.order_by(Member.id).all()

    memberInfo = []

    count = len(members)
    for member in members:
        xueya = Sensor.query.filter_by(member=member,sensor_type='xueya').order_by(desc(Sensor.timestamp)).first()
        xueyang = Sensor.query.filter_by(member=member,sensor_type='xueyang').order_by(desc(Sensor.timestamp)).first()
        maibo = Sensor.query.filter_by(member=member,sensor_type='maibo').order_by(desc(Sensor.timestamp)).first()
        tiwen = Sensor.query.filter_by(member=member,sensor_type='tiwen').order_by(desc(Sensor.timestamp)).first()
        m = {}
        m["member_id"]= member.id
        m["nickname"] = member.nickname
        m["phone"] = member.phone
        m["sex"] = member.sex
        m["birthday"] = datetime.strftime(member.birthday,"%Y-%m-%d")
        m["weight"] = member.weight
        m["height"] = member.height
        if xueya is not None:
            m["xueya"] = xueya.sensor_data
        if xueyang is not None:
            m["xueyang"] = xueyang.sensor_data
        if maibo is not None:
            m["maibo"] = maibo.sensor_data
        if tiwen is not None:
            m["tiwen"] = tiwen.sensor_data
        memberInfo.append(m)
    return jsonify({'count':len(members),"members":memberInfo})



@api.route('/family/member/update',methods=["POST"])
@verify_access_token
def family_member_update():
    member_id = request.json.get('member_id')
    nickname  = request.json.get('nickname')
    phone = request.json.get('phone')
    sex  = request.json.get('sex')
    weight = request.json.get('weight')
    height = request.json.get('height')
    birthday = request.json.get("birthday")
    pic = request.json.get('pic')
    birthday = datetime.strptime(birthday,"%Y-%m-%d")


    if member_id is None:
        return bad_request(40010)
    member = Member.query.filter_by(id = member_id).first()
    if not member:
        return bad_request(40005)

    if nickname is not None:
        member.nickname = nickname
    if phone is not None:
        member.phone = phone
    if weight is not None:
        member.weight = weight
    if height is not None:
        member.height = height
    if pic is not None:
        member.pic = pic
    if birthday is not None:
        member.birthday = birthday
    if sex == Sex.MAN or sex == Sex.WOMAN:
        member.sex = sex

    return bad_request(0)

@api.route('/family/member/delete',methods=["POST"])
@verify_access_token
def family_member_delete():
    member_id = request.json.get('member_id')
    if not member_id:
        return bad_request(40010)
    member = Member.query.filter_by(id = member_id).first()
    
    if not member:
        return bad_request(40005)

    db.session.delete(member)

    return bad_request(0)

@api.route('/family/member/get',methods=["POST"])
@verify_access_token
def family_member_get():
    member_id = request.json.get('member_id')
    if not member_id:
        return bad_request(40010)
    member = Member.query.filter_by(id = member_id).first()
    
    if not member:
        return bad_request(40005)
    return jsonify(member.to_json)
