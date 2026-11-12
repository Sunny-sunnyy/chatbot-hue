# Rà trong dự án: phần nào chưa ổn (C, đợt rà khoảng cách 12/11)

Người làm: C (`hue-rag-e1`). Viết 19:07 12/11/2026 (`date`). A giao (`CURRENT_HANDOFF.md` "Đợt rà khoảng cách", dòng C). Chỉ đọc, 0 USD.
Không đề xuất tính năng mới (việc của E / B); file này chỉ gom **cái đang có mà chưa ổn**, kèm bằng chứng, để A tổng hợp trình User.

## 1. Đã đọc gì · nhãn bằng chứng

- `CURRENT_HANDOFF.md` mục "Giới hạn biết", "Câu hỏi A còn nợ"; `bai_hoc/16` (bảng "Chỗ còn yếu"); `Project_Status.md` §4.
- Log `backend/logs/application.log` (1.062 dòng `chat_metrics`, 22 dòng `chat_feedback`) — tổng hợp bằng `data/phase_11/dot_2_dem/tools/log_tong.py`.
- 18 câu tự viết C gửi hệ thống thật hôm nay (`c_dot_2_dem_implementation.md` trong `report_agent/2026-11-08_phase_9_ban_13/`).

Nhãn: **[đo]** số từ một lượt đo có report · **[hôm nay]** C chạy / kiểm lại 12/11 · **[log]** đếm từ log (xem cảnh báo dưới) · **[ghi]** chỉ có trong handoff / bài học, C chưa kiểm lại.

**Cảnh báo về log:** log dùng chung cho pytest, lượt đo của agent và server; không có nội dung câu; hệ thống chưa deploy ⇒ **không có dòng nào chắc chắn là người dùng thật**.
399 / 1.062 dòng `chat_metrics` là lỗi 4xx / 5xx và 480 dòng `router_failed` — khớp với các test không nạp khoá, không phải sự cố vận hành. 22 dòng đánh giá
(15 👎 / 7 👍) cũng không tách được khỏi test ⇒ **không dùng làm bằng chứng chất lượng**. Số [log] dưới đây chỉ là tín hiệu.

## 2. Bảng phần chưa ổn

Mức ảnh hưởng: **cao** = người dùng nhận câu sai hoặc không được việc ở loại câu hay gặp · **vừa** = chậm / thiếu ý / phải hỏi lại · **thấp** = hiếm hoặc chỉ ảnh hưởng người vận hành.
Sửa **rẻ** = sửa chữ / dữ liệu / một hàm, đo 1 lượt nhỏ · **vừa** = một bậc có đo an toàn + Golden · **đắt** = đổi thiết kế hoặc cần dữ liệu / hạ tầng mới.

### A. Chất lượng câu trả lời

