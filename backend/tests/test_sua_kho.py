"""Lệnh đề xuất / duyệt sửa kho khi một giá đổi (`ops/`). Model ở đây là phản hồi DỰNG SẴN (chỉ để dựng điều kiện) — các test này kiểm phần
code: tìm theo giá trị, thay đúng chuỗi số, file vá áp được bằng git, lệnh duyệt. Model phán đúng tới đâu trên kho thật: xem report của việc."""
import re
import socket
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
    (tmp_path / "README.md").write_text("dòng một\n", encoding="utf-8")
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


@pytest.mark.parametrize("dong, gia_cu, gia_moi, mong", [
    ("Giá vé là 250 nghìn đồng cho người lớn.", 250_000, 250_500, "Giá vé là 250.500 đồng cho người lớn."),
    ("Chi phí khoảng 1,5 triệu đồng/người.", 1_500_000, 1_555_000, "Chi phí khoảng 1.555.000 đồng/người."),
    ("Vé 250k đ một lượt", 250_000, 250_500, "Vé 250.500 đ một lượt"),
    ("Vé 250k VNĐ", 250_000, 250_500, "Vé 250.500 VNĐ"),
    ("Vé 250k một lượt", 250_000, 250_500, "Vé 250.500 đồng một lượt"),          # sau số không có chữ đơn vị tiền ⇒ vẫn viết đủ "đồng"
    ("Vé 250k, đồng thời tặng nước", 250_000, 250_500, "Vé 250.500 đồng, đồng thời tặng nước"),  # "đồng thời" không phải đơn vị tiền
    ("Chi phí khoảng 1,5 triệu đồng/người.", 1_500_000, 1_800_000, "Chi phí khoảng 1,8 triệu đồng/người."),  # viết được theo kiểu cũ ⇒ như trước
    # người đọc nhánh (C) bắt: bản đầu cấm chữ "thời" ở BẤT KỲ đâu phía sau ⇒ "… đồng trong thời gian lễ hội" vẫn ra "đồng đồng"
    ("Vé 250 nghìn đồng trong thời gian lễ hội.", 250_000, 250_500, "Vé 250.500 đồng trong thời gian lễ hội."),
    ("Vé 250 nghìn đồng mỗi người trong thời điểm cao điểm.", 250_000, 250_500, "Vé 250.500 đồng mỗi người trong thời điểm cao điểm."),
])
def test_gia_moi_le_don_vi_khong_lap_chu_dong(dong, gia_cu, gia_moi, mong):
    """Soát khác hãng 22/11 (Gemini, điểm 2): dòng kho viết "<số> nghìn / triệu đồng", giá mới không tròn theo đơn vị đó ⇒ code viết đủ số kèm
    "đồng" rồi giữ nguyên chữ "đồng" sẵn có phía sau ⇒ "250.500 đồng đồng" vào kho."""
    assert sua_kho.dong_moi(dong, sua_kho.quet_bai("a.md", dong, gia_cu), gia_moi) == mong


def test_model_bo_sot_bia_ma_hoac_tra_hai_lan_thi_khong_vao_file_va():
    cac_lan = sua_kho.quet_bai("a.md", "# A\n\nThành Mẫu 200.000\n\nLăng B 200.000\n\nQuán C 200.000\n\n## Nguồn dữ liệu\n\n- Vé 200.000 (đối chiếu ngày 1/1/2026): x", 200_000)
    for n, lan in enumerate(cac_lan, 1):
        lan.ma = f"c{n}"
    assert cac_lan[3].trong_muc_nguon
    tra = sua_kho.KetQuaPhanDoan(cac_cho=[sua_kho.PhanDoanMotCho(ma=m, phan_doan=p, ly_do="x") for m, p in
                                           [("c1", "dung"), ("c2", "dung"), ("c2", "khong"), ("c9", "dung"), ("c4", "dung")]])
    cac_lan[3].phan_doan = cac_lan[3].code_tu_xep[0]  # như `phan_doan` làm trước khi gọi model
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


