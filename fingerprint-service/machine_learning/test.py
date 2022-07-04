import sys
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import csv, ast, re, uuid
from functions import *
from src.fingerprint_pb2 import Fingerprint
from numpy import prod


cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint_test')
session.row_factory = dict_factory

session.execute('TRUNCATE fingerprints')


def predict(unknown_fingerprint, expected_id):
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
    

    fingerprints = session.execute(f'SELECT * FROM fingerprints')

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

    max_probs = []

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

        if phone == expected_id or (expected_id[5:] == phone):
            print(f'\nEXPECTED\n{expected_id}\n{probabilities} {similarity} -> {phone} {phone_fingerprints[phone][0].get("kernel_name")}')

        if max_similarity < similarity and similarity >= .2:
            #print(f'{probabilities} {similarity} -> {phone} {phone_fingerprints[phone][0].get("kernel_name")}')
            max_similarity = similarity
            phone_identified = phone
            max_probs = probabilities
    
    if phone_identified != None:
        print(f'PREDICTED\n{phone_identified}\n{max_probs} {max_similarity} -> {phone_identified} {phone_fingerprints[phone_identified][0].get("kernel_name")}')
    
    return phone_identified

phone_uuids = {}

phones_and_its_fingerprints = {}

with open('ordered_fingerprints.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')

    for row in csv_reader:
        removelist = "."

        ringtones = row[7].split(',')
        input_methods = row[2].split(',')

        ringtones_processed = []
        input_methods_processed = []
        location_providers_processed = []

        for location_provider in row[4].split(','):
            l = location_provider.strip()
            location_providers_processed.append(l)

        for ringtone in ast.literal_eval(row[7]):
            r = ringtone.strip()
            ringtones_processed.append(r)

        for input_method in input_methods:
            i = input_method
            input_methods_processed.append(i.strip())

        if row[0] in phone_uuids.keys():
            pass
        else:
            phone_uuids[row[0]] = str(uuid.uuid4())
            phones_and_its_fingerprints[phone_uuids[row[0]]] = []

        #print(input_methods_processed)
        phone_uid = phone_uuids[row[0]]
        row[7] = ringtones_processed
        row[2] = input_methods_processed
        row[4] = location_providers_processed

        phones_and_its_fingerprints[phone_uid].append(row)

    test = {}

    for phone_uid in phones_and_its_fingerprints.keys():
        if len(phones_and_its_fingerprints[phone_uid]) > 1:
            rows = phones_and_its_fingerprints[phone_uid][:len(phones_and_its_fingerprints[phone_uid]) - 1]
            if len(phones_and_its_fingerprints[phone_uid]) == 1:
                rows = phones_and_its_fingerprints[phone_uid]
            else:
                test[phone_uid] = phones_and_its_fingerprints[phone_uid][len(phones_and_its_fingerprints[phone_uid]) - 1]
            for row in rows:
                args = [
                    str(uuid.uuid4()),
                    ",".join(row[7]).strip(),
                    str(abs(int(row[1]))),
                    ",".join(row[2]).strip(), # inputmethods
                    row[5],
                    row[3], # Kernel
                    ",".join(row[4]).strip(), # providers
                    phone_uid,
                    row[6],
                    row[8],
                    row[9],
                    row[10],
                    now()]

                statement = session.prepare(
                        'INSERT INTO fingerprints(uid, available_ringtones , external_storage_capacity, input_methods, is_password_shown ,kernel_name ,location_providers , phone_id ,ringtone ,screen_timeout ,wallpaper ,wifi_policy, created_at) '
                    'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
                session.execute(statement, args)
            
        else:
            test['test_' + phone_uid] = phones_and_its_fingerprints[phone_uid][0]

    
    correct = 0
    
    for idx, key in enumerate(list(test.keys())):
        
        print(idx+1)
        data = test[key]
        fingerprint = Fingerprint(
            review_uid = "",
            external_storage_capacity = abs(int(data[1])),
            input_methods = ",".join(data[2]),
            kernel_name = data[3],
            location_providers = ",".join(data[4]),
            is_password_shown = int(data[5]),
            ringtone = data[6],
            available_ringtones = ",".join(data[7]),
            screen_timeout = int(data[8]),
            wallpaper = data[9],
            wifi_policy = int(data[10])
        )
        res = predict(fingerprint, key)
        if res == key or (key[:4] == "test" and res is None):
            correct += 1
        else:
            print(F"\nINCORRECT! {data[3]}")
        print("\n\n\n")
    print(f'accuraccy { correct/len(list(test.keys())) * 100 }% from {len(list(test.keys()))}')
