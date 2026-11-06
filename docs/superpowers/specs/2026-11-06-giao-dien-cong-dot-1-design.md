# Spec — Giao diện cổng du lịch, đợt 1 (bản 1, nháp chờ review)

A viết 22:32 06/11/2026 (`date`). Nền `main` `c07e2df`. Mức rủi ro: **trung bình** (đổi giao diện người dùng thấy + 3 API chỉ đọc + một đường lịch trình mới do code quyết; không đổi kho, không đổi chỉ mục, không model / provider mới).

## 0. Căn cứ để review

1. `session_prompt/CURRENT_HANDOFF.md` — mục "Quyết định User tối 06/11 — giao diện" + "Quyết định User — lịch trình sau kín v2" (User chọn: dòng Nguồn; cổng mức 2, hai đợt; lịch trình qua biểu mẫu trước).
2. `data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md` §3 (15 mẫu nên học) + §4 (10 điều không chép) — B172 (private).
3. `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` §1–§8 — C211, mỗi ý có `file:hàm` (private).
4. Code: `backend/api/routes/chat.py` (`ChatRequest`, `SourceResponse`, `_source_responses`), `backend/llm/assistant.py` (`lich_trinh_for_turn`), `backend/api/app.py` (`FRONTEND_CSP`, `create_app`), `frontend/src/App.jsx`, `frontend/src/markdown.js`.

**Có bộ kín hay không:** **không** — đường biểu mẫu là code tất định (giá trị từ nút, code gọi công cụ), đo bằng bộ đã thấy chạy 2 lượt (luật cắt giảm 05/11, `Session_Prompt.md` §7 (2)).

## 1. Mục tiêu — 5 dòng khám phá (`propose-options` §4b)

1. **Vấn đề + đo bằng gì:** người xem thấy hue_rag là "một chatbot", trong khi đề tài là *ứng dụng hỗ trợ trải nghiệm* và hệ thống đã có kho 5 lĩnh vực, lịch trình, thời tiết, tra web, ảnh, (sắp) giọng nói — không tính năng nào thấy được trước khi gõ đúng câu. Đo bằng: **số tính năng chính tới được trong ≤ 2 lần bấm từ trang chủ** (đếm bằng Playwright) + User đọc / dùng thử và nhận xét (mốc người, không chấm điểm).
2. **Ba ô:** đo được (Playwright đếm, tiêu chí §6) · dữ liệu có (kho 204 file, API chat, công cụ đã merge — đợt 1 **không cần dữ liệu mới**) · giá trị = *làm khác đi* (lộ tính năng, đọc bài kho, lên lịch bằng nút) — không phải rẻ / nhanh hơn.
3. **Mốc đơn giản nhất:** giao diện hiện tại (`main`: một trang hỏi đáp, 5 chủ đề gợi ý, số nguồn trong câu).
4. **Tiêu chí thành công bằng số:** §6.
5. **Phương án B nếu dưới ngưỡng:** giữ khung cổng nhưng bỏ phần trượt (vd biểu mẫu lịch trình đo không đạt ⇒ ẩn biểu mẫu, giữ đường chat như `main`); không chặn phần còn lại.

## 2. Quyết định

