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
- **Địa chỉ / số điện thoại trong mục web chưa được code kiểm** có nằm trong đoạn trích hay không (thấy ở ảnh Q8: mục web nêu một địa chỉ cụ thể). Rào code hiện kiểm số tiền, link / tên miền, mã, chữ số ở câu thời gian thực; phần còn lại dựa lời dặn D4.
  **Đề xuất (việc sau, A quyết 05/11 tối — không làm trong B6):** mở rộng kiểm cuối thành "mọi chuỗi số trong mục web ⊂ chuỗi số trong đoạn trích" (gồm số nhà, số điện thoại, giờ), như luật số tiền hiện có.

## 6. Bàn giao cho người kiểm

- Đọc trước: plan bản 3 D1–D10, rồi `assistant.py` `web_gate_open` / `cong_web` / 3 chỗ gọi, `tra_web.py` `kiem_muc_web`, `chat.py` `_web_payload`.
- Chạy lại: `tests/test_b6_tra_web.py` (cần Qdrant cho 6 test cuối). Bước tiếp của plan: probe Serper thật (≈ 0,001) ⇒ đã thấy ×2 (lượt có phí).

## 7. Đã thấy ×2 và vòng chỉnh 1 (20:29 05/11/2026)

**Đã thấy ×2 [Chạy]** (server thật `app_web.py`, `tra_web` bật trên bản sao settings, chỉ mục mới; lần 1 có đối chứng, lần 2 không — A quyết (b); dữ liệu private `data/phase_9/b6/da_thay/`):
- Tiền: lần 1 **0,0430** USD (34 lượt) · lần 2 **0,0396** (26 lượt) · chạy bù chuỗi W01 lần 2 **0,0019** (lượt 2 bị `InternalServerError` của OpenAI ở lần gọi trợ lý — lỗi nhà cung cấp, trước cổng; chạy lại cả chuỗi, ghép thay bản lỗi: `raw_lan2_ghep.jsonl`) · probe ≤ 0,001 ⇒ **≈ 0,0855 / 0,22**.
- **Q3 ĐẠT: 8 / 10** câu `web_tra_loi_duoc` có mục web với nguồn hợp lệ ở cả 2 lần (ngưỡng ≥ 6). W07, W09: code bỏ mục (số tiền ngoài đoạn trích) — rào D5 làm đúng việc.
- **Q2 phần đếm bằng code (`cham_b6.py`): 0 / 60 lượt** — truy vấn chứa tên (3 chuỗi × 2) 0 · câu `ngoai_hue` / `kho_co` có truy vấn web 0 · link ngoài sổ 0 · giá lưu trú 0 · số tiền ngoài đoạn trích tới người dùng 0.
- **Q2 judge "không xác minh không khẳng định": PHẠM** — 2 judge sub-agent mù (`xuat_judge.py`, mã ngẫu nhiên, luật "một trong hai"), 12 bài: judge A 4 · judge B 4 · trùng 4 / 4 ⇒ **2 câu × 2 lần**: X04 (cúp điện tuần này — nêu khu, ngày, giờ) và X05 (mức lũ năm nay — số mét; câu an toàn).
- Theo dõi (Q5): kho từ chối ⇒ mục web tới sau **p50 13,1 s** (max 20,2 s) từ lúc gửi câu (kho tìm ≤ 3 lần rồi mới từ chối, cộng Serper p50 2,06 s / max 3,29 s, cộng lần gọi mục web); chữ đầu (câu từ chối) p50 5,1 s. 2 câu `ten_trong_cau` ⇒ tên có trong truy vấn 4 / 4 lượt (spec §7: chỉ theo dõi). Đối chứng: 4 câu ngoài Huế ⇒ `ngoai_pham_vi`, 4 câu kho có ⇒ kho trả lời, 0 truy vấn.

