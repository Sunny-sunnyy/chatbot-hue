# STATUS A — ghi đè 16:25 22/11/2026 (giờ `date`; KẾT PHIÊN CHIỀU 22/11 — chủ dự án mở NGAY năm phiên mới sau phiên này; 23/11 làm cả ngày và chủ dự án TỰ TEST trong lúc nhóm làm). Vai: phiên điều phối. Terminal phiên vừa đóng: `hue-rag-fc`; B `hue-rag-73` · C `hue-rag-72` · phiên đo E `hue-rag-ab` · D `hue-rag-85` — phiên mới sẽ có tên khác, dò lại bằng danh sách phiên

Việc đang mở, ai làm, bước kế: sổ việc `session_prompt/VIEC_DANG_MO.md` khối A — đọc gạch "VIỆC CHO NĂM PHIÊN MỞ LẠI" và các dòng X10, X11, K10. Quyết định của chủ dự án: `session_prompt/HIEN_TRANG.md` mục 4 (bốn gạch đầu là của chiều 22/11: lịch 23/11 + cách nhóm tránh server của chủ dự án trong buổi test · bài Hội An · bộ câu kín chạy một lần SAU buổi tự test). Thứ chủ dự án đọc: `bai_hoc/VIEC_MOI_XONG.md` mục 44. Trang này chỉ ghi phần riêng của phiên điều phối.

## Hệ thống lúc đóng phiên
Main có 47 tính năng mở (K10 `nho_dap_cuoc_co_lich` mở 16:13; bản rào lệnh bỏ / thay của lịch; giữ chữ tới khi kiểm xong) · kho 267 bài / 9.479 điểm (bài "Đi từ Huế tới Hội An") · đã nhìn trên trình duyệt 16:21: năm phần, 16 / 16 lượt, 0 lỗi (`data/test_cuoi/chay_2026-11-22_e_nhin_gom/KET_QUA.md`) · server TẮT, Qdrant bật. Cả bộ test lần đủ gần nhất: 75 file / 2.140 ca trên nhánh giữ chữ TRƯỚC khi mở K10 và bản rào — sau đó chỉ chạy các file chạm (8 file đạt) ⇒ lượt cổng kế phải phủ.

## Việc của phiên điều phối mở lại, theo thứ tự
1. Gộp các nhánh sổ kết phiên còn lại (phiên đo: sửa `data/test_cuoi/DANH_SACH.md` là file riêng tư + `STATUS_E.md` + nếu có chỗ sửa mục 44; D: `STATUS_D.md`).
2. Giao theo sổ: B dựng X10 "thẻ nơi" (tiêu chí ghi trước: `data/thu_bedrock_2026-11-21/b_dem_chua_co_2211/TIEU_CHI_X10.md`), C phản biện / đọc code + soạn X11 (Hải Vân Quan, sửa đúng một dòng; cập nhật chỉ mục CHỈ khi server tắt, không trong buổi chủ dự án test), phiên đo soát danh sách test trước 9h 23/11 rồi chấm X10, D đợt sửa gom.
3. MỘT lượt cả bộ test trên main hiện tại TRƯỚC 9h 23/11 (cổng trước buổi chủ dự án tự test) — phiên đo chạy.
4. Hàng câu chờ chủ dự án, MỖI LẦN MỘT CÂU có ô tick, không nhắc lại câu đã hỏi: (a) bộ kiểm lúc lưu code thôi chặn chép ≥ 40 ký tự từ kho / bộ câu mẫu vào tài liệu (giữ chặn câu kín) — nhóm khuyến nghị "được"; (b) bài nháp đỗ ô tô (mỏng) + câu quy định chụp ảnh: ghi / bỏ; (c) lệnh sửa giá với hai bài gắn luật điều kiện — khuyến nghị để sửa tay; (d) "bỏ hoạt động buổi tối": để trống hay tự lấp. KHÔNG nêu: AWS, tiền OpenAI, chuyện trình bày.
5. Trong buổi chủ dự án test 23/11: chép nguyên văn lỗi anh báo vào `data/loi_user/2026-11-23.md`, đếm / tái hiện rồi mới giao; gom bản sửa thành đợt, nói rõ "chạy lại lệnh bật để có bản sửa X, Y".
6. Nợ của phiên điều phối: viết gọn `HIEN_TRANG.md` mục 1–4 (đang rất dài) · `report_agent/2026-11-22/TONG_HOP.md` phần chiều (dời các dòng của `CURRENT_HANDOFF.md`) · vòng cải tiến cách làm (đầu vào: dòng "CHỐT VÒNG GÓP Ý CHÉO" + các bẫy dưới).

## Đang chạy / file tạm
Agent con: 0. Tiến trình nền: 0. Cây tạm: 0. File riêng tư tạo trong phiên: `data/thu_bedrock_2026-11-21/do_ba_ben_2026-11-22/TIEU_CHI.md`, `…/k10_cuoc_co_lich_2026-11-22/TIEU_CHI.md`, `…/b_dem_chua_co_2211/TIEU_CHI_X10.md`, các dòng thêm ở `data/loi_user/2026-11-22.md`.

## Bẫy của phiên 22/11 (đầu vào cho vòng cải tiến)
- Giao sửa hai điểm hiếm (0 / 873 tin thật) trước khi đếm — B bắt. Từ đó: đếm trước, hiếm thì một dòng giới hạn.
- Bốn lần chuyển tiếp một câu / con số chưa mở file gốc (ba lần buổi trưa + chiều: nói với chủ dự án "vé lẻ Cung An Định nằm ngoài phạm vi bản chữa" trước khi phép đếm 3 của B cho thấy nó vào được — đã đính chính ngay tin sau). Trước khi chuyển một con số: hỏi "file đo ở đâu".
- Ước tiền một lượt thật thấp ba lần (K10: ước 0,3, thật 0,84) — lượt "viết lại" tự tìm kho 3–4 lần. Từ giờ người CHẠY tự ước trước khi chạy và ghi vào file kết quả (B đã ghi vào sổ của mình).
- Tiêu chí ghi trước có lỗ ba lần, đều do NGƯỜI ĐỌC chỉ ra trước khi có số (so số đếm khi một bên toàn màn hình lỗi · chấm theo kho ↔ theo ngữ cảnh · "danh sách đã bỏ quán đầu" không đòi các quán còn lại phải đủ). Giữ: gửi tiêu chí cho người chấm TRƯỚC khi chạy.
- Thứ tự "gộp bài kho vào cây chính TRƯỚC, cập nhật chỉ mục SAU" — C chặn lệnh giao sai thứ tự của phiên điều phối; khoảng hở giữa hai bước server bật lên sẽ trả 409.
- Làm đúng, giữ: một lần bật trình duyệt GOM cho năm thay đổi thay vì năm lần · người viết ≠ người chạy ≠ người chấm ở bản rào và K10 · phép đếm 0 đồng đổi thiết kế X10 hai lần trước khi viết dòng code nào · hỏi chủ dự án mỗi lần một câu có ô tick (hai câu, hai trả lời trong vài phút).
