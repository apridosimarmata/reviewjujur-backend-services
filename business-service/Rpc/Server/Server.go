package business

import (
	"business-service/Models"
	"context"
	"log"

	"github.com/google/uuid"
	uuidSatori "github.com/satori/go.uuid"
)

type Server struct {
}

func (s *Server) UpdateBusinessScore(ctx context.Context, request *ScoreUpdateRequest) (*Empty, error) {
	log.Printf("Receive message body from client: %s", request)
	var business Models.Business

	err := Models.GetBusinessByUid(&business, uuid.UUID(uuidSatori.FromStringOrNil(request.BusinessUid)))

	if err != nil {
		log.Printf(err.Error())
		return &Empty{}, err
	}

	business.TotalScore += int(request.Score)
	business.ReviewsCount += 1

	Models.Update(&business)

	return &Empty{}, nil
}
