# Bỏ một hoạt động buổi tối: dòng báo nay nói đủ các tối bị đổi — report của phiên C (viết 10:01 22/11/2026)

Việc: phiên đo thấy ở lượt trình duyệt sáng 22/11 (đường sửa lịch có sẵn, không do tính năng nào mở hôm nay); phiên điều phối đồng ý bản "nêu tên".
Nhánh `p9-c-bao-toi-xep-lai`: `backend/llm/sua_lich_v2.py` (nhánh `bo_diem` + chỗ dựng câu), `backend/tests/test_sua_lich_v2.py` (2 ca), một câu ở runbook
10.2. Không công tắc mới (sửa câu chữ cho đúng sự thật); lịch và cách xếp KHÔNG đổi. Người đọc: phiên B.

## Người dùng thấy gì khác

| Tin (lịch 3 ngày kiểu cân bằng) | Trước | Sau |
|---|---|---|
| "Bỏ Chợ Đông Ba đi" (hoạt động tối ngày 1) | "Đã bỏ Chợ Đông Ba, thêm Ca Huế trên sông Hương (ngày 3, buổi tối) vào chỗ trống." — trong khi tối ngày 1 và ngày 2 cũng đã đổi, không được nói | "Đã bỏ Chợ Đông Ba. Buổi tối xếp lại: ngày 1 Phố đi bộ Nguyễn Đình Chiểu, ngày 2 Khu phố Tây Huế, ngày 3 Ca Huế trên sông Hương (mới thêm)." |
| Bỏ hoạt động tối của NGÀY CUỐI, hoặc bỏ một điểm ban ngày mà không tối nào bị chuyển ngày | dòng báo cũ | y nguyên dòng báo cũ |

## Vì sao có chuyện này (không sửa ở đây)
Mỗi lần lịch được xếp lại, bộ xếp chọn LẠI hoạt động tối cho từng ngày: lấy ứng viên chưa dùng đầu tiên theo thứ tự (`lich_trinh_v2._xep_toi`); bộ sửa lịch
chỉ giữ chỗ điểm ban ngày. Bỏ hoạt động tối ngày 1 ⇒ ngày 1 nhận cái vốn của ngày 2, ngày 2 nhận của ngày 3, ngày cuối nhận cái mới. Dòng báo cũ chỉ kể
điểm chưa từng có trong lịch. Giữ nguyên các tối khác và chỉ lấp chỗ trống là đổi cách xếp — gắn với câu "bỏ buổi tối: để trống hay lấp" đang chờ chủ dự án.

## Số đếm trước khi sửa (0 đồng, 54 lịch mẫu 2–4 ngày × 3 kiểu đi × 6 sở thích)
- Bỏ từng hoạt động tối: 150 lệnh ⇒ 45 (30 %) có tối của NGÀY KHÁC đổi mà dòng báo không nói; tối bị bỏ không ở ngày cuối: 45 / 101; ở ngày cuối: 0 / 49.
- Bỏ từng điểm ban ngày: 436 lệnh ⇒ 1.

## Lệnh kiểm + đầu ra [máy kiểm; hàm thuần trên bảng lịch thật, không dựng app, không model]
| Lệnh (từ `backend/` của cây nhánh, không nạp env) | Đầu ra |
|---|---|
| `… pytest tests/test_sua_lich_v2.py -q` trên code CŨ + 2 ca mới | `2 failed, 13 passed` |
| cùng lệnh trên code mới | `15 passed` (ca 1: đúng nguyên câu của bảng trên + ca ngày cuối giữ câu cũ; ca 2: 27 lịch mẫu × bỏ từng điểm — tối nào đổi vì bị chuyển ngày thì tên hoạt động tối mới của ngày đó phải có trong câu, không thì câu đúng khuôn cũ) |
| `test_sua_lich_them` · `test_sua_lich_kem_hoi` · `test_doi_cho_ngay` · `test_sua_lich_buoi_toi` | 9 · 7 · 47 · 7 passed |

