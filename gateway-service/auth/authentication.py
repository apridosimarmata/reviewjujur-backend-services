import http
import jwt, json
from flask import jsonify
from routes.user import url as user_url
from utils import request as req
from .models import AuthenticationResponse, AdministratorAuthenticationResponse


def create_authentication_response(user):
    resp = AuthenticationResponse(user)
    return resp.as_dict()

def create_admin_authentication_response(whatsapp_no):
    resp = AdministratorAuthenticationResponse(whatsapp_no)
    return resp.as_dict()

def by_email(request):
    result = req.post_data(user_url + '/authentication/password', request.json)
    if json.loads(result[0]).get('meta').get('code') == 200:
        if json.loads(result[0]).get('result').get('verifiedAt') is None:
            return req.make_response(http.HTTPStatus.FORBIDDEN, "Verifikasi nomor WhatsApp diperlukan", None)
        return req.make_response(http.HTTPStatus.OK, "Berhasil masuk", create_authentication_response(json.loads(result[0]).get('result')))
    print("ss")
    return result

def by_phone(request):
    result = req.post_data(user_url + '/authentication/whatsapp?' + request.query_string.decode('utf-8') , request.json)
    if json.loads(result[0]).get('meta').get('code') == 200:
        if json.loads(result[0]).get('result').get('verifiedAt') is None:
            return req.make_response(http.HTTPStatus.FORBIDDEN, "Verifikasi nomor WhatsApp diperlukan", None)
        return req.make_response(http.HTTPStatus.OK, "Berhasil masuk", create_authentication_response(json.loads(result[0]).get('result')))
    return result

def request_code(whatsapp_no):
    return req.get_data(user_url + '/verification/whatsapp/' + whatsapp_no)

def admin_request_code(whatsapp_no):
    return req.get_data(user_url + '/administrator/verification/whatsapp/' + whatsapp_no)

def admin_by_phone(request):
    result = req.post_data(user_url + '/administrator/authentication/whatsapp' , request.json)
    if json.loads(result[0]).get('meta').get('code') == 200:
        return req.make_response(http.HTTPStatus.OK, "Berhasil masuk", create_admin_authentication_response(request.json.get('whatsappNo')))
    return result
