package Models

import "github.com/google/uuid"

type Location struct {
	Uid         uuid.UUID `json:"uid" gorm:"primary_key;size:36"`
	ProvinceUid uuid.UUID `json:"province_uid" gorm:"not null;size:36"`
	Name        string    `json:"name" gorm:"not null;size:20"`
}

type LocationRequest struct {
	ProvinceUid string `json:"province_uid" gorm:"not null;size:36"`
	Name        string `json:"name" gorm:"not null;size:20"`
}
