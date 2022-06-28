package Controllers

import (
	"business-service/Models"
	"business-service/Utils"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	uuidSatori "github.com/satori/go.uuid"
)

func SearchBusiness(c *gin.Context) {
	pagination := Models.NewBusinessPagination()

	if c.Query("page") != "" {
		pagination.Page, _ = strconv.Atoi(c.Query("page"))
	}

	if c.Query("limit") != "" {
		pagination.Limit, _ = strconv.Atoi(c.Query("limit"))
	}

	if c.Query("businessName") != "" {
		pagination.BusinessName = c.Query("businessName")
	}

	if c.Query("businessAddress") != "" {
		pagination.BusinessAddress = c.Query("businessAddress")
	}

	if c.Query("locationUid") != "" {
		pagination.LocationUid = c.Query("locationUid")
	}

	if c.Query("sort") != "" {
		pagination.Sort = c.Query("sort")
	}

	message := ""

	// Get location name

	locationUid, err := uuidSatori.FromString(pagination.LocationUid)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	var location Models.Location

	err = Models.GetLocationsByUid(&location, uuid.UUID(locationUid))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	pagination.Location = location.Name

	// Get province name

	var province Models.Province

	err = Models.GetProvinceByUid(&province, location.ProvinceUid)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	pagination.Province = province.Name

	result, _ := Models.PaginateBusiness(pagination)

	Utils.MakeResponse(c, 200, &message, result)
}

func GetBusinessByUid(c *gin.Context) {
	var business Models.Business
	var message string

	err := Models.GetBusinessByUid(&business, uuid.UUID(uuidSatori.FromStringOrNil(c.Params.ByName("businessUid"))))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	message = "Success"

	Utils.MakeResponse(c, http.StatusOK, &message, business)
}

func GetBusinessByUserUid(c *gin.Context) {
	var business Models.Business
	var message string
	err := Models.GetBusinessByOwnerUid(&business, uuid.UUID(uuidSatori.FromStringOrNil(c.Params.ByName("userUid"))))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	message = "Success"

	Utils.MakeResponse(c, http.StatusOK, &message, business)
}

func RegisterBusiness(c *gin.Context) {
	Utils.LoadEnv()
	sess := Utils.ConnectAws()

	var businessRequest Models.BusinessRequest
	var message string
	err := c.BindJSON(&businessRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	fileName := Utils.RandStringRunes(20)

	go Utils.AddFileToS3(sess, businessRequest.Photo, fileName)

	var business Models.Business

	business.Uid = uuid.New()

	business.Address = businessRequest.Address
	business.Name = businessRequest.Name
	business.Photo = fileName

	business.CreatedAt = Utils.Now()
	business.OwnerUid = uuid.UUID(uuidSatori.FromStringOrNil(businessRequest.OwnerUid))
	business.ProvinceUid = uuid.UUID(uuidSatori.FromStringOrNil(businessRequest.ProvinceUid))
	business.LocationUid = uuid.UUID(uuidSatori.FromStringOrNil(businessRequest.LocationUid))

	err = Models.CreateBusiness(&business)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, nil)
		return
	}

	Utils.MakeResponse(c, http.StatusOK, &message, business)
}

func RegisterProvince(c *gin.Context) {
	var provinceRequest Models.ProvinceRequest
	var message string

	err := c.BindJSON(&provinceRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	var province Models.Province
	province = Models.Province{ProvinceRequest: provinceRequest}

	province.Uid = uuid.New()

	err = Models.CreateProvince(&province)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, nil)
		return
	}

	message = "Province created"
	Utils.MakeResponse(c, http.StatusOK, &message, province)
}

func RegisterLocation(c *gin.Context) {
	var locationRequest Models.LocationRequest
	var message string

	err := c.BindJSON(&locationRequest)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusBadRequest, &message, nil)
		return
	}

	var province Models.Province

	err = Models.GetProvinceByUid(&province, uuid.UUID(uuidSatori.FromStringOrNil(locationRequest.ProvinceUid)))

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	var location Models.Location

	location.Name = locationRequest.Name
	location.ProvinceUid = uuid.UUID(uuidSatori.FromStringOrNil(locationRequest.ProvinceUid))
	location.Uid = uuid.New()

	err = Models.CreateLocation(&location)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, nil)
	}

	message = "Location created"

	Utils.MakeResponse(c, http.StatusOK, &message, location)
}

func GetAllProvinces(c *gin.Context) {
	var provinces []Models.Province
	var message string

	err := Models.GetAllProvinces(&provinces)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusInternalServerError, &message, nil)
		return
	}

	message = "Success"

	Utils.MakeResponse(c, http.StatusOK, &message, provinces)
}

func GetLocationsByProvinceUid(c *gin.Context) {
	var province Models.Province
	var message string

	provinceUid := uuid.UUID(uuidSatori.FromStringOrNil(c.Params.ByName("provinceUid")))

	err := Models.GetProvinceByUid(&province, provinceUid)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	var locations []Models.Location

	err = Models.GetLocationsByProvinceUid(&locations, province.Uid)

	if err != nil {
		message = err.Error()
		Utils.MakeResponse(c, http.StatusNotFound, &message, nil)
		return
	}

	message = "Success"

	Utils.MakeResponse(c, http.StatusOK, &message, locations)
}
