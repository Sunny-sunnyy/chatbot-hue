# Tin vừa nhờ đổi chỗ hai ngày vừa hỏi — report của phiên C (viết 09:02 22/11/2026)

Việc: sổ việc khối A, chỗ chưa ổn phiên đo thấy sau khi mở "đổi chỗ ngày 1 với ngày 2" tối 21/11. Nhánh `p9-c-doi-cho-kem-hoi`:
`backend/llm/sua_lich_v2.py` (hàm mới `cap_ngay_doi_cho_kem_hoi`), `backend/llm/len_ke_hoach.py` (hai dòng), test, một câu ở runbook mục 10.2.
Không thêm công tắc: đường mới chỉ chạy khi hai tính năng ĐÃ MỞ (`sua_lich_doi_cho_ngay`, `sua_lich_kem_hoi`) cùng bật và model báo tin có câu hỏi.

## Người dùng thấy gì khác

| Tin | Trước (main `3f7bb847`, lượt đo 21/11) | Sau (nhánh này, lượt thật 09:02 22/11/2026, model đang chạy) |
|---|---|---|
| "đổi chỗ ngày 1 với ngày 2, mà vé vào Đại Nội bao nhiêu?" | Lịch KHÔNG đổi; hai dòng: "Chưa làm: đổi chỗ, gộp hay tách các ngày — mình chưa sửa được kiểu này…" (sai nghĩa: gửi riêng thì đổi được) + "Chưa làm: phần câu hỏi…" | Lịch ĐÃ đổi chỗ hai ngày; "Đã đổi chỗ các điểm buổi sáng và chiều của ngày 1 với ngày 2; hoạt động buổi tối giữ theo từng ngày." + "Chưa làm: phần câu hỏi trong tin này mình chưa trả lời… Bạn gửi riêng câu hỏi đó, mình trả lời ngay." |
| gửi riêng "vé vào Đại Nội bao nhiêu?" ngay sau | trả lời được | trả lời được (200.000 đồng / người lớn, có nguồn) |

## Cách làm

Model vẫn chỉ nói "đây là câu sửa chưa hỗ trợ" + "tin còn có câu hỏi"; phần đọc cặp ngày vẫn do CODE theo danh sách cho phép. Hàm mới cắt tin ở dấu
câu / từ nối ("mà", "à mà", "còn", "cho mình hỏi"…), và chỉ nhận khi: đúng MỘT vế đọc được cặp ngày bằng bộ đọc cũ; mọi vế còn lại không nhắc ngày
nào của lịch và không có động từ sửa (bỏ, thêm, thay, dời, gộp…). Khác ⇒ giữ nguyên hành vi cũ. Nguyên tắc cũ giữ nguyên: từ chối nhầm được phép,
áp sai thì không.

## Lệnh kiểm + đầu ra [máy kiểm]

| Lệnh (từ `backend/` của cây nhánh, không nạp env) | Đầu ra |
|---|---|
| `… pytest tests/test_doi_cho_ngay.py -q` | `38 passed` (26 ca cũ + 12 ca mới: 4 tin được nhận, 7 tin phải từ chối, 1 ca qua luồng sửa lịch kể cả nhánh "model không báo có câu hỏi ⇒ như cũ") |
| `… pytest tests/test_sua_lich_kem_hoi.py` · `test_sua_lich_them.py` · `test_sua_lich_v2.py` | `7 passed` · `9 passed` · `13 passed` |
| lượt thật: `chay_doi_cho_kem_hoi.py` của phiên đo, chạy từ cây nhánh | ba lượt 200; lượt 2 `hai_ngay_da_doi_cho: True`, hai dòng như bảng; 0,070 USD — `data/thu_bedrock_2026-11-21/do/doi_cho_ngay/kem_hoi_nhanh_c_2211/` (riêng tư) |

## Chưa làm · giới hạn

- CHƯA: một phiên khác đọc nhánh; lượt nhìn trình duyệt (khối báo dùng đúng thành phần giao diện của mọi lượt sửa, không có chữ / khuôn mới).
- Giới hạn (đã ghi runbook 10.2): vế hỏi có nhắc một ngày của lịch hoặc có động từ sửa ⇒ vẫn ra câu chung "Chưa làm: đổi chỗ, gộp hay tách các
  ngày…"; model không báo "tin có câu hỏi" ⇒ như cũ. Số lượt thật gặp loại tin này: chưa có (tính năng mới mở tối 21/11) — sửa vì dòng báo cũ nói sai nghĩa.

Phép này KHÔNG cho biết: tỉ lệ model báo đúng "tin có câu hỏi" cho loại tin này (mới một tin, một lượt) · hướng rộng hơn: trả lời luôn câu hỏi trong
cùng lượt sửa (hiện mọi lượt sửa-kèm-hỏi đều bảo gửi riêng) · đếm rẻ nhất: đếm tin loại này trong sổ lượt thật sau buổi chủ dự án dùng thử.

## Sau review của phiên B (09:21 22/11/2026) — ba điểm, đều nhận

| Điểm | Tái hiện (test thêm TRƯỚC khi sửa) | Sửa |
|---|---|---|
| F1 — vế còn lại là lời rút lại / phủ định ("…, à mà thôi, vé Đại Nội bao nhiêu?", "đừng, đổi chỗ…") mà hàm vẫn trả cặp ngày | 7 ca của phiên B: 7 / 7 đỏ trên bản `e23e691` | vế còn lại có từ rút lời / phủ định (thôi, khỏi, không cần, đừng, khoan, huỷ, nhầm, lộn, quên, không phải, bỏ qua) ⇒ không đổi chỗ |
| F2 — vế hỏi nhắc một ngày của lịch bằng chữ "hôm" ("…, mà hôm đầu có mưa không?") vẫn đổi chỗ | 2 ca: 2 / 2 đỏ | thêm mốc "hôm đầu / hôm thứ hai / hôm cuối…" ("hôm nay", "hôm qua" không tính) |
| F3 — động từ sửa ngoài danh sách (lùi, cắt, bớt…) | không sửa code | một câu giới hạn ở runbook 10.2 |

`pytest tests/test_doi_cho_ngay.py -q`: thêm 9 ca ⇒ `9 failed, 38 passed` trên code cũ ⇒ `47 passed` sau khi sửa; `test_sua_lich_kem_hoi.py` 7 passed · `test_sua_lich_v2.py` 13 passed. Tin của lượt thật (mục trên) không chạm các từ mới nên không chạy lại lượt có phí.
