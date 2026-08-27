# Language & Keyword Quality Audit — Golden Dataset V2

> **Historical audit input:** Findings này đã góp phần dẫn tới Golden Dataset V3
> complexity reset; không dùng để tiếp tục ép correction theo quota V2.

Reviewer: Codex
Date: `2026-08-27 +07`
Scope: toàn bộ 100 rows trong `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`
Status: rubric đã được user xác nhận; dùng làm canonical input cho correction tiếp theo

## 1. Nguyên tắc đề xuất

### Question

- Viết như một người dùng Việt Nam thực sự hỏi trợ lý du lịch/ẩm thực.
- Mỗi câu có một intent chính. Chỉ ghép hai ý khi chúng có quan hệ tự nhiên,
  chẳng hạn địa chỉ + không gian của cùng một quán.
- Không thêm “theo cẩm nang”, “theo mô tả trong tài liệu” nếu người dùng không
  thực sự cần giới hạn theo một tài liệu cụ thể.
- Không để tên entity tiết lộ luôn đáp án đang hỏi.
- Reference chỉ trả lời đúng phạm vi câu hỏi; không thêm chi tiết ngoài source
  hoặc chi tiết không được hỏi chỉ để chứa keyword.

### Keywords

- Dùng 2–4 semantic anchors; không cố đạt bốn.
- Ưu tiên tên món, tên quán/thương hiệu và thuộc tính trực tiếp trả lời intent.
- Với câu hỏi địa chỉ: nên có tên entity + địa chỉ chính; phường, landmark chỉ
  thêm khi chúng có giá trị phân biệt.
- Với giờ/giá: dùng tên entity hoặc chi nhánh + giờ/giá; không dùng địa chỉ nếu
  địa chỉ không cần để phân biệt chi nhánh.
- Với comparative: dùng hai entity/món và 1–2 điểm khác biệt chính.
- Với spanning/planning/holistic: ưu tiên tên món/quán hoặc các chặng của kế
  hoạch, không dùng bốn địa chỉ như proxy cho nội dung câu trả lời.
- Loại keyword trùng lặp, quá chung, nguyên câu dài hoặc từ viết tắt không cần
  thiết. Tên thương hiệu chính thức và đơn vị chuẩn là ngoại lệ hợp lý.

User xác nhận ngoại lệ cuối cùng: giữ nguyên tên thương hiệu chính thức như
`AEON MALL`, `KOI Thé`, `ANH KAFE` và đơn vị chuẩn như `VNĐ`; loại hoặc viết đầy
đủ các từ viết tắt mô tả không cần thiết như `CNN`, `BBQ`, `TTTM`, `TP`.

Theo quyết định bổ sung của user, Implementer được phép research trên internet
về quán ăn, đồ uống, món Huế và nhu cầu du lịch Huế để kiểm tra cách hỏi tự
nhiên, phát hiện mâu thuẫn hoặc thông tin có thể đã thay đổi, rồi báo cáo và thảo
luận với Reviewer/user. Web không tự trở thành Golden evidence: mọi sửa
reference/keywords/evidence vẫn phải dựa trên curated corpus, trừ khi user phê
duyệt riêng việc cập nhật corpus sau khi xem nguồn và mâu thuẫn được báo cáo.

## 2. Sáu ví dụ user nêu — hướng sửa đề xuất

