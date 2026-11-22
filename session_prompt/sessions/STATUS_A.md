# STATUS A — ghi đè 11:20 22/11/2026 (giờ `date`; KẾT PHIÊN SÁNG 22/11). Vai: phiên điều phối. Terminal phiên này: `hue-rag-7a` (đổi khi mở lại); B `hue-rag-b1` · C `hue-rag-4f` · phiên đo E `hue-rag-67` · D `hue-rag-85` (D do chủ dự án lái, có thể còn mở)

Việc đang mở, ai làm, bước kế: sổ việc `session_prompt/VIEC_DANG_MO.md` khối A (viết lại lúc kết phiên). Quyết định của chủ dự án + việc đang chờ chủ dự án: `session_prompt/HIEN_TRANG.md` mục 3 – 4. Diễn biến của buổi: `report_agent/2026-11-22/TONG_HOP.md`. Trang này chỉ ghi phần riêng của phiên điều phối.

## Việc đầu của phiên điều phối khi mở lại
- (ghi 11:40 22/11/2026) Chủ dự án tắt và mở lại BỐN phiên A, B, C, E; phiên D GIỮ NGUYÊN ở terminal `hue-rag-85`, đang viết giáo trình cho chủ dự án ⇒ ngay khi mở: gửi tên terminal mới của phiên điều phối cho D (D đang chờ tên mới để gửi yêu cầu gộp nhánh `origin/p9-d-giao-trinh`; main đã có tới commit `80f89d8` của D). Gói soát khác hãng đã sẵn (`data/review_khac_hang/2026-11-22_moc_sang/DE_BAI.md`) — kiểm thư mục đó có file `KET_QUA_*.md` chưa.
- Đọc `HIEN_TRANG.md` mục 4 ba gạch đầu (22/11): giá trong kho chỉ cần tương đối — chỉ sửa chỗ kho tự xung đột hoặc thiếu, không đối chiếu giá với web · được tra cứu rồi sửa chỗ kho sai (đã thu hẹp bởi gạch trên) · không nhắc chuyện AWS / tiền Bedrock.
- Giao theo thứ tự "VIỆC ĐẦU của phiên sau" ở sổ việc khối A: gói soát khác hãng (chờ chủ dự án nói "gửi"; phần "cách nhóm đang test" đã có ở `data/review_khac_hang/2026-11-22_moc_sang/CACH_NHOM_DANG_TEST.md`) ⇒ cập nhật danh sách cho buổi chủ dự án test ⇒ vòng cải tiến cách làm (ba ứng viên ở `SO_CAI_TIEN_CACH_LAM.md`, khối "PHIÊN SÁNG 22/11/2026") ⇒ đọc + gộp nhánh phép kiểm của phiên đo ⇒ ba phép thử "một khối hỏng thì sao" cho giáo trình.
- Chủ dự án đang chờ / đang đọc: bài mẫu giáo trình `bai_hoc/giao_trinh/06_KIEN_TRUC.md` (trả lời cho phiên D) · câu A / B về bộ kiểm chặn trích từ kho (đã hỏi một lần, chưa trả lời — không nhắc lại quá một lần) · bài nháp "Huế → Hội An" (đã nhắc một lần).
- Viết lại TOÀN TRANG `HIEN_TRANG.md` mục 4 khi có dịp (mục này đã dài thêm ba gạch 22/11; mục 1 – 3 đã cập nhật trong buổi).

## Đang khai báo sửa
- không.

## Đang chạy / file tạm lúc ghi
- Agent con của phiên điều phối: 0 đang chạy (ba agent con của buổi đã xong: soạn lại nháp leo bậc · tra bốn chỗ kho · tra giá thuyền). Tiến trình nền: 0. Cây tạm của phiên điều phối: đã gỡ hết. Collection thử của phiên điều phối (`hue_thu_truoc_2211`, `hue_thu_truoc_leo_bac`): đã xoá; Qdrant chỉ còn collection đang chạy (9.458 điểm). Ba bản chụp Qdrant tự động của ba lần chạy thật còn trong container (runbook 5b). File riêng tư phiên điều phối tạo 22/11 (GIỮ): `data/bo_sung_kho_2026-11-22/`, `data/sua_kho_2026-11-22/`, `data/loi_user/2026-11-22.md`, `/tmp/hr_a_kiem_thuyen/` (trang tải về để kiểm giá — xoá được).

## Đã học / bẫy của phiên sáng 22/11
- Bốn lần nói một điều SUY TỪ CODE như đã thấy ("server từ chối khởi động" · "vector từ khoá phải ghi lại vì cách tìm cần" · "khi tắt thì tin đó làm được" · "chữ hiện rồi bị gỡ") — ba lần phiên khác / agent kiểm của phiên D bắt. Trước khi nói với chủ dự án về hành vi khi hỏng: có lượt chạy thật chưa; chưa thì gắn nhãn "đọc code, chưa chạy".
- Đọc một phép chung của chủ dự án ("chỗ nào không chính xác thì tra cứu rồi sửa") RỘNG thành đợt đối chiếu giá với web; chủ dự án phải kéo lại. Lấy nghĩa hẹp nhất hợp với việc đang bàn, nói lại một dòng trước khi làm rộng hơn (đã ghi trí nhớ).
- Tự đặt lệnh "giữ lượt có phí nhỏ" và báo số USD khi thấy ảnh tín dụng AWS — trái lời chủ dự án 21/11; tài khoản đó không phải tài khoản cấp khoá Bedrock.
- Quyết mở "nhớ câu trả lời liền trước" trên bốn chuỗi đều là "hỏi tiếp"; kiểu tin "sửa lại thứ vừa viết" lọt ⇒ màn hình lỗi 3 / 7, phiên đo bắt ở cổng đóng.
- Làm đúng, giữ: đổi dòng settings thật rồi chạy test TRƯỚC khi gộp bản mở · chờ ba phiên "máy trả" trước khi đổi chỉ mục thật · đọc diff thay người đọc đang bận để không chặn việc · tự mở lại trang nguồn trước khi sửa kho · cổng đóng (cả bộ test + demo + server thật) trước khi nói "ổn".
