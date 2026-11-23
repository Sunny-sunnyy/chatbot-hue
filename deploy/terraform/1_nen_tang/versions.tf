# File này ghim bản Terraform và bản bộ cắm AWS (provider), và khai báo vùng + thẻ chung.
# Bản CHÍNH XÁC của bộ cắm được ghi trong `.terraform.lock.hcl` (file đó ĐƯỢC commit) — máy nào chạy `terraform init` cũng tải đúng bản ấy.
terraform {
  # Từ 1.17 trở lên, dưới 2.0 (bản dùng lúc viết: 1.17.2). Chuỗi này GIỐNG thư mục 2_may_chu.
  required_version = ">= 1.17.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.73"
    }
  }

  # KHÔNG có khối `backend`: state nằm ngay trong thư mục này trên máy người chạy (một người, một môi trường).
  # Khoá học để state trên S3 vì máy chạy pipeline là máy tạm; ở đây không có pipeline. Mất file state: xem deploy/guides/1_nen_tang.md, mục Gỡ lỗi.
}

provider "aws" {
  # Khoá lấy từ hồ sơ AWS CLI đang chọn (biến môi trường AWS_PROFILE — guide 0); file này không chứa khoá nào.
  region = var.aws_region

  # Mọi tài nguyên của thư mục này tự mang hai thẻ dưới đây — guide 7 tìm tài nguyên sót theo thẻ `Project`.
  default_tags {
    tags = local.common_tags
  }
}
