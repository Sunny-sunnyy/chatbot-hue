"""Trang theo dõi (plan `report_agent/2026-11-20/e_trang_theo_doi_plan.md`) — hàm gom theo ngày + rào khoá của `GET /api/theo_doi`. 0 USD, không model,
không Qdrant. Dòng log trong test tự dựng (đúng dạng dòng `chat_metrics` thật); khoá trong test là khoá giả."""
import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import theo_doi as td

KHOA_GIA = "khoa-gia-chi-dung-trong-test-0123"


def _dong(ngay: str, **m) -> str:
    goc = {"outcome": "success", "model": "gpt-x", "refusal": False, "usd": 0.001, "total_ms": 4000, "git_sha": "aaaa1111"}
    return f"[{ngay} 10:00:00] INFO - chat - chat_metrics {json.dumps({**goc, **m})}\n"


LOG = [
    "[2026-11-19 09:00:00] INFO - api - Full-corpus retrieval service started successfully\n",       # không phải dòng số đo
    _dong("2026-11-19"),                                                                                # trả lời từ kho
    _dong("2026-11-19", refusal=True, usd=0.0005, total_ms=2000),                                       # từ chối
    _dong("2026-11-19", refusal=True, has_web_section=True, usd=0.002, total_ms=9000),                  # có mục web
    _dong("2026-11-19", outcome="out_of_scope", model=None, usd=0.0001, total_ms=1000),                 # ngoài phạm vi
    _dong("2026-11-19", model="probe", usd=0),                                                          # model giả của test ⇒ bỏ
    _dong("2026-11-20", lich_trinh_ok=True, usd=0.003, total_ms=20000, git_sha="bbbb2222"),             # lượt lịch
    _dong("2026-11-20", sua_lich={"n_ap": 1}, usd=0.0002, total_ms=3000, git_sha="bbbb2222"),           # lượt sửa lịch
    _dong("2026-11-20", cache="trung", model=None, usd=0, total_ms=1, git_sha="cccc3333"),              # trúng bản lưu
    _dong("2026-11-20", cache="truot", git_sha="cccc3333"),                                             # tra bản lưu trượt ⇒ lượt thường
    _dong("2026-11-20", outcome="generation_failed", model=None, usd=0, total_ms=50, git_sha="cccc3333"),  # lỗi
    '[2026-11-20 11:00:00] INFO - chat - chat_metrics {"outcome": "success", "mod',                    # dòng cắt dở khi log xoay vòng
]


def test_daily_summary_puts_every_turn_in_exactly_one_column():
    kq = td.tong_hop(LOG)
    assert kq["bo_model_gia"] == 1 and kq["bo_dong_hong"] == 1
    hom_nay, hom_qua = kq["ngay"]  # ngày mới nhất trước
    assert hom_nay == {"ngay": "2026-11-20", "luot": 5, "tra_loi": 1, "tu_choi": 0, "ngoai_pham_vi": 0, "web": 0, "lich": 2, "cache": 1, "loi": 1,
                       "usd": 0.0042, "p50_ms": 4000, "p95_ms": 20000, "git_sha": "cccc3333"}  # độ trễ của 4 lượt không lỗi [1, 3000, 4000, 20000] ms, cùng phép chọn như `scripts/dem_chat_metrics.py`; mã bản = lượt gần nhất
    assert hom_qua == {"ngay": "2026-11-19", "luot": 4, "tra_loi": 1, "tu_choi": 1, "ngoai_pham_vi": 1, "web": 1, "lich": 0, "cache": 0, "loi": 0,
                       "usd": 0.0036, "p50_ms": 4000, "p95_ms": 9000, "git_sha": "aaaa1111"}
    for hang in kq["ngay"]:
        assert hang["luot"] == sum(hang[c] for c in td.COT)
    assert [h["ngay"] for h in td.tong_hop(LOG, so_ngay=1)["ngay"]] == ["2026-11-20"]  # chỉ giữ N ngày gần nhất


def test_response_carries_only_daily_numbers_never_a_single_turn():
    # dòng log thật có `turn_id` (mã lượt ngẫu nhiên) ⇒ không được đi ra trang; phản hồi chỉ gồm các khoá đã liệt kê
    kq = td.tong_hop([_dong("2026-11-20", turn_id="ma-luot-bi-mat", today="2026-11-20")])
    assert set(kq) == {"ngay", "bo_model_gia", "bo_dong_hong"}
    assert set(kq["ngay"][0]) == {"ngay", "luot", *td.COT, "usd", "p50_ms", "p95_ms", "git_sha"}
    assert "ma-luot-bi-mat" not in json.dumps(kq)


def test_rotated_files_are_read_oldest_first_and_missing_ones_skipped(tmp_path):
    (tmp_path / "application.log.2").write_text(_dong("2026-11-18", git_sha="cu"), encoding="utf-8")
    (tmp_path / "application.log").write_text(_dong("2026-11-18", git_sha="moi"), encoding="utf-8")
    kq = td.tong_hop(td.doc_log(tmp_path))
    assert kq["ngay"][0]["luot"] == 2 and kq["ngay"][0]["git_sha"] == "moi"


def test_route_is_off_without_a_key_and_refuses_a_wrong_one(tmp_path, monkeypatch, caplog):
    (tmp_path / "application.log").write_text("".join(LOG), encoding="utf-8")
    monkeypatch.setattr(td, "LOGS_DIR", tmp_path)
    monkeypatch.setattr(td, "doc_log", lambda thu_muc=tmp_path, _goc=td.doc_log: _goc(thu_muc))
    app = FastAPI()
    app.include_router(td.router)
    client = TestClient(app)
    monkeypatch.delenv(td.KHOA_ENV, raising=False)
    assert client.get("/api/theo_doi", headers={td.KHOA_HEADER: KHOA_GIA}).status_code == 404   # chưa đặt khoá ⇒ như đường không tồn tại
    monkeypatch.setenv(td.KHOA_ENV, "ngan")
    assert client.get("/api/theo_doi", headers={td.KHOA_HEADER: "ngan"}).status_code == 404     # khoá quá ngắn ⇒ vẫn tắt
    monkeypatch.setenv(td.KHOA_ENV, KHOA_GIA)
    for sai in ({}, {td.KHOA_HEADER: ""}, {td.KHOA_HEADER: KHOA_GIA[:-1]}, {td.KHOA_HEADER: KHOA_GIA + "x"}):
        r = client.get("/api/theo_doi", headers=sai)
        assert r.status_code == 403 and "ngay" not in r.json() and "luot" not in r.text
    assert client.get(f"/api/theo_doi?khoa={KHOA_GIA}").status_code == 403                       # khoá trong URL không được nhận
    with caplog.at_level("DEBUG"):
        dung = client.get("/api/theo_doi", headers={td.KHOA_HEADER: KHOA_GIA})
    assert dung.status_code == 200 and [h["luot"] for h in dung.json()["ngay"]] == [5, 4] and dung.json()["so_ngay"] == td.SO_NGAY
    assert KHOA_GIA not in caplog.text and KHOA_GIA not in dung.text                              # khoá không vào log, không vọng lại trong phản hồi
