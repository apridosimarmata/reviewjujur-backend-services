from flask import Blueprint, request, make_response
import http
from utils.request import *
from auth import authentication, authorization
from utils.auth import admin_access_token_required

prefix = 'auth'

auth = Blueprint(prefix, __name__)

@auth.route('/authentication/email', methods = ['POST'])
def authenticate_by_email():
    return authentication.by_email(request)

@auth.route('/authentication/whatsapp', methods = ['POST'])
def authenticate_by_phone():
    return authentication.by_phone(request)

@auth.route('/authentication/whatsapp/<whatsapp_no>', methods = ['GET'])
def request_phone_authentication(whatsapp_no):
    return authentication.request_code(whatsapp_no)

@auth.route('/administrator/authentication/whatsapp', methods = ['POST'])
def authenticate_admin_by_phone():
    return authentication.admin_by_phone(request)

@auth.route('/administrator/authentication/whatsapp/<whatsapp_no>', methods = ['GET'])
def request_admin_phone_authentication(whatsapp_no):
    return authentication.admin_request_code(whatsapp_no)

@auth.route('/administrator/authorize', methods = ['GET'])
@admin_access_token_required
def authorize_administrator():
    return make_response(http.HTTPStatus.OK, 'Success', None)

from utils.auth import access_token_required, admin_access_token_required

@auth.route('/authorization', methods = ['GET'])
@access_token_required
def is_token_valid():
    return authorization.authorize(request)

@auth.route('/authorization/refresh')
def refresh_token():
    if request.headers.get('Access-Refresh-Token') is None:
        return make_response(http.HTTPStatus.UNAUTHORIZED, 'Access-Refresh-Token missing', None)
    return authorization.refresh_token(request.headers.get('Access-Refresh-Token'))
