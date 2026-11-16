# Bài 14 — Việc dễ nhầm thì code làm: ngày âm lịch, thời tiết, khoảng cách, lịch trình

*Cập nhật lần cuối: 21:08, ngày 16/11/2026 · câu ghi chú "chưa tính kẹt xe" nay do code nối. Trước: 20:49, ngày 16/11/2026 · số đo của mục "code tra sẵn" nay là số đo lại trên bản đang chạy. Trước: 19:34 16/11/2026 · thêm mục "code tra sẵn khi câu nêu rõ hai nơi" (bật tối 16/11). Trước: 15:17 16/11/2026 · thêm mục "Khoảng cách giữa hai điểm" (bật 16/11). Trước: 12:33 15/11/2026 · thời tiết "tuần sau" có số cho phần nằm trong 7 ngày dự báo (sửa câu cũ ở "Khi nào hỏng"). Trước: 13:45 14/11/2026 · mục biểu mẫu là bản đầu; từ 14/11 chạy bản 2 (bài 23).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Công cụ ngày — **mới** | **`ngay_lich`** (thư viện **lunar-vn** 1.4.0) | Code tính hôm nay, đổi ngày dương ↔ âm theo lịch Việt Nam. |
| Lịch tính sẵn — **mới** | **`lich_san`** → nguồn **"Lịch hệ thống"** | Khi câu có từ chỉ ngày, code tính sẵn các ngày liên quan và đưa vào ngữ cảnh **trước** lần gọi model đầu. |
| Công cụ thời tiết — **mới** | **`thoi_tiet`** (dịch vụ **Open-Meteo**) | Code lấy dự báo 7 ngày cho Huế, dựng sẵn các con số. |
| Công cụ khoảng cách — **mới** | **`khoang_cach`** | Code tra số km đường đi và số phút đi xe giữa hai điểm trong bảng lịch; model chỉ chọn mã hai điểm. |
| Khoảng cách tính sẵn — **mới** | **`khoang_cach_tinh_san`** | Khi câu nêu rõ hai nơi trong bảng, code tra số **trước** lần gọi model đầu, model khỏi phải gọi công cụ. |
| Bảng tìm đường — **mới** | **OSRM** (Open Source Routing Machine) | Dịch vụ tìm đường trên bản đồ mở; mình chỉ gọi **một lần** để dựng sẵn bảng km / phút. |
| Biểu mẫu lên kế hoạch — **mới** | **`lich_trinh_bieu_mau`** + **`lich_trinh`** | Người dùng chọn số ngày, người đi cùng, sở thích bằng nút; code xếp lịch theo buổi; model chỉ viết lời. |
| Câu cố định | ví dụ **`CAU_BAO_LU`**, **`CAU_NGOAI_7_NGAY`** | Câu viết sẵn trong code cho trường hợp đặc biệt; model không được tự viết. |

---

*Bài 12 nêu nguyên tắc chia việc: phép tính, luật, thứ tự bắt buộc thì code làm; model chỉ chọn và diễn đạt. Bài này kể bốn chỗ áp nguyên tắc đó rõ nhất:
ngày tháng, thời tiết, khoảng cách, và lịch trình.*

## Quay lại người hướng dẫn viên

Khách hỏi: *"Rằm tháng Giêng năm nay là thứ mấy?"* Một người hướng dẫn viên cẩn thận **không nhẩm**. Nhẩm ngày âm lịch rất dễ sai một ngày, và sai một ngày
thì khách lỡ cả lễ hội. Họ **mở cuốn lịch ra xem**. Khách hỏi *"mai Huế mưa không?"*, họ **mở dự báo** ra đọc, không đoán theo mùa.

Khách nhờ *"lên giúp lịch đi Huế 2 ngày, đi cùng ba mẹ"*, họ cũng không ứng khẩu. Họ có sẵn **một bảng các điểm** ghi điểm nào hợp buổi sáng, buổi chiều hay
buổi tối, có hợp người lớn tuổi không. Họ xếp theo bảng đó, rồi mới **kể lại bằng lời** cho khách. Khách hỏi *"từ đây sang lăng kia bao xa?"*, họ
**nhìn bản đồ**, không nói đại "chắc tầm 5 cây".

Trong mọi trường hợp, phần **con số và thứ tự** đến từ dụng cụ (lịch, dự báo, bảng điểm). Phần người làm là **chọn dụng cụ** và **nói cho dễ nghe**.

## Ngày tháng và âm lịch

**Vì sao không để model tự tính:** model không biết hôm nay là ngày nào, trừ khi được cho biết. Đổi ngày âm ↔ dương là phép tính thiên văn, model hay lệch
một ngày. Câu kiểu "rằm tháng Giêng năm nay" còn phải biết "năm nay" là năm âm nào. Đầu tháng 1 dương lịch thì có khi vẫn đang ở năm âm cũ.