@pytest.mark.parametrize("tham_so_thu", [["--thu"], ["--collection-thu", "thu_col", "--ban-ghi-thu", "ban_ghi_thu"]])
def test_thu_ma_quen_goc_thi_khong_cham_kho_cua_repo_chua_code(repo, monkeypatch, tham_so_thu):
    """Review E 22/11 (F1): `--thu` không kèm `--goc` từng áp file vá vào kho của chính repo chứa code rồi in "Chế độ thử". Soát khác hãng 22/11
    (Gemini, điểm 1): cùng kiểu quên `--goc` với cặp `--collection-thu` / `--ban-ghi-thu` từng áp + LƯU BẢN GHI GIT vào kho của repo chứa code
    rồi chỉ cập nhật collection thử."""
    from ingestion import cap_nhat_rieng
    _, ra, _ = de_xuat(repo, monkeypatch)
    monkeypatch.setattr(duyet_sua_kho, "GOC_REPO", repo)  # coi repo tạm là repo chứa code ⇒ `--goc` mặc định trỏ vào nó
    monkeypatch.setattr(cap_nhat_rieng, "dong_bo", lambda **k: {"da_khop": True, "bai_doi": [], "so_doan_tinh_lai": 0, "giay": 0})  # không chạm Qdrant
    assert duyet_sua_kho.main([str(ra), *tham_so_thu]) == 2
    assert git(repo, "status", "--porcelain", "--", "knowledge-base-hue") == "" and git(repo, "log", "--oneline").count("\n") == 1


def test_file_va_co_them_file_ngoai_de_xuat_thi_khong_ap(repo, monkeypatch):
    """Review E 22/11 (F3): file vá bị nối thêm một đoạn sửa file ngoài danh sách bài của đề xuất ⇒ dừng, không áp gì."""
    _, ra, _ = de_xuat(repo, monkeypatch)
    with (ra / "de_xuat.patch").open("a", encoding="utf-8") as f:
        f.write("--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n-dòng một\n+dòng lạ\n")
    assert duyet_sua_kho.main([str(ra), "--goc", str(repo), "--thu"]) == 2
    assert git(repo, "status", "--porcelain") .replace("?? de_xuat/\n", "") == ""


def test_con_so_trong_tieu_de_muc_duoc_liet_ke_va_khong_tu_sua():
    """Review E 22/11 (F4): số trong dòng tiêu đề từng không vào nhóm nào. Nay: có trong danh sách, xếp cứng "không rõ", không hỏi model."""
    cac_lan = sua_kho.quet_bai("a.md", "# A\n\n## Vé Thành Mẫu 200.000 đồng\n\nThành Mẫu 200.000\n", 200_000)
    assert [(x.so_dong, x.la_tieu_de) for x in cac_lan] == [(3, True), (5, False)]
    for n, lan in enumerate(cac_lan, 1):
        lan.ma = f"c{n}"
    model = ModelDungSan()
    import asyncio
    asyncio.run(sua_kho.phan_doan(model, "vé Thành Mẫu", 200_000, cac_lan, None, 5))
    assert [x.phan_doan for x in cac_lan] == ["khong_ro", "dung"] and model.da_nhan[0].count("⟦") == 1


def test_duyet_dung_khi_bai_dang_co_thay_doi_chua_luu_ban_ghi_git(repo, monkeypatch, capsys):
    """Soát khác hãng 22/11 (điểm 1): bài đã có một sửa đổi CHƯA lưu bản ghi git từ TRƯỚC lúc lập đề xuất ⇒ mã băm vẫn khớp, lệnh duyệt áp giá rồi
    `git commit -- <bài>` lưu CẢ sửa đổi đó — thứ người duyệt chưa hề đọc. Nay: dừng trước khi áp; chế độ thử (không lưu bản ghi) không bị chặn."""
    bai = repo / "knowledge-base-hue" / "travel" / "tickets" / "Vé tham quan.md"
    bai.write_text(VE.replace("Vườn Đông | 150.000", "Vườn Đông | 999.000"), encoding="utf-8")  # sửa dở, chưa commit, có từ trước lúc đề xuất
    _, ra, _ = de_xuat(repo, monkeypatch)
    assert duyet_sua_kho.main([str(ra), "--goc", str(repo)]) == 2
    assert "200.000 | 40.000" in bai.read_text(encoding="utf-8")       # chưa áp gì
    assert git(repo, "log", "--oneline").count("\n") == 1              # không có bản ghi git mới
    assert "chưa lưu bản ghi git" in capsys.readouterr().err


