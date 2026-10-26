# Review C36 — phân loại lỗi tầng trả lời (A, 2026-10-26 20:50 +0700)

Người kiểm: A (`hue-rag-2d`). Đối tượng: `phan_loai_loi_C.md` (C, untracked lúc kiểm). Mức rủi ro: thấp (chỉ đọc, 0 USD, không đổi chatbot).

## Cổng tối thiểu
- Chỉ thêm 1 file tracked + private trong `data/cai_tien_tung_khau_2026-10-26/`; không đổi code. Report không chép câu hỏi / đáp án / nội dung kho
  (chỉ `case_index`, số đếm, nhãn) — A đọc hết; `data/tools/overlap_scan.py` 0 trùng.

## Kiểm độc lập (script A `/tmp/a_c36_check.py`, gọi `attach_labels` của harness, không dùng bảng của C)
| Khẳng định của C | A tính lại | Khớp |
|---|---|---|
| 88 câu dev chính; ctx 10 bị cờ 10 câu (19, 22, 48, 67, 68, 113, 120, 159, 167, 168) | 88; cùng 10 câu | ✓ |
| ctx 5 bị cờ 15; ctx 10 sửa 30, 89, 134, 143, 172; không câu mới | cùng | ✓ |
| Completeness mất 46 điểm ở ctx 10 | 46 | ✓ |
| 48 / 67 / 159 / 167 đủ đoạn đúng trong pool 30 nhưng không đủ ở top-10 | `runtime.jsonl`: `pool_union_gold_all` 1,0, `top10_gold_all` 0,0 | ✓ |
| 120 vắng cả pool 30 | `pool_union_gold_frac` 0,0 | ✓ |

Nhãn từng câu (đọc nội dung) A không chấm lại — một người gắn nhãn, C đã ghi ở §8.

## Finding
- **m1 (minor):** §9 lệnh chạy lại `c36_labels.py` dùng `python3` (Python hệ thống) — trái `Session_Prompt.md` §10; sửa thành `uv run python`.
  A sửa trực tiếp khi commit (một chữ, không đổi nội dung).

## Kết luận
`ready_for_user_confirmation` (0 blocker / 0 major / 1 minor đã sửa). Ý §7 (80 % điểm mất có thiếu bằng chứng ⇒ trần lợi của "khâu trả lời
trước" nhỏ) là bằng chứng đi ngược phạm vi User chọn 20:3x ⇒ A trình User (WORKFLOW §9.3).
