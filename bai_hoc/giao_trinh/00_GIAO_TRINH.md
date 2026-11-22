# Giáo trình hue_rag: hiểu cả hệ thống từ đầu, không cần đọc code

*Cập nhật 14:19, ngày 22/11/2026 · mục lục và khuôn bài chốt sau khi anh trả lời bốn câu hỏi sáng 22/11; khuôn thêm hai mục "Quyết định và lý do" và "Nếu… thì sao" theo yêu cầu của anh trưa 22/11, bài 6 là bài mẫu · đã viết xong chặng 2 và chặng 3 (bài 7–16) và hai bài khác (bài 2, 21), mỗi bài đã qua một lượt đối chiếu độc lập với chương trình và số đo; các bài còn lại viết theo từng chặng · mọi con số trong bộ này lấy từ hệ thống đang chạy và các phép đo đã ghi, không có phép thử mới.*

**Bộ này cho ai.** Cho anh, người sẽ tự chạy thử, tự trình bày và tự trả lời câu hỏi về đồ án. Không cần đọc code. Biết dùng một chatbot là đủ để bắt đầu.

**Đọc thế nào.** Đọc theo đúng số thứ tự: bài sau dựa trên bài trước, khái niệm mới luôn được giảng trước khi dùng. Mỗi bài chia hai nửa:

- **Nửa để hiểu** (từ đầu bài tới mục "Những điều cần nhớ"): đọc lần đầu chỉ cần nửa này. Trong đó có hai mục để anh giải thích lại được chứ không chỉ kể lại được: **"Quyết định và lý do"** (vì sao làm thế này mà không làm thế khác, và cái giá của lựa chọn) và **"Nếu… thì sao"** (một thứ hỏng, hoặc điều kiện đổi, thì hệ thống làm gì).
- **Nửa để tra** (từ mục "Cấu hình đang chạy" trở xuống): model nào, tham số nào, đã thử phương án nào, ra số bao nhiêu, hỏng ở đâu. Không cần đọc để hiểu bài, nhưng đây là chỗ trả lời các câu "cụ thể là bao nhiêu" và "đã thử cách nào, ra số nào".

**Con số của hệ thống trong bộ này** (số bài, số đoạn, tính năng nào đang mở) là số lúc bài được viết, ghi ở dòng cập nhật của từng bài. Hệ thống vẫn đang được làm tiếp nên vài con số có thể đã lớn hơn khi anh đọc; cách hoạt động thì không đổi theo.

**Năm ví dụ dùng suốt cả bộ** (đều là lượt chạy thật qua hệ thống):

| Ví dụ | Người dùng gõ / chọn | Dùng để giảng |
|---|---|---|
| **Ví dụ chính** | *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"* | đường đi bình thường của một câu hỏi: tìm ra 10 đoạn, model viết, có 5 nguồn |
| **Ví dụ "kho không có"** | *"Chùa Thiên Mụ có chỗ đậu ô tô không?"* | kho không nói tới thì hệ thống từ chối thay vì đoán, rồi tra web ở một mục riêng |
| **Ví dụ "phải tìm thêm"** | *"Mặc áo dài vào Đại Nội có được miễn vé không?"* | lần tìm đầu chưa đủ, trợ lý tự tìm thêm hai lần rồi mới trả lời |
| **Ví dụ "kho có mà tìm không ra"** | *"Vào chùa ở Huế có phải cởi giày không?"* | giới hạn của bước tìm: kho có một câu trả lời nhưng ba lần tìm đều không lấy ra |
| **Ví dụ lập lịch** | trang Lên kế hoạch: 3 ngày, 2 người lớn, thích di tích | chương trình xếp 11 điểm vào 3 ngày, model chỉ viết câu mô tả |

## Đường chính: chín chặng

Cột cuối: ✅ đã viết · ⬜ chưa viết.

### Chặng 0 — Nền: vì sao phải xây cả một hệ thống quanh model?

