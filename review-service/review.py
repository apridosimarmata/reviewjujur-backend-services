import http
from cassandra.cluster import Cluster
from cassandra.query import dict_factory, tuple_factory
import uuid
from utils import now
from models import ResponseModel

cluster = Cluster(['172.17.0.2'])
session = cluster.connect('review')
session.row_factory = tuple_factory

def create(review):
    review_uid = str(uuid.uuid4())

    # Creating the actual review
    statement = session.prepare('INSERT INTO reviews(uid, business_uid, user_uid, text, score, status, status_updated_at, created_at) '
    'VALUES(?, ?, ?, ?, ?, ?, ?, ?)')

    try:
        session.execute(statement, [review_uid, review.business_uid, review.user_uid, review.text, review.score, 1, now(), now()])
    except Exception as e:
        return ResponseModel(f'{e}', http.HTTPStatus.INTERNAL_SERVER_ERROR, None)
    
    # Create business reviews row
    statement = session.prepare('INSERT INTO business_reviews(business_uid, review_uid) VALUES (?, ?)')

    try:
        session.execute(statement, [review.business_uid, review_uid])
    except Exception as e:
        return ResponseModel(f'{e}', http.HTTPStatus.INTERNAL_SERVER_ERROR, None)
    
    # Creaate user reviews row
    statement = session.prepare('INSERT INTO user_reviews(user_uid, review_uid) VALUES (?, ?)')

    try:
        session.execute(statement, [review.user_uid, review_uid])
    except Exception as e:
        return ResponseModel(f'{e}', http.HTTPStatus.INTERNAL_SERVER_ERROR, None)

    return ResponseModel('Success', http.HTTPStatus.OK, {'reviewUid' : review_uid})

def update():
    pass