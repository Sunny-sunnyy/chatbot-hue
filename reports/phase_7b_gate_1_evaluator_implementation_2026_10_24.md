# Implementation Report: Phase 7B Gate 1 — evaluator full-corpus

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Canonical guide / spec:

```text
docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md
guides/full_corpus_rag.md (contract evaluation, rubric 1–5)
```

## 1. Phạm vi

Việc B2 trong `session_prompt/CURRENT_HANDOFF.md` = spec 7B §5 Gate 1:

1. Review thiết kế trước khi code: 2 major + 4 minor gửi A; A đồng ý cả 6 mặc định
   (2026-10-24) và đã đưa vào spec (commit `dba4881`).
2. Module evaluator, prompt judge, test logic thuần.
3. Retrieval eval 176 case: hai lần `dense_bm25_rrf` và một lần `native_hybrid_rrf`.
4. Smoke 10 (sinh + judge luna), ghi token thật, dự báo tiền Gate 2.

Không chạy Run 1/Run 2; không sửa runtime, prompt sinh, Golden, Qdrant.

## 2. Thay đổi chính

| File | Vai trò |
|---|---|
| `backend/evaluation/full_corpus_eval.py` (mới) | Một module, CLI 6 lệnh: `retrieval`, `generate`, `judge-luna`, `retry`, `export-judge-input`, `summarize` |
| `backend/evaluation/full_corpus_judge_prompt.md` (mới) | Prompt judge cố định dùng chung cho Claude và luna: rubric đúng bảng trong guide, quy tắc cấm dùng kiến thức ngoài, định dạng đầu vào, JSON đầu ra |
| `backend/tests/test_full_corpus_eval.py` (mới) | 10 test logic thuần |

Luồng mỗi case trong `generate` (`answer_case`) đi theo đúng thứ tự `api/routes/chat.py`:
`retrieval_service.search` (top-10) → `FullCorpusContextBuilder.build` (top-5) → nếu không
có source thì trả `INSUFFICIENT_ANSWER`, không gọi model (giống API) → nếu có thì
`generator.generate_answer` → `select_cited_sources`. Component được dựng như `create_app`:
`build_full_corpus_retrieval_service`, `FullCorpusContextBuilder` với tham số từ
`full_corpus_generation`, `OpenAIFullCorpusGenerator.from_environment`, cùng `settings.yaml`.

Các quyết định đã chốt với A:

- **Lỗi citation** (API trả 500): vẫn giữ text và đưa đi chấm; dòng ghi `citation_error`;
  report có tỉ lệ lỗi citation (tổng và theo category), tức tỉ lệ User sẽ gặp lỗi 500.
  Lỗi citation không phải lỗi kỹ thuật và không làm run thành `incomplete`.
- **Từ chối**: `answer.strip() == INSUFFICIENT_ANSWER`, cùng điều kiện nhánh fallback
  của `llm/citations.py`.
- **Keyword**: hàm metric chép từ `evaluation/eval.py` (MRR, nDCG, Coverage, trung bình
  đều trên keyword), thêm chuẩn hóa NFC + casefold ở cả hai phía; so khớp trên
  `search_text` của top-10. Module không import `eval.py` (evaluator Foods sẽ bị dọn).
- **Judge luna**: dùng chung `OpenAIResponsesModel` và client của generator;
  `ModelSettings(max_tokens=1024, include_usage=True, store=False)`, không có tham số
  sampling (evaluator Foods cũ chết vì `temperature`, xem B1 §5.2); structured output
  `JudgeScores` (3 số nguyên có ràng buộc 1–5, feedback).
- **Lỗi kỹ thuật**: mỗi case bắt lỗi riêng, ghi nguyên `Type: message <- Cause: message`
  vào `error`; không retry tự động. `retry <kind> --file …` chỉ chạy lại các dòng có
  `error` và ghi đè đúng dòng đó.
- **Song song**: `asyncio.Semaphore(4)` cho cả sinh lẫn judge.

### 2.1 Schema file cho Gate 3 (judge Claude, C)

`case_index` = chỉ số dòng **0-based** trong `golden_full_corpus.jsonl`, dùng chung với
`data/evaluation/phase_7b/subsets.json`.

**Đầu vào chấm** (B tạo bằng `export-judge-input`), JSONL, mỗi dòng:

```json
{"case_index": 17, "question": "…", "reference_answer": "…", "answer": "…"}
```

File không có category, tên run hay điểm. Thứ tự dòng được xáo bằng `--seed`; mỗi lần
chấm lại dùng một seed khác. Lệnh mẫu:

