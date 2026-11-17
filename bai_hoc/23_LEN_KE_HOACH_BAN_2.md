# Bài 23 — "Lên kế hoạch" bản 2: code xếp lịch theo luật, nghiệm thu trượt rồi đạt nhờ dữ liệu và ba sửa nhỏ

*Cập nhật lần cuối: 13:56, ngày 17/11/2026 · thêm chiều 17/11: ngày mưa mà khách không chọn sở thích thì buổi chiều không còn dành cho điểm thiên nhiên ngoài trời. Trước: 11:56, ngày 17/11/2026 · thêm trưa 17/11: giới hạn "đi rồi quay lại cùng khu trong một ngày". Trước: 21:25, ngày 16/11/2026 · thêm tối 16/11: bản đồ dưới lịch (bật, và ba lỗi hiển thị chỉ lộ khi nhìn ảnh). Trước: 15:02, ngày 16/11/2026 · ghi chú ăn ở phá Tam Giang (bữa có gợi ý 86,4 ⇒ 94,5 %); sửa dòng giới hạn ăn uống đã cũ. Trước: 15:48, ngày 15/11/2026 · thêm chiều 15/11: bảng điểm có thêm 7 nơi (41 điểm) và chuyện lượt chạy thật bắt bốn nơi "chỉ in tên". Trước: 10:36, ngày 15/11/2026 · thêm sáng 15/11: lịch chỉ đổi điểm khi dự báo mưa đủ lớn (≥ 6 mm). Trước: 15:57, ngày 14/11/2026 · thay phần biểu mẫu bản cũ ở bài 14; đã sửa theo một lượt kiểm độc lập (ghi ở Nguồn). Thêm ghi chú chiều 14/11: lịch nay sửa được bằng lời và có gợi ý chỗ ở (bài 25); trang chưa xếp lịch hiện một lịch "Ví dụ" do chính bộ xếp dựng; không còn dòng ghi công dưới ảnh.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Bộ xếp bản 2 — **mới** | **`xep_v2`** (`backend/llm/lich_trinh_v2.py`), cờ **`len_ke_hoach_v2`** | Code xếp điểm vào từng buổi theo một chuỗi luật có thứ tự, tính cả giờ gợi ý. |
| Bảng điểm | **`diem_v9.json`** (41 điểm từ chiều 15/11; trước là `diem_v8.json`, 34 điểm) | Bảng anh duyệt: điểm nào ở cụm nào, mở mấy giờ, tham quan bao lâu, trong nhà hay ngoài trời, hợp sở thích nào. |
| Quỹ phút — **mới** | (trong spec: "quỹ phút"; code `QUY`) | Số phút tham quan tối đa của một buổi, tuỳ kiểu đi. Giúp nút "đi nhẹ / khám phá nhiều" thật sự đổi lịch. |
| Đoạn mô tả — **mới** | **`doan_mo_ta`** (một cột của bảng điểm) | Mã của đúng một đoạn trong sổ tay mà model được đọc để viết câu tả điểm đó. Chọn đoạn nào là việc của người dựng bảng. |
| Câu dự phòng | **`cau_du_phong`** | Câu tả do code viết sẵn, dùng khi câu của model không qua kiểm. |
| Khung lịch | **khung** (`kiem_khung_v2` kiểm) | Phần do code dựng: ngày, buổi, giờ, tên điểm. Model không được đổi phần này. |
| Bộ 20 yêu cầu mẫu — **mới** | **bộ 20** | 20 yêu cầu lên lịch mẫu dùng trong lúc chỉnh, để đếm câu dự phòng. |
| Bộ để dành — **mới** | **bộ quyết** (12 tổ hợp) | 12 tổ hợp yêu cầu chưa ai xem khi chỉnh, để dành cho lần quyết bật hay không. |
| Ghim — **mới** | **marker** (thư viện Leaflet; `frontend/src/BanDoLich.jsx`), cờ **`ban_do_lich`** | Dấu tròn có số đánh dấu vị trí một điểm trên bản đồ (nhìn xa, ghim sát nhau có thể vẽ lệch một chút để khỏi che nhau). |
| Ô bản đồ — **mới** | **tile** | Các mảnh ảnh nền ghép lại thành bản đồ, tải từ một máy chủ bản đồ mở. |
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
1. **An toàn cho trẻ em và người lớn tuổi:** không xếp buổi tối (từ chiều 15/11 buổi để trống không hiện thành một mục trong lịch nữa — anh yêu cầu; lý do nằm ở một dòng trong phần ghi chú của lịch), mỗi buổi tối đa 1 điểm, tránh điểm nhiều bậc thang.
2. **Giờ mở cửa, ngày hoạt động, mùa:** điểm tạm dừng theo mùa thì không xếp vào tháng đó.
3. **Cụm gần nhau:** một ngày tối đa 2 cụm, và hai cụm phải kề nhau. Cụm xa chỉ xếp khi đi từ 3 ngày.
4. Điểm ưu tiên của từng sở thích, rồi **mưa**, rồi sở thích, rồi kiểu đi.