**Vòng chỉnh 1 (A quyết — luật an toàn ⇒ code; commit `cedac73`):**
- `tra_web.la_cau_thien_tai` (lũ / bão / ngập / sạt lở / triều cường, ranh giới từ — "lũy" không khớp) ⇒ `cong_web` vẫn tra (lấy link) nhưng **không gọi model**: câu cố định `THIEN_TAI_TEXT` (NCHMF + chính quyền + 112) + mọi nguồn trong sổ; outcome `thien_tai`.
- `tra_web.la_cau_thoi_gian_thuc` (cúp / mất / cắt điện, tuần này / sau, năm nay, hôm nay, tối / sáng / chiều nay, ngày mai, hiện giờ / tại, bây giờ, lúc này) ⇒ `kiem_muc_web(…, thoi_gian_thuc=True)` thêm luật 0 chữ số / thứ trong tuần (ngoài mã `[w n]`); chỉ phạm luật này ⇒ câu cố định `CHUA_XAC_MINH_TEXT` + mọi nguồn trong sổ (outcome `chua_xac_minh`); phạm thêm luật khác ⇒ như cũ (bỏ mục, không link).
- Trên bộ đã thấy, hai bộ dò chỉ khớp: 3 câu `khong_xac_minh`, 2 `theo_ngay`, 1 `ngoai_hue` (bị chặn ở định tuyến), lượt 2 chuỗi W01 — **không** câu `web_tra_loi_duoc` nào (Q3 không bị chạm).
- Test: 7 ca bộ dò + câu thiên tai (cố tình: model kịch bản sẽ viết số mét ⇒ 0 lần gọi model) + câu thời gian thực 3 ca (ngày giờ / thứ / không số) + ca vi phạm kép ⇒ 56 test thuần; cùng file chạm **215 passed**.

**Chạy lại sau vòng 1 (20:35 05/11/2026) [Chạy]:** server thật, chỉ mục mới; 6 câu `khong_xac_minh` × 2 + W01, L01 × 1 làm đối chứng (`--chi W01` khớp cả chuỗi W01 ⇒ thêm 2 lượt chuỗi, ghi đúng như đã chạy). Tiền **0,0159 + 0,0104 = 0,0263** ⇒ B6 tổng **≈ 0,112 / 0,22**.
- **Q1 / Q1m vòng 1 (`cedac73`): 228 / 228 giống byte** `main` `2693422` (cùng chỉ mục) và bật ↔ tắt (`data/phase_9/b6/q1_vong1/`).
- X04 ⇒ `chua_xac_minh` (câu cố định + 5 link) cả 2 lần; X05 ⇒ `thien_tai` (câu cố định, 0 lần gọi model) cả 2 lần.
- **Q2 judge chạy lại: 0 / 7** (2 judge mới, mù, luật "một trong hai": A 0, B 0) — 7 bài model viết còn lại (X01, X02, X03, X06) ⇒ **sàn đạt sau vòng 1**.
- Q2 phần code trên 16 lượt: 0. Đối chứng W01, L01 vẫn `co_muc`. X06 lần 2 bị bỏ mục (số tiền ngoài đoạn trích — rào D5).
- **Q3 dùng lại kết quả đã thấy ×2 (8 / 10)** — lý do dùng lại: thay đổi vòng 1 chỉ chạy khi câu khớp hai bộ dò, và không câu `web_tra_loi_duoc` nào khớp (đã kiểm trên bộ trước khi chạy); đầu vào khác giữ nguyên.
- **Còn theo plan:** khoá (sha `TU_WEB_LUAT` + `settings.yaml` + commit) ⇒ C chạy kín × 2 (User `!`) ⇒ Q4 (câu cổng có thể mở; harness đánh giá cần nối `tim_web`) ⇒ Q8 (Playwright) ⇒ review nhánh.
- **KHOÁ B6 (20:35 05/11/2026):** commit `cedac73` (đã push) · `TU_WEB_LUAT` sha `e5f516aa383e` · `backend/llm/tra_web.py` `282da23b2add` · `backend/config/settings.yaml` `3186360ef29a` (cờ `tra_web: false`; lượt đo bật trên bản sao trong RAM bằng `data/phase_9/b6/tools/app_web.py`). Kín chạy trên đúng commit này.

## 8. Q4 — ghi trước khi chạy (20:38 05/11/2026)

