import { existsSync } from "node:fs";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// Ảnh lễ hội thật không có giấy phép mở ⇒ để ở `public/anh/rieng/` (gitignore). Quyết lúc build để bản clone không có file
// vẫn chạy, không tải ảnh 404 rồi mới đổi (ghi công phải khớp ảnh thật sự hiện ra — `src/anh.js`).
const CO_ANH_LE_HOI_RIENG = existsSync(new URL("./public/anh/rieng/lv_festivals.jpg", import.meta.url));

// FastAPI phục vụ thư mục `dist/` dưới đường `/static/` (trang chính ở `/`) ⇒ mọi đường dẫn tài nguyên trong bản build bắt đầu bằng `/static/`.
export default defineConfig({
  base: "/static/",
  define: { __CO_ANH_LE_HOI_RIENG__: JSON.stringify(CO_ANH_LE_HOI_RIENG) },
  plugins: [react(), tailwindcss()],
});