| # | Quyết định | Ai / lý do | Cái giá |
|---|---|---|---|
| D1 | Câu trả lời **không hiện số `[n]` trong chữ**; dưới câu một dòng **"Nguồn: <tên> · <tên>"**, bấm mở đoạn gốc (đợt 1: khung nguồn hiện có; có `bai_id` ⇒ link trang bài Khám phá). Tầng máy giữ `[n]` + bộ kiểm citation như cũ | User 06/11 tối | mất "câu nào từ nguồn nào" trên giao diện |
| D2 | Cổng **mức 2** (như Huế TRIPO), **hai đợt**; đợt 1 = khung cổng từ cái đã có; đợt 2 = bản đồ, lưu trú, ăn uống theo cơ sở, sự kiện (spec riêng, sau nghiên cứu C209) | User 06/11 tối | ~1–1,5 tuần agent cho đợt 1 |
| D3 | **Lịch trình qua biểu mẫu "Lên kế hoạch" — code quyết hẳn** (C211 §2 cách (b)): `ChatRequest` thêm `bieu_mau: true` ⇒ bỏ định tuyến, **code gọi thẳng** `lich_trinh` với giá trị nút (nút thắng **cả 4 trường**), model chỉ viết lời theo khung; câu gõ tự do giữ như `main` (cờ `lich_trinh` vẫn tắt) | User chọn "biểu mẫu trước"; A chọn (b) vì biểu mẫu là lối vào chính và luật "trường bắt buộc ⇒ code" (hiện `assistant.py:lich_trinh_for_turn` cho tham số model thắng nút ở `di_cung` / `kieu_di` / `so_thich` — A đọc code xác nhận) | thêm một nhánh đường trả lời + cờ |
| D4 | Cờ mới `assistant.lich_trinh_bieu_mau` (tắt tới khi đạt §6 Q-F) — tách khỏi `lich_trinh` (câu tự do) | A | một cờ nữa |
| D5 | Điều hướng **bằng hash** (`#/`, `#/kham-pha/<linh_vuc>`, `#/kham-pha/bai/<id>`, `#/len-ke-hoach`, `#/tro-ly`, `#/gioi-thieu`); **0 gói router**, 0 đổi server / CSP | A (C211 §7) | URL có `#` |
| D6 | API chỉ đọc mới: `GET /api/kham_pha`, `GET /api/kham_pha/bai?id=` (chỉ `id` nằm nguyên văn trong `corpus.sources` của build record; lạ / `..` / `evaluation/` / tên có `sealed` ⇒ 404; cache RAM lúc khởi động), `GET /api/thoi_tiet` (từ `thoi_tiet.lay_du_bao`, cache 30 phút có sẵn, không gọi model, lỗi ⇒ ẩn ô), `GET /api/tinh_nang` (chỉ boolean các cờ) | A (C211 §1, §3, §5) | 4 route + test |
| D7 | `SourceResponse` thêm `bai_id` (đường dẫn bài khi nằm trong `corpus.sources`, khác ⇒ `null`) | A (C211 §4) | đổi khuôn JSON công khai ⇒ sửa test khuôn |
| D8 | Khung trợ lý: **nút nổi mọi trang** (laptop: khung ~380 × 560 góc phải, không rời trang; điện thoại: phủ màn) + trang `#/tro-ly` đầy đủ; **một** cuộc trò chuyện qua các trang (cookie đã có); điện thoại có **thanh dưới**, trợ lý là nút giữa | B172 mẫu #1, #2 | — |
| D9 | Trang chủ: ô hỏi lớn gửi thẳng trợ lý + chip gợi ý theo nhóm (câu mẫu viết mới — **không** câu Golden / kín) · 5 ô Khám phá (5 lĩnh vực kho) · thẻ "Lên kế hoạch" · ô thời tiết nhỏ (khi cờ bật) · dải "Trợ lý trả lời từ kho có nguồn, có thể sai" | B172 #3–#5, #13–#15 | — |
| D10 | Trang danh sách **một khuôn** cho 5 lĩnh vực (tiêu đề + chip loại con theo thư mục cấp 2 + lưới thẻ + "Xem thêm"); thẻ **chỉ hiện trường kho có** (tên, loại, 1–2 dòng tóm tắt) — không sao, không "Liên hệ", không giờ / giá chung chung | B172 #6, #7; tránh lỗi TRIPO §1.3 | — |
| D11 | Trang bài: đường dẫn · bài kho (Markdown qua `marked` + DOMPurify như hiện tại; link ngoài thêm `target="_blank" rel="noopener noreferrer"`) · **nút "Hỏi trợ lý về điểm này"** (mở khung chat với câu điền sẵn) · "bài khác cùng loại" | B172 #8, #9 | — |
| D12 | Trang `#/gioi-thieu`: trợ lý làm được gì, trả lời từ kho có nguồn, giới hạn (có thể sai, chưa có lưu trú / bản đồ — đợt 2), dữ liệu người dùng (cookie 30 phút, chỉ RAM, không lưu chữ) | B172 #13 | — |
| D13 | **Không chép** nhận diện cổng nhà nước (logo, tên, mascot, màu + bố cục y hệt, dòng bản quyền); không đăng nhập, đặt chỗ, sao đánh giá, "gần bạn" | B172 §4 | — |
| D14 | Thư viện: giữ React 19 + Vite 8 + Tailwind 4 + `marked` + DOMPurify + Be Vietnam Pro; **thêm tối đa 1 font tiêu đề** gói `@fontsource` nếu bản mẫu được chọn cần (A duyệt tên; `.npmrc` `before=` như cũ); 0 Radix / shadcn | A | — |

