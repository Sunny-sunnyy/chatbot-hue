"""Sửa lịch bằng lời trên lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-sua-lich-v2-plan.md`; giữ D1–D11 của plan 05/11).

Model chọn **hành động có tên** (`HanhDong`); **code** áp tối đa `MAX_AP` / lượt. Mỗi hành động = một lần **xếp lại** bằng `xep_v2` với
`giu` (mọi điểm ban ngày không bị chạm giữ đúng ngày / buổi) + `loai` (điểm đã bỏ không quay lại) — giờ gợi ý, luật cụm, quỹ phút, mùa, mưa
đều do đúng một bộ xếp tính; khung mới chỉ được nhận khi `kiem_khung_v2` = 0 lỗi, không thì giữ khung cũ + lý do. Hàm thuần — không mạng,
không SDK. Trạng thái lưu của cuộc (`luu`): {tham_so, ngay_di, mua, khung, loai} — chỉ dữ liệu code dựng (không chữ người dùng).
"""
import collections
import copy
import re
import unicodedata
import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from llm import lich_trinh_v2 as v2
from llm.do_so import ngay_tu_cau
from llm.hoi_lai import NGAY_DI_TOI_DA
from llm.lich_trinh import chuan_ten

MAX_AP = 2
MAX_HANH_DONG = 3  # ý thứ 3 trở đi ⇒ "Chưa làm"
MAX_LUA_CHON = 3
SoThich = Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"]


class HanhDong(BaseModel):
    """Một hành động sửa. `ten` = điểm bị chạm (bỏ / thêm / thay / dời); `ten_moi` = điểm thay vào; `ngay` / `buoi` = chỗ muốn đặt.
    `doi_tham_so` chỉ mang trường người dùng nói muốn đổi. `doi_hang_o` (plan 2026-11-15-sua-lich-hang-cho-o): `ngan_sach` = mức hạng chỗ ở
    người dùng NÊU RÕ; xin đổi hạng mà không nêu hạng ⇒ để trống ⇒ code nói "bạn nói rõ hạng" (không đoán mức).
    `doi_ngay_di` (plan 2026-11-15-sua-lich-ngay-di) KHÔNG có trường: ngày do code đọc từ chữ người dùng (`ngay_di_moi`) — model không viết ngày."""
    model_config = ConfigDict(extra="forbid")
    loai: Literal["bo_diem", "them_diem", "thay_diem", "doi_buoi", "doi_so_ngay", "doi_tham_so", "doi_hang_o", "doi_ngay_di"]
    ten: str | None = Field(default=None, max_length=80)
    ten_moi: str | None = Field(default=None, max_length=80)
    ngay: int | None = Field(default=None, ge=1, le=5)
    buoi: Literal["sang", "chieu"] | None = None
    so_ngay: int | None = Field(default=None, ge=1, le=5)
    kieu_di: Literal["nhe_nhang", "can_bang", "kham_pha"] | None = None
    so_thich: list[SoThich] | None = Field(default=None, max_length=2)
    tre_em: int | None = Field(default=None, ge=0, le=6)  # "đi cùng trẻ nhỏ" ⇒ ≥ 1; "không có trẻ em" ⇒ 0
    lon_tuoi: bool | None = None  # "có người lớn tuổi"
    ngan_sach: Literal["binh_dan", "vua", "cao"] | None = None  # khoá của `luu_tru_lich.MUC_NGAN_SACH`


class HanhDongCHT(HanhDong):
    """Cờ `sua_lich_chua_ho_tro` (plan 2026-11-17-chua-ho-tro-plan.md): thêm `chua_ho_tro` — MODEL nhận "câu sửa lịch mà bộ hành động chưa làm
    được" (đổi chỗ / gộp / tách ngày, dời giờ cả lịch…). Không trường nào: câu hiện ra do code viết. Cờ tắt ⇒ khuôn `HanhDong` cũ (giống byte)."""
    loai: Literal["bo_diem", "them_diem", "thay_diem", "doi_buoi", "doi_so_ngay", "doi_tham_so", "doi_hang_o", "doi_ngay_di", "chua_ho_tro"]


class HanhDongToi(HanhDongCHT):
    """Cờ `sua_lich_buoi_toi` (21/11/2026): `buoi` có thêm "toi" để model NÓI LẠI ĐƯỢC điều người dùng nói. Khuôn chỉ có sáng / chiều ⇒ câu "dời X sang
    buổi tối" không có cách ghi đúng: Sonnet để trống buổi (người dùng thấy "Chưa rõ ngày / buổi" dù họ nói rõ — 5 / 9 lượt thật), luna đổi thành
    "chiều" (2 / 9). Xếp được vào buổi tối hay không vẫn do CODE quyết và trả lời (`ap`). Cờ tắt ⇒ khuôn `HanhDongCHT` cũ (giống byte)."""
    buoi: Literal["sang", "chieu", "toi"] | None = None


class HanhDongHoi(HanhDongCHT):
    """Cờ `sua_lich_kem_hoi` (21/11/2026): thêm `hoi_them` — MODEL báo "ngoài ý sửa lịch, tin này còn hỏi một thông tin". Không trường nào: hành động này
    không sửa gì, code chỉ dùng nó để thêm MỘT dòng cố định vào khối thay đổi (`CAU_HOI_THEM`). Vì sao: người dùng mô phỏng 21/11 — 4 / 4 tin vừa sửa
    lịch vừa hỏi, cả hai model: lịch được sửa, phần hỏi bị bỏ không một lời, người dùng phải hỏi tới lần ba. Cờ tắt ⇒ khuôn `HanhDongCHT` cũ (giống byte)."""
    loai: Literal["bo_diem", "them_diem", "thay_diem", "doi_buoi", "doi_so_ngay", "doi_tham_so", "doi_hang_o", "doi_ngay_di", "chua_ho_tro", "hoi_them"]


class HanhDongToiHoi(HanhDongToi):
    """Hai cờ `sua_lich_buoi_toi` + `sua_lich_kem_hoi` cùng bật: khuôn buổi tối có thêm `hoi_them`."""
    loai: Literal["bo_diem", "them_diem", "thay_diem", "doi_buoi", "doi_so_ngay", "doi_tham_so", "doi_hang_o", "doi_ngay_di", "chua_ho_tro", "hoi_them"]


class HanhDongToiHoiBo(HanhDongToiHoi):
    """Công tắc `bo_toi_hoi_lai` (23/11/2026; chủ dự án: bỏ hoạt động tối thì "nên hỏi lại người dùng đổi hoạt động hay là để trống"): `cach_toi` để
    model NÓI LẠI ĐƯỢC người dùng muốn gì với BUỔI TỐI vừa bị bỏ — "doi" = đổi sang hoạt động tối khác, "de_trong" = để trống tối đó; họ không nói ⇒
    trường để trống ⇒ CODE hỏi lại (`ap`), không tự chọn. Chỉ có nghĩa với `bo_diem` một hoạt động buổi tối. Công tắc tắt ⇒ khuôn cũ (giống byte)."""
    cach_toi: Literal["doi", "de_trong"] | None = None


CHUA_HO_TRO = "chua_ho_tro"
HOI_THEM = "hoi_them"
# Bắt đầu bằng "Chưa làm" ⇒ giao diện hiện đúng kiểu dòng chưa làm, không gắn tiền tố "Không đổi được" (`frontend/src/LichV2.jsx` `ThayDoi`).
CAU_HOI_THEM = ("Chưa làm: phần câu hỏi trong tin này mình chưa trả lời — lượt này mình chỉ sửa lịch. Bạn gửi riêng câu hỏi đó, mình trả lời ngay.")
NHAN_HANH_DONG = {"bo_diem": "bỏ điểm", "them_diem": "thêm điểm", "thay_diem": "thay điểm", "doi_buoi": "dời buổi",
                  "doi_so_ngay": "đổi số ngày", "doi_tham_so": "đổi kiểu lịch", "doi_hang_o": "đổi hạng chỗ ở", "doi_ngay_di": "đổi ngày đi"}
CAU_VIEC_KHAC = ("Chưa làm: đổi chỗ, gộp hay tách các ngày — mình chưa sửa được kiểu này trên lịch. Mình sửa được từng điểm (bỏ, thêm, thay, "
                 "dời sang buổi / ngày khác); bạn nói cụ thể điểm muốn đổi nhé.")
CAU_CHUA_HO_TRO = ("Chưa làm: việc này mình chưa sửa được trên lịch — lịch giữ nguyên. Mình sửa được từng điểm (bỏ, thêm, thay, dời sang "
                   "buổi / ngày khác) hoặc đổi số ngày, kiểu đi, sở thích, ngày đi, hạng chỗ ở; bạn nói cụ thể nhé.")
NHAN_BUOI = {"sang": "sáng", "chieu": "chiều", "toi": "tối"}
# Dời một điểm bị từ chối (đếm 20/11: 152 / 176 lần dời thử bị từ chối, mọi ca cùng một câu chung): mã `kiem_khung_v2` của khung thử ⇒ MỘT lý do
# lời thường. Nói ở mức cả lịch — bộ kiểm chỉ trả mã, không trả ngày, và lỗi có thể nằm ở ngày của điểm bị đổi chỗ. Thứ tự xét: khu > kín > giờ mở.
MA_LUAT_KHU = {"cum_khong_ke", "qua_2_cum", "ghep_khong_ke", "cum_xa"}
MA_LUAT_KIN = {"qua_day_buoi", "vuot_quy", "sang_chong_chieu", "gio_chong", "han_che_qua_day", "day_qua_gio"}
CAU_LY_DO = {"khu": "một ngày sẽ phải đi hai khu không liền nhau", "kin": "lịch sẽ có buổi quá kín hoặc quá giờ",
             "gio_mo": "điểm sẽ rơi ngoài giờ mở cửa",
             "ban_ngay": "đây là điểm tham quan ban ngày, còn buổi tối lịch chỉ xếp hoạt động buổi tối"}  # cờ `sua_lich_buoi_toi`
# Lý do riêng của "đổi chỗ hai ngày" (đếm 20/11 trên 15.360 cặp: 1.346 ca bị chặn đều vì điểm khu xa rơi vào ngày 1; 183 ca có ngày đi / mưa mà
# một điểm không đứng được ở buổi của nó sau khi đổi)
CAU_LY_DO_NGAY = {"xa_ngay_dau": "ngày 1 sẽ có điểm ở khu xa trung tâm, mà lịch không xếp khu xa vào ngày đầu",
                  "khong_giu_cho": "với ngày đi của lịch (thứ trong tuần, dự báo mưa) có điểm không đứng được ở buổi của nó sau khi đổi"}


def _loai_ly_do(ma) -> str | None:
    """Mã `kiem_khung_v2` của một khung thử ⇒ MỘT loại lý do lời thường (khoá của `CAU_LY_DO`); thứ tự xét: khu > kín > giờ mở."""
    ma = set(ma)
    return "khu" if ma & MA_LUAT_KHU else "kin" if ma & MA_LUAT_KIN else "gio_mo" if "ngoai_gio_mo" in ma else None


NHAN_TRUONG = {"so_ngay": "số ngày", "kieu_di": "kiểu đi", "so_thich": "sở thích", "tre_em": "số trẻ em", "lon_tuoi": "người lớn tuổi",
               "ngan_sach": "hạng chỗ ở"}
CAU_KHONG_DOI = {
    "ngoai_bang": "«{diem}» chưa có trong danh sách điểm của lịch.",
    "khong_co_trong_lich": "{diem} không có trong lịch hiện tại.",
    "da_co_trong_lich": "{diem} đã có trong lịch.",
    "khong_buoi_hop_le": "{diem} không đi được vào buổi đó.",
    "khong_hop_luat": "{diem} đặt ở chỗ đó sẽ làm lịch phạm luật xếp (giờ mở cửa / cụm xa / quá dày) nên mình chưa đổi.",
    "thieu_cho": "Chưa rõ ngày / buổi để dời {diem}.",
    # cờ `sua_lich_buoi_toi`: điểm ĐI ĐƯỢC buổi tối nhưng code chưa có phép xếp tay vào buổi tối (hoạt động tối do bộ xếp chọn, mỗi tối một hoạt động)
    "toi_chua_xep": "Mình chưa đặt được {diem} vào buổi tối theo ý bạn — hoạt động buổi tối do lịch tự chọn. Bạn có thể bỏ hoạt động tối đang có, lịch sẽ "
                    "tự chọn một hoạt động khác.",
    # review của phiên khác 21/11: xin đặt vào buổi tối một điểm ĐANG ở đúng buổi tối đó ⇒ không khuyên "bỏ hoạt động tối đang có" (chính là nó)
    "toi_dang_o": "{diem} đang ở buổi tối ngày {ngay} rồi.",
    # … và thêm / dời một điểm ban ngày CHƯA có trong lịch vào buổi tối ⇒ nói rõ buổi nào và vì sao (trước: "không đi được vào buổi đó")
    "ban_ngay_khong_toi": "{diem} không xếp được vào buổi tối vì đây là điểm tham quan ban ngày, còn buổi tối lịch chỉ xếp hoạt động buổi tối.",
    # lỗi có sẵn (phiên khác tái hiện 4 / 4 lượt, hai model, 21/11): THAY một hoạt động buổi tối ⇒ code báo "… không có trong lịch hiện tại" dù nó đang ở
    # buổi tối của chính lịch đó (`_vi_tri` chỉ có buổi ban ngày). Code chưa thay được hoạt động buổi tối ⇒ nói thật điều đó.
    "toi_chua_thay": "Mình chưa thay được hoạt động buổi tối theo ý bạn — hoạt động buổi tối do lịch tự chọn. Bạn có thể bỏ {diem}, lịch sẽ tự chọn một "
                     "hoạt động tối khác.",
    # công tắc `bo_toi_de_trong`: bỏ hoạt động tối thì tối đó để trống ⇒ hai câu trên không còn đúng lời khuyên "bỏ … lịch sẽ tự chọn hoạt động khác"
    "toi_chua_xep_trong": "Mình chưa đặt được {diem} vào buổi tối theo ý bạn — hoạt động buổi tối do lịch tự chọn.",
    "toi_chua_thay_trong": "Mình chưa thay được hoạt động buổi tối theo ý bạn — hoạt động buổi tối do lịch tự chọn. Bạn có thể bỏ {diem} để tối đó trống.",
    "van_cho_cu": "{diem} vẫn ở chỗ cũ — bạn nói lại từng điểm một nhé.",
    "het_diem_thay": "Không còn điểm phù hợp để thay {diem} (đặt được vào đúng chỗ đó) nên mình giữ nguyên.",
    # đổi số ngày / kiểu lịch mà không đổi được gì (trước 15/11 tối: lượt sửa im lặng, không dòng nào)
    "tham_so_chua_ro": "Mình chưa rõ bạn muốn {diem} thành gì — bạn nói cụ thể hơn nhé.",  # {diem} = nhãn hành động
    "tham_so_dang_dung": "Lịch đang đúng như vậy rồi ({diem}).",  # {diem} = "kiểu đi: nhẹ nhàng; số trẻ em: 1 trẻ em"
    # đổi hạng chỗ ở: {diem} = tên mức ("2–3 sao"…)
    "hang_chua_ro": "chỗ ở — bạn muốn hạng nào: 1 sao / đạt chuẩn, 2–3 sao hay 4–5 sao? Nói hạng thì mình đưa gợi ý chỗ ở hạng đó vào lịch.",
    "hang_dang_dung": "Lịch đang gợi ý chỗ ở hạng {diem} rồi.",
    "hang_khong_co": "Khu chỗ ở của lịch này chưa có cơ sở hạng {diem} trong danh mục nên mình giữ nguyên.",
    "khong_muc_o": "Lịch này không có mục gợi ý chỗ ở (lịch 1 ngày) nên không có hạng để đổi.",
    # đổi ngày đi: {diem} = ngày dd/mm
    "ngay_chua_ro": "ngày đi — bạn nói một ngày cụ thể (ví dụ 20/12, hoặc thứ Bảy tuần sau) thì mình đổi.",
    "ngay_khong_co": "Ngày bạn nêu không có trong lịch nên mình chưa đổi ngày đi.",
    "ngay_ngoai_han": "Mình chỉ xếp được ngày đi từ hôm nay tới 180 ngày nữa nên chưa đổi sang {diem}.",
    "ngay_dang_dung": "Lịch đang đi từ ngày {diem} rồi.",
    "ngay_pham_luat": "Đi từ {diem} thì lịch không xếp được đúng luật (giờ mở cửa / cụm xa) nên mình giữ ngày cũ.",
}