**Quỹ phút:** điểm ngắn tính 75 phút, điểm nửa buổi 150 phút. Đi giữa hai điểm cùng cụm tính 15 phút, cụm kề 30 phút. Một buổi "cân bằng" có tối đa 210 phút,
"khám phá" 240 phút, "nhẹ nhàng" 1 điểm. Từ quỹ phút ra **giờ gợi ý** cho từng điểm, và dòng "khoảng N phút đi" giữa hai điểm liền nhau. Số phút đi này
chính là số bộ xếp đã dùng để giãn giờ, nên giờ in ra và phút đi không thể lệch nhau.

**Mưa:** chỉ xét khi ngày đi nằm trong 7 ngày tới (có dự báo thật). Từ 15/11 có hai mức:
- khả năng mưa từ 60 % trở lên ⇒ có một dòng "Nếu mưa" như trước;
- **đổi điểm sang trong nhà** chỉ khi thêm điều kiện lượng mưa dự báo từ **6 mm / ngày** trở lên. 6 mm là đầu cấp "Mưa" theo quy chuẩn khí tượng Việt Nam; dưới đó là "mưa nhỏ".

Vì sao đổi: con số "khả năng mưa" của dịch vụ dự báo là giờ có khả năng cao nhất trong ngày, nên chỉ cần một giờ có thể lấm tấm là đủ 60 %. Một năm có
222 / 365 ngày như vậy.

Cách đo: lấy một năm dự báo ở Huế, so với lượng mưa đo lại từ quan trắc (bộ dữ liệu ERA5). Thước "mưa thật" giữ cố định là từ 6 mm trở lên, cho cả luật cũ lẫn luật mới.
- Ngày lịch coi là mưa mà thật ra mưa dưới 6 mm (chỉ lấm tấm hoặc không mưa): **106 ⇒ 15**.
- Đổi lại, có 32 ngày mưa thật mà lịch không đổi điểm (luật cũ chỉ sót 2). Nhưng **30 / 32** ngày đó vẫn có dòng "Nếu mưa" nhắc.
- Chuyến 2–5 ngày có ít nhất một ngày bị xếp kiểu ngày mưa: **80 % ⇒ 50 %**.

Giới hạn: số trên dùng bản dự báo tầm ngắn nhất. Khách xếp lịch trước 1–7 ngày thì dự báo kém hơn.

**Sửa chiều 17/11 — ngày mưa, khách không chọn sở thích:** khi khách bỏ trống ô sở thích, lịch có luật cũ "chiều mỗi ngày một điểm thiên nhiên". Luật đó chọn điểm chiều **trước** bước "ngày mưa xét điểm trong nhà trước", mà mọi điểm thiên nhiên trong bảng đều ngoài trời. Vì vậy ngày dự báo mưa to, lịch vẫn đưa khách ra đầm hoặc phá (nhóm thấy khi tự thử: dự báo mưa 100 %, 37 mm, lịch vẫn Đầm Chuồn buổi chiều). Nay ngày mưa (cùng hai mức ở trên) thì bỏ luật thiên nhiên; ngày khô giữ như cũ.
- Đo bằng cách cho bộ xếp chạy 3.880 lịch, bản cũ và bản mới cùng đầu vào, rồi so từng lịch (không gọi model, không tốn tiền). Lịch ngày khô và lịch có chọn sở thích giống hệt bản cũ (2.880 / 2.880 và 3.600 / 3.600) — đúng ý, vì chỉ muốn đổi một trường hợp.
- Trên 300 ngày mưa không chọn sở thích, ngày có điểm ở vùng biển – đầm phá: **109 ⇒ 0**. Ví dụ lịch 1 ngày mưa: Đại Nội → Đầm Chuồn đổi thành Đại Nội → chùa Thiên Mụ → điện Hòn Chén.
- Chưa ổn hẳn: vẫn **181 / 300** ngày đó toàn điểm ngoài trời (trước sửa 253). Lý do là dữ liệu: kho ghi lăng, chùa, kể cả Đại Nội là đường dạo ngoài trời, cả bảng chỉ 12 / 41 điểm trong nhà hoặc nửa trong nửa ngoài. Khách có chọn sở thích thì điểm ưu tiên vẫn giữ chỗ dù mưa (luật anh đã duyệt). Phần còn lại vẫn trông vào dòng "Nếu mưa".

