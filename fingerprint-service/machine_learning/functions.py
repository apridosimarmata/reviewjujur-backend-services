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

def number_string_extract_probabilities(phone_id, column_name, phone_fingerprints):
    events = 0
    changed_event = 0
    
    for phone in phone_fingerprints.keys():
        events += len(phone_fingerprints[phone]) - 1
        for index, fingerprint in enumerate(phone_fingerprints[phone]):
            if index > 0 and fingerprint.get(column_name) != phone_fingerprints[phone][index - 1].get(column_name):
                changed_event += 1

    fingerprints_list = [fingerprint for each_phone_fingerprints in phone_fingerprints.values() for fingerprint in each_phone_fingerprints]
    probability_of_phone = len(phone_fingerprints[phone_id]) / len(fingerprints_list)
    return {
        'changed_probability' : changed_event/events,
        'unchanged_probability' : events-changed_event/events,
        'phone_probability' : probability_of_phone,
        'phone_probability_if_changed' : 0}
