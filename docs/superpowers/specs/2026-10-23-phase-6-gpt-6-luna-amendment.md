# Phase 6 — gpt-6-luna model + Qdrant port amendment

**Date:** 2026-10-23 (+07)
**Status:** Approved by User (direct instruction, see §1)
**Owner:** Reviewer (Claude Opus 5.5, session `hue-rag-66`)
**Implementer:** Claude Opus 5.5, session `hue-rag-08`
**Risk level:** High (provider model change + paid calls)
**Execution authorization:** Only through `session_prompt/CURRENT_HANDOFF.md`

Tài liệu này là một delta gộp spec + plan + Review Contract cho đúng hai thay
đổi: đổi model OpenAI và đổi host port Qdrant. Mọi contract khác của Phase 6
trong các tài liệu sau giữ nguyên:

```text
docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md
docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md
handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
```

Nơi các tài liệu đó ghi `gpt-5.4-nano`, `gpt-5.4-mini` hoặc
`http://localhost:6333`, giá trị trong tài liệu này thay thế.

## 1. Quyết định của User ngày 2026-10-23

User trực tiếp quyết định trong phiên Reviewer:

1. Đổi **mọi** model OpenAI của dự án sang `gpt-6-luna`: Phase 6 full-corpus
   generation, Foods `llm.answer_model`, `evaluation.answer_model` và
   `evaluation.judge_model`. Lý do User nêu: rẻ hơn và mạnh hơn
   `gpt-5.4-nano`/`gpt-5.4-mini`.
2. Đổi host port Qdrant của hue_rag để chạy song song với `mekongai-template`
   (đang giữ `127.0.0.1:6333-6334`).
3. Cho phép gọi API có phí cho live run Phase 6 trên `gpt-6-luna`.
4. Không cần trình duyệt riêng spec/plan cho delta này: Reviewer viết tài liệu,
   gửi Implementer nhận xét khả thi, chỉ trình lại User nếu nhận xét làm đổi
   scope, acceptance hoặc quyền. Đây là ngoại lệ User cấp trực tiếp cho exact
   task này theo `Session_Prompt.md`, không phải tiền lệ chung.
5. Không sửa quy trình/skills dù cả hai vai trò hiện là Claude.

Reviewer đã quan sát ngày 2026-10-23 bằng `GET /v1/models` (không tốn phí):
`gpt-6-luna` có trong danh sách model của tài khoản. Chưa quan sát behavior
generation của model này.

## 2. Model contract mới

```text
Provider: OpenAI direct (không đổi)
SDK boundary: OpenAI Agents SDK, versions đang pin trong uv.lock (không đổi)
Phase 6 generation model: gpt-6-luna (floating alias, không pin snapshot)
Foods llm.answer_model: gpt-6-luna
evaluation.answer_model: gpt-6-luna
evaluation.judge_model: gpt-6-luna
Token encoding for packer: o200k_base (giữ; xem rủi ro R1)
Reasoning/sampling: không cấu hình/không truyền cho Phase 6 (không đổi)
Caps/budget/timeout/retries/max_turns: 2048/256, 16384/2048/512, 45s, 0, 1 (không đổi)
```

Không thêm fallback về `gpt-5.4-nano`, không thêm model selector, không thêm
config field mới. Chỉ thay giá trị model và các guard đang khóa cứng giá trị cũ.

## 3. Qdrant port contract mới

```text
docker-compose.yml ports: "127.0.0.1:6335:6333", "127.0.0.1:6336:6334"
backend/config/settings.yaml database.url: http://localhost:6335
```

Port trong container giữ 6333/6334; volume `./qdrant_storage` không đổi nên dữ
liệu không bị ảnh hưởng. Bind `127.0.0.1` vẫn mở được bằng
`http://localhost:6335/dashboard` (cùng cơ chế Mekong đang dùng ở 6333) và không
lộ Qdrant không có API key ra LAN. Guide/report lịch sử ghi 6333 giữ nguyên.

## 4. Exact implementation scope

Implementer chỉ sửa:

| Path | Thay đổi |
|---|---|
| `backend/config/settings.yaml` | 4 model values → `gpt-6-luna`; `database.url` → `:6335`; thay comment "verified 2026-08-13" bằng nguồn quan sát mới hoặc xóa nếu không còn đúng |
| `backend/core/settings_loader.py` | guard model → `gpt-6-luna` |
| `backend/llm/openai_tokenizer.py` | `OPENAI_GENERATION_MODEL` → `gpt-6-luna` |
| `backend/llm/generator_openai_full_corpus.py` | comment/default model → `gpt-6-luna` |
| `backend/ingestion/full_corpus_pipeline.py` | URL guard → `http://localhost:6335` |
| `docker-compose.yml` | ports như §3 |
| `backend/tests/test_phase6_settings.py`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_llm_generator_openai.py` | expected model string |
| `notebooks/06_generation_and_api.ipynb`, `notebooks/07_evaluation.ipynb` | đổi 5 chuỗi model trong Markdown mô tả cấu hình hiện hành (NB06 3, NB07 2) sang `gpt-6-luna`; không sửa code cell; outputs rỗng, `execution_count: null` (Reviewer chốt 2026-10-23 sau feasibility comment của Implementer) |

Không sửa prompt, cases, retrieval, context packer, citations, API/UI, runner
logic, dependencies hoặc Qdrant data. Không xóa container/volume Mekong.

## 5. Rủi ro đã biết

- **R1 tokenizer:** chưa biết `gpt-6-luna` có dùng `o200k_base` không. Implementer
  chạy no-cost `tiktoken.encoding_for_model("gpt-6-luna")`. Nếu trả encoding
  khác `o200k_base`, dừng và báo Reviewer (đổi contract). Nếu tiktoken không
  biết model, ghi `not verified` và giữ `o200k_base` làm budget ứng dụng.
- **R2 reasoning tokens vs caps:** nếu model mặc định reasoning, cap 256 của
  Representation B hoặc 2048 của answer có thể bị tiêu hết. Không đổi caps
  trước khi quan sát; nếu live run cho `incomplete`/empty, ghi FAIL thật.
- **R3 SDK support:** Agents SDK 0.19.4 có thể chưa biết model mới; construction
  không gọi mạng phải PASS trong non-paid gate.
- **R4 Foods/evaluation path chưa live-verify:** `backend/evaluation/eval.py` gửi
  `temperature` cho Foods generator. Phase này không chạy Foods evaluation, nên
  compatibility của `temperature` với `gpt-6-luna` là `not live-verified` cho
  tới phase evaluation.
- **R5 judge cùng model với generator:** User chấp nhận. Self-preference bias
  không phụ thuộc vào việc hai lời gọi ở phiên khác nhau; Phase 7B/8 phải ghi
  đây là limitation khi báo kết quả chất lượng.
- **R6 so sánh lịch sử:** benchmark Foods/Phase 7 cũ đo với `gpt-5.4-nano`; chúng
  không mô tả cấu hình mới. Phase 8 so Qwen với `gpt-6-luna`.

## 6. `conditional_evidence` investigation

Case cũ hỏi giá vé Đại Nội và chính sách miễn giảm; `gpt-5.4-nano` trả
`INSUFFICIENT_ANSWER` dù Reviewer probe trước đó thấy 5 sources / 777 tokens có
thông tin vé. Root cause chưa được chứng minh vì artifact cũ không lưu excerpts.

Không sửa prompt/retrieval phòng xa trong phase này. Live run mới lưu
`packed_evidence`. Nếu case này FAIL lần nữa, Implementer đọc artifact private
và báo trong report (không chép excerpts vào tracked file) evidence có chứa giá
vé/miễn giảm hay không, và câu nào trong prompt có thể dẫn tới từ chối. Reviewer
quyết định correction sau đó. Nếu case PASS, ghi "quan sát PASS sau khi đổi
model", không ghi là đã sửa lỗi.

## 7. Verification và Review Contract delta

Non-paid gate của Implementer (phải PASS hết trước paid run):

1. `git diff --check` exit 0; diff chỉ chứa paths ở §4.
2. Hue Qdrant chạy trên 6335 (`docker compose up -d` tại repo root);
   `curl http://localhost:6335/collections` thấy collections hue; Mekong trên
   6333 vẫn chạy.
3. Metadata v2 complete verify `VERIFIED` đủ 33.840 points trên 6335.
4. Focused suite như Check 1 trong implementation report 2026-10-01 PASS.
5. R1 tokenizer check và SDK/generator construction-only check với
   `gpt-6-luna`, `max_retries=0`, `max_turns=1`, không reasoning/sampling field.
6. Uvicorn từ `backend/`, `/health` 200 với 5 components ready, rồi dừng server.
7. Old artifact vẫn là ledger cũ (5 attempts, FAIL, 3 PASS/2 FAIL).
8. Implementer tính `sha256sum` cho đúng 15 files trong fingerprint list của
   handoff, gửi Reviewer.

Reviewer gate trước paid run: đọc exact diff, kiểm guard/test/config, ghi
fingerprint mới vào `CURRENT_HANDOFF.md`, rồi nhắn Implementer `GO`. Không có
`GO` thì không paid run.

Paid authority: đúng **một** invocation runner hiện có, tối đa **5** attempted
calls tới `gpt-6-luna` (1 Representation B + 4 answers), retries 0, không call
thứ sáu, không rerun dù FAIL.

User cấp trước ngày 2026-10-23 đúng một lần chạy bổ sung (tối đa 5 calls) chỉ khi
`conditional_evidence` FAIL, sau khi Reviewer duyệt một focused correction có
root-cause evidence và gửi `GO` mới với fingerprint mới.

Báo cáo bắt buộc: Implementer viết implementation report đầy đủ; Reviewer viết
review report theo `session_prompt/TEMPLATE_CODEX_REVIEW.md` và user report theo
`session_prompt/TEMPLATE_USER_REPORT.md`.

Git: User cấp `commit_and_push` cho Reviewer ngày 2026-10-23, chỉ sau khi User
xác nhận closure Phase 6, phạm vi là các file của amendment này cùng docs/reports
liên quan; không commit private data (`data/`, `knowledge-base-hue/`,
`qdrant_storage/`) hoặc file untracked không liên quan.

Final review dùng verdict và minimum gate của Review Contract 2026-10-01, thay
`gpt-5.4-nano` bằng `gpt-6-luna`.

## 8. Ngoài scope

Git commit/push trước User closure, cleanup Qdrant, Foods evaluation run, Phase 7/8/9, Qwen,
prompt/retrieval tuning, đổi caps, đổi quy trình/skills.
