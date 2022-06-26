from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import csv, ast, re, uuid
from functions import *
from src.fingerprint_pb2 import Fingerprint
from model import predict


cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

session.execute('TRUNCATE fingerprints')

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
            for row in phones_and_its_fingerprints[phone_uid][len(phones_and_its_fingerprints[phone_uid]) - 1:]:
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
            
            test[phone_uid] = phones_and_its_fingerprints[phone_uid][len(phones_and_its_fingerprints[phone_uid]) - 1]
            #print(phone_uid, end = ' -')
            #print(test[phone_uid])
    
    correct = 0
    
    for key in test.keys():
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
        print(f"should be {key}")
        if predict(fingerprint) == key:
            correct += 1
        else:
            print(F"INCORRECT! {data[3]}")
    
    print(f'accuraccy { correct/len(list(test.keys())) * 100 }%')