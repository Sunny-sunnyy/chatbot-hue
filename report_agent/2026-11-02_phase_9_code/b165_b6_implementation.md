# Implementation Report: Phase 9 — B6 tra web qua cổng code (B165, phần 0 USD)

Người làm: B (Claude Code, Opus 5.5)
Date: 19:46 05/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-05-phase-9-b6-plan.md` bản 3 sha `6e5c3b21065d` (A duyệt tối 05/11; review B vòng 2 ready)
Nhánh: `p9-b6` từ `main` `2693422`; commit code `7873e0f` + sửa `d7ec216` (mục 4). Worktree `/tmp/b_b6` (symlink `data/`, `knowledge-base-hue/`).

## 1. Phạm vi

- **Đã làm (bước 2 của plan §6):** code D1–D10 + test, cờ `tra_web: false`. 0 USD.
- **Chưa làm:** Playwright (Q8), probe Serper thật (bước 3, ≈ 0,001), lượt đo có phí Q2–Q5 (trần 0,22 / dừng 0,21).

## 2. Thay đổi chính

| File | Việc |
|---|---|
| `backend/llm/tra_web.py` (mới) | Module **duy nhất** gọi Serper (D3): `cau_tim_web` (D2: câu hỏi lượt này, bỏ email / SĐT, ≤ 120 ký tự, thêm " Huế"); `tim_web` (một lần, `gl=vn hl=vi num=5`, timeout, không thử lại; thiếu khoá ⇒ "loi" **không mở kết nối**; hết giờ / mạng / HTTP ≠ 200 (gồm hết hạn mức) / JSON hỏng / sai schema ⇒ "loi"; 0 kết quả ⇒ "rong"); `doc_ket_qua` (sổ web w1..w5, chỉ link `http(s)`, bỏ `utm_*`, tên miền); `dau_vao_model` (câu hỏi + đoạn trích có mã, **không** gửi link); `kiem_muc_web` (D5). |
| `backend/llm/assistant.py` | Cờ `tra_web` (cần `router` + `tim_them`, D10); `AnswerTrace.web`; `web_gate_open` (D1 — **một chỗ**); `cong_web`; gọi từ `answer_turn`, `answer_turn_stream` (cả nhánh `refusal_no_sources`) và `answer_turn_stream_parallel` **sau khi gộp** trace phụ; `turn_usd` cộng USD Serper. |
| `backend/llm/generator_openai_full_corpus.py`, `full_corpus_prompt.py` | Agent riêng `hue_web_section` + `generate_web_section` (D4: lời dặn `TU_WEB_LUAT`, không công cụ, không lịch sử, không kho, `max_output_tokens` 1024). Agent dựng thêm không đổi yêu cầu nào đang có. |
| `backend/api/routes/chat.py` | `ChatResponse.web`; sự kiện SSE `web` sau `sources` (cả nhánh câu cố định); log D9: `has_web_section`, `web_outcome`, `web_n_ket_qua`, `web_n_ma`, `web_kiem` + mục `tools` "tra_web" (ms, trạng thái, mã lỗi, số kết quả, USD) — không chữ. |
| `backend/api/app.py` | `app.state.tim_web` dựng ở rìa từ `SERPER_API_KEY` khi cờ bật (khoá không đọc / in ở đâu khác). |
| `backend/config/settings.yaml` | `tra_web: false`, `tra_web_timeout_seconds: 5`. |
| `backend/api/conversations.py` | Chỉ sửa docstring `stored_answer` (xem lệch 1). |
| `frontend/src/markdown.js`, `App.jsx` | `renderWebHtml`: mã `[w n]` ⇒ số nhỏ link `#web-<lượt>-<n>`; khối "Từ web (chưa kiểm)" + danh sách nguồn web (tiêu đề, tên miền, link ngoài `rel="noopener noreferrer nofollow"`, trình duyệt kiểm lại gốc `http(s)://`); trạng thái "Kho chưa có — đang tra web…". |
| `backend/tests/test_b6_tra_web.py` (mới), `test_assistant_boundary.py` | Xem mục 3; boundary cho `httpx` ở `llm.tra_web`. |

