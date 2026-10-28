# Plan: đo "trước ↔ sau" đợt sửa kho (B78)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-ac`) · Date: 09:48 28/10/2026 (`date`) · **Bản 2** (bản 1 `7b79c3971bc7`, 09:34)
Việc: `session_prompt/CURRENT_HANDOFF.md` mục B78 (A giao 28/10). Chỉ viết plan, **chưa chạy**, 0 USD. B không đụng kho / Qdrant / Golden / câu kín.
Spec: `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (User duyệt sha `937cf8969810`). Plan này chi tiết hóa spec §5 bước 0 + bước 9 và §6.
Bản 2 đóng m-1 … m-6 của review C72 (`sua_kho_do_truoc_sau_plan_review.md`, bản 1: ready 0 / 0 / 6) và ghi quyết định A cho 3 câu §8 (CURRENT_HANDOFF mục B78) —
danh sách sửa ở §9. Trạng thái: chờ C kiểm phần sửa ⇒ A duyệt sha ⇒ chạy bộ "trước" khi A giao.

## Căn cứ để review

1. File này — toàn bộ.
2. Spec sửa kho: §2, §5 bước 0, 2, 6–9 + "Dừng + khôi phục", §6, §7 (tiền). Spec 8.2 `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`: §10.2 (luật
   "không làm hỏng", mức tụt luật (i)) và §11 (B0 không chặn B1; đo lại p95 ở bộ "trước").
3. `skills/run-experiment/SKILL.md` §1 (tiêu chí ghi trước, cỡ mẫu, hai dòng không đếm cùng lỗi), §2 (kiểm người chấm), §3 mục 1, 6, 8, §4.
4. Code trên `main` `510e1a8` (đường đo + hành vi production mà sàn trỏ tới):
   - `backend/evaluation/full_corpus_eval.py:162-164` (`is_refusal`), `:322-364` (`answer_case`: thứ tự như `chat.py`, `except Exception` ⇒ `error`), `:367-386` (`run_generation`);
   - `backend/api/routes/chat.py:128-135` (500 `context_budget_error`), `:140-144` (từ chối khi không có nguồn), `:177-189` (500 `citation_integrity_error`);
     `backend/api/app.py:161-165` (500 chung); `backend/retrieval/full_corpus_context.py:60-61` (bỏ đoạn không có evidence — m-3);
   - `backend/evaluation/full_corpus_judge_prompt.md:13-15` (chi tiết thêm không bị trừ Accuracy), `:29` (Accuracy 3 = "ít nhất một sai lệch thực chất").

Số đếm trong plan tính lại được (chỉ đọc, chỉ in số) bằng `data/sua_kho_2026-10-27/tools/b78_{counts,cit,touched}.py` (sha `010037f7d9dd`, `feb413b57979`,
`7c3ade66174d`; chạy từ `backend/`: `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/sua_kho_2026-10-27/tools/b78_<x>.py`).

## 1. Câu hỏi thí nghiệm và hai bên so

**Lớp bài toán:** sửa nội dung kho (thông tin mâu thuẫn / cũ) + loại file danh mục khỏi index có làm chatbot **tệ đi** ở chỗ nào không; ở câu chạm phần đã sửa
thì có tốt lên không. Đây là phép kiểm **"không làm hỏng"** (spec §6), không phải phép chọn biến thể.

| Bên | Chatbot | Kho / index | Khi nào chạy |
|---|---|---|---|
| **trước** | `main` sau merge B1 (`510e1a8` hoặc commit lúc chạy, ghi trong meta): context 10 + NFC, `gpt-6-luna`, reasoning mặc định, citation v2 | 205 file, 8.459 đoạn, T1 `cefb2d1ad609` | spec bước 0, **trước bước 1** |
| **sau** | cùng code; chỉ đổi `exclude_files` (bước 3) | kho đã sửa (bước 2), 204 file, ≈ 8.426 đoạn, T1 mới (bước 6) | sau bước 6 |

- **Đổi gộp một lần** (đúng spec): 40 mục B73 + 14 edit tên đơn vị + mục từ 16 câu User (nếu có trả lời) + loại file danh mục. Plan không tách phần của từng
  mục; phần "câu chạm" (§3) chỉ cho biết câu nào có thể đổi vì sửa kho.
- **Chatbot "trước":** spec bước 0 ghi "chatbot cuối 8.2 (sau merge B1)". Từ 28/10 B0 không chặn B1 (spec 8.2 §11), và A đã merge `p82-b1` (`510e1a8`). B3 (câu kín)
  không đổi chatbot. **A quyết 28/10 (lệch thứ tự spec sửa kho §2, A duyệt — m-4):** bộ "trước" chạy **trước B3 / trước khi đóng 8.2**; tính vào trần đợt 0,15 USD;
  **không chạy cùng lúc với B3 hay lượt trả phí nào khác** (W5 `wall_ms` tuần tự sẽ lệch nếu máy / mạng đang bận); kiểm **"còn hiệu lực"** ngay trước bước 1:
  1. `git diff <commit trước> HEAD -- backend/ ':(exclude)backend/tests' ':(exclude)backend/experiments'` rỗng (code / cấu hình runtime không đổi);
  2. T1 chạy lại giống byte T1 của bộ "trước";
  3. Qdrant 1 collection, 8.459 point; build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` cùng sha với lúc chạy bộ "trước".
  Một điều kiện trượt ⇒ chạy lại bộ "trước" trên HEAD (≈ +0,037 USD, vẫn trong trần §6) trước khi đụng kho.
