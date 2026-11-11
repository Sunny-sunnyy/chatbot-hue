# Bài 14 — Việc dễ nhầm thì code làm: ngày âm lịch, thời tiết, lịch trình

*Cập nhật lần cuối: 14:04, ngày 11/11/2026 · sửa hai câu sai (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Công cụ ngày — **mới** | **`ngay_lich`** (thư viện **lunar-vn** 1.4.0) | Code tính hôm nay, đổi ngày dương ↔ âm theo lịch Việt Nam. |
| Lịch tính sẵn — **mới** | **`lich_san`** → nguồn **"Lịch hệ thống"** | Khi câu có từ chỉ ngày, code tính sẵn các ngày liên quan và đưa vào ngữ cảnh **trước** lần gọi model đầu. |
| Công cụ thời tiết — **mới** | **`thoi_tiet`** (dịch vụ **Open-Meteo**) | Code lấy dự báo 7 ngày cho Huế, dựng sẵn các con số. |
| Biểu mẫu lên kế hoạch — **mới** | **`lich_trinh_bieu_mau`** + **`lich_trinh`** | Người dùng chọn số ngày, người đi cùng, sở thích bằng nút; code xếp lịch theo buổi; model chỉ viết lời. |
| Câu cố định | ví dụ **`CAU_BAO_LU`**, **`CAU_NGOAI_7_NGAY`** | Câu viết sẵn trong code cho trường hợp đặc biệt; model không được tự viết. |

---

*Bài 12 nêu nguyên tắc chia việc: phép tính, luật, thứ tự bắt buộc thì code làm; model chỉ chọn và diễn đạt. Bài này kể ba chỗ áp nguyên tắc đó rõ nhất:
ngày tháng, thời tiết, và lịch trình.*

## Quay lại người hướng dẫn viên

Khách hỏi: *"Rằm tháng Giêng năm nay là thứ mấy?"* Một người hướng dẫn viên cẩn thận **không nhẩm**. Nhẩm ngày âm lịch rất dễ sai một ngày, và sai một ngày
thì khách lỡ cả lễ hội. Họ **mở cuốn lịch ra xem**. Khách hỏi *"mai Huế mưa không?"*, họ **mở dự báo** ra đọc, không đoán theo mùa.

Khách nhờ *"lên giúp lịch đi Huế 2 ngày, đi cùng ba mẹ"*, họ cũng không ứng khẩu. Họ có sẵn **một bảng các điểm** ghi điểm nào hợp buổi sáng, buổi chiều hay
buổi tối, có hợp người lớn tuổi không. Họ xếp theo bảng đó, rồi mới **kể lại bằng lời** cho khách.

Trong cả ba trường hợp, phần **con số và thứ tự** đến từ dụng cụ (lịch, dự báo, bảng điểm). Phần người làm là **chọn dụng cụ** và **nói cho dễ nghe**.

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
- Câu về **bão, lũ, ngập** ⇒ câu cố định trỏ tới Trung tâm Dự báo khí tượng thủy văn quốc gia, cổng cảnh báo lũ quét, và **gọi 112** khi nguy hiểm. Model không
  được tự viết về thiên tai.
- Công cụ thời tiết **chỉ được đưa** khi câu có từ khoá thời tiết (bài 12).

Trang chủ của cổng du lịch cũng có một ô thời tiết đọc thẳng từ đây, không gọi model.

## Biểu mẫu "Lên kế hoạch"

Người dùng điền biểu mẫu bằng nút: **số ngày**, **đi cùng ai** (một mình, bạn bè, gia đình có trẻ em, người lớn tuổi…), **sở thích**. Rồi:
1. Lượt này **không qua bước xếp loại**. Code gọi thẳng phần xếp lịch với **đúng giá trị các nút**.
2. **Code xếp lịch theo buổi** (sáng, chiều, tối) từ **một bảng điểm anh đã duyệt**. Bảng ghi điểm nào hợp buổi nào, hợp ai, có trong nhà không. Buổi sáng ưu
   tiên điểm hợp sở thích. Nhóm có trẻ em hoặc người lớn tuổi thì **không xếp buổi tối**, và dòng buổi tối ghi rõ lý do để trống.
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
- **Thời tiết "tuần sau"** không có số dự báo (ngoài 7 ngày), chỉ có câu cố định.
- **Biểu mẫu:** nút "đi dày" gần như không tác dụng, vì bảng điểm còn thiếu cột thời lượng (chờ anh duyệt bảng mới). Không có ô "lo trời mưa", không có ô giờ
  tới / giờ về.
- **Lịch trình từ câu gõ tự do chưa bật.**

## Ba điều chính

1. **Ngày âm lịch:** code tính bằng lunar-vn theo giờ Việt Nam, chỉ năm 1976–2100. Từ 10/11, **tính sẵn trước** lần gọi model đầu, nên câu có ngày nhanh hơn
   hẳn (chữ đầu 5,60 → 2,35 s) và rẻ hơn.
2. **Thời tiết:** code lấy dự báo 7 ngày bằng toạ độ cố định, dựng sẵn số. Bão lũ và ngoài 7 ngày thì dùng **câu cố định**. **Lịch trình:** code xếp theo buổi
   từ bảng anh duyệt, model chỉ viết lời, link do code dựng.
3. Chuyện thật: **dặn model "đừng cộng tổng" không đủ**, model vẫn tự viết dòng "Tổng". Phép tính phải ở code, và thêm công cụ cũng đổi hành vi câu khác.

**Bài sau:** Bài 15 — Khi sổ không có: tra web một lần (có rào chắn bằng code) và hỏi bằng ảnh (gợi ý, chờ người dùng xác nhận).

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- lunar-vn 1.4.0 (thuật toán Hồ Ngọc Đức, UTC+7), năm 1976–2100, câu cố định ngoài khoảng, không dùng lịch Trung Quốc: `backend/llm/ngay_lich.py` (đầu file, `NAM_MIN`, `NAM_MAX`, `CAU_NGOAI_KHOANG`); `pyproject.toml` [code, xem 11/11]. Ví dụ Tết 1985 (21/01 ↔ 20/02): chú thích đầu `ngay_lich.py` [code, xem 11/11]
- Lịch tính sẵn: `ngay_lich.py` `lich_san`, gọi trong `backend/llm/assistant.py` khi dò thấy từ chỉ ngày [code]
- Câu ngày nhanh (10/11, 19 câu): 5,60 → 2,35 s; 10,14 → 4,56 s; 0,00049 → 0,00036 USD; 52 → 31 lần gọi; 0 lần gọi công cụ dự phòng: `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `session_prompt/Project_Status.md` §4 [đã chạy]. T1 (09/11): bớt 9 câu từ chối nhầm, 0 sai ngày [đã chạy]
- Thời tiết: Open-Meteo, `TIMEOUT_S = 3.0`, `CACHE_S = 30 phút`, `CAU_BAO_LU`, `CAU_NGOAI_7_NGAY`: `backend/llm/thoi_tiet.py` [code, xem 11/11]
- Biểu mẫu: `assistant.py` `answer_bieu_mau`; xếp lịch, không buổi tối cho nhóm hạn chế: `backend/llm/lich_trinh.py`; cờ `lich_trinh_bieu_mau: true`, `lich_trinh: false`: `settings.yaml` [code, xem 11/11]; 24 / 24, 12 / 12 × 2, p95 4,25 s (07/11): `07_…` [đã chạy]
- B4 (dặn không cộng tổng: 1 / 2 câu kín tự ghi dòng "Tổng") và B5c (code tính tiền 8 / 8; miễn vé bỏ điều kiện 3 / 3 ↔ 1 / 3), 05/11: `07_…`, `session_prompt/Session_Prompt.md` §7 [đã chạy]
- Giới hạn "đi dày", không ô mưa / giờ tới về: `session_prompt/CURRENT_HANDOFF.md` [tài liệu]
- Các câu ví dụ là câu tự đặt.
- **Sửa 14:03 11/11/2026:** (1) bản trước ghi code tính sẵn cả "ngày kia" — sai: "ngày kia" chỉ được dò thấy, rồi model vẫn gọi công cụ (`lich_san`, chú thích đầu hàm); (2) bản trước ghi dòng "Tổng" có "con số không đúng" — sai: phép nhân khớp luật kho, bị tính là lỗi vì luật đo cấm con số tổng (`07_…` mục B4 vòng 1).

</details>
