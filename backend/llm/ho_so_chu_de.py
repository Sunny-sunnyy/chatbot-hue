"""Công tắc `ho_so_chu_de` — HỒ SƠ THEO CHỦ ĐỀ (bản thử, nhánh thu-b-ho-so-chu-de; chủ dự án chọn 22:19 24/11/2026: người dùng CHỌN chủ đề từ danh sách, không
gõ tự do). Phần này: DANH SÁCH CHỦ ĐỀ do code dựng từ mục lục kho.

Mỗi chủ đề = một luật thành viên do code áp lên mục lục (thư mục của bài + mẫu trên TÊN bài) và một tên gọi cho du khách (đặt tay, cố định ở đây). Chủ đề
có dưới `NGUONG_BAI` bài thì KHÔNG hiện (kho đổi ⇒ danh sách tự đổi). Model không tham gia chọn bài: tập bài của một chủ đề là kết quả của luật, nên không
có bài "độn" (phép thử 24/11/2026: để model tự chọn bài từ cả mục lục thì 3 / 6 chủ đề bị độn bài lạc đề; code chọn tập bài thì 6 / 6 đạt).

Dựng một hồ sơ (route `api/routes/ho_so.py`): model GOM tập bài của chủ đề thành mục + đặt tên mục (`kiem_dan_y` kiểm lại bằng code: bài nào cũng có mặt
đúng một lần) ⇒ mỗi mục: code chọn đoạn của chính các bài trong mục, MỘT lời gọi có khuôn viết các ý ngắn có nguồn, code lọc ý bằng luật của sổ tay
(`so_tay.loc_y`: có nguồn hợp lệ, đủ ngắn, vế nói giờ / giá bị gỡ), chọn ý sao cho MỖI BÀI của mục có ít nhất một ý (`chon_y_phu_bai`), bài không có ý nào
⇒ ô thiếu mang tên bài; giờ mở cửa / giá vé do code chép từ bảng thẻ nơi (`dong_du_kien`). Model không được kể "kho còn thiếu gì" (đó là hiểu biết riêng
của model — bản thử 24/11/2026 nó gọi tên cũ của một bảo tàng kho CÓ bài là thứ kho thiếu).

Module thuần: không đọc cấu hình, không SDK, không mạng.
"""
import math
import re
from dataclasses import dataclass

from llm import so_tay as st
from llm import the_noi as thn

NGUONG_BAI = 5      # chủ đề có ít bài hơn ⇒ không vào danh sách
TRAN_BAI = 40       # nhiều hơn ⇒ lấy `TRAN_BAI` bài đầu theo thứ tự mục lục (ghi `bi_cat` để nói thật)


@dataclass(frozen=True)
class ChuDe:
    ma: str
    ten: str                      # tên hiện cho du khách
    thu_muc: tuple[str, ...]      # bài thuộc chủ đề phải nằm dưới một trong các thư mục này của kho
    co: str | None = None         # mẫu (không phân biệt hoa thường) phải khớp TÊN bài; None = mọi bài của thư mục
    khong: str | None = None      # mẫu loại trừ trên tên bài


