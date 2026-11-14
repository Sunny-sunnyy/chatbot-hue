# Bài 25 — Trợ lý làm việc thật: sửa lịch bằng lời, câu hỏi nhiều ý, chỗ ở, quán ăn, ảnh dưới câu trả lời

*Cập nhật lần cuối: 18:50, ngày 14/11/2026 · thêm tối 14/11: chọn khách sạn theo hạng cao trước + ảnh khách sạn, ảnh quán ở thẻ bữa, bỏ quán đã đóng, năm trong câu hỏi không làm mất mục web. Trước: 17:13, ngày 14/11/2026 · nối tiếp bài 23 và 15. Thêm chiều 14/11: quán ăn trong lịch, khu ở theo buổi tối, lịch mẫu đủ đi – ăn – ở, so tiền mục web theo giá trị, hai lần thử / đếm rồi không làm. Số ảnh 184 / 216, 38 ảnh "không chắc".*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Lần hiểu ý sửa | `sua_lich_v2` (một lần gọi model, đầu ra có khuôn) | Model đọc câu "bỏ chợ Đông Ba đi" rồi trả về **hành động có tên** (bỏ / thêm / thay…). Code mới là bên áp. |
| Vế hỏi — **mới** | `so_y` (đếm vế) | Một phần của câu có từ hỏi riêng ("mấy giờ", "ở đâu", "… không?"). Câu hai vế = hỏi hai việc. |
| Dòng ý thiếu | `CAU_Y_THIEU` ("Tư liệu chưa có thông tin về: …") | Dòng trợ lý viết cho phần kho không có, thay vì từ chối cả câu. |
| Đạt cả hai lần — **mới** | **pass^2** | Một chuỗi câu chỉ tính là đạt khi chạy hai lần đều đúng. Model mỗi lần trả lời hơi khác, nên đạt một lần chưa đủ. |
| Bộ nhớ đệm lời nhắc — **mới** | **prompt cache** (`prompt_cache_key`) | Phần đầu giống hệt nhau của các lần gọi được nhà cung cấp nhớ lại, tính rẻ hơn. |
| Cờ | flag trong `settings.yaml` | Công tắc bật / tắt từng tính năng, không cần sửa code. |
| Mô phỏng toàn tổ hợp | 3.840 khung (mọi tổ hợp biểu mẫu) | Chạy bộ xếp lịch trên mọi cách điền biểu mẫu rồi đếm bằng code, 0 USD. |
| Bản đồ mở — **mới** | **OpenStreetMap (OSM)** | Bản đồ do cộng đồng tự đóng góp; có tên và toạ độ quán, nhưng mình chưa kiểm và dữ liệu không ghi ngày kiểm, nên gắn nhãn "chưa kiểm". |

---

*Bài 23 kể lịch "Lên kế hoạch" bản 2: code xếp, model chỉ viết câu tả. Bài 15 kể chuyện tra web khi sổ không có. Bài này kể các việc xong chiều 14/11,
đều theo hướng anh chọn: **trợ lý làm được việc**, không chỉ trả lời một câu. Tất cả giữ một nguyên tắc từ bài 14: **việc dễ nhầm thì code làm**, model
chỉ đọc hiểu và diễn đạt.*

## Quay lại người hướng dẫn viên

Khách nói "bỏ chợ tối nay đi, mình mệt rồi". Một người hướng dẫn viên tốt không vẽ lại cả lịch từ đầu. Họ gạch đúng một dòng, giữ nguyên những chỗ khác,
và nói rõ đã đổi gì. Khách hỏi một câu gồm hai việc, trong đó sổ tay chỉ có một: người giỏi trả lời phần biết, nói thẳng phần chưa biết, chứ không từ
chối cả câu. Khách đi ba ngày thì cần biết nên ở khu nào. Và khi kể về một nơi, đưa khách xem một tấm ảnh thì dễ hình dung hơn mười câu tả.

Các việc dưới đây dạy trợ lý làm đúng những thói quen đó, cộng thêm việc gợi ý chỗ ăn trên đường đi.

## 1. Sửa lịch bằng lời

**Bước này nằm ở đâu.** Vẫn là giai đoạn trả lời của RAG, nhưng chia làm hai nửa:
- **Model hiểu ý:** đọc câu người dùng cùng lịch hiện tại, trả về một danh sách hành động có tên. Có 6 loại: bỏ, thêm, thay, dời buổi, đổi số ngày, đổi
  tham số (kiểu đi, sở thích, có trẻ em / người lớn tuổi).
- **Code áp:** mỗi hành động là một lần chạy lại **đúng bộ xếp của bài 23**, giữ nguyên chỗ của mọi điểm không bị chạm. Khung mới chỉ được nhận khi qua đủ
  phần kiểm của bộ xếp; không qua thì giữ khung cũ và nói lý do.
- Đầu thẻ lịch có khối "Đã đổi / Không đổi được" do code viết. Điểm không đổi thì giữ câu tả cũ, chỉ điểm mới mới gọi model viết câu.

**Vì sao model không tự viết lại lịch.** Nếu để model sửa thẳng chữ của lịch, nó có thể đổi luôn giờ, thêm điểm đóng cửa, hoặc lặng lẽ bỏ cảnh báo. Để
model chỉ đọc ý thì phần dễ sai (giờ mở cửa, mùa, cụm gần) vẫn do đúng một bộ xếp tính, như mọi lịch khác.

**Đo thế nào.**

