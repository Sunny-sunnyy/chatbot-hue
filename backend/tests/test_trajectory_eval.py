"""Unit test cho `evaluation/trajectory_eval.py` (0 USD)."""
import json

from evaluation.trajectory_eval import (
    DEFAULT_LOG_PATH,
    dinh_dang_bang,
    doc_log,
    la_goi_cong_cu_model,
    loc_luot,
    main,
    tinh_quy_dao,
)


def test_la_goi_cong_cu_model_distinguishes_code_steps_from_model_tools():
    assert la_goi_cong_cu_model({"name": "tim_kho", "ms": 10.0}) is False  # bước tìm đầu của code
    assert la_goi_cong_cu_model({"name": "tim_kho", "ms": 10.0, "by": "model"}) is True
    assert la_goi_cong_cu_model({"name": "thoi_tiet", "ms": 10.0, "by": "code"}) is False
    assert la_goi_cong_cu_model({"name": "thoi_tiet", "ms": 10.0}) is True
    for name in ("ngay_lich", "liet_ke_bai", "khoang_cach", "gan_diem", "lich_trinh"):
        assert la_goi_cong_cu_model({"name": name, "ms": 0.0}) is True
    for code_step in ("lich_san", "su_kien_san", "khoang_cach_san", "tra_web", "viet_lai_het_luot", "cuu_max_turns"):
        assert la_goi_cong_cu_model({"name": code_step, "ms": 0.0}) is False


def test_doc_log_and_tinh_quy_dao_on_mixed_log_and_jsonl(tmp_path):
    rows = [
        {
            "outcome": "success",
            "route": "tro_ly_hue",
            "model": "gpt-6-luna",
            "usd": 0.001,
            "loi_kiem": None,
            "llm_calls": [{"route": "tro_ly_hue", "usd": 0.001}],
            "tools": [
                {"name": "tim_kho", "ms": 20.0},
                {"name": "ngay_lich", "ms": 0.0, "loai": "am"},
                {"name": "ngay_lich", "ms": 0.0, "loai": "am", "lap": True},
            ],
        },
        {
            "outcome": "max_turns",
            "route": "tro_ly_hue",
            "model": "gpt-6-luna",
            "usd": 0.002,
            "loi_kiem": None,
            "llm_calls": [{"route": "tro_ly_hue", "usd": 0.002}],
            "tools": [
                {"name": "tim_kho", "ms": 20.0, "by": "model"},
                {"name": "khoang_cach", "ms": 0.0},
                {"name": "khoang_cach", "ms": 0.0},
                {"name": "khoang_cach", "ms": 0.0},
            ],
        },
        {
            "outcome": "success",
            "route": "tro_ly_hue",
            "model": "gpt-6-luna",
            "usd": 0.0015,
            "loi_kiem": None,
            "cuu_max_turns": {"thanh_cong": True},
            "llm_calls": [{"route": "tro_ly_hue", "usd": 0.0015}],
            "tools": [
                {"name": "tim_kho", "ms": 15.0, "by": "model"},
                {"name": "viet_lai_het_luot", "ms": 100.0, "tu_choi": False},
                {"name": "cuu_max_turns", "ms": 120.0, "thanh_cong": True},
            ],
        },
        {
            "outcome": "retracted",
            "route": "tro_ly_hue",
            "model": "gpt-6-luna",
            "usd": 0.0005,
            "loi_kiem": "khong_trich_dan",
            "llm_calls": [{"route": "tro_ly_hue", "usd": 0.0005}],
            "tools": [],
        },
        {
            "outcome": "out_of_scope",
            "route": "ngoai_pham_vi",
            "model": None,
            "usd": 0.0001,
            "loi_kiem": None,
            "llm_calls": [{"route": "router", "usd": 0.0001}],
            "tools": [],
        },
        {
            "outcome": "success",
            "route": "tro_ly_hue",
            "model": "probe",
            "usd": 0.999,
            "llm_calls": [],
            "tools": [],
        },
    ]

    log_file = tmp_path / "sample.log"
    log_lines = [
        "[2026-11-27 11:00:00] INFO - api - Starting",
        f"[2026-11-27 11:00:01] INFO - chat - chat_metrics {json.dumps(rows[0])}",
        f"[2026-11-27 11:00:02] INFO - chat - chat_metrics {json.dumps(rows[1])}",
        "[2026-11-27 11:00:03] INFO - chat - chat_metrics {truncated_json",
        json.dumps(rows[2]),  # JSONL thuần xen kẽ vẫn đọc được
        json.dumps(rows[3]),
        json.dumps(rows[4]),
        json.dumps(rows[5]),
    ]
    log_file.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    parsed = doc_log(log_file)
    assert len(parsed) == 6
    filtered = loc_luot(parsed)
    assert len(filtered) == 5  # bỏ probe

    stats = tinh_quy_dao(filtered)
    assert stats["tong_luot"] == 5
    assert stats["phan_bo_route"] == {"tro_ly_hue": 4, "ngoai_pham_vi": 1}
    # Tool model theo từng lượt: [2, 4, 1, 0, 0] -> tổng 7, TB 1.4, p95 = 4.0
    assert stats["tong_goi_tool_model"] == 7
    assert stats["so_vong_tool_tb"] == 1.4
    assert stats["so_vong_tool_p95"] == 4.0
    assert stats["luot_co_lap"] == 1 and stats["so_lan_lap"] == 1 and stats["ty_le_lap"] == 0.2
    assert stats["luot_max_turns"] == 1 and stats["ty_le_max_turns"] == 0.2
    assert stats["luot_het_luot_viet_lai"] == 1 and stats["ty_le_het_luot_viet_lai"] == 0.2
    assert stats["luot_cuu_max_turns"] == 1 and stats["luot_cuu_max_turns_thanh_cong"] == 1 and stats["ty_le_cuu_max_turns"] == 0.2
    assert stats["luot_loi_kiem"] == 1 and stats["ty_le_loi_kiem"] == 0.2
    assert stats["luot_thanh_cong"] == 2
    assert stats["tong_usd"] == 0.0051
    assert stats["usd_moi_luot_thanh_cong"] == round(0.0051 / 2, 8)
    assert stats["usd_tb_luot_thanh_cong"] == round(0.0025 / 2, 8)
    assert stats["theo_tool"]["khoang_cach"]["goi"] == 3
    assert stats["theo_tool"]["ngay_lich"] == {"goi": 2, "lap": 1, "het_luot": 0}

    bang = dinh_dang_bang(stats)
    assert "Tổng lượt" in bang and "Tỉ lệ gọi lặp" in bang and "USD / lượt thành công" in bang


def test_cli_json_and_real_application_log_if_present(tmp_path, capsys):
    sample = tmp_path / "empty.jsonl"
    sample.write_text("", encoding="utf-8")
    assert main(["--log", str(sample), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["tong_luot"] == 0 and out["usd_moi_luot_thanh_cong"] is None

    if DEFAULT_LOG_PATH.is_file() and any(m.get("model") == "gpt-6-luna" for m in doc_log(DEFAULT_LOG_PATH)):
        assert main(["--log", str(DEFAULT_LOG_PATH), "--model", "gpt-6-luna", "--json"]) == 0
        real_stats = json.loads(capsys.readouterr().out)
        assert real_stats["tong_luot"] > 0 and "tro_ly_hue" in real_stats["phan_bo_route"]
