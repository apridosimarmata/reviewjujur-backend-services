from flask import request, Flask
from config import config
from src import fingerprint_pb2_grpc, fingerprint_pb2
from models import Review, ResponseModel
import grpc, review, http

channel = grpc.insecure_channel(f"localhost:{config.get('FINGERPRINT_PORT_GRPC')}", options=(('grpc.enable_http_proxy', 0),))

client = fingerprint_pb2_grpc.FingerprintServiceStub(channel)

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def create():
    review_data = request.json
    fingerprint_data = review_data.get('fingerprint')

    data = None
    try:
        data = Review(
            text = review_data.get('text'),
            score = review_data.get('score'),
            user_uid = review_data.get('userUid'),
            business_uid = review_data.get('businessUid')
            )
        result = review.create(data).to_json()
        review_uid = result[0].json.get('result').get('reviewUid')

        phone_fingerprint = fingerprint_pb2.Fingerprint(
            review_uid = review_uid,
            external_storage_capacity = abs(fingerprint_data.get('sd_card_capacity')),
            input_methods = ",".join(fingerprint_data.get('input_methods')),
            kernel_name = fingerprint_data.get('kernel_information'),
            location_providers = ",".join(fingerprint_data.get('location_providers')),
            is_password_shown = int(fingerprint_data.get('password_is_shown')),
            ringtone = fingerprint_data.get('ringtone'),
            available_ringtones = ",".join(fingerprint_data.get('ringtone_list')),
            screen_timeout = fingerprint_data.get('screen_timeout'),
            wallpaper = fingerprint_data.get('wallpaper_info'),
            wifi_policy = int(fingerprint_data.get('wifi_sleeping_policy'))
        )        
        
        client.Predict(phone_fingerprint)

        return result
    except Exception as e:
        print(e)
        return ResponseModel(F'{e}', http.HTTPStatus.BAD_REQUEST, None).to_json()