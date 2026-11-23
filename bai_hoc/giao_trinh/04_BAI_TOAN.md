# Bài 4 — Bài toán: ai dùng, hỏi gì, nhận gì, và những thứ cố ý không làm

*Cập nhật 12:56, ngày 23/11/2026 · khớp hệ thống trưa 23/11 (49 tính năng mở, 5 tắt, kho 267 bài): nối hai mốc mới vào câu kể số tính năng (giờ quán trong "gần một điểm"; hai tính năng đang tắt gộp 12:34) · bản 18:13, ngày 22/11/2026, khớp hệ thống tối 22/11 (48 tính năng, kho 267 bài): thêm thẻ nơi · phạm vi và các luật của sản phẩm chép từ các quyết định đã ghi của chủ dự án; người viết không chạy lại gì ngoài lệnh đếm tính năng.*

**Bài trước đã biết:** ba ý nền: model ngôn ngữ viết trôi chảy mà vẫn sai; RAG cho model đọc tài liệu trước khi viết; công cụ cho model nhờ chương trình làm việc phải đúng.
**Bài này thêm:** chính sản phẩm. hue_rag làm gì, cho ai, theo luật nào, và ranh giới của nó ở đâu.

## Ý chính

- hue_rag là một **ứng dụng web hỗ trợ trải nghiệm văn hoá và du lịch Huế**. Người dùng là du khách và người dân; họ gõ tiếng Việt có dấu.
- Nó làm ba việc: **trả lời câu hỏi** từ một kho bài viết đã soạn, có ghi nguồn; **làm giúp vài việc cần tính** (ngày âm lịch, thời tiết, khoảng cách); và **lên một lịch tham quan** rồi sửa lịch theo lời người dùng.
- Luật gốc của sản phẩm: **chỉ trả lời từ kho**. Kho không có thì nói không có. Ngày, khoảng cách, lịch do chương trình tính; model chỉ diễn đạt.
- Thứ tự ưu tiên do chủ dự án đặt: chất lượng trước, tốc độ và tiền sau. Trong các loại lỗi, nặng nhất là sai một cảnh báo an toàn, nhẹ nhất là từ chối nhầm.
- Có một danh sách những thứ **cố ý không làm**. Biết danh sách này quan trọng ngang biết hệ thống làm được gì.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| phạm vi | **scope** | những việc sản phẩm nhận làm, và những việc nó nói rõ là không làm |
| ngoài kho | **out of corpus** | câu hỏi về Huế mà kho không có bài nào trả lời |
| ngoài phạm vi | **out of scope** | câu hỏi không thuộc việc của sản phẩm (nơi khác, kiến thức chung, nhờ viết mã…) |
| điều kiện không được vỡ | — (hồ sơ dự án gọi là "sàn") | một điều ghi trước mà mọi thay đổi phải giữ |

## Sản phẩm là gì, cho ai

Tên đề tài: *"Xây dựng ứng dụng hỗ trợ trải nghiệm văn hóa và du lịch Huế dựa trên Retrieval-Augmented Generation"*.

Người dùng là **du khách** sắp đi hoặc đang ở Huế, và **người dân** muốn tra cứu. Họ không biết gì về kỹ thuật. Họ mở một trang web, gõ câu hỏi bằng tiếng Việt có dấu, hoặc bấm vài nút để nhờ lên lịch.

Sản phẩm được làm và đo như một sản phẩm thật cho người dùng thật, không như một bản thử ý tưởng. Hiện nó chạy trên máy của chủ dự án và chưa đưa lên mạng.

## Người dùng nhận được ba loại việc

**1. Hỏi đáp có nguồn.** Người dùng hỏi về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, đi lại, vé, chỗ ở. Hệ thống trả lời từ kho 267 bài, dưới câu trả lời có dòng nguồn bấm vào xem được đoạn gốc. Ví dụ chính của cả bộ thuộc loại này: *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"*.

**2. Việc cần tính hoặc cần dữ liệu của hôm nay.** "Rằm tháng Giêng năm nay là ngày dương nào", "mai có mưa không", "từ Đại Nội tới chùa Thiên Mụ bao xa", "gần chợ Đông Ba có quán gì", "cuối tuần này có lễ hội gì". Những câu này do chương trình tính hoặc tra, rồi model diễn đạt (chặng 5). Người dùng cũng có thể gửi một tấm ảnh để hỏi "đây là đâu, món gì".

