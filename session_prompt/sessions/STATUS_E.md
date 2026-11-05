# STATUS E — tạo bởi A 09:38 05/11/2026 (phiên E chưa mở)

Terminal: `hue-rag-7a` (mở 09:47 05/11/2026) · Agent: Claude Opus 5.5 (User mở) · Vai: **thực thi** (như B / C — `WORKFLOW.md` §1).

## Bối cảnh cho E (A viết — đọc trước)
- E mở 05/11/2026 theo User (A khuyến nghị "thêm 1 phiên E"): làm việc **không chồng file chung** với B / C. Hiện B sửa `backend/llm/*`, `backend/api/*`,
  `frontend/src/*` (B4b ⇒ B5); C review + bộ đo. E **không sửa** các file đó, không sửa `session_prompt/` (trừ file này + dòng của E trong handoff).
- Máy ~15 GB RAM, từng treo ⇒ E **không chạy server chatbot / Playwright / tải model** khi chưa hỏi A (một việc nặng một lúc). Lượt đo tốc độ của B / C đang chạy ⇒ E không chạy việc nặng (W31).
- Hệ thống hiện tại: `Project_Status.md` §4; Phase 9 spec `docs/superpowers/specs/2026-11-02-phase-9-design.md`; đề xuất tính năng mở rộng (User duyệt 05/11)
  `bao_cao_he_thong/DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` — **User 05/11: không dồn hết vào Phase 9, tách Phase 10, 11, 12…** (A đang sắp lại; giọng nói / ảnh nhiều khả năng thành Phase 10).
- **User 05/11 về giọng nói:** "cần nghiên cứu thêm các mô hình **open-source**, mô hình **của Việt Nam** (speech-to-text, text-to-speech), **không gọi API ngay**".
- Tra web: `scripts/tra_web_codex.sh <yêu cầu .md> <tên_ngắn>` (chỉ thông tin công khai) + WebFetch kiểm 2–3 ý chính; **không bao giờ gọi `agy`**. Không đọc `.env`. Code / script luôn `uv run`.

## Việc đầu tiên: E1 — xem mục E1 trong `CURRENT_HANDOFF.md` ("PHIÊN 05/11 — VIỆC ĐANG GIAO")

## Đang làm
- E1 nghiên cứu STT / TTS tiếng Việt (A "làm đi" 09:47 05/11/2026; 0 USD; Codex + WebFetch)

## Đang khai báo sửa
- `data/phase_10_nghien_cuu/giong_noi/` (mới, private) · `data/tra_cuu_cli/2026-11-05_e1-*` (đầu ra script) · file này

## Vừa xong
- —

## Đã học / bẫy gặp
- —

## Việc dở / câu hỏi cho A
- —
