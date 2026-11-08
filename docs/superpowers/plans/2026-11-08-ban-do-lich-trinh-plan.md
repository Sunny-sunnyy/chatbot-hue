# Plan — bản đồ lịch trình (P1 đợt 2 cổng)

Người viết: B · bản 1 · 09:35 08/11/2026 (`date`) · trạng thái: **chờ review** (A chọn người, ≤ 2 vòng) ⇒ A duyệt ⇒ code trên nhánh riêng.
Nguồn: User 08/11 chọn làm bản đồ trước đóng gói (A giao). Đầu vào: `report_agent/2026-11-06_giao_dien_cong/c209_implementation.md` (P1 / P2, tile, CSP),
spec cổng đợt 1 `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` (D2: bản đồ thuộc đợt 2; D12: Giới thiệu đang ghi "chưa có bản đồ"),
`data/phase_9/lich_trinh/diem_toa_do_v5.json` + `toa_do_ghi_chu.md`, code lịch hiện tại.

## 1. Vấn đề + đo bằng gì

Lịch trình (biểu mẫu "Lên kế hoạch", đang bật) chỉ có chữ + danh sách link Google Maps từng điểm. Người xem không thấy các điểm nằm đâu, ngày nào đi cụm
nào. **Đo:** người dùng thấy được trên **một** bản đồ các điểm của từng ngày, đánh số đúng thứ tự trong lịch (kiểm tất định: số ghim = số điểm có toạ
độ, số trên ghim = thứ tự trong khung do code xếp) + User xem ảnh chụp, nhận xét (mốc người, không chấm điểm).

**Không cần model:** toạ độ, thứ tự, số ghim đều do code dựng từ bảng ⇒ không lời dặn mới, không lượt model mới (luật AI FDE: dữ liệu / thứ tự bắt buộc
⇒ code). Không có **bộ kín** (chỉ hiển thị tất định — `Session_Prompt.md` §7 cắt giảm (2)).

## 2. Người dùng thấy gì

Dưới câu trả lời có lịch (đúng chỗ khối "Bản đồ từng điểm" hiện nay — `frontend/src/chat.jsx:380` `LichExtras`):

1. **Thanh chọn ngày** "Ngày 1 · Ngày 2 · …" (chỉ hiện khi lịch ≥ 2 ngày); mặc định Ngày 1.
2. **Bản đồ** cao 260 px (điện thoại 220 px), khung tự vừa các ghim của ngày đang chọn. Mỗi điểm một **ghim tròn có số** 1, 2, 3… theo thứ tự trong ngày
   (sáng → chiều → tối, trong một buổi theo thứ tự khung). Bấm ghim ⇒ ô nhỏ: tên điểm · buổi · link "Mở Google Maps" (link cũ, code dựng).
   **Không vẽ đường nối** — không có dữ liệu đường đi thật; đường thẳng dễ bị hiểu là lộ trình.
3. **Dòng ghi công** góc phải dưới, luôn hiện (luật OSM): "© OpenStreetMap contributors · Toạ độ: dữ liệu mở thành phố Huế".
4. **Danh sách điểm** dưới bản đồ (giữ danh sách link Google Maps hiện nay, thêm số thứ tự trùng số ghim). Điểm **không có toạ độ** vẫn nằm trong danh
   sách, có nhãn "chưa có trên bản đồ", không có ghim.
5. Ngày không có điểm nào có toạ độ ⇒ không vẽ bản đồ cho ngày đó, chỉ danh sách + dòng "Các điểm ngày này chưa có vị trí trên bản đồ".
6. Không tải được ảnh bản đồ (mất mạng, OSM chặn) ⇒ nền xám của thư viện; danh sách + link Google Maps vẫn dùng được. Không thêm cơ chế dự phòng.

Trang Giới thiệu: mục "Giới hạn" bỏ "Chưa có bản đồ"; mục "Dữ liệu của bạn" thêm một câu: "Khi lịch có bản đồ, trình duyệt của bạn tải ảnh bản đồ từ máy
chủ OpenStreetMap — máy chủ đó nhận địa chỉ IP và vùng bản đồ bạn đang xem." (đường ra mới, §5).

## 3. Dữ liệu — toạ độ do code gắn

