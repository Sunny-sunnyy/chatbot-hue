# Review B42 — phân loại lỗi tầng tìm (A, 2026-10-26 21:0x +0700)

Người kiểm: A (`hue-rag-2d`). Đối tượng: `phan_loai_loi_B.md` (B). Mức rủi ro: thấp (chỉ đọc Qdrant, 0 USD, không đổi chatbot).

## Cổng tối thiểu
- 1 file tracked mới + private `data/cai_tien_tung_khau_2026-10-26/b42_*`, `tools/b42_*`; không đổi code. Report chỉ có chỉ số câu, số đếm, hạng —
  A đọc hết; hook quét trùng 0.

## Kiểm độc lập (A, từ `data/phase_8_1/g1/runtime.jsonl` — không dùng output của B)
| Khẳng định của B | A tính lại | Khớp |
|---|---|---|
| 40 câu dev có đoạn đúng | 40 | ✓ |
| đủ đoạn đúng: pool 30 = 31, top-10 = 22, context 5 = 17 | 31 / 22 / 17 | ✓ |
| natural 6 / 12 ở cả context 5 và 10 | 6 / 6 trên 12 | ✓ |
| 18 câu thiếu ở context 10 (danh sách §3.4) | cùng 18 câu | ✓ |

Phần chia nguyên nhân (hạng dense sâu `limit=300`, BM25 cả kho) A không chạy lại — dựa trên lượt Qdrant mới của B; B đã kiểm chéo tầng với G1 40 / 40.

## Finding
- Không có. Ghi chú (không chặn): §4 H-a trích đúng 8.1 G1.3 (`native p30` không khác) — nghĩa là "mở rộng pool" một mình đã thử; tín hiệu còn lại
  là pool rộng **kèm** xếp lại (8.1: rerank luna MRR +0,17) và nhóm "BM25 kéo xuống" (5 fact). A dùng khi viết tài liệu thiết kế.

## Kết luận
`ready_for_user_confirmation` (0 / 0 / 0). Cùng C36: phần thiếu còn lại ở context 10 chỉ sửa được ở tầng tìm ⇒ A trình User lại phạm vi đợt.
