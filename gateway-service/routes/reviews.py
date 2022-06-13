from flask import Blueprint, jsonify, request, make_response
import requests, os
from utils.request import *
from utils.auth import access_token_required
from auth import authorization as auth

url = 'http://'  + os.environ.get('REVIEW_HOST') + ':' + os.environ.get('REVIEW_PORT_REST')

prefix = 'reviews'

review = Blueprint(prefix, __name__)

def get_url(request):
    return url + remove_prefix(request.full_path, prefix)

@user.route('', methods = ['POST'])
def register():
    return post_data(get_url(request) , request.json)