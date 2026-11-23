variable "aws_region" {
  description = "Vùng AWS dựng máy. Phải TRÙNG vùng của tầng nền (thùng chứa gói nằm ở đó)."
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Tiền tố tên mọi tài nguyên và giá trị thẻ Project. Phải TRÙNG với tầng nền."
  type        = string
  default     = "hue-rag"
}

variable "instance_type" {
  description = "Loại máy EC2. Mặc định t3a.medium (2 CPU, 4 GB RAM): app đo được khoảng 0,9 GB + Qdrant 0,2 GB. KHÔNG chọn họ máy ARM (tên có chữ g sau số, ví dụ t4g): ảnh app dựng cho amd64."
  type        = string
  default     = "t3a.medium"

  validation {
    condition     = !can(regex("^[a-z]+[0-9]+g", var.instance_type))
    error_message = "Loại máy này thuộc họ ARM (chữ g sau số, ví dụ t4g.medium). Ảnh app dựng cho linux/amd64 nên hộp sẽ không chạy được — chọn họ x86 như t3a hoặc t3."
  }
}

variable "root_volume_gb" {
  description = "Dung lượng đĩa gốc (GB). 40 GB đủ cho hệ điều hành, ảnh app khoảng 3,6 GB cả lúc còn file nén, chỉ mục và vùng nhớ tráo."
  type        = number
  default     = 40

  validation {
    condition     = var.root_volume_gb >= 30
    error_message = "Đĩa dưới 30 GB không đủ chỗ: lúc nạp ảnh app trên máy cùng lúc có file nén và ảnh đã giải nén."
  }
}

variable "swap_gb" {
  description = "Dung lượng vùng nhớ tráo (swap) tạo lúc máy bật lần đầu, tính bằng GB. Máy 4 GB không có swap thì hộp app có thể bị giết khi thiếu RAM — mất mọi cuộc trò chuyện đang mở. Đặt 0 để không tạo."
  type        = number
  default     = 2

  validation {
    condition     = var.swap_gb >= 0 && var.swap_gb <= 8 && floor(var.swap_gb) == var.swap_gb
    error_message = "swap_gb là số nguyên từ 0 tới 8."
  }
}

variable "instance_profile_name" {
  description = "Tên hồ sơ gắn máy do tầng nền tạo — lấy bằng `terraform output -raw instance_profile_name` trong thư mục 1_nen_tang. Cho máy quyền tải gói từ thùng và nhận phiên Session Manager; KHÔNG có quyền gọi model."
  type        = string

  validation {
    condition     = !startswith(var.instance_profile_name, "DIEN-")
    error_message = "instance_profile_name còn là chữ mẫu DIEN-… của terraform.tfvars.example. Thay bằng giá trị in ra ở guide 3 bước 2: terraform output -raw instance_profile_name (thư mục 1_nen_tang)."
  }
}

variable "artifact_bucket_name" {
  description = "Tên thùng S3 chứa gói do tầng nền tạo — lấy bằng `terraform output -raw artifact_bucket_name` trong thư mục 1_nen_tang. Terraform chỉ ghi tên này vào một file trên máy để lệnh tải gói ở guide 4 khỏi gõ lại."
  type        = string

  validation {
    condition     = !startswith(var.artifact_bucket_name, "DIEN-")
    error_message = "artifact_bucket_name còn là chữ mẫu DIEN-… của terraform.tfvars.example. Thay bằng giá trị in ra ở guide 3 bước 2: terraform output -raw artifact_bucket_name (thư mục 1_nen_tang). Tên này chỉ được ghi vào máy một lần lúc máy bật lần đầu — sai thì phải thay máy."
  }
}

variable "alert_topic_arn" {
  description = "ARN chủ đề email cảnh báo của tầng nền. Có giá trị thì tạo MỘT báo động: máy không qua kiểm tra trạng thái ⇒ gửi email. Để chuỗi rỗng thì không tạo báo động."
  type        = string
  default     = ""

  validation {
    condition     = !startswith(var.alert_topic_arn, "DIEN-")
    error_message = "alert_topic_arn còn là chữ mẫu DIEN-… của terraform.tfvars.example. Thay bằng giá trị in ra ở guide 3 bước 2: terraform output -raw alert_topic_arn (thư mục 1_nen_tang), hoặc để chuỗi rỗng nếu không muốn báo động máy hỏng."
  }
}
