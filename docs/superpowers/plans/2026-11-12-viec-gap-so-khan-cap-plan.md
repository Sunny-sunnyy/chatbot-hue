# Plan (mức nhẹ) — "việc gấp": code nối dòng số khẩn cấp khi định tuyến xếp khẩn cấp · **NHÁP — chờ User chọn (đảo một phần quyết định bỏ khẩn cấp 08–09/11)**

Người viết: C, 20:18 12/11/2026 (`date`), A giao. Chưa code, 0 USD. Repo public: không chép câu hỏi / câu trả lời.

## Căn cứ để review

- Lượt đếm 12/11: `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` mục 3e (việc gấp) + mục 3c (2) (câu ngoài phạm vi mở cổng web).
- Quyết định cũ: spec Phase 9 `docs/superpowers/specs/2026-11-02-phase-9-design.md` §12.1 (việc G), §12.3 (dòng "Quan sát khẩn cấp"), §12.8 ("Bỏ tuyến khẩn cấp");
  report bậc cổng 2 nhóm `report_agent/2026-11-08_phase_9_ban_13/b_g_cong_implementation.md` (phương án B); `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-09.md`.
- Code: `backend/llm/assistant.py` (chỗ gán `emergency_by = "router"`; hàm `web_gate_open`; hàm `set_notice`) · `backend/api/routes/chat.py` (trường `notice` của câu trả lời + sự kiện `notice` của đường stream) · `backend/llm/tra_web.py` (`THIEN_TAI_TEXT` — mẫu câu cố định do code nối).
- Bảng số: `data/phase_9/so_khan_cap.md` (private; kiểm nguồn 02/11/2026).

## 1. Lỗi đã đếm (12/11, 6 câu "việc gấp" tự viết, hệ thống thật)

- **0 / 6 câu** có một số khẩn cấp nào trong câu trả lời.
- **3 / 6 câu** (trẻ lạc · người bị thương trên núi · người bị sóng cuốn): kho từ chối, mục web chỉ viết "không nêu cần gọi ai" ⇒ chờ 18–25 giây, **không có hướng dẫn nào**.
- 1 câu kho trả lời (chỉ tới ban quản lý nơi xảy ra việc, không nhắc báo công an); 2 câu web khuyên chung chung, chưa kiểm.
- Định tuyến đã xếp "khẩn cấp" ở 4 / 6 câu — tức hệ thống **biết** đây là việc gấp nhưng không làm gì khác với nhãn đó.
- Kho: 0 bài có số 113 / 114; 0 bài có chữ "trình báo" ⇒ trợ lý chỉ-từ-kho không thể tự nói ra.

## 2. Quyết định cũ và cái mới khác gì

| | **Đã gỡ 09/11** (User chọn 08/11: "không cần, không tập trung") | **Đề xuất hôm nay** |
|---|---|---|
| Ai quyết "đây là khẩn cấp" | định tuyến **và** một luật từ khoá bằng code (cờ đã tắt từ trước) | **chỉ** định tuyến (đang chạy sẵn, không đổi lời dặn); không có luật từ khoá |
| Người dùng nhận gì | **chỉ** một câu soạn sẵn 4–5 dòng **thay** cho câu trả lời; model không được gọi, kho không được dùng | **câu trả lời của trợ lý như hôm nay** (phần kho có vẫn trả lời, vd chỉ tới ban quản lý, cảnh báo sông nước) **+ một dòng số khẩn cấp** do code nối ở kênh "ghi chú" sẵn có |
| Tuyến riêng | có tuyến khẩn cấp + nhánh giao diện riêng | không — vẫn là tuyến trợ lý Huế; không thêm nhánh giao diện |
| Khi kho không có | câu soạn sẵn (đủ số) | câu từ chối của kho + dòng số; **không tra web** cho lượt đó |
| Vì sao khi đó gỡ | User muốn gọn (chỉ tách xã giao ↔ về Huế); spec ghi rõ hậu quả "câu khẩn cấp có thể nhận câu từ chối thường hoặc mục web" và User nhận | số đếm 12/11 cho thấy hậu quả đó xảy ra ở 3 / 6 câu, đúng loại lỗi User xếp nặng nhất (28/10); cách mới không dựng lại tuyến / câu soạn sẵn, chỉ thêm một dòng |

Cái **không** quay lại: tuyến khẩn cấp, câu soạn sẵn thay câu trả lời, luật từ khoá, hướng dẫn sơ cứu, số địa phương.

## 3. Việc đề xuất (tất định, do code)

