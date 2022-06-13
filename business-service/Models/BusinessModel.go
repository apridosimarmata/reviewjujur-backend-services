package Models

import (
	"time"

	"github.com/google/uuid"
)

type Business struct {
	Uid         uuid.UUID `json:"uid" gorm:"primary_key;size:36"`
	OwnerUid    uuid.UUID `json:"owner_uid" gorm:"not null;size:36"`
	LocationUid uuid.UUID `json:"location_uid" gorm:"not null;size:36"`
	ProvinceUid uuid.UUID `json:"province_uid" gorm:"not null;size:36"`

	Name    string `json:"name" gorm:"not null;size:20"`
	Address string `json:"address" gorm:"not null;size:20"`
	Photo   string `json:"photo" gorm:"not null;size:100"`

	ReviewsCount int `json:"reviews_count" gorm:"default:0"`
	TotalScore   int `json:"total_score" gorm:"default:0"`

	CreatedAt  time.Time  `json:"created_at" gorm:"not null"`
	ModifiedAt *time.Time `json:"modified_at"`
}

type BusinessRequest struct {
	OwnerUid    string `json:"owner_uid"`
	LocationUid string `json:"location_uid"`
	ProvinceUid string `json:"province_uid"`

	Name    string `json:"name"`
	Address string `json:"address"`
	Photo   string `json:"photo" gorm:"not null;size:40"`
}