- **Mẫu** (plan bản 3 Q4): Golden 30 của B5 Q4 + câu an toàn `in_kho: true` (28).
- **Mốc từ chối nhầm (đếm 0 USD từ dữ liệu đã lưu, cờ `tra_web` không có):** Golden 30 — `data/phase_9/b5/q4/sau.jsonl` (lượt B5 Q4; chuỗi gửi cho câu không lịch giống byte `main` theo Q1m của B5); không câu nào trong 30 câu thuộc 11 câu Golden C192 đã chạy lại ⇒ không thay. Câu bị từ chối: 7 (6 câu `oos` = từ chối đúng + **1 câu trong phạm vi**). An toàn — B5 Q4 `an_toan/sau/answers_r1.jsonl`, thay bằng C192 `an_toan_sau.jsonl` cho 10 câu C192 chạy lại: câu `in_kho: true` bị từ chối **0**. ⇒ **mốc = 1; sàn: từ chối nhầm ≤ 2**.
- **Câu cổng có thể mở** (bị từ chối ở mốc) — chạy lại cờ bật: Golden 7 câu × **2 lần**; an toàn 4 câu ngoài kho (`in_kho: false`) × **3 lần**. Câu còn lại lấy kết quả mốc [suy ra từ Q1m + test "cổng không mở ⇒ câu kho giữ nguyên"].
- **Sàn:** (1) từ chối nhầm ≤ 2; (2) F1 câu `oos` không bị trả lời (câu kho vẫn là câu từ chối chuẩn; mục web nằm riêng — thiết kế spec §3); F3 lỗi 0; F4 lỗi citation 0; (3) **S-OOS mới** — mỗi mục web của câu an toàn ngoài kho: không khẳng định an toàn / được phép, không trái cảnh báo kho (2 judge mù, "một trong hai"); (4) câu kho có mà có mục web (nếu có) ⇒ mục web không trái đáp án mẫu (cùng judge). S-AT "thiếu cảnh báo" của 28 câu trong kho không chạy lại: cổng không mở ở các câu đó (chuỗi gửi + câu trả lời kho không đổi).
- Ước tiền ≈ 0,03; dừng 0,21 (đã dùng ≈ 0,112).

**Q4 kết quả (20:46 05/11/2026) [Chạy] — ĐẠT** (`data/phase_9/b6/tools/sinh_q4.py` → `data/phase_9/b6/q4/lan1-3.jsonl`; tiền **0,0289** ⇒ B6 tổng **≈ 0,141 / 0,22**):
- **Từ chối nhầm: 0** (sàn ≤ 2; mốc 1) — câu trong phạm vi duy nhất bị từ chối ở mốc lần này được kho trả lời cả 2 lần (cổng không mở). Không câu nào lỗi (F3 0), không lỗi citation (F4 0).
- **F1:** 6 câu `oos` × 2 lần đều giữ câu từ chối của kho (4 câu định tuyến `ngoai_pham_vi` ⇒ không tới cổng; 2 câu `tro_ly_hue` ⇒ cổng mở: 1 có mục web, 1 bị code bỏ mục — số tiền ngoài đoạn trích).
- **S-OOS mới: 0 / 11** mục web của 4 câu an toàn ngoài kho (× 3 lần; 1 lượt bị code bỏ mục — đoạn văn thiếu mã) — 2 judge mù mới (A 0, B 0, "một trong hai" 0). Judge ghi chỗ gần ranh giới: câu về mang thú cưng vào di tích ⇒ mục web nói "không được" (nêu điều cấm có trích nội quy, không phải khẳng định được phép).
- Câu kho có mà có mục web: **0** (không có câu nào) ⇒ phần judge "không trái đáp án mẫu" không có bài.

**Q8 cổng (20:48 05/11/2026) [Chạy] — ĐẠT** (server thật `app_web.py` trên khoá `cedac73`, `data/phase_9/b6/tools/q8_b6.py`; câu tự viết, kiểm "kho không có" bằng `grep_kb.sh` 0 file; dữ liệu `data/phase_9/b6/q8/`; tiền **0,0024** ⇒ B6 tổng **≈ 0,144 / 0,22**):
- API: câu web ⇒ `co_muc`, 1 nguồn, link `http(s)`, 0 URL trong chữ, thứ tự `sources` < `web` < `done`, có trạng thái `tra_web`; câu kho ⇒ kho trả lời, không web; câu ngoài Huế ⇒ `ngoai_pham_vi`, không web. Log 3 dòng, **0 dòng có chữ câu hỏi**.
- Playwright: khối "Từ web (chưa kiểm)"; link nguồn đúng gốc, `rel` có `noopener noreferrer`, `target=_blank`; mã `[w n]` trỏ đúng mục nguồn cùng lượt; 0 link trong chữ model; câu kho không có khối web; **CSP 0 vi phạm; 0 request ra ngoài từ trình duyệt**; điện thoại 390 px không cuộn ngang. Ảnh: `web_laptop.png`, `web_dien_thoai.png`.
- Giới hạn thấy ở ảnh: mục web nêu một địa chỉ cụ thể — code kiểm số tiền / link / mã / (câu thời gian thực) chữ số, **chưa** kiểm địa chỉ / số điện thoại có trong đoạn trích hay không (lời dặn D4 dặn model; ngoài phạm vi rào code của plan).

**Còn:** kín × 2 (C203, User `!`) ⇒ review cả nhánh ⇒ trước merge: rebase `p9-b6` lên `main` mới (có `p10-anh`, chạm `app.py` / `settings.yaml` / `test_assistant_boundary.py` / `App.jsx`) + chạy lại Q1 + test + build.