## Chưa làm · giới hạn
- CHƯA: các file test dựng app và một lượt nhìn trình duyệt — chờ phiên điều phối báo đã ghi bài mới vào kho + cập nhật chỉ mục (cây cũ lệch chỉ mục thì app
  bị từ chối khởi động). Dòng báo là chữ thường trong khối thay đổi sẵn có, không có thành phần giao diện mới.
- Lệnh THAY / THÊM / DỜI một điểm ban ngày cũng xếp lại lịch; nếu lần xếp đó làm hoạt động tối bị chuyển ngày thì dòng báo của các lệnh ấy vẫn chưa nói
  (chưa đếm; với lệnh bỏ điểm ban ngày là 1 / 436).
- Ngày không có hoạt động tối sau khi xếp được ghi "không có hoạt động tối" trong dãy.

Phép này KHÔNG cho biết người dùng có muốn các tối khác đứng yên không (câu của chủ dự án) · hướng rộng hơn: cho bộ xếp giữ chỗ cả hoạt động tối khi sửa ·
đếm rẻ nhất kế: cùng phép đếm cho lệnh thay / thêm / dời.

## Thêm 10:07 22/11/2026 — lệnh THAY (phiên điều phối chọn nối vào cùng nhánh) + kết quả đọc của phiên B

**Lệnh thay.** Đếm 0 đồng trên 54 lịch mẫu: lệnh "thay Y bằng X" áp được 3.036 lần, 145 lần (4,8 %) buổi tối đổi mà dòng báo không nói (130 lần có hoạt động tối
bị chuyển ngày) — khi X vốn là nơi lịch đang dùng làm hoạt động tối, ví dụ "thay Đại Nội Huế bằng Chợ Đông Ba": Chợ Đông Ba lên ban ngày nên tối ngày 1 nhận
hoạt động vốn của ngày 2, tối ngày 2 nhận cái mới. Lệnh dời: 0 / 403; lệnh thêm: 0 / 23. Sửa: đoạn so buổi tối tách thành hai hàm nhỏ dùng chung
(`_toi_xep_lai`, `_cau_toi_xep_lai`) cho `bo_diem` và `thay_diem`; câu thành "Đã thay Đại Nội Huế bằng Chợ Đông Ba. Buổi tối xếp lại: ngày 1 …, ngày 2 … (mới thêm)."
Câu của lệnh bỏ không đổi so với bản `de141dc`.

| Lệnh | Đầu ra |
|---|---|
| `pytest tests/test_sua_lich_v2.py -q` trên code `de141dc` + ca test của lệnh thay | `1 failed, 15 passed` |
| cùng lệnh trên code mới | `16 passed` |
| `test_sua_lich_them` · `test_sua_lich_kem_hoi` · `test_doi_cho_ngay` · `test_sua_lich_buoi_toi` | 9 · 7 · 47 · 7 passed |

**Phiên B đọc bản `de141dc`: gộp được, 0 điểm phải sửa.** B dò bằng một bất biến khác (mọi thay đổi ở buổi tối của mọi ngày phải đọc ra được từ câu báo; 588 lệnh bỏ điểm
trên 54 lịch mẫu): 0 vi phạm. Một quan sát của B, ghi thành giới hạn (runbook 10.2): lịch 4 ngày, bỏ hoạt động tối ngày cuối khi bộ xếp hết ứng viên ⇒ nó lấy LẠI
hoạt động tối của ngày 1 cho ngày 4; câu báo nói đúng ("ngày 1 Phố đi bộ…, …, ngày 4 Phố đi bộ…") nhưng người dùng thấy một hoạt động ở hai tối — 6 / 52 lệnh bỏ tối
ngày cuối; trước nhánh này lượt đó chỉ ra "Đã bỏ Cầu Trường Tiền." Thuộc câu "bỏ buổi tối: để trống hay lấp" đang chờ chủ dự án.
