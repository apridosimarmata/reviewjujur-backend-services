var cassandra = require('cassandra-driver');
const axios = require('axios')

const client = new cassandra.Client({
    contactPoints: ['172.17.0.3'],
    localDataCenter: 'datacenter1',
    keyspace: 'fingerpint',
});

function insertFingerprint(res ,params){
    const query = 'INSERT INTO fingerprints (uid, class, externalStorageCapacity, inputMethods, kernelName, locationProviders, isPasswordShown, ringtone, availableRingtone, screenTimeout, wallpaper, wifiPolicy)\
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
    const params = [uuidv4(), params.androidId, params.externalStorageCapacity, params.inputMethods, params.kernelName, params.locationProviders, params.isPasswordShown, params.ringtone, params.availableRingtone, params.screenTimeout, params.wallpaper, params.wifiPolicy]
    client.execute(query, params, function(err, result){
        if(err){
            console.log(err);
          }else{
            console.log(result);
            var rate = parseInt(req.body.place_score) + parseInt(req.body.treatment_score) + parseInt(req.body.product_score)
            
            axios.patch('https://umkm.sireto.id/api/v1/umkm/score', {business_id : req.body.business_id, score : rate/3})
              .then((res) => {
                  console.log(res);
              }).catch((err) => {
                  console.error(err);
              });

          }
    });
}