# Bộ khung mang sang dự án mới (làm việc với coding agent)

Soạn 10:20 18/11/2026. Mục đích: dựng một dự án mới (hoặc sắp lại một dự án đang có) để **bất kỳ coding agent nào** làm được theo cùng một cách.
Tất cả [chưa chạy] ở một dự án thứ hai — sửa bộ khung này sau lần chép đầu tiên.

## Chép gì, theo thứ tự nào

| # | Chép | Thành | Phải sửa chỗ nào |
|---|---|---|---|
| 1 | `AGENTS.mau.md` | `AGENTS.md` ở gốc repo (và `CLAUDE.md` một dòng `@AGENTS.md`) | điền luật cứng, lệnh chạy + lệnh kiểm, bảng quyền; giữ < 5 KB |
| 2 | `../CACH_LAM_VIEC.md` | `guides/CACH_LAM_VIEC.md` | chỉ viết lại mục 9 "Ở repo này" (bảng đường dẫn + sở thích của chủ dự án); mục 1–8 và 10 giữ nguyên; chép kèm `../CACH_LAM_VIEC_NGUON.md` (bảng nguồn của mục 10) |
| 3 | `HIEN_TRANG.mau.md` | trang hiện trạng (một trang, viết lại tại chỗ) | toàn bộ nội dung; giữ khuôn mục |
| 4 | `BAO_CAO_4_Y.mau.md` | khuôn báo cáo mỗi việc xong | không cần sửa |
| 5 | `GOI_REVIEW_KHAC_HANG.mau.md` | dùng khi cần người chấm khác hãng | điền bối cảnh + ranh giới của dự án |
| 6 | `VIEC_DANG_MO.mau.md` | mục lục việc (một trang ghi đè, mỗi việc kéo quá một ngày một khối) [đang thử ở repo gốc từ 19/11/2026] | toàn bộ nội dung; giữ khuôn khối |
| 7 | `TONG_HOP_NGAY.mau.md` | `TONG_HOP.md` trong thư mục báo cáo của từng ngày [đang thử ở repo gốc từ 19/11/2026] | điền mỗi ngày; phần đầu là khối "phiên sau" |
| 8 | skill (bảng dưới) | `skills/<tên>/SKILL.md` | theo cột "Mang đi" |

Sau khi chép: bật hook git nếu có (`git config core.hooksPath <thư mục hook>`), rồi mở công cụ và hỏi "bạn đã nạp file hướng dẫn nào, trích dòng đầu" để chắc nó đọc `AGENTS.md`.

## Tổ chức thư mục (bốn loại, đừng trộn)

- **Code + test** — trong git.
- **Dữ liệu riêng** (dữ liệu gốc, bộ câu chấm, kết quả đo chi tiết, khoá) — NGOÀI git, có tên thư mục cố định ghi trong `AGENTS.md`, có hook chặn commit nhầm, có bản sao ngoài máy.
- **Tài liệu cho người** (chủ dự án đọc) — một thư mục riêng, lời thường; chỉ viết việc đã xong.
- **Sổ việc cho agent** — `AGENTS.md` (luật, ngắn) · ba trang GHI ĐÈ đọc lúc mở phiên (trang hiện trạng · mục lục việc · mục đầu sổ riêng của từng phiên) ·
  một thư mục báo cáo cho MỖI NGÀY (báo cáo từng phiên + tổng hợp ngày + nhật ký từng phiên — để tra, không bắt đọc; báo cáo đã đặt vào ngày nào thì không dời) · sổ tay lệnh (runbook).
  Chi tiết + lý do: `../CACH_LAM_VIEC.md` mục 5 "Làm việc theo thư mục từng ngày" [đang thử từ 19/11/2026].

## Phát triển theo cỡ việc

- **Nhỏ** (≤ một hàm, lùi được ngay): làm, test file chạm, một dòng nhật ký.
- **Vừa** (người dùng thấy khác): kế hoạch một trang (file đổi · thứ tự · rủi ro · bằng chứng) ⇒ làm ⇒ một lượt kiểm bởi phiên khác.
- **Lớn** (không lùi được, tiền, dữ liệu, bảo mật — hoặc việc nhiều ngày, nhiều file): chủ dự án nói ý bằng lời thường ⇒ agent hỏi lại tối đa ba câu ⇒ năm dòng đề bài do AGENT soạn, chủ dự án sửa / tick ⇒ kế hoạch ⇒ làm ⇒ review (khác hãng nếu được) ⇒ chủ dự án tự thử.
Chi tiết mức kiểm: `../CACH_LAM_VIEC.md` mục 2.

## Skill nào mang đi được (10 skill của repo gốc, thư mục `skills/`)

| Skill | Mang đi | Lý do một dòng |
|---|---|---|
| `practical-project-coding` | nguyên, bỏ mục "Ranh giới theo khâu pipeline" | luật viết code / test chung: "xong khi" ghi trước, test phải thấy đỏ, sửa lỗi bốn bước |
| `giao-viec-agent-con` | nguyên | khuôn lời giao + cách nhận kết quả — cần ở mọi dự án, mọi công cụ có agent con |
| `soat-tich-hop` | nguyên, đổi hai đường dẫn ví dụ | soát chỗ các tính năng gặp nhau sau đợt gộp + gói review khác hãng + bảng đối chiếu |
| `agent-design-review` | nguyên, sửa dòng hiện trạng | danh sách kiểm khi thiết kế agent có công cụ — chung cho mọi sản phẩm có agent |
| `agent-security-review` | nguyên, sửa dòng hiện trạng | danh sách kiểm bảo mật agent + mục 7b thử chốt chặn của chính coding agent bằng file giả |
| `propose-options` | sửa nhẹ | khuôn đưa lựa chọn cho chủ dự án là chung; đổi tên dự án + đường dẫn tài liệu thiết kế |
| `teach-and-quiz` | sửa nhẹ | cách giảng + hỏi lại là chung; đổi đường dẫn sổ học và thư mục tài liệu cho người |
| `risk-gated-agent-review` | sửa nhẹ | cổng tối thiểu + bảng kiểm theo tác động là chung; đổi đường dẫn mẫu report; làm một mình: người kiểm = phiên mới ngữ cảnh sạch |
| `run-experiment` | phải sửa | khung "tiêu chí ghi trước, mốc, đổi một thứ, luật giữ / gỡ" là chung; bộ câu, thủ tục bộ an toàn, tên báo cáo khâu là của một hệ RAG |
| `improve-workflow` | sửa nhẹ | nhịp cuối ngày ba bước + nấc "máy trước chữ sau" là chung; đổi tên sổ cải tiến và các file luật |

Bảng này lập sau khi **đọc trọn 8 skill cũ (đã sửa) và viết 2 skill mới** (18/11/2026); chưa skill nào được chép thử sang một dự án thứ hai [chưa chạy]. Công cụ khác Claude Code tìm skill ở thư mục
`.agents/skills` (theo tài liệu công khai, chưa thử) ⇒ ở dự án mới đặt skill vào đó hoặc tạo liên kết.
