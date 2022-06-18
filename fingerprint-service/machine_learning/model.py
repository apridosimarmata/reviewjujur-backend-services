from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from .functions import *

import math

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

phone_ids = session.execute('SELECT phone_id FROM fingerprints')
phone_ids_unique = set()

for value in phone_ids:
    phone_ids_unique.add(value.get('phone_id'))

phone_fingerprints = {}

def predict(unknown_fingerprint):
    fingerprints = session.execute('SELECT * FROM fingerprints')
    phone_fingerprints = {}
    for fingerprint in fingerprints:
        try:
            phone_fingerprints[fingerprint.get('phone_id')].append(fingerprint)
        except:
            phone_fingerprints[fingerprint.get('phone_id')] = [fingerprint]

    max_similarity = 0
    phone_identified = None
    probs = None
    for phone in phone_fingerprints.keys():
        probabilities = []
        # List type

        # Available ringtones [1]
        probabilities.append(jaccard_index(set(unknown_fingerprint.available_ringtones.split(',')), set(phone_fingerprints[phone][-1].get('available_ringtones').split(','))))

        # String type

        # Wallpaper [2]
        if unknown_fingerprint.wallpaper == phone_fingerprints[phone][-1].get('wallpaper'):
            probabilities.append(number_string_extract_probabilities('wallpaper', phone_fingerprints[phone]).get('unchanged_probability_in_phone'))
        else:
            probabilities.append(number_string_extract_probabilities('wallpaper', phone_fingerprints[phone]).get('changed_probability_in_phone'))
        
        # Kernel [3]
        if unknown_fingerprint.kernel_name == phone_fingerprints[phone][-1].get('kernel_name'):
            probabilities.append(number_string_extract_probabilities('kernel_name', phone_fingerprints[phone]).get('unchanged_probability_in_phone'))
        else:
            probabilities.append(number_string_extract_probabilities('kernel_name', phone_fingerprints[phone]).get('changed_probability_in_phone'))
        
        # Input methods [4]
        if unknown_fingerprint.input_methods == phone_fingerprints[phone][-1].get('input_methods'):
            probabilities.append(number_string_extract_probabilities('input_methods', phone_fingerprints[phone]).get('unchanged_probability_in_phone'))
        else:
            probabilities.append(number_string_extract_probabilities('input_methods', phone_fingerprints[phone]).get('changed_probability_in_phone'))
        
        # Ringtone [5]
        if unknown_fingerprint.ringtone == phone_fingerprints[phone][-1].get('ringtone'):
            probabilities.append(number_string_extract_probabilities('ringtone', phone_fingerprints[phone]).get('unchanged_probability_in_phone'))
        else:
            probabilities.append(number_string_extract_probabilities('ringtone', phone_fingerprints[phone]).get('changed_probability_in_phone'))
        
        # Number / Int

        # Screen time out [6]
        if str(unknown_fingerprint.screen_timeout) == phone_fingerprints[phone][-1].get('screen_timeout'):
            probabilities.append(number_string_extract_probabilities('external_storage_capacity', phone_fingerprints[phone]).get('unchanged_probability_in_phone'))
        else:
            probabilities.append(number_string_extract_probabilities('external_storage_capacity', phone_fingerprints[phone]).get('changed_probability_in_phone'))
        
        # External storage [7]
        if str(unknown_fingerprint.external_storage_capacity) == phone_fingerprints[phone][-1].get('external_storage_capacity'):
            probabilities.append(number_string_extract_probabilities('external_storage_capacity', phone_fingerprints[phone]).get('unchanged_probability_in_phone'))
        else:
            probabilities.append(number_string_extract_probabilities('external_storage_capacity', phone_fingerprints[phone]).get('changed_probability_in_phone'))
        
        # Enumerate data type

        # Is Password Shown [8]
        probabilities.append(enumerate_probability('is_password_shown', phone_fingerprints[phone], str(unknown_fingerprint.is_password_shown)))
        
        # Location Providers [9]
        probabilities.append(enumerate_probability('location_providers', phone_fingerprints[phone], unknown_fingerprint.location_providers))

        # Wifi Policy
        probabilities.append(enumerate_probability('wifi_policy', phone_fingerprints[phone], str(unknown_fingerprint.wifi_policy)))

        similarity = math.fsum(probabilities) / len(probabilities)
        if similarity > .6:
            #print(f"{probabilities} -> {similarity}")
            pass

        if phone == '4714e6b76c4138b4':
            print(probabilities)

        if max_similarity < similarity and .8 < similarity:
            max_similarity = similarity
            phone_identified = phone
            probs = probabilities

    print(f"identified as {phone_identified} == {unknown_fingerprint.phone_id} with similarity {max_similarity} -> {probs}")
    if phone_identified == unknown_fingerprint.phone_id:
        print("correct!")