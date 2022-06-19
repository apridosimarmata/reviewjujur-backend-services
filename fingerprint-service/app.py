from src import fingerprint_pb2_grpc
from concurrent import futures
from models import FingerprintRPCServer
from config import config
import grpc

def serve_fingerprint_rpc():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        port = config.get('FINGERPRINT_PORT_GRPC')
        fingerprint_pb2_grpc.add_FingerprintServiceServicer_to_server(
            FingerprintRPCServer(), server
        )
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"FINGERPRINT GRPC Running on {port}")
        server.wait_for_termination()
        

if __name__ == "__main__":
    serve_fingerprint_rpc()