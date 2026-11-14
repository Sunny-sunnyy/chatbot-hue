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