**Model chỉ viết câu tả:**
- Một lần gọi, trả về mỗi điểm một câu ≤ 30 từ, dựa trên một đoạn kho của chính điểm đó.
- Code kiểm từng câu: không được có giờ, tiền, link, tên điểm khác. Câu nào trượt thì **code thay bằng câu dự phòng cho riêng điểm đó**; các câu khác giữ nguyên.
- Khung lịch hiện ngay trên màn hình, câu tả hiện dần sau.

**Phần phụ:**
- **Ảnh cho 24 / 34 điểm**, lấy từ Wikimedia Commons, giấy phép mở. Tác giả và giấy phép giữ trong bảng dữ liệu; từ chiều 14/11 trang không hiện dòng ghi công nữa (anh yêu cầu). Một người xem mù kiểm 10 lịch: ảnh đúng điểm 10 / 10; có một ảnh lăng người xem ghi "đúng loại, không chắc đúng lăng". Từ chiều 15/11: 40 / 41 điểm có ảnh (tối 14/11: 33 / 34; chỉ còn thiếu biển Thuận An) — 26 ảnh từ Wikimedia Commons, 13 ảnh lấy lại từ trang web đã dùng ở mục Khám phá (đã có người nhìn kiểm đúng nơi), 1 ảnh làng nón Tây Hồ do anh tự tìm (bài 24).
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

## Chiều 15/11: thêm 7 nơi vào bảng điểm

Sổ tay của người hướng dẫn viên có hơn 260 bài, nhưng bảng điểm để xếp lịch chỉ có 34 nơi. Hệ quả mình đã đếm được: khách chọn sở thích "chụp ảnh" thì
hơn một nửa số điểm ban ngày trong lịch lại là điểm **không** hợp chụp ảnh, vì bảng hết điểm hợp và bộ xếp phải lấp bằng di tích.

Anh chọn thêm 7 nơi đã có bài trong sổ tay: chùa Từ Hiếu, cầu Trường Tiền, đèo Hải Vân, chợ Bến Ngự, làng nón Tây Hồ, nhà vườn An Hiên, đầm Lập An.
Ba nơi khác bị loại vì thiếu căn cứ (hai nơi không tìm được nguồn nào ghi nên ở bao lâu; một nơi chính sổ tay cảnh báo chưa đón khách bài bản).

**Đo thế nào.** Code chạy đủ 3.840 tổ hợp biểu mẫu (số ngày × trẻ em × người lớn tuổi × kiểu đi × sở thích × 4 ngày đi) trên bảng cũ và bảng mới, rồi
đếm trong các lịch chọn đúng một sở thích: bao nhiêu phần trăm điểm ban ngày nằm **ngoài** sở thích đó. Số càng thấp càng tốt; mốc để so là bảng 34 điểm.

| Sở thích | Bảng 34 điểm | Bảng 41 điểm | Đọc thế nào |
|---|---|---|---|
| Chụp ảnh | 51,7 % | 36,8 % | Từ hơn một nửa số điểm ban ngày là điểm lấp xuống còn hơn một phần ba. Lợi nhất. |
| Ẩm thực | 56,4 % | 44,0 % | Đỡ hơn, vẫn cao: bảng mới chỉ thêm một chợ. |
| Thiên nhiên | 24,4 % | 17,6 % | Đỡ nhẹ; vẫn còn 64 buổi sáng / chiều không có điểm nào để xếp (trước 72), vì một nơi thiên nhiên định thêm đã bị loại trước khi vào bảng. |
| Lễ hội – nghệ thuật | 39,0 % | 39,1 % | Không đổi: sổ tay không có nơi nào để bù. |
| Di tích | 0 % | 0 % | Vốn đã đủ. |

Không lịch nào trong 3.840 phạm luật xếp (0 lỗi ở bước kiểm khung), cả 7 nơi mới đều được xếp.

**Một chỗ phải sửa trong code:** hai nơi xa nhất (Hải Vân, Lập An) nằm phía đông kinh tuyến 108, ngoài cái khung toạ độ mà code dùng để chặn toạ độ gõ
nhầm. Để nguyên thì server từ chối khởi động. Khung được nới về phía đông tới 108,25, vừa đủ cho hai nơi này.

