# Plan: Phase 8.2 B3 — mốc cuối trên câu kín (B72)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-2d`) · Date: 2026-10-27 14:10 +0700 (`date`) · Bản 2 (sửa theo review C `phase_8_2_b3_plan_review.md` vòng 1 + quyết định A 14:2x 27/10 cho M-1, M-2 và §8; bản 1 `9d60b16b63da`)
Việc: `session_prompt/CURRENT_HANDOFF.md` mục B72 (A giao 14:1x 27/10). Chỉ viết plan, **chưa chạy**. B **không mở câu kín** khi viết plan.
Với câu kín, B chỉ đọc metadata: số dòng 36, md5 `ddc59587b502`, 4 field, phân bố loại câu trong `data/phase_8_1/baseline/g0_6_manifest.json`.
Trạng thái: chờ review (một session khác B, A chỉ định) ⇒ A duyệt sha ⇒ chạy khi **User quyết mở câu kín**.

## Căn cứ để review

1. File này — toàn bộ.
2. Spec 8.2 `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`: §3 mục 7–8, §5 "B3", §6 mục 4, §7 (tiền, judge), §10.2 (luật
   "không làm hỏng", dòng "Test … = không làm hỏng" và mức tụt luật (i)).
3. `skills/run-experiment/SKILL.md` §1 (tiêu chí ghi trước, cỡ mẫu), §3 mục 1, 6, 8 (nhiễu A/A, judge, harness ghi từng dòng), §4.
4. `session_prompt/Session_Prompt.md` §5 (câu kín, giữ mù) và `backend/evaluation/full_corpus_eval.py:322-382` (`answer_case`, `run_generation` —
   đường harness gọi), `backend/api/routes/chat.py:181-189` (API trả 500 khi `CitationIntegrityError`).

## 1. Câu hỏi thí nghiệm và hai chatbot so

**Lớp bài toán:** sau 8.2, chatbot có tốt hơn hay ít nhất **không tệ hơn** trên câu chưa ai dùng để chọn? 120 câu dev đã dùng để chọn, 56 câu
test đã bị nhìn ở 8.1. Câu kín là phép kiểm cuối (spec §8 dòng "Test 56 câu đã bị nhìn").

| Nhánh | Commit | Hành vi |
|---|---|---|
| **đầu** (mốc) | `f26485b` (spec §3 mục 8) | context 5, chưa NFC, bộ kiểm citation cũ (chỉ nhận `[n]`) |
| **cuối** | `main` lúc chạy, **sau quyết định B1** (ghi sha trong meta) | dự kiến context 10 + NFC (B1) + bộ kiểm citation v2 (`9e6d371`, rà code gói 1a: nhận cả `[Nguồn n]`) |

B đã đối chiếu `git diff f26485b 576f84e` (14:0x 27/10):
- `answer_case` và `run_generation` giống từng dòng.
- `full_corpus_prompt.py` chỉ gom chỗ dựng tin nhắn (C-03, commit `47a4e32` ghi "outputs byte-identical").
- `full_corpus_context.py` chỉ bỏ nhánh `apply_chat_template` không dùng.
- `settings.yaml` chỉ đổi đường dẫn file điều kiện và bỏ tham số Representation B.
- `pyproject.toml` và `uv.lock` không đổi.
- Cách nạp module khác (gói 1b `1e4acd0`): nhánh đầu còn tự chèn `sys.path` / import `backend.core…`. Phần tìm kiếm được T1 ở cả hai
  worktree kiểm (§5 bước 3); `preflight` in `__file__` của `evaluation.full_corpus_eval`, `retrieval.full_corpus` để chắc code nạp đúng worktree.

⇒ **"cuối − đầu" đo gộp ba thay đổi:** context 10, NFC, citation v2. B3 là phép kiểm tổng, không tách phần của từng thay đổi (§8 mục 2).
Nếu B0 dừng B1, "cuối" là `main` context 5. Khi đó B3 vẫn chạy được và chỉ đo citation v2; report ghi rõ.
(Không thêm nhánh thứ ba để tách — §8.)