| Case | Nhận định | Hướng sửa |
|---|---|---|
| `foods-0098` | Địa chỉ không phải semantic keywords của intent lập lịch; hai khoảng giờ trong reference không có source | Question: “Nếu chỉ có nửa ngày buổi sáng ở Huế, tôi nên ăn bún bò và uống cà phê ở đâu?” Keywords: `Quán bún bò Mệ Kéo`, `Bún bò Hạnh`, `The Lab Coffee Huế`, `MoKa KaFe`. Bỏ hai khoảng giờ khỏi reference. |
| `foods-0006` | Địa chỉ là đáp án trực tiếp nên hợp lệ, nhưng nên có entity name | Keywords: `Bánh ép Gia Di`, `4 Phùng Chí Kiên`, có thể bỏ `Xuân Phú` để giữ hai anchor rõ nhất. |
| `foods-0008` | Tên quán đã chứa `17 Hàn Mặc Tử`, gần như tiết lộ câu trả lời | Question: “Quán Cơm Hến 17 Hàn Mặc Tử thuộc phường nào của thành phố Huế?” Keywords: `Cơm Hến 17 Hàn Mặc Tử`, `phường Vỹ Dạ`. Reference phải nhắc lại tên quán thay vì chỉ viết “Quán”. |
| `foods-0087` | Keywords toàn địa chỉ; scope “ăn vặt, món ngọt” không chứa cơm hến | Nếu giữ bốn địa điểm: hỏi “Đi Huế cùng nhóm bạn thì nên ghé đâu để ăn món địa phương, ăn vặt và món ngọt?” Keywords: `Bánh ép Huệ`, `Quán Bà Cư`, `Cơm hến Hoa Đông`, `Chè Hẻm Huế`. |
| `foods-0059` | Câu hỏi không được answer phần “trải nghiệm”; `CNN` không cần làm keyword | Nên viết lại thành holistic case thật sự, ví dụ lịch sử + không gian của quán gốc, bổ sung đúng section trải nghiệm. Keywords đề xuất: `Quán Cà Phê Muối gốc`, `năm 2010`, `không gian hoài cổ`, `khoảng sân mở`. |
| `foods-0084` | Ghép danh sách món nên thử với đặc trưng hai loại nước dùng là hai intent rời | Question: “Lần đầu đến Huế nên thử những món ăn tiêu biểu nào?” Keywords: `bún bò Huế`, `cơm hến`, `bánh canh Nam Phổ`, `chè heo quay`. Reference bỏ phần giải thích nước dùng hoặc chuyển nó sang case food-knowledge riêng. |
| `foods-0041` | Thiếu subject entity, còn street + ward bị dùng đồng thời | Keywords: `DeChill`, `102 Huyền Trân Công Chúa`, `Đồi Vọng Cảnh`; bỏ `Phường Thủy Xuân` nếu không cần chấm chi tiết hành chính. |
| `foods-0044` | Cấu trúc sở hữu bị ngược và bỏ sót vị trí bên trong trung tâm thương mại | Question: “Chi nhánh KOI Thé nằm ở đâu trong AEON MALL Huế?” Keywords: `KOI Thé`, `lô T133, tầng 1`, `AEON MALL Huế`. Reference viết đầy đủ “trung tâm thương mại”, không dùng `TTTM`. |

## 3. Nhóm phải rewrite hoặc thay case

