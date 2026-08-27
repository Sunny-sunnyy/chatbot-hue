# Phase 8 Golden Dataset V3 Design

Date: 2026-08-27
Status: approved_design
Scope: replace the pending Golden Dataset V2 review target with a smaller,
tourist-likelihood-driven Golden Dataset V3 without running the Phase 8 model
benchmark.

## 1. Purpose

Golden Dataset V3 is a Vietnamese, single-turn benchmark for common questions
that tourists are realistically likely to ask while exploring Hue food and
drink.

V3 corrects the central failure mode of V2: the dataset must not be shaped by
an exact 100-row target, exact category quotas, or a source-family-by-category
matrix. Those constraints encouraged repeated templates and technically valid
but unnatural questions. V3 keeps diagnostic labels and exact evidence while
making question quality the gating requirement.

## 2. Approved size rule

The full dataset must contain exactly one of these sizes:

```text
50, 45, or 40 rows
```

The selection order is `50 -> 45 -> 40`:

1. Prefer 50 only when all 50 cases pass the approved quality rubric.
2. Use 45 when a further five cases would introduce weak, repeated, forced, or
   low-likelihood questions.
3. Use 40 when the same problem occurs before 45.

The Implementer proposes the highest defensible size. The Reviewer reads every
case. The user reads every question and decides the final size and content with
the Reviewer. A validator PASS never constitutes quality approval.

## 3. Question contract

Every question must:

- be written in natural Vietnamese with diacritics;
- be clear, common, easy to understand, and plausible for a tourist in Hue;
- stand alone without conversation history;
- contain one primary intent and at most one closely related condition;
- avoid riddles, distant inference, SEO phrasing, promotional phrasing, and
  quota-shaped wording;
- avoid leaking the name of a research website or publisher into the wording;
- be materially distinct from every other question.

Direct questions about location are allowed when they have practical tourist
value. Direct questions whose sole intent is a price or opening time are not
included. Price and opening-time information may instead be added to the
reference answer when it is relevant, useful, current in the corpus, and
supported by evidence.

The same dish or venue may appear more than once only when the intents are
materially different. A sequence that merely replaces the dish or venue name
inside one repeated template is not acceptable.

## 4. Coverage without quotas

The initial source-family lens is approximately:

- restaurants: 20;
- cafes: 10;
- local specialties: 10;
- food guides: 10.

These numbers are authoring orientation only. They are not validator rules,
acceptance criteria, minimums, or targets that must sum to the final size.
Restaurants and cafes may contribute more cases when they support more useful
questions. Local specialties and food guides may contribute fewer when further
questions would be repetitive or forced.

There is no source-family-by-category matrix.

### 4.1 Tourist-needs checklist

The author and reviewers use this qualitative checklist to detect obvious
dataset imbalance:

1. dishes worth trying on a first visit to Hue;
2. breakfast, lunch, afternoon snack, dinner, or late-night food;
3. where to eat, including a useful venue or convenient location;
4. ingredients, flavour, spiciness, texture, and distinguishing features;
5. how a dish is eaten, including accompaniments or dipping sauce;
6. needs such as vegetarian food, families, groups, quiet spaces, or a useful
   cafe experience;
7. simple food choices or an itinerary for one session or one day;
8. food that can be carried or bought as a gift;
9. origins or food culture that an ordinary tourist may realistically ask
   about.

The checklist has no quotas. The dataset need not contain all nine intents when
doing so would reduce quality.

### 4.2 Diagnostic categories

V3 retains the nine V2 category names for reporting and comparison:

```text
direct_fact
temporal
comparative
numerical
relationship
spanning
holistic
food_knowledge
guide_planning
```

There are no category quotas or category minimums. Category is assigned after a
question has been selected for its tourist value. Questions must never be
created or rewritten to fill a missing category.

## 5. Data files and schema

V3 is separate from V2:

```text
knowledge-base-hue/foods/evaluation/golden_v3.jsonl
knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl
```

V2 and the Phase 7 datasets remain unchanged.

Every full row contains exactly six fields:

```json
{
  "case_id": "foods-v3-0001",
  "question": "...",
  "keywords": ["...", "..."],
  "reference_answer": "...",
  "category": "food_knowledge",
  "evidence": {
    "foods/local_specialties/example.md": ["Tóm tắt"]
  }
}
```

IDs are sequential in file order, beginning at `foods-v3-0001` and ending at
the selected dataset size.

### 5.1 Keywords

- Each row has two to four concrete words or phrases.
- Every keyword appears in `reference_answer`, using case-insensitive matching.
- The declared evidence supports the keyword's meaning.
- A keyword need not occur literally in every declared evidence section.
- Keywords support answer evaluation and are not retrieval ground truth.

### 5.2 Reference answers

A reference answer normally uses two to four sentences:

1. answer the primary intent directly;
2. add only useful practical information supported by the evidence.