```bash
uv run python -m evaluation.full_corpus_eval export-judge-input \
  --answers run1_answers.jsonl --seed <seed> --out <tên file chấm>.jsonl [--cases <case_index…>]
```

**Điểm** (C ghi; luna ghi cùng schema, kèm thêm `input_tokens`, `output_tokens`, `error`),
JSONL, mỗi nguồn chấm một file:

```json
{"case_index": 17, "accuracy": 4, "completeness": 3, "relevance": 5, "feedback": "…"}
```

Ràng buộc: ba điểm là số nguyên 1–5, mỗi `case_index` xuất hiện một lần.
`validate_score_rows` kiểm các ràng buộc này và `summarize --answers … --scores …` báo lỗi
trong `score_errors`. Judge Claude nhận nguyên nội dung `full_corpus_judge_prompt.md` cùng
đầu vào từng case theo đúng định dạng ghi trong prompt (giống `build_judge_message`).

## 3. Cách đã chạy thật

Mọi lệnh chạy từ `backend/`, với `HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m …`:

```bash
python -m pytest tests/test_full_corpus_eval.py -q -p no:cacheprovider
python -m evaluation.full_corpus_eval retrieval --treatment dense_bm25_rrf    --out retrieval_dense_bm25_rrf_1.jsonl
python -m evaluation.full_corpus_eval retrieval --treatment dense_bm25_rrf    --out retrieval_dense_bm25_rrf_2.jsonl
python -m evaluation.full_corpus_eval retrieval --treatment native_hybrid_rrf --out retrieval_native_hybrid_rrf_1.jsonl
python -m evaluation.full_corpus_eval generate --golden smoke --out smoke_answers_1.jsonl            # paid
python -m evaluation.full_corpus_eval judge-luna --answers smoke_answers_1.jsonl --out smoke_judge_luna_1.jsonl  # paid
python -m evaluation.full_corpus_eval export-judge-input --answers smoke_answers_1.jsonl --seed 1 --out /tmp/…
python -m evaluation.full_corpus_eval summarize --retrieval … --answers … --scores …
python -m evaluation.full_corpus_eval retry generate   --file smoke_answers_1.jsonl            # (không env) → "no error rows"
python -m evaluation.full_corpus_eval retry judge-luna --file smoke_judge_luna_1.jsonl --answers smoke_answers_1.jsonl
```

Dữ liệu và dependency thật: Golden 176 + smoke 10 (private); Qdrant
`hue_full_corpus_7a2_e5_small_384` (chỉ đọc); e5-small local; OpenAI `gpt-6-luna`.
Kết quả private nằm ở `data/evaluation/phase_7b/`.

## 4. Kết quả quan sát

### 4.1 Test logic thuần

`10 passed`. Phạm vi: keyword MRR/nDCG/Coverage (rank, top-K, casefold, NFD→NFC), định
nghĩa từ chối, tỉ lệ từ chối và lỗi citation, macro-average theo category, tính tiền,
`validate_score_rows`, `merge_retried`, file đầu vào chấm (ẩn category, xáo theo seed),
và test hồi quy cho bug `select_cases` (mục 5.1).

### 4.2 Retrieval eval — 158 case (176 trừ 18 `out_of_scope`), K=10

Hai lần `dense_bm25_rrf` cho file **giống hệt từng byte** (`cmp`; SHA-256 cùng
`cefb2d1a…`) → **tất định: PASS**.

| Treatment | n | MRR@10 | nDCG@10 | Keyword Coverage@10 |
|---|---:|---:|---:|---:|
| `dense_bm25_rrf` (runtime) | 158 | 0,7212 | 0,7546 | 92,35 |
| `native_hybrid_rrf` | 158 | 0,7263 | 0,7613 | 93,41 |

Theo category (`dense_bm25_rrf` / `native_hybrid_rrf`):

| Category | n | MRR | nDCG | Coverage |
|---|---:|---|---|---|
| direct_fact | 75 | 0,818 / 0,819 | 0,846 / 0,849 | 98,0 / 98,7 |
| conditional | 29 | 0,816 / 0,816 | 0,816 / 0,816 | 94,8 / 94,8 |
| multi_source | 29 | 0,543 / 0,563 | 0,604 / 0,636 | 84,2 / 89,4 |
| comparative | 25 | 0,527 / 0,533 | 0,583 / 0,580 | 82,0 / 80,7 |

`native_hybrid_rrf` nhỉnh hơn một chút, rõ nhất ở `multi_source`. Đây là **quan sát** trên
một lần chạy với keyword proxy. 7B chưa có ngưỡng nhiễu, nên chưa kết luận được là tốt hơn
thật; để Phase 8 xem.

