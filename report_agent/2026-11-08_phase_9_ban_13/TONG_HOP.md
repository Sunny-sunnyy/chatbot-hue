# TỔNG HỢP đợt `2026-11-08_phase_9_ban_13` — chốt phạm vi trước đóng gói, spec bản 13, việc nhỏ (NHÁP)

C viết nháp 12:15 08/11/2026 (`date`), A duyệt / sửa lúc kết phiên. Chỗ ghi "(B / E cập nhật lúc kết phiên)" là phần B / E chưa xong khi viết.
File tracked, repo public: không chép nội dung kho, câu Golden, câu kín; câu đo tả ở mức loại câu.

**Mã dùng trong file (giải nghĩa):** spec bản 13 = mục §12 thêm vào tài liệu thiết kế Phase 9 ngày 08/11 · G = cổng 2 nhóm (định tuyến chỉ còn "trò chuyện xã giao" / "về Huế") ·
T1 = công cụ ngày + âm lịch · T2 = tra web thành công cụ · T3 = bảng vé + giờ mở cửa · T4 = lịch trình từ câu gõ tự do · cờ = công tắc bật / tắt tính năng trong `settings.yaml` ·
S1–S6 = các sàn đo chung của spec §12.3 (S1 bộ an toàn 32 câu đủ 4 số; S2 / S2b câu ngoài phạm vi không bị trả lời / không có mục web; S3 / S3b câu về Huế không bị xếp nhầm;
S4 chất lượng mẫu Golden 30; S5 tốc độ; S6 tiền) · Q1 = chuỗi gửi model giống từng byte bản cũ khi cờ tắt · "mức nhẹ" = luật User 08/11 cho việc nhỏ (plan 1 trang, đo 1 lượt).

## Mục tiêu

- **Chốt phạm vi trước đóng gói** (User 09:29 08/11/2026): ngoài phần bắt buộc (so sánh cuối B7, đóng gói, báo cáo) làm thêm bản đồ lịch trình · bật hỏi bằng ảnh · giữ giọng nói;
  không làm giao diện tiếng Anh; rà mọi file `.md` tìm tính năng đã ghi mà chưa làm.
- **Spec bản 13** (User 10:30–10:46 08/11): đổi định tuyến thành 2 nhóm, bỏ tuyến khẩn cấp, câu ngoài phạm vi do trợ lý Huế tự từ chối; thêm 4 công cụ T1–T4.
- **Làm nhanh, ít tốn thời gian test** (User 11:02 + 11:29 08/11): bỏ mốc ngày; "mức nhẹ" cho việc nhỏ; 5 cách giảm thời gian test.

## Quyết định theo giờ (giờ A ghi nhận bằng `date`; nguồn `session_prompt/CURRENT_HANDOFF.md` mục 2b–2d, spec §12.8)

| Giờ (08/11) | Ai | Quyết định |
|---|---|---|
| 09:27 | User | Chưa deploy; chỉ deploy khi đủ tính năng, ổn định, đóng gói + Docker đầy đủ |
| 09:29 | User | Phạm vi thêm: bản đồ lịch trình · bật hỏi bằng ảnh · giữ giọng nói; không tiếng Anh; rà `.md` tìm tính năng chưa làm |
| 09:37 | A | Duyệt plan bản đồ lịch trình (cờ `ban_do_lich` tắt mặc định) |
| 09:58 (A ghi nhận) | User | Duyệt "Nhóm 1 + 2" — 14 việc nhỏ trước đóng gói (chia B / C / E) |
| 10:30 | User | Định tuyến 2 nhóm; bỏ tuyến khẩn cấp (không câu soạn sẵn, không công cụ); câu ngoài phạm vi ⇒ trợ lý Huế tự từ chối, giữ sàn 0 câu ngoài kho bị trả lời |
| 10:38 | User | Làm cả 4 công cụ T1–T4; trần tiền Phase 9 nâng 2,5 ⇒ **3,5 USD** (quỹ so sánh cuối B7 0,35 giữ riêng) |
| 10:46 | User | Thứ tự: C viết spec cả gói ⇒ review ≤ 2 vòng ⇒ đợt 1 song song (B G · E T1 · C T3) ⇒ đợt 2 (T2 rồi T4) |
| 10:56 | User | T2: trợ lý **chỉ quyết lúc tra web**; code dựng câu tra, tra, viết mục web riêng; trợ lý không đọc chữ web |
| 11:01 | User | **Duyệt spec bản 13** (sha `5557f0fd7650`) |
| 11:02 | User | Bỏ mốc ngày, làm càng nhanh càng tốt (sàn + trần tiền giữ) |
| 11:10 | User | Bảng T3: 14 chỗ kho tự ghi khác nhau ⇒ hiện cả hai nguyên văn kèm nguồn; câu 2–5 của phiếu A theo khuyến nghị C |
| 11:13 · 11:17 · 11:29 | A | Duyệt plan T3 bản 2 · plan G bản 2 · plan T1 bản 2 |
| 11:29 | User | "Mức nhẹ" cho việc nhỏ (≤ 0,2 USD, không đổi kiến trúc: plan 1 trang A duyệt, đo 1 lượt — riêng bộ an toàn 2 lượt — 1 review cả nhánh, không bộ kín) + 5 cách giảm thời gian test |
| 12:04 | User | G: nâng mức dừng tiền lên 0,75 USD, cho chỉnh lời dặn nhiều vòng, ghi báo cáo đủ |
| 12:04 (A ghi nhận) | User | T3: duyệt vòng 3 (ngoài plan) để sửa một lỗi code thật, không nới sàn |
| 08/11 (spec §12.8) | User | Câu khẩn cấp có thể nhận câu từ chối thường (A đã nêu rủi ro, User chấp nhận) · câu "hỏi về chính trợ lý" = trò chuyện xã giao (A) |

