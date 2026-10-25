# Implementation Report: Phase 8.2 B1 — context 10 + NFC câu hỏi vào chatbot (B23)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-de`)
Date: 2026-10-25 16:45 +0700 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` (User duyệt 16:21, sha `dabae90b2b60`)
§3.2, §4, §5 B1 · plan `phase_8_2_b1_plan.md` (A duyệt sha `1a5ac660bd5d`, review `phase_8_2_b1_plan_review.md`)
Trạng thái: **chờ review** (người kiểm: A). Chưa commit (B không commit).

## 1. Phạm vi

Làm đúng plan: đổi context 5 → 10 đoạn, thêm NFC câu hỏi ở một chỗ, harness đo B1, chạy T1–T5. Không đổi prompt / model / retrieval /
index; Qdrant chỉ đọc; không mở câu kín. Đổi so với plan: thêm file rỗng `backend/experiments/phase_8_2/__init__.py` (cần để chạy
`python -m experiments.phase_8_2.b1`, như `phase_8_1/__init__.py`).

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `backend/config/settings.yaml:56` | `max_context_documents: 10` |
| `backend/core/settings_loader.py:77` | kiểm cứng `!= 10` |
| `backend/tests/test_phase6_settings.py:25` | giá trị ghim 10 |
| `backend/retrieval/full_corpus.py` | hàm thuần `normalize_query` (kiểm rỗng như cũ + `unicodedata.normalize("NFC", …)`); `search` gọi nó ở dòng đầu |
| `backend/tests/test_full_corpus_retrieval.py` | `test_normalize_query_turns_nfd_into_nfc_and_rejects_blank` (chuỗi tự viết) |
| `backend/experiments/phase_8_2/{__init__,b1}.py` (mới) | harness: `run` / `merge` / `check` / `export-judge` / `check-judge` / `analyze` / `nfd-check`; gọi `full_corpus_eval.run_generation` không ghi đè tham số |

Luồng sau sửa: câu hỏi → `search` (NFC → e5 + BM25 → Qdrant → RRF top-10) → context builder lấy **tối đa 10** đoạn → `gpt-6-luna` →
citation. **Giới hạn đã biết (A đồng ý ở review plan):** context builder và model vẫn nhận chuỗi gốc người dùng gửi; chỉ tầng tìm
kiếm được NFC (đúng tầng 8.1 G1.4 đo được hại).

## 3. Cách đã chạy thật

Từ `backend/`, Qdrant `:6335` thật (chỉ đọc), e5-small CPU, `gpt-6-luna` thật:

```bash
# 0. đối chứng trước sửa, code HEAD 5e6936b (free)
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.b1 nfd-check --question "$(cat ../data/phase_8_2/b1/nfd_question.txt)"
# 1. test nhỏ
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_retrieval.py tests/test_full_corpus_context.py tests/test_api_chat.py -q
# 2. T1
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m evaluation.full_corpus_eval retrieval --out /home/minhhieu/hue_rag/data/phase_8_2/b1/retrieval_dense_bm25_rrf.jsonl
# 3. nfd-check sau sửa; lượt sinh: pilot → rest → test_pilot → test_rest; merge
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.b1 run --cases pilot --name b1_pilot   # (rest, test_pilot, test_rest tương tự)
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.b1 merge --parts b1_pilot b1_rest --name b1_dev        # và b1_test
# 4. T2 / T3
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.b1 check
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.b1 export-judge --batch-size 20   # 294 câu trả lời khác nhau / 352, 15 lô
#    8 sub-agent judge Claude mới (model kế thừa session: Claude Opus 5.5, global.anthropic.claude-opus-5-5 — cùng model judge G2),
#    mỗi agent 2 lô (1 agent 1 lô), chỉ Read full_corpus_judge_prompt.md + lô, Write scores_NN.jsonl
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.b1 check-judge
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.b1 analyze
# 5. T4 / T5 live: port 8000 trống (ss -ltn) → uvicorn api.app:app --port 8000 (nền) → /health ok → POST /api/chat câu NFC + bản NFD → dừng server
```

Câu kiểm NFD / live do B tự viết (một câu hỏi giá vé, không lấy từ Golden / câu kín), lưu ở `data/phase_8_2/b1/nfd_question.txt`.

## 4. Kết quả quan sát (lần chạy mới, 16:3x–16:45)

| # | Tiêu chí (spec B1.2) | Kết quả | Đạt |
|---|---|---|---|
| — | test nhỏ (4 file) | **44 passed** | ✓ |
| T1 | retrieval 158 câu giống byte `cefb2d1a…` | sha256 `cefb2d1ad6094913…826e4`, **158** dòng | ✓ |
| T2 | 176 / 176 `top_chunk_ids`, `context_sources`, `input_tokens` = G2.1a | **176 / 176** cả ba trường (0 câu lệch) | ✓ |
| T3 | 0 câu OOS bị trả lời; lỗi kỹ thuật 0; Completeness không khác (CI chứa 0), G2.1a chấm lại cùng lượt mù | OOS trả lời **0 / 18**; lỗi **0**; Completeness 176 câu: +0,023 [−0,006; +0,057] **không khác**, 4 / 171 / 1 | ✓ |
| T4 | `/chat` câu thật: tới 10 nguồn đóng gói, có citation | HTTP 200, có `[n]`; API trích nguồn **số 8** (chỉ có khi context > 5); số nguồn đóng gói = 10 (đo ở T5) | ✓ |
| T5 | câu NFD cùng nguồn với bản NFC | `nfd-check` sau sửa: 10 id `search` **giống**, nguồn đóng gói **giống** (10 / 10). Trước sửa (HEAD): **khác** cả hai — phép đo bắt được thay đổi. Live: NFD HTTP 200, có citation; `sources` API giống bản NFC (chỉ ghi, không quyết) | ✓ |

**Nhiễu A/A context 10** (lượt B1 ↔ G2.1a: cùng đầu vào từng token, chỉ khác lần gọi model) — dùng cho E1 / E2:

| Tập | Chỉ số | Chênh TB | CI 95% | T / H / T | Câu đổi điểm |
|---|---|---|---|---|---|
| 176 câu | Completeness | +0,023 | [−0,006; +0,057] | 4 / 171 / 1 | 5 |
| 176 câu | Accuracy | +0,006 | [−0,017; +0,028] | 3 / 171 / 2 | 5 |
| 176 câu | Relevance | −0,023 | [−0,057; +0,011] | 3 / 166 / 7 | 10 |
| dev chính (88: dev, bỏ unnatural, trong phạm vi) | Completeness | 0,000 | [−0,034; +0,034] | 1 / 86 / 1 | 2 |
| dev chính | Accuracy | 0,000 | [−0,034; +0,034] | 1 / 86 / 1 | 2 |
| dev chính | Relevance | −0,023 | [−0,068; +0,023] | 1 / 84 / 3 | 4 |

Chỉ số theo dõi (không thuộc tiêu chí B1.2, ghi làm nhiễu):
- **Lỗi citation (validator production): B1 12 câu, G2.1a 8 câu**; chỉ 2 câu chung ⇒ **giữa hai lượt cùng cấu hình, lỗi citation dao
  động mạnh** (10 câu chỉ lỗi ở một lượt). *Suy ra*: E2 (chỉ số quyết = số câu lỗi citation) cần mức "vượt nhiễu" tính từ cặp này,
  và có thể cần > 1 lượt mốc. Số case lỗi: `data/phase_8_2/b1/check.json`.
- Câu trả lời giống hệt chữ: 58 / 176; câu đổi từ chối ↔ trả lời: 0; từ chối 30 / 30.
- Độ trễ đầu–cuối mỗi câu (harness, concurrency 4): B1 p50 1,86 s / p95 4,01 s; G2.1a p50 1,73 s / p95 2,89 s (khác lần đo, mạng /
  provider; cùng đầu vào).

**Tiền thật (từ usage log):** lượt sinh 176 câu **0,0369194 USD** (291.269 token vào / 15.585 ra; pilot 0,0019197 — ước × 17,6 =
0,034, thực tế lệch +9%, dưới ngưỡng 50%). Live `/chat` 2 câu: API không ghi usage ⇒ *ước* ≈ 0,0004 USD. **Tổng ≈ 0,0373 USD** ≤ trần
B23 0,06. Judge: quota Claude, 0 USD.

Dữ liệu: `data/phase_8_2/b1/` — `b1_{dev,test}.jsonl` (+ phần, `.meta.json`), `check.json`, `analyze.json`, `judge/` (map sha
`74fcff0fe0fa`, 15 lô + 15 file điểm, 294 / 294 điểm, 0 lỗi schema), `retrieval_dense_bm25_rrf.jsonl`, `nfd_check_{before,after}.json`,
`live_chat.json`.

## 5. Lỗi và giới hạn

- Câu đưa model chưa NFC (giới hạn chấp nhận ở review plan).
- T5 dùng một câu tự viết; NFD là biến đổi máy (người dùng thật hiếm khi gửi NFD — chưa biết tỉ lệ).
- `test_api_chat.py` dùng `TestClient` không gọi OpenAI (A kiểm ở review plan); không chạy full suite.
- Báo cáo cho User (`bao_cao_he_thong/` 4 chỗ) là việc của A theo spec §5.
- Chatbot đang chạy trên máy User chưa khởi động lại với code mới (B chỉ chạy server kiểm ở port 8000 rồi dừng).

## 6. Bàn giao cho người kiểm

- Đọc trước: §4 bảng T1–T5; diff 5 file `backend/` + `backend/experiments/phase_8_2/b1.py`.
- Chạy lại rẻ nhất: T1 (free, tất định) và `b1.py check` (free, đọc file); `nfd-check` (free).
- B1.3 spec: "Đạt + review chéo + B0 không dừng ⇒ A commit" — B0 (User đọc cặp mù) chưa xong, nên commit / đưa vào chatbot chờ B0
  theo spec.
- File B sửa (chưa commit): `backend/config/settings.yaml`, `backend/core/settings_loader.py`, `backend/retrieval/full_corpus.py`,
  `backend/tests/test_phase6_settings.py`, `backend/tests/test_full_corpus_retrieval.py`, `backend/experiments/phase_8_2/__init__.py`,
  `backend/experiments/phase_8_2/b1.py`, report này, `phase_8_2_b1_plan.md`.
