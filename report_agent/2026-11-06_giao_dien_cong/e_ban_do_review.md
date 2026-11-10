# Review: bản đồ lịch trình (P1 đợt 2 cổng) — nhánh `p11-ban-do`

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 3 minor không chặn)
Người kiểm: E (Claude Code, `hue-rag-22`)
Date: 10:14 08/11/2026
Plan: `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` bản 1 — sha256 tính lại từ file: `e738f6f9f3ae` (khớp)
Implementation report: `report_agent/2026-11-06_giao_dien_cong/b_ban_do_implementation.md`

## 1. Phạm vi đã review

- Git: nhánh `p11-ban-do` = `origin/p11-ban-do` = `d0adf31`, 1 commit trên `main` `1611d34` (merge-base đúng `1611d34`). Diff 16 file +279 / −26, khớp bảng §2 của report. `git diff --check`: sạch.
- Đọc exact diff toàn bộ: `api/app.py`, `routes/cong.py`, `settings.yaml`, `llm/assistant.py`, `llm/lich_trinh.py`, 3 file test, `BanDoLich.jsx` (mới), `chat.jsx`, `App.jsx`, `pages.jsx`, `index.css`, `vite.config.js`, `package.json` + lock.
- Đối chiếu tiêu chí §7 plan. Theo A, trọng tâm là **cờ tắt**: CSP giống byte, chuỗi gửi model không đổi, 0 host lạ. Phần cờ bật (Q-M1–Q-M6) dùng bằng chứng của B; E kiểm thêm phía code.
- Thay đổi ngoài plan đã khai báo: `data:` trong `img-src` khi cờ bật (A duyệt); `assetsInlineLimit: 0`; sửa test B6 hỏng sẵn (A giao). Cả ba đều có lý do và bằng chứng trong report.

## 2. Findings

Không có blocker / major.

### m-1 (minor) — số trên ghim đi qua `innerHTML` mà trình duyệt không kiểm

- Vị trí: `frontend/src/BanDoLich.jsx` — `L.divIcon({ html: String(item.thu_tu) })`. Leaflet gán `html` bằng `innerHTML`.
- Yêu cầu: plan §3 "trình duyệt kiểm lại trước khi vẽ"; file đã có `toaDoHopLe` cho toạ độ và lọc `map_url` theo `MAP_PREFIX`, nhưng `thu_tu` không được kiểm.
- Bằng chứng: `thu_tu` do code server dựng (`enumerate(ids, 1)`, `lich_trinh.py` `ban_do`) ⇒ hôm nay luôn là số nguyên. Thêm nữa, CSP `script-src 'self'` chặn trình xử lý nội dòng.
- Tác động: hiện **không khai thác được** (dữ liệu không từ model / người dùng). Chỉ là một chỗ HTML thô không cùng mức kiểm như hai trường bên cạnh.
- Tiêu chí đóng (khi tiện): chỉ vẽ ghim khi `Number.isInteger(item.thu_tu)`, hoặc dựng icon bằng `textContent`. Không cần đo lại có phí.

### m-2 (minor) — hai hàm kiểm toạ độ phía trình duyệt khác nhau

- Vị trí: `chat.jsx` `coToaDo` (2 số hữu hạn) ↔ `BanDoLich.jsx` `toaDoHopLe` (2 số trong khung Huế).
- Tác động: lịch mà mọi toạ độ đều hữu hạn nhưng ngoài khung Huế ⇒ vẫn tải chunk Leaflet, rồi chỉ hiện "chưa có vị trí". Server đã chặn toạ độ ngoài khung lúc khởi động (E thử phá 8 kiểu, mục 4) ⇒ ca này không xảy ra với dữ liệu đang chạy. Ghi nhận, không cần sửa.

### m-3 (minor, ngoài code) — độ phủ toạ độ thấp ở lịch thiên nhiên

- 17 / 28 điểm có toạ độ (E đếm lại: khớp report). Lịch 3 ngày thiên nhiên chỉ 1 / 6 điểm có ghim (số của B). Bản đồ nhiều ngày gần như trống là thứ User sẽ thấy khi demo.
- Đúng plan §3 ("không làm ở bậc này"). Nên đưa vào câu hỏi cho User cùng lúc với quyết định bật cờ: bổ sung toạ độ 11 điểm là việc dữ liệu riêng.

### Ghi nhận (không phải finding)

- `assetsInlineLimit: 0` áp cho cả bundle chính, nhưng bản build hiện tại không có ảnh nhỏ nào trong bundle chính (E liệt kê `dist/assets`: chỉ font ≥ 6,5 KB + 3 PNG của Leaflet) ⇒ hôm nay không đổi gì khi cờ tắt.
- Ô ghim dựng bằng DOM + `textContent`; link trong ô ghim là `map_url` đã lọc `MAP_PREFIX` ⇒ đúng plan.
- Allow-list deploy chưa có `diem_toa_do_v5.json` (report §5 đã ghi) ⇒ vào checklist deploy.

## 3. Cách người kiểm chạy lại thật

Worktree `/tmp/e_bd` (detached tại `d0adf31`, không đụng `/tmp/b_bando` của B), symlink `data/` + kho.

