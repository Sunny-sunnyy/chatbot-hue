# Bài 28 — Chương trình xếp lịch theo luật nào: một lịch thật được xếp từng bước

*Cập nhật 17:03, ngày 23/11/2026 · khớp hệ thống 16:21 23/11 (51 tính năng mở, 7 tắt, kho 267 bài); chưa gồm các bản gộp từ 16:38 (chờ phiếu) · đã áp biên bản kiểm · lịch ví dụ là lượt thật 21/11 (Claude Sonnet 5.5); biến thể "Đổi một ô" do người viết chạy bộ xếp, không gọi model · dòng cũ: Nguồn.*

**Bài trước đã biết:** người dùng bấm tám ô; chương trình xếp lịch từ bảng 41 điểm; model chỉ viết câu mô tả (bài 27).
**Bài này thêm:** chương trình chọn điểm và tính giờ theo những luật nào, luật nào thắng khi hai luật kéo ngược nhau, và vì sao các con số là 75, 150, 210, 240 phút. Bài đi từng bước trên chính lịch ví dụ: 3 ngày, 2 người lớn, cân bằng, thích di tích.

## Ý chính

- Bộ xếp là **chương trình thuần**: không gọi mạng, không gọi model; cùng tám giá trị luôn ra cùng một lịch.
- Luật có **thứ tự ưu tiên**: an toàn cho trẻ em và người lớn tuổi → giờ mở cửa, thứ, mùa → gom điểm gần nhau (một ngày nhiều nhất 2 cụm kề nhau) → điểm ưu tiên của sở thích → sở thích → kiểu đi. Luật đứng dưới chỉ được chọn trong số điểm mà các luật đứng trên đã cho qua.
- Thời gian tính **bằng phút cố định**: điểm ngắn 75, nửa buổi 150; đi trong cụm 15, sang cụm kề 30. Quỹ một buổi: "cân bằng" 210 phút, "khám phá nhiều" 240, "nhẹ nhàng" đúng 1 điểm. Giờ in ra là phép cộng các số này. Ngoại lệ (từ 15:38 23/11, chỉ đoàn không có trẻ nhỏ / người lớn tuổi): ngày người dùng tự xin thêm điểm sau khi lịch đã xếp được vượt quỹ phút, tới 3 điểm một buổi, miễn còn giờ mở cửa, 60 phút ăn trưa, sáng kết trước 13:30, chiều trước 18:00 (bài 31).
- Mỗi buổi chọn **điểm đầu** trước, rồi mới thêm điểm thứ hai nếu còn quỹ; buổi tối chọn **sau cùng**. Cái giá đã đếm được: có lịch đi Đại Nội, sang chùa Thiên Mụ, rồi quay lại Ngọ Môn trong cùng ngày, như chính lịch ví dụ.
- Đổi một ô là lịch đổi theo một luật đọc được, ví dụ có người lớn tuổi thì mỗi buổi một điểm và không buổi tối.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| điểm đầu của buổi | **anchor** | điểm được chọn trước tiên cho một buổi sáng hay chiều |
| quỹ phút | **time budget** | số phút tối đa của một buổi, gồm phút tham quan và phút đi giữa hai điểm |
| điểm ưu tiên | **priority point** | 3–4 điểm tiêu biểu nhất của mỗi sở thích, ghi sẵn trong bảng, được xét trước |
| điểm lấp | **filler** | điểm di tích theo thứ tự bảng, dùng khi hết điểm hợp sở thích |
| cụm kề | **adjacent cluster** | hai cụm được ghi sẵn là cùng hướng, đi nối được trong một ngày |
| nhóm hạn chế | — | lịch có trẻ em hoặc có người lớn tuổi |
| chương trình thuần | **deterministic code** | chương trình không gọi gì bên ngoài; cùng đầu vào luôn ra cùng kết quả |

## Bảy luật, xếp theo thứ tự ưu tiên

Khi hai luật kéo ngược nhau, luật đứng trên thắng.

| Bậc | Luật | Ở lịch ví dụ |
|---|---|---|
| 1 | **Nhóm hạn chế**: mỗi buổi một điểm, không buổi tối, tránh điểm nhiều bậc thang khi cùng cụm có điểm thay | không áp |
| 2 | **Giờ mở cửa, thứ, mùa:** điểm phải xong trước giờ đóng; đóng cửa vào thứ đó hay tạm dừng theo mùa thì không xếp | chỉ xét giờ mở cửa (không có ngày đi) |
| 3 | **Gom gần:** một ngày nhiều nhất 2 cụm và hai cụm phải kề nhau; cụm "phía nam xa" chiếm cả ngày, chỉ xếp khi lịch từ 3 ngày và không ở ngày 1 | mỗi ngày 2 cụm |
| 4 | **Điểm ưu tiên** của sở thích đứng đầu thứ tự xét | 4 điểm ưu tiên của "di tích": Đại Nội, chùa Thiên Mụ, lăng Tự Đức, lăng Khải Định |
| 5 | **Ngày mưa** (dự báo khả năng mưa từ 60 % và lượng mưa từ 6 mm): ngoài điểm ưu tiên, xét điểm trong nhà trước | không có dự báo |
| 6 | **Sở thích:** điểm hợp sở thích theo thứ tự bảng; hai sở thích thì xen kẽ; không chọn thì dùng nhóm "chung" và thêm một điểm thiên nhiên mỗi ngày (đầu buổi chiều; ngày mưa thì không) | di tích theo thứ tự bảng |
| 7 | **Kiểu đi:** quỹ phút mỗi buổi, nhiều nhất 2 điểm một buổi | cân bằng, quỹ 210 phút |

Số người lớn không vào bộ xếp. Buổi tối được chọn sau khi sáng và chiều đã chốt, nên không làm đổi phần ban ngày.

## Ngày 1 của lịch ví dụ, từng bước

Chương trình lập **thứ tự xét**: 4 điểm ưu tiên của di tích, rồi các di tích khác theo thứ tự bảng. Giờ bắt đầu: sáng 8:00, chiều 13:30.

| Bước | Chương trình làm gì | Kết quả |
|---|---|---|
| 1. Điểm đầu buổi sáng | lấy điểm đầu tiên trong thứ tự xét đi được buổi sáng, kịp giờ mở cửa, và còn một điểm "bạn" cho buổi chiều ở cùng cụm hoặc cụm kề | **Đại Nội** (cụm Kinh thành, nửa buổi): 8:00 + 150 phút = **8:00 – 10:30** |
| 2. Điểm đầu buổi chiều | điểm kế tiếp đi được buổi chiều và hợp cụm của ngày | **chùa Thiên Mụ** (cụm Kim Long, kề Kinh thành, ngắn): **13:30 – 14:45**. Ngày đã đủ 2 cụm |
| 3. Thêm điểm vào buổi sáng | thêm một điểm cùng cụm hoặc cụm kề với điểm ngay trước, nếu tổng phút còn trong quỹ | đã dùng 150; thêm một điểm ngắn cùng cụm thành 150 + 15 + 75 = 240 > 210 ⇒ **không thêm** |
| 4. Thêm điểm vào buổi chiều | như trên | đã dùng 75. Lăng Tự Đức, Khải Định (cụm Thủy Xuân) kề Kim Long nhưng sẽ là cụm thứ ba ⇒ bỏ qua. **Ngọ Môn – Kỳ Đài** (cụm Kinh thành, kề Kim Long, 30 phút đi): 75 + 30 + 75 = 180 ≤ 210 ⇒ **15:15 – 16:30** |
| 5. Buổi tối | chọn sau cùng: chỉ ở hai cụm trung tâm, hợp sở thích trước, rồi theo thứ tự bảng; không có ngày đi thì chỉ lấy hoạt động diễn mọi tối | **chợ Đông Ba**, 18:00 – 23:00, kèm dòng "phố ẩm thực đêm trước cổng chợ; trong chợ đóng cửa khoảng 18:00" |

