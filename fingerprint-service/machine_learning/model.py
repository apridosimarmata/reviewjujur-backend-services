from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from machine_learning.functions import *

from numpy import prod

import math, re, constants

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

phone_ids = session.execute('SELECT phone_id FROM fingerprints')
phone_ids_unique = set()

for value in phone_ids:
    phone_ids_unique.add(value.get('phone_id'))

phone_fingerprints = {}

def predict(unknown_fingerprint):#,expected_id):
    to_compare = {}

    remove = "."
    ringtones = unknown_fingerprint.available_ringtones.split(',')
    inputMethods = unknown_fingerprint.input_methods.split(',')
    locationProviders = unknown_fingerprint.location_providers.split(',')

    ringtones_processed = []
    input_methods_processed = []
    location_providers_processed = []

    for inputMethod in inputMethods:
        input_methods_processed.append(re.sub(r'[^\w'+remove+']', '',inputMethod))
    unknown_fingerprint.input_methods = ",".join(input_methods_processed)
    
    for ringtone in ringtones:
        ringtones_processed.append(ringtone.strip())
    unknown_fingerprint.available_ringtones = ",".join(ringtones_processed).strip()

    for locationProvider in locationProviders:
        location_providers_processed.append(re.sub(r'[^\w'+remove+']', '', locationProvider))
    unknown_fingerprint.location_providers = ",".join(location_providers_processed)

    fingerprints = session.execute('SELECT * FROM fingerprints')
    phone_fingerprints = {}
    for fingerprint in fingerprints:
        try:
            phone_fingerprints[fingerprint.get('phone_id')].append(fingerprint)
        except:
            phone_fingerprints[fingerprint.get('phone_id')] = [fingerprint]

    max_similarity = 0
    sum = 0
    phone_identified = None

    to_compare['wallpaper'] = unknown_fingerprint.wallpaper
    to_compare['kernel_name'] = unknown_fingerprint.kernel_name
    to_compare['input_methods'] = ",".join(input_methods_processed)
    to_compare['ringtone'] = unknown_fingerprint.ringtone
    to_compare['screen_timeout'] = str(unknown_fingerprint.screen_timeout)
    to_compare['external_storage_capacity'] = str(unknown_fingerprint.external_storage_capacity)
    to_compare['is_password_shown'] = str(unknown_fingerprint.is_password_shown)
    to_compare['location_providers'] = ",".join(location_providers_processed)
    to_compare['wifi_policy'] = str(unknown_fingerprint.wifi_policy)
    to_compare['available_ringtones'] = set(ringtones_processed)

    for phone in phone_fingerprints.keys():
        probabilities = []
        # List type

        # Available ringtones [1]
        probabilities.append(jaccard_index(to_compare['available_ringtones'], set(phone_fingerprints[phone][-1].get('available_ringtones').split(','))))

        # String type

        # Wallpaper [2]
        if to_compare['wallpaper'] == phone_fingerprints[phone][-1].get('wallpaper'):
            probabilities.append(number_string_extract_probabilities('wallpaper', phone_fingerprints[phone], constants.UNCHANGED_EVENT))
        else:
            probabilities.append(number_string_extract_probabilities('wallpaper', phone_fingerprints[phone], constants.CHANGED_EVENT))
        
        # Kernel [3]
        if to_compare['kernel_name'] == phone_fingerprints[phone][-1].get('kernel_name'):
            probabilities.append(number_string_extract_probabilities('kernel_name', phone_fingerprints[phone], constants.UNCHANGED_EVENT))
        else:
            probabilities.append(number_string_extract_probabilities('kernel_name', phone_fingerprints[phone], constants.CHANGED_EVENT))
        
        # Input methods [4]
        if to_compare['input_methods'] == phone_fingerprints[phone][-1].get('input_methods'):
            probabilities.append(number_string_extract_probabilities('input_methods', phone_fingerprints[phone], constants.UNCHANGED_EVENT))
        else:
            probabilities.append(number_string_extract_probabilities('input_methods', phone_fingerprints[phone], constants.CHANGED_EVENT))
        
        # Ringtone [5]
        if to_compare['ringtone'] == phone_fingerprints[phone][-1].get('ringtone'):
            probabilities.append(number_string_extract_probabilities('ringtone', phone_fingerprints[phone], constants.UNCHANGED_EVENT))
        else:
            probabilities.append(number_string_extract_probabilities('ringtone', phone_fingerprints[phone], constants.CHANGED_EVENT))
        
        # Number / Int

        # Screen time out [6]
        if to_compare['screen_timeout'] == phone_fingerprints[phone][-1].get('screen_timeout'):
            probabilities.append(number_string_extract_probabilities('screen_timeout', phone_fingerprints[phone], constants.UNCHANGED_EVENT))
        else:
            probabilities.append(number_string_extract_probabilities('screen_timeout', phone_fingerprints[phone], constants.CHANGED_EVENT))
        
        # External storage [7]
        if to_compare['external_storage_capacity'] == phone_fingerprints[phone][-1].get('external_storage_capacity'):
            probabilities.append(number_string_extract_probabilities('external_storage_capacity', phone_fingerprints[phone], constants.UNCHANGED_EVENT))
        else:
            probabilities.append(number_string_extract_probabilities('external_storage_capacity', phone_fingerprints[phone], constants.CHANGED_EVENT))
        
        # Enumerate data type

        # Is Password Shown [8]
        probabilities.append(enumerate_probability('is_password_shown', phone_fingerprints[phone], to_compare['is_password_shown']))
        
        # Location Providers [9]
        probabilities.append(enumerate_probability('location_providers', phone_fingerprints[phone], to_compare['location_providers']))

        # Wifi Policy
        probabilities.append(enumerate_probability('wifi_policy', phone_fingerprints[phone], to_compare['wifi_policy']))

        similarity = prod(probabilities)

        sum += similarity

        if max_similarity < similarity and similarity >= 0.0:
            print(f'{probabilities} {similarity} -> {phone} {phone_fingerprints[phone][0].get("kernel_name")}')
            max_similarity = similarity
            phone_identified = phone
    
    # If it's a new device
    if phone_identified is None:
        print("New device, saving fingerprint")
        phone_identified = save_new_fingerprint(unknown_fingerprint)
    
    # If the device known but the fingerprint is new
    # Check the submitted fingerprint to each fingerprint in fingerprints of identified phone
    if phone_identified != None and not check_if_fingerprint_exist_in_phone_fingerprints(phone_fingerprints[phone_identified], to_compare):
        print("Known device, new fingerprint. Saving ...")
        save_new_fingerprint_of_known_device(phone_identified, unknown_fingerprint)

    #print(f"Sending callback to the REVIEW-SERVICE {phone_identified}")

    send_fingerprint_callback(
        review_uid = unknown_fingerprint.review_uid,
        phone_id = phone_identified)
    
    return phone_identified
