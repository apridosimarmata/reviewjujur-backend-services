from flask import Blueprint, request, make_response
from utils.request import *
from utils.auth import admin_access_token_required
import os

user_url = 'http://'  + os.environ.get('USER_HOST') + ':' + os.environ.get('USER_PORT_REST')
review_url = 'http://'  + os.environ.get('REVIEW_HOST') + ':' + os.environ.get('REVIEW_PORT_REST')

prefix = 'administrator'

administrator = Blueprint(prefix, __name__)

def get_url(url, request):
    return url + request.full_path

@administrator.route('/users', methods = ['GET'])
@admin_access_token_required
def administrator_get_users():
    return get_data(get_url(user_url, request))

@administrator.route('/users/<user_uid>', methods = ['GET'])
@admin_access_token_required
def administrator_get_user_by_uid(user_uid):
    return get_data(get_url(user_url, request))

@administrator.route('/users/suspend', methods = ['PATCH'])
@admin_access_token_required
def administrator_suspend_user_by_uid():
    return patch_data(get_url(user_url, request), request.json)

@administrator.route('/reviews/user/<user_uid>', methods = ['GET'])
@admin_access_token_required
def administrator_get_reviews_user_by_uid(user_uid):
    return get_data(get_url(review_url, request))