from distutils import ccompiler
import http
from re import S
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import uuid
from src.utils import now, one_week_ago
from src.models import ResponseModel
from src.services import notification
from config import config
from utils import to_camel_case

cluster = Cluster(['172.17.0.2'])
session = cluster.connect('review')
session.row_factory = dict_factory

statuses_key = {}

statuses = session.execute('SELECT * FROM status')

for status in statuses:
    print(status)
    statuses_key[status.get('status')] = status.get('id')

def create(review):
    review_uid = str(uuid.uuid4())
    now_timestamp = now()

    # Creating the actual review1655817789
    statement = session.prepare('INSERT INTO reviews(uid, business_uid, user_uid, text, score, status, status_updated_at, created_at) '
    'VALUES(?, ?, ?, ?, ?, ?, ?, ?)')

    try:
        session.execute(statement, [review_uid, review.business_uid, review.user_uid, review.text, review.score, statuses_key['PENDING'], now_timestamp, now_timestamp])
    except Exception as e:
        return ResponseModel(f'{e}', http.HTTPStatus.INTERNAL_SERVER_ERROR, None)
    
    # Create business reviews row
    statement = session.prepare('INSERT INTO business_reviews(business_uid, created_at, phone_uid, review_uid, score) VALUES (?, ?, ?, ?, ?)')

    try:
        session.execute(statement, [review.business_uid, now_timestamp, "", review_uid, review.score])
    except Exception as e:
        return ResponseModel(f'{e}', http.HTTPStatus.INTERNAL_SERVER_ERROR, None)
    
    # Create user reviews row
    statement = session.prepare('INSERT INTO user_reviews(user_uid, created_at, business_uid, review_uid) VALUES (?, ?, ?, ?)')

    try:
        session.execute(statement, [review.user_uid, now_timestamp, review.business_uid, review_uid])
    except Exception as e:
        return ResponseModel(f'{e}', http.HTTPStatus.INTERNAL_SERVER_ERROR, None)

    return ResponseModel('Success', http.HTTPStatus.OK, {'reviewUid' : review_uid})

def update(review_uid, phone_id):
    print("Received a callback from FINGERPRINT-SERVICE")
    statement = session.prepare('SELECT * FROM reviews where uid = ?')
    arg = [review_uid]
    current_review = session.execute(statement, arg)[0]

    one_week_ago_timestamp = one_week_ago()

    # Checking wether has made a review in past 7 days
    user_uid = current_review.get('user_uid')
    statement = session.prepare('SELECT * FROM user_reviews where user_uid = ? AND created_at > ?')

    args = [user_uid, one_week_ago_timestamp]
    reviews = session.execute(statement, args)

    user_business_review_count = 0

    '''for review in reviews:
        if review.get('business_uid') == current_review.get('business_uid'):
            if user_business_review_count >= 1:
                statement = session.prepare('UPDATE reviews set status = ? where uid = ?')
                args = [statuses_key['REJECTED'], review_uid]
                session.execute(statement, args)
                notification.send_user_notification_review_rejected(
                    user_uid = user_uid,
                    business_uid = current_review.get('business_uid'),
                    reason = config.get('REJECTED_TOO_FREQUENTLY')
                )
                return
            else:
                user_business_review_count += 1'''

    # Checking wether the phone has been used to create a review in past 7 days
    statement = session.prepare('SELECT * FROM business_reviews where business_uid = ? AND created_at > ?')
    args = [current_review.get('business_uid'), one_week_ago_timestamp]
    reviews = session.execute(statement, args)

    

    for review in reviews:
        if review.get('phone_uid') == phone_id:
            statement = session.prepare('UPDATE reviews set status = ? where uid = ?')
            args = [statuses_key['REJECTED'], review_uid]
            session.execute(statement, args)
            notification.send_user_notification_review_rejected(
                user_uid = user_uid,
                business_uid = current_review.get('business_uid'),
                reason = config.get('REJECTED_TOO_FREQUENTLY')
            )
            return

    
    # Review is valid, update the phone_id
    query = None

    query = f"UPDATE reviews set status = {statuses_key['ACCEPTED']}, status_updated_at = {now()} where uid = \'{current_review.get('uid')}\'"
    statement = session.prepare(query)
    session.execute(statement)

    query = f"UPDATE business_reviews set phone_uid = \'{str(phone_id)}\' where business_uid = \'{review.get('business_uid')}\' and created_at = {current_review.get('created_at')}"
    statement = session.prepare(query)
    session.execute(statement)

    
    notification.send_notification_review_accepted(
        user_uid = user_uid,
        business_uid = current_review.get('business_uid'),
    )

def get_business_reviews(business_uid, created_at):
    statement = None
    if created_at is None:
        statement = f'SELECT * FROM business_reviews where business_uid = \'{business_uid}\' ORDER BY created_at LIMIT 10'
    else:
        statement = f'SELECT * FROM business_reviews where business_uid = \'{business_uid}\' AND created_at > {created_at} ORDER BY created_at LIMIT 10'
    
    review_uids = []

    for review in session.execute(statement):
        if review.get('phone_uid') != '':
            review_uids.append(review.get('review_uid'))
        
    reviews = []

    for uid in review_uids:
        try:
            review = session.execute(f'SELECT * FROM reviews where uid = \'{uid}\'')[0]
            to_append = {}
            for key in review.keys():
                if type(review[key]) == int:
                    to_append[to_camel_case(key)] = str(review[key])
                else:
                    to_append[to_camel_case(key)] = review[key]
            reviews.append(to_append)
        except Exception as e:
            print(e)
            pass
    print(reviews)
    return ResponseModel(
            'Success',
            http.HTTPStatus.OK,
            reviews
        ).to_json()

def get_user_reviews(user_uid, created_at):
    statement = None
    if created_at is None:
        statement = f'SELECT * FROM user_reviews where user_uid = \'{user_uid}\' ORDER BY created_at LIMIT 10'
    else:
        statement = f'SELECT * FROM user_reviews where user_uid = \'{user_uid}\' AND created_at > {created_at} ORDER BY created_at LIMIT 10'

    review_uids = []

    for review in session.execute(statement):
        review_uids.append(review.get('review_uid'))
        
    reviews = []

    for uid in review_uids:
        try:
            review = session.execute(f'SELECT * FROM reviews where uid = \'{uid}\'')[0]
            to_append = {}
            for key in review.keys():
                if type(review[key]) == int:
                    to_append[to_camel_case(key)] = str(review[key])
                else:
                    to_append[to_camel_case(key)] = review[key]
            for key in statuses_key.keys():
                if statuses_key[key] == review.get('status'):
                    to_append['status'] = key
            reviews.append(to_append)
        except Exception as e:
            print(e)
            pass

    return ResponseModel(
            'Success',
            http.HTTPStatus.OK,
            reviews
        ).to_json()