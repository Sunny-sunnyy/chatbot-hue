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
| A1 | **Câu "ăn gì / quán nào gần điểm X"** phần lớn không trả lời được từ kho | [hôm nay] 5 / 6 câu không đủ dùng (3 từ chối, 2 một phần); kho có 81 bài quán / cà phê nhưng chỉ 12 bài có câu định vị theo điểm tham quan (15 nếu tính cả thư mục món ăn), 4 bài có toạ độ | **cao** (loại câu khách du lịch hỏi tự nhiên) | **rẻ–vừa**: thêm dòng "khu / gần điểm nào" cho bài quán (sửa kho, build lại chỉ mục), đo lại 6 câu + bộ an toàn |
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

## 3b. Đếm trên B7 giữa kỳ (0 USD, chỉ đọc file sinh của B — ghi 19:25 12/11/2026; phần chờ B ghi rõ "CHỜ")

A giao sau khi đọc mục 3. Nguồn: lượt sinh B7 giữa kỳ bên trợ lý trên `main` `dfd0c96` + bên RAG mốc (`data/phase_9/b7/`, private). C **không** đọc thư mục chấm mù,
không chạy lại, không sửa file của B. Script: `data/ra_khoang_cach_2026-11-12/tools/dem_b7.py` (in số đếm + `case_index`). Định nghĩa dùng chung với báo cáo của E
(`e_khoang_cach_agentic.md` mục 4, ứng viên 1–3). Chưa có điểm chấm ⇒ mọi số dưới đây là **đếm bằng code**, chưa nói được câu trả lời đúng / đủ tới đâu.

### (a) Từ chối nhầm: "tìm trượt" hay "model không dùng đoạn đúng"? — Golden 176, đường chỉ-kho

| | Trợ lý (`main`) | RAG mốc |
|---|---:|---:|
| Câu trong kho bị từ chối (trên 158) | **3** (2 nhiều nguồn, 1 hỏi một ý) | **13** (9 nhiều nguồn, 3 so sánh, 1 hỏi một ý) |

- Cả 3 câu trợ lý từ chối cũng là câu RAG mốc từ chối. Cả 3 có nhãn đoạn đúng: lần tìm đầu chỉ phủ **1 / 2 · 1 / 2 · 0 / 2** ý cần có; model đã tìm thêm 1–2 lần,
  2 / 3 câu lần tìm thêm **không ra đoạn mới nào**.
- Trên 55 câu có nhãn đoạn đúng: lần tìm đầu phủ đủ mọi ý ở 32 câu — **0 câu trong số này bị từ chối**; thiếu ít nhất một ý ở 23 câu (13 nhiều nguồn, 7 so sánh) —
  3 câu bị từ chối, 18 câu model có tìm thêm.
- **Kết luận: 3 / 3 câu từ chối nhầm là "tìm trượt"; 0 câu "có đủ đoạn đúng mà model không dùng".** ⇒ **không đủ lỗi** để sửa lời dặn theo hướng "bớt từ chối";
  phần còn lại (3 câu ≈ 2 %) nằm ở khâu tìm.
- **Trả lời một phần (bổ sung 19:28 12/11/2026, sau khi B chấm mù xong Golden):** trong 32 câu lần tìm đầu phủ đủ ý, **0 câu** có điểm Đủ ý ≤ 3. Cả 5 câu trợ lý trả lời mà Đủ ý ≤ 3
  (4 nhiều nguồn, 1 có điều kiện; không câu nào Đúng ≤ 3) đều thuộc nhóm lần tìm đầu **thiếu** đoạn đúng ⇒ cùng kết luận: thiếu ý là do tìm, không phải model bỏ đoạn đúng.
  Phân bố Đủ ý của 155 câu đã trả lời: 136 câu 5 điểm · 14 câu 4 · 4 câu 3 · 1 câu 2.
- Lệch với quan sát hôm nay ở mục 2 dòng A2 (1 / 18 câu tự viết bị từ chối dù kho có bài): câu đó có phép tính ngày, khác loại câu Golden; một ca, chưa đủ để kết luận ngược.

### (b) Các lần model tìm thêm có ích không — Golden trong kho (158 câu)

| Model tìm thêm | Số câu | RAG mốc từ chối ⇒ trợ lý trả lời | Trợ lý từ chối | USD / câu (TB) | Thời gian gọi model (trung vị) |
|---|---:|---:|---:|---:|---:|
| 0 lần | 132 | 0 | 0 | 0,00039 | 4,4 s |
| 1 lần | 22 | **8** | 2 | 0,00055 | 7,7 s |
| 2 lần | 4 | **2** | 1 | 0,00067 | 10,5 s |

