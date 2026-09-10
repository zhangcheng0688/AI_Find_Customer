package config

import (
	"os"
	"time"
)

type Config struct {
	HTTPAddr        string
	DatabaseURL     string
	SQLitePath      string
	DevTenantID     string
	DevTenantName   string
	EnableChaser    bool
	DemoChaseAfter  time.Duration
	ChaseTick       time.Duration
	BrandName       string
	BrandLogo       string
	ThemeColor      string
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func Load() Config {
	chaseAfter, err := time.ParseDuration(getenv("DEMO_CHASE_AFTER", "30s"))
	if err != nil {
		chaseAfter = 30 * time.Second
	}
	tick, err := time.ParseDuration(getenv("CHASE_TICK", "5s"))
	if err != nil {
		tick = 5 * time.Second
	}
	return Config{
		HTTPAddr:       getenv("HTTP_ADDR", ":8080"),
		DatabaseURL:    os.Getenv("DATABASE_URL"),
		SQLitePath:     getenv("SQLITE_PATH", "data/api.db"),
		DevTenantID:    getenv("DEV_TENANT_ID", "dev-tenant"),
		DevTenantName:  getenv("DEV_TENANT_NAME", "Dev Cable Co"),
		EnableChaser:   getenv("ENABLE_CHASER", "true") != "false",
		DemoChaseAfter: chaseAfter,
		ChaseTick:      tick,
		BrandName:      getenv("BRAND_NAME", "Agent 工厂"),
		BrandLogo:      os.Getenv("BRAND_LOGO"),
		ThemeColor:     getenv("THEME_COLOR", "#1677ff"),
	}
}
