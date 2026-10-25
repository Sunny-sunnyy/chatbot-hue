# Đề xuất cho bạn: nên sửa gì sau khi rà code Phase 0–7

**Cập nhật lần cuối: 18:56 25/10/2026 — bản 2: đủ kiểm chéo hai chiều (B kiểm C 5 / 5 đúng; C kiểm B 4 đúng + 1 đúng một phần).**
Người viết: A · Rà: B (dựng kho tìm kiếm), C (trả lời + đánh giá) · Kiểm chéo: B kiểm C, C kiểm B.
Tỉ giá ước: 1 USD ≈ 25.000 đồng. **Chưa sửa gì** — bạn đồng ý mục nào thì mới sửa mục đó.

## 1. Tóm tắt

- Rà toàn bộ code, test, notebook, guide đang có (Phase 0–7; code thử nghiệm 8.1 chỉ hỏi "còn cần không"). Chỉ đọc, **0 USD**.
- **39 phát hiện** (1 B tự rút vì sai): 2 nặng, khoảng 14 vừa, còn lại nhẹ. Kiểm chéo top 5 mỗi bên, chạy lại bằng chứng bằng script
  riêng: B kiểm C 5 / 5 đúng; C kiểm B 4 đúng, 1 đúng một phần (lệnh test trong guide không tốn tiền như B lo, chỉ báo lỗi khi thiếu key).
- **Chatbot đang chạy có 1 lỗi người dùng gặp thật**: khoảng **2–4,5 % câu hỏi** (4–8 / 176) bị báo lỗi thay vì trả lời,
  dù câu trả lời đúng và có ghi nguồn (mục 1a dưới).
- Còn lại chủ yếu là: mã lỗi API sai, một chốt an toàn khi dựng lại kho bị hỏng mà test vẫn xanh, guide cũ tả hệ thống đã gỡ,
  code thừa. **Không có lỗi làm sai câu trả lời** ngoài mục 1a.
- Bạn cần quyết: **gói nào sửa, thứ tự nào** (mục 3), và 3 câu hỏi ở mục 4.

## 2. Các gói đề xuất

Mỗi gói sửa xong thì: commit + push trước khi sửa; một session khác review; chạy test + đường thật; cập nhật báo cáo khâu.

### Gói 1 — Lỗi chatbot đang gặp (nên sửa đầu tiên)

| # | Phase | Lỗi bằng lời thường | Sửa thế nào (nhỏ nhất) | Rủi ro / cách kiểm |
|---|---|---|---|---|
| 1a | 6 | **Báo lỗi nhầm khi model ghi nguồn kiểu "[Nguồn 2]"** thay vì "[2]". Hệ thống tự đặt nhãn "[Nguồn n]" cho tài liệu đưa vào model, nhưng bộ kiểm trích dẫn chỉ hiểu "[n]" ⇒ người dùng nhận "Câu trả lời không đáp ứng yêu cầu trích dẫn". A, B đều đếm lại: mọi lỗi trích dẫn của chatbot hiện tại đều do định dạng này | Bộ kiểm nhận cả hai dạng, đổi "[Nguồn n]" về "[n]" trước khi gửi giao diện. Không đổi câu trả lời của model | Thấp. Kiểm offline trên câu trả lời đã sinh sẵn (B đã thử: không câu đúng nào bị đổi thành sai) + 1 câu hỏi thật qua API (~0,001 USD). **Hệ quả:** số "lỗi trích dẫn" của 7B / 8.1 phải tính lại theo định nghĩa mới (miễn phí, ra file mới, không ghi đè mốc đã khóa) |
| 1b | 1, 6 | **API báo sai loại lỗi**: cùng một module bị nạp hai lần dưới hai tên ⇒ khi Qdrant lỗi, API báo "lỗi nội bộ 500" thay vì "tạm không tìm được 503"; khi kho đổi mà chưa dựng lại, báo "tạm không khả dụng" thay vì "cần lập chỉ mục lại" (C đã tái tạo được). Chatbot vẫn an toàn (không trả lời bừa), chỉ báo sai lý do | Dùng **một kiểu import** cho cả API, lệnh dựng kho, test, harness; tách lỗi "model không nạp được" khỏi lỗi "cần lập chỉ mục lại"; bỏ nhánh 409 không bao giờ chạy (C-11) | Vừa — chạm ~10 file và đổi lệnh chạy ở guide. Thêm 2 test miễn phí đi qua đúng ranh giới API ↔ tìm kiếm (hiện chưa có test nào); kết quả tìm kiếm phải giống hệt từng byte trước / sau |

### Gói 2 — Chốt an toàn trước lần dựng lại kho tìm kiếm

