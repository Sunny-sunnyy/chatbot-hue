# Đếm "mưa bằng dữ liệu" — C · 18:18 14/11/2026 · 0 USD

A giao (sau bàn nhóm "đợt agent kế"): có cần thêm điểm trong nhà cho ngày mưa không. Script + số: `data/dem_mua_2026-11-14/dem_mua.py` ⇒ `dem_mua.json` (private). Không ghi kho, không sửa code.

## Đã có sẵn trong hệ thống (đọc code)
- Xếp lịch: ngày dự báo mưa ≥ 60 % ⇒ điểm KHÔNG ưu tiên xét trong nhà → cả hai → ngoài trời (`lich_trinh_v2.py:161-250`); điểm ưu tiên giữ chỗ.
- Lời cho người dùng: mỗi ngày mưa đúng một dòng "Nếu mưa" do code viết (`len_ke_hoach.py:62-74`): gợi ý thay điểm ngoài trời bằng điểm trong nhà cùng cụm, hoặc nói thẳng "chưa có điểm trong nhà để thay — mang áo mưa hoặc đổi ngày".
⇒ "nút đề xuất mưa" phần lớn đã có dưới dạng dòng "Nếu mưa". Việc còn lại chỉ là dữ liệu / luật đổi ngày.

## Số đo (3.840 khung như mô phỏng quán; trường hợp xấu nhất: MỌI ngày mưa 100 %)
- Lượt điểm ngoài trời: 76,9 % (không dự báo) ⇒ 67,8 % (mưa) — luật mưa có tác dụng ở trung tâm: Bờ Nam 39 ⇒ 9 %, Kinh thành 62 ⇒ 45 %; KHÔNG tác dụng ở An Cựu / biển–đầm phá / nam xa (100 % ⇒ 100 %), Thủy Xuân 84 ⇒ 80 %.
- Dòng "Nếu mưa" trên 11.520 ngày mưa: **thay được 51,8 %** · **không thay được 33,3 %** · ngày đều trong nhà 15,0 %.
- 3.833 ngày "không thay được" theo điểm: phá Tam Giang 1.588 + Đầm Chuồn 802 + Bạch Mã 720 = **3.110 (81 %)** — cụm không có điểm trong nhà nào và là chuyến THIÊN NHIÊN (thêm điểm trong nhà ở đó không thực tế); phần còn lại nhỏ: Thiên Mụ 163, Ngự Bình 148, Lăng Dục Đức 111, rải rác ≤ 58.
- 13 / 34 cột `trong_nha` "C ước": đọc lại cả 13 — không sai hiển nhiên (lăng, đầm, phá, biển, thác = ngoài trời; Ca Huế thuyền có mái = cả hai). Tranh luận được: Phố cổ Bao Vinh, Khu phố Tây (có quán trong nhà) ⇒ "cả hai"; ảnh hưởng nhỏ (≤ 8 ngày "không thay được").

## Đề xuất (chưa làm)
1. **Không thêm điểm trong nhà vào kho** cho đợt này: 81 % ca thiếu nằm ở chuyến thiên nhiên, điểm trong nhà cùng cụm không có thật; thêm ở An Cựu / Kim Long chỉ cứu ~420 / 11.520 ngày (3,6 %).
2. Nếu muốn làm tiếp: **đổi ngày bằng code** — lịch ≥ 2 ngày có ngày mưa và ngày khô ⇒ dời ngày phá / đầm / Bạch Mã sang ngày khô (không gọi model, đo bằng 3.840 khung với dự báo trộn). Trước khi xây: đếm trên dự báo thật đã lưu trong log (bao nhiêu lịch thật có ≥ 1 ngày mưa ≥ 60 % VÀ có ngày khô) — nếu gần 0 thì không xây.
3. Sửa dữ liệu nhỏ, rẻ: Bao Vinh / phố Tây ⇒ "cả hai" — chỉ khi có căn cứ kho (grep_kb), không ước thêm.