**3. Lên kế hoạch.** Ở trang Lên kế hoạch, người dùng chọn số ngày, người đi cùng, sở thích; chương trình xếp các điểm tham quan vào từng buổi, kèm giờ, chỗ ở, quán ăn, bản đồ. Sau đó họ sửa lịch bằng lời ("dời lăng Tự Đức sang chiều ngày 2") và tải lịch về (chặng 6).

Ngoài ra có trang Khám phá để đọc thẳng các bài của kho, có ảnh.

## Các luật của sản phẩm

Bốn luật dưới đây do chủ dự án chốt. Mọi quyết định kỹ thuật ở các chặng sau đều phải giữ chúng.

1. **Chỉ trả lời từ kho, có nguồn.** Câu ngoài kho phải bị từ chối. Điều kiện không được vỡ: 0 câu ngoài kho được trả lời bằng kho. Khi kho từ chối, hệ thống tra web một lần, nhưng để riêng ở một mục ghi rõ "chưa kiểm".
2. **Việc phải luôn đúng thì chương trình làm.** Phép tính, ngày, tiền, thứ tự bắt buộc do chương trình; model chỉ diễn đạt. Luật này chưa giữ được trọn với tiền: khi người dùng hỏi tổng tiền vé, model vẫn tự cộng các giá lấy từ kho; bản cho chương trình cộng đã thử và bị bỏ (bài 24).
3. **Chất lượng trước, tốc độ và tiền sau.** Thời gian chờ và tiền mỗi câu được đo và báo, nhưng không được dùng để cắt chất lượng.
4. **Thứ tự các loại lỗi, từ nặng tới nhẹ:** sai hoặc thiếu một cảnh báo an toàn · nói chắc mà sai · trả lời một câu ngoài kho · thiếu ý · từ chối nhầm.

Luật thứ tư giải thích nhiều quyết định "bỏ" ở các bài sau: một thay đổi làm bớt từ chối nhầm (lỗi nhẹ nhất) mà làm tăng câu ngoài kho được trả lời (lỗi nặng hơn) thì bị bỏ.

## Những thứ cố ý không làm

| Không làm | Người dùng gặp gì | Vì sao |
|---|---|---|
| Câu hỏi gõ không dấu | hay nhận câu từ chối | bước tìm gần như không khớp được chữ không dấu (bài 10); chủ dự án xếp ngoài phạm vi |
| Tiếng Anh | không hỗ trợ | chủ dự án chốt: người dùng gõ tiếng Việt có dấu |
| Tình huống khẩn cấp (bị cướp, mất giấy tờ, số điện thoại khẩn cấp) | được xử lý như một câu hỏi thường về Huế; không có phần hướng dẫn riêng | chủ dự án chốt ngoài phạm vi |
| Đặt phòng, đặt bàn, mua vé, gửi tin thay người dùng | nhận một câu nói thật "mình chưa làm thay được", kèm cách tự làm | hệ thống không nối với dịch vụ đặt chỗ nào |
| Giá phòng trong phần gợi ý chỗ ở | không hiện | luật nhóm đặt từ 05/11; ngày 14/11 chủ dự án chọn cách gợi ý chỗ ở không kèm giá (bài 30) |
| Giọng nói | không có | chủ dự án cho dừng trước mốc cuối tháng 11; còn chờ chủ dự án nói rõ là bỏ hẳn hay làm sau |
| Nhớ sở thích của từng người giữa các lần dùng | không có; mỗi lần mở lại trang là một cuộc trò chuyện mới | chủ dự án chốt không làm |
| Câu hỏi không thuộc văn hoá, du lịch Huế | nhận một câu cố định: "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế…" | ngoài phạm vi của sản phẩm |

Một dòng trong bảng này không phải là một lỗi còn nợ. Nó là một ranh giới đã được chọn.

Riêng việc **đưa lên mạng** thì khác loại: nó chưa làm, không bắt buộc với đồ án, và là một bước còn nằm trong lộ trình; nếu làm thì làm sau khi mọi thứ xong ở máy.

## Quyết định và lý do

Các quyết định của bài này là quyết định về **sản phẩm**, do chủ dự án chốt. Các quyết định kỹ thuật ở những bài sau đều phải giữ chúng.