- **10 / 10 câu trợ lý cứu được so với RAG mốc đều là câu model có tìm thêm**; không câu nào mốc trả lời được mà trợ lý lại từ chối.
- 30 lần tìm thêm: lần thứ nhất 26 lần (20 ra đoạn mới, 6 không ra gì), lần thứ hai 4 lần (cả 4 ra đoạn mới, cứu 2 câu). **Không câu Golden trong kho nào dùng tới lần thứ ba.**
- Giá của tìm thêm: mỗi lần thêm ≈ +0,00012–0,00016 USD và ≈ +3 giây gọi model. Trung bình câu trong kho 0,00042 USD; 23 / 158 câu vượt 0,0005.
- **Kết luận: tìm thêm đang có ích rõ trên Golden ⇒ không cắt.** Nghi vấn "lần tìm thứ 3–4 vô ích" (mục 2 dòng B1) **không có bằng chứng trên Golden**; nó chỉ
  thấy ở câu kho thiếu hẳn ⇒ đếm riêng ở mục (b2) dưới.

### (b2) Câu kho thiếu hẳn — đường web (bổ sung 19:28 12/11/2026)

Hai nguồn: lượt web của B7 (17 câu, chạy trong tiến trình — file **không ghi** số lần tìm và thời gian) và 18 câu C gửi qua server thật hôm nay (có đủ từng bước).

- **Lượt web B7 (17 câu "Huế nhưng kho thiếu"):** 16 / 17 kho từ chối và mở cổng web; mục web có nội dung 10, "không tin cậy" 6. Tiền: **0,00183 USD / câu đi web** (câu không đi web 0,00057).
- **8 câu đi web trong 18 câu của C:** cả câu trung vị **22,9 giây**, 0,0020 USD / câu. Thời gian nằm chủ yếu ở **3–4 lượt gọi model của trợ lý trước khi từ chối** (10–20 giây);
  tra web + viết mục web chỉ 5–9 giây. **6 / 8 câu model xin tìm kho lần thứ ba và bị code chặn vì hết lượt (0 đoạn mới)** — mỗi lần như vậy vẫn tốn một lượt gọi model
  (≈ 0,0001 USD và vài giây) mà không thể đổi kết quả. 2 câu còn lại dừng ở 2 lần tìm.
- 10 câu kho trả lời được trong 18 câu: trung vị 16,8 giây cả câu, model tìm thêm 2 lần ở 6 / 10 câu (loại câu này khó hơn Golden, nơi 132 / 158 câu không cần tìm thêm).
- **Kết luận: đủ lỗi cho một sửa nhỏ** — khi đã hết lượt tìm thì không để model xin tìm nữa (bỏ công cụ ở lượt cuối, hoặc trả lời / từ chối ngay): cắt một lượt gọi model vô ích ở
  6 / 8 câu đi web, không đụng 2 lần tìm đang có ích. Đây là bản hẹp của ứng viên 5 trong báo cáo của E. Chưa đo ⇒ cần một lượt nhỏ có bộ an toàn trước khi bật.
- Giới hạn: 8 câu tự viết, một lượt, đường `/api/chat` không stream (người dùng thật thấy chữ đầu sớm hơn tổng thời gian này).

### (c) Số tiền / giờ / ngày trong câu trả lời ↔ chữ của đoạn ngữ cảnh — 155 câu trong kho trợ lý đã trả lời

| | Số tiền | Chuỗi số khác (giờ, ngày, năm, tuổi… từ 2 chữ số) |
|---|---:|---:|
| Có trong 10 đoạn của lần tìm đầu | 32 | 131 |
| Câu có "Lịch hệ thống" (ngày do code tính) | — | 3 |
| Không ở 10 đoạn đầu, có ở đoạn khác của kho | 2 | 10 |
| **Không có ở đoạn nào của kho** | **0** | **0** |

- 12 số "ngoài 10 đoạn đầu" nằm ở 11 câu. 4 câu là câu model có tìm thêm (file sinh không ghi id đoạn tìm thêm ⇒ **không kiểm được**, nhiều khả năng số đến từ đoạn
  tìm thêm). 7 câu không tìm thêm, C xem từng ca: 4 ca số lấy **từ chính câu hỏi** (giờ, tuổi, tháng người hỏi nêu) · 1 ca năm có trong đoạn nhưng viết liền ngày tháng ·
  1 ca thuộc **câu cố định do code nối** · 1 ca model **tự trừ hai giá** có trong đoạn (phép trừ đúng).
