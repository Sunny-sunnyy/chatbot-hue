"""Quét chữ trùng >= 40 ký tự liên tiếp với Golden / kho tri thức (private) — chỉ in số dòng + loại nguồn, không in nội dung.

Vì sao: repo PUBLIC; báo cáo chép nhầm câu Golden hay đoạn kho thì lộ vĩnh viễn trong lịch sử git. Hai lần (25/10, 26/10) quét
tay rồi nối `; git commit` nên commit vẫn chạy dù quét báo trùng ⇒ đưa vào `.githooks/pre-commit` (sổ cải tiến W16).
File này không chứa dữ liệu: chỉ đọc Golden / kho trên máy; clone không có kho thì báo bỏ qua, exit 0.

  uv run python .githooks/overlap_scan.py <file> …   # quét cả file (A quét file người khác viết trước khi stage)
  uv run python .githooks/overlap_scan.py --staged    # hook: chỉ dòng THÊM MỚI đã stage (file cũ còn trùng không chặn khi sửa dòng khác)
Exit 3 khi có dòng trùng (lỗi chạy — thiếu file, import… — ra mã khác, để hook báo đúng loại).
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # working tree đang commit (có thể là worktree /tmp): git diff + import backend
# Kho / Golden đọc từ working tree chính (cha của git-common-dir): worktree /tmp thường không có symlink kho ⇒ không được
# lặng lẽ bỏ qua quét (review C 26/10 M-1).
MAIN_ROOT = Path(subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.strip()).parent
KB = MAIN_ROOT / "knowledge-base-hue"
GOLDEN = KB / "evaluation/golden_full_corpus.jsonl"
HIT_EXIT = 3
WINDOW = 40


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def build_grams() -> dict[str, str]:
    sys.path.insert(0, str(ROOT / "backend"))
    from llm.full_corpus_prompt import INSUFFICIENT_ANSWER  # câu từ chối chuẩn, có trong code public ⇒ không tính trùng

    refusal = norm(INSUFFICIENT_ANSWER)
    grams: dict[str, str] = {}

    def add(text: str, tag: str) -> None:
        t = norm(text).replace(refusal, " ")
        for i in range(0, max(0, len(t) - WINDOW + 1), 5):
            grams.setdefault(t[i:i + WINDOW], tag)

    for line in GOLDEN.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            add(row["question"], "golden_q")
            add(row["reference_answer"], "golden_a")
    for path in KB.rglob("*.md"):
        if not {"evaluation", "meta", "_source-dumps"} & set(path.parts):
            add(path.read_text(encoding="utf-8"), "corpus")
    return grams


def staged_added_lines() -> list[tuple[str, list[tuple[int, str]]]]:
    """Dòng thêm mới đã stage theo từng file, kèm số dòng trong file mới (đọc từ đầu hunk `@@ -a,b +c,d @@`)."""
    diff = subprocess.run(["git", "-c", "core.quotePath=false", "diff", "--cached", "-U0", "--no-color", "--diff-filter=ACMR"],
                          cwd=ROOT, capture_output=True, text=True, check=True).stdout
    files: dict[str, list[tuple[int, str]]] = {}
    current, n = None, 0
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            current = None
        elif line.startswith("+++ ") and current is None:
            current = line[6:].rstrip("\t") if line.startswith("+++ b/") else None  # tên có khoảng trắng: git thêm tab cuối
        elif line.startswith("@@") and current is not None:
            n = int(re.match(r"@@ -\S+ \+(\d+)", line).group(1))
            files.setdefault(current, [])
        elif line.startswith("+") and current is not None and current in files:
            files[current].append((n, line[1:]))
            n += 1
    return list(files.items())


def hits(lines: list[tuple[int, str]], grams: dict[str, str]) -> dict[str, list[int]]:
    found: dict[str, list[int]] = {}
    for n, line in lines:
        t = norm(line)
        for i in range(0, max(0, len(t) - WINDOW + 1)):
            tag = grams.get(t[i:i + WINDOW])
            if tag:
                found.setdefault(tag, []).append(n)
                break
    return found


def main() -> int:
    if not GOLDEN.exists():
        print("overlap_scan: không có Golden / kho trên máy — bỏ qua")
        return 0
    if sys.argv[1:] == ["--staged"]:
        inputs = staged_added_lines()
    else:
        inputs = [(Path(f).name, list(enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1))) for f in sys.argv[1:]]
    grams = build_grams()
    any_hit = False
    for label, lines in inputs:
        found = hits(lines, grams)
        any_hit |= bool(found)
        print(label, found or "0 trùng")
    return HIT_EXIT if any_hit else 0


if __name__ == "__main__":
    sys.exit(main())
