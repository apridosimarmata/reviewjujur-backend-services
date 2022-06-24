import grpc
from src.grpc import notifications_pb2_grpc, notifications_pb2
from config import config

channel = grpc.insecure_channel(f"localhost:{config.get('NOTIFICATION_PORT_GRPC')}", options=(('grpc.enable_http_proxy', 0),))

client = notifications_pb2_grpc.NotificationServiceStub(channel)

def send_user_notification_review_rejected(user_uid, business_uid, reason):
    client.SendUserNoticationReviewRejected(
        notifications_pb2.ReviewNotificationRequest(
            user_uid = user_uid,
            business_uid = business_uid,
            reason = reason
        )
    )

def send_notification_review_accepted(user_uid, business_uid):
    client.SendNotificationReviewAccepted(
        notifications_pb2.ReviewNotificationRequest(
            user_uid = user_uid,
            business_uid = business_uid,
            reason = "-"
        )
    )

