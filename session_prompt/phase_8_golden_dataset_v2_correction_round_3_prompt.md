# Implementer Prompt: Phase 8 Golden Dataset V2 — Consolidated Correction Round 3

> **Historical — superseded 2026-08-27:** V2 correction dừng sau complexity
> reset. Không tiếp tục correction vòng mới; dùng Golden Dataset V3 design/plan
> và `session_prompt/phase_8_golden_dataset_v3_implementer_prompt.md`.

Role: Implementer
Gate: Phase 8 Gate 0
Date: `2026-08-27 +07`
Status: authorized correction only; Gate 1 remains closed

## 1. Read before editing

Read completely:

1. `session_prompt/phase_8_golden_dataset_v2_implementer_prompt.md`
2. `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`
3. `docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md`
4. `reports/phase_8_golden_dataset_v2_codex_review.md`
5. `reports/phase_8_golden_dataset_v2_language_quality_audit.md`
6. `reports/phase_8_golden_dataset_v2_implementation_report.md`
7. every complete Markdown H2 section used or considered as evidence for a
   changed case.

The user-confirmed language/keyword rubric in the language-quality audit is
binding for this correction.

## 2. Objective

Perform one consolidated quality correction over all 100 Golden V2 cases so
that question, keywords, reference answer, category and evidence are:

- natural Vietnamese that a real food/travel user might ask;
- single-intent unless two parts are naturally inseparable;
- concise, transparent and directly grounded in the closed-world corpus;
- annotated with 2–4 semantic keywords, not address strings selected merely for
  easy substring matching;
- still compliant with the exact category quotas, primary-authoring matrix and
  20-row deep-equal smoke contract.

Do not optimize gold labels or wording for the current retrieval model.

Internet research is authorized for the bounded purposes defined in Task F.

## 3. Authorized files

Modify only as needed:

- `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`
- `knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl`
- `reports/phase_8_golden_dataset_v2_implementation_report.md`

Do not modify validator/runtime/tests unless a genuine contract defect blocks
this correction; stop and report that defect instead of changing code silently.

## 4. Required correction work

### Task A — Rewrite or replace the mandatory question-level findings

Review and correct at minimum:

`foods-0008`, `foods-0023`, `foods-0028`, `foods-0039`, `foods-0040`,
`foods-0044`, `foods-0053`, `foods-0054`, `foods-0059`, `foods-0062`,
`foods-0063`, `foods-0072`, `foods-0073`, `foods-0075`, `foods-0080`,
`foods-0083`, `foods-0084`, `foods-0087`, `foods-0090`, `foods-0098`,
`foods-0100`.

Follow the exact issue and suggested direction in
`reports/phase_8_golden_dataset_v2_language_quality_audit.md`.

Mandatory facts to fix include:

- `foods-0028`: the source brand is `Nhà hàng cơm niêu Chạn`, not “Chân”;
- `foods-0098`: remove invented `7:00 – 8:00` and `8:30 – 10:00` times;
- `foods-0063` and `foods-0072`: do not state that all bánh nậm uses bột gạo tẻ;
- `foods-0090`: replace with a genuine `food_knowledge` case instead of changing
  its category and breaking the source/category matrix.

### Task B — Natural-language polish

Review and polish at minimum:

`foods-0027`, `foods-0036`, `foods-0037`, `foods-0042`, `foods-0055`,
`foods-0056`, `foods-0065`, `foods-0067`, `foods-0079`, `foods-0081`,
`foods-0082`, `foods-0085`, `foods-0086`, `foods-0088`, `foods-0089`,
`foods-0092`, `foods-0095`, `foods-0097`.

Remove benchmark/document-centric phrasing such as “theo cẩm nang”, “theo mô
tả trong tài liệu” and formulaic “Tổng quan các…” where a direct user question
is clearer.

### Task C — Perform a complete 100-case keyword pass

Do not limit the audit to the listed examples. Apply the confirmed rubric to all
100 cases.

Rules:

1. Exactly 2–4 keywords; prefer two or three when sufficient.
2. For a specific venue/entity question, include its name when the reference and
   valid evidence support that keyword.
3. For direct address questions, use entity name + main address; ward/landmark
   only when useful.
4. For hours/prices, use entity or branch + exact time/price; omit unrelated
   location tokens.
5. For comparative questions, use compared entities/dishes plus the key
   differentiators.
6. For spanning/holistic/planning, use dish names, venue names or itinerary
   stages; do not use four street addresses as proxies for semantic content.
7. Remove duplicated, overly generic, context-free or sentence-length keywords.
8. Preserve official brand names (`AEON MALL`, `KOI Thé`, `ANH KAFE`) and
   standard units (`VNĐ`, `g`, `ml`). Remove or write out nonessential descriptive
   abbreviations such as `CNN`, `BBQ`, `TTTM`, `TP`.
9. Every keyword must still occur in the reference and in at least one valid
   declared evidence section under the existing validator contract.

The systematic ID groups and examples are listed in section 5 of the language
quality audit. Read and apply that section completely.

### Task D — Complete alternative-evidence correction

Audit all 100 rows again, not only the counterexamples. At minimum fix:

- `foods-0052`: add `foods/food-guides.md :: Theo ngân sách` if it remains a
  valid answer source after rewriting;
- `foods-0062`: include
  `foods/restaurants/banh ep gia di.md :: Món ăn / trải nghiệm` if the rewritten
  origin question is still answered by that section;
- `foods-0090`: recompute evidence from scratch after replacing the case.

List every curated source/H2 section that can provide valid evidence. Do not add
a section merely because it shares words, and do not omit a valid alternative
because it is not the primary authoring source.

