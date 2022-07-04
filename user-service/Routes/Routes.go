package Routes

import (
	"user-service/Controllers"

	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	router := gin.Default()

	router.POST("/", Controllers.Register)

	router.GET("/")

	router.GET("/verification/whatsapp/:whatsapp_no", Controllers.RequestVerificationCode)

	router.POST("/authentication/whatsapp", Controllers.VerifyVerificationCode)

	router.POST("/authentication/password", Controllers.VerifyPassword)

	router.PATCH("/name", Controllers.UpdateName)

	router.PATCH("/password", Controllers.UpdatePassword)

	/* Administrator routers */

	router.GET("/administrator/verification/whatsapp/:whatsapp_no", Controllers.AdministratorRequestVerificationCode)

	router.POST("/administrator/authentication/whatsapp", Controllers.AdministratorVerifyVerificationCode)

	router.GET("/administrator/users", Controllers.GetUsers)

	router.GET("/administrator/users/:user_uid", Controllers.GetUserByUid)

	router.PATCH("/administrator/users/suspend", Controllers.SuspendUser)

	return router
}