- **Kết luận: 0 số tiền / giờ sai nguồn trên 155 câu ⇒ dưới ngưỡng E ghi trước (≥ 3 câu) ⇒ không đủ lỗi để xây bộ kiểm.** Hai ghi chú nếu sau này vẫn làm: bộ kiểm
  phải cho phép số trong câu hỏi và câu cố định của code (4 + 1 / 7 ca báo nhầm ở trên); có 1 ca model tự làm phép tính tiền — đúng, nhưng thuộc loại "phép tính ⇒ code".
- Giới hạn: đối chiếu theo **dãy chữ số**, không theo nghĩa (số đúng nhưng gắn nhầm đối tượng không bị bắt); chỉ lượt Golden, chưa đếm bộ an toàn.

### (d) Độ ổn định giữa 2 lượt (bên trợ lý)

- **An toàn 32 câu × 2 lượt: 0 câu đổi kết luận** trả lời ↔ từ chối (28 trả lời, 4 từ chối + mở web ở cả hai lượt; tuyến, cổng web, lỗi trích dẫn đều giống nhau).
  Chữ câu trả lời giống hệt ở 5 / 32 câu — khác chữ là bình thường.
- **"Có ↔ không cảnh báo" giữa 2 lượt an toàn (bổ sung 19:55 12/11/2026, sau khi B chấm mù xong; đọc `compare` của B, 27 câu có cảnh báo cần giữ):** đảo cảnh báo 0 / 0 và sai điều kiện
  0 / 0 ở cả hai lượt (ổn định). Nhãn **"thiếu cảnh báo" đổi ở 4 / 27 câu** giữa hai lượt (lượt 1 có 8 câu thiếu, lượt 2 có 6 câu; 3 câu chỉ thiếu ở lượt 1, 1 câu chỉ thiếu ở lượt 2);
  5 câu thiếu ở cả hai lượt. Bên RAG mốc (1 lượt) cũng thiếu 8 câu. Ở 1 câu loại miễn / giảm, sinh lại cho thấy trợ lý thiếu 3 / 6 lần so với mốc 1 / 6 (B đã ghi là sàn phạm).
  ⇒ **vượt ngưỡng E ghi trước (≥ 3 câu đổi)**: việc "có nhắc cảnh báo hay không" **không ổn định** giữa các lần hỏi cùng một câu. Chưa tách được dao động của model với
  dao động của người chấm (mỗi lượt là chữ khác nhau, chấm riêng).
- **Ngoài phạm vi (S2) 44 câu × 2 lượt (bổ sung 19:28 12/11/2026): 0 câu đổi kết luận** — 42 câu nhận câu "ngoài phạm vi", 2 câu nhận câu "kho không đủ thông tin" và **mở cổng web** ở cả
  hai lượt (web trả "không tin cậy" nên không hiện nội dung). Ổn định, nhưng 2 câu này là việc của sàn "ngoài phạm vi có mục web" — B / E xét trong report B7, C chỉ ghi nhận.
- **Kết luận độ ổn định:** trả lời ↔ từ chối **0 / 76 câu đổi** (ổn định); nhắc cảnh báo **4 / 27 câu đổi** ⇒ **đủ lỗi để xem tiếp**: trước khi xây gì, một lượt đếm rẻ theo
  đề xuất của E — sinh thêm lần 3 cho bộ an toàn (≈ 0,02 USD) và chấm cả 3 lần trong **cùng một lô mù** để tách dao động model ↔ người chấm; 5 câu thiếu ở cả hai lượt là
  nơi nên đọc trước (thiếu ổn định = lỗi thật, không phải nhiễu).

### (e) Bốn câu trợ lý tụt Đủ ý so với RAG mốc (A hỏi thêm; số tụt đúng bằng ngưỡng 4)

| | 4 câu tụt |
|---|---|
| Loại câu | 2 câu có điều kiện · 1 nhiều nguồn · 1 hỏi một ý |
| Mức tụt | cả 4 câu **5 → 4** (1 điểm); điểm Đúng giữ 5 → 5 ở cả 4 |
| Định tuyến | cả 4 đúng tuyến trợ lý Huế |
| Tìm thêm | **0 / 4** câu model tìm thêm; 10 đoạn ngữ cảnh **giống hệt** bên RAG mốc ở cả 4 |
| Câu trả lời | cả 4 **ngắn hơn** bản mốc (còn 37 %–84 % số chữ) |