| Số | Bài | |
|---|---|---|
| 1 | [Model ngôn ngữ là gì, và vì sao nó viết trôi chảy mà vẫn sai](01_MODEL_NGON_NGU.md) | ✅ |
| 2 | [RAG là gì: cho model đọc tài liệu trước khi trả lời](02_RAG_LA_GI.md) | ✅ |
| 3 | [Trợ lý và công cụ: model chỉ "xin", chương trình mới là thứ chạy](03_TRO_LY_VA_CONG_CU.md) | ✅ |

### Chặng 1 — Bức tranh: hệ thống này làm gì, cho ai, gồm những khối nào?

| Số | Bài | |
|---|---|---|
| 4 | [Bài toán: ai dùng, hỏi gì, nhận gì, và những thứ cố ý không làm](04_BAI_TOAN.md) | ✅ |
| 5 | [Người dùng thấy gì: các trang của ứng dụng](05_NGUOI_DUNG_THAY_GI.md) | ✅ |
| 6 | [Kiến trúc: các khối, vì sao đặt như vậy, và khi một khối hỏng thì sao](06_KIEN_TRUC.md) — **bài mẫu theo khuôn mới** | ✅ |

### Chặng 2 — Chuẩn bị kho: làm một lần, trước khi có câu hỏi nào

| Số | Bài | |
|---|---|---|
| 7 | [Kho dữ liệu: 266 bài viết về Huế, ai soạn, lấy từ đâu, kiểm thế nào](07_KHO_DU_LIEU.md) | ✅ |
| 8 | [Cắt bài thành đoạn (chunking)](08_CAT_DOAN.md) | ✅ |
| 9 | [Thông tin gắn kèm mỗi đoạn (metadata) và "chữ để tìm"](09_METADATA.md) | ✅ |
| 10 | [Biến mỗi đoạn thành một dãy số mang nghĩa: embedding](10_EMBEDDING.md) | ✅ |
| 11 | [Tìm theo chữ trùng: từ khoá BM25](11_TU_KHOA_BM25.md) | ✅ |
| 12 | [Cất vào Qdrant, cập nhật khi kho đổi, và vì sao kho lệch chỉ mục thì không câu hỏi nào được trả lời](12_QDRANT.md) | ✅ |

### Chặng 3 — Trả lời một câu hỏi: mỗi lần người dùng gõ

| Số | Bài | |
|---|---|---|
| 13 | [Tìm: lấy 30 ứng viên, trộn hai bảng xếp hạng, giữ 10 đoạn](13_TIM.md) | ✅ |
| 14 | [Xếp lại bằng model (reranking): đã thử ba cách, không dùng](14_XEP_LAI.md) | ✅ |
| 15 | [Viết câu trả lời: lời dặn, ngữ cảnh 10 đoạn, và số nguồn [n]](15_VIET_CAU_TRA_LOI.md) | ✅ |
| 16 | [Kiểm nguồn bằng chương trình, và câu từ chối cố định](16_KIEM_NGUON_VA_TU_CHOI.md) | ✅ |

### Chặng 4 — Vì sao tin được: đo

| Số | Bài | |
|---|---|---|
| 17 | [Bộ 176 câu hỏi mẫu: đề kiểm tra của hệ thống](17_BO_CAU_HOI_MAU.md) | ✅ |
| 18 | [Chấm bước tìm: đoạn đúng có lọt vào 10 đoạn không](18_CHAM_BUOC_TIM.md) | ✅ |
| 19 | [Chấm câu trả lời: ba thang điểm, người chấm là model, và nhiễu](19_CHAM_CAU_TRA_LOI.md) | ✅ |
| 20 | [Một thí nghiệm được làm thế nào, và nhìn cả bảng các lần so sánh thấy gì](20_MOT_THI_NGHIEM.md) | ✅ |

### Chặng 5 — Trợ lý hỏi đáp: khi tìm một lần rồi viết là chưa đủ

