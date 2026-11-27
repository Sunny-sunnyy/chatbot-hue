# TẦNG NỀN của bản deploy hue_rag: những thứ gần như không tốn tiền, dựng MỘT lần và để yên —
#   (1) ngân sách + email cảnh báo tiền,
#   (2) chủ đề gửi email cảnh báo (tầng máy chủ gắn báo động "máy hỏng" vào đây),
#   (3) thùng S3 riêng tư chứa gói deploy,
#   (4) vai gắn máy: quyền của máy chủ — CHỈ tải gói và cho mở phiên Session Manager.
# Máy chủ, mạng, địa chỉ IP (thứ bắt đầu tính tiền) nằm ở thư mục 2_may_chu.
# Không có quyền gọi model nào của AWS ở đây: bản deploy gọi model của OpenAI bằng một khoá đặt trên máy (guide 4).

# Mã tài khoản đang đăng nhập — để đặt tên thùng không trùng với ai trên toàn AWS.
data "aws_caller_identity" "current" {}

locals {
  # Thẻ chung, gắn qua `default_tags` ở versions.tf.
  common_tags = {
    Project   = var.project_name
    ManagedBy = "terraform"
  }

  # Tên thùng phải là duy nhất TOÀN CẦU ⇒ ghép thêm mã tài khoản.
  artifact_bucket_name = "${var.project_name}-artifacts-${data.aws_caller_identity.current.account_id}"
}

# ---------------------------------------------------------------------------
# (1) Ngân sách — chỉ CẢNH BÁO, không phải phanh
# ---------------------------------------------------------------------------

# Theo dõi tiền của CẢ tài khoản trong tháng (không lọc theo thẻ: lọc theo thẻ đòi bật "cost allocation tag" bằng tài khoản gốc).
# Email cảnh báo của ngân sách gửi THẲNG tới địa chỉ, không qua chủ đề ở mục (2).
resource "aws_budgets_budget" "monthly" {
  name         = "${var.project_name}-monthly"
  budget_type  = "COST"
  limit_amount = tostring(var.monthly_budget_usd)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  # Tính tiền TRƯỚC khi trừ tín dụng / hoàn tiền: tín dụng không che mất mức dùng thật.
  cost_types {
    include_credit = false
    include_refund = false
  }

  # Ba mốc theo tiền ĐÃ tiêu…
  dynamic "notification" {
    for_each = [50, 80, 100]
    content {
      comparison_operator        = "GREATER_THAN"
      threshold                  = notification.value
      threshold_type             = "PERCENTAGE"
      notification_type          = "ACTUAL"
      subscriber_email_addresses = [var.alert_email]
    }
  }

  # …và một mốc theo tiền AWS DỰ BÁO cho hết tháng (AWS cần vài tuần dữ liệu mới dự báo được).
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }
}

# ---------------------------------------------------------------------------
# (2) Chủ đề gửi email cảnh báo
# ---------------------------------------------------------------------------

resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts"
}

# AWS gửi một thư "Subscription Confirmation" tới địa chỉ này; CHƯA bấm xác nhận thì cảnh báo qua chủ đề không tới.
resource "aws_sns_topic_subscription" "alert_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# Cho phép dịch vụ CloudWatch gửi cảnh báo (báo động máy hỏng ở tầng máy chủ) vào đúng chủ đề này.
resource "aws_sns_topic_policy" "alerts" {
  arn = aws_sns_topic.alerts.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowCloudWatchPublish"
      Effect    = "Allow"
      Principal = { Service = "cloudwatch.amazonaws.com" }
      Action    = "sns:Publish"
      Resource  = aws_sns_topic.alerts.arn
      Condition = {
        StringEquals = {
          "aws:SourceAccount" = data.aws_caller_identity.current.account_id
        }
      }
    }]
  })
}

# ---------------------------------------------------------------------------
# (3) Thùng chứa gói deploy — RIÊNG TƯ
# ---------------------------------------------------------------------------

# Gói (ảnh app nén, bản chụp chỉ mục, file cấu hình) nằm ở s3://<thùng>/<mã commit>/ — guide 2 đẩy lên, guide 4 tải về máy chủ.
# Gói mang file dữ liệu riêng của dự án ⇒ thùng này không bao giờ mở công khai (khác thùng giao diện web của dự án tuần 2).
# Không bật lưu phiên bản: mỗi gói nằm ở một thư mục theo mã commit, không ghi đè; và thùng không lưu phiên bản thì làm rỗng được bằng một lệnh lúc phá.
resource "aws_s3_bucket" "artifacts" {
  bucket = local.artifact_bucket_name
}

# Chặn cả bốn kiểu mở công khai.
resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Mọi file thuộc chủ thùng, không dùng ACL.
resource "aws_s3_bucket_ownership_controls" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Mã hoá lúc lưu bằng khoá do S3 quản lý (không tốn thêm tiền).
resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Tự dọn mảnh upload dở nếu lệnh đẩy gói bị đứt mạng giữa chừng, tránh rò tiền lưu trữ và làm gọn bước phá.
resource "aws_s3_bucket_lifecycle_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    id     = "abort-incomplete-multipart-upload"
    status = "Enabled"

    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 3
    }
  }
}

# ---------------------------------------------------------------------------
# (4) Vai gắn máy (instance role + instance profile)
# ---------------------------------------------------------------------------

# Vai mà máy EC2 được phép nhận. Máy tự xin khoá TẠM của vai này từ AWS — không ai chép khoá AWS nào lên máy.
resource "aws_iam_role" "instance" {
  name = "${var.project_name}-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# Quyền 1: ĐỌC gói trong đúng thùng ở mục (3). Không quyền ghi, không quyền xoá, không thùng nào khác.
resource "aws_iam_role_policy" "read_artifacts" {
  name = "read-artifacts"
  role = aws_iam_role.instance.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ListArtifactBucket"
        Effect   = "Allow"
        Action   = "s3:ListBucket"
        Resource = aws_s3_bucket.artifacts.arn
      },
      {
        Sid      = "ReadArtifacts"
        Effect   = "Allow"
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.artifacts.arn}/*"
      }
    ]
  })
}

# Quyền 2: cho Session Manager mở phiên vào máy (thay SSH — máy không mở cổng 22). Chính sách có sẵn của AWS.
resource "aws_iam_role_policy_attachment" "session_manager" {
  role       = aws_iam_role.instance.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# "Hồ sơ gắn máy": cái vỏ để gắn vai vào một máy EC2. Thư mục 2_may_chu nhận TÊN của nó qua biến `instance_profile_name`.
resource "aws_iam_instance_profile" "instance" {
  name = "${var.project_name}-instance-profile"
  role = aws_iam_role.instance.name
}