- Đường sinh: harness gọi `answer_case` (`full_corpus_eval.py:322-364`) — cùng thứ tự `chat.py` (tìm → đóng gói → sinh → kiểm citation). Khác API ở một chỗ không
  ảnh hưởng điểm: `answer_case` lưu chữ model **trước** `normalize_citations` (`chat.py:177`), còn validator dùng cùng mẫu bắt cả `[Nguồn n]`; judge bỏ qua dấu
  trích dẫn (`full_corpus_judge_prompt.md:16`).

## 2. Harness (private `data/sua_kho_2026-10-27/tools/truoc_sau.py`, 0 USD trừ lệnh `run`)

Chạy từ `backend/`, Qdrant chỉ đọc. Gọi code production, không tham số ghi đè. Phần chấm / thống kê chép logic `experiments/phase_8_2/b1.py`
(`pooled_items`, `scored_rows`, `paired`), không import file thí nghiệm cũ. Kết quả ở `data/sua_kho_2026-10-27/{eval_truoc,eval_sau,judge}/`.

- **`preflight --arm truoc|sau`** (free) ⇒ `preflight_<arm>.json`: `git rev-parse HEAD`; `max_context_documents` (= 10); collection + `points_count`; sha build record;
  số file discovery; md5 Golden; **md5 từng câu** (`question`, `reference_answer`, `keywords` tách riêng, theo `case_index`); **số đoạn trong collection không có
  `evidence_parts`** (scroll payload) — phải = 0 ở **cả hai** bên, khác 0 ⇒ dừng (m-3: builder bỏ đoạn không có evidence, `retrieval/full_corpus_context.py:60-61`, nên
  `top_chunk_ids[:context_sources]` chỉ đúng là context khi số này = 0; review C72 đếm bên hiện tại 0 / 8.459) — chỉ in số đếm.
  Bên `sau`: md5 `question` của **mọi** câu phải trùng bên `trước` (bước 8 chỉ sửa `reference_answer` / `keywords`); khác ⇒ dừng (cặp không còn cùng câu hỏi).
- **`run --arm --cases pilot|rest|lines:<n,…> --name`** (có phí):
  - dựng service / context / generator **như `run_generation`** (`full_corpus_eval.py:367-372`, cùng `settings.yaml`);
  - mỗi câu gọi `answer_case`; **đồng thời 1** (tuần tự) — để `wall_ms` gần thời gian một người dùng chờ, so được với mốc API tuần tự B65 (p50 3,3 s / p95 5,7 s,
    context 5). Không đổi chất lượng; chỉ chậm hơn (176 câu ≈ 8–12 phút);
  - **ghi từng dòng ngay** (append + flush) kèm `wall_ms` (`perf_counter` quanh `answer_case`), `usd` (`cost_usd`);
  - **từ chối ghi đè** (`raise SystemExit('exists')`); `<name>.meta.json` ghi lúc bắt đầu và lúc kết thúc, kể cả khi lỗi (commit, md5 Golden, n, tổng token, USD, giờ);
  - `answer_case` bắt mọi lỗi của câu vào `error`; generator ném lỗi ⇒ không có usage ⇒ `input_tokens: null`, tiền ước bằng token TB của bên đó (cận trên = câu tốn
    nhất) — skill §3.8. **Không tự retry, không fallback**; chạy lại là lệnh riêng `run --cases lines:<n>` (file mới), `merge` lấy lượt chạy lại thay dòng lỗi, giữ cả hai.
