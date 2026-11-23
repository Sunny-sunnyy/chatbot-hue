# `deploy/` — đưa hue_rag lên AWS

Viết: 20:07 23/11/2026 (giờ `date`), phiên B soạn nháp, phiên điều phối chốt. Trang này cho người mở thư mục lần đầu: bộ này gồm gì, làm theo thứ tự nào, lúc nào bắt
đầu tốn tiền, lùi và phá ở đâu. Cách làm từng bước nằm trong các guide; lý do chọn phương án nằm ở
`docs/superpowers/specs/2026-11-23-deploy-aws-design-ban-3.md`.

**Trạng thái: CHƯA có gì được tạo trên AWS.** Nhóm agent không gọi AWS và không chạy `terraform plan` / `apply`; mọi lệnh tạo, sửa, xoá trên AWS do chủ dự án
gõ theo guide. Phần đã chạy thật là phần chạy được ở máy: gói Docker (dựng ảnh, chạy thử trọn gói, đóng gói) và ba phép kiểm Terraform không cần tài khoản.

## Bản deploy là gì

MỘT máy ảo EC2 ở vùng Singapore chạy ba hộp Docker — cửa vào Caddy (HTTPS), ứng dụng hue_rag, chỉ mục Qdrant — và **chỉ bật quanh ngày demo / ngày chấm**.
Model viết của bản deploy là `gpt-6-luna` của OpenAI, gọi bằng một khoá đặt trong file trên máy chủ; máy chủ không có quyền gọi model nào của AWS.

## Thư mục

| Thư mục | Là gì |
|---|---|
| `docker/` | gói ba hộp + script dựng ảnh, thử ở máy, đóng gói (`docker/README.md`) |
| `terraform/1_nen_tang/` | TẦNG NỀN, gần 0 đồng, dựng một lần: ngân sách + email cảnh báo, thùng S3 chứa gói, vai gắn máy |
| `terraform/2_may_chu/` | TẦNG MÁY CHỦ — thứ tính tiền: mạng nhỏ, nhóm bảo mật 80 / 443, máy, địa chỉ IP tĩnh |
| `guides/` | hướng dẫn từng bước 0 → 7, mỗi guide đủ 11 mục; `guides/hue-rag-deploy-policy.json` là tờ quyền của người dùng deploy |

Hai thư mục Terraform độc lập: mỗi thư mục một file state nằm ngay trong thư mục đó trên máy người chạy; giá trị đi từ tầng nền sang tầng máy chủ bằng cách
chép tay các đầu ra. Không `-target`, không workspace, không `-auto-approve`.

## Thứ tự làm

| # | Guide | Làm xong thì có gì | Tiền |
|---|---|---|---|
| 0 | `guides/0_dieu_kien_truoc.md` | người dùng AWS riêng cho việc deploy + hồ sơ AWS CLI, công cụ trên máy, khoá OpenAI riêng có trần cứng | 0 |
| 1 | `guides/1_nen_tang.md` | tầng nền: cảnh báo tiền, email cảnh báo đã xác nhận, thùng chứa gói, quyền của máy chủ | gần 0 |
| 2 | `guides/2_dong_goi.md` | ảnh dựng từ đúng một commit, đã chạy thử trọn gói ở máy bằng khoá OpenAI, gói nằm trong thùng | vài xu |
| 3 | `guides/3_may_chu.md` | máy chủ + địa chỉ IP, vào được bằng Session Manager | **BẮT ĐẦU TÍNH TIỀN** |
| 4 | `guides/4_bat_lan_dau.md` | ba hộp chạy trên máy, địa chỉ HTTPS mở được, một câu hỏi thật trả lời được | đang tính |
| 5 | `guides/5_kiem_va_go_loi.md` (kèm buổi diễn tập) | danh sách kiểm từ ngoài đã tick; bảng "thấy gì ⇒ xem gì ⇒ làm gì" | — |
| 6 | `guides/6_ngay_demo.md` | dừng tạm, bật lại trước giờ demo, cập nhật bản mới, lùi bản, hai nút khẩn cấp | dừng tạm: còn tiền đĩa + IP |
| 7 | `guides/7_pha_sach.md` | phá có kiểm, không còn tài nguyên nào tính tiền | hết |

Lúc soạn trang này: guide 0, 1 (phiên B) và 2, 3, 4, 6 (phiên C) đã viết; guide 5 và 7 (phiên đo) chưa viết.

## Tiền, lùi, phá — tra nhanh

- **Tiền bắt đầu ở guide 3.** Máy đang bật khoảng 0,06 USD mỗi giờ; máy đã dừng vẫn tốn khoảng 0,25 USD mỗi ngày cho đĩa và địa chỉ IP. Bật 60–100 giờ một
  tháng: khoảng 10–12 USD; để bật liên tục: khoảng 42 USD (bảng tiền: bản thiết kế mục 4).