Giữa hai điểm cùng buổi, thẻ lịch hiện dòng "khoảng 30 phút đi". Đó đúng là con số bộ xếp vừa dùng để giãn giờ, nên giờ in ra và phút đi không thể lệch nhau.

Ngày 1 có một chỗ dở nhóm đã đếm: đi Đại Nội, sang Thiên Mụ, rồi **quay lại** Ngọ Môn, mà Ngọ Môn là cổng của Đại Nội. Gốc: điểm thêm chỉ xét cụm của điểm ngay trước; không bước nào sắp lại thứ tự đi của cả ngày (quyết định 3).

## Ngày 2, ngày 3, và buổi tối

**Ngày 2.** Hai điểm ưu tiên còn lại cùng ở cụm Thủy Xuân: lăng Tự Đức sáng (8:00 – 10:30), lăng Khải Định chiều (13:30 – 16:00). Cả hai là điểm nửa buổi, thêm điểm nào cũng vượt quỹ. Tối: phố đi bộ Nguyễn Đình Chiểu (hoạt động tối không lặp cho tới khi hết lựa chọn).

**Ngày 3.** Hết điểm ưu tiên, chương trình đi tiếp các di tích theo thứ tự bảng. Sáng: phố cổ Bao Vinh (cụm Kinh thành, 8:00 – 10:30). Chiều: trường Quốc Học (bờ nam, kề Kinh thành, 13:30 – 14:45), rồi cung An Định (cùng cụm bờ nam, 15 phút đi): 75 + 15 + 75 = 165 phút ⇒ 15:00 – 16:15. Tối: phố Tây.

Cả lịch: 8 điểm ban ngày, 3 hoạt động tối. Không thiếu điểm ưu tiên nào, nên phần ghi chú chỉ có một dòng: giờ trong lịch là giờ gợi ý.

## Đổi một ô thì lịch đổi ra sao

Người viết chạy lại bộ xếp, mỗi lần đổi đúng một ô so với lịch ví dụ (không gọi model).

| Đổi gì | Lịch mới | Luật nào làm việc đó |
|---|---|---|
| kiểu đi "nhẹ nhàng" | 6 điểm ban ngày, mỗi buổi một điểm; ngày 3 thành Ngọ Môn và Bao Vinh | bậc 7: nhẹ nhàng đúng 1 điểm một buổi |
| kiểu đi "khám phá nhiều" | 11 điểm ban ngày, bắt đầu 7:30 và 13:00; ngày 1 thêm Ngọ Môn buổi sáng và điện Hòn Chén buổi chiều | bậc 7: quỹ 240 vừa nửa buổi cộng một điểm ngắn |
| có người lớn tuổi (hoặc trẻ em) | 6 điểm ban ngày, không buổi tối; ngày 2 thành lăng Đồng Khánh và Thiệu Trị (không bậc thang); ghi chú nêu Thiên Mụ, Tự Đức có nhiều bậc thang | bậc 1: hết điểm thay cùng cụm thì vẫn xếp và ghi chú |
| 2 ngày | đúng hai ngày đầu của lịch ví dụ | bộ xếp đi lần lượt từng ngày theo cùng một thứ tự xét, nên bớt ngày cuối không làm đổi các ngày trước |
| không chọn sở thích, kiểu đi | chiều ngày 1 là Đầm Chuồn; hai dòng ghi chú nói lịch đã giả định gì | bậc 6, luật mặc định |

## Quyết định và lý do

### 1. Vì sao thời gian tính bằng hai mức cố định 75 và 150 phút, và quỹ một buổi là 210 hay 240 phút?

Mỗi điểm trong bảng chỉ mang nhãn "ngắn" hoặc "nửa buổi", không mang số phút riêng.

- **Đã chọn:** ngắn 75 phút, nửa buổi 150 phút; quỹ cân bằng 210, khám phá nhiều 240; nhiều nhất 2 điểm một buổi.
- **Vì sao:** thiết kế ghi kèm phép thử số: hai điểm ngắn cùng cụm 165 phút, cụm kề 180 ⇒ vừa "cân bằng"; nửa buổi cộng ngắn 240 ⇒ chỉ vừa "khám phá nhiều"; ba điểm ngắn 255 ⇒ không vừa mức nào, "đúng ý: không nhồi". Mọi số là bội của 15 phút nên giờ in ra không cần làm tròn. Lý do của chính hai mức 75 và 150: chưa thấy ghi lý do. Điều thấy được: thời lượng của từng điểm (ví dụ Đại Nội "2,5 tới 3,5 giờ") được quy về một trong hai nhãn.
- **Cách khác:** luật "đi dày" của bản đầu (chỉ ghép thêm khi điểm đầu là điểm ngắn): đã đo trên cùng bảng, khác "thong thả" ở 3 / 120 cặp, tức bấm gần như không đổi gì ⇒ bỏ. Số phút riêng cho từng điểm: chưa thử.
- **Cái giá:** một điểm thật sự cần 2 giờ vẫn được tính 150 phút. Thời lượng của 31 trên 41 điểm dựa vào web (bài 27); nhãn sai thì giờ gợi ý sai theo.

### 2. Vì sao buổi sáng bắt đầu 8:00, buổi chiều 13:30, và điểm thêm buổi sáng phải xong trước buổi chiều 60 phút?

- **Đã chọn:** sáng 8:00, chiều 13:30 (khám phá nhiều: 7:30 và 13:00). Điểm thêm của buổi sáng phải xong trước giờ đầu buổi chiều ít nhất 60 phút.
- **Vì sao:** giờ chiều chọn để điểm cuối xong trước giờ đóng 30 phút, vì kho không ghi giờ ngừng bán vé: buổi chiều xong muộn nhất 17:00, trước giờ đóng 17:30 của Quần thể di tích. Mốc 60 phút có từ 17/11: nhóm tự thử gặp lịch xong Kinh thành 12:45 mà 13:00 đã ở phá Tam Giang; đếm trên 960 cách điền biểu mẫu, có 26 ngày như vậy.
- **Cách khác:** không chừa giờ ăn trưa (bản trước 17/11): đã đo, bỏ.
- **Cái giá:** phút đi chỉ ước theo cụm (15 hoặc 30 phút) và chỉ in giữa hai điểm cùng buổi; giữa sáng và chiều lịch chỉ chừa ít nhất 60 phút cho ăn trưa và đi lại, không tính đường thật. Lịch không dời theo giờ tới, giờ về.