## 2. Ai làm gì — giữ mù (`Session_Prompt.md` §5)

- **A không đọc nội dung câu kín**, kể cả file ghi lại câu; không mở file câu trả lời / lô chấm / điểm kèm feedback của B3. A chỉ giao việc và đọc
  report B3 (chỉ số đếm).
- **3 câu A đã thấy** (spec §3 mục 7; A thấy do User trích — `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md:42`; A không biết số dòng) — quyết định
  A 14:2x: **người chạy** đọc `knowledge-base-hue/evaluation/phase_8_1/sealed_user_feedback_private.md`, khớp ra số dòng trong `sealed_official.jsonl`
  (khớp `question` sau NFC + bỏ khoảng trắng thừa; lệnh `match-seen` chỉ in số dòng + số khớp), ghi `data/phase_8_2/b3/a_seen_lines.json`.
  Khớp đúng 3 dòng khác nhau ⇒ dựng S33. **Không đủ 3** ⇒ chỉ báo S36, kèm ghi chú số câu khớp được (không đoán).
- **Người chạy: B** (quyết định A 14:2x; B viết harness). **C** review plan và review report.
  - Người chạy chỉ chạy script. Script **không in nội dung**: chỉ số dòng, số đếm, đúng / sai, md5, token, ms.
  - Người chạy không đọc file câu trả lời, file lô chấm hay feedback judge.
  - Cần hiểu một câu vi phạm sàn ⇒ báo A số dòng + loại câu, A / User quyết có mở hay không.
- **Judge:** sub-agent Claude **mới**, do người chạy giao rõ là được đọc câu kín.
  - Mỗi sub-agent chỉ `Read` `backend/evaluation/full_corpus_judge_prompt.md` + lô của mình, rồi `Write` file điểm. Không đọc file khác.
  - Lô chấm không ghi nhánh (§4).
  - Brief judge ghi: **tin trả lời cuối chỉ gồm đường dẫn file điểm + số item đã chấm**, không chép câu hỏi / đáp án / câu trả lời / feedback
    (tin đó hiện thẳng trong ngữ cảnh người chạy).
- **Report tracked** (`phase_8_2_b3_implementation.md`): chỉ số dòng, số đếm theo loại câu (5 loại đã công khai trong manifest), đúng / sai,
  md5, token, USD, ms.
  - Không có nội dung câu hỏi / đáp án / câu trả lời / feedback.
  - Không có tên file corpus hay tiêu đề nguồn mà câu dựa vào.
- Grep **nội dung corpus** trong việc này loại `evaluation/`, `meta/`, `*sealed*`. Script tạm để `/tmp` và xóa khi xong. Script dùng lại để
  `data/phase_8_2/b3/tools/`. `rm` bị chặn ⇒ nhờ User `!`.

## 3. Harness (private `data/phase_8_2/b3/tools/b3.py`, 0 USD tới lệnh `run`)

Một file chạy được ở **cả hai commit**: chạy từ `<worktree>/backend`, `import evaluation.full_corpus_eval` của chính worktree đó. Hai commit cùng
có `answer_case`, `build_retrieval`, `build_context_builder`, `OpenAIFullCorpusGenerator`, `cost_usd`, `CONCURRENCY` 4 (đã kiểm `git show`).

- **`preflight --arm start|end`** (free):
  - md5 câu kín = `ddc59587b502`, 36 dòng;
  - `git rev-parse HEAD` của worktree = commit của nhánh;
  - `max_context_documents` đọc từ `settings.yaml` của worktree (đầu 5; cuối theo B1);
  - Qdrant 1 collection, 8.459 point;
  - đếm câu có `unicodedata.normalize("NFC", q) != q` và câu > 500 ký tự (giới hạn API `chat.py:38`) — **chỉ in số đếm**.
