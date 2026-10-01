# Paid execution handoff — Full-corpus Phase 6 OpenAI baseline

Target role: implementer
Authored by: reviewer
Handoff kind: paid_execution
State: authorized_pending_execution
Authorization granted by User: 2026-10-01 (+07)
Execution timing: next User-initiated session; do not execute in the current Reviewer session
Base commit: d0494072ae335f1e3f2492ed3be30a3ed42acb8b
Head commit: Phase 6 authorized commit on `main`; resolve with `git rev-parse HEAD`
Risk level: high
Git authorization: none
Sub-agent authorization: none
Paid-call authorization: exactly one bounded invocation, maximum 5 attempted calls

User đã xác nhận explicit authority cho đúng replacement sequence ở mục 3,
nhưng yêu cầu dừng tối nay và tiếp tục vào phiên ngày mai. Authority này đã
được ghi nhận; không cần xin lại nếu approval fingerprint và mọi preflight ở
mục 2 vẫn khớp. Không agent nào được chạy command trước khi User mở phiên tiếp
theo và giao đúng handoff này cho Implementer.

## 1. Context routing cho phiên Implementer tiếp theo

- `full-read`: `session_prompt/IMPLEMENTER_WORKFLOW.md`
- `full-read`: `session_prompt/Session_Prompt.md`
- `full-read`: `session_prompt/Project_Status.md`
- `full-read`: `session_prompt/CURRENT_HANDOFF.md`
- `full-read`: `reports/full_corpus_phase_6_openai_baseline_correction_4_codex_review_2026_10_01.md`
- `targeted-read`: `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md` — Correction 4, prior five-call ledger và handoff sections
- `full-read`: `handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md`
- `targeted-read`: `docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md` — Global constraints, Task 6 và live runner acceptance
- `reference-only`: `data/full_corpus_phase_6_live_smoke.json` — old 3 PASS/2 FAIL artifact sẽ bị replacement run thay atomically

Exact next action: chỉ preflight fingerprint/state rồi chạy đúng một paid
invocation ở mục 3. Không sửa code, config, cases, dependencies hoặc prompts.

## 2. Mandatory no-cost preflight và stop conditions

Từ repository root, chạy đúng hash check sau:

```bash
sha256sum \
  data/full_corpus_phase_6_live_cases.json \
  backend/llm/phase6_live_smoke.py \
  backend/llm/evidence_recorder.py \
  backend/llm/generator_openai_full_corpus.py \
  backend/llm/full_corpus_prompt.py \
  backend/llm/openai_tokenizer.py \
  backend/llm/representation_b.py \
  backend/api/app.py \
  backend/api/routes/chat.py \
  backend/retrieval/full_corpus_context.py \
  backend/llm/citations.py \
  backend/config/settings.yaml \
  backend/core/settings_loader.py \
  pyproject.toml \
  uv.lock
```

Expected approval fingerprint:

```text
8eae4b39b1b52b45e6fc101c563a39325e3e115323d134a24549a970df6a6542  data/full_corpus_phase_6_live_cases.json
b503daf929cce3101eadf8152d4319030c2d0a333f213701a843ab5656047b64  backend/llm/phase6_live_smoke.py
4111af729e0b12da9a68747f2d4fceadcbb02a292dcecf53787e4b70ace862e2  backend/llm/evidence_recorder.py
798f70baac119ecde497a90e670e0d0034dec554979708eb0bb58c4eb56b2510  backend/llm/generator_openai_full_corpus.py
3ca145b82fa308663ff52bc78fbf033b9fb267172178588f3bed00046b4cfd39  backend/llm/full_corpus_prompt.py
7a486fc5266854fdb8f3d7d29de0dc80956969fb03f910a92d0095125d638b4e  backend/llm/openai_tokenizer.py
e323a504acd43982d33cd2558825079c783b323fee7f0693c4a8b2275c8feaec  backend/llm/representation_b.py
de78c742dd04d00d7fec9c1c1214a638ebcb74e1957adb95333598fca10fbe19  backend/api/app.py
13670088d25a46ee1806d6925e16de439d2712395bd37bf107814c5d1ea8f30d  backend/api/routes/chat.py
c71b2191d530dd5bc450923a6c065cf4eb02008e83050274d56bca50225f616b  backend/retrieval/full_corpus_context.py
abaee46b3b51780fb2067e0c686190de279ecfa12f4652843b1cd360a6f861a5  backend/llm/citations.py
3df1faf34f6664659c2c2e41f0e8669e2575b70d08f7b591c2a8e6dcb81c5bb7  backend/config/settings.yaml
0dd6040a906575c066c626eec0bd8d8d40aa77c1c7725e9a486366821a82279d  backend/core/settings_loader.py
c87a66fd34c36c67c3a90328828d94dd0489cb0204cef2acdfc9524d5fb9ace9  pyproject.toml
61e77b5a50c30e55728eaa1ede1dc7bb89789e11cf99d20c3b4ab1fea75ba984  uv.lock
```