### 3. Vì sao gom điểm theo cụm, và phút đi ước theo cụm mà không tra bảng khoảng cách?

- **Đã chọn:** 8 cụm; một ngày nhiều nhất 2 cụm kề nhau; điểm thêm phải cùng cụm hoặc cụm kề với điểm ngay trước; đi trong cụm 15 phút, sang cụm kề 30 phút.
- **Vì sao:** luật "một ngày nhiều nhất 2 cụm" có từ thiết kế gốc của lịch; danh sách cụm kề ghi trước theo vị trí kho ghi, nghĩa là "cùng hướng", không phải đường đi. Lý do của số 2 và của 15, 30 phút: chưa thấy ghi lý do. Điều thấy được: bảng khoảng cách có từ 16/11, sau khi bộ xếp đã chạy (14/11); kế hoạch làm bảng ghi rõ "công cụ này KHÔNG đổi lịch", không nêu vì sao.
- **Cách khác:** dùng số phút thật từ bảng khoảng cách: chưa thử (kế hoạch 16/11 chủ ý để ngoài phạm vi). Bản sửa hẹp cho ca "quay lại": đã đo, ca dễ thấy về 0 nhưng làm đổi một ca mưa và một chuỗi đo sửa lịch ⇒ nhóm chốt giữ giới hạn (20/11).
- **Cái giá:** ca "quay lại cùng khu" còn nguyên: 104 trên 960 cách điền biểu mẫu có ít nhất một ngày như vậy (đếm cả buổi tối); ca Đại Nội → Thiên Mụ → Ngọ Môn là 8 trên 960, đúng lịch ví dụ.

### 4. Vì sao có trẻ em hay người lớn tuổi thì lịch bị giới hạn chặt như vậy?

- **Đã chọn:** mỗi buổi một điểm, không buổi tối, giờ như "nhẹ nhàng" dù người dùng chọn kiểu đi khác; điểm nhiều bậc thang được thay bằng điểm cùng cụm khi có. Luật này đứng bậc 1, thắng cả điểm ưu tiên. Từ 13:47 23/11 đầu thẻ lịch (dòng "Mình hiểu…", ô "Thời gian") cũng ghi "nhẹ nhàng" cho nhóm này và bỏ câu ghi chú "Chưa chọn kiểu đi…"; chỉ đổi chữ, cách xếp giữ nguyên; tóm tắt biểu mẫu và phần đưa cho model vẫn theo kiểu đi đã lưu ("Chi tiết để tra").
- **Vì sao:** lúc làm lịch bản đầu, nhóm đọc một hệ thống lập lịch khác và thấy nó xếp 5–6 điểm một ngày khi có người lớn tuổi, xếp cả điểm sau giờ đóng cửa. Luật an toàn được đặt lên đầu để tránh đúng hai lỗi đó.
- **Cách khác:** cho nhóm này một hoạt động tối nhẹ khi bảng đánh dấu "hợp gia đình": thiết kế có nêu, chưa làm.
- **Cái giá:** gia đình khoẻ mạnh muốn đi nhiều vẫn bị giữ ở mức nhẹ. Từ 15/11 buổi để trống không hiện thành một mục; lý do nằm ở một dòng ghi chú (chủ dự án yêu cầu).

Ba quyết định nhỏ hơn (ngày mưa, cụm xa, buổi sáng chọn điểm còn "bạn chiều") nằm ở nửa để tra.

## Nếu… thì sao

Bộ xếp không gọi gì bên ngoài nên không có thứ "hỏng"; bảng dưới là khi điều kiện đổi (không xếp được: bài 29).

| Nếu | Bộ xếp làm gì | Người dùng thấy gì |
|---|---|---|
| ngày đi rơi vào thứ một điểm đóng cửa | không xếp điểm đó ngày ấy | điểm khác thay chỗ; không có dòng báo riêng |
| ngày đi rơi vào tháng điểm ưu tiên tạm dừng (thác Nhị Hồ, tháng 9 – 2) | không xếp | "… đang tạm dừng đón khách vào thời gian này trong năm (theo kho) nên mình chưa xếp." |
| dự báo mưa to cho một ngày trong 7 ngày tới | ngoài điểm ưu tiên, xét điểm trong nhà trước | lịch có thể khác ngày khô; luôn có đúng một dòng "Nếu mưa ngày …" |
| sở thích có ít điểm | lấp bằng di tích theo thứ tự bảng | điểm lấp không có nhãn; thiếu điểm ưu tiên thì có dòng "Lịch này chưa xếp được điểm tiêu biểu nhất cho sở thích …" |

## Dễ nhầm

- **"Lịch đã tính đường đi thật giữa các điểm."** Không. Phút đi là 15 hay 30 theo cụm; bảng khoảng cách chỉ dùng ở ô hỏi đáp.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Vì sao buổi sáng ngày 1 của lịch ví dụ chỉ có Đại Nội?</summary>

Đại Nội là điểm nửa buổi, 150 phút. Thêm một điểm ngắn cùng cụm thành 150 + 15 + 75 = 240 phút, vượt quỹ 210 của kiểu "cân bằng".

</details>

<details>
<summary>2. Vì sao buổi chiều ngày 1 có Ngọ Môn mà không có lăng Tự Đức?</summary>

Ngày đã có hai cụm (Kinh thành, Kim Long). Lăng Tự Đức ở cụm thứ ba nên bị luật "nhiều nhất 2 cụm" chặn; Ngọ Môn ở cụm Kinh thành, kề Kim Long, vừa quỹ 180 phút.

</details>

<details>
<summary>3. Ca "đi rồi quay lại cùng khu" sinh ra từ đâu, và vì sao chưa sửa?</summary>

Bộ xếp chọn điểm đầu của sáng và chiều trước, rồi thêm điểm theo cụm của điểm ngay trước; không bước nào sắp lại cả ngày.

</details>

## Cấu hình đang chạy

