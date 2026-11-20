# Tổng hợp ngày 20/11/2026 (thứ Sáu)

Người giữ: phiên điều phối. Report của từng phiên nằm cùng thư mục (tiền tố `b_` / `c_` / `e_`). Lời User nguyên văn: `data/loi_user/2026-11-20.md` (riêng tư).

## PHIÊN SAU ĐỌC TRƯỚC (GHI ĐÈ lúc kết phiên; ≤ 20 dòng: thoả thuận máy liên dự án · thứ tự việc mở đầu phiên, trỏ mục lục việc · câu đang chờ User · thứ đang chạy / phải bật lại · bẫy của ngày)

Viết 13:03 20/11/2026 (giờ `date`), KẾT PHIÊN NHẸ giữa ngày — các mục 1–4 dưới đây CHƯA viết, làm ở lần kết phiên cuối ngày; diễn biến theo giờ: các dòng "Ghi trong phiên" của `session_prompt/CURRENT_HANDOFF.md`.
- **Thứ tự mở đầu:** `session_prompt/HIEN_TRANG.md` ⇒ `session_prompt/VIEC_DANG_MO.md` ⇒ `session_prompt/sessions/STATUS_A.md`.
- **Trạng thái:** phần của nhóm trước buổi chủ dự án test ĐÃ XONG. Code đứng yên ở `d8651d4`: cả bộ test 55 file, 1.554 đạt, 0 hỏng; danh sách test trình duyệt 13 dòng đạt; sao lưu ổ khác xong.
- **Trong ngày:** soát mù khác hãng ba lượt (hai lượt đọc cả phần mới + một lượt riêng cho các bản sửa; ba model của hai hãng, chủ dự án lái phần lớn) ⇒ 12 bản sửa nhỏ đã gộp, mỗi bản có người thứ hai đọc; các điểm còn lại ghi giới hạn (`guides/RUNBOOK_BAN_GIAO.md` mục 10). Bài cho chủ dự án: `bai_hoc/VIEC_MOI_XONG.md` mục 16, 17.
- **Việc đầu tiên phiên sau:** hỏi chủ dự án ba câu đang gác (một bản sửa đã duyệt nhưng chưa ai viết được · bộ bài đánh giá model đi tiếp cách nào · một đề xuất cải tiến cách làm) rồi mời chủ dự án test một lần ở máy local.
- **Bẫy của ngày:** `STATUS_A.md` mục 7 (lượt viết bị hệ thống dừng ở hai cụm việc; ổ sao lưu không phân biệt hoa thường; lỡ chạy cả bộ test hai bản song song; việc sửa nhỏ làm quá cỡ buổi sáng).
- **Tiền API tới lúc viết ≈ 0,11 USD** (số từng phiên báo, chưa cộng lại từ log).

## 1. Việc trong ngày và kết quả (viết 13:08 20/11/2026, giờ `date`; tới lúc kết phiên giữa ngày)

| Việc | Kết quả | Báo cáo trong thư mục này | Phần riêng tư |
|---|---|---|---|
| Mở máy: Docker không còn container nào | Dựng lại container Qdrant, chỉ mục ở thư mục gắn còn nguyên: 9.436 điểm | (sổ việc) | — |
| Sửa nhỏ cờ nhớ tên: câu hỏi tiếp chỉ xin liệt kê lại thì lượt đó không nhận dòng ghi chú | Đã gộp. Hai bộ dò của người không viết code: bắt nhầm 0 / 32 + 0 / 3; nhận đúng 9 / 20 + 5 / 5. Lượt thật: tác dụng phụ của dòng ghi chú hết; lỗi có sẵn "danh sách thiếu một hai mục" còn 5 / 6 lần ở cả hai bên. Làm QUÁ CỠ so với lợi (vòng tự soi) | `b_nho_ten_liet_ke_lai_implementation.md` | `data/kich_ban_pho_thong_2026-11-19/viec_2_sua_nho/` |
| Soát mù khác hãng, đợt một (một model, hai lượt) | 13 điểm khác nhau: 11 tái hiện, 1 xác nhận bằng đọc code, 1 trùng giới hạn; 0 điểm sai. Sửa: hiện chữ dần phát nốt phần đuôi · lượt sửa lịch không đổi gì không ghi đè bản lưu (kèm ca ngược) · dời hai điểm cùng đích không còn báo "đã dời" · câu liệt kê có câu thứ hai. Ghi giới hạn tám điểm | `b_sua_sau_soat.md`, `c_sua_sau_soat.md` | `data/review_khac_hang/2026-11-19_diem_dung_buoc_5/` (`DOI_CHIEU.md`, `tai_hien/`) |
| Soát mù khác hãng, đợt hai (hai model của hãng thứ hai, chủ dự án lái) | 16 phát hiện = 10 trùng + 6 mới, cả 6 có thật (3 nói quá mức). Sửa: dòng ý thiếu không còn bị coi là đã nêu cảnh báo · "dông" như "giông" ở câu nói thật · ẩn nút in trong vùng trò chuyện. Ghi giới hạn ba điểm | `b_sua_sau_soat.md` | như trên |
| Danh sách test bằng trình duyệt thật trên bản 29 cờ | 13 dòng đạt, 1 khác mong đợi (đã sửa cột mong đợi), 2 không chạy. Lộ MỘT lỗi mới của cờ nhớ tên: hỏi A ⇒ hỏi B ⇒ gõ lại nguyên văn A thì trả lời B (bật 0 / 3, tắt 3 / 3) ⇒ sửa hẹp, đo lại 3 / 3; chuỗi "câu trỏ lại gõ lại" 3 / 3 | `b_sua_sau_soat.md` | `data/test_cuoi/CHAY_E_2026-11-20.md`, `data/test_cuoi/chay_2026-11-20/` |
| Lượt soát RIÊNG cho các bản sửa (ba model, chủ dự án lái) | 10 + 11 + 12 phát hiện, phần lớn trùng. Bản sửa "gõ lại câu cũ" đã gây một lỗi mới (câu lược tên nơi gõ lại mất dòng tên nơi) ⇒ chủ dự án chọn "sửa hai dòng rồi đóng": thu hẹp điều kiện gỡ · khối đầu toàn khoảng trắng thì phát cả câu. Rồi duyệt đề xuất của nhóm sửa thêm hai điểm: thẻ lịch và các bản xuất giữ câu 112 sau lượt sửa làm được (ĐÃ gộp) · không báo "đã dời" khi lịch không đổi (KHÔNG làm được — lượt viết bị hệ thống dừng; ghi giới hạn). Còn lại ghi giới hạn ở runbook 10.1, 10.3b | `e_the_lich_giu_112.md` | `DOI_CHIEU.md` mục "ĐỢT SỬA" |
| Cả bộ test một lượt trên bản cuối | main `d8651d4`: 55 file, 1.554 đạt, 0 hỏng (lỡ chạy hai bản song song; mã thoát cả 109 tiến trình đều 0) ⇒ code đứng yên | `b_ca_bo_test.md` | `data/test_rong_2026-11-20/` |
| Sao lưu sang ổ khác | Xong, 3,6 GB; kho 496 ↔ 496 file; một file rơi do ổ đích không phân biệt hoa thường — đã chép bù, mã băm khớp | (sổ việc) | — |
| Sổ ghi việc `bao_cao_he_thong/` | Cập nhật cho tối 18/11, 19/11 và các sửa 20/11 (ba trang) | — | — |
| Bộ bài đánh giá coding agent (chủ dự án giao) | Mới có khung mười bài + khuôn mở đầu + hai script; CHƯA có đề: lượt viết của các phiên thực thi bị hệ thống dừng ⇒ dừng, chờ chủ dự án chọn | — | `data/danh_gia_model_2026-11-20/` |