CHU_DE = (
    ChuDe("lang_tam", "Lăng tẩm các vua Nguyễn", ("heritages/heritage/",), r"^Lăng\b"),
    ChuDe("kinh_thanh", "Kinh thành, Đại Nội và di tích cung đình", ("heritages/heritage/",),
          r"Đại Nội|Kinh thành|Quần thể Di tích|Cửu Đỉnh|Lục Bộ|Cung An Định|^Đàn |Hổ Quyền|Bảo tàng|^Phủ "),
    ChuDe("chua", "Chùa và nơi thờ tự", ("heritages/heritage/",), r"^Chùa\b|Nhà thờ|^Điện Hòn Chén"),
    ChuDe("di_san", "Di sản tư liệu và di sản phi vật thể", ("heritages/heritage/",), r"Châu bản|Mộc bản|Thơ văn|Nhã nhạc|Bài Chòi|thờ Mẫu|Tri thức dân gian"),
    ChuDe("bien_dam_pha", "Biển và đầm phá", ("travel/places/",), r"^Bãi biển|^Đầm |^Phá |đầm phá|^Vịnh "),
    ChuDe("nui_suoi", "Núi, đồi, suối và thác", ("travel/places/",), r"^Núi |^Suối |^Thác |^Đồi |^Đèo |^Hòn |Bạch Mã|Thác A Nôr"),
    ChuDe("cho", "Chợ và mua sắm", ("travel/places/",), r"^Chợ |chợ Bao Vinh|AEON"),
    ChuDe("pho_cau", "Phố đi bộ, cầu và công viên ven sông", ("travel/places/",), r"^Phố đi bộ|^Khu phố|^Cầu |^Công viên|^Cồn "),
    ChuDe("le_hoi", "Lễ hội dân gian và làng xã", ("festivals/festival/",), r"^Lễ hội|^Hội |^Ngày hội|^Chợ quê"),
    ChuDe("nghi_le", "Nghi lễ và tín ngưỡng", ("festivals/festival/",), r"^Lễ (?!hội)|^Đại lễ"),
    ChuDe("tet_festival", "Tết và Festival Huế", ("festivals/festival/",), r"^Tết |^Festival"),
    ChuDe("nghe_thuat", "Ca Huế và nghệ thuật biểu diễn", ("performing_arts/arts/",)),
    ChuDe("mon_dac_san", "Món đặc sản Huế", ("foods/local_specialties/",)),
    ChuDe("bun_bo", "Bún bò Huế: món và quán", ("foods/", "heritages/heritage/"), r"bún bò"),
    ChuDe("com_hen", "Cơm hến: món và quán", ("foods/",), r"cơm hến|cháo hến|bún hến"),
    ChuDe("banh", "Các loại bánh Huế: món và quán", ("foods/local_specialties/", "foods/restaurants/"), r"^Bánh |bánh canh|Quán Bánh|bánh Bà", r"bánh mì"),
    ChuDe("quan_chay", "Quán chay", ("foods/restaurants/",), r"\bchay\b"),
    ChuDe("ca_phe", "Quán cà phê", ("foods/cafes/",)),
    ChuDe("luu_tru", "Chọn khu để ở khi đến Huế", ("travel/services/",), r"^Lưu trú"),
    # Tên nói "cách", không hứa bảng giá: ý nào của model nêu số tiền đều bị code gỡ (giá chỉ đi đường code chép, mà bài vé không phải một "nơi" có dòng trong
    # bảng thẻ nơi) — lượt thật 24/11/2026 bỏ 7 ý nêu giá ở chủ đề này; bảng giá nằm trong bài vé, mở từ khối nguồn của mục.
    ChuDe("ve_di_lai", "Cách mua vé, đi lại và tính chi phí", ("travel/tickets/", "travel/services/"), r"^Vé |vé du lịch|^Đi lại|^Đi từ|^Chi phí|^Leo bậc"),
)


def bai_cua(chu_de: ChuDe, muc_luc) -> list:
    """Các bài mục lục thuộc một chủ đề, theo thứ tự mục lục."""
    co = re.compile(chu_de.co, re.IGNORECASE) if chu_de.co else None
    khong = re.compile(chu_de.khong, re.IGNORECASE) if chu_de.khong else None
    return [b for b in muc_luc if b.rel.startswith(chu_de.thu_muc) and (co is None or co.search(b.tieu_de))
            and not (khong is not None and khong.search(b.tieu_de))]


def danh_sach(muc_luc) -> list[dict]:
    """Danh sách chủ đề hiện cho người dùng: chỉ chủ đề có đủ `NGUONG_BAI` bài, theo thứ tự của `CHU_DE`."""
    ra = []
    for c in CHU_DE:
        bai = bai_cua(c, muc_luc)
        if len(bai) >= NGUONG_BAI:
            ra.append({"ma": c.ma, "ten": c.ten, "so_bai": min(len(bai), TRAN_BAI), "bi_cat": len(bai) > TRAN_BAI})
    return ra


# ---------- dựng hồ sơ ----------
SO_MUC_TOI_DA = 8
BAI_MOI_MUC = 6            # dàn ý của model: mỗi mục nhiều nhất chừng này bài (mục dự phòng do code chia cũng vậy)
SO_DOAN_MUC = 12           # số đoạn kho đưa cho model ở một mục (chia đều cho các bài của mục, mỗi bài ít nhất 2)
TRAN_KY_TU_Y = 240         # một ý của hồ sơ dài hơn ⇒ bỏ (sổ tay: 200; ý hồ sơ hay mang tên riêng + năm nên nới)
Y_IT_NHAT, Y_NHIEU_NHAT = 6, 10
NGUONG_MONG = 3            # mục còn dưới chừng này ý ⇒ `muc_do: "mong"`
MUC_KHAC = "Các bài khác của chủ đề"
NHAN_DU_KIEN = "Giờ mở cửa và giá vé"
CUM_XEP = "tổng quan giới thiệu lịch sử nổi bật đặc điểm"


def chia_muc_du_phong(so_bai: int) -> list[dict]:
    """Dàn ý do CODE chia khi bước dàn ý của model hỏng: các bài theo thứ tự kho, mỗi mục `BAI_MOI_MUC` bài, tên mục để trống (route đặt tên bằng tên bài)."""
    return [{"tieu_de": "", "bai": list(range(i, min(i + BAI_MOI_MUC, so_bai + 1)))} for i in range(1, so_bai + 1, BAI_MOI_MUC)]


