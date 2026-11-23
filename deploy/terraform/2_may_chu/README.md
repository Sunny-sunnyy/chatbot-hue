# `2_may_chu` — tầng MÁY CHỦ (thứ bắt đầu tính tiền)

Một mạng nhỏ, một nhóm bảo mật chỉ mở 80 / 443, một máy EC2 chạy Docker, một IP tĩnh, và (tuỳ chọn) một báo động trạng thái máy.
Dựng SAU tầng nền `../1_nen_tang`; phá TRƯỚC tầng nền. Hướng dẫn từng bước: `deploy/guides/3_may_chu.md`.

| File | Việc |
|---|---|
| `versions.tf` | phiên bản Terraform (từ 1.17) + bộ cắm AWS (`~> 6.73`), vùng, hai thẻ chung `Project`, `ManagedBy` |
| `variables.tf` | `aws_region` · `project_name` · `instance_type` · `root_volume_gb` · `swap_gb` · `instance_profile_name` · `artifact_bucket_name` · `alert_topic_arn` |
| `main.tf` | mạng, nhóm bảo mật, máy, IP tĩnh, báo động |
| `outputs.tf` | `instance_id` · `public_ip` · `site_name` |
| `user_data.sh.tftpl` | chạy một lần lúc máy bật lần đầu: vùng nhớ tráo, Docker + Compose, AWS CLI, thư mục `/srv/hue` — không tải gói, không bật app |
| `terraform.tfvars.example` | mẫu; chép thành `terraform.tfvars` (không vào git) rồi điền hai tên lấy từ đầu ra của tầng nền |
| `.terraform.lock.hcl` | bản bộ cắm đã kiểm — có trong git |

Hai tầng không đọc state của nhau: `instance_profile_name`, `artifact_bucket_name` (và `alert_topic_arn` nếu muốn báo động) chép tay từ
`terraform output` của `1_nen_tang`.

Đã kiểm ở máy, không gọi AWS (23/11/2026, Terraform 1.17.2, bộ cắm AWS 6.73.0): `terraform fmt -check` sạch · `terraform init -backend=false` ·
`terraform validate` ⇒ "Success! The configuration is valid." · đoạn lệnh lúc máy bật, sau khi Terraform điền giá trị mẫu, qua `bash -n`.
CHƯA kiểm (chỉ biết khi chủ dự án `apply`): ảnh Ubuntu tìm được theo bộ lọc tên · máy có hiện "Online" ở Session Manager · Docker, AWS CLI cài xong ·
vai gắn máy tải được gói · báo động gửi được email.

Nhóm KHÔNG chạy `plan` / `apply` / `destroy` ở thư mục này; chủ dự án gõ mọi lệnh tạo và xoá.
