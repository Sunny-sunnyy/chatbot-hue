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
- **E8 Phase 10 A1** — code + kiểm XONG (11:17 05/11/2026): T1–T9 + A1b đạt; report `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` `8d2399b3b425`. **Commit + push nhánh `p10-anh` bị auto mode chặn** (luật User: commit / push hỏi trước; quyền A là tin phiên khác) ⇒ 6 file *staged* trong `/tmp/e_anh`, **chờ User đồng ý**. Tiền A1 0,00038418 USD.
- E1 giọng nói: **dở — tạm dừng 09:51 05/11/2026 theo User**; phần đã kiểm `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md`; Codex `e1-stt`, `e1-tts` để chạy hết, chưa đọc

## Đang khai báo sửa
- `docs/superpowers/plans/2026-11-05-phase-10-a1-plan.md` (E8) · sẽ: worktree `/tmp/e_anh` nhánh `p10-anh` (`backend/llm/nhan_anh.py`, `backend/api/routes/anh.py`, `backend/tests/test_p10_anh.py`, `backend/api/app.py`, `backend/config/settings.yaml`), `data/phase_10/anh/` · không (các file E đã viết: `data/phase_10_nghien_cuu/`, `data/phase_11_nghien_cuu/luu_tru/`, `…b5-plan_review.md` vòng 3–6, `docs/superpowers/specs/2026-11-05-phase-10-design.md` nháp — chưa commit, A commit) · `data/phase_10_nghien_cuu/giong_noi/` (mới, private) · `data/phase_10_nghien_cuu/anh/` · `data/tra_cuu_cli/2026-11-05_e1-*`, `…_e2-anh` (đầu ra script) · file này

## Vừa xong
- **A2 P1 XONG — KẾT QUẢ ÂM** (11:37 05/11/2026): v0 / v1 / v2 × 2 lượt, chưa vòng nào đạt cả Q-a + Q-c hai lượt; tiền Phase 10 0,078545 / 0,15. Report mục A2 trong `e8_a1_implementation.md`. Chờ A / User chọn (P2 SigLIP / gợi ý + M0 / dừng).
- **Rà over-engineering** `data/ra_soat_over_engineering_2026-11-05/E.md` (38 dòng).
- **E7 XONG** — `scripts/tra_web_codex.sh` +47/−5 (chưa commit, A review): đếm trang mở đúng (khớp E6 trên 6 thư mục), `--dem`, câu cấm; probe `e7-probe-url-mau` PARTIAL (0 trang đặt chỗ, URL mẫu có nhãn; 1 lần mở lỗi không quy được). Probe là gói User, 0 USD API.
- **E6 XONG** — `data/tra_cuu_cli/e6_ra_soat_script.md` sha `f0df99e5ecd8`: `url_da_mo` thiếu vì lô mở trang có `action.type: other` (results `ref_id` *view*); đếm đúng 8–41 trang / lượt; Codex tự mở URL tự dựng do hướng dẫn "URL đã mở" + yêu cầu "URL mẫu" ⇒ đề xuất câu cấm + cách đếm mới (A sửa script)
- Spec Phase 10 bản 2 `bf67b90fb6fc` ⇒ **B vòng 2 ready** (review `6aeebc5e0914`)
- **E5 XONG** — `data/phase_11_nghien_cuu/luu_tru/e5_khu_o_va_link.md` sha `9c5411f6c032` (kho: 1 mục "nên ở khu nào", 3 nhóm khu; link chính Google Maps URLs; Booking User quyết; Agoda không)
- **Plan B5 vòng 5** bản 6 `46c1ec1a8242` ⇒ changes_requested 0/1/2 (M-2 "Trả lời luôn" hỏi không dứt) · **vòng 6** bản 7 `b572443dc9cd` ⇒ **ready** — review `…b5-plan_review.md` sha `d576aa9c9ef8`
- **E3** review plan B5 bản 4 ⇒ changes_requested 0/1/5; **vòng 4a** bản 5 `dff61a2db4e6` (tạm, bị thay vì User đổi hướng B4b) — `…b5-plan_review.md`
- **E4** nháp spec Phase 10 sha `d640b8696edd` ⇒ B review changes_requested 0/2/6 ⇒ **E4b bản 2 `bf67b90fb6fc`** (A10 chặn gửi chéo trang: thân `image/*` + Sec-Fetch-Site/Origin 403 + byte trước khi đọc; Q-k kín; luật A/A; Q-d ca khó; bảng FDE có file:dòng; lịch thay cột Phase 10 spec 9 §11.4) — chờ B kiểm
- **E2 XONG 09:57 05/11/2026** — `data/phase_10_nghien_cuu/anh/nghien_cuu_anh.md` sha `0dcc2c717498` (0 USD; Codex e2-anh + 12 WebFetch); tóm đã nhắn A. Đề xuất P1 luna enum + xác nhận, P2 SigLIP 2 chạy máy; ngưỡng ghi trước mục 5.1; lượt đo P1 ước 0,04–0,07 USD.

## Đã học / bẫy gặp
- `max_tokens` gồm suy luận: 512 cắt 4 / 66 ảnh khó (đầu ra hỏng ⇒ chấm "không nhận ra" ⇒ số đo lạc quan) ⇒ luôn đếm `output_tokens == trần` trong lượt đo.
- Commit / push từ E: auto mode coi "A cho phép" là tin phiên khác, không phải User đồng ý (luật CLAUDE.md của User) ⇒ E cần User xác nhận ngay trong terminal E (hoặc User `!`).
- Lỡ chạy `python3` hệ thống (không Pillow) để tạo ảnh test ⇒ luôn `uv run`.
- Gõ tay giờ "10:21" vào spec (hook bắt) ⇒ luôn `T=$(date …)` trước, kể cả khi sửa bằng Edit.
- `main` đổi giữa lúc viết (B4b merge) ⇒ `file:dòng` lệch ⇒ grep lại số dòng ngay trước khi báo sha.
- Tin A / C có thể tới **sau** khi đã ghi review (bản 5 bị thay giữa chừng) ⇒ ghi kết luận "tạm, bị thay" thay vì xoá; trước khi ghi kết luận vòng, kiểm lại sha file plan.
- Codex tự "thử mở" URL trang đặt phòng dù yêu cầu không bảo ⇒ yêu cầu Codex ghi rõ "không mở URL tìm kiếm / trang của hãng".
- `tra_web_codex.sh`: `url_da_mo.txt` **đếm thiếu** (bỏ lô mở trang `other`) — E6 chứng minh; tới khi A sửa script, đếm trang mở bằng jq trên `results[].ref_id` chứa `view`.
- Bảng token ảnh của OpenAI không có dòng `gpt-6-luna` ⇒ số token ảnh là giả định (theo `gpt-5.6-luna`), cần 1 lần gọi thật để kiểm.

## Việc dở / câu hỏi cho A
- E1 giọng nói dở (xem "Đang làm").
- —
