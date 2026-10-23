# Phase 7A Golden Full-corpus Implementation Plan

> **For agentic workers:** Dự án này thực thi qua `session_prompt/CURRENT_HANDOFF.md`
> (Implementer session), không tự chạy hết plan. Mỗi gate dừng chờ Reviewer/User.
> Steps dùng checkbox (`- [ ]`).

**Goal:** Tạo bộ Golden full-corpus khoảng 175 câu tự nhiên, kiểm chứng được, cùng smoke 10 câu, theo spec Phase 7A.

**Architecture:** Một module Python nhỏ, không gọi mạng (`backend/evaluation/golden_full_corpus.py`), kiểm tra và gộp các file JSONL authoring. Câu hỏi do Implementer (và sub-agent ở Task 3) viết sau khi đọc curated Markdown. Reviewer đối chiếu 100% case, User đọc pilot và mẫu.

**Tech Stack:** Python 3 qua `uv`, stdlib `json`/`unicodedata`/`argparse`, pytest; corpus discovery có sẵn `ingestion.source_state.discover_full_corpus_files`.

**Spec:** `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` (User-approved 2026-10-23)

**Status:** Plan và Review Contract User-approved 2026-10-23. Execution chỉ qua `CURRENT_HANDOFF.md`.

## Global Constraints

- Schema chính thức đúng 4 field: `question`, `keywords`, `reference_answer`, `category`.
- File authoring thêm đúng 2 field: `partition`, `sources`; cả hai bị loại khi merge.
- Category ∈ {`direct_fact`, `multi_source`, `comparative`, `conditional`, `out_of_scope`}.
- Partition và thứ tự merge: `foods`, `heritages`, `festivals`, `performing_arts`, `travel_places`, `travel_services`, `travel_tickets`.
- Keyword xuất hiện nguyên văn (NFC, phân biệt dấu và hoa thường) trong curated corpus 205 file do `discover_full_corpus_files()` trả về.
- Case không phải `out_of_scope` có ≥1 keyword không nằm trong `question` và nằm trong `reference_answer` (so sánh casefold).
- `out_of_scope`: `keywords == []`, `sources == []`, `reference_answer ==` `INSUFFICIENT_ANSWER` trong `backend/llm/full_corpus_prompt.py`.
- Quy mô khoảng 175 (±20% mỗi category), mỗi partition ≥10 case; không ép đủ số bằng câu gượng.
- Chỉ câu có một đáp án khách quan; không câu xin lời khuyên hoặc phụ thuộc sở thích.
- Không gọi API có phí; không sửa curated Markdown, retrieval, generation, Qdrant.
- `knowledge-base-hue/` là private: không commit; tracked report không chép câu hỏi, đáp án hay excerpt.
- Chạy Python bằng `uv run` từ `backend/`.

## File Structure

| Path | Trách nhiệm | Tracked |
|---|---|---|
| `backend/evaluation/golden_full_corpus.py` | Kiểm tra case/file, gộp authoring, tạo smoke, CLI | có |
| `backend/tests/test_golden_full_corpus.py` | Test logic thuần của module | có |
| `knowledge-base-hue/meta/golden-full-corpus-writing-guide.md` | Hướng dẫn viết có ví dụ tốt/xấu thật (sau pilot) | private |
| `knowledge-base-hue/<dir>/evaluation/golden_full_corpus_authoring.jsonl` | File authoring mỗi partition | private |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | File chính thức | private |
| `knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl` | Smoke 10 | private |
| `knowledge-base-hue/evaluation/phase_7a_review_notes.md` | Ghi chú review và mẫu cho User (Reviewer viết) | private |
| `reports/phase_7a_golden_*_2026_*.md` | Implementation/review reports | có |

`<dir>` theo partition: `foods`, `heritages`, `festivals`, `performing_arts`,
`travel/places`, `travel/services`, `travel/tickets`.

---

### Task 1: Module kiểm tra và gộp Golden

**Files:**
- Create: `backend/evaluation/golden_full_corpus.py`
- Test: `backend/tests/test_golden_full_corpus.py`

