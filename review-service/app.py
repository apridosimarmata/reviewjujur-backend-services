import http
from flask import Flask, request
from src.fingerprint_pb2_grpc import FingerprintServiceStub
from src.fingerprint_pb2 import Fingerprint
import review
from models import ResponseModel, Review
import grpc

app = Flask(__name__)

channel = grpc.insecure_channel("localhost:6006", options=(('grpc.enable_http_proxy', 0),))

client = FingerprintServiceStub(channel)

@app.route('/', methods = ['POST'])
def create():
    request_data = request.json
    data = None
    try:
        data = Review(
            text = request_data.get('text'),
            score = request_data.get('score'),
            user_uid = request_data.get('userUid'),
            business_uid = request_data.get('businessUid')
            )
        return review.create(data).to_json()
    except Exception as e:
        return ResponseModel(F'{e}', http.HTTPStatus.BAD_REQUEST, None).to_json()

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5004)
