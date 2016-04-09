from datetime import datetime
import uuid,json
from flask import current_app
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Role:
    FAMILY = 0x01
    DOCTOR = 0x02

class Sex:
    MAN = 0x01
    WOMAN = 0x02

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer,primary_key=True)
    doctor_name = db.Column(db.String(64),unique=True)
    phone = db.Column(db.String(64))
    birthday = db.Column(db.DateTime(),default=datetime.utcnow)
    sex = db.Column(db.Integer)
    pic = db.Column(db.String(64))
    descp = db.Column(db.String(64))
   
    def __repr__(self):
        return '<Doctor %r>' % self.doctor_name

    def to_json(self):
        doctor_json = {
                'doctor_name':self.doctor_name,
                'phone':self.phone,
                'birthday':datetime.strftime(self.birthday,"%Y-%m-%d"),
                'sex':self.sex,
                'pic':self.pic,
                'descp':self.descp
            }
        return doctor_json


class Family(db.Model):
    __tablename__ = 'family'
    id = db.Column(db.Integer,primary_key=True)
    family_name=db.Column(db.String(64),unique=True)
    phone = db.Column(db.String(64))
    address = db.Column(db.String(64))
    descp = db.Column(db.String(64))
    pic = db.Column(db.String(64))
    members = db.relationship('Member',backref='family',lazy='dynamic')

    def __repr__(self):
        return '<Family %r>' % self.family_name
    
    def to_json(self):
        family_json = {
                'family_name':self.family_name,
                'phone':self.phone,
                'address':self.address,
                'descp':self.descp,
                'pic':self.pic,
            }
        return family_json

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    role = db.Column(db.Integer)
    passwd = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' %self.username

    def to_json(self):
        user_json = {
                'username':self.username,
                'role':self.role,
                'passwd':self.passwd,
                }
        return user_json

    @staticmethod
    def new_family(family_name,passwd,phone,address,descp="",pic=""):
        user = User(username=family_name,passwd=passwd,role=Role.FAMILY)
        family = Family(family_name=family_name,phone=phone,address=address,descp=descp,pic=pic)
        db.session.add(user)
        db.session.add(family)
        db.session.commit()

    @staticmethod
    def new_doctor(doctor_name,passwd,phone,birthday,sex,descp="",pic=""):
        user = User(username=doctor_name,passwd=passwd,role=Role.DOCTOR)
        doctor = Doctor(doctor_name=doctor_name,phone=phone,birthday=birthday,sex=sex,descp=descp,pic=pic)
        db.session.add(user)
        db.session.add(doctor)
        db.session.commit()

class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer,primary_key=True)
    family_id = db.Column(db.Integer,db.ForeignKey('family.id'))
    nickname = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    birthday = db.Column(db.DateTime(),default=datetime.utcnow)
    weight = db.Column(db.String(64))
    height = db.Column(db.String(64))
    pic = db.Column(db.String(64))
    sensor = db.relationship('Sensor',backref='member',lazy='dynamic')

    def __repr__(self):
        return '<Member %r>' % self.nickname

    def to_json(self):
        member_json = {
                'member_id':self.id,
                'nickname':self.nickname,
                'phone':self.phone,
                'sex':self.sex,
                'birthday':datetime.strftime(self.birthday,"%Y-%m-%d"),
                'weight':self.weight,
                'height':self.height,
                'pic':self.pic,
            }
        return member_json

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'))
    sensor_type = db.Column(db.String(64))
    sensor_data = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return '<Sensor %r:%r:%r>' %(self.sensor_type,self.sensor_data,self.timestamp)

    def to_json(self):
        sensor_json = {
            'sensor_type':self.sensor_type,
            'sensor_data':json.loads(self.sensor_data),
            'timestamp':self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        return sensor_json



class Ship(db.Model):
    __tablename__ = 'ship'
    id = db.Column(db.Integer,primary_key=True)
    family_name = db.Column(db.String(64))
    doctor_name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class App(db.Model):
    __tablename__ = 'app'
    id = db.Column(db.Integer,primary_key=True)
    appid = db.Column(db.String(64),unique=True)
    appsecret = db.Column(db.String(64))

    def __repr__(self):
        return '<App %r %r>' %(self.appid,self.appsecret)

    @staticmethod
    def new_app(appid):
        app = App(appid=appid,appsecret=str(uuid.uuid1()))
        db.session.add(app)
        db.session.commit()
        return app
    def generate_auth_token(self,expiration):
        s =  Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'appid':self.appid,'appsecret':self.appsecret})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return App.query.filter_by(appid=data['appid']).first()