**Interfaces:**
- Consumes: `ingestion.source_state.discover_full_corpus_files() -> (Path, list[str])`, `ingestion.source_state.read_source_lf(path) -> str`, `llm.full_corpus_prompt.INSUFFICIENT_ANSWER: str`
- Produces:
  - `CATEGORIES: tuple[str, ...]`, `PARTITION_DIRS: dict[str, str]`
  - `load_corpus() -> tuple[Path, dict[str, str]]` (kb root, rel path → NFC text)
  - `check_case(row: dict, corpus: dict[str, str], authoring: bool) -> list[str]`
  - `check_file(path: Path, corpus: dict[str, str], authoring: bool) -> tuple[list[str], list[dict]]`
  - `merge_authoring(kb_root: Path) -> list[dict]`
  - `select_smoke(lines: list[str], line_numbers: list[int]) -> list[str]`
  - CLI `python -m evaluation.golden_full_corpus {check PATH [--authoring] | merge | smoke N1 … N10}`

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path

import json
import pytest

from evaluation.golden_full_corpus import (
    check_case,
    check_file,
    merge_authoring,
    select_smoke,
)
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

CORPUS = {
    "heritages/heritage/a.md": "# Lăng Tự Đức\nVé tham quan lăng Tự Đức là 150.000 đồng.",
}


def authoring_row(**changes):
    row = {
        "question": "Vé vào lăng Tự Đức giá bao nhiêu?",
        "keywords": ["150.000 đồng", "Tự Đức"],
        "reference_answer": "Vé tham quan lăng Tự Đức là 150.000 đồng.",
        "category": "direct_fact",
        "partition": "heritages",
        "sources": ["heritages/heritage/a.md"],
    }
    row.update(changes)
    return row


def test_valid_authoring_case_passes():
    assert check_case(authoring_row(), CORPUS, authoring=True) == []


def test_official_file_rejects_authoring_fields():
    errors = check_case(authoring_row(), CORPUS, authoring=False)
    assert errors and "fields must be" in errors[0]


def test_keyword_must_be_verbatim_in_corpus():
    errors = check_case(authoring_row(keywords=["200.000 đồng", "Tự Đức"]), CORPUS, authoring=True)
    assert any("not verbatim in corpus" in e for e in errors)


def test_requires_answer_keyword_absent_from_question():
    row = authoring_row(keywords=["Tự Đức"])
    errors = check_case(row, CORPUS, authoring=True)
    assert any("answer keyword" in e for e in errors)


def test_out_of_scope_rules():
    good = authoring_row(
        question="Giá vé vào Văn Miếu Hà Nội là bao nhiêu?",
        keywords=[],
        reference_answer=INSUFFICIENT_ANSWER,
        category="out_of_scope",
        sources=[],
    )
    assert check_case(good, CORPUS, authoring=True) == []
    bad = dict(good, reference_answer="Không biết.")
    assert any("INSUFFICIENT_ANSWER" in e for e in check_case(bad, CORPUS, authoring=True))


def test_check_file_reports_line_and_duplicates(tmp_path: Path):
    path = tmp_path / "golden.jsonl"
    line = json.dumps(authoring_row(), ensure_ascii=False)
    path.write_text(line + "\n" + line + "\n{bad json\n", encoding="utf-8")
    errors, rows = check_file(path, CORPUS, authoring=True)
    assert len(rows) == 2
    assert any(e.startswith("line 3:") for e in errors)
    assert any("duplicate question" in e for e in errors)


