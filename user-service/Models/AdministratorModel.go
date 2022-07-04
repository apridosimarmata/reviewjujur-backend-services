package Models

import (
	"time"

	"github.com/google/uuid"
)

type Administrator struct {
	Uuid            uuid.UUID `gorm:"primary_key;"`
	Name            string    `json:"name" binding:"required"`
	WhatsappNo      string    `json:"whatsappNo" gorm:"unique" binding:"required"`
	CreatedAt       time.Time `json:"createdAt"`
	CodeRequestedAt *int64
}

type AdministratorLoginRequest struct {
	Email    string `json:"email" gorm:"unique" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

type AdministratorVerificationCodeRequest struct {
	WhatsappNo       string `json:"whatsappNo" binding:"required,numeric"`
	VerificationCode string `json:"code"`
}