- **`merge`**, **`check`** (free): mỗi bên đủ 176 dòng, `case_index` không trùng; in các số của sàn F1, F3, F4 (§4) + từ chối, token, USD / câu, `wall_ms` p50 / p95.
- **`applied`** (free, sau bước 2): đọc danh sách edit **đã áp thật** `data/sua_kho_2026-10-27/applied_edits.jsonl` (người áp ghi ở bước 2, theo thứ tự: `file`, `old`,
  `new`, nguồn mục) — một nguồn duy nhất cho §3.
- **`touched`** (free, sau bước 6 và bước 8): dựng tập câu chạm theo §3 ⇒ `touched.json` (chỉ `case_index` + lý do a / b / c / d).
- **`export-judge`**, **`check-judge`**, **`analyze`** (free) — như `b1.py`: câu trả lời giống hệt chữ trong cùng câu chấm **một lần**; `item` là số mờ, xáo seed
  `20261024`; `map.json` item → [(bên, `case_index`)]; lô ≈ 20 item (`g2_generate.write_batches`); `validate_score_rows`; `bootstrap_mean_diff` 10.000 vòng, seed
  `20261024`, chênh = sau − trước. `export-judge` ghi md5 Golden lúc xuất; phải bằng md5 Golden sau bước 8 (User đã duyệt).
- **`rejudge`** (free): xuất lô chấm lại mù cho câu ứng viên sàn F2 — item của **cả hai** bên (§4).
- **`rerun-f4 --lines <n,…>`** (có phí, chỉ khi F4 vỡ — §4): sinh lại đúng câu đó **một lần** ở bên `sau` ⇒ file riêng `eval_sau/f4_rerun.jsonl` (append, từ chối ghi đè), giữ
  nguyên dòng gốc; ghi nhãn context giống / khác lần đầu (so `top_chunk_ids[:context_sources]`). Chỉ là bằng chứng, **không** thay dòng gốc, không đổi kết quả F4.

Pilot: 10 câu `random.Random(20261024).sample(range(1, 177), 10)` ở bên `trước` ⇒ ước lại tiền; `rest` = 166 câu còn lại. Bên `sau` chạy đủ 176 một lượt
(đã biết tiền từ bên `trước`). Số pilot không báo riêng.

## 3. Tập câu

Từ `golden_full_corpus.jsonl` (176) + `data/phase_8_1/golden_realism_final.jsonl` (`0b65d1c138d2`) — đếm bằng `b78_counts.py`:

| Tập | Định nghĩa | n |
|---|---|---:|
| OOS | `category == out_of_scope` | 18 |
| trong phạm vi | còn lại | 158 |
| **số chính** (spec §6) | trong phạm vi, bỏ nhãn `unnatural` (natural 82 + capability_only 65 trên 176) | **129** |
| **chạm** | số chính ∩ (a ∪ b ∪ c ∪ d) dưới | ước ≈ 29 + phần c, a |
| **không chạm** | số chính − chạm | ước ≈ 95–100 |

Câu **chạm** — dựng bằng máy sau bước 6 + 8, không đọc nội dung (luật ghi trước, C68 M-2 (3)):
- **(a)** Golden của câu đổi ở bước 8 (md5 `reference_answer` hoặc `keywords` khác `preflight_truoc`).
- **(b)** context bên `trước` (`top_chunk_ids[:context_sources]`) có đoạn mà một `evidence_part` giao khoảng ký tự của `old` (vị trí trong file backup ở `meta/`) của
  một edit trong `applied_edits.jsonl`. `old` không tìm thấy trong file backup (edit dựng trên kết quả edit trước) ⇒ coi mọi đoạn của file đó là chạm (thừa hơn thiếu).
- **(c)** context bên `sau` có đoạn mà `evidence_part` giao **mọi** chỗ xuất hiện của `new` trong file đã sửa. Edit **xóa** (`new` rỗng — `str.find("")` khớp vị trí 0,
  vô nghĩa) ⇒ edit đó **chỉ dùng (b)** (m-3). Review C72: 123 edit hiện có 0 `new` rỗng, 0 `new` < 12 ký tự, 0 `new` đã có > 1 lần trong file gốc; edit từ 16 câu User áp
  cùng luật.