- **`run --arm --cases pilot|rest --name`** (có phí):
  - Dựng service / context / generator **như `run_generation`** (cùng 4 dòng, cùng `settings.yaml` của worktree, không tham số ghi đè).
  - Mỗi câu gọi `answer_case` với chuỗi câu hỏi **nguyên văn trong file** (không tự NFC — để đo đúng việc NFC của chatbot cuối).
  - `case_index` = số dòng 1..36, kèm `category`.
  - Đồng thời 4 (như evaluator), `asyncio.as_completed`, **ghi từng dòng ngay** (append + flush) ngay khi xong câu đó, kèm `wall_ms` (thời gian
    gọi `answer_case`, đo bằng `perf_counter`).
  - **Từ chối ghi đè** (`raise SystemExit('exists')`).
  - Ghi `<name>.meta.json` lúc bắt đầu và lúc kết thúc, kể cả khi lỗi: commit, md5, `max_context_documents`, model, n, tổng token, USD
    (`cost_usd`), giờ.
  - `answer_case` đã bắt lỗi của từng câu vào trường `error`. Khi generator ném lỗi thì không lấy được usage ⇒ ghi `usage: null`, ước tiền bằng
    token TB của nhánh đó (cận trên = câu tốn nhất) — skill §3.8. Script **không tự retry, không fallback**; chạy lại một lần là lệnh riêng
    `run --lines <n>` (§4), `merge` lấy lượt chạy lại thay dòng lỗi và giữ cả hai trong hồ sơ.
  - `preflight` đếm thêm câu có nhãn độ tự nhiên ≠ natural (§4) — chỉ in số đếm.
- **`merge`**, **`check`** (free): mỗi nhánh 36 dòng, gồm:
  - `error` ≠ null; out_of_scope bị trả lời;
  - từ chối trong phạm vi; `citation_error`; `context_sources`;
  - token, USD / câu; `wall_ms` p50 / p95.
- **`export-judge`**, **`check-judge`**, **`analyze`** (free) — như `experiments/phase_8_2/b1.py` (`pooled_items` / `scored_rows` / `paired`).
  `b1.py` hiện chỉ có trên nhánh `p82-b1` (vào `main` khi merge B1); `b3.py` chép logic đó, không import.
  - Câu trả lời giống hệt chữ trong cùng câu chấm **một lần**.
  - `item` là số mờ, xáo seed `20261024`; `map.json` item → [(nhánh, dòng)].
  - Lô ≈ 12 item, ghi bằng `g2_generate.write_batches`.
  - Điểm kiểm bằng `validate_score_rows`; số điểm = số item.
  - Thống kê: `bootstrap_mean_diff` (10.000 vòng, seed `20261024`), chênh = cuối − đầu.

Pilot: 10 dòng chọn bằng máy (`random.Random(20261024).sample(range(1, 37), 10)`), chạy ở **cả hai nhánh**; phần còn lại (`rest`) chạy sau khi
ước lại tiền. Số pilot không báo riêng làm kết quả, chỉ dùng để ước tiền (như B1).

## 4. Tiêu chí ghi trước

**Tập báo cáo** (spec §3 mục 7):
- **S33** = 36 dòng bỏ 3 dòng A đã thấy — **tập quyết** (chưa người điều phối nào đọc).
- **S36** = cả 36 dòng — báo kèm.
- Hai tập ra kết luận khác nhau ⇒ báo cả hai; kết luận theo S33. `match-seen` không ra đủ 3 dòng (§2) ⇒ chỉ có S36, kết luận theo S36, ghi chú.
- Chỉ số câu trả lời tính trên phần **trong phạm vi** của mỗi tập. Số out_of_scope = 3 trong S36 (manifest); trong S33, script đếm.

**Độ tự nhiên:** spec 8.1 G0.4 (`docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md:92-95`) soạn câu kín theo văn nói; User duyệt mẫu bản 5.
Không giả định suông: `preflight` đếm câu có nhãn ≠ natural trong `knowledge-base-hue/evaluation/phase_8_1/sealed_realism.jsonl` (khớp theo `question` NFC với
36 câu; **chỉ in số đếm**, kèm số câu không khớp được). 0 ⇒ không lọc. > 0 ⇒ báo thêm "S33 bỏ câu không tự nhiên"; kết luận vẫn theo S33, hai tập
khác kết luận ⇒ A trình User.

