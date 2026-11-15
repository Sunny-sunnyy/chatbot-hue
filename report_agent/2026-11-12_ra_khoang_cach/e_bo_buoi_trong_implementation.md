# Buổi để trống không hiện trong lịch (E · 16:11 15/11/2026, `date`)

Người làm: E. A giao (User thử trên bản đang chạy, A ghi nhận 16:06 15/11/2026: "nếu để trống thì không cần thêm vào lịch gợi ý"). Nhánh `p9-bo-buoi-trong`.

## 1. Đã đổi (tầng hiển thị — không đụng bộ xếp, lời dặn, chuỗi gửi model)
- **Giao diện** (`LichV2.jsx`, dùng chung cho trang Lên kế hoạch và lịch trong trang Trợ lý): mục loại "nghỉ" của server không được vẽ nữa — gồm cả ba kiểu: "để trống — đi cùng trẻ nhỏ / người lớn tuổi", "tối nghỉ sau chuyến đi xa", "tối tự do — kho chưa có hoạt động". Gỡ code + CSS chỉ phục vụ mục này.
- **Chữ thuần của lịch** (`ghep_chu` — nguồn của nút "Sao chép lịch", "Tải về (.txt)" và lịch sử trò chuyện): bỏ dòng "- Tối: …" của mục nghỉ. File .ics vốn đã không xuất mục này.
- **Dữ liệu server giữ nguyên**: khung lịch vẫn có mục "nghỉ" (test luật xếp và bộ chấm 6 ý đọc nó) — chỉ không hiện.
- **Lý do còn một dòng, một lần cho cả lịch:** nhóm có trẻ em / người lớn tuổi vốn đã có ghi chú "…mỗi buổi một điểm, không xếp buổi tối" trong "Ghi chú của lịch" ⇒ giữ, không thêm gì. Với "tối nghỉ sau chuyến đi xa" và "tối tự do" **không có** ghi chú sẵn ⇒ bỏ hẳn (cách đơn giản nhất; A: không có chỗ sẵn thì bỏ). Hệ quả: ngày đi cụm xa chỉ còn hai mục sáng / chiều, không dòng nào nói vì sao tối trống — nếu User muốn có thì thêm một dòng ghi chú (đổi nhỏ ở server).

## 2. Kiểm
| Bước | Kết quả |
|---|---|
| `test_len_ke_hoach_v2` + `test_static_ui` + `test_quan_lich` + `test_luu_tru_lich` (sau rebase) | 126 đạt (26 s); 1 chuỗi kỳ vọng của `ghep_chu` đổi theo hành vi mới |
| `npm run build` | đạt |
| Playwright 1440, bản build do FastAPI phục vụ, 2 lịch thật qua biểu mẫu | **Có trẻ em:** 4 mục (2 sáng, 2 chiều, 0 tối); chữ "Để trống / Tối nghỉ / Tối tự do" trên trang 0, trong chữ trả lời 0; ghi chú "không xếp buổi tối" còn; server vẫn gửi mục nghỉ (4 lần xuất hiện trong luồng). **2 người lớn:** 8 mục, buổi tối 2 mục vẫn hiện, chữ trả lời có 2 dòng "- Tối…"; 0 lỗi console |
| Test rộng, Q1 | NOT RUN — không chạm chuỗi gửi model |

Ảnh + số (private): `data/bo_buoi_trong_2026-11-15/sau/`; kịch bản `tools/pw_buoi_trong.py`. Tiền ≈ 0,001 USD (2 lịch). Chưa chụp "trước" (hành vi cũ đã rõ từ ảnh của User).

## 3. Kèm trong nhánh (A dặn gộp): vài dòng số tài liệu
Khám phá 260 / 263, ảnh lịch 40 / 41, và việc này — bài 23 / 24 / 25 / 14, README bài học, sổ khâu 07, README sổ, nhật ký. E tự đối chiếu số với report ảnh (chỉ thêm dòng số).

**Giải thích ngắn:** lịch không còn mục "Tối: để trống…"; ai đi cùng trẻ nhỏ vẫn thấy một dòng ghi chú nói lịch không xếp buổi tối, nên không tưởng lịch thiếu.
