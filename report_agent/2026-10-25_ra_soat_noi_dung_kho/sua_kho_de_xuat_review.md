# Review: đề xuất sửa kho B73 (C66)

Decision: **ready_for_user_confirmation** (vòng 2, 14:44 27/10/2026) — 41 mục "sửa": **giữ 40 · giữ có điều kiện 1 · bỏ 0**. Vòng 1: giữ 37 · sửa 3 · có điều kiện 1 · bỏ 0.
Người kiểm: C (Claude Opus 5.5, `hue-rag-86`) · 14:41 27/10/2026 (`date`) · Việc: `session_prompt/CURRENT_HANDOFF.md` → C66. 0 USD; kho chỉ đọc.
Chi tiết từng mục (private): `data/sua_kho_2026-10-27/review_c66.md`. File này không chép nội dung kho — chỉ mã mục, số đếm.

## 1. Phạm vi

- 41 diff / 111 edit / 61 file của `data/sua_kho_2026-10-27/` (B73); đọc mọi cặp chữ cũ / mới; mở dòng căn cứ trong kho cho 9 mục nhóm "sub-agent đã thấy Golden Foods cũ", 3 mục
  "edit vượt dòng" và 11 mục khác. Không đọc `evaluation/`, Golden, câu kín.
- 12 mục chuyển nhóm (tra ngoài / không cần sửa): đọc lý do, không review sâu.

## 2. Kết quả

| Nhóm | Số mục | Giữ | Sửa | Có điều kiện | Bỏ |
|---|---:|---:|---:|---:|---:|
| Sub-agent đã thấy Golden Foods cũ (đối chiếu chỉ với kho) | 9 | 9 | 0 | 0 | 0 |
| Có edit vượt dòng | 3 | 2 | 1 | 0 | 0 |
| Còn lại | 29 | 26 | 2 | 1 | 0 |
| **Tổng** | **41** | **37** | **3** | **1** | **0** |

- Nhóm 9 mục: mọi đổi tên đơn vị hành chính khớp ghi chú sắp xếp đơn vị trong kho; hai loại suy luận nhiều bước mà B nêu đều có từng bước bằng câu trong kho.
- 3 mục "sửa": 1 mục bản mới **bỏ mất thông tin** chỉ có ở chỗ đó (ngoài phạm vi mục); 1 mục một edit **đổi câu đúng thành sai** (câu chỉ hướng hiểu được hai chiều — cần viết
  lại không hai nghĩa); 1 mục bỏ một cụm của câu gốc (sửa nhỏ).
- Kiểm máy: áp **toàn bộ 111 edit lần lượt** (trong bộ nhớ) — 0 lỗi, 0 chồng trong cùng mục; 0 field rỗng / dòng đổi số. Script của B chỉ kiểm chồng giữa hai mục khác nhau;
  file `.diff` là bản xem từng edit, áp bằng thay chuỗi từ `edits/*.jsonl`, không áp patch.

## 3. Giới hạn

- Một người đọc; 18 / 41 mục chỉ đọc cặp cũ / mới + lý do B, không mở dòng căn cứ.
- Sự cố nhỏ của C: một lệnh tìm đầu tiên in vài dòng ghi chép nghiên cứu trong thư mục ghi chú của kho (không phải đánh giá / Golden / câu kín); sau đó loại thư mục đó khỏi mọi lệnh tìm.

## 4. Bước tiếp

B sửa 3 mục theo tiêu chí đóng trong file private ⇒ C kiểm phần sửa ⇒ A trình User đợt sửa kho (áp kho + build lại index là việc rủi ro cao, cần User duyệt).

## 5. Vòng 2 — kiểm phần sửa (14:44 27/10/2026)

B sửa đúng 3 mục theo tiêu chí đóng (viết lại câu chỉ hướng một nghĩa; giữ lại hai thông tin bị mất; giữ lại cụm bị bỏ). C kiểm sha diff mới, đọc lại từng chuỗi, chạy lại áp
toàn bộ 111 edit lần lượt: 0 lỗi. Cả 3 mục **đóng**. Thư mục `diffs_them/` (B thêm sau) không thuộc phạm vi review này.
