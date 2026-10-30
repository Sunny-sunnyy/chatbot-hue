# Review: C88 — harness Qwen3-Embedding-8B (B92) + plan "Sửa đổi 30/10"

Người kiểm: C (Claude Opus 5.5, `hue-rag-0e`) · Date: 11:30 30/10/2026 (`date`) · Việc: A giao C88 30/10. Người làm: B (`hue-rag-24`).
Đầu vào: nhánh `b92-qwen3-harness` tới **`400ccdc`** (`e70007b..400ccdc`: `8545650` + `400ccdc`); report `qwen3_8b_harness_implementation.md`; plan `qwen3_8b_plan.md`
bản A duyệt `52555da95828` §2–§4, §6, §8 + mục "Sửa đổi 30/10" (bản mới **`70ee5d44c260`**, sha C tính từ file). Skill `risk-gated-agent-review`. 0 USD; không gọi OpenRouter,
không tạo collection.

## 1. Phạm vi đã review

- Cổng tối thiểu: `git diff --name-status e70007b..400ccdc` = 5 file như report (2 mới, 3 sửa); không file ngoài phạm vi; `git diff --check` sạch. Commit `400ccdc` chỉ đổi 1 dòng
  (`build()` so provider bằng `OPENROUTER_EXPECTED_PROVIDER`).
- Đọc exact diff 3 file production / g1 + toàn bộ `qwen3_8b.py` + test; so với `OpenRouterDenseRunner` production (`embedding/full_corpus.py:281-372`) và
  `FullCorpusRetrievalService.search` (`retrieval/full_corpus.py:419-457`).
- Plan: `git diff` file plan so với `HEAD` (`git show HEAD:… | sha256sum` = `52555da95828`).

## 2. Findings

### M-1 (`qwen3_8b.py` `QUERY_RETRIES = 1` + `g1_retrieval.run_config`) — đường lỗi câu hỏi khác plan §4.2, không khai báo

- **Yêu cầu:** plan §4.2: "Câu hỏi 8B **không** thử lại: lỗi ⇒ dòng lỗi, chạy lại đúng câu đó một lần (đo đúng tỉ lệ lỗi mà runtime sẽ gặp)"; §3 theo dõi `dense_ms` p50 / p95 và
  chênh so với +50 ms; §8 dừng khi "lỗi gọi câu hỏi > 5 % một lượt".
- **Code:** runner câu hỏi tự thử lại 1 lần sau khi **ngủ 10 s** (hoặc Retry-After) bên trong `_embed`. Lần thử thứ hai lỗi ⇒ `RuntimeError` ⇒ `search` đổi thành
  `RetrievalDependencyError` (`full_corpus.py:430-433`) ⇒ `g1.run_config` **không** bắt theo câu ⇒ cả lượt dừng, `retrieve` chưa kịp ghi `<name>.jsonl` (ghi sau khi xong cả lượt).
  Report §1 tả "câu hỏi: 1 lần chạy lại (plan §4.2)" như là khớp plan; §2 không liệt kê.
- **Tác động:** (a) `dense_ms` đo từ `t_dense_start` tới sau truy vấn Qdrant (`full_corpus.py:429-457`) ⇒ câu được thử lại có `dense_ms` ≥ 10 s ⇒ p95 `dense_ms` và "p95 cả câu ước" (§3)
  lệch về phía xấu khi có lỗi — đúng chỉ số latency mà luật (i) dùng; (b) luật dừng "> 5 %" không bao giờ áp: một câu lỗi hai lần là mất cả lượt (vẫn còn log `queries_<name>.jsonl`,
  nhưng chạy lại cả lượt — tiền nhỏ, ≈ 0,0002 USD, nhưng 7A2 từng gặp 504 Nebius nên khả năng xảy ra không nhỏ). Không có bằng chứng sai bị ghi thành PASS (lỗi to tiếng) ⇒ major, không blocker.