Khi `trace.emergency_by == "router"`:
1. **Nối dòng số khẩn cấp cố định** vào kênh ghi chú của câu trả lời (trường `notice` — đang dùng cho dòng "thông tin có thể đã thay đổi"; giao diện đã hiện, đường stream đã có sự kiện).
   Chữ lấy từ bảng số đã kiểm (113 công an · 114 cháy, cứu nạn · 115 cấp cứu y tế · 112 thiên tai) + một câu "nói rõ bạn ở đâu, chuyện gì đang xảy ra". Lượt đã có ghi chú
   "có thể đã thay đổi" ⇒ dòng số đứng trước, hai dòng cùng hiện.
2. **Không mở cổng web** cho lượt đó (thêm một điều kiện vào `web_gate_open`): bớt 10–15 giây chờ và không gửi câu hỏi lúc gấp ra dịch vụ tìm web; đồng thời đóng đúng ca
   "câu y tế chung bị xếp khẩn cấp ⇒ mở web" mà User đã nhận làm giới hạn 09/11.
3. Trợ lý **vẫn trả lời phần kho có** — không đổi lời dặn, không đổi công cụ, không thêm lần gọi model.

- **File · hàm chạm:** `backend/llm/assistant.py` (`set_notice`: thêm nhánh theo `emergency_by`; `web_gate_open`: thêm điều kiện; cờ mới trong `AssistantFlags`) ·
  `backend/llm/full_corpus_prompt.py` (hằng chữ dòng số) · `backend/config/settings.yaml` (cờ `so_khan_cap`, mặc định tắt tới khi đo đạt) · test. `chat.py`, giao diện: không sửa
  (đã chuyển `notice` nguyên văn) — xác nhận bằng một lần xem trên bản build.
- **Chuỗi gửi model:** không đổi ở mọi lượt (dòng số nối **sau** khi model trả lời, ngoài chuỗi gửi model) ⇒ giống byte cả khi cờ bật.
- **Việc lúc làm (bắt buộc, 0 USD):** mở lại nguồn của bảng số bằng WebFetch (số có thể đã gộp — ghi chú 02/11 nhắc một kế hoạch gộp về 113); số nào không còn xác nhận được ⇒ bỏ
  khỏi dòng, báo A. Ghi ngày kiểm vào report + nhắc kiểm lại trước bảo vệ / deploy.

## 4. Tiêu chí ghi trước

| | Mức | Đo bằng |
|---|---|---|
| **Quyết** | **mọi** lượt định tuyến xếp khẩn cấp có dòng số (100 % — tất định) và **0** lượt mở cổng web | 22 câu: 6 câu việc gấp 12/11 + bộ khẩn cấp bước 0 (10) + 6 câu khẩn cấp của bộ tự viết 03/11; qua server thật, 1 lượt; đếm bằng code (`emergency_by`, `notice`, `web_outcome`) |
| Câu thường **không** có dòng số | 0 câu | Golden 176 + an toàn 32 ×2: đếm lượt có `emergency_by`. Mốc [Chạy 12/11, lượt B7 giữa kỳ]: **0 / 176** câu Golden bị xếp khẩn cấp; an toàn: đếm lại trên file B7 trước khi code (file hôm nay không ghi trường này ⇒ chạy lại 32 câu ×1) |
| An toàn 32 ×2 | 4 số như mọi bậc — và vì chuỗi gửi model giống byte, kỳ vọng **không đổi so với lượt B7**; khác ⇒ dừng, tìm nguyên nhân | bộ an toàn |
| Ngoài phạm vi | 0 câu ngoài phạm vi bị trả lời; cổng web mở ở câu ngoài phạm vi **giảm** (ca y tế hết; ca "có chữ Huế" không đổi) | 44 câu ×1 |
| Không mất mục web đáng có | trong 22 câu trên, đếm câu mà **hôm nay** mục web cho lời khuyên dùng được: báo số (ước 2 / 6 ở lượt 12/11 — lời khuyên chung chung, chưa kiểm); C đề xuất chấp nhận mất | đọc bằng mắt, ghi report |
| Giống byte khi cờ tắt | 228 / 228 | Q1 sẵn có |
| Test theo loại lượt | xếp khẩn cấp + kho trả lời ⇒ câu trả lời + dòng số · xếp khẩn cấp + kho từ chối ⇒ câu từ chối + dòng số, không web · câu thường ⇒ không dòng số · lượt vừa khẩn cấp vừa có ghi chú "có thể đã thay đổi" ⇒ đủ hai dòng · đường stream phát sự kiện ghi chú · cờ tắt ⇒ như hôm nay | test mới, 0 USD |
| Giao diện | dòng số hiện rõ, đọc được trên điện thoại | một khổ màn, bản build do FastAPI phục vụ |

## 5. Phần hở: 2 / 6 câu việc gấp định tuyến **không** xếp khẩn cấp (mất giấy tờ · bị ép giá)

