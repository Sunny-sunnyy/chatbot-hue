# Phase 7 Simple Evaluation Design

**Status:** Approved by the user on 2026-08-23.

## 1. Purpose

Phase 7 will be redesigned around one understandable RAG evaluation flow:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

The first design must be simple enough for a person to read and explain. Its
starting level of complexity should be comparable to:

- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py`
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation`

These are direct design and coding-style references for Phase 7 evaluation.
Phase 7 must reuse the current Hue RAG backend instead of copying a second RAG
implementation into the repository. They are not implementation blueprints for
unrelated backend phases.

Later phases may research, optimize, or introduce a more advanced technique when
there is a demonstrated need. An advanced technique must still be explained
clearly, verified with the real system, and removed when its complexity exceeds
its practical value.

This specification supersedes the earlier over-engineered Phase 7 evaluation
architecture and its calibration, artifact, cost, identity, and resume workflows.

## 2. Phase 7 file structure

The intended evaluation package is deliberately small:

```text
backend/evaluation/
|-- __init__.py
|-- test.py
|-- template.py
|-- eval.py
`-- evaluator.py

backend/tests/
`-- test_evaluation.py

knowledge-base-hue/foods/evaluation/
|-- test2.jsonl
`-- tests.jsonl

notebooks/
`-- 07_evaluation.ipynb
```

Responsibilities:

- `test.py` loads evaluation questions from a path supplied by the caller.
- `template.py` contains all prompts owned by the evaluation feature. It must
  not duplicate the production generation prompt already owned by the main
  backend.
- `eval.py` contains retrieval evaluation, answer evaluation, metric
  calculation, batch execution, and simple CSV reporting.
- `evaluator.py` contains the Gradio interface and combines the useful,
  understandable behavior of the old `evaluator.py` and `evaluator2.py`.
- `test_evaluation.py` is the only Phase 7 code test file.

Do not split this feature into calibration, generation, judge, artifact, cost,
identity, summary, or validator modules.

## 3. Test data

The first live evaluation uses `test2.jsonl` containing 20 real questions copied
from the existing 104-question dataset. The selection should be distributed
reasonably across the eight existing content categories.

The loader needs only the fields used by the simple evaluation:

- `question`
- `category`
- `reference_answer`
- `keywords`

After the 20-question run is stable, running the full evaluation requires only
changing the input path to the existing 104-question `tests.jsonl` file.

## 4. Retrieval evaluation

The initial Phase 7 implementation evaluates only `dense_only`.

For each question:

1. Call the current backend retrieval service.
2. Keep the returned chunks in retrieval order.
3. Search for each expected keyword directly in the retrieved chunk text,
   case-insensitively.
4. Calculate MRR, nDCG, the number of keywords found, and keyword coverage.
5. Return a human-readable result row.

MRR and nDCG are keyword-based. They do not depend on a gold file path, source,
section, artifact identity, or package relationship.

The results are displayed in the UI and overwrite one fixed file:

```text
retrieval_results.csv
```

The main columns are:

```text
category, question, keywords, mrr, ndcg,
keywords_found, total_keywords, keyword_coverage, error
```

`eval.py` may accept a straightforward argument such as
`profile="dense_only"`. It must not pre-build profile comparison machinery.
After the baseline is stable, the same evaluation may be run for:

- `dense_only`
- `hybrid_no_rerank`
- `hybrid_rerank`

## 5. Answer evaluation

For each question:

1. Use the current backend with the `dense_only` profile.
2. Retrieve relevant chunks and build the context through the current backend.
3. Generate the answer with `gpt-5.4-nano` through the production generation
   path.
4. Ask `gpt-5.4-mini` to compare the generated answer with the reference answer.
5. Return three scores from 1 to 5 and concise feedback.

The three scores are:

- `accuracy`
- `completeness`
- `relevance`

There is no groundedness score, calibration stage, judge gate, or reusable judge
package.

