# Bộ khung mang sang dự án mới (làm việc với coding agent)

Soạn 10:20 18/11/2026. Mục đích: dựng một dự án mới (hoặc sắp lại một dự án đang có) để **bất kỳ coding agent nào** làm được theo cùng một cách.
Tất cả [chưa chạy] ở một dự án thứ hai — sửa bộ khung này sau lần chép đầu tiên.

## Chép gì, theo thứ tự nào

| # | Chép | Thành | Phải sửa chỗ nào |
|---|---|---|---|
| 1 | `AGENTS.mau.md` | `AGENTS.md` ở gốc repo (và `CLAUDE.md` một dòng `@AGENTS.md`) | điền luật cứng, lệnh chạy + lệnh kiểm, bảng quyền; giữ < 4 KB |
| 2 | `../CACH_LAM_VIEC.md` | `guides/CACH_LAM_VIEC.md` | chỉ viết lại mục 9 "Ở repo này" (bảng đường dẫn + sở thích của chủ dự án); mục 1–8 và 10 giữ nguyên |
| 3 | `HIEN_TRANG.mau.md` | trang hiện trạng (một trang, viết lại tại chỗ) | toàn bộ nội dung; giữ khuôn mục |
| 4 | `BAO_CAO_4_Y.mau.md` | khuôn báo cáo mỗi việc xong | không cần sửa |
| 5 | `GOI_REVIEW_KHAC_HANG.mau.md` | dùng khi cần người chấm khác hãng | điền bối cảnh + ranh giới của dự án |
| 6 | skill (bảng dưới) | `skills/<tên>/SKILL.md` | theo cột "Mang đi" |

Sau khi chép: bật hook git nếu có (`git config core.hooksPath <thư mục hook>`), rồi mở công cụ và hỏi "bạn đã nạp file hướng dẫn nào, trích dòng đầu" để chắc nó đọc `AGENTS.md`.

## Tổ chức thư mục (bốn loại, đừng trộn)

- **Code + test** — trong git.
- **Dữ liệu riêng** (dữ liệu gốc, bộ câu chấm, kết quả đo chi tiết, khoá) — NGOÀI git, có tên thư mục cố định ghi trong `AGENTS.md`, có hook chặn commit nhầm, có bản sao ngoài máy.
- **Tài liệu cho người** (chủ dự án đọc) — một thư mục riêng, lời thường; chỉ viết việc đã xong.
- **Sổ việc cho agent** — `AGENTS.md` (luật, ngắn) · một trang hiện trạng viết lại tại chỗ · nhật ký nối đuôi (để tra, không bắt đọc) · sổ tay lệnh (runbook).

## Phát triển theo cỡ việc

- **Nhỏ** (≤ một hàm, lùi được ngay): làm, test file chạm, một dòng nhật ký.
- **Vừa** (người dùng thấy khác): kế hoạch một trang (file đổi · thứ tự · rủi ro · bằng chứng) ⇒ làm ⇒ một lượt kiểm bởi phiên khác.
- **Lớn** (không lùi được, tiền, dữ liệu, bảo mật — hoặc việc nhiều ngày, nhiều file): chủ dự án nói ý bằng lời thường ⇒ agent hỏi lại tối đa ba câu ⇒ năm dòng đề bài do AGENT soạn, chủ dự án sửa / tick ⇒ kế hoạch ⇒ làm ⇒ review (khác hãng nếu được) ⇒ chủ dự án tự thử.
Chi tiết mức kiểm: `../CACH_LAM_VIEC.md` mục 2.

## Skill nào mang đi được (8 skill của repo gốc, thư mục `skills/`)

| Skill | Mang đi | Lý do một dòng |
|---|---|---|
| `practical-project-coding` | nguyên | luật viết code / test chung, không gắn dự án |
| `agent-design-review` | nguyên, sửa dòng hiện trạng | danh sách kiểm khi thiết kế agent có công cụ — chung cho mọi sản phẩm có agent |
| `agent-security-review` | nguyên, sửa dòng hiện trạng | danh sách kiểm bảo mật agent — chung |
| `propose-options` | sửa nhẹ | khuôn đưa lựa chọn cho chủ dự án là chung; đổi tên dự án + ví dụ |
| `teach-and-quiz` | sửa nhẹ | cách giảng + hỏi lại là chung; đổi đường dẫn sổ học |
| `run-experiment` | phải sửa | khung "tiêu chí ghi trước, mốc, đổi một thứ" là chung; danh sách khâu + bộ đo là của một hệ RAG |
| `risk-gated-agent-review` | phải sửa | viết cho mô hình nhiều phiên có phiên điều phối; làm một mình thì rút còn phần đối chiếu diff ↔ tiêu chí |
| `improve-workflow` | chỉ repo gốc | gắn chặt sổ cải tiến + vai điều phối của repo gốc; dự án mới dùng mục 5 + 7 của trang cách làm việc |

Bảng này lập từ phần đầu + số dòng nhắc tên dự án của mỗi skill, **chưa đọc trọn từng skill**. Công cụ khác Claude Code tìm skill ở thư mục `.agents/skills` (theo tài liệu
công khai, chưa thử) ⇒ ở dự án mới đặt skill vào đó hoặc tạo liên kết.