def test_merge_strips_authoring_fields_in_partition_order(tmp_path: Path):
    for partition, rel_dir in (("foods", "foods"), ("heritages", "heritages")):
        folder = tmp_path / rel_dir / "evaluation"
        folder.mkdir(parents=True)
        row = authoring_row(partition=partition, question=f"Câu của {partition}?")
        (folder / "golden_full_corpus_authoring.jsonl").write_text(
            json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    merged = merge_authoring(tmp_path)
    assert [r["question"] for r in merged] == ["Câu của foods?", "Câu của heritages?"]
    assert all(set(r) == {"question", "keywords", "reference_answer", "category"} for r in merged)


def test_select_smoke_copies_exact_lines():
    lines = [f'{{"n": {i}}}' for i in range(1, 21)]
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    assert select_smoke(lines, numbers) == [lines[n - 1] for n in numbers]
    with pytest.raises(ValueError):
        select_smoke(lines, [1, 1, 3, 5, 7, 9, 11, 13, 15, 17])
```

- [ ] **Step 2: Run tests to verify they fail**

Run (từ `backend/`): `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q`
Expected: FAIL / collection error `ModuleNotFoundError: No module named 'evaluation.golden_full_corpus'`

- [ ] **Step 3: Write the implementation**

```python
"""Phase 7A Golden full-corpus: kiểm tra và gộp file câu hỏi. Không gọi mạng."""

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from ingestion.source_state import discover_full_corpus_files, read_source_lf
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

CATEGORIES = ("direct_fact", "multi_source", "comparative", "conditional", "out_of_scope")
# Thứ tự khóa cũng là thứ tự ghép file chính thức.
PARTITION_DIRS = {
    "foods": "foods",
    "heritages": "heritages",
    "festivals": "festivals",
    "performing_arts": "performing_arts",
    "travel_places": "travel/places",
    "travel_services": "travel/services",
    "travel_tickets": "travel/tickets",
}
OFFICIAL_FIELDS = ("question", "keywords", "reference_answer", "category")
AUTHORING_FIELDS = OFFICIAL_FIELDS + ("partition", "sources")
AUTHORING_NAME = "golden_full_corpus_authoring.jsonl"
OFFICIAL_NAME = "golden_full_corpus.jsonl"
SMOKE_NAME = "golden_full_corpus_smoke.jsonl"
SMOKE_SIZE = 10


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def load_corpus() -> tuple[Path, dict[str, str]]:
    root, rel_paths = discover_full_corpus_files()
    return root, {rel: nfc(read_source_lf(root / rel)) for rel in rel_paths}


def check_case(row: dict, corpus: dict[str, str], authoring: bool) -> list[str]:
    expected = AUTHORING_FIELDS if authoring else OFFICIAL_FIELDS
    if set(row) != set(expected):
        return [f"fields must be {sorted(expected)}, got {sorted(row)}"]

    errors = []
    question, keywords, answer, category = (row[name] for name in OFFICIAL_FIELDS)
    if not isinstance(question, str) or not question.strip():
        errors.append("question must be a non-empty string")
    if not isinstance(answer, str) or not answer.strip():
        errors.append("reference_answer must be a non-empty string")
    if not isinstance(keywords, list) or not all(isinstance(k, str) and k.strip() for k in keywords):
        errors.append("keywords must be a list of non-empty strings")
    if category not in CATEGORIES:
        errors.append(f"unknown category {category!r}")
    sources = row.get("sources", [])
    if authoring:
        if row["partition"] not in PARTITION_DIRS:
            errors.append(f"unknown partition {row['partition']!r}")
        if not isinstance(sources, list):
            errors.append("sources must be a list")
        else:
            errors += [f"source not in curated corpus: {s}" for s in sources if s not in corpus]
    if errors:
        return errors

    if category == "out_of_scope":
        if keywords:
            errors.append("out_of_scope keywords must be []")
        if answer != INSUFFICIENT_ANSWER:
            errors.append("out_of_scope reference_answer must equal INSUFFICIENT_ANSWER")
        if authoring and sources:
            errors.append("out_of_scope sources must be []")
        return errors

    if not keywords:
        errors.append("keywords must not be empty")
    if authoring and not sources:
        errors.append("sources must not be empty")
    for keyword in keywords:
        if not any(nfc(keyword) in text for text in corpus.values()):
            errors.append(f"keyword not verbatim in corpus: {keyword!r}")
    folded_question, folded_answer = nfc(question).casefold(), nfc(answer).casefold()
    if not any(
        nfc(k).casefold() not in folded_question and nfc(k).casefold() in folded_answer
        for k in keywords
    ):
        errors.append("needs >=1 answer keyword: absent from question, present in reference_answer")
    return errors


def check_file(path: Path, corpus: dict[str, str], authoring: bool) -> tuple[list[str], list[dict]]:
    errors, rows = [], []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {number}: must be a JSON object")
            continue
        errors += [f"line {number}: {e}" for e in check_case(row, corpus, authoring)]
        rows.append(row)
    counts = Counter(nfc(str(r.get("question", ""))) for r in rows)
    errors += [f"duplicate question: {q!r}" for q, n in counts.items() if n > 1]
    return errors, rows


def merge_authoring(kb_root: Path) -> list[dict]:
    merged = []
    for partition, rel_dir in PARTITION_DIRS.items():
        path = kb_root / rel_dir / "evaluation" / AUTHORING_NAME
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            row = json.loads(line)
            if row["partition"] != partition:
                raise ValueError(f"{path} line {number}: partition {row['partition']!r} != {partition!r}")
            merged.append({name: row[name] for name in OFFICIAL_FIELDS})
    return merged


def select_smoke(lines: list[str], line_numbers: list[int]) -> list[str]:
    if len(line_numbers) != SMOKE_SIZE or len(set(line_numbers)) != SMOKE_SIZE:
        raise ValueError(f"smoke needs exactly {SMOKE_SIZE} distinct line numbers")
    if not all(1 <= n <= len(lines) for n in line_numbers):
        raise ValueError("smoke line number out of range")
    return [lines[n - 1] for n in line_numbers]


def print_distribution(rows: list[dict]) -> None:
    print("category:", dict(Counter(r.get("category") for r in rows)))
    if any("partition" in r for r in rows):
        print("partition:", dict(Counter(r.get("partition") for r in rows)))
    print("total:", len(rows))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evaluation.golden_full_corpus")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check")
    check.add_argument("path", type=Path)
    check.add_argument("--authoring", action="store_true")
    commands.add_parser("merge")
    smoke = commands.add_parser("smoke")
    smoke.add_argument("line_numbers", type=int, nargs="+")
    args = parser.parse_args(argv)

    kb_root, corpus = load_corpus()
    official = kb_root / "evaluation" / OFFICIAL_NAME

    if args.command == "check":
        errors, rows = check_file(args.path, corpus, args.authoring)
        print_distribution(rows)
    elif args.command == "merge":
        errors = []
        for rel_dir in PARTITION_DIRS.values():
            path = kb_root / rel_dir / "evaluation" / AUTHORING_NAME
            if path.is_file():
                errors += [f"{path.name} ({rel_dir}): {e}" for e in check_file(path, corpus, True)[0]]
        if not errors:
            merged = merge_authoring(kb_root)
            official.parent.mkdir(parents=True, exist_ok=True)
            official.write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8"
            )
            errors, rows = check_file(official, corpus, authoring=False)
            print_distribution(rows)
    else:
        lines = official.read_text(encoding="utf-8").splitlines()
        selected = select_smoke(lines, args.line_numbers)
        (official.parent / SMOKE_NAME).write_text("".join(l + "\n" for l in selected), encoding="utf-8")
        errors = []
        print("smoke:", len(selected))

    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run (từ `backend/`): `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q`