The results are displayed in the UI and overwrite one fixed file:

```text
answer_results.csv
```

The main columns are:

```text
category, question, reference_answer, generated_answer,
accuracy, completeness, relevance, feedback, error
```

If one provider call fails, record a plain error for that question and continue
with the remaining questions. Do not add automatic retry, resume, partial
artifact, or recovery orchestration.

## 6. User interface

`evaluator.py` provides one simple Gradio interface with:

- a test-file path, defaulting to `test2.jsonl`;
- one control named `Số câu chạy cùng lúc`, defaulting to `3`;
- a button named `Đánh giá retrieval`;
- a button named `Đánh giá câu trả lời`;
- visible progress;
- a detailed result table;
- a small average-score summary;
- the path of the CSV file that was written.

The two evaluation buttons work independently. Concurrent work may finish in a
different order, but the displayed and saved rows must follow the question order
from the input file.

A button press is allowed to execute real paid API calls directly. There is no
extra consent dialog, CLI confirmation flag, cost cap, or cost estimation code.

## 7. Minimal tests

Keep only `backend/tests/test_evaluation.py`, with approximately six to eight
clear checks:

1. `test2.jsonl` loads exactly 20 real questions.
2. Every question contains the required fields.
3. MRR calculation is correct.
4. nDCG calculation is correct.
5. Retrieval evaluation returns the columns used by the UI.
6. Answer evaluation returns exactly three scores and feedback.
7. Generator/yield values match the Gradio outputs.
8. `load_tests(path)` uses the supplied path.

The metric checks must use real project questions or knowledge-base content, not
invented identifiers or fake artifacts. The test suite is not evidence that the
provider integration works; real provider execution supplies that evidence.

Do not target a test count, retain technical tests for removed mechanisms, or
create additional Phase 7 test files without a concrete user-facing need.

## 8. Notebook 07

Rewrite `notebooks/07_evaluation.ipynb` as a short, sequential learning document:

1. Explain Phase 7 in ordinary language.
2. Import the small evaluation API.
3. Load `test2.jsonl`.
4. Show one real question.
5. Run retrieval for that question.
6. Explain and display keyword-based MRR and nDCG.
7. Run answer evaluation for that question.
8. Display accuracy, completeness, relevance, and feedback.
9. Run the 20-question set.
10. Display the summary.
11. Optionally launch the same Gradio interface.

Each cell should do one thing. Explanatory Markdown should appear immediately
before short code cells. The notebook must call readable backend functions rather
than reproduce implementation logic.

Use these notebook directories as required style references:

- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`
- `/home/minhhieu/llm_rag/tai_lieu/notebook_simple`

Do not put artifact discovery, checksum comparison, package matching, audit
contracts, or a test suite inside the notebook.

## 9. Real-system verification policy

The following policy applies to the entire Hue RAG system, all completed phases,
and all future phases, not only Phase 7:

- Use real project data.
- Use the real backend path, database, services, models, and APIs.
- The implementer and reviewer may access online services.
- The implementer and reviewer may make the user-approved paid OpenAI calls.
- Do not use fake IDs, fake artifacts, fake datasets, fake providers, mocked
  provider responses, or fabricated results as completion evidence.
- A local code test does not replace a live integration run.
- Completion evidence must come from the real production path or a real small
  data run through that same path.

The Phase 7 verification order is:

1. Run the small code test file.
2. Run retrieval evaluation on the 20 real questions.
3. Run real generation and real judging on the 20 real questions.
4. Inspect the UI and the two real CSV files.
5. After the small run is stable, change the path and run the 104 real questions.

## 10. Whole-project simplicity policy

Code across the whole project must be easy to understand, simple, clear, and no
more technical than the demonstrated requirement needs.

The initial Phase 7 evaluation design should begin at the level demonstrated by:

- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py`
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation`

Phase 0 through Phase 6 will use separate, phase-appropriate reference material
provided by the user. Those phases should not copy the Phase 7 references merely
to satisfy a general style rule.

The whole project inherits the general principles of readable code, simple data
flow, minimal necessary structure, and real-system verification. This is not a
permanent ban on advanced techniques. Implementers may research and optimize when
a real requirement, measured problem, or verified limitation justifies it. The
reviewer must then ask:

1. What real problem does this solve?
2. Is there a simpler solution?
3. Can a person understand the code and its data flow?
4. Did a real-system run demonstrate the benefit?
5. Is the added complexity proportionate to that benefit?

If those questions cannot be answered clearly, the advanced technique is
over-engineering and must be removed.

Across existing and future phases, remove unnecessary instances of:

- cost accounting and cost-estimation code;
- consent gates for API use already approved by the user;
- calibration;
- resume workflows;
- run identity and generation run identity;
- timestamps used to manage evaluation packages;
- checksums;
- package matching;
- tamper detection;
- partial artifacts and artifact-audit machinery;
- layered validators;
- technical tests that exist only to support removed machinery.

Do not rename or relocate an unnecessary mechanism to preserve it. Keep a more
advanced mechanism only when it supports a concrete runtime requirement, can be
explained plainly, and survives the proportionality review above.

## 11. Review gate before Phase 8

Phase 8 must not begin immediately after the new Phase 7 is complete. First,
review Phase 6 back through Phase 0.

For each phase:

1. The user provides the relevant simple reference material.
2. Compare the current code, folders, tests, and notebook with that material.
3. Identify unnecessary files, validators, abstractions, tests, and technical
   workflows.
4. Propose a simpler phase design for user approval.
5. Rebuild the necessary code and notebook.
6. Verify the phase through the real system with real data and online services
   where applicable.
7. Continue only when the code and notebook are understandable and the user has
   accepted the result.

All notebooks from Phase 0 through Phase 6 must also be rewritten where needed,
using these style references:

- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`
- `/home/minhhieu/llm_rag/tai_lieu/notebook_simple`

## 12. Project documentation changes

The implementation must update at least:

- `session_prompt/REVIEWER_WORKFLOW.md`
- `session_prompt/IMPLEMENTER_WORKFLOW.md`
- `session_prompt/Session_Prompt.md`
- `session_prompt/Project_Status.md`

It must also update relevant guides, README files, reports, and templates that
still prescribe the rejected Phase 7 architecture or conflict with this policy.

The documents must state plainly that:

- code must be understandable, simple, clear, and not over-engineered or more
  technical than necessary;
- Phase 7 evaluation should use the two full-path code references above;
- Phase 0 through Phase 6 should use the separate reference material supplied by
  the user for each phase;
- notebook design should use the two full-path notebook directories above;
- implementers and reviewers may run real online services and approved paid APIs;
- fake execution and fake evidence are prohibited across the entire system;
- tests should protect necessary behavior instead of maximizing test count;
- unnecessary cost accounting, consent, calibration, resume, identity,
  timestamp, checksum, package-matching, and tamper-detection machinery must be
  removed;
- advanced research and optimization remain allowed when a real need is shown,
  the benefit is verified, and the implementation is not over-engineered.

`Project_Status.md` must record the Phase 7 reset and the Phase 0-6 simplicity
review as a mandatory gate before Phase 8.

## 13. Acceptance criteria

The redesign is complete only when:

- the Phase 7 package follows the small approved file structure;
- `test2.jsonl` contains 20 real, reasonably distributed questions;
- both UI buttons run the real backend;
- the real 20-question retrieval and answer evaluations complete;
- the two fixed CSV files contain real results;
- the single small Phase 7 test file passes;
- Notebook 07 is short, sequential, and understandable;
- the rejected Phase 7 machinery and its unnecessary tests are removed;
- the required project documents reflect the whole-project simplicity and
  real-verification policy;
- no fake execution or fabricated evidence is used;
- the Phase 0-6 review gate is recorded before Phase 8.
