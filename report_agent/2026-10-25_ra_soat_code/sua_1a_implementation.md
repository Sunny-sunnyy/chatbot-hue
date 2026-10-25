# Implementation Report: rà code — gói 1a (C-09: citation `[Nguồn n]`)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-7f`) · việc C35
Date: 2026-10-25 19:51 (`date`) · nền `main` `5d3376f` · chưa commit (A commit sau review)
Canonical: `bao_cao_he_thong/DE_XUAT_SUA_CODE.md` gói 1a (User duyệt 19:4x); mục C35 trong `session_prompt/CURRENT_HANDOFF.md`;
finding C-09 `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md`. Review: B.

## 1. Phạm vi

- **Được duyệt:** validator citation nhận cả `[n]` lẫn `[Nguồn n]` (hoa / thường, khoảng trắng); text gửi UI đổi `[Nguồn n]` → `[n]`
  (`frontend/app.js` chỉ tách `[n]`, không sửa frontend). **Không** đổi prompt hay nhãn context (đó là thí nghiệm).
- **File:** `backend/llm/citations.py`, `backend/tests/test_citations.py` (giao ban đầu); `backend/api/routes/chat.py` (A duyệt thêm 19:5x —
  `chat.py` trả `generated.text` nguyên văn nên không sửa được text gửi UI chỉ trong `citations.py`); `backend/tests/test_api_chat.py` (A duyệt
  19:5x, cho ca test route A yêu cầu). Không chạm file khác; B26 (tài liệu) làm song song trên `guides/`, không chồng.
- Paid: 2 lượt `gpt-6-luna`, **0,000427 USD** (trần chung gói 1–5: 0,05 USD).

## 2. Thay đổi chính

- `llm/citations.py`: một pattern chung `CITATION_PATTERN = \[\s*(?:nguồn\s*)?(\d+)\s*\]` (`re.IGNORECASE`) — `select_cited_sources` đếm
  marker bằng pattern này (luật cũ giữ nguyên: câu từ chối không được có citation, câu trả lời phải có ≥ 1 citation, id phải có trong context);
  hàm mới `normalize_citations(answer)` thay mọi marker khớp pattern bằng `[n]`. Comment ghi *vì sao* (context gắn nhãn `[Nguồn n]`).
- `api/routes/chat.py` (+2 / −2 dòng thực): `answer = normalize_citations(generated.text)`; dùng `answer` cho cả `select_cited_sources` lẫn
  `ChatResponse`. Không đổi import nào khác (gói 1b sẽ sửa import của file này — diff giữ nhỏ để rebase dễ).
- Test: `test_citations.py` +3 test (5 ca): `[Nguồn 2]`; trộn `[1]` + `[Nguồn 2]`; hoa / thường / khoảng trắng; `[Nguồn 99]` vẫn lỗi; câu từ
  chối kèm `[Nguồn 1]` vẫn lỗi; `normalize_citations` chỉ đổi marker (chữ "Nguồn" thường và `[Nguồn]` không số giữ nguyên, câu từ chối giữ
  nguyên). `test_api_chat.py` +1 test route: retrieval + context thật (Qdrant chỉ đọc, e5 local), generator thay bằng text cố định
  "… [Nguồn 1]." đặt vào `app.state` (chỉ để kiểm logic route, không gọi OpenAI, **không** dùng `require_openai_key` — C-17) ⇒ 200, `answer`
  chỉ còn `[1]`, `sources` = `[1]`. Test trả generator gốc về `app.state` trước khi tắt app để lifespan đóng đúng client thật (khi có key).
- **Định nghĩa "lỗi citation" của evaluator đổi từ commit này.** `evaluation/full_corpus_eval.py:361` và `experiments/phase_8_1/g2_generate.py:206`
  gọi cùng `select_cited_sources` ⇒ tự dùng validator mới; chúng **lưu `answer` gốc** (text lưu có thể còn `[Nguồn n]`) nhưng `citation_error`
  tính theo định nghĩa mới. ⇒ Số lỗi citation cũ (7B, 8.1, G0.6, B1) **không so trực tiếp** với số đo sau commit này; tính lại ở gói 3c, ra file
  mới, **không ghi đè G0.6** (manifest `9ea480d0d083`). Evaluator / harness không sửa.