**Code làm gì:**
- Dùng thư viện **lunar-vn**, bản Python của thuật toán Hồ Ngọc Đức, tính theo **giờ Việt Nam (UTC+7)**. Không dùng thư viện lịch Trung Quốc, vì Trung Quốc tính
  theo UTC+8 nên có năm Tết lệch hẳn (ví dụ năm 1985: Tết Việt Nam 21/01, Trung Quốc 20/02).
- Chỉ nhận năm **1976–2100**. Trước 1976 hai miền Việt Nam dùng lịch âm khác nhau, nên với năm cũ code trả câu cố định thay vì đoán.
- Câu nói một ngày âm mà **không nêu năm**, hoặc nói "năm nay" ⇒ code nêu cả **lần đã qua và lần sắp tới**, để người dùng không bị nhầm năm.

**Lịch tính sẵn (từ 10/11).** Ban đầu, ngày là một **công cụ**: model tự quyết gọi, đợi code tính, rồi mới viết. Mỗi lần gọi công cụ là một vòng qua lại, nên câu
có ngày rất chậm. Nay khi code **dò thấy từ chỉ ngày** trong câu ("hôm nay", "mai", "cuối tuần", "rằm", "Tết"…), nó **tính sẵn** hôm nay, mai, 7 ngày của tuần này
hoặc tuần sau (khi câu nói tới), rằm tháng này / tháng tới, cộng với các ngày âm nêu trong câu hoặc trong 10 đoạn kho, rồi thêm thành một nguồn tên **"Lịch hệ thống"** vào ngữ cảnh **trước** lần gọi model
đầu. Công cụ ngày vẫn còn, nhưng chỉ làm dự phòng.

| Đo gì (19 câu có ngày, 10/11) | Trước (gọi công cụ) | Sau (tính sẵn) | Nghĩa là |
|---|---|---|---|
| Chữ đầu tiên, trung vị | 5,60 s | **2,35 s** | từ vượt mức 3 s xuống dưới mức |
| Chữ đầu tiên, câu chậm (95 %) | 10,14 s | **4,56 s** | từ vượt mức 5 s xuống dưới mức |
| Tiền một câu | 0,00049 USD | **0,00036 USD** | rẻ hơn, dưới trần |
| Số lần gọi model (cả 19 câu) | 52 | **31** | bớt hẳn các vòng qua lại |
| Model gọi công cụ ngày dự phòng | — | 0 lần | lịch tính sẵn đã đủ |

Trước đó (09/11), khi mới thêm công cụ ngày: **bớt 9 câu từ chối nhầm**, **0 câu sai ngày**.

## Dự báo thời tiết

**Code làm gì:**
- Gọi **Open-Meteo** (dịch vụ dự báo miễn phí) với **toạ độ cố định** ở trung tâm thành phố Huế. Không gửi chữ nào của người dùng ra ngoài.
- Hạn **3 giây**, không thử lại. Lưu tạm kết quả **30 phút**, vì dự báo không đổi từng phút và đỡ gọi lại.
- **Code dựng sẵn các con số** (nhiệt độ, mưa…) ghi kèm nguồn và giờ lấy. Số nào model viết ra phải nằm trong tập số code đã đưa.
- Hỏi ngày **ngoài 7 ngày tới** ⇒ câu cố định: "mình chỉ có dự báo 7 ngày tới…"; số nào model nêu thêm (nếu có) chỉ là khí hậu chung theo tài liệu.
- Hỏi **"tuần sau"** (từ 15/11): **code** tính những ngày của tuần sau còn nằm trong 7 ngày dự báo, đưa đúng các ngày đó kèm dòng "dự báo chỉ có tới <thứ, ngày>".
  Chỉ khi hôm nay là thứ Hai (cả tuần sau đều quá 7 ngày) hoặc hỏi "tuần sau nữa" mới ra câu cố định. Trước 15/11, mọi câu "tuần sau" đều ra câu cố định —
  kể cả Chủ nhật hỏi "thứ hai tuần sau", tức ngày mai.
- Câu về **bão, lũ, ngập** ⇒ câu cố định trỏ tới Trung tâm Dự báo khí tượng thủy văn quốc gia, cổng cảnh báo lũ quét, và **gọi 112** khi nguy hiểm. Model không
  được tự viết về thiên tai.
- Công cụ thời tiết **chỉ được đưa** khi câu có từ khoá thời tiết (bài 12).

Trang chủ của cổng du lịch cũng có một ô thời tiết đọc thẳng từ đây, không gọi model.

## Khoảng cách giữa hai điểm

