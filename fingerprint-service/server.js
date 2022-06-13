const fingerprint =  require('./src/fingerprint')
const fingerprintGrpc = require('./src/grpc')

const grpc = require("@grpc/grpc-js");

const grpcServer = fingerprintGrpc.grpcServer


grpcServer.addService(fingerprintGrpc.fingerprintProto.FingerprintService.service, {
    insertNewFingerprint: (params, callback) => {
        fingerprint.insertFingerprint(params.request)
        callback(null, null);
    },
});

grpcServer.bindAsync(
    "0.0.0.0:6001",
    grpc.ServerCredentials.createInsecure(),
    () => {
        console.log("GRPC -> Listening at 0.0.0.0:6001");
        grpcServer.start();
    }
);

