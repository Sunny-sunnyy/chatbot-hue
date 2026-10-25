# Phase 8.2 B1 — plan: context 10 + NFC vào chatbot (B23)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-de`) · 2026-10-25 16:25 +0700 (`date`) · Việc: B23 (A giao 16:2x) ·
Spec: `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` (User duyệt 16:21, sha `dabae90b2b60`, commit
`5e6936b`) · Trạng thái: **chờ A review + duyệt sha** — chưa sửa code, chưa gọi API.

## Căn cứ để review

1. File này — toàn bộ.
2. Spec 8.2 — §3.2 (NFC một chỗ), §4 (phạm vi), §5 B1 (tiêu chí B1.2), §7 (tiền, pilot).
3. `backend/retrieval/full_corpus.py:462-470` (`FullCorpusRetrievalService.search` — chỗ đặt NFC đề xuất) và
   `backend/api/routes/chat.py:47-75` (đường API gọi `search`).
4. `backend/evaluation/full_corpus_eval.py:327-375` (`answer_case`, `run_generation` — đường evaluator; cũng gọi `search`).

## 1. Chỗ đặt NFC và lý do

**Đề xuất:** đầu `FullCorpusRetrievalService.search` (`backend/retrieval/full_corpus.py:462`), ngay sau kiểm câu rỗng:
`query = unicodedata.normalize("NFC", query)`. Mọi bước sau trong `search` (embed dense, tách từ BM25, Qdrant) dùng câu đã NFC.

- **Một chỗ mọi đường đi qua** (spec §3.2): API (`chat.py` gọi `state.retrieval_service.search`), evaluator (`answer_case` và
  `run_retrieval_eval`) và harness 8.1 / 8.2 đều gọi đúng hàm này.
- **Đúng chỗ có hại đã đo:** 8.1 G1.4 đo thiệt hại NFD ở tầng **tìm kiếm** (MRR −0,204; NFD → NFC giống hệt). Chưa có số đo nào
  về bước sinh với câu NFD.
- **Không đổi câu đã NFC** ⇒ Golden (đã NFC khi nạp, `golden_full_corpus.py:33`) cho retrieval giống byte (tiêu chí B1.2 dòng 1).
- **Giới hạn (ghi rõ):** `context_builder.build(query, …)` và `generator.generate_answer(query, …)` vẫn nhận chuỗi gốc. Với
  câu NFD: tìm kiếm giống bản NFC, nhưng câu hỏi đưa model là NFD (đếm token khác ⇒ câu trả lời có thể khác chữ). Đây không phải
  hồi quy (hôm nay model cũng nhận NFD).
- **Phương án khác (A chọn nếu muốn):** NFC ở đầu `chat.py` (sau `strip`) **và** ở `answer_case` — chuẩn hóa cả câu đưa model,
  nhưng là **hai** chỗ, trái chữ "một chỗ" của §3.2. B đề xuất cách trên vì đơn giản hơn và khớp bằng chứng.

## 2. File sửa

| File | Sửa |
|---|---|
| `backend/config/settings.yaml:56` | `max_context_documents: 5` → `10` |
| `backend/core/settings_loader.py:77-78` | kiểm cứng `!= 5` → `!= 10` |
| `backend/tests/test_phase6_settings.py:25` | giá trị ghim `5` → `10` |
| `backend/retrieval/full_corpus.py` | `import unicodedata`; một dòng NFC đầu `search` (mục 1) |
| `backend/tests/test_full_corpus_retrieval.py` | một test nhỏ: câu NFD đi qua bước chuẩn hóa của `search` thành đúng chuỗi NFC (xem dưới) |
| `backend/experiments/phase_8_2/b1.py` (mới) | harness đo B1 (mục 3) — không đổi runtime |

