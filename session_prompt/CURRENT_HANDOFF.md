# CURRENT_HANDOFF — khối trỏ (từ 19/11 sổ việc theo giờ nằm ở thư mục ngày)

Cập nhật: 22:32 19/11/2026 (A, KẾT PHIÊN CUỐI NGÀY 19/11). Bản đầy đủ tới lúc này, nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-19.md` (đã `cmp` giống hệt trước khi cắt); các bản trước ở `archive/`.

## PHIÊN SAU ĐỌC TRƯỚC
1. `session_prompt/HIEN_TRANG.md` (đủ) ⇒ `session_prompt/VIEC_DANG_MO.md` (bước kế CHỈ ghi ở đó; việc ĐẦU TIÊN: việc 2 — sửa nhỏ cờ `nho_ten_goi_y`, rồi soát khác hãng) ⇒ `session_prompt/sessions/STATUS_<X>.md` mục đầu ⇒ khối đầu `report_agent/2026-11-19/TONG_HOP.md`. Chạy `scripts/mo_ngay.sh`.
2. Máy mở lại ⇒ `/tmp` MẤT + Qdrant có thể tắt: `docker compose up -d qdrant`, kiểm 9.436 điểm. `frontend/dist` cây chính đã dựng lại 19/11 tối.
3. Không hỏi quyền phiên (bảng "Quyền thường trực" trong `AGENTS.md`). Tên terminal đổi mỗi lần mở: A nhắn trước, B / C / E trả lời một tin.

## Ghi trong phiên (A nối dòng mới ở đây; cuối ngày dời sang `TONG_HOP.md` của ngày)
- 22:32 19/11/2026 — tên terminal tối 19/11 (CŨ khi mở lại): A `hue-rag-67` · B `hue-rag-02` · C `hue-rag-c6` · E `hue-rag-29`. Lần "đọc ngắn" thứ sáu: 0 tin rải, 0 lần vấp luật do chưa đọc (tự khai).
- 08:23 20/11/2026 — MỞ PHIÊN 20/11. Tên terminal: A `hue-rag-a6` · C `hue-rag-49` · E `hue-rag-95` · B `hue-rag-04`. Máy mở lại: Docker 0 container (kể cả container đã dừng) ⇒ A bật lại `docker compose up -d qdrant`, thư mục chỉ mục còn nguyên, kiểm 9.436 điểm ĐẠT. Giao việc 2 (`VIEC_DANG_MO.md` khối 2): B viết plan mức nhẹ + code · E soạn bộ dò ≥ 20 câu (không xem bộ từ của B) rồi review nhánh · C chạy phép đo (kịch bản đích × 3 mỗi bên + bộ 17 chuỗi) sau khi nhánh sẵn. Lần "đọc ngắn" thứ bảy: 0 tin rải (C, E tự khai).
- 08:27 20/11/2026 — A duyệt plan việc 2 bản `d26eb6099da3` (riêng tư, đường dẫn ở `VIEC_DANG_MO.md` khối 2); tiêu chí câu ghép: nửa hỏi về một nơi ⇒ không nhận. E thêm việc: cập nhật sổ ghi việc `bao_cao_he_thong/` cho tối 18/11 + 19/11 (nhánh riêng, A đọc diff). Máy: ba phiên điều phối thoả thuận mỗi lúc một việc nặng, xin lượt trước; một dự án khác bật bộ ~10 GB buổi sáng ⇒ hue_rag chưa bật server tới khi được báo trả RAM. A đã chép quyết định 18/11 + 19/11 vào `Project_Status.md` mục 5; sửa ba chỗ lệch của `mo_ngay.sh kiem` (còn một: tên nhánh đã xoá trong `STATUS_B.md`, B bỏ khi ghi đè sổ). Một lần vấp luật giờ `date` (B, giờ ước trong plan, đã sửa).
