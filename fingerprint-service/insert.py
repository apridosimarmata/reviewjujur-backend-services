import csv, re
from http import client
from utils import *
import uuid
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

phone_uuids = {}

with open('fingerprints.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')

    for row in csv_reader:
        removelist = "."
        del row[len(row)-1]
        del row[0]
        ringtones = row[7].split(',')
        input_methods = row[2].split(',')

        ringtones_processed = []
        input_methods_processed = []
        location_providers_processed = []

        for location_provider in row[4].split(','):
            location_providers_processed.append(re.sub(r'[^\w'+removelist+']', '', location_provider))
        for ringtone in ringtones:
            ringtones_processed.append(re.sub(r'[^\w'+removelist+']', '', ringtone))

        for input_method in input_methods:
            input_methods_processed.append(re.sub(r'[^\w'+removelist+']', '', input_method))
    
        statement = session.prepare(
            'INSERT INTO fingerprints(uid, available_ringtones , external_storage_capacity, input_methods, is_password_shown ,kernel_name ,location_providers , phone_id ,ringtone ,screen_timeout ,wallpaper ,wifi_policy, created_at) '
        'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')

        if row[0] in phone_uuids.keys():
            pass
        else:
            phone_uuids[row[0]] = str(uuid.uuid4())

        args = [
            str(uuid.uuid4()),
            ",".join(ringtones_processed),
            str(abs(int(row[1]))),
            ",".join(input_methods_processed), # inputmethods
            row[5],
            row[3], # Kernel
            ",".join(location_providers_processed), # providers
            phone_uuids[row[0]],
            row[6],
            row[8],
            row[9],
            row[10],
            now()]
        session.execute(statement, args)