## 3. Câu hỏi cho User (trước khi code giao diện — mỗi lần một câu)

- **Q-U1 Hướng nhìn:** chọn 1 trong 3 bản mẫu HTML tĩnh của B (`data/nghien_cuu_giao_dien_2026-11-06/mau/`) — màu, chữ, cảm giác.
- **Q-U2 Ảnh:** kho gần như không có ảnh được phép dùng (B172: 2 file). (a) không ảnh — hình vẽ SVG / hoa văn / khối màu; (b) ảnh công khai có giấy phép mở (vd Wikimedia Commons) kèm dòng ghi công; (c) ảnh bạn tự chụp. Ảnh mới = dữ liệu mới ⇒ bạn quyết.
- **Q-U3 "Đi dày" trên biểu mẫu:** cột thời lượng từ kho không làm lịch dày hơn (E21, `data/phase_9/lich_trinh/diem_cho_user_v6.md`: 4 hướng). Mặc định nếu chưa quyết: **ẩn lựa chọn "đi dày"** khỏi biểu mẫu (không hứa điều code chưa làm được).
- **Q-U4 Ô thời tiết + công cụ thời tiết:** bật cờ `thoi_tiet` (B5b đã đạt luật ghi trước) để trang chủ có ô nhiệt độ hôm nay + trợ lý trả lời câu dự báo?
- **Q-U5 Tên hiển thị của cổng** (chữ ở đầu trang) — vd tên ngắn từ đề tài; không dùng tên giống cổng nhà nước.

## 4. Phạm vi

**Trong:** `frontend/src/` (khung cổng, trang chủ, Khám phá danh sách + bài, Lên kế hoạch, Trợ lý trang + nút nổi, Giới thiệu, dòng Nguồn, thanh dưới điện thoại); `backend/api/routes/` (4 route D6, `bai_id` D7, `bieu_mau` D3); `backend/llm/assistant.py` (đường biểu mẫu); `backend/config/settings.yaml` (cờ D4); test.
**Ngoài:** kho, chỉ mục, Qdrant, Golden; bản đồ, lưu trú / ăn uống theo cơ sở, sự kiện theo ngày (đợt 2); đổi lời dặn model; đường câu gõ tự do của lịch trình (giữ `main`); Sửa 1 / Sửa 2 của E20; đăng nhập / lưu lịch trình; tiếng Anh.

## 5. Bước

| Bước | Ai | Việc | Đầu ra |
|---|---|---|---|
| S0 | B (B173) → User | 3 bản mẫu tĩnh ⇒ User chọn Q-U1; A hỏi Q-U2 … Q-U5 | lựa chọn ghi vào §3 bản 2 |
| S1 | B | Backend: D3 + D4 + D6 + D7 + test; Q1 228 / 228 giống byte (cờ mới tắt) + Q1m (cờ `lich_trinh_bieu_mau` bật) | nhánh `p11-cong-dot-1` |
| S2 | B | Frontend theo bản mẫu đã chọn: D1, D5, D8–D12 | cùng nhánh |
| S3 | C | Đo đường biểu mẫu (§6 Q-F) trên bộ đã thấy ×2; Playwright §6 | report đo |
| S4 | C (hoặc E) | Review cả nhánh một lần (`risk-gated-agent-review`) | review |
| S5 | A | Merge (cờ `lich_trinh_bieu_mau` theo kết quả Q-F) + cổng ổn định + báo cáo (`LUONG_HOAT_DONG_HE_THONG.md` đổi — người dùng thấy giao diện mới) ⇒ User dùng thử | — |

## 6. Tiêu chí nghiệm thu (ghi trước)

