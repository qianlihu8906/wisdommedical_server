from flask import jsonify,request,g
from ..models import App
from . import api
from .errors import bad_request
from functools import wraps

def verify_token(token):
    app = App.verify_auth_token(token)
    return app

@api.route('/token')
def get_token():
    grant_type = request.args.get("grant_type")
    appid = request.args.get("appid")
    appsecret = request.args.get("appsecret")

    if grant_type == 'client_credential':
        if not appid or not appsecret:
            return bad_request(40001)
        app = App.query.filter_by(appid=appid).first()
        if not app:
            return bad_request(40001)
        if appsecret != app.appsecret:
            return bad_request(40001)
        token = app.generate_auth_token(1800)
        return jsonify({"access_token":token.decode('ascii'),'expires_in':1800})
    return bad_request(40009)

def verify_access_token(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
#        access_token = request.args.get('access_token')
#        android_app = verify_token(access_token)
#        if not android_app:
#            return bad_request(40002)
#        g.current_android_app = android_app
        return f(*args,**kwargs)
    return wrapper