- **Máy KHÔNG tự dừng.** Cuối mỗi buổi: lệnh dừng máy ở guide 6 (danh sách cuối buổi, mục 6.7). Ngân sách của AWS chỉ gửi email, không ngắt gì, và tới chậm tới một ngày.
- **Dừng tạm ↔ phá:** dừng máy (guide 6 mục 6.1) giữ nguyên đĩa và địa chỉ; phá riêng tầng máy chủ (guide 7) đưa tiền về gần 0 mà vẫn giữ gói và quyền —
  lần sau làm lại guide 3–4.
- **Lùi một bản cập nhật hỏng:** guide 6 mục 6.4 (bước cập nhật giữ sẵn bản trước ngay trên máy để lùi). Lùi code ở máy mình không tự chạy trên máy chủ.
- **Phá sạch:** guide 7 — thứ tự NGƯỢC là bắt buộc: `2_may_chu` trước, làm rỗng thùng, rồi `1_nen_tang`.
- **Dừng, bật lại, cập nhật đều làm MẤT mọi cuộc trò chuyện và lịch đang mở** — chúng nằm trong bộ nhớ của tiến trình ứng dụng.
- **Chốt tiền gọi model:** trần lượt mỗi ngày trong ứng dụng đứng trước; phía OpenAI là trần cứng của project và số tiền nạp trước — cả hai không ngắt tức
  thời (guide 0 Bước 9).

## Thứ CHƯA kiểm được vì chưa chạy trên AWS

Tờ quyền của người dùng deploy có đủ cho cả hai thư mục Terraform không · `plan` / `apply` của cả hai thư mục · thư cảnh báo có tới không · máy có hiện
"Online" ở Session Manager, Docker và vùng nhớ tráo có sẵn sau khi máy bật không · máy tải được gói từ thùng bằng vai gắn máy không · chứng chỉ HTTPS thật ·
chữ chạy dần của model đi qua cửa vào tới trình duyệt · dừng / bật MÁY thật (mới giả lập bằng dừng / bật hộp) · phá thật. Buổi diễn tập ngắn ở guide 5
(dựng hai tầng, bật, hỏi một câu, phá — tiền máy dưới 1 USD) là cách đổi gần hết danh sách này thành "đã kiểm".

## Khái niệm nào đã học ở đâu

| Khái niệm | Đã gặp ở khoá AI Production | Ở hue_rag |
|---|---|---|
| Tài khoản gốc + MFA, người dùng IAM, nhóm quyền | tuần 1 ngày 5, tuần 2, guide 1 của dự án tuần 3 — đã làm | guide 0: thêm MỘT người dùng mới với tờ quyền hẹp |
| Ngân sách + email cảnh báo | tuần 1 ngày 5, tạo bằng tay — đã làm | guide 1: tạo bằng Terraform |
| Terraform: `init` / `plan` / `apply` / `destroy`, biến, đầu ra, tfvars, state | tuần 2 và tuần 3–4 — đã làm | hai thư mục; state ở máy, không lên S3 |
| Thùng S3 | tuần 2, tuần 3–4 — đã làm | thùng RIÊNG TƯ chứa gói |
| Vai cho một dịch vụ | tuần 2: vai của hàm Lambda — đã làm | MỚI: vai gắn MÁY, chỉ để tải gói và vào máy |
| Docker, Dockerfile, ảnh `linux/amd64` | tuần 1 ngày 5, tuần 3 — đã làm | ảnh nén đặt trong thùng, không dùng kho ảnh ECR |
| Máy EC2, mạng, subnet, nhóm bảo mật | sổ tay Terraform — đã HỌC, chưa làm trong dự án nào | guide 3 |
| IP tĩnh · Session Manager · dừng / bật máy · nhiều hộp bằng Docker Compose · Caddy tự xin chứng chỉ | chưa gặp | MỚI — guide 3, 4, 6 giảng từ đầu |
| "Co về 0", "khởi động lạnh" | tuần 2 ngày 1 — đã học | co về 0 BẰNG TAY (dừng máy); bật lại trước giờ demo |
| "Có trạng thái ↔ không trạng thái" | tuần 2 ngày 1, tuần 3 ngày 4 — đã học | lý do chia hai tầng; lý do dừng máy là mất cuộc đang mở |
| OpenAI: nạp trước, hết là ngừng ↔ AWS: chỉ cảnh báo | tuần 1 — đã làm | guide 0 Bước 9, guide 1 mục 9 — ở hue_rag viết đúng là KHÔNG ngừng tức thời (guide 0 Bước 9) |
| Trần chi phí đặt cứng (số lượt chạy cùng lúc = 2) | tuần 1 ngày 5 — đã làm | trần lượt mỗi ngày trong ứng dụng, vượt thì trả lỗi 429 |
