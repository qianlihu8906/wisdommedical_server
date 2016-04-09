from flask import jsonify
from . import api

errmsg = {
                0:{"errcode":0,"errmsg":"success"},
                -1:{"errcode":-1,"errmsg":"system is busy"},
                40001:{"errcode":40001,"errmsg":"appid or appsecret hint"},
                40002:{"errcode":40002,"errmsg":"invalid access_token"},
                40003:{"errcode":40003,"errmsg":"family_name is registed"},
                40004:{"errcode":40004,"errmsg":"family_name is not existed"},
                40005:{"errcode":40005,"errmsg":"family_member is not existed"},
                40006:{"errcode":40006,"errmsg":"doctor_name is registed"},
                40007:{"errcode":40007,"errmsg":"doctor_name is not existed"},
                40008:{"errcode":40008,"errmsg":"invalid sensor type"},
                40009:{"errcode":40009,"errmsg":"invalid token method"},
                40010:{"errcode":40010,"errmsg":"miss necessary args"},
                40011:{"errcode":40011,"errmsg":"doctor and famliy not relationship"},
                40012:{"errcode":40012,"errmsg":"passwd and username not match"},
                40013:{"errcode":40013,"errmsg":"member is existed"},
                40014:{"errcode":40014,"errmsg":"already added"},
                40015:{"errcode":40015,"errmsg":"filename must be photo"},
   }

def bad_request(errcode):
    response = jsonify(errmsg[errcode])
    response.status_code = 200
    return response

