# STATUS A — ghi đè 11:57 22/11/2026 (giờ `date`; MỞ PHIÊN TRƯA 22/11). Vai: phiên điều phối. Terminal phiên này: `hue-rag-fc` (đổi khi mở lại); B `hue-rag-73` · C `hue-rag-72` · phiên đo E `hue-rag-ab` · D `hue-rag-85` (D do chủ dự án lái)

Việc đang mở, ai làm, bước kế: sổ việc `session_prompt/VIEC_DANG_MO.md` khối A (gạch đầu = đợt soát khác hãng đang chạy, có bảng từng điểm). Quyết định của chủ dự án + việc đang chờ chủ dự án: `session_prompt/HIEN_TRANG.md` mục 3 – 4. Diễn biến buổi sáng: `report_agent/2026-11-22/TONG_HOP.md`. Trang này chỉ ghi phần riêng của phiên điều phối.

## Việc của phiên điều phối trong phiên này
- Nhận tin từng điểm của B, C, phiên đo (khuôn: thật / không thật · người dùng gặp khi nào · đã sửa gì hoặc dòng giới hạn · lệnh kiểm + đầu ra) ⇒ quyết sửa / ghi giới hạn, giao người đọc bản sửa (khác người viết), gộp, cập nhật bảng ở sổ việc khối A.
- File của Gemini về (`data/review_khac_hang/2026-11-22_moc_sang/KET_QUA_*.md`) ⇒ ghép bảng đối chiếu (skill `soat-tich-hop`), điểm mới giao theo người viết code. Không soát vòng hai.
- Gộp `p12-c-doc-kiem-cap-nhat` khi C gửi dòng `ĐÃ PUSH` (C đã đọc nhánh phép kiểm của phiên đo; đọc diff dòng runbook rồi gộp).
- Trước lượt bật server của phiên đo (có tắt / bật Qdrant): hỏi B, C "máy trả"; báo phiên điều phối dự án khác đang mở một dòng.
- Cổng đóng cuối đợt (một lần, sau khi các bản sửa đã gộp): các file test chạm + kịch bản demo một lần; cân theo số bản sửa thật có.
- Vòng cải tiến cách làm (sổ việc khối A việc 3): ba ứng viên ở `SO_CAI_TIEN_CACH_LAM.md` khối "PHIÊN SÁNG 22/11/2026" + năm ý phê bình cách test của GPT-6 + gọt luật ba lượt của skill `run-experiment`; một phiên khác đọc rồi mới sửa file luật.
- Viết lại mục 4 của `HIEN_TRANG.md` khi có dịp (đang dài; mục 2 – 3 đã sửa các dòng cũ lúc mở phiên trưa).
- Chưa rõ, cần xem trước khi nói với chủ dự án: bài nháp mỏng "Đỗ ô tô ở khu trung tâm Huế" (`data/bo_sung_kho_2026-11-21/nhap/`) không thấy dấu vết đã trình chủ dự án; bài "chụp ảnh ở chùa / lăng" không soạn được vì không có nguồn (`…/BAO_CAO.md`).

## Đang khai báo sửa
- `session_prompt/VIEC_DANG_MO.md`, `HIEN_TRANG.md`, `CURRENT_HANDOFF.md`, trang này (ghi thẳng main).

## Đang chạy / file tạm lúc ghi
- Agent con: 0. Tiến trình nền: 0. Cây tạm của phiên điều phối: 0. Còn trong `/tmp` từ buổi sáng (xoá được, không phải worktree): `/tmp/hr_a_kiem_thuyen/`, `/tmp/hr_a_mo_gan_diem.patch`, `/tmp/hr_tracuu*`.

## Đã học / bẫy (giữ từ phiên sáng 22/11 — vẫn đúng)
- Bốn lần nói một điều SUY TỪ CODE như đã thấy; trước khi nói với chủ dự án về hành vi khi hỏng: có lượt chạy thật chưa; chưa thì gắn nhãn "đọc code, chưa chạy".
- Đọc một phép chung của chủ dự án RỘNG hơn ý; lấy nghĩa hẹp nhất hợp với việc đang bàn, nói lại một dòng trước khi làm rộng hơn.
- Không tự đặt lệnh về tiền Bedrock, không báo số USD khi không được hỏi; không nhắc chuyện AWS.
- Quyết mở một tính năng chạm lịch sử trên bộ thử chỉ có một kiểu lượt nối tiếp ⇒ lọt lỗi; bộ thử phải có: hỏi tiếp · nhờ sửa lại thứ vừa viết · gõ lại câu cũ.
- Bẫy mới lúc mở phiên trưa: tài liệu ghi "mở lại máy ⇒ /tmp mất" nhưng lần này chỉ các phiên được mở lại, máy không khởi động lại — kiểm `git worktree list` + `ls /tmp/hr_*` thay vì tin câu đó · hai phiên cùng nhận một việc đọc (B và C cùng nhận đọc nhánh phép kiểm) vì tin giao việc của phiên điều phối tới sau khi phiên đã tự bắt đầu phần 0 đồng — giao việc đọc thì hỏi "ai đã bắt đầu" trước.
