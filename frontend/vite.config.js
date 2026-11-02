import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// FastAPI phục vụ thư mục `dist/` dưới đường `/static/` (trang chính ở `/`) ⇒ mọi đường dẫn tài nguyên trong bản build bắt đầu bằng `/static/`.
export default defineConfig({
  base: "/static/",
  plugins: [react(), tailwindcss()],
});