## 3. Cách đã chạy thật

Từ `backend/`, `main` `5d3376f` + diff trên; script của C ở `/tmp/c35/`, bản dùng lại `data/ra_soat_code_2026-10-25/tools/sua_1a/` (private):

1. `HF_HUB_OFFLINE=1 uv run python -I /tmp/c35/offline_compare.py before` — **trước khi sửa**: chạy `select_cited_sources` của HEAD trên mọi câu
   trả lời đã sinh thật, ghi từng câu (tập id nguồn trích hoặc loại lỗi) ra `/tmp/c35/before.json`. 14 file: 7B Run 1 / 2 (176 + 176), 8.1 G2
   (G2.0 dev / test, G2.1a dev / test, G2.1b thứ tự, P1, P2, G2.4 none / low / high), 8.2 B1 dev / test — 1.600 câu (bỏ câu có lỗi kỹ thuật).
   Nguồn dựng như harness G2 (`PackedSource` id 1..`context_sources`).
2. Sửa code ⇒ `… offline_compare.py after` (so từng câu với `before.json`).
3. `HF_HUB_OFFLINE=1 uv run python -I /tmp/c35/normalize_check.py` — `normalize_citations` trên 1.600 câu.
4. `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_citations.py tests/test_full_corpus_context.py tests/test_full_corpus_eval.py -q -p no:cacheprovider`;
   `… tests/test_api_chat.py -q`; `… -v` cho test mới. Không `--env-file`.
5. `HF_HUB_OFFLINE=1 uv run --env-file ../.env python -I /tmp/c35/live_api.py` — `create_app` thật (lifespan thật: build record, Qdrant đọc, e5 CPU,
   generator `gpt-6-luna` thật), `POST /api/chat` qua route thật (ASGI trong tiến trình), 2 câu **tự viết** (không lấy Golden). Bọc
   `generate_answer` chỉ để đọc usage (trả nguyên kết quả).

## 4. Kết quả quan sát

**Tiêu chí (1) — offline trên mọi file đã sinh: ĐẠT.**

| File | câu | lỗi citation trước → sau | câu đạt thành lỗi | câu đạt đổi tập nguồn |
|---|---:|---:|---:|---:|
| 7B Run 1 | 176 | 4 → **0** | 0 | 0 |
| 7B Run 2 | 176 | 6 → 2 | 0 | 0 |
| 8.1 G2.0 baseline dev / test | 120 / 56 | 4 / 4 → **0 / 0** | 0 | 0 |
| 8.1 G2.1a context 10 dev / test | 120 / 56 | 4 / 4 → 0 / 0 | 0 | 0 |
| 8.1 G2.1b thứ tự / P1 / P2 | 120 × 3 | 6 / 3 / 1 → 2 / 2 / 1 | 0 | 0 |
| 8.1 G2.4 none / low / high | 120 × 3 | 8 / 9 / 4 → 2 / 4 / 1 | 0 | 0 |
| 8.2 B1 dev / test | 120 / 56 | 6 / 6 → 0 / 0 | 0 | 0 |
| **Tổng** | **1.600** | **69 → 14** (55 câu hết lỗi) | **0** | **0** |

14 lỗi còn lại đều là `Grounded answer has no citation` (không có ngoặc số nào). `normalize_citations`: đổi text **đúng 55 câu** (đều có chữ
"Nguồn" — chính các câu hết lỗi), 0 câu khác bị đổi, 0 câu còn sót `[Nguồn`, marker trước = sau ở cả 1.600 câu; câu từ chối không đổi.
Số khớp bảng C-09 tính độc lập trước đó (`recheck_both.py`, có chuẩn hóa NFC) ⇒ không có câu dạng NFD bị lọt.

