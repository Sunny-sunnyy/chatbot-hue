# Full-corpus RAG Wave 1 — Correction 2

Target role: implementer
Authored by: reviewer
Handoff kind: correction
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none

## Objective và nguồn điều khiển

Đóng đúng W1-C1-R1..R3 tại
`reports/full_corpus_rag_wave_1_correction_1_codex_review_2026_09_12.md`. Đây là
delta hẹp thứ hai của Wave 1. Các phần Correction 1 đã đạt không được viết lại;
approved Spec/Plan/Review Contract/Wave 1 prompt vẫn giữ hiệu lực. Không mở Wave
2.1.

Sau bootstrap Implementer, full-read review report trên, prompt này, Correction 1
report, preview artifact và mọi task source/test định sửa. Targeted-read exact
requirements được review report dẫn chiếu. Các guide/status, corpus ngoài sáu named
samples và Điện Hòn Chén, `.env`, logs, caches, Qdrant state, notebooks và wave sau
là reference-only.

## Required correction delta

1. Sửa `ConditionManager` trực tiếp:
   - selector bắt buộc đúng `heading_path: list[str]`, `block_type: str`,
     `exact_text: str`; malformed config fail closed;
   - global validation và per-document resolution dùng cùng exact matcher;
   - không wildcard, alias, match-first, regex DSL hoặc fallback;
   - thêm focused tests cho malformed schema, missing/duplicate condition và
     missing/duplicate target/source.
2. Sửa default tokenizer checker để không reuse config/tokenizers của settings khác.
   Giải pháp đơn giản nhất là bỏ singleton config-blind; nếu cache thì key phải bao
   trọn ID/limit/prefix/word-segmentation. Giữ local-only, `truncation=False`, thiếu
   bất kỳ tokenizer nào fail closed. Thêm regression test gọi hai config khác nhau
   trong cùng process và chứng minh config sau được dùng.
3. Bổ sung đúng acceptance tests còn thiếu, không tái cấu trúc production code nếu
   không cần:
   - blockquote parse/heading/exact slice và image/separator behavior;
   - oversized paragraph sentence split, table row split giữ header/condition và
     nested-list split giữ exact parent plus sub-item;
   - generic condition/parser error làm preview non-PASS, tách khỏi synthetic
     oversized case;
   - sáu named sample tests kiểm exact evidence slice/range và quan hệ trong đúng
     chunk, không ghép toàn file rồi chỉ tìm từ rời;
   - full repeated chunks/IDs/UUID5 và hai preview outputs `read_bytes()` bằng nhau;
   - bỏ hard-code chunk count `8460` như một implementation invariant; đối chiếu
     generated totals với checked-in canonical artifact và derived breakdown sums.
4. Regenerate canonical preview bằng source cuối cùng. Sửa lại chính Correction 1
   implementation report để nó chỉ là evidence index trung thực: exact test names,
   exact command/result/stdout, exact artifact counts, changed paths và mọi
   `not run`/failure. Không ghi progress log không được CLI thật phát ra, không tự
   kết luận `CLOSED`/`APPROVED` và không đề xuất mở trực tiếp Wave 2.1.

## Allowed paths

- `backend/ingestion/chunking/full_corpus_chunker.py`;
- `backend/ingestion/preview.py` chỉ nếu cần cho exact error/determinism behavior;
- `backend/tests/test_full_corpus_chunker.py`;
- `backend/config/full_corpus_conditions.json` chỉ nếu strict validation phát hiện
  config canonical thật sự sai;
- `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`;
- `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`;
- `session_prompt/CURRENT_HANDOFF.md`.

Không sửa corpus, settings/schema/parser/source-state nếu không có finding yêu cầu,
không sửa guides/status/spec/plan/Review Contract/review reports, không thêm
dependency và không chạm API/embedding/vectorstore/retrieval/generation/frontend/
Golden/evaluation/notebook.

## Acceptance và checks phải chạy lại

Acceptance đạt khi W1-C1-R1..R3 có direct tests/evidence, canonical artifact vẫn
`PASS`, 205 files, zero errors/oversized, mọi representation vừa ba tokenizer và
domain/P7 totals tự nhất quán. Không có silent fallback, config-order dependence,
partial success, evidence loss/duplication hoặc fabricated execution claim.

Implementer chạy fresh đúng các offline checks sau:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction2-uv-cache uv run python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_markdown_chunker.py -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction2-uv-cache uv run python -m backend.ingestion.preview --output reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction2-uv-cache uv run python -m backend.ingestion.preview --output /tmp/full_corpus_rag_wave_1_preview_correction2_repeat.json
cmp reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json /tmp/full_corpus_rag_wave_1_preview_correction2_repeat.json
git diff --check
```

Không chạy `backend/tests` toàn bộ hoặc `test_ingestion_pipeline.py`: chúng dùng
real Qdrant/embedder và nằm ngoài offline Wave 1 acceptance. Không gọi model/API,
embedding inference, Qdrant, frontend, notebook hoặc benchmark.

## Next action duy nhất

Implementer thực hiện delta trên, self-review exact diff, cập nhật report/artifact
trung thực và chuyển `CURRENT_HANDOFF.md` sang Reviewer với handoff kind exact
`correction`. Không bắt đầu Wave 2.1.