| Đo gì | Cách đo | Kết quả | Vì sao ổn |
|---|---|---|---|
| Code áp có phạm luật không | mô phỏng mọi tổ hợp lịch × 8 kiểu thử (6 loại hành động, có loại thử hai biến thể), ~15.000 lần áp, 0 USD | **0 vi phạm**. Lần đầu bắt **2 lỗi thật**: điểm đã bỏ quay lại qua danh sách lấp chỗ (240 khung); "thêm" gần như luôn trượt (4 / 1.920). Cả hai đã sửa | lỗi luật chỉ lộ khi chạy đủ tổ hợp, như bài 23 |
| Hiểu ý đúng không | 10 chuỗi câu sửa đã thấy + 5 chuỗi kín (người khác viết), tính "đạt cả hai lần" | đã thấy **7 / 10** ⇒ sau **một** vòng chỉnh lời dặn **9 / 10** (sàn 8 / 10); kín **4 / 5** (sàn 4 / 5) | bộ kín không ai chỉnh theo, nên chống được "học thuộc đề" |
| Câu thường có bị nhầm thành câu sửa không | bộ an toàn 32 câu × 2, hỏi trong một cuộc đã có lịch | **0 / 64** thành lượt sửa | câu an toàn đi đúng đường cũ |
| Câu vừa sửa lịch vừa khẩn cấp | 8 câu trộn do người khác viết, × 2 | **0 / 16** thành lượt sửa (sau khi sửa một lỗi chặn người review tìm ra, kể ở dưới) | câu khẩn cấp không bị biến thành lượt sửa |

Người review tìm ra một **lỗi chặn**: câu kiểu "bỏ điểm chiều nay, mình vừa bị ngã đau chân" bị biến thành lượt sửa lịch, mất phần khẩn cấp. Lý do: lần
hiểu ý chạy **trước** bộ định tuyến, mà bộ định tuyến là nơi duy nhất nhận ra câu khẩn cấp. Sửa: cho hai lần gọi chạy **song song**; định tuyến báo khẩn
cấp thì đi đường khẩn cấp như cũ. Mình không bắt model tự khai "khẩn cấp", vì luật an toàn nên nằm ở chỗ đã được đo.
Lưu ý: 0 / 16 chỉ đo là câu không bị biến thành lượt sửa. Câu trả lời khẩn cấp vẫn chưa có số 112–115, đây là giới hạn anh đã
nhận từ 12/11.

**Tiền.** Đo đúng sai ≈ 0,25 USD (cao hơn ước 0,07 vì mỗi chuỗi phải xếp cả lịch trước). Mỗi câu trong cuộc có lịch tốn thêm một lần hiểu ý: phần lời
dặn ~1.244 token giống hệt nhau mọi lượt, nên mình gắn một khoá đệm cố định ⇒ lần hiểu ý từ 0,00024 xuống ≈ 0,00007–0,0001 USD (người review đo trên log thật 6 lần: 0,00007).

## 2. Câu hỏi nhiều ý

**Vấn đề.** Luật trả lời cũ (bài 8) rất chặt: thiếu căn cứ cho **một** ý ⇒ từ chối **cả** câu. Hỏi "vé Đại Nội bao nhiêu, dịp Tết có chương trình gì",
kho chỉ có giá vé ⇒ khách không nhận được cả giá vé. Đo ngày 14/11 trên 10 câu hỏi kèm kiểu này: phần kho có chỉ được trả lời **4 / 10**.

**Vòng 1 — đổi lời dặn: trượt.** Lời dặn mới cho trả lời theo từng ý, ý thiếu thì viết dòng "Tư liệu chưa có thông tin về: …".
- Hỏi kèm lên **10 / 10**, 0 câu bịa.
- Nhưng trên bộ 176 câu mẫu: **3 / 18 câu ngoài kho bị trả lời** (sàn 0) và **2 lỗi trích dẫn** mới.
- Lý do: nới luật từ chối thì câu ngoài kho tìm được một lời khuyên chung chung để nói. Sàn cứng trượt ⇒ không bật.

**Vòng 2 — để code quyết:**
- (a) Câu trả lời mà **mọi** dòng đều là dòng ý thiếu ⇒ code đổi thành đúng câu từ chối chuẩn.
- (b) Luật theo ý **chỉ chạy khi code đếm được ≥ 2 vế hỏi**. Câu một ý giữ nguyên luật cũ, nên phần lớn câu hỏi đi đúng con đường đã đo từ trước.

Kết quả vòng 2:
- Hỏi kèm **10 / 10**.
- Bộ kín 10 câu ngoài kho: **0 / 10** bị trả lời.
- Bộ 176 câu: còn **1 / 18** câu ngoài kho bị trả lời. Nhưng câu đó **không đi vào luật mới**: yêu cầu gửi model giống hệt khi tắt cờ, nên chênh chỉ do model
  lấy mẫu. Cả bộ 176 có **0 câu** đi vào luật mới.
- Anh chọn bật.

**Sửa nhỏ sau khi bật.** Người điều phối thử câu "Đại Nội mở cửa mấy giờ **và** gần đó có quán karaoke nào giá rẻ không?" ⇒ bị từ chối cả câu.
- Lý do: code chỉ tách vế ở dấu phẩy / chấm phẩy / dấu hỏi, nên câu nối bằng "và" bị đếm là 1 vế.
- Sửa: tách thêm ở "và / còn / với", nhưng chỉ tính là vế khi **chính phần đó** có từ hỏi. Nhờ vậy "bún bò và bánh khoái giá bao nhiêu" vẫn là một câu hỏi.
- Đếm trước khi đo: 0 câu trong bộ 176, bộ an toàn 32 và 10 câu hỏi kèm đổi số vế ⇒ không cần chạy lại ba bộ đó.
- Đo 5 câu đổi số vế × 2 lượt: luật chạy **10 / 10**, **0** câu bị từ chối cả câu, 0 lần ý ngoài kho được trả lời bằng kho.

