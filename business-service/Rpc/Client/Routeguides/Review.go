package routeguides

import (
	review "business-service/Rpc/Client/Review"
	"context"
)

func GetBusinessRating(businessUid string) (rating *review.Rating, err error) {
	var businessRequest review.GetBusinessRatingRequest

	businessRequest.BusinessUid = businessUid

	res, err := review.DialReviewAPI(context.Background()).NotificationServiceClient.GetBusinessRating(context.Background(), &businessRequest)

	if err != nil {
		return nil, err
	}

	return res, nil
}
