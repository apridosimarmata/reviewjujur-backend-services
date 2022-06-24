//Config/Database.go
package Configs

import (
	"fmt"
	"log"
	"os"

	"path/filepath"

	"github.com/jinzhu/gorm"
	"github.com/joho/godotenv"
)

var DB *gorm.DB

// DBConfig represents db configuration
type DBConfig struct {
	Host     string
	Port     int
	User     string
	DBName   string
	Password string
}

func goDotEnvVariable(key string) string {

	filePath, _ := filepath.Abs(".env")
	err := godotenv.Load(filePath)

	if err != nil {
		log.Fatalf("Error loading .env file", err.Error())
	}

	return os.Getenv(key)
}

func BuildDBConfig() *DBConfig {
	dbConfig := DBConfig{
		Host:     goDotEnvVariable("DB_HOST"),
		Port:     3306,
		User:     "root",
		Password: goDotEnvVariable("DB_PASS"),
		DBName:   "reviewapp",
	}
	return &dbConfig
}
func DbURL(dbConfig *DBConfig) string {
	return fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local",
		dbConfig.User,
		dbConfig.Password,
		dbConfig.Host,
		dbConfig.Port,
		dbConfig.DBName,
	)
}
