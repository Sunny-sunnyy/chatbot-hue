"""Lệnh đề xuất / duyệt sửa kho khi một giá đổi (`ops/`). Model ở đây là phản hồi DỰNG SẴN (chỉ để dựng điều kiện) — các test này kiểm phần
code: tìm theo giá trị, thay đúng chuỗi số, file vá áp được bằng git, lệnh duyệt. Model phán đúng tới đâu trên kho thật: xem report của việc."""
import re
import subprocess
from types import SimpleNamespace

import pytest

from ops import de_xuat_sua_kho, duyet_sua_kho, sua_kho

VE = """# Vé mẫu

## Vé lẻ

| Điểm | Người lớn | Trẻ em |
|---|---|---|
| **Thành Mẫu** | 200.000 | 40.000 |
| Vườn Đông | 150.000 | 30.000 |

## Vé gộp

- **Tuyến Vườn Đông – Vườn Tây:**
  - Người lớn: 200.000 đồng/người/tuyến
- Ghép vé Thành Mẫu (200.000 đồng) với vé một vườn (150.000 đồng) thì tổng là 350.000 đồng.
- Ghép tất cả các điểm thì tổng là 1.200.000 đồng.

## Nguồn dữ liệu

- Biểu giá mẫu (đối chiếu ngày 01/02/2026): https://vi-du.example/bieu-gia
"""
NHA_HAT = "# Nhà hát\n\nChưa gồm vé vào Thành Mẫu 200k; vé xem hát 300.000 đồng."  # không có mục nguồn, không xuống dòng cuối file


def git(goc, *lenh):
    return subprocess.run(["git", "-C", str(goc), *lenh], capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path):
    kho = tmp_path / "knowledge-base-hue" / "travel" / "tickets"
    kho.mkdir(parents=True)
    (kho / "Vé tham quan.md").write_text(VE, encoding="utf-8")
    (kho / "Nhà hát.md").write_bytes(NHA_HAT.encode())
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", "-A")
    git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "kho")
    return tmp_path


class ModelDungSan:
    """Phán "đúng" khi dòng đang xét có chữ Thành Mẫu, còn lại "không"; ghi lại chữ đã nhận để test đọc."""
    model, responses_model = "model-dung-san", None

    def __init__(self):
        self.da_nhan = []

    async def _run(self, agent, prompt, call_log, timeout):
        self.da_nhan.append(prompt)
        cho = [sua_kho.PhanDoanMotCho(ma=ma, phan_doan="dung" if "Thành Mẫu" in dong else "khong", ly_do="dòng nêu tên nơi")
               for ma, dong in re.findall(r"^\[(c\d+)\].*?^Dòng: (.*?)$", prompt, flags=re.S | re.M)]
        return SimpleNamespace(final_output=sua_kho.KetQuaPhanDoan(cac_cho=cho))


def de_xuat(repo, monkeypatch, model=None):
    model = model or ModelDungSan()
    monkeypatch.setattr("llm.generator_openai_full_corpus.OpenAIFullCorpusGenerator.from_environment", classmethod(lambda cls, s: model))
    ra = repo / "de_xuat"
    ma = de_xuat_sua_kho.main(["--gia", "Vé vào cổng Thành Mẫu, người lớn", "--cu", "200.000", "--moi", "250.000", "--nguon", "https://vi-du.example/moi",
                               "--goc", str(repo), "--ra", str(ra)])
    return ma, ra, model


