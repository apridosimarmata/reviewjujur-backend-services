from flask import Blueprint, request
import os
from utils.request import *
from utils.auth import access_token_required
from auth import authorization as auth

url = 'http://'  + os.environ.get('BUSINESS_HOST') + ':' + os.environ.get('BUSINESS_PORT_REST')

prefix = 'businesses'

business = Blueprint(prefix, __name__)

def get_url(request):
    return url + remove_prefix(request.full_path, prefix)

@business.route('', methods = ['POST'])
@access_token_required
def register():
    user = auth.AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    request.json['ownerUid'] = user.get('uuid')
    return post_data(get_url(request) , request.json)

@business.route('/user', methods = ['GET'])
@access_token_required
def get_by_user():
    user = auth.AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    request.path += "/" + user.get('uuid')
    return get_data(get_url(request))

@business.route('/provinces', methods = ['POST'])
@access_token_required
def add_province():
    return post_data(get_url(request), request.json)

@business.route('/provinces', methods = ['GET'])
def get_provinces():
    return get_data(get_url(request))

@business.route('/locations', methods = ['POST'])
@access_token_required
def add_location():
    return post_data(get_url(request), request.json)

@business.route('/locations/<province_uid>', methods = ['GET'])
def get_locations(province_uid):
    return get_data(get_url(request))

@business.route('/search', methods = ['GET'])
def search():
    return get_data(get_url(request))

@business.route('/<business_uid>', methods = ['GET'])
def get_business_by_uid(business_uid):
    return get_data(get_url(request))

