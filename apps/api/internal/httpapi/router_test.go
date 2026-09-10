package httpapi

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/chaser"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/config"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/models"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/store"
	"gorm.io/gorm"
)

func setup(t *testing.T) (*gin.Engine, config.Config, *gorm.DB) {
	t.Helper()
	gin.SetMode(gin.TestMode)
	cfg := config.Config{
		SQLitePath:     filepath.Join(t.TempDir(), "t.db"),
		DevTenantID:    "dev-tenant",
		DevTenantName:  "Dev Cable Co",
		BrandName:      "Agent 工厂",
		ThemeColor:     "#1677ff",
		DemoChaseAfter: time.Hour,
		ChaseTick:      time.Hour,
	}
	db, err := store.Open(cfg)
	if err != nil {
		t.Fatal(err)
	}
	if err := store.Seed(db, cfg); err != nil {
		t.Fatal(err)
	}
	if err := db.Create(&models.Tenant{ID: "other-tenant", Name: "Other", DisplayName: "Other", ThemeColor: "#000"}).Error; err != nil {
		t.Fatal(err)
	}
	return New(db, cfg), cfg, db
}

func TestHealthAndMissionFlow(t *testing.T) {
	engine, _, _ := setup(t)

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()
	engine.ServeHTTP(w, req)
	if w.Code != 200 {
		t.Fatalf("health %d %s", w.Code, w.Body.String())
	}

	raw, _ := json.Marshal(map[string]any{"bot_id": "bot-quote", "type": "inquiry", "status": "open"})
	req = httptest.NewRequest(http.MethodPost, "/tenants/dev-tenant/missions", bytes.NewReader(raw))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Tenant-Id", "dev-tenant")
	w = httptest.NewRecorder()
	engine.ServeHTTP(w, req)
	if w.Code != 201 {
		t.Fatalf("create %d %s", w.Code, w.Body.String())
	}
	var created struct {
		OK   bool `json:"ok"`
		Data struct {
			Mission models.Mission `json:"mission"`
		} `json:"data"`
	}
	if err := json.Unmarshal(w.Body.Bytes(), &created); err != nil {
		t.Fatal(err)
	}
	id := created.Data.Mission.ID

	for _, st := range []string{"running", "done"} {
		patch, _ := json.Marshal(map[string]string{"status": st})
		req = httptest.NewRequest(http.MethodPatch, "/tenants/dev-tenant/missions/"+id+"/status", bytes.NewReader(patch))
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("X-Tenant-Id", "dev-tenant")
		w = httptest.NewRecorder()
		engine.ServeHTTP(w, req)
		if w.Code != 200 {
			t.Fatalf("patch %s %d %s", st, w.Code, w.Body.String())
		}
	}

	patch, _ := json.Marshal(map[string]string{"status": "running"})
	req = httptest.NewRequest(http.MethodPatch, "/tenants/dev-tenant/missions/"+id+"/status", bytes.NewReader(patch))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Tenant-Id", "dev-tenant")
	w = httptest.NewRecorder()
	engine.ServeHTTP(w, req)
	if w.Code != 409 {
		t.Fatalf("expected 409 got %d %s", w.Code, w.Body.String())
	}
}

func TestTenantIsolation(t *testing.T) {
	engine, _, _ := setup(t)
	raw, _ := json.Marshal(map[string]any{"bot_id": "b", "type": "inquiry"})
	req := httptest.NewRequest(http.MethodPost, "/tenants/dev-tenant/missions", bytes.NewReader(raw))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Tenant-Id", "other-tenant")
	w := httptest.NewRecorder()
	engine.ServeHTTP(w, req)
	if w.Code != 403 {
		t.Fatalf("expected 403 got %d %s", w.Code, w.Body.String())
	}

	req = httptest.NewRequest(http.MethodGet, "/tenants/dev-tenant/missions", nil)
	w = httptest.NewRecorder()
	engine.ServeHTTP(w, req)
	if w.Code != 401 {
		t.Fatalf("expected 401 got %d", w.Code)
	}
}

func TestIdempotentExternalMsg(t *testing.T) {
	engine, _, _ := setup(t)
	raw, _ := json.Marshal(map[string]any{
		"bot_id": "bot-quote", "type": "inquiry", "external_msg_id": "msg-1",
	})
	post := func() string {
		req := httptest.NewRequest(http.MethodPost, "/tenants/dev-tenant/missions", bytes.NewReader(raw))
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("X-Tenant-Id", "dev-tenant")
		w := httptest.NewRecorder()
		engine.ServeHTTP(w, req)
		if w.Code != 201 && w.Code != 200 {
			t.Fatalf("code %d %s", w.Code, w.Body.String())
		}
		var env struct {
			Data struct {
				Mission    models.Mission `json:"mission"`
				Idempotent bool           `json:"idempotent"`
			} `json:"data"`
		}
		_ = json.Unmarshal(w.Body.Bytes(), &env)
		return env.Data.Mission.ID
	}
	if post() != post() {
		t.Fatal("expected same mission id")
	}
}

func TestChaserAdvancesWaitingMission(t *testing.T) {
	_, cfg, db := setup(t)
	past := time.Now().Add(-time.Minute)
	m := models.Mission{
		TenantID: "dev-tenant",
		BotID:    "bot-quote",
		Type:     "inquiry",
		Status:   "waiting",
		DueAt:    &past,
	}
	if err := db.Create(&m).Error; err != nil {
		t.Fatal(err)
	}
	if err := chaser.Tick(db, cfg); err != nil {
		t.Fatal(err)
	}
	var got models.Mission
	if err := db.First(&got, "id = ?", m.ID).Error; err != nil {
		t.Fatal(err)
	}
	if !bytes.Contains(got.ContextJSON, []byte("催办A")) {
		t.Fatalf("context %s", got.ContextJSON)
	}
}
