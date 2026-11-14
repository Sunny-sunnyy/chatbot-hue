# Plan (mức nhẹ) — Sửa lịch bằng lời, nhiều lượt, trên lịch bản 2 · B · 12:07 14/11/2026

A giao 14/11 (agent đợt 1, việc (b); User chọn "4 việc theo thứ tự nhóm"). Nền: `main` (lịch bản 2 BẬT) + nhánh `p9-sua-lich` `79b3d9c` (harness `sua_lich` viết cho bộ xếp CŨ, cờ tắt, chưa đo). Giao diện: E đã chừa `lich.thay_doi = [{cau, duoc}]` ở đầu thẻ LichV2.

**Mục tiêu người dùng thấy:** sau khi có lịch, gõ "bỏ lăng Tự Đức", "ngày 2 cho Bao Vinh sang chiều", "thay Kinh thành bằng chỗ khác" ⇒ lịch đổi ngay. Đầu thẻ có khối "Đã đổi: … / Không đổi được: … (lý do)"; nói "thay" mà không nói thay bằng gì ⇒ thẻ chọn ≤ 3 điểm.

## Thiết kế (giữ nguyên các quyết định D1–D11 của plan 05/11, đổi nền sang bản 2)
1. **Code quyết, model chỉ hiểu ý.** Model gọi công cụ `sua_lich(hanh_dong: list[HanhDong])`, với 6 loại có tên: `bo_diem`, `them_diem`, `thay_diem`, `doi_buoi`, `doi_so_ngay`, `doi_tham_so`; `extra="forbid"`; tối đa 3, code áp tối đa 2.
   - Công cụ **chỉ được đưa** khi cuộc trò chuyện đang có lịch bản 2 đã lưu (giống cách gắn công cụ ngày / thời tiết).
   - Tên điểm khớp bảng v8 bằng code (`ten` + `ten_khac`, có chuẩn NFC); không khớp ⇒ ghi "Không đổi được".
2. **Bộ xếp:** `xep_v2` thêm `giu` (điểm giữ chỗ ngày / buổi) + `loai` (điểm không cho quay lại). Mặc định giữ hành vi cũ: test so **3.840 tổ hợp giống byte** với khi không truyền hai tham số này. Mọi khung sau sửa qua `kiem_khung_v2` (0 lỗi) mới nhận.
3. **Lưu theo cuộc** (`api/conversations.py`, RAM, cùng hạn 30 phút): sau lượt lịch đạt, lưu `{tham_so, ngay_di, khung, loai, cau}` — chỉ dữ liệu code dựng, không lưu chữ người dùng. "Cuộc trò chuyện mới" xoá.
4. **Viết lại câu:** chỉ gọi model cho các mục MỚI; mục không đổi giữ câu cũ đã kiểm ⇒ rẻ hơn lượt đầu. Kiểm câu giữ nguyên (`kiem_cau`, dự phòng theo mục).
5. **Sự kiện:** `lich_khung` (khung mới + `thay_doi` + `the_chon`), `lich_cau`, `lich_xong` như lượt đầu ⇒ giao diện LichV2 vẽ lại đúng chỗ.
6. **Cờ** `sua_lich_v2` (TẮT). Tắt ⇒ chuỗi gửi model giống byte (Q1 228 / 228).

## Tiêu chí ghi trước
| Mã | Tiêu chí | Đo bằng | Tiền |
|---|---|---|---|
| Luôn | khung sau sửa `kiem_khung_v2` = 0 lỗi; điểm đã bỏ không quay lại; điểm không chạm giữ đúng ngày / buổi; ≤ 2 hành động áp / lượt | test + mô phỏng 0 USD (mọi hành động trên khung của 3.840 tổ hợp) | 0 |
| Q1 | cờ tắt ⇒ chuỗi gửi model giống byte; `xep_v2` mặc định giống byte 3.840 / 3.840 | test | 0 |
| **Q3 (quyết)** | bộ chuỗi `data/phase_9/bo_do_sua_lich/`: hành động code áp **đúng nhãn** `ky_vong` — **pass^2**: đã thấy **≥ 8 / 10**, kín **≥ 4 / 5** (người chạy kín: B; A không mở). Lượt đầu chuỗi gửi bằng biểu mẫu với tham số của nhãn | harness chạy server thật | ≈ 0,05 |
| Q5 | an toàn 32 ×2: 0 câu đổi tuyến / 0 câu an toàn lạc sang sửa lịch | bộ an toàn | ≈ 0,02 |
| UI | Playwright 1440 + 390: khối "Đã đổi / Không đổi được" + thẻ chọn hoạt động bằng bàn phím; 0 lỗi console | Playwright | ≈ 0,002 |

**Dừng:** Q3 trượt sau một vòng chỉnh mô tả công cụ ⇒ báo A, không hạ ngưỡng.

**Giờ:** ~1,5 ngày (port + test 0,7 · harness bản 2 0,3 · giao diện 0,2 · đo 0,3).

## Bảng rà AI FDE (agent-design-review + agent-security-review)
| Mục | Hiện trạng / thiết kế | Khớp / lệch |
|---|---|---|
| Có cần model? | Hiểu câu tự do ⇒ hành động: cần model. Áp, xếp, kiểm luật, chọn điểm thay: code | khớp (§2 skill) |
| Tham số công cụ | Enum loại + tên điểm (khớp bảng bằng code) + ngày / buổi số nhỏ; phạm vi cuộc do code điền từ cookie, model không điền | khớp |
| Lời từ chối thành kết quả công cụ | Hành động không áp được ⇒ trả mã + câu cố định cho model và cho khối "Không đổi được"; không làm sập lượt | khớp |
| Trần + phục hồi | ≤ 3 hành động gửi / ≤ 2 áp; `max_turns` như vòng hiện tại; khung hỏng ⇒ giữ khung cũ + lý do | khớp |
| Trí nhớ | Một loại (khung của cuộc), RAM 30 phút, xoá khi "Cuộc mới"; không lưu chữ tự do | khớp |
| Chữ người dùng là dữ liệu | Câu sửa chỉ ra hành động trong enum; không vào truy vấn ngoài; tên điểm ngoài bảng bị bỏ | khớp |
| Đường ra mới | Không (không mạng mới, không ghi ngoài) | khớp |
| Bộ ba chết người | Không có dữ liệu riêng tư + nội dung ngoài + kênh ra cùng lúc trong đường này | khớp |
