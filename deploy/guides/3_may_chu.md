# Guide 3 — Dựng máy chủ (tầng `2_may_chu`) — TỪ ĐÂY BẮT ĐẦU TÍNH TIỀN

Viết: 19:50 23/11/2026, phiên C. Chưa ai chạy guide này trên AWS: mọi lệnh Terraform ở đây mới qua `terraform fmt` + `terraform validate` ở máy
(không gọi AWS). Dòng nào ghi **[chưa kiểm trên AWS]** là điều chỉ biết chắc khi chủ dự án chạy thật — buổi diễn tập của guide 5 đổi các dòng đó
thành "đã kiểm".

Từ dùng: **tầng** = một thư mục Terraform có state riêng · **state** = file Terraform ghi "đã tạo những gì" · **nhóm bảo mật** (security group) = tường lửa
của máy · **IP tĩnh** (Elastic IP) = địa chỉ công khai không đổi · **vai gắn máy** = quyền AWS gắn thẳng vào máy, máy tự xin khoá tạm · **dịch vụ thông tin
máy** (IMDS) = địa chỉ nội bộ nơi máy hỏi khoá tạm của vai · **Session Manager** = cách mở cửa sổ lệnh vào máy qua AWS, không cần cổng 22 · **hồ sơ**
(profile) = bộ khoá + vùng của AWS CLI đặt tên riêng (tạo ở guide 0).

## 1. Mục tiêu

Sau guide này có MỘT máy ảo đang chạy ở Singapore, có địa chỉ công khai không đổi, vào được bằng Session Manager, đã cài sẵn Docker — nhưng CHƯA
chạy trợ lý Huế (việc đó ở guide 4).

## 2. Sẽ dựng gì

Mười một tài nguyên (mười hai nếu bật báo động), đều mang thẻ `Project = hue-rag`:

| Tài nguyên | Để làm gì | Tính tiền? |
|---|---|---|
| Mạng riêng + một subnet công khai + cổng ra internet + bảng định tuyến + dòng gắn subnet (5) | cho máy một chỗ đứng có đường ra internet | không |
| Nhóm bảo mật + hai luật vào (80, 443) + một luật ra (4) | chỉ để web đi vào hộp Caddy; không mở cổng 22 | không |
| Máy EC2 `t3a.medium` (2 CPU, 4 GB RAM), đĩa 40 GB mã hoá | chạy ba hộp Docker | **có — theo giờ lúc máy bật; đĩa tính cả lúc máy dừng** |
| IP tĩnh | địa chỉ không đổi qua mỗi lần dừng / bật | **có — theo giờ, CẢ LÚC MÁY DỪNG** |
| (tuỳ chọn) một báo động | máy không qua kiểm tra trạng thái 10 phút ⇒ email | gần 0 |

Lúc máy bật lần đầu nó tự chạy một đoạn lệnh (`user_data.sh.tftpl`): tạo vùng nhớ tráo 2 GB, cài Docker + Docker Compose, cài AWS CLI, tạo thư mục
`/srv/hue`. Đoạn đó KHÔNG tải gói và KHÔNG bật app — làm tay ở guide 4 để mỗi bước nhìn thấy được.

**Ba thứ MỚI so với những gì đã học (khoá học chưa có dự án nào dựng máy EC2):**

- **IP tĩnh.** Máy EC2 thường được cấp một địa chỉ công khai MỚI mỗi lần bật. Trang của ta cần một cái tên cố định để xin chứng chỉ HTTPS, nên ta xin
  riêng một địa chỉ và gắn vào máy. Địa chỉ này tính tiền theo giờ kể cả lúc máy dừng — chỉ hết khi phá tầng này.
- **Vai gắn máy + dịch vụ thông tin máy.** Ở dự án `twin` hàm Lambda có một "vai thực thi". Máy EC2 cũng mang một vai như vậy (tạo ở tầng nền): khi lệnh
  `aws` chạy trên máy, nó hỏi một địa chỉ nội bộ của máy để lấy khoá tạm của vai — nên KHÔNG có khoá AWS dài hạn nào nằm trên máy. Ở dự án này vai chỉ
  có hai quyền: tải gói từ thùng và nhận phiên Session Manager. Vai KHÔNG gọi model: model là của OpenAI, khoá OpenAI đặt trong một file ở guide 4.