def ten_cua_diem(bang: v2.BangV2, id_: str) -> str:
    return bang.theo_id[id_]["ten"]


def khop_ten(bang: v2.BangV2, ten: str | None) -> str | None:
    """Tên người dùng / model nêu ⇒ id điểm của bảng: id nguyên văn, hoặc tên / tên khác khớp NGUYÊN tên sau chuẩn hoá (NFC, casefold, bỏ
    hậu tố " Huế"); không khớp ⇒ None (không đoán gần đúng)."""
    if not ten:
        return None
    if ten in bang.theo_id:
        return ten
    t = chuan_ten(ten)
    dung = next((d["id"] for d in bang.diem if t in (chuan_ten(x) for x in v2.ten_cua(d))), None)
    if dung is not None or len(t.split()) < 2:
        return dung
    # tên ngắn ("Quốc Học" ⇒ "Trường Quốc Học Huế"): nhận khi nằm trong ĐÚNG MỘT điểm của bảng (≥ 2 chữ — Q3 pilot 14/11); nhiều điểm ⇒ không đoán
    gan = {d["id"] for d in bang.diem for x in v2.ten_cua(d) if f" {t} " in f" {chuan_ten(x)} "}
    return gan.pop() if len(gan) == 1 else None


# Rào sau lần hiểu ý (C 15/11, lỗi thứ hạng 2 "nói chắc sai"): "đi từ ngày 20/12" từng ra hành động đổi số ngày 3 ⇒ 1 và báo "Đã đổi" (đếm
# `report_agent/2026-11-12_ra_khoang_cach/c_dem_sua_lich_truong.md`). Code chỉ nhận đổi số ngày khi CON SỐ có trong chữ người dùng gõ, đứng TRƯỚC chữ
# "ngày" (số trong một ngày tháng như "ngày 20/12" không tính), hoặc là số tương đối "thêm / bớt k ngày" khớp số ngày hiện tại ± k. Thiếu số ⇒ không nhận.
_SO_CHU = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "tư": 4, "năm": 5, "sáu": 6}
_SO = r"(\d+|một|hai|ba|bốn|tư|năm|sáu)"
_N_NGAY = re.compile(rf"(?<![\w/.-])(?<!thứ\s){_SO}\s*(?:ngày|hôm|n(?=\s*\d+\s*đ))", re.I)  # "3 ngày", "2 hôm", "4N3Đ"; "thứ hai ngày 20/12" không tính
_THEM = re.compile(rf"(thêm|tăng|kéo dài|nối)\s+(?:thêm\s+)?{_SO}\s*ngày", re.I)
_BOT = re.compile(rf"(bớt|giảm|rút|cắt|bỏ)\s+(?:bớt\s+|đi\s+)?{_SO}\s*(?:ngày|hôm)", re.I)
_BO_NGAY = re.compile(r"bỏ\s+(?:bớt\s+|đi\s+)?ngày\s+(cuối|\d+)", re.I)  # "bỏ ngày cuối", "bỏ ngày 3" (= ngày cuối) ⇒ bớt 1


def _so(x: str) -> int:
    return int(x) if x.isdigit() else _SO_CHU[x.lower()]


def so_ngay_co_trong_cau(cau: str, so_ngay: int | None, hien_tai: int) -> bool:
    """Hành động đổi số ngày ⇒ `so_ngay` mới có căn cứ trong chữ người dùng (tuyệt đối "còn 2 ngày" hoặc tương đối "thêm một ngày")?"""
    if so_ngay is None:
        return False
    t = unicodedata.normalize("NFC", cau)
    if any(_so(m.group(2)) + hien_tai == so_ngay for m in _THEM.finditer(t)) or any(hien_tai - _so(m.group(2)) == so_ngay for m in _BOT.finditer(t)):
        return True
    if so_ngay == hien_tai - 1 and any(m.group(1).lower() == "cuối" or int(m.group(1)) == hien_tai for m in _BO_NGAY.finditer(t)):
        return True
    tuong_doi = {m.start(2) for r in (_THEM, _BOT) for m in r.finditer(t)}  # số sau "thêm / bớt" là số tương đối, không phải tổng số ngày
    return any(_so(m.group(1)) == so_ngay for m in _N_NGAY.finditer(t) if m.start(1) not in tuong_doi)


# Sau lần hiểu ý (C 17/11, tự thử 16/11): bộ hành động không có "đổi chỗ / gộp / tách ngày". Khi MODEL đã nhận câu là câu sửa (ra hành động, hoặc
# "đổi số ngày" bị rào chặn) mà câu có ý đổi chỗ ngày ⇒ dòng "Chưa làm" nói đúng việc (trước: "Chưa làm: đổi số ngày" sai việc, hoặc ý đổi chỗ bị bỏ
# lặng). Danh sách dạng câu CHỈ dùng ở đây: lưới rộng ở đường "model trả rỗng" đã thử và bỏ (bộ kề bên E: 10 / 20 câu thường bị bắt nhầm).
_VIEC_NGAY = re.compile(r"(?<!\w)(?:đổi chỗ|hoán đổi|hoán vị|hoán|tráo|đảo|gộp|tách|sắp xếp lại|xếp lại|sắp lại|đổi thứ tự)\s+"
                        r"(?:lại\s+)?(?:thứ tự\s+)?(?:của\s+)?(?:các\s+|hai\s+|2\s+)?(?:ngày|buổi của ngày)(?!\s+(?:đi|khởi hành|xuất phát|về))",
                        re.I)
_MOC_NGAY = re.compile(r"(?<!\w)ngày\s*(?:\d|đầu|cuối)", re.I)
_DONG_TU_DOI_CHO = re.compile(r"(?<!\w)(?:đổi chỗ|hoán|tráo|đảo)(?!\w)", re.I)
VIEC_KHAC = "viec_khac"  # mã "Chưa làm" của ý sửa mà bộ hành động chưa có


def la_viec_ngay_chua_lam(cau: str) -> bool:
    """Câu có ý đổi chỗ / gộp / tách / xếp lại CÁC NGÀY của lịch: "đổi chỗ ngày 1 với ngày 2", "đảo thứ tự hai ngày", "ngày 1 và ngày 3 đổi chỗ
    cho nhau". Không: "đổi chỗ ở", "đổi ngày đi". Chỉ gọi khi model đã nhận câu là câu sửa."""
    t = unicodedata.normalize("NFC", cau)
    hai_ngay = len(_MOC_NGAY.findall(t)) >= 2 and not re.search(r"đổi chỗ\s+ở", t, re.I)
    return bool(_VIEC_NGAY.search(t) or (hai_ngay and _DONG_TU_DOI_CHO.search(t)))


# Cờ `sua_lich_doi_cho_ngay` (20/11, plan `report_agent/2026-11-20/c_doi_cho_ngay_plan.md`): "đổi chỗ ngày 1 với ngày 2" ⇒ code hoán đổi nội dung hai ngày.
# Đọc câu theo DANH SÁCH CHO PHÉP (như `doi_buoi_tu_cau`): một động từ đổi chỗ + ĐÚNG hai mốc ngày khác nhau + từ đệm; gặp chữ nào khác (tên điểm,
# gộp / tách, buổi, ngày đi…) ⇒ None ⇒ giữ dòng "Chưa làm" (từ chối nhầm được phép, áp sai thì không).
_DT_DOI_NGAY = re.compile(r"(?<!\w)(?:đổi chỗ|hoán đổi|hoán vị|hoán|tráo|đảo)(?!\w)", re.I)
# tên riêng `_SO_CHU_MOC`: bảng này từng mang tên `_SO_CHU`, đè lên bảng cùng tên của rào đổi số ngày ở trên (bảng đó có "sáu") ⇒ `_so("sáu")` văng KeyError
_SO_CHU_MOC = {"một": 1, "nhất": 1, "hai": 2, "ba": 3, "bốn": 4, "tư": 4, "năm": 5}
_MOC_DOI = re.compile(r"(?<!\w)ngày\s+(?:thứ\s+)?(\d|một|nhất|hai|ba|bốn|tư|năm|đầu tiên|đầu|cuối cùng|cuối)(?!\w)", re.I)
_HAI_NGAY = re.compile(r"(?<!\w)(?:hai|2)\s+ngày(?!\w)", re.I)
_DEM_DOI_NGAY = {"với", "và", "cho", "nhau", "giúp", "hộ", "dùm", "giùm", "mình", "tôi", "em", "bạn", "ơi", "hãy", "nhé", "nha", "đi", "lại", "thứ", "tự",
                 "của", "lịch", "trong", "ạ", "thì", "luôn", "nhỉ", "vị", "trí", "sang", "lên", "xuống"}
_DUOC_KHONG = re.compile(r"(?<!\w)được\s+(?:không|ko|chứ)(?=[\s?.!ạ]*$|\s+(?:ạ|nhỉ|bạn)\b)")  # lời nhờ cuối câu; "không" ở chỗ khác là phủ định ⇒ None (review E)


def cap_ngay_doi_cho(cau: str, so_ngay: int) -> tuple[int, int] | None:
    """Hai ngày người dùng nhờ ĐỔI CHỖ cho nhau, hoặc None khi câu không đúng khuôn. Chỉ đọc chữ của lượt này."""
    t = " ".join(unicodedata.normalize("NFC", cau).casefold().split())
    if len(_DT_DOI_NGAY.findall(t)) != 1:
        return None
    moc = []
    for m in _MOC_DOI.finditer(t):
        chu = m.group(1)
        moc.append(1 if chu.startswith("đầu") else so_ngay if chu.startswith("cuối") else _SO_CHU_MOC.get(chu) or int(chu))
    con = _DUOC_KHONG.sub(" ", _MOC_DOI.sub(" ", _DT_DOI_NGAY.sub(" ", t)))
    if not moc and so_ngay == 2 and len(_HAI_NGAY.findall(con)) == 1:  # lịch 2 ngày: "đổi chỗ hai ngày cho nhau"
        moc, con = [1, 2], _HAI_NGAY.sub(" ", con)
    if len(moc) != 2 or moc[0] == moc[1] or not all(1 <= n <= so_ngay for n in moc):
        return None
    if any(tu not in _DEM_DOI_NGAY for tu in re.findall(r"\w+", con)):
        return None
    return min(moc), max(moc)


# Tin vừa nhờ đổi chỗ hai ngày vừa HỎI ("đổi chỗ ngày 1 với ngày 2, mà vé vào Đại Nội bao nhiêu?" — lượt đo 21/11: hai dòng "Chưa làm", dòng đầu nói
# như thể trợ lý không đổi chỗ ngày được, trong khi gửi riêng vế sửa thì làm được). Chỉ gọi khi MODEL đã báo tin còn có câu hỏi (`hoi_them`). Cắt tin
# ở dấu câu / từ nối; ĐÚNG một vế đọc được cặp ngày, mọi vế còn lại không nhắc ngày nào của lịch, không có động từ sửa, không có lời rút lại ⇒ cặp đó; khác ⇒ None
# (vẫn giữ nguyên tắc của `cap_ngay_doi_cho`: từ chối nhầm được phép, áp sai thì không).
_TACH_VE = re.compile(r"[,;.?!\n]+|(?<!\w)(?:à mà|mà|còn|nhân tiện|tiện thể|với lại|cho (?:mình|em|tôi) hỏi|cho hỏi)(?!\w)", re.I)
_VE_CON_Y_SUA = re.compile(r"(?<!\w)(?:bỏ|thêm|thay|dời|chuyển|giữ|gộp|tách|xoá|xóa|đổi|hoán|tráo|đảo|xếp)(?!\w)", re.I)
# review B 22/11: vế còn lại là lời RÚT LẠI / phủ định ("à mà thôi", "à nhầm", "khoan đã", "đừng") ⇒ người dùng không còn muốn đổi ⇒ None;
# vế hỏi nhắc một ngày của lịch bằng chữ "hôm" ("hôm đầu có mưa không") ⇒ như nhắc "ngày 1" ⇒ None ("hôm nay", "hôm qua" không tính).
_VE_RUT_LOI = re.compile(r"(?<!\w)(?:thôi|khỏi|không cần|ko cần|k cần|đừng|khoan|huỷ|hủy|nhầm|lộn|quên|không phải|ko phải|bỏ qua)(?!\w)", re.I)
_MOC_HOM = re.compile(r"(?<!\w)hôm\s+(?:thứ\s+)?(?:\d|một|nhất|hai|ba|bốn|tư|năm|đầu|cuối)(?!\w)", re.I)
# Soát khác hãng 22/11 (#8): "à không" đứng riêng một vế vẫn ra cặp ngày; đếm cùng ngày 68 / 153 tin có lời rút lại ("để sau", "từ từ", "kệ đi"…) lọt
# qua danh sách chữ cấm ở trên ⇒ thêm DANH SÁCH CHO PHÉP: vế KHÁC vế đổi chỗ phải là một CÂU HỎI — có từ hỏi, có lời nhờ trả lời ("gợi ý giúp
# mình quán bún bò", "cho mình biết giờ mở cửa" — phiên điều phối nêu: kiểu tin này dễ gặp hơn lời rút), hoặc khuôn "có / đã / được / phải / nên …
# không / chưa" ở cuối vế, hoặc kết bằng dấu "?" — và không mở đầu bằng lời phủ định ("à không", "chưa", "hông"; "không sao", "không đâu" có từ hỏi mà
# vẫn là lời rút; riêng "không biết / chưa rõ … bao nhiêu" là cách hỏi thường gặp ⇒ không tính là phủ định). Vế nào không phải câu hỏi ⇒ None.
_VE_HOI = re.compile(r"(?<!\w)(?:bao nhiêu|bao lâu|bao xa|bao giờ|mấy|gì|nào|đâu|sao|ai|hỏi|hả|nhỉ"
                     r"|gợi ý|tư vấn|giới thiệu|đề xuất|kể|(?:chỉ|tìm|xem)\s+(?:giúp|giùm|dùm|hộ|cho)|chỉ\s+(?:mình|em|tớ|đường)|cho\s+(?:mình|em|tôi|anh|chị|tớ)\s+(?:biết|xin)"  # lời NHỜ trả lời
                     r"|(?:có|đã|được|phải|nên)(?!\w)(?!\s+lẽ).*(?<!\w)(?:không|ko|chưa)(?:\s+(?:ạ|vậy|thế|bạn))*\s*$)(?!\w)", re.I)