## Kết quả từng việc

| Việc | Kết quả | Số chính | Hồ sơ |
|---|---|---|---|
| Rà tính năng đã ghi mà chưa làm | xong | C: 31 ý người dùng thấy + 47 ý kỹ thuật · E: 22 + 21 | `data/ra_soat_tinh_nang_2026-11-08/{C,E}.md` (private) |
| 7 ảnh cổng | **vào `main`** `c9931be` | ảnh không giấy phép mở chưa từng vào git (quét toàn bộ lịch sử); 7 / 7 ghi công đúng | `report_agent/2026-11-06_giao_dien_cong/c_anh_cong_review.md` |
| Bật hỏi bằng ảnh trên cổng | **vào `main`** `3da1cb1` + cờ `anh.bat` **bật** `cf57309` | thẻ gợi ý không che câu trả lời (390 + 1440); câu riêng tư ở trang Giới thiệu đúng với code (ảnh có toạ độ GPS ⇒ đầu ra sạch) | `report_agent/2026-11-05_phase_10_anh/e_bat_anh_implementation.md`, `c_bat_anh_review.md` |
| Bản đồ lịch trình | **vào `main`** `a4fde29`, cờ `ban_do_lich` **tắt** (chờ User xem ảnh + phiếu toạ độ 11 điểm) | 0,00306 USD | `report_agent/2026-11-06_giao_dien_cong/b_ban_do_implementation.md` |
| Việc nhỏ Nhóm 1 + 2 — B (sao chép / tải lịch, buổi tối chỉ khi có sở thích; link Maps theo toạ độ **bỏ**) | **vào `main`** `1ff425c` | — | `report_agent/2026-11-06_giao_dien_cong/b_lich_nho_implementation.md` |
| Việc nhỏ — E (nút Dừng huỷ lần gọi model, ô chat 500 ký tự, gợi ý dưới câu từ chối của kho, dòng "Nguồn" gộp theo bài, lỗi stream huỷ lần gọi) | **vào `main`** `56b8baa` | — | `report_agent/2026-11-06_giao_dien_cong/e_viec_nho_implementation.md` |
| Việc nhỏ — C (tóm tắt thẻ Khám phá, nút "Báo thông tin chưa đúng", ảnh nhỏ cho điện thoại, link "Nguồn ảnh", số trong mục web phải có trong kết quả tìm, mã lượt trong log số đo) | **vào `main`** `ad21b6c` | 100 / 204 thẻ bỏ nhãn trường · trang chủ trên điện thoại 424 ⇒ 148 KB · Khám phá 447 ⇒ 107 KB · ≈ 0,009 USD | `report_agent/2026-11-06_giao_dien_cong/c_viec_nho_implementation.md` |
| Spec bản 13 | **User duyệt** `5557f0fd7650` sau 2 vòng review | — | `docs/superpowers/specs/2026-11-02-phase-9-design.md` §12 + `…design_review_v13.md` |
| **G** cổng 2 nhóm | **đang chỉnh** (nhánh `p9-g-cong`) | định tuyến đạt S3; cả câu: S2 0 / 48 đạt, S2b trượt 5–7 / 48 (câu về nơi khác ⇒ trợ lý trả "không đủ thông tin" ⇒ mở tra web) ⇒ User cho chỉnh nhiều vòng | `report_agent/2026-11-08_phase_9_ban_13/b_g_cong_implementation.md` — (B cập nhật lúc kết phiên) |
| **T1** ngày + âm lịch | **đạt, chờ review nhánh** `p9-t1-ngay` | lượt 3: 2 người chấm mù khớp 27 / 27; câu từ chối nhầm được cứu 8; lỗi nói chắc không căn cứ / sai ngày 0; `max_turns` 0; tiền ≤ 0,112 / 0,13 | `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md` — (E cập nhật lúc kết phiên) |
| **T3** bảng vé + giờ mở cửa | **âm theo luật ghi trước — cờ tắt, chờ User chọn hướng** | bảng 60 điểm (User duyệt; 1.011 / 1.011 chuỗi kiểm đúng dòng kho) · Q2 (20 câu): `main` 16 · vòng 1 17 · vòng 2 18 · vòng 3 **19** / 20 (sàn 19 ✓) · khối điều kiện 4 / 4 ✓ · **sàn Q3 trượt 6 / 10** (model tự nêu điều kiện miễn giảm, chép từ đoạn kho) · ≈ 0,085 USD | `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` |
| T2, T4 | chưa mở (đợt 2, sau khi G vào `main`) | — | — |

