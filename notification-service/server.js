const whatsapp = require('./whatsapp');
const user = require('./user')

const grpc = require("@grpc/grpc-js");
const PROTO_PATH = "notifications.proto";
var protoLoader = require("@grpc/proto-loader");

const options = {
  longs: String,
  oneofs: true,
  keepCase: true,
  enums: String,
  defaults: true,
};

var packageDefinition = protoLoader.loadSync(PROTO_PATH, options);
const notificationsProto = grpc.loadPackageDefinition(packageDefinition);

whatsapp.initializeWhatsappWeb()

const server = new grpc.Server()

server.addService(notificationsProto.NotificationService.service, {
  sendUserNoticationReviewRejected : (call, callback) => {

    user = user.getUserByUid(
        call.request.user_uid,
        (user) => {

          whatsapp.sendMessage(
            user.whatsappNo,
            call.request.reason + " Try again later, " + user.name
          )

          callback()
          }
        )
  },

  sendNotificationReviewAccepted : (call, callback) => {
    user = user.getUserByUid(
      call.request.user_uid,
      (user) => {

        whatsapp.sendMessage(
          user.whatsappNo,
          "Thank you, " + user.name + ". Your review has been published."
        )

        callback()
        }
      )
  },

  sendUserVerificationCode : (call, callback) => {
      whatsapp.sendMessage(
        call.request.whatsappNo,
        "*" + call.request.verificationCode + "* adalah kode verifikasi ReviewJujur Anda."
      )
      callback();
  },
})

server.bindAsync(
    "127.0.0.1:6005",
    grpc.ServerCredentials.createInsecure(),
    (error, port) => {
      console.log("Server running at http://127.0.0.1:6005");
      server.start();
    }
);