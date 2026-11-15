# Review — nhánh `p9-ghi-chu-an` (ghi chú ăn uống Bạch Mã / Nhị Hồ)

Người kiểm: E (`hue-rag-3e`) · ghi lúc 09:53 15/11/2026 (`date`) · người làm: C · A giao (risk-gated-agent-review, một lượt cả nhánh, mức nhẹ).
Phạm vi: `81e3aff` (code, 4 file +29/−2) + `8d0280b` (bài học 25, sổ 07). So với `main` `6c7c01b`.

**Kết luận: `ready_for_user_confirmation`** (A merge được). Có 2 minor, không chặn. m-1 chỉ cần sửa một câu chữ; sửa xong A xác nhận bằng grep, không cần review vòng 2.

## Đã kiểm (tự chạy, không dựa vào report của C)

| Cổng | Kết quả |
|---|---|
| Đường dẫn đổi / ngoài phạm vi | 6 file đúng như C báo; không chạm `data/`, cờ, `settings.yaml`, lời dặn |
| `git diff --check` (cả 2 commit) | sạch |
| Chỉ hiện khi bữa không có quán | Đúng: `elif` sau `if chon` (`quan_lich.py` ~dòng 105). Bữa có quán thì giữ nguyên như cũ. Hai điểm này 0 quán trong 10 km, quán gần nhất 36,1–38,9 km (`dem.json`), nên không có bữa nào có quán mà vẫn bị ghi chú đè |
| Không vào model | `gan_o_an` (`len_ke_hoach.py` ~dòng 115) ghi `lich["an"]`. `tin_nhan_model` không đọc khoá này, `dong_chu` chỉ dựng chữ chép / tải |
| Test (worktree riêng `/tmp/e_rv` detached, `.venv` main) | 7 file lịch / quán / lưu trú: **114 passed, 22,5 s**. Không chạy lại cả `backend/tests` (C đã chạy 1048 passed; nhánh chỉ chạm `quan_lich` + JSX / CSS) |
| Câu ghi chú ↔ kho (`scripts/grep_kb.sh` + đọc đúng dòng) | Nhị Hồ trưa: khớp :52–56 (chòi sạp, 6 hộ quản lý) và :69 (ăn uống dã ngoại). Nhị Hồ tối: khớp :167 (07:30–17:30, kho ghi thêm "mùa khô tháng 4–8"; câu đã có chữ "thường" nên chấp nhận). Bạch Mã: xem m-1 |
| Số trong bài 25 / sổ 07 ↔ `data/dem_quan_nam_xa_2026-11-15/dem.json` | 720 / 3.840 (18,8 %), 1.080 / 22.680 (4,8 %), chỉ khi có "Thiên nhiên" (5 tổ hợp, mỗi tổ hợp 144 / 240), 1–2 ngày 0 / 768, 36–38 km: **khớp**. 2.040 = 3.960 − 1.920 (`dong_bien` trong `dem_theo_cum_kho4_bo_hue_an.json`): **khớp**. 1.080 / 2.040 ≈ 0,53, nên viết "một nửa" là đúng |
| Ảnh Playwright `c_ga_ghi_chu_1440.png` | 2 câu hiện đúng dưới tiêu đề bữa, chữ cùng màu chữ thường |

## Finding

**m-1 (minor, nên sửa — sửa một câu):** câu Bạch Mã nói rộng hơn kho.
- Vị trí: `backend/llm/quan_lich.py` `GHI_CHU_AN[("bach_ma","trua")]`; `bai_hoc/25` đoạn "Sáng 15/11" ("vì trong vùng lõi không có hàng quán").
- Kho (`travel/places/Vườn quốc gia Bạch Mã.md:207`) ghi: "trong **vùng lõi Ngũ Hồ** và đỉnh núi không có hàng quán **bán thức ăn tươi sống**". Cùng bài, dòng 187 ghi Bạch Mã Village ở vùng đệm chân núi có "dịch vụ ăn uống thương mại".
- Câu hiện tại "trong vùng lõi và trên đỉnh núi không có hàng quán" bỏ mất "Ngũ Hồ", nên đọc thành cả vùng lõi không có chỗ ăn.
- Tác động thấp: lời khuyên "mang đồ ăn trưa" vẫn đúng. Nhưng luật của nhánh là "chữ theo kho".
- Đóng khi: câu ghi "khu Ngũ Hồ và đỉnh núi". Ví dụ: "Mang theo đồ ăn trưa khô và nước uống — khu Ngũ Hồ và đỉnh núi không có hàng quán bán đồ ăn." Bài 25 sửa theo.

**m-2 (minor, tuỳ C):** mục `("thac_nhi_ho","trua")` không xảy ra trong mô phỏng.
- `dem.json` `bua_theo_loai` chỉ có `trua @ bach_ma` 720 và `toi @ thac_nhi_ho` 360. Bữa trưa ở Nhị Hồ 0 / 3.840 khung, vì bộ xếp luôn đặt Bạch Mã buổi sáng, Nhị Hồ buổi chiều.
- Tài liệu lại tả 3 câu như người dùng sẽ thấy: sổ 07 "Nhị Hồ (trưa, tối)", bài 25 "(mang đồ ăn trưa; chòi ăn tại chỗ; …)".
- Không hại (1 dòng, chữ đúng kho). Có thể xảy ra khi sửa lịch bằng lời dời Nhị Hồ sang sáng, nhưng chưa kiểm.
- Đóng khi (chọn một): (a) bỏ mục đó, vì luật "đếm trước khi xây" không thấy bữa nào cần; hoặc (b) giữ mục, nhưng bài 25 / sổ 07 ghi rõ "trong mô phỏng chỉ gặp trưa Bạch Mã và tối Nhị Hồ".
- E nghiêng về (a). Câu Nhị Hồ trưa cũng là câu duy nhất không có test nào chạy qua.

## Câu C nhờ xét

- **3 câu có khớp kho không:** Nhị Hồ ×2 khớp; Bạch Mã lệch nhẹ (m-1).
- **Tiêu đề "Ăn tối gần Thác Nhị Hồ" + "ăn tối sau khi về nơi nghỉ":** đọc được, không gây hiểu lầm nặng, vì câu nhắc nói rõ phải làm gì. Bài 25 đã ghi điểm này ở mục giới hạn. Không cần sửa. Nếu muốn gọn hơn thì có thể thêm một nhánh riêng cho tiêu đề, nhưng E thấy không đáng.

## Tiền / thời gian
0 USD. Pytest 22,5 s. Không Playwright (dùng ảnh của C; nhánh chỉ thêm 1 span + 1 dòng CSS).
