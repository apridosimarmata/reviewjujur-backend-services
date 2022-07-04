from utils.constants import EXPIRED_TOKEN, SIGNATURE_ERROR
from http import HTTPStatus
from utils.request import make_response
from .models import AuthenticationResponse, AdministratorAuthenticationResponse

def authorize(request):
    user = AuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    if user == EXPIRED_TOKEN:
        return refresh_token(request.headers.get('Access-Refresh-Token'))
    elif user == SIGNATURE_ERROR:
        return make_response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable', None)
    elif isinstance(user, dict):
        return make_response(HTTPStatus.OK, None, user)
    else:
        return make_response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Server: Unknown Error', None)

def authorize_admin(request):
    admin = AdministratorAuthenticationResponse.extract_user(request.headers.get('Access-Token'))
    if admin == EXPIRED_TOKEN:
        return make_response(HTTPStatus.GONE, 'Access Expired', None)
    elif admin == SIGNATURE_ERROR:
        return make_response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable', None)
    elif isinstance(admin, dict):
        return make_response(HTTPStatus.OK, None, admin)
    else:
        return make_response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Server: Unknown Error', None)

def refresh_token(refresh_token):
    user = AuthenticationResponse.extract_user(refresh_token)
    if user == EXPIRED_TOKEN:
        return make_response(HTTPStatus.GONE, 'Please Log-in again', None)
    elif user == SIGNATURE_ERROR:
        return make_response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable', None)
    elif isinstance(user, dict):
        return make_response(HTTPStatus.CREATED, None, AuthenticationResponse(user))
    else:
        return make_response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Server: Unknown Error', None)

def create_authorization_response(code):
    if code == EXPIRED_TOKEN:
        return make_response(HTTPStatus.GONE, 'Access Expired', None)
    else:
        return make_response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable', None)

