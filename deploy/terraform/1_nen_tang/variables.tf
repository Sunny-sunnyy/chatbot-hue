# File này khai báo mọi giá trị đầu vào của tầng nền. Giá trị thật đặt ở `terraform.tfvars`
# (chép từ `terraform.tfvars.example`; file `terraform.tfvars` KHÔNG vào git).

variable "aws_region" {
  description = "Vùng AWS dựng mọi thứ. Phải GIỐNG vùng của thư mục 2_may_chu."
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Tiền tố tên của mọi tài nguyên và giá trị thẻ Project. Để nguyên hue-rag, trừ khi tài khoản đã có tài nguyên trùng tên."
  type        = string
  default     = "hue-rag"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "project_name chỉ gồm chữ thường, số và dấu gạch ngang."
  }
}

variable "alert_email" {
  description = "Email nhận cảnh báo tiền và cảnh báo máy. Dùng địa chỉ đọc hằng ngày; sau khi dựng phải bấm xác nhận trong thư AWS gửi."
  type        = string

  validation {
    condition     = can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.alert_email))
    error_message = "alert_email phải là một địa chỉ email."
  }
}

variable "monthly_budget_usd" {
  description = "Mức ngân sách theo tháng (USD) cho CẢ tài khoản. Chỉ để CẢNH BÁO qua email ở 50 %, 80 %, 100 % — AWS không tự ngắt dịch vụ khi vượt."
  type        = number
  default     = 10

  validation {
    condition     = var.monthly_budget_usd >= 1
    error_message = "monthly_budget_usd phải từ 1 USD trở lên."
  }
}