- **Bảng toạ độ:** `data/phase_9/lich_trinh/diem_toa_do_v5.json` (C204: 33 điểm, nguồn data.hue.gov.vn bản tải 05/08/2026, khớp tên chặt, mơ hồ ⇒
  `null`). Bảng lịch đang chạy là `diem_v3.json` (28 điểm, `backend/config/settings.yaml:71`) ⇒ **17 / 28 điểm có toạ độ**; 11 thiếu (phần lớn là cảnh / phố:
  phố cổ, 3 phố đi bộ, núi, đồi, đầm, phá, bãi biển, vườn quốc gia, thác — `toa_do_ghi_chu.md`). 5 điểm thêm của v5 không có trong v3 ⇒ bỏ qua.
- **Nạp lúc khởi động** (cạnh `nap_bang_lich`, `backend/llm/assistant.py:115`): settings mới `lich_trinh_toa_do: ../data/phase_9/lich_trinh/diem_toa_do_v5.json`;
  chỉ nạp khi cờ `ban_do_lich` bật. Kiểm: mỗi toạ độ khác `null` là 2 số nằm trong khung Huế (vĩ độ 16,0–16,8; kinh độ 107,0–108,0) và `id` có trong bảng
  lịch hoặc bị bỏ qua — sai khung ⇒ `ValueError`, không khởi động (cùng kiểu `nap_bang`).
- **Gắn vào dữ liệu giao diện:** `lich_trinh.ban_do` (`backend/llm/lich_trinh.py:424`) hiện trả `[{ten, map_url}]` theo `diem_trong_khung` ⇒ thêm `ngay`,
  `buoi`, `thu_tu` (thứ tự trong ngày, từ 1) và `toa_do` (`[vĩ độ, kinh độ]` hoặc `null`). Cờ tắt ⇒ khuôn **giữ nguyên** như hiện nay.
- Dữ liệu này chỉ đi tới **giao diện** (sự kiện SSE `lich_trinh`, `lich_cho_giao_dien` `backend/llm/assistant.py:630`); **chuỗi gửi model không đổi** —
  model không thấy, không tạo, không sửa toạ độ.
- **Trình duyệt kiểm lại** trước khi vẽ (như `MAP_PREFIX` hiện có, `chat.jsx:28`): `toa_do` phải là 2 số hữu hạn trong khung Huế, không thì coi như
  `null`.
- **Không làm ở bậc này:** bổ sung toạ độ 11 điểm thiếu (cần nguồn mới — OSM hoặc nhập tay — và User kiểm bằng mắt từng điểm ⇒ việc dữ liệu riêng, User
  quyết); đổi link Google Maps sang toạ độ (đề xuất C197, A quyết riêng); ghim quán ăn / lưu trú (P3).

## 4. Thư viện + nguồn ảnh bản đồ

| Phương án | Đổi gì | Tốn gì | Khi nào sai | Chọn khác mất gì |
|---|---|---|---|---|
| **(a) Leaflet 1.9.4 + tile ảnh OSM — khuyến nghị** | 1 gói npm (BSD-2, không phụ thuộc, phát hành 05/2023 — trước mốc `.npmrc` `before=2026-10-19`); CSP thêm 1 host ảnh | JS ước ~40 KB gzip (đo khi code), **tải riêng** chỉ khi có lịch có toạ độ | OSM "best-effort, không SLA", có thể chặn khi dùng nặng / thương mại — đồ án lưu lượng thấp nên ít khả năng; nếu bị chặn chỉ mất ảnh nền | — |
| (b) MapLibre GL + OpenFreeMap | gói lớn (~200 KB+ gzip), cần WebGL; tile vector + glyph + sprite ⇒ CSP thêm `connect-src` và có thể `worker-src blob:` | nặng gấp ~5 lần; nhiều host hơn | máy yếu / trình duyệt tắt WebGL ⇒ không bản đồ | được: không lo luật dùng tile OSMF, cho thương mại |
| (c) MapLibre + PMTiles tự host (P2 của C209) | 0 host ngoài | dung lượng tile vùng Huế **chưa đo**; thêm bước dựng tile + chỗ để | — | được: 0 đường ra mới. Mất: thêm việc dữ liệu + deploy |
| (d) Không bản đồ, giữ danh sách link | 0 | 0 | — | không đạt mục tiêu §1 |

Lý do khuyến nghị (a): nhỏ nhất đủ nhu cầu (17 ghim tĩnh, không cần tile vector / xoay / 3D); CSP chỉ thêm một host ảnh; Leaflet chạy được dưới CSP hiện
tại (không `eval`, không `<style>` chèn — chỉ đặt style qua CSSOM, không bị `style-src 'self'` chặn) — **phải đo trên bản build FastAPI**, sai ⇒ dừng, báo A.
Chuyển sang (c) sau này chỉ đổi lớp ảnh nền, phần dữ liệu §3 giữ nguyên.

