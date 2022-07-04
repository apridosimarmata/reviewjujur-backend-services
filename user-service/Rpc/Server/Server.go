package user

import (
	"context"
	"log"
	"user-service/Models"
)

type Server struct {
}

func (s *Server) GetUserByUid(ctx context.Context, user *UserByUidRequest) (*User, error) {
	log.Printf("Receive message body from client: %s", user.Uid)
	var userModel Models.User

	err := Models.GetByUid(&userModel, user.Uid)
	if err != nil {
		log.Printf(err.Error())
		return nil, err
	}

	var userResponse User
	userResponse.Email = userModel.Email
	userResponse.Name = userModel.Name
	userResponse.WhatsappNo = userModel.WhatsappNo
	userResponse.UnsuspendAt = int32(*userModel.UnsuspendAt)
	userResponse.Uid = userModel.Uuid.String()

	return &userResponse, nil
}
