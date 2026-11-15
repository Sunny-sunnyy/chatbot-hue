# Bảng điểm lịch v9: thêm 7 nơi vào "Lên kế hoạch" (E · 15:34 15/11/2026, `date`)

Người làm: E (Claude Code). A giao theo handoff "Việc đầu phiên sau" mục 2 (User chọn 15/11). Nhánh `p9-diem-v9`. Reviewer: B.
Nháp + căn cứ từng trường: `e_diem_lich_moi_nhap.md` (B review ready, 3 minor đã đóng). Báo cáo này chỉ kể phần **dựng bảng thật + đo**.

## 1. Đã đổi gì

| Chỗ | Đổi |
|---|---|
| Bảng điểm (private) | `data/phase_9/lich_trinh/diem_v9.json` = v8 + 7 điểm (Từ Hiếu, Trường Tiền, Hải Vân, Bến Ngự, làng nón Tây Hồ, An Hiên, Lập An) ⇒ 41 điểm. Bảng v8 không sửa. md5 `eb6cfd95df6b`. |
| Toạ độ (private) | `diem_toa_do_v9.json` = v7 + 7 dòng. md5 `f6068ff37d61`. |
| Ảnh lịch (private + tracked) | `bang_anh_v4.json` = v2 + 6 ảnh (tên `v3` đã có từ 14/11, không dùng) ⇒ 39 / 41 điểm có ảnh; 6 file mới ở `frontend/public/anh/lich/`. Làng nón Tây Hồ không ảnh. md5 `00ccb4619455`. |
| `settings.yaml` | 3 đường bảng trỏ bản mới (chỉ 3 dòng đó). |
| `lich_trinh.py` | `KHUNG_HUE` kinh độ tối đa 108,0 ⇒ **108,25** (A quyết): Hải Vân (108,13) và Lập An (108,06) thuộc TP Huế nhưng ở phía đông kinh tuyến 108; để nguyên thì server không khởi động. |
| `quan_lich.py` | 3 ghi chú ăn (Lập An trưa + tối, Hải Vân trưa) — xem mục 4. |
| `lich_trinh_v2.py` | `kiem_cau`: câu chỉ có mã nguồn (không chữ) tính là rỗng ⇒ câu dự phòng — xem mục 5. |
| Test | `test_ban_do_lich.py`: 2 toạ độ phía đông kinh tuyến 108 nạp được. `test_len_ke_hoach_v2.py`: ngoại lệ cụm xa (mục 3) + ca "chỉ có mã nguồn". |

Dựng lại được: `uv run python data/diem_lich_moi_2026-11-15/tools/dung_v9.py <thư mục frontend>` (ghi đè 3 bảng + 6 ảnh).

**Ảnh (luật chọn ảnh, ≤ 10 ảnh ⇒ người giao chọn + reviewer nhìn lại):** 6 ảnh là ảnh Khám phá "chắc" của đúng bài, đã qua người nhìn 14–15/11; E nhìn lại cả 6 hôm nay:
cổng tam quan + hồ bán nguyệt (Từ Hiếu) · cầu vòm thép trên sông (Trường Tiền) · tàu trên sườn đèo, tên file do tác giả đặt đúng nơi (Hải Vân — **B xem giúp**: ảnh là đường sắt qua đèo, không phải Hải Vân Quan) · mặt tiền chợ có biển tên (Bến Ngự; có người đi xe đạp nhỏ, không rõ mặt) · lối vào dưới vòm cây (An Hiên) · cây khô + bè tre trên đầm, chú thích tác giả đúng nơi (Lập An). Không trẻ em, không số điện thoại.

## 2. Mô phỏng 3.840 khung (0 USD) — khớp mốc ghi trong handoff

`data/diem_lich_moi_2026-11-15/tools/mo_phong_v9.py` (cùng 4 ngày đi như C), bảng thật v8 ↔ v9; kết quả `mo_phong_v9.json`:

| Sở thích (điểm ban ngày phải lấy NGOÀI sở thích) | v8 | v9 | Mốc handoff |
|---|---|---|---|
| ẩm thực | 56,4 % | **44,0 %** | 44,0 |
| chụp ảnh | 51,7 % | **36,8 %** | 36,8 |
| thiên nhiên | 24,4 % (buổi trống 72) | **17,6 %** (64) | 17,6 |
| lễ hội / nghệ thuật | 39,0 % | 39,1 % | — (kho không có nơi để bù) |
| di tích | 0 % | 0 % | 0 |

**0 lỗi `kiem_khung_v2`** trên cả hai bảng; cả 7 điểm mới được xếp (136–740 lượt / điểm).

## 3. ĐỔI TIÊU CHÍ — A duyệt 15/11 (điểm kiểm cho B)

