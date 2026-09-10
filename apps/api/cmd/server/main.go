package main

import (
	"log"

	"github.com/zhangcheng0688/agent-factory/apps/api/internal/chaser"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/config"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/httpapi"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/store"
)

func main() {
	cfg := config.Load()
	db, err := store.Open(cfg)
	if err != nil {
		log.Fatalf("db: %v", err)
	}
	if err := store.Seed(db, cfg); err != nil {
		log.Fatalf("seed: %v", err)
	}
	chaser.Start(db, cfg)
	r := httpapi.New(db, cfg)
	log.Printf("api listening on %s (tenant=%s)", cfg.HTTPAddr, cfg.DevTenantID)
	if err := r.Run(cfg.HTTPAddr); err != nil {
		log.Fatal(err)
	}
}
