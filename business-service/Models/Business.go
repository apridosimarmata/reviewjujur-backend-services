package Models

import (
	"fmt"
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

func GetBusinessByOwnerUid(business *Business, ownerUid uuid.UUID) (err error) {
	if err = Configs.DB.Where("owner_uid = ?", ownerUid).First(business).Error; err != nil {
		return err
	}
	return nil
}

func Update(business *Business) (err error) {
	Configs.DB.Save(business)
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

	query := db.Model(value).Where("name like ? OR address like ?", "%"+businessPagination.Query+"%", "%"+businessPagination.Query+"%")

	if businessPagination.LocationUid != "" {
		query.Where("location_uid = ?", businessPagination.LocationUid).Count(&totalRows)
	} else {
		query.Count(&totalRows)
	}

	businessPagination.TotalRows = totalRows
	businessPagination.TotalPages = int(math.Ceil(float64(totalRows) / float64(businessPagination.Limit)))

	return func(db *gorm.DB) *gorm.DB {
		fmt.Println("page ", businessPagination.GetOffset())
		query := db.Model(value).Offset(businessPagination.GetOffset()).Limit(businessPagination.GetLimit()).Order(businessPagination.GetSort()).Where("name like ? OR address like ?", "%"+businessPagination.Query+"%", "%"+businessPagination.Query+"%")

		if businessPagination.LocationUid != "" {
			query = query.Where("location_uid = ?", businessPagination.LocationUid)
		}

		return query
	}
}
