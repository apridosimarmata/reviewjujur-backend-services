# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/review.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from src import fingerprint_pb2 as src_dot_fingerprint__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10src/review.proto\x1a\x15src/fingerprint.proto\"B\n\x1a\x46ingerprintCallbackRequest\x12\x12\n\nreview_uid\x18\x01 \x01(\t\x12\x10\n\x08phone_id\x18\x02 \x01(\t2M\n\rReviewService\x12<\n\x13\x46ingerprintCallback\x12\x1b.FingerprintCallbackRequest\x1a\x06.Empty\"\x00\x62\x06proto3')



_FINGERPRINTCALLBACKREQUEST = DESCRIPTOR.message_types_by_name['FingerprintCallbackRequest']
FingerprintCallbackRequest = _reflection.GeneratedProtocolMessageType('FingerprintCallbackRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINGERPRINTCALLBACKREQUEST,
  '__module__' : 'src.review_pb2'
  # @@protoc_insertion_point(class_scope:FingerprintCallbackRequest)
  })
_sym_db.RegisterMessage(FingerprintCallbackRequest)

_REVIEWSERVICE = DESCRIPTOR.services_by_name['ReviewService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FINGERPRINTCALLBACKREQUEST._serialized_start=43
  _FINGERPRINTCALLBACKREQUEST._serialized_end=109
  _REVIEWSERVICE._serialized_start=111
  _REVIEWSERVICE._serialized_end=188
# @@protoc_insertion_point(module_scope)