Test `test_simulation_always_rules` có sàn "số điểm: nhẹ nhàng ≤ cân bằng ≤ khám phá". Với v9 sàn này trượt ở **1 / 320 tổ hợp** (không ngày đi) = **4 / 1.280** (4 ngày đi, cùng một tổ hợp); v8: 0.
- Tổ hợp: 3 ngày · không trẻ em / lớn tuổi · sở thích chỉ "chụp ảnh" ⇒ **9 / 12 / 10**.
- Vì sao: kiểu khám phá dùng hết điểm chụp ảnh gần sớm hơn ⇒ ngày 3 đi cụm xa (sáng Hải Vân, chiều Lập An); ngày cụm xa chỉ 2 điểm và tối nghỉ (luật sẵn có). Cân bằng ngày 3 còn ở trung tâm: 3 điểm + 1 buổi tối. Không phải lỗi xếp.
- A chọn (a): nới **đúng một** điều kiện — "khám phá" được ít điểm hơn "cân bằng" **chỉ khi** nó có số ngày cụm xa nhiều hơn hẳn (so chặt, tính từ khung); mọi tổ hợp khác vẫn phải đơn điệu; test in số ngoại lệ (`pytest -s`: "ngoại lệ cụm xa: 1 / 320") và dừng nếu > 6 (≈ 2 %). Bộ xếp và nhãn dữ liệu không đổi. E không tự hợp thức hoá: đã dừng, báo A 3 phương án, A quyết.
- Phương án bỏ: (b) gỡ nhãn chụp ảnh khỏi Hải Vân + Lập An (chỉnh dữ liệu để qua test, mất lợi ích chính); (c) sửa bộ xếp (đổi khung ở nhiều tổ hợp khác — quá tay).
- Hệ quả cho thước chấm bộ lịch (ý 3 của `nghiem_thu.py` cũng dùng phép so này, chưa có ngoại lệ): 17 yêu cầu chạm ở mục 5 đều đơn điệu ⇒ không bị ảnh hưởng hôm nay; tổ hợp ngoại lệ không nằm trong bộ 20 / 12.

## 4. Nơi ở + quán ăn (đường thật `gan_o_an`, 0 USD)

`tools/an_o_v9.py`, 3.840 khung, cờ như `settings.yaml` của nhánh (bảng lưu trú v5): không lỗi; ô Nơi ở rỗng 768 = 768 (không đổi).

| | v8 | v9 trước ghi chú | v9 |
|---|---|---|---|
| Bữa có quán gợi ý | 80,7 % (18.306 / 22.680) | 75,2 % | 75,2 % (17.115 / 22.752) |
| Bữa có quán **hoặc** ghi chú ăn | 85,5 % | 80,0 % | **85,5 %** |

Vì sao tụt: Hải Vân, Lập An cách quán gần nhất trong bảng hàng chục km; làng nón Tây Hồ không có quán trong 2 km. Dùng cơ chế sẵn có `GHI_CHU_AN` (đang dùng cho Bạch Mã / Nhị Hồ) thêm 3 câu theo đúng nội dung kho (bài Đầm Lập An mục nhà hàng ven đầm; bài Đèo Hải Vân mục thông số tuyến — chân đèo phía bắc là Lăng Cô). **Còn hở (giới hạn):** Tây Hồ 144 bữa + Hải Vân bữa tối 72 bữa không quán, không ghi chú (kho không nói gì về ăn uống ở đó ⇒ không viết).

## 5. Lượt thật (có phí) — chỉ yêu cầu chạm đường đổi

Đếm trước bằng code (`tools/dem_cham.py`, 0 USD): khung đổi giữa v8 và v9 ở **9 / 20** yêu cầu bộ lịch + **8 / 12** bộ quyết ⇒ chỉ chạy 17 yêu cầu đó, 1 lượt, server nhánh cổng 8894 (đã kiểm cổng + thư mục chạy), harness `tools/nghiem_thu_v9.py` (= `nghiem_thu.py`, chỉ đổi đường bảng).

| Lượt | Bản | Đạt 6 ý (code) | Câu dự phòng | Tiền (log, lọc theo sha) |
|---|---|---|---|---|
| 1: 17 yêu cầu (+ 1 pilot) | `a124771` | **17 / 17** | 9 — **cả 9 ở điểm mới** | 0,0089 USD |
| 2: 11 yêu cầu có 4 điểm sửa | `29a9121` | **11 / 11** | 1 (một điểm cũ, không liên quan) | 0,0062 USD |

