# TỔNG HỢP đợt `2026-11-06_b5_cau_tu_nhien` — lịch trình B5: câu đo tự nhiên, sửa lỗi, kín v2

A viết 22:43 06/11/2026 (kết phiên tối 06/11). Đợt **đóng** (mục tiêu đo lại lịch trình trên câu tự nhiên đã xong; hướng tiếp đổi sang biểu mẫu — spec giao diện cổng đợt 1, đợt `2026-11-06_giao_dien_cong/`).

## Mục tiêu
Đo lại lịch trình B5 bằng câu giống người thật hỏi (bộ kín cũ không tự nhiên — S100), sửa trước các lỗi code đã thấy.

## Quyết định theo giờ (User, A ghi nhận bằng `date` — nguyên văn ở `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`)
- 10:03 / 10:47 06/11: agent chấm trước; câu kín cũ không tự nhiên ⇒ gác, làm bộ v2.
- Tối 06/11: User duyệt bộ kín v2 (sửa 4 / 5 câu); kín v2 không đạt ⇒ chọn "biểu mẫu trước".

## Kết quả
| Việc | Kết quả | Hồ sơ |
|---|---|---|
| E19 câu tự nhiên | 20 lượt hỏi thật + TRIPO vòng 4 ⇒ 8 câu mẫu; bộ kín v2 5 câu md5 `de95ff85e491` | `e19_implementation.md` |
| B171 sửa 2 loại lỗi | merge `dbb4004` cờ tắt; C review 2 vòng ready | `b171_implementation.md`, `b171_review.md` |
| Kín v2 | **3 / 5 không đạt** (i 4 · ii 3 · iii 4 / 5; 2 agent khớp 15 / 15); 0,003 USD | `e19_kin_v2.md` |
| E20 từ chối khi hỏi kèm | nguyên nhân chứng minh bằng code (`tim_kho` bị chặn sau lịch); sửa để khi bật câu tự do | `e20_tu_choi_hoi_kem.md` |
| C210 hỏi lại số ngày | chưa tái tạo được; không sửa code | `c210_implementation.md` |
| E21 cột thời lượng | 7 / 33 điểm có trong kho; "đi dày" không đổi ⇒ câu User | `data/phase_9/lich_trinh/diem_cho_user_v6.md` (private) |

## Giới hạn
Bộ kín v2 nhỏ (5 câu); harness kín không lưu tham số model ⇒ không biết gốc lỗi hỏi lại thừa. Câu gõ tự do chưa bật.

## Bước tiếp
Lịch trình qua biểu mẫu trong giao diện cổng đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md`, tiêu chí Q-F).

Tiền đợt ≈ 0,05 USD (B171 0,029 · kín v2 0,003 · E20 0,008 · C210 0,004 · cổng A).