### 1. Vì sao chỉ trả lời từ kho, mà không cho model trả lời thêm bằng hiểu biết của nó?

- **Đã chọn:** kho không có thì từ chối; khi đó tra web một lần và để riêng ở một mục ghi "chưa kiểm".
- **Vì sao:** quyết định đã ghi của chủ dự án. Điều thấy được: sản phẩm trả lời về giá vé, giờ mở cửa, quy định, và câu từ kho thì có nguồn để người dùng tự xem lại.
- **Cách khác:** cho model dùng hiểu biết sẵn có: không thử, vì đây là luật nền. Phép gần nhất đã đo là nới luật từ chối: khi câu hỏi có hai ý mà kho chỉ có một, cho trả lời ý kho có. Kết quả: 2 câu ngoài kho bị trả lời, nên bỏ (bài 15). Từ 14/11 có một bản hẹp hơn cho tin hỏi nhiều ý: ý nào kho có thì trả lời, ý nào thiếu thì ghi rõ "Tư liệu chưa có thông tin về: …" (bài 23).
- **Cái giá:** từ chối nhầm: 3 trên 158 câu kho có (khoảng 2 %) ở lượt đo 12/11 với gpt-6-luna; 0 trên 78 câu ở lượt đo 21/11 với Claude (mẫu nhỏ hơn). Và khi kho từ chối, câu hỏi của người dùng được gửi ra một dịch vụ tìm web bên ngoài.

### 2. Vì sao xếp "từ chối nhầm" là lỗi nhẹ nhất, "sai một cảnh báo an toàn" là lỗi nặng nhất?

- **Đã chọn:** thứ tự lỗi ở luật 4.
- **Vì sao:** quyết định đã ghi của chủ dự án. Lập luận của người viết: bị từ chối thì người dùng biết mình chưa có câu trả lời và đi hỏi nơi khác; nhận một câu sai nghe chắc thì họ không có dấu hiệu nào để nhận ra.
- **Cái giá:** nhiều thay đổi làm bớt từ chối nhầm đã bị bỏ vì chúng làm tăng một loại lỗi nặng hơn (bài 15, bài 20).

### 3. Vì sao chất lượng đứng trước tốc độ và tiền?

- **Đã chọn:** thời gian chờ và tiền mỗi câu được đo và báo, không được dùng làm lý do cắt chất lượng.
- **Vì sao:** quyết định đã ghi của chủ dự án.
- **Cái giá:** có lượt người dùng chờ lâu (câu lâu nhất ở lượt đo 21/11 là 17,7 giây); mỗi câu hỏi với model đang chạy tốn khoảng 0,018 USD ở ví dụ chính.

### 4. Vì sao chỉ nhận tiếng Việt có dấu, không làm tiếng Anh và không xử lý câu gõ không dấu?

- **Đã chọn:** người dùng gõ tiếng Việt có dấu.
- **Vì sao:** hai quyết định đã ghi của chủ dự án. Với câu không dấu còn một điều đo được: bước tìm gần như không khớp được chữ không dấu với kho viết có dấu (bài 10).
- **Cách khác:** tiếng Anh: chưa thử.
- **Cái giá:** du khách không đọc được tiếng Việt thì không dùng được; người gõ không dấu hay nhận câu từ chối.

### 5. Vì sao không có phần xử lý riêng cho tình huống khẩn cấp?

- **Đã chọn:** câu khẩn cấp được xử lý như một câu hỏi thường về Huế.
- **Vì sao:** quyết định đã ghi; chủ dự án chốt ba lần rằng việc này ngoài phạm vi sản phẩm.
- **Cách khác:** từng có một câu trả lời soạn sẵn kèm số điện thoại khẩn cấp (tới 09/11); đã bỏ. Cách nhận ra câu khẩn cấp bằng luật từ khoá cũng đã thử: đúng 14 trên 14 câu đã thấy nhưng 0 trên 8 câu chưa thấy, và chặn nhầm 2 trên 8.
- **Cái giá:** người hỏi lúc gặp nạn nhận câu trả lời theo những gì kho có, hoặc câu từ chối kèm mục "Từ web" nếu kho không có.

### 6. Vì sao không đặt phòng, mua vé thay người dùng?