- **Session Manager.** Không mở cổng 22, không có khoá SSH. Lệnh `aws ssm start-session` mở một cửa sổ lệnh vào máy qua chính AWS; ai được vào do
  quyền của người dùng IAM quyết định.

**Bớt gì so với sổ tay Terraform, vì sao:** sổ tay dựng mạng có subnet riêng, cổng NAT và bộ cân bằng tải đứng trước máy. Ở đây chỉ MỘT subnet công
khai và máy đứng thẳng ra internet sau nhóm bảo mật: chỉ có một máy nên không có gì để cân bằng, và bộ cân bằng tải lẫn cổng NAT đều tính tiền theo giờ
kể cả lúc máy dừng — trái với cách dùng "chỉ bật quanh ngày demo".

**Khác khoá học, vì sao không dùng:**

| Thứ khoá học dùng | Ở đây | Vì sao |
|---|---|---|
| Lambda / App Runner chạy app | một máy EC2 chạy Docker | cuộc trò chuyện, lịch đang xếp, bộ đếm lượt nằm trong bộ nhớ của MỘT tiến trình, và chỉ mục Qdrant nằm trên đĩa — đưa lên Lambda phải sửa lõi |
| Nền tảng agent có sẵn (AgentCore) | không | trợ lý đã chạy trong chính app; thêm một nền tảng là thêm thứ phải giải thích mà không đổi gì người dùng thấy |
| API Gateway + giới hạn tần suất ở cổng | hộp Caddy + trần lượt trong app | một máy một cửa vào; trần lượt mỗi địa chỉ và trần tổng mỗi ngày do app tự đếm |
| S3 + CloudFront cho giao diện | giao diện nằm trong ảnh app | một ảnh một lệnh bật; không có lưu lượng nào cần mạng phân phối |
| Kho ảnh ECR | ảnh nén đặt trong thùng S3 riêng tư | bớt một dịch vụ; ảnh mang file bảng riêng tư (guide 2) |
| WAF, VPC Endpoint, GuardDuty | không | bản demo bật vài giờ; lớp chặn là nhóm bảo mật + trần lượt + số tiền nạp trước ở OpenAI |
| Đăng nhập người dùng | không | sản phẩm không có tài khoản người dùng |
| Aurora | không | không có dữ liệu quan hệ; chỉ mục là Qdrant trong một hộp |
| Secrets Manager | file quyền 600 trên máy | một máy, một khoá; không bí mật nào đi vào state Terraform (guide 4) |

## 3. Điều kiện trước

- Guide 0 xong: có hồ sơ AWS CLI riêng cho việc deploy (các lệnh dưới viết `--profile hue-deploy` — thay bằng tên hồ sơ đã đặt ở guide 0), Terraform
  từ 1.17, phần cắm Session Manager cho AWS CLI.
- Guide 1 xong: tầng nền đã `apply`, email cảnh báo đã bấm xác nhận.
- Guide 2 xong thì tốt (gói đã nằm trong thùng) nhưng không bắt buộc cho guide này — máy dựng xong mà chưa có gói thì chỉ là đang tính tiền mà chưa
  dùng. **Nên làm guide 2 TRƯỚC.**
- Biết trước: từ lệnh `apply` của guide này, mỗi giờ máy bật tốn khoảng 0,047 USD, cộng tiền đĩa và IP (mục 9).

## 4. File liên quan

| File | Việc |
|---|---|
| `deploy/terraform/2_may_chu/versions.tf` | phiên bản Terraform + bộ cắm AWS, vùng, thẻ chung |
| `deploy/terraform/2_may_chu/variables.tf` | bảy biến, mỗi biến một dòng mô tả tiếng Việt |
| `deploy/terraform/2_may_chu/main.tf` | mạng, nhóm bảo mật, máy, IP tĩnh, báo động tuỳ chọn |
| `deploy/terraform/2_may_chu/outputs.tf` | ba đầu ra: `instance_id`, `public_ip`, `site_name` |
| `deploy/terraform/2_may_chu/user_data.sh.tftpl` | đoạn lệnh chạy một lần lúc máy bật lần đầu |
| `deploy/terraform/2_may_chu/terraform.tfvars.example` | mẫu để chép thành `terraform.tfvars` |
| `deploy/terraform/2_may_chu/.terraform.lock.hcl` | ghi đúng bản bộ cắm đã kiểm (6.73.0) — có trong git |