- **(d)** context bên `trước` có đoạn của file danh mục bị loại.

Ước trước (B78, trên context lượt B1 25/10 — cùng cấu hình bên `trước`, kho chưa sửa; 123 edit = 109 của 40 mục + 14 edit tên đơn vị, 65 file; 0 edit không tìm thấy
`old`): 114 đoạn chạm + 33 đoạn file danh mục ⇒ **(b) ∪ (d) = 29 / 129** câu số chính (file-level thô sẽ là 79 / 129 — vì thế dùng mức đoạn). (a), (c) và edit từ 16 câu
User chưa biết ⇒ tập chạm thật lớn hơn; số thật do `touched` in.

## 4. Tiêu chí ghi trước

**A/A (nhiễu)** — dùng lại, không chạy mới (spec §6): lượt B1 ↔ G2.1a (context 10 ↔ context 10, cùng đầu vào từng token; `phase_8_2_b1_implementation.md` §4).
B tính lại bằng `b78_counts.py` trên đúng các tập ở §3 (điểm judge sẵn có, validator citation hiện tại `b78_cit.py`):

| Tập | Completeness thắng / hòa / tụt | Accuracy thắng / hòa / tụt | Từ chối đổi | OOS bị trả lời | Lỗi citation (validator hiện tại) | "Nói chắc sai" |
|---|---|---|---|---|---|---|
| số chính 129 | 4 / 124 / 1 | 3 / 124 / 2 | 0 | — | — | 0 / 0 |
| trong phạm vi 158 | 4 / 153 / 1 | 3 / 153 / 2 | 0 | — | — | 0 / 0 |
| 176 | 4 / 171 / 1 | 3 / 171 / 2 | 0 | 0 / 0 | 0 / 0 (C65: 12 lỗi v1 của B1 đều hết với v2) | — |

⇒ **A/A = 2** (số lớn của hai chỉ số, đúng spec §6) ⇒ mức tụt "≤ A/A + 3" = **5 câu**.

```yaml
experiment_id: sua_kho_truoc_sau
baseline: "main sau merge B1 (510e1a8 hoặc HEAD lúc chạy) + kho/index hiện tại (205 file, 8.459 đoạn, T1 cefb2d1ad609)"
changed_variable: "nội dung kho (đợt 1 đã áp) + exclude_files thêm file danh mục; build lại index tại chỗ"
unchanged: [chunker, embedding e5-small, retrieval dense_bm25_rrf, context 10, prompt, model gpt-6-luna, reasoning mặc định, validator citation, judge Claude]
data: {golden: knowledge-base-hue/evaluation/golden_full_corpus.jsonl, n: 176, main: 129, judge_golden: "bản sau bước 8 (User duyệt) cho CẢ HAI bên"}
metrics:
  - {id: F1, name: OOS bị trả lời, fn: "refusal == false và citation_error == null trên category out_of_scope (bên sau) — người dùng thấy câu trả lời; OOS có citation_error thuộc F4", role: floor, floor: "0 / 18", src: "full_corpus_eval.py:162-164 = điều kiện fallback; chat.py:140-144, :177-189"}
  - {id: F2, name: nói chắc sai mới, fn: "§4 dòng F2", role: floor, floor: "0 câu (trên 158 trong phạm vi)", noise: "A/A 0 / 0", src: "chat.py:177-189 (câu tới người dùng), judge_prompt.md:29"}
  - {id: F3, name: lỗi kỹ thuật / 500 khác citation, fn: "error != null", role: floor, floor: "0 mỗi bên sau một lần chạy lại (trừ context_budget_error: không chạy lại)", src: "full_corpus_eval.py:362; chat.py:128-135; app.py:161-165"}
  - {id: F4, name: 500 citation mới, fn: "citation_error != null ở sau và == null ở trước, cùng case_index", role: floor, floor: "0", noise: "A/A 0 / 0 (validator hiện tại)", src: "chat.py:177-189"}
  - {id: T1, name: Completeness số chính, fn: "analyze.paired (sau − trước); câu 500 citation chấm 1", role: tolerance, max_worse: "số câu tụt ≤ 5 trên 129; TB ≥ −0,1 trên 129 VÀ trên tập không chạm"}
  - {id: T2, name: Accuracy số chính, fn: như T1, role: tolerance, max_worse: như T1}
  - {id: T3, name: từ chối nhầm trong phạm vi, fn: "refusal == true, category != out_of_scope (158)", role: tolerance, max_worse: "sau ≤ trước + 1", noise: "A/A 0 câu đổi"}
  - {id: W1, name: câu chạm — Completeness / Accuracy, fn: "analyze.paired trên tập chạm", role: watch, note: "báo riêng (spec bước 9); kỳ vọng ≥ 0"}
  - {id: W2, name: Accuracy = 4 có trả lời (sai lệch nhỏ), fn: "đếm mỗi bên, 158", role: watch, noise: "A/A 6 / 7"}
  - {id: W3, name: Relevance, role: watch}
  - {id: W4, name: USD / câu, output_tokens / câu, input_tokens / câu, fn: cost_usd, role: watch}
  - {id: W5, name: wall_ms p50 / p95 (tuần tự), role: watch, note: "so mốc p95 5,7 s (B65, context 5) — spec 8.2 §11"}
  - {id: W6, name: tầng tìm, fn: "số câu đổi top-10 (T1 cũ ↔ mới); đoạn đúng trong context: gold v3 (trước) ↔ gold v4 (sau, chỉ sau bước 7)", role: watch}
  - {id: W7, name: Completeness — "tốt hơn", fn: "CI 95 % trên 129", role: watch}
  - {id: W8, name: Accuracy 5 ⇒ 4 mới, fn: "cùng case_index, trong phạm vi (158), cả hai bên có câu trả lời người dùng thấy; trước 5, sau 4", role: watch, note: "C đọc từng câu, ghi 'sai fact (số / giờ / giá / tên…)' hoặc 'khác cách diễn đạt'; câu sai fact báo A trong report — không phải sàn (m-1)"}
result: {paired_delta: null, ci95: null, wins_ties_losses: null}
conclusion: null   # không làm hỏng / làm hỏng / chưa đủ
```