_VE_MO_DAU_PHU_DINH = re.compile(r"^\W*(?:(?:à|ờ|ơ|ừ|ừm|ấy|ý|ui|úi|ôi|ủa|hm+)\W+)*(?:không|ko|k|hông|hem|khum|chưa)(?!\w)(?!\s+(?:biết|rõ)(?!\w))", re.I)


def _la_ve_hoi(ve: str, ket_bang_dau_hoi: bool) -> bool:
    return not _VE_MO_DAU_PHU_DINH.search(ve) and bool(ket_bang_dau_hoi or _VE_HOI.search(ve))


def cap_ngay_doi_cho_kem_hoi(cau: str, so_ngay: int) -> tuple[int, int] | None:
    cau = unicodedata.normalize("NFC", cau)
    ve, dau = [], 0  # (vế, vế đó kết bằng dấu "?")
    for m in _TACH_VE.finditer(cau):
        ve.append((cau[dau:m.start()], "?" in m.group()))
        dau = m.end()
    ve = [(v, hoi) for v, hoi in ve + [(cau[dau:], False)] if v.strip()]
    doc = [(v, hoi, cap_ngay_doi_cho(v, so_ngay)) for v, hoi in ve]
    cap = [c for _, _, c in doc if c]
    if len(ve) < 2 or len(cap) != 1 or any(c is None and (_MOC_NGAY.search(v) or _MOC_HOM.search(v) or _VE_CON_Y_SUA.search(v) or _VE_RUT_LOI.search(v)
                                                           or not _la_ve_hoi(v, hoi)) for v, hoi, c in doc):
        return None
    return cap[0]


def doi_cho_ngay(bang: v2.BangV2, luu: dict, a: int, b: int) -> dict:
    """Hoán đổi nội dung ban ngày của ngày `a` và ngày `b` (mỗi điểm giữ buổi của nó) rồi đi đúng đường xếp-rồi-kiểm của mọi lượt sửa. Trả gói như `ap`.
    Hợp luật và mọi điểm đứng đúng chỗ mới ⇒ `da_ap` có mục `doi_cho_ngay` (+ `xep_them`: thứ bộ xếp đổi THÊM so với phép hoán đổi thuần — buổi tối,
    điểm lấp — để dòng báo nói rõ). Không ⇒ khung giữ nguyên, `khong_doi` có lý do quy từ mã luật (bảng lý do của "dời một điểm")."""
    luu = copy.deepcopy(luu)
    khung = copy.deepcopy(luu["khung"])
    kq = {"da_ap": [], "khong_doi": [], "chua_lam": [], "doi_truong": [], "the": None, "ngay_di": None, "xep_lai": None}
    doi = {a: b, b: a}
    giu = {j: (doi.get(ngay, ngay), buoi) for j, (ngay, buoi) in _vi_tri(khung).items()}
    if khung.get("day_them"):  # công tắc `sua_lich_them_day`: dấu "ngày được dày" đi theo NỘI DUNG của ngày khi hai ngày đổi chỗ
        luu["day_them"] = sorted({doi.get(d, d) for d in khung["day_them"]})
    k = _xep(bang, luu, _ts(khung["tham_so"]), giu, list(luu["loai"]))
    ma = set(v2.kiem_khung_v2(bang, k))
    vt_moi = _vi_tri(k)
    if ma or any(vt_moi.get(j) != cho for j, cho in giu.items()):
        kq["khong_doi"].append({"diem": f"ngày {a} với ngày {b}", "ma_luat": "ngay_khong_doi_cho",
                                "ly_do": "xa_ngay_dau" if "cum_xa" in ma else "khu" if ma & MA_LUAT_KHU else "kin" if ma & MA_LUAT_KIN
                                else "gio_mo" if "ngoai_gio_mo" in ma else "khong_giu_cho" if not ma else None})
        return {**kq, "khung": khung, "luu": luu}
    # Khung mong đợi = hoán đổi buổi sáng + chiều, buổi TỐI giữ theo ngày (hoạt động tối gắn với thứ trong tuần — đếm 20/11: 150 / 153 lịch thử giữ
    # nguyên buổi tối theo ngày). Bộ xếp ra khác khung này ⇒ `xep_them` để dòng báo nói rõ.
    mong = copy.deepcopy(khung)
    na, nb = (next(ng for ng in mong["ngay"] if ng["ngay"] == n) for n in (a, b))
    for buoi in v2.BUOI_NGAY:
        na["buoi"][buoi], nb["buoi"][buoi] = nb["buoi"][buoi], na["buoi"][buoi]
    them = _so_cho(mong, k)
    kq["da_ap"].append({"loai": "doi_cho_ngay", "ngay_a": a, "ngay_b": b, "xep_them": them if any(them.values()) else None})
    luu.update(tham_so=copy.deepcopy(k["tham_so"]), khung=copy.deepcopy(k))
    return {**kq, "khung": k, "luu": luu}


def loc_hanh_dong(hanh_dong: list, cau: str, luu: dict) -> tuple[list, int]:
    """(hành động giữ, số hành động đổi số ngày bị bỏ vì không có căn cứ trong câu). Hành động khác giữ nguyên."""
    hien_tai = luu["khung"]["tham_so"]["so_ngay"]
    giu = [h for h in hanh_dong if h.loai != "doi_so_ngay" or so_ngay_co_trong_cau(cau, h.so_ngay, hien_tai)]
    return giu, len(hanh_dong) - len(giu)


# Rào "bỏ / thay phải có chỗ NEO" (C 22/11/2026). Lỗi đã thấy thật (5 / 6 lượt, cả hai trạng thái công tắc nhớ đáp): trong cuộc đã có lịch, sau lượt
# "Kể các quán chè ở Huế", tin "Bỏ quán đầu đi rồi viết lại danh sách" bị lần hiểu ý gán "quán đầu" cho ĐIỂM ĐẦU CỦA LỊCH ⇒ "Đã bỏ Đại Nội Huế, thêm…".
# Lần hiểu ý chỉ thấy lịch + đúng câu này (không thấy lượt trước) nên mọi lời trỏ vào danh sách / câu trả lời vừa rồi ("bỏ cái thứ hai đi", "thay món đó
# bằng món khác") đều có thể rơi vào một điểm của lịch. Code chỉ nhận hành động bỏ / thay khi câu người dùng có MỘT trong hai:
#   (a) tên điểm bị chạm (đủ tên / tên khác, hoặc một khúc ≥ 2 chữ mà `khop_ten` nhận đúng điểm đó: "Tự Đức", "Thiên Mụ");
#   (b) mốc của LỊCH: "ngày 2", "hôm đầu", "buổi chiều", "lịch", "kế hoạch", "chuyến đi". "điểm đầu / cuối / thứ hai" đứng TRẦN không phải mốc: lượt
#       thật 22/11 "Kể các điểm tham quan miễn phí" ⇒ "Bỏ điểm đầu đi rồi viết lại danh sách" lại bỏ Đại Nội — danh sách vừa kể rất hay là danh sách
#       điểm; cả 6 lệnh "không tên nhưng có mốc" của sổ vết đều kèm ngày hoặc "lịch", không lệnh nào chỉ dựa vào "điểm + vị trí".
# Không có ⇒ hành động bị bỏ (lịch giữ nguyên); lượt không còn hành động nào ⇒ đi đường hỏi đáp thường (đã chạy song song — không tốn thêm).
# Đếm trước trên sổ vết (60 lượt sửa có hành động, 23 hành động bỏ / thay): 16 có tên trong câu · 6 không tên nhưng có mốc lịch · 1 không có gì — chính
# là ca lỗi. Chặn nhầm được phép (người dùng nhắn lại kèm tên), áp sai thì không. "du lịch", "lịch sử", "lịch sự", "âm lịch" không phải mốc của lịch;
# "ngày 2/12" là ngày tháng, không phải ngày 2 của lịch.
_SO_VI_TRI = r"(?:\d|một|nhất|hai|ba|bốn|tư|năm|đầu|cuối)"
_MOC_LICH = re.compile(rf"(?<!\w)(?:(?:ngày|hôm)\s*(?:thứ\s+)?{_SO_VI_TRI}(?![/.-]\d)|buổi\s+(?:sáng|trưa|chiều|tối)"
                       rf"|(?<!du )(?<!âm )(?<!dương )lịch(?!\s+(?:sử|sự|âm|dương))|kế hoạch|chuyến đi)(?!\w)", re.I)
# tên model điền mà không phải điểm nào của bảng: chỉ gồm các chữ trỏ / vị trí này ⇒ không phải tên riêng ("quán đầu", "cái thứ hai", "món đó")
_CHU_TRO = frozenset("quán món cái chỗ điểm nơi câu mục dòng ý đầu tiên cuối cùng thứ số đó này kia ấy nãy vừa rồi trên dưới nhất một hai ba bốn tư năm".split())


def _ten_trong_cau(bang: v2.BangV2, id_: str | None, ten_model: str | None, cau: str) -> bool:
    chu = " " + " ".join(re.findall(r"\w+", chuan_ten(cau))) + " "
    if id_ is None:  # không phải điểm của bảng: giữ khi model chép một TÊN có trong câu ("Hồ Tịnh Tâm") ⇒ `ap` nói thật "không có trong lịch"
        tu = re.findall(r"\w+", chuan_ten(ten_model or ""))
        return bool(tu) and f" {' '.join(tu)} " in chu and not all(w in _CHU_TRO or w.isdigit() for w in tu)
    for ten in v2.ten_cua(bang.theo_id[id_]):
        tu = re.findall(r"\w+", chuan_ten(ten))
        if tu and f" {' '.join(tu)} " in chu:
            return True
        # khúc ≥ 2 chữ liền nhau của tên: phải chứa một chữ TÊN RIÊNG (viết hoa trong tên, không tính chữ đầu) và `khop_ten` nhận khúc đó là ĐÚNG điểm
        # này. Đếm trên bảng 41 điểm: không có điều kiện tên riêng thì 71 khúc chung cũng lọt ("trung tâm", "thành phố", "truyền thống", "đường đi").
        # Chữ loại đứng đầu tên ("bãi biển", "phố cổ", "lăng") cố ý không đủ: danh sách vừa kể cũng có thể toàn bãi biển / lăng.
        rieng = {w.casefold() for w in re.findall(r"\w+", unicodedata.normalize("NFC", ten))[1:] if w[0].isupper()}
        for n in range(len(tu) - 1, 1, -1):
            if any(rieng & set(tu[i:i + n]) and f" {' '.join(tu[i:i + n])} " in chu and khop_ten(bang, " ".join(tu[i:i + n])) == id_
                   for i in range(len(tu) - n + 1)):
                return True
    return False


def loc_bo_thay(bang: v2.BangV2, hanh_dong: list, cau: str) -> tuple[list, list]:
    """(hành động giữ, hành động bỏ / thay bị bỏ vì câu không có tên điểm bị chạm lẫn mốc của lịch). Hành động loại khác giữ nguyên."""
    if _MOC_LICH.search(unicodedata.normalize("NFC", cau)):
        return list(hanh_dong), []
    giu, bo = [], []
    for h in hanh_dong:
        co_neo = h.loai not in ("bo_diem", "thay_diem") or _ten_trong_cau(bang, khop_ten(bang, h.ten), h.ten, cau)
        (giu if co_neo else bo).append(h)
    return giu, bo


# Cờ `sua_lich_doi_cho_code` (lượt đo cuối 18/11: sửa lịch bằng lời 7 / 10 — câu "cho A lên sáng ngày 1, còn B để sáng ngày 3" bị model gắn
# `chua_ho_tro` ổn định dù `ap` làm được, kể cả đổi chỗ hai điểm). Code chỉ đọc câu SAU khi model đã trả `chua_ho_tro` và không hành động nào khác.
# Đọc theo DANH SÁCH CHO PHÉP (bộ dò của C + review E 19/11: bản đầu dùng danh sách từ cấm ⇒ áp sai câu hỏi giá, câu tả chỗ đang đứng, câu đổi chỗ
# "cho nhau", ngày nói bằng chữ): mỗi vế chỉ được gồm tên một điểm + một từ dời + [buổi] sáng / chiều + ["ngày N"] + vài từ đệm; gặp BẤT KỲ chữ nào
# khác ⇒ rỗng ⇒ giữ câu "chưa hỗ trợ" (từ chối nhầm được phép, áp sai thì không).
_VE = re.compile(r"[,;]|\b(?:còn|và)\b")
_TU_DOI = {"lên", "sang", "để", "về", "xuống", "qua", "vào"}  # phải đứng GIỮA tên điểm và buổi: "A lên sáng", "A để buổi chiều"
_BUOI_DOI = {"sáng": "sang", "chiều": "chieu"}  # hành động `doi_buoi` chỉ có hai buổi ban ngày
_TU_DEM = {"cho", "vậy", "thì", "nhé", "nha", "giúp", "mình", "hãy", "bạn", "ơi", "dời", "chuyển", "đưa", "xếp", "ạ"}
_DIEM = re.compile(r"\x00(\d+)\x00")


def _doc_ve(ve: str) -> tuple[int, str, int | None] | None:
    """Một vế ⇒ (số thứ tự điểm, buổi, ngày | None), hoặc None khi vế có chữ ngoài danh sách cho phép / thiếu / thừa thành phần."""
    tu = ve.split()
    diem = [k for k, t in enumerate(tu) if _DIEM.fullmatch(t)]
    buoi = [k for k, t in enumerate(tu) if t in _BUOI_DOI]
    doi = [k for k, t in enumerate(tu) if t in _TU_DOI]
    ngay = [k for k, t in enumerate(tu) if t == "ngày"]
    if len(diem) != 1 or len(buoi) != 1 or not doi or len(ngay) > 1 or not all(diem[0] < k < buoi[0] for k in doi):
        return None
    so = None
    if ngay:
        if ngay[0] + 1 >= len(tu) or not tu[ngay[0] + 1].isdecimal():
            return None
        so = int(tu[ngay[0] + 1])
    da_dung = {diem[0], buoi[0], *doi, *(ngay and (ngay[0], ngay[0] + 1))}
    for k, t in enumerate(tu):
        if k in da_dung or t in _TU_DEM or (t == "buổi" and k + 1 == buoi[0]):
            continue
        return None
    return int(_DIEM.fullmatch(tu[diem[0]]).group(1)), _BUOI_DOI[tu[buoi[0]]], so


