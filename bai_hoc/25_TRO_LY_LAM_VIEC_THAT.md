# Bài 25 — Trợ lý làm việc thật: sửa lịch bằng lời, câu hỏi nhiều ý, chỗ ở, ảnh dưới câu trả lời

*Cập nhật lần cuối: 15:57, ngày 14/11/2026 · bài mới; nối tiếp bài 23 và 15.*

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

---

*Bài 23 kể lịch "Lên kế hoạch" bản 2: code xếp, model chỉ viết câu tả. Bài 15 kể chuyện tra web khi sổ không có. Bài này kể bốn việc xong chiều 14/11,
đều theo hướng anh chọn: **trợ lý làm được việc**, không chỉ trả lời một câu. Cả bốn giữ một nguyên tắc từ bài 14: **việc dễ nhầm thì code làm**, model
chỉ đọc hiểu và diễn đạt.*

## Quay lại người hướng dẫn viên

Khách nói "bỏ chợ tối nay đi, mình mệt rồi". Một người hướng dẫn viên tốt không vẽ lại cả lịch từ đầu. Họ gạch đúng một dòng, giữ nguyên những chỗ khác,
và nói rõ đã đổi gì. Khách hỏi một câu gồm hai việc, trong đó sổ tay chỉ có một: người giỏi trả lời phần biết, nói thẳng phần chưa biết, chứ không từ
chối cả câu. Khách đi ba ngày thì cần biết nên ở khu nào. Và khi kể về một nơi, đưa khách xem một tấm ảnh thì dễ hình dung hơn mười câu tả.

Bốn việc dưới đây dạy trợ lý làm đúng bốn thói quen đó.

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
- **Chọn khu** bằng cách đếm các điểm tham quan ban ngày của lịch theo khu. Mặc định là trung tâm hai bờ sông Hương.
  - Phía tây (Kim Long, Thủy Xuân) chỉ khi hơn một nửa số điểm ở đó **và** đoàn không có trẻ em / người lớn tuổi.
  - Ven biển chỉ khi ≥ 60 % số điểm ở ven biển.
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

## 4. Ảnh dưới câu trả lời

Hỏi trợ lý về một nơi hay một món, câu trả lời giờ có **một ảnh** ở dưới. Bấm vào ảnh thì mở bài trong Khám phá. Ảnh lấy từ bộ ảnh đã có của Khám phá
(167 / 207 bài có ảnh, bài 24).

**Code quyết có hiện ảnh không,** model không chọn ảnh. Chỉ hiện khi đủ các điều kiện:
- trợ lý trả lời bằng kho, không phải câu từ chối, không có mục web, không phải lịch;
- **mọi nguồn được trích thuộc đúng một bài**, và bài đó nói về một thứ cụ thể (một nơi, một món, một lễ hội hay một loại hình nghệ thuật), không phải
  bài tổng quan;
- ảnh không thuộc 29 ảnh mà người kiểm ghi "không chắc đúng nơi". Ở Khám phá, 29 ảnh này từng có nhãn "Ảnh minh hoạ". Đặt cạnh câu trả lời, ảnh sai nơi
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

## Khi nào hỏng

