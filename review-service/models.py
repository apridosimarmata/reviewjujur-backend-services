from dataclasses import dataclass
import http
from multiprocessing.sharedctypes import Value
import uuid
from flask import jsonify

class ResponseModel:
    def __init__(self, message, status_code, result):
        self.meta = {
        'code' : status_code,
        'message' : message
        }

        self.response = {
            'meta' : self.meta,
            'result' : result
        }

    def to_json(self):
        return jsonify(
            self.response
         ), 200, {'Content-Type': 'application/json'}

@dataclass
class Review:
    text: str
    business_uid: str
    user_uid: str
    score: int

    def __post_init__(self):
        if self.score is None or type(self.score) != int or self.score < 1 or self.score > 5 :
            raise ValueError('Score must be between 1 to 5')
        
        if self.text is None or len(self.text) < 20 or len(self.text) > 100:
            raise ValueError('Review text must be at least 20 chars and 100 chars maximum')
        
        if self.business_uid is None:
            raise ValueError('Business UID is missing')
        else:
            try:
                uuid.UUID(self.business_uid)
            except:
                raise ValueError('Business UID is invalid')
        
        if self.user_uid is None:
            raise ValueError('User UID is missing')
        else:
            try:
                uuid.UUID(self.user_uid)
            except:
                raise ValueError('Business UID is invalid')
        



    