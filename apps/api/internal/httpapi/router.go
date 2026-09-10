package httpapi

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/config"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/mission"
	"github.com/zhangcheng0688/agent-factory/apps/api/internal/models"
	"gorm.io/datatypes"
	"gorm.io/gorm"
)

type Server struct {
	DB  *gorm.DB
	Cfg config.Config
}

func New(db *gorm.DB, cfg config.Config) *gin.Engine {
	s := &Server{DB: db, Cfg: cfg}
	r := gin.New()
	r.Use(gin.Logger(), gin.Recovery())
	r.Use(cors.New(cors.Config{
		AllowAllOrigins:  true,
		AllowMethods:     []string{"GET", "POST", "PATCH", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "X-Tenant-Id"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: false,
		MaxAge:           12 * time.Hour,
	}))

	r.GET("/health", s.health)
	r.GET("/tenants/:tenantId", s.requireTenant(), s.getTenant)
	r.POST("/tenants/:tenantId/missions", s.requireTenant(), s.createMission)
	r.GET("/tenants/:tenantId/missions", s.requireTenant(), s.listMissions)
	r.GET("/tenants/:tenantId/missions/:id", s.requireTenant(), s.getMission)
	r.PATCH("/tenants/:tenantId/missions/:id/status", s.requireTenant(), s.patchStatus)
	r.POST("/tenants/:tenantId/missions/:id/cancel", s.requireTenant(), s.cancelMission)
	return r
}

func ok(c *gin.Context, status int, data any) {
	c.JSON(status, gin.H{"ok": true, "data": data})
}

func fail(c *gin.Context, status int, msg string) {
	c.JSON(status, gin.H{"ok": false, "error": msg})
}

func (s *Server) health(c *gin.Context) {
	sqlDB, err := s.DB.DB()
	if err != nil {
		fail(c, http.StatusServiceUnavailable, err.Error())
		return
	}
	if err := sqlDB.Ping(); err != nil {
		fail(c, http.StatusServiceUnavailable, err.Error())
		return
	}
	ok(c, http.StatusOK, gin.H{
		"service": "api",
		"db":      "ok",
		"tenant":  s.Cfg.DevTenantID,
	})
}

func (s *Server) requireTenant() gin.HandlerFunc {
	return func(c *gin.Context) {
		pathID := c.Param("tenantId")
		headerID := strings.TrimSpace(c.GetHeader("X-Tenant-Id"))
		if headerID == "" {
			fail(c, http.StatusUnauthorized, "missing X-Tenant-Id")
			c.Abort()
			return
		}
		if headerID != pathID {
			fail(c, http.StatusForbidden, "tenant mismatch")
			c.Abort()
			return
		}
		var t models.Tenant
		if err := s.DB.First(&t, "id = ?", pathID).Error; err != nil {
			if errors.Is(err, gorm.ErrRecordNotFound) {
				fail(c, http.StatusNotFound, "tenant not found")
			} else {
				fail(c, http.StatusInternalServerError, err.Error())
			}
			c.Abort()
			return
		}
		c.Set("tenant", t)
		c.Next()
	}
}

func (s *Server) getTenant(c *gin.Context) {
	t := c.MustGet("tenant").(models.Tenant)
	ok(c, http.StatusOK, t)
}

type createMissionBody struct {
	BotID         string          `json:"bot_id"`
	Type          string          `json:"type"`
	Status        string          `json:"status"`
	DueAt         *time.Time      `json:"due_at"`
	Assignee      string          `json:"assignee"`
	ContextJSON   json.RawMessage `json:"context_json"`
	ExternalMsgID string          `json:"external_msg_id"`
}

func (s *Server) createMission(c *gin.Context) {
	tenantID := c.Param("tenantId")
	var body createMissionBody
	if err := c.ShouldBindJSON(&body); err != nil {
		fail(c, http.StatusBadRequest, err.Error())
		return
	}
	if body.BotID == "" || body.Type == "" {
		fail(c, http.StatusBadRequest, "bot_id and type are required")
		return
	}
	st := mission.Open
	if body.Status != "" {
		parsed, err := mission.ParseStatus(body.Status)
		if err != nil {
			fail(c, http.StatusBadRequest, err.Error())
			return
		}
		st = parsed
	}

	if body.ExternalMsgID != "" {
		var existing models.Mission
		err := s.DB.Where("tenant_id = ? AND external_msg_id = ?", tenantID, body.ExternalMsgID).First(&existing).Error
		if err == nil {
			ok(c, http.StatusOK, gin.H{"mission": existing, "idempotent": true})
			return
		}
		if !errors.Is(err, gorm.ErrRecordNotFound) {
			fail(c, http.StatusInternalServerError, err.Error())
			return
		}
	}

	due := body.DueAt
	if due == nil && body.Type == "inquiry" {
		t := time.Now().Add(s.Cfg.DemoChaseAfter)
		due = &t
	}
	ctx := body.ContextJSON
	if len(ctx) == 0 {
		ctx = json.RawMessage(`{}`)
	}
	now := time.Now()
	m := models.Mission{
		ID:            uuid.NewString(),
		TenantID:      tenantID,
		BotID:         body.BotID,
		Type:          body.Type,
		Status:        string(st),
		DueAt:         due,
		Assignee:      body.Assignee,
		ContextJSON:   datatypes.JSON(ctx),
		LastActionAt:  &now,
		ExternalMsgID: body.ExternalMsgID,
	}
	if err := s.DB.Create(&m).Error; err != nil {
		fail(c, http.StatusInternalServerError, err.Error())
		return
	}
	ok(c, http.StatusCreated, gin.H{"mission": m, "idempotent": false})
}

func (s *Server) listMissions(c *gin.Context) {
	tenantID := c.Param("tenantId")
	q := s.DB.Where("tenant_id = ?", tenantID)
	if st := c.Query("status"); st != "" {
		if _, err := mission.ParseStatus(st); err != nil {
			fail(c, http.StatusBadRequest, err.Error())
			return
		}
		q = q.Where("status = ?", st)
	}
	var items []models.Mission
	if err := q.Order("created_at DESC").Limit(200).Find(&items).Error; err != nil {
		fail(c, http.StatusInternalServerError, err.Error())
		return
	}
	ok(c, http.StatusOK, items)
}

func (s *Server) loadMission(c *gin.Context) (*models.Mission, bool) {
	tenantID := c.Param("tenantId")
	id := c.Param("id")
	var m models.Mission
	if err := s.DB.Where("id = ? AND tenant_id = ?", id, tenantID).First(&m).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			fail(c, http.StatusNotFound, "mission not found")
		} else {
			fail(c, http.StatusInternalServerError, err.Error())
		}
		return nil, false
	}
	return &m, true
}

