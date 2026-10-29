// BioChemVerse API — server Go: health check & readiness (stdlib saja).
//
// Jalankan:
//
//	go run .
//
// Endpoint:
//
//	GET /health         -> liveness
//	GET /health/ready   -> readiness (cek TCP ke PostgreSQL & Redis)
package main

import (
	"encoding/json"
	"log"
	"net"
	"net/http"
	"os"
	"time"
)

type healthResponse struct {
	Status string `json:"status"`
}

type readinessResponse struct {
	Status      string `json:"status"`
	Postgres    string `json:"postgres"`
	Redis       string `json:"redis"`
	Environment string `json:"environment"`
}

func env(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

// tcpOK mengecek ketersediaan layanan lewat koneksi TCP singkat.
func tcpOK(addr string) bool {
	conn, err := net.DialTimeout("tcp", addr, 2*time.Second)
	if err != nil {
		return false
	}
	_ = conn.Close()
	return true
}

func writeJSON(w http.ResponseWriter, code int, payload any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(payload)
}

func withCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", env("CORS_ORIGIN", "http://localhost:5173"))
		w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	port := env("PORT", "8001")
	postgresAddr := env("POSTGRES_ADDR", "localhost:5432")
	redisAddr := env("REDIS_ADDR", "localhost:6379")
	environment := env("ENV", "development")

	mux := http.NewServeMux()

	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, healthResponse{Status: "ok"})
	})

	mux.HandleFunc("GET /health/ready", func(w http.ResponseWriter, r *http.Request) {
		pgStatus, redisStatus := "ok", "ok"
		if !tcpOK(postgresAddr) {
			pgStatus = "down"
		}
		if !tcpOK(redisAddr) {
			redisStatus = "down"
		}
		if pgStatus != "ok" || redisStatus != "ok" {
			writeJSON(w, http.StatusServiceUnavailable, readinessResponse{
				Status: "degraded", Postgres: pgStatus, Redis: redisStatus, Environment: environment,
			})
			return
		}
		writeJSON(w, http.StatusOK, readinessResponse{
			Status: "ready", Postgres: pgStatus, Redis: redisStatus, Environment: environment,
		})
	})

	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		writeJSON(w, http.StatusOK, map[string]string{
			"name": "BioChemVerse API (Go)", "docs": "/health",
		})
	})

	server := &http.Server{
		Addr:              ":" + port,
		Handler:           withCORS(mux),
		ReadHeaderTimeout: 5 * time.Second,
	}

	log.Printf("BioChemVerse Go API listening on :%s (postgres=%s, redis=%s)", port, postgresAddr, redisAddr)
	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}