- **Có chung một gốc:** cùng ngữ cảnh, cùng tuyến, trợ lý viết ngắn hơn và bỏ một ý phụ. **Không** phải tìm thêm kéo đoạn nhiễu, **không** phải định tuyến.
- Không phải xu hướng chung: trên 132 câu hai bên cùng 10 đoạn và không tìm thêm, độ dài trung vị trợ lý / mốc = 1,00 (9 câu ngắn hơn ≥ 30 %, 12 câu dài hơn ≥ 30 %); trong 9 câu
  ngắn hơn hẳn, 2 câu tụt, 7 câu giữ điểm. ⇒ khớp với **dao động lời văn của model giữa hai lần sinh** (hai bên dùng lời dặn khác nhau) hơn là một lỗi có hệ thống; mỗi câu chỉ
  có một lượt nên không tách được khỏi nhiễu người chấm (A/A 01/11: 1 câu).
- Đối trọng: 10 câu trợ lý **tăng** Đủ ý (6 câu mốc từ chối, 7 câu nhờ tìm thêm; 6 nhiều nguồn, 2 so sánh). Chênh trung bình +0,19 [0,05; 0,36] trên 129 câu.
- **Kết luận: không đủ lỗi để sửa.** Nếu lượt cuối tháng 12 lại thấy đúng kiểu "cùng ngữ cảnh, ngắn hơn, mất ý" ở ≥ 4 câu thì mới xét lời dặn về độ đủ ý.

### Tóm tắt (đổi thứ tự ưu tiên ở mục 3)

| Mục ở mục 3 | Sau khi đếm trên B7 |
|---|---|
| (2) từ chối cả câu | **hạ**: trên Golden chỉ còn 3 câu từ chối + 5 câu thiếu ý, tất cả do tìm trượt; 0 câu "có đủ đoạn đúng mà từ chối / thiếu ý" |
| (3) đường web / tìm nhiều lần chậm | **giữ, thu hẹp thành một sửa nhỏ**: tìm thêm có ích trên Golden (cứu 10 câu) ⇒ không cắt; chỉ cắt lượt xin tìm lần ba bị chặn (6 / 8 câu đi web) |
| (4) số tiền / giờ chưa kiểm với đoạn trích | **hạ**: 0 ca sai trên 155 câu ⇒ không xây |
| độ ổn định | trả lời ↔ từ chối 0 / 76 câu đổi; **nhắc cảnh báo 4 / 27 câu đổi + 5 câu thiếu ở cả hai lượt ⇒ mục mới, xếp cao** (thiếu cảnh báo là loại lỗi nặng nhất theo thứ tự lỗi) |
| 4 câu tụt Đủ ý | chung gốc "cùng ngữ cảnh, viết ngắn hơn"; không phải tìm / định tuyến; không đủ lỗi để sửa |

## 3c. Chẩn đoán hai sàn B báo phạm ở lượt B7 giữa kỳ (0 USD, chỉ đọc — ghi 19:59 12/11/2026)

A giao. Nguồn: file sinh + nhãn chấm an toàn của B (`data/phase_9/b7/an_toan/`, `s2/`), các lượt đo cũ của bậc cổng 2 nhóm (`data/phase_9/g_cong/ket_qua/`), report bậc đó.
C không sửa gì, không chạy lại. Nhãn: **[chứng minh]** = đọc thấy trực tiếp trong dữ liệu · **[giả thuyết]** = suy ra, chưa có phép thử tách.

### (1) An toàn — "thiếu cảnh báo mới" ở 1 câu loại miễn / giảm (trợ lý 3 / 6 lần ↔ RAG mốc 1 / 6)

| Câu hỏi của A | Trả lời |
|---|---|
| Ngữ cảnh trợ lý nhận có đoạn chứa điều kiện bị coi là thiếu không? | **Có — và chỉ trợ lý có.** [chứng minh] Mọi lần trợ lý bị gắn "thiếu" đều vì **một** điều kiện phụ (ưu đãi chỉ áp dụng trong giờ mở cửa), người chấm trích từ đoạn số 12 / 13 — tức đoạn do **model tìm thêm** mang về (ngữ cảnh trợ lý 15–17 đoạn) |
| Khác gì ngữ cảnh mốc? | [chứng minh] Mốc chỉ có 10 đoạn của lần tìm đầu, **không có** đoạn chứa điều kiện đó ⇒ người chấm **không thể** gắn "thiếu điều kiện này" cho mốc. Lần duy nhất mốc bị gắn thiếu là vì một điều kiện khác |
| Tìm trượt hay model bỏ? | **Không phải tìm trượt.** Model có đoạn đó trong tay; 3 / 8 lần nó nêu điều kiện này, 5 / 8 lần không. Trong 5 lần không nêu: 2 lần cả hai người chấm gắn thiếu, 2 lần chỉ một người gắn, 1 lần không ai gắn ⇒ có cả dao động của model lẫn của người chấm |
| Có lịch hệ thống / lời dặn nào chen vào? | [chứng minh] Không thấy dòng lịch hệ thống hay câu cố định nào trong câu trả lời; phần chính (được miễn, giấy tờ cần xuất trình) đúng và giống nhau ở mọi lần, hai bên |
| Câu trả lời ngắn hơn không (cùng gốc 4 câu tụt)? | **Không cùng gốc.** 4 câu tụt là "cùng ngữ cảnh, viết ngắn hơn"; câu này là "ngữ cảnh **nhiều hơn** mốc". Độ dài trợ lý 195–289 chữ; mốc 190–504 chữ, dài hơn ở các lần mốc kể thêm một mức phí ở nguồn khác và nói "nguồn mâu thuẫn" (trợ lý trả lời thẳng, không kể mâu thuẫn — người chấm không tính đó là thiếu) |