**Một sàn kiểm phải nới, có người duyệt.** Từ đầu có một phép kiểm: cùng một biểu mẫu, lịch "nhẹ nhàng" không được nhiều điểm hơn "cân bằng", và "cân
bằng" không nhiều hơn "khám phá nhiều". Với bảng mới, đúng 1 trong 320 biểu mẫu phạm (320 là 3.840 tổ hợp bỏ đi kiểu đi và ngày đi, vì phép này so ba kiểu đi của cùng một biểu mẫu): đi 3 ngày, chỉ chọn chụp ảnh, ba kiểu đi ra 9 / 12 / 10 điểm.
Nhìn vào lịch thì không phải lỗi: kiểu "khám phá nhiều" dành hẳn ngày thứ ba đi Hải Vân và Lập An, mà ngày đi xa thì chỉ xếp hai điểm và để tối nghỉ.
Phép kiểm đếm số điểm, nên một chuyến đi xa lại bị tính là "đi ít hơn". Người làm không tự sửa phép kiểm cho qua: dừng lại, đưa người điều phối ba cách,
và người điều phối chọn nới đúng một điều kiện — "khám phá" được ít điểm hơn "cân bằng" **chỉ khi** nó có nhiều ngày đi xa hơn. Phép kiểm in ra số tổ
hợp rơi vào ngoại lệ và tự dừng nếu vượt 6 (khoảng 2 %), để lần thêm điểm sau không ai lặng lẽ dựa vào ngoại lệ này.

## Một chuyện thật nữa: mô phỏng sạch, chạy thật thì bốn nơi mới hay chỉ in tên và loại điểm

Bảng 41 điểm qua mọi phép kiểm bằng code: đúng khuôn, 0 lỗi khung. Nhưng các phép đó chỉ kiểm **khung lịch**, không kiểm **câu tả** — câu tả do model
viết, phải chạy thật mới thấy.

Chạy thật thì tốn tiền, nên trước hết code đếm: trong 32 yêu cầu của bộ 20 và bộ để dành, yêu cầu nào ra khung lịch khác đi khi đổi bảng? Có 17. Chỉ 17
yêu cầu đó được chạy thật (chưa tới 0,01 USD). Cả 17 đạt đủ 6 ý chấm bằng code. Nhưng đọc từng câu thì thấy: 9 mục chỉ in câu dự phòng kiểu "tên điểm —
điểm chụp ảnh", và **cả 9 đều rơi vào bốn nơi mới**: cầu Trường Tiền, đèo Hải Vân, đầm Lập An, làng nón Tây Hồ. Thêm 2 mục chỉ hiện mỗi dấu trích nguồn,
không có chữ nào. Ba nơi mới còn lại (Từ Hiếu, Bến Ngự, An Hiên) thì câu nào cũng ổn.

Gốc lỗi nằm ở cột "đoạn mô tả". Với bốn nơi kia, bảng nháp chọn đoạn sổ tay đứng đầu khi tìm bằng tên — và đoạn đứng đầu lại là một dòng thông tin
chung: tên gọi khác, độ cao đỉnh đèo, số nan của khung nón. Model được dặn chỉ viết theo đoạn được đưa, mà đoạn đó không có gì để tả, nên nó trả câu
rỗng hoặc câu vô vị và code thay bằng câu dự phòng. Ba nơi viết tốt là ba nơi tình cờ trúng đoạn "Tổng quan".

Sửa bằng dữ liệu, không đổi lời dặn: chọn lại cho bốn nơi một đoạn thật sự **tả** nơi đó (cảnh đèo nhìn xuống biển, hoàng hôn và hàu ở đầm, xem chằm
nón ở làng, đèn trên cầu buổi tối), đọc tay từng đoạn, ưu tiên đoạn không nêu nguyên tên một điểm khác trong bảng (câu tả mà nhắc tên điểm khác thì code sẽ chặn). Chạy lại 11 yêu cầu có
bốn nơi này: 11 / 11 đạt, 17 / 17 mục của bốn nơi là câu model viết, không còn câu dự phòng nào ở điểm mới. Kèm một sửa nhỏ trong code: câu chỉ có dấu
trích nguồn nay bị coi là câu rỗng và được thay bằng câu dự phòng, thay vì lọt ra màn hình.

Bài học giống lần người chấm mù ở trên, thêm một ý: **mô phỏng kiểm được phần code viết, không kiểm được phần model viết.** Thêm dữ liệu cho phần model
đọc thì phải chạy thật một lượt nhỏ và đọc từng câu.