- **Đã chọn:** hệ thống trả một trong ba câu nói thật theo loại việc, kèm cách người dùng tự làm. Ví dụ, câu mở đầu của một trong ba câu: "Mình chưa đặt phòng, đặt bàn hay mua vé thay bạn được".
- **Vì sao:** hệ thống không nối với dịch vụ đặt chỗ nào. Đã đo trên lượt thật: 11 trên 12 lượt ra đúng câu nói thật của loại việc đó.
- **Cái giá:** người dùng phải rời ứng dụng để đặt.

## Nếu… thì sao

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa |
|---|---|---|---|
| người dùng hỏi một điều về Huế mà kho không có | từ chối bằng câu cố định, rồi tra web một lần | câu "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)." rồi mục web. Tra web không ra thì: câu từ chối, một dòng cố định của mục web (ví dụ "Mình chưa tìm thấy thông tin phù hợp trên web."), và gợi ý cách hỏi | đã có (bài 16, 25) |
| người dùng gõ không dấu | bước tìm gần như không khớp được | hay nhận câu từ chối | **không làm**; ranh giới đã chọn |
| người dùng hỏi một việc không thuộc Huế | bước xếp loại câu đưa vào tuyến "ngoài phạm vi" | "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" | đã có (bài 22) |
| người dùng nhờ đặt phòng, mua vé | trả một câu nói thật theo loại việc | câu nói rõ là chưa làm thay được, kèm cách tự làm | đã có |
| giá vé, giờ mở cửa ngoài đời đổi mà kho chưa sửa | hệ thống trả lời theo kho | giá cũ, kèm dòng "có thể đã thay đổi — hãy kiểm lại với nơi đến trước khi đi" | có dòng nhắc; việc sửa kho do người làm (bài 7) |
| có người dùng thật, hỏi kiểu câu nhóm chưa từng nghĩ tới | — | — | chưa biết: mọi phép đo dùng câu do nhóm soạn hoặc do một model đóng vai du khách |

## Dễ nhầm

- **"Đây là một chatbot hỏi gì cũng trả lời."** Không. Nó chỉ trả lời về văn hoá, du lịch Huế, và chỉ từ kho của nó.
- **"Từ chối là hỏng."** Không. Từ chối đúng một câu ngoài kho là hành vi được thiết kế. Thứ bị coi là lỗi là từ chối một câu mà kho có.
- **"Lịch tham quan do model nghĩ ra."** Không. Chương trình xếp lịch theo luật; model chỉ viết câu mô tả cho từng điểm.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. hue_rag làm ba loại việc nào cho người dùng?</summary>

Hỏi đáp có nguồn từ kho bài viết; các việc cần tính hoặc cần dữ liệu của hôm nay (ngày âm lịch, thời tiết, khoảng cách); và lên một lịch tham quan rồi sửa lịch theo lời người dùng.

</details>

<details>
<summary>2. Vì sao chỉ trả lời từ kho? Cái giá là gì?</summary>

Quyết định của chủ dự án; câu từ kho có nguồn để người dùng xem lại. Cái giá: từ chối nhầm (3 trên 158 câu ở lượt đo 12/11), và khi kho từ chối thì câu hỏi được gửi ra dịch vụ tìm web.

</details>

<details>
<summary>3. Thứ tự các loại lỗi là gì, và nó quyết định điều gì?</summary>

Từ nặng tới nhẹ: sai hoặc thiếu một cảnh báo an toàn, nói chắc mà sai, trả lời một câu ngoài kho, thiếu ý, từ chối nhầm. Một thay đổi làm bớt lỗi nhẹ mà làm tăng lỗi nặng hơn thì bị bỏ.

</details>

<details>
<summary>4. Kể ba thứ hệ thống cố ý không làm, và người dùng gặp gì ở mỗi thứ.</summary>

Câu gõ không dấu: hay nhận câu từ chối. Tình huống khẩn cấp: được xử lý như câu hỏi thường, không có hướng dẫn riêng. Đặt phòng, mua vé thay: nhận câu nói thật là chưa làm thay được, kèm cách tự làm.

</details>

## Chi tiết để tra

