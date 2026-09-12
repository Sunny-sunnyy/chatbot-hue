# Implementer — Correction 1 cho Verified Architecture Extraction từ `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Đây là correction delta hẹp cho artifact extraction mới. Không mở lại hoặc sửa
report survey 885 dòng và không triển khai runtime.

## 1. Bootstrap và mức đọc

Đọc đúng thứ tự; mọi file `full-read` phải đọc tới EOF nếu output bị cắt:

1. `full-read` — `session_prompt/Session_Prompt.md`.
2. `targeted-read` — `session_prompt/Project_Status.md`: các mục current runtime,
   full-corpus design, decisions, safety và đoạn `llm_rag` hiện hành.
3. `full-read` — `session_prompt/IMPLEMENTER_WORKFLOW.md`.
4. `full-read` — `skills/risk-gated-agent-review/SKILL.md`.
5. `full-read` — `session_prompt/CURRENT_HANDOFF.md`.
6. `full-read` —
   `handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md`.
7. `full-read` —
   `reports/llm_rag_verified_architecture_extraction_2026_09_11.md`.
8. `full-read` —
   `reports/llm_rag_verified_architecture_extraction_implementation_report_2026_09_11.md`.
9. `full-read` —
   `reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`.
10. `full-read` — correction prompt này.
11. `targeted-read` — `guides/full_corpus_rag.md`: `Quyết định đã chốt`,
    `Nội dung chưa chốt`, `Chuỗi tài liệu và điểm duyệt`.
12. `targeted-read` — decision notes
    `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`:
    `Qdrant collection strategy` và `Decision queue sau Verified Architecture Extraction`.

Report survey 885 dòng, survey corrections cũ và hai tài liệu `tai_lieu` của
reference là `reference-only`; không mở mặc định. Source chỉ targeted-read đúng
anchors cần sửa/đối chiếu. Không dùng `practical-project-coding`, network hay
subagent.

## 2. Findings phải đóng

Đóng đủ VAE-R1–VAE-R4 trong Codex review:

1. Giữ lexical baseline/sparse consumer và các lựa chọn lifecycle, payload,
   fusion/reranker, context/API budgets ở trạng thái open. Không biến Foods
   runtime hay Reviewer recommendation thành canonical full-corpus decision.
2. Mỗi technical source claim chỉ có một authoritative occurrence/anchor trên
   toàn artifact. Giữ đúng sáu H2 bắt buộc, nhưng bỏ bảng/cột source lặp; §4 chỉ
   nêu mapping ngắn không lặp source fact/anchor và không chọn mechanism còn mở.
3. Xóa self-review/completion prose, lời cấm tuyệt đối và version dependency
   không decision-relevant.
4. Bỏ hoặc thu hẹp claim `architectureTypes` tạo 0 chunks vì static source chỉ
   chứng minh điều kiện. Mô tả sparse mapping đúng `set(tokens)`. Mô tả test
   boundary đúng: 20 unit tests trong ba file, một phần pure deterministic và
   provider/integration paths dùng fake/monkeypatch; không suy “mọi test đều
   monkeypatch” hoặc inventory toàn test tree.
5. Anchor one-shot/non-streaming phải trỏ đúng canonical decision. Tách hai
   disjoint ranges `sparse_embedder.py:21, 52-56` và
   `chat_openai.py:26-46, 139-165` thành các link độc lập. Kiểm semantic từng
   anchor, không chỉ existence/EOF.
6. Nhãn `[Observed in llm_rag]`, `[Design inference]`,
   `[Canonical Hue decision]`, `[Not verified]` phải phản ánh đúng từng claim;
   mapping/open recommendation không được để không nhãn theo cách trông như
   requirement đã chốt.
7. Giữ artifact tối đa 320 dòng/55.000 bytes và đúng sáu H2 theo contract gốc.

Không thêm finding, inventory, validator framework, glossary, traceability,
self-review hoặc quyết định Hue mới để xử lý correction.

## 3. File được phép thay đổi

Chỉ được sửa/tạo:

```text
reports/llm_rag_verified_architecture_extraction_2026_09_11.md
reports/llm_rag_verified_architecture_extraction_correction_1_implementation_report_2026_09_11.md
session_prompt/CURRENT_HANDOFF.md
```

Không sửa implementation report gốc, Codex review, contract/correction prompt,
guide, decision notes, source/runtime/tests/corpus/Golden/index/dependencies hay
repository `/home/minhhieu/llm_rag`.

## 4. Verification bắt buộc

1. Full-read extraction đã sửa tới EOF.
2. Kiểm đúng sáu H2, `wc -l -c` và các nhóm nội dung bị loại.
3. Với mọi local link, kiểm path tồn tại; dùng `awk 'END { print NR }'` cho đầu
   và cuối range. Validator phải so cả range trong label với URL fragment và
   tách disjoint ranges thành link riêng.
4. Semantic-check lại exact claims bị VAE-R1–VAE-R3 ảnh hưởng.
5. Chạy `git diff --check` và `git status --short --untracked-files=all`.
   Correction report phải phân biệt ba task paths với các thay đổi worktree có
   sẵn; không nói toàn status chỉ có ba paths.

Không chạy/import project code, tests, model, API, Qdrant, frontend, notebook
hoặc benchmark; không đọc `.env`, logs hay data generated/raw/processed.

## 5. Evidence reuse và Review Contract

Có thể reuse trong cùng correction series các focused source checks đã đạt và
không bị wording/anchor sửa: `processed_dir`, pipeline/upsert, dense-only query,
raw fusion, UUID/lifecycle và reranker score. Không gọi chúng là fresh run nếu
không đọc lại. Mọi claim/anchor bị correction phải được kiểm lại.

Risk giữ `medium`. Reviewer sẽ chạy lại minimum diff gate, full-read extraction
và correction report, structure/size/duplication/labels, toàn bộ path/range
validator và semantic checks bị ảnh hưởng. Reviewer không chạy runtime.

## 6. Bàn giao

Khi hoàn tất, cập nhật `CURRENT_HANDOFF.md`:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none
```

Next action duy nhất: Reviewer re-review Correction 1 theo Codex review và
correction contract. Không claim approved/completed, không resume Decision Queue,
Written Spec hoặc Plan.