### 4.3 Smoke 10 (paid)

| Mục | Kết quả |
|---|---|
| Lỗi kỹ thuật | 0/10 (run `complete`) |
| Lỗi citation | 0/10 |
| Từ chối | đúng 1/1 `out_of_scope`; từ chối nhầm 2/9 case trong phạm vi (1 `comparative`, 1 `multi_source`) |
| Judge luna | 10/10 hợp lệ, `score_errors` rỗng; output lớn nhất 301 token (< 1024, không bị cắt), không lỗi parse |
| Điểm luna (n=10, chỉ để kiểm đường chạy, không phải baseline) | Accuracy 4,1 · Completeness 4,1 · Relevance 4,1 |
| Context | cả 10 case đóng gói đủ 5 source |

**Usage thật:**

| Lượt | Calls | Input tokens | Output tokens | USD |
|---|---:|---:|---:|---:|
| Sinh | 10 | 9.854 | 664 | 0,00132 |
| Judge luna | 10 | 9.253 | 1.152 | 0,00150 |
| **Tổng smoke** | 20 | 19.107 | 1.816 | **0,00282** (giới hạn 0,02) |

Trước đó B1 có 1 request OpenAI trả 400, ước tính ~0 USD (B1 §5.1). Tổng paid của B trong
session: **~0,0028 USD**.

### 4.4 Dự báo tiền Gate 2 (từ trung bình smoke)

Trung bình mỗi lượt: sinh ~985 input / ~66 output token; judge ~925 input / ~115 output.

| Việc Gate 2 | Lượt | USD dự báo |
|---|---:|---:|
| Run 1 + Run 2 (176 × 2) | 352 | 0,046 |
| Judge luna Run 1 (176) + chấm lại 30 | 206 | 0,031 |
| **Tổng** | 558 | **~0,077** |

Nếu nhân hệ số an toàn ×2 (smoke chỉ 10 case, có thể thiên lệch) thì còn ~0,155 USD, vẫn
dưới ngưỡng cắt giảm 0,5 USD và giới hạn cứng 0,6 USD. Không cần cắt giảm theo spec §6.
Ước lượng xấu nhất trong spec (~4k input/lượt sinh) cao hơn số thật khoảng 4 lần, vì chunk
ngắn (trung vị 85 token).

## 5. Lỗi và giới hạn

### 5.1 Bug tìm thấy và đã sửa trong lúc tự kiểm

Bản đầu của `select_cases` hiểu danh sách rỗng là "mọi case". Hệ quả: `retry` trên một
file không có dòng lỗi sẽ chạy lại **cả 176 case (paid)**. Bug lộ ra khi B chạy `retry`
**không có** `--env-file`; lệnh dừng ở `OPENAI_API_KEY is missing` trước mọi lượt gọi, nên
không tốn tiền. Đã sửa: `None` = mọi case, `[]` = không case nào; `retry` thoát sớm với
"no error rows". Có test hồi quy. Chạy lại thật cả hai kiểu `retry`: in "no error rows".

### 5.2 Giới hạn

- Điểm luna smoke chỉ để kiểm đường chạy (n=10), không phải baseline.
- Đường `retry` khi **có** dòng lỗi mới được kiểm ở mức logic (`merge_retried` có test).
  Chưa chạy thật vì smoke không có lỗi; B không tạo lỗi giả (Session_Prompt §8).
- Hai từ chối nhầm trong smoke là hành vi của runtime (quan sát), không thuộc phạm vi sửa ở 7B.
- Concurrency 4: retrieval service được gọi đồng thời qua `asyncio.to_thread`, giống API.
  Smoke 10 case chạy song song không có lỗi.
- Chưa có lệnh tính nhiễu và mức khớp giữa các nguồn (judge lần 1 với lần 2, Run 1 với
  Run 2, User/Claude/luna). Theo spec §5, phần đó làm ở Gate 4 khi đã có dữ liệu Gate 2–3,
  trên cùng schema điểm ở §2.1.

## 6. Bàn giao cho người kiểm

- Đọc trước: `answer_case` và `run_judge_luna` trong `backend/evaluation/full_corpus_eval.py`
  (so với `api/routes/chat.py` và `api/app.py`), sau đó đến prompt judge.
- Chạy lại nhanh, không tốn tiền: pytest file test mới; một lệnh `retrieval` rồi `cmp` với
  `retrieval_dense_bm25_rrf_1.jsonl`.
- Gate 2 cần A quyết: đồng ý dự báo ~0,08 USD và giao Run 1/Run 2 + judge luna. Tập con
  lấy từ `subsets.json`, không chọn lại.
- Không commit (B không có quyền).
