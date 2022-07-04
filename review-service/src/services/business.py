import grpc
from src.grpc import business_pb2_grpc
from src.grpc.business_pb2 import ScoreUpdateRequest
from config import config

channel = grpc.insecure_channel(f"localhost:{config.get('BUSINESS_PORT_GRPC')}", options=(('grpc.enable_http_proxy', 0),))

client = business_pb2_grpc.BusinessServiceStub(channel)

def update_business_score(score, business_uid):
    client.UpdateBusinessScore(ScoreUpdateRequest(
        score = score,
        business_uid = business_uid
    ))