- **Đóng khi (một trong hai, A chọn):**
  1. **C khuyên — ghi lệch, ít code:** report §2 + plan "Sửa đổi 30/10" ghi rõ: câu hỏi tự thử lại 1 lần trong runner; câu lỗi hai lần ⇒ dừng lượt, chạy lại cả lượt (tên mới);
     latency `dense_ms` p50 / p95 tính **chỉ trên câu một lần gọi** (đối chiếu `queries_<name>.jsonl`: mỗi câu có đúng một dòng `status` 200 và không dòng lỗi), kèm số câu bị loại;
     tỉ lệ lỗi gọi = dòng ≠ 200 / tổng dòng log. Một hàm nhỏ trong `retrieve` / `aa` in số này để không đếm tay.
  2. Theo đúng plan: `QUERY_RETRIES = 0` + bắt lỗi theo câu (dòng lỗi) + lệnh chạy lại các câu lỗi một lần — phải sửa vòng lặp `g1.run_config` (code dùng chung của g1) ⇒ thêm rủi ro
     ở chỗ T1 / g1 đang khóa; C không khuyên.

### m-1 (`qwen3_8b.py:143-148`) — response 200 không phải JSON làm mất dòng log của lần gọi đó

- `body = response.json()` chạy **trước** `_log`; body 200 hỏng ⇒ `JSONDecodeError` thoát, lần gọi không có trong `attempts.jsonl` / `queries_*.jsonl` (tỉ lệ lỗi đếm thiếu 1). Đổi thứ
  tự (log `status` / `ms` trước, parse sau) hoặc ghi chú. Không chặn.

### Ngoài phạm vi (ghi để biết)

- `retry_wait` với 429 + `Retry-After` rất lớn sẽ ngủ đúng chừng đó (không có trần). Plan không đặt trần; người chạy thấy log và dừng tay được.

## 3. Cách người kiểm chạy lại thật

- Worktree riêng `/tmp/c88_wt` (detached ở `400ccdc`): `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_qwen3_8b_harness.py -q`
  ⇒ **3 passed** (7,3 s). Test chỉ logic thuần (lịch thử lại, cache batch), không giả lập HTTP, không gọi mạng ✓.
- Plan: `git diff -U0 -- qwen3_8b_plan.md` ⇒ một hunk `@@ -208,0 +209,18 @@`, **0 dòng xóa** ⇒ chỉ thêm ở cuối; `HEAD` = `52555da95828`; file hiện tại `70ee5d44c260`.

## 4. Kết quả quan sát (đối chiếu yêu cầu A giao)

| Kiểm | Kết quả |
|---|---|
| Mặc định giữ hành vi (`build_candidate`, `build_full_corpus_retrieval_service`) | ✓ đọc code: `dense_runner=None` ⇒ đúng `create_dense_runner(spec)` như cũ; runner truyền vào sai spec ⇒ raise (cả hai chỗ). g1 `run_config` mặc định: `--candidate e5-small-384`, `collection` / `record` None, `sparse_state_path` = `SPARSE_STATE_PATH` = mặc định của factory (`full_corpus.py:646`, cùng hằng import từ `ingestion.full_corpus_pipeline`) ⇒ cùng lời gọi như trước. Không caller nào khác của `g1.run_config` (`git grep` + `data/**/*.py`) ⇒ thêm `args.candidate` không làm hỏng script cũ. T1 giống byte: **dùng lại bằng chứng B** (report §3; code đường mặc định C đọc không đổi); C **không** chạy lại T1 (B sắp ở bước 2–6 đợt 2 — W31), chạy lại sau rebase lên kho đợt 2 như report §5 |
| Thử lại 429 / 5xx ≤ 3 + Retry-After (batch đoạn) | ✓ `retry_wait`: chỉ 429, ≥ 500, timeout (`httpx.TimeoutException`); lịch 10 / 30 / 90 s; 429 + `Retry-After` số giây ⇒ max; dạng ngày giờ ⇒ theo lịch. `DOCUMENT_RETRIES = 3` ⇒ tối đa 4 lần gọi (1 + 3 lần thử lại, đúng "tối đa 3 lần, chờ 10 / 30 / 90"); hết ⇒ `RuntimeError`, cache các batch trước giữ. 4xx khác, lỗi kết nối không phải timeout ⇒ raise ngay (đúng plan "chỉ với") |
| Cache batch | ✓ `.npy` ghi trước, `.json` meta sau (thiếu meta = chưa xong ⇒ gọi lại, ghi đè `.npy` dở); khóa = sha chuỗi đã `prepare_document` + số dòng ⇒ kho đổi ⇒ dừng; batch từ cache vẫn thêm provider vào `providers_seen`. Pilot ghi batch 0, 1 vào cache, build dùng lại (cùng cách đánh số) — đúng ý plan "không trả tiền hai lần" |
| Pin Nebius + `data_collection: deny` | ✓ `_post` gửi đúng `OPENROUTER_PROVIDER_ROUTING` (`{"order": ["nebius"], "allow_fallbacks": False, "data_collection": "deny"}`), cùng model, `encoding_format`, batch 64 (`spec.batch_size`), timeout 180 s (client của lớp cha). Provider ≠ `"Nebius"` ⇒ `parse_embeddings_response` raise (không thử lại), lần gọi đã nằm trong log |
| So chuỗi provider | ✓ từ `400ccdc` `build()` so `[OPENROUTER_EXPECTED_PROVIDER]` (= `"Nebius"`, `full_corpus.py:282`); không còn chuỗi gõ tay |
| `providers_seen` vào build record | ✓ lớp con của `OpenRouterDenseRunner` ⇒ nhánh `isinstance` của `build_candidate` vẫn chạy |
| Không gọi API thật trong test | ✓ (§3) |
| Độ đơn giản | Đạt: logic riêng chỉ ở `experiments/`; production thêm đúng một tham số mặc định None ở hai factory (mẫu §4.1); không retry / fallback trong runtime |
| Plan "Sửa đổi 30/10" `70ee5d44c260` | ✓ chỉ thêm; ghi "không sửa các mục trên; không đổi tiêu chí §7"; nội dung khớp quyết định A: mốc e5 chạy lại trên kho sau đợt 2 (hai lần, giống từng dòng trừ `dense_ms`) **thay** điều kiện "lệch bảng §5"; cỡ mẫu tính lại trước pilot (n, trần thắng, thiếu ở pool dense, câu có thể tụt; n ≠ 40 ⇒ tính lại ngưỡng CI bằng `bootstrap_mean_diff`; không thể ra "tốt hơn" ⇒ dừng báo A); cùng file nhãn cho hai bên; lệch §4.2 (A duyệt) + hằng provider ghi lại |