func (s *Server) getMission(c *gin.Context) {
	m, okm := s.loadMission(c)
	if !okm {
		return
	}
	ok(c, http.StatusOK, m)
}

type statusBody struct {
	Status string `json:"status"`
}

func (s *Server) patchStatus(c *gin.Context) {
	m, okm := s.loadMission(c)
	if !okm {
		return
	}
	var body statusBody
	if err := c.ShouldBindJSON(&body); err != nil || body.Status == "" {
		fail(c, http.StatusBadRequest, "status is required")
		return
	}
	to, err := mission.ParseStatus(body.Status)
	if err != nil {
		fail(c, http.StatusBadRequest, err.Error())
		return
	}
	if err := mission.Transition(mission.Status(m.Status), to); err != nil {
		fail(c, http.StatusConflict, err.Error())
		return
	}
	now := time.Now()
	m.Status = string(to)
	m.LastActionAt = &now
	if err := s.DB.Save(m).Error; err != nil {
		fail(c, http.StatusInternalServerError, err.Error())
		return
	}
	ok(c, http.StatusOK, m)
}

type cancelBody struct {
	Reason string `json:"reason"`
}

func (s *Server) cancelMission(c *gin.Context) {
	m, okm := s.loadMission(c)
	if !okm {
		return
	}
	var body cancelBody
	_ = c.ShouldBindJSON(&body)
	if body.Reason == "" {
		body.Reason = "cancelled"
	}
	if err := mission.Transition(mission.Status(m.Status), mission.Done); err != nil {
		fail(c, http.StatusConflict, err.Error())
		return
	}
	now := time.Now()
	m.Status = string(mission.Done)
	m.CancelReason = body.Reason
	m.LastActionAt = &now
	m.DueAt = nil
	if err := s.DB.Save(m).Error; err != nil {
		fail(c, http.StatusInternalServerError, err.Error())
		return
	}
	ok(c, http.StatusOK, m)
}
