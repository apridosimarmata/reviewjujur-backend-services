from src import fingerprint_pb2_grpc, fingerprint_pb2
from machine_learning import model

class FingerprintRPCServer(fingerprint_pb2_grpc.FingerprintServiceServicer):
    def Predict(self, request, context):
        model.predict(request)
        return fingerprint_pb2.Empty()