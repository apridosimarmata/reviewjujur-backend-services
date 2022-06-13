const grpc = require("@grpc/grpc-js");
const PROTO_PATH = "./src/fingerprint.proto";

var protoLoader = require("@grpc/proto-loader");

const options = {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
};

var packageDefinition = protoLoader.loadSync(PROTO_PATH, options);
const fingerprintProto = grpc.loadPackageDefinition(packageDefinition);

const grpcServer = new grpc.Server();

module.exports =  {
  grpcServer,
  fingerprintProto
}