*Các hằng số nằm trong chương trình, không nằm ở file cấu hình; đọc trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| thời lượng | ngắn 75 phút · nửa buổi 150 phút | quyết định 1 | chưa thử số phút riêng từng điểm |
| phút đi trong một buổi | cùng cụm 15 · cụm kề 30 · cụm khác không ghép | quyết định 3 | chưa thử số từ bảng khoảng cách |
| quỹ một buổi | nhẹ nhàng 1 điểm · cân bằng 210 · khám phá nhiều 240 | quyết định 1 | luật "đi dày" cũ: bỏ (3 / 120) |
| số điểm tối đa | 2 một buổi, 4 một ngày; ngày người dùng tự xin thêm sau khi xếp: đoàn thường, 3 một buổi, không tính quỹ (từ 15:38 23/11, bài 31) | ba điểm ngắn đã vượt quỹ 240 | — |
| giờ bắt đầu | sáng 8:00, chiều 13:30; khám phá nhiều 7:30, 13:00; nhóm hạn chế như nhẹ nhàng | quyết định 2 | bản nháp thiết kế: sáng 8:00 – 11:00, chiều 14:00 – 17:00 |
| chừa giờ ăn trưa | 60 phút | quyết định 2 | không chừa: 26 ngày sát giờ trên 960 cách điền |
| số ngày tối đa | 5 | chủ dự án chốt | — |
| cụm | 8 cụm; 8 cặp kề: Kinh thành – bờ nam, Kinh thành – Kim Long, Kinh thành – đầm phá biển, bờ nam – An Cựu, An Cựu – Thủy Xuân, Thủy Xuân – Kim Long, Thủy Xuân – lăng xa, Kim Long – lăng xa | quyết định 3; "phía nam xa" không kề cụm nào | — |
| cụm phía nam xa | chỉ khi lịch từ 3 ngày, không ở ngày 1; ngày đó tối nghỉ | quyết định nhỏ hơn | đã mô phỏng có / không luật ngày 1 |
| ngày mưa | khả năng mưa ≥ 60 % và lượng mưa ≥ 6 mm | quyết định 5 | chỉ 60 %: bỏ |
| hoạt động buổi tối | chỉ cụm Kinh thành và bờ nam; một hoạt động một tối; không lặp tới khi hết; hợp sở thích trước | khách đã về khu trung tâm | — |
| ngưỡng hiện một loại sở thích | ≥ 4 điểm | bài 27 | — |

## Đã so

**Bản đầu so với bản hiện nay.** Bản đầu (07/11) xếp mỗi buổi một điểm theo thứ tự bảng: 7 trên 28 điểm không bao giờ được xếp, nút "đi dày" đổi khung 0 trên 120 lần, lịch không có giờ, không hỏi ngày đi. Bản hiện nay viết lại bộ xếp (bật 14/11).

| Phép đo (chỉ chương trình, 0 USD) | Kết quả | Kết luận |
|---|---|---|
| mô phỏng bản thử trên bảng 34 điểm: 5 mức số ngày × 2 nhóm × 6 sở thích × 3 kiểu đi = 180 lịch | 0 điểm lặp, 0 ngày rỗng, 0 ngày quá 2 cụm; ba kiểu đi ra ba khung khác nhau ở 24 / 30 nhóm không hạn chế (sàn 70 %); trung bình 2,00 / 2,76 / 3,24 điểm một ngày; 1 / 30 điểm ban ngày không bao giờ được xếp | giữ |
| luật "đi dày" cũ trên cùng bảng | khác "thong thả" ở 3 / 120 cặp | bỏ |
| sáng tràn sang chiều (người chấm mù thấy, 14/11) | 52 / 3.840 khung ⇒ 0 / 3.840 | sửa |
| chừa 60 phút ăn trưa (17/11) | 26 ngày sát giờ trên 960 cách điền; so 4.800 lịch cũ ↔ mới: 130 lịch đổi, đều là lịch có ngày như vậy | giữ |
| ngày mưa, không chọn sở thích: bỏ luật "chiều một điểm thiên nhiên" (17/11) | 100 / 3.880 lịch đổi, đều đúng loại cần đổi; ngày có điểm biển – đầm phá 109 ⇒ 0 / 300; ngày toàn ngoài trời 253 ⇒ 181 / 300 | giữ |
| mốc mưa 6 mm (15/11, một năm dự báo so với mưa đo lại) | coi nhầm là mưa 106 ⇒ 15 ngày; chuyến 2–5 ngày có ít nhất một ngày xếp kiểu mưa 80 % ⇒ 50 % | giữ |
| thêm 7 điểm (15/11, 3.840 tổ hợp, đếm điểm ngoài sở thích ở lịch một sở thích) | chụp ảnh 51,7 % ⇒ 36,8 %; ẩm thực 56,4 % ⇒ 44,0 %; thiên nhiên 24,4 % ⇒ 17,6 %; lễ hội 39,0 % ⇒ 39,1 %; 0 lỗi khung | giữ |
| sửa hẹp ca "quay lại cùng khu" (17/11) | ca hẹp: 8 trên 960 cách điền và 24 trên 3.840 khung ⇒ 0 và 0; ca rộng (đếm theo ngày, chỉ buổi sáng và chiều — cách đếm khác số 104 ở "Giới hạn"): 65 ngày trong 960 cách điền và 258 trong 3.840 khung ⇒ 20 và 76; điểm ban ngày giảm khoảng 0,4 %; đổi một ca mưa và một chuỗi sửa lịch | không gộp; giữ giới hạn |

**Đọc bảng thế nào:** mọi phép trên chỉ đếm khung lịch do chương trình xếp, không chạy model; chúng kiểm được luật, không kiểm được lịch có hay không. Ba lỗi người review và người chấm mù tìm ra (bài 29) là thứ mô phỏng không bắt.

**Giới hạn của phép đo:** "960" là số cách điền biểu mẫu, không phải số người dùng; một ca 8 / 960 có thể là ca nhiều người bấm nhất (lịch mặc định "cân bằng + di tích").

## Quyết định nhỏ hơn

**Vì sao ngày mưa chỉ đổi điểm khi dự báo có từ 6 mm mưa?** Dự báo khả năng mưa từ 60 % thì lịch có một dòng "Nếu mưa…"; đổi thứ tự sang điểm trong nhà thì cần thêm lượng mưa dự báo từ 6 mm. Chủ dự án chốt ngày 15/11: 6 mm là đầu cấp "Mưa" theo quy chuẩn khí tượng Việt Nam. Con số "khả năng mưa" của dịch vụ dự báo là giờ cao nhất trong ngày, nên một giờ có thể lấm tấm là đủ 60 %: một năm có 222 / 365 ngày như vậy. Cách khác (chỉ mốc 60 %) đã đo, bỏ: bảng ở mục "Đã so". Cái giá: chỉ 12 / 41 điểm trong nhà hoặc có phần trong nhà, và điểm ưu tiên vẫn giữ chỗ dù mưa, nên ngày mưa to vẫn có thể toàn điểm ngoài trời; lúc đó chỉ còn dòng "Nếu mưa".

**Vì sao cụm "phía nam xa" chỉ xếp khi đi từ 3 ngày, và không ở ngày 1?** Chủ dự án chọn luật "từ 3 ngày" lúc làm lịch bản đầu. Luật "không ở ngày 1" có từ thiết kế bản hiện nay; chương trình giữ một tham số chỉ để mô phỏng so có / không luật này. Ngày có điểm xa thì bộ xếp để tối nghỉ; thẻ lịch không hiện dòng nào cho buổi tối đó (bài 29). Cái giá: lịch 1–2 ngày không bao giờ có Bạch Mã, đèo Hải Vân.

