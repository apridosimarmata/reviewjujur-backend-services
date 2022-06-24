from flask import request, Flask
from config import config
from src.grpc import fingerprint_pb2
from src.models import Review, ResponseModel
from src.services import fingerprint
import src.review, http

app = Flask(__name__)

@app.route('/business', methods = ['GET'])
def get_by_business():
    business_uid = request.args.get('businessUid')
    created_at = request.args.get('createdAt')
    if business_uid != None:
        if created_at != None:
            return src.review.get_business_reviews(business_uid, int(created_at))
        else:
            return src.review.get_business_reviews(business_uid, None)
    return ResponseModel(
        'Business UID not provided',
        http.HTTPStatus.OK,
    ).to_json()

@app.route('/user/<user_uid>', methods = ['GET'])
def get_by_user(user_uid):
    created_at = request.args.get('createdAt')
    if user_uid != None:
        if created_at != None:
            return src.review.get_user_reviews(user_uid, int(created_at))
        else:
            return src.review.get_user_reviews(user_uid, None)
    return ResponseModel(
        'User UID not provided',
        http.HTTPStatus.OK,
    ).to_json()


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
        result = src.review.create(data).to_json()

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
        
        fingerprint.predict(phone_fingerprint)

        return result
    except Exception as e:
        print(f"Exception: {e}")
        return ResponseModel(F'{e}', http.HTTPStatus.BAD_REQUEST, None).to_json()