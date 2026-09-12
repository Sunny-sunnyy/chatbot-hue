# Full-corpus RAG Wave 1 — Correction 3

Target role: implementer
Authored by: reviewer
Handoff kind: correction
State: active
Base commit: d631d3cc47a66d7a43c71f36c585d73ae9d21f9e
Head commit: worktree
Risk level: low
Git authorization: none
Sub-agent authorization: none

## Objective và nguồn điều khiển

Đóng duy nhất W1-C2-R1 trong
`reports/full_corpus_rag_wave_1_correction_2_codex_review_2026_09_12.md`. Đây là
delta test-evidence hẹp của Wave 1. W1-C1-R1 và W1-C1-R2 đã closed; không mở lại
production implementation, canonical counts hoặc Wave 2.1.

Full-read review report trên, prompt này, current implementation report và
`backend/tests/test_full_corpus_chunker.py`. Targeted-read exact determinism/sample
requirements được review report dẫn chiếu và exact source sections của Mệ Kéo/Gia
Lạc. Các guide/status, corpus khác, runtime modules, artifact content và wave sau
là reference-only trừ khi fresh check phát hiện contradiction phải báo dừng.

## Required correction delta

1. Sửa test full-corpus determinism để:
   - gọi `chunk_full_corpus()` hai lần;
   - deep-compare ordered chunk objects cùng `chunk_id` và `point_id`;
   - assert point IDs unique, bằng `point_id_for_chunk_id(chunk_id)` và là UUID
     version 5;
   - giữ hai generated preview outputs `read_bytes()` bằng nhau và totals derive từ
     canonical artifact.
2. Siết test Mệ Kéo:
   - không nối nhiều chunk;
   - chọn exact chunk cho mệnh đề bún không có thịt bò và exact chunk cho thành
     phần; assert nội dung/quan hệ trong chính chunk/evidence part và exact source
     slice.
3. Siết test Gia Lạc:
   - không nối nhiều chunk;
   - chọn exact historical chunk chứa Nam Phổ cùng ngữ cảnh lịch sử, exact
     contemporary chunk chứa Chợ Mai cùng Nguyễn Đình Tứ, và exact
     non-commercial chunk chứa cả quan hệ không thương mại đơn thuần/cầu may;
   - assert historical/contemporary là hai chunk IDs khác nhau và mọi evidence
     part được dùng là exact source slice.
4. Cập nhật implementation report thành evidence index đúng test names/commands/
   results. Không tuyên bố approved/closed.

## Allowed paths

- `backend/tests/test_full_corpus_chunker.py`;
- `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`;
- `session_prompt/CURRENT_HANDOFF.md`.

Không sửa production code/config, corpus, canonical artifact, dependency/lockfile,
guides/status/spec/plan/contracts/review reports hoặc bất kỳ Wave 2 path nào.

## Acceptance và checks phải chạy lại

Acceptance đạt khi direct assertions đóng đủ ba nhánh của W1-C2-R1, không còn
multi-chunk concatenation trong hai sample tests, repeated chunks/IDs/UUID5 được
so sánh thật, và existing Wave 1 suite/artifact vẫn ổn định.

Implementer chạy fresh:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction3-uv-cache uv run python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_markdown_chunker.py -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction3-uv-cache uv run python -m backend.ingestion.preview --output /tmp/full_corpus_rag_wave_1_preview_correction3.json
cmp reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json /tmp/full_corpus_rag_wave_1_preview_correction3.json
git diff --check
```

Không chạy full backend/live suite; không gọi model/API inference, embedding,
Qdrant, frontend, notebook hoặc benchmark. Không Git write hoặc dùng subagent.

## Next action duy nhất

Implementer thực hiện delta test-only trên, self-review exact diff, cập nhật report
trung thực và chuyển `CURRENT_HANDOFF.md` sang Reviewer với handoff kind exact
`correction`. Không bắt đầu Wave 2.1.