def doi_buoi_tu_cau(bang: v2.BangV2, luu: dict, cau: str) -> list[HanhDong]:
    """Câu có ĐÚNG hai vế, mỗi vế: tên MỘT điểm đang có trong lịch + từ dời + buổi sáng / chiều (+ "ngày N" trong lịch) ⇒ hai hành động `doi_buoi`
    (vế sau không nêu ngày ⇒ ngày của vế trước). Còn lại ⇒ []. Tên điểm = cụm tên / tên khác của bảng; đánh dấu tên của CẢ bảng trước khi tách vế
    (tên dài trước — tên có chữ "và" không bị cắt đôi); điểm ngoài lịch ⇒ []."""
    if "?" in cau or "？" in cau:  # câu hỏi ("… được không?", "… ạ?") không phải yêu cầu dời — bộ bù của C 19/11; hỏi lịch sự bị từ chối nhầm: chấp nhận
        return []
    trong_lich, so_ngay = _vi_tri(luu["khung"]), luu["khung"]["tham_so"]["so_ngay"]
    chu = f" {chuan_ten(re.sub(r'[^\w\s,;]', ' ', unicodedata.normalize('NFC', cau)))} "
    thu_tu = [d["id"] for d in bang.diem]
    # mỗi tên hai dạng: nguyên (thường hoá) và dạng `chuan_ten` đã bỏ hậu tố " Huế" — "Đại Nội Huế" và "Đại Nội" đều là một điểm
    ten = {(dang, d["id"]) for d in bang.diem for x in v2.ten_cua(d) for dang in (chuan_ten(x), " ".join(unicodedata.normalize("NFC", x).casefold().split()))}
    for t, i in sorted(ten, key=lambda t: (-len(t[0]), t)):
        chu = re.sub(rf"(?<!\w){re.escape(t)}(?!\w)", f" \x00{thu_tu.index(i)}\x00 ", chu)
    ve = [v for v in (x.strip() for x in _VE.split(chu)) if v]
    doc = [_doc_ve(v) for v in ve]
    if len(ve) != 2 or None in doc or doc[0][0] == doc[1][0] or any(thu_tu[d] not in trong_lich for d, _, _ in doc):
        return []
    ra, ngay_truoc = [], None
    for d, buoi, ngay in doc:
        ngay_truoc = ngay if ngay is not None else ngay_truoc
        if ngay_truoc is not None and not 1 <= ngay_truoc <= so_ngay:
            return []
        ra.append(HanhDong(loai="doi_buoi", ten=thu_tu[d], ngay=ngay_truoc, buoi=buoi))
    # Hai vế cùng MỘT đích (ngày, buổi): lần dời sau tự đổi chỗ ngược lần dời trước ⇒ lịch y nguyên mà vẫn báo "đã dời" (soát khác hãng 20/11) ⇒ không đọc
    if len({(h.ngay if h.ngay is not None else trong_lich[h.ten][0], h.buoi) for h in ra}) == 1:
        return []
    return ra


def luu_tu_lich(khung: dict, ngay_di: str | None, mua: dict | None) -> dict:
    """Trạng thái lưu sau một lượt lịch đạt (bản sao sâu). `mua` {ngày ISO: %} của dự báo đã dùng để xếp."""
    return {"tham_so": copy.deepcopy(khung["tham_so"]), "ngay_di": ngay_di,
            "mua": {(k.isoformat() if isinstance(k, dt.date) else k): v for k, v in (mua or {}).items()},
            "khung": copy.deepcopy(khung), "loai": []}


def _ts(tham_so: dict) -> v2.ThamSoV2:
    return v2.ThamSoV2(so_ngay=tham_so["so_ngay"], tre_em=tham_so["tre_em"], lon_tuoi=tham_so["lon_tuoi"], kieu_di=tham_so["kieu_di"],
                       so_thich=tuple(tham_so["so_thich"]), nguoi_lon=tham_so.get("nguoi_lon"),
                       ngan_sach=tham_so.get("ngan_sach"), toi_trong=tuple(tham_so.get("toi_trong") or ()),
                       toi_chon=tuple((int(n), j) for n, j in tham_so.get("toi_chon") or ()))


def _vi_tri(khung: dict) -> dict[str, tuple[int, str]]:
    return {i: (ng["ngay"], b) for ng in khung["ngay"] for b in v2.BUOI_NGAY for i in ng["buoi"][b]}


def _ngay_toi(khung: dict) -> dict[str, list[int]]:
    """Hoạt động buổi tối của lịch ⇒ các ngày nó đang đứng (`_vi_tri` chỉ có hai buổi ban ngày)."""
    out: dict[str, list[int]] = {}
    for ng in khung["ngay"]:
        for i in ng["buoi"]["toi"]:
            out.setdefault(i, []).append(ng["ngay"])
    return out


def _xep(bang, luu: dict, ts: v2.ThamSoV2, giu: dict | None, loai, day_moi: int | None = None) -> dict:
    ngay = dt.date.fromisoformat(luu["ngay_di"]) if luu["ngay_di"] else None
    mua = {dt.date.fromisoformat(k): v for k, v in luu["mua"].items()} or None
    k = v2.xep_v2(bang, ts, ngay_bat_dau=ngay, mua=mua, giu=giu, loai=frozenset(loai))
    # Công tắc `sua_lich_them_day`: NGÀY được vượt nhịp đi = ngày ỨNG VIÊN (người dùng đã tự xin thêm điểm vào đó: dấu của khung đã lưu, dấu của các
    # bước trước trong CHÍNH lượt này ở `luu["day_them"]`, cộng `day_moi` = ngày đang thử thêm) mà nội dung SAU lần xếp này thật sự vượt nhịp
    # (`v2.ngay_vuot_nhip`). Dấu tính lại mỗi lần ⇒ đổi chỗ hai ngày thì dấu đi theo nội dung, bỏ điểm / đổi kiểu đi làm ngày hết vượt thì dấu tự gỡ.
    # Ngày có dấu: ghi vào khung để `kiem_khung_v2` biết, tính lại giờ (buổi chiều lùi theo buổi sáng). Không ngày nào có dấu ⇒ trả đúng khung của
    # `xep_v2` (giống byte như trước).
    ung = {d for d in (*(luu.get("day_them") or ()), *(luu["khung"].get("day_them") or ()), *(() if day_moi is None else (day_moi,))) if d <= ts.so_ngay}
    day = [] if ts.han_che else sorted(d for d in ung if v2.ngay_vuot_nhip(bang, k["tham_so"], next(x for x in k["ngay"] if x["ngay"] == d)))
    if day:
        k["day_them"] = day
        giu_ids, T = set(giu or ()), bang.theo_id
        for ng in k["ngay"]:
            if ng["ngay"] not in day:
                continue
            g = v2.gio_ngay_day(bang, k["tham_so"], ng)
            # Điểm bộ xếp TỰ LẤP vào một buổi vừa trống của ngày đã dày được chọn theo giờ đầu buổi thường; buổi chiều đã lùi thì điểm lấp có thể rơi ngoài
            # giờ mở cửa hoặc kéo buổi chiều quá giờ kết ⇒ bỏ điểm lấp đó (buổi để trống) thay vì để cả lệnh của người dùng bị từ chối (đếm trên 2.249
            # lệnh "bỏ <điểm>" ngay sau một lần thêm dày: 16 lệnh từng kẹt vì đúng chỗ này). Điểm người dùng giữ / xin thì không bao giờ bị bỏ ở đây.
            # Các trường `thieu_uu_tien`, `toi_nghi`, `tam_dung_mua` của khung không tính lại sau khi gỡ (đọc chéo 23/11: 8 lần gỡ trên lưới 108 lịch, 0
            # lần để lại trường sai; hoạt động tối đã chọn trước đó chỉ có thể kém tối ưu, không trùng điểm ban ngày).
            hong = {j for b in v2.BUOI_NGAY for j in ng["buoi"][b]
                    if j not in giu_ids and (v2.dat_gio(T[j], g[j][0]) != g[j] or (b == "chieu" and g[j][1] > v2.GIO_KET_CHIEU_DAY))}
            if hong:
                for b in v2.BUOI_NGAY:
                    ng["buoi"][b] = [j for j in ng["buoi"][b] if j not in hong]
                for f in ("ngoai_so_thich", "hop_so_thich"):
                    k[f] = [j for j in k[f] if j not in hong]
                for j in hong:
                    k["gio"].pop(j, None)
                g = v2.gio_ngay_day(bang, k["tham_so"], ng)
            k["gio"].update({j: v2.in_gio(*x) for j, x in g.items()})
    return k


def _dung_luat(bang, khung: dict) -> bool:
    return not v2.kiem_khung_v2(bang, khung)