## 5. Giới hạn hoặc phần chưa chạy

- **NOT RUN (C):** T1 158 câu, 4 file pytest còn lại (B: 70 passed), `preflight` — dùng lại bằng chứng B vì B chuẩn bị bước 2–6 đợt 2 (W31); T1 phải chạy lại sau rebase lên kho đợt 2.
- Mọi đường mạng (thử lại thật, log từ response thật, cache từ response thật, `pilot`, `build`, `retrieve`, `aa`) chỉ đọc code; `pilot` là lần chạy thật đầu tiên.

## 6. Decision và bước tiếp theo

- **Code B92 (`400ccdc`): `changes_requested` — 0 blocker / 1 major / 1 minor.** M-1 đóng bằng cách 1 (ghi lệch + latency chỉ trên câu một lần gọi) là đủ; C kiểm lại phần sửa.
- **Plan "Sửa đổi 30/10" `70ee5d44c260`: `ready_for_user_confirmation`** — A duyệt sha được; nếu M-1 đóng bằng cách 1 thì thêm một dòng vào mục này (sha mới, C kiểm lại dòng đó).

## 7. Vòng 2 (C, 11:35 30/10/2026 `date`) — phần sửa M-1, m-1

Đầu vào (sha từ file): commit `fb0b82c` (`400ccdc..fb0b82c`: 2 file +56 / −5, `git diff --check` sạch); plan `9f3d616e2a59` (A duyệt trước `70ee5d44c260`); report
`34b346a665f5`.

- **M-1 — đóng** (cách 1 A chọn + 2 điểm A thêm). `query_latency` / lệnh `latency --name` (cũng in trong `retrieve`): p50 / p95 `dense_ms` **mọi câu** và **chỉ câu gọi một lần**, số
  câu thử lại + tỉ lệ, cờ `stop_retried_over_5pct`, số dòng log ≠ 200. Ghép log ↔ câu: `split_calls` gom theo `attempt` 0 (lần thử lại nối vào lần gọi của nó); lần gọi đầu là warm-up
  của factory; mỗi dòng g1 đúng một `search` ⇒ đúng một lần gọi (treatment mặc định `dense_bm25_rrf` không nhúng thêm); số lần gọi ≠ số dòng + 1 ⇒ `ValueError`. Kiểm logic nhỏ (thư mục
  tạm, đã xóa): log 4 lần gọi / 3 dòng (1 câu thử lại) ⇒ `retried` 1, chỉ-một-lần n 2; bỏ dòng warm-up ⇒ **raise** "3 calls in log != 3 rows + 1 warm-up" — không ghép lệch lặng lẽ.
  Plan "Sửa đổi 30/10" mục 6: chỉ thêm (0 dòng xóa so với `HEAD` `52555da95828`); thay đúng §4.2 đường lỗi câu hỏi + luật dừng §8 thành "câu phải thử lại > 5 % ⇒ dừng, báo A". Report
  §2 mục 5 ghi lệch.