| Case | Vấn đề chính | Hướng correction |
|---|---|---|
| `foods-0008` | Entity name tiết lộ địa chỉ | Chuyển intent sang hỏi phường hoặc thay direct fact khác. |
| `foods-0023` | Hỏi giá một tô nhưng answer/keywords thêm khoảng giá món khác | Chỉ giữ `Quán Thúy`, `bánh canh Nam Phổ`, `20.000 VNĐ`. |
| `foods-0028` | Sai tên thương hiệu: dataset ghi `Cơm Niêu Chân`, source là `Nhà hàng cơm niêu Chạn` | Sửa toàn bộ question/reference thành `Chạn`; keyword có tên nhà hàng và các món tiêu biểu. |
| `foods-0039` | Ghép nguồn gốc bánh với cách ướp thịt, hai intent không liên quan | Chỉ hỏi cách ướp thịt ba chỉ; hoặc chỉ hỏi nguồn gốc, tránh trùng `foods-0062`. |
| `foods-0040` | Hỏi “nhân và gia vị” nhưng answer chủ yếu liệt kê nhân | Hỏi “Bánh mì Đông Ba thường có những loại nhân nào?”. |
| `foods-0044` | Câu hỏi đảo quan hệ KOI Thé/AEON MALL | Dùng wording ở mục 2 và thêm `lô T133, tầng 1`. |
| `foods-0053` | “Gắn liền với thương hiệu sáng lập nào” mơ hồ và reference không trả lời | Hỏi “Quán Cà Phê Muối gốc ra đời năm nào và có những cơ sở nào ở Huế?”. |
| `foods-0054` | “Con đường lịch sử” là claim không được source chứng minh; câu ghép gượng | Hỏi “Giao Cafe nằm ở đâu và có phong cách không gian như thế nào?”. |
| `foods-0059` | Holistic question/reference không khớp, keyword `CNN` không cần thiết | Viết lại thành lịch sử + trải nghiệm/không gian, khai báo section tương ứng. |
| `foods-0062` | Hỏi nguồn gốc nhưng answer/keywords thêm cách chế biến | Chỉ hỏi/trả lời nguồn gốc; keywords `bánh ép Huế`, `vùng biển Thuận An`. |
| `foods-0063` | Hỏi lá gói nhưng answer/keywords thêm nhân và tuyệt đối hóa bột gạo tẻ | Chỉ giữ lá dong/lá chuối và cách gói-hấp; không dùng `bột gạo tẻ`. |
| `foods-0072` | `banh nam.md :: Tóm tắt` không chứng minh “bột gạo tẻ”; source chi tiết nói công thức thay đổi | Mô tả bánh nậm là lớp bột mỏng gói lá rồi hấp, không tuyệt đối hóa loại bột. |
| `foods-0073` | Answer diễn đạt lủng củng; keywords lặp `mắm ruốc` và bỏ tên hai món | Keywords: `mắm ruốc Huế`, `bánh canh Nam Phổ`, `bún bò Huế`, `cơm hến`; viết lại answer theo ba món. |
| `foods-0075` | “Ý nghĩa kết hợp nguyên liệu” mơ hồ và không được answer | Hỏi “Cơm âm phủ được trình bày như thế nào và thường gồm những thành phần gì?”. |
| `foods-0080` | Câu quá dài, keyword `cắt hạt lựu`, `nước sôi`, `đường phèn` thiếu ngữ cảnh | Hỏi “Chè bột lọc heo quay được làm như thế nào?”; dùng `thịt heo quay`, `bột năng`, `nước đường phèn gừng`. |
| `foods-0083` | Ghép hai nhu cầu độc lập: mở khuya hoặc gần ga | Chọn một intent, ưu tiên các quán cà phê mở đến 24:00; bỏ CỦI Coffee hoặc tạo case khác nếu matrix cho phép. |
| `foods-0084` | Hai intent không tự nhiên | Chỉ hỏi món nên thử như mục 2. |
| `foods-0087` | Scope món ăn vặt/ngọt không bao gồm cơm hến | Mở scope thành món địa phương + ăn vặt + món ngọt, hoặc bỏ cơm hến. |
| `foods-0090` | Hỏi danh sách thương hiệu/địa chỉ nhưng gán `food_knowledge` để lấp quota | Thay bằng food-knowledge case thật, ví dụ điểm chung về cách làm/thưởng thức của bánh bèo, bánh nậm và bánh bột lọc từ guide. Không đổi category đơn thuần làm vỡ matrix. |
| `foods-0098` | Reference thêm giờ không có source; keywords sai trọng tâm planning | Dùng wording/keywords ở mục 2. |
| `foods-0100` | “Đầy đủ các món đặc sản chính” là overclaim | Hỏi đơn giản “Gợi ý lịch trình food tour 2 ngày tại Huế?” và dùng tên món/quán làm keywords. |

## 4. Nhóm nên chỉnh wording để giống người hỏi thật