Không vào git (đã chặn ở `.gitignore`): `terraform.tfvars`, `terraform.tfstate*`, thư mục `.terraform/`.

**Khác bài tuần 2 của khoá học ở hai điểm:** bài đó commit `terraform.tfvars` và không commit file khoá phiên bản; ở đây ngược lại — `terraform.tfvars`
của ta có tên thùng gắn mã tài khoản và repo này công khai, còn file khoá phiên bản được commit để lần `init` nào cũng tải đúng một bản bộ cắm.

## 5. Cấu hình

Hai giá trị BẮT BUỘC, lấy từ tầng nền (hai tầng không đọc state của nhau — chép tay, như cách đã làm ở tuần 2 ngày 4):

| Biến | Lấy ở đâu |
|---|---|
| `instance_profile_name` | `terraform output -raw instance_profile_name` trong `1_nen_tang` |
| `artifact_bucket_name` | `terraform output -raw artifact_bucket_name` trong `1_nen_tang` |

Tuỳ chọn (mặc định trong ngoặc): `aws_region` (`ap-southeast-1`) · `project_name` (`hue-rag`) · `instance_type` (`t3a.medium`) · `root_volume_gb` (40) ·
`swap_gb` (2) · `alert_topic_arn` (rỗng = không tạo báo động; muốn có thì điền `terraform output -raw alert_topic_arn` của tầng nền).

**Không đổi `instance_type` sang họ máy ARM** (tên có chữ `g` sau số, ví dụ `t4g.medium`): ảnh app dựng cho `amd64`. Khoá học dạy đúng bẫy này theo
chiều ngược lại — `apply` xanh mà hộp chết lặp. Terraform của ta chặn sẵn: đặt `t4g…` thì `plan` báo lỗi ngay.

## 6. Từng bước

Mỗi khối lệnh ghi rõ ĐANG ĐỨNG Ở THƯ MỤC NÀO — lỗi hay gặp nhất của kiểu nhiều thư mục là `apply` nhầm thư mục.

**Bước 1 — đúng người, đúng vùng.** Hồ sơ mặc định trên máy là người dùng của khoá học, cùng tài khoản: quên `--profile` thì lệnh vẫn chạy một phần
bằng nhầm người.

```bash
aws sts get-caller-identity --profile hue-deploy          # NHÌN dòng "Arn": phải là người dùng IAM mới của việc deploy
aws configure get region --profile hue-deploy             # phải in ap-southeast-1
export AWS_PROFILE=hue-deploy AWS_REGION=ap-southeast-1   # từ đây mọi lệnh aws / terraform trong cửa sổ này dùng hồ sơ đó
```

**Bước 2 — lấy hai cái tên của tầng nền.**

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/1_nen_tang
terraform output -raw instance_profile_name; echo
terraform output -raw artifact_bucket_name; echo
```

**Bước 3 — điền file giá trị của tầng máy chủ.**

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu
cp -n terraform.tfvars.example terraform.tfvars
nano terraform.tfvars        # thay hai dòng DIEN-… bằng hai cái tên vừa in
```

**Bước 4 — chuỗi lệnh sổ tay dạy: `fmt` ⇒ `init` ⇒ `validate` ⇒ `plan`.** Chưa lệnh nào ở bước này tạo gì.

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu
terraform fmt -check          # không in gì = định dạng sạch
terraform init                # tải bộ cắm AWS đúng bản trong .terraform.lock.hcl
terraform validate            # mong: Success! The configuration is valid.
terraform plan -out=may_chu.tfplan
```

ĐỌC bản kế hoạch trước khi đi tiếp. Mong thấy dòng cuối `Plan: 11 to add, 0 to change, 0 to destroy.` (12 nếu đã điền `alert_topic_arn`). Không có dòng
nào "destroy" hay "replace". Thấy số khác ⇒ DỪNG, xem mục 8.

**Bước 5 — `apply`: BẮT ĐẦU TÍNH TIỀN.**

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu
terraform apply may_chu.tfplan
terraform output              # ghi lại ba dòng: instance_id, public_ip, site_name
```