1. **Ca dò E 0 USD, khác cách B** (B kiểm 1 lịch 3 ngày): `data/phase_11/ban_do/e_review/do_ban_do.py` — `xep` thật trên bảng thật cho **mọi 432 tổ hợp** (số ngày × đi cùng × kiểu đi × sở thích, có cả `None`). Kiểm bất biến: cờ bật ⇒ **cùng điểm, cùng thứ tự** (tên + `map_url`) như cờ tắt; `thu_tu` = 1..k mỗi ngày; `buoi` sáng → chiều → tối; `toa_do` = bảng hoặc `None`; cờ tắt chỉ 2 trường. Thử phá `nap_toa_do` 8 kiểu + id lạ.
2. **Q1 cờ tắt:** `capture_all.py` (0 USD, không mạng) chạy **mới** trên `main` `1611d34` (thư mục chính, backend khớp `1611d34`) và trên nhánh (`ban_do_lich: false`); `cmp` hai file. Không dùng mốc `main_2a2a40e` của B.
3. **Server cờ tắt** (cổng 8853, build `npm ci && npm run build` của nhánh) + `data/phase_11/ban_do/e_review/co_tat.py`:
   - CSP header ở `/` và `/static/index.html` so **byte** với hằng `FRONTEND_CSP` import từ `main`;
   - Playwright 1440 + 390 qua 5 trang (`#/`, Khám phá, Lên kế hoạch, Giới thiệu, Trợ lý): mọi host được gọi, chunk `BanDoLich`, lỗi CSP / console / pageerror;
   - **1 lượt biểu mẫu thật** (2 ngày, có phí) ở 1440.
4. Test: `pytest tests/test_ban_do_lich.py tests/test_cong_dot_1.py tests/test_b6_tra_web.py tests/test_static_ui.py tests/test_b5_lich_trinh.py -q`.

## 4. Kết quả quan sát (lần chạy mới của E)

| Kiểm | Kết quả |
|---|---|
| Bất biến 432 tổ hợp | **0 sai** — cờ bật giữ đúng điểm + thứ tự của cờ tắt; `thu_tu` / `buoi` / `toa_do` đúng; cờ tắt đúng 2 trường. 17 / 28 điểm có toạ độ |
| Thử phá `nap_toa_do` | NaN, vô cực, chuỗi số, `True`, mảng, thiếu kinh độ, đảo (kinh, vĩ), ngoài khung (Hà Nội): **8 / 8 `ValueError`**; id không có trong bảng ⇒ bỏ qua đúng |
| Q1 chuỗi gửi model, cờ tắt | `main` 1611d34 ↔ nhánh: **giống byte** (228 dòng, mỗi dòng 2 lần bắt) |
| CSP cờ tắt | `/` và `/static/index.html`: **giống byte** hằng `FRONTEND_CSP` của `main` |
| Host được gọi, cờ tắt | 1440 + 390, 5 trang + 1 lượt biểu mẫu: chỉ `127.0.0.1:8853` — **0 host lạ**, **0 request chunk `BanDoLich`** |
| Lượt biểu mẫu cờ tắt | danh sách link cũ "Bản đồ từng điểm" 4 dòng, 0 `.bd`, 0 ghim (ảnh `e_review/co_tat/bieu_mau_co_tat_1440.png`) |
| Giới thiệu cờ tắt | vẫn "Chưa có bản đồ…", không có câu OpenStreetMap |
| Lỗi giao diện | 0 lỗi CSP / console / pageerror |
| `/api/tinh_nang` | có `ban_do_lich: false` |
| Test | **355 passed** (khớp số B sau rebase) |
| Log | 1 dòng `chat_metrics` (`success`) = 1 lượt; grep chữ câu biểu mẫu trong log = 0 |

**Tiền E: 0,00038 USD** (1 lượt biểu mẫu). Q1 + dò + test: 0.

**Dùng lại bằng chứng của B, không chạy lại:** Q-M1–Q-M6 cờ bật (ghim đúng 6 / 6 ngày, tile 66 / 66 từ đúng host, 0 lỗi CSP sau khi thêm `data:`, câu thường không tải chunk, cỡ chunk 44,54 KB, Referer chỉ gốc trang), T3 cờ bật, Q1 cờ bật.
- Lý do dùng lại: phần cờ bật sau rebase không đổi (rebase chỉ xung đột ở `vite.config.js` `define` + Giới thiệu); E build lại nhánh, cỡ chunk khớp B (44,54 KB JS / 2,63 KB CSS); 432 tổ hợp của E phủ phần dữ liệu cờ bật ở backend.

## 5. Giới hạn hoặc phần chưa chạy

- E **không** chạy trình duyệt khi cờ bật (Q-M1–Q-M6 là của B, xem mục 4). Vị trí ghim đúng chỗ bằng mắt là Q-M7 của User — chưa có nhận xét.
- Không thử cảnh OSM chặn tile (đúng plan §2.6).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Cờ tắt ⇒ chatbot y như `main` (CSP byte, chuỗi gửi model byte, 0 host lạ, giao diện lịch như cũ) ⇒ merge an toàn với cờ tắt.
Bật cờ là quyết định User / A, nên kèm:
- (1) User xem ảnh `data/phase_11/ban_do/anh_v2/` (Q-M7);
- (2) User biết độ phủ 17 / 28 (m-3);
- (3) đường ra mới tới OSM đã ghi trên Giới thiệu.

m-1 sửa khi tiện, không mở vòng review riêng. A merge + cổng ổn định trên `main`.