| Cases | Vấn đề/hướng chỉnh |
|---|---|
| `foods-0027` | Thay “thành phần topping” bằng “món ăn kèm”. |
| `foods-0036`, `foods-0037` | Bỏ công thức “Tổng quan về…”; hỏi trực tiếp lịch sử/điểm đặc trưng của quán. |
| `foods-0042` | Câu hỏi chỉ hỏi địa chỉ nên reference không cần thêm phong cách Hanok. |
| `foods-0055` | “Đặc điểm trải nghiệm ra sao” quá chung; hỏi thẳng các loại hình trải nghiệm. Bỏ keyword `BBQ` hoặc viết “tiệc nướng”. |
| `foods-0056` | Hạn chế `hidden cafe/bar`; hỏi quán hoạt động thế nào ban ngày và ban đêm. |
| `foods-0065` | Bỏ cụm meta “theo mô tả trong tài liệu”. |
| `foods-0067` | “Cách phục vụ phần cơm/bún và nước dùng” khó hiểu; hỏi về phần tinh bột chính và cách dùng nước. |
| `foods-0079` | Rút thành “Tri thức dân gian về bún bò Huế được ghi danh là di sản gì?”. |
| `foods-0081`, `foods-0082`, `foods-0088`, `foods-0089`, `foods-0097` | Bỏ tiền tố “theo cẩm nang”; hỏi trực tiếp nhu cầu ăn uống. |
| `foods-0085`, `foods-0086` | Bỏ “Tổng quan các…”; chuyển thành câu hỏi tư vấn trực tiếp cho người ăn chay/gia đình. |
| `foods-0092` | Rút thành “Buổi trưa ở Huế có thể ăn gì và ở đâu?”. |
| `foods-0095` | Rút thành “Ở Huế có quán ăn đêm nào mở tới khoảng 2:30–3:00 sáng?”. |

## 5. Nhóm cần keyword pass có hệ thống

### Entity-specific direct/temporal/numerical cases

Các case sau đang thiếu tên entity trong keywords, dùng địa chỉ/phường thay entity,
hoặc dùng location không cần thiết cho intent giờ/giá:

`foods-0001`–`foods-0016`, `foods-0021`–`foods-0024`,
`foods-0041`–`foods-0048`, `foods-0051`, `foods-0052`.

Ngoại lệ: địa chỉ/branch identifier vẫn giữ khi cần phân biệt đúng cơ sở, ví dụ
`81 Đào Duy Từ` hoặc `5 Nguyễn Huệ`.

### Spanning/holistic/planning cases dùng địa chỉ làm proxy

Các case sau nên ưu tiên tên quán, tên món hoặc chặng của kế hoạch:

`foods-0032`–`foods-0035`, `foods-0074`, `foods-0081`–`foods-0087`,
`foods-0090`–`foods-0100`.

Địa chỉ vẫn hợp lý nếu question thực sự yêu cầu địa chỉ (`foods-0032`–`0035`,
`foods-0082`, `foods-0091`, một phần `foods-0095`), nhưng keyword set không nên
chỉ gồm các chuỗi số đường mà thiếu tên địa điểm.

### Keywords mơ hồ, trùng hoặc quá dài

- `foods-0007`: `04 Phan Bội Châu` và `Phan Bội Châu` trùng thông tin.
- `foods-0055`: `BBQ` là viết tắt không cần thiết.
- `foods-0059`: `CNN` không phải answer anchor cốt lõi.
- `foods-0069`: nên dùng `bánh canh Nam Phổ` + một cụm tỷ lệ hoàn chỉnh thay vì
  tách hai nửa tỷ lệ thành hai keywords.
- `foods-0070`: nên thêm `mè xửng Huế`; hai con số riêng không đủ ngữ cảnh.
- `foods-0073`: hai keyword về mắm ruốc bị trùng nghĩa.
- `foods-0076`: `khuấy đều`, `độ sánh đặc trưng` quá chung; nên dùng `nhân tôm
  cua`, `màu đỏ gạch`, `bột gạo`, `nước dùng sánh`.
- `foods-0080`: ba thao tác/nguyên liệu rời thiếu tên món và ngữ cảnh.
- `foods-0084`, `foods-0088`: keyword đang là các mệnh đề dài; nên tách thành
  tên món + thành phần/hương vị phân biệt.

## 6. Kết luận audit

Đã đọc đủ 100/100 rows. Vấn đề không chỉ nằm ở vài typo riêng lẻ mà là một pattern
annotation: nhiều keywords được chọn để khớp chuỗi dễ dàng thay vì đại diện cho
ý nghĩa câu trả lời. Correction tiếp theo nên là một language/keyword pass có
rubric rõ ràng, sau đó mới chạy validator và retrieval; không sửa gold để tối ưu
metric của model hiện tại.

Chưa sửa dataset, smoke subset, validator, tests hoặc implementation report trong
audit này.