**Kết luận (sửa 20:04 12/11/2026 sau phản biện của E trong vòng tự soi; E kiểm độc lập: đoạn có ở 8 / 8 lần của trợ lý, 0 / 7 lần của mốc):** sàn phạm ở câu này có **hai nửa**.
[chứng minh] Nửa thứ nhất **do cách so**: thước "thiếu điều kiện có trong ngữ cảnh" chấm mỗi bên theo ngữ cảnh của chính nó; trợ lý tìm thêm nên có thêm điều kiện để "thiếu",
mốc thì không. [chứng minh] Nửa thứ hai **là lỗi thật của khâu viết**: trợ lý có đoạn trong tay mà không nêu điều kiện ở 5 / 8 lần — cùng gốc với mục (1b). Việc đổi thước
**không** dùng để hạ sàn: điều kiện từ đoạn tìm thêm vẫn phải báo (báo riêng), và thước mới phải ghi trước khi sinh lượt cuối. [giả thuyết] Mức nguy hiểm thấp: điều kiện bị thiếu là điều hiển nhiên (chỉ vào được trong giờ mở cửa), không phải cảnh báo an toàn.
**Sửa nhỏ nhất khả dĩ (không làm):** sửa ở **thước**, không sửa hệ thống — khi so "mới so với mốc", chỉ tính điều kiện nằm trong đoạn **cả hai bên cùng có** (hoặc chấm mốc trên
ngữ cảnh của trợ lý); điều kiện từ đoạn tìm thêm báo riêng. Đây là đổi tiêu chí ⇒ ghi vào plan lượt cuối trước khi đo, không áp ngược cho lượt giữa kỳ.

### (1b) Đọc 5 câu thiếu cảnh báo ở **cả hai** lượt + 4 câu đổi nhãn giữa hai lượt

| Nhóm | Số câu | Đọc thấy gì |
|---|---:|---|
| Thiếu ở cả hai lượt của trợ lý | 5 (2 cảnh báo an toàn, 1 sông nước, 1 giấy tờ, 1 giờ) | [chứng minh] Ở **4 / 5 câu RAG mốc thiếu đúng các điều kiện đó** ⇒ lỗi có từ Phase 1–8, trợ lý không thêm vào. Đoạn chứa điều kiện nằm trong 10 đoạn đầu ở cả hai bên ⇒ **không phải tìm trượt**; model trả lời đúng điều được hỏi và bỏ điều kiện đứng cạnh. Câu còn lại (loại giờ): mỗi lượt chỉ một trong hai người chấm gắn ⇒ nhiễu chấm |
| — trong đó đòi hợp lý | 2–3 | câu hỏi về một dịch vụ dưới nước mà câu trả lời không nhắc "không xuống nước khi mưa lớn / mùa lũ có thể tạm ngừng"; câu hỏi giấy tờ mà chỉ trả lời một trường hợp ⇒ thiếu thật |
| — trong đó thước đòi nhiều | 2 | câu trả lời đã nêu 4–5 cảnh báo chính, bị gắn thiếu vì chưa kể hết mọi cảnh báo phụ có trong đoạn |
| Đổi nhãn giữa hai lượt | 4 | 2 câu chỉ **một** người chấm gắn (nhiễu chấm) · 1 câu điều kiện đến từ đoạn tìm thêm (cùng cơ chế mục (1)) · 1 câu model lúc nêu lúc không (dao động thật; sinh lại: trợ lý 3 / 3 ↔ mốc 3 / 3 theo luật "một trong hai người chấm") |

