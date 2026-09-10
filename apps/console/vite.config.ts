import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api-proxy": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\/api-proxy/, ""),
      },
      "/gw-proxy": {
        target: "http://localhost:8081",
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\/gw-proxy/, ""),
      },
    },
  },
});
