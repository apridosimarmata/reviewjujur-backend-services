package main

import (
	"business-service/Configs"
	"business-service/Models"
	"business-service/Routes"
	"fmt"

	"github.com/jinzhu/gorm"
)

func main() {
	var err error
	Configs.DB, err = gorm.Open("mysql", Configs.DbURL(Configs.BuildDBConfig()))
	if err != nil {
		fmt.Println("Status: ", err)
	}

	defer Configs.DB.Close()
	Configs.DB.AutoMigrate(
		&Models.Business{},
		&Models.Province{},
		&Models.Location{},
	)

	r := Routes.SetupRouter()

	r.Run(":5002")
}