```yaml
experiment_id: p82_b3_sealed_final
baseline: f26485b (chatbot đầu 8.2: context 5, chưa NFC, citation v1)
changed_variable: chatbot cuối 8.2 (main sau B1) — gộp context 10 + NFC + citation v2 (§1)
unchanged: [corpus, chunker, embedding, index, retrieval dense_bm25_rrf, prompt, model gpt-6-luna, reasoning mặc định, judge Claude]
data: {file: knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl, md5: ddc59587b502, n: 36, decide_set: S33, also: S36}
metrics:
  - {name: out_of_scope bị trả lời, fn: "refusal == false trên category out_of_scope", better: down, role: floor, floor: 0 (nhánh cuối), src: "full_corpus_eval.is_refusal"}
  - {name: lỗi kỹ thuật (mạng / provider), fn: "error != null sau một lần chạy lại đúng câu đó", better: down, role: floor, floor: 0 mỗi nhánh}
  - {name: Completeness trong phạm vi, fn: "analyze.paired (cuối − đầu); câu 500 citation chấm 1", better: up, role: tolerance, max_worse: "TB ≥ −0,1 và số câu tụt ≤ A/A + 3 = 5", noise: "A/A = 2 (§4 dòng Nhiễu)"}
  - {name: Accuracy trong phạm vi, fn: "analyze.paired; câu 500 citation chấm 1", better: up, role: tolerance, max_worse: "TB ≥ −0,1 và số câu tụt ≤ A/A + 3 = 5", noise: "A/A = 2"}
  - {name: từ chối nhầm trong phạm vi, fn: "refusal == true, category != out_of_scope", better: down, role: tolerance, max_worse: "+1 câu", noise: "B1↔G2.1a: 0 câu đổi từ chối ↔ trả lời"}
  - {name: câu API trả 500 vì citation, fn: "citation_error != null theo bộ kiểm của commit nhánh đó", role: watch, note: "báo riêng mỗi nhánh; điểm đã tính 1 ở hai dòng trên", src: "api/routes/chat.py:181-189"}
  - {name: Completeness — "tốt hơn", fn: "analyze.paired ci95", better: up, role: watch, note: "chỉ báo; CI 95 % > 0 ⇒ ghi 'tốt hơn trên câu kín'"}
  - {name: Relevance, role: watch}
  - {name: USD / câu, fn: cost_usd, role: watch}
  - {name: output_tokens / câu, role: watch}
  - {name: wall_ms p50 / p95 (đồng thời 4), role: watch}
  - {name: context_sources TB, role: watch}
  - {name: câu NFC ≠ nguyên văn (số đếm), role: watch, note: "0 ⇒ phần NFC không được câu kín thử"}
result: {paired_delta: null, ci95: null, wins_ties_losses: null}
conclusion: null   # không làm hỏng / làm hỏng / chưa đủ (lỗi kỹ thuật); kèm "tốt hơn" nếu watch CI > 0
```

- **Câu 500 vì citation = câu trả lời hỏng** (quyết định A 14:2x cho M-1 review C): trên đường production mọi `CitationIntegrityError` ra 500
  (`chat.py:181-189`), người dùng không thấy câu trả lời ⇒ ở **cả hai nhánh**, câu có `citation_error` được gán Completeness = Accuracy = 1 (judge vẫn
  chấm chữ, điểm đó chỉ báo), gộp vào TB và "số câu tụt". Số câu 500 mỗi nhánh báo riêng (theo dõi). Không có luật riêng cho citation ⇒ không có hai
  dòng tiêu chí đếm cùng một lỗi (skill §1 mục 3). Lý do không theo nguyên "Sàn chung" §10.2: mục đó viết cho biến thể Bước 2 so với mốc B1, còn B3 so
  đầu ↔ cuối trên đường production.