**F2 — "nói chắc sai"** (thứ tự lỗi User đồng ý 28/10: nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm):
- Một câu **nói chắc sai** = câu trong phạm vi mà người dùng **thấy câu trả lời** (`error == null`, `refusal == false`, `citation_error == null` — API trả 200 chỉ khi qua
  kiểm citation, `chat.py:177-189`) **và** judge cho **Accuracy ≤ 3** (rubric: 3 = "có ít nhất một sai lệch thực chất", 2 = "phần lớn sai", 1 = "sai hoàn toàn" —
  `full_corpus_judge_prompt.md:29-31`). Không phân biệt câu có rào ("có thể", "chưa chắc") hay không: mọi câu trả lời không từ chối đều tính là "nói" (luật đếm,
  không cần đọc chữ).
- **Ứng viên mới** = nói chắc sai ở `sau` mà không ở `trước`, cùng `case_index` (theo điểm lượt chấm chính).
- Ứng viên ⇒ `rejudge`: một sub-agent judge **mới** chấm lại mù item `sau` **và** item `trước` của câu đó (cùng prompt, xáo thứ tự). **Tính là mới** khi theo điểm `rejudge`
  của **cả hai** item: bên `sau` vẫn nói chắc sai **và** bên `trước` không (m-1). Lý do: nhiễu judge-only (2 / 88 câu đổi điểm, `Project_Status.md` §8) — bỏ phần nhiễu
  chấm, không bỏ phần nhiễu sinh (người dùng cũng gặp).
- **Golden sót** (ghi trước, m-1): câu tính là mới thuộc **tập chạm**, và C (người kiểm, không phải người chạy) đọc thấy câu trả lời `sau` **khớp kho đã sửa** còn Golden (bước 8)
  chưa sửa theo ⇒ **không tính vào F2**; ghi riêng, chuyển thành mục Golden đợt 2, A trình User. Câu không thuộc tập chạm ⇒ không áp luật này.
- A/A: B1 0 câu, G2.1a 0 câu (trên 158; Accuracy của câu có trả lời chỉ có 4 hoặc 5) ⇒ sàn 0 khớp nhiễu.
- **Giữa các sàn không chồng** (m-2): F1 chỉ OOS người dùng thấy câu trả lời; F2 chỉ trong phạm vi, loại `citation_error`; mọi câu `citation_error` mới (OOS hay trong phạm vi)
  thuộc F4; lỗi kỹ thuật (`error`) thuộc F3 — mỗi câu vỡ sàn thuộc đúng một dòng F.