## Tối 16/11: bản đồ dưới lịch

**Làm gì.** Dưới lịch nay có một khung bản đồ. Mỗi ngày là một bộ **ghim** có số, số trên ghim là thứ tự đi trong ngày và khớp với danh sách đánh số
ngay dưới bản đồ; bấm nút "Ngày 1 / Ngày 2…" thì ghim đổi theo, bấm một ghim thì hiện tên điểm và link mở Google Maps. Bản đồ chỉ ghim điểm tham quan
và hoạt động buổi tối, chưa ghim quán ăn hay khách sạn.

**Vì sao làm vậy.** Lịch xếp theo "cụm gần nhau", nhưng đọc chữ thì khó thấy ngày nào đi gọn, ngày nào đi xa; nhìn ghim là thấy. Toạ độ từng điểm lấy
từ bảng do code giữ, **model không tạo toạ độ** — cùng nguyên tắc với giờ và tên điểm trong khung lịch. Phần vẽ bản đồ là một thư viện mã nguồn mở
chạy trong trình duyệt và được tải riêng: câu hỏi thường ở trang Trợ lý không tải nó và không gọi máy chủ bản đồ lần nào (đã đếm: 0 yêu cầu).
**Ô bản đồ** (các mảnh ảnh nền) lấy từ một máy chủ của cộng đồng OpenStreetMap ở Đức, vì máy chủ chính không nối được từ máy lúc thử; trang chỉ cho
phép tải ảnh từ đúng một máy chủ đó, và trang Giới thiệu nói rõ máy chủ ấy nhận địa chỉ IP của người xem.

**Đo thế nào trước khi bật (chiều 16/11).** Ba lịch thật 1, 2 và 3 ngày: ngày nào số ghim cũng bằng số điểm có toạ độ, và số trên ghim đúng thứ tự
1, 2, 3… của danh sách (3 ghim; 3 và 5; 3, 5 và 4). Trên điện thoại có một lỗi thật: vuốt một ngón qua khung thì bản đồ trượt đi 144 điểm ảnh còn
trang đứng yên, tức người dùng kẹt lại ở bản đồ. Sửa: trên điện thoại một ngón là cuộn trang (đo lại: trang cuộn, bản đồ đứng yên), muốn xem gần thì
dùng nút cộng / trừ hoặc hai ngón. Mốc để so là chính bản trước khi sửa, đo cùng một cách.

**Chuyện thật: số đo đạt hết, nhìn ảnh mới thấy ba lỗi.** Ngay sau khi bật, mình cho trình duyệt tự động xếp một lịch 2 ngày trên bản đang chạy rồi
mở ảnh chụp ra nhìn. Bảng số báo "ghim khớp, không lỗi", nhưng ảnh cho thấy ba chỗ mà phép đếm không biết để đo:
- **Số nằm lệch lên góc ghim**, không ở giữa. Gốc: bộ kiểu dáng của thư viện bản đồ được tải sau và đè lên kiểu của mình. Sửa một dòng.
- **Màn hẹp, ghim thấp nhất bị dòng ghi công che nửa.** Dòng ghi công nằm đè lên mép dưới khung, màn hẹp nó xuống hai dòng. Sửa: khi căn bản đồ cho vừa
  các ghim thì chừa lề dưới rộng hơn. Đo ở màn 390 điểm ảnh, ngày có 5 ghim: 1 ghim bị che ⇒ 0. Cái giá: bản đồ lùi ra một mức.
- **Hai điểm nằm gần nhau thì ghim này che số ghim kia** (trong lịch thử là Lăng Đồng Khánh và Đồi Vọng Cảnh, cách nhau vài trăm mét). Sửa: ghim nào rơi sát một ghim đã vẽ thì vẽ lệch sang
  phải một chút; vị trí thật của điểm không đổi, phóng gần thì tự hết lệch. Đo "số cặp ghim che nhau quá nửa" trên cùng lịch: 1 ⇒ 0, ở cả màn hẹp lẫn
  màn rộng. Mỗi phép đếm mới đều được chạy trên bản cũ trước để chắc nó ra "có lỗi" — một phép đếm lúc nào cũng ra 0 thì không chứng minh được gì.

## Khi nào hỏng

