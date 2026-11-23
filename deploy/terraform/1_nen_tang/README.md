# `1_nen_tang` — tầng nền của bản deploy hue_rag

Viết: 19:50 23/11/2026 (giờ `date`), phiên B. Hướng dẫn từng bước: `deploy/guides/1_nen_tang.md` — đọc guide đó để chạy; trang này chỉ là bản tóm tắt cho người mở thư mục.

Dựng 11 tài nguyên gần như không tốn tiền, một lần rồi để yên: ngân sách tháng + email cảnh báo tiền · chủ đề gửi email cảnh báo · thùng S3 riêng tư chứa
gói deploy · vai gắn máy (chỉ đọc thùng đó + Session Manager). Máy chủ, mạng, địa chỉ IP ở thư mục `../2_may_chu`.

| Đầu vào (`terraform.tfvars`) | Mặc định |
|---|---|
| `alert_email` | phải điền |
| `monthly_budget_usd` | 10 |
| `aws_region` | `ap-southeast-1` |
| `project_name` | `hue-rag` (để nguyên — chính sách quyền `deploy/guides/hue-rag-deploy-policy.json` viết theo tiền tố này) |

| Đầu ra | Ai dùng |
|---|---|
| `artifact_bucket_name` | `2_may_chu` (biến cùng tên) · guide 2, 4 |
| `instance_profile_name` | `2_may_chu` (biến cùng tên) |
| `instance_role_name` | xem quyền máy chủ khi gỡ lỗi |
| `alert_topic_arn` | `2_may_chu` (biến cùng tên; để rỗng thì không tạo báo động máy hỏng) |

Luật của thư mục: chạy bằng hồ sơ AWS CLI `hue-rag-deploy` · luôn `terraform plan` rồi mới `terraform apply`, không `-auto-approve`, không `-target`, không workspace ·
state nằm ngay trong thư mục này trên máy người chạy, không vào git · `terraform.tfvars` không vào git, `.terraform.lock.hcl` có vào git.

Đã kiểm ở máy, không gọi AWS: `terraform fmt -check` · `terraform init -backend=false` · `terraform validate`. CHƯA chạy `plan` / `apply` trên tài khoản thật.