Test nhỏ (spec B1.1 "câu NFD → NFC giống hệt"): để không dựng stub cho cả service, tách chuẩn hóa thành hàm thuần
`normalize_query(query) -> str` trong `full_corpus.py` (kiểm rỗng như cũ + NFC) mà `search` gọi; test hàm này với một chuỗi
NFD tự viết (không lấy từ Golden). Bằng chứng thật cho NFC là kiểm T4 / T5 dưới (Qdrant + e5 thật).

## 3. Harness `backend/experiments/phase_8_2/b1.py`

Gọi code production, **không tham số ghi đè**: `full_corpus_eval.run_generation(cases)` (settings mới ⇒ context 10, prompt mặc định,
reasoning mặc định — đúng như G2.1a nhưng không qua `--max-context-documents`). Lệnh con:

- `run --cases {pilot,rest,test_pilot,test_rest} --name …` (paid): chọn câu bằng `g2_generate.select` (cùng seed 20261024 ⇒ cùng 10
  câu pilot dev / test như G2.1a); ghi `data/phase_8_2/b1/<name>.jsonl` + `.meta.json` (usage, USD theo `g2_generate.usage`).
- `merge` (free): gộp pilot + rest ⇒ `b1_dev.jsonl` (120), `b1_test.jsonl` (56).
- `check` (free): so từng câu với G2.1a (`data/phase_8_1/g2/g2_context10.jsonl` + `t_context10.jsonl`): `top_chunk_ids`,
  `context_sources`, `input_tokens` bằng nhau; đếm câu OOS bị trả lời (`refusal` false ở `category == out_of_scope`); đếm `error`.
- `export` (free): gộp câu trả lời B1 (176) + G2.1a (176) thành lô chấm **mù** (số item mờ, xáo theo seed 20261024; câu trả lời giống
  hệt từng ký tự trong cùng câu chỉ chấm một lần — như `g2_generate.pooled_items`), ghi `data/phase_8_2/b1/judge/batch_*.jsonl` + `map.json`.
- `analyze` (free): ghép điểm; chênh Completeness theo cặp B1 − G2.1a bằng `full_corpus_eval.bootstrap_mean_diff` (10.000 vòng, seed
  20261024) + `verdict`; thắng / hòa / thua; số câu đổi điểm (nhiễu A/A).
- `nfd-check --question …` (free): dựng retrieval + context builder production; so `search(NFD)` với `search(NFC)` (10 id đầu, thứ tự)
  và nguồn đóng gói (`context_builder.build` trên NFC) — Qdrant + e5 thật.

Lặp lại vài hàm nhỏ của `g2_generate` (đọc / ghi theo đường dẫn) vì `g2_generate` ghim `OUT_DIR` vào `data/phase_8_1/g2/`; không
sửa harness 8.1.

**Judge:** Claude sub-agent (quota, 0 USD), cùng prompt judge của `full_corpus_eval` như G2; mỗi sub-agent một lô ~25 item, ghi
`scores_<lô>.jsonl`; brief đọc lại trước khi gửi; ghi model id. Kiểm đủ điểm bằng `check` trước `analyze`.

## 4. Tiêu chí B1.2 (chép đúng spec §5 B1.2) và cách đo