An answer may include an address, price, opening time, or practical warning
when relevant. It must not copy a long source passage, advertise a venue, or
include facts merely because they are available.

### 5.3 Evidence

`evidence` maps a canonical Markdown source path, relative to
`knowledge-base-hue`, to one or more exact H2 headings in that file.

Evidence is minimal but sufficient:

- normally one source and one section;
- multiple sections or files only when the natural question genuinely requires
  synthesis;
- no multi-source question created merely to obtain `spanning` or `holistic`
  coverage.

Retrieval relevance remains binary and embedding-independent:

```text
document.metadata.source is a key in case.evidence
AND
document.metadata.section is listed under that source
```

The correct source with the wrong section is nonrelevant.

## 6. Web research boundary

The Implementer and Reviewer may use web search to:

- study how tourists naturally ask about Hue food;
- identify common tourist needs;
- check whether corpus information appears current or conflicted;
- discover potentially useful missing knowledge.

Web pages are not direct Golden evidence. Every V3 reference answer and evidence
mapping must remain supported by Markdown that is approved and indexed by the
system.

When useful web information is missing from the corpus, the Implementer must:

1. report the proposed fact and source;
2. propose the exact curated Markdown addition or correction;
3. pause that case for user and Reviewer approval;
4. include the case only after the Markdown is approved and indexed.

No web source is ingested automatically.

## 7. Authoring approach

V3 uses a curate-first approach:

1. Review all 100 V2 cases against the V3 rubric.
2. Keep, rewrite, or reject each candidate.
3. Recheck the question, keywords, reference answer, category, and evidence even
   when a V2 row is copied unchanged.
4. Compare the retained set with the tourist-needs checklist.
5. Add new cases only for meaningful uncovered needs.
6. Do not require a reuse count and do not build a 60- or 70-case pool merely
   to prune it.
7. Build and review the 40-case baseline, then consider exactly five more for
   45 and exactly five more for 50.

The permanent implementation report records only aggregate counts for reused,
rewritten, new, and rejected cases plus material conflicts. V3 does not add an
annotation database, semantic judge, registry, manifest, or audit framework.

## 8. Smoke subset

`golden_v3_smoke.jsonl` contains exactly 10 complete rows copied unchanged from
the user-approved full V3 file.

Selection is intentionally simple: choose a reasonably varied set of strong
cases. Smoke has no category quota, source-family quota, optimization algorithm,
or matrix. It is for quick technical checks only. Official quality decisions
use the full 40-, 45-, or 50-row dataset.

## 9. Deterministic validation

Code validates only properties that can be checked reliably:

- valid JSONL and exactly six fields;
- full size in `{40, 45, 50}`;
- sequential V3 IDs in file order;
- nonempty question and reference answer;
- question uniqueness after basic whitespace/case normalization;
- two to four nonempty keywords present in the reference answer;
- category membership in the approved nine-name set;
- nonempty evidence whose files and declared H2 headings exist;
- smoke size exactly 10, unique IDs, and rows deep-equal to full V3.

The validator does not enforce source counts, category counts, checklist counts,
semantic uniqueness, tourist likelihood, answer length, or naturalness. Those
are manual review decisions.

V2 validation remains available so historical V2 behavior and files are not
silently redefined.

## 10. Human quality gate

For every case, the Reviewer and user verify:

1. a tourist could realistically ask it;
2. it is standalone, clear, and focused;
3. it is not SEO-like, promotional, forced, or template-cloned;
4. it differs materially from other cases;
5. the reference answer is direct, concise, and useful;
6. every answer claim is supported by the declared evidence;
7. the evidence is minimal but sufficient.

Dataset approval additionally requires:

- the highest defensible size among 50, 45, and 40;
- reasonable qualitative variety without quota pressure;
- deterministic validator PASS;
- real retrieval metadata verification on an isolated test collection;
- full user and Reviewer review;
- an exact 10-row smoke subset after full approval.

## 11. Engineering constraints

- Keep code small, direct, readable, and consistent with existing project
  patterns.
- Do not over-engineer or add abstractions beyond the V3 contract.
- Use TDD for validator and test changes.
- Use real corpus data and real services for completion evidence.
- Unit-level error-path tests may construct minimal model values, but they are
  never implementation or completion evidence.
- Do not use fake, mock, replay, or fabricated outputs as implementation or
  completion proof.
- Do not mutate the active Qdrant collection.

## 12. Out of scope

- Phase 8 embedding, tokenizer, sparse, fusion, reranker, generator, or judge
  benchmark runs;
- paid generation or judge calls;
- production model/profile changes;
- active collection mutation;
- automatic ingestion of web discoveries;
- English or bilingual Golden cases;
- refusal evaluation;
- editing or deleting V2 and historical Phase 7 datasets;
- semantic LLM validation, annotation platforms, registries, manifests, or
  generalized audit packages.
