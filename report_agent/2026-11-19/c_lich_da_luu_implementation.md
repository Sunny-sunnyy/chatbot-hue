# Lịch đã lưu vào lượt hỏi thường — báo cáo thực hiện (phiên C)

Viết: 15:52 19/11/2026 (giờ `date`). Việc đứng đầu thứ tự sửa mà chủ dự án chọn sau lượt đo 80 kịch bản phổ thông (19/11). Kế hoạch, bộ câu dò, kết quả từng lượt, sổ vết: riêng tư ở `data/lich_da_luu_2026-11-19/` (không vào repo công khai) — báo cáo này chỉ ghi số và đường dẫn.

**Xong khi (ghi trước khi sửa code):** file test của tính năng đạt hết, gồm test "chỉ mang lịch tới lớp ngoài thì đỏ" và test "cờ tắt chuỗi gửi model không đổi"; rồi lượt thật theo tiêu chí ghi trước trong kế hoạch.

## 1. Người dùng thấy gì khác

- **Trước:** người dùng lập lịch bằng biểu mẫu rồi hỏi tiếp bằng lời về chính lịch đó ("ngày 1 đi hết mấy tiếng", "tóm gọn lịch này để chép", "tổng tiền vé của lịch này"). Trợ lý không nhìn thấy lịch vừa lập nên trả lời trên một lịch mẫu lấy từ kho — nói chắc mà sai, 3 / 3 kịch bản ở lượt đo trưa 19/11.
- **Sau (cờ `lich_vao_hoi_thuong`, chủ dự án chọn BẬT 19/11):** trong cuộc trò chuyện đã có lịch, mỗi lượt hỏi thường nhận thêm một nguồn "Lịch bạn đang có" do code in: tham số lịch, từng ngày (buổi, giờ, tên điểm), và các con số code tính sẵn — số điểm mỗi ngày, giờ bắt đầu, giờ kết thúc mục ban ngày cuối, khoảng từ đầu tới cuối, tổng thời lượng tham quan, ngày dài nhất. Model chỉ diễn đạt.
- Ví dụ ở lượt thật: hỏi ngày 1 mất mấy tiếng và có kịp về trước 5 giờ chiều không ⇒ trả lời "5 giờ tham quan, chưa tính đi lại ăn nghỉ; phần ban ngày từ 8:00 đến 16:00; chưa tính đường về nên không xác nhận chắc" — đúng các số code in cho lịch đang có.

## 2. Bằng chứng

| Đo gì | Kết quả | So với mốc | Nhãn |
|---|---|---|---|
| Test bằng đồ giả (model thay bằng bản trả lời theo kịch bản; bộ tìm thật) — file `backend/tests/test_lich_vao_hoi_thuong.py` | 14 đạt | chưa có trước việc này | [máy kiểm]; phiên B chạy lại 14 đạt [người thứ hai kiểm] |
| Cố ý phá: chỉ mang lịch tới lớp trace ngoài | 2 test đỏ | — | [máy kiểm] |
| Cố ý phá: phép kiểm số thời tiết nhận lại số của nguồn lịch | 1 test đỏ | — | [máy kiểm] |
| Cờ tắt: chuỗi gửi model so với `main` chụp cùng ngày (228 dòng) — chụp trên NHÁNH `6c29008` trước khi gộp; bản đã gộp chưa chụp lại | giống từng byte | `main` trước gộp | [máy kiểm] |
| Cờ bật, cuộc KHÔNG có lịch: chuỗi gửi model so với cờ tắt (228 dòng) | giống từng byte | cờ tắt | [máy kiểm] |
| Lượt thật giai đoạn 1 (lịch + số giờ): 8 kịch bản quyết + 29 cuộc dò bên bật, 15 cuộc bên tắt cùng buổi | 0 lỗi hạ tầng · 0 câu trả lời bị rút · nguồn lịch có ở 32 / 32 lượt hỏi thường; không có ở lượt sửa (6), trò chuyện (1), ngoài phạm vi (3) | — | [máy kiểm] |
| Người đọc 100 % lượt thật (phiên E — người soạn bộ dò, không viết code) | 0 con số về lịch sai / 32 lượt · 0 điểm ngoài lịch bị nói như trong lịch · 0 lượt nói "đã sửa" khi lịch không đổi · 0 câu ngoài kho được trả lời · kéo lịch vào không cần thiết 0 / 12 (ngưỡng ≤ 2) | bên cờ tắt cùng buổi | [người thứ hai kiểm] |
| Hai kịch bản từng sai (hỏi số giờ · tóm lịch để chép), mỗi cái 2 lần | xong 4 / 4, trên đúng lịch | trưa 19/11: sai 2 / 2 | [người thứ hai kiểm] |
| Kịch bản "tổng tiền vé của lịch", 2 lần | trả lời trên đúng lịch, nhưng tổng 700.000 đồng do MODEL tự cộng giá kho (đúng) ⇒ KHÔNG đạt dòng quyết ghi trước "phép tính tiền phải do code" | trưa 19/11: tính trên lịch khác | [người thứ hai kiểm] |
| Hỏi ngay sau một lượt sửa lịch (2 chuỗi) | trả lời theo lịch ĐÃ sửa | — | [người thứ hai kiểm] |
| Tiền lượt thật giai đoạn 1 | 0,073 USD (cộng cả phần câu trả lời chạy song song bị bỏ: khoảng 0,075) | trần ghi trước 0,15 | [máy kiểm] |