### Task E — Preserve contracts

- Keep IDs `foods-0001` through `foods-0100` sequential and questions unique.
- Preserve exact global category quotas and the exact 40/20/20/20 authoring
  matrix. Do not reallocate without stopping for user approval.
- Update every changed smoke row by copying it deep-equal from full. Do not
  change smoke membership unless necessary; if necessary, report the reason and
  coverage before proceeding.
- Preserve Phase 7 `tests.jsonl` and `test2.jsonl` byte-for-byte.
- Keep active Qdrant collection read-only.

### Task F — Authorized internet research and conflict reporting

The Implementer may search the internet for information related to:

- restaurants, food stalls and cafes in Huế;
- beverages and traditional dishes of Huế;
- realistic food, cafe and itinerary needs of travelers visiting Huế;
- names, addresses, opening hours, prices, menus, history, culinary descriptions
  and travel suitability that may help detect ambiguity or conflict in the
  curated corpus.

Research purposes are limited to:

1. checking whether questions and terminology sound natural for real travelers;
2. discovering possible contradictions, ambiguity, stale information or naming
   problems in the curated corpus;
3. collecting evidence for a discussion with Reviewer and user before a corpus
   or ground-truth decision is made.

Research requirements:

- Open and read the actual source page; do not rely on search snippets.
- Prefer official venue pages, official tourism/cultural authorities and other
  primary sources. Use reputable secondary sources only when primary sources
  are unavailable or when an independent comparison is useful.
- Record page title, direct URL, publisher/site, publication/update date when
  available, and research access date.
- For a material conflict, prefer an official primary source or corroborate with
  two independent credible sources. Clearly distinguish observed facts from
  Implementer inference.
- Treat hours, prices, addresses and operating status as time-sensitive. A web
  mismatch does not automatically prove that a dated corpus snapshot is wrong.
- Research may inform natural wording, but external facts must not be copied
  into `reference_answer`, `keywords` or `evidence` unless the user explicitly
  approves a corpus update and the corresponding Markdown source is updated
  through a separately authorized task.
- Web pages are never valid Golden V2 `evidence` keys. Golden V2 remains a
  closed-world benchmark over `knowledge-base-hue/foods/`.

When research finds a contradiction, do not silently choose a side. Report:

```text
affected case IDs
corpus source + exact H2 section + corpus claim
web source links + dates + web claim
whether the difference may be temporal
impact on question/reference/keywords/evidence/category
recommended options and the single decision needed from Reviewer/user
```

The Implementer may pause at a checkpoint and discuss these findings with the
Reviewer and user. This is a valid outcome and must not be described as a failed
implementation.

## 5. Implementation report corrections

Update the existing implementation report with:

- full/smoke paths and counts;
- exact category, authoring-source and smoke coverage;
- honest totals for reused, rewritten and new cases, with the counting rule;
- source conflicts and user-approved reallocations, explicitly `none` when none;
- a concise internet-research section listing queries/topics, consulted sources,
  corroborations, contradictions and unresolved decisions; explicitly `none`
  when no material contradiction is found;
- validator and pytest commands with exact observed outcomes;
- isolated metadata/relevance test outcome and cleanup result;
- exact command or stable script path for any optional Hit/MRR/NDCG claims;
- the remaining retrieval-miss case ID when Hit@5 is below 100%;
- explicit statements that Phase 7 files and active collection were not mutated
  and that no fake output/source was used.

If an optional metric cannot be reproduced by an exact command, remove that
claim rather than describe an unnamed one-off script.

## 6. Verification

From `backend/`, run at minimum:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-correction-r3-uv-cache \
  uv run python -m evaluation.golden_dataset

HF_HUB_OFFLINE=1 \
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-correction-r3-uv-cache \
  uv run --env-file ../.env python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v2 and not binary_relevance'

HF_HUB_OFFLINE=1 \
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-correction-r3-uv-cache \
  uv run --env-file ../.env python -m pytest \
  tests/test_evaluation.py::test_golden_v2_binary_relevance_uses_real_retrieval_metadata \
  -q --tb=short -s
```

Also run from repo root:

```bash
git diff --check
git diff -- knowledge-base-hue/foods/evaluation/tests.jsonl \
  knowledge-base-hue/foods/evaluation/test2.jsonl
git status --short
```

The structural validator passing does not replace the required manual 100-case
language, semantic and alternative-evidence audit.

## 7. Stop conditions and prohibited work

Stop and ask the user if a natural grounded case cannot satisfy an exact matrix
cell, or if internet research exposes a material conflict that changes the
ground truth. Do not force an unnatural question, silently move the quota or
silently resolve a source conflict.

Do not:

- import external-web facts into question/reference/keywords/evidence without a
  separate explicit user decision and an authorized corpus update;
- use fake, mock, replay or fabricated output as completion evidence;
- weaken validator rules;
- add semantic validators, audit frameworks, manifests or generated packages;
- run paid generation/judging or Phase 8 model comparisons;
- mutate the active collection;
- change production settings, stage, commit or push;
- declare Gate 0 approved.

## 8. Handoff

Return one concise correction report containing:

1. exact changed files;
2. all rewritten/replaced case IDs and keyword-pass count;
3. any source conflicts, unresolved cases or approved decisions;
4. internet research performed, direct source links, dates, findings and any
   discussion required from Reviewer/user;
5. exact validation/test commands and real outcomes;
6. smoke deep-equality and isolated cleanup evidence;
7. Phase 7/active-collection/no-fake confirmations;
8. a request for Codex Reviewer to re-run Gate 0 review.

Gate 0 remains `changes_requested` until Reviewer and user explicitly approve it.