Ai kiểm việc nào: mỗi bản sửa có một phiên khác người viết đọc diff và chạy lại test (biên bản `REVIEW_E*.md` trong hai thư mục riêng tư ở cột cuối; review của C ghi trong các report `b_…`, `e_…`).

## 2. Quyết định của chủ dự án trong ngày (đủ ở `session_prompt/HIEN_TRANG.md` mục 4)

- Chạy soát khác hãng bằng cả hai hãng (ba model), kể cả một lượt riêng cho các bản sửa; cách làm: chủ dự án mở AI trong thư mục dự án và đưa MỘT file đề bài tự đủ.
- Sau lượt soát các bản sửa: "sửa hai dòng rồi đóng", mọi điểm khác ghi giới hạn, không soát vòng nữa; sau đó duyệt đề xuất của nhóm sửa thêm đúng hai điểm.
- Đề xuất trình chủ dự án phải là ý của đa số hoặc cả nhóm thống nhất (ghi rõ từng phiên; phiên không trả lời được = không có ý kiến).
- Muốn một BỘ bài (10–20 bài) đánh giá model thay coding agent hiện tại: bài liên quan trực tiếp dự án, model tự khai tên, tự đặt tên file kết quả, ghi giờ + cách làm + cách nghĩ; bài giảng cho chủ dự án là chuyện nhỏ.
- Không cho AI khác điền hộ file "câu chủ dự án tự gõ" (điều phối khuyên, chủ dự án không phản đối).
- Các nhiệm vụ và câu hỏi còn lại để PHIÊN SAU làm; yêu cầu mọi file `.md` đủ ngữ cảnh cho phiên sau.
- Điều phối tự quyết trong phạm vi (đã báo): giữ cờ nhớ tên BẬT khi thấy lỗi "gõ lại câu cũ" · ghi giới hạn thay vì sửa lõi cho các ca hiện chữ dần chưa từng thấy thật · ẩn nút in ở cả khung nổi lẫn trang Trợ lý.

## 3. Đang mở khi viết file này (nguồn duy nhất: `session_prompt/VIEC_DANG_MO.md`)

Buổi chủ dự án test một lần ở máy local · ba câu chờ chủ dự án · bộ bài đánh giá model (dừng ở khung) · vài việc nhỏ chưa đo · nợ tài liệu cuối ngày (nhật ký, bảng quyết định theo ngày, vòng cải tiến, vòng tự soi 2).

## 4. Tiền API trong ngày (số từng phiên báo, chưa cộng lại từ log)

Phiên E ≈ 0,091 USD (test trình duyệt 0,0371 · đo lỗi gõ lại 0,0212 + 0,0154 · các lượt thử nhỏ) · phiên C ≈ 0,017 (phép "kể hết" 0,0142 + ba lần chạy một file test có khoá) · phiên B ≈ 0,005 cận trên (cả bộ test) · điều phối 0 ⇒ khoảng **0,11 USD**. Ba model khác hãng chạy bằng gói của chủ dự án, không tính tiền API.