**Sửa tiếp: mục web chỉ viết cho ý thiếu.** Với câu "một ý kho có + một ý không có", mục "Từ web (chưa kiểm)" của bài 15 lại viết luôn cả ý kho đã trả
lời. Có lần kho ghi Đại Nội mở cửa 7:00, ngay bên dưới web ghi 6:30.
- Đo trên các lượt có mục web: lỗi này xảy ra ở **4 / 4** lượt.
- Sửa: code chọn đúng vế ứng với dòng ý thiếu, rồi dặn model "chỉ viết cho phần này".
- Đo lại: **0 / 11** mục web còn nhắc lại ý kho.
- Câu gửi Serper vẫn là cả câu như trước. Vế tách riêng có thể mất tên nơi ("gần đó có quán karaoke nào…"), nên tìm kém hơn.

**Tiền cả việc** ≈ 0,40 USD: vòng 1 + vòng 2 ≈ 0,35, sửa "và" ≈ 0,015, mục web ≈ 0,035.

## 3. Chỗ ở trong lịch

Lịch từ 2 ngày có thêm thẻ **"Nơi ở gợi ý"** ở cuối: một khu cho cả chuyến, một câu lý do, và 3–5 khách sạn trải từ cao tới bình dân. Mỗi khách sạn có
nút "Tìm phòng" mở trang tìm kiếm của Booking. Thẻ **không có giá, không báo còn phòng**, và ghi rõ "chưa kiểm giá, phòng trống" cùng nguồn danh mục.

**Mọi thứ do code chọn**, model không chọn khách sạn nào:
- **Chọn khu.** Lịch có hoạt động buổi tối, và mọi điểm buổi tối đều ở trung tâm ⇒ ở **trung tâm**, vì tối nào khách cũng về đó (luật thêm cuối chiều
  14/11, xem chuyện thật thứ hai). Lịch không có buổi tối, hoặc có điểm tối ngoài trung tâm, thì đếm các điểm tham quan ban ngày theo khu; mặc định vẫn là trung tâm hai bờ sông Hương:
  - phía tây (Kim Long, Thủy Xuân) chỉ khi hơn một nửa số điểm ở đó **và** đoàn không có trẻ em / người lớn tuổi;
  - ven biển chỉ khi ≥ 60 % số điểm ở ven biển.
- **Chọn khách sạn** trong khu: tối đa 2 cơ sở 4–5 sao, 2 cơ sở 2–3 sao, 1 cơ sở 1 sao hoặc đạt chuẩn. Danh mục có 140 cơ sở: 139 từ danh mục công khai
  của Cục Du lịch Quốc gia, 1 từ tin ngành du lịch thành phố; mỗi cơ sở có hạng và khu.

**Đo:**
- **Mô phỏng 3.840 khung lịch** (0 USD): lịch 1 ngày không có thẻ; lịch ≥ 2 ngày có thẻ 3.072 / 3.072; mọi khách sạn có trong danh mục và đúng khu; khu
  đúng luật; 0 link lạ.
- **Người xem độc lập** (một agent mới mở, chỉ đọc 10 lịch kèm gợi ý) chấm "khu ở có hợp lý không":
  - Lượt 1 ra **9 / 10** (sàn ≥ 9 / 10, đã đạt), nhưng chỉ ra **2 lỗi thật**:
    - Bạch Mã / Nhị Hồ (đi trong ngày) bị tính là "ven biển", nên một lịch bị gợi ý ở biển sai;
    - khu ven biển gộp cả Thuận An lẫn Lăng Cô, cách nhau ~40 km.
  - Mình sửa cả hai: không đếm cụm đi trong ngày; khách sạn ven biển chỉ chọn cùng phía với các điểm của lịch.
  - Lượt 2 trên cùng 10 lịch, một người xem mới khác: **10 / 10**.
- Trình duyệt thật ở hai khổ màn hình: thẻ hiện đủ, link mở tab mới, 0 lỗi.

Tiền ≈ 0,0025 USD (4 lượt xếp lịch thật cho trình duyệt).

**Sửa tối 14/11 — khách sạn 5 sao chưa từng được gợi ý.** Đếm lại trên 3.840 khung: trong cùng một mức (ví dụ cao cấp), code xếp theo **tên** theo thứ tự chữ cái, nên
luôn ra hai khách sạn 4 sao có tên đứng đầu bảng chữ cái. Kết quả: trong **6.108 lần chọn khách sạn ở mức cao cấp, 0 lần ra 5 sao**, 3 sao 0 lần, 72 % lịch nhận cùng một bộ 5. Lỗi này không ai thấy khi
nhìn từng lịch, chỉ lộ khi đếm. Sửa: trong mỗi mức lấy **hạng cao trước** (một 5 sao rồi một 4 sao; một 3 sao rồi một 2 sao; 1 sao trước "đạt chuẩn"), cùng hạng
thì gần cụm có nhiều điểm nhất của lịch trước, rồi có ảnh trước, rồi theo tên. Sau sửa: lịch ở khu trung tâm **3.036 / 3.036** có cả một khách sạn 5 sao và một khách sạn 3 sao.