Sau đó chỉ chạy các no-cost checks:

1. `git diff --check` phải exit 0.
2. Metadata v2 complete verify phải `VERIFIED` đủ 33.840 points.
3. `OPENAI_API_KEY` phải tồn tại trong environment nhưng không được in/log.
4. Không có process paid runner khác đang chạy.
5. Old artifact phải vẫn là ledger 5 attempts, overall FAIL, 3 PASS/2 FAIL.

Stop ngay, không paid call nếu hash lệch, code/config/cases thay đổi, verify
không đạt, key thiếu, artifact không đúng old ledger, hoặc có runner khác. Ghi
handoff về Reviewer với observed mismatch; không tự sửa để tiếp tục.

## 3. Exact authorized paid invocation

Chỉ khi mục 2 đạt toàn bộ, chạy đúng một lần:

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-openai-live-uv-cache \
  uv run --env-file ../.env python -m llm.phase6_live_smoke \
  --cases ../data/full_corpus_phase_6_live_cases.json \
  --output ../data/full_corpus_phase_6_live_smoke.json \
  --confirm-paid
```

Authorized scope:

- đúng một invocation, tối đa 5 attempted OpenAI calls tới `gpt-5.4-nano`;
- call 1 Representation B, calls 2–5 bốn answer cases exact schema/order;
- mọi attempted request đều tính kể cả failure;
- retries 0, max_turns 1, timeout 45 giây, caps 256/2048;
- không model fallback, không call thứ sáu, không rerun dù partial/FAIL/exception;
- Qdrant/Metadata v2/private corpus read-only;
- không commit/push và không sửa code/config/cases trước hoặc sau run.

SDK không cung cấp exact cost accounting; cost boundary là số attempted calls
và caps phía trên.

## 4. Required post-run evidence và handoff

Sau invocation, dù PASS hay FAIL:

1. Không chạy lại.
2. Xác nhận artifact parse được, `call_attempt_count <= 5`, Qdrant before/after
   được ghi truthful và không có secret/raw provider exception.
3. Cập nhật implementation report bằng observed command exit/status, attempt
   count và summary an toàn; không chép private query/answer/excerpts vào tracked
   report.
4. Chuyển `CURRENT_HANDOFF.md` về Reviewer với `Handoff kind: final_review`,
   `Paid-call authorization: consumed`, exact artifact pointer và mọi
   limitation/failure.
5. Reviewer sau đó audit artifact; Implementer không tự tuyên bố Phase 6 PASS.

## 5. Resume prompt cho ngày mai

Gửi Implementer đúng bốn bootstrap files và nói:

> User đã cấp authority ngày 2026-10-01 cho đúng một bounded replacement
> five-call invocation, execution được hoãn sang phiên hôm nay. Hãy thực hiện
> `CURRENT_HANDOFF.md` theo thứ tự preflight → một invocation → post-run
> handoff; không retry hoặc call thứ sáu.