- Tên đề tài bằng tiếng Anh: *Developing a Retrieval-Augmented Generation-Based Application for Cultural and Tourism Experiences in Hue*.
- Tối 22/11 hệ thống có 48 tính năng đang mở và 3 đang tắt (đếm 17:21; lúc 10:25 là 42 mở, từ 14:47 thêm ba tính năng ở khâu tìm và bước viết lại của tin dài nhiều ý — bài 21, 23; từ 15:42 thêm tính năng giữ chữ tới khi qua bước kiểm nguồn — bài 6; từ 16:08 thêm việc nhớ câu trả lời liền trước cả trong cuộc đã lập lịch — bài 23, 31; từ 17:15 thêm thẻ nơi: ở tin nhiều ý hỏi giờ, địa chỉ, nơi được nhắc tên được gắn dòng giờ, địa chỉ chép từ bài riêng của nơi đó, và hàng vé lẻ chép từ bài vé — bài 23). Từ 11:56 23/11 là 49 mở, 3 tắt (đếm 12:25 23/11): thêm giờ quán trong công cụ "gần một điểm", cạnh tên quán in dòng giờ hoạt động chép từ bài kho của quán — bài 24. Từ 12:34 23/11 là 49 mở, 5 tắt (đếm 12:51 23/11): thêm hai tính năng đang tắt, vòng công cụ cuối chỉ được viết và dòng báo của công cụ khoảng cách khi không có số cho một cặp nơi (phụ lục B). Con số này đổi theo từng buổi làm việc; bảng từng tính năng ở phụ lục B của giáo trình.
- Câu xin lên lịch gõ trong ô hỏi đáp ("lên lịch giúp mình 2 ngày") không ra một lịch; hệ thống trả lời từ kho và thêm một dòng trỏ sang trang Lên kế hoạch. Việc xếp lịch từ câu gõ tự do đã thử hai lần, chưa đạt điều kiện ghi trước, đang tắt (bài 28).
- Câu nhờ làm thay: đo trên lượt thật ngày 19/11, 11 trên 12 lượt ra đúng câu nói thật của loại việc đó.
- Kho còn thiếu vài mảng thông tin người dùng hay hỏi (chỗ đậu ô tô, quy định chụp ảnh); xem bài 7.
- Mọi phép đo trong giáo trình này dùng câu hỏi do nhóm soạn hoặc do một model đóng vai du khách; chưa có số đo với người dùng thật.

