package chaser

import (
	"encoding/json"
	"log"
	"time"

	"github.com/zhangcheng0688/agent-factory/apps/api/internal/config"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/mission"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/models"
	"gorm.io/datatypes"
	"gorm.io/gorm"
)

type ctxShape struct {
	Chases []map[string]any `json:"chases"`
}

func Start(db *gorm.DB, cfg config.Config) {
	if !cfg.EnableChaser {
		return
	}
	go func() {
		t := time.NewTicker(cfg.ChaseTick)
		defer t.Stop()
		for range t.C {
			if err := Tick(db, cfg); err != nil {
				log.Printf("chaser: %v", err)
			}
		}
	}()
}

func Tick(db *gorm.DB, cfg config.Config) error {
	now := time.Now()
	var due []models.Mission
	if err := db.Where("status = ? AND cancel_reason = ? AND due_at IS NOT NULL AND due_at <= ?",
		string(mission.Waiting), "", now).Find(&due).Error; err != nil {
		return err
	}
	for i := range due {
		if err := chaseOne(db, &due[i], cfg, now); err != nil {
			log.Printf("chaser mission %s: %v", due[i].ID, err)
		}
	}
	return nil
}

func chaseOne(db *gorm.DB, m *models.Mission, cfg config.Config, now time.Time) error {
	var ctx ctxShape
	_ = json.Unmarshal(m.ContextJSON, &ctx)
	n := len(ctx.Chases) + 1
	entry := map[string]any{
		"at":      now.Format(time.RFC3339),
		"n":       n,
		"message": chaseCopy(n),
	}
	ctx.Chases = append(ctx.Chases, entry)

	raw, err := json.Marshal(ctxMerged(m.ContextJSON, ctx.Chases))
	if err != nil {
		return err
	}
	m.ContextJSON = datatypes.JSON(raw)
	m.LastActionAt = &now
	if n >= 2 {
		if err := mission.Transition(mission.Status(m.Status), mission.HandedOff); err != nil {
			return err
		}
		m.Status = string(mission.HandedOff)
		m.DueAt = nil
	} else {
		next := now.Add(cfg.DemoChaseAfter)
		m.DueAt = &next
	}
	return db.Save(m).Error
}

func chaseCopy(n int) string {
	if n >= 2 {
		return "催办B：仍未回复，已升级负责销售。"
	}
	return "催办A：报价/关键问题发出后客户尚未回复，现自动催办。"
}

func ctxMerged(original datatypes.JSON, chases []map[string]any) map[string]any {
	out := map[string]any{}
	_ = json.Unmarshal(original, &out)
	out["chases"] = chases
	return out
}