**Ảnh và bản đồ cho khách sạn.** Mỗi khách sạn trên thẻ có link "Bản đồ" (tìm theo tên + địa chỉ) bên cạnh "Tìm phòng", và một ảnh nhỏ nếu có ảnh chắc.
- Ảnh: một agent con chọn trong 5 ảnh tìm được của từng cơ sở, rồi người làm nhìn lại mọi ảnh nhận (bác 2: một ảnh vẽ phối cảnh, một biển có số điện thoại).
  **66 / 140** cơ sở có ảnh chắc; ảnh "vừa" không dùng, vì ảnh sai cạnh tên khách sạn dễ làm khách tưởng đúng nơi. Tính theo lần hiện thì **97,6 %** ô khách sạn
  hiện ra có ảnh — các cơ sở hay được gợi ý gần như đều có ảnh.
- Toạ độ: tra 140 cơ sở, chỉ nhận khi tên, loại hình lưu trú, số chi nhánh và tên đường đều khớp ⇒ **82 / 140** (mức đặt trước là 100 — trượt). Luật nhận phải siết
  sau khi soát tay thấy nhận nhầm một nhà hàng cùng tên và lẫn chi nhánh "2" với cơ sở gốc; sai toạ độ còn tệ hơn giữ toạ độ ước (~1 km).
- Tiền ≈ 0,28 USD (tra toạ độ + tìm ảnh). Giới hạn: chỉ khoảng 12 / 140 cơ sở từng hiện trong lịch, nên phần lớn ảnh khách sạn chưa có chỗ hiện.

## 4. Quán ăn trong lịch

Mỗi ngày của lịch có tối đa hai dòng **"Ăn trưa gần …"** và **"Ăn tối gần …"**, mỗi dòng 1–2 quán. Quán có bài trong kho thì bấm mở bài; quán lấy từ bản
đồ mở thì có nhãn **"từ bản đồ mở, chưa kiểm"** và link bản đồ. Không có giờ, giá hay điện thoại, vì các nguồn này không ghi ngày kiểm.

**Đếm trước khi xây.** Câu hỏi đầu tiên: có đủ quán để gợi ý không? Mô phỏng 3.840 khung lịch cho **22.680 bữa**; mức đạt ghi trước là ≥ 50 % số bữa có ít
nhất 2 quán cùng cụm.
- Bản đếm đầu ghi quán kho phủ **74,7 %** và cộng bản đồ mở thì **95,2 %**. Người đếm tự bắt lỗi: file quán "kho" thật ra trộn ba nguồn, chỉ **28** quán
  là quán kho.
- Đếm lại: chỉ quán kho **33,5 %** (dưới mức), quán kho cộng bản đồ mở **74,7 %** (đạt). Vì vậy mới xây, và dùng cả bản đồ mở có nhãn.

**Code chọn quán** theo luật: cùng cụm với điểm, **trong vòng 2 km**, quán kho trước, quán ăn trước cà phê, gần trước, không lặp quán trong cả chuyến.
Ba luật này đều do lượt đo bắt:
- **Trần 2 km:** mô phỏng đầu có 5 % số dòng "ăn gần X" mà quán cách xa hơn 9,3 km (cụm rộng như phá, biển, lăng xa), nghe như sai nghĩa.
- **Bữa tối gần điểm buổi tối:** trình duyệt lần đầu hiện "ăn tối gần Đầm Chuồn" trong khi tối hôm đó khách ở chợ Đông Ba.
- **Tên có chữ cà phê thì là cà phê:** người xem bắt 2 tiệm cà phê bị ghi "quán ăn".

**Đo** (0 USD, trừ ≈ 0,0013 USD cho 2 lượt xếp lịch thật): 80,7 % số bữa có dòng; quán cách điểm trung vị 0,78 km, xa nhất 1,99 km; 0 quán ngoài bảng, 0 khác
cụm, 0 lặp. Người xem độc lập 10 lịch (8 lịch có buổi ở Thủy Xuân / Kim Long): **10 / 10** đạt cả ba câu (hợp chỗ, nhãn đúng nguồn, không số lạ).

**Chỗ yếu, nói thẳng (lúc chiều):** quán kho chỉ có ở ba cụm trung tâm. Ở Thủy Xuân, Kim Long gần như chỉ có quán bản đồ mở, tên hay viết không dấu hoặc chung chung,
khách có ít lý do để chọn (tối 14/11 đã bổ sung, xem dưới). Phá Tam Giang, biển Thuận An, Bạch Mã không có dòng ăn (xa quán quá 2 km hoặc không có quán).

**Tối 14/11:** tám bài quán mới vào kho (bài 22; bảy quán có vị trí vào lịch) đưa bữa có quán kho **49,3 ⇒ 69,1 %** — Thủy Xuân 62,6 %, Kim Long 57,2 %, biển / đầm
phá 48,5 %, vùng xa phía nam vẫn 0. Thẻ bữa có thêm **ảnh quán**: quán kho dùng ảnh Khám phá (ảnh "không chắc"
thì không hiện); quán bản đồ mở chỉ tìm ảnh cho đúng **15 quán từng hiện** trong 3.840 lịch (khoảng 400 quán còn lại chưa bao giờ được chọn), được 5 ảnh chắc. Cũng
nhờ đếm "quán nào thật sự hiện", người làm thấy một quán chay **đã đóng cửa** vẫn được gợi ý ở **324 / 3.840** lịch (kho đã loại quán này, nhưng bảng bản đồ mở
vẫn còn tên) ⇒ bỏ khỏi bảng.

## 5. Lịch mẫu "Ví dụ" đủ đi – ăn – ở