**Bài sau (bài 5):** người dùng nhìn thấy gì khi mở ứng dụng: các trang, và một lượt hỏi trông ra sao trên màn hình.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Tên đề tài, người dùng, "làm như sản phẩm thật", chất lượng trước: `bai_hoc/00_HUE_RAG_TRONG_3_PHUT.md` mục "hue_rag là gì" và nguồn của nó ở `session_prompt/Project_Status.md` [quyết định đã ghi].
- Bốn luật, thứ tự lỗi, các thứ không làm (tiếng Anh, khẩn cấp, giá phòng, giọng nói, nhớ sở thích), chưa đưa lên mạng: `session_prompt/HIEN_TRANG.md` mục 1, mục 2 và mục 4 (phần "Sản phẩm") [quyết định đã ghi].
- Câu không dấu ngoài phạm vi: `bai_hoc/04_EMBEDDING_VA_TU_KHOA.md` mục "Khi nào hỏng" (chủ dự án chốt 25/10).
- Tuyến khẩn cấp được xử lý như câu về Huế, không có câu soạn sẵn: `backend/llm/assistant.py`, hàm `_pick_route` (chú thích "phương án B") [code]. Luật từ khoá cho câu khẩn cấp (14 / 14; 0 / 8; chặn nhầm 2 / 8): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 32.
- Câu cố định cho câu ngoài phạm vi và ba câu "không làm thay": `backend/llm/full_corpus_prompt.py` (`OUT_OF_SCOPE_ANSWER`, `CAU_LAM_THAY`); 11 / 12 lượt: `bai_hoc/BAN_DO_DU_AN.md`, bảng "Cái gì ĐANG chạy".
- Tải lại trang là cuộc trò chuyện mới: `bai_hoc/README.md` (dòng bài 13, thêm 15/11).
- 49 tính năng mở, 5 tắt (thêm 12:56 23/11/2026): lệnh đếm ra `49`, với `false` ra `5` — người gom phụ lục tự chạy 12:51 23/11/2026 trên cây chính, main `5138622d` [tự chạy lệnh đếm]; hai dòng tắt mới `vong_cuoi_chi_viet`, `khoang_cach_trang_thai`: `git diff b4931a6b origin/main -- backend/config/settings.yaml` [code]; gộp 12:34: bài 38 "Chi tiết để tra" [chép]. Mốc 12:25 giữ dưới đây.
- 49 tính năng mở, 3 tắt (thêm 12:35 23/11/2026): cùng lệnh đếm ra `49`, với `false` ra `3` — người gom phụ lục tự chạy 12:25 23/11/2026 trên cây chính, main `0367e775` [tự chạy lệnh đếm]; tính năng thứ 49 là `gan_diem_gio` (`backend/config/settings.yaml` dòng 90; bài 24 dùng giờ commit gộp 11:56) [code; chép bài 24]. Mốc tối 22/11 giữ dưới đây.
- 48 tính năng mở, 3 tắt (`today_line`, `lich_trinh`, `so_vet`): lệnh đếm ở `guides/RUNBOOK_BAN_GIAO.md` mục 0 (dòng 26) ra `48` — người sửa tự chạy 17:21 22/11/2026 trên cây chính, main `4e2746c0` [tự chạy lệnh đếm]; runbook ghi `48` lúc 17:18 trên main `2a9c9e9c` sau khi mở `the_noi` (`backend/config/settings.yaml` dòng 100, "BẬT 17:15") [chép]. Trước đó `47` chạy 16:13 22/11/2026 trên main `2a221e5` sau khi mở `nho_dap_cuoc_co_lich` (`backend/config/settings.yaml` dòng 76, "MỞ 16:08") [chép từ runbook; người sửa chạy lại lệnh 22/11 trên main `0430104e` ra `47` — đã chạy]. Trước đó `46` lúc 15:51 trên main `15cd5985` sau khi mở `giu_chu_toi_kiem`. Lần đếm 15:11 22/11/2026 của người viết: 45 [đã chạy]. Trước đó: 41 lúc 10:17; 42 lúc 10:25 sau khi `tim_theo_ve` mở; 45 từ 14:47 sau khi mở `tim_ve_bo_cut`, `tach_cau_tim_model`, `het_luot_viet_lai` (runbook mục 0). Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml` [code; đã chạy lệnh đếm].
- Model vẫn tự cộng tổng tiền vé; bản chương trình cộng đã bỏ: chú thích `lich_vao_hoi_thuong` ở `settings.yaml`; `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 20. Giọng nói còn chờ chủ dự án nói rõ: `session_prompt/HIEN_TRANG.md` mục 3.
- Dòng trỏ sang trang Lên kế hoạch; lịch từ câu gõ tự do tắt: `backend/config/settings.yaml` (`len_lich_dan_trang`, `lich_trinh`) và `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 22.
- Chưa có số đo với người dùng thật: `bai_hoc/BAN_DO_DU_AN.md` mục "Chỗ còn yếu đã biết" ý 5.
- Mục "Quyết định và lý do" và "Nếu… thì sao" (đã sửa theo biên bản `data/hoc_cung_D/kiem/bai_22_va_muc_moi_01_03_04.md`): nới luật từ chối (2 câu ngoài kho bị trả lời) `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 11; tin nhiều ý từ 14/11 `backend/config/settings.yaml` (`cau_nhieu_y`); từ chối nhầm 3 / 158 (12/11, gpt-6-luna) `bai_hoc/BAN_DO_DU_AN.md`, 0 / 78 và câu lâu nhất 17,7 giây (21/11, Claude) `data/thu_bedrock_2026-11-21/do/TONG_HOP_BAN_0.md` [riêng tư]; câu soạn sẵn khẩn cấp tới 09/11 `bai_hoc/12_VI_SAO_CAN_TRO_LY.md`; ba câu nói thật (nguyên văn) `backend/llm/full_corpus_prompt.py` (`CAU_LAM_THAY`); câu dẫn sang mục web `frontend/src/moDauWeb.js`; dòng cố định của mục web `backend/llm/tra_web.py`; dòng "có thể đã thay đổi" `data/hoc_cung_D/vi_du_di_suot_vet.json`. Câu "bị từ chối thì người dùng biết…" là lập luận, ghi rõ trong bài.

</details>
