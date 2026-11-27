locals {
  name_prefix = var.project_name

  common_tags = {
    Project   = var.project_name
    ManagedBy = "terraform"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# Dữ liệu tra từ AWS (không tạo gì)
# ---------------------------------------------------------------------------------------------------------------------

# Mã tài khoản đang đăng nhập — để gắn điều kiện aws:SourceAccount cho vai của lịch tự dừng máy.
data "aws_caller_identity" "current" {}

# Vùng sẵn có của vùng AWS đang chọn — lấy bằng khối data như sổ tay Terraform, không ghi cứng "a / b".
data "aws_availability_zones" "available" {
  state = "available"
}

# Ảnh hệ điều hành: Ubuntu 24.04 (noble) bản CHUẨN cho máy chủ của Canonical — như sổ tay Terraform (sổ tay dùng 22.04).
# Không dùng bản "minimal": bản đó không cài sẵn phần mềm Session Manager, mà Session Manager là đường DUY NHẤT vào máy này.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# Mạng nhỏ: một mạng riêng, MỘT subnet công khai, cổng ra internet. Bớt so với sổ tay: không subnet riêng, không NAT,
# không cân bằng tải — chỉ có một máy, và cân bằng tải tính tiền theo giờ kể cả lúc máy dừng.
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = { Name = "${local.name_prefix}-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = { Name = "${local.name_prefix}-subnet-cong-khai" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "${local.name_prefix}-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = { Name = "${local.name_prefix}-rt-cong-khai" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ---------------------------------------------------------------------------------------------------------------------
# Nhóm bảo mật: chỉ mở 80 và 443 (hộp Caddy). KHÔNG mở cổng 22 — vào máy bằng Session Manager.
# Cổng của app (8000) và của Qdrant (6333) không mở ra ngoài: hai hộp đó chỉ nói chuyện trong mạng riêng của Docker.
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_security_group" "web" {
  name        = "${local.name_prefix}-web"
  description = "hue-rag: chi mo 80 va 443 cho hop Caddy; khong mo cong 22"
  vpc_id      = aws_vpc.main.id

  tags = { Name = "${local.name_prefix}-web" }
}

resource "aws_vpc_security_group_ingress_rule" "web" {
  for_each = toset(["80", "443"])

  security_group_id = aws_security_group.web.id
  description       = "Web vao hop Caddy, cong ${each.value}"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = tonumber(each.value)
  to_port           = tonumber(each.value)
}

# Ra ngoài tự do: máy cần tải Docker, hai ảnh Qdrant + Caddy, gói từ thùng S3, gọi API của OpenAI, xin chứng chỉ HTTPS.
resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.web.id
  description       = "Ra ngoai tu do"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# ---------------------------------------------------------------------------------------------------------------------
# Máy chủ
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_instance" "app" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web.id]
  associate_public_ip_address = true # có mạng ngay lúc bật lần đầu (cài Docker) — trước khi IP tĩnh được gắn

  # VAI GẮN MÁY (tạo ở tầng nền): máy tự xin khoá tạm để tải gói từ thùng và nhận phiên Session Manager.
  # Không có khoá AWS dài hạn nào nằm trên máy.
  iam_instance_profile = var.instance_profile_name

  # Dịch vụ thông tin máy (nơi máy lấy khoá tạm của vai): bắt buộc kiểu có mã phiên (IMDSv2), bước nhảy 1 ⇒ các hộp
  # Docker KHÔNG tới được dịch vụ này; chỉ lệnh chạy thẳng trên máy (AWS CLI tải gói) mới lấy được khoá tạm.
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_gb
    encrypted             = true
    delete_on_termination = true

    tags = merge(local.common_tags, { Name = "${local.name_prefix}-dia-goc" })
  }

  # Máy họ t: kiểu "standard" = hết điểm CPU thì máy chậm lại chứ KHÔNG tính thêm tiền (kiểu "unlimited" thì có).
  credit_specification {
    cpu_credits = "standard"
  }

  # Chạy MỘT lần lúc máy bật lần đầu: vùng nhớ tráo, Docker + Compose, AWS CLI, thư mục /srv/hue.
  # KHÔNG tải gói, KHÔNG bật app — hai việc đó làm tay ở guide 4 để mỗi bước nhìn thấy được.
  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    swap_gb              = var.swap_gb
    artifact_bucket_name = var.artifact_bucket_name
    aws_region           = var.aws_region
  })

  # Ba thuộc tính dưới đây mà đổi thì Terraform sẽ đòi THAY MÁY (mất chỉ mục, chứng chỉ, mọi thứ trên đĩa):
  # - `ami`: Canonical ra ảnh mới gần như mỗi tuần ⇒ lần `plan` sau sẽ thấy ảnh "mới nhất" khác ảnh máy đang chạy;
  # - `user_data`: chỉ có nghĩa ở lần bật đầu tiên;
  # - `associate_public_ip_address`: AWS tự đổi giá trị này khi IP tĩnh được gắn / máy dừng rồi bật.
  # Muốn máy dùng ảnh hoặc đoạn lệnh mới: phá tầng này rồi dựng lại (guide 6), không sửa tại chỗ.
  lifecycle {
    ignore_changes = [ami, user_data, associate_public_ip_address]
  }

  tags = { Name = "${local.name_prefix}-may-chu" }

  depends_on = [
    aws_route_table_association.public,
    aws_vpc_security_group_egress_rule.all,
  ]
}