**Kết luận (1b):** gốc ở **khâu viết**, không ở khâu tìm; phần lớn là lỗi cũ chung với RAG mốc. Trong 14 lần gắn "thiếu" của hai lượt trợ lý, 4 lần chỉ một người chấm gắn.
**Vì vậy C đề xuất KHÔNG chạy lượt 3 an toàn (≈ 0,02 USD)**: việc đọc 0 USD đã tách được 4 câu đổi nhãn (2 nhiễu chấm · 1 do đoạn tìm thêm · 1 dao động model); lượt 3 không
đổi kết luận nào ở trên. Việc đáng làm hơn nếu User muốn giảm "thiếu cảnh báo": một câu trong lời dặn trả lời kiểu "bằng chứng có cảnh báo an toàn gắn trực tiếp với việc người
hỏi sắp làm thì nêu kèm một câu" — là đổi lời dặn ⇒ một bậc đo đủ (an toàn ×2 + Golden), có rủi ro câu trả lời dài ra; chưa có plan.

### (2) Ngoài phạm vi có mở cổng web — 2 / 44 câu, ở cả hai lượt

| | Câu thứ nhất (loại y tế chung) | Câu thứ hai (loại "có nhắc Huế nhưng việc là soạn văn bản") |
|---|---|---|
| Đường đi hôm nay | định tuyến đưa vào trợ lý ⇒ trợ lý trả câu "kho không đủ thông tin" (không phải câu "ngoài phạm vi") ⇒ code mở cổng web ⇒ web bị lọc "không tin cậy" | như bên trái |
| Người dùng thấy | chỉ câu từ chối + dòng "chưa tra được thông tin đáng tin"; **không có nội dung sai** | như bên trái |
| Tốn | ≈ 0,002 USD / câu + **câu hỏi được gửi tới dịch vụ tìm web** (đường ra ngoài) | như bên trái |
| Lịch sử [chứng minh] | Đúng câu này, đúng đường này ở lượt khoá phương án B tối 09/11 — là **1 câu User đã nhận làm giới hạn** | Ở lượt khoá phương án B và lượt tốc độ chung 09/11 trên `main`: bị chặn đúng ở định tuyến. Nhưng ở 2 lượt đo khác tối 09/11 và 10/11 (nhánh khác, lời dặn định tuyến chưa đổi) nó **đã** đi vào trợ lý; 08/11 có lượt vào trợ lý nhưng trợ lý dùng đúng câu "ngoài phạm vi" |
| Xếp loại | **Giới hạn đã nhận** — không mới | **Cùng cơ chế, khác cửa vào ⇒ tính là loại mới so với cái User đã nhận** (User nhận ca "định tuyến xếp nhầm khẩn cấp"; ca này là "câu ranh giới có chữ Huế, định tuyến dao động giữa các lần + trợ lý chọn nhầm câu từ chối") |

- [chứng minh] Câu thứ hai dao động từ trước khi đổi lời dặn định tuyến ngày 10/11 ⇒ **không quy được** cho thay đổi "câu lịch chung"; [giả thuyết] thay đổi đó có thể làm
  nó nghiêng hẳn về phía trợ lý (hôm nay 2 / 2) vì câu có nhắc số ngày — muốn biết phải chạy câu đó vài lần trên bản trước 10/11 (≈ 0,002 USD), chưa làm.
- Hai lớp cùng trượt mới ra lỗi: (a) định tuyến cho câu ngoài phạm vi vào trợ lý; (b) trợ lý trả câu "không đủ thông tin" thay vì câu "ngoài phạm vi". Lớp (b) chính là rủi ro
  spec đã ghi trước ("model chọn nhầm câu").
- **Sửa nhỏ nhất khả dĩ (không làm):** (i) cho câu loại y tế: khi định tuyến đã xếp "khẩn cấp" thì code **không mở cổng web** cho lượt đó — một điều kiện ở chỗ mở cổng, tất
  định, không đổi lời dặn; chặn đúng ca User đã nhận; (ii) cho câu ranh giới "có chữ Huế": không có tín hiệu code nào ⇒ hoặc nhận thêm giới hạn này (hậu quả: người dùng thấy câu
  từ chối, tốn ≈ 0,002 USD, câu hỏi đi ra dịch vụ tìm web), hoặc chỉnh lời dặn — là một bậc đo đủ. C nghiêng về (i) + nhận (ii) ở lượt giữa kỳ, quyết lại ở lượt cuối.
- Giới hạn: file lượt S2 không ghi trường "định tuyến xếp khẩn cấp" ⇒ việc câu thứ nhất hôm nay vẫn đi qua nhãn khẩn cấp là suy từ lượt 09/11 [giả thuyết]; kiểm bằng một lần
  gửi câu đó qua server và đọc log (≈ 0,002 USD).