Trang Lên kế hoạch lúc chưa xếp có một lịch mẫu 2 ngày (bài 23). Khi bật chỗ ở và quán ăn, lịch mẫu vẫn chỉ có điểm tham quan, vì nó không đi qua bước gắn
hai khối đó. Mình tách bước gắn chỗ ở + quán của lịch thật thành **một hàm dùng chung**, rồi cho lịch mẫu gọi đúng hàm đó; vẫn không gọi model.

Người review góp hai ý, cả hai đã làm:
- lịch mẫu là thứ khách thấy đầu tiên, nên **chỉ hiện quán có bài trong kho** (không hiện tên bản đồ mở). Còn 3 bữa; bữa trưa gần lăng Tự Đức không có quán
  kho trong 2 km nên bỏ, không đoán;
- lịch mẫu bị gợi ý **ở khu phía tây** dù cả hai tối đều ở trung tâm ⇒ đó là lỗi của luật chọn khu, sửa ở luật (chuyện thật thứ hai).

Lịch mẫu bây giờ: khu ở trung tâm hai bờ sông Hương, 5 khách sạn, 3 bữa có quán kho.

## 6. Mục "Từ web": so số tiền theo giá trị

Mục web có luật bằng code: **mọi số tiền trong mục phải có trong đoạn trích web** (bài 15). Đếm trên 76 mục web đã lưu (0 USD), luật này chặn **16** mục, phần
lớn vì cách viết: trang web ghi "100.000 VNĐ", model chép "100.000 đồng"; "65.000đ" với "65.000 đồng"; "594,000" với "594.000". Code cũ so **nguyên chuỗi**
nên coi là khác nhau và thay cả mục bằng câu "chưa tra được tin đáng tin".

Sửa: đổi số tiền ra **giá trị bằng đồng** rồi mới so; luật không nới. Cách viết mơ hồ thì không đoán, vẫn so nguyên chuỗi như cũ (ví dụ "1.500 triệu" là
1,5 tỷ hay 1.500 triệu?). Người review thử thêm và bắt ba chỗ, sửa hai: "2 triệu rưỡi" từng bị đọc thành 2 triệu (nay là 2.500.000); "150K" chữ hoa từng
không được nhận là tiền. Chỗ thứ ba giữ nguyên, ghi ở "Khi nào hỏng".

**Đo:** mục web được hiện **43 ⇒ 51 / 76**. Một số bịa thật (220.000 đồng, đoạn trích chỉ có 160, 170, 200, 250 nghìn) vẫn bị chặn **4 / 4** lần. 8 mục mới
được hiện: người làm và người review đều kiểm từng số tiền, tất cả có trong đoạn trích.

**Tối 14/11 — năm trong câu hỏi.** Đếm lại 76 mục: vẫn **21** mục bị thay câu cố định, và 16 mục trong đó là chặn nhầm. Người dùng hỏi kiểu tháng 12/2026 có
chương trình gì, model viết "chưa xác minh được … năm 2026", mà luật số (mọi con số phải có trong đoạn trích) không xét câu hỏi. Bản sửa đầu cho qua **mọi** số có
trong câu hỏi; người review bắt: như vậy giờ hay ngày người dùng gõ sai cũng được nhắc lại như sự thật, trong khi cả 11 mục được cứu chỉ nhờ **số năm**. Bản sửa
cuối chỉ cho qua **năm** (dạng 19xx / 20xx đứng riêng); giờ, ngày, số nhà, tiền vẫn phải có trong đoạn trích. Bị thay **21 ⇒ 10 / 76** (mục web được hiện 51 ⇒ 62 / 76). Trong 10 mục còn bị thay: 5 chặn đúng, 1 lỗi khác, 4 mục
bị chặn vì model tóm "01/5/2026" thành "tháng 5/2026" — chặn về phía an toàn. 0 USD. (Ví dụ câu hỏi ở trên là mình tự đặt.)

## 7. Thử rồi bỏ, đếm rồi không làm

- **Cho lần viết mục web "nghĩ ít" (mức suy luận low).** Mục tiêu là nhanh hơn; mức đạt ghi trước là nhanh hơn ≥ 1,5 s. Đo 76 lần gọi, xen kẽ hai bản:
  nhanh hơn **0,87 s** (2,95 ⇒ 2,08 s trung vị), chất lượng không tụt, tiền lần viết giảm 32 %. **Trượt mức nhanh ⇒ bỏ**, không đo tiếp phần chấm tay.
  Mức 1,5 s đặt theo số đếm từ log (4,94 s mỗi lần viết), cao hơn hẳn số đo lần này; lý do chưa chứng minh (có thể lúc đó máy chạy nhiều lượt đo cùng lúc).
  Lượt đo này lại là nơi phát hiện lỗi so tiền ở mục 6.
- **Đổi cách tìm web cho dòng ý thiếu.** Hiện mục web có thông tin dùng được ở **3 / 16** lượt. Cách tìm tốt nhất mình thử được cho **6 / 16**, chỉ vừa chạm mức
  ghi trước, mà lại phải gửi chữ do model viết ra ngoài (luật hiện tại chỉ gửi chữ người dùng). Mức "bỏ hẳn tra web" là dưới 3 / 16, cũng không chạm. ⇒ **Giữ
  nguyên**, không xây. Tốn 0,016 USD cho 16 lượt tìm.

## 8. Ảnh dưới câu trả lời

Hỏi trợ lý về một nơi hay một món, câu trả lời giờ có **một ảnh** ở dưới. Bấm vào ảnh thì mở bài trong Khám phá. Ảnh lấy từ bộ ảnh đã có của Khám phá
(nay 249 / 263 bài có ảnh, bài 24).

