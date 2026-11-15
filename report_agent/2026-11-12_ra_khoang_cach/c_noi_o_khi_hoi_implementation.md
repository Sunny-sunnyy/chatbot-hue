# Khối "Nơi ở gợi ý" chỉ hiện khi người dùng hỏi · C · 16:16 15/11/2026

User thử bản đang chạy 15/11: "đưa vào lúc người dùng không hỏi là không phù hợp". Plan `docs/superpowers/plans/2026-11-15-noi-o-chi-khi-hoi-plan.md` (A duyệt `d99fb6ec4a5c`). Nhánh `p9-o-khi-hoi` (tách từ nhánh bậc 1 `p9-sua-hang-o`; code ở `2456c2f`). **Chờ review cả nhánh.** Không đổi lời dặn, không đổi khuôn đầu ra của model.

## Làm gì
- **Trước:** lịch từ 2 ngày luôn có khối "Nơi ở gợi ý" (khu + ≤ 5 cơ sở mọi hạng).
- **Sau:** "đã hỏi" = lịch có mức hạng chỗ ở — chọn ở ô hạng sao của biểu mẫu, hoặc nói bằng lời (hành động đổi hạng của bậc 1). `len_ke_hoach.gan_o_an` chỉ dựng khối khi có mức (một điều kiện; không cờ, không trường lưu mới — mức vốn được giữ qua mọi lượt sửa).
  - Chưa hỏi, lịch ≥ 2 ngày ⇒ không khối; server gửi khoá `cho_o_link` ⇒ giao diện hiện một dòng link "Cần chỗ ở? Xem gợi ý theo khu" sang trang Chỗ ở. Lịch 1 ngày: không dòng nào.
  - Chữ chép / tải .txt / lịch sử chat: không còn dòng nơi ở khi chưa hỏi (dòng link không vào chữ).
  - Nói bằng lời trên lịch chưa có khối, có nêu hạng ⇒ khối bật ở hạng đó, câu báo "Đã thêm gợi ý chỗ ở hạng 4–5 sao." (thay cho "Đã đổi hạng chỗ ở: chưa chọn → …").
  - Xin chỗ ở mà không nêu hạng ⇒ hỏi lại hạng (câu sẵn có sửa chữ: "chỗ ở — bạn muốn hạng nào: … Nói hạng thì mình đưa gợi ý chỗ ở hạng đó vào lịch.").
  - Lịch mẫu "Ví dụ": tổ hợp ví dụ thêm mức 2–3 sao (A quyết) ⇒ ví dụ vẫn có khối; nút "Xếp lịch như ví dụ" gửi đúng tổ hợp đó, dòng tóm tắt thêm "chỗ ở 2–3 sao".
- File: `backend/llm/len_ke_hoach.py`, `backend/llm/sua_lich_v2.py` (chữ câu báo), `backend/api/routes/cong.py` (1 dòng), `frontend/src/LichV2.jsx`, `frontend/src/LenKeHoach.jsx` (1 chuỗi), test.

## Kết quả (mọi dòng [Chạy])
| Tiêu chí | Kết quả |
|---|---|
| T1 — 3.840 khung không mức: không khối, khoá link đúng khi ≥ 2 ngày; 549 khung × 3 mức: khối = hàm chọn nơi ở cho mức đó | đạt (`test_luu_tru_lich.py::test_lodging_block_only_when_the_user_asked`) |
| T2 — chữ `ghep_chu`: chưa hỏi ⇒ 0 dòng "Nơi ở gợi ý"; đã hỏi ⇒ có | đạt |
| T3 — nói bằng lời trên lịch chưa có khối: có hạng ⇒ khối bật đúng hạng + "Đã thêm…"; không hạng ⇒ hỏi lại, lịch không đổi; sửa khác sau đó giữ mức (test sẵn có) | đạt |
| T4 — chuỗi gửi model | không file lời dặn nào đổi so với nhánh gốc; khối nơi ở vốn không vào tin nhắn (test sẵn có giữ) |
| T5 — lịch mẫu có khối theo tổ hợp có hạng | đạt (`test_len_ke_hoach_v2.py`) |
| UI — Playwright 1440, 2 lượt lịch thật 3 ngày | **DAT**: không chọn hạng ⇒ 0 khối, 1 dòng link, bấm mở `#/cho-o`; chọn 4–5 sao ⇒ 1 khối, 5 cơ sở đều 4 / 5 sao, không dòng link; 0 lỗi console, 0 yêu cầu ra ngoài. C đã nhìn ảnh lượt "không hỏi": dòng link nằm dưới "Ghi chú của lịch", trên dòng nguồn |
| Test file chạm | `test_luu_tru_lich.py` 18 đạt (19 s) |
| Test rộng `backend/tests` (không khoá) | 1.087 đạt, 254,6 s; 1 hỏng + 4 lỗi đều là test cần khoá OpenAI đã biết (`test_phase6_settings`, `test_api_chat::test_health…`, `test_openai_full_corpus_generator` ×2, `test_phase6_live_smoke`) |

- 1 test cũ sửa theo luật mới (test luật "buổi tối ⇒ trung tâm" nay đặt mức hạng trước khi dựng khối).
- **Không chạy:** bộ câu đổi hạng / Q3 / Q5 / Q5b (lời dặn + khuôn đầu ra không đổi ⇒ 0 câu chạm model), Golden, đo độ trễ, khổ màn 390 (thay đổi không theo cỡ màn).
- **Tiền:** 0,0012 USD (2 lượt lịch thật của Playwright, đếm theo mã bản `2456c2f`).

## Điều người quyết cần biết
- Nhánh này **đứng trên nhánh bậc 1** — merge bậc 1 trước; nhánh ngày đi (bậc 2) rebase sau.
- Các số cũ "ô nơi ở có ảnh 95,3 %", "lịch có nơi ở" đo khi khối luôn hiện ⇒ thành lịch sử; ghi ở sổ 07 khi merge.
- Chưa làm (đúng plan): câu xin chỗ ở không nêu hạng ⇒ hiện khối mọi hạng; biểu mẫu không tự đồng bộ nút hạng theo lời.
- Câu đo bậc 1 bộ H2 ("rẻ hơn"…) nay ra chữ câu hỏi lại mới — hành vi (không đổi mức, có dòng hỏi lại) giữ nguyên, chỉ chữ đổi.

**Dữ liệu (private):** `data/noi_o_khi_hoi_2026-11-15/` (`tools/pw_noi_o.py`, `ket_qua_pw.json`, ảnh `anh/`).

**Giải thích ngắn:** lịch không còn tự đưa danh sách khách sạn khi người dùng chưa hỏi; chỉ để một dòng link nhỏ. Chọn hạng sao ở biểu mẫu hoặc nói "cho mình khách sạn 4 sao" thì khối chỗ ở mới hiện, đúng hạng đó.