# IP TĨNH: địa chỉ công khai giữ nguyên qua mỗi lần dừng / bật máy (IP tự cấp thì đổi mỗi lần bật) ⇒ tên trang và
# chứng chỉ HTTPS không phải làm lại. Lưu ý tiền: IP tĩnh tính tiền theo giờ CẢ LÚC MÁY DỪNG; chỉ hết khi phá tầng này.
resource "aws_eip" "app" {
  domain   = "vpc"
  instance = aws_instance.app.id

  tags = { Name = "${local.name_prefix}-ip-tinh" }

  depends_on = [aws_internet_gateway.main]
}

# ---------------------------------------------------------------------------------------------------------------------
# (Tuỳ chọn) MỘT báo động: máy không qua kiểm tra trạng thái của AWS trong 10 phút ⇒ email qua chủ đề cảnh báo của
# tầng nền. Máy đang DỪNG thì không có số đo ⇒ coi là bình thường, không báo. Chỉ tạo khi `alert_topic_arn` có giá trị.
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_cloudwatch_metric_alarm" "status_check" {
  count = var.alert_topic_arn == "" ? 0 : 1

  alarm_name          = "${local.name_prefix}-may-khong-qua-kiem-tra-trang-thai"
  alarm_description   = "hue-rag: may chu khong qua kiem tra trang thai cua AWS trong 10 phut"
  namespace           = "AWS/EC2"
  metric_name         = "StatusCheckFailed"
  statistic           = "Maximum"
  period              = 300
  evaluation_periods  = 2
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"

  dimensions = {
    InstanceId = aws_instance.app.id
  }

  alarm_actions = [var.alert_topic_arn]
}

# ---------------------------------------------------------------------------------------------------------------------
# (Tuỳ chọn, bật mặc định) Lịch tự dừng máy ban đêm bằng EventBridge Scheduler — 0 đồng trong mức miễn phí.
# Tránh rủi ro quên tắt máy sau demo (~41,95 USD/tháng nếu bật liên tục). Máy đang dừng thì lệnh stop giữ nguyên trạng thái.
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role" "scheduler" {
  count = var.auto_stop_enabled ? 1 : 0

  name = "${local.name_prefix}-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "scheduler.amazonaws.com" }
      Condition = {
        StringEquals = {
          "aws:SourceAccount" = data.aws_caller_identity.current.account_id
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "scheduler_stop_ec2" {
  count = var.auto_stop_enabled ? 1 : 0

  name = "stop-ec2-instance"
  role = aws_iam_role.scheduler[0].name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "StopOnlyHueRagAppInstance"
      Effect   = "Allow"
      Action   = "ec2:StopInstances"
      Resource = aws_instance.app.arn
    }]
  })
}

resource "aws_scheduler_schedule" "auto_stop" {
  count = var.auto_stop_enabled ? 1 : 0

  name                         = "${local.name_prefix}-tu-dung-dem"
  group_name                   = "default"
  description                  = "hue-rag: tu dung may EC2 moi dem luc 23:30 gio Viet Nam"
  schedule_expression          = var.auto_stop_schedule
  schedule_expression_timezone = "Asia/Ho_Chi_Minh"
  state                        = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:ec2:stopInstances"
    role_arn = aws_iam_role.scheduler[0].arn

    input = jsonencode({
      InstanceIds = [aws_instance.app.id]
    })
  }
}
