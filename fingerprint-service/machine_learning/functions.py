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

def number_string_extract_probabilities(column_name, phone_fingerprints):
    phone_events = len(phone_fingerprints) - 1
    changed_event_in_phone = 0
    
    for index, fingerprint in enumerate(phone_fingerprints):
        if index > 0 and fingerprint.get(column_name) != phone_fingerprints[index - 1].get(column_name):
                changed_event_in_phone += 1
    
    changed_probability_in_phone = 1

    if phone_events > 0:
        changed_probability_in_phone = changed_event_in_phone / phone_events

    return {'changed_probability_in_phone' : changed_probability_in_phone, 'unchanged_probability_in_phone' : 1 - changed_probability_in_phone}

def enumerate_probability(column_name, phone_fingerprints, value):
    count = 0
    for fingerprint in phone_fingerprints:
        if fingerprint.get(column_name) == value:
            count += 1
    
    count += 1

    return count / (len(phone_fingerprints) + 1)