**Vì sao cần (đếm trước khi xây, 16/11):** kho có bài về từng nơi, nhưng hầu như không ghi "từ nơi này sang nơi kia bao xa". Mình hỏi 6 câu kiểu đó trên
server đang chạy: **4 / 6 câu bị từ chối** rồi mới ra mục "Từ web". 2 câu còn lại được ước từ câu "cách trung tâm … km" trong bài. Một lỗi có thật, đủ lớn để làm.

**Code làm gì:**
- **Dựng bảng sẵn một lần:** lấy toạ độ của 40 / 41 điểm trong bảng lịch (một điểm chưa có toạ độ), gửi **một lần** cho OSRM để lấy số km đường đi và số phút
  đi ô tô giữa mọi cặp: **1.560 cặp**, đủ cả. Chỉ toạ độ công khai đi ra ngoài, không chữ nào của người dùng. Lúc chatbot chạy **không gọi mạng**, chỉ tra bảng.
- **Model chỉ chọn mã:** công cụ có danh sách cố định 41 mã điểm (kèm tên khác, như "Hiếu Lăng" là lăng Minh Mạng) và một mã "khác". Model đọc câu hỏi, chọn mã
  hai nơi. Nơi không có trong bảng (khách sạn, sân bay, "trung tâm", nơi ngoài Huế) ⇒ chọn "khác" ⇒ code trả câu cố định "Mình chưa có số khoảng cách cho nơi
  này". Code không tự đoán tên nơi từ chữ người dùng.
- **Code viết dòng có số:** "Từ A đến B: khoảng X km đường đi, khoảng Y phút đi xe (ước theo đường)", kèm "chưa tính kẹt xe hay dừng nghỉ". Dòng này là một
  nguồn có mã [n] như mọi nguồn khác.
- **Code kiểm số model viết:** số km và số phút trong câu trả lời phải nằm trong số của nguồn khoảng cách (km so với km, phút so với phút) hoặc trong đoạn kho
  được trích. Lệch ⇒ rút câu trả lời lại, như khi trích nguồn sai.
- **Code nối câu ghi chú (từ tối 16/11):** câu "chưa tính kẹt xe hay dừng nghỉ" phải luôn đi cùng số ước. Lúc đầu mình để model tự chép câu này từ nguồn;
  đếm lại 52 câu của bốn lượt đo thì model chỉ chép ở **33 câu** (khoảng 65 %), bỏ ở phần còn lại — đường model gọi công cụ và đường code tra sẵn bỏ như
  nhau (17 / 26 và 16 / 26). Nay khi câu trả lời có trích nguồn khoảng cách mà chữ model không nhắc "kẹt xe", code tự đặt câu ghi chú vào dòng lưu ý cố định
  dưới câu trả lời; model đã viết rồi thì code không lặp. Thử trên bản đang chạy: 3 câu model bỏ ghi chú ⇒ cả 3 có dòng lưu ý; 1 câu model tự viết ⇒ không
  lặp. Chỗ còn hở: nếu chữ "kẹt xe" xuất hiện ở một ý khác của câu trả lời thì code tưởng đã có và không thêm.
- Công cụ **chỉ được đưa** khi câu có từ khoá kiểu "bao xa", "mấy km", "có gần không", hay "mất bao lâu" đi kèm từ di chuyển ("đi", "từ", "sang"…). Câu như
  "nấu nồi bún bò mất bao lâu" không có từ di chuyển ⇒ không đưa công cụ.

**Đo ra sao (16 câu qua server tạm, 16/11):** 14 câu có hai nơi trong bảng, 2 câu có nơi ngoài bảng.

| Đo gì | Kết quả | So với đâu · nghĩa là |
|---|---|---|
| Model chọn đúng cặp điểm | **13 / 14** | luật ghi trước là ≥ 12 / 14 ⇒ đạt. Câu còn lại hỏi "có gần nhau không"; model trả lời từ bài kho (có trích nguồn), không gọi công cụ |
| Số sai tới tay người dùng | **0** | sàn là 0. Không câu nào có số km / phút lệch nguồn, không câu nào bị rút lại |
| Nơi ngoài bảng mà ra số | **0 / 2** | sàn là 0. Một câu model chọn "khác", một câu model không gọi công cụ; cả hai bị từ chối rồi ra mục "Từ web" như trước (số trong mục web là của web, có ghi nguồn) |
| Tiền một câu có công cụ | khoảng **0,0008 USD** | trước đây câu loại này bị từ chối rồi tra web, khoảng 0,0023 USD ⇒ rẻ hơn; nhưng vẫn trên trần chung 0,0005 USD một câu |
| Chữ đầu tiên, trung vị / câu chậm (95 %) | **3,7 s / khoảng 6,2 s** | mức anh chốt là 3 s / 5 s ⇒ **chưa ổn**: câu loại này thường gọi model 3 lần (phân loại, gọi công cụ, viết) |

