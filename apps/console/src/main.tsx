import React from "react";
import ReactDOM from "react-dom/client";
import { ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";
import App from "./App";
import "./index.css";

const themeColor = import.meta.env.VITE_THEME_COLOR || "#1677ff";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ConfigProvider
      locale={zhCN}
      theme={{ token: { colorPrimary: themeColor, borderRadius: 6 } }}
    >
      <App />
    </ConfigProvider>
  </React.StrictMode>,
);
