# Implementation Report: Phase 8.2 B3 — mốc cuối trên câu kín (B80)

Người chạy: B (Claude Opus 5.5, terminal `hue-rag-ac`) · Date: 10:14 28/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` mục B80 (A giao 28/10; **User 09:59 28/10: "Chạy B3
ngay"** — mở 36 câu kín cho người chạy B).
Plan: `phase_8_2_b3_plan.md` (A duyệt sha `27e75be5ed44`). Người kiểm: C (C74, giữ mù).
**Giữ mù:** report này chỉ có số dòng (1–36), số đếm theo loại câu, đúng / sai, md5, token, USD, ms. Không có nội dung câu hỏi / đáp án / câu trả lời / feedback, không tên
file nguồn. B (người chạy) chỉ chạy script in số; không đọc file câu trả lời, lô chấm hay feedback.

## Tóm tắt cho User (lời thường)

- **Thử gì:** so chatbot **đầu 8.2** (5 đoạn ngữ cảnh, bộ kiểm trích dẫn cũ) với chatbot **cuối 8.2** (đang chạy: 10 đoạn + chuẩn hóa chữ câu hỏi + bộ kiểm trích dẫn mới) trên
  36 câu kín chưa ai dùng để chọn — phép kiểm cuối của Phase 8.2.
- **Kết quả:** chatbot cuối **không làm hỏng gì** và **tốt hơn rõ**: điểm đủ ý +0,82 / 5 (khoảng tin cậy +0,39 … +1,33), điểm đúng +0,70, **0 câu bị chấm thấp hơn**;
  câu ngoài kho vẫn từ chối đúng 3 / 3; câu trong kho bị từ chối nhầm 4 → 2; câu báo lỗi trích dẫn (người dùng thấy lỗi) 4 → 0.
- **Giới hạn:** người chấm là Claude (chưa có mốc người); chỉ báo được tập 36 câu (khớp được 1 / 3 câu A đã thấy, nên không dựng được tập 33 câu "chưa ai đọc");
  không câu kín nào gõ dạng NFD ⇒ phần chuẩn hóa chữ không được thử ở đây. Tiền: **≈ 0,0138 USD** (~345 đồng).

## 1. Phạm vi

Theo plan §5: worktree hai nhánh ⇒ T1 ⇒ preflight ⇒ pilot ⇒ rest ⇒ merge ⇒ check ⇒ judge ⇒ analyze ⇒ report. Không đổi chatbot, không ghi Qdrant, không sửa câu kín.

| Nhánh | Commit | Hành vi (preflight) |
|---|---|---|
| đầu | `f26485b` (worktree `/tmp/b3_start`) | `max_context_documents` 5; chưa NFC; validator v1 (chỉ nhận `[n]`) |
| cuối | `249d270` = `main` lúc chạy (worktree `/tmp/b3_end`); `backend/` giống `510e1a8` (`git diff --stat 510e1a8 249d270 -- backend/` rỗng) | 10; NFC; validator v2 |

## 2. Thay đổi chính

- Harness private `data/phase_8_2/b3/tools/b3.py` (sha `6615b7310e15`), đúng plan §3: `match-seen`, `preflight`, `run` (đồng thời 4, `as_completed`, ghi từng dòng + flush,
  `wall_ms`, từ chối ghi đè, meta ghi lúc đầu và trong `finally`), `merge` (kèm `--retry`), `check`, `export-judge`, `check-judge`, `analyze`. Phần chấm / thống kê chép logic
  `experiments/phase_8_2/b1.py`, không import. Không file tracked nào đổi ngoài report này.
- **C65 — câu 500 kiểu "validator v1 không nhận `[Nguồn n]`":** `check` phát lại luật v1 (chép từ `f26485b` `llm/citations.py`) và v2 (`main` `normalize_citations` +
  `select_cited_sources`) trên câu trả lời đã lưu. Bên đầu: câu có `citation_error` (v1) mà v2 qua. Bên cuối: câu có `[Nguồn n]`, v1 sẽ 500, v2 qua.

## 3. Cách đã chạy thật

```bash
# match-seen (repo chính, free)
cd backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/phase_8_2/b3/tools/b3.py match-seen
git worktree add --detach /tmp/b3_start f26485b; git worktree add --detach /tmp/b3_end 249d270   # + symlink data/, knowledge-base-hue/
# mỗi worktree, từ <wt>/backend:
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m evaluation.full_corpus_eval retrieval --out .../data/phase_8_2/b3/t1_<arm>.jsonl
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python .../b3.py preflight --arm <arm>
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python .../b3.py run --arm <arm> --cases pilot|rest --name <arm>_pilot|<arm>_rest
# repo chính, free:
b3.py merge --arm <arm> --parts <arm>_pilot <arm>_rest;  b3.py check;  b3.py export-judge --batch-size 12
# 3 sub-agent judge mới (model kế thừa session: global.anthropic.claude-opus-5-5, cùng judge B1 / G2), mỗi agent 2 lô; chỉ Read judge prompt + lô, Write scores_NN.jsonl
b3.py check-judge;  b3.py analyze
```

Qdrant `:6335` thật (chỉ đọc), e5-small CPU, `gpt-6-luna` thật. Thứ tự: B3 chạy trước bộ "trước" B78 và trước lượt C73 — không chồng lượt trả phí.

## 4. Kết quả quan sát

**Kiểm trước khi chạy (free):**

| Kiểm | Kết quả | Đạt |
|---|---|---|
| md5 câu kín / số dòng | `ddc59587b502` / 36 (cả hai preflight) | ✓ |
| T1 158 câu ở cả hai worktree | sha `cefb2d1ad609` cả hai, 158 dòng — giống byte mốc | ✓ |
| Code nạp từ đúng worktree | `module_files_outside_worktree` rỗng cả hai (`evaluation.full_corpus_eval`, `retrieval.full_corpus`) | ✓ |
| HEAD | đầu `f26485b`, cuối `249d270` | ✓ |
| Qdrant | 1 collection, 8.459 point | ✓ |
| Câu NFC ≠ nguyên văn / câu > 500 ký tự | 0 / 0 ⇒ **phần NFC không được câu kín thử** | (watch) |
| Câu nhãn ≠ natural (`sealed_realism.jsonl`, khớp theo `line`) | 0; 0 câu không khớp ⇒ không có tập "bỏ câu không tự nhiên" | — |
| **match-seen** (3 câu A đã thấy) | khớp **1** dòng (NFC + gộp khoảng trắng, câu hỏi là chuỗi con của ghi chú User) ⇒ **không đủ 3 ⇒ chỉ S36** (plan §2, không đoán) | — |

**Sinh (có phí):** pilot 10 dòng (`random.Random(20261024).sample(range(1, 37), 10)` = 2, 5, 12, 13, 17, 20, 24, 25, 28, 33) mỗi nhánh = 0,0035524 USD ⇒ ước 36 × 2 ≈ 0,0128
(≤ 1,5 × 0,012 ⇒ chạy tiếp); rest 26 dòng mỗi nhánh. **0 dòng lỗi**, không chạy lại câu nào.

**`check` (do script in, `data/phase_8_2/b3/check.json`):**

| Chỉ số | đầu | cuối |
|---|---:|---:|
| Lỗi kỹ thuật (`error`) | 0 | **0** |
| OOS bị trả lời (3 câu OOS) | 0 | **0** |
| Từ chối trong phạm vi (33 câu) | 4 | **2** |
| Câu 500 vì citation (validator của chính nhánh) | 4 | **0** |
| — trong đó / tương ứng **C65** "v1 không nhận `[Nguồn n]`" | **4 / 4** (cả 4 câu 500 bên đầu đều chỉ vì v1; v2 qua) | **5** (câu có `[Nguồn n]`: v1 sẽ 500, v2 qua) |
| Số nguồn ngữ cảnh TB | 5 | 10 |
| Token vào / ra (36 câu, 36 lần gọi) | 34.463 / 4.176 | 60.657 / 4.425 |
| Token ra TB / câu | 116,0 | 122,9 |
| USD (36 câu) · USD / câu | 0,0055343 · 0,0001537 | 0,0082782 · 0,0002299 |
| `wall_ms` p50 / p95 (đồng thời 4, không phải chờ của một người dùng) | 4.885,6 / 9.170,3 | 3.659,2 / 9.066,8 |

**Judge:** 63 item khác nhau / 72 câu trả lời (câu giống hệt chữ chấm một lần), 6 lô; `check-judge`: 63 / 63 điểm, 0 lỗi schema, 0 thiếu, 0 thừa.

**`analyze` — S36, trong phạm vi n = 33, chênh = cuối − đầu, câu 500 citation chấm Completeness = Accuracy = 1 (plan §4), bootstrap 10.000 vòng seed 20261024
(`data/phase_8_2/b3/analyze.json`):**

| Chỉ số | TB đầu | TB cuối | Chênh | CI 95 % | Thắng / hòa / thua |
|---|---:|---:|---:|---|---|
| Completeness | 3,606 | 4,424 | **+0,818** | [+0,394; +1,333] | 12 / 21 / **0** |
| Accuracy | 3,879 | 4,576 | **+0,697** | [+0,273; +1,212] | 8 / 25 / **0** |
| Relevance (watch) | 4,394 | 4,545 | +0,152 | [−0,121; +0,515] | 3 / 27 / 3 |

**Đối chiếu tiêu chí ghi trước (plan §4, trên S36 vì không dựng được S33):**

| Dòng | Ngưỡng | Kết quả | Đạt |
|---|---|---|---|
| sàn — OOS bị trả lời (nhánh cuối) | 0 | 0 / 3 | ✓ |
| sàn — lỗi kỹ thuật sau một lần chạy lại | 0 mỗi nhánh | 0 / 0 (không cần chạy lại) | ✓ |
| mức tụt — Completeness | TB ≥ −0,1 và số câu tụt ≤ A/A + 3 = 5 | +0,818; 0 câu tụt | ✓ |
| mức tụt — Accuracy | như trên | +0,697; 0 câu tụt | ✓ |
| mức tụt — từ chối nhầm trong phạm vi | +1 câu | 4 → 2 (−2) | ✓ |
| watch — "tốt hơn" Completeness | CI 95 % > 0 ⇒ ghi "tốt hơn trên câu kín" | CI [+0,394; +1,333] | **tốt hơn** |

⇒ **Kết luận theo plan: "không làm hỏng"**, kèm **"tốt hơn trên câu kín"** (watch CI > 0).

**Số phụ để đọc kết luận (watch, không thuộc tiêu chí; cùng điểm judge):**
- Theo điểm judge **thô** (không gán 1 cho câu 500): Completeness +0,364 [+0,091; +0,727], 8 / 24 / 1; Accuracy +0,242 [+0,030; +0,545], 4 / 29 / 0. Judge chấm chữ của 4 câu 500
  bên đầu là (4, 4), (5, 5), (5, 5), (5, 5) (Accuracy, Completeness) — tức nội dung đúng nhưng người dùng thấy lỗi.
- **Bỏ 4 câu 500** (29 câu trong phạm vi, không câu nào 500 ở cả hai nhánh): Completeness +0,448 [+0,138; +0,828], 8 / 21 / 0; Accuracy +0,276 [+0,034; +0,621], 4 / 25 / 0.
  ⇒ lợi **không** chỉ đến từ bộ kiểm trích dẫn mới; phần 10 đoạn ngữ cảnh vẫn tốt hơn với CI > 0.
- Câu thắng Completeness (12) theo loại: conditional 5, multi_source 3, direct_fact 2, comparative 2.

**Tiền thật (token từ usage, `cost_usd`):** đầu 0,0055343 + cuối 0,0082782 = **0,0138125 USD** (trần B3 0,03; ước plan 0,012). Judge: quota Claude (3 sub-agent ≈ 112 nghìn
token), 0 USD.

## 5. Lỗi và giới hạn

- **Chỉ S36:** `match-seen` khớp 1 / 3 câu A đã thấy ⇒ theo plan §2 không dựng S33, kết luận theo S36; S36 gồm 3 câu A đã thấy (do User trích ở 8.1). B không nới luật khớp
  (plan: "không đoán").
- **NFC không được thử:** 0 / 36 câu kín khác dạng NFC ⇒ "cuối − đầu" ở đây đo context 10 + validator v2 (NFC trung tính).
- **Judge Claude, chưa có mốc người** (B0 làm sau — spec 8.2 §11). Cùng judge prompt / rubric / model với B1 / G2 ⇒ không chạy "kiểm người chấm 4 phiếu" (plan §4).
- **Nhiễu A/A:** không chạy trên câu kín (plan §8 quyết định 3); dùng A/A B1 ↔ G2.1a + 7B Run 1 ↔ 2 cho mức tụt. Bộ câu khác ⇒ giới hạn.
- `wall_ms` đo khi gọi đồng thời 4 trong harness, không phải thời gian chờ của một người dùng qua API; p95 trên 36 giá trị ≈ giá trị lớn thứ nhì.
- Gộp ba thay đổi (context 10, NFC, validator v2): B3 là phép kiểm tổng, không tách phần của từng thay đổi (plan §1) — số phụ "bỏ 4 câu 500" chỉ gợi ý phần của context 10.

## 6. Bàn giao cho người kiểm

- **Dữ liệu** (private `data/phase_8_2/b3/`): `{start,end}_{pilot,rest}.jsonl` + `.meta.json`, `{start,end}.jsonl`, `check.json`, `judge/` (`map.json`, 6 lô, 6 file điểm),
  `analyze.json`, `t1_{start,end}.jsonl`, `preflight_{start,end}.json`, `a_seen_lines.json`; script `tools/b3.py` sha `6615b7310e15`.
- **C (C74) chạy lại, free, từ `backend/` của repo chính:** `PYTHONPATH=$PWD uv run python ../data/phase_8_2/b3/tools/b3.py check` / `check-judge` / `analyze` ⇒ số trùng §4
  (`check` và `analyze` ghi đè `check.json` / `analyze.json` cùng nội dung — chỉ đọc lại thì dùng `cat`); kiểm md5 câu kín, sha T1, commit + `max_context_documents` trong meta
  / preflight; đọc `b3.py` tìm chỗ in nội dung (lệnh nào cũng chỉ in số).
- Worktree `/tmp/b3_start`, `/tmp/b3_end` đã gỡ (symlink xóa trước). Không còn file tạm của B3 ở `/tmp`.
- Report này không chứa nội dung câu kín; hook `overlap_scan.py` quét câu kín khi commit.