## Tiền (USD, từ report / STATUS — số log `chat_metrics`)

| Session | Hôm nay | Gồm |
|---|---|---|
| C | ≈ 0,096 | review bật ảnh 0,0020 · việc nhỏ ≈ 0,009 · T3 0,0853 (Q2 4 lượt + sinh bộ an toàn nhánh ×2) |
| E | ≈ 0,128 (cận trên) | T1 ≤ 0,112 · kiểm bật ảnh 0,0083 (Phase 10) · review C ≈ 0,0004 |
| B | (B cập nhật lúc kết phiên) | bản đồ 0,00306 · G (đang chạy, mức dừng 0,75) |
| A | ≈ 0,003 | 4 lượt cổng ổn định trên `main` (mỗi lượt 2 câu chat, 1 lượt thêm 1 ảnh); tra cứu Codex và các sub-agent review / viết bộ đo = quota tài khoản, 0 USD API |

Phase 9: trần **3,5** (đã dùng ≈ 2,05 trước hôm nay + phần hôm nay); quỹ B7 0,35 giữ riêng.

## Giới hạn

- **T3:** sàn "model không tự nêu điều kiện miễn giảm" trượt vì đoạn kho tìm được vẫn có các điều kiện đó — thiết kế chỉ giữ chữ điều kiện **của bảng** ngoài model. Câu
  sub-agent nghi sai (trẻ 7–12 tuổi miễn phí ở Bảo tàng Cổ vật) **đúng với kho** ⇒ không phải lỗi đang chạy. Lỗi công cụ đo: 20 câu Q2 chạy trong **một** cuộc trò chuyện (đã sửa;
  các lượt cùng thước). Lỗi thiết kế: khi câu không nêu tên điểm, code lấy điểm của câu trước ⇒ đổi chủ đề vẫn bị gắn lưu ý điểm cũ. Bộ an toàn, mẫu Golden, tốc độ chưa đo.
- **G:** S2b (câu nơi khác bị mở tra web) chưa đạt — đang chỉnh lời dặn.
- **Bỏ tuyến khẩn cấp:** câu khẩn cấp có thể nhận câu từ chối thường — User chấp nhận; bộ khẩn cấp chỉ quan sát.
- Test `test_cong_dot_1::test_weather_and_feature_routes` hỏng khi nạp khoá OpenAI (A bật cờ ảnh) — **đã sửa** `e7ad76f` (E; test tự đặt cờ), 22 / 22 cả có lẫn không khoá.
- Tốc độ (S5) các việc hôm nay chưa đo chính thức (máy dùng chung; A xếp lượt riêng).

## Bước tiếp

1. **User chọn hướng T3:** phương án B của spec (bảng chỉ dùng kiểm số cuối, không công cụ) hay việc mới — code lọc câu điều kiện khỏi chữ model, hoặc đổi sàn Q3 (User duyệt).
2. G: chỉnh lời dặn tới khi S2b = 0, lượt quyết cuối trên bộ kín ⇒ review ⇒ merge ⇒ mở đợt 2 (T2 rồi T4).
3. T1: review nhánh ⇒ merge (cờ tắt) ⇒ bật khi User duyệt.
4. Bản đồ: User xem ảnh + phiếu toạ độ ⇒ bật cờ.
5. Giọng nói: User thu 40 câu theo hướng dẫn.
6. Sau đó: so sánh cuối B7 ⇒ đóng gói + Docker ⇒ deploy khi User nói.