**Vì sao điểm lấp đi theo thứ tự dòng trong bảng?** Khi hết điểm ưu tiên và điểm hợp sở thích, bộ xếp lấy di tích theo đúng thứ tự dòng của bảng điểm, nên thứ tự dòng quyết định ngày 3 của lịch ví dụ có Bao Vinh. Vì sao thứ tự dòng là như vậy: chưa thấy ghi lý do. Điều thấy được: chương trình không có cột xếp hạng nào khác cho điểm lấp.

**Vì sao điểm đầu buổi sáng phải còn một "bạn chiều" cùng cụm hoặc cụm kề?** Để buổi chiều không phải lấp bằng điểm ngoài sở thích. Luật có từ một lần sửa ngày 06/11 của bản đầu (sửa hai loại lỗi lịch bằng chương trình) và được giữ. Mô phỏng lần đầu thấy 2 / 960 khung thiếu điểm ưu tiên số 1 vì điểm đó chỉ hợp buổi chiều.

## Giới hạn đã biết

- Ca "đi rồi quay lại cùng khu": 104 trên 960 cách điền biểu mẫu có ít nhất một ngày như vậy, tính cả buổi tối (17/11); bảng "Đã so" đếm theo ngày, chỉ ban ngày, nên ra 65. Giữ giới hạn từ 20/11.
- Phút đi theo cụm, không phải đường thật; chỉ in giữa hai điểm cùng buổi.
- Chưa có giờ tới, giờ về; ngày đầu và cuối vẫn đủ buổi.
- Ngày mưa to vẫn có thể toàn điểm ngoài trời (181 / 300 ngày mưa không chọn sở thích ở phép đếm 17/11).
- Lịch mặc định 1 ngày có một điểm đầm phá buổi chiều, giờ 13:30 – 16:00 trong khi bảng ghi đẹp nhất lúc hoàng hôn; chủ dự án chọn giữ ngày 17/11.
- Điểm lấp ngoài sở thích không có nhãn trên thẻ lịch.
- Nguồn "Lịch bạn đang có" đưa cho model ở câu hỏi tiếp (bài 27), và câu lịch sử của lượt biểu mẫu, ghi kiểu đi ĐÃ LƯU, không ghi mức xếp thật: nhóm hạn chế để trống kiểu đi thì nguồn ghi "đi cân bằng" (câu lịch sử không nhắc kiểu đi), chọn mức nào thì cả hai ghi mức đó (đọc từ chương trình, chưa thử thật; chưa biết model có nhắc lại không). Nhóm hạn chế chọn một mức khác "nhẹ nhàng" thì bản sao chép và file chữ có hai dòng nói khác nhau: dòng đầu (tóm tắt biểu mẫu) ghi mức đã chọn, dòng "Mình hiểu" ngay dưới ghi "đi nhẹ nhàng". File .txt: thấy ở ca chọn "Cân bằng" (dòng đầu "… · 1 trẻ em · cân bằng", dòng "Mình hiểu: … đi nhẹ nhàng."), tải một lần trên trình duyệt chiều 23/11, do một agent con chạy, chưa có người thứ hai kiểm; bản sao chép và ca "khám phá nhiều": đọc từ chương trình, chưa thử.

## Chi tiết để tra

- Ngày đi làm đổi lịch theo thứ và mùa (mục "Nếu… thì sao"). Chưa có ngày đi thì điểm có thứ đóng cửa vẫn được xếp, vì đa số ngày nó mở; điểm chỉ mở vài tối trong tuần thì không xếp.
- Thứ tự xét của lịch ví dụ: Đại Nội, chùa Thiên Mụ, lăng Tự Đức, lăng Khải Định (ưu tiên "di tích"), rồi các điểm di tích còn lại theo thứ tự bảng. Không chọn sở thích thì danh sách ưu tiên "chung" cũng là bốn điểm này.
- Hai sở thích: thứ tự xét là xen kẽ A1, B1, A2, B2…; một điểm hợp cả hai chỉ xét một lần ở vị trí sớm nhất.
- Giờ mở cửa: điểm mở muộn hơn giờ bắt đầu thì dời tới giờ mở; giờ kết thúc vượt giờ đóng thì không thêm điểm đó. Điểm kho không ghi giờ thì không ràng buộc.
- Hoạt động tối "diễn mọi tối" được lặp lại khi hết lựa chọn mới, kèm nhãn "có thể đi lại". Điểm tối là buổi diễn (loại lễ hội – nghệ thuật) mà chưa có ngày đi thì có nhãn "kiểm lịch diễn trước khi đi".
- Ghi chú do chương trình viết theo mã: chưa chọn kiểu đi, nhóm hạn chế, chưa chọn sở thích, điểm thay vì bậc thang, thiếu điểm ưu tiên, tạm dừng theo mùa, bậc thang, mùa mưa, giờ gợi ý. Model không viết câu nào trong phần ghi chú.
- Chữ đầu thẻ của nhóm hạn chế (sửa 23/11, ở nhánh chính 13:47). Lịch của đoàn có trẻ em hay người lớn tuổi từ trước vẫn xếp nhẹ nhàng; bản sửa không chạm bộ xếp, chỉ đổi chữ ở những nơi lấy lại đầu thẻ. Hai ca: (T) để trống ô kiểu đi — mặc định của biểu mẫu; (C) chọn "cân bằng" hay "khám phá nhiều". Ví dụ (T), 2 người lớn, 1 trẻ em, 2 ngày, trước: "Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · đi cân bằng", ô "Thời gian" "2 ngày · cân bằng", và hai câu ghi chú liền nhau nói ngược nhau ("Chưa chọn kiểu đi nên mình xếp mức cân bằng." rồi "Đi cùng trẻ em hoặc người lớn tuổi nên mình xếp nhẹ nhàng: mỗi buổi một điểm, không xếp buổi tối."). Từng nơi dòng chữ xuất hiện (đọc từ chương trình; trên trình duyệt: ảnh thẻ ca (T) trước / sau chụp bằng script, rồi một lượt chiều 23/11, do một agent con chạy, chưa có người thứ hai kiểm, thấy đúng cột "Nay" ở ba hàng đầu cho cả (T) lẫn (C) chọn "cân bằng", và ở hai hàng file .txt cho ca (C); các hàng khác chưa ai nhìn):