Expected: `8 passed`

- [ ] **Step 5: Real corpus smoke of the CLI**

Run (từ `backend/`), dùng file tạm ngoài repo:

```bash
printf '%s\n' '{"question":"x?","keywords":[],"reference_answer":"x","category":"out_of_scope","partition":"foods","sources":[]}' > /tmp/golden_cli_probe.jsonl
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check /tmp/golden_cli_probe.jsonl --authoring; echo "exit=$?"
```

Expected: in ra `total: 1`, một lỗi `INSUFFICIENT_ANSWER`, `exit=1`. Đây là bằng chứng
module load được 205 file corpus thật mà không gọi mạng.

- [ ] **Step 6:** Không commit (Implementer Git: none). Ghi diff, kết quả test và CLI vào report pilot.

---

### Task 2: Pilot `heritages` và hướng dẫn viết (GATE P)

**Files:**
- Create (private): `knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl` (~20 case)
- Create (private): `knowledge-base-hue/meta/golden-full-corpus-writing-guide.md`
- Create: `reports/phase_7a_golden_pilot_implementation_2026_MM_DD.md`

**Interfaces:**
- Consumes: CLI `check --authoring` của Task 1; spec §3–§6.
- Produces: hướng dẫn viết (được Task 3 dùng nguyên văn), ~20 case pilot.