Trước khi bật còn có bộ 27 câu dò từ khoá do một người khác soạn: **0 câu khoảng cách bị bỏ sót**. Bộ 32 câu an toàn: không câu nào có từ khoá ⇒ chuỗi gửi
model của bộ an toàn không đổi, không cần chạy lại.

### Làm cho nhanh hơn: code tra sẵn khi câu nêu rõ hai nơi (làm và đo tối 16/11)

Dòng cuối của bảng trên là chỗ chưa ổn: chữ đầu tiên 3,7 s, vượt mức 3 s anh chốt. Mình đọc log từng câu thì thấy chỗ tốn nhất là **lần gọi model chỉ để nói
"gọi công cụ với hai mã này"** — khoảng 1,8 s, rồi mới tới lần gọi thứ hai để viết. Giống người hướng dẫn viên phải hỏi lại "anh muốn tra cặp nào?" dù câu
hỏi đã nêu rõ hai nơi.

**Code làm gì:** cùng cách với "lịch tính sẵn" ở phần ngày tháng. Khi câu **đang gõ** có từ khoá khoảng cách **và** code đọc được **đúng hai** tên điểm của
bảng, code tra bảng ngay, đưa dòng có số vào ngữ cảnh trước lần gọi model đầu, và lượt đó không đưa công cụ nữa. Model chỉ còn việc viết. Bước kiểm số sau
khi viết vẫn chạy như cũ.

Đọc tên nơi từ chữ người dùng là việc dễ nhầm, nên luật đặt dè dặt — **không chắc thì về đường cũ** (model gọi công cụ, chậm hơn nhưng đúng). Code chỉ
nhận câu **đúng một dạng quen**: "[từ] A, một từ nối, B, rồi tới ngay từ hỏi khoảng cách" — như "Từ A đến B bao xa?", "A cách B mấy km?", "A với B cách
nhau bao xa?", "A có gần B không?".
- Tên phải khớp nguyên cụm với tên hoặc tên khác trong bảng, cụm dài xét trước. Hai chỗ nới: tên trong bảng kết thúc bằng "Huế" thì đọc được cả khi bỏ chữ
  "Huế" ("Đại Nội Huế" ⇒ "Đại Nội"); và một danh sách nhỏ tên gõ tắt chỉ dùng cho việc đọc câu ("Đông Ba", "Thiên Mụ", "Tràng Tiền").
- Trước tên thứ nhất chỉ được là "từ" / "đi từ" hoặc không có gì; giữa hai tên chỉ được là một từ nối trong danh sách ngắn ("đến", "sang", "ra", "cách",
  "với"…). Có chữ khác chen vào ⇒ đường cũ.
- Một nơi, ba nơi trở lên, một tên nhắc hai lần, hay một cụm tên trỏ tới hai điểm ⇒ đường cũ.
- Câu so sánh ("nơi nào gần hơn") và câu hỏi tiếp kiểu "từ đó sang lăng kia bao xa" ⇒ đường cũ.

**Đo ra sao:** trước khi tốn tiền, một người khác (không viết code này) soạn 32 câu dò, có cả câu bẫy: tên trùng một phần, tên nằm trong tên khách sạn, câu
ba nơi, câu nhắc hai nơi mà hỏi việc khác. Luật dừng ghi trước: **0 câu ra sai cặp**. Mọi số trong bảng dưới là của **bản cuối, đang chạy** (sau khi review — chuyện kể ngay sau bảng). 16 câu đo có phí đã chạy hai lần: một lần trên bản đầu
(trung vị chữ đầu 1,80 s) và một lần đo lại sau khi bật trên bản cuối; hai lần ra gần như nhau, bảng ghi lần sau.

