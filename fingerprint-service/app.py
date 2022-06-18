from flask import Flask

from src.database import session

from src.fingerprint_pb2 import Fingerprint, Empty
from src import fingerprint_pb2_grpc
from concurrent import futures
import grpc, logging, uuid
from machine_learning import model

class FingerprintRPCServer(fingerprint_pb2_grpc.FingerprintServiceServicer):
    def InsertNewFingerprint(self, request, context):
        insert_fingerprint_query = (
            "INSERT INTO fingerprints "
            "(uid, phone_id, external_storage_capacity, input_methods, kernel_name, location_providers, is_password_shown, ringtone, available_ringtones, screen_timeout, wallpaper, wifi_policy) "
            "VALUES ("
            f"'{str(uuid.uuid4())}', "
            f"'{request.phone_id}', "
            f"'{str(request.external_storage_capacity)}', "
            f"'{request.input_methods}', "
            f"'{request.kernel_name}', "
            f"'{request.location_providers}', "
            f"'{str(request.is_password_shown)}', "
            f"'{request.ringtone}', "
            f"'{request.available_ringtones}', "
            f"'{str(request.screen_timeout)}', "
            f"'{request.wallpaper}', "
            f"'{str(request.wifi_policy)}')")
        session.execute(insert_fingerprint_query)
        model.predict(request)
        return Empty()


app = Flask(__name__)
  
@app.route('/')
def hello_world():
    return 'Hello World'
  
def serve_fingerprint_rpc():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        port = 6006
        fingerprint_pb2_grpc.add_FingerprintServiceServicer_to_server(
            FingerprintRPCServer(), server
        )
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(server)
        server.wait_for_termination()

app.run(host = '0.0.0.0', port = 5004)
serve_fingerprint_rpc()
logging.basicConfig()