- **Lỗi thật lượt 1 bắt được:** 4 điểm (Trường Tiền, Hải Vân, Lập An, Tây Hồ) nháp gắn `doan_mo_ta` = "đoạn đứng đầu khi tìm bằng tên" ⇒ rơi vào dòng thông tin chung một ý (tên gọi, độ cao, số nan tre) ⇒ model không có gì để tả: 9 / 17 mục của 4 điểm này ra câu dự phòng, 2 mục chỉ hiện mỗi mã nguồn, vài câu chỉ nhắc tên gọi. 3 điểm còn lại (Từ Hiếu, Bến Ngự, An Hiên) nháp trúng đoạn "Tổng quan" ⇒ 0 câu dự phòng.
- **Sửa (dữ liệu, như cách B làm ở v8):** gắn lại 4 đoạn tả điểm, E đọc tay, tránh đoạn nêu tên điểm khác của bảng (luật `ten_khac`); bảng ghi trong `tools/dung_v9.py` (`DOAN_MO_TA`, có đoạn cũ ⇒ mới + lý do). Lượt 2: 17 / 17 mục của 4 điểm là câu model, 0 dự phòng; E đọc cả 17 câu — đều tả đúng nơi.
- **Sửa nhỏ kèm theo (code, 1 dòng + 1 ca test):** câu chỉ có mã nguồn lọt kiểm cuối (lượt 1: 2 mục; lượt cũ trên v8 cũng có 1 / 102) ⇒ `kiem_cau` coi là rỗng ⇒ câu dự phòng.
- Khung hiện chậm nhất 1,24 s (lượt 1, lịch 5 ngày có dự báo) / 1,05 s (lượt 2) — sàn khung 1 s đã là giới hạn nhận từ 13/11; trung vị 0,20–0,30 s.
- Server khởi động thật với 3 bảng mới (kiểm đoạn mô tả có trong chỉ mục, kiểm ảnh có file): `/health` 5 / 5, `/` 200, ảnh mới 200, lịch mẫu trả về.
- Tiền E việc này: **0,0151 USD** (`scripts/dem_chat_metrics.py --sha`), chưa review.

## 6. Test

| Bước | Kết quả | Thời gian đo |
|---|---|---|
| 7 file chạm bảng lịch, không khoá / có khoá (đổi đường bảng trong `settings.yaml`) | 493 đạt + 1 trượt (sàn mục 3, trước khi A quyết) ở cả hai | 76 s / 77 s |
| 3 file chạm sau mọi sửa (`test_len_ke_hoach_v2`, `test_quan_lich`, `test_ban_do_lich`) | 120 đạt | 24 s |
| Test rộng `backend/tests`, không khoá, bản `29a9121` | **1.084 đạt**; 1 trượt + 4 lỗi = đúng nhóm test cần khoá OpenAI ghi trong handoff | 4 phút 09 s |
| Playwright | NOT RUN — nhánh chỉ đổi ảnh + dữ liệu bảng (luật 15/11) | — |
| Q1 "chuỗi gửi model giống byte" | NOT RUN — không chạm lời dặn / công cụ; chuỗi gửi model của lịch đổi theo điểm mới là chủ đích | — |

## 7. Giới hạn / việc còn lại

- Chợ Bến Ngự: thời lượng "nửa buổi" 1 nguồn, nhóm chưa tự đọc được trang (403) — User chốt GIỮ có cờ (A ghi nhận 15:12 15/11/2026); cờ nằm ở `thoi_luong_can_cu`.
- Một câu ở lượt 2 tả đèn buổi tối cho mục xếp buổi sáng của cầu Trường Tiền (đoạn mô tả nói cả ngày lẫn tối) — đúng theo kho, chưa đẹp; không sửa.
- Làng nón Tây Hồ: không ảnh; toạ độ là chùa làng (đại diện); cụm `an_cuu` theo tâm gần nhất (đã ghi ở nháp).
- **Sau khi merge:** bản deploy nháp (`data/phase_12/deploy_nhap/`: `CHUA` + `COPY`) đổi sang 3 bảng mới — E làm ngay sau merge (chưa đổi để không lệch `main`); sổ ghi việc + `bai_hoc/` do A xếp.
- Trường `luu_y` của 7 điểm mới viết kiểu ghi chú nội bộ (có số dòng kho) — bản 2 không hiện trường này cho người dùng; nếu sau này hiện thì phải viết lại.

**Giải thích ngắn:** lịch "Lên kế hoạch" có thêm 7 nơi để người chọn ẩm thực / chụp ảnh / thiên nhiên ít bị xếp điểm ngoài sở thích hơn (vd chụp ảnh 51,7 ⇒ 36,8 %). Lượt chạy thật bắt được một lỗi của bảng nháp (4 nơi gắn nhầm đoạn kho nghèo ý nên lịch chỉ in tên) và đã sửa bằng dữ liệu; một sàn test được A nới đúng một điều kiện vì ngày đi xa vốn ít điểm.