| Đo gì | Kết quả | So với đâu · nghĩa là |
|---|---|---|
| Bộ dò 32 câu (không tốn tiền) | **29 đúng · 0 sai cặp · 3 về đường cũ** | luật dừng là 0 sai cặp ⇒ đạt. Ba câu về đường cũ: một câu nhắc điểm chưa có toạ độ, hai câu có mệnh đề dẫn trước tên ("Mình ở A, muốn qua B…") — chậm như cũ nhưng không sai |
| 21 câu phá của người review (không tốn tiền) | **20 đúng · 0 sai cặp · 1 về đường cũ** | bản đầu: **15 / 21 ra sai** ⇒ phải sửa (xem dưới) |
| 16 câu đo lại qua server tạm: đi đường nào | **13 nhanh · 3 cũ** | 3 câu đường cũ: một câu hỏi tiếp "từ đó sang…", hai câu có nơi ngoài bảng |
| Đúng cặp điểm | **14 / 14** | lần đo công cụ 16/11 là 13 / 14 |
| Số sai tới tay người dùng · nơi ngoài bảng ra số | **0 · 0 / 2** | sàn đều là 0 ⇒ giữ nguyên |
| Chữ đầu tiên, trung vị của 13 câu đường nhanh | **1,9 s** | đường công cụ 3,7 s; mức anh chốt 3 s ⇒ **ổn**. Còn 2 / 13 câu trên 3 s: một câu hỏi thêm "nên đi buổi nào" nên model tìm kho thêm (4,0 s), một câu 3,9 s chưa rõ vì sao (lần đo trên bản đầu cũng 2 / 13 câu) |
| Tiền một câu đường nhanh | khoảng **0,0004 USD** (trung vị) | đường công cụ khoảng 0,0008 ⇒ rẻ bằng nửa. **12 / 13 câu** dưới trần chung 0,0005; câu hỏi thêm "nên đi buổi nào" tốn hơn 0,0005 một chút vì model tìm kho thêm |

Mẫu mới 13 câu nên mình chưa nói được gì về "câu chậm nhất trong 20 câu"; chỉ nói được trung vị và đếm số câu vượt 3 s.

**Bản đầu sai ở đâu, review bắt thế nào.** Bản đầu chỉ **đếm tên**: câu có đúng hai tên điểm là tra. Bộ 32 câu soạn trước cho 31 đúng, 0 sai, mình tưởng đã
ổn. Người review (không viết code này) tự soạn 21 câu phá và **15 câu ra sai cặp**. 14 câu thuộc ba kiểu: câu có đủ hai tên nhưng hỏi khoảng cách tới một nơi thứ ba
("A và B cách trung tâm bao xa?", "từ ga đến A và B…"); tên điểm nằm trong một tên riêng khác (khách sạn, nhà hàng, cây cầu mang tên đó); câu so sánh viết
kiểu khác. Câu thứ 15 viết ngược chiều ("đến B từ A"), code đọc thành đi từ B. Ở các câu đó code sẽ đưa cho model số của **cặp không được hỏi**, và bước kiểm số vẫn cho qua vì số "có nguồn". Cách sửa không phải thêm danh sách
từ cấm, mà đổi hướng: **chỉ nhận dạng câu quen, còn lại từ chối**. Sau sửa: 0 câu ra sai trên cả hai bộ. Cái giá của việc siết: trên bộ 32 câu, số câu được tra sẵn giảm 2 (hai câu có mệnh đề
dẫn trước tên, nay về đường cũ); còn 16 câu đo thì kiểm lại không tốn tiền vẫn đủ 13 câu được tra sẵn. Bài học: với code đọc chữ người dùng, "có đủ hai tên" chưa nói được câu đang hỏi gì.

