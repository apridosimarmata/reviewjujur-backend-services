const grpc = require("@grpc/grpc-js");
var protoLoader = require("@grpc/proto-loader");
const PROTO_PATH = "user.proto";

const options = {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
  };
  
var packageDefinition = protoLoader.loadSync(PROTO_PATH, options);

const UserService  = grpc.loadPackageDefinition(packageDefinition).user.UserService;

const client = new UserService(
  "localhost:6001",
  grpc.credentials.createInsecure()
);

console.log(client)

module.exports = {
    async getUserByUid(userUid, callback){

        user = await client.GetUserByUid(
            {uid : userUid},
            (error, user) => {
                if(!error){
                    console.log(error)
                }
                callback(
                    {
                        'name' : user.name,
                        'whatsappNo' : user.whatsappNo
                    }
                )
            }
        )
    }
}