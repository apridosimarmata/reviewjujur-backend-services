package Models

import (
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"

	Configs "business-service/Configs"
)

func CreateLocation(location *Location) (err error) {
	if err = Configs.DB.Create(location).Error; err != nil {
		return err
	}
	return nil
}

func GetLocationsByProvinceUid(locations *[]Location, provinceUid uuid.UUID) (err error) {
	if err = Configs.DB.Where("province_uid = ?", provinceUid).Find(locations).Error; err != nil {
		return err
	}
	return nil
}

func GetLocationsByUid(location *Location, locationUid uuid.UUID) (err error) {
	if err = Configs.DB.Where("uid = ?", locationUid).Find(location).Error; err != nil {
		return err
	}
	return nil
}

