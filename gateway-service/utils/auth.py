from functools import wraps
from flask import request, jsonify
from auth.authorization import create_authorization_response
from auth.models import AuthenticationResponse, AdministratorAuthenticationResponse
from .constants import JSON_CONTENT

def access_token_required(f):
    @wraps(f)
    def check_if_access_token_exist(*args, **kwargs):
        if request.headers.get('Access-Token') is None or request.headers.get('Access-Refresh-Token') is None:
            return jsonify({
                'meta' : {
                    'code' : 401,
                    'message' : 'Unauthorized'
                }
            }), 401, JSON_CONTENT
        else:
            user = AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
            if isinstance(user, int):
                return create_authorization_response(user)
        return f(*args, **kwargs)
    return check_if_access_token_exist

def admin_access_token_required(f):
    @wraps(f)
    def check_if_access_token_exist(*args, **kwargs):
        if request.headers.get('Access-Token') is None:
            return jsonify({
                'meta' : {
                    'code' : 401,
                    'message' : 'Unauthorized'
                }
            }), 401, JSON_CONTENT
        else:
            admin = AdministratorAuthenticationResponse.extract_user(request.headers.get('Access-Token'))
            if isinstance(admin, int):
                return create_authorization_response(admin)
        return f(*args, **kwargs)
    return check_if_access_token_exist