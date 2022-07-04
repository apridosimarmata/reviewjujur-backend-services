package Controllers

import (
	"net/http"
	"time"
	"user-service/Models"
	routeguides "user-service/Rpc/Client/RouteGuides"
	"user-service/Utils"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

var empty = Models.Empty{}

func Register(c *gin.Context) {
	var message string

	var userRequest Models.UserRequest
	err := c.BindJSON(&userRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	user := Models.User{UserRequest: userRequest}
	user.Uuid = uuid.New()
	user.CreatedAt = Utils.Now()
	user.Password, err = Utils.HashPassword(userRequest.Password)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	nowUnix := user.CreatedAt.Unix()

	user.CodeRequestedAt = &nowUnix
	user.UnsuspendAt = &nowUnix

	err = Models.Create(&user)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	message = "User created"

	routeguides.SendUserVerificationCode(user, Utils.GetOTP(nowUnix))

	Utils.MakeResponse(c, http.StatusOK, &message, nil)
}

func RequestVerificationCode(c *gin.Context) {
	var user Models.User
	whatsapNo := c.Params.ByName("whatsapp_no")

	var message string

	err := Models.GetByWhatsappNo(&user, whatsapNo)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	now := time.Now().Unix()

	user.CodeRequestedAt = &now

	err = Models.Update(&user)

	if err != nil {
		message := err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	err = routeguides.SendUserVerificationCode(user, Utils.GetOTP(*&now))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, user)
	}

	message = "Verification code sent"

	Utils.MakeResponse(c, http.StatusOK, &message, nil)
}

func VerifyVerificationCode(c *gin.Context) {
	var message string
	var user Models.User

	var verificationCodeRequest Models.UserVerificationCodeRequest
	err := c.BindJSON(&verificationCodeRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	err = Models.GetByWhatsappNo(&user, verificationCodeRequest.WhatsappNo)

	if err != nil {
		message := err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	if !Utils.ValidateOTP(verificationCodeRequest.VerificationCode, *user.CodeRequestedAt) {
		message = "Wrong code"
		Utils.MakeResponse(c, http.StatusUnauthorized, &message, nil)
		return
	}

	var userResponse Models.UserResponse
	userResponse.Uuid = user.Uuid.String()
	userResponse.Email = user.Email
	userResponse.WhatsappNo = user.WhatsappNo
	userResponse.Name = user.Name
	userResponse.VerifiedAt = user.VerifiedAt

	if c.Query("whatsAppVerification") != "" {

		if user.VerifiedAt != nil {
			message = "Already verified"
			Utils.MakeResponse(c, http.StatusOK, &message, userResponse)
			return
		}

		now := Utils.Now()
		user.VerifiedAt = &now
		err = Models.Update(&user)

		message = "Verified"
	}

	message = "Accepted"

	userResponse.VerifiedAt = user.VerifiedAt

	Utils.MakeResponse(c, http.StatusOK, &message, userResponse)
}

func VerifyPassword(c *gin.Context) {
	var message string
	var verifyPasswordRequest Models.UserVerifyPasswordRequest
	err := c.BindJSON(&verifyPasswordRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	var user Models.User

	err = Models.GetByEmail(&user, verifyPasswordRequest.Email)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	if !Utils.CheckPasswordHash(verifyPasswordRequest.Password, user.Password) {
		message = "Wrong password"
		Utils.MakeResponse(c, http.StatusUnauthorized, &message, nil)
		return
	}

	var userResponse Models.UserResponse

	userResponse.Uuid = user.Uuid.String()
	userResponse.Email = user.Email
	userResponse.WhatsappNo = user.WhatsappNo
	userResponse.Name = user.Name
	userResponse.VerifiedAt = user.VerifiedAt

	Utils.MakeResponse(c, http.StatusOK, nil, userResponse)
}

func UpdateName(c *gin.Context) {
	var user Models.User
	var userChangeNameRequest Models.UserChangeNameRequest
	var message string
	err := c.BindJSON(&userChangeNameRequest)
	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	err = Models.GetByEmail(&user, userChangeNameRequest.Email)

	if err != nil {
		message = "user not found"
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	user.Name = userChangeNameRequest.Name
	err = Models.Update(&user)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, nil)
		return
	}

	message = "Updated successfully"
	Utils.MakeResponse(c, http.StatusOK, &message, nil)
}

func UpdatePassword(c *gin.Context) {
	var user Models.User
	var userChangePasswordRequest Models.UserChangePasswordRequest
	var message string
	err := c.BindJSON(&userChangePasswordRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	err = Models.GetByEmail(&user, userChangePasswordRequest.Email)

	if err != nil {
		message = "User not found"
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	user.Password, err = Utils.HashPassword(userChangePasswordRequest.NewPassword)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	err = Models.Update(&user)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, nil)
		return
	}

	message = "Updated successfully"
	Utils.MakeResponse(c, http.StatusOK, &message, nil)
}
