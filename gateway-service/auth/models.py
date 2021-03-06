from dataclasses import dataclass, asdict
import jwt, time
from utils.constants import *

#secret_key = secrets.token_urlsafe(16)
secret_key = "AMNTAPAP"
@dataclass
class AuthenticationResponse:
    token: str
    refreshToken: str

    def __init__(self, user):
        self.token = jwt.encode({
            'uuid' : user.get('uuid'),
            'email' : user.get('email'),
            'whatsappNo' : user.get('whatsappNo'),
            'name' : user.get('name'),
            'exp' : time.time() + 900
            },
            secret_key,
            algorithm = "HS256"
        )
        self.refreshToken = jwt.encode({
            'uuid' : user.get('uuid'),
            'email' : user.get('email'),
            'whatsappNo' : user.get('whatsappNo'),
            'name' : user.get('name'),
            'exp' : time.time() + 2592000
            },
            secret_key,
            algorithm = "HS256"
        )

    def as_dict(self):
        return asdict(self)
    
    @staticmethod
    def extract_user(token):
        try:
            return jwt.decode(token, secret_key, algorithms = "HS256")
        except Exception as e:
            if isinstance(e, jwt.ExpiredSignatureError):
                return EXPIRED_TOKEN
            elif isinstance(e, jwt.InvalidSignatureError):
                return SIGNATURE_ERROR
            else:
                return UNKNOWN_ERROR

@dataclass
class AdministratorAuthenticationResponse:
    token: str
    
    def __init__(self, whatsapp_no):
        self.token = jwt.encode({
            'whatsappNo' : whatsapp_no,
            'role' : 'ADMINISTRATOR',
            'exp' : time.time() + 1800
            },
            secret_key,
            algorithm = "HS256"
        )

    def as_dict(self):
        return asdict(self)

    @staticmethod
    def extract_user(token):
        try:
            return jwt.decode(token, secret_key, algorithms = "HS256")
        except Exception as e:
            if isinstance(e, jwt.ExpiredSignatureError):
                return EXPIRED_TOKEN
            elif isinstance(e, jwt.InvalidSignatureError):
                return SIGNATURE_ERROR
            else:
                return UNKNOWN_ERROR