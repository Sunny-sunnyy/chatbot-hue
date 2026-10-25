# Review: rà code — gói 1a (C-09: citation `[Nguồn n]`) — C35

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor không chặn) — việc rủi ro trung bình ⇒ A đóng, báo User
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-c3`)
Date: 2026-10-25 19:56 +0700 (`date`) · nền `main` `5d3376f` + diff chưa commit của C · chỉ đọc · **0 USD** (không gọi paid)
Canonical guide: mục C35 trong `session_prompt/CURRENT_HANDOFF.md` (tiêu chí 1–3; A duyệt thêm `chat.py`, `test_api_chat.py` 19:5x);
`bao_cao_he_thong/DE_XUAT_SUA_CODE.md` gói 1a
Implementation report: `report_agent/2026-10-25_ra_soat_code/sua_1a_implementation.md`

Không đọc `STATUS_C.md`; không dùng script hay `before.json` của C — mốc "trước" lấy thẳng từ `git show 5d3376f:backend/llm/citations.py`.

## 1. Phạm vi đã review

- **Cổng tối thiểu:** `git status --short` — phần của C đúng 4 file khai báo (`backend/llm/citations.py`, `backend/api/routes/chat.py`,
  `backend/tests/test_citations.py`, `backend/tests/test_api_chat.py`) + report untracked; các file `guides/` đang đổi là của B26 (B, không
  chồng). Exact diff 4 file đã đọc hết; `git diff --check -- backend/` sạch. Không có thay đổi ngoài phạm vi (không đổi prompt, nhãn context,
  evaluator, harness, frontend).
- Đọc thêm: mọi nơi dùng `select_cited_sources` / `CITATION_PATTERN` (`grep -rn` trong `backend/`, `frontend/`, `notebooks/`) — chỉ route,
  evaluator (`full_corpus_eval.py:361`), harness 8.1 (`g2_generate.py:206`); `frontend/app.js:44` tách `\[\d+\]`.

## 2. Findings

Không có blocker hoặc major.

### m-01 (minor) — Regex không khớp chữ "nguồn" dạng NFD ⇒ fail-closed như trước (A hỏi (a))
- Vị trí: `backend/llm/citations.py:11`.
- Bằng chứng: probe `CITATION_PATTERN.findall(unicodedata.normalize("NFD", "[Nguồn 2]"))` ⇒ `[]`; dữ liệu thật `c35_offline.py`: **0 / 1.600** câu
  trả lời có dạng NFD (`unicodedata.normalize("NFC", a) != a`) ở cả 14 file.
- Tác động: câu NFD (chưa từng thấy) sẽ vẫn ra 500 `citation_integrity_error` như hành vi cũ — không sai lặng, không mất an toàn. Thêm chuẩn hóa
  NFC là phòng xa khi chưa có quan sát (`Session_Prompt.md` §7) ⇒ đồng ý với C để nguyên.
- Tiêu chí đóng: không cần sửa; nếu log thấy `citation_integrity_error` mà text có "Nguồn" thì mở lại.

### m-02 (minor) — Test route dùng generator cố định (stub) — hợp contract test, không phải bằng chứng provider (A hỏi (c))
- Vị trí: `backend/tests/test_api_chat.py:98-114`.
- Quan sát: test dựng `create_app(load_settings())` thật (lifespan thật: build record, Qdrant `:6335` chỉ đọc, e5 local, tokenizer, context builder
  thật), chỉ thay `app.state.generator` bằng một lớp trả text cố định rồi trả lại bản gốc trước khi tắt app. Không gọi OpenAI, không cần key, không
  ghi Qdrant. Cùng kiểu phụ thuộc như các test hiện có: `conftest.py` ghi "Fixtures dùng runtime thật (build record, Qdrant chỉ đọc, e5 local)";
  `test_citations.py` vốn đã cần Qdrant qua fixture `full_corpus_documents`.
- Đánh giá: đây là kiểm logic của route (text đã chuẩn hóa được dùng cho cả validator lẫn `ChatResponse`) với input nhỏ — hợp `Session_Prompt.md`
  §6 vì **không** là bằng chứng duy nhất: đường model thật có 2 lượt API thật của C (report §4) + 55 câu thật đã sinh offline. Không cần
  `require_openai_key` (tránh C-17) — đúng.
- Tiêu chí đóng: không cần sửa. Ghi nhận: test phụ thuộc kho có ≥ 1 nguồn cho câu hỏi cố định (nếu kho đổi tới mức câu đó ra fallback, test đỏ —
  dễ chẩn đoán).

### Ghi chú (không phải finding)
- (b) A hỏi: `normalize_citations` có đổi ngoài ý muốn không. **Không** trên dữ liệu: text bị đổi đúng **55** câu, **0** câu vốn đạt bị đổi text
  (`text_changed_on_ok = 0`); **0** câu có dạng khoảng trắng trong ngoặc (`[ 3 ]`, `[3 ]`, `[Nguồn2]`, `[ Nguồn…`) ở 1.600 câu; sau chuẩn hóa 0 câu
  còn `[nguồn`, marker `[n]` sau chuẩn hóa = marker regex mới trên text gốc ở mọi câu; validator mới trên text đã chuẩn hóa = trên text gốc ở mọi câu.
- Hành vi giữ nguyên (probe): `[1](http://x)` vẫn tính là citation 1 và text giữ nguyên; `[2024]` vẫn tính là id 2024 (⇒ lỗi id lạ như trước);
  `[Nguồn 1, 2]` không khớp (như trước). Không câu thật nào có các dạng này (lỗi còn lại chỉ loại "không có citation").
- Report §2 ghi đúng: evaluator / harness lưu `answer` gốc, `citation_error` theo định nghĩa mới ⇒ số cũ không so trực tiếp; tính lại ở 3c ra file
  mới, không ghi đè G0.6.

## 3. Cách người kiểm chạy lại thật

- `git show 5d3376f:backend/llm/citations.py > /tmp/b27/citations_old.py`; `cd backend && HF_HUB_OFFLINE=1 uv run python -I /tmp/b27/c35_offline.py`
  — nạp validator cũ (file trên) và mới (working tree), chạy trên mọi câu trả lời đã sinh thật: `data/evaluation/phase_7b/run{1,2}_answers.jsonl`,
  `data/phase_8_1/g2/*.jsonl` (bỏ `pilot` / `rest`), `data/phase_8_2/b1/b1_{dev,test}.jsonl` — 14 file; nguồn dựng id 1..`context_sources` như harness
  G2. Chỉ in số đếm.
- Probe regex (`uv run python -I -c …`) trên 9 chuỗi tự viết (NFC, NFD, hoa, không dấu, không cách, link Markdown, năm, nhiều id, khoảng trắng).
- `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_citations.py tests/test_full_corpus_context.py tests/test_full_corpus_eval.py
  tests/test_api_chat.py -q -p no:cacheprovider` — **không** `--env-file`; Qdrant `:6335` trả 200 trước khi chạy.
- Không gọi API trả phí (dùng lại 2 lượt live của C — xem §4).

## 4. Kết quả quan sát

- **Offline (fresh, script B):** 1.600 câu · lỗi citation **69 → 14** · câu đạt thành lỗi **0** · câu đạt đổi tập nguồn **0** · text đổi 55 (đều là câu
  vốn lỗi) · NFD 0 · dạng khoảng trắng 0 · 14 lỗi còn lại đều `Grounded answer has no citation`. Từng file khớp bảng §4 report C (7B Run 1 4 → 0, Run 2
  6 → 2, G2.0 4 / 4 → 0 / 0, G2.1a 4 / 4 → 0 / 0, G2.1b 6 / 3 / 1 → 2 / 2 / 1, G2.4 8 / 9 / 4 → 2 / 4 / 1, B1 6 / 6 → 0 / 0). ⇒ **tiêu chí (1) ĐẠT**.
- **Pytest (fresh):** `39 passed, 1 warning, 3 errors in 25.88s`. 3 error = `test_health_is_cached_and_ready_after_real_lifespan`,
  `test_real_first_chunk_budget_error_has_no_partial_answer`, `test_production_app_state_has_no_last_chat_trace_after_chat`, cùng thông điệp
  `Failed: OPENAI_API_KEY is not set in the environment` (fixture `require_openai_key`; 3 test này đã có ở `5d3376f` — `git show … | grep -c
  require_openai_key` = 3) ⇒ lỗi đã biết C-17, không do C35. Test mới (5 ca citations + 1 route) nằm trong 39 passed ⇒ **tiêu chí (2) ĐẠT**.
- **API thật — dùng lại bằng chứng của C (không phải lần chạy mới):** 2 câu tự viết, 200, `sources` khớp marker, 0,000427 USD (report §4). Dùng lại
  hợp lệ vì B review đúng diff mà C đã chạy (không đổi sau lượt live). Lượt live không có câu `[Nguồn n]` (model tự viết `[n]`) — nhánh đó được che bởi
  test route + 55 câu thật offline ⇒ **tiêu chí (3) ĐẠT** với giới hạn C đã ghi.
- Độ đơn giản: 1 regex + 1 hàm 1 dòng + 2 dòng route; không lớp / cấu hình / fallback mới ⇒ tương xứng.

## 5. Giới hạn hoặc phần chưa chạy

- Không quan sát qua HTTP một câu model thật viết `[Nguồn n]` (B không gọi paid; C cũng chưa — hiếm, ~4,5 % câu).
- Không chạy cả `backend/tests/` (chỉ 4 file liên quan, theo `Project_Status.md` §8).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Gói 1a đúng mục việc: 500 do `[Nguồn n]` hết trên mọi dữ liệu đã sinh, không câu đạt nào đổi, UI nhận `[n]`.
A tự đóng (rủi ro trung bình), commit 4 file + report + review, báo User; trong báo cáo cho User ghi rõ định nghĩa "lỗi citation" đổi từ commit
này (số cũ không so trực tiếp; tính lại ở 3c ra file mới). Sau commit: cập nhật `Project_Status.md` §8 (bẫy `[Nguồn n]` đã có xử lý ở validator) và
4 chỗ `bao_cao_he_thong/` (hành vi API đổi).