| Cách | Hệ quả | C đề xuất |
|---|---|---|
| **Nhận giới hạn** | hai loại này vẫn như hôm nay (kho từ chối ⇒ web khuyên chung chung). Không nguy hiểm tính mạng | **chọn ở đợt này** — ghi rõ trong report + trang giới thiệu |
| Thêm vào kho một bài "khi gặp sự cố ở Huế" (mất đồ / giấy tờ, bị ép giá: báo ai) | trợ lý trả lời được từ kho, có trích dẫn; là bổ sung kho từ nguồn ngoài ⇒ luật sửa kho, User duyệt nguồn | gộp vào đợt sửa kho "ăn gần + di chuyển" nếu User chọn đợt đó |
| Sửa lời dặn định tuyến để xếp cả hai loại vào khẩn cấp | đổi lời dặn định tuyến = **một bậc đo riêng** (bộ tuyến + ngoài phạm vi + an toàn); rủi ro xếp nhầm câu thường | không làm ở đợt này |

Giới hạn còn lại sau khi làm: định tuyến xếp nhầm một câu **không** gấp vào khẩn cấp (đã thấy: câu y tế chung) ⇒ câu đó có thêm dòng số — vô hại, C đề xuất nhận.
Định tuyến lỗi / quá giờ ⇒ không có nhãn ⇒ không có dòng số (như hôm nay).

## 6. Rà theo khung AI FDE (ngắn)

| Mục | Hiện trạng | Khớp / lệch | Trong plan |
|---|---|---|---|
| Số, luật, thứ tự bắt buộc ⇒ code; model chỉ diễn đạt | số khẩn cấp hôm nay **không có ở đâu**; nếu có thì chỉ khi model / web tự nói | lệch | dòng số là **hằng do code nối**, model không viết, không sửa được |
| Mốc rẻ nhất / có cần model không | — | — | không thêm lần gọi model; không đổi lời dặn |
| Chữ người dùng là dữ liệu | nhãn khẩn cấp do định tuyến sinh từ câu người dùng | khớp — nhãn chỉ bật một dòng cố định + **đóng** một đường ra (web); không mở quyền gì | người dùng cố ý gõ câu "gấp" chỉ nhận thêm dòng số và mất mục web của lượt đó |
| Đường ra ngoài | câu việc gấp bị kho từ chối đang được gửi tới dịch vụ tìm web | lệch nhẹ (câu lúc gấp có thể chứa chi tiết cá nhân) | lượt xếp khẩn cấp không còn gửi ra |
| Thông tin an toàn phải có nguồn kiểm được | bảng số có nguồn + ngày kiểm 02/11 | khớp, cần làm mới | bước kiểm lại bằng WebFetch lúc làm + nhắc trước bảo vệ |
| Đường phục hồi khi phần mới hỏng | — | — | cờ `so_khan_cap`; tắt ⇒ đúng hành vi hôm nay |
| Dữ liệu cá nhân / log | log đã có `emergency_by`, không nội dung | khớp | không thêm trường có nội dung |

## 7. Tiền · giờ

- **Tiền ≤ 0,06 USD:** 22 câu khẩn cấp (sau sửa không còn web ≈ 0,0006 / câu) 0,015 · an toàn 32 ×2 0,03 (kỳ vọng giống B7; chạy vì là sàn) · ngoài phạm vi 44 câu 0,009 · cổng ổn định 0,002.
  Golden 176: **không sinh lại** — chuỗi gửi model giống byte và 0 / 176 câu bị xếp khẩn cấp ở lượt B7 ⇒ dùng lại (ghi rõ là dùng lại + lý do).
- **Giờ:** ~1,5–2 giờ agent (kiểm số 15 phút · code + test 40 phút · đo 30 phút · report + một review cả nhánh).
- Bài học: thêm một đoạn vào bài 14 ("việc dễ nhầm thì code làm") + dòng trong bảng tổng bài 19 khi việc xong.

## 8. Cần User chọn

1. Có làm không — tức **đảo một phần** lựa chọn 08/11 "bỏ khẩn cấp": không dựng lại tuyến hay câu soạn sẵn, chỉ thêm một dòng số do code nối khi định tuyến xếp khẩn cấp.
2. Lượt xếp khẩn cấp **không tra web** nữa (mất 2 / 6 lời khuyên chung chung từ web, đổi lại nhanh hơn ~10–15 giây và không gửi câu hỏi ra ngoài) — đồng ý?
3. Phần hở mục 5: nhận giới hạn ở đợt này (C đề xuất), hay thêm bài "khi gặp sự cố" vào kho cùng đợt sửa kho.