- [ ] **Step 1:** Đọc đầy đủ các file `heritages/` trong curated corpus (29 file theo `discover_full_corpus_files`) trước khi viết.
- [ ] **Step 2:** Viết ~20 case `heritages` theo spec §3–§6, gồm cả 5 category, ít nhất 2 `out_of_scope` gần domain, ít nhất 2 câu dùng tên gọi khác có thật, và ít nhất 1 câu mà đáp án nằm trong bảng nếu `heritages` có bảng phù hợp. Mỗi case có `sources`.
- [ ] **Step 3:** Với mỗi `out_of_scope`, tìm text trên corpus để chắc thực thể/chủ đề không có; ghi lệnh tìm (không ghi nội dung) vào report.
- [ ] **Step 4:** Chạy `HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl --authoring` → exit 0.
- [ ] **Step 5:** Viết hướng dẫn viết (≤1 trang) gồm: quy tắc spec §6 viết gọn, 5 ví dụ tốt và 5 ví dụ xấu lấy từ chính quá trình pilot kèm lý do, và mẫu `reference_answer`.
- [ ] **Step 6:** Report pilot: diff Task 1, test/CLI output, số case theo category, case đã tự loại và lý do, limitation. Không chép câu hỏi/đáp án.
- [ ] **Step 7:** Chuyển handoff về Reviewer (`final_review` cho Task 1–2), nhắn `hue-rag-66`, **dừng**.

**GATE P (Reviewer + User):** Reviewer review Task 1 code và đối chiếu 20/20 case
với corpus, ghi findings vào `knowledge-base-hue/evaluation/phase_7a_review_notes.md`.
User đọc toàn bộ case pilot và hướng dẫn viết. Implementer sửa theo một correction
handoff nếu cần. Task 3 chỉ mở khi User xác nhận hướng dẫn viết.

---

### Task 3: Viết song song các partition còn lại

**Files (private):**
- Modify: `knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl` (bổ sung tới ~37)
- Create: `knowledge-base-hue/<dir>/evaluation/golden_full_corpus_authoring.jsonl` cho `foods`, `festivals`, `performing_arts`, `travel/places`, `travel/services`, `travel/tickets`
- Create: `reports/phase_7a_golden_implementation_2026_MM_DD.md`

**Interfaces:**
- Consumes: hướng dẫn viết đã User xác nhận; CLI `check --authoring`.
- Produces: 7 file authoring hợp lệ.

- [ ] **Step 1:** Giao mỗi partition cho một sub-agent (được phép trong Task 3). Prompt sub-agent gồm: spec §3–§6, hướng dẫn viết, danh sách file `.md` của partition, target số case theo spec §5, đường dẫn output, ranh giới (chỉ ghi file authoring của mình; không sửa corpus; không gọi API).
- [ ] **Step 2:** Mỗi sub-agent đọc hết file `.md` của partition trước khi viết.
- [ ] **Step 3:** Implementer chạy `check --authoring` cho từng file đến khi exit 0, rồi tự đọc từng case để kiểm văn phong và tính khách quan; sửa hoặc xóa case kém.
- [ ] **Step 4:** Kiểm câu trùng chủ đề giữa các partition (cùng một dữ kiện hỏi hai lần) và xử lý.
- [ ] **Step 5:** Report: số case theo partition × category so với spec §5, case đã xóa/sửa và lý do, out-of-scope search ledger, sub-agent đã dùng, limitation.
- [ ] **Step 6:** Chuyển handoff về Reviewer, nhắn `hue-rag-66`, **dừng**.

