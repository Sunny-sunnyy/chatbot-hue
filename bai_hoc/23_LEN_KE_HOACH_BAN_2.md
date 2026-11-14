# Bài 23 — "Lên kế hoạch" bản 2: code xếp lịch theo luật, nghiệm thu trượt rồi đạt nhờ dữ liệu và ba sửa nhỏ

*Cập nhật lần cuối: 13:40, ngày 14/11/2026 · bài mới; thay phần biểu mẫu bản cũ ở bài 14; đã sửa theo một lượt kiểm độc lập (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Bộ xếp bản 2 — **mới** | **`xep_v2`** (`backend/llm/lich_trinh_v2.py`), cờ **`len_ke_hoach_v2`** | Code xếp điểm vào từng buổi theo một chuỗi luật có thứ tự, tính cả giờ gợi ý. |
| Bảng điểm | **`diem_v8.json`** (34 điểm) | Bảng anh duyệt: điểm nào ở cụm nào, mở mấy giờ, tham quan bao lâu, trong nhà hay ngoài trời, hợp sở thích nào. |
| Quỹ phút — **mới** | (trong spec: "quỹ phút"; code `QUY`) | Số phút tham quan tối đa của một buổi, tuỳ kiểu đi. Giúp nút "đi nhẹ / khám phá nhiều" thật sự đổi lịch. |
| Câu dự phòng | **`cau_du_phong`** | Câu tả do code viết sẵn, dùng khi câu của model không qua kiểm. |
| Khung lịch | **khung** (`kiem_khung_v2` kiểm) | Phần do code dựng: ngày, buổi, giờ, tên điểm. Model không được đổi phần này. |
| Bộ 20 yêu cầu mẫu — **mới** | **bộ 20** | 20 yêu cầu lên lịch mẫu dùng trong lúc chỉnh, để đếm câu dự phòng. |
| Bộ để dành — **mới** | **bộ quyết** (12 tổ hợp) | 12 tổ hợp yêu cầu chưa ai xem khi chỉnh, để dành cho lần quyết bật hay không. |
| Phép dò toàn bộ — **mới** | **ca dò** | Code chạy mọi tổ hợp biểu mẫu để tìm đúng một loại lỗi (vd buổi sáng tràn sang chiều). |

---

*Bài 14 kể biểu mẫu "Lên kế hoạch" bản đầu: code xếp theo buổi, model chỉ viết lời. Bài này kể bản 2, bật ngày 14/11: vì sao phải làm lại, bộ xếp mới theo
luật nào, và chuyện nghiệm thu lần đầu trượt: phần câu dự phòng đạt nhờ sửa dữ liệu, phần chấm mù đạt sau ba sửa nhỏ trong code.*

## Quay lại người hướng dẫn viên

Bản đầu giống một người hướng dẫn viên mới vào nghề. Mỗi buổi chỉ dẫn khách một điểm, luôn đi theo thứ tự in trong bảng. Đo lại thì thấy **7 / 28 điểm không bao
giờ được xếp**, và nút "đi dày" đổi khung lịch **0 / 120 lần**, tức bấm cũng như không. Lịch không có giờ, cũng không hỏi ngày đi.

Người hướng dẫn viên có nghề làm khác. Họ hỏi đi mấy ngày, ngày nào, đi với ai, thích gì. Họ biết lăng nào mở cửa lúc mấy giờ, hai điểm cách nhau bao xa,
buổi sáng đủ thời gian cho hai điểm hay chỉ một. Gặp ngày mưa thì đổi sang điểm trong nhà. Bản 2 là người hướng dẫn viên đó, viết thành code.

## Bản 2 làm gì

**Biểu mẫu bốn nhóm:** ai đi (người lớn, trẻ em, có người lớn tuổi không), đi bao lâu và khi nào (1–5 ngày; ngày đi có thể để trống), đi kiểu nào (nhẹ nhàng /
cân bằng / khám phá nhiều), thích gì (tối đa 2). Ô nào không làm lịch đổi được thì không hiện.

**Code xếp theo luật, ưu tiên từ trên xuống:**
1. **An toàn cho trẻ em và người lớn tuổi:** không xếp buổi tối (lịch ghi "tối nghỉ"), mỗi buổi tối đa 1 điểm, tránh điểm nhiều bậc thang.
2. **Giờ mở cửa, ngày hoạt động, mùa:** điểm tạm dừng theo mùa thì không xếp vào tháng đó.
3. **Cụm gần nhau:** một ngày tối đa 2 cụm, và hai cụm phải kề nhau. Cụm xa chỉ xếp khi đi từ 3 ngày.
4. Điểm ưu tiên của từng sở thích, rồi **mưa**, rồi sở thích, rồi kiểu đi.

**Quỹ phút:** điểm ngắn tính 75 phút, điểm nửa buổi 150 phút. Đi giữa hai điểm cùng cụm tính 15 phút, cụm kề 30 phút. Một buổi "cân bằng" có tối đa 210 phút,
"khám phá" 240 phút, "nhẹ nhàng" 1 điểm. Từ quỹ phút ra **giờ gợi ý** cho từng điểm, và dòng "khoảng N phút đi" giữa hai điểm liền nhau. Số phút đi này
chính là số bộ xếp đã dùng để giãn giờ, nên giờ in ra và phút đi không thể lệch nhau.

**Mưa:** chỉ xét khi ngày đi nằm trong 7 ngày tới (có dự báo thật) và khả năng mưa từ 60 % trở lên. Ngày đó ưu tiên điểm trong nhà, và có một dòng "Nếu mưa".

**Model chỉ viết câu tả:**
- Một lần gọi, trả về mỗi điểm một câu ≤ 30 từ, dựa trên một đoạn kho của chính điểm đó.
- Code kiểm từng câu: không được có giờ, tiền, link, tên điểm khác. Câu nào trượt thì **code thay bằng câu dự phòng cho riêng điểm đó**; các câu khác giữ nguyên.
- Khung lịch hiện ngay trên màn hình, câu tả hiện dần sau.

**Phần phụ:**
- **Ảnh cho 24 / 34 điểm**, lấy từ Wikimedia Commons, giấy phép mở, dòng ghi công đủ tác giả và giấy phép. Một người xem mù kiểm 10 lịch: ảnh đúng điểm 10 / 10; có một ảnh lăng người xem ghi "đúng loại, không chắc đúng lăng".
- **Nút "Thêm vào lịch (.ics)":** code trong trình duyệt dựng file lịch điện thoại từ khung lịch, không gửi gì ra ngoài.
  - Kiểm trên 44 lịch đã lưu: 33 lịch có ngày đi, cho ra 288 sự kiện. Một trình đọc độc lập báo 0 lỗi.
  - Chưa thử mở trên Google Calendar, vì cần đăng nhập.

## Nghiệm thu: lần đầu trượt

Luật ghi trước có hai sàn chính:
- **Bộ 20 yêu cầu mẫu:** ≥ 18 / 20 lịch có không quá 1 câu dự phòng.
- **Bộ để dành 12 tổ hợp × 2 lượt:** hai người chấm mù, sàn ≥ 11 / 12 mỗi lượt. Mỗi lịch chấm 6 ý, gồm có hợp người đi cùng không, có hợp ngày mưa không.

Lần đầu (13/11), hai lượt chạy bộ 20: **16 / 20 và 17 / 20** lịch đạt. Lượt đầu có 2 lịch quá 30 % câu dự phòng, nặng nhất 33 %. Người điều phối quyết **không bật**.

Mình tìm gốc lỗi trước khi sửa. Câu dự phòng **dồn vào đúng nhóm điểm có bài kho mỏng**, hoặc không có bài riêng. Đoạn kho đưa cho model không có gì để
tả, nên model trả câu rỗng, và code thay bằng câu dự phòng. Lỗi không nằm ở luật xếp, cũng không nằm ở model.

## Phần câu dự phòng đạt nhờ dữ liệu

Cách sửa phần này vì vậy nằm ở **dữ liệu**, không sửa code:
- Viết thêm bài kho cho các điểm mỏng: đó là lần ghi kho sáng 14/11 ở bài 22.
- Với 10 điểm, chọn tay đúng đoạn kho dùng để tả (cột "đoạn mô tả"; sau một lỗi ở mục dưới thành 11 điểm).

Đo lại 14/11:

| Đo gì | Lần đầu | Sau khi sửa dữ liệu | Vì sao ổn |
|---|---|---|---|
| Lịch có ≤ 1 câu dự phòng, bộ 20 (lượt đầu) | 16 / 20 | **20 / 20** (cả bộ chỉ 1 câu dự phòng) | vượt sàn 18 / 20 |
| Lịch có > 30 % câu dự phòng (lượt đầu) | 2 | 0 | đúng mức "không lịch nào" |
| Lúc đủ câu (so bản đang chạy) | — | 4,06 s, bản cũ 5,12 s (sau các sửa code: 4,56 s) | không chậm hơn |
| Bộ để dành, hai người chấm mù | 10 / 12 mỗi lượt | **12 / 12 × 2 lượt** (sau khi sửa code, mục dưới) | sàn 11 / 12 |

Lượt chấm mù đầu ra 10 / 12 mỗi lượt, chỉ vì **một** lỗi: thiếu dòng "Nếu mưa" ở 2 tổ hợp. Sửa xong, hai người chấm mù **mới** chấm lại 6 lịch có đổi:
6 / 6 đạt. Dọc đường còn lộ thêm hai lỗi khác (mục sau).

Anh quyết bật lúc 10:46 ngày 14/11, kèm điều kiện sửa giờ Đại Nội trước. Bản 2 chạy cho mọi người dùng từ 11:00.

## Một chuyện thật: ba lỗi người chấm mù bắt, mô phỏng thì không

Mô phỏng bằng code chạy hàng nghìn khung lịch, nhưng chỉ bắt được điều mình đã nghĩ tới để kiểm. Người chấm mù đọc lịch như khách thật. Ba lỗi dưới đây
đều do họ thấy trước:

1. **Ngày mưa không có dòng "Nếu mưa"** (đây là lỗi làm lượt chấm đầu ra 10 / 12). Hai ngày dự báo mưa 76 % và 89 % mà lịch không nhắc gì. Lý do: ngày đó toàn điểm trong nhà, code nghĩ không có gì
   để đổi nên bỏ dòng. Nhưng khách vẫn cần biết. Sửa: ngày mưa **luôn có đúng một dòng**, ba trường hợp: có điểm đổi được, toàn điểm trong nhà, không đổi
   được. Phép dò toàn bộ 9.600 khung: 0 thiếu, 0 thừa.
2. **Buổi sáng tràn sang buổi chiều** (người chấm ghi chú thêm, không nằm trong 6 ý chấm). Quỹ phút không tính thời gian chờ tới giờ mở cửa. Có buổi sáng
   kéo tới 14:00 trong khi buổi chiều bắt đầu 13:00. Mình viết phép dò cho mọi tổ hợp: **52 / 3.840 khung** bị chồng. Sửa: điểm thêm buổi sáng chỉ nhận khi xong trước giờ đầu buổi chiều. Sau sửa: 0 / 3.840.
3. **Câu nội bộ lọt ra người dùng** (hai người chấm mù mới thấy ở lượt chấm lại). Một câu tả viết kiểu "tài liệu không cung cấp thông tin về điểm này". Gốc: đoạn kho chọn cho điểm đó lại tả công trình
   bên cạnh. Sửa hai đầu: chọn lại đoạn đúng, và thêm một luật kiểm câu chặn kiểu "tài liệu không có…". Thử luật trên 1.068 câu đã lưu: bắt đúng 1, chặn nhầm 0.

Thêm một lỗi người điều phối thấy khi dùng thật: lịch không có ngày đi thì **mọi** hoạt động buổi tối đều bị gắn nhãn "kiểm lịch diễn", kể cả chợ đêm. Sửa:
nhãn chỉ gắn cho điểm có suất diễn. Đếm lại: 228 / 960 ⇒ 0 / 960.

Bài học: **mô phỏng bắt lỗi luật, người chấm mù bắt lỗi "khách đọc thấy kỳ"**. Cần cả hai.

## Khi nào hỏng

- **Khung lịch có lúc hiện quá 1 giây**, ở lượt đầu có dự báo khi bộ nhớ đệm thời tiết còn trống. Anh đã nhận đây là giới hạn.
- **Một nhãn được gắn sau khi thấy sàn trượt.** Sở thích "lễ hội – nghệ thuật" chỉ đạt 43 %, dưới sàn 50 %. Một điểm được gắn thêm nhãn này (có căn cứ trong
  kho) và sàn lên đúng 50 %, không còn biên. Việc này đã đưa anh duyệt, nhưng là chỗ mỏng.
- **Lịch chưa có ăn uống và lưu trú.** Bản đồ trong lịch có code nhưng chưa bật.
- **File .ics:** khung giờ qua nửa đêm sẽ mất sự kiện (bảng hiện chưa có điểm như vậy). Hai lịch cùng ngày bắt đầu có thể ghi đè nhau trong ứng dụng lịch.
- **Bảng điểm chỉ có 34 điểm.** Điểm ngoài bảng thì lịch không xếp được.

## Ba điều chính

1. Bản 2 là **code xếp theo chuỗi luật có thứ tự** (an toàn ⇒ giờ mở cửa, mùa ⇒ cụm gần ⇒ mưa ⇒ sở thích ⇒ kiểu đi) với quỹ phút và giờ gợi ý. Model chỉ
   viết một câu tả mỗi điểm, câu nào trượt kiểm thì code thay.
2. Nghiệm thu lần đầu **trượt** (16 / 20). Gốc lỗi là **bài kho mỏng**, nên phần câu dự phòng sửa bằng dữ liệu, không sửa code: 20 / 20. Phần chấm mù
   đạt 12 / 12 × 2 sau khi sửa ba lỗi nhỏ trong code. Bật từ 14/11.
3. Chuyện thật: người chấm mù thấy **ba lỗi** mà mô phỏng không bắt (dòng ngày mưa, sáng chồng chiều 52 / 3.840 khung, câu nội bộ). Mô phỏng và người đọc
   thật bổ sung cho nhau.

**Bài sau:** Bài 24 — Giao diện H1 "Sông Hương": chọn hướng, hiệu ứng làm bằng gì, và đo thế nào để đẹp mà không chậm.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Bản cũ 7 / 28 điểm không xếp, "đi dày" 0 / 120: `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` §2, §3.1 [đã chạy]
- Biểu mẫu 4 nhóm, thứ tự luật, quỹ phút 75 / 150, phút đi 15 / 30, quỹ 210 / 240, mưa ≥ 60 % trong 7 ngày, câu ≤ 30 từ, kiểm câu, câu dự phòng: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` §3.1, §5, §5b, §5c; `backend/llm/lich_trinh_v2.py` [code]
- Nghiệm thu, 16 / 20 – 17 / 20, gốc lỗi bài mỏng, 20 / 20, 4,06 ↔ 5,12 s, 10 điểm có đoạn mô tả, bật 10:46 / 11:00 ngày 14/11: `report_agent/…/b_len_ke_hoach_dot_1_implementation.md` §0, §4.2, §9, §12; `report_agent/…/e_review_len_ke_hoach_dot_1.md` [đã chạy]
- Ba lỗi người chấm mù, 9.600 khung, 52 / 3.840 ⇒ 0, 1.068 câu, 12 / 12 × 2, 6 / 6: `report_agent/…/e_review_len_ke_hoach_nhanh_1411.md` (M-1, M-2, "Kiểm phần sửa"); `b_len_ke_hoach_dot_1_implementation.md` §10, §11 [đã chạy]
- Nhãn tối 228 / 960 ⇒ 0: `report_agent/…/b_lich_truong_gd_implementation.md`, `c_review_lich_truong_gd.md` [đã chạy]
- Ảnh 24 / 34, 10 / 10, một ảnh lăng "không chắc đúng lăng": `report_agent/…/b_anh_lich_implementation.md`, `c_review_anh_lich.md`; .ics 44 lịch ⇒ 33 có ngày ⇒ 288 sự kiện: `session_prompt/CURRENT_HANDOFF.md`, `session_prompt/sessions/STATUS_E.md` (mốc 12:07 14/11); giới hạn qua nửa đêm / UID: `report_agent/…/c_review_xuat_ics.md`; cách làm: `docs/superpowers/plans/2026-11-14-xuat-lich-ics-plan.md`, `frontend/src/lich_ics.js` [code, đã chạy]
- **Sửa 13:40 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_24.md`): bản trước nói "không sửa một dòng code nào" — sai, bộ chấm mù đạt sau 3 sửa code; cột "lần đầu" ghép hai lượt (nay lượt đầu: 16 / 20 và 2 lịch > 30 %); 10 / 12 chỉ do thiếu dòng "Nếu mưa"; nhóm hạn chế là "không xếp buổi tối" chứ không chỉ "không tối muộn"; giải nghĩa bộ 20 / bộ để dành / phép dò.
- Nhãn lễ hội 43 % ⇒ 50 %: `b_len_ke_hoach_dot_1_implementation.md` §4.1, `c_so_moc_buoc_b.md` [đã chạy]
- Khung > 1 s là giới hạn đã nhận: `b_len_ke_hoach_dot_1_implementation.md` §5 [tài liệu]

</details>