**Tiêu chí (2) — test: ĐẠT.** `test_citations.py` + `test_full_corpus_context.py` + `test_full_corpus_eval.py`: **35 passed** (17,9 s). Test mới
`-v`: 10 / 10 ca `test_citations.py` + test route đều PASSED. `test_api_chat.py` cả file: **4 passed, 3 error** — 3 error là test cũ dùng
`require_openai_key` khi không có key (`pytest.fail`, lỗi đã biết C-17), không liên quan thay đổi này; test route mới chạy được khi không có key.
Test route cần Qdrant `:6335` đang chạy (đọc collection runtime) + e5 trong HF cache — giống các test retrieval khác.

**Tiêu chí (3) — API thật: ĐẠT.**

| Câu (tự viết) | status | marker trong `answer` | `sources` | khớp | `answer` còn `[Nguồn` |
|---|---|---|---|---|---|
| 1 | 200 | [1, 2, 3] | [1, 2, 3] | ✔ | không |
| 2 | 200 | [1, 2] | [1, 2] | ✔ | không |

2 lượt gọi, input 1.637 + output 526 token = **0,000427 USD**. Cả hai lượt model tự viết `[n]` (không viết `[Nguồn n]` — dạng này hiếm, ~4,5 %
câu ở 8.1) ⇒ lượt thật chứng minh route + validator mới không làm hỏng đường bình thường; nhánh `[Nguồn n]` trên route được chứng minh bằng
test route (logic) + 55 câu thật đã sinh (offline).

`git diff --check`: sạch. `git diff --stat` phần của C: `chat.py` 7, `citations.py` 9, `test_api_chat.py` 21, `test_citations.py` 30 dòng.

## 5. Lỗi và giới hạn

- Chưa quan sát một lượt API thật mà model viết `[Nguồn n]` (không ép được nếu không đổi prompt — ngoài phạm vi). Muốn quan sát phải gọi
  ~20+ câu (tốn ~0,005 USD) — không làm, vì offline 55 câu thật + test route đã che nhánh đó.
- Pattern nhận thêm `[ 2 ]` (khoảng trắng trong ngoặc) cho cả dạng `[n]` — mục việc cho phép "khoảng trắng"; 1.600 câu: không câu đạt nào đổi tập
  nguồn ⇒ không có tác dụng phụ quan sát được.
- Pattern không nhận dạng NFD của "nguồn" (model trả NFC; đếm lại với NFC cho cùng số). Không thêm chuẩn hóa NFC (không có nhu cầu quan sát được).
- Không đổi evaluator / harness: `answer` lưu trong file kết quả sau này vẫn là text gốc của model (có thể còn `[Nguồn n]`), khác `answer` API trả.
- Số lỗi citation theo định nghĩa mới cho các mốc cũ chỉ có trong bảng trên (tính offline); file số mới chính thức là việc của gói 3c.

## 6. Bàn giao cho người kiểm (B)

- Đọc trước: `git diff backend/llm/citations.py backend/api/routes/chat.py backend/tests/test_citations.py backend/tests/test_api_chat.py`; mục 4.
- Chạy lại (free): `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_citations.py tests/test_full_corpus_context.py
  tests/test_full_corpus_eval.py "tests/test_api_chat.py::test_chat_returns_bracket_citations_when_model_writes_nguon_label" -q`. So offline: người
  kiểm tự viết script (hoặc đọc `data/ra_soat_code_2026-10-25/tools/sua_1a/offline_compare.py`); mốc "trước" phải chụp từ `5d3376f`
  (`git show 5d3376f:backend/llm/citations.py`), không dùng `before.json` của C.
- Lượt paid chỉ khi B thấy cần (≤ 1–3 câu, trong trần 0,05 USD chung).
- Lệch đã được duyệt: thêm `chat.py` + `test_api_chat.py` (A 19:5x).
