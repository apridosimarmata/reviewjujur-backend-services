from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from functions import *

import math

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

chance_to_modify = [
    0,
    2,
    2,
    4,
    1,
    1,
    0,
    8,
    5,
    3,
    3,
    2
]

values = [
    [1],
    [],
    [],

]

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

phone_ids = session.execute('SELECT * FROM fingerprints')

phone_fingerprints = {}

for phone in phone_ids:
    try:
        phone_fingerprints[phone['phone_id']].append(phone)
    except:
        phone_fingerprints[phone['phone_id']] = [phone]

need_to_syntetic = []

for phone in phone_fingerprints.keys():
    if len(phone_fingerprints[phone]) < 2:
        need_to_syntetic.append(phone)


import random 

def syntetic_from(a_fingerprint):
    copy = a_fingerprint
    for idx, column in enumerate(column_names):
        if random.randrange(1,11) <= chance_to_modify[idx]:
            copy


def start_syntetic():
    for phone in need_to_syntetic:
        number_of_syntetic = random.randrange(2, 5)
        for randomize in range(0, number_of_syntetic):
            syntetic_from(phone_fingerprints[phone][-1])