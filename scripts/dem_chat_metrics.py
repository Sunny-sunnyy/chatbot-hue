#!/usr/bin/env python3
"""Đếm dòng `chat_metrics` của ĐÚNG một bản code trong log (0 USD, chỉ đọc; dòng log không có nội dung câu hỏi / trả lời).

Log `backend/logs/application.log` dùng chung cho mọi bản đã chạy + pytest ⇒ đếm không lọc sẽ trộn lượt của bản cũ.
    python3 -I scripts/dem_chat_metrics.py                 # liệt kê các git_sha có trong log + số dòng
    python3 -I scripts/dem_chat_metrics.py --sha <sha>     # chỉ bản đó: số lượt theo tuyến, tốc độ, tiền
    python3 -I scripts/dem_chat_metrics.py --sha HEAD      # bản của thư mục chứa script này
    … --jsonl  ⇒ in các dòng đã lọc (JSON) để script khác đọc tiếp
Mặc định bỏ lượt không tốn tiền (pytest dùng model giả); `--ca-luot-0-dong` để giữ.
"""
import argparse
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]


def doc(log: Path):
    for line in log.open(encoding="utf-8", errors="replace"):
        if "chat_metrics " in line:
            try:
                yield json.loads(line.split("chat_metrics ", 1)[1])
            except json.JSONDecodeError:
                continue  # dòng bị cắt khi log xoay vòng


def co_tien(m: dict) -> bool:
    return m.get("model") != "probe" and sum((c.get("usd") or 0) for c in m.get("llm_calls") or []) > 0


def phan_vi(xs, p):
    xs = sorted(x for x in xs if x is not None)
    return "-" if not xs else f"{xs[min(len(xs) - 1, round(p * (len(xs) - 1)))] / 1000:.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--log", type=Path, default=GOC / "backend/logs/application.log")
    ap.add_argument("--sha", help="git_sha cần lọc; HEAD = bản của thư mục chứa script này")
    ap.add_argument("--ca-luot-0-dong", action="store_true", help="giữ cả lượt không tốn tiền (pytest, lỗi trước model)")
    ap.add_argument("--jsonl", action="store_true")
    a = ap.parse_args()
    rows = list(doc(a.log))
    if not a.sha:
        dem = Counter(m.get("git_sha") or "(dòng cũ, chưa có git_sha)" for m in rows)
        for sha, n in dem.most_common():
            print(f"{sha:30s} {n:6d} dòng · có tiền {sum(co_tien(m) for m in rows if (m.get('git_sha') or '(dòng cũ, chưa có git_sha)') == sha)}")
        return
    sha = a.sha
    if sha == "HEAD":
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=GOC, capture_output=True, text=True, check=True).stdout.strip()
    cung_sha = [m for m in rows if m.get("git_sha") == sha]
    rows = [m for m in cung_sha if a.ca_luot_0_dong or co_tien(m)]
    if a.jsonl:
        for m in rows:
            print(json.dumps(m, ensure_ascii=False))
        return
    print(f"git_sha {sha}: {len(rows)} lượt · {sum(m.get('usd') or 0 for m in rows):.4f} USD (bỏ {len(cung_sha) - len(rows)} lượt 0 đồng)")
    nhom = defaultdict(list)
    for m in rows:
        nhom[m.get("route")].append(m)
    for route, ms in sorted(nhom.items(), key=lambda kv: -len(kv[1])):
        ft, tt = [m.get("first_text_ms") for m in ms], [m.get("total_ms") for m in ms]
        print(f"  {str(route):16s} n={len(ms):4d} · chữ đầu p50 {phan_vi(ft, .5)} p95 {phan_vi(ft, .95)} s · cả câu p50 {phan_vi(tt, .5)} p95 {phan_vi(tt, .95)} s"
              f" · từ chối {sum(bool(m.get('refusal')) for m in ms)}")


if __name__ == "__main__":
    main()