| Nơi hiện | Trước bản sửa | Nay | Căn cứ |
|---|---|---|---|
| dòng "Mình hiểu…" trên thẻ (và trong chữ trả lời ở khung Trợ lý) | (T) "đi cân bằng" · (C) mức đã chọn | "đi nhẹ nhàng" ở cả hai ca | dòng dựng từ tham số đầu thẻ |
| ô "Thời gian" ở đầu thẻ | (T) "… · cân bằng" · (C) mức đã chọn | "… · nhẹ nhàng" | đọc tham số đầu thẻ |
| mục ghi chú của lịch | (T) câu "Chưa chọn kiểu đi…" + câu nhẹ nhàng · (C) chỉ câu nhẹ nhàng | chỉ câu nhẹ nhàng | danh sách giả định của bộ xếp |
| bản in | giấu dòng "Mình hiểu"; vẫn in ô "Thời gian" (ghi như thẻ) | ô "Thời gian" ghi "nhẹ nhàng" | khối in của trang |
| dòng ĐẦU của bản sao chép / file .txt (tóm tắt biểu mẫu) | (T) không có kiểu đi · (C) mức đã chọn | không đổi | tóm tắt dựng từ lựa chọn trên biểu mẫu |
| dòng "Mình hiểu" trong bản sao chép / file .txt | như thẻ | "đi nhẹ nhàng" (bỏ đuôi "sai thì bấm Sửa") | lấy chữ trả lời của lượt |
| trang bìa PowerPoint | tóm tắt = dòng "Mình hiểu" | "đi nhẹ nhàng" | bìa cắt từ dòng "Mình hiểu" |
| câu lịch sử của lượt biểu mẫu | (T) không nhắc kiểu đi · (C) "đi cân bằng" / "đi khám phá nhiều" | không đổi | câu ghép từ giá trị biểu mẫu |
| nguồn "Lịch bạn đang có" đưa cho model | (T) "đi cân bằng" · (C) mức đã chọn | không đổi | tham số lịch đã lưu |

Lịch đã lưu giữ lựa chọn của người dùng: lệnh sửa bỏ trẻ em khỏi đoàn thì kiểu đi cũ dùng lại. Tìm ra: một lượt trình duyệt do công cụ tự lái đầu chiều 23/11 thấy hai câu ghi chú liền nhau; một lượt khác lúc 13:30 thấy lại "đi cân bằng" ở đầu thẻ. Kiểm: một file test mới ba ca (nhóm hạn chế với kiểu đi trống / cân bằng / khám phá nhiều; đoàn thường như cũ), người viết code chạy, người viết bài không chạy; ảnh thẻ trước (13:08) và sau (13:45), ca (T), chụp bằng script trên máy chủ thật. Sau bản sửa, file .txt của ca (C) "cân bằng" đã được tải một lần trong lượt đó; file .txt ca (T), nút sao chép, PowerPoint và bản in chưa ai thử.
- Các biến thể ở mục "Đổi một ô": người viết chạy bộ xếp trưa 22/11 trên bảng 41 điểm đang chạy; mọi lịch qua bước kiểm khung với 0 lỗi.

**Bài sau (bài 29):** khi yêu cầu không xếp được thì sao, bước kiểm lịch kiểm những gì, và phần việc nhỏ của model được kiểm thế nào.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Luật và thứ tự ưu tiên: docstring đầu `backend/llm/lich_trinh_v2.py` (bậc 1–7, "Số người lớn không vào bộ xếp", "Buổi tối xếp ở bước (e)"); `xep_v2` (`thu_tu_xet`, `_xen_ke`, `dung_duoc`, `tranh_bac_thang`, `diem_dau` — luật "bạn chiều" B171, chú thích "2 / 960 khung"; vòng thêm điểm với `NGHI_TRUA`), `_xep_toi` (`CUM_TOI`, không lặp, `CAU_TOI`), `dat_gio`, `tam_dung`, `dung_thu`, `CAU_GHI_CHU` [code].
- Hằng số: `PHUT` 75 / 150, `DI_CUNG_CUM` 15, `DI_CUM_KE` 30, `QUY` 210 / 240, `TOI_DA_BUOI` 2, `GIO_BAT_DAU`, `NGHI_TRUA` 60 (chú thích "tự thử 16/11: 15 phút từ Kinh thành ra phá"), `NGUONG_MUA` 60, `MM_MUA_XEP` 6 (chú thích "User 15/11… 222 / 365"), `SO_NGAY_TOI_DA` 5, `NGUONG_LOAI` 4 — `lich_trinh_v2.py`; `CUM_KE_GOC`, `CUM_XA` ("Quyết 2 của User"), `_cum_hop` — `backend/llm/lich_trinh.py` [code].
- Phép thử số 165 / 180 / 240 / 255, "đúng ý: không nhồi", giờ chiều sớm 30 phút vì kho không ghi giờ ngừng bán vé, xong muộn nhất 17:00, mô phỏng 180 lịch, luật "đi dày" 3 / 120, bản nháp giờ 8:00 – 11:00 / 14:00 – 17:00: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` mục 5c.3 và bảng 3.1–3.2 [chép].
- Luật nhóm hạn chế và hệ thống khác (xếp sau giờ đóng, 5–6 điểm / ngày khi có người lớn tuổi): `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` (phần nền, D3, D4) [chép]. Hoạt động tối nhẹ cho nhóm hạn chế "nếu bảng đánh dấu hợp gia đình": spec mục 3.2, dòng Buổi tối [chép]. Buổi để trống không hiện từ 15/11: `lich_trinh_v2.py` (`ghep_chu`, chú thích "User 15/11") [code].
- Lịch ví dụ: `data/hoc_cung_D/vi_du_lap_lich_vet.json` (`lich.v2_khung`) [riêng tư; đã chạy]. Người viết chạy lại `xep_v2` + `kiem_khung_v2` + `dung_lich` trên `data/phase_9/lich_trinh/diem_v10.json` trưa 22/11 bằng `uv run --no-sync python` (không mạng, không model): lịch ví dụ ra giống từng điểm, từng giờ của vết; năm biến thể ở mục "Đổi một ô" là kết quả của lần chạy đó, 0 lỗi khung [đã chạy, riêng tư].
- Bản đầu 7 / 28, 0 / 120; 52 / 3.840; 26 ngày trên 960 cách điền (mẫu số 2.879 chỉ có ở bài cũ 23, bỏ), 4.800 lịch, 130 (`data/lich_nho_2026-11-17/README.md`, người kiểm đối chiếu); mưa 106 ⇒ 15, 32 ngày, 30 / 32, 80 % ⇒ 50 %; 3.880 lịch, 100 đổi, 109 ⇒ 0 / 300, 253 ⇒ 181; 12 / 41 điểm trong nhà; bảy điểm mới và bảng phần trăm; 104 / 960, 8 / 960 và bản sửa hẹp: `bai_hoc/23_LEN_KE_HOACH_BAN_2.md` (các mục "Quay lại người hướng dẫn viên", "Bản 2 làm gì", "Một chuyện thật", "Chiều 15/11", "Khi nào hỏng" và khối nguồn của bài đó, trỏ tới `report_agent/2026-11-12_ra_khoang_cach/…` và `data/dem_lich_2026-11-17/`, `data/di_lai_2026-11-17/`) [chép; người viết không mở lại các report gốc].
- Giữ giới hạn "quay lại" (phiên điều phối chốt 20/11), phút đi phá Tam Giang, lịch mặc định 1 ngày (chủ dự án chọn giữ 17/11), chưa có giờ tới / về: `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 [chép].
- Điểm lấp không có nhãn trên thẻ: `frontend/src/LichV2.jsx` (`NHAN_MUC_V2` chỉ có "có thể đi lại", "kiểm lịch diễn") và `lich_trinh_v2.py` (`NHAN_MUC`) [suy từ code, chưa thử trên giao diện].
- Bảng khoảng cách dựng 16/11, bộ xếp bật 14/11: `settings.yaml` (`khoang_cach_bang`, `len_ke_hoach_v2`) [chép]. "Công cụ này KHÔNG đổi lịch — lịch vẫn dùng phút theo cụm": `docs/superpowers/plans/2026-11-16-khoang-cach-plan.md` dòng 32 [chép]. Bộ xếp không đọc bảng khoảng cách: `_phut_di` [code].
- Luật "bạn chiều" có từ B171, đóng tối 06/11: `report_agent/README.md` dòng 37, `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` dòng 1–3 [chép, theo biên bản kiểm].
- "Chưa thấy ghi lý do" cho 75 / 150, số 2 cụm, 15 / 30 phút: đã dò spec mục 5c.3, plan B5 (D4), chú thích `lich_trinh.py` §2b, bài cũ 23.