Chi tiết dùng Leaflet:
- `import("leaflet")` động ⇒ Vite tách chunk riêng; bundle chính chỉ tăng phần component bản đồ.
- CSS của Leaflet import qua Vite (file `.css` cùng gốc — hợp `style-src 'self'`).
- Ghim bằng `L.divIcon` (một `<div>` có số, CSS của mình) ⇒ không dùng ảnh ghim mặc định của Leaflet (đường dẫn ảnh hay vỡ khi bundle).
- Tile `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, `maxZoom` 18, `attributionControl` bật.
- Không tải trước vùng, không lưu offline (luật OSMF cấm).
- Không đặt `Referrer-Policy` chặn Referer (luật OSMF đòi Referer; mặc định trình duyệt chỉ gửi gốc trang).

## 5. CSP và đường ra mới

- CSP hiện tại (`backend/api/app.py:47` `FRONTEND_CSP`): `img-src 'self' blob:`, `connect-src 'self'`, không host ngoài.
- **Đổi:** cờ `ban_do_lich` bật ⇒ `img-src 'self' blob: https://tile.openstreetmap.org`. Cờ tắt ⇒ CSP **giữ nguyên byte**. Không đổi `connect-src`,
  `script-src`, `style-src` (Leaflet tải ảnh nền bằng thẻ `<img>`, không `fetch`).
- **Gửi ra ngoài (mới):** trình duyệt người dùng ⇒ máy chủ tile OSMF: IP, vùng + mức zoom đang xem (gần đúng các cụm điểm trong lịch), User-Agent,
  Referer = gốc trang. **Không** gửi chữ câu hỏi / câu trả lời / cookie của trang (khác gốc). Server hue_rag không gọi OSM.
- Ghi trên trang Giới thiệu (§2).

## 6. Cờ, cỡ, file sẽ sửa

- Cờ `settings.yaml` `assistant.ban_do_lich: false` (mặc định tắt); `/api/tinh_nang` thêm `ban_do_lich` để giao diện biết (`backend/api/routes/cong.py:106`).
  Bật = A / User quyết sau khi đạt §7.
- Cỡ: bundle chính tăng ≤ 3 KB gzip; chunk bản đồ (Leaflet + component) ≤ 60 KB gzip JS + ≤ 5 KB CSS; chỉ tải khi có lịch có ≥ 1 toạ độ.
- File:
  - backend: `backend/llm/lich_trinh.py` (`ban_do` + nạp toạ độ), `backend/llm/assistant.py` (cờ + nạp), `backend/config/settings.yaml`, `backend/api/app.py`
    (CSP theo cờ), `backend/api/routes/cong.py` (`tinh_nang`);
  - frontend: `frontend/package.json` + `package-lock.json` (`leaflet` 1.9.4), `frontend/src/BanDoLich.jsx` (mới), `frontend/src/chat.jsx` (`LichExtras` gọi bản
    đồ), `frontend/src/pages.jsx` (Giới thiệu), `frontend/src/index.css`;
  - test (§7); deploy nháp (nhánh `p12-deploy-nhap`): allow-list `dung_dockerignore.py` thêm `diem_toa_do_v5.json` — ghi vào checklist deploy, không sửa
    ở nhánh này.

## 7. Test + tiêu chí nghiệm thu (ghi trước)

**Test tự động (0 USD):**
- T1 `ban_do` với cờ bật: điểm có toạ độ ⇒ `toa_do` đúng bảng; điểm thiếu ⇒ `null`; `ngay` / `buoi` / `thu_tu` khớp khung (1 lịch 3 ngày dựng bằng `xep`
  thật trên bảng thật). Cờ tắt ⇒ khuôn cũ (khoá tập trường).
- T2 nạp bảng toạ độ: toạ độ ngoài khung Huế / không phải số ⇒ `ValueError`.
- T3 CSP: cờ tắt ⇒ giống byte chuỗi hiện nay; cờ bật ⇒ thêm đúng một host ở `img-src`, phần còn lại giống byte.
- T4 Q1: chuỗi gửi model 228 / 228 giống byte với mốc `main` (`capture_all.py`), cờ `ban_do_lich` tắt và bật.
- `test_static_ui.py` (CSP, không script nội dòng, không `eval` trong mọi chunk — test hiện có quét `assets/*.js` nên bắt cả chunk Leaflet).

