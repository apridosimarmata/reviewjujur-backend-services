import uuid
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from src import review_pb2_grpc, review_pb2
import grpc, constants
from config import config

from utils import *

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

column_names = [
    'phone_id',
    'available_ringtones',
    'external_storage_capacity',
    'input_methods',
    'is_password_shown',
    'kernel_name',
    'location_providers',
    'ringtone',
    'screen_timeout',
    'wallpaper',
    'wifi_policy'
]

def jaccard_index(set1, set2):
    intersection = set1 & set2
    union = set1.union(set2)
    jaccard_index = max(len(intersection), 1) / max(len(union), 1)
    return jaccard_index

def number_string_extract_probabilities(column_name, phone_fingerprints, event_type):
    # Adding current event, last fingerprint vs unknown fingerprint
    phone_events = 1

    changed_event = 0
    unchanged_event = 0

    # events for saved fingerprints, from one fingerprint to another.
    phone_events += len(phone_fingerprints) - 1

    if event_type == constants.UNCHANGED_EVENT:
        unchanged_event += 1
        for index, fingerprint in enumerate(phone_fingerprints):
            if index > 0 and fingerprint.get(column_name) == phone_fingerprints[index - 1].get(column_name):
                unchanged_event += 1

        # Returning probability of unchanged value
        return unchanged_event/phone_events
    else:
        changed_event += 1
        for index, fingerprint in enumerate(phone_fingerprints):
            if index > 0 and fingerprint.get(column_name) != phone_fingerprints[index - 1].get(column_name):
                changed_event += 1
        
        # Returning probability of changed value
        return changed_event/phone_events
import ast
def enumerate_probability(column_name, phone_fingerprints, value):
    if column_name == 'location_providers':
        values = value.split(",")
        prob = [1, 1]
        for fingerprint in phone_fingerprints:
            fingerprint_value = ast.literal_eval(fingerprint.get(column_name))
            if values[0] == fingerprint_value[0]:
                prob[0] += 1

            if values[1] == fingerprint_value[1]:
                prob[1] += 1
        return (prob[0] / (len(phone_fingerprints) + 1)) * (prob[1] / (len(phone_fingerprints) + 1))
    else:
        count = 0
        fingerprint_values = []
        for fingerprint in phone_fingerprints:
            for item in fingerprint.get(column_name).split(","):
                fingerprint_values.append(item)
        
        count += 1

        for item in fingerprint_values:
            if item == value:
                count += 1
        return count / (len(fingerprint_values) + 1)

def save_new_fingerprint(unknown_fingerprint):
    new_phone_id = str(uuid.uuid4())
    statement = session.prepare(
    'INSERT INTO fingerprints(uid, available_ringtones , external_storage_capacity, input_methods, is_password_shown , kernel_name, location_providers, phone_id, ringtone, screen_timeout , wallpaper, wifi_policy, created_at) '
    'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
    args = [
        str(uuid.uuid4()),
        unknown_fingerprint.available_ringtones,
        str(abs(unknown_fingerprint.external_storage_capacity)),
        unknown_fingerprint.input_methods,
        str(unknown_fingerprint.is_password_shown),
        unknown_fingerprint.kernel_name,
        unknown_fingerprint.location_providers,
        new_phone_id,
        unknown_fingerprint.ringtone,
        str(unknown_fingerprint.screen_timeout),
        unknown_fingerprint.wallpaper,
        str(unknown_fingerprint.wifi_policy),
        now()
    ]

    session.execute(statement, args)

    return new_phone_id

def save_new_fingerprint_of_known_device(phone_id, fingerprint):
    statement = session.prepare(
    'INSERT INTO fingerprints(uid, available_ringtones , external_storage_capacity, input_methods, is_password_shown , kernel_name, location_providers, phone_id, ringtone, screen_timeout , wallpaper, wifi_policy, created_at) '
    'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')

    args = [
        str(uuid.uuid4()),
        fingerprint.available_ringtones,
        str(abs(fingerprint.external_storage_capacity)),
        fingerprint.input_methods,
        str(fingerprint.is_password_shown),
        fingerprint.kernel_name,
        fingerprint.location_providers,
        phone_id,
        fingerprint.ringtone,
        str(fingerprint.screen_timeout),
        fingerprint.wallpaper,
        str(fingerprint.wifi_policy),
        now()
    ]

    session.execute(statement, args)
    print(f"saved with id {phone_id}")

    return

channel = grpc.insecure_channel(f"localhost:{config.get('REVIEW_PORT_GRPC')}", options=(('grpc.enable_http_proxy', 0),))

def send_fingerprint_callback(review_uid, phone_id):
    client = review_pb2_grpc.ReviewServiceStub(channel)
    client.FingerprintCallback(
        review_pb2.FingerprintCallbackRequest(
                review_uid = review_uid,
                phone_id = phone_id
            )
        )

def check_if_fingerprint_exist_in_phone_fingerprints(phone_fingerprints, fingerprint):
    for fingerprint in phone_fingerprints:
        for col in column_names:
            if fingerprint.get(col) != fingerprint.get(col):
                return  False
    return True