---

### Task 4: Reviewer đối chiếu, User đọc mẫu, correction (GATE R)

**Thực hiện bởi:** Reviewer và User; Implementer chỉ sửa theo correction handoff.

- [ ] **Step 1 (Reviewer):** Đối chiếu từng case với `sources` và corpus: đáp án đúng và đủ, khách quan, tự nhiên, đúng category, keyword đáp án hợp lý, `out_of_scope` thật sự vắng mặt. Ghi các case cần sửa/xóa vào `phase_7a_review_notes.md`.
- [ ] **Step 2 (Reviewer):** Chọn ngẫu nhiên 10–15 case mỗi partition (ghi seed hoặc cách chọn), cùng mọi case bị đánh dấu, để User đọc.
- [ ] **Step 3 (User):** Đọc mẫu, đồng ý, sửa hoặc xóa.
- [ ] **Step 4 (Implementer):** Thực hiện một correction batch; chạy lại `check --authoring` cho mọi file.
- [ ] **Step 5 (Reviewer):** Kiểm lại đúng các case đã sửa.

---

### Task 5: Merge, smoke và closure

**Files (private):** `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`, `knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl`

- [ ] **Step 1 (Implementer):** `HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus merge` → exit 0; ghi distribution in ra.
- [ ] **Step 2 (Reviewer + User):** Reviewer đề xuất 10 số dòng phủ đủ 5 category và ≥5 partition; User duyệt.
- [ ] **Step 3 (Implementer):** `HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus smoke N1 … N10` → `smoke: 10`.
- [ ] **Step 4 (Implementer):** Chạy lại `check` cho file chính thức; cập nhật implementation report.
- [ ] **Step 5 (Reviewer):** Final review; cập nhật `guides/full_corpus_rag.md` (phần Golden theo spec §2), `Project_Status.md`, user report; User xác nhận closure.

---

## Review Contract

**Risk level:** medium. Một module mới không gọi mạng; dữ liệu private; không đổi runtime/API/Qdrant. Rủi ro chính là chất lượng nội dung Golden, tức quyết định chất lượng của Phase 7B/8.

**Evidence Implementer phải cung cấp:**
- base/head, mọi changed/untracked path (kể cả private file đã tạo, chỉ ghi path);
- output pytest của `tests/test_golden_full_corpus.py` và CLI probe Task 1 Step 5;
- exit code `check` cho từng file authoring/chính thức cùng distribution;
- danh sách sub-agent đã dùng và partition mỗi agent viết;
- out-of-scope search ledger (lệnh tìm, không nội dung);
- case đã tự xóa/sửa và lý do; limitation.

**Kiểm tra độc lập tối thiểu của Reviewer:**
1. validate handoff, base/head, `git status`, `git diff --check`;
2. đọc exact diff Task 1; rerun `tests/test_golden_full_corpus.py`;
3. tự chạy `check` cho mọi file private;
4. đối chiếu 100% case với corpus (GATE P: 20/20; GATE R: toàn bộ);
5. kiểm `out_of_scope` bằng tìm text độc lập trên một mẫu;
6. kiểm smoke deep-equal (mỗi dòng smoke có nguyên văn trong file chính thức);
7. xác nhận không có câu hỏi/đáp án trong tracked file.

**Evidence được reuse khi correction:** test Task 1 nếu module không đổi; kết quả đối chiếu các case không bị sửa.

**Cần authority mới:** gọi API có phí; sửa curated Markdown; đổi schema/category/spec; tạo Golden ngoài 7 partition; commit/push.

**Authority trong plan:**
- Sub-agent: chỉ Task 3 (viết authoring), mỗi agent một partition.
- Git Implementer: none. Commit/push do Reviewer khi User cấp.
- Paid calls: none.

**Closure:** User xác nhận Phase 7A sau final review; Reviewer cập nhật docs active; Phase 7B vẫn đóng cho tới khi có spec/plan riêng.
