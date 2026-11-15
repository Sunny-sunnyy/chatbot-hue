# Plan (mức nhẹ) — Khối "Nơi ở gợi ý" chỉ hiện khi người dùng hỏi · C · 16:09 15/11/2026

User thử bản đang chạy 15/11 (A ghi nhận 16:06 15/11/2026): "đưa vào lúc người dùng không hỏi là không phù hợp". Làm sau khi bậc 1 (đổi hạng chỗ ở bằng lời) vào `main`, trước lượt có phí của bậc 2. Chưa code.

**Căn cứ để review:** `backend/llm/len_ke_hoach.py` (`gan_o_an`) · `backend/llm/sua_lich_v2.py` (`ly_do_giu_hang`, hành động `doi_hang_o`) · `frontend/src/LichV2.jsx` (`NoiO`) · `backend/api/routes/cong.py` (`dung_lich_mau`).

## Hiện trạng
- Lịch từ 2 ngày trở lên **luôn** có khối "Nơi ở gợi ý" (khu + ≤ 5 cơ sở, trải mọi hạng) dù người dùng không chọn gì về chỗ ở.
- Người dùng "hỏi" về chỗ ở bằng hai đường đã có: (a) chọn hạng ở ô "Chỗ ở theo hạng sao (không bắt buộc)" của biểu mẫu; (b) nói bằng lời — hành động `doi_hang_o` của bậc 1. Cả hai đều ghi mức hạng vào tham số lịch, và mức này đã được giữ qua mọi lượt sửa.

## Cách làm — không đổi lời dặn, không trạng thái mới
1. **"Đã hỏi" = tham số lịch có mức hạng.** `gan_o_an` chỉ dựng khối Nơi ở khi `tham_so.ngan_sach` có giá trị (1 điều kiện). Không thêm cờ, không thêm trường lưu.
2. **Chưa hỏi** (lịch ≥ 2 ngày, cờ nơi ở bật): lịch không có khối (không khu, không thẻ); code gắn một khoá nhỏ để giao diện hiện **một dòng link**: "Cần chỗ ở? Xem gợi ý theo khu" ⇒ trang Chỗ ở (`#/cho-o`). Lịch 1 ngày: không dòng nào (như cũ).
3. **Chữ chép / tải .txt / .ics / lịch sử chat:** không còn dòng nơi ở khi chưa hỏi (các đường này đã chỉ in khi lịch có khối); dòng link không vào chữ.
4. **Nói bằng lời khi lịch chưa có khối** ("cho mình khách sạn 4 sao"): `doi_hang_o` thử mức mới bằng hàm dựng ô Nơi ở (không phụ thuộc khối đang hiện hay không) ⇒ ghi mức ⇒ khối **bật** ở mức đó; câu báo "Đã đổi hạng chỗ ở: chưa chọn → 4–5 sao." đổi chữ thành "Đã thêm gợi ý chỗ ở hạng 4–5 sao." khi trước đó chưa có mức. Chỉ lịch 1 ngày / cờ tắt mới trả "không có mục chỗ ở".
5. **Xin chỗ ở mà không nêu hạng** ("gợi ý chỗ ở đi"): bậc này **hỏi lại hạng** — dòng sẵn có sửa chữ: "chỗ ở — bạn muốn hạng nào: 1 sao / đạt chuẩn, 2–3 sao hay 4–5 sao? Nói hạng thì mình thêm gợi ý vào lịch." + dòng link trang Chỗ ở vẫn ở đó. *Chưa làm:* hiện khối mọi hạng cho câu này — cần một trạng thái "đã hỏi, không hạng" đi qua bộ xếp và chưa biết model có xếp câu "gợi ý chỗ ở" vào `doi_hang_o` không (bộ H2 chỉ đo câu "đổi / rẻ hơn / sang hơn") ⇒ để sau, nếu làm thì đếm 6–8 câu trước (≈ 0,002 USD).
6. **Lịch mẫu "Ví dụ"** (trang Lên kế hoạch): đề xuất thêm mức "2–3 sao" vào tổ hợp ví dụ (1 dòng) ⇒ ví dụ vẫn cho thấy khối Nơi ở, và nút "Xếp lịch như ví dụ" gửi đúng tổ hợp có hạng đó — nhất quán với luật "có hỏi mới hiện". *Chọn khác:* để ví dụ không có khối (0 dòng sửa) — mất chỗ giới thiệu tính năng. **A quyết.**

## Tiêu chí ghi trước (0 USD trừ Playwright)
| Mã | Kiểm | Ngưỡng |
|---|---|---|
| T1 | test 3.840 khung: không mức ⇒ `o_dau` rỗng, có khoá link khi ≥ 2 ngày; có mức (3 mức) ⇒ khối như hôm nay (so byte với hàm hiện tại) | 0 lệch |
| T2 | chữ `ghep_chu` (chép / .txt / lịch sử): không mức ⇒ 0 dòng "Nơi ở"; có mức ⇒ giống byte bản trước | 0 lệch |
| T3 | sửa bằng lời trên lịch chưa có khối: `doi_hang_o` có mức ⇒ khối bật đúng mức + câu "Đã thêm…"; không mức ⇒ câu hỏi lại hạng, lịch không đổi; sửa khác (bỏ điểm, đổi số ngày) sau khi đã có mức ⇒ khối còn | đạt |
| T4 | chuỗi gửi model: 25 hằng lời dặn + tin nhắn viết câu / hiểu ý giống byte `main` (khối nơi ở vốn không vào tin nhắn) | giống byte |
| T5 | lịch mẫu theo quyết định mục 6 | đạt |
| UI | Playwright 1 khổ màn (1440), lịch thật 2 lượt: không chọn hạng ⇒ 0 khối, 1 dòng link mở đúng `#/cho-o`; chọn hạng ⇒ khối như cũ; 0 lỗi console | đạt · ≈ 0,008 USD |

- **Không chạy:** H1–H3 / Q3 / Q5 / Q5b (lời dặn + khuôn đầu ra không đổi ⇒ 0 câu chạm model), Golden, đo độ trễ. Test rộng một lần trước bàn giao (chạm giao diện + lõi lịch).
- **Tiền:** ≈ 0,01 USD. **Review:** một review cả nhánh (đổi câu người dùng thấy). **Tài liệu:** `bai_hoc/25` + sổ 07 cùng đợt.
- **Số cũ thành lịch sử:** "ô có ảnh 95,3 %", "bữa / lịch có nơi ở" đo trên lịch luôn có khối — ghi chú ở sổ 07 khi merge.

## Bảng rà AI FDE (ngắn)
| Mục | Thiết kế | Khớp / lệch |
|---|---|---|
| Model ↔ code | Model không đổi. Hiện / ẩn khối: một điều kiện code trên tham số đã có | khớp |
| Trí nhớ | Không trường mới — "đã hỏi" suy từ mức hạng đang lưu | khớp |
| Đường ra / dữ liệu mới | Không; link trang Chỗ ở là link nội bộ đã có | khớp |
| Làm sai mà báo đã làm | Câu "Đã thêm gợi ý chỗ ở hạng X" chỉ in khi khối thật sự dựng được ở mức X (T3) | khớp |