- **Đi rồi quay lại cùng khu trong một ngày** (đếm 17/11, mô phỏng 0 USD, 960 cách điền biểu mẫu): một ngày có thể đi khu A → khu khác → quay lại khu
  A — **104 / 960** lịch có ít nhất một ngày như vậy. Ca dễ thấy nhất: lịch "cân bằng + di tích" (cả lịch ví dụ) đi Đại Nội → chùa Thiên Mụ → quay lại Ngọ
  Môn – Kỳ Đài — **8 / 960**; Ngọ Môn lại chính là cổng của Đại Nội. Lý do: bộ xếp chọn điểm đầu buổi sáng và điểm đầu buổi chiều trước, rồi mới chèn điểm
  thêm sau mỗi điểm đầu theo khu của điểm ngay trước; không bước nào sắp thứ tự đi của cả ngày. Đã thử một bản sửa hẹp (điểm thêm không quay về khu đã rời):
  ca dễ thấy về 0, ca rộng còn khoảng 1 / 3, nhưng làm đổi một ca mưa và một chuỗi sửa lịch ⇒ **để sau lượt đo cuối B7**, chưa vào bản chạy.
- **Bản đồ cần mạng tới máy chủ ô bản đồ**, và máy chủ đang dùng có lúc chậm: vừa đổi ngày, khung có thể xám vài giây rồi mới
  hiện (tối 16/11 có lần chụp trúng lúc khung còn xám, có lần ô hiện gần như ngay; chưa đo thành con số). Mất mạng tới máy chủ đó thì chỉ còn ghim trên nền xám; danh sách đánh số dưới bản đồ vẫn đủ. Ghim vẽ lệch để khỏi che nhau nên ở mức nhìn xa có
  thể cách vị trí thật vài chục điểm ảnh.
- **Khung lịch có lúc hiện quá 1 giây**, ở lượt đầu có dự báo khi bộ nhớ đệm thời tiết còn trống. Anh đã nhận đây là giới hạn.
- **Một nhãn được gắn sau khi thấy sàn trượt.** Sở thích "lễ hội – nghệ thuật" chỉ đạt 43 %, dưới sàn 50 %. Một điểm được gắn thêm nhãn này (có căn cứ trong
  kho) và sàn lên đúng 50 %, không còn biên. Việc này đã đưa anh duyệt, nhưng là chỗ mỏng.
- **Ăn uống ở nơi xa còn mỏng.** Lịch gợi ý quán trong 2 km quanh điểm, và chỗ ở theo khu (bài 25). Ở những nơi không có quán nào trong bảng gần như vậy, lịch in **một câu ghi chú lấy từ sổ tay** thay cho tên quán: đầm Lập An và đèo Hải Vân (ven đầm có nhiều nhà hàng hải sản), làng nón Tây Hồ (chưa có gợi ý quán, nên ăn ở trung tâm), và từ 16/11 **phá Tam Giang** (quán dân dã ven đầm ở Đan Điền, Thuận An có bánh khoái cá kình; bữa tối có sàn bè hải sản ven phá). Phá Tam Giang trước đó là nơi trống bữa nhiều nhất: điểm đặt ở cầu Tam Giang, hai quán Đầm Chuồn trong bảng quán của lịch cách khoảng 9,3 km, và tra web không ra quán nào đủ nguồn trong 2 km. Đếm bằng mô phỏng trên mọi tổ hợp lịch (22.752 bữa, không tốn tiền): bữa có dòng gợi ý (quán hoặc ghi chú) **86,4 % ⇒ 94,5 %**; bữa có **tên quán** vẫn **75,2 %** — ghi chú chỉ nói điều sổ tay biết, không thay được một cái tên. Hai quán ven đầm Lập An đã viết nháp cho sổ tay cách điểm 2,5–2,75 km, nên dù vào sổ cũng không hiện trong lịch. Bản đồ trong lịch có code nhưng chưa bật.
- **File .ics:** khung giờ qua nửa đêm sẽ mất sự kiện (bảng hiện chưa có điểm như vậy). Hai lịch cùng ngày bắt đầu có thể ghi đè nhau trong ứng dụng lịch.
- **Bảng điểm có 41 điểm** (34 điểm tới sáng 15/11). Điểm ngoài bảng thì lịch không xếp được.

## Ba điều chính

1. Bản 2 là **code xếp theo chuỗi luật có thứ tự** (an toàn ⇒ giờ mở cửa, mùa ⇒ cụm gần ⇒ mưa ⇒ sở thích ⇒ kiểu đi) với quỹ phút và giờ gợi ý. Model chỉ
   viết một câu tả mỗi điểm, câu nào trượt kiểm thì code thay.
