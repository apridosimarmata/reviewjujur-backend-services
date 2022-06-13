package Models

import (
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"

	Configs "business-service/Configs"
)

func CreateProvince(province *Province) (err error) {
	if err = Configs.DB.Create(province).Error; err != nil {
		return err
	}
	return nil
}

func GetProvinceByUid(province *Province, uid uuid.UUID) (err error) {
	if err = Configs.DB.Where("uid = ?", uid).Find(province).Error; err != nil {
		return err
	}
	return nil
}

func GetAllProvinces(provinces *[]Province) (err error) {
	if err = Configs.DB.Order("name desc").Find(provinces).Error; err != nil {
		return err
	}
	return nil
}