- **Sàn ↔ mức tụt có chồng** (m-2, sửa câu bản 1): một câu F2 mới cũng là câu tụt Accuracy ở T2; một câu F4 mới (chấm 1) cũng là câu tụt ở T1 / T2. Ghi trước: **T1 / T2 luôn
  tính trên đủ tập, kể cả câu đã vỡ sàn; không tính lại** khi A / User xét sau. Vì sàn vỡ đã là "làm hỏng" (dừng + khôi phục), phần chồng không đổi kết luận.
- **Giới hạn:** judge **không** trừ Accuracy cho chi tiết thêm mà đáp án tham chiếu không xác nhận cũng không phủ nhận (`full_corpus_judge_prompt.md:13-15`) ⇒ F2 bắt
  "nói ngược đáp án", **không bắt "bịa thêm"**. Đo bịa cần thước bám nguồn riêng (câu trả lời ↔ context) — chưa có, ngoài plan này (§8 câu 2).

**Luật chấm câu 500 citation** (như plan B3): người dùng không thấy câu trả lời ⇒ ở cả hai bên câu có `citation_error` được gán Completeness = Accuracy = 1 trong T1 / T2
(judge vẫn chấm chữ, chỉ báo). Câu 500 ở cả hai bên chấm 1 ở cả hai ⇒ chênh 0; câu 500 **mới** thuộc F4 và cũng tụt ở T1 / T2 (xem "Sàn ↔ mức tụt có chồng").

**"500 mới" của spec §6** — B hiểu: F3 (500 khác citation: `context_budget_error` `chat.py:128-135`, 500 chung `app.py:161-165`; trong harness cả hai thành `error`)
+ F4 (500 citation mới). Nhiễu F4 ở cấu hình production context 10: **0 / 352** lần gọi (A/A B1 ↔ G2.1a, `b78_cit.py`). Con số 14 / 1.600 câu của rà code 1a gộp **cả các biến
thể** 8.1 (prompt, reasoning khác — review C72 m-5) ⇒ không phải nhiễu của cấu hình này. F4 vẫn có thể vỡ vì nhiễu sinh, nhưng không chắc.
**F4 vỡ (A quyết 28/10, m-5):** trước khi khôi phục, `rerun-f4` sinh lại đúng câu đó **một lần** ở bên `sau` (index mới còn) — chỉ làm bằng chứng (≈ 0,0002 USD / câu); rồi
dừng + khôi phục theo spec §5; sau khôi phục A trình User kèm bằng chứng để quyết áp lại hay không. Bên `trước` không sinh lại được (index cũ đã xóa) — không cần.

**Mức tụt và giải thích (spec §6 "mỗi câu tụt có giải thích"):**
- T1 / T2: **số câu tụt đếm trên 129 (gồm câu chạm)**; TB kiểm trên 129 **và** trên tập không chạm (câu chạm có thể tốt lên vì `trước` bị chấm theo Golden đã sửa — C68
  M-2 — làm TB 129 đẹp giả; TB tập không chạm chặn chuyện đó).
- Mỗi câu tụt (T1 / T2) `analyze` gắn nhãn bằng máy: **fact đã sửa** (câu thuộc tập chạm) · **tìm đổi đoạn** (tập (nguồn, `evidence_parts`) của context hai bên khác nhau) ·
  **nhiễu** (context hai bên giống nhau). C đọc câu trả lời hai bên của câu nhãn "nhiễu" và câu nhãn "tìm đổi đoạn" không chạm, xác nhận không có lỗi kho mới (ví dụ edit
  làm mất ý); câu có lỗi kho mới ⇒ ghi finding, A trình User.
- Không đổi tiêu chí sau khi thấy số.

**Kết luận:**
- **không làm hỏng** = qua F1–F4 và T1–T3.
- **làm hỏng** = vỡ một dòng ⇒ dừng, báo A kèm `case_index` + loại câu (report tracked chỉ ghi loại câu); **khôi phục theo spec §5 "Dừng + khôi phục"** (giữ spec — A quyết
  28/10); F4 vỡ thì `rerun-f4` trước khi khôi phục (trên); sau khôi phục A trình User. Sàn F1 / F3 / F4 biết ngay sau `check` bên `sau` (trước judge); F2 và T1–T3 biết sau
  `analyze` (sau bước 8).
- **chưa đủ** = lỗi kỹ thuật còn sau một lần chạy lại; hoặc thiếu điểm judge.
- Chỉ số "tốt hơn" (W1, W7) không quyết.

