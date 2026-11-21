"""Công cụ `gan_diem` — "gần một điểm có gì" (cờ `gan_diem`, 21/11/2026; plan private `data/thu_bedrock_2026-11-21/c_muc_5/PLAN_P1.md`).

Vì sao: kho không viết "quán A gần điểm B" nên trợ lý không khẳng định được "gần" — lượt mốc 12 vai: câu "trưa gần Đại Nội có quán nào ăn ngon" ra "tư liệu
không nói quán nào nằm gần Đại Nội" ở 4 / 5 lượt, trong khi hệ thống đã có toạ độ của 42 quán có bài kho và 40 điểm (quanh Đại Nội có 17 quán kho trong 2 km).

Mọi thứ do CODE tính, model chỉ gửi hai giá trị trong danh sách đóng (mã điểm, loại) và diễn đạt kết quả:
- quán ăn / cà phê: bảng quán của thẻ lịch (`quan_lich`), CHỈ dòng có bài kho, ≤ `KM_TOI_DA` km đường chim bay quanh toạ độ điểm, gần trước, tối đa `SO_TOI_DA`;
- điểm tham quan: bảng khoảng cách đang có (`khoang_cach`) ⇒ `SO_TOI_DA` điểm gần nhất theo km đường đi, in km + phút như công cụ khoảng cách.
Không có gì / nơi ngoài bảng ⇒ một dòng cố định nói thật. Không quán nguồn mở, không đọc địa chỉ để suy "gần", không nhận chữ tự do của người dùng.
"""
import re
import unicodedata

from llm import khoang_cach as kc
from llm.quan_lich import _km as km_chim_bay

KHAC = kc.KHAC
LOAI = ("quan_an", "ca_phe", "diem_tham_quan")
NHAN_LOAI = {"quan_an": "quán ăn", "ca_phe": "quán cà phê", "diem_tham_quan": "điểm tham quan"}
KM_TOI_DA = 2.0  # cùng ngưỡng "gần" của mục ăn uống trong thẻ lịch (`quan_lich.KM_TOI_DA`)
SO_TOI_DA = 5
NGUON_SOURCE = "he-thong-gan-diem"  # `source` của nguồn — không thuộc tiền tố bài kho
MUC_NGUON = "Hệ thống tính theo vị trí"
CAU_NGOAI_BANG = "Mình chưa có vị trí của nơi này nên chưa tính được những gì ở gần đó."
CAU_GHI_CHU_QUAN = ("Khoảng cách tính theo đường chim bay từ vị trí trên bản đồ, đường đi thật có thể dài hơn; giờ mở cửa, món và giá xem ở bài của "
                    "từng quán trong kho.")
CAU_GHI_CHU_DIEM = kc.CAU_GHI_CHU

# Từ khoá của lượt (câu cuối hoặc câu hỏi liền trước) — chỉ để quyết có ĐƯA công cụ hay không khi cổng công cụ ở chế độ theo từ khoá. Bật thừa vô hại
# (model không gọi); bỏ sót ⇒ lượt đi như cũ.
_TU_KHOA = re.compile(r"(?<!\w)(?:gần|quanh|cạnh|lân cận|kế bên|sát bên)(?!\w)", re.IGNORECASE)


def co_tu_khoa_luot(query: str, history) -> bool:
    def co(t: str) -> bool:
        return bool(_TU_KHOA.search(unicodedata.normalize("NFC", t)))
    return co(query) or bool(history and co(history[-1][0]))


def _chu_cach(km: float, muc: str | None) -> str:
    """Chữ khoảng cách của một quán. Toạ độ mức "ước" ⇒ chỉ nói theo nấc, không số lẻ (vị trí quán có thể lệch vài trăm mét).
    Nấc gần viết "chưa tới 1 km": bản đầu viết "trong khoảng 1 km" thì model chép lại thành "khoảng 1 km" ở 8 / 8 lần của lượt đo 21/11 — quán cách vài
    trăm mét nghe như cách một cây số."""
    if muc == "uoc":
        return "chưa tới 1 km" if km < 1 else "khoảng 1–2 km"
    return kc._km(km)


def quan_gan(theo_cum: dict, toa_diem: tuple[float, float], loai: str) -> list[tuple[dict, float]]:
    """Quán CÓ BÀI KHO đúng loại trong `KM_TOI_DA` km quanh toạ độ điểm, gần trước (bằng nhau ⇒ theo tên), tối đa `SO_TOI_DA`. Xét mọi cụm: điểm ở rìa
    cụm vẫn thấy quán của cụm kề (mục ăn uống của thẻ lịch chỉ lấy cùng cụm vì nó gắn với đường đi trong ngày)."""
    ung = [(q, km_chim_bay(toa_diem, q["toa"])) for ds in theo_cum.values() for q in ds if q["nguon"] == "kho" and q["loai"] == loai]
    return sorted((x for x in ung if x[1] <= KM_TOI_DA), key=lambda x: (x[1], x[0]["ten"]))[:SO_TOI_DA]


