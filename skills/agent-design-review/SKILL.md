---
name: agent-design-review
description: Dùng khi thiết kế, sửa hoặc rà một agent / trợ lý LLM có công cụ — có cần agent không, chia việc code ↔ mô hình, công cụ và tham số, vòng lặp + đường phục hồi, agent con, trí nhớ, lời dặn. Danh sách kiểm theo khoá AI FDE; đầu ra là bảng hiện trạng (file:dòng) · khớp / lệch · đề xuất. Không tự sửa — mỗi sửa là một bậc đo (run-experiment); viết code ⇒ practical-project-coding; bảo mật công cụ ⇒ agent-security-review.
---

# Rà thiết kế agent — hue_rag (dùng từ Phase 9)

Theo khung_fde v1.2 (khung làm dự án theo khoá AI FDE — bản cá nhân của User, private, ngoài repo), đã chỉnh cho hue_rag: điền
đường dẫn; bỏ mọi ví dụ / sự cố của dự án khác (`Session_Prompt.md` §5). W41, User 31/10: chép sẵn cho Phase 9 (agentic RAG / gợi ý).
hue_rag hiện là RAG hỏi đáp, **chưa có agent / công cụ**: chỉ dùng khi thiết kế hoặc rà một agent / trợ lý có công cụ.

Nguồn: khung_fde, nguyên tắc mục 2 (mã bài `W1D2·17` = tuần 1, ngày 2, bài 17 — summary khoá ver4 của User, private). Luật dự án (`session_prompt/Session_Prompt.md`, `AGENTS.md`) thắng skill này khi khác nhau.

## 1. Có cần agent không
- Vấn đề đo được + mốc không agent (luật, script, một lời gọi, quy trình cố định) — skill `propose-options` mục 4b.
- Luồng cố định ⇒ code / quy trình cố định; agent chỉ khi bước tiếp theo phụ thuộc phán đoán (W1D2·17, W2D1·47).
- 3 bẫy: "agent cho X" (nói giải pháp, chưa nói vấn đề); agent theo sơ đồ tổ chức người; đầu ra nghe hợp lý mà không đo (W2D1·46).

## 2. Chia việc code ↔ mô hình
- Bất biến, phép tính, luật tiền, thứ tự bắt buộc ⇒ code / backend; mục tiêu ở lời dặn (W1D5·42–43, W2D1·53, W3D5·119).
- Lời dặn hay câu cố định **hứa một hành động** (chuyển người, gửi, ghi) ⇒ code làm hành động đó.
- Quyết định có giá lỗi cao (tạo đơn, trả tiền) không dựa vào cờ mô hình tự khai; code kiểm điều kiện.
- Mỗi luật / ngưỡng / hằng số một nơi gốc; agent đi theo câu trả lời của nơi đó (W2D3·69, W2D5·82).

## 3. Công cụ
- Tham số chọn phạm vi (khách, phiên, người) do code điền từ ngữ cảnh, mô hình không điền (W1D5·43, W3D5·119).
- Tham số mô hình đi vào URL / đường dẫn / truy vấn ⇒ mã hoá + thử `../`, `/`, `?`, `%2F` (lối lộ dữ liệu hay gặp).
- Lời từ chối của backend trả về như kết quả công cụ để mô hình sửa, không làm agent sập (W1D3·26).
- "Không thấy" ≠ "không tồn tại"; lỗi hạ tầng ≠ kết quả rỗng; kết quả tra cứu kèm nguồn (W3D3·106).
- Công cụ tự viết ⇒ `@tool`; MCP chỉ cho công cụ người khác viết; vài file hướng dẫn ⇒ skill (W2D2·58).
- Không đưa hành động duyệt (ký vượt hạn mức, hoàn tiền) vào danh sách công cụ của mô hình (W1D3·25, W3D2·96).

## 4. Vòng lặp và phục hồi
- Trần lượt gọi mô hình + thời hạn mỗi lời gọi; hết trần ⇒ đường có thật (chuyển người / để lại cho người), không chỉ câu chữ (W1D5·41, 43).
- Tách rõ: xong / để lại cho người / hỏng. Bước có tác dụng thật (ghi đơn, trả tiền) chống chạy lặp — kiểm bản ghi gốc, khoá chống trùng (W2D3·64–65, 68).

## 5. Agent con, trí nhớ, lời dặn
- Một agent trước; agent con chỉ với 1 trong 5 lý do (cô lập ngữ cảnh, kiểm độc lập, rẻ hơn, nhanh hơn, khoanh quyền) + đo thấy hơn (W2D1·46–47).
- Trí nhớ: một loại trước, thêm khi đo thấy lợi; tắt khi đánh giá; namespace do code; không lưu chữ tự do của người dùng (W2D2·61, W3D3·104–106).
- Lời dặn: mục tiêu · có gì để dựa · xong trông thế nào; input gọn; viết lại cả lời dặn thì đo lại (W1D4·33–34, W1D5·42).

## 6. Đầu ra
Bảng: mục · hiện trạng (`file:dòng`) · khớp / lệch · đề xuất. Mỗi sửa đề xuất là **một bậc đo** (skill `run-experiment`), User duyệt trước khi làm. Chưa duyệt thì không sửa code.
