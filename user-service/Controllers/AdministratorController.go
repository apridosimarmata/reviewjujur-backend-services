package Controllers

import (
	"net/http"
	"strconv"
	"time"
	"user-service/Models"
	routeguides "user-service/Rpc/Client/RouteGuides"
	"user-service/Utils"

	"github.com/gin-gonic/gin"
)

func AdministratorVerifyVerificationCode(c *gin.Context) {
	var message string
	var administrator Models.Administrator

	var verificationCodeRequest Models.AdministratorVerificationCodeRequest
	err := c.BindJSON(&verificationCodeRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	err = Models.GetAdministratorByWhatsApp(&administrator, verificationCodeRequest.WhatsappNo)

	if err != nil {
		message := err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	if !Utils.ValidateOTP(verificationCodeRequest.VerificationCode, *administrator.CodeRequestedAt) {
		message = "Wrong code"
		Utils.MakeResponse(c, http.StatusUnauthorized, &message, nil)
		return
	}

	message = "Accepted"

	Utils.MakeResponse(c, http.StatusOK, &message, nil)

	return
}

func AdministratorRequestVerificationCode(c *gin.Context) {
	var administrator Models.Administrator
	whatsapNo := c.Params.ByName("whatsapp_no")

	var message string

	err := Models.GetAdministratorByWhatsApp(&administrator, whatsapNo)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	now := time.Now().Unix()

	administrator.CodeRequestedAt = &now

	err = Models.AdministratorUpdate(&administrator)

	if err != nil {
		message := err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	var user Models.User

	user.Name = administrator.Name
	user.WhatsappNo = administrator.WhatsappNo
	user.Email = ""
	user.FcmToken = ""

	err = routeguides.SendUserVerificationCode(user, Utils.GetOTP(*&now))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, user)
	}

	message = "Verification code sent"

	Utils.MakeResponse(c, http.StatusOK, &message, nil)
}

func GetUsers(c *gin.Context) {
	pagination := Models.NewUserPagination()

	if c.Query("page") != "" {
		pagination.Page, _ = strconv.Atoi(c.Query("page"))
	}

	if c.Query("limit") != "" {
		pagination.Limit, _ = strconv.Atoi(c.Query("limit"))
	}

	if c.Query("query") != "" {
		pagination.Query = c.Query("query")
	}

	if c.Query("sort") != "" {
		pagination.Sort = c.Query("sort")
	}

	message := "Success"

	result, _ := Models.PaginateUser(pagination)

	Utils.MakeResponse(c, http.StatusOK, &message, result)
}

func GetUserByUid(c *gin.Context) {
	var message string
	var user Models.User

	err := Models.GetByUid(&user, c.Params.ByName("user_uid"))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	var userResponse Models.UserResponse

	userResponse.Email = user.Email
	userResponse.Name = user.Name
	userResponse.Uuid = user.Uuid.String()
	userResponse.WhatsappNo = user.WhatsappNo
	userResponse.VerifiedAt = user.VerifiedAt
	userResponse.UnsuspendAt = strconv.FormatInt(*user.UnsuspendAt, 10)

	message = "Success"

	Utils.MakeResponse(c, http.StatusOK, &message, userResponse)
}

func SuspendUser(c *gin.Context) {
	var message string
	var suspendRequest Models.UserSuspendRequest

	err := c.BindJSON(&suspendRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	var user Models.User

	err = Models.GetByUid(&user, suspendRequest.Uid)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	oneDayLater := Utils.OneDayLater().Unix()
	user.UnsuspendAt = &oneDayLater

	Models.Update(&user)

	message = "Success"

	Utils.MakeResponse(c, http.StatusOK, &message, nil)
}