2. Nghiệm thu lần đầu **trượt** (16 / 20). Gốc lỗi là **bài kho mỏng**, nên phần câu dự phòng sửa bằng dữ liệu, không sửa code: 20 / 20. Phần chấm mù
   đạt 12 / 12 × 2 sau khi sửa ba lỗi nhỏ trong code. Bật từ 14/11.
3. Chuyện thật: người chấm mù thấy **ba lỗi** mà mô phỏng không bắt (dòng ngày mưa, sáng chồng chiều 52 / 3.840 khung, câu nội bộ). Mô phỏng và người đọc
   thật bổ sung cho nhau. Chiều 15/11 thêm một lần nữa: bảng điểm lên 41 nơi, mô phỏng sạch, nhưng 17 lịch chạy thật mới lộ ra: ở bốn nơi mới, 11 / 17 mục
   không có câu tả (9 câu dự phòng, 2 mục chỉ có dấu nguồn) vì gắn nhầm đoạn sổ tay nghèo ý — mô phỏng không kiểm được phần model viết.

**Bài sau:** Bài 24 — Giao diện H1 "Sông Hương": chọn hướng, hiệu ứng làm bằng gì, và đo thế nào để đẹp mà không chậm.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Đi rồi quay lại cùng khu (17/11): 104 / 960, 8 / 960 `data/dem_lich_2026-11-17/dem_quay_lai.py` (C) [đã chạy]; bản sửa hẹp WIP `p9-khong-quay-lai-cum` của E, 960 + 3.840 khung, hẹp 8 / 24 ⇒ 0 / 0, rộng 65 / 258 ⇒ 20 / 76, điểm ban ngày −0,47 % / −0,42 %, ca mưa + chuỗi S01: `data/di_lai_2026-11-17/README.md` [đã chạy, chưa merge].
- Bản cũ 7 / 28 điểm không xếp, "đi dày" 0 / 120: `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` §2, §3.1 [đã chạy]
- Ngày mưa bỏ luật thiên nhiên khi không chọn sở thích (17/11): 3.880 lịch so bản cũ ↔ mới, 109 ⇒ 0 / 300, 253 ⇒ 181, 2.880 / 2.880 + 3.600 / 3.600 giống hệt — `report_agent/2026-11-12_ra_khoang_cach/b_mua_bo_thien_nhien_implementation.md`, script `data/mua_bo_thien_nhien_2026-11-17/tools/` [đã chạy]; luật ở `backend/llm/lich_trinh_v2.py` (`la_ngay_mua`, `diem_dau`) [code].
- Ngưỡng mưa 6 mm (User 15/11): số so ERA5 ≥ 6 mm (106 ⇒ 15 báo thừa, sót 32 với 30 / 32 có dòng nhắc, chuyến 80,4 ⇒ 50,0 %): `report_agent/2026-11-12_ra_khoang_cach/c_dem_mua.md` phần 5, script `data/dem_mua_2026-11-14/so_mua_that_qcvn.py` [đã chạy]; mốc QCVN 84:2024 `b_nguong_mua_3_model.md`; code `MM_MUA_XEP`, `len_ke_hoach.ngay_mua_xep` [code].
- Biểu mẫu 4 nhóm, thứ tự luật, quỹ phút 75 / 150, phút đi 15 / 30, quỹ 210 / 240, mưa ≥ 60 % trong 7 ngày, câu ≤ 30 từ, kiểm câu, câu dự phòng: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` §3.1, §5, §5b, §5c; `backend/llm/lich_trinh_v2.py` [code]
- Nghiệm thu, 16 / 20 – 17 / 20, gốc lỗi bài mỏng, 20 / 20, 4,06 ↔ 5,12 s, 10 điểm có đoạn mô tả, bật 10:46 / 11:00 ngày 14/11: `report_agent/…/b_len_ke_hoach_dot_1_implementation.md` §0, §4.2, §9, §12; `report_agent/…/e_review_len_ke_hoach_dot_1.md` [đã chạy]
- Ba lỗi người chấm mù, 9.600 khung, 52 / 3.840 ⇒ 0, 1.068 câu, 12 / 12 × 2, 6 / 6: `report_agent/…/e_review_len_ke_hoach_nhanh_1411.md` (M-1, M-2, "Kiểm phần sửa"); `b_len_ke_hoach_dot_1_implementation.md` §10, §11 [đã chạy]
- Nhãn tối 228 / 960 ⇒ 0: `report_agent/…/b_lich_truong_gd_implementation.md`, `c_review_lich_truong_gd.md` [đã chạy]
- Ảnh 24 / 34, 10 / 10, một ảnh lăng "không chắc đúng lăng": `report_agent/…/b_anh_lich_implementation.md`, `c_review_anh_lich.md`; .ics 44 lịch ⇒ 33 có ngày ⇒ 288 sự kiện: `session_prompt/CURRENT_HANDOFF.md`, `session_prompt/sessions/STATUS_E.md` (mốc 12:07 14/11); giới hạn qua nửa đêm / UID: `report_agent/…/c_review_xuat_ics.md`; cách làm: `docs/superpowers/plans/2026-11-14-xuat-lich-ics-plan.md`, `frontend/src/lich_ics.js` [code, đã chạy]
- **Sửa 13:40 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_24.md`): bản trước nói "không sửa một dòng code nào" — sai, bộ chấm mù đạt sau 3 sửa code; cột "lần đầu" ghép hai lượt (nay lượt đầu: 16 / 20 và 2 lịch > 30 %); 10 / 12 chỉ do thiếu dòng "Nếu mưa"; nhóm hạn chế là "không xếp buổi tối" chứ không chỉ "không tối muộn"; giải nghĩa bộ 20 / bộ để dành / phép dò.
- Nhãn lễ hội 43 % ⇒ 50 %: `b_len_ke_hoach_dot_1_implementation.md` §4.1, `c_so_moc_buoc_b.md` [đã chạy]
- **Sửa / thêm 15:02 16/11/2026:** dòng "Ăn uống ở nơi xa" bản trước ghi bữa tối Hải Vân và làng nón Tây Hồ "để trống" — đã có ghi chú từ tối 15/11 (`backend/llm/quan_lich.py` `GHI_CHU_AN`, chú thích 15/11 tối) ⇒ sửa. Ghi chú phá Tam Giang: chữ theo `knowledge-base-hue/travel/places/Phá Tam Giang.md` dòng 149 + 192, code `GHI_CHU_AN[("pha_tam_giang", …)]` [code, merge `9ac14cf`]; 86,4 ⇒ 94,5 %, 75,2 %, 22.752 bữa, 1.824 bữa Tam Giang: mô phỏng `data/sua_kho_2026-11-16_lap_an/tools/dem_bua_tam_giang.py` (riêng tư) [đã chạy]; quán Đầm Chuồn ~9 km, tra web không ra quán đủ nguồn: `data/tra_cuu_cli/2026-11-16_quan-tam-giang-lap-an/` + B tự mở trang [đã chạy]; hai quán Lập An 2,5–2,75 km (toạ độ Photon theo tên đường, đo bằng công thức khoảng cách của `quan_lich`): `data/sua_kho_2026-11-16_lap_an/TIEU_CHI.md` (riêng tư) [đã chạy].
- Bảng 41 điểm (chiều 15/11): 51,7 ⇒ 36,8 % / 56,4 ⇒ 44,0 / 24,4 ⇒ 17,6 / 39,0 ⇒ 39,1 / 0, buổi trống 72 ⇒ 64, 0 lỗi khung, khung toạ độ 108,25, ngoại lệ 1 / 320 (9 / 12 / 10, trần 6), 17 / 32 yêu cầu có khung đổi, 9 câu dự phòng ở 4 nơi + 2 câu chỉ có mã nguồn, chạy lại 11 / 11 và 17 / 17 mục, ảnh 39 / 41, ghi chú ăn, ảnh 26 Commons + 13 web: `report_agent/2026-11-12_ra_khoang_cach/e_diem_v9_implementation.md` mục 1–5, 8 [đã chạy]; 3 nơi bị loại: `e_diem_lich_moi_nhap.md` [đã chạy]; review `b_review_diem_v9.md` (B tính lại số mô phỏng + ngoại lệ, khớp); code `KHUNG_HUE`, `kiem_cau`, `GHI_CHU_AN`, test `test_simulation_always_rules` [code]. Số lượt thật (17 / 17, 9 câu dự phòng, 11 / 11) là số của người làm, người review không chạy lại lượt có phí.
- **Kiểm độc lập chiều 15/11** (agent ngữ cảnh mới, 82 mục: 70 đúng, 0 sai, 10 câu dễ hiểu nhầm đã sửa, 2 không kiểm được — "tránh đoạn nhắc tên điểm khác" và số 1 / 102 của lượt cũ): biên bản private `data/tai_lieu_v9_nhap_2026-11-15/kiem_doc_lap_bai_23_chieu_1511.md`.
- Khung > 1 s là giới hạn đã nhận: `b_len_ke_hoach_dot_1_implementation.md` §5 [tài liệu]

</details>