| # | Phần chưa ổn | Bằng chứng | Ảnh hưởng | Sửa |
|---|---|---|---|---|
| A1 | **Câu "ăn gì / quán nào gần điểm X"** phần lớn không trả lời được từ kho | [hôm nay] 5 / 6 câu không đủ dùng (3 từ chối, 2 một phần); kho có 81 bài quán / cà phê nhưng chỉ 15 bài có câu định vị theo điểm tham quan, 4 bài có toạ độ | **cao** (loại câu khách du lịch hỏi tự nhiên) | **rẻ–vừa**: thêm dòng "khu / gần điểm nào" cho bài quán (sửa kho, build lại chỉ mục), đo lại 6 câu + bộ an toàn |
| A2 | **Từ chối cả câu khi kho chỉ có một phần câu trả lời** | [hôm nay] 1 / 18: kho có bài riêng về đúng lễ hội được hỏi nhưng trợ lý từ chối rồi ra web; [đo] hai bậc 09/11 (web cho câu hỏi kèm, lịch trình câu tự do) âm cùng gốc này; [đo] từ chối nhầm còn 4–6 / 158 câu trong kho (≈ 3 %), dồn ở câu nhiều nguồn / so sánh | **vừa–cao** (người dùng thấy "không có thông tin" dù kho có) | **vừa**: đổi lời dặn trả lời ⇒ phải qua bộ an toàn + ngoài kho; đã thử gián tiếp 2 lần chưa đạt ⇒ cần lượt đếm riêng trước (bao nhiêu câu Golden bị từ chối mà có ≥ 1 đoạn đúng trong ngữ cảnh) |
| A3 | **Câu hỏi cơ sở lưu trú cụ thể** rơi vào từ chối + web hên xui | [hôm nay] 3 / 4 câu kho từ chối; web cho danh sách tên ở 2 / 3, 1 câu web không ra gì; câu "nên ở khu nào" 2 / 2 ổn | **vừa** | **rẻ**: ý đã có trong backlog — code dựng "khu nên ở + link tìm phòng" thay câu từ chối |
| A4 | **Kiểm nguồn chỉ kiểm mã trích có thật, chưa kiểm số tiền / giờ có trong đoạn được trích** | [ghi] bài 16; **chưa đo** có bao nhiêu câu sai kiểu này. [hôm nay] 0 / 10 câu kho trả lời có tên / giờ / ngày lệch bài được trích (mẫu nhỏ) | **cao nếu xảy ra** (sai cảnh báo / giá là lỗi nặng nhất theo thứ tự lỗi), tần suất chưa biết | **rẻ để đếm** (0 USD: quét số tiền / giờ trong câu trả lời của lượt Golden B7 so với đoạn trích); sửa = **vừa** |
| A5 | **Bản đang chạy chưa được chấm lại trên cả 176 câu** | [ghi] mỗi bậc trợ lý chỉ đo trên bộ riêng + mẫu 30 | vừa (rủi ro chưa biết) | đang xử lý: lượt B7 giữa kỳ hôm nay |
| A6 | **Chưa có câu của người dùng thật; không đếm được người ta hỏi loại gì** | [hôm nay] log không có nội dung và không có nhãn loại câu; mọi bộ đo do AI soạn; [ghi] bài 16: bộ kín thấp hơn bộ quen ≈ 0,4 điểm | vừa (mọi ưu tiên đang dựa trên phỏng đoán) | **rẻ**: thêm một nhãn loại câu do code gắn vào `chat_metrics` (không ghi nội dung); thu câu thật có đồng ý khi deploy = **vừa** |
| A7 | **Lịch trình**: câu gõ tự do tắt; biểu mẫu "đi dày" gần như không tác dụng; nhóm người lớn tuổi / trẻ em không có buổi tối; câu lịch bị rút khi thiếu mã trích | [đo] lịch trình câu tự do 2 lần chưa đạt; [đo] "kiểu đi" không đổi khung ở 0 / 120 tổ hợp với bảng điểm đang dùng; [ghi] rút lại 1 / 9 | vừa (tính năng nổi bật khi trình bày) | "đi dày": **rẻ** nếu User duyệt phiếu thời lượng v7 (đang chờ); câu tự do: **đắt** (đã đóng hồ sơ) |
| A8 | **Không nhớ câu trả lời** ("quán thứ hai bạn vừa kể") | [ghi] lựa chọn an toàn có chủ đích; chưa đo trên bộ lớn hơn 6 câu bẫy | thấp–vừa | vừa (cần bộ câu hỏi tiếp lớn hơn) |
| A9 | **Mục web hay bị chặn hoặc không ra thông tin** | [log, 09–12/11] 28 lượt có tra web: 17 có mục · 7 "chưa xác minh" · 4 "không tin cậy"; mã kiểm cuối hỏng 11 lần (số thời gian thực 7, số ngoài đoạn trích 3, giá lưu trú 1) ⇒ rào chạy đúng nhưng ~4 / 10 lượt web người dùng không nhận thêm thông tin; [hôm nay] 3 / 8 | vừa | luật kiểm số so theo dãy chữ số (đã biết có ca nhầm) — **rẻ** để đếm ca chặn nhầm; nới luật = **vừa** (chạm an toàn) |
| A10 | **Câu ngày kiểu "tháng tới / cuối tuần"** còn do model tự tính | [ghi] giới hạn bậc ngày + âm lịch; [hôm nay] 1 câu "tuần sau" code tính đúng khoảng ngày, 1 câu "cuối tuần này" bị từ chối | thấp–vừa | rẻ (thêm dạng vào hàm lịch tính sẵn) — đếm trước: bộ câu ngày của B7 |

### B. Tốc độ

| # | Phần chưa ổn | Bằng chứng | Ảnh hưởng | Sửa |
|---|---|---|---|---|
| B1 | **Câu đi đường web rất chậm** | [ghi] chữ đầu mục web p50 ≈ 13 s; [log, 09–12/11] cả câu có web p50 ≈ 15 s, p95 ≈ 26 s (n = 28); [hôm nay] 3 loại câu đợt 2: cả câu trung vị 19–24 s (không stream) | **cao** cho đúng loại câu kho thiếu (người dùng chờ lâu để nhận "chưa xác minh") | vừa: trợ lý gọi tìm kho tới 4 lần rồi mới từ chối rồi mới tra web — đếm trước xem lần tìm thứ 3–4 có từng cứu được câu nào không; cắt được ⇒ rẻ |
| B2 | **Câu chào hỏi chậm, ảnh chậm** | [đo] câu chào hỏi chậm nhất 7,73 s (chạy song song đã thử, chưa đạt); ảnh 6–9 s | vừa | chào hỏi: đã thử 1 cách; ảnh: chưa thử — vừa |
| B3 | **Câu về Huế nhiều lần tìm**: tốc độ sau các bậc mới chưa có số chung | [log, 09–12/11] chữ đầu câu Huế không web p50 5,6 s / p95 11,3 s — **n = 17, lẫn lượt đo biến thể, không phải số đo**; số đo sạch gần nhất là sàn chung 09/11 | chưa rõ | cần một lượt đo chữ đầu sạch trên `main` (đã hẹn "đo lại lúc đóng code") |

### C. Tiền