Cần trước đợt sửa kho (139 mục rà kho C32 đang chờ) và trước khi thử Qwen3-8B.

| # | Phase | Vấn đề | Sửa | Rủi ro / cách kiểm |
|---|---|---|---|---|
| 2a | 2 | (mức vừa — chưa gây hại hôm nay, nhưng phải sửa trước khi dựng lại) **Đoạn quá dài không bị chặn**: model vector âm thầm cắt phần cuối ⇒ vector chỉ hiểu nửa đầu đoạn. Test "chặn" lại kiểm một bản sao khác và một file kết quả cũ từ 09/2026 ⇒ luôn xanh dù code sai. Hôm nay kho chưa có đoạn nào quá dài (đoạn dài nhất 255 / 256), nên **chưa gây hại** | Khi chia đoạn, đoạn nào vượt thì báo lỗi, dừng dựng kho (dùng bộ kiểm đã có). Test gọi đúng hàm thật | Thấp. 8.459 đoạn phải giống hệt (so mã băm từng đoạn). C thử: một câu 900 chữ ⇒ đoạn 906 token (giới hạn 512) mà không báo lỗi. Tokenizer huydang (256) đang sát mép ⇒ kế hoạch dựng lại phải tính |
| 2b | 2, 7A2 | Test "kho khớp bản ghi" chỉ so **số đoạn**, không so nội dung ⇒ đổi cách chia mà vẫn ra 8.459 đoạn thì không ai biết | Thêm so dấu vân tay nội dung (đã có sẵn trong bản ghi; đo hôm nay: khớp) | Thấp |
| 2c | 4 | Guide **không có quy trình dựng lại kho** (phải xóa 3 thứ theo đúng thứ tự — từng là bẫy) | Viết một mục "Dựng lại khi kho đổi" trong guide chung | Không đụng code |

### Gói 3 — Sửa công cụ đo trước khi chạy lại 8.2

| # | Phase | Vấn đề | Sửa | Rủi ro |
|---|---|---|---|---|
| 3a | 8.1 | Hàm so cặp của thí nghiệm 8.1 **đảo thắng / thua** ở chỉ số "số câu từ chối" (càng ít càng tốt). Kết luận 8.1 **không bị ảnh hưởng** (report 8.1 không dùng chỉ số này để quyết), nhưng kế hoạch E1 của 8.2 dùng đúng hàm này | Dùng một hàm so cặp chung của bộ đánh giá (đã đúng), bỏ 4–5 bản chép | Thấp, không đụng chatbot |
| 3b | 6 | Cách ghép tin nhắn gửi model viết ở hai nơi ⇒ đếm token có thể lệch khi đổi prompt | Một hàm chung | Thấp; số token phải giống hệt |
| 3c | 8.1 | **Không phải sửa code — một quyết định cũ có thể phải xem lại.** 8.1 bỏ "suy luận none" vì lỗi trích dẫn tăng 4 → 8; đếm lại sau 1a thì chỉ 0 → 2 (đúng ngưỡng cho phép), trong khi độ đầy đủ tăng có ý nghĩa | Sau khi sửa 1a: thí nghiệm lại theo luật 8.1 (xác nhận trên nhóm kiểm) — đây là **giả thuyết**, chưa kết luận | Có phí nhỏ nếu phải sinh lại; A ước trước khi chạy |

### Gói 4 — Tài liệu (guide, notebook) lệch code

| # | Phase | Vấn đề | Sửa |
|---|---|---|---|
| 4a | 0–4 | Guide Phase 0–4 và mục lục `guides/README.md` tả hệ thống Foods, 4 collection, file đã xóa **như đang chạy**; không trỏ tới code chia đoạn / dựng kho hiện tại | Ba cách để bạn chọn (mục 4, câu 3) |
| 4b | 7, 8 | Guide Phase 7 (tự ghi "canonical") chỉ tả bộ chấm Foods đã gỡ; guide 8 chưa có 7B / 8.1 / 8.2 | Thêm khối "Hiện hành" 5–8 dòng đầu mỗi guide |
| 4c | nhiều | Lệnh trong guide / notebook thiếu `uv run`; một lệnh chạy cả thư mục test (gồm test cần key OpenAI — không tốn tiền, nhưng báo đỏ khi thiếu key); notebook 06 nói có ô gọi API tốn phí nhưng không có; notebook 04 một ô làm 5 việc | Sửa từng dòng |
| 4d | 5, 6, 9 | Lệch nhỏ khác (giá trị cũ, thiếu bảng mã lỗi API) | Sửa từng dòng |

Đo bằng "số đường dẫn / lệnh chết trong guide" trước và sau (đếm bằng script).

