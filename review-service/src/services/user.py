import grpc
from src.grpc import user_pb2_grpc
from src.grpc.user_pb2 import UserByUidRequest
from config import config

channel = grpc.insecure_channel(f"localhost:{config.get('USER_PORT_GRPC')}", options=(('grpc.enable_http_proxy', 0),))

client = user_pb2_grpc.UserServiceStub(channel)

def get_user_by_uid(user_uid):
    return client.GetUserByUid(UserByUidRequest(
        uid = user_uid
    ))