Ở đây KHÔNG dùng `-auto-approve` và không có lệnh `-target` nào (khoá học dùng `-target` để dựng kho ảnh trước; ta giải việc "cái nào trước" bằng hai
thư mục). Lệnh `apply` chạy khoảng một tới hai phút **[chưa kiểm trên AWS]**.

**Bước 6 — chờ máy tự chuẩn bị** (cài Docker…): khoảng ba tới năm phút sau khi `apply` xong **[chưa kiểm trên AWS]**. Không cần gõ gì; sang mục 7.

## 7. Kiểm

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu
ID=$(terraform output -raw instance_id)

# (a) máy đang chạy và qua hai phép kiểm trạng thái của AWS
aws ec2 describe-instance-status --instance-ids "$ID" \
  --query 'InstanceStatuses[0].[InstanceState.Name,SystemStatus.Status,InstanceStatus.Status]' --output text
#     mong: running  ok  ok      (mới bật thì hai chữ sau còn "initializing" — chờ thêm một hai phút)

# (b) Session Manager thấy máy
aws ssm describe-instance-information --filters "Key=InstanceIds,Values=$ID" \
  --query 'InstanceInformationList[0].PingStatus' --output text
#     mong: Online

# (c) vào máy
aws ssm start-session --target "$ID"
```

Trong cửa sổ lệnh của máy (dấu nhắc đổi thành `$` của người dùng `ssm-user`):

```bash
sudo -i                                   # thành root: thư mục /srv/hue và Docker đều của root
cloud-init status --wait                  # mong: status: done   (đang chạy thì lệnh này tự chờ)
cat /var/log/hue-may-chu-san-sang         # mong: một dòng "may chu san sang luc …"
docker --version && docker compose version    # Compose phải từ 2.24
swapon --show                             # mong: /swapfile … 2G
aws --version
cat /srv/hue/may.env                      # mong: HUE_THUNG=<tên thùng> và AWS_DEFAULT_REGION=ap-southeast-1
set -a; . /srv/hue/may.env; set +a        # nạp hai dòng trên thành biến của cửa sổ lệnh này
aws s3 ls "s3://$HUE_THUNG/"              # máy đọc được thùng bằng vai của nó (thùng trống thì không in gì, không báo lỗi)
exit                                      # thoát root
exit                                      # thoát phiên
```

Vì sao `sudo -i`: người dùng `ssm-user` do Session Manager tự tạo ở phiên đầu tiên, nên lúc máy bật lần đầu chưa có ai để giao thư mục; và lệnh Docker
cần quyền root. Mọi lệnh trên máy ở guide 4 và guide 6 đều gõ sau `sudo -i`.

Nếu đã bật báo động: nó chỉ gửi được email sau khi địa chỉ nhận đã bấm xác nhận ở guide 1.

## 8. Gỡ lỗi

| Thấy gì | Xem gì | Làm gì |
|---|---|---|
| `plan` in số tài nguyên khác 11 / 12, hoặc có dòng "destroy" | đang đứng ở thư mục nào (`pwd`); `terraform state list` | đứng nhầm `1_nen_tang` ⇒ quay lại đúng thư mục; state có sẵn tài nguyên ⇒ đã `apply` trước đó, đọc kỹ kế hoạch |
| `AccessDenied` / `UnauthorizedOperation` khi `apply` | tên hành động trong dòng lỗi | người dùng IAM thiếu quyền đó ⇒ bổ sung vào chính sách ở guide 0 rồi `apply` lại (Terraform làm tiếp phần còn dở) |
| `Invalid IAM Instance Profile name` | hai dòng trong `terraform.tfvars` | chép sai tên, hoặc tầng nền dựng ở vùng / tài khoản khác ⇒ lấy lại bằng `terraform output` ở `1_nen_tang` |
| Lỗi "Loại máy này thuộc họ ARM" | `instance_type` | đổi về `t3a.medium` |
| Lỗi "đã tồn tại" (`already exists`) | tài nguyên cùng tên còn sót từ lần dựng trước mà state không biết | xoá tay tài nguyên đó trên trang AWS, hoặc `terraform import`; đừng sửa tay file state |
| `PingStatus` không ra `Online` sau 10 phút | (a) máy có `running ok ok` chưa; (b) vai của tầng nền có chính sách `AmazonSSMManagedInstanceCore` chưa | chưa `ok` ⇒ chờ; thiếu chính sách ⇒ sửa ở tầng nền; vẫn không được ⇒ `aws ec2 get-console-output --instance-id "$ID" --output text \| tail -n 60` xem máy khởi động tới đâu |
| `cloud-init status` ra `error` | `sudo tail -n 80 /var/log/cloud-init-output.log` | thường là một lệnh tải bị rớt mạng ⇒ phá tầng này rồi dựng lại (mục 10) nhanh hơn sửa tay |
| `start-session` báo thiếu `session-manager-plugin` | — | cài phần cắm Session Manager (guide 0) |
| Mất file `terraform.tfstate` của thư mục này | — | Terraform không còn biết đã tạo gì ⇒ phá tay theo thẻ `Project = hue-rag` (guide 7) |

**State nằm ở đâu:** `deploy/terraform/2_may_chu/terraform.tfstate` trên máy chủ dự án (trong WSL). Ở khoá học state để trên S3 vì máy chạy
pipeline là máy tạm; ở đây một người `apply` từ máy mình nên state ở máy. Không xoá, không sửa tay, không chép vào thư mục đồng bộ.

## 9. Ghi chú chi phí

Giá công khai vùng Singapore, phiên B tự mở bảng giá AWS ngày 23/11/2026:

| Trạng thái | Tốn gì | Khoảng bao nhiêu |
|---|---|---|
| Máy BẬT | máy 0,0472 USD / giờ + đĩa + IP | bật liên tục cả tháng: khoảng 41,95 USD; bật 60–100 giờ một tháng: khoảng 10–12 USD |
| Máy DỪNG (guide 6) | đĩa 40 GB + IP tĩnh | khoảng 7,5 USD / tháng |
| Đã phá tầng này | không còn gì của tầng này | 0; còn lại tiền lưu gói ở thùng của tầng nền (vài xu một tháng) |

AWS không có giới hạn cứng tự ngắt dịch vụ: ngân sách của tầng nền chỉ CẢNH BÁO và tới chậm (tới một ngày). Máy không tự dừng — quên tắt là mất
tiền; danh sách cuối buổi ở guide 6 có dòng "tắt máy".

## 10. Dọn dẹp

Phá riêng tầng này (tầng nền và gói trong thùng giữ nguyên; lần sau làm lại guide 3 rồi guide 4):

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu
terraform plan -destroy        # ĐỌC: chỉ được có tài nguyên tên bắt đầu hue-rag-
terraform destroy              # gõ yes
```

Phá tầng này là MẤT: chỉ mục trên đĩa máy (nạp lại được từ gói), chứng chỉ HTTPS (Caddy xin lại), file `hue.env` và `hue.khoa.env` gõ tay trên máy,
và mọi cuộc trò chuyện (mất hẳn). Phá tầng máy chủ TRƯỚC, tầng nền SAU — ở đây thứ tự này là bắt buộc vì máy đang dùng vai của tầng nền. Phá sạch
có kiểm: guide 7.

Muốn máy dùng ảnh hệ điều hành mới hơn hoặc đổi đoạn lệnh lúc bật: cũng là phá rồi dựng lại. Terraform của ta cố ý BỎ QUA thay đổi của ảnh hệ điều hành
(Canonical ra ảnh mới gần như mỗi tuần — không bỏ qua thì một lần `apply` vô tình sẽ thay cả máy).

## 11. Guide kế

`4_bat_lan_dau.md` — tải gói về máy, đặt khoá OpenAI, bật ba hộp, mở trang bằng HTTPS và hỏi một câu thật.