def _toi_xep_lai(cu: dict, moi: dict) -> list[dict] | None:
    """Bộ xếp chọn LẠI hoạt động tối cho từng ngày mỗi lần xếp (`lich_trinh_v2._xep_toi`: lấy ứng viên chưa dùng đầu tiên) ⇒ bỏ hoạt động tối ngày 1,
    hoặc thay một điểm ban ngày bằng nơi lịch đang dùng làm hoạt động tối, kéo các tối sau sang ngày khác — mà dòng báo chỉ kể điểm bị bỏ / thay (lượt
    trình duyệt 22/11; đếm: 45 / 150 lệnh bỏ hoạt động tối, 145 / 3.036 lệnh thay). Có hoạt động tối nằm ở ngày KHÁC ngày cũ của nó ⇒ trả cả dãy buổi tối
    SAU khi xếp (`moi_them`: hoạt động tối chưa từng có trong lịch) để dòng báo nói đủ; không thì None. Không đổi cách xếp."""
    # soát khác hãng 22/11 (K7): lịch 5 ngày LẶP một hoạt động tối ở hai ngày ⇒ tra theo CÁC ngày cũ của nó (bảng `mã ⇒ một ngày` bị ghi đè, báo giả
    # "Buổi tối xếp lại" ở mọi lệnh bỏ / thay dù không tối nào đổi)
    toi_cu = _ngay_toi(cu)
    if not any(j in toi_cu and ng["ngay"] not in toi_cu[j] for ng in moi["ngay"] for j in ng["buoi"]["toi"]):
        return None
    da_co = {j for ng in cu["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    return [{"ngay": ng["ngay"], "diem": list(ng["buoi"]["toi"]), "moi_them": [j for j in ng["buoi"]["toi"] if j not in da_co]} for ng in moi["ngay"]]


def _cau_toi_xep_lai(bang: v2.BangV2, xep_toi: list[dict]) -> str:
    return " Buổi tối xếp lại: " + ", ".join(
        f"ngày {x['ngay']} " + (" và ".join(ten_cua_diem(bang, j) + (" (mới thêm)" if j in x["moi_them"] else "") for j in x["diem"])
                                or "không có hoạt động tối") for x in xep_toi) + "."


def _cho_thu(bang, khung: dict, id_: str, ngay: int | None, buoi: str | None) -> list[tuple[int, str]]:
    """Chỗ ứng viên theo ngày / buổi người dùng nói, chỉ buổi điểm đi được; buổi trống trước."""
    d = bang.theo_id[id_]
    cho = [(ng["ngay"], b) for ng in khung["ngay"] for b in v2.BUOI_NGAY
           if (ngay is None or ng["ngay"] == ngay) and (buoi is None or b == buoi) and b in d["buoi"]]
    return sorted(cho, key=lambda c: bool(next(ng for ng in khung["ngay"] if ng["ngay"] == c[0])["buoi"][c[1]]))


def _goi_y_doi(bang, luu: dict, ts, khung: dict, vt: dict, loai, i: str) -> list[dict]:
    """Các chỗ điểm `i` (đang ở trong lịch) dời ĐƯỢC — thử bằng đúng phép thử của lần dời thật; cho câu "Dời được sang: …"."""
    goi_y = []
    for cho in sorted(_cho_thu(bang, khung, i, None, None), key=lambda c: (c[0], v2.BUOI_NGAY.index(c[1]))):
        if cho != vt[i]:
            k2, _, kia = _thu_cho(bang, luu, ts, vt, loai, i, cho, True)
            if k2 is not None:
                goi_y.append({"ngay": cho[0], "buoi": cho[1], "doi_voi": kia})
    return goi_y


def _cach_them(bang, luu: dict, ts, khung: dict, vt: dict, loai, i: str, ngay: int | None, buoi: str | None, day: bool = False) -> list[dict]:
    """Cờ `sua_lich_them_khong_the`: các cách CÓ ĐƯỢC điểm `i` (chưa ở trong lịch) trong phạm vi ngày / buổi người dùng nói (None = mọi buổi).
    `{ngay, buoi, thay}` — `thay` None: thêm thẳng vào buổi đó, không mất điểm nào; `thay` = id: lệnh "thay <điểm đó> bằng <i>" làm được. Thử bằng ĐÚNG
    phép thử của lần áp thật (`_thu_cho` của lệnh thêm, `_thu_giu` của lệnh thay) ⇒ gợi ý nào cũng là việc chính bộ áp nhận. Trong một buổi, điểm ngoài
    sở thích người dùng đứng trước (như thứ tự của lần tự thế chỗ cũ)."""
    st, ra = set(ts.so_thich), []
    for cho in sorted(_cho_thu(bang, khung, i, ngay, buoi), key=lambda c: (c[0], v2.BUOI_NGAY.index(c[1]))):
        k1 = _thu_cho(bang, luu, ts, vt, loai, i, cho, False)[0]
        if k1 is not None:  # ngày đó ĐÃ dày từ trước (có dấu) ⇒ lần thử thường cũng qua: vẫn phải nói cái giá cạnh câu gợi ý
            ra.append({"ngay": cho[0], "buoi": cho[1], "thay": None, **({"day": True} if cho[0] in (k1.get("day_them") or ()) else {})})
            continue
        if day and _thu_cho(bang, luu, ts, vt, loai, i, cho, False, day_moi=cho[0])[0] is not None:  # công tắc `sua_lich_them_day`: thêm thẳng được nếu ngày đó dày hơn nhịp đi
            ra.append({"ngay": cho[0], "buoi": cho[1], "thay": None, "day": True})
            continue
        for z in sorted((j for j, v in vt.items() if v == cho and j != i), key=lambda j: bool(st & set(bang.theo_id[j]["loai"]))):
            if _thu_giu(bang, luu, ts, {**{x: v for x, v in vt.items() if x not in (z, i)}, i: cho}, [x for x in loai if x != i] + [z], can=i) is not None:
                ra.append({"ngay": cho[0], "buoi": cho[1], "thay": z})
    return ra


def _hai_cach(bang, ts, cach: list[dict], ngay: int | None) -> list[dict]:
    """Hai cách nêu cho người dùng (review của phiên khác 21/11: xếp theo ngày rồi buổi thì gợi ý đầu thường là "thay Đại Nội…" ở một ngày KHÁC ngày được
    xin): cùng ngày được xin trước · thêm thẳng (không mất gì) trước · điểm bị thay là điểm không có thứ hạng ưu tiên trước, rồi điểm ngoài sở thích."""
    st = set(ts.so_thich)

    def khoa(g: dict):
        d = bang.theo_id[g["thay"]] if g["thay"] is not None else None
        return (ngay is not None and g["ngay"] != ngay, d is not None, bool(d and d.get("uu_tien")), bool(d and st & set(d["loai"])), g["ngay"], v2.BUOI_NGAY.index(g["buoi"]))
    return sorted(cach, key=khoa)[:2]


def _mot_cach_khong_mat(bang, ts, cach: list[dict], ngay: int | None) -> list[dict]:
    """Công tắc `sua_lich_them_day`: có cách THÊM THẲNG (không mất điểm nào) thì chỉ nêu MỘT cách đó; không có mới nêu hai cách "thay…" như cũ. Vì
    sao (lượt trình duyệt 23/11): câu gợi ý ghép "thêm X vào buổi … hoặc thay Y bằng X" — người dùng chép nguyên câu là gửi một lệnh hai nghĩa."""
    khong_mat = [g for g in cach if g["thay"] is None]
    return _hai_cach(bang, ts, khong_mat, ngay)[:1] if khong_mat else _hai_cach(bang, ts, cach, ngay)


def _thu_giu(bang, luu: dict, ts, giu: dict, loai, can: str | None = None) -> dict | None:
    """Xếp lại với `giu`; nhận khi đúng luật và (nếu có) điểm `can` thật sự có trong khung."""
    k = _xep(bang, luu, ts, giu, loai)
    if not _dung_luat(bang, k) or (can is not None and can not in _vi_tri(k)):
        return None
    return k


def _thu_cho(bang, luu: dict, ts, vt: dict, loai, i: str, cho: tuple[int, str], doi_cho: bool,
             day_moi: int | None = None) -> tuple[dict | None, list[str], str | None]:
    """Thử đặt điểm `i` vào `cho`, mọi điểm khác giữ nguyên chỗ; `doi_cho` và chỗ đích có đúng một điểm ⇒ hai điểm đổi chỗ cho nhau.
    Trả (khung nếu đúng luật và có `i` — không thì None, mã luật `kiem_khung_v2` khung thử phạm, điểm bị đổi chỗ). Dùng chung cho lần dời thật
    và cho gợi ý "dời được sang" ⇒ gợi ý nào cũng là chỗ mà chính đường dời thật nhận."""
    giu = {**{j: v for j, v in vt.items() if j != i}, i: cho}
    o_kia = [j for j, v in giu.items() if v == cho and j != i]
    kia = o_kia[0] if doi_cho and len(o_kia) == 1 else None
    if kia is not None:
        giu[kia] = vt[i]
    k = _xep(bang, luu, ts, giu, [x for x in loai if x != i], day_moi)  # `day_moi`: thử với ngày này được vượt nhịp đi (công tắc `sua_lich_them_day`)
    loi = v2.kiem_khung_v2(bang, k)
    return (k if not loi and i in _vi_tri(k) else None), loi, kia


def _lua_chon_thay(bang, luu: dict, ts, khung: dict, loai: list[str], cu: str) -> list[str]:
    """2–3 điểm đặt được vào đúng chỗ điểm cũ (đúng luật): cùng cụm trước, hợp sở thích trước, chưa có trong lịch, không thuộc `loai`."""
    vt = _vi_tri(khung)
    cho = vt[cu]
    giu0 = {i: v for i, v in vt.items() if i != cu}
    st = set(ts.so_thich)
    ung = [d for d in bang.diem if d["id"] not in vt and d["id"] not in loai and d["id"] != cu and cho[1] in d["buoi"]]
    ung.sort(key=lambda d: (d["cum"] != bang.theo_id[cu]["cum"], bool(st) and not (st & set(d["loai"]))))  # sort ổn định: thứ tự bảng
    out = []
    for d in ung:
        if _thu_giu(bang, luu, ts, {**giu0, d["id"]: cho}, loai + [cu], can=d["id"]) is not None:
            out.append(d["id"])
        if len(out) == MAX_LUA_CHON:
            break
    return out


THU = ("thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "Chủ nhật")


def _dd_mm(ngay: dt.date, hom_nay: dt.date | None = None) -> str:
    return f"{ngay.day}/{ngay.month}" + (f"/{ngay.year}" if hom_nay is not None and ngay.year != hom_nay.year else "")


def ngay_di_moi(cau: str, hom_nay: dt.date) -> dict:
    """Ngày đi mới đọc từ CHỮ NGƯỜI DÙNG (`do_so.ngay_tu_cau`) + hạn của biểu mẫu (hôm nay … +180 ngày) ⇒ {"ngay": date} hoặc {"ma", "diem"}
    (khoá + chữ điền của `CAU_KHONG_DOI`). Nơi gọi (`len_ke_hoach.hieu_va_ap`) lấy dự báo cho ngày đó rồi đưa cả gói vào `ap(ngay_moi=…)`."""
    ngay = ngay_tu_cau(cau, hom_nay)
    if isinstance(ngay, str):
        return {"ma": ngay, "diem": None}
    if not hom_nay <= ngay <= hom_nay + dt.timedelta(days=NGAY_DI_TOI_DA):
        return {"ma": "ngay_ngoai_han", "diem": _dd_mm(ngay, hom_nay)}
    return {"ngay": ngay}


def ten_muc_o(ngan_sach: str) -> str:
    return v2.ltl.TEN_MUC[v2.ltl.MUC_NGAN_SACH[ngan_sach]]


def ly_do_giu_hang(bang: v2.BangV2, luu_tru: dict | None, khung: dict, moi: str | None) -> str | None:
    """Mã lý do KHÔNG đổi hạng chỗ ở (khoá của `CAU_KHONG_DOI`), None = đổi được. Thử bằng đúng hàm dựng ô "Nơi ở" của lịch: mức mới phải ra
    cơ sở THUỘC mức đó — `chon_co_so` tự lùi về mọi hạng khi mức trống, lùi lặng lẽ ở đây thành "nói đã đổi mà hạng không đổi"."""
    if moi is None:
        return "hang_chua_ro"
    o = v2.o_dau_khung(luu_tru, bang, khung, moi) if luu_tru is not None else None
    if o is None:
        return "khong_muc_o"
    if moi == khung["tham_so"].get("ngan_sach"):
        return "hang_dang_dung"
    if any(v2.ltl.MUC_HANG[c["xep_hang"]] != v2.ltl.MUC_NGAN_SACH[moi] for c in o["co_so"]):
        return "hang_khong_co"
    return None


def _hang_o_sau_cung(hanh_dong: list[HanhDong]) -> list[HanhDong]:
    """Review bậc 1 (m-1, m-2): hạng chỗ ở model đặt nhầm vào hành động khác ⇒ tách thành một `doi_hang_o` (không thì lượt sửa im lặng);
    mọi `doi_hang_o` xét SAU CÙNG, trên khung cuối lượt (không thì "khách sạn 4 sao, rút còn 1 ngày" báo đã thêm chỗ ở cho lịch 1 ngày)."""
    khac, hang = [], []
    for h in hanh_dong:
        if h.loai != "doi_hang_o" and h.ngan_sach is not None:
            hang.append(HanhDong(loai="doi_hang_o", ngan_sach=h.ngan_sach))
            h = h.model_copy(update={"ngan_sach": None})
            if h.loai == "doi_tham_so" and all(getattr(h, f) is None for f in ("kieu_di", "so_thich", "tre_em", "lon_tuoi")):
                continue
        (hang if h.loai == "doi_hang_o" else khac).append(h)
    return khac + hang


def _so_cho(cu: dict, moi: dict) -> dict:
    """Hai khung ⇒ điểm đổi ngày / buổi (`doi_cho`), điểm rời lịch (`ra`), điểm mới vào (`vao`). Vị trí lấy trên CẢ BA buổi (review B: tính
    ban ngày riêng, buổi tối riêng làm điểm dời ngày ↔ tối nằm ở cả "bớt" lẫn "thêm"). Cho câu báo "lịch xếp lại"."""
    def cho(k: dict) -> dict[str, set]:  # điểm ⇒ TẬP (ngày, buổi): một điểm buổi tối có thể nằm ở nhiều ngày
        out: dict[str, set] = {}
        for ng in k["ngay"]:
            for bu in v2.BUOI:
                for j in ng["buoi"][bu]:
                    out.setdefault(j, set()).add((ng["ngay"], bu))
        return out
    vt, vt_moi = cho(cu), cho(moi)
    return {"doi_cho": sorted(j for j in vt if j in vt_moi and vt_moi[j] != vt[j]),
            "ra": sorted(set(vt) - set(vt_moi)), "vao": sorted(set(vt_moi) - set(vt))}


def ap(bang: v2.BangV2, luu: dict, hanh_dong: list[HanhDong], sua_chon: dict | None = None, luu_tru: dict | None = None,
       ngay_moi: dict | None = None, them_khong_the: bool = False, them_day: bool = False, bo_toi_de_trong: bool = False, bo_toi_hoi_lai: bool = False) -> dict:
    """Áp hành động trên **bản sao** khung đã lưu ⇒ {khung, luu, da_ap, khong_doi, chua_lam, doi_truong, the}.
    `the` khác None ⇒ lượt dừng ở thẻ chọn, khung KHÔNG đổi. `sua_chon` {cu, moi} (bấm nút của thẻ) ⇒ bỏ qua hành động model.
    `luu_tru` = bảng lưu trú đang dùng (None khi cờ nơi ở tắt) — chỉ hành động `doi_hang_o` cần.
    `ngay_moi` = gói của `ngay_di_moi` (+ `mua` {ngày ISO: %} dự báo cho ngày mới, `co_du_bao`) — chỉ `doi_ngay_di` cần; thiếu ⇒ "chưa rõ ngày".
    Đổi ngày đi: thử GIỮ mọi điểm ở chỗ cũ với ngày mới; phạm luật ⇒ xếp lại (điểm đã bỏ không quay lại); kết quả `kq["ngay_di"]`.
    `them_khong_the` (cờ `sua_lich_them_khong_the`): lệnh THÊM chỉ làm được bằng cách thế chỗ một điểm đang có ⇒ KHÔNG áp, báo điểm nào thay được;
    lệnh thêm bị luật xếp chặn ⇒ lý do + chỗ làm được. Mặc định False ⇒ như cũ (tự thế chỗ, câu chung).
    `them_day` (cờ `sua_lich_them_day`, 23/11/2026): lệnh THÊM mà luật xếp chặn CHỈ vì nhịp đi (số điểm một buổi, quỹ phút) ⇒ vẫn thêm, ngày đó được ghi
    dấu "dày hơn nhịp đã chọn" (`khung["day_them"]`), giờ của ngày tính lại (buổi chiều lùi theo buổi sáng, giữ bữa trưa), dòng báo nói rõ. Giờ mở cửa,
    luật khu, khu xa, luật của đoàn có trẻ nhỏ / người lớn tuổi KHÔNG nới. Đo trên 108 lịch vừa xếp × mọi điểm chưa có: 0 ⇒ 319 / 3.492 lệnh
    "thêm X" làm được, đều của đoàn thường — 319 / 1.116 với trần "buổi sáng kết ≤ 13:30" (không trần: 340). Mặc định False ⇒ như cũ với lịch chưa có
    ngày nào dày (lịch đã có ngày dày vẫn được giữ đúng luật — không thì mọi lệnh sửa sau đó bị chặn).
    `bo_toi_de_trong` (công tắc cùng tên, 23/11/2026): BỎ một hoạt động buổi tối ⇒ tối đó ĐỂ TRỐNG (ghi ngày vào `tham_so.toi_trong` ⇒ các lần xếp lại sau
    cũng không chọn lại), điểm ban ngày và buổi tối của các ngày khác giữ nguyên. Đếm trước khi làm (960 tổ hợp biểu mẫu, 652 lệnh bỏ tối): bản cũ lấp
    652 / 652, làm đổi buổi tối của NGÀY KHÁC ở 412, sinh một hoạt động lặp hai tối ở 213. Mặc định False ⇒ như cũ (bộ xếp chọn hoạt động tối khác)."""
    luu = copy.deepcopy(luu)
    khung = copy.deepcopy(luu["khung"])
    loai = list(luu["loai"])
    ts = _ts(khung["tham_so"])
    kq = {"da_ap": [], "khong_doi": [], "chua_lam": [], "doi_truong": [], "the": None, "ngay_di": None, "xep_lai": None}
    if sua_chon is not None:
        hanh_dong = [HanhDong(loai="bo_diem", ten=sua_chon["cu"])] if sua_chon["moi"] == "bo" else \
            [HanhDong(loai="thay_diem", ten=sua_chon["cu"], ten_moi=sua_chon["moi"])]
    hanh_dong = _hang_o_sau_cung(list(hanh_dong)[:MAX_HANH_DONG])
    # review E M-1: "thay" không nói thay bằng gì ⇒ lượt chỉ dừng ở thẻ chọn; mọi hành động khác của lượt vào "Chưa làm" (không áp nửa chừng
    # rồi mất khi thẻ trả khung cũ). Không có điểm thay ⇒ "Không đổi được" và các hành động khác đi tiếp như thường.
    if sua_chon is None:
        for h in hanh_dong:
            i = khop_ten(bang, h.ten)
            if h.loai == "thay_diem" and h.ten_moi is None and i is not None and i in _vi_tri(khung):
                lua_chon = _lua_chon_thay(bang, luu, ts, khung, loai, i)
                if lua_chon:
                    kq["the"] = {"cu": i, "ten_cu": ten_cua_diem(bang, i),
                                 "lua_chon": [{"gia_tri": j, "nhan": ten_cua_diem(bang, j)} for j in lua_chon] + [{"gia_tri": "bo", "nhan": "Bỏ điểm này, không thay"}]}
                    kq["chua_lam"] = [x.loai for x in hanh_dong if x is not h]
                    return {**kq, "khung": copy.deepcopy(luu["khung"]), "luu": luu}
                break
    kq["chua_lam"] = [h.loai for h in hanh_dong[MAX_AP:]]

    def khong(ten: str | None, ma: str) -> None:
        kq["khong_doi"].append({"diem": ten or "?", "ma_luat": ma})

    truoc_doi = None

    for h in hanh_dong[:MAX_AP]:
        vt = _vi_tri(khung)
        i = khop_ten(bang, h.ten)
        if h.loai in ("doi_so_ngay", "doi_tham_so"):
            moi = {"so_ngay": h.so_ngay, "kieu_di": h.kieu_di, "so_thich": None if h.so_thich is None else tuple(h.so_thich),
                   "tre_em": h.tre_em, "lon_tuoi": h.lon_tuoi}
            doi = {f: v for f, v in moi.items() if v is not None and v != getattr(ts, f)}  # chỉ trường khác giá trị đang dùng
            if not doi:  # không trường nào / mọi trường trùng giá trị đang dùng ⇒ nói ra, không im lặng
                neu = {f: v for f, v in moi.items() if v is not None}
                khong("; ".join(f"{NHAN_TRUONG[f]}: {_gia_tri(f, v)}" for f, v in neu.items()) if neu else NHAN_HANH_DONG[h.loai],
                      "tham_so_dang_dung" if neu else "tham_so_chua_ro")
                continue
            ts_moi = v2.ThamSoV2(**{**ts.__dict__, **doi})
            st = set(ts_moi.so_thich)
            giu = {j: v for j, v in vt.items() if v[0] <= ts_moi.so_ngay and (not st or st & set(bang.theo_id[j]["loai"]))}
            k = _thu_giu(bang, luu, ts_moi, giu, loai) or _xep(bang, luu, ts_moi, None, loai)  # giữ làm phạm luật ⇒ xếp lại không giữ
            if not _dung_luat(bang, k):
                khong(NHAN_HANH_DONG[h.loai], "khong_hop_luat")
                continue
            kq["doi_truong"] += [(f, getattr(ts, f), v) for f, v in doi.items()]
            if h.loai == "doi_tham_so":  # đổi kiểu lịch có thể xếp lại điểm ⇒ câu báo nói rõ (đổi số ngày thì dòng "số ngày" đã tự nói)
                truoc_doi = truoc_doi or khung  # hai lần đổi kiểu lịch trong một lượt ⇒ so khung trước lần đầu với khung sau lần cuối
                kq["xep_lai"] = _so_cho(truoc_doi, k)
            khung, ts = k, ts_moi
            kq["da_ap"].append({"loai": h.loai})
        elif h.loai == "doi_ngay_di":
            nm = ngay_moi or {"ma": "ngay_chua_ro", "diem": None}
            if "ma" in nm:
                khong(nm["diem"], nm["ma"])
                continue
            moi, cu = nm["ngay"], luu["ngay_di"]
            if moi.isoformat() == cu:
                khong(_dd_mm(moi), "ngay_dang_dung")
                continue
            luu_moi = {**luu, "ngay_di": moi.isoformat(), "mua": dict(nm.get("mua") or {})}
            k = _thu_giu(bang, luu_moi, ts, vt, loai) or _xep(bang, luu_moi, ts, None, loai)  # giữ chỗ phạm luật (thứ đóng cửa…) ⇒ xếp lại
            if not _dung_luat(bang, k):
                khong(_dd_mm(moi), "ngay_pham_luat")
                continue
            kq["ngay_di"] = {"cu": cu, "moi": moi.isoformat(), "co_du_bao": bool(nm.get("co_du_bao")), **_so_cho(khung, k)}
            luu, khung = luu_moi, k
            kq["da_ap"].append({"loai": "doi_ngay_di"})
        elif h.loai == "doi_hang_o":  # hạng không vào bộ xếp ⇒ KHÔNG xếp lại: điểm, ngày, buổi giữ nguyên; chỉ ô "Nơi ở" đổi
            ma = ly_do_giu_hang(bang, luu_tru, khung, h.ngan_sach)
            if ma is not None:
                khong(None if h.ngan_sach is None else ten_muc_o(h.ngan_sach), ma)
                continue
            kq["doi_truong"].append(("ngan_sach", ts.ngan_sach, h.ngan_sach))
            ts = v2.ThamSoV2(**{**ts.__dict__, "ngan_sach": h.ngan_sach})
            khung = {**khung, "tham_so": {**khung["tham_so"], "ngan_sach": h.ngan_sach}}
            kq["da_ap"].append({"loai": "doi_hang_o"})
        elif h.loai == "bo_diem":
            toi = {j for ng in khung["ngay"] for j in ng["buoi"]["toi"]}
            if i is None or (i not in vt and i not in toi):
                khong(h.ten if i is None else ten_cua_diem(bang, i), "ngoai_bang" if i is None else "khong_co_trong_lich")
                continue
            # Công tắc `bo_toi_hoi_lai`: bỏ một hoạt động BUỔI TỐI ⇒ theo điều người dùng nói (`cach_toi` của khuôn): chưa nói ⇒ lịch giữ nguyên, hỏi
            # lại hai lựa chọn; "de_trong" ⇒ nhánh để trống ngay dưới; "doi" ⇒ thay ĐÚNG tối đó, các tối khác được ghim (`toi_chon`) nên không dồn hàng.
            cach = getattr(h, "cach_toi", None) if bo_toi_hoi_lai else None
            if bo_toi_hoi_lai and i in toi and i not in vt and cach is None:
                o_ngay = _ngay_toi(khung)[i]
                kq["khong_doi"].append({"diem": ten_cua_diem(bang, i), "ma_luat": "bo_toi_hoi", "ngay": [n for n in o_ngay if n == h.ngay] or o_ngay})
                continue
            if cach == "doi" and i in toi and i not in vt:
                o_ngay = _ngay_toi(khung)[i]
                bo_ngay = [n for n in o_ngay if n == h.ngay] or o_ngay
                ghim = {**dict(ts.toi_chon), **{ng["ngay"]: ng["buoi"]["toi"][0] for ng in khung["ngay"] if ng["buoi"]["toi"]}}
                ts_moi = v2.ThamSoV2(**{**ts.__dict__, "toi_chon": tuple(sorted((n, j) for n, j in ghim.items() if n not in bo_ngay))})
                loai_moi = loai if set(o_ngay) - set(bo_ngay) else loai + [i]  # còn đứng ở tối khác (đã ghim) ⇒ không đưa vào danh sách "đã bỏ"
                k = _thu_giu(bang, luu, ts_moi, dict(vt), loai_moi)  # giữ MỌI điểm ban ngày ở chỗ cũ
                if k is None:
                    khong(ten_cua_diem(bang, i), "khong_hop_luat")
                    continue
                xep_toi = _toi_xep_lai(khung, k)  # mong None: các tối khác đã ghim; có đổi (hiếm) thì dòng báo vẫn nêu
                moi = {ng["ngay"]: (ng["buoi"]["toi"][0] if ng["buoi"]["toi"] else None) for ng in k["ngay"]}
                khung, loai, ts = k, loai_moi, ts_moi
                kq["da_ap"].append({"loai": "bo_diem", "diem": i, "toi_doi": [{"ngay": n, "diem": moi[n]} for n in bo_ngay],
                                    **({"toi_xep_lai": xep_toi} if xep_toi else {})})
                continue
            if (bo_toi_de_trong or cach == "de_trong") and i in toi and i not in vt:
                # các tối đang có hoạt động này; người dùng nêu ngày mà ngày đó không có nó ⇒ coi như nói về mọi tối có nó (không đoán ngày khác)
                o_ngay = _ngay_toi(khung)[i]
                bo_ngay = [n for n in o_ngay if n == h.ngay] or o_ngay
                ts_moi = v2.ThamSoV2(**{**ts.__dict__, "toi_trong": tuple(sorted(set(ts.toi_trong) | set(bo_ngay)))})
                con_lai = set(o_ngay) - set(bo_ngay)  # hoạt động lặp ở tối khác vẫn giữ ⇒ không đưa vào danh sách "đã bỏ" (không thì tối kia cũng mất)
                loai_moi = loai if con_lai else loai + [i]
                k = _thu_giu(bang, luu, ts_moi, dict(vt), loai_moi)  # giữ MỌI điểm ban ngày ở chỗ cũ
                if k is None:
                    khong(ten_cua_diem(bang, i), "khong_hop_luat")
                    continue
                xep_toi = _toi_xep_lai(khung, k)  # mong None: các tối khác không đổi; có đổi (hiếm) thì dòng báo vẫn nêu
                khung, loai, ts = k, loai_moi, ts_moi
                kq["da_ap"].append({"loai": "bo_diem", "diem": i, "toi_trong": bo_ngay, **({"toi_xep_lai": xep_toi} if xep_toi else {})})
                continue
            k = _thu_giu(bang, luu, ts, {j: v for j, v in vt.items() if j != i}, loai + [i])
            if k is None:
                khong(ten_cua_diem(bang, i), "khong_hop_luat")
                continue
            # bộ xếp lấp chỗ trống bằng điểm kế tiếp (giữ chỗ điểm không chạm) ⇒ điểm MỚI vào lịch phải có trong lời báo (tự thử 16/11:
            # "Đã bỏ X." mà lịch có thêm điểm khác; mô phỏng 910 / 960 khung). Cả buổi tối: bỏ hoạt động tối ⇒ bộ xếp chọn hoạt động tối khác.
            truoc = set(vt) | toi
            lap = [{"diem": j, "ngay": ng["ngay"], "buoi": b} for ng in k["ngay"] for b in v2.BUOI for j in ng["buoi"][b] if j not in truoc]
            xep_toi = _toi_xep_lai(khung, k)  # buổi tối của ngày khác cũng đổi ⇒ dòng báo nêu cả dãy buổi tối
            khung, loai = k, loai + [i]
            kq["da_ap"].append({"loai": "bo_diem", "diem": i, **({"lap": lap} if lap else {}), **({"toi_xep_lai": xep_toi} if xep_toi else {})})
        elif h.loai in ("them_diem", "doi_buoi"):
            if i is None:
                khong(h.ten, "ngoai_bang")
                continue
            # xin thêm vào BUỔI TỐI một điểm đang có trong lịch ban ngày ("thêm Đại Nội về đêm vô tối ngày 1" — bước hiểu ý điền tên điểm ban ngày): câu "đã
            # có trong lịch" đúng chữ mà sai việc (lượt người dùng mô phỏng 22/11, hai lượt liền) ⇒ để lệnh đi tới nhánh buổi tối bên dưới, nơi có câu nói thật
            if h.loai == "them_diem" and i in vt and h.buoi != "toi":
                khong(ten_cua_diem(bang, i), "da_co_trong_lich")
                continue
            if h.loai == "doi_buoi" and h.buoi is None:
                khong(ten_cua_diem(bang, i), "thieu_cho")
                continue
            ngay = h.ngay if h.ngay is not None else (vt[i][0] if h.loai == "doi_buoi" and i in vt else None)
            # soát khác hãng 22/11 (K8a): "thêm Ca Huế trên sông Hương vào lịch" — nơi CHỈ có buổi tối mà người dùng không gõ chữ "tối" — từng rơi xuống
            # nhánh thêm ban ngày và ra "đặt vào buổi nào cũng phạm luật xếp" ⇒ coi như xin buổi tối
            chi_toi = h.loai == "them_diem" and h.buoi is None and set(bang.theo_id[i]["buoi"]) == {"toi"}
            if h.buoi == "toi" or chi_toi:  # code KHÔNG xếp tay vào buổi tối ⇒ luôn là một câu nói thật
                toi = _ngay_toi(khung)
                if i in toi and (h.ngay is None or h.ngay in toi[i]):  # đang ở đúng buổi tối được xin
                    kq["khong_doi"].append({"diem": ten_cua_diem(bang, i), "ma_luat": "toi_dang_o", "ngay": h.ngay if h.ngay is not None else toi[i][0]})
                elif "toi" in bang.theo_id[i]["buoi"]:
                    khong(ten_cua_diem(bang, i), "toi_chua_xep_trong" if bo_toi_de_trong else "toi_chua_xep")
                elif h.loai == "doi_buoi" and i in vt:  # điểm ban ngày đang ở trong lịch ⇒ lý do + các chỗ dời được (như lần dời bị luật xếp chặn)
                    kq["khong_doi"].append({"diem": ten_cua_diem(bang, i), "ma_luat": "khong_buoi_hop_le", "dich": [ngay, "toi"], "ly_do": "ban_ngay",
                                            "goi_y": _goi_y_doi(bang, luu, ts, khung, vt, loai, i)})
                else:
                    khong(ten_cua_diem(bang, i), "ban_ngay_khong_toi")
                continue
            if h.buoi is not None and h.buoi not in bang.theo_id[i]["buoi"]:
                khong(ten_cua_diem(bang, i), "khong_buoi_hop_le")
                continue
            giu0 = {j: v for j, v in vt.items() if j != i}
            doi_cho = h.loai == "doi_buoi" and i in vt  # dời điểm ĐANG ở trong lịch (chỗ đích có đúng một điểm ⇒ đổi chỗ hai điểm)
            k, loi, ma_cho = None, [], []  # `ma_cho`: mã luật của TỪNG chỗ đã thử ở vòng quyết định (cho lý do của lệnh thêm không nói rõ một buổi)
            for cho in _cho_thu(bang, khung, i, ngay, h.buoi):
                k, loi, _ = _thu_cho(bang, luu, ts, vt, loai, i, cho, doi_cho)
                ma_cho.append(loi)
                if k is not None:
                    break
            day = None
            if k is None and h.loai == "them_diem" and them_day and not ts.han_che:
                # Chủ dự án chọn 23/11/2026 "cho ngày dày thêm": người dùng XIN thêm thì lịch nhận, vượt nhịp đi đã chọn, miễn giờ còn đi được thật.
                # Thử lại từng chỗ với ngày đó được vượt nhịp; `kiem_khung_v2` vẫn giữ mọi luật còn lại + bữa trưa + giờ kết buổi chiều.
                # `loi` nay là mã luật của lần thử ĐÃ nới nhịp ⇒ lý do từ chối bên dưới nói đúng thứ còn chặn (giờ mở cửa, khu…), không còn "quá kín"
                ma_cho = []
                for cho in _cho_thu(bang, khung, i, ngay, h.buoi):
                    k, loi, _ = _thu_cho(bang, luu, ts, vt, loai, i, cho, False, day_moi=cho[0])
                    ma_cho.append(loi)
                    if k is not None:
                        break
            the_cho = None
            if k is None and h.loai == "them_diem" and them_khong_the:
                # Người dùng mô phỏng 21/11 (vai sửa lịch, cả hai model): nhờ "thêm X" ⇒ code tự thế chỗ một điểm đang có ⇒ người dùng xin trả lại ⇒ code
                # thế chỗ điểm kia, lặp ba lượt. Đếm trên bộ áp (144 lịch mẫu): 33–63 % lệnh thêm rơi vào thế chỗ, điểm bị thế là điểm chính 58–84 %.
                # Cờ bật: KHÔNG tự thế — nói điểm nào thay được (người dùng tự quyết bằng lệnh "thay Y bằng X" đã có); không thay được ⇒ lý do + chỗ làm được.
                ten = ten_cua_diem(bang, i)
                trong = _cach_them(bang, luu, ts, khung, vt, loai, i, ngay, h.buoi, day=them_day and not ts.han_che)
                # công tắc `sua_lich_them_day`: chỗ được xin không nhận thêm (khu, giờ mở cửa…) nhưng CÙNG điểm thêm thẳng được ở buổi khác ⇒ nêu cách
                # đó TRƯỚC các cách "thay…" (không mất điểm nào). Năm lệnh thêm đã ghi của người dùng mô phỏng: 3 / 5 thuộc ca này.
                khac = ([g for g in _cach_them(bang, luu, ts, khung, vt, loai, i, None, None, day=True) if g["thay"] is None]
                        if them_day and not ts.han_che and (ngay is not None or h.buoi is not None) and not any(g["thay"] is None for g in trong) else [])
                # lý do = mã luật của lần thử thêm thẳng; chỉ chắc khi người dùng nói rõ MỘT buổi (không nói chỗ ⇒ `loi` là của chỗ thử sau cùng,
                # không phải lý do chung — review của phiên khác 21/11) ⇒ ngoài ca đó để None, câu dùng lời chung
                ma = set(loi) if ngay is not None and h.buoi is not None else set()
                ly_do = _loai_ly_do(ma)
                # công tắc `sua_lich_them_day`, lệnh KHÔNG nói rõ một buổi: lý do của TỪNG chỗ đã thử, loại gặp nhiều đứng trước. Đếm 23/11/2026 trên
                # lưới 108 lịch: 797 lệnh "thêm X" của đoàn thường bị từ chối — 701 chỉ vướng MỘT loại (690 là khu), 96 lẫn hai ba loại ⇒ một loại thì
                # câu nói thẳng loại đó, lẫn thì nêu từng loại (trước đó mọi ca đều đọc "lịch đang kín…", kể cả 20 / 30 điểm của lịch mặc định). Đoàn có
                # trẻ nhỏ / người lớn tuổi GIỮ câu cũ: không có lần thử nới nhịp, chỗ nào cũng vướng trần "hai điểm một ngày" ⇒ "lịch đang kín" là đúng
                theo_cho = ({"ly_do_cho": [x for x, _ in collections.Counter(filter(None, map(_loai_ly_do, ma_cho))).most_common()] if ly_do is None else []}
                            if them_day and not ts.han_che else {})
                if trong:
                    kq["khong_doi"].append({"diem": ten, "ma_luat": "them_can_thay", "dich": [ngay, h.buoi],
                                            "cach": _mot_cach_khong_mat(bang, ts, khac + trong, ngay) if them_day else _hai_cach(bang, ts, trong, ngay),
                                            "ly_do": ly_do, **theo_cho,
                                            "dang_co": [ten_cua_diem(bang, j) for j, v in vt.items() if v == (ngay, h.buoi)]})
                else:
                    kq["khong_doi"].append({"diem": ten, "ma_luat": "them_bi_chan", "dich": [ngay, h.buoi], "ly_do": ly_do, **theo_cho,
                                            "cach": [] if ngay is None and h.buoi is None
                                            else _mot_cach_khong_mat(bang, ts, khac or _cach_them(bang, luu, ts, khung, vt, loai, i, None, None), ngay) if them_day
                                            else _hai_cach(bang, ts, _cach_them(bang, luu, ts, khung, vt, loai, i, None, None), ngay)})
                continue
            if k is None and h.loai == "them_diem":
                # buổi đã kín (lịch bản 2 thường đủ quỹ phút) ⇒ thế chỗ một điểm lấp / ngoài sở thích ở đúng buổi đó; câu báo nói rõ điểm bị thế
                st = set(ts.so_thich)
                for cho in _cho_thu(bang, khung, i, ngay, h.buoi):
                    o = sorted((j for j, v in giu0.items() if v == cho), key=lambda j: bool(st & set(bang.theo_id[j]["loai"])))
                    for z in o:
                        k = _thu_giu(bang, luu, ts, {**{j: v for j, v in giu0.items() if j != z}, i: cho}, [x for x in loai if x != i], can=i)
                        if k is not None:
                            the_cho = z
                            break
                    if k is not None:
                        break
            if k is None and doi_cho:  # nói lý do + các chỗ điểm này dời ĐƯỢC (thử bằng đúng phép thử của lần dời thật); `ma_luat` giữ nguyên
                ma = set(loi)
                goi_y = _goi_y_doi(bang, luu, ts, khung, vt, loai, i)
                kq["khong_doi"].append({"diem": ten_cua_diem(bang, i), "ma_luat": "khong_hop_luat", "dich": [ngay, h.buoi], "goi_y": goi_y,
                                        "ly_do": "khu" if ma & MA_LUAT_KHU else "kin" if ma & MA_LUAT_KIN else "gio_mo" if "ngoai_gio_mo" in ma else None})
                continue
            if k is None:
                khong(ten_cua_diem(bang, i), "khong_hop_luat")
                continue
            xep_toi = _toi_xep_lai(khung, k)  # soát khác hãng 22/11 (G5): nơi vừa vào ban ngày vốn là hoạt động tối ⇒ các buổi tối bị chọn lại, phải báo
            khung, loai = k, [x for x in loai if x != i]
            # Dòng báo "dày hơn nhịp" gắn theo KẾT QUẢ, không theo nhánh đã đi qua (đọc chéo 23/11: lần thêm thứ hai vào một ngày đã dày qua được ở lần
            # thử thường nên từng không có dòng báo): ngày của điểm vừa thêm mang dấu sau lần xếp này ⇒ báo. Dời một điểm SANG một ngày khác đang dày cũng báo.
            ng_i = _vi_tri(k)[i][0]
            if ng_i in (k.get("day_them") or ()) and (h.loai == "them_diem" or vt.get(i, (ng_i,))[0] != ng_i):
                day = ng_i
            if k.get("day_them"):  # các bước sau của CHÍNH lượt này phải thấy ngày ứng viên (dấu của khung đầu lượt là bản cũ)
                luu["day_them"] = sorted({*(luu.get("day_them") or ()), *k["day_them"]})
            kq["da_ap"].append({"loai": h.loai, "diem": i, "ngay": _vi_tri(k)[i][0], "buoi": _vi_tri(k)[i][1], "the_cho": the_cho,
                                **({"toi_xep_lai": xep_toi} if xep_toi else {}), **({"day": _tin_day(k, day)} if day is not None else {})})
        elif h.loai == "thay_diem":
            if i is None or i not in vt:
                khong(h.ten if i is None else ten_cua_diem(bang, i),
                      "ngoai_bang" if i is None else ("toi_chua_thay_trong" if bo_toi_de_trong else "toi_chua_thay") if i in _ngay_toi(khung) else "khong_co_trong_lich")
                continue
            if h.ten_moi is None:  # không nói thay bằng gì ⇒ thẻ chọn (khung không đổi lượt này)
                lua_chon = _lua_chon_thay(bang, luu, ts, khung, loai, i)
                if not lua_chon:
                    khong(ten_cua_diem(bang, i), "het_diem_thay")
                    continue
                kq["the"] = {"cu": i, "ten_cu": ten_cua_diem(bang, i),
                             "lua_chon": [{"gia_tri": j, "nhan": ten_cua_diem(bang, j)} for j in lua_chon] + [{"gia_tri": "bo", "nhan": "Bỏ điểm này, không thay"}]}
                return {**kq, "khung": copy.deepcopy(luu["khung"]), "luu": luu}
            j = khop_ten(bang, h.ten_moi)
            if j is None:
                khong(h.ten_moi, "ngoai_bang")
                continue
            if j in vt:
                khong(ten_cua_diem(bang, j), "da_co_trong_lich")
                continue
            giu_thay, loai_thay = {**{x: v for x, v in vt.items() if x != i}, j: vt[i]}, [x for x in loai if x != j] + [i]
            k = _thu_giu(bang, luu, ts, giu_thay, loai_thay, can=j)
            if k is None and them_khong_the and vt[i][1] in bang.theo_id[j]["buoi"]:
                # cùng cờ: lệnh THAY bị luật xếp chặn nằm ngay trên đường người dùng đi sau dòng gợi ý của lệnh thêm (chọn thay một điểm KHÁC điểm được
                # gợi ý: 0 / 3 áp được, chỉ nhận câu chung) ⇒ lý do cụ thể + tối đa hai cách có được điểm mới, như lệnh thêm bị chặn
                ma = set(v2.kiem_khung_v2(bang, _xep(bang, luu, ts, giu_thay, loai_thay)))
                kq["khong_doi"].append({"diem": ten_cua_diem(bang, j), "ma_luat": "thay_bi_chan", "cu": ten_cua_diem(bang, i), "dich": list(vt[i]),
                                        "ly_do": "khu" if ma & MA_LUAT_KHU else "kin" if ma & MA_LUAT_KIN else "gio_mo" if "ngoai_gio_mo" in ma else None,
                                        "cach": _hai_cach(bang, ts, _cach_them(bang, luu, ts, khung, vt, loai, j, None, None), vt[i][0])})
                continue
            if k is None:
                khong(ten_cua_diem(bang, j), "khong_buoi_hop_le" if vt[i][1] not in bang.theo_id[j]["buoi"] else "khong_hop_luat")
                continue
            xep_toi = _toi_xep_lai(khung, k)  # điểm thay VÀO vốn là hoạt động tối ⇒ các buổi tối bị chọn lại
            khung, loai = k, [x for x in loai if x != j] + [i]
            kq["da_ap"].append({"loai": "thay_diem", "diem": i, "moi": j, **({"toi_xep_lai": xep_toi} if xep_toi else {})})
    # điểm "đã dời" mà cuối lượt vẫn ở đúng chỗ cũ (dời về chỗ đang đứng; hai lần dời đổi chỗ ngược nhau) ⇒ không báo "Đã dời" (soát khác hãng 20/11)
    vt_cu, vt_moi = _vi_tri(luu["khung"]), _vi_tri(khung)
    for a in [a for a in kq["da_ap"] if a["loai"] == "doi_buoi" and a["diem"] in vt_moi and vt_cu.get(a["diem"]) == vt_moi[a["diem"]]]:
        kq["da_ap"].remove(a)
        khong(ten_cua_diem(bang, a["diem"]), "van_cho_cu")
    if not kq["da_ap"]:  # không ý nào làm được ⇒ trả đúng khung đã lưu (bộ xếp có thể đã đổi thứ tự / giờ trong buổi — review E)
        khung = copy.deepcopy(luu["khung"])
    luu.update(tham_so=copy.deepcopy(khung["tham_so"]), khung=copy.deepcopy(khung), loai=loai)
    return {**kq, "khung": khung, "luu": luu}


def _gia_tri(f: str, v) -> str:
    if f == "tre_em":
        return f"{v} trẻ em"
    if f == "lon_tuoi":
        return "có" if v else "không"
    if f == "so_ngay":
        return f"{v} ngày"
    if f == "ngan_sach":
        return ten_muc_o(v)
    if f == "kieu_di":
        return {"nhe_nhang": "nhẹ nhàng", "can_bang": "cân bằng", "kham_pha": "khám phá nhiều"}.get(v, str(v))
    return ", ".join(v2.NHAN_LOAI.get(x, x) for x in v) or "không chọn"


MAX_TEN_XEP_LAI = 6  # quá số tên này ⇒ câu báo chỉ nêu số điểm (review B: đổi sở thích ở lịch 5 ngày ra tới 27 tên / 528 ký tự)


def _phan_xep_lai(bang: v2.BangV2, x: dict) -> str:
    gon = len(x["ra"]) + len(x["vao"]) > MAX_TEN_XEP_LAI
    ten = lambda ds: f"{len(ds)} điểm" if gon else ", ".join(ten_cua_diem(bang, j) for j in ds)  # noqa: E731
    phan = [f"{len(x['doi_cho'])} điểm đổi ngày hoặc buổi" if x["doi_cho"] else "",
            "bớt " + ten(x["ra"]) if x["ra"] else "", "thêm " + ten(x["vao"]) if x["vao"] else ""]
    return "; ".join(p for p in phan if p)


def _tin_day(khung: dict, ngay: int) -> dict:
    """Số liệu cho dòng báo "ngày này dày hơn nhịp đã chọn" (công tắc `sua_lich_them_day`): kiểu đi + mỗi buổi có điểm {số điểm, từ, đến} — giờ lấy từ
    chính `khung["gio"]` (do code tính)."""
    ng = next(x for x in khung["ngay"] if x["ngay"] == ngay)
    buoi = {b: {"so": len(ng["buoi"][b]), "tu": khung["gio"][ng["buoi"][b][0]].split("–")[0].strip(), "den": khung["gio"][ng["buoi"][b][-1]].split("–")[1].strip()}
            for b in v2.BUOI_NGAY if ng["buoi"][b]}
    return {"ngay": ngay, "kieu_di": khung["tham_so"]["kieu_di"], "buoi": buoi}


def _cau_day(d: dict) -> str:
    return (f" Ngày {d['ngay']} nay dày hơn nhịp {v2.NHAN_KIEU_DI[d['kieu_di']]} bạn chọn: "
            + "; ".join(f"buổi {NHAN_BUOI[b]} {x['so']} điểm, {x['tu']} – {x['den']}" for b, x in d["buoi"].items()) + ".")


def _cau_cach(bang: v2.BangV2, x: str, g: dict, kem_cho: bool) -> str:
    """Câu người dùng nhắn để làm một cách của `_cach_them` ("thay Y bằng X" / "thêm X vào buổi … ngày …")."""
    cho = f"buổi {NHAN_BUOI[g['buoi']]} ngày {g['ngay']}"
    if g["thay"] is None:
        return f"thêm {x} vào {cho}"
    return f"thay {ten_cua_diem(bang, g['thay'])} bằng {x}" + (f" ({cho})" if kem_cho else "")


def cau_goi_y(bang: v2.BangV2, kq: dict) -> tuple[str, ...]:
    """Các câu ĐÃ được gợi ý trong khối thay đổi của lượt này (do code dựng, không chữ người dùng / chữ model) — route nhớ đúng một lượt để lần hiểu ý
    của lượt kế hiểu được lời đồng ý cụt ("ok thay đi"). Lượt không có dòng gợi ý ⇒ rỗng."""
    return (tuple(_cau_cach(bang, k["diem"], g, False) for k in kq["khong_doi"] for g in k.get("cach") or ())
            + tuple(c for k in kq["khong_doi"] if k["ma_luat"] == "bo_toi_hoi" for c in _cau_bo_toi(k)))


def _cau_bo_toi(k: dict) -> tuple[str, str]:
    """Hai câu người dùng được mời nhắn sau lệnh bỏ một hoạt động buổi tối chưa nói rõ cách (công tắc `bo_toi_hoi_lai`)."""
    ngay = ", ".join(str(n) for n in k["ngay"])
    return (f"đổi {k['diem']} (buổi tối ngày {ngay}) sang hoạt động tối khác", f"bỏ {k['diem']}, để trống buổi tối ngày {ngay}")


def _cau_them(bang: v2.BangV2, k: dict) -> str:
    """Câu của lệnh THÊM chưa làm (cờ `sua_lich_them_khong_the`). Mọi cách nêu ra đều đã được `_cach_them` thử bằng phép thử của lần áp thật."""
    x = k["diem"]
    ngay, buoi = k["dich"]
    noi = (f"buổi {NHAN_BUOI[buoi]} ngày {ngay}" if ngay is not None and buoi is not None else f"ngày {ngay}" if ngay is not None
           else f"buổi {NHAN_BUOI[buoi]}" if buoi is not None else None)

    moi = "ly_do_cho" in k  # mục dựng khi công tắc `sua_lich_them_day` bật ⇒ chữ mới; tắt ⇒ câu y như cũ
    # lệnh không nói rõ một buổi: lý do của các chỗ đã thử — một loại thì nói thẳng, lẫn thì nêu từng loại (không gán lý do của một buổi cho cả lịch)
    cho_vuong = k.get("ly_do_cho") or []
    vuong = CAU_LY_DO[cho_vuong[0]] if len(cho_vuong) == 1 else ", ".join(f"có buổi thì {CAU_LY_DO[m]}" for m in cho_vuong)

    def cach(g: dict, kem_cho: bool) -> str:
        # cách "thêm thẳng nhưng ngày đó dày hơn nhịp đi" (công tắc `sua_lich_them_day`): nói rõ cái giá ngay cạnh câu gợi ý; câu để nhắn giữ nguyên
        if not moi:
            return _cau_cach(bang, x, g, kem_cho or bool(g.get("day"))) + (" (ngày đó sẽ dày hơn nhịp bạn chọn)" if g.get("day") else "")
        # chữ mới: câu để nhắn nằm RIÊNG trong «…» (lượt trình duyệt 23/11: "thay A bằng X hoặc thay B bằng X" — chép nguyên là gửi một lệnh hai
        # nghĩa); chỗ của điểm bị thay và cái giá "dày hơn nhịp" đứng NGOÀI dấu
        ngoai = (f" (buổi {NHAN_BUOI[g['buoi']]} ngày {g['ngay']})" if kem_cho and g["thay"] is not None else "") + (" (ngày đó sẽ dày hơn nhịp bạn chọn)" if g.get("day") else "")
        return f"«{_cau_cach(bang, x, g, False)}»{ngoai}"

    if k["ma_luat"] == "them_can_thay":
        ro = ngay is not None and buoi is not None  # người dùng nói rõ một buổi ⇒ nêu buổi đó đang có gì; không thì mỗi cách kèm buổi của nó
        vi = f"thêm vào đó thì {CAU_LY_DO[k['ly_do']]}" if k["ly_do"] else "không xếp thêm được một điểm nữa"  # lý do chỉ chắc khi nói rõ một buổi
        o = (f"{noi} đang có {' và '.join(k['dang_co'])}; {vi}" if ro and k["dang_co"]
             else f"đặt vào {noi} thì vướng: {vuong}" if vuong and noi else f"đặt vào buổi nào cũng vướng: {vuong}" if vuong
             else f"{noi or 'lịch'} đang kín, không xếp thêm được một điểm nữa")
        # "đủ câu": lần hiểu ý không thấy lượt trước ⇒ câu đồng ý cụt ("ok thay đi") không được hiểu (đo 21/11: 0 / 6 lượt mỗi model)
        return f"Chưa làm: thêm {x} — {o}. Muốn đổi, bạn nhắn đủ câu: {' hoặc '.join(cach(g, not ro) for g in k['cach'])}."
    vi = (f"vì {CAU_LY_DO[k['ly_do']]}" if k["ly_do"] else f"vì {vuong}" if vuong and noi else f"vì đặt vào buổi nào cũng vướng: {vuong}" if vuong
          else "vì đặt vào đó lịch sẽ phạm luật xếp (giờ mở cửa / cụm xa / quá dày)" if noi or k["ma_luat"] == "thay_bi_chan"
          else "vì đặt vào buổi nào lịch cũng phạm luật xếp (giờ mở cửa / cụm xa / quá dày)")  # không nói chỗ ⇒ không gán lý do riêng của một buổi
    dau = (f"Chưa làm: thay {k['cu']} bằng {x} — {vi}." if k["ma_luat"] == "thay_bi_chan"
           else f"Chưa làm: thêm {x}" + (f" vào {noi}" if noi else "") + f" — {vi}.")
    if not k["cach"]:
        return f"{dau} Lịch này hiện không còn chỗ nào xếp được {x}."
    return f"{dau} Làm được, bạn nhắn đủ câu: {' hoặc '.join(cach(g, True) for g in k['cach'])}."


def _cau_khong_doi(bang: v2.BangV2, k: dict) -> str:
    """Một dòng "không đổi được". Mục có `goi_y` (dời một điểm đang ở trong lịch bị luật xếp chặn) ⇒ lý do + các chỗ dời được."""
    if k["ma_luat"] == "ngay_khong_doi_cho":  # cờ `sua_lich_doi_cho_ngay`: hoán đổi hai ngày bị luật xếp chặn ⇒ lý do lời thường, lịch giữ nguyên
        vi = f"vì {(CAU_LY_DO | CAU_LY_DO_NGAY)[k['ly_do']]}" if k["ly_do"] else "vì lịch sẽ phạm luật xếp (giờ mở cửa / cụm xa / quá dày)"
        return f"Chưa đổi chỗ {k['diem']} được {vi} — lịch giữ nguyên."
    if k["ma_luat"] in ("them_can_thay", "them_bi_chan", "thay_bi_chan"):  # cờ `sua_lich_them_khong_the`; mở đầu "Chưa làm" ⇒ giao diện không gắn "Không đổi được"
        return _cau_them(bang, k)
    if k["ma_luat"] == "bo_toi_hoi":  # công tắc `bo_toi_hoi_lai`; mở đầu "Chưa làm" ⇒ giao diện không gắn "Không đổi được"
        doi, trong = _cau_bo_toi(k)
        return (f"Chưa làm: bỏ {k['diem']} (buổi tối ngày {', '.join(str(n) for n in k['ngay'])}) — bạn muốn đổi sang một hoạt động tối khác hay để trống "
                f"tối đó? Bạn nhắn một trong hai câu: “{doi}” hoặc “{trong}”.")
    if "goi_y" not in k:
        return CAU_KHONG_DOI[k["ma_luat"]].format(diem=k["diem"], ngay=k.get("ngay"))
    ngay, buoi = k["dich"]
    dau = (f"{k['diem']} chưa dời sang buổi {NHAN_BUOI[buoi]} ngày {ngay} được vì {CAU_LY_DO[k['ly_do']]}." if k["ly_do"]
           else CAU_KHONG_DOI["khong_hop_luat"].format(diem=k["diem"]))
    if not k["goi_y"]:
        return f"{dau} Trong lịch này {k['diem']} chỉ đứng được ở chỗ hiện tại."
    cho = "; ".join(f"buổi {NHAN_BUOI[g['buoi']]} ngày {g['ngay']}" + (f" (đổi chỗ với {ten_cua_diem(bang, g['doi_voi'])})" if g["doi_voi"] else "")
                    for g in k["goi_y"])
    return f"{dau} Dời được sang: {cho}."


def thay_doi(bang: v2.BangV2, kq: dict) -> list[dict]:
    """Khối đầu thẻ lịch (giao diện H1 `lich.thay_doi`): mỗi ý một dòng do CODE viết — {cau, duoc}."""
    out = []
    for a in kq["da_ap"]:
        t = a["loai"]
        if t == "bo_diem":
            xep_toi = a.get("toi_xep_lai")  # có ⇒ buổi tối của ngày khác cũng đổi: nêu cả dãy buổi tối, hoạt động tối mới nằm trong dãy đó
            lap = "; ".join(f"{ten_cua_diem(bang, x['diem'])} (ngày {x['ngay']}, buổi {NHAN_BUOI.get(x['buoi'], 'tối')})"
                            for x in a.get("lap", ()) if not (xep_toi and x["buoi"] == "toi"))
            if a.get("toi_doi") is not None:  # công tắc `bo_toi_hoi_lai`, người dùng chọn ĐỔI: nói tối nào đổi sang gì; hết mục chưa dùng ⇒ nói thật là để trống
                co = "; ".join(f"buổi tối ngày {x['ngay']} đổi sang {ten_cua_diem(bang, x['diem'])}" for x in a["toi_doi"] if x["diem"])
                het = ", ".join(str(x["ngay"]) for x in a["toi_doi"] if not x["diem"])
                out.append(f"Đã bỏ {ten_cua_diem(bang, a['diem'])}" + (f"; {co}" if co else "")
                           + (f"; buổi tối ngày {het} để trống vì lịch không còn hoạt động tối nào khác chưa dùng" if het else "") + "."
                           + (_cau_toi_xep_lai(bang, xep_toi) if xep_toi else ""))
                continue
            trong = a.get("toi_trong")  # công tắc `bo_toi_de_trong`: nói rõ tối nào để trống (không có dòng này người đọc chờ một hoạt động thay vào)
            out.append(f"Đã bỏ {ten_cua_diem(bang, a['diem'])}" + (f", thêm {lap} vào chỗ trống." if lap else
                                                                   f"; buổi tối ngày {', '.join(str(n) for n in trong)} để trống." if trong else ".")
                       + (_cau_toi_xep_lai(bang, xep_toi) if xep_toi else ""))
        elif t == "them_diem":
            thay = f", thế chỗ {ten_cua_diem(bang, a['the_cho'])}" if a.get("the_cho") else ""
            out.append(f"Đã thêm {ten_cua_diem(bang, a['diem'])} (ngày {a['ngay']}, buổi {NHAN_BUOI[a['buoi']]}{thay})."
                       + (_cau_day(a["day"]) if a.get("day") else "")
                       + (_cau_toi_xep_lai(bang, a["toi_xep_lai"]) if a.get("toi_xep_lai") else ""))
        elif t == "doi_buoi":
            out.append(f"Đã dời {ten_cua_diem(bang, a['diem'])} sang buổi {NHAN_BUOI[a['buoi']]} ngày {a['ngay']}."
                       + (_cau_day(a["day"]) if a.get("day") else "")
                       + (_cau_toi_xep_lai(bang, a["toi_xep_lai"]) if a.get("toi_xep_lai") else ""))
        elif t == "thay_diem":
            out.append(f"Đã thay {ten_cua_diem(bang, a['diem'])} bằng {ten_cua_diem(bang, a['moi'])}."
                       + (_cau_toi_xep_lai(bang, a["toi_xep_lai"]) if a.get("toi_xep_lai") else ""))
        elif t == "doi_cho_ngay":
            out.append(f"Đã đổi chỗ các điểm buổi sáng và chiều của ngày {a['ngay_a']} với ngày {a['ngay_b']}; hoạt động buổi tối giữ theo từng ngày.")
            if a.get("xep_them"):  # nói thật khi bộ xếp đổi nhiều hơn điều được nhờ
                out.append("Ngoài phần đổi chỗ, lịch xếp lại thêm: " + _phan_xep_lai(bang, a["xep_them"]) + ".")
    # lịch chưa có mức hạng (khối nơi ở chưa hiện) ⇒ lượt này BẬT khối: nói "đã thêm", không nói "đổi … chưa chọn → …"
    out += [f"Đã thêm gợi ý chỗ ở hạng {ten_muc_o(moi)}." for f, cu, moi in kq["doi_truong"] if f == "ngan_sach" and cu is None]
    out += [f"Đã đổi {NHAN_TRUONG[f]}: {_gia_tri(f, cu)} → {_gia_tri(f, moi)}."
            for f, cu, moi in kq["doi_truong"] if not (f == "ngan_sach" and cu is None)]
    xl = kq.get("xep_lai")
    if xl is not None:
        out.append("Lịch xếp lại theo lựa chọn mới: " + _phan_xep_lai(bang, xl) + "." if any(xl.values()) else "Các điểm trong lịch giữ nguyên chỗ.")
    nd = kq.get("ngay_di")
    if nd:
        moi = dt.date.fromisoformat(nd["moi"])
        out.append(f"Đã đổi ngày đi: {_dd_mm(dt.date.fromisoformat(nd['cu'])) if nd['cu'] else 'chưa chọn'} → {_dd_mm(moi)} ({THU[moi.weekday()]}).")
        if nd["doi_cho"] or nd["ra"] or nd["vao"]:
            out.append("Lịch xếp lại theo ngày mới (thứ trong tuần, mùa, dự báo): " + _phan_xep_lai(bang, nd) + ".")
        else:
            out.append("Các điểm trong lịch giữ nguyên chỗ.")
        if not nd["co_du_bao"]:
            out.append(v2.CAU_CHUA_DU_BAO)
    dong = [{"cau": c, "duoc": True} for c in out]
    dong += [{"cau": _cau_khong_doi(bang, k), "duoc": False} for k in kq["khong_doi"]]
    co_dinh = {VIEC_KHAC: CAU_VIEC_KHAC, CHUA_HO_TRO: CAU_CHUA_HO_TRO}
    dong += [{"cau": co_dinh.get(t) or f"Chưa làm: {NHAN_HANH_DONG[t]} — bạn nhắn tiếp nhé.", "duoc": False} for t in kq["chua_lam"]]
    if kq.get("hoi_them"):  # cờ `sua_lich_kem_hoi`: tin còn có câu hỏi ⇒ nói thật là lượt sửa chưa trả lời nó (dòng cuối khối, `duoc` False ⇒ không đổi "có ý nào áp được")
        dong.append({"cau": CAU_HOI_THEM, "duoc": False})
    return dong


# Cổng từ khoá đã thử và BỎ (đo 14/11, `tools/do_cong_tu_sua.py`): bộ chuỗi đã thấy 17 / 19 câu sửa qua cổng, câu diễn đạt lạ 3 / 10 (sàn A
# đặt 8 / 10) ⇒ khi cuộc có lịch đã lưu, lượt nào cũng qua lần "hiểu ý sửa" (rỗng ⇒ đường trả lời thường).


def tin_nhan_hieu(bang: v2.BangV2, luu: dict, cau: str, goi_y: tuple[str, ...] = ()) -> str:
    """Tin nhắn cho lần "hiểu ý sửa": lịch hiện tại (ngày · buổi · tên — dữ liệu code) + tham số + câu người dùng.
    `goi_y` (cờ `sua_lich_them_khong_the`, chỉ ở lượt NGAY SAU một lượt có dòng gợi ý): các câu code đã gợi ý ở lượt trước — lần hiểu ý không thấy lượt
    trước nên lời đồng ý cụt ("ok thay đi") từng ra danh sách rỗng; ở model đang chạy lượt đó rơi sang đường hỏi đáp thường và viết "Mình đã thêm…"
    trong khi lịch không đổi (chuỗi đo 21/11). Rỗng ⇒ tin nhắn giống từng byte bản cũ."""
    k, ts = luu["khung"], luu["khung"]["tham_so"]
    dong = [f"Tham số: {ts['so_ngay']} ngày · kiểu đi {ts['kieu_di']} · sở thích {', '.join(ts['so_thich']) or 'không chọn'}", "Lịch hiện tại:"]
    for ng in k["ngay"]:
        for b in v2.BUOI:
            ten = [ten_cua_diem(bang, j) for j in ng["buoi"][b]]
            if ten:
                dong.append(f"- Ngày {ng['ngay']} · {({'sang': 'sáng', 'chieu': 'chiều', 'toi': 'tối'})[b]}: {'; '.join(ten)}")
    trong = {j for ng in k["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    dong += ["", "Điểm khác có thể thêm / thay vào (chép đúng tên khi điền ten / ten_moi): "
             + "; ".join(d["ten"] for d in bang.diem if d["id"] not in trong)]  # điểm trong lịch đã có tên ở trên ⇒ không lặp (bớt token)
    them = ""
    if goi_y:
        them = ("\n\nLượt ngay trước, trợ lý CHƯA làm một lệnh sửa của người dùng và đã đề nghị họ nhắn đủ một trong các câu sau:\n"
                + "\n".join(f"- {c}" for c in goi_y)
                + "\nNếu câu người dùng dưới đây chỉ là lời ĐỒNG Ý với đề nghị đó mà không nêu đủ tên điểm (\"ok thay đi\", \"ừ đổi luôn nhé\", \"thay cái đó đi\"…): "
                  "chỉ có MỘT câu đề nghị ⇒ trả đúng hành động của câu đó; có hai câu mà không rõ họ chọn câu nào ⇒ không tự chọn, trả một hành động "
                  "chua_ho_tro. Câu người dùng từ chối, còn phân vân, hoặc hỏi chuyện khác ⇒ KHÔNG coi là đồng ý, xử lý như một câu bình thường.")
    return "\n".join(dong) + them + "\n\nCâu người dùng: " + cau.strip()


def sua_ap(kq: dict) -> dict:
    """Dữ liệu code của lượt sửa (id điểm, mã luật — không chữ): cho bộ đo so với nhãn và cho log."""
    return {"da_ap": kq["da_ap"], "doi_truong": [[f, cu, moi] for f, cu, moi in kq["doi_truong"]], "ngay_di": kq.get("ngay_di"),
            "khong_doi": kq["khong_doi"], "chua_lam": kq["chua_lam"], "the": None if kq["the"] is None else kq["the"]["cu"]}