- **Q-K (Khám phá):** `/api/kham_pha` trả đúng **204 / 204** bài của `corpus.sources`, đúng 5 lĩnh vực; 0 bài ngoài danh sách; `id` ngoài danh sách / `..` / `evaluation/…` / có `sealed` ⇒ 404 (test).
- **Q-N (Nguồn):** trên 10 câu tự viết có trích dẫn (Playwright): **0** số `[n]` / chip số hiện trong chữ; tập tên ở dòng "Nguồn" = tập nguồn được trích của câu đó (so với `sources` của API) 10 / 10.
- **Q-F (biểu mẫu lịch trình — quyết bật cờ):** ≥ 12 tổ hợp biểu mẫu tự viết (đủ 6 kiểu "đi cùng ai", có / không sở thích, 1 / 2 / 3 ngày), chạy **×2**: khung lịch nhận **đúng 4 giá trị chọn** 24 / 24 (code đếm); **0** thẻ hỏi lại; **0** lượt chữ model là câu từ chối thay lịch; sàn Q2 B5 (code đếm: 0 điểm ngoài bảng, 0 giờ / giá, 0 vi phạm luật xếp) 24 / 24; 2 sub-agent Claude chấm (iii) "không thêm điều sai" ≥ 11 / 12 **mỗi lượt**. Trượt ⇒ cờ tắt, biểu mẫu ẩn (phương án B §1).
- **Q-G (giao diện):** Playwright 1440 + 390: mọi trang hash mở được và tải lại đúng trang; **0 lỗi CSP**, 0 lỗi console; cờ tắt ⇒ mục tương ứng ẩn; ≥ **6** tính năng chính (hỏi trợ lý, 5 lĩnh vực Khám phá, Lên kế hoạch khi bật, thời tiết khi bật, Giới thiệu, hỏi bằng ảnh khi bật) tới được trong ≤ 2 lần bấm từ trang chủ; chữ chính tương phản ≥ 4,5 : 1; bundle JS gzip ≤ 200 KB.
- **Q-C (chat không hỏng):** Q1 228 / 228 giống byte `main` khi cờ mới tắt; cổng ổn định (`/health` 5 / 5, 1 câu trong kho + 1 ngoài kho, `chat_metrics` = số câu, 0 câu hỏi trong log); stream, nhớ 3 lượt, 👍 / 👎, "Cuộc trò chuyện mới" chạy như `main` trong khung nổi lẫn trang trợ lý.
- **Tiền:** ≤ **0,03 USD** (Q-F ≈ 24 × ~0,0006 + cổng); vượt dự phóng ⇒ dừng, báo A.

## 7. Bảng rà khung AI FDE (nhẹ — `agent-design-review` + `agent-security-review`)

| Mục | Hiện trạng | Khớp / lệch | Đề xuất |
|---|---|---|---|
| Trường bắt buộc ⇒ code | `assistant.py:lich_trinh_for_turn` — tham số model thắng nút ở 3 trường | **lệch** | D3: đường biểu mẫu code gọi công cụ, nút thắng cả 4 trường |
| Có cần model không | Khám phá / thời tiết / tính năng = dữ liệu tĩnh | khớp | D6 không gọi model |
| Nguồn dữ liệu mới | không (kho 204 file đã có, Open-Meteo đã có ở B5b) | khớp | — |
| Đường ra mới | `/api/thoi_tiet` gọi Open-Meteo **từ server** (không gửi gì của người dùng; ≤ 1 lần / 30 phút) | khớp | CSP trình duyệt không đổi |
| Chữ người dùng là dữ liệu | `id` bài từ URL | rủi ro đọc file tuỳ ý | D6: so nguyên chuỗi với `corpus.sources`, không ghép đường dẫn; test `..` / `evaluation/` / `sealed` |
| Hiển thị nội dung | Markdown kho + câu trả lời qua DOMPurify | khớp | thêm `rel="noopener noreferrer"` link ngoài (C211 §1 phát hiện) |
| Dữ liệu cá nhân | cookie 30 phút, RAM | khớp | nói ra ở D12 |
| Bộ ba chết người (dữ liệu riêng · nội dung lạ · kênh ra) | không thêm kênh ra | khớp | — |

## 8. Quyền, tiền, rủi ro

- Quyền: trong quyền phiên (A tự điều phối; B / C push nhánh riêng); spec này User duyệt một lần (sha từ file) trước S1. Font tiêu đề mới (nếu có) A duyệt.
- Tiền: §6.
- Rủi ro: (1) thời gian — đợt 1 tranh giờ với Phase 9 B7 / Phase 10 / deploy (đóng code 25–30/12) ⇒ đợt 1 giữ đúng phạm vi §4; (2) giống trang nhà nước ⇒ D13; (3) bài kho dài, đọc trên điện thoại khó ⇒ thu gọn "Đọc thêm"; (4) không ảnh ⇒ phụ thuộc Q-U2; (5) khung nổi + trang trợ lý dùng chung một cuộc ⇒ test chuyển trang giữa lúc đang stream.

## Chỗ đổi

- Bản 1 (22:32 06/11/2026): bản đầu.