| # | Tiêu chí (spec) | Đo bằng | Đạt khi |
|---|---|---|---|
| T1 | retrieval 158 câu trong phạm vi giống byte mốc `cefb2d1a…` | `full_corpus_eval retrieval` ra `data/phase_8_2/b1/retrieval_dense_bm25_rrf.jsonl`; `sha256sum`, `wc -l` | sha256 = `cefb2d1ad609…`, 158 dòng |
| T2 | lượt sinh 176 câu: `top_chunk_ids`, `context_sources`, `input_tokens` bằng G2.1a 176 / 176 | `b1.py check` | 176 / 176 cả ba trường |
| T3 | judge Claude, G2.1a chấm lại cùng lượt mù: 0 câu OOS bị trả lời, lỗi kỹ thuật 0, Completeness không khác (CI chứa 0) | `b1.py check` (OOS, lỗi), `b1.py analyze` (176 câu theo cặp) | 0 / 18 OOS trả lời; 0 lỗi; CI 95% chứa 0. Ghi số câu đổi điểm = **nhiễu A/A context 10** cho E1 / E2 |
| T4 | API live `/chat`: một câu hỏi thật trả tới 10 nguồn đã đóng gói, có citation | uvicorn port 8000 (lệnh ở `LUONG_HOAT_DONG_HE_THONG.md`), `curl POST /api/chat` câu B tự viết (không lấy Golden / câu kín) | HTTP 200, câu trả lời có `[n]`, `sources` ≤ 10 và ⊆ nguồn đóng gói; *tới 10 nguồn đã đóng gói* đo ở T5 (API chỉ trả nguồn được trích) |
| T5 | một câu NFD trả cùng nguồn với bản NFC của nó | `b1.py nfd-check` (tất định) + `curl` bản NFD | tất định: 10 id `search` và nguồn đóng gói giống hệt NFC (số nguồn đóng gói ghi ra — "tới 10"); live: HTTP 200, có citation. `sources` của API phụ thuộc câu trả lời model ⇒ ghi so sánh, **không** dùng làm đạt / không đạt (B hiểu "nguồn" = nguồn đóng gói; A sửa nếu ý khác) |

Thêm (đối chứng, free): chạy `nfd-check` **trước khi sửa code** (HEAD `5e6936b`) ⇒ kỳ vọng NFD ≠ NFC — cho thấy T5 đo được thay đổi.
Lệch bất kỳ T1–T5 ⇒ **dừng**, tìm nguyên nhân, báo A; không sửa tiêu chí.

## 5. Thứ tự và lệnh (chạy từ `backend/`)

```bash
# 0. đối chứng trước sửa (free)
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.b1 nfd-check --question "<câu B tự viết>"
# 1. sửa code (mục 2); test nhỏ
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_retrieval.py tests/test_full_corpus_context.py tests/test_api_chat.py -q
# 2. T1 (free)
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m evaluation.full_corpus_eval retrieval --out /home/minhhieu/hue_rag/data/phase_8_2/b1/retrieval_dense_bm25_rrf.jsonl
# 3. pilot (paid ~0,004 USD) ⇒ ước lại; rồi rest, test_pilot, test_rest
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.b1 run --cases pilot --name b1_pilot
# 4. merge, check (T2, phần T3) ; export ⇒ sub-agent judge ⇒ analyze (T3)
# 5. T4 / T5 live: uvicorn chạy nền, curl câu NFC + NFD, dừng server
```

Test được chọn: file chạm settings / retrieval / context / API, không có paid call (`Project_Status.md` §8 — không dùng
`--deselect`; `test_api_chat.py` B kiểm trước khi chạy là không gọi API thật, nếu có thì bỏ khỏi danh sách).

## 6. Tiền và giới hạn

- Ước từ G2.1a (cùng cấu hình): dev 0,0245 + test 0,0116 ≈ **0,036 USD**; live 2 câu ≈ 0,0005. Tổng ≈ 0,037 ≤ trần B23 **0,06**.
- Pilot 10 câu trước; ước lại = pilot × 17,6; vượt ước pilot > 50% ⇒ dừng báo A.
- Judge: quota Claude, 0 USD. Qdrant chỉ đọc (không tạo collection). Không commit. Không mở câu kín, không chép câu Golden vào report.
- Server uvicorn: chạy nền, dừng bằng TaskStop khi xong; bị chặn ⇒ nhờ User `!`.

## 7. Đầu ra

`phase_8_2_b1_implementation.md` (khuôn implementation): T1–T5 với số thật, lệnh, USD từ log, nhiễu A/A context 10; trạng thái
"chờ review"; nhắn A. Dữ liệu `data/phase_8_2/b1/`.
