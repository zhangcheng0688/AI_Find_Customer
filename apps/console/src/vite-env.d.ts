/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE: string;
  readonly VITE_GATEWAY_BASE: string;
  readonly VITE_TENANT_ID: string;
  readonly VITE_BRAND_NAME: string;
  readonly VITE_BRAND_LOGO: string;
  readonly VITE_THEME_COLOR: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