- **Lỗi kỹ thuật** (mạng / provider, trường `error`): chạy lại **đúng câu đó một lần** (`run --lines <n> --name <arm>_retry`, file mới), ghi cả lượt
  lỗi lẫn lượt chạy lại; vẫn lỗi ⇒ kết luận "chưa đủ".
- Hai sàn chung khác của §10.2 **không áp** cho câu kín: "0 câu mất đoạn đúng khỏi context" (câu kín không có nhãn đoạn đúng) và "câu 120, 168 vẫn từ chối"
  (câu dev, không thuộc bộ này).
- "Lỗi kỹ thuật" đếm `error` (exception trước / trong lúc sinh), khác `citation_error` (có câu trả lời nhưng citation sai) — không chồng nhau.
- **Kết luận:**
  - **không làm hỏng** = qua 2 sàn và 3 mức tụt trên S33.
  - **làm hỏng** = vi phạm một trong các điều trên ⇒ A trình User kèm số dòng + loại câu (không kèm nội dung).
  - Lỗi kỹ thuật còn sau một lần chạy lại ⇒ "chưa đủ".
- Chỉ số "tốt hơn" không quyết (spec §10.6 Q2: tập kiểm nhỏ thì xác nhận = "không làm hỏng").

**Cỡ mẫu** (*suy ra*, ghi trước):
- S33 có khoảng 30 câu trong phạm vi.
- Theo bảng spec §10.3, 4 thắng / 0 thua cho p 0,026 trên 40 câu ⇒ cận dưới CI 95 % > 0 cần khoảng ≥ 4 câu thắng ròng.
- 8.1 test cho context 10 Completeness +0,27 (56 câu) ⇒ nếu hiệu ứng giữ thì "tốt hơn" có thể thấy được, nhưng **"chưa rõ" là kết quả hợp lệ**.
- Mức tụt "≤ 5 câu" và "TB ≥ −0,1" trên ~30 câu (một câu ±1 = ±0,033 TB): với n này, dòng TB thường chặn trước (thua ròng > 3 câu ±1 là trượt).
  Đây là phép kiểm "không làm hỏng", không phải phép chọn.

**Nhiễu A/A:** không chạy A/A trên câu kín. Dùng lại A/A context 10 B1 ↔ G2.1a (`phase_8_2_b1_implementation.md` §4 trên nhánh `p82-b1`: Completeness
4 / 171 / 1, Accuracy 3 / 171 / 2, 0 câu đổi từ chối) và 7B Run 1 ↔ 2 cho context 5 (16 / 176 câu đổi điểm). Lý do: cùng model, cùng prompt; bộ
câu khác ⇒ ghi là giới hạn. **A/A dùng cho mức tụt = 2 câu** (m-2 review C): context 10 có 1 câu Completeness tụt / 176 (≈ 0,2 / 33); context 5 có
16 / 176 câu đổi điểm hai chiều ở mọi chỉ số (≈ 3 / 33, chia đôi ≈ 1,5 tụt) ⇒ lấy cận trên làm tròn 2 ⇒ mức tụt = A/A + 3 = 5 (theo spec §10.2). Không chạy
A/A trên câu kín (quyết định A 14:2x, §8).

**Judge:**
- Claude sub-agent, ghi model id (session hiện tại: `global.anthropic.claude-opus-5-5`, cùng judge B1 / G2).
- Hai nhánh chấm **cùng lượt mù**.
- Cùng judge prompt, rubric, model ⇒ không cần lượt "kiểm người chấm 4 phiếu" (skill §2). Đổi model judge ⇒ chạy 4 phiếu trên câu **không kín**
  trước.

## 5. Cách chạy (khi User quyết mở câu kín; sau B0 + quyết định B1)

1. **A:**
   - giao B trong `CURRENT_HANDOFF.md`, ghi rõ "được mở câu kín qua script + sub-agent judge";
   - commit `main`.
   B: `match-seen` (§2) ⇒ `a_seen_lines.json`.
