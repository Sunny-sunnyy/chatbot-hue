# Ngày đăng cạnh tiêu đề nguồn web (B, 14:20 17/11/2026)

Việc: lô lỗi nhỏ chiều 17/11 — "tin lũ cũ hiện như tin hiện tại" ở danh sách nguồn web. A duyệt CHỈ phần hiện ngày (không lọc theo tuổi tin). Nhánh `p9-ngay-nguon-web` từ `origin/main` `c1fd6c9`. Dữ liệu (private): `data/ngay_web_2026-11-17/`.

## Tái hiện (0 USD)
Lượt đo câu bão sáng 17/11 (ca 9, sha `383f055`, `data/cau_bao_2026-11-17/do/lui_bo31/ket_qua.jsonl`): mục web câu cố định "thông tin thay đổi theo thời gian… xem nguồn chính thức bên dưới" + 5 nguồn chỉ có tiêu đề / tên miền, không ngày. Gốc: `tra_web.doc_ket_qua` bỏ trường `date` của Serper. 3 file Serper thô đã lưu: 10 / 25 kết quả có `date`, một dạng duy nhất "N thg N, NNNN".

Một lượt Serper thật (A duyệt, 0,001 USD; `serper_lu.json`), câu về mực nước sông Hương: 1 / 5 kết quả có `date` = "17 thg 11, 2025" — đúng tin "Lũ khẩn cấp trên sông Bồ, sông Hương" của một năm trước; 4 / 5 không có ngày. Không thấy dạng tương đối ("N ngày trước").

## Đã làm
- `backend/llm/tra_web.py`: `ngay_dang(chuoi, hom_nay)` — chỉ đọc dạng "N thg N, NNNN" (khớp toàn chuỗi); ngày không có thật / sau hôm nay (giờ VN) / dạng khác ⇒ None. `doc_ket_qua` thêm trường `ngay` vào mỗi nguồn.
- `backend/api/routes/chat.py` `_web_payload`: tiêu đề gửi giao diện = tiêu đề + " (dd/mm/yyyy)" khi có ngày. **Chuỗi gửi model không đổi** (`dau_vao_model` chỉ dùng tiêu đề + đoạn trích gốc; test khẳng định ngày không có trong đó). Giao diện không đổi code.

## Kiểm [Chạy]
| Phép kiểm | Kết quả |
|---|---|
| Bộ dò 23 ca do C soạn (`ca.json`, chạy `chay_ca.py`) | **0 SAI**; 6 từ chối: 5 ca tương đối ("3 ngày trước", "5 giờ trước"…) + "Hôm qua" — chưa thấy ở Serper thật ⇒ không đọc (luật §8: từ chối nhầm được phép) |
| `test_b6_tra_web.py` + `test_mo_dau_web.py` | 135 đạt (1 test mới) |
| Test rộng | không chạy — nhánh đổi một hàm thuần + chỗ gọi, test file chạm đủ |

## Giới hạn
Kết quả Serper không có ngày (đa số: 15 / 25 file cũ, 4 / 5 lượt thật) vẫn không có ngày — tin cũ không ngày vẫn có thể đọc như tin mới. Không lọc tin theo tuổi (A chọn: luật ẩn có thể gạt hết nguồn). Serper đổi dạng ngày ⇒ mất ngày, không ra ngày sai.

## Thời gian
pytest 2 file 33 s · bộ dò < 5 s · lượt Serper thật < 2 s.