**Code quyết có hiện ảnh không,** model không chọn ảnh. Chỉ hiện khi đủ các điều kiện:
- trợ lý trả lời bằng kho, không phải câu từ chối, không có mục web, không phải lịch;
- **mọi nguồn được trích thuộc đúng một bài**, và bài đó nói về một thứ cụ thể (một nơi, một món, một lễ hội hay một loại hình nghệ thuật), không phải
  bài tổng quan;
- ảnh không thuộc nhóm ảnh mà người kiểm ghi "không chắc đúng nơi" (29 ảnh lúc làm; tối 14/11 là 49: 20 ảnh minh hoạ bài chủ đề, 29 ảnh bài một nơi). Ở Khám phá, 29 ảnh đầu từng có nhãn "Ảnh minh hoạ". Đặt cạnh câu trả lời, ảnh sai nơi
  sẽ thành một lời khẳng định sai, nên ở đây không hiện.

Không đổi gì ở máy chủ, không đổi câu gửi model, 0 USD.

## Một chuyện thật: bật rồi mới thấy chậm, và lần đo "thêm cho tới khi đạt"

Sửa lịch bằng lời qua đủ các phép đo đúng sai và được bật lúc 14:04. Ngay sau đó mình đo độ trễ: một câu hỏi thường trong cuộc **đã có lịch** mất **4,17 s** tới
chữ đầu, trong khi cuộc chưa có lịch chỉ **2,23 s**. Sàn anh chốt là ≤ 3 s. Lý do: mọi câu trong cuộc có lịch phải chờ lần hiểu ý xong rồi mới bắt đầu
trả lời, kể cả câu không định sửa gì. Người điều phối **tắt cờ** lúc 14:14.

Sửa: đường trả lời thường chạy **ngay lập tức**, song song với lần hiểu ý. Chữ được giữ lại cho tới khi biết câu có phải câu sửa hay không. Nếu là câu sửa
thì bỏ phần đã chạy (tốn ≈ 0,0001 USD mỗi lần); nếu không thì đưa chữ ra luôn.

Lần đo đầu sau khi sửa ra chênh **+0,31 s**, vượt ngưỡng phụ +0,3 s. Mình chạy thêm 10 câu **sau khi đã thấy số đó**, gộp lại thì ra +0,16 s. Đó là "đo thêm
cho tới khi đạt", tức là đo sai cách: cỡ mẫu phải ghi trước khi chạy. Vì vậy mình đo lại từ đầu, chốt **n = 20 trước khi chạy**:
- cuộc chưa có lịch: **2,58 s**;
- cuộc đã có lịch: **2,65 s**;
- chênh **+0,07 s**, đạt cả sàn 3 s lẫn ngưỡng phụ.

Hai nhóm chậm hơn lần đo trước ≈ 0,3 s vì máy và API dao động, nên chênh giữa hai nhóm mới là số quyết. Cờ được bật lại lúc 15:08.

Bài học: **qua phép đo đúng sai chưa phải là xong**, độ trễ cũng là một sàn. Và khi một số vừa trượt, đừng chạy thêm cho tới khi nó đạt.

## Chuyện thật thứ hai: người xem chấm 10 / 10 mà vẫn sai

Luật chọn khu ở đã qua hai lượt người xem độc lập (9 / 10 rồi 10 / 10). Nhưng khi lịch mẫu có chỗ ở, người review thấy ngay: lịch được gợi ý **ở khu phía tây**
(3 / 5 điểm ban ngày ở phía tây), trong khi **cả hai tối** khách ở chợ Đông Ba và phố đi bộ, tức là phải đi về mỗi tối. Vì sao người xem không bắt? Bảng đưa cho
người xem **không có cột buổi tối**. Người xem chỉ chấm được thứ họ nhìn thấy.

Sửa hai lần, cùng một thước:
- **Thử 1:** đếm điểm buổi tối như điểm ban ngày. Người xem mới, bảng có buổi tối: **8 / 10**, dưới mức 9 ⇒ bỏ.
- **Thử 2:** lịch có buổi tối và mọi điểm tối ở trung tâm ⇒ ở trung tâm. Người xem mới khác, cùng 10 lịch: **10 / 10** ⇒ giữ. Người review đề nghị code tự
  kiểm "mọi điểm tối ở trung tâm" bằng bảng khu, thay vì tin rằng bộ xếp luôn đặt buổi tối ở trung tâm; đã sửa.

Hệ quả nói rõ để anh biết: trong 3.840 khung mô phỏng, **không lịch nào còn được gợi ý khu phía tây**, vì lịch người lớn nào cũng có buổi tối ở trung tâm.

Bài học: **bảng đưa người chấm phải có đủ thứ ảnh hưởng tới quyết định**, không thì điểm cao cũng không nói lên gì.

## Khi nào hỏng