## 3d. Danh sách sau khi đếm (xếp lại theo bằng chứng 12/11 — ghi 20:01 12/11/2026; thay thứ tự ở mục 3)

Thứ tự lỗi User đã chốt (nặng ⇒ nhẹ): sai / thiếu cảnh báo an toàn, điều kiện vào khu vực › nói chắc sai › trả lời câu ngoài kho › thiếu ý › từ chối nhầm.
Mọi dòng là **đề xuất**, chưa làm gì. Giờ = giờ agent; tiền = USD API ước.

### Đáng làm (xếp theo mức nặng × độ chắc của bằng chứng)

| # | Việc | Lỗi đếm được hôm nay | Mức nặng | Sửa nhỏ nhất khả dĩ · cách đo | Giờ / tiền | Cần User quyết |
|---|---|---|---|---|---|---|
| 1 | **Khâu viết bỏ cảnh báo / điều kiện dù đoạn có trong ngữ cảnh** | 5 / 27 câu an toàn thiếu ở **cả hai** lượt (2–3 câu thiếu thật, 2 câu do thước đòi nhiều); 4 / 5 câu RAG mốc cũng thiếu ⇒ lỗi có từ Phase 1–8 (mục 3c 1b) | **nặng nhất** (thiếu cảnh báo an toàn) — nhưng không phải lỗi mới | Một câu trong lời dặn trả lời: bằng chứng có cảnh báo an toàn gắn trực tiếp với việc người hỏi sắp làm ⇒ nêu kèm một câu. Đo: an toàn 32 ×2 (thiếu cảnh báo giảm ở ≥ 2 trong 3 câu thiếu thật, 0 lỗi mới ở 3 số còn lại) + Golden 176 (không tụt; câu trả lời không dài ra quá mức ghi trước) + S2. **Đã thử gần giống 1 lần:** vòng chỉnh lời dặn của bậc cổng 2 nhóm 09/11 sửa được "sai điều kiện" nhưng thiếu cảnh báo mưa lũ **không đổi** và làm trượt sàn ngoài phạm vi (2 / 44) ⇒ phải bỏ. Phase 8 cũng có một lần đổi lời dặn "trả lời một phần" phạm sàn ngoài kho ⇒ đây là việc **dễ âm** | ~4 giờ · ≤ 0,15 (là bậc đo đủ, không phải mức nhẹ) | có mở một bậc chỉnh lời dặn trước lượt cuối không; nhận trước là có thể âm |
| 2 | **Ăn gần điểm X** — thêm dòng định vị cho bài quán (plan nháp `2026-11-12-an-gan-dinh-vi-quan-plan.md`) | 5 / 6 câu không đủ dùng từ kho; 12 / 81 bài quán có câu định vị | thiếu ý + từ chối nhầm (nhẹ) — nhưng **tần suất cao nhất** đo được và là câu khách hỏi tự nhiên | sửa kho ≤ 53 bài, build lại chỉ mục; 12 câu ăn gần ≥ 8 đủ dùng + an toàn ×2 + tìm 158 câu | 3–4 giờ · ≤ 0,08 | làm / không; cách A (chỉ từ kho) hay B (toạ độ dữ liệu mở, C khuyến nghị) |
| 3 | **Định tuyến đã xếp "khẩn cấp" ⇒ code không mở cổng web** | 1 / 44 câu ngoài phạm vi (loại y tế), 2 / 2 lượt; đúng ca User nhận làm giới hạn 09/11 (mục 3c (2)) | thấp về nội dung (người dùng chỉ thấy câu từ chối) · có **đường ra**: câu hỏi y tế gửi tới dịch vụ tìm web + ≈ 0,002 USD / câu | một điều kiện tất định ở chỗ mở cổng web; test: lượt có nhãn khẩn cấp ⇒ không gọi web; chạy lại 44 câu ngoài phạm vi ×1 + 30 câu quan sát khẩn cấp (không câu nào mất mục web **đáng có**) | ~45 phút · ≈ 0,01 | không cần hỏi nếu A coi là siết một giới hạn đã nhận; lưu ý: câu khẩn cấp thật về Huế mà kho thiếu cũng sẽ không còn mục web |
| 4 | **Hết lượt tìm thì không cho model xin tìm nữa** (plan nháp `…-het-luot-tim-plan.md`; probe thư viện [Chạy] đạt) | 6 / 8 câu kho thiếu tốn một lượt gọi model vô ích; cả câu trung vị 22,9 s | không thuộc thang lỗi chất lượng — tốc độ + tiền ở đúng loại câu kho thiếu | bỏ công cụ tìm sau 2 lần tìm thật; 16 câu kho thiếu + 26 câu Golden có tìm thêm + an toàn ×2 + ngoài phạm vi 44 | ~2 giờ · ≤ 0,09 | làm / không |
| 5 | **Nhãn loại câu trong log** (plan nháp `…-nhan-loai-cau-plan.md`) | hôm nay không đếm được theo loại câu từ log | không phải lỗi chất lượng — thiếu dữ liệu để xếp ưu tiên | trường nhãn do code dò từ khoá, chỉ ghi tên nhãn | ~1 giờ · ≈ 0,001 | đồng ý ghi nhãn loại câu (không nội dung) vào log khi đưa lên mạng |
| 6 | **Câu hỏi cơ sở lưu trú cụ thể** ⇒ "khu nên ở + link tìm phòng do code dựng" | 3 / 4 câu kho từ chối; web cứu 2 / 3 | từ chối nhầm (nhẹ nhất) | đã nằm trong backlog Phase 11; chưa có plan | ~3 giờ · ≤ 0,05 (ước thô) | làm trước hay sau lượt cuối |
| 7 | **Sửa thước "thiếu cảnh báo mới" cho lượt cuối** (so trên đoạn cả hai bên cùng có; điều kiện từ đoạn tìm thêm báo riêng) | sàn an toàn phạm ở 1 câu chủ yếu do cách so (mục 3c (1)); E đang kiểm độc lập | ảnh hưởng **kết luận** của lượt cuối, không đổi hệ thống | sửa plan B7 trước lượt cuối; **không** sửa ngược kết quả giữa kỳ (vẫn ghi "phạm") | ~30 phút · 0 | duyệt đổi tiêu chí (sau khi người khác review) |

