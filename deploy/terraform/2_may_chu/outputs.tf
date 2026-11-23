output "instance_id" {
  description = "Mã máy — dùng cho lệnh vào máy (Session Manager), dừng, bật ở guide 4 và guide 6."
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "IP tĩnh của máy — giữ nguyên qua mỗi lần dừng / bật."
  value       = aws_eip.app.public_ip
}

output "site_name" {
  description = "Tên trang ghép từ IP tĩnh (dạng 1-2-3-4.sslip.io) — điền vào HUE_SITE ở guide 4 khi không có tên miền riêng, để hộp Caddy xin được chứng chỉ HTTPS."
  value       = "${replace(aws_eip.app.public_ip, ".", "-")}.sslip.io"
}