def kiem_dan_y(muc_model: list[dict], so_bai: int) -> list[dict]:
    """Dàn ý model trả (`[{tieu_de, bai: [số 1…so_bai]}]`) ⇒ dàn ý đã qua luật của code: số lạ bị gỡ · một bài chỉ đứng ở mục ĐẦU TIÊN nêu nó · mục không còn
    bài nào bị bỏ · nhiều hơn `SO_MUC_TOI_DA` mục ⇒ các mục thừa dồn vào mục cuối · bài không mục nào nêu ⇒ một mục cuối `MUC_KHAC` (không bài nào của
    chủ đề bị lặng lẽ bỏ). Rỗng / hỏng ⇒ `chia_muc_du_phong`."""
    da, muc = set(), []
    for m in muc_model or ():
        bai = []
        for n in m.get("bai") or ():
            if isinstance(n, int) and 1 <= n <= so_bai and n not in da:
                da.add(n)
                bai.append(n)
        if bai:
            muc.append({"tieu_de": " ".join(str(m.get("tieu_de") or "").split())[:90], "bai": bai})
    if not muc:
        return chia_muc_du_phong(so_bai)
    if len(muc) > SO_MUC_TOI_DA:
        muc = muc[:SO_MUC_TOI_DA - 1] + [{"tieu_de": muc[SO_MUC_TOI_DA - 1]["tieu_de"], "bai": [n for m in muc[SO_MUC_TOI_DA - 1:] for n in m["bai"]]}]
    con = [n for n in range(1, so_bai + 1) if n not in da]
    if con:
        muc.append({"tieu_de": MUC_KHAC, "bai": con})
    return muc


def so_doan_moi_bai(so_bai: int) -> int:
    return max(2, SO_DOAN_MUC // max(so_bai, 1))


def chon_y_phu_bai(y: list[str], bai_cua_nguon: dict[int, str], thu_tu_bai: list[str]) -> tuple[list[str], list[str]]:
    """Các ý đã qua `so_tay.loc_y` (mỗi dòng kết bằng "[n][m]") ⇒ (các ý được giữ theo thứ tự gốc, các bài của mục KHÔNG có ý nào). Mỗi bài của mục lấy trước
    MỘT ý đầu tiên nói về nó, rồi mới lấy thêm theo thứ tự cho tới trần (`Y_IT_NHAT`…`Y_NHIEU_NHAT` theo số bài) — bản thử 24/11/2026 lấy sáu ý đầu làm mục
    "các lăng đầu triều" không còn ý nào về Lăng Thiệu Trị."""
    cua = [{bai_cua_nguon[int(n)] for n in re.findall(r"\[(\d+)\]", dong) if int(n) in bai_cua_nguon} for dong in y]
    tran = min(Y_NHIEU_NHAT, max(Y_IT_NHAT, len(thu_tu_bai) + 2))
    chon = []
    for bai in thu_tu_bai:
        if any(bai in cua[i] for i in chon):
            continue
        i = next((i for i in range(len(y)) if i not in chon and bai in cua[i]), None)
        if i is not None:
            chon.append(i)
    chon += [i for i in range(len(y)) if i not in chon][:max(tran - len(chon), 0)]
    chon = sorted(chon)[:max(tran, len(thu_tu_bai))]
    co = {b for i in chon for b in cua[i]}
    return [y[i] for i in chon], [b for b in thu_tu_bai if b not in co]


def dong_du_kien(bai: list, bang_the: "thn.Bang | None", tu_so: int) -> tuple[dict | None, list[dict]]:
    """Khối "Giờ mở cửa và giá vé" của một mục, do code chép từ bảng thẻ nơi cho từng bài là MỘT nơi có dòng nhãn: (đoạn `gach` hoặc None, nguồn đánh số
    từ `tu_so`). Bài không có dòng nào thì không có dòng (không in ô thiếu ở đây — hồ sơ không phải thẻ điểm)."""
    the = {n.rel: n for n in (bang_the.noi if bang_the else ())}
    gach, nguon = [], []
    for b in bai:
        noi = the.get(b.rel)
        if noi is None:
            continue
        gio = next((st._NHAN_GIO.sub("", d).strip().rstrip(".") for d in noi.dong if st._NHAN_GIO.match(d)), None)
        ve = st._ve_chu(noi.ve) if noi.ve else None
        if not (gio or ve):
            continue
        so = []
        if gio:
            nguon.append({"id": tu_so + len(nguon), "title": noi.ten, "bai_id": noi.rel, "heading_path": [thn.MUC_THE], "excerpts": [d for d in noi.dong if st._NHAN_GIO.match(d)]})
            so.append(nguon[-1]["id"])
        if ve:
            nguon.append({"id": tu_so + len(nguon), "title": bang_the.ve_tieu_de, "bai_id": bang_the.ve_rel or None, "heading_path": [thn.MUC_VE],
                          "excerpts": [d for d in (bang_the.ve_dau, noi.ve) if d]})
            so.append(nguon[-1]["id"])
        gach.append(f"{b.tieu_de} — " + "; ".join(x for x in (f"giờ mở cửa: {gio}" if gio else None, f"giá vé: {ve}" if ve else None) if x) + " " + "".join(f"[{n}]" for n in so))
    return ({"nhan": NHAN_DU_KIEN, "kieu": "gach", "chu": None, "gach": gach} if gach else None), nguon


def muc_do(so_y: int) -> str:
    return "mong" if so_y < NGUONG_MONG else "du"
