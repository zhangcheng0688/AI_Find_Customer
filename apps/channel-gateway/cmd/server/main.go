package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

func getenv(k, d string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return d
}

type ingestBody struct {
	TenantID      string `json:"tenantId"`
	BotID         string `json:"botId"`
	UserID        string `json:"userId"`
	Text          string `json:"text"`
	ExternalMsgID string `json:"externalMsgId"`
}

type apiEnvelope struct {
	OK    bool            `json:"ok"`
	Error string          `json:"error"`
	Data  json.RawMessage `json:"data"`
}

func main() {
	addr := getenv("HTTP_ADDR", ":8081")
	apiBase := strings.TrimRight(getenv("API_BASE_URL", "http://localhost:8080"), "/")
	r := gin.New()
	r.Use(gin.Logger(), gin.Recovery())
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true, "data": gin.H{"service": "channel-gateway"}})
	})
	r.POST("/dev/ingest", func(c *gin.Context) {
		var body ingestBody
		if err := c.ShouldBindJSON(&body); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"ok": false, "error": err.Error()})
			return
		}
		if body.TenantID == "" || body.BotID == "" || body.Text == "" || body.ExternalMsgID == "" {
			c.JSON(http.StatusBadRequest, gin.H{"ok": false, "error": "tenantId, botId, text, externalMsgId are required"})
			return
		}
		if body.UserID == "" {
			body.UserID = "anonymous"
		}
		mockReply := fmt.Sprintf("（壳占位）已收到：「%s」。下一步由扣子 Agent + RAGFlow 作答，而不是行业询价流程。", body.Text)
		payload := map[string]any{
			"bot_id":          body.BotID,
			"type":            "chat",
			"status":          "waiting",
			"assignee":        "builder",
			"external_msg_id": body.ExternalMsgID,
			"context_json": map[string]any{
				"userId":       body.UserID,
				"text":         body.Text,
				"mockReply":    mockReply,
				"channel":      "console",
				"orchestrator": "pending-coze",
				"knowledge":    "pending-ragflow",
			},
		}
		raw, _ := json.Marshal(payload)
		req, err := http.NewRequest(http.MethodPost, apiBase+"/tenants/"+body.TenantID+"/missions", bytes.NewReader(raw))
		if err != nil {
			c.JSON(http.StatusBadGateway, gin.H{"ok": false, "error": err.Error()})
			return
		}
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("X-Tenant-Id", body.TenantID)
		client := &http.Client{Timeout: 10 * time.Second}
		res, err := client.Do(req)
		if err != nil {
			c.JSON(http.StatusBadGateway, gin.H{"ok": false, "error": "api: " + err.Error()})
			return
		}
		defer res.Body.Close()
		b, _ := io.ReadAll(res.Body)
		var env apiEnvelope
		if err := json.Unmarshal(b, &env); err != nil || !env.OK {
			msg := strings.TrimSpace(string(b))
			if env.Error != "" {
				msg = env.Error
			}
			c.JSON(http.StatusBadGateway, gin.H{"ok": false, "error": msg})
			return
		}
		c.JSON(http.StatusOK, gin.H{
			"ok":        true,
			"mockReply": mockReply,
			"data":      json.RawMessage(env.Data),
		})
	})
	log.Printf("channel-gateway listening on %s api=%s", addr, apiBase)
	if err := r.Run(addr); err != nil {
		log.Fatal(err)
	}
}