**Khi nào hỏng:** câu viết khác dạng quen thì về đường cũ — đúng nhưng chậm như trước. Và câu có nơi thứ ba nằm **sau** từ hỏi ("Từ A đến B bao xa, rồi sang
C nữa?") mà C **không** phải tên code đọc được (một khách sạn, hay tên gõ trần của một lăng) thì code vẫn trả khoảng cách A–B: số đúng cho chặng đầu,
chưa trả lời hết câu. Nếu C là tên có trong bảng thì câu có ba tên, về đường cũ.

### Chuyện thật: hằng số "40 km/h" chọn bằng mắt, review bắt

OSRM tính theo tốc độ cho phép của con đường, nên ra nhanh hơn thực tế: 4 km chỉ 4 phút. Bản đầu, mình đặt luật "đi không nhanh hơn 40 km/h". Hằng số này mình
chọn sau khi **nhìn 2 cặp** (4 km / 4 phút và 15 km / 14 phút), và quên mất bước plan đã ghi: "đối chiếu 5 cặp với nguồn công khai".

Người review (một agent khác) chạy lại cả bảng và thấy hằng số đó **đổi số phút ở 1.082 / 1.560 cặp**, tức phần lớn con số người dùng thấy do một con số mình
chọn bằng mắt. Mình tra 8 cặp trên các bài du lịch công khai (có km và / hoặc số phút, phần lớn tính "từ trung tâm"), rồi tự mở lại 3 nguồn để kiểm:

| Cặp (loại đường) | Số phút nguồn ghi | Luật cũ (sàn 40 km/h) | Luật mới (1,25 × OSRM + 5) |
|---|---|---|---|
| Đại Nội → lăng Tự Đức (nội thành, ~6 km) | 20 (xe máy) / 20–25 (taxi) | 12 — quá nhanh | **20** |
| Huế → đầm Lập An (đường dài, ~65 km) | ~75 (xe riêng) | 105 — quá chậm | **84** |
| Cả 6 cặp so được | — | **3 / 6** trong khoảng nguồn | **6 / 6** trong hoặc sát khoảng nguồn |

Số km của OSRM thì khớp nguồn, lệch khoảng 10 % (lớn nhất 12 %); chỉ số phút cần sửa. Luật mới **1,25 × phút OSRM + 5**: đi thật mất thêm khoảng một phần tư
thời gian so với OSRM, cộng 5 phút ra vào chỗ đỗ xe. Đây vẫn là **luật ước** khớp 6 điểm đối chiếu, không phải số đo thật trên đường. Bài học: một hằng số quyết con số người dùng
thấy thì phải đối chiếu với nguồn trước, không chọn bằng cảm giác.

## Biểu mẫu "Lên kế hoạch"

*Mục này tả **bản đầu** (07/11). Từ 14/11, chatbot chạy **bản 2**: biểu mẫu bốn nhóm, code xếp theo chuỗi luật có giờ gợi ý, quỹ phút, mưa, ảnh từng điểm. Xem bài 23.*

Người dùng điền biểu mẫu bằng nút: **số ngày**, **đi cùng ai** (một mình, bạn bè, gia đình có trẻ em, người lớn tuổi…), **sở thích**. Rồi:
1. Lượt này **không qua bước xếp loại**. Code gọi thẳng phần xếp lịch với **đúng giá trị các nút**.
2. **Code xếp lịch theo buổi** (sáng, chiều, tối) từ **một bảng điểm anh đã duyệt**. Bảng ghi điểm nào hợp buổi nào, hợp ai, có trong nhà không. Buổi sáng ưu
   tiên điểm hợp sở thích. Nhóm có trẻ em hoặc người lớn tuổi thì **không xếp buổi tối**, và lý do được ghi rõ (ở bản 2 từ 15/11: một dòng trong phần ghi chú của lịch, buổi để trống không còn hiện thành mục riêng — bài 23).
3. Code **kiểm khung**: đủ số buổi, không trùng điểm, đúng luật bảng.
4. Model viết lời theo khung, **một lần, không công cụ**, với mức suy luận thấp cho nhanh.
5. Code **kiểm cuối** (lời có nói ngược khung không), rồi nối thêm **link mở Google Maps** cho từng điểm. Link do code dựng từ tên điểm, model không tự viết link.

Kết quả (07/11): sàn kiểm bằng code **24 / 24**; lời khớp khung **12 / 12**, chạy hai lượt đều vậy; chữ đầu tiên câu chậm 4,25 giây.

**Lịch trình từ câu gõ tự do** ("lên lịch giúp mình đi Huế 3 ngày") **chưa bật**. Phần code có rồi, nhưng chưa qua luật ghi trước. Hiện chỉ dùng qua biểu mẫu.

## Một chuyện thật: dặn model "đừng cộng tổng" không đủ

Ngày 05/11, thử để trợ lý ước chi phí chuyến đi. Cách đầu tiên: **dặn rõ trong lời dặn** "không tự cộng tổng tiền, không nhân giá theo số người, số ngày". Chạy
bộ câu kín: ở **1 trên 2 câu**, model vẫn **tự viết thêm một dòng "Tổng"** bằng phép tính của chính nó. Phép tính lần đó tình cờ khớp, nhưng luật ghi
trước cấm model tự đưa con số tổng (lần sau nó có thể tính sai mà không ai chặn). Kết quả âm.

Cách thứ hai: để **code tính tiền**. Code đúng **8 / 8** phép tính. Nhưng lại lộ một lỗi khác: ở câu về miễn vé, model **bỏ mất điều kiện** miễn vé cả 3 / 3 lần
(bản đang chạy chỉ 1 / 3). Thêm công cụ làm đổi cách model trả lời cả phần không liên quan. Bản này cũng dừng.

Bài học có hai phần, và chính là gốc của nguyên tắc ở bài 12:
1. **Dặn model không làm một phép tính thì không đủ.** Phép tính phải do code làm.
2. **Thêm công cụ cũng có giá.** Lời dặn và công cụ đổi thì cách model trả lời câu khác cũng đổi theo. Nên công cụ chỉ đưa khi code thấy đúng loại câu, và mọi
   thay đổi phải đo lại bộ an toàn.

Một chuyện nhỏ cùng tinh thần: lượt đo đầu của câu ngày, model chọn nhầm lần "năm sau" cho câu hỏi "năm nay". Sửa bằng **code** (code chọn đúng năm âm theo
"năm nay / năm sau"), không sửa bằng lời dặn.

## Khi nào hỏng

- **Dạng ngày ít gặp** ("tháng tới", "ngày kia của tuần sau"…) vẫn đi đường cũ, model tự cộng ngày.
- **Câu có ngày đúng nhưng thiếu `[n]`** thì bị rút lại (1 / 9 câu lịch ngày 10/11, bài 8).
- **Thời tiết "tuần sau"**: chỉ có số cho phần nằm trong 7 ngày (đầu tuần); cuối tuần sau vẫn chưa có dự báo. Câu "thứ hai tuần sau" nhận cả các ngày có dự báo của tuần sau, không riêng thứ Hai.
- **Biểu mẫu bản đầu:** nút "đi dày" gần như không tác dụng, vì bảng điểm còn thiếu cột thời lượng; không xét mưa. Bản 2 (bài 23) đã sửa hai chỗ này.
  Cả hai bản đều **chưa có ô giờ tới / giờ về**.
- **Lịch trình từ câu gõ tự do chưa bật.**
- **Khoảng cách:** chỉ giữa hai điểm trong bảng lịch. "Cách trung tâm bao xa", khách sạn, sân bay ⇒ chưa có số. Số phút là luật ước (6 cặp đối chiếu),
  không tính kẹt xe; không có đi bộ hay đi thuyền. Câu hỏi nhiều cặp cùng lúc: bước kiểm số không tách theo cặp nên số của cặp này dùng cho cặp kia vẫn lọt.
  Câu viết không dấu ("dai noi cach thien mu may km") không bật công cụ. "Bao lâu" có kèm từ di chuyển ở bất kỳ đâu trong câu thì bật thừa (vd "đi Huế nên ở
  bao lâu?") — vô hại: model không gọi công cụ, hoặc công cụ trả "chưa có số".

## Ba điều chính

1. **Ngày âm lịch:** code tính bằng lunar-vn theo giờ Việt Nam, chỉ năm 1976–2100. Từ 10/11, **tính sẵn trước** lần gọi model đầu, nên câu có ngày nhanh hơn
   hẳn (chữ đầu 5,60 → 2,35 s) và rẻ hơn.
2. **Thời tiết:** code lấy dự báo 7 ngày bằng toạ độ cố định, dựng sẵn số. Bão lũ và ngoài 7 ngày thì dùng **câu cố định**. **Khoảng cách:** bảng km / phút
   dựng sẵn một lần từ OSRM, model chỉ chọn mã hai nơi; từ 16/11 câu nêu rõ hai nơi thì code tra sẵn, chữ đầu 3,7 → 1,9 s. **Lịch trình:** code xếp theo buổi từ bảng anh duyệt, model chỉ viết lời, link do code dựng.
3. Chuyện thật: **dặn model "đừng cộng tổng" không đủ**, model vẫn tự viết dòng "Tổng". Phép tính phải ở code, và thêm công cụ cũng đổi hành vi câu khác.
   Và hằng số trong code (như "40 km/h") cũng phải đối chiếu nguồn trước khi dùng.

**Bài sau:** Bài 15 — Khi sổ không có: tra web một lần (có rào chắn bằng code) và hỏi bằng ảnh (gợi ý, chờ người dùng xác nhận).

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- "Tuần sau" từ 15/11: `backend/llm/thoi_tiet.py` `ngay_tuan_sau`, `ngoai_7_ngay`; đo: câu thời tiết "tuần sau" ×3 gọi công cụ 3 / 3, 0 số lạ; bộ an toàn 32 không đổi; `report_agent/2026-11-12_ra_khoang_cach/b_tuan_sau_implementation.md` [code + đã chạy 15/11]
- lunar-vn 1.4.0 (thuật toán Hồ Ngọc Đức, UTC+7), năm 1976–2100, câu cố định ngoài khoảng, không dùng lịch Trung Quốc: `backend/llm/ngay_lich.py` (đầu file, `NAM_MIN`, `NAM_MAX`, `CAU_NGOAI_KHOANG`); `pyproject.toml` [code, xem 11/11]. Ví dụ Tết 1985 (21/01 ↔ 20/02): chú thích đầu `ngay_lich.py` [code, xem 11/11]
- Lịch tính sẵn: `ngay_lich.py` `lich_san`, gọi trong `backend/llm/assistant.py` khi dò thấy từ chỉ ngày [code]
- Câu ngày nhanh (10/11, 19 câu): 5,60 → 2,35 s; 10,14 → 4,56 s; 0,00049 → 0,00036 USD; 52 → 31 lần gọi; 0 lần gọi công cụ dự phòng: `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `session_prompt/Project_Status.md` §4 [đã chạy]. T1 (09/11): bớt 9 câu từ chối nhầm, 0 sai ngày [đã chạy]
- Thời tiết: Open-Meteo, `TIMEOUT_S = 3.0`, `CACHE_S = 30 phút`, `CAU_BAO_LU`, `CAU_NGOAI_7_NGAY`: `backend/llm/thoi_tiet.py` [code, xem 11/11]
- Biểu mẫu: `assistant.py` `answer_bieu_mau`; xếp lịch, không buổi tối cho nhóm hạn chế: `backend/llm/lich_trinh.py`; cờ `lich_trinh_bieu_mau: true`, `lich_trinh: false`: `settings.yaml` [code, xem 11/11]; 24 / 24, 12 / 12 × 2, p95 4,25 s (07/11): `07_…` [đã chạy]
- B4 (dặn không cộng tổng: 1 / 2 câu kín tự ghi dòng "Tổng") và B5c (code tính tiền 8 / 8; miễn vé bỏ điều kiện 3 / 3 ↔ 1 / 3), 05/11: `07_…`, `session_prompt/Session_Prompt.md` §7 [đã chạy]
- Giới hạn "đi dày", không ô mưa / giờ tới về: `session_prompt/CURRENT_HANDOFF.md` [tài liệu]
- Khoảng cách (16/11): `backend/llm/khoang_cach.py` (`HE_SO_OSRM`, `PHUT_CONG`, `_TU_KM`, `_TU_THOI_GIAN`, `kiem_so`), `assistant.py` `khoang_cach_for_turn`; cờ `khoang_cach: true` (`6a53680`, bạn bật); bảng `data/phase_9/lich_trinh/khoang_cach_v1.json` md5 `cb76ab72199c` (private) [code]. Đếm trước 4 / 6 từ chối; đo 16 câu: 13 / 14 đúng cặp, 0 số sai, 0 / 2 ngoài bảng ra số, ≈ 0,00081 USD / câu, chữ đầu p50 3,7 s / p95 ≈ 6,2 s (nội suy; 14 câu có công cụ, lượt sau sửa — 17 dòng `chat_metrics` cuối của `data/khoang_cach_2026-11-16/application_8041_r2.log`, private); bộ dò 27 câu 0 bỏ sót; an toàn 32 chạm 0: `report_agent/2026-11-12_ra_khoang_cach/c_khoang_cach_implementation.md` [đã chạy 16/11]. Review bắt sàn 40 km/h (1.082 / 1.560 cặp): `data/review_khoang_cach_2026-11-16/review.md`; đối chiếu 6 cặp 3 / 6 ⇒ 6 / 6: report trên, mục "Sửa theo review" M1; nguồn công khai: `data/tra_cuu_cli/2026-11-16_quang-duong-hue/` (private) [đã chạy]. Tiền câu từ chối + web ≈ 0,0023 (trung bình 4 câu): lượt đếm trước [đã chạy]. Đối chiếu bài: `data/khoang_cach_2026-11-16/doi_chieu_bai_hoc.md` (agent con, 70 khẳng định, sửa 12 chỗ).
- Ghi chú kẹt xe do code nối (16/11 tối): `backend/llm/assistant.py` `set_notice`; [đã chạy] đếm 33 / 52 từ 4 file kết quả lượt đo (`data/khoang_cach_2026-11-16/`), 4 câu thật trên bản `bc785ae` (3 có dòng lưu ý, 1 không lặp); review B 12 ca phá; `c_kc_tinh_san_implementation.md` mục 3d.
- Khoảng cách tính sẵn (16/11): `backend/llm/khoang_cach.py` (`tim_hai_diem`, `cap_tinh_san`, `TEN_NGAN`), `assistant.py` `_nguon_khoang_cach_san`; cờ `khoang_cach_tinh_san: true` (`3ccdada`, bạn bật tối 16/11); [đã chạy] bộ dò 32 câu 29 / 0 / 3 và 21 câu phá của review 20 / 0 / 1 (bản đầu 31 / 0 / 1 và 15 / 21 sai), lượt đo 16 câu trên bản cuối `1e45a78` (13 đường nhanh, chữ đầu trung vị 1,87 s đo ở phía gọi, 0,0122 USD cả lượt; lượt trên bản đầu `50fbf4e`: 1,80 s, 0,0131 USD); `report_agent/2026-11-12_ra_khoang_cach/c_kc_tinh_san_implementation.md`.
- Các câu ví dụ là câu tự đặt.
- **Sửa 14:03 11/11/2026:** (1) bản trước ghi code tính sẵn cả "ngày kia" — sai: "ngày kia" chỉ được dò thấy, rồi model vẫn gọi công cụ (`lich_san`, chú thích đầu hàm); (2) bản trước ghi dòng "Tổng" có "con số không đúng" — sai: phép nhân khớp luật kho, bị tính là lỗi vì luật đo cấm con số tổng (`07_…` mục B4 vòng 1).

</details>