| Số | Bài | |
|---|---|---|
| 21 | [Harness: phần chương trình bao quanh model](21_HARNESS.md) | ✅ |
| 22 | [Xếp loại câu trước khi tìm: bốn tuyến](22_XEP_LOAI_CAU.md) | ✅ |
| 23 | [Tìm thêm, nhớ câu hỏi trước, và câu hỏi nhiều ý](23_TIM_THEM_NHO_NHIEU_Y.md) | ✅ |
| 24 | [Việc phải đúng thì chương trình tính: ngày âm lịch làm mẫu, rồi thời tiết, khoảng cách và các công cụ khác](24_VIEC_PHAI_DUNG_THI_CHUONG_TRINH_TINH.md) | ✅ |
| 25 | [Khi kho không có: tra web một lần, để riêng mục "chưa kiểm"](25_TRA_WEB.md) | ✅ |
| 26 | [Hỏi bằng ảnh](26_HOI_BANG_ANH.md) | ✅ |

### Chặng 6 — Lên kế hoạch: chương trình xếp lịch, model chỉ diễn đạt

| Số | Bài | |
|---|---|---|
| 27 | [Trang Lên kế hoạch: từ mấy nút chọn tới một lịch, và bảng điểm tham quan đứng sau](27_TRANG_LEN_KE_HOACH.md) | ✅ |
| 28 | [Chương trình xếp lịch theo luật nào: một lịch thật được xếp từng bước](28_CHUONG_TRINH_XEP_LICH.md) | ✅ |
| 29 | [Khi không xếp được, bước kiểm lịch, và phần việc của model](29_KHONG_XEP_DUOC_KIEM_LICH_VIEC_CUA_MODEL.md) | ✅ |
| 30 | [Quanh một lịch: chỗ ở, quán ăn, ảnh, bản đồ, xuất file](30_QUANH_MOT_LICH.md) | ✅ |
| 31 | [Sửa lịch bằng lời: model hiểu ý, chương trình áp và kiểm](31_SUA_LICH_BANG_LOI.md) | ✅ |
| 32 | [Đo một trợ lý: hội thoại nhiều lượt, người dùng mô phỏng, kịch bản chạy lặp](32_DO_MOT_TRO_LY.md) | ✅ |

### Chặng 7 — Máy móc bên dưới

| Số | Bài | |
|---|---|---|
| 33 | [Model viết, mức suy luận, và đổi model bằng một dòng cấu hình](33_MODEL_VIET_VA_DOI_MODEL.md) | ✅ |
| 34 | [Người dùng chờ bao lâu, một câu tốn bao nhiêu tiền](34_CHO_BAO_LAU_TON_BAO_NHIEU.md) | ✅ |
| 35 | [Trang web và máy chủ: ai gửi gì cho ai](35_TRANG_WEB_VA_MAY_CHU.md) | ✅ |
| 36 | [Bật hệ thống trên máy, và đóng gói bằng Docker](36_BAT_HE_THONG_VA_DOCKER.md) | ✅ |
| 37 | [Bảo mật: khoá bí mật, dữ liệu người dùng, và chữ lạ chen vào lời dặn](37_BAO_MAT_VA_DU_LIEU_NGUOI_DUNG.md) | ✅ |
| 38 | [Bộ test: chương trình tự kiểm những gì](38_BO_TEST.md) | ✅ |

### Chặng 8 — Nhìn lại

| Số | Bài | |
|---|---|---|
| 39 | Đồ án được làm thế nào: một người quyết định và nhiều coding agent | ⬜ |
| 40 | Làm được tới đâu, còn yếu ở đâu, hướng phát triển | ⬜ |
| 41 | Kể lại toàn bộ trong một phút, trong năm phút, và kịch bản chạy thử | ⬜ |

## Phụ lục để tra (viết sau khi đường chính đủ)

| | Phụ lục | |
|---|---|---|
| A | [Mọi tham số cấu hình: giá trị đang chạy, dùng để làm gì, bài nào giảng](PL_A_THAM_SO.md) | ✅ |
| B | [Mọi tính năng đang mở và đang tắt: làm gì, một con số, bài nào giảng](PL_B_TINH_NANG.md) | ✅ |
| C | Sổ mọi phép so sánh đã làm, kể cả phương án bị bỏ; mỗi phép so chỉ có số ở một nơi | ⬜ |
| D | Lời dặn gửi model và mô tả từng công cụ, chép nguyên văn từ chương trình | ⬜ |
| E | Thuật ngữ Việt – Anh | ⬜ |
| F | Các con số chính trên một trang | ⬜ |