## Phần 2 — "đổi ngày bằng code" có đáng không (18:20 14/11/2026, A giao; 0 USD)
Script `data/dem_mua_2026-11-14/dem_doi_ngay.py`; dự báo thật đã qua: Open-Meteo Historical Forecast, Huế, 14/11/2025–13/11/2026 (`open_meteo_hue_12thang.json`, xác suất mưa lớn nhất / ngày; "mưa" = ≥ 60 % như luật hệ thống).
- Cách đếm: 768 khung lịch 2–5 ngày × mọi ngày khởi hành trong năm (278.400 chuyến). Ngày "kẹt" = ngày mưa có điểm ngoài trời thuộc cụm không có điểm trong nhà nào (An Cựu, biển–đầm phá, làng xã, nam xa). "Cứu được" = mọi ngày kẹt đổi được với một ngày khô không kẹt trong cùng chuyến. Đây là **cận trên** (bỏ qua luật cụm xa ngày 1, quỹ phút khi đổi).
- **222 / 365 ngày** có xác suất mưa ≥ 60 % ⇒ ở Huế "ngày mưa" theo ngưỡng này là chuyện thường; 85,5 % khung có ≥ 1 ngày ở cụm không trong nhà.
- Chuyến có ≥ 1 ngày kẹt: **61,1 %**; đổi ngày cứu được **22,4 % số đó** (= 13,7 % mọi chuyến).
- Theo tháng khởi hành: mùa khô 1–4: kẹt 35–47 %, cứu 20–53 %; **mùa mưa 9–12: kẹt 70–78 %, cứu chỉ 8–21 %** (thường mọi ngày trong chuyến đều mưa) — đúng lúc cần thì đổi ngày ít tác dụng nhất.

## Đề xuất chốt
- **Không xây "đổi ngày" lúc này:** lợi cận trên 13,7 % chuyến, mùa mưa 8–21 % số chuyến kẹt; phải đụng bộ xếp (luật cụm, quỹ phút, sửa lịch giữ chỗ) ⇒ phức tạp không tương xứng. Dòng "Nếu mưa" hiện có (nói thẳng + "đổi ngày") giữ vai chính.
- Ý rẻ hơn nếu sau này cần: ngưỡng mưa đang dùng (xác suất lớn nhất ≥ 60 %) rất hay chạm ở Huế — xét thêm lượng mưa (`precipitation_sum`, đã có trong dữ liệu dự báo) để chỉ coi "mưa to" là kẹt; cần đếm lại trước, và là đổi luật hệ thống ⇒ A / User quyết.

## Phần 3 — số cho câu hỏi ngưỡng "mưa" (18:21 14/11/2026, A giao; 0 USD)
Script `data/dem_mua_2026-11-14/dem_nguong.py` ⇒ `dem_nguong.json`; cùng dữ liệu Open-Meteo Historical Forecast 12 tháng (lượng mưa = `precipitation_sum` dự báo, mm / ngày). Ngưỡng 60 % là luật trong spec User duyệt ⇒ phần này chỉ đưa số, không đổi gì.
- 222 ngày xác suất ≥ 60 %, lượng mưa dự báo: **< 1 mm: 28** · 1–5 mm: 79 · 5–10 mm: 45 · **≥ 10 mm: 70**. ⇒ ~1/2 số "ngày mưa" theo luật hiện hành chỉ mưa nhỏ (< 5 mm).

| "Mưa" là | Ngày mưa / năm | Chuyến 2–5 ngày có ≥ 1 ngày mưa | Ngày mưa tháng 9–12 | Tháng 1–4 |
|---|---|---|---|---|
| ≥ 60 % (hiện hành) | 222 | 80,4 % | 97 | 43 |
| ≥ 60 % và ≥ 1 mm | 194 | 75,6 % | 92 | 40 |
| ≥ 60 % và ≥ 5 mm | 115 | 52,8 % | 67 | 18 |
| ≥ 60 % và ≥ 10 mm | 70 | 38,3 % | 46 | 10 |

- Ý nghĩa: luật hiện hành bật "Nếu mưa" + xếp trong nhà trước ở 4 / 5 chuyến; thêm điều kiện ≥ 5 mm ⇒ ~1 / 2 chuyến, ≥ 10 mm ⇒ ~2 / 5. Đánh đổi: ngưỡng cao hơn ⇒ ít cảnh báo thừa ngày mưa phùn, nhưng ngày dự báo 5–10 mm vẫn có thể ướt khi đi phá / lăng. Lượng mưa dự báo cũng có sai số (chưa đo so với mưa thật).

## Phần 4 — so với mưa "thật" (18:22 14/11/2026; 0 USD; `so_mua_that.py`)
- **Bẫy đã kiểm:** `archive-api` mặc định trả **đúng y số** của historical forecast (365 / 365 ngày giống hệt) ⇒ không độc lập; lần so đầu (trúng 100 %) **sai, đã bỏ**. Dùng ERA5 (`models=era5`, tái phân tích dựng từ quan trắc, ô ~25 km — gần mưa thật hơn, KHÔNG phải trạm đo); 360 / 365 ngày có số.
- "Mưa thật" = ERA5 ≥ 5 mm: 124 ngày.

| Luật "mưa" | Ngày báo mưa | Đúng (ERA5 ≥ 5 mm) | Báo thừa | Bỏ sót ngày mưa thật |
|---|---|---|---|---|
| ≥ 60 % (hiện hành) | 218 | 122 (56 %) | 96 | 2 / 124 (2 %) |
| ≥ 60 % và ≥ 1 mm | 190 | 117 (62 %) | 73 | 7 (6 %) |
| ≥ 60 % và ≥ 5 mm | 111 | 95 (86 %) | 16 | 29 (23 %) |
| ≥ 60 % và ≥ 10 mm | 66 | 61 (92 %) | 5 | 63 (51 %) |

