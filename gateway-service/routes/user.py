from crypt import methods
from flask import Blueprint, request
import os
from utils.request import *
from utils.auth import access_token_required
from auth import authorization as auth

url = 'http://'  + os.environ.get('USER_HOST') + ':' + os.environ.get('USER_PORT_REST')

prefix = 'users'

user = Blueprint(prefix, __name__)

def get_url(request):
    return url + remove_prefix(request.full_path, prefix)

@user.route('', methods = ['POST'])
def register():
    return post_data(get_url(request) , request.json)

@user.route('/verification/whatsapp', methods = ['POST'])
def verify_whatsapp_number():
    return post_data(get_url(request) , request.json)

@user.route('/name', methods = ['PATCH'])
@access_token_required
def update_name():
    user = auth.AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    request.json['email'] = user.get('email')
    return patch_data(get_url(request), request.json)

@user.route('/password', methods = ['PATCH'])
@access_token_required
def update_password():
    user = auth.AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    request.json['email'] = user.get('email')
    print(request.json)
    return patch_data(get_url(request), request.json)
