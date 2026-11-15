# Review — nhánh `p9-ngan-sach-o` (chọn chỗ ở theo hạng sao)

Người kiểm: E (`hue-rag-3e`) · ghi lúc 10:42 15/11/2026 (`date`) · người làm: B · plan khách sạn bản 2 §2 (sha `b5d8bc184090`, User duyệt 15/11).
Phạm vi: `855a535`, dựng trên `3c27cc9` (main lúc đó). 11 file, +160 / −17 (gồm report của B).

**Kết luận: `ready_for_user_confirmation`.** Có 1 minor về chữ nhãn, không chặn.

## Đã kiểm (tự chạy / đọc code)

| Cổng | Kết quả |
|---|---|
| Đúng plan bản 2 | Nút "1 sao · 2–3 sao · 4–5 sao", không bắt buộc. Đủ 5 chỗ chạm của B (`ThamSoV2` + `tu_truong`, dict `tham_so` trong `xep_v2`, `sua_lich_v2._ts`, `gan_o_an ⇒ o_dau ⇒ chon_co_so`, `O_BIEU_MAU_V2`). "Mình hiểu" không thêm mức. Mức trống ⇒ lùi im lặng về (2, 2, 1). Đều như plan |
| Lệch plan: nút ở `LenKeHoach.jsx`, không ở `chung.jsx` | Chấp nhận. `LenKeHoachV2` là biểu mẫu bản 2 đang chạy; `BIEU_MAU` của `chung.jsx` là biểu mẫu cũ. Plan ghi nhầm chỗ, hành vi đúng ý plan |
| T1 — không chọn ⇒ như cũ | Đọc code: `chon_co_so(…, None)` ⇒ `_chon(SO_THEO_MUC)`, đúng vòng lặp cũ. Khoá `ngan_sach` chỉ thêm vào `tham_so` khi có chọn ⇒ khung lưu giống byte. Test khẳng định 0 khung mô phỏng có khoá (B băm 3.840 khung main = nhánh — E không chạy lại) |
| Trạng thái lịch bị sửa từ trình duyệt ⇒ `MUC_NGAN_SACH[x]` lỗi `KeyError`? | Không xảy ra: lịch lưu ở server (`conversations.lay_lich`, `chat.py:453`), giá trị chỉ vào qua `TruongInput` (Literal ba giá trị, `extra="forbid"`) |
| Lịch cũ đã lưu / lịch mẫu "Ví dụ" (không có khoá) | `ts_k.get("ngan_sach")` / `tham_so.get` ⇒ `None` ⇒ như cũ |
| T3 — model không thấy mức | Test so byte `tin_nhan_model`, `tin_nhan_hieu`, `ghep_cau_v2`, `minh_hieu` có / không mức. Đúng chỗ cần khoá |
| T4 — sửa lịch giữ mức | Test đi qua `sl.ap` thật (đổi số ngày ⇒ xếp lại) ⇒ `gan_o_an` chỉ ra 4–5 sao |
| Test cũ đổi ví dụ ô lạ `ngan_sach` ⇒ `gia_phong` | Đúng: `ngan_sach` nay là ô thật, nên đổi ví dụ để test "ô lạ bị từ chối" vẫn có nghĩa |
| `settings.yaml` đổi cờ ⇒ chạy cả có / không `--env-file` | `test_luu_tru_lich` + `test_len_ke_hoach_v2` + `test_sua_lich_v2`: **111 passed** cả hai cách (26,8 s / 27,7 s) |
| `git diff --check` | sạch |

## Finding

**m-1 (minor, tuỳ A / User):** nút "1 sao" gồm cả cơ sở **không có sao**.
- `MUC_HANG` xếp "Đạt chuẩn phục vụ khách du lịch" chung mức với 1 sao (`luu_tru_lich.py:22`).
- Ở trung tâm, mức này có nhiều cơ sở 1 sao (đứng trước theo hạng), nên 5 cơ sở hiện ra đều là 1 sao.
- Nhưng ở ven biển phía Thuận An, hai cơ sở mức này (Phúc Khang, Villa Louise Beach) đều là "Đạt chuẩn". Khách bấm "1 sao" sẽ thấy 2 cơ sở không có sao. Đây là E suy từ bảng lưu trú v2, chưa chạy mô phỏng riêng. Chỉ gặp ở lịch ven biển (36 / 3.840 khung theo đếm của C).
- Đóng khi (chọn một): (a) đổi nhãn thành "1 sao / đạt chuẩn" (1 dòng JSX); hoặc (b) giữ như plan đã duyệt và ghi vào giới hạn. E nghiêng về (a): nhãn khớp đúng thứ khách thấy.

## Tiền / thời gian
0 USD. Pytest 2 × ~27 s. Không Playwright (B đã chạy 1440). Nhánh chỉ thêm một nhóm nút cùng kiểu `chip` đang có.
