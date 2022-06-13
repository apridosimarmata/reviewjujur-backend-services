package Models

import "github.com/google/uuid"

type Province struct {
	Uid uuid.UUID `json:"uid" gorm:"primary_key:size:36"`
	ProvinceRequest
}

type ProvinceRequest struct {
	Name string `json:"name" gorm:"not null;size:30"`
}