- Bài đã qua một lượt đối chiếu độc lập (người kiểm chỉ đọc, tự chạy lại bộ xếp và phần áp lệnh), trưa 22/11/2026: `data/hoc_cung_D/kiem/bai_27_32.md` [riêng tư]; các dòng SAI / LỆCH đã áp, dòng không áp ghi ở `data/hoc_cung_D/viet/viet_27_32.md` mục "Sau lượt kiểm" [riêng tư].

- Hai cách đếm ca "quay lại cùng khu" (phân xử 22/11): 104 là số KHUNG có ít nhất một ngày đi cụm X → cụm khác → X, xét cả sáng, chiều, tối (`data/dem_lich_2026-11-17/dem_quay_lai.py`, vòng `seq` gồm ba buổi) [riêng tư; đọc code đếm, không chạy lại]; 65 là số NGÀY có mẫu X…Y…X chỉ trong sáng + chiều (`data/di_lai_2026-11-17/tools/dem.py`, `ds = sang + chieu`; README bảng main `4195a42`) [riêng tư; đọc code đếm, không chạy lại].

- Đợt 14:08 23/11/2026 (V2 đầu chiều; người viết đọc cây chính `64f188fa`, không chạy test, không chạy server). Dòng Cập nhật trước (16:11 22/11): "phân xử chỗ lệch giữa các bài · trước đó: đã sửa theo một lượt đối chiếu độc lập · luật và hằng số đọc từ chương trình trưa 22/11; lịch ví dụ là lượt thật ngày 21/11 (Claude Sonnet 5.5); các biến thể ở mục "Đổi một ô" do người viết chạy riêng bộ xếp trên bảng điểm đang chạy (chỉ chương trình, không gọi model, không tốn tiền); các con số đo cũ chép từ báo cáo gốc."
  - Bỏ câu "Chưa chọn kiểu đi…" cho nhóm hạn chế: `backend/llm/lich_trinh_v2.py` hàm `xep_v2`, dòng `gia_dinh = (["kieu_di"] if ts.kieu_di is None and not ts.han_che else [])` + chú thích ngày 23/11 (commit `8ab947e4`, 13:28) [code]. Đầu thẻ ghi "nhẹ nhàng": hàm `dung_lich`, khối `if ts["tre_em"] >= 1 or ts["lon_tuoi"]: ts = {**ts, "kieu_di": "nhe_nhang"}` + chú thích "Chỉ đổi chữ HIỆN RA: tham số lưu trong khung giữ nguyên lựa chọn của người dùng (bỏ trẻ nhỏ khỏi đoàn bằng lệnh sửa thì kiểu đi cũ dùng lại)" (commit `048bd76d`, 13:44; gộp `9c7196b2` 13:47) [code]. Câu ghi chú nguyên văn: `CAU_GHI_CHU` (`kieu_di`, `han_che`); "đi …": `dong_minh_hieu_v2`, `NHAN_KIEU_DI`; ô "Thời gian": `frontend/src/LichV2.jsx` dòng 181 (`KIEU_V2[ts.kieu_di]`) [code].
  - Bộ xếp không đổi: `xep_v2` dòng `quy = None if ts.han_che else QUY[kieu]` ("nhóm hạn chế: trần là nhẹ nhàng") không nằm trong diff của hai commit (`git show 8ab947e4 048bd76d -- backend/llm/lich_trinh_v2.py`) [đã chạy lệnh git]. Lịch lưu giữ lựa chọn: `backend/llm/sua_lich_v2.py` dòng 422 (`"tham_so": copy.deepcopy(khung["tham_so"])`), `xep_v2` trả `"kieu_di": kieu` (= lựa chọn, trống thì `KIEU_DI_MAC_DINH` "can_bang") [code]. Bảng "từng nơi dòng chữ xuất hiện" (áp biên bản `data/hoc_cung_D/kiem/dot_2311_chieu_k2_kiem.md` bài 28 hàng 5, 6, lượt áp 14:30 23/11) [code, người viết đã mở từng chỗ]: dòng "Mình hiểu" `dong_minh_hieu_v2` gọi trong `dung_lich` sau khối 23/11; chữ trả lời có dòng đó: `lich_trinh_v2.py` dòng 779; ô "Thời gian": `frontend/src/LichV2.jsx` dòng 181 (`lich.tham_so`); bản in: `frontend/src/lkh.css` dòng 295 (giấu `.lich-hieu`), khối `.lkh-thanh` trong `@media print` dòng 304, 320–321 (vẫn in); dòng đầu bản sao chép / .txt: `LichV2.jsx` `vanBanLich` (`turn.question + turn.summary`, rồi `answerText` bỏ đuôi "sai thì bấm Sửa"), `frontend/src/App.jsx` dòng 92 (chú thích "dòng đầu … là tóm tắt biểu mẫu"), `frontend/src/LenKeHoach.jsx` dòng 165, 169–176 (`tomTat` lấy `truong.kieu_di` chỉ khi có chọn); file thật trước sửa: `data/playwright_mcp/luot_2311_toi_nhe/D_lich_goc_the_chat.txt` dòng 1 "Lên kế hoạch tham quan Huế · 2 ngày · 2 người lớn · 1 trẻ em", dòng 3 "Mình hiểu: … · đi cân bằng." (ca T) [riêng tư; đã mở]; bìa PowerPoint: `backend/api/lich_pptx.py` dòng 62; câu lịch sử: `backend/llm/hoi_lai.py` `ghep_cau_v2` (chỉ thêm "đi …" khi `moi.get("kieu_di")`), gọi ở `backend/api/routes/chat.py` dòng 254; nguồn cho model: `dong_lich_dang_co` (`luu["tham_so"]`). Ca (C) ở bản sao chép, PowerPoint, nguồn cho model: [suy từ code, chưa thử].
  - Giới hạn nguồn "Lịch bạn đang có": `dong_lich_dang_co` dựng dòng "Tham số của lịch" từ `luu["tham_so"]` (= tham số lưu, kiểu đi đã chọn hoặc "can_bang"); `assistant.py` dòng 1337; `settings.yaml` `lich_vao_hoi_thuong: true` [suy từ code, chưa thử].
  - Test: `backend/tests/test_ghi_chu_kieu_di.py` (ba ca: nhóm hạn chế không chọn kiểu đi chỉ có câu nhẹ nhàng; đoàn thường giữ câu mặc định, chọn kiểu đi thì không có; đầu thẻ ghi nhẹ nhàng với `None`, `can_bang`, `kham_pha` và tham số khung giữ lựa chọn) [code; "the schedule test files pass" là lời commit `8ab947e4` — đã chạy, phiên khác; người viết không chạy].
  - Ảnh: trước `data/thu_bedrock_2026-11-21/harness/c_toi_nhe_2311/anh2/truoc_ca1_tre_em_1536.png` (giờ file 13:08: "Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · đi cân bằng", "2 ngày · cân bằng", hai câu ghi chú liền nhau) · sau `…/anh_ghi_chu/sau_ca1_tre_em_1536.png` (13:45: "đi nhẹ nhàng", "2 ngày · nhẹ nhàng", chỉ câu nhẹ nhàng) [riêng tư; đã mở cả hai]; biểu mẫu của ca: `…/chup_the.py` docstring ("biểu mẫu mặc định 2 ngày + 1 trẻ em") [đã mở].
  - Lượt tìm ra: `data/playwright_mcp/luot_2311_toi_nhe/NHAT_KY.md` (bắt đầu 13:03, mục "Điều lạ" 6(a) "hai dòng ghi chú liền nhau …") ; lượt 13:30: `data/playwright_mcp/luot_2311_them_day/NHAT_KY.md` bước G (1) ("Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · đi cân bằng") [riêng tư; đã mở]. Lời gộp `9c7196b2` ghi "Found by the browser pass at midday"; nhật ký lượt trưa `luot_2311_trua` không có điều này (bước A là đoàn 2 người lớn) [đã mở; ghi lệch ở báo cáo].

