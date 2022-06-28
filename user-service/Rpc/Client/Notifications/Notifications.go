package notifications

import (
	"context"
	"fmt"
	"log"
	"sync"

	grpc "google.golang.org/grpc"
)

type dialNotificationsAPI struct {
	NotificationServiceClient NotificationServiceClient
}

var initDefaultNotificationsAPI *dialNotificationsAPI = nil
var onceDefaultNotificationsAPI sync.Once

func DialNotificationsAPI(context context.Context) *dialNotificationsAPI {
	onceDefaultNotificationsAPI.Do(func() {
		conn, err := grpc.Dial("localhost:6005", grpc.WithInsecure())

		if err != nil {
			log.Println(fmt.Printf("did not connect: %s", err))
		}

		initDefaultNotificationsAPI = &dialNotificationsAPI{
			NotificationServiceClient: NewNotificationServiceClient(conn),
		}
	})

	return initDefaultNotificationsAPI
}
