from src.grpc.server.review_pb2_grpc import add_ReviewServiceServicer_to_server
from src.grpc.server.server import ReviewService
from concurrent import futures
from config import config
from src.routes import app
import grpc, threading


def serve_fingerprint_rpc():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        port = config.get('REVIEW_PORT_GRPC')
        add_ReviewServiceServicer_to_server(
            ReviewService(), server
        )
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"REVIEW GRPC Running on {port}")
        server.wait_for_termination()

if __name__ == "__main__":
    grpc_thread = threading.Thread(target=serve_fingerprint_rpc)
    grpc_thread.start()
    app.run(host = '0.0.0.0', port = config.get('REVIEW_PORT_REST'))
    grpc_thread.join()