## Khuôn của mỗi bài

**Nửa để hiểu**

1. **Tên bài** là một câu hỏi hoặc một câu khẳng định.
2. **Dòng cập nhật:** viết lúc nào, số lấy từ đâu.
3. **Nối mạch:** "Bài trước đã biết… Bài này thêm…".
4. **Ý chính:** 3–5 gạch; đọc riêng mục này cũng nắm được bài.
5. **Từ dùng trong bài:** chỉ các từ mới của bài; tên dùng trong bài · tên gốc tiếng Anh · nghĩa.
6. **Thân bài:** 3–5 mục, tên mỗi mục là một câu khẳng định (đọc riêng các tên mục là ra dàn ý của bài). Nói thẳng cơ chế, không dùng ẩn dụ; ví dụ lấy từ lượt chạy thật; mỗi hình tối đa 6 ô.
7. **Quyết định và lý do:** mỗi quyết định thiết kế của phần này viết thành một câu hỏi "Vì sao…?". Mở bằng hai ba câu kể tình huống bằng lời thường (giảng luôn khái niệm mới nếu có), rồi chốt bằng bốn gạch: **đã chọn** gì · **vì sao** · **cách khác** (ghi rõ là "đã đo", "chưa thử" hay "quyết định đã ghi") · **cái giá** phải trả cho lựa chọn đó. Chỗ nào không tìm thấy lý do được ghi lại thì viết đúng một dạng: "chưa thấy ghi lý do; điều thấy được là…", không thêm câu đoán. Mỗi bài giữ bốn tới sáu quyết định quan trọng ở đây; quyết định nhỏ nằm ở nửa để tra. Chỉ viết về thứ hệ thống thật sự có. Có ba loại câu hỏi: *vì sao đặt ở đây* (việc này làm ở máy chủ hay ở giao diện; chương trình làm hay giao cho model; tính sẵn hay tính lúc hỏi) · *vì sao làm cách này* (gọi thẳng hay xếp hàng chờ; một lần hay nhiều lần; tự viết hay dùng đồ có sẵn) · *vì sao là con số này*.
8. **Nếu… thì sao:** kể trọn một tình huống, rồi một bảng ngắn các tình huống đáng nhớ nhất (nếu · người dùng thấy gì · muốn hết lỗi thì ai làm gì); bảng đủ nằm ở nửa để tra. Hai loại tình huống. *Khi có thứ hỏng:* dịch vụ bên ngoài sập hoặc chậm, quá hạn giờ, dữ liệu lệch nhau, người dùng làm điều không ngờ. *Khi điều kiện đổi:* kho lớn gấp mười, nhiều người dùng cùng lúc, đổi model. Mỗi tình huống ghi: hệ thống làm gì · người dùng thấy gì · đã có hay chưa có. Chỗ nào chưa xử lý thì ghi thẳng "chưa có". Lời báo cho người dùng chép nguyên văn từ chương trình; tình huống nào chưa được thử thật thì ghi rõ là đọc từ chương trình.
9. **Dễ nhầm:** 1–3 câu người mới hay nói, kèm câu sửa.
10. **Câu hỏi tự kiểm** (anh chọn thêm trưa 22/11): khoảng 4 câu kiểu "vì sao…", "nếu… thì sao", đáp án một hai câu, gập lại, bấm mới hiện. Bài đã có mục này thì không còn mục "Những điều cần nhớ" (nó lặp lại "Ý chính"); các bài viết theo khuôn cũ vẫn còn mục đó.

