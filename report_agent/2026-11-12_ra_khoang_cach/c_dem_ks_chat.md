# Đếm trước — thẻ khách sạn trong chat (C, 12:17 15/11/2026)

A giao 15/11 (bước "khách sạn sau" của ảnh chat). 12 câu tự đặt (`data/anh_chat_2026-11-15/cau_khach_san.json`) qua **lõi trợ lý thật**, cờ theo `settings.yaml` (có tra web). Script `data/ks_chat_2026-11-15/tools/hoi.py` ⇒ `hoi.jsonl`; khớp tên ⇒ `dem.json`. Tiền **0,0083 USD**. Bảng lưu trú v4: 137 cơ sở, 58 có ảnh.

## Số [đã chạy]
| Đo gì | Số |
|---|---|
| Câu trả lời bằng bài lưu trú trong kho | 10 / 12 (2 câu sang mục web: một khu nghỉ dưỡng ven đầm, một khách sạn không có trong danh mục) |
| Câu nêu tên ≥ 1 cơ sở có trong bảng | **10 / 12** — mọi câu trả lời bằng kho |
| … nêu **đúng tên đầy đủ** như bảng ("Khách sạn …") | chỉ 4 / 12 ⇒ phải khớp **tên lõi** (bỏ tiền tố loại hình: "Khách sạn", "Khách sạn nghỉ dưỡng", "Khu nghỉ dưỡng") |
| Câu có ≥ 1 cơ sở được nêu có ảnh | **7 / 12** |
| Số cơ sở được nêu mỗi câu | 1–6 (câu danh sách 5 sao trung tâm: 4; câu "nên ở đâu cho tiện Đại Nội": 6) ⇒ cần trần 3 |
| Nguồn được trích | luôn là bài "Lưu trú ở Huế — …" (loại dịch vụ), đôi khi kèm cẩm nang / bài một nơi |

**Khớp nhầm thấy được:** 1 / 23 lần khớp. Câu ven biển chỉ nói "Villa Louise Beach" nhưng tên lõi "Villa Louise" của một cơ sở khác cũng khớp, vì nằm lọt trong tên dài hơn ⇒ cần luật **lấy tên dài nhất** ở cùng chỗ.
- Các bẫy khác đã soạn trong 12 câu đều **không** khớp nhầm ở lượt này: tên trùng sông ("Hương Giang" chỉ xuất hiện trong tên khách sạn), "Lăng Cô" trong tên khu nghỉ dưỡng, cơ sở không ảnh (Moonlight), cơ sở ngoài danh mục (Hilton ⇒ web, 0 khớp).

**Thấy thêm (ngoài việc ảnh):** câu hỏi đích danh một khu nghỉ dưỡng ven đầm có trong kho (2 bài lưu trú có tên) lại bị kho từ chối ⇒ sang mục web. Đây là lỗi tìm, ghi cho A; chưa đếm rộng.

## Kết luận
**Đáng làm.** Câu hỏi khách sạn gần như luôn nêu tên cơ sở; 7 / 12 có ít nhất một cơ sở có ảnh. Plan: `docs/superpowers/plans/2026-11-15-the-khach-san-chat-plan.md`.