### Nhận làm giới hạn / không làm (có số đếm)

| Việc | Số đếm | Vì sao không làm |
|---|---|---|
| Câu ranh giới "có chữ Huế nhưng việc không phải hỏi về Huế" mở cổng web | 1 / 44, 2 / 2 lượt; dao động định tuyến đã có từ trước 10/11 | không có tín hiệu code; chỉnh lời dặn định tuyến là một bậc đo đủ cho 1 câu ⇒ đề xuất nhận thêm giới hạn này ở giữa kỳ, quyết lại ở lượt cuối |
| Sửa lời dặn để "bớt từ chối cả câu" | 3 / 158 câu từ chối + 5 câu thiếu ý, **tất cả do tìm trượt**; 0 câu đủ đoạn đúng mà bị từ chối | lỗi không nằm ở lời dặn. Phần tìm trượt (8 câu, đa số nhiều nguồn) chỉ có một ứng viên cũ chưa đo: thử lại xếp lại ở 10 đoạn |
| Bộ kiểm số tiền / giờ với đoạn trích | 0 số sai nguồn / 155 câu | dưới ngưỡng ghi trước (≥ 3) |
| Sửa 4 câu tụt Đủ ý | 4 câu, cùng ngữ cảnh, viết ngắn hơn; đối lại 10 câu tăng | khớp dao động lời văn + nhiễu chấm; xem lại ở lượt cuối |
| Chạy lần 3 bộ an toàn | — | A quyết bỏ: không đổi quyết định nào |
| Trang / lịch sự kiện theo ngày | 4 / 6 câu kho trả lời đủ dùng | không đủ lỗi; không nguồn nào có lịch sự kiện của tuần |
| Cắt bớt số lần tìm thêm | tìm thêm cứu 10 / 10 câu so với mốc | đang có ích |

**Gợi ý thứ tự làm nếu User chỉ chọn vài việc:** 3 và 5 (rẻ, chắc, làm ngay được) ⇒ 2 (lợi rõ nhất cho người dùng) ⇒ 4 ⇒ rồi mới cân 1 (nặng nhất nhưng dễ âm và là lỗi cũ).
Việc 7 phải xong trước lượt cuối dù chọn gì.

## 4. Giới hạn của bản rà này

- C không chạy lại lượt đo nào; số [đo] lấy từ handoff, `Project_Status.md`, bài học và STATUS của C — chưa mở lại từng report gốc.
- Số [log] lẫn test và lượt đo biến thể; số [hôm nay] là 18 câu tự viết, một lượt.
- Không rà giao diện bằng trình duyệt, không rà hỏi bằng ảnh / giọng nói / bản đồ (đang dở hoặc có thước riêng).
