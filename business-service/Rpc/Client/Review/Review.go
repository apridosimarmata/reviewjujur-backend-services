package review

import (
	"context"
	"fmt"
	"log"
	"sync"

	grpc "google.golang.org/grpc"
)

type dialReviewApi struct {
	NotificationServiceClient ReviewServiceClient
}

var initDefaultReviewAPI *dialReviewApi = nil
var onceDefaultReviewAPI sync.Once

func DialReviewAPI(context context.Context) *dialReviewApi {
	onceDefaultReviewAPI.Do(func() {
		conn, err := grpc.Dial("localhost:6005", grpc.WithInsecure())

		if err != nil {
			log.Println(fmt.Printf("did not connect: %s", err))
		}

		initDefaultReviewAPI = &dialReviewApi{
			NotificationServiceClient: NewReviewServiceClient(conn),
		}
	})

	return initDefaultReviewAPI
}