**Lệch nhỏ so với plan (B tự quyết trong phạm vi, luật 05/11 (3)):**
1. **D7:** plan ghi "`stored_answer` cắt khối Từ web". Code làm trực tiếp hơn: chữ web **không bao giờ** vào `trace.answer` (nằm riêng ở `trace.web`), nên lịch sử nhớ không thể chứa chữ web, không cần cắt. Test route kiểm lịch sử (nhớ cả câu trả lời) không có chữ web.
2. **D6 "mục web stream sau":** mục web gửi **một sự kiện `web`** (không stream từng chữ) vì kiểm cuối D5 phải xong trước khi hiện (rào 3). Trước đó có trạng thái `tra_web`. Chữ đầu mục web (Q5) = lúc gửi sự kiện `web`.
3. **D6 "link trong khung nguồn":** danh sách nguồn web nằm ngay dưới khối "Từ web" của lượt (không ở khung nguồn kho bên cạnh) ⇒ mã `[w n]` luôn có đích trong cùng lượt.
4. **0 kết quả:** plan không ghi; code ra câu cố định riêng "Mình chưa tìm thấy thông tin phù hợp trên web." (`web_rong`).
5. **Model lỗi ở lần gọi mục web:** ra câu cố định của `web_loi` + `kiem = ["model_loi"]` (câu kho vẫn hiện; lỗi có trong log).
6. **USD Serper:** ghi 0,001 / lần khi Serper trả 200 (gói rẻ nhất, B122); probe bước 3 xác nhận cách tính lượt dùng thử.

## 3. Cách đã chạy thật

Từ `/tmp/b_b6/backend`:

```bash
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest -q -p no:cacheprovider tests/test_b6_tra_web.py tests/test_assistant_boundary.py \
  -k "not non_stream_path and not stream_paths and not chat_route_never and not flag_off_never"
```

## 4. Kết quả quan sát