- **m-1 — đóng.** `_embed` ghi log trước khi parse; 200 không phải JSON ⇒ dòng log có `error` rồi `RuntimeError` (không thử lại — đúng "chỉ 429 / 5xx / timeout").
- Test: worktree riêng `/tmp/c88b_wt` ở `fb0b82c` (đã gỡ) ⇒ `tests/test_qwen3_8b_harness.py` **4 passed**.

**Kết luận vòng 2:** code B92 `fb0b82c` **`ready_for_user_confirmation`** 0 / 0 / 0; plan `9f3d616e2a59` ready. Còn lại trước lượt có phí: T1 chạy lại sau rebase lên kho đợt 2
(§5), mốc e5 + cỡ mẫu theo "Sửa đổi 30/10" mục 1–2.

## 8. Vòng 3 — phần chuẩn bị chạy (C, 14:52 30/10/2026 `date`): `ready_for_user_confirmation` 0 / 0 / 0

Đầu vào (sha C tính từ file): plan `qwen3_8b_plan.md` **`d6d6c7d51584`** (bản A duyệt `9f3d616e2a59` = `git show HEAD`); nhánh `b92-qwen3-harness` đỉnh `01bf0c2` trên `main` `bfb0b41`.

- **Plan:** `diff` với `HEAD` = đúng 2 chỗ "11:3x" ⇒ "11:26 30/10/2026" (khớp dòng A ghi trong `CURRENT_HANDOFF.md` "(A, 11:26 30/10/2026) B92 xong") + thêm "Sửa đổi 30/10" mục 7 (5 dòng);
  không đổi mục nào khác, không đổi §7 ✓.
- **Rebase:** `git range-diff e70007b..fb0b82c bfb0b41..b92-qwen3-harness`: 3 / 3 commit "=" (patch giống hệt); diff của diff chỉ khác dòng `index` ⇒ nhánh mang đúng code đã review vòng 2 ✓.
  `GOLD_PATH` trên nhánh = **gold v5** (từ `main` `bfb0b41`) ✓.
- **T1 trên nhánh** (worktree riêng `/tmp/c96_wt`, symlink kho / data, đã gỡ): **`4d5bbe9e0edc`** = T1 `main` sau đợt 2 (C kiểm ở B93 bước 6) ⇒ đường mặc định không đổi ✓.
- **Mốc e5** (`data/phase_8_1/g1/c78_e5_{dev,test}{,_rerun}.jsonl`): dev 108 / test 50 dòng; hai lần **giống từng dòng** trừ `dense_ms` và `config` (tên lượt) ⇒ tất định ✓. C đếm lại từ file:
  dev 40 câu có nhãn — context đủ **24**, top-10 **24**, pool dense **33**, thiếu ở context **16**, thiếu ngay ở pool dense **7**; dev số chính 32 — 19 / 19 / 26 / 13 / 6; test 15 — 9 / 9 / 11 / 6 / 4;
  test số chính 10 — 7 / 7 / 8 / 3 / 2 — **khớp mục 7** ✓.
- **Cỡ mẫu:** `bootstrap_mean_diff` (10.000 vòng, seed `20261024`) trên 40 cặp nhị phân, C tìm số thắng nhỏ nhất cho cận dưới CI > 0: **4 / 0, 7 / 1, 9 / 2, 11 / 3** (với số thắng ít hơn 1,
  cận dưới = 0 ⇒ `verdict` "no_difference") — **khớp** ✓. Trần thắng 16 ≥ 4 ⇒ có thể ra "tốt hơn"; sàn: 24 câu có thể tụt ✓.

**Kết luận vòng 3:** plan `d6d6c7d51584` + nhánh `01bf0c2` sẵn cho pilot có phí (A duyệt sha). Nhắc từ plan: pilot ước > 1,5 × ⇒ dừng; câu phải thử lại > 5 % ⇒ dừng.