2. **Người chạy:**
   - tạo worktree `/tmp/b3_start` (`git worktree add --detach /tmp/b3_start f26485b`) và `/tmp/b3_end` (`main` HEAD);
   - symlink `data/`, `knowledge-base-hue/`;
   - `uv run --project /home/minhhieu/hue_rag`; Qdrant chỉ đọc.
3. **Free:**
   - T1 ở cả hai worktree: `python -m evaluation.full_corpus_eval retrieval --out data/phase_8_2/b3/t1_<arm>.jsonl` ⇒ phải giống byte
     `cefb2d1ad609`. Dùng Golden, không dùng câu kín; xác nhận index và tìm kiếm giống nhau.
   - Sau đó chạy `preflight` hai nhánh.
4. **Pilot:** `run --cases pilot` hai nhánh (`--env-file /home/minhhieu/hue_rag/.env`) ⇒ ước lại tiền 36 câu.
5. **rest** hai nhánh ⇒ `merge` ⇒ `check`.
6. **Judge:**
   - `export-judge` ⇒ giao sub-agent judge (mỗi agent ≤ 2 lô) ⇒ `check-judge` ⇒ `analyze` (S33, S36).
   - **Ghép khóa nhánh chỉ sau khi đủ điểm.**
7. **Báo cáo:**
   - report `phase_8_2_b3_implementation.md`: bảng do script in ra, không gõ tay;
   - 3–5 dòng lời thường cho User.
   - Gỡ worktree + symlink; xóa `/tmp` tạm; nhắn A + người review.

## 6. Tiền, thời gian, dừng

- **Ước** (từ token thật):
  - Context 5 ≈ 0,000133 USD / câu (handoff, "Quyền").
  - Context 10 ≈ 0,00021 USD / câu: B1 176 câu = 291.269 vào / 15.585 ra ⇒ 0,0369 USD.
  - 36 câu × 2 nhánh ≈ **0,012 USD**; pilot ≈ 0,0034.
- **Trần B3: 0,03 USD** (spec §7 ước 0,015). 8.2 đã dùng ≈ 0,212 + 0,0003 (B71) / 0,5.
- **Dừng + báo A:**
  - md5 / số dòng / commit / T1 lệch;
  - ước sau pilot > 1,5 × 0,012;
  - `error` ≠ null còn sau một lần chạy lại đúng câu đó (§4) ⇒ "chưa đủ";
  - script in ra thứ gì ngoài số đếm (lỗi code ⇒ sửa script, không dùng output đó);
  - cần đọc nội dung để kết luận.
- **Thời gian:** sinh ≈ 2–4 phút / nhánh (đồng thời 4); judge ≈ 6 lô; tổng ≈ 1 giờ.

## 7. Hợp đồng kiểm

- **Người chạy nộp:**
  - `data/phase_8_2/b3/`: `{start,end}_{pilot,rest}.jsonl` + `.meta.json`, `{start,end}.jsonl`, `check.json`, `judge/` (`map.json`, lô, điểm),
    `analyze.json`, `t1_*.jsonl`, `preflight_*.json`;
  - sha 12 của script;
  - report.
- **Người review** (≠ người chạy; không đọc nội dung):
  - chạy lại `check`, `check-judge`, `analyze` (free) ⇒ số trùng report;
  - kiểm md5 câu kín, sha T1, meta commit / `max_context_documents`;
  - đọc diff script tìm chỗ in nội dung;
  - grep report tracked: không có nội dung câu (hook `overlap_scan.py` quét câu kín khi commit).

## 8. Quyết định của A (14:2x 27/10) cho các câu hỏi bản 1

1. Người chạy: **B**.
2. **Không** thêm nhánh thứ ba "`main` context 5 trước merge B1" (≈ +0,005 USD): B3 là phép kiểm tổng; phần citation v2 đã đo offline ở rà code 1a
   (69 → 14 lỗi / 1.600 câu).
3. **Không** chạy A/A trên câu kín (≈ +0,007 USD): dùng A/A B1 ↔ G2.1a + 7B Run 1 ↔ 2, ghi giới hạn (§4 "Nhiễu A/A").
