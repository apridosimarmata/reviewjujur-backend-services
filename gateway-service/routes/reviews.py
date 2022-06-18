from flask import Blueprint, request
import os
from utils.request import *
from utils.auth import access_token_required
from auth import authorization as auth

url = 'http://'  + os.environ.get('REVIEW_HOST') + ':' + os.environ.get('REVIEW_PORT_REST')

prefix = 'reviews'

review = Blueprint(prefix, __name__)

def get_url(request):
    return url + remove_prefix(request.full_path, prefix)

@review.route('', methods = ['POST'])
@access_token_required
def create():
    user = auth.AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    request.json['userUid'] = user.get('uuid')
    return post_data(get_url(request) , request.json)