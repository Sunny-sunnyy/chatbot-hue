# STATUS A — ghi đè 22:26 21/11/2026 (giờ `date`; KẾT PHIÊN TỐI 21/11). Vai: phiên điều phối. Terminal phiên này: `hue-rag-55` (đổi khi mở lại); phiên tối: B `hue-rag-bb` · C `hue-rag-62` · E `hue-rag-b6`

Việc đang mở, ai làm, bước kế: sổ việc `session_prompt/VIEC_DANG_MO.md` (khối A viết lại lúc kết phiên). Quyết định của chủ dự án + việc đang chờ chủ dự án: `session_prompt/HIEN_TRANG.md` mục 3 (gạch 0) và mục 4 (sáu gạch đầu là của tối 21/11). Trang này chỉ ghi phần riêng của phiên điều phối.

## Việc đầu của phiên điều phối khi mở lại
- Đọc `HIEN_TRANG.md` mục 4 sáu gạch đầu TRƯỚC khi giao việc: model cũ đang GÁC (không gọi OpenAI; test không nạp env) · một harness, chỉ đo trên model đang chạy · không hỏi chủ dự án bật / tắt, không nói chữ "cờ" với chủ dự án · LUẬT ĐO GỌN (sổ việc khối A gạch thứ hai) — chủ dự án đã nhắc lần thứ mười về đo / test quá nhiều; đếm tiến độ bằng số tính năng tới được người dùng, không bằng số ô đo.
- Giao theo thứ tự "NHÁNH CHỜ" của sổ việc khối A: mở bản sửa "mục web chỉ khi cả câu bị từ chối" (B) ⇒ một phiên đọc nhánh công cụ "gần một điểm có gì" rồi mở (C viết) ⇒ sửa hai chỗ giao diện để mở "thêm điểm không tự thế chỗ" + chữ sai nghĩa của tin "đổi chỗ ngày + hỏi" (C) ⇒ tìm kho theo từng vế (B). VIỆC LỚN của ngày: mục [7] đề xuất sửa kho bằng lệnh chạy tay + cập nhật riêng bài đã sửa — bắt đầu bằng một trang thiết kế gọn cho phần cập nhật riêng (chủ dự án: "mai rồi triển khai").
- Gửi chủ dự án hướng dẫn từng bước cấp quyền chữ chạy dần (tra tài liệu AWS trước — tên quyền mới nêu theo trí nhớ); nhắc MỘT lần việc đọc bài nháp "Huế → Hội An".
- Viết lại TOÀN TRANG `HIEN_TRANG.md` (mục 4 đã dài thêm sáu gạch trong một tối) và làm vòng cải tiến cách làm (skill `improve-workflow`): ứng viên số một là gọt luật ba lượt trong skill `run-experiment` cho khớp LUẬT ĐO GỌN; ý của các phiên ở `SO_CAI_TIEN_CACH_LAM.md` (khối "Phiên tối 21/11").
- Chưa làm lúc kết phiên: `report_agent/2026-11-21/TONG_HOP.md` của ngày (dòng theo giờ đang nằm ở `CURRENT_HANDOFF.md`); chép các ý mới của tối 21/11 vào `Y_CHUA_THU.md` cho đủ (lọc điểm tham quan theo loại cho công cụ "gần một điểm"; bật sổ vết ở một lượt đo để thấy câu tìm model viết).

## Đang khai báo sửa
- không.

## Đang chạy / file tạm lúc ghi
- Agent con của phiên điều phối: 0 đang chạy. Tiến trình nền của phiên điều phối: 0 (đồng hồ hẹn đã hết). File riêng tư phiên điều phối tạo tối 21/11 (GIỮ): `data/thu_bedrock_2026-11-21/soat_tich_hop/`, `…/do/moc_12vai/doc_mu/` (bản xuất giấu tên model, luật chấm, bảng gom), `…/b_buoc_4/kem_hoi/bo_mu*`, `…/b_buoc_4/go_tat/bo_mu*`, `…/c_sua_3/bo_mu_tra_loi*`, `…/c_muc_5/bo_mu_gan_x*`, `data/su_kien_theo_ngay_2026-11-20/luot_that/kiem_ngay_duong_A.py` + `bo_do_khoang_ngay_A_2111*`, `data/phase_12_agent_sua_kho_2026-11-21/`, `data/bo_sung_kho_2026-11-21/`. `/tmp/hr_a_khoi_A.md` xoá được.

## Đã học / bẫy của phiên tối 21/11
- Áp nguyên bộ "ba lượt lặp + tiêu chí ghi trước + bộ mù + người đọc thứ hai" cho gần như mọi thay đổi ⇒ chủ dự án nhắc lần thứ mười; tới 22:00 mới có tính năng tới người dùng. Dấu hiệu sớm lẽ ra phải thấy: hàng làn đo dài hơn hàng việc xây.
- Hỏi chủ dự án ba lần một câu bật / tắt bằng chữ nội bộ ("cờ") · nói "gác luna" không rõ là gác ĐO chứ không tách harness · báo chủ dự án một điều mới suy từ code ("thẻ lịch có thể gợi ý quán đã đóng") rồi phải đính chính sau phép đếm.
- Bản xuất cho người đọc mù do chính mình viết in nhầm dòng đánh dấu thành lượt "None" — người đọc bắt; script kiểm ngày của mình có ba chỗ sót — E bắt. Việc phiên điều phối tự làm vẫn cần người khác đọc.
- Máy ngủ 80 phút khi chủ dự án đi vắng: không biết được từ bên trong; lần sau chủ dự án nói đi vắng thì nhắc MỘT dòng tắt chế độ ngủ.
- Làm đúng, giữ: người soạn bộ câu thử khác người viết code (bắt câu đồng ý cụt, "bn" = bạn) · đếm 0 đồng trước khi xây (ba hướng không xây, hai hướng đổi hẳn nhờ số đếm) · đọc diff thay người đọc đang bận để không chặn việc · một lượt thật trước khi mở (bắt một bản sửa làm hỏng mọi lượt).
