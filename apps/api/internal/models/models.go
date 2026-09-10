package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/datatypes"
	"gorm.io/gorm"
)

type Tenant struct {
	ID          string    `json:"id" gorm:"primaryKey"`
	Name        string    `json:"name"`
	DisplayName string    `json:"display_name"`
	LogoURL     string    `json:"logo_url"`
	ThemeColor  string    `json:"theme_color"`
	CreatedAt   time.Time `json:"created_at"`
}

type User struct {
	ID        string    `json:"id" gorm:"primaryKey"`
	TenantID  string    `json:"tenant_id" gorm:"index"`
	Email     string    `json:"email"`
	Role      string    `json:"role"`
	CreatedAt time.Time `json:"created_at"`
}

type Mission struct {
	ID            string         `json:"id" gorm:"primaryKey"`
	TenantID      string         `json:"tenant_id" gorm:"index;not null"`
	BotID         string         `json:"bot_id" gorm:"not null"`
	Type          string         `json:"type" gorm:"not null"`
	Status        string         `json:"status" gorm:"index;not null"`
	DueAt         *time.Time     `json:"due_at"`
	Assignee      string         `json:"assignee"`
	ContextJSON   datatypes.JSON `json:"context_json"`
	LastActionAt  *time.Time     `json:"last_action_at"`
	CancelReason  string         `json:"cancel_reason"`
	ExternalMsgID string         `json:"external_msg_id" gorm:"index"`
	CreatedAt     time.Time      `json:"created_at"`
	UpdatedAt     time.Time      `json:"updated_at"`
}

func (m *Mission) BeforeCreate(tx *gorm.DB) error {
	if m.ID == "" {
		m.ID = uuid.NewString()
	}
	if len(m.ContextJSON) == 0 {
		m.ContextJSON = datatypes.JSON([]byte("{}"))
	}
	return nil
}