def test_duyet_dung_truoc_khi_ap_khi_cong_server_con_mo(repo, monkeypatch, capsys):
    """Soát khác hãng 22/11 (điểm 4): đường duyệt gọi thẳng lệnh cập nhật chỉ mục nên từng bỏ qua cả lời cảnh báo cổng; server còn chạy thì trả
    lời trên chỉ mục đang ghi dở. Nay: dò cổng TRƯỚC khi áp — kho chưa đổi, chỉ mục chưa bị đọc hay ghi."""
    from ingestion import cap_nhat_rieng
    _, ra, _ = de_xuat(repo, monkeypatch)
    monkeypatch.setattr(duyet_sua_kho, "GOC_REPO", repo)  # coi repo tạm là repo của server ⇒ đường duyệt THẬT (không collection thử)
    monkeypatch.setattr(cap_nhat_rieng, "dong_bo", lambda **k: pytest.fail("không được chạm chỉ mục khi server còn chạy"))
    with socket.socket() as o:  # một cổng thật đang nghe đóng vai cổng server
        o.bind(("127.0.0.1", 0))
        o.listen()
        monkeypatch.setattr(cap_nhat_rieng, "CONG_SERVER", o.getsockname()[1])
        assert duyet_sua_kho.main([str(ra)]) == 3
    assert git(repo, "status", "--porcelain", "--", "knowledge-base-hue") == "" and git(repo, "log", "--oneline").count("\n") == 1
    assert "server đang chạy" in capsys.readouterr().err


def test_gia_nam_trong_bang_ma_file_dieu_kien_chep_thi_de_xuat_bao_va_duyet_dung(repo, monkeypatch, capsys):
    """Soát khác hãng 22/11 (Gemini Carbon, điểm 1): file điều kiện của bộ chia đoạn chép nguyên văn cả BẢNG GIÁ ở `targets[*].exact_text`; phép dò cũ
    chỉ đọc `condition.exact_text` ⇒ bản đề xuất không báo, lệnh duyệt áp + lưu bản ghi git rồi bước chia đoạn mới báo lỗi (kho đã sửa, chỉ mục cũ).
    Nay: bản đề xuất nêu tên bài; lệnh duyệt DỪNG trước khi áp (bài và file điều kiện phải đổi cùng lúc — lệnh này không sửa file điều kiện)."""
    import json
    bang = "| Điểm | Người lớn | Trẻ em |\n|---|---|---|\n| **Thành Mẫu** | 200.000 | 40.000 |\n| Vườn Đông | 150.000 | 30.000 |"
    assert bang in VE
    meta = repo / "knowledge-base-hue" / "meta"
    meta.mkdir()
    (meta / "full_corpus_conditions.json").write_text(json.dumps([{
        "source": "travel/tickets/Vé tham quan.md",
        "condition": {"heading_path": ["Vé mẫu", "Vé lẻ"], "block_type": "paragraph", "exact_text": "Giá áp dụng cho khách đi lẻ."},
        "targets": [{"heading_path": ["Vé mẫu", "Vé lẻ"], "block_type": "table", "exact_text": bang}]}], ensure_ascii=False), encoding="utf-8")
    _, ra, _ = de_xuat(repo, monkeypatch)
    assert "full_corpus_conditions.json" in (ra / "DE_XUAT.md").read_text(encoding="utf-8").split("## 4.")[1]
    assert duyet_sua_kho.main([str(ra), "--goc", str(repo)]) == 2
    assert git(repo, "status", "--porcelain", "--", "knowledge-base-hue/travel") == "" and git(repo, "log", "--oneline").count("\n") == 1
    loi = capsys.readouterr().err
    assert "knowledge-base-hue/meta/full_corpus_conditions.json" in loi and "200.000 ⇒ 250.000" in loi and "TẮT server, rồi từ `backend/`" in loi