**Cỡ mẫu** (*suy ra*, ghi trước):
- Trên 129 câu, một câu ±1 điểm = ±0,0078 TB ⇒ "TB ≥ −0,1" trên 129 chỉ trượt khi thua ròng ≳ 13 điểm, nên dòng "≤ 5 câu tụt" thường chặn trước. Trên tập không chạm (≈ 95–100)
  một câu ±1 ≈ ±0,01 TB.
- Lượt B1: Accuracy 117 / 129 câu số chính đã 5 điểm, Completeness tương tự gần trần ⇒ W1 / W7 nhiều khả năng **"không khác" / "chưa rõ"** — kết quả hợp lệ (phép kiểm
  là "không làm hỏng"). Câu chạm ≈ 30+ câu: "tốt hơn" chỉ thấy nếu ≥ ~4 câu thắng ròng.

**Judge:** sub-agent Claude mới, ghi model id (session hiện tại `global.anthropic.claude-opus-5-5`, cùng judge B1 / G2); hai bên chấm **cùng lượt mù**, **cùng Golden sau
bước 8**; cùng prompt / rubric / model ⇒ không cần "kiểm người chấm 4 phiếu" (skill §2); đổi model judge ⇒ chạy 4 phiếu trước. Mỗi sub-agent chỉ `Read`
`full_corpus_judge_prompt.md` + lô của mình, `Write` file điểm; tin trả lời cuối chỉ gồm đường dẫn + số item.

## 5. Cách chạy

1. **Bộ "trước"** (spec bước 0; khi A giao — được trước B3 / trước đóng 8.2; trước bước 1; **không chạy cùng lúc B3 / lượt trả phí khác**):
   - `cd backend && HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --out ../data/sua_kho_2026-10-27/eval_truoc/t1_truoc.jsonl` (không gọi API trả phí
     ⇒ không nạp `.env` — m-6; chỉ lệnh `run` / `rerun-f4` dùng `--env-file ../.env`)
     ⇒ sha phải = `cefb2d1ad609`; khác ⇒ dừng.
   - `preflight --arm truoc` ⇒ `run --arm truoc --cases pilot` ⇒ ước lại ⇒ `run --cases rest` ⇒ `merge` ⇒ `check` (F1, F3, F4 bên trước; lỗi kỹ thuật ⇒ chạy lại đúng câu đó
     một lần).
   - Ghi commit, sha T1, sha build record vào `eval_truoc/README.md`; nhắn A.
2. **Ngay trước bước 1:** kiểm "còn hiệu lực" (§1) ⇒ trượt thì chạy lại bộ "trước".
3. **Bước 2–6** theo spec (ngoài plan này); bước 2 ghi `applied_edits.jsonl`.
4. **Bộ "sau"** (sau bước 6, chatbot đã khởi động lại được): `preflight --arm sau` (md5 `question` khớp; collection ≈ 8.426 point; 0 đoạn thiếu evidence) ⇒ `run --arm sau
   --cases all` ⇒ `merge` ⇒ `check` ⇒ F1 / F3 / F4. F4 vỡ ⇒ `rerun-f4` ⇒ dừng + khôi phục (§4).
5. **Sau bước 8** (Golden User duyệt) **và bước 7** (gold v4, cho W6): `applied` ⇒ `touched` ⇒ `export-judge` ⇒ sub-agent judge (mỗi agent ≤ 2 lô) ⇒ `check-judge` ⇒
   `analyze` ⇒ F2 ứng viên ⇒ `rejudge` ⇒ `analyze` lần cuối. **Ghép khóa bên chỉ sau khi đủ điểm.**
6. **Report** `sua_kho_do_truoc_sau_implementation.md` (bảng do script in, không gõ tay; câu tả ở mức loại câu) + 3–5 dòng lời thường cho User; nhắn A + C.

## 6. Tiền, thời gian, dừng

- **Ước** từ token thật: lượt B1 176 câu context 10 = 291.269 vào / 15.585 ra ⇒ **0,0369 USD / bên** ⇒ hai bên ≈ **0,074 USD**; pilot ≈ 0,002. Bộ `sau` có thể rẻ hơn chút
  (file danh mục ra khỏi context 3 câu). Chạy lại bộ "trước" (§1) ⇒ ≈ +0,037. `rerun-f4` (chỉ khi F4 vỡ) ≈ 0,0002 USD / câu. Judge, rejudge: quota Claude, 0 USD.