def test_tim_theo_gia_tri_khong_theo_chu():
    dong = "tổng 1.200.000 đồng; vé 200.000đ; ô bảng | 200.000 |; 200k; 200 nghìn; 200,000 VND; 200.000 tờ văn bản; 2.200.000; 200.0005"
    assert [m.group(0) for m in sua_kho.tim_trong_dong(dong, 200_000)] == ["200.000", "200.000", "200k", "200 nghìn", "200,000", "200.000"]
    assert sua_kho.doc_gia("200k") == sua_kho.doc_gia("200.000 đồng") == sua_kho.doc_gia("200000") == 200_000
    with pytest.raises(ValueError):
        sua_kho.doc_gia("hai trăm")
    assert sua_kho.ten_rieng("Vé vào cổng Thành Mẫu, người lớn") == ["Thành Mẫu"] and sua_kho.ten_rieng("vé Lăng Tự Đức và Cung An Định") == ["Lăng Tự Đức", "Cung An Định"]
    assert sua_kho.ten_rieng("Vé thuyền trên sông Hương") == []  # một chữ viết hoa lẻ không đủ chắc để lọc


@pytest.mark.parametrize("so, dv, moi, mong", [
    ("200.000", None, 250_000, ("250.000", False)), ("200,000", None, 250_000, ("250,000", False)), ("200000", None, 250_000, ("250000", False)),
    ("200", "k", 250_000, ("250", False)), ("200", " nghìn", 250_500, ("250.500 đồng", True)),
    ("1,2", " triệu", 1_500_000, ("1,5", False)), ("1,2", " triệu", 2_000_000, ("2", False)),
])
def test_viet_lai_giu_kieu_viet_cu(so, dv, moi, mong):
    assert sua_kho.viet_lai(so, dv, moi) == mong


def test_mot_dong_hai_lan_chi_thay_lan_duoc_duyet():
    cac_lan = sua_kho.quet_bai("a.md", "Lăng A 200.000 đồng, Thành Mẫu 200.000 đồng", 200_000)
    assert len(cac_lan) == 2
    assert sua_kho.dong_moi(cac_lan[0].dong, cac_lan[1:], 250_000) == "Lăng A 200.000 đồng, Thành Mẫu 250.000 đồng"


def test_model_bo_sot_bia_ma_hoac_tra_hai_lan_thi_khong_vao_file_va():
    cac_lan = sua_kho.quet_bai("a.md", "# A\n\nThành Mẫu 200.000\n\nLăng B 200.000\n\nQuán C 200.000\n\n## Nguồn dữ liệu\n\n- Vé 200.000 (đối chiếu ngày 1/1/2026): x", 200_000)
    for n, lan in enumerate(cac_lan, 1):
        lan.ma = f"c{n}"
    assert cac_lan[3].trong_muc_nguon
    tra = sua_kho.KetQuaPhanDoan(cac_cho=[sua_kho.PhanDoanMotCho(ma=m, phan_doan=p, ly_do="x") for m, p in
                                           [("c1", "dung"), ("c2", "dung"), ("c2", "khong"), ("c9", "dung"), ("c4", "dung")]])
    cac_lan[3].phan_doan = "khong"  # như `phan_doan` làm trước khi gọi model
    dieu_la = sua_kho.gan_phan_doan(cac_lan, tra)
    assert [x.phan_doan for x in cac_lan] == ["dung", "khong_ro", "khong_ro", "khong"]  # c2 hai phán đoán · c3 bỏ sót · dòng nguồn không cho model đổi
    assert len(dieu_la) == 4  # c2 trái nhau · c9 bịa · c4 (dòng nguồn, không nằm trong danh sách hỏi) · c3 bỏ sót