- **Sửa lịch** chưa thêm hay đổi được hoạt động buổi tối, chỉ bỏ được. Tên điểm lạ ⇒ "Không đổi được" chứ không đoán. Câu chỉ chỗ bằng ngày / buổi ("bớt
  một chỗ ở ngày 2") giờ để model chọn điểm bỏ; về sau nên đưa thẻ chọn cho đúng nguyên tắc "code quyết".
- **Câu nhiều ý** chỉ chạy khi đếm được ≥ 2 vế. Câu hai ý mà không có từ hỏi riêng ở mỗi vế, hoặc nối bằng "hay", vẫn đi luật cũ (thiếu một ý ⇒ từ chối
  cả câu). Chữ "với" dùng như giới từ ("mua gì làm quà với giá bao nhiêu") có thể bị đếm thừa một vế. Hậu quả nhỏ, nhưng có.
- **Mục web** chọn vế theo số từ chung với dòng ý thiếu, sau khi bỏ các từ đã có ở phần trả lời (vd tên nơi). Nếu vẫn hoà hoặc không có từ chung ⇒ mục
  web viết cho cả câu như trước.
- **Chỗ ở:** lịch có buổi tối luôn ra trung tâm; trong 3.840 khung mô phỏng không lịch nào còn ra khu phía tây. Trong cùng mức, hạng cao đứng trước (tối 14/11), rồi cơ sở
  gần cụm có nhiều điểm nhất, rồi có ảnh, rồi theo tên — nên nhiều lịch trung tâm vẫn ra cùng 5 khách sạn; chỉ khoảng 12 / 140 cơ sở từng hiện. Không có giá, không có điểm đánh giá.
- **Quán ăn:** sau tối 14/11 Thủy Xuân, Kim Long, biển / đầm phá đã có quán kho ở hơn một nửa số bữa; phần còn lại là quán bản đồ mở, chưa kiểm. Vùng xa phía
  nam (Bạch Mã, Nhị Hồ) không có dòng ăn.
- **So tiền mục web:** "1,500 đ" được đọc là 1.500 đồng (dấu phẩy ngăn nghìn kiểu tiếng Anh); "10K bước" bị nhận là tiền, nên có thể bị chặn nhầm (hướng
  an toàn).
- **Ảnh** chỉ hiện khi mọi nguồn thuộc một bài, nên câu so sánh hai nơi không có ảnh. 6 bài chưa có ảnh nào, đều là quán.

## Ba điều chính

1. Mọi việc giữ một cách chia: **model đọc hiểu / diễn đạt, code quyết và kiểm**. Model hiểu ý sửa, code áp bằng đúng bộ xếp. Code đếm vế hỏi và chọn vế
   cho mục web. Code chọn khu ở, khách sạn, quán ăn, và có hiện ảnh hay không.
2. Mỗi việc **đo đúng chỗ đổi** rồi mới bật:
   - sửa lịch: ~15.000 lần áp 0 vi phạm, hiểu ý 9 / 10 + kín 4 / 5, an toàn 0 / 64;
   - câu nhiều ý: vòng 1 trượt ⇒ vòng 2 bằng code đạt, sửa "và", mục web nhắc lại ý kho 4 / 4 ⇒ 0 / 11;
   - chỗ ở: 3.840 khung + người xem 9 / 10 ⇒ sửa 2 lỗi ⇒ 10 / 10; thêm luật buổi tối (thử 1 bỏ 8 / 10, thử 2 giữ 10 / 10);
   - quán ăn: đếm trước (sửa 95,2 ⇒ 74,7 %) rồi mới xây; mục web: so tiền theo giá trị, 43 ⇒ 51 / 76, số bịa vẫn chặn.
3. Hai chuyện thật: sửa lịch qua đo đúng sai nhưng **phạm sàn tốc độ** ⇒ tắt, sửa, đo lại với cỡ mẫu chốt trước; người xem chấm 10 / 10 mà vẫn sai vì bảng
   thiếu buổi tối. Cùng ngày có hai việc **thử rồi bỏ / đếm rồi không làm** (suy luận low −0,87 s < 1,5 s; đổi cách tìm web 6 / 16 vừa chạm mức).

**Bài sau:** chưa có.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Sửa lịch bằng lời: 6 hành động, mô phỏng ~15.000 lần áp 0 vi phạm, 2 lỗi (240 khung; 4 / 1.920), Q3 7 / 10 ⇒ 9 / 10, kín 4 / 5, Q5 0 / 64, Q5b 0 / 16, tiền ≈ 0,25 USD, độ trễ 4,17 ⇒ 2,37 (n = 20 gộp, "đo thêm tới khi đạt") ⇒ đo lại n = 20 chốt trước 2,58 / 2,65 s, đệm 1.244 token 0,00024 ⇒ 0,0001 USD, phần huỷ ≈ 0,0001 USD: `report_agent/2026-11-12_ra_khoang_cach/b_sua_lich_v2_implementation.md` [đã chạy]; lỗi chặn câu trộn khẩn cấp: `e_review_sua_lich_v2.md` + mục "Sau review E" của report trên [đã chạy]; giới hạn chỉ bỏ được buổi tối: `session_prompt/CURRENT_HANDOFF.md` mục "Giới hạn đã nhận" [tài liệu]; câu ví dụ "bỏ điểm chiều nay, mình vừa bị ngã…" là **ví dụ tự đặt** (câu thật do E viết, không chép).
- Câu nhiều ý vòng 1 (4 / 10 ⇒ 10 / 10; 3 / 18; 2 lỗi trích dẫn; 0,16 USD): `report_agent/…/c_cau_nhieu_y_do.md` [đã chạy]; vòng 2 (10 / 10; kín 0 / 10; 1 / 18 câu 161 đường không đổi; 0 / 176 đi vào luật; ≈ 0,19 USD; cộng ≈ 0,35): `c_cau_nhieu_y_do_v2.md` [đã chạy]; anh chọn bật: `CURRENT_HANDOFF.md` 14:44 14/11 [tài liệu]; sửa "và" (0 câu đổi vế; 10 / 10; 0,0151 USD): `c_so_y_va_implementation.md`, review `b_review_so_y_va.md` [đã chạy]; mục web 4 / 4 ⇒ 0 / 11, 0,0349 USD, Serper vẫn cả câu: `c_web_y_thieu_implementation.md`, review `b_review_web_y_thieu.md` [đã chạy]; bỏ từ đã có ở phần trả lời khi chọn vế (sửa m-1 của review): commit `0b7ef90`, `backend/llm/assistant.py` [code]. Ví dụ "bún bò và bánh khoái" là ca test trong code [code].
- Chỗ ở: luật khu (50 % / 60 %, trẻ em ⇒ trung tâm), 2 / 2 / 1 theo hạng, 140 cơ sở danh mục Cục Du lịch Quốc gia, 3.840 khung (3.072 / 3.072), người xem 9 / 10 ⇒ 10 / 10, hai lỗi sửa, ≈ 0,0025 USD: `report_agent/…/b_luu_tru_lich_implementation.md` [đã chạy]; E review ready: `e_review_luu_tru_lich.md`; cờ bật: `backend/config/settings.yaml` `luu_tru_lich: true` [code].
- Ảnh dưới câu trả lời: điều kiện, 29 ảnh `kc` (nay 49: 20 chủ đề + 29 một nơi), backend không đổi: `report_agent/…/c_review_anh_tra_loi.md`, merge `4be483e` [code]; 184 / 216: bài 24.
- Câu "Đại Nội … và gần đó có quán karaoke…" là câu người điều phối thử thật, có trong report sửa "và" và ca test [đã chạy].
- Giờ bật / tắt / bật lại sửa lịch (14:04 · 14:14 · 15:08): commit `e0cb02e`, `3985816`, `69def87` [code]. Tiền đệm 0,00007 / lần: `e_review_sua_lich_v2.md` [đã chạy]. 139 + 1 cơ sở: trường `nguon` của bảng lưu trú [đã chạy]. 7 loại bài có ảnh: `frontend/src/anhTraLoi.js` [code].
- Quán ăn: đếm 22.680 bữa, 28 quán kho, 33,5 / 74,7 % (bản đầu 74,7 / 95,2 sai), 16 lượt Serper 0,016 USD (đếm web ý thiếu 3 / 16, tốt nhất 6 / 16): `report_agent/2026-11-12_ra_khoang_cach/c_dem_truoc_khi_xay.md` [đã chạy]; 2 km (p95 9,3 km), bữa tối gần điểm tối, cà phê, 80,7 %, 0,78 / 1,94 / 1,99 km, người xem 10 / 10, 0,0013 USD, giới hạn: `c_quan_lich_implementation.md`, review `b_review_quan_lich.md` [đã chạy]
- Khu ở theo buổi tối (thử 1 8 / 10, thử 2 10 / 10, phía tây 0 / 3.840): mục cuối `b_luu_tru_lich_implementation.md`; review `e_review_o_toi.md` (m-1 kiểm bằng bảng khu, đã sửa) [đã chạy]
- Lịch mẫu đi – ăn – ở, chỉ quán kho, 3 bữa, khu trung tâm: `b_review_lich_mau_an_o.md`, `b_review_lich_mau_quan_kho.md`; ảnh `data/ui_mau_2026-11-14/anh_chup/lich_mau_cuoi_1411/` [đã chạy]
- So tiền theo giá trị (16 ⇒ 4 chặn vì tiền, 43 ⇒ 51 / 76, 220.000 4 / 4, 8 mục mới qua, "2 triệu rưỡi", "150K"): `b_tien_web_chuan_hoa_implementation.md`, `e_review_tien_web.md` [đã chạy]
- Suy luận low (2,95 ⇒ 2,08 s, sàn 1,5 s, −32 % tiền lần viết, log 4,94 s): `b_web_suy_luan_thap_implementation.md` [đã chạy]
- Kiểm độc lập phần chiều (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25_chieu.md`): 57 mục — 52 đúng, 0 sai, 5 dễ hiểu nhầm; đã sửa cả 5 + 3 chỗ tuỳ chọn.
- Cập nhật 17:13, ngày 14/11/2026: thêm mục 4–7, chuyện thật thứ hai, sửa mục chỗ ở, Khi nào hỏng, Ba điều chính; mục ảnh thành mục 8.
- **Sửa 16:05 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25.md`, 135 khẳng định: 1 sai, 9 dễ hiểu nhầm): sửa câu "hoà điểm" của mục web (lỗi đã sửa trước khi merge); loại hành động thứ 6; 8 kiểu thử; 0 / 16 không đo số khẩn cấp; 139 + 1 cơ sở; thứ tự khách sạn; loại bài có ảnh; giờ bật.

- Tối 14/11: khách sạn (abc ⇒ hạng cao trước, 5 sao 0 / 6.108 ⇒ 3.036 / 3.036, ảnh 66 / 140, 97,6 %, Places 82 / 140, ≈ 0,283 USD): `report_agent/2026-11-12_ra_khoang_cach/b_khach_san_implementation.md`, review `c_review_khach_san.md`; quán 69,1 %: bài 22; ảnh quán 15 quán hiện / 5 ảnh, quán đã đóng 324 / 3.840: `c_anh_quan_implementation.md`, `e_review_anh_quan.md`, `e_review_quan_bo_da_dong.md`; năm trong câu hỏi 21 ⇒ 10 / 76: `a_web_so_cau_hoi_implementation.md`, `c_review_web_so_cau_hoi.md`, đếm gốc `e_dem_web_thay_cau.md` [đã chạy]
- Kiểm độc lập phần tối 14/11 (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_24_25_toi_1411.md`): 77 ý — 58 đúng, 6 sai, 10 dễ hiểu nhầm, 3 không kiểm được; đã sửa cả 16 + bỏ ngoặc kép câu dặn không nguyên văn.
</details>
