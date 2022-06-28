# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from src.grpc import fingerprint_pb2 as src_dot_grpc_dot_fingerprint__pb2
from src.grpc.server import review_pb2 as src_dot_grpc_dot_server_dot_review__pb2


class ReviewServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FingerprintCallback = channel.unary_unary(
                '/ReviewService/FingerprintCallback',
                request_serializer=src_dot_grpc_dot_server_dot_review__pb2.FingerprintCallbackRequest.SerializeToString,
                response_deserializer=src_dot_grpc_dot_fingerprint__pb2.Empty.FromString,
                )
        self.GetBusinessRating = channel.unary_unary(
                '/ReviewService/GetBusinessRating',
                request_serializer=src_dot_grpc_dot_server_dot_review__pb2.GetBusinessRatingRequest.SerializeToString,
                response_deserializer=src_dot_grpc_dot_server_dot_review__pb2.Rating.FromString,
                )


class ReviewServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FingerprintCallback(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBusinessRating(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReviewServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FingerprintCallback': grpc.unary_unary_rpc_method_handler(
                    servicer.FingerprintCallback,
                    request_deserializer=src_dot_grpc_dot_server_dot_review__pb2.FingerprintCallbackRequest.FromString,
                    response_serializer=src_dot_grpc_dot_fingerprint__pb2.Empty.SerializeToString,
            ),
            'GetBusinessRating': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBusinessRating,
                    request_deserializer=src_dot_grpc_dot_server_dot_review__pb2.GetBusinessRatingRequest.FromString,
                    response_serializer=src_dot_grpc_dot_server_dot_review__pb2.Rating.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ReviewService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReviewService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FingerprintCallback(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReviewService/FingerprintCallback',
            src_dot_grpc_dot_server_dot_review__pb2.FingerprintCallbackRequest.SerializeToString,
            src_dot_grpc_dot_fingerprint__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBusinessRating(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReviewService/GetBusinessRating',
            src_dot_grpc_dot_server_dot_review__pb2.GetBusinessRatingRequest.SerializeToString,
            src_dot_grpc_dot_server_dot_review__pb2.Rating.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
