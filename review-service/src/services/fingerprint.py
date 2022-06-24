import grpc
from src.grpc import fingerprint_pb2_grpc
from config import config

channel = grpc.insecure_channel(f"localhost:{config.get('FINGERPRINT_PORT_GRPC')}", options=(('grpc.enable_http_proxy', 0),))

client = fingerprint_pb2_grpc.FingerprintServiceStub(channel)

def predict(phone_fingerprint):
    client.Predict(phone_fingerprint)
