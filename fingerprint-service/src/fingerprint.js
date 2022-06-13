var cassandra = require('cassandra-driver');
var uuid = require('uuid')

const client = new cassandra.Client({
    contactPoints: ['172.17.0.3'],
    localDataCenter: 'datacenter1',
    keyspace: 'fingerprint',
});

function insertFingerprint(params){
    const query = 'INSERT INTO fingerprints (uid, phone_id, external_storage_capacity, input_methods, kernel_name, location_providers, is_password_shown, ringtone, available_ringtones, screen_timeout, wallpaper, wifi_policy)\
                    VALUES(\''+ uuid.v4().toString() + '\',\''+ params.androidId + '\',\''+ params.externalStorageCapacity.toString() + '\',\''+ params.inputMethods + '\',\''+ params.kernelName + '\',\''+ params.locationProviders + '\',\''+ params.isPasswordShown.toString() + '\',\''+ params.ringtone + '\',\''+ params.availableRingtone + '\',\''+ params.screenTimeout.toString() + '\',\''+ params.wallpaper + '\',\''+ params.wifiPolicy.toString() + '\')';

    client.execute(query, [], function(err, result){
        if(err){
            console.log(err);
          }else{
            console.log(result);
          }
    })
}

module.exports = {
    insertFingerprint
}