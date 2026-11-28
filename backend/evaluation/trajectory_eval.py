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
from typing import Any, Iterable
import unicodedata

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
    "tinh_ve_va_gio_tham_quan",
    "goi_y_luu_tru",
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


_TOOL_TELEMETRY_KEYS = frozenset({
    "name", "ms", "by", "lap", "het_luot", "bao_lu", "n", "n_ket_qua", "n_bai", "n_o_ten",
    "n_queries", "n_new", "n_ve", "n_them_ve", "n_cum_tu", "trang_thai", "loi",
    "sau_du_bao", "sau_lich", "khong_co", "thanh_cong",
})
_KHONG_CO_DIEM = frozenset({"", "khong_co", "khong_ro", "khac"})


def _chuan_gia_tri(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value).strip().casefold()
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, (list, tuple)):
        return tuple(_chuan_gia_tri(x) for x in value)
    if isinstance(value, dict):
        return tuple(sorted((str(k), _chuan_gia_tri(v)) for k, v in value.items()))
    return value


def _trich_tham_so_tool(entry: dict[str, Any]) -> dict[str, Any]:
    """Lấy dict tham số enum từ mục `trace.tools` (hỗ trợ cả `entry['args']` lẫn các khoá phẳng của `chat_metrics`)."""
    args: dict[str, Any] = {}
    if isinstance(entry.get("args"), dict):
        args.update(entry["args"])
    for k, v in entry.items():
        if k not in _TOOL_TELEMETRY_KEYS and k != "args":
            args[k] = v
    return args


def _sorted_key_for_tool_call(name: str, args: dict[str, Any]) -> tuple[str, tuple[tuple[str, Any], ...]]:
    """Khoá chuẩn hoá bất biến theo thứ tự tham số (tham chiếu `ragas/_tool_call_accuracy.py`)."""
    norm_name = str(_chuan_gia_tri(name))
    norm_items = tuple(sorted((str(k), _chuan_gia_tri(v)) for k, v in args.items()))
    return norm_name, norm_items


def _chuan_ky_vong_call(spec: str | dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if isinstance(spec, str):
        return spec, {}
    name = str(spec["name"])
    if isinstance(spec.get("args"), dict):
        return name, dict(spec["args"])
    args = {k: v for k, v in spec.items() if k not in {"name", "args", "strict"}}
    return name, args


def _diem_trong_goi(args: dict[str, Any]) -> set[str]:
    points = set()
    for key in ("diem_1", "diem_2", "diem_3", "diem_a", "diem_b", "diem", "diem_goc"):
        val = args.get(key)
        if isinstance(val, str):
            norm = _chuan_gia_tri(val)
            if norm not in _KHONG_CO_DIEM:
                points.add(norm)
    return points


def _khop_goi_cong_cu(actual_entry: dict[str, Any], expected_spec: str | dict[str, Any]) -> bool:
    exp_name, exp_args = _chuan_ky_vong_call(expected_spec)
    if _chuan_gia_tri(actual_entry.get("name") or "") != _chuan_gia_tri(exp_name):
        return False
    if not exp_args:
        return True
    act_args = _trich_tham_so_tool(actual_entry)
    for k, exp_val in exp_args.items():
        if k == "diem_set":
            wanted = {_chuan_gia_tri(x) for x in exp_val if _chuan_gia_tri(x) not in _KHONG_CO_DIEM}
            if not wanted.issubset(_diem_trong_goi(act_args)):
                return False
            continue
        act_val = act_args.get(k)
        if isinstance(exp_val, dict) and "any_of" in exp_val:
            allowed = {_chuan_gia_tri(x) for x in exp_val["any_of"]}
            if _chuan_gia_tri(act_val) not in allowed:
                return False
        elif _chuan_gia_tri(act_val) != _chuan_gia_tri(exp_val):
            return False
    return True


def _max_bipartite_match(actual: list[dict[str, Any]], expected: list[str | dict[str, Any]]) -> int:
    """Ghép 1-1 cực đại giữa `expected` và `actual` không phân biệt thứ tự."""
    match_actual: list[int | None] = [None] * len(actual)

    def dfs(exp_idx: int, seen: list[bool]) -> bool:
        for act_idx, act_entry in enumerate(actual):
            if seen[act_idx] or not _khop_goi_cong_cu(act_entry, expected[exp_idx]):
                continue
            seen[act_idx] = True
            if match_actual[act_idx] is None or dfs(match_actual[act_idx], seen):
                match_actual[act_idx] = exp_idx
                return True
        return False

    matched = 0
    for exp_idx in range(len(expected)):
        if dfs(exp_idx, [False] * len(actual)):
            matched += 1
    return matched


def _lcs_match(actual: list[dict[str, Any]], expected: list[str | dict[str, Any]]) -> int:
    """Ghép giữ đúng thứ tự (LCS) giữa `expected` và `actual`."""
    m, n = len(expected), len(actual)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if _khop_goi_cong_cu(actual[j - 1], expected[i - 1]):
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def score_tool_calls(
    actual_tools: Iterable[dict[str, Any]],
    expected_tools: Iterable[str | dict[str, Any]],
    *,
    strict_order: bool = False,
    ignore_tim_kho: bool = True,
    forbidden_tools: Iterable[str] = (),
) -> dict[str, Any]:
    """Chấm `ToolCallAccuracy` (0 USD) cho một lượt: precision, recall, F1, exact_match, gọi thừa & gọi cấm."""
    exp_list = list(expected_tools)
    act_list = [
        t for t in actual_tools
        if la_goi_cong_cu_model(t) and not (ignore_tim_kho and t.get("name") == "tim_kho")
    ]
    n_exp = len(exp_list)
    n_act = len(act_list)

    if n_exp == 0 and n_act == 0:
        tp = 0
        precision = 1.0
        recall = 1.0
        f1 = 1.0
    else:
        tp = _lcs_match(act_list, exp_list) if strict_order else _max_bipartite_match(act_list, exp_list)
        precision = tp / n_act if n_act > 0 else 0.0
        recall = tp / n_exp if n_exp > 0 else 1.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    forbidden_set = {_chuan_gia_tri(x) for x in forbidden_tools}
    forbidden_hits = sum(1 for t in act_list if _chuan_gia_tri(t.get("name") or "") in forbidden_set)

    return {
        "tp": tp,
        "n_expected": n_exp,
        "n_actual": n_act,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "exact_match": tp == n_exp == n_act,
        "extra_calls": max(0, n_act - tp),
        "missing_calls": max(0, n_exp - tp),
        "forbidden_hits": forbidden_hits,
        "actual_keys": [_sorted_key_for_tool_call(str(t.get("name") or ""), _trich_tham_so_tool(t)) for t in act_list],
    }


def doc_ket_qua_do(path: Path) -> list[dict[str, Any]]:
    """Đọc kết quả từ file `dot2_*.json` (`{"results": [...]}`), JSON list, hoặc file log/JSONL (`doc_log`)."""
    raw = Path(path).read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return []
    if raw.startswith("{") or raw.startswith("["):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict) and isinstance(data.get("results"), list):
            out: list[dict[str, Any]] = []
            for item in data["results"]:
                if not isinstance(item, dict):
                    continue
                metrics = item.get("metrics") if isinstance(item.get("metrics"), dict) else {}
                merged = {**metrics}
                for key in ("id", "case_index", "subgroup", "category", "query"):
                    if key in item and key not in merged:
                        merged[key] = item[key]
                if "tools" not in merged and isinstance(item.get("tools"), list):
                    merged["tools"] = item["tools"]
                out.append(merged)
            return out
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
    return doc_log(Path(path))


def _spec_tu_case_bo_cau(case: dict[str, Any]) -> dict[str, Any]:
    """Suy ra `{expected_tools, forbidden_tools, subgroup}` từ một mục trong `bo_cau_dot2.json` / `bo_cau_dot4a.json`."""
    subgroup = case.get("subgroup")
    if "expected_tools" in case:
        return {
            "expected_tools": list(case["expected_tools"]),
            "forbidden_tools": list(case.get("forbidden_tools") or ()),
            "subgroup": subgroup,
        }
    cid = str(case.get("id") or "")
    expected: list[dict[str, Any]] = []
    forbidden: list[str] = []

    if case.get("need_tool"):
        expected.append({"name": str(case["need_tool"]), "args": dict(case.get("expected_args") or {})})
    elif cid.startswith("mn_bao_"):
        forbidden.append("goi_y_phuong_an_mua_nang")
    elif cid.startswith("mn_ngoai_"):
        if "ngoài phạm vi" in str(case.get("note") or "").casefold():
            forbidden.append("goi_y_phuong_an_mua_nang")
    elif cid.startswith("mn_"):
        args: dict[str, Any] = {}
        if case.get("diem_goc"):
            args["diem_goc"] = case["diem_goc"]
        if case.get("buoi"):
            args["buoi"] = case["buoi"]
        expected.append({"name": "goi_y_phuong_an_mua_nang", "args": args})
    elif cid.startswith("ss_vh_") or cid.startswith("ss_ng_"):
        forbidden.append("so_sanh_diem_den")
    elif cid.startswith("ss_"):
        expected.append({"name": "so_sanh_diem_den", "args": dict(case.get("expected_args") or {})})

    return {"expected_tools": expected, "forbidden_tools": forbidden, "subgroup": subgroup}


def chuan_hoa_ky_vong_bo_cau(raw: Any, group: str | None = None) -> dict[str, dict[str, Any]]:
    """Chuẩn hoá file bộ câu (`bo_cau_dot2.json`, `bo_cau_dot4a.json` hoặc map `id -> spec`) thành `dict[id, spec]`."""
    if isinstance(raw, dict) and "results" not in raw:
        # Nếu là dict các nhóm như `{"H2_mua_nang": [...], ...}` hoặc map `id -> spec/list`.
        if group is not None and isinstance(raw.get(group), list):
            items = raw[group]
        elif all(isinstance(v, list) for k, v in raw.items() if k != "meta"):
            items = [item for k, v in raw.items() if k != "meta" and isinstance(v, list) for item in v]
        else:
            out: dict[str, dict[str, Any]] = {}
            for k, v in raw.items():
                if k == "meta":
                    continue
                if isinstance(v, list):
                    out[str(k)] = {"expected_tools": v, "forbidden_tools": [], "subgroup": None}
                elif isinstance(v, dict):
                    out[str(k)] = _spec_tu_case_bo_cau({"id": str(k), **v})
            return out
        return {str(c.get("id") or c.get("case_index")): _spec_tu_case_bo_cau(c) for c in items if isinstance(c, dict)}
    if isinstance(raw, list):
        return {str(c.get("id") or c.get("case_index")): _spec_tu_case_bo_cau(c) for c in raw if isinstance(c, dict)}
    raise ValueError("Unsupported expected-tools specification format")


def _tong_hop_nhom_tool_accuracy(cases: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(cases)
    if n == 0:
        return {"n": 0}
    return {
        "n": n,
        "precision": round(sum(c["precision"] for c in cases) / n, 6),
        "recall": round(sum(c["recall"] for c in cases) / n, 6),
        "f1": round(sum(c["f1"] for c in cases) / n, 6),
        "exact_match_rate": round(sum(bool(c["exact_match"]) for c in cases) / n, 6),
        "exact_matches": sum(bool(c["exact_match"]) for c in cases),
        "extra_call_turns": sum(c["extra_calls"] > 0 for c in cases),
        "total_extra_calls": sum(c["extra_calls"] for c in cases),
        "total_missing_calls": sum(c["missing_calls"] for c in cases),
        "forbidden_hit_turns": sum(c["forbidden_hits"] > 0 for c in cases),
    }


def tinh_tool_call_accuracy(
    rows: Iterable[dict[str, Any]],
    expected_by_id: dict[str, Any],
    *,
    strict_order: bool = False,
    ignore_tim_kho: bool | None = None,
) -> dict[str, Any]:
    """Tính `ToolCallAccuracy` (0 USD) trên danh sách lượt chạy đối chiếu với `expected_by_id`."""
    norm_specs: dict[str, dict[str, Any]] = {}
    for k, v in expected_by_id.items():
        if isinstance(v, list):
            norm_specs[str(k)] = {"expected_tools": v, "forbidden_tools": [], "subgroup": None}
        else:
            norm_specs[str(k)] = _spec_tu_case_bo_cau({"id": str(k), **v}) if "expected_tools" not in v else v

    if ignore_tim_kho is None:
        has_expected_tim_kho = any(
            _chuan_gia_tri(_chuan_ky_vong_call(call)[0]) == "tim_kho"
            for spec in norm_specs.values()
            for call in spec.get("expected_tools", ())
        )
        ignore_tim_kho = not has_expected_tim_kho

    per_case: list[dict[str, Any]] = []
    by_subgroup: dict[str, list[dict[str, Any]]] = {}

    for idx, row in enumerate(rows):
        row_id = row.get("id")
        key = str(row_id if row_id is not None else row.get("case_index", idx))
        if key not in norm_specs:
            continue
        spec = norm_specs[key]
        scored = score_tool_calls(
            row.get("tools") or (),
            spec.get("expected_tools") or (),
            strict_order=strict_order,
            ignore_tim_kho=ignore_tim_kho,
            forbidden_tools=spec.get("forbidden_tools") or (),
        )
        subgroup = row.get("subgroup") or spec.get("subgroup") or "(khac)"
        case_out = {"id": key, "subgroup": subgroup, **scored}
        per_case.append(case_out)
        by_subgroup.setdefault(subgroup, []).append(case_out)

    return {
        "strict_order": strict_order,
        "ignore_tim_kho": ignore_tim_kho,
        "overall": _tong_hop_nhom_tool_accuracy(per_case),
        "by_subgroup": {sg: _tong_hop_nhom_tool_accuracy(items) for sg, items in sorted(by_subgroup.items())},
        "per_case": per_case,
    }


def dinh_dang_bang_tool_accuracy(stats: dict[str, Any]) -> str:
    """Định dạng bảng Markdown kết quả `ToolCallAccuracy`."""
    ov = stats["overall"]
    if ov.get("n", 0) == 0:
        return "| Nhóm | n | Precision | Recall | F1 | Exact | Gọi thừa (lượt/lần) | Cấm |\n|---|---:|---:|---:|---:|---:|---:|---:|\n| overall | 0 | - | - | - | - | - | - |"
    lines = [
        f"Mode: `strict_order={stats['strict_order']}`, `ignore_tim_kho={stats['ignore_tim_kho']}`",
        "",
        "| Nhóm | n | Precision | Recall | F1 | Exact | Gọi thừa (lượt/lần) | Cấm |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, s in [("overall", ov), *stats["by_subgroup"].items()]:
        lines.append(
            f"| {label} | {s['n']} | {s['precision']:.3f} | {s['recall']:.3f} | {s['f1']:.3f} | "
            f"{s['exact_matches']}/{s['n']} ({_pct(s['exact_match_rate'])}) | "
            f"{s['extra_call_turns']}/{s['total_extra_calls']} | {s['forbidden_hit_turns']} |"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Đánh giá quỹ đạo Agent từ chat_metrics (0 USD)")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG_PATH, help="Đường dẫn application.log, JSONL hoặc dot2_*.json")
    ap.add_argument("--sha", default=None, help="Chỉ lọc lượt có git_sha này")
    ap.add_argument("--model", default=None, help="Chỉ lọc lượt có model này")
    ap.add_argument("--giu-test", action="store_true", help="Giữ cả lượt model giả lập (probe, fake-bench)")
    ap.add_argument("--chi-co-tien", action="store_true", help="Chỉ giữ lượt có phát sinh chi phí USD > 0")
    ap.add_argument("--expected", type=Path, default=None, help="File JSON kỳ vọng tool (bo_cau_dot2.json / bo_cau_dot4a.json) để tính ToolCallAccuracy")
    ap.add_argument("--group", default=None, help="Tên nhóm trong file --expected (vd: H2_mua_nang)")
    ap.add_argument("--strict-order", action="store_true", help="So khớp thứ tự chặt cho ToolCallAccuracy")
    ap.add_argument("--include-tim-kho", action="store_true", help="Tính cả tim_kho vào ToolCallAccuracy thay vì bỏ qua khi không có trong kỳ vọng")
    ap.add_argument("--json", action="store_true", help="In JSON thay cho bảng Markdown")
    args = ap.parse_args(argv)

    raw_rows = doc_ket_qua_do(args.log)
    filtered = loc_luot(raw_rows, sha=args.sha, model=args.model, bo_test_model=not args.giu_test, chi_co_tien=args.chi_co_tien)
    stats = tinh_quy_dao(filtered)
    if args.expected is not None:
        exp_raw = json.loads(args.expected.read_text(encoding="utf-8"))
        exp_map = chuan_hoa_ky_vong_bo_cau(exp_raw, group=args.group)
        ignore_tk = False if args.include_tim_kho else None
        tool_acc = tinh_tool_call_accuracy(filtered, exp_map, strict_order=args.strict_order, ignore_tim_kho=ignore_tk)
        if args.json:
            print(json.dumps({"trajectory": stats, "tool_call_accuracy": tool_acc}, ensure_ascii=False, indent=2))
        else:
            print(dinh_dang_bang(stats))
            print()
            print(dinh_dang_bang_tool_accuracy(tool_acc))
        return 0

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(dinh_dang_bang(stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