| # | Phần chưa ổn | Bằng chứng | Ảnh hưởng | Sửa |
|---|---|---|---|---|
| C1 | **Tiền mỗi câu sát / vượt sàn 0,0005 USD** | [đo] 0,00047 / câu Huế (09/11); [log, 09–12/11] trung bình 0,000502, 22 / 42 câu vượt 0,0005 (lẫn lượt đo); [hôm nay] câu lưu trú / ăn gần / sự kiện ≈ 0,0013 / câu; câu có web ≈ 0,0018 | thấp với người dùng; **vừa** với yêu cầu phi chức năng đã chốt | vừa: mỗi lần gọi model đang trả phí "ghi đệm" cho gần hết phần vào mà không đọc lại đệm ([ghi] handoff: "ghi đệm giữ như cũ") — đáng một lượt đếm 0 USD trên log |
| C2 | Tiền ghi trong log là **cận dưới** khi người dùng bấm Dừng giữa chừng | [ghi] | thấp | rẻ / chấp nhận |

### D. Vận hành, đưa lên mạng

| # | Phần chưa ổn | Bằng chứng | Ảnh hưởng | Sửa |
|---|---|---|---|---|
| D1 | **Chưa chạy trên máy chủ thật; một nhà cung cấp model** | [ghi] bản Docker cục bộ đã đạt; AWS chưa thử | cao cho mốc "đóng = đã chạy trên AWS" | vừa–đắt (cần tài khoản, tên miền, khoá riêng — User) |
| D2 | **Log dùng chung cho test và server** ⇒ khi deploy không tách được số người dùng thật nếu có ai chạy test trên máy đó; harness đếm dòng log có thể hụt khi log xoay vòng | [hôm nay] 399 / 1.062 dòng là lỗi từ test; [ghi] bẫy xoay vòng 10 MB (log hiện 1,43 MB) | thấp hôm nay, **vừa** khi cần số thật | rẻ: test ghi log sang file khác |
| D3 | **Giới hạn lượt theo IP giữ trong RAM**, sau proxy phải cấu hình đúng tiêu đề chuyển tiếp | [ghi] checklist deploy; docstring `backend/api/gioi_han.py` còn ghi theo một cấu hình proxy khác với Dockerfile ([hôm nay] còn) | thấp–vừa (cấu hình sai ⇒ mọi người chung một sổ đếm) | rẻ |
| D4 | Log truy cập của uvicorn có ghi IP hay không | B đang probe hôm nay (report bước 0 của B) | thấp | rẻ |

### E. Tài liệu lệch code (rẻ, sửa khi chạm)

| # | Chỗ lệch | Bằng chứng |
|---|---|---|
| E1 | Chú thích `settings.yaml` cạnh hai cờ đang **bật** (công cụ ngày, hỏi bằng ảnh) còn ghi "TẮT tới khi đạt" | [hôm nay] còn nguyên |
| E2 | Báo cáo khâu 07 còn dòng "câu lịch thuần ⇒ ngoài phạm vi"; báo cáo luồng 01 thiếu nút "Báo thông tin chưa đúng" và ý "câu không về Huế cũng gửi đoạn kho tới OpenAI"; vài số dòng `file:dòng` cũ ở báo cáo 05 / 06 / 07 / 10 | [ghi] |
| E3 | Nhãn cũ của một câu trong bộ câu ngày 30/10 còn ghi "từ chối" | [ghi]; plan B7 bản 2 §3 đã có cách xử lý trước khi sinh |
| E4 | `Project_Status.md` §1 ghi sai model của các session; dòng "Qdrant tắt" đã cũ | [hôm nay] |

## 3. Năm mục C xếp trên cùng (đề xuất thứ tự cho A)

1. **A1 ăn gần** — lỗi rõ nhất đếm được hôm nay (5 / 6), sửa bằng dữ liệu, không cần tính năng mới.
2. **A2 từ chối cả câu** — gốc chung của từ chối nhầm ≈ 3 % và của hai bậc âm 09/11; cần lượt đếm 0 USD trên kết quả Golden của B7 trước khi quyết.
3. **B1 đường web chậm 15–25 s** — đúng lúc kho thiếu thì người dùng lại chờ lâu nhất; đếm trước xem các lần tìm kho thứ 3–4 có ích không.
4. **A4 số tiền / giờ không được kiểm với đoạn trích** — chưa thấy lỗi, nhưng là loại lỗi nặng nhất; đếm 0 USD trên lượt Golden B7 là đủ để biết có đáng làm.
5. **A6 không biết người dùng hỏi gì** — một nhãn loại câu trong log là việc rẻ, làm trước khi deploy thì từ ngày đầu đã có số.

Ba trong năm mục (A2, A4, B1) **dùng lại được kết quả lượt B7 giữa kỳ** để đếm, không tốn thêm tiền API.

## 4. Giới hạn của bản rà này

- C không chạy lại lượt đo nào; số [đo] lấy từ handoff, `Project_Status.md`, bài học và STATUS của C — chưa mở lại từng report gốc.
- Số [log] lẫn test và lượt đo biến thể; số [hôm nay] là 18 câu tự viết, một lượt.
- Không rà giao diện bằng trình duyệt, không rà hỏi bằng ảnh / giọng nói / bản đồ (đang dở hoặc có thước riêng).