- Nâng nhãn 15:40 23/11/2026 (giờ `date`): "Giới hạn đã biết" gạch "Nguồn Lịch bạn đang có…" (phần hai dòng) và "Chi tiết để tra" gạch "Chữ đầu thẻ của nhóm hạn chế" (câu dẫn bảng chín nơi, câu cuối) — `data/playwright_mcp/luot_2311_chieu_main/NHAT_KY.md` mục (1) hàng D1 (1 trẻ em, không chọn kiểu đi: "Thời gian 2 ngày · nhẹ nhàng", "Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · đi nhẹ nhàng — sai thì bấm Sửa.", ghi chú mở bằng câu nhẹ nhàng, không còn câu "Chưa chọn kiểu đi…"), hàng D2 (cùng đoàn, CHỌN "Cân bằng": trang như D1) và hàng D2 "Tải về (.txt)"; mục (2) hàng "(4) Lịch đoàn có trẻ nhỏ"; mục (3) điều lạ 1; mục (4) gạch "Không tải .txt của lịch D1" [riêng tư; đã mở trọn; người chạy: agent con của phiên điều phối, máy chủ tạm 8017, 15:20–15:21; chưa có người thứ hai kiểm]. File tải về `luot_2311_chieu_main/D_lich_tre_em_can_bang.txt` dòng 1 "Lên kế hoạch tham quan Huế · 2 ngày · 2 người lớn · 1 trẻ em · cân bằng", dòng 3 "Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · đi nhẹ nhàng." [riêng tư; người viết đã mở]; ảnh `D_dau_the_tre_em_1536.png` (bước D1: "2 ngày · nhẹ nhàng", dòng "Mình hiểu… đi nhẹ nhàng — sai thì bấm Sửa.") [riêng tư; đã mở xem]. Lượt không thử "khám phá nhiều", "Có người lớn tuổi", nút sao chép, PowerPoint, bản in. Dòng Cập nhật trước: "Cập nhật 14:30, ngày 23/11/2026 · khớp hệ thống 13:52 23/11 (50 tính năng mở, 5 tắt, kho 267 bài) · đầu thẻ lịch của nhóm hạn chế ghi "nhẹ nhàng" · lịch ví dụ là lượt thật 21/11 (Claude Sonnet 5.5); biến thể "Đổi một ô" do người viết chạy bộ xếp, không gọi model · dòng cũ: Nguồn."

- Đợt cuối chiều 23/11/2026 (Việc 1 của lời giao đợt): câu "Ngoại lệ: ngày người dùng tự xin thêm điểm…" ở "Ý chính" và hàng "số điểm tối đa" — `backend/llm/lich_trinh_v2.py` `kiem_khung_v2` (`TOI_DA_BUOI + (1 if day else 0)`; `not day and … vuot_quy`; `day_them = set() if han_che`), `xep_v2` không đổi (`git show a02586fa -- backend/llm/lich_trinh_v2.py` chỉ thêm hằng số, `ngay_vuot_nhip`, `cau_ngay_day`, `gio_ngay_day`, nhánh `day_them` của `kiem_khung_v2` và một dòng của `dung_lich`); mốc 15:38: `git show --stat a02586fa` [code]. Chỉ hai file dùng dấu ngày dày: `git grep -n "day_them" origin/main -- backend/llm` chỉ ra `lich_trinh_v2.py` và `sua_lich_v2.py` [code]. Dòng Cập nhật trước: "Cập nhật 15:40, ngày 23/11/2026 · khớp hệ thống 15:29 23/11 (50 tính năng mở, 7 tắt, kho 267 bài) · nâng nhãn theo lượt trình duyệt chiều 23/11 · lịch ví dụ là lượt thật 21/11 (Claude Sonnet 5.5); biến thể "Đổi một ô" do người viết chạy bộ xếp, không gọi model · dòng cũ: Nguồn."
- Áp biên bản kiểm độc lập (`data/hoc_cung_D/kiem/dot_2311_chieu2_k1_kiem.md` mục "Bài 28" dòng 1, 2 [riêng tư]): "chỉ đoàn không có trẻ nhỏ / người lớn tuổi" — `kiem_khung_v2` `day_them = set() if han_che`, `sua_lich_v2._xep` `[] if ts.han_che` [code]; ba trần và 60 phút: `GIO_KET_SANG_DAY`, `GIO_KET_CHIEU_DAY`, `NGHI_TRUA`, `day_qua_gio` [code]. Lịch ví dụ ở thân bài (lượt thật 21/11) có Chợ Đông Ba buổi tối — từ 16:38 23/11 bảng điểm mới không còn; chưa sửa ở đợt này (chờ phiếu buổi tối). Dòng Cập nhật trước: "Cập nhật 16:37, ngày 23/11/2026 · khớp hệ thống 16:23 23/11 (51 tính năng mở, 7 tắt, kho 267 bài) · một câu trỏ sang bài 31: ngày người dùng tự xin thêm điểm được vượt quỹ và trần 2 điểm một buổi · lịch ví dụ là lượt thật 21/11 (Claude Sonnet 5.5); biến thể "Đổi một ô" do người viết chạy bộ xếp, không gọi model · dòng cũ: Nguồn."
</details>
