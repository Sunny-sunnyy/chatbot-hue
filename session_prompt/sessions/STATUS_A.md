# STATUS A — ghi đè 17:47 21/11/2026 (giờ `date`; kết phiên 21/11). Vai: phiên điều phối. Terminal phiên này: `hue-rag-bf` (đổi khi mở lại)

Việc đang mở, ai làm, bước kế: sổ việc `session_prompt/VIEC_DANG_MO.md` (khối đầu = ba ngày thử đuổi một con số). Quyết định của chủ dự án + câu đang chờ: `session_prompt/HIEN_TRANG.md` mục 3, 4. Trang này chỉ ghi phần riêng của phiên điều phối.

## Việc đầu của phiên điều phối khi mở lại
- (ghi 18:12 21/11/2026) Phiên sau chủ dự án ĐI VẮNG (tự nói lúc kết phiên 21/11): câu thuộc quyền chủ dự án thì gác vào `HIEN_TRANG.md` mục 3, không mở hộp hỏi, không chờ; mở bốn phiên cho bước 0–3, tới bước sửa rút còn hai. Việc gác lúc kết phiên (nhánh bỏ dòng ghi nguồn bản đồ, đề xuất hook chờ lời chủ dự án…): sổ việc khối A, gạch "Việc GÁC".
- Nhắn tên terminal; giao việc theo khối đầu của sổ việc — tin giao việc mở đầu bằng "quyết định nào đang chờ kết quả này", không giao danh sách bước. KHÔNG giao lại hàng đo cờ và các mục Phase 9–12: chúng đứng chờ.
- Mặc định: giao NGAY theo sổ việc. Chỉ khi prompt mở phiên hoặc lời chủ dự án nêu một mục đích KHÁC sổ việc (như buổi bàn chiều 21/11) thì hỏi MỘT câu trước khi giao.
- Khởi động bước 2 của khối A ngay lúc mở: một agent con ngữ cảnh mới soát tích hợp chỉ đọc (skill `soat-tich-hop`), vai đo đọc kết quả. Báo chủ dự án con số ước của bước 0 (8–10 USD Bedrock, khoảng 100 phút máy) trước khi chạy.
- Hỏi chủ dự án khi việc cần tới: mở hai phiên hay bốn cho ba ngày thử; các câu còn chờ ở `HIEN_TRANG.md` mục 3 (mỗi lần một câu).
- Ghi ba con số cách làm của ngày vào `session_prompt/SO_CAI_TIEN_CACH_LAM.md`; chép ý mới các phiên nêu vào `session_prompt/Y_CHUA_THU.md`.

- (ghi 18:14 21/11/2026) Chủ dự án muốn TIẾP TỤC buổi trò chuyện bàn hướng khi về ("khi nào tôi đi về có thể tiếp tục trò chuyện trao đổi brainstorming"): chuẩn bị sẵn để bàn — con số trước ↔ sau của việc chính, đề xuất hook đang chờ, danh sách `Y_CHUA_THU.md` (các ý cải tiến sản phẩm 13–17), số phiên.

## Đang khai báo sửa
- không (các nhánh của lượt soát 21/11: xem `git branch -r --no-merged origin/main`).

## Đang chạy / file tạm lúc ghi
- 0 server, 0 tiến trình đo, Qdrant bật. Worktree của A: `/tmp/hr_a_trang_thai` (nhánh viết lại trang trạng thái — gỡ sau khi gộp). File tạm: `/tmp/hr_a_tra_*.md` (xoá được).

## Đã học / bẫy của phiên 21/11
- Giao lại việc theo sổ khi chủ dự án muốn cả nhóm bàn chuyện khác · đưa chủ dự án một con số trước khi có người thứ hai kiểm · chủ dự án hỏi về KẾT QUẢ mà chuyển xuống nhóm câu hỏi về ĐẦU VÀO · bàn nhiều vòng mà chưa sửa file nào · báo số byte trước khi áp bản đọc của người khác · nối bảy dòng vào trang hiện trạng mà không viết lại ⇒ bốn chỗ cùng xưng "việc đầu" · viết luật trái một quyết định còn hiệu lực (người đọc bắt) · sửa file luật riêng của chủ dự án rộng quá phạm vi một dự án (người đọc bắt) · chỉ giao agent con soát khi chủ dự án muốn các phiên cùng soát.
- Làm đúng, giữ: mỗi phiên một góc khác nhau (luật / lịch sử / nguồn ngoài) cho ra phát hiện không trùng · agent ngữ cảnh mới đọc như phiên vừa mở bắt được chỗ hai nghĩa mà người viết không thấy, phiên có lịch sử bắt được chỗ trái quyết định cũ — cần cả hai · tự mở nguồn chính trước khi đưa chủ dự án · đề nghị trước, cả nhóm chốt, rồi mới sửa.