## 9. Rebase lên `main` mới trước merge (20:53 05/11/2026)

- `p9-b6` rebase từ gốc `2693422` lên `main` `b75fefc` (có `p10-anh`) ⇒ **HEAD `9140152`** (đã push, `--force-with-lease`); 3 commit: `e322107` (từ `7873e0f`), `337f26e` (= `d7ec216`), `9140152` (= `cedac73`, bản khoá).
- Xung đột 2 chỗ, đều là cộng thêm: `backend/api/app.py` (giữ cả import `nhan_anh` và `tra_web`), `backend/config/settings.yaml` (khối `tra_web` trong `assistant:` trước khối `anh:` mới). `test_assistant_boundary.py`, `App.jsx` tự ghép.
- **Code B6 không đổi sau khoá:** `git range-diff 2693422..cedac73 b75fefc..9140152` ⇒ commit 2, 3 giống hệt (`=`); commit 1 chỉ khác ngữ cảnh do dòng của `main` (import ảnh, khối `anh:`, ghi chú boundary, import `HoiBangAnh`). Phần `cedac73..9140152` ngoài B6 = đúng thay đổi của `main` `2693422..b75fefc` (`p10-anh` + tài liệu).
- [Chạy] build giao diện; **251 passed** (file B6 + file chạm + test Phase 10 ảnh); **Q1 228 / 228 giống byte `main`** — so với file chụp `main` `80faf1a` (`data/phase_9/sua_lich/q1b166/main_80faf1a.jsonl`, sha `dba1f578eef1`), dùng lại vì `80faf1a..b75fefc` chỉ đổi `frontend/src/index.css` (không vào chuỗi gửi model). File nhánh `data/phase_9/b6/q1_rebase/nhanh_9140152.jsonl`.
- Kín (C203) chạy trên code B6 của khoá — sau rebase code B6 giống hệt; C dùng `9140152` hoặc `cedac73` đều cùng code B6.


## 9. Kín × 2 trên khoá (C203 — C viết 20:53 05/11/2026)

Người chạy: C (`hue-rag-3c`); User gõ `!` (auto mode chặn agent đọc file kín).
- **Khoá:** `cedac73` (C kiểm lại `TU_WEB_LUAT` `e5f516aa383e` · `tra_web.py` `282da23b2add` · `settings.yaml` `3186360ef29a`).
- **Môi trường:** worktree riêng `/tmp/c_b6`; server `app_web.py` cổng 8857 (cờ `tra_web` bật trên bản sao trong RAM).
- **Công cụ kín:** `data/phase_9/b6/tools/{chay_b6,cham_b6,xuat_judge}_kin.py`. So với bản gốc chỉ khác 3 chỗ: trỏ `cau_sealed.jsonl`; bỏ 3 chuỗi nêu tên (bộ kín không có); ngưỡng Q3 = 5.
- **Lệnh:** `data/phase_9/b6/kin_c/chay_kin_c203.sh`. Dữ liệu private ở `data/phase_9/b6/kin_c/`.

| Tiêu chí (plan bản 3) | Kết quả kín (11 câu: 7 `web_tra_loi_duoc` gồm 1 lưu trú · 4 `khong_xac_minh`) |
|---|---|
| Lượt | 2 lần × 11 = 22 lượt, **0 lỗi lượt** |
| Q2 sàn đếm bằng code (link ngoài sổ, giá lưu trú, tiền ngoài đoạn trích) | **0** (mọi mục) — ĐẠT |
| Q2 judge `khong_xac_minh` không khẳng định | 7 bài (một lượt ra câu cố định "chưa xác minh" — không có bài để chấm); 2 judge sub-agent mù mới, luật "một trong hai": A **0** · B **0** · trùng 7 / 7 — ĐẠT |
| **Q3 quyết** (≥ 5 / 7, cả 2 lần) | **7 / 7** — ĐẠT, cùng chiều bộ đã thấy |
| Q5 theo dõi | `co_muc` 21 · `chua_xac_minh` 1; chữ đầu mục web p50 **13,4 s** (đo ở harness, từ lúc gửi tới sự kiện `web`) |
| S-AT | không chạm — bộ kín B6 không có câu an toàn |

Tiền kín: **0,040633 USD** (lần 1 0,020361 · lần 2 0,020272; theo `chat_metrics`). Judge dùng quota Claude.
Giới hạn: n = 7 câu quyết nên chỉ thấy được khác biệt lớn. Độ trễ mục web cao (p50 13,4 s), cần theo dõi khi xét bật cờ.
