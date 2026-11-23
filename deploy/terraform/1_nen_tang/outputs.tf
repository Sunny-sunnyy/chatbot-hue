# Giá trị in ra sau `terraform apply`. Hai giá trị đầu chép TAY sang `terraform.tfvars` của thư mục 2_may_chu
# (hai thư mục không đọc state của nhau); tên thùng còn dùng ở guide 2 (đẩy gói) và guide 4 (tải gói).

output "artifact_bucket_name" {
  description = "Tên thùng S3 chứa gói deploy."
  value       = aws_s3_bucket.artifacts.bucket
}

output "instance_profile_name" {
  description = "Tên hồ sơ gắn máy — điền vào biến instance_profile_name của 2_may_chu."
  value       = aws_iam_instance_profile.instance.name
}

output "instance_role_name" {
  description = "Tên vai gắn máy (để xem quyền của máy chủ khi gỡ lỗi)."
  value       = aws_iam_role.instance.name
}

output "alert_topic_arn" {
  description = "ARN của chủ đề gửi email cảnh báo — điền vào 2_may_chu nếu thư mục đó gắn báo động máy hỏng."
  value       = aws_sns_topic.alerts.arn
}