**Kiểm trên hệ thống thật (bản build do FastAPI phục vụ, Playwright 1440 + 390), cờ bật trên server thử:**
- Q-M1: 3 lượt biểu mẫu thật (1 / 2 / 3 ngày, sở thích khác nhau) — **≈ 0,0015 USD** (3 lượt luna; trần 0,005). Mỗi lượt: số ghim mỗi ngày = số điểm có
  toạ độ của ngày đó trong sự kiện `lich_trinh`; số trên ghim = `thu_tu`; danh sách có đủ điểm, điểm thiếu có nhãn.
- Q-M2: **0 lỗi CSP / console / pageerror**; ảnh tile trả 200 từ đúng `tile.openstreetmap.org`; không request tới host nào khác ngoài trang + host đó.
- Q-M3: dòng ghi công hiện trong khung bản đồ ở cả 2 cỡ màn.
- Q-M4: câu thường (không lịch) ⇒ 0 request tới host tile, chunk bản đồ **không** tải.
- Q-M5: cỡ bundle như §6.
- Q-M6: chữ câu hỏi không có trong URL / header nào gửi tới host tile (đọc request Playwright).
- Q-M7: ảnh chụp 3 lượt × 2 cỡ màn ⇒ A đưa User xem (vị trí ghim đúng chỗ bằng mắt — toạ độ dữ liệu mở có thể lệch vài trăm mét, C197).
- Cổng ổn định như handoff (`/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho, `chat_metrics` = số câu, grep câu hỏi trong log = 0).

**Đạt** = T1–T4 + `test_static_ui` đạt và Q-M1–Q-M6 đạt hết; Q-M7 là nhận xét của User (không chấm). Q-M2 có lỗi CSP do Leaflet ⇒ dừng, báo A (không tự
nới CSP ngoài `img-src`).

## 8. Bảng rà ngắn — `agent-security-review` (chỉ mục chạm)

| Mục | Hiện trạng | Mức | Đề xuất / đã có trong plan |
|---|---|---|---|
| 1. Bộ ba chết người | không thêm công cụ / nguồn vào ngữ cảnh model; đường ra mới đi từ **trình duyệt**, không từ agent | — | không đổi |
| 3. Giới hạn ở code, không ở lời dặn | toạ độ từ bảng do code nạp + kiểm khung lúc khởi động; trình duyệt kiểm lại trước khi vẽ | minor | §3 (đã có) |
| 4. Tham số vào URL | URL tile chỉ chứa z / x / y do Leaflet tính; không chữ người dùng, không chữ model | — | Q-M6 |
| 5. Dữ liệu cá nhân / đường ra | IP + vùng xem tới OSMF (mới) | minor | ghi trên Giới thiệu (§2); cờ tắt ⇒ 0 request |
| CSP | thêm đúng 1 host ở `img-src`, theo cờ | minor | T3 + Q-M2 |
| Chuỗi cung ứng | gói mới `leaflet` 1.9.4 (0 phụ thuộc, 2023), `.npmrc` `ignore-scripts` + `before` giữ | minor | review lockfile chỉ thêm 1 gói |
| Phụ thuộc dịch vụ ngoài | OSMF best-effort, có thể chặn | minor | mất ảnh nền, danh sách vẫn dùng được (§2.6); deploy công khai lưu lượng lớn ⇒ xét (c) |

`agent-design-review`: không agent / công cụ / vòng lặp mới; chia việc code ↔ model đúng luật (toạ độ, thứ tự, số ghim = code; model chỉ viết lời lịch
như hiện nay). Không còn mục khác chạm.

## 9. Tiền, thời gian, ngoài phạm vi

- Tiền: ≈ 0,0015 USD (Q-M1) + 2 câu cổng ổn định ≈ 0,0006 ⇒ trần **0,005 USD**. Không đổi model, không đổi kho / chỉ mục.
- Thời gian ước: ~½ ngày code + kiểm.
- Ngoài: toạ độ 11 điểm thiếu; ghim quán / lưu trú / sự kiện (P3); đường đi thật; câu gõ tự do của lịch (cờ `lich_trinh` vẫn tắt); tile tự host (c).

## 10. Cần A quyết (trước khi code)

1. Phương án (a) Leaflet + tile OSM — đồng ý? (đổi sang (c) thì plan thêm bước dựng tile + đo dung lượng.)
2. Chỗ hiện bản đồ: chỉ dưới câu trả lời có lịch (plan này). Có cần thêm bản đồ trên trang "Lên kế hoạch" không? (B đề xuất **không** — cùng một lịch,
   hiện hai chỗ là thừa.)
3. Bổ sung toạ độ 11 điểm thiếu — để việc dữ liệu riêng sau (User quyết) hay gộp vào? (B đề xuất **để riêng**: cần User kiểm từng điểm.)