- **48 passed** (test thuần B6 + boundary) [Chạy]. Gồm: truy vấn D2; schema / link / `utm_*`; thiếu khoá ⇒ 0 request; thân yêu cầu do code dựng; 7 loại lỗi Serper ≠ rỗng; kiểm cuối từng luật (9 ca); câu lưu trú có giá; cổng 13 nhánh (gồm `refusal_no_sources` mở, `OUT_OF_SCOPE_ANSWER` không mở, khoảng trắng thừa mở, trả lời một phần không mở, lượt ghép không mở); lần gọi mục web: lời dặn riêng, `tools` rỗng, **một** tin nhắn user (không lịch sử), không link trong đầu vào; đoạn trích cài lệnh ⇒ mục bị bỏ (3 dạng: tên miền trần, link Markdown, mã ngoài sổ); lỗi tra / 0 kết quả ⇒ 0 lần gọi model; model lỗi ⇒ câu cố định.
- **Sau C192 (chỉ mục mới 8.435 điểm) [Chạy]:**
  - **Lỗi thật test bắt được ⇒ sửa `d7ec216`:** đường #6 dựng bản cờ `replace(flags, router=False)` cho phần chạy song song; cờ `tra_web` đòi `router` ⇒ `ValueError` ⇒ **mọi lượt stream sẽ vỡ khi bật `tra_web`** (vì `song_song_tra_loi` đang bật). Sửa: bản cờ đó tắt luôn `tra_web` (phần song song vốn không được tra; cổng chạy bằng cờ gốc sau khi gộp).
  - **51 / 51 test B6 passed** (gồm 6 test Qdrant: 3 đường mở cổng sau câu trả lời, chữ web không đi qua `delta`; câu trò chuyện qua #6 song song ⇒ 0 request Serper; cờ tắt ⇒ 0 request; route: `sources` < `web` < `done`, `/api/chat` có `web`, lịch sử nhớ cả câu trả lời không chứa chữ web, log `has_web_section` / `web_*` đúng, không chữ truy vấn / kết quả).
  - **216 passed** khi chạy cùng file test bị chạm: `test_b5_lich_trinh`, `test_b2_tool_loop`, `test_b3_memory`, `test_toc_do_song_song`, `test_assistant`, `test_static_ui`, `test_chat_stream`, `test_assistant_boundary`, `test_feedback`, `test_emergency`, `test_citations`. Không chạy `test_api_chat.py` / `test_openai_full_corpus_generator.py` (cần khoá OpenAI).
  - **Build giao diện** `npm ci && npm run build` ở worktree: xong.
  - **Q1 ĐẠT 228 / 228 giống byte `main`**: `capture_all.py` (qua `/tmp/b164/capture_flags.py`, không cờ) trên nhánh ↔ file chụp `main` `2693422` cùng chỉ mục (`data/phase_9/sua_lich/q1/main_2693422.jsonl`) — sha `dba1f578eef1` cả hai.
  - **Q1m ĐẠT 228 / 228**: cờ `tra_web` bật ↔ tắt, chạy **không** có `SERPER_API_KEY` (`env -u`) như plan Q1m; sha `dba1f578eef1` (`data/phase_9/b6/q1/nhanh_tat.jsonl`, `nhanh_bat.jsonl`). Đúng như plan: lượt chụp chỉ chứng minh phần trước cổng (công cụ chụp dừng ở lần gọi model đầu); hành vi cổng do test.
- **Probe Serper thật (bước 3, 19:57 05/11/2026) [Chạy] — ĐẠT, không chạm điều kiện dừng:** 1 lần gọi (`data/phase_9/b6/tools/probe_serper.py`, câu tìm công khai tự viết; phản hồi thô private `data/phase_9/b6/probe/serper_raw.json`). HTTP 200, 2,16 s; khoá cấp trên `organic` / `searchParameters` / `credits`; mục `organic` có `title`, `link`, `snippet` (+ `date`, `position`, `rating`…) ⇒ **khớp schema code dùng**; `searchParameters` xác nhận `gl=vn`, `hl=vi`, `num=5`; `credits: 1` ⇒ **1 lượt / lần gọi** như B122. Chính phản hồi đó qua `doc_ket_qua` ⇒ sổ web 5 mục, tên miền đúng. Phản hồi không cho biết lượt là dùng thử hay trả phí ⇒ code giữ 0,001 USD / lần (cận trên); 2,16 s là phần chờ đáng kể của đường web (theo dõi Q5).
- Tiền: phần code **0 USD**; probe ≤ **0,001 USD** (0 nếu còn lượt dùng thử).

## 5. Lỗi và giới hạn

- Test dùng Serper ghi sẵn (khuôn theo tài liệu Serper, B122 "[Tự khai] (trường)") ⇒ schema thật chỉ chắc sau probe bước 3.
- Mẫu bắt URL (D5 (ii)) có thể bắt nhầm chữ thường có dạng `x.vn` / `x.com` ⇒ mục bị bỏ (an toàn hơn để lọt) — theo dõi ở Q5 (`web_kiem`).
- Câu hỏi tiếp ("còn giá vé ở đó?") tra bằng câu lượt này ⇒ truy vấn mơ hồ (plan §10).
- Chưa có điều kiện "lượt có thời tiết (B5b)" ở cổng — B5b chưa có trên `main`; thêm khi B5b merge.

## 6. Bàn giao cho người kiểm

- Đọc trước: plan bản 3 D1–D10, rồi `assistant.py` `web_gate_open` / `cong_web` / 3 chỗ gọi, `tra_web.py` `kiem_muc_web`, `chat.py` `_web_payload`.
- Chạy lại: `tests/test_b6_tra_web.py` (cần Qdrant cho 6 test cuối). Bước tiếp của plan: probe Serper thật (≈ 0,001) ⇒ đã thấy ×2 (lượt có phí).