- **Sửa lịch** chưa thêm hay đổi được hoạt động buổi tối, chỉ bỏ được. Tên điểm lạ ⇒ "Không đổi được" chứ không đoán. Câu chỉ chỗ bằng ngày / buổi ("bớt
  một chỗ ở ngày 2") giờ để model chọn điểm bỏ; về sau nên đưa thẻ chọn cho đúng nguyên tắc "code quyết".
- **Câu nhiều ý** chỉ chạy khi đếm được ≥ 2 vế. Câu hai ý mà không có từ hỏi riêng ở mỗi vế, hoặc nối bằng "hay", vẫn đi luật cũ (thiếu một ý ⇒ từ chối
  cả câu). Chữ "với" dùng như giới từ ("mua gì làm quà với giá bao nhiêu") có thể bị đếm thừa một vế. Hậu quả nhỏ, nhưng có.
- **Mục web** chọn vế theo số từ chung với dòng ý thiếu, sau khi bỏ các từ đã có ở phần trả lời (vd tên nơi). Nếu vẫn hoà hoặc không có từ chung ⇒ mục
  web viết cho cả câu như trước.
- **Chỗ ở** được chọn theo số điểm, không theo số ngày: một ngày đi nhiều lăng có thể kéo cả chuyến sang khu phía tây. Trong cùng mức hạng, cơ sở
  gần cụm có nhiều điểm nhất đứng trước, còn lại xếp theo tên, nên nhiều lịch trung tâm ra cùng 5 khách sạn. Phía tây chỉ có 5 cơ sở trong danh mục. Không có giá, không có điểm đánh giá.
- **Ảnh** chỉ hiện khi mọi nguồn thuộc một bài, nên câu so sánh hai nơi không có ảnh. 40 bài chưa có ảnh nào.

## Ba điều chính

1. Cả bốn việc giữ một cách chia: **model đọc hiểu / diễn đạt, code quyết và kiểm**. Model hiểu ý sửa, code áp bằng đúng bộ xếp. Code đếm vế hỏi và chọn vế
   cho mục web. Code chọn khu ở, khách sạn, và có hiện ảnh hay không.
2. Mỗi việc **đo đúng chỗ đổi** rồi mới bật:
   - sửa lịch: ~15.000 lần áp 0 vi phạm, hiểu ý 9 / 10 + kín 4 / 5, an toàn 0 / 64;
   - câu nhiều ý: vòng 1 trượt ⇒ vòng 2 bằng code đạt, sửa "và", mục web nhắc lại ý kho 4 / 4 ⇒ 0 / 11;
   - chỗ ở: 3.840 khung + người xem 9 / 10 ⇒ sửa 2 lỗi ⇒ 10 / 10.
3. Chuyện thật: sửa lịch qua đo đúng sai nhưng **phạm sàn tốc độ** (4,17 s) ⇒ tắt ⇒ cho chạy song song ⇒ đo lại với cỡ mẫu chốt trước: 2,65 so với 2,58 s.

**Bài sau:** chưa có.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Sửa lịch bằng lời: 6 hành động, mô phỏng ~15.000 lần áp 0 vi phạm, 2 lỗi (240 khung; 4 / 1.920), Q3 7 / 10 ⇒ 9 / 10, kín 4 / 5, Q5 0 / 64, Q5b 0 / 16, tiền ≈ 0,25 USD, độ trễ 4,17 ⇒ 2,37 (n = 20 gộp, "đo thêm tới khi đạt") ⇒ đo lại n = 20 chốt trước 2,58 / 2,65 s, đệm 1.244 token 0,00024 ⇒ 0,0001 USD, phần huỷ ≈ 0,0001 USD: `report_agent/2026-11-12_ra_khoang_cach/b_sua_lich_v2_implementation.md` [đã chạy]; lỗi chặn câu trộn khẩn cấp: `e_review_sua_lich_v2.md` + mục "Sau review E" của report trên [đã chạy]; giới hạn chỉ bỏ được buổi tối: `session_prompt/CURRENT_HANDOFF.md` mục "Giới hạn đã nhận" [tài liệu]; câu ví dụ "bỏ điểm chiều nay, mình vừa bị ngã…" là **ví dụ tự đặt** (câu thật do E viết, không chép).
- Câu nhiều ý vòng 1 (4 / 10 ⇒ 10 / 10; 3 / 18; 2 lỗi trích dẫn; 0,16 USD): `report_agent/…/c_cau_nhieu_y_do.md` [đã chạy]; vòng 2 (10 / 10; kín 0 / 10; 1 / 18 câu 161 đường không đổi; 0 / 176 đi vào luật; ≈ 0,19 USD; cộng ≈ 0,35): `c_cau_nhieu_y_do_v2.md` [đã chạy]; anh chọn bật: `CURRENT_HANDOFF.md` 14:44 14/11 [tài liệu]; sửa "và" (0 câu đổi vế; 10 / 10; 0,0151 USD): `c_so_y_va_implementation.md`, review `b_review_so_y_va.md` [đã chạy]; mục web 4 / 4 ⇒ 0 / 11, 0,0349 USD, Serper vẫn cả câu: `c_web_y_thieu_implementation.md`, review `b_review_web_y_thieu.md` [đã chạy]; bỏ từ đã có ở phần trả lời khi chọn vế (sửa m-1 của review): commit `0b7ef90`, `backend/llm/assistant.py` [code]. Ví dụ "bún bò và bánh khoái" là ca test trong code [code].
- Chỗ ở: luật khu (50 % / 60 %, trẻ em ⇒ trung tâm), 2 / 2 / 1 theo hạng, 140 cơ sở danh mục Cục Du lịch Quốc gia, 3.840 khung (3.072 / 3.072), người xem 9 / 10 ⇒ 10 / 10, hai lỗi sửa, ≈ 0,0025 USD: `report_agent/…/b_luu_tru_lich_implementation.md` [đã chạy]; E review ready: `e_review_luu_tru_lich.md`; cờ bật: `backend/config/settings.yaml` `luu_tru_lich: true` [code].
- Ảnh dưới câu trả lời: điều kiện, 29 ảnh `kc`, backend không đổi: `report_agent/…/c_review_anh_tra_loi.md`, merge `4be483e` [code]; 167 / 207: bài 24.
- Câu "Đại Nội … và gần đó có quán karaoke…" là câu người điều phối thử thật, có trong report sửa "và" và ca test [đã chạy].
- Giờ bật / tắt / bật lại sửa lịch (14:04 · 14:14 · 15:08): commit `e0cb02e`, `3985816`, `69def87` [code]. Tiền đệm 0,00007 / lần: `e_review_sua_lich_v2.md` [đã chạy]. 139 + 1 cơ sở: trường `nguon` của bảng lưu trú [đã chạy]. 7 loại bài có ảnh: `frontend/src/anhTraLoi.js` [code].
- **Sửa 16:05 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25.md`, 135 khẳng định: 1 sai, 9 dễ hiểu nhầm): sửa câu "hoà điểm" của mục web (lỗi đã sửa trước khi merge); loại hành động thứ 6; 8 kiểu thử; 0 / 16 không đo số khẩn cấp; 139 + 1 cơ sở; thứ tự khách sạn; loại bài có ảnh; giờ bật.

</details>