def test_de_xuat_khong_ghi_kho_va_file_va_chi_cham_dung_cho(repo, monkeypatch):
    ma, ra, model = de_xuat(repo, monkeypatch)
    assert ma == 0 and git(repo, "status", "--porcelain", "--", "knowledge-base-hue") == ""  # lệnh đề xuất không ghi kho
    assert len(model.da_nhan) == 1 and model.da_nhan[0].count("⟦") == 4  # một lời gọi; bốn lần xuất hiện, số 1.200.000 không phải ứng viên
    assert "Tuyến Vườn Đông – Vườn Tây" in model.da_nhan[0]  # dòng cha của "Người lớn: 200.000" có trong chữ gửi model
    git(repo, "apply", str(ra / "de_xuat.patch"))
    khac = [d for d in git(repo, "diff", "-U0", "--", "knowledge-base-hue").splitlines() if d[:1] in "+-" and d[:3] not in ("+++", "---")]
    assert khac == [
        "-Chưa gồm vé vào Thành Mẫu 200k; vé xem hát 300.000 đồng.",
        "+Chưa gồm vé vào Thành Mẫu 250k; vé xem hát 300.000 đồng.",
        "+", "+## Nguồn dữ liệu", "+", "+- Giá vé vào cổng Thành Mẫu, người lớn: 250.000 đồng (đối chiếu ngày " + khac[5].split("ngày ")[1],
        "-| **Thành Mẫu** | 200.000 | 40.000 |", "+| **Thành Mẫu** | 250.000 | 40.000 |",
        "-- Ghép vé Thành Mẫu (200.000 đồng) với vé một vườn (150.000 đồng) thì tổng là 350.000 đồng.",
        "+- Ghép vé Thành Mẫu (250.000 đồng) với vé một vườn (150.000 đồng) thì tổng là 350.000 đồng.",
        "+- Giá vé vào cổng Thành Mẫu, người lớn: 250.000 đồng (đối chiếu ngày " + khac[5].split("ngày ")[1],
    ]
    ban = (ra / "DE_XUAT.md").read_text(encoding="utf-8")
    assert "Sẽ sửa: 3 chỗ ở 2 bài" in ban and "Không phải giá này: 1 chỗ" in ban
    assert "350.000" in ban.split("Bạn sửa tay nếu cần")[1].split("\n")[0]  # dòng có tổng tính từ giá cũ được đánh dấu
    assert "tổng là 1.200.000" in ban.split("## 4.")[1]  # câu tổng khác trong bài được nhắc xem lại
    # bảng ngoài kho chép nguyên văn một câu vừa bị sửa ⇒ bị nêu tên; câu chép không đổi ⇒ không
    bang = repo / "bang.json"
    bang.write_text('{"dong": [{"chu": "| **Thành Mẫu** | 200.000 | 40.000 |"}, {"chu": "| Vườn Đông | 150.000 | 30.000 |"}]}', encoding="utf-8")
    bai = "travel/tickets/Vé tham quan.md"
    moi = (repo / "knowledge-base-hue" / bai).read_text(encoding="utf-8")
    assert sua_kho.cau_chep_bi_doi(bang, {bai: VE}, {bai: moi}) == [(bai, "| **Thành Mẫu** | 200.000 | 40.000 |")]


def test_duyet_thu_ap_dung_va_tu_choi_khi_bai_da_doi(repo, monkeypatch, capsys):
    _, ra, _ = de_xuat(repo, monkeypatch)
    bai = repo / "knowledge-base-hue" / "travel" / "tickets" / "Vé tham quan.md"
    goc = bai.read_text(encoding="utf-8")
    bai.write_text(goc.replace("Vườn Đông | 150.000", "Vườn Đông | 160.000"), encoding="utf-8")  # kho đổi sau khi lập đề xuất
    assert duyet_sua_kho.main([str(ra), "--goc", str(repo), "--thu"]) == 2
    assert "200.000 | 40.000" in bai.read_text(encoding="utf-8")  # không áp gì
    bai.write_text(goc, encoding="utf-8")
    assert duyet_sua_kho.main([str(ra), "--goc", str(repo), "--thu"]) == 0
    assert "250.000 | 40.000" in bai.read_text(encoding="utf-8") and "Người lớn: 200.000 đồng/người/tuyến" in bai.read_text(encoding="utf-8")
    assert git(repo, "log", "--oneline").count("\n") == 1  # chế độ thử không tạo bản ghi git
    assert duyet_sua_kho.main([str(ra), "--goc", str(repo), "--thu"]) == 2  # duyệt lần hai: bài đã khác lúc đề xuất ⇒ từ chối
