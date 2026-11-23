# Tầng MÁY CHỦ (`2_may_chu`) — thứ BẮT ĐẦU TÍNH TIỀN: mạng nhỏ + nhóm bảo mật + một máy EC2 + IP tĩnh.
# Dựng SAU tầng nền (`../1_nen_tang`): tầng này dùng hai cái tên tầng nền in ra (thùng chứa gói, hồ sơ gắn máy),
# chép tay vào `terraform.tfvars` — hai tầng KHÔNG đọc state của nhau.
# Hướng dẫn từng bước: deploy/guides/3_may_chu.md.

terraform {
  required_version = ">= 1.17.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.73"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # Mọi tài nguyên của tầng này tự mang hai thẻ chung ⇒ guide 7 (phá sạch) tìm tài nguyên sót theo thẻ `Project`.
  default_tags {
    tags = local.common_tags
  }
}