**Luật về độ dài** (anh duyệt trưa 22/11, sau khi đọc bài 6): nửa để hiểu không nói một điều hai lần. Đoạn dẫn trước một quyết định chỉ có khi phải giảng một khái niệm mới; bảng chi tiết nằm ở nửa để tra; "Dễ nhầm" nhiều nhất 3 gạch. Không bỏ: mục giảng nền, đủ bốn gạch của mỗi quyết định, bảng tình huống hỏng.

**Nửa để tra** (bài nào có mục nào thì ghi mục đó; bài nền thường chỉ có hai mục cuối)

*Hai mục 7 và 8 thêm trưa 22/11/2026 theo yêu cầu của anh: đọc xong phải giải thích được từng quyết định và nói được "hỏng thì sao", không chỉ kể được hệ thống gồm những gì. Mục "Vì sao không làm cách khác" của khuôn cũ nhập vào mục 7. **Bài 6 (kiến trúc) là bài mẫu đầu tiên theo khuôn mới**; anh đã đọc và duyệt trưa 22/11. Các bài 1–11 và 17–38 đã theo khuôn này. Các bài 12–16 vẫn theo khuôn cũ, còn mục "Vì sao không làm cách khác" ở nửa để tra, và đang được chuyển dần.*

11. **Cấu hình đang chạy:** bảng mục · giá trị · dùng để làm gì và vì sao là giá trị đó · đã thử giá trị khác chưa.
12. **Đã so:** vấn đề thật đã gặp · so cái gì với cái gì, trên bộ câu nào · bảng kết quả kể cả phương án bị bỏ · đọc bảng thế nào · đã chọn gì · giới hạn của phép đo. Mỗi con số ghi rõ đo với model viết nào.
    Bài nào giảng lời dặn thì có thêm bảng **lời dặn**: từng phần, một câu nguyên văn.
13. **Giới hạn đã biết:** chỗ hệ thống còn yếu, kèm con số.
14. **Chi tiết để tra:** con số phụ, ngoại lệ, ngày đo.
15. **Bài sau.**
16. **Nguồn** (thu gọn, anh không cần đọc): mỗi con số và mỗi khẳng định trỏ về file code hoặc file số đo.

Luật viết: thân bài không có tên file, tên hàm, mã bản code, ngày giờ phép thử, tên phiên làm việc. Mỗi chữ "vì" trong bài phải có căn cứ ở code, ở số đo hoặc ở một quyết định đã ghi; không có thì viết "chưa rõ vì sao". Mỗi con số đi kèm thứ nó đếm và mốc để so.

## Bộ bài cũ

Bộ 27 bài ở thư mục [`bai_hoc/`](../README.md) giữ nguyên để tra cho tới khi đường chính của giáo trình đủ. Việc mới xong trong lúc giáo trình đang viết vẫn được ghi ở [Việc mới xong](../VIEC_MOI_XONG.md).

<details>
<summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

- Bốn câu anh trả lời sáng 22/11/2026 (mức nền: ba bài nền ngắn · bốn chỗ vướng của bộ cũ: không ghép được bức tranh, quá nhiều chi tiết thi công, thiếu cấu hình và kết quả so sánh, ẩn dụ che cơ chế · nhịp giao: viết tiếp theo chặng · bài mẫu thứ ba: harness): ghi chép riêng của phiên viết giáo trình.
- Năm ví dụ: sổ ghi từng lượt của hệ thống trên máy phát triển, các ngày 20–21/11/2026 [đã chạy; người viết không chạy lại]; bản sao riêng tư ở `data/hoc_cung_D/vi_du_*_vet.json`. "Kho không nói về chỗ đậu xe ở chùa Thiên Mụ": dò bằng `scripts/grep_kb.sh` ngày 22/11/2026. "Kho có câu về giày dép": biên bản kiểm độc lập `data/hoc_cung_D/kiem/bai_02_10.md`.
- Model viết: hệ thống đang chạy Claude Sonnet 5.5 (đổi tạm từ 21/11/2026); phần lớn phép so cũ đo với gpt-6-luna. Mỗi bài ghi rõ con số nào đo với model nào.
- Luật nội dung: `session_prompt/WORKFLOW.md` mục 6 và mục 10.

</details>
