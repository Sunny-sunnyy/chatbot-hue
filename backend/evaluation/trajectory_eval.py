"""Đánh giá quỹ đạo Agent (Trajectory Eval, 0 USD) trên `application.log` hoặc file JSONL.

Chạy từ `backend/`:
    uv run python -m evaluation.trajectory_eval
    uv run python -m evaluation.trajectory_eval --log logs/application.log --model gpt-6-luna
    uv run python -m evaluation.trajectory_eval --log path/to/metrics.jsonl --json
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Iterable

DEFAULT_LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "application.log"
TEST_MODELS = frozenset({"probe", "fake-bench"})
MODEL_TOOL_NAMES = frozenset({
    "ngay_lich",
    "liet_ke_bai",
    "khoang_cach",
    "gan_diem",
    "thoi_tiet",
    "lich_trinh",
    "goi_y_phuong_an_mua_nang",
    "so_sanh_diem_den",
})


def la_goi_cong_cu_model(entry: dict) -> bool:
    """True nếu mục `trace.tools` là một lần model gọi công cụ (không tính bước code như `tim_kho` đầu, `lich_san`, `tra_web`, `viet_lai_het_luot`)."""
    name = entry.get("name")
    if name == "tim_kho":
        return entry.get("by") == "model"
    if name == "thoi_tiet":
        return entry.get("by") != "code"
    return name in MODEL_TOOL_NAMES


def doc_log(path: Path) -> list[dict]:
    """Đọc các bản ghi `chat_metrics` từ file log (`chat_metrics {...}`) hoặc file JSONL thuần (mỗi dòng một JSON dict)."""
    rows: list[dict] = []
    with Path(path).open(encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            payload = line.split("chat_metrics ", 1)[1] if "chat_metrics " in line else line
            if not payload.startswith("{"):
                continue
            try:
                obj = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and any(k in obj for k in ("outcome", "route", "tools", "llm_calls")):
                rows.append(obj)
    return rows


def loc_luot(
    rows: Iterable[dict],
    *,
    sha: str | None = None,
    model: str | None = None,
    bo_test_model: bool = True,
    chi_co_tien: bool = False,
) -> list[dict]:
    """Lọc danh sách lượt theo `git_sha`, `model`, loại lượt test (`probe`/`fake-bench`) hoặc chỉ giữ lượt có phát sinh chi phí."""
    out: list[dict] = []
    for m in rows:
        if bo_test_model and m.get("model") in TEST_MODELS:
            continue
        if sha is not None and m.get("git_sha") != sha:
            continue
        if model is not None and m.get("model") != model:
            continue
        if chi_co_tien and sum((c.get("usd") or 0.0) for c in (m.get("llm_calls") or [])) <= 0:
            continue
        out.append(m)
    return out


def phan_vi(values: Iterable[float | int], p: float) -> float | None:
    """Tính phân vị `p` (0..1) theo thứ tự sắp tăng; rỗng trả None."""
    xs = sorted(float(x) for x in values if x is not None)
    if not xs:
        return None
    idx = min(len(xs) - 1, round(p * (len(xs) - 1)))
    return xs[idx]


def _da_cuu_max_turns(m: dict) -> tuple[bool, bool]:
    """Trả `(da_chay_cuu, thanh_cong)` cho một bản ghi lượt."""
    flag = m.get("cuu_max_turns")
    tools = m.get("tools") or []
    tool_entry = next((t for t in tools if t.get("name") == "cuu_max_turns"), None)
    if isinstance(flag, dict):
        return True, bool(flag.get("thanh_cong"))
    if tool_entry is not None:
        return True, bool(tool_entry.get("thanh_cong"))
    if flag is True:
        return True, m.get("outcome") != "max_turns" and m.get("loi_kiem") is None
    return False, False


def tinh_quy_dao(rows: Iterable[dict]) -> dict:
    """Tính bảng chỉ số quỹ đạo Agent từ các dòng `chat_metrics`."""
    data = list(rows)
    tong_luot = len(data)
    route_counts: Counter[str] = Counter()
    outcome_counts: Counter[str] = Counter()
    tool_rounds_per_turn: list[int] = []
    tool_breakdown: dict[str, dict[str, int]] = {}

    luot_co_lap = 0
    so_lan_lap = 0
    luot_max_turns = 0
    luot_viet_lai = 0
    luot_cuu_max_turns = 0
    luot_cuu_max_turns_thanh_cong = 0
    luot_loi_kiem = 0
    luot_thanh_cong = 0
    tong_usd = 0.0
    usd_thanh_cong = 0.0

    for m in data:
        route_counts[m.get("route") or "(khong_ro)"] += 1
        outcome = m.get("outcome") or "(khong_ro)"
        outcome_counts[outcome] += 1

        tools = m.get("tools") or []
        model_tools = [t for t in tools if la_goi_cong_cu_model(t)]
        tool_rounds_per_turn.append(len(model_tools))

        for t in model_tools:
            ten = str(t.get("name"))
            stat = tool_breakdown.setdefault(ten, {"goi": 0, "lap": 0, "het_luot": 0})
            stat["goi"] += 1
            if t.get("lap"):
                stat["lap"] += 1
            if t.get("het_luot"):
                stat["het_luot"] += 1

        lap_in_turn = sum(1 for t in tools if t.get("lap"))
        if lap_in_turn > 0:
            luot_co_lap += 1
            so_lan_lap += lap_in_turn

        if outcome == "max_turns":
            luot_max_turns += 1
        if any(t.get("name") == "viet_lai_het_luot" for t in tools):
            luot_viet_lai += 1
        da_cuu, cuu_ok = _da_cuu_max_turns(m)
        if da_cuu:
            luot_cuu_max_turns += 1
            if cuu_ok:
                luot_cuu_max_turns_thanh_cong += 1
        if m.get("loi_kiem") is not None:
            luot_loi_kiem += 1

        usd = float(m.get("usd") or 0.0)
        tong_usd += usd
        if outcome == "success":
            luot_thanh_cong += 1
            usd_thanh_cong += usd

    tong_goi_tool_model = sum(tool_rounds_per_turn)
    return {
        "tong_luot": tong_luot,
        "phan_bo_route": dict(route_counts.most_common()),
        "phan_bo_outcome": dict(outcome_counts.most_common()),
        "tong_goi_tool_model": tong_goi_tool_model,
        "so_vong_tool_tb": round(tong_goi_tool_model / tong_luot, 4) if tong_luot else 0.0,
        "so_vong_tool_p95": phan_vi(tool_rounds_per_turn, 0.95) if tong_luot else None,
        "luot_co_lap": luot_co_lap,
        "so_lan_lap": so_lan_lap,
        "ty_le_lap": round(luot_co_lap / tong_luot, 6) if tong_luot else 0.0,
        "ty_le_goi_lap": round(so_lan_lap / tong_goi_tool_model, 6) if tong_goi_tool_model else 0.0,
        "luot_max_turns": luot_max_turns,
        "ty_le_max_turns": round(luot_max_turns / tong_luot, 6) if tong_luot else 0.0,
        "luot_het_luot_viet_lai": luot_viet_lai,
        "ty_le_het_luot_viet_lai": round(luot_viet_lai / tong_luot, 6) if tong_luot else 0.0,
        "luot_cuu_max_turns": luot_cuu_max_turns,
        "luot_cuu_max_turns_thanh_cong": luot_cuu_max_turns_thanh_cong,
        "ty_le_cuu_max_turns": round(luot_cuu_max_turns / tong_luot, 6) if tong_luot else 0.0,
        "luot_loi_kiem": luot_loi_kiem,
        "ty_le_loi_kiem": round(luot_loi_kiem / tong_luot, 6) if tong_luot else 0.0,
        "luot_thanh_cong": luot_thanh_cong,
        "tong_usd": round(tong_usd, 8),
        "usd_moi_luot_thanh_cong": round(tong_usd / luot_thanh_cong, 8) if luot_thanh_cong else None,
        "usd_tb_luot_thanh_cong": round(usd_thanh_cong / luot_thanh_cong, 8) if luot_thanh_cong else None,
        "theo_tool": dict(sorted(tool_breakdown.items(), key=lambda kv: (-kv[1]["goi"], kv[0]))),
    }


def _pct(ratio: float) -> str:
    return f"{ratio * 100:.2f}%"


def dinh_dang_bang(stats: dict) -> str:
    """Định dạng bảng tóm tắt các chỉ số quỹ đạo để in ra màn hình hoặc báo cáo."""
    usd_all = "-" if stats["usd_moi_luot_thanh_cong"] is None else f"{stats['usd_moi_luot_thanh_cong']:.6f} USD"
    usd_ok = "-" if stats["usd_tb_luot_thanh_cong"] is None else f"{stats['usd_tb_luot_thanh_cong']:.6f} USD"
    p95 = "-" if stats["so_vong_tool_p95"] is None else f"{stats['so_vong_tool_p95']:.1f}"
    lines = [
        "| Chỉ số quỹ đạo | Giá trị |",
        "|---|---|",
        f"| Tổng lượt | {stats['tong_luot']} (thành công: {stats['luot_thanh_cong']}) |",
        f"| Phân bố route | {json.dumps(stats['phan_bo_route'], ensure_ascii=False)} |",
        f"| Phân bố outcome | {json.dumps(stats['phan_bo_outcome'], ensure_ascii=False)} |",
        f"| Số vòng tool model TB / p95 | {stats['so_vong_tool_tb']:.3f} / {p95} (tổng {stats['tong_goi_tool_model']} lần gọi) |",
        f"| Tỉ lệ gọi lặp (`lap`) | {stats['luot_co_lap']}/{stats['tong_luot']} ({_pct(stats['ty_le_lap'])}) · theo lần gọi: {stats['so_lan_lap']}/{stats['tong_goi_tool_model']} ({_pct(stats['ty_le_goi_lap'])}) |",
        f"| Tỉ lệ chạm `max_turns` | {stats['luot_max_turns']}/{stats['tong_luot']} ({_pct(stats['ty_le_max_turns'])}) |",
        f"| Tỉ lệ `het_luot_viet_lai` | {stats['luot_het_luot_viet_lai']}/{stats['tong_luot']} ({_pct(stats['ty_le_het_luot_viet_lai'])}) |",
        f"| Tỉ lệ `cuu_max_turns` | {stats['luot_cuu_max_turns']}/{stats['tong_luot']} ({_pct(stats['ty_le_cuu_max_turns'])}) · cứu đạt: {stats['luot_cuu_max_turns_thanh_cong']} |",
        f"| Tỉ lệ `loi_kiem` | {stats['luot_loi_kiem']}/{stats['tong_luot']} ({_pct(stats['ty_le_loi_kiem'])}) |",
        f"| USD / lượt thành công | tổng/thành công: {usd_all} · TB lượt thành công: {usd_ok} (tổng chi: {stats['tong_usd']:.6f} USD) |",
    ]
    if stats["theo_tool"]:
        lines.append("")
        lines.append("| Công cụ model | Số lần gọi | Lặp (`lap`) | Hết lượt (`het_luot`) |")
        lines.append("|---|---:|---:|---:|")
        for ten, s in stats["theo_tool"].items():
            lines.append(f"| `{ten}` | {s['goi']} | {s['lap']} | {s['het_luot']} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Đánh giá quỹ đạo Agent từ chat_metrics (0 USD)")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG_PATH, help="Đường dẫn application.log hoặc file JSONL")
    ap.add_argument("--sha", default=None, help="Chỉ lọc lượt có git_sha này")
    ap.add_argument("--model", default=None, help="Chỉ lọc lượt có model này")
    ap.add_argument("--giu-test", action="store_true", help="Giữ cả lượt model giả lập (probe, fake-bench)")
    ap.add_argument("--chi-co-tien", action="store_true", help="Chỉ giữ lượt có phát sinh chi phí USD > 0")
    ap.add_argument("--json", action="store_true", help="In JSON thay cho bảng Markdown")
    args = ap.parse_args(argv)

    raw_rows = doc_log(args.log)
    filtered = loc_luot(raw_rows, sha=args.sha, model=args.model, bo_test_model=not args.giu_test, chi_co_tien=args.chi_co_tien)
    stats = tinh_quy_dao(filtered)
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(dinh_dang_bang(stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
