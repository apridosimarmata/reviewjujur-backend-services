package Models

import (
	"math"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"

	Configs "business-service/Configs"

	"github.com/google/uuid"
)

func (business *Business) BeforeCreate(scope *gorm.Scope) error {
	scope.SetColumn("ID", uuid.New().String())
	return nil
}

func CreateBusiness(business *Business) (err error) {
	if err = Configs.DB.Create(business).Error; err != nil {
		return err
	}
	return nil
}

func GetBusinessByUid(business *Business, businessUid uuid.UUID) (err error) {
	if err = Configs.DB.Where("uid = ?", businessUid).First(business).Error; err != nil {
		return err
	}
	return nil
}

func PaginateBusiness(businessPagination BusinessPagination) (any BusinessPagination, err error) {
	var res []*Business
	Configs.DB.Scopes(paginate(&res, &businessPagination, Configs.DB)).Find(&res)
	businessPagination.Rows = res
	return businessPagination, nil
}

func paginate(value interface{}, businessPagination *BusinessPagination, db *gorm.DB) func(db *gorm.DB) *gorm.DB {
	var totalRows int64
	db.Model(value).Count(&totalRows)

	businessPagination.TotalRows = totalRows
	businessPagination.TotalPages = int(math.Ceil(float64(totalRows) / float64(businessPagination.Limit)))

	return func(db *gorm.DB) *gorm.DB {
		return db.Offset(businessPagination.GetOffset()).Limit(businessPagination.GetLimit()).Order(businessPagination.GetSort()).Where("name like ?", "%"+businessPagination.BusinessName+"%").Where("address like ?", "%"+businessPagination.BusinessAddress+"%").Where("location_uid = ?", businessPagination.LocationUid)
	}
}
