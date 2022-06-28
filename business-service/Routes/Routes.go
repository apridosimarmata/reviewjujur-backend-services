package Routes

import (
	"business-service/Controllers"

	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	router := gin.Default()

	router.POST("/", Controllers.RegisterBusiness)

	router.GET("/user/:userUid", Controllers.GetBusinessByUserUid)

	router.GET("/:businessUid", Controllers.GetBusinessByUid)

	router.POST("/provinces", Controllers.RegisterProvince)

	router.GET("/provinces", Controllers.GetAllProvinces)

	router.POST("/locations", Controllers.RegisterLocation)

	router.GET("/locations/:provinceUid", Controllers.GetLocationsByProvinceUid)

	router.GET("/search", Controllers.SearchBusiness)

	return router
}
