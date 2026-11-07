# Review: cổng đợt 1 — S4 phần 1, backend nhánh `p11-cong-dot-1` `0cb0b0a`

Decision: **(tạm) ready_for_user_confirmation — phần backend** · 0 blocker · 0 major · 4 minor. Còn 3 ca dò cần CPU **chờ chạy sau lượt đo X1b của C** (§4); kết luận cuối ghi lại sau khi có số.
Người kiểm: E (Claude Opus 5.5) · 12:48 07/11/2026 (`date`)
Căn cứ: spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` (bản duyệt `ff3c317ec88b` + sửa chữ §3) §2 D3 / D4 / D6 / D7, §6 Q-K · Q-F phần tất định · Q-C, §7.
Implementation report: **chưa có** (m-1) ⇒ chỉ mục = commit message `1c31ce4` + `0cb0b0a`.

## 1. Phạm vi đã review

- Diff `git diff main...0cb0b0a -- backend/` (merge-base, vì `main` đã đi tiếp ở phần tài liệu): 6 file, +543 / −26 — `api/app.py`, `api/routes/chat.py`, `api/routes/cong.py` (mới), `config/settings.yaml`, `llm/assistant.py`, `tests/test_cong_dot_1.py` (mới). `git diff --check` sạch. Không có file ngoài `backend/` trên nhánh so với merge-base.
- Không review: frontend (S2, phần 2); chữ model ở lượt biểu mẫu (C đo X1).
- Worktree riêng `/tmp/e_rv` (detached `0cb0b0a`, symlink `data/` + `knowledge-base-hue/` — gỡ khi xong).

## 2. Đối chiếu tiêu chí

| Tiêu chí | Bằng chứng | Kết quả |
|---|---|---|
| D3 nút thắng cả 4 trường, code gọi `lich_trinh`, không định tuyến / công cụ | `assistant.py` `_xep_bieu_mau` gọi `lich_trinh_for_turn(...)(so_ngay, di_cung, kieu_di, so_thich)` từ `trace.truong`; `answer_turn` / `answer_turn_stream` rẽ khi `trace.bieu_mau`; test `test_qf_every_button_combo…` (120 tổ hợp, 1 lần gọi / lượt, `tools == []`) [Chạy: đạt] | khớp |
| D3 chữ gõ không tới model | `chat.py` `_model_query`: `bieu_mau` ⇒ `query = CAU_BIEU_MAU` rồi `ghep_cau`; `TruongInput` chỉ nhận `Literal` ⇒ không chữ tự do nào. Lịch sử nhớ đúng câu ghép (`_remember(…, query)` sau `_model_query`) | khớp |
| D3 rẽ **trước** #6 song song | `answer_turn_stream_parallel`: `if trace.bieu_mau or …` ⇒ đi `answer_turn_stream`; test 4c "1 lần gọi" cả stream | khớp |
| D3 tra web không mở ở lượt biểu mẫu | `web_gate_open` cần `trace.truong is None` và `trace.lich is None` ⇒ đóng | khớp (đọc code) |
| D4 cờ `lich_trinh_bieu_mau` tắt; bật cần bảng | `settings.yaml` `false`; `AssistantFlags.__post_init__` raise khi thiếu bảng; cờ tắt ⇒ cả 2 route 404 **trước** khi tìm kho | khớp |
| D6 `/api/kham_pha` 204 / 204, 5 lĩnh vực | `cong.py` `nap_kham_pha(*discover_full_corpus_files)` chỉ sau khi retrieval đã kiểm hash với build record; test `test_explore_lists_exactly…` [Chạy: đạt] | khớp |
| D6 `/api/kham_pha/bai` chỉ id nguyên văn | `bai.get(id)` (tra dict, không ghép đường dẫn) + `_bi_chan` (`..`, `/`, `evaluation/`, `meta/`, `_source-dumps/`, `sealed`) | khớp — ca dò riêng của E §4 (a) **chờ chạy** |
| D6 `/api/thoi_tiet` cờ tắt ⇒ 404; lỗi ⇒ không số | `cong.py` `thoi_tiet`; `DuBao` "ok" luôn đủ 7 ngày (`doc_phan_hoi` raise khi khác) ⇒ `ngay[0]` an toàn | khớp |
| D6 `/api/tinh_nang` chỉ boolean | 4 boolean | khớp |
| D7 `bai_id` chỉ cho bài kho | `_source_responses(cited, bai_ids)`: `source in bai_ids` else `None`; test với nguồn `open-meteo` ⇒ null | khớp |
| 4c mỗi loại lượt | test lượt biểu mẫu đầu (có / không lịch sử × stream / không), lượt hỏi tiếp sau biểu mẫu (cờ bật ⇒ chuỗi gửi giống cờ tắt), model từ chối ⇒ code dựng lời | khớp |
| Q-C cờ tắt ⇒ Q1 228 / 228 giống byte | commit nói đạt; **không có file bằng chứng** | **chờ chạy** §4 (b) |

## 3. Findings

- **m-1 (minor) — thiếu report S1.** Không có `report_agent/2026-11-06_giao_dien_cong/s1_*`; bằng chứng tự kiểm (Q1 228 / 228, Q1m, 20 test, pilot 3 lượt thật — 1 / 3 model tự viết) chỉ có trong commit message, không lệnh / file kết quả. *Đóng:* B viết report S1 ngắn (lệnh + đường dẫn file Q1 + số pilot + tiền) trước merge S5.
- **m-2 (minor, chuyển S2) — lượt biểu mẫu vẫn trả thẻ "Sửa".** `lich_cho_giao_dien` (`assistant.py:630`) dựng `sua` = thẻ hỏi lại `lich_trinh`; "Gửi" của thẻ đi đường câu ghép **không** `bieu_mau` ⇒ cờ `lich_trinh` (câu tự do) đang tắt ⇒ không xếp lịch. Spec D3: "muốn đổi thì điền lại biểu mẫu". *Đóng:* S2 không hiện thẻ "Sửa" ở lượt biểu mẫu (hoặc nút dẫn về biểu mẫu); hoặc backend bỏ `sua` khi `trace.bieu_mau` — B chọn một.
- **m-3 (minor) — sửa `0cb0b0a` đổi cả đường câu tự do.** `_lay_nguon_lich` (chọn đoạn bằng chứng dài nhất) dùng chung cho công cụ `lich_trinh` của câu gõ tự do — ngoài D3 nhưng cờ đó tắt ⇒ người dùng không thấy; đã ghi trong commit. Đoạn dài hơn ⇒ ngữ cảnh lớn hơn ⇒ có thể chạm luật "vượt ngân sách ⇒ bớt ngày cuối". *Đóng:* ca dò §4 (c) cho 0 lượt bị bớt ngày (hoặc báo số); ghi vào báo cáo khâu khi xét bật câu tự do.
- **m-4 (minor, không cần sửa) — API vẫn nhận `kieu_di = day_lich`.** Q-U3 chỉ ẩn ở giao diện; gửi thẳng API vẫn chạy, và theo E21 "đi dày" xếp như "thong thả" ⇒ vô hại. Ghi lại để S2 không hiện nút.

**Câu hỏi độ đơn giản:** `cong.py` 112 dòng, một nhiệm vụ mỗi hàm, không lớp phụ; `_bi_chan` là lớp thứ hai rẻ đúng yêu cầu spec §7. Nhánh biểu mẫu trong `answer_turn_stream` dùng lại vòng đọc chung thay vì chép ⇒ hợp lý. Không thấy over-engineering.

## 4. Người kiểm chạy lại

Đã chạy (worktree `/tmp/e_rv`, `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest …`, không khoá, 0 USD):
- `tests/test_cong_dot_1.py`: **20 passed** (38 s).
- 13 file liên quan (`test_assistant*`, `test_b2_tool_loop`, `test_b3_memory`, `test_b5_lich_trinh`, `test_b5b_thoi_tiet`, `test_b6_tra_web`, `test_chat_stream`, `test_citations`, `test_emergency`, `test_feedback`, `test_toc_do_song_song`, `test_p10_anh`): **522 passed**.
- `test_api_chat.py` + `test_phase6_settings.py`: 13 passed, 1 failed + 1 error = đúng 2 test cần `OPENAI_API_KEY` (bẫy đã biết, `Project_Status.md` §8).
- ⚠ Hai lượt pytest trên có thể trùng đầu lượt đo X1b của C (từ 12:45) ⇒ đã báo C đối chiếu giờ.

**Chờ chạy sau X1b (CPU / Qdrant):**
- (a) ca dò riêng `/tmp/e_rv_do/do_cong.py` (khác cách B): id NFD, có dấu cách, tiền tố `knowledge-base-hue/`, gạch ngược, `//`, null byte, 301 ký tự, `%2e%2e%2f` và mã hoá 2 lần `%252e…`; so tập `/api/kham_pha` với `corpus.sources`; bất biến "chữ lạ trong `query` không vào câu gửi model".
- (b) Q1: `capture_all.py` trên worktree `main` ↔ `0cb0b0a`, `cmp`.
- (c) `/tmp/e_rv_do/do_ngan_sach.py`: 120 tổ hợp — số lượt bị "bớt ngày" vì ngân sách.

**Bất biến kiểm:** cờ `lich_trinh_bieu_mau` tắt ⇒ mọi lượt chat như `main` (Q1) và lượt có `bieu_mau` ⇒ 404 trước khi chạm kho / model.