Ai kiểm: phiên E review kế hoạch hai vòng (vòng 1: 4 điểm lớn — trong đó "lịch phải mang qua HAI lớp trace, không phải một" — và 7 điểm nhỏ, C nhận cả); phiên B review nhánh (1 điểm lớn: C loại hẳn số của nguồn lịch khỏi phép kiểm số khoảng cách làm câu trả lời nêu đúng số giờ của lịch bị rút — đã sửa, có hai test thấy đỏ trước khi sửa); phiên E đọc tay; phiên điều phối duyệt theo mã băm và gộp.

## 3. Chưa làm / giới hạn

- **Tổng tiền vé do code tính (giai đoạn 2): ĐÃ THỬ, CHƯA BẬT.** Code cộng từ bảng giá chép từ kho (26 / 41 điểm có giá, đã soát); phép tính khớp 5 / 5 ca đối chiếu của người review (3 ca có phép cộng, 2 ca kiểm "không cộng": bảng chưa có giá, không biết số người). Trong 26 điểm, 25 dòng giá được soát độc lập, 1 dòng thêm sau do phiên điều phối đối; 5 câu lưu ý về giá chưa có người thứ hai soát. Nhưng ở lượt thật, câu hỏi về tổng tiền / giá vé bị trả câu từ chối khuôn 6 / 12 lượt qua hai lần chạy (lần đầu 4 / 6; sau MỘT bản sửa câu chữ 2 / 6; chưa tính 1 / 1 ở cuộc chẩn đoán. Tính trên mọi lượt gõ có liên quan tới tiền: 4 / 10 và 2 / 8). Nguyên nhân đã xác nhận bằng sổ vết: model tự gọi tìm kho đi kiếm giá của đúng các điểm bảng chưa có giá, không thấy, rồi viết câu từ chối theo lời dặn "bằng chứng không đủ" — dù tổng do code in nằm ngay trong ngữ cảnh. Lượt không tìm thêm thì luôn được trả lời (11 / 11): 9 lượt dùng số code in, 2 lượt là số model tự tính và đúng (tổng theo ngày ở bản chưa in dòng đó; một câu giả định). Theo luật ghi trước (một bản sửa, không vòng hai) ⇒ dừng; nhánh giữ làm hồ sơ: `origin/p9-c-lich-tien-ve`. Tiền phần này: 0,034 USD.
- **Vì vậy với cờ đang bật:** hỏi tổng tiền vé ⇒ model tự cộng giá kho trên đúng lịch (đúng 3 / 3 ở lượt thật, nhưng là số model tính). Câu giả định ("nếu thêm một người…") cũng là số model tự tính.
- Lỗi có sẵn thấy lại ở lượt đo, không do cờ: một câu giả định "nếu bỏ X thì…" bị lần hiểu ý sửa lịch thực hiện như lệnh sửa (điểm bị bỏ thật).
- Lịch lưu trong RAM, hết hạn sau 30 phút không nhắn; đường gọi không stream không nạp lịch.
- Chưa có test ở mức route cho "hỏi ngay sau lượt sửa" (đã kiểm bằng lượt thật thay thế); lượt hỏi bằng ảnh và lượt ghép sau thẻ hỏi lại chưa có test riêng.
- Mẫu: một lịch mặc định (2 ngày, 2 người lớn) + một lịch gia đình; câu do agent viết, mỗi câu 1–2 lần chạy.
- Giới hạn nhận khi review: thời gian đi lại model bịa mà trùng một số-có-đơn-vị-thời-gian của lịch vẫn lọt phép kiểm số khoảng cách.

## 4. Cách thử trong 2 phút

1. Bật hệ thống theo `guides/RUNBOOK_BAN_GIAO.md` mục 1–2, mở giao diện.
2. Vào "Lên kế hoạch", để mặc định (2 ngày, 2 người lớn), bấm tạo lịch.
3. Gõ: "ngày 1 đi hết mấy tiếng, có kịp về trước 5 giờ chiều không" ⇒ đúng là: nêu 5 giờ tham quan và khung 8:00 – 16:00 của CHÍNH lịch vừa hiện. Sai là: nhắc tới điểm không có trong lịch trên màn hình.
4. Gõ: "tóm gọn lịch này để mình chép" ⇒ đúng là: đủ các mục của lịch trên màn hình, đúng giờ.

## 5. Bảng bàn giao

| | |
|---|---|
| Đã làm | kế hoạch 2 bản + khối sửa sau duyệt · code giai đoạn 1 (đã gộp `1a9a0f8`) · lượt thật giai đoạn 1 · code + lượt thật + một bản sửa giai đoạn 2 (nhánh hồ sơ) · nhánh bật cờ `origin/p9-c-bat-lich-vao-hoi-thuong` |
| Chưa làm | cả bộ test trên nhánh bật cờ (chờ lượt máy) · lượt thật trên đúng mã commit bật cờ |
| Tự hoãn + lý do | test mức route cho "sau lượt sửa" — dựng cả app tốn RAM, đã có hai chuỗi lượt thật thay thế · chữa gốc "model tự tìm thêm rồi từ chối" — phiên điều phối mở thành việc riêng |
| Lệnh kiểm | từ `backend/`: `uv run pytest tests/test_lich_vao_hoi_thuong.py -q` ⇒ `14 passed` (cần Qdrant bật + dữ liệu riêng tư) |
