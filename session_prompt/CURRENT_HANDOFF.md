# Active — Phase 7A2 Gate 2: build 2 index + cutover runtime

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: 5e8aff1
Head commit: worktree
Risk level: high (provider mới, gửi corpus private ra ngoài, tạo collection, cutover runtime)
Git authorization: none (Implementer không commit; Reviewer commit sau review)
Sub-agent authorization: theo standing authorization trong `IMPLEMENTER_WORKFLOW.md`
Paid-call authorization: đúng spec §5.6 (xem dưới); User đã duyệt trong spec, không cần xin xác nhận lại
Qdrant authorization: chỉ tạo `hue_full_corpus_7a2_e5_small_384` và `hue_full_corpus_7a2_qwen3_8b_4096`

## Mục tiêu

Thực hiện plan Task 4–8: build record là nguồn sự thật duy nhất, hai
candidate + dense runner OpenRouter, một đường build thẳng, build thật hai
index trên corpus đã sửa, cutover runtime full-corpus sang
`hue_full_corpus_7a2_e5_small_384` và nghiệm thu end-to-end.

Gate 1 đã User-closed 2026-10-24 (m1 xong). Corpus hiện tại: 205 file,
8.459 chunk.

## Đọc trước khi làm

- `full-read`: plan `docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md`
  phần Global Constraints, Gate 2 (Task 4–8) và Review Contract
- `full-read`: spec `docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md` §5, §8, §9
- `full-read`: source/test mà Task 4–8 liệt kê trong mục **Files**
- `reference-only`: `reports/phase_7a2_openrouter_embedding_survey_2026_10_23.md`
  (hợp đồng API OpenRouter), `reports/full_corpus_phase_6_gpt_6_luna_review_2026_10_23.md`
  (baseline 5 case live smoke)

## Quyền paid (spec §5.6) — tối đa, không vượt

- OpenRouter `qwen/qwen3-embedding-8b`: tối đa 2 lần build đầy đủ; tối đa 50
  call embed query (gồm mẫu cosine Task 7 Step 3 và retrieval smoke Task 8 Step 4).
- `gpt-6-luna`: đúng một lần live smoke 5 call.
- Build 8B lỗi: được xóa đúng collection `hue_full_corpus_7a2_qwen3_8b_4096`
  của chính lần build lỗi (và record nếu đã ghi) rồi build lại, trong giới hạn
  2 lần. Không xóa collection nào khác.
- Mọi request OpenRouter gửi `provider: {"data_collection": "deny"}`; không pin
  provider, không retry/fallback/resume.

## Rủi ro đã biết

1. API full-corpus đang FAIL freshness có chủ đích cho tới cutover; không phải
   regression.
2. Task 4 phải làm trước mọi lần build: `prepare_full_corpus_input()` hiện raise
   vì hằng số `EXPECTED_CHUNK_COUNT=8460`/identity cũ.
3. OpenRouter 429 (survey từng gặp DeepInfra `engine_overloaded`): lỗi giữa
   build tiêu một lần build. Hai lần đều lỗi thì dừng và báo Reviewer; pin
   provider là quyết định mới của User.
4. Chunker cần tokenizer e5-small/e5-base/huydang trong HF cache; cảnh báo
   "Token indices sequence length…" là bình thường.
5. Collection Foods `hue_foods_e5_small_384` và `_dense`: không đụng tới (User
   giữ qua Phase 7). API chỉ phục vụ full-corpus; settings/tests/benchmark Foods
   cũ còn tham chiếu collection Foods — không sửa phần đó trong Gate 2.
6. `phase6_live_smoke.py` và test liên quan: đọc trước khi sửa (Task 5 Step 5,
   Task 8 Step 3); không đổi 5 case hay logic chấm.

## Dừng và báo Reviewer khi

- cần vượt giới hạn paid, xóa collection ngoài quyền trên, đổi chunker/payload/
  retrieval profile/generation, hoặc cutover sang 8B;
- cả 2 lần build 8B đều lỗi;
- live smoke có regression so với Phase 6 mà chưa tìm được root cause trong
  phạm vi (ghi root cause đã biết, không chạy lại);
- spec/plan mâu thuẫn với source theo cách làm đổi behavior hoặc scope.

## Đầu ra

- Report `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md` theo
  plan Task 8 Step 6 (plan ghi hậu tố `_2026_10_23`; dùng ngày thực tế; không chép corpus, câu hỏi Golden, vector hay payload).
- Thay handoff này bằng handoff `final_review` cho Reviewer (Target role:
  reviewer), giữ acceptance mapping, changed files, lệnh/kết quả, số call
  paid đã dùng, failed/skipped/not verified.
- SendMessage cho Reviewer (`hue-rag-c3`) khi xong hoặc khi gặp điều kiện dừng.

## Sau Gate 2

Reviewer review độc lập theo Review Contract (read-only count/payload/chiều,
đọc hai build record, health runtime; không chạy lại paid call), User đóng Gate
2, rồi mới mở Gate 3 (xóa 13 collection spec §6.1).

## Lịch sử

Gate 1 closure: `reports/phase_7a2_gate_1_review_2026_10_23.md` (approved
2026-10-24), commit `5e8aff1`.
