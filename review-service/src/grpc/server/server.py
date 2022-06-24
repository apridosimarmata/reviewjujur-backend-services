from src.grpc.server.review_pb2_grpc import ReviewServiceServicer
from src.grpc.fingerprint_pb2 import Empty

from src import review

class ReviewService(ReviewServiceServicer):
    def FingerprintCallback(self, request, context):
        review.update(
            review_uid = request.review_uid,
            phone_id = request.phone_id
        )
        return Empty()
        