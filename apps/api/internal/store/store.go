package store

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/glebarez/sqlite"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/config"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

func Open(cfg config.Config) (*gorm.DB, error) {
	gormCfg := &gorm.Config{Logger: logger.Default.LogMode(logger.Warn)}
	var (
		db  *gorm.DB
		err error
	)
	if cfg.DatabaseURL != "" {
		db, err = gorm.Open(postgres.Open(cfg.DatabaseURL), gormCfg)
	} else {
		if dir := filepath.Dir(cfg.SQLitePath); dir != "" && dir != "." {
			if err := os.MkdirAll(dir, 0o755); err != nil {
				return nil, fmt.Errorf("mkdir sqlite: %w", err)
			}
		}
		db, err = gorm.Open(sqlite.Open(cfg.SQLitePath), gormCfg)
	}
	if err != nil {
		return nil, err
	}
	if err := db.AutoMigrate(&models.Tenant{}, &models.User{}, &models.Mission{}); err != nil {
		return nil, err
	}
	return db, nil
}

func Seed(db *gorm.DB, cfg config.Config) error {
	t := models.Tenant{
		ID:          cfg.DevTenantID,
		Name:        cfg.DevTenantName,
		DisplayName: cfg.BrandName,
		LogoURL:     cfg.BrandLogo,
		ThemeColor:  cfg.ThemeColor,
	}
	return db.Where(models.Tenant{ID: cfg.DevTenantID}).Assign(t).FirstOrCreate(&t).Error
}