- Giới hạn: historical forecast ghép các bản dự báo tầm ngắn nhất; người dùng xếp lịch trước 1–7 ngày ⇒ dự báo thật kém hơn bảng này. ERA5 thô ⇒ mưa cục bộ có thể lệch.
- Đọc: hiện hành gần như không bỏ sót nhưng gần 1 / 2 lần báo là thừa; ≥ 5 mm: báo đúng 86 %, bỏ sót ~1 / 4 ngày mưa vừa.
- **Phương án 3** (B, C, E đồng ý — chờ User): xếp lại lịch khi ≥ 60 % VÀ ≥ 5 mm; dòng "Nếu mưa" vẫn hiện từ ≥ 60 %. Kiểm [Chạy]: 29 ngày mưa thật (ERA5 ≥ 5 mm) mà ngưỡng 5 mm bỏ sót ⇒ **27 / 29 vẫn có dòng "Nếu mưa"**; còn 2 ngày không nhắc (= mức bỏ sót của luật hiện hành).

## Phần 5 — đo lại theo cấp QCVN 84:2024 (10:23 15/11/2026; 0 USD; `so_mua_that_qcvn.py` ⇒ `.json`)
- **Sửa lỗi đo của phần 4:** "mưa thật" = ERA5 ≥ 5 mm trùng đúng ngưỡng đang thử ⇒ thiên vị 5 mm. Nay dùng **một thước cố định** cho mọi luật: ERA5 ≥ 6 mm (đầu cấp "Mưa", QCVN — nguồn B `b_nguong_mua_3_model.md`) và ≥ 16 mm (mưa vừa).

| Luật | Báo / năm | Mốc ≥ 6 mm (114 ngày): đúng · sót | Mốc ≥ 16 mm (56 ngày): báo thừa · sót | Chuyến 2–5 ngày có ngày xếp lại |
|---|---|---|---|---|
| ≥ 60 % (hiện hành) | 218 | 51 % · 2 % | 162 · 0 / 56 | 80,4 % |
| ≥ 60 % và ≥ 5 mm | 111 | 80 % · 22 % | 59 · 4 / 56 | 52,8 % |
| ≥ 60 % và ≥ 6 mm | 97 | 85 % · 28 % | 45 · 4 / 56 | 50,0 % |
| ≥ 60 % và ≥ 10 mm | 66 | 91 % · 47 % | 22 · 12 / 56 | 38,3 % |

- **Bảng A yêu cầu — 5 ↔ 6 mm trên hai thước cố định** (mỗi thước dùng chung cho cả hai ngưỡng):

| Thước "mưa thật" | Luật | Báo | Đúng | Thừa | Sót | Ngày sót vẫn có dòng "Nếu mưa" |
|---|---|---|---|---|---|---|
| ERA5 ≥ 5 mm (124 ngày, như phần 4) | ≥ 60 % và ≥ 5 mm | 111 | 95 (86 %) | 16 | 29 (23 %) | 27 / 29 |
| ERA5 ≥ 5 mm | ≥ 60 % và ≥ 6 mm | 97 | 85 (88 %) | 12 | 39 (31 %) | 37 / 39 |
| ERA5 ≥ 6 mm (114 ngày) | ≥ 60 % và ≥ 5 mm | 111 | 89 (80 %) | 22 | 25 (22 %) | 23 / 25 |
| ERA5 ≥ 6 mm | ≥ 60 % và ≥ 6 mm | 97 | 82 (85 %) | 15 | 32 (28 %) | 30 / 32 |

  Trên cả hai thước, 6 mm đổi khoảng 4–10 ngày sót để bớt 4–7 ngày báo thừa. Ngày sót vẫn có nhắc ở mọi dòng, chỉ trừ 2 ngày.
- Ngày mưa thật mà luật 6 mm bỏ sót vẫn có dòng "Nếu mưa" (≥ 60 %): 30 / 32 ngày ≥ 6 mm; 4 / 4 ngày ≥ 16 mm.
- **Đề xuất (B, C, E):** phương án 3 với **6 mm** thay 5 mm. Khác 5 mm rất ít, nhưng có mốc chính thức và ít báo thừa hơn. Không lên 10 mm (sót 21 % ngày mưa vừa). Chờ User.
- Giới hạn như phần 4: dự báo lịch sử là bản tầm ngắn nhất, dự báo thật 1–7 ngày kém hơn; ERA5 có ô ~25 km, không phải trạm đo.
