package Models

import (
	"time"

	"github.com/google/uuid"
)

type Business struct {
	Uid         uuid.UUID `json:"uid" gorm:"primary_key;size:36"`
	OwnerUid    uuid.UUID `json:"ownerUid" gorm:"not null;size:36"`
	LocationUid uuid.UUID `json:"locationUid" gorm:"not null;size:36"`
	ProvinceUid uuid.UUID `json:"provinceUid" gorm:"not null;size:36"`

	Name    string `json:"name" gorm:"not null;size:20"`
	Address string `json:"address" gorm:"not null;size:30"`
	Photo   string `json:"photo" gorm:"not null;size:100"`

	ReviewsCount int `json:"reviewsCount" gorm:"default:0"`
	TotalScore   int `json:"totalScore" gorm:"default:0"`

	CreatedAt  time.Time  `json:"createdAt" gorm:"not null"`
	ModifiedAt *time.Time `json:"modifiedAt"`
}

type BusinessRequest struct {
	OwnerUid    string `json:"ownerUid"`
	LocationUid string `json:"locationUid"`
	ProvinceUid string `json:"provinceUid"`

	Name    string `json:"name"`
	Address string `json:"address"`
	Photo   string `json:"photo" gorm:"not null"`
}