def diem_gan(bang: kc.BangKhoangCach, diem: str) -> list[tuple[str, float, int]]:
    """`SO_TOI_DA` điểm tham quan gần `diem` nhất theo km đường đi của bảng khoảng cách ⇒ (mã, km, phút đã chỉnh như công cụ khoảng cách)."""
    ung = [(j, v["km"], int(v["phut"] * kc.HE_SO_OSRM + 0.5) + kc.PHUT_CONG) for j in bang.ids if j != diem and (v := bang.cap.get(f"{diem}|{j}")) is not None]
    return sorted(ung, key=lambda x: (x[1], x[0]))[:SO_TOI_DA]


def tieu_de(bang: kc.BangKhoangCach, diem: str, loai: str) -> str:
    return f"Gần {bang.ten[diem]}: {NHAN_LOAI[loai]}" if diem in bang.ten else f"Gần một nơi ngoài danh sách: {NHAN_LOAI[loai]}"


def ket_qua(bang: kc.BangKhoangCach, theo_cum: dict, toa_do: dict, diem: str, loai: str) -> tuple[tuple[str, ...], int]:
    """(các dòng của nguồn, số quán / điểm trả ra). Nơi ngoài danh sách hoặc điểm không có toạ độ / không có trong bảng khoảng cách ⇒ câu cố định, 0."""
    if diem == KHAC or diem not in bang.ten:
        return (CAU_NGOAI_BANG,), 0
    ten = bang.ten[diem]
    if loai == "diem_tham_quan":
        ds = diem_gan(bang, diem)
        if not ds:
            return (CAU_NGOAI_BANG,), 0
        dong = [f"Các điểm tham quan gần {ten} nhất (theo đường đi):"]
        dong += [f"- {bang.ten[j]}: {kc._km(km)} đường đi, {kc._phut(phut)}." for j, km, phut in ds]
        return (*dong, CAU_GHI_CHU_DIEM), len(ds)
    toa = toa_do.get(diem)
    if toa is None:
        return (CAU_NGOAI_BANG,), 0
    ds = quan_gan(theo_cum, toa, loai)
    if not ds:
        return (f"Trong kho chưa có bài về {NHAN_LOAI[loai]} nào trong khoảng {KM_TOI_DA:g} km quanh {ten}.",), 0
    dong = [f"{NHAN_LOAI[loai].capitalize()} có bài trong kho quanh {ten} (gần trước):"]
    dong += [f"- {q['ten']}: cách {ten} {_chu_cach(km, q.get('muc_toa_do'))} theo đường chim bay." for q, km in ds]
    return (*dong, CAU_GHI_CHU_QUAN), len(ds)


def mo_ta_cong_cu(bang: kc.BangKhoangCach) -> str:
    """Mô tả công cụ: luật ngắn + danh sách `mã: tên (tên khác)` (cùng danh sách với công cụ khoảng cách) để model ánh xạ tên người dùng gõ ⇒ mã."""
    dong = [f"{i}: {bang.ten[i]}" + (f" ({', '.join(bang.ten_khac[i])})" if bang.ten_khac[i] else "") for i in bang.ids]
    return ("Những gì Ở GẦN một điểm ở Huế trong danh sách dưới, do hệ thống tính theo vị trí: quán ăn hoặc quán cà phê có bài trong kho, hoặc các điểm tham "
            "quan gần nhất. Chỉ gọi khi người dùng hỏi quanh / gần MỘT nơi có gì (ăn gì gần đó, quán nào gần, gần đó còn điểm nào để ghé). diem = mã của "
            f"nơi được hỏi; nơi không có trong danh sách (khách sạn, ga, sân bay, \"trung tâm\", \"chỗ mình ở\"…) ⇒ \"{KHAC}\", không chọn điểm gần giống. "
            "loai = quan_an | ca_phe | diem_tham_quan. Kết quả là một nguồn có mã [n]: chỉ gọi là \"gần\" những nơi có trong đó và chỉ dùng đúng chữ "
            "khoảng cách trong đó, ghi mã [n]; địa chỉ, giờ mở cửa, món của từng quán thì tìm trong kho theo tên quán. Kết quả nói không có ⇒ nói thật "
            "là chưa có, không tự nêu quán khác là gần.\n"
            "Danh sách:\n" + "\n".join(dong))