- **Trần: 0,15 USD** (spec §7) — gồm cả chạy lại bộ "trước" (tối đa ≈ 0,111). Trong trần phiên 1 USD (User 28/10).
- **Dừng + báo A:** T1 / commit / md5 `question` lệch; ước sau pilot > 1,5 × 0,037; lỗi kỹ thuật còn sau một lần chạy lại; vượt trần; sàn vỡ (§4 "Kết luận").
- **Thời gian:** mỗi bên ≈ 8–12 phút (tuần tự); judge ≈ 2 × 176 câu ⇒ ~250–300 item khác nhau (lượt B1: 294 / 352), ~15 lô; tổng ≈ 1,5 giờ chia hai lúc.

## 7. Hợp đồng kiểm

- **Người chạy (B) nộp:** `data/sua_kho_2026-10-27/{eval_truoc,eval_sau}/` (phần + `.meta.json`, bộ gộp, `check_*.json`, `preflight_*.json`, `t1_*.jsonl`), `applied_edits.jsonl`,
  `touched.json`, `judge/` (`map.json`, lô, điểm, `rejudge/`), `analyze.json`; sha 12 của `truoc_sau.py`; report.
- **Người kiểm (C):** chạy lại `check`, `touched`, `check-judge`, `analyze` (free) ⇒ số trùng report; kiểm sha T1, commit, md5 Golden ở meta; đọc diff harness (gọi
  `answer_case`, append, từ chối ghi đè, không retry); đọc câu tụt nhãn "nhiễu" / "tìm đổi đoạn" không chạm, mọi câu F2 (gồm kiểm luật "Golden sót") và mọi câu W8
  (ghi "sai fact" / "khác cách diễn đạt") (§4); grep report tracked không có nội dung kho / Golden (hook `overlap_scan.py` khi commit).

## 8. Quyết định của A cho 3 câu hỏi bản 1 (`CURRENT_HANDOFF.md` mục B78, 28/10)

1. **F4 vỡ chỉ vì 500 citation:** **giữ spec §5** "sàn vỡ ⇒ dừng + khôi phục" (không đổi spec). Thêm: F4 vỡ ⇒ `rerun-f4` sinh lại đúng câu đó một lần ở bên `sau` (file
   riêng, giữ cả hai) làm bằng chứng; sau khôi phục A trình User để quyết áp lại hay không (§4). (Bản 1 đề xuất "A trình User **trước** khi khôi phục" — không dùng.)
2. **"Bịa thêm"** chưa có thước: đồng ý ghi giới hạn, không thêm thước mới giữa chừng; thêm dòng watch W8 "Accuracy 5 ⇒ 4 mới" (C đọc từng câu). Thước bám nguồn (câu trả lời ↔
   context) là việc riêng cho lần đo sau.
3. **Khi nào chạy bộ "trước":** được chạy **trước B3 / trước khi đóng 8.2** (A duyệt lệch thứ tự spec §2); không chạy cùng lúc B3 / lượt trả phí khác; kiểm "còn hiệu lực" (§1).

## 9. Sửa ở bản 2 (theo review C72, bản 1 `7b79c3971bc7`)

| Finding | Sửa ở |
|---|---|
| m-1 Accuracy 4 mới không được đọc; "mới" sau rejudge; Golden sót | §4 YAML W8; §4 F2 ("Tính là mới" theo điểm `rejudge` của cả hai item; luật "Golden sót"); §7 C đọc W8 |
| m-2 câu "không chồng" chưa đúng; F1 ↔ F4 | §4 YAML F1 (loại `citation_error`); §4 "Giữa các sàn không chồng" + "Sàn ↔ mức tụt có chồng" (T1 / T2 tính đủ, không tính lại) |
| m-3 `new` rỗng; index "sau" có đoạn thiếu evidence | §3 (c); §2 `preflight` đếm đoạn thiếu evidence cả hai bên, ≠ 0 ⇒ dừng; §5 mục 4 |
| m-4 chạy bộ "trước" sớm lệch spec §2 | §1 (A quyết + điều kiện không chạy cùng lượt trả phí khác); §5 mục 1; §8 câu 3 |
| m-5 "A trình User trước khi khôi phục" lệch spec §5 | §4 "500 mới" + "Kết luận" (giữ spec; `rerun-f4` làm bằng chứng); §2 lệnh `rerun-f4`; §6 tiền; §8 câu 1 |
| m-6 lệnh T1 nạp key thừa | §5 mục 1 |