### Gói 5 — Dọn code thừa, đơn giản hóa (không đổi hành vi)

Code không còn ai gọi, kiểm tra chồng lớp, nhánh không bao giờ chạy, test khóa code không dùng. Khoảng 17 mục nhỏ (B-02, B-04–B-07,
B-09, B-14, B-15, C-04, C-06, C-07, C-10, C-17, C-18, C-20…). Đề xuất **gộp vào cùng lần sửa** gói 1 / gói 2 ở đúng file đó, không mở
việc riêng. Kiểm: 8.459 đoạn giống hệt, kết quả tìm kiếm giống hệt từng byte, test đạt. Một số mục cần bạn chọn giữ / gỡ (mục 4, câu 2).

## 3. Thứ tự A đề xuất

1. **Review + đưa "10 đoạn + NFC" (B1, đã đạt) vào bản chính trước** — vì gói 1b đụng đúng file B1 sửa; làm B1 trước thì không phải chạy lại
   bằng chứng B1. (Đây cũng là câu hỏi 3 còn treo — A vẫn nghiêng cách này.) *Chưa đổi chatbot thật* cho tới khi bạn đọc cặp mù như spec 8.2.
2. **Gói 1** (1a trước, nhỏ và người dùng gặp thật; rồi 1b).
3. **Gói 3** (trước khi chạy lại 8.2) — 3c là thí nghiệm, hỏi bạn trước nếu có phí.
4. **Gói 2 + gói 5** cùng đợt dựng lại kho.
5. **Gói 4** bất cứ lúc nào (chỉ tài liệu); có thể để B / C làm song song gói 1.

Tiền dự kiến: gói 1–2, 4–5 gần 0 (vài câu hỏi API thật để kiểm, < 0,01 USD); gói 3c ước riêng trước khi chạy.

## 4. Câu hỏi cho bạn

1. **Đồng ý gói nào?** (A đề xuất: 1, 3a–3b, 2, 4, 5; 3c hỏi lại khi có ước tiền.)
2. **Giữ hay gỡ** hai công cụ cũ: (a) đường "Representation B" (agent thứ hai tạo đoạn tìm kiếm — chatbot không dùng, 8.2 để ngoài phạm vi)
   và (b) hai bộ chạy kiểm khói Phase 5 / 6 (một cái đã hỏng khi chạy, một cái là chỗ duy nhất kiểm thật qua API nhưng mang theo nhiều nhánh
   thừa). A nghiêng: gỡ (a) và bộ Phase 5; giữ bộ Phase 6 nhưng bỏ phần thừa.
3. **Guide Phase 0–4** (4a): (a) thêm một dòng "lịch sử — hiện hành xem …" đầu mỗi guide (nhỏ nhất); (b) viết lại phần hiện hành;
   (c) chuyển vào `guides/history/`. A nghiêng (a).
4. **Repo đang public** — hai chỗ lệch luật dữ liệu đã có từ trước: (a) một file cấu hình (5.324 ký tự), test chia đoạn (1.327) và 2 script chuyển đổi cũ (3.693) chứa
   nguyên văn ~10.300 ký tự nội dung kho (từ trang công khai, không phải bí mật); (b) 48 đường dẫn tới một dự án khác của bạn trong 6 guide (cùng loại câu hỏi 6 còn treo). Chọn:
   để nguyên / chuyển sang chỗ private từ giờ (không xóa lịch sử) / xóa cả lịch sử git (không đảo ngược được — chỉ khi bạn yêu cầu).
   A nghiêng: chuyển từ giờ, không xóa lịch sử.

## 5. Chi tiết kỹ thuật (cho agent)

- Đợt: `report_agent/2026-10-25_ra_soat_code/` — `ra_soat_code_B.md` (B-01…B-21), `ra_soat_code_C.md` (C-01…C-20), `kiem_cheo_B.md`,
  `kiem_cheo_C.md`, `TONG_HOP.md`.
- Mã phát hiện theo gói: 1a = C-09; 1b = B-01 / C-01 + C-11; 2a = B-11 (+ B-04); 2b = B-20; 2c = B-18; 3a = C-02 + C-20; 3b = C-03;
  3c = C-09 (suy ra); 4a = B-16; 4b = C-12; 4c = B-17, B-21, C-14; 4d = C-13, B-19; 5 = B-02, B-05–B-07, B-09, B-14, B-15, C-04, C-06,
  C-07, C-10, C-17, C-18; câu hỏi 2 = C-05, C-19; câu hỏi 4 = B-12, B-19; thiết kế để sau = B-03 (cấu hình sinh câu trả lời ghim cứng), B-13.
