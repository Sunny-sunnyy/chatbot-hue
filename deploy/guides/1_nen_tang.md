# Guide 1 — Tầng nền: ngân sách + email cảnh báo, thùng chứa gói, vai gắn máy

Viết: 19:50 23/11/2026 (giờ `date`), phiên B. Người gõ lệnh: chủ dự án. Guide trước: `0_dieu_kien_truoc.md`. Guide kế: `2_dong_goi.md`.

**Trạng thái của guide này:** thư mục Terraform `deploy/terraform/1_nen_tang/` đã qua ba phép kiểm chạy được ở máy không cần AWS — `terraform fmt -check`,
`terraform init -backend=false`, `terraform validate` ("Success", bộ cắm AWS 6.73.0) **[máy]**. CHƯA ai chạy `plan` / `apply` trên tài khoản thật: nhóm không
gọi AWS. Vì vậy mọi "kết quả phải thấy" của lệnh `terraform plan`, `apply`, `aws …` dưới đây ghi theo cách file được viết và mang nhãn **[chưa chạy]**.

Từ dùng: **tầng nền** = nhóm tài nguyên gần như không tốn tiền, dựng một lần rồi để yên · **tầng máy chủ** = máy, mạng, địa chỉ IP — thứ tính tiền, ở guide 3 ·
**ngân sách** (budget) = một mức tiền theo tháng để AWS gửi email khi tiền thật chạm các mốc của mức đó · **chủ đề** (SNS topic) = một "đầu mối gửi thư":
dịch vụ nào đăng tin lên chủ đề thì mọi email đã đăng ký đều nhận · **thùng** (S3 bucket) = nơi cất file trên AWS · **gói** = bộ file máy chủ cần để chạy
hue_rag (guide 2 tạo) · **vai gắn máy** (instance role) = quyền AWS gắn thẳng vào máy chủ; máy tự xin khoá tạm của vai, không ai chép khoá AWS lên máy ·
**hồ sơ gắn máy** (instance profile) = cái vỏ AWS dùng để gắn một vai vào một máy · **state** = file Terraform ghi lại "tôi đã tạo những gì" ·
**đầu ra** (output) = giá trị Terraform in ra sau khi dựng.

Nhãn nguồn: **[AWS]** = phiên B tự mở trang tài liệu AWS ngày 23/11/2026 · **[khoá]** = theo bài của khoá AI Production · **[máy]** = đã chạy trên máy này ·
**[chưa chạy]** = chưa làm thật trên tài khoản.

## 1. Mục tiêu

Dựng bằng Terraform bốn thứ mà tầng máy chủ và các guide sau cần, với chi phí gần 0: lưới cảnh báo tiền, đầu mối email cảnh báo, chỗ cất gói, và quyền của
máy chủ. Sau guide này vẫn chưa có máy nào chạy.

## 2. Sẽ dựng gì

11 tài nguyên, tên đều bắt đầu bằng `hue-rag-` và mang hai thẻ `Project = hue-rag`, `ManagedBy = terraform`:

| Nhóm | Tài nguyên | Tên | Để làm gì |
|---|---|---|---|
| Ngân sách | 1 ngân sách tháng | `hue-rag-monthly` | gửi email khi tiền ĐÃ tiêu của cả tài khoản chạm 50 %, 80 %, 100 % mức đặt, và khi AWS DỰ BÁO cả tháng vượt mức |
| Email cảnh báo | 1 chủ đề + 1 đăng ký email | `hue-rag-alerts` | đầu mối cho báo động "máy hỏng" của tầng máy chủ (guide 3, 5) |
| Thùng chứa gói | 1 thùng + 3 thiết lập (chặn mở công khai · mọi file thuộc chủ thùng · mã hoá lúc lưu) | `hue-rag-artifacts-<mã tài khoản>` | guide 2 đẩy gói lên, guide 4 tải gói về máy chủ |
| Vai gắn máy | 1 vai + 1 quyền đọc thùng + 1 chính sách Session Manager gắn vào + 1 hồ sơ gắn máy | `hue-rag-instance-role`, `hue-rag-instance-profile` | máy chủ CHỈ được: tải gói từ đúng thùng trên, và cho mở phiên Session Manager |

Máy chủ KHÔNG có quyền gọi model nào của AWS, không quyền ghi hay xoá thùng: bản deploy gọi model của OpenAI bằng một khoá đặt trong file trên máy (guide 4).

**Vì sao chia HAI tầng.** Đây là cặp "có trạng thái ↔ không trạng thái" của khoá học [khoá]: tầng nền giữ những thứ muốn còn mãi (gói đã đẩy lên, email đã
xác nhận, quyền) và gần 0 đồng; tầng máy chủ là thứ tính tiền, dựng và phá được nhiều lần mà không đụng tầng nền. Ở khoá học, bài toán "thứ này phải có
trước thứ kia" được giải bằng `terraform apply -target`; ở đây giải bằng hai thư mục — **không có lệnh `-target` nào trong cả bộ guide**. Cũng **không dùng
workspace**: chỉ có một môi trường, tách bằng thư mục.

## 3. Điều kiện trước

- Xong guide 0: hồ sơ AWS CLI `hue-rag-deploy`, vùng `ap-southeast-1`, Terraform từ 1.17.
- Một địa chỉ email đọc hằng ngày.

## 4. File liên quan

Thư mục `deploy/terraform/1_nen_tang/`:

| File | Là gì | Vào git? |
|---|---|---|
| `versions.tf` | ghim bản Terraform + bộ cắm AWS, vùng, thẻ chung | có |
| `variables.tf` | bốn giá trị đầu vào | có |
| `main.tf` | 11 tài nguyên, mỗi khối một dòng chú thích | có |
| `outputs.tf` | bốn đầu ra | có |
| `terraform.tfvars.example` | giá trị mẫu | có |
| `.terraform.lock.hcl` | bản chính xác của bộ cắm AWS (6.73.0) + mã băm | có |
| `terraform.tfvars` | giá trị THẬT của chủ dự án (email) — tự tạo ở Bước 2 | KHÔNG |
| `terraform.tfstate`, `terraform.tfstate.backup` | state — Terraform tự tạo ở Bước 5 | KHÔNG |
| `.terraform/` | bộ cắm tải về (khoảng 770 MB) | KHÔNG |

Ba dòng "KHÔNG" đã bị `.gitignore` chặn. **Khác bài tuần 2 của khoá học ở ba chỗ, có chủ ý:** bài đó commit `terraform.tfvars` (ở đây file này mang email
và repo là công khai) · bài đó không commit file ghim bộ cắm (ở đây có, để máy nào cũng tải đúng một bản) · bài đó có script chạy `apply -auto-approve`
(ở đây mỗi lần dựng đều đọc bản kế hoạch rồi mới gõ `yes`).

**State nằm ở đâu, mất thì sao.** State là "trái tim" của Terraform — không xoá, không sửa tay [khoá]. Nó nằm ngay trong thư mục trên, trên đĩa của WSL.
Ở khoá học state được đưa lên S3 vì máy chạy pipeline là máy tạm; ở đây một người chạy từ máy mình nên state ở máy. Mất file state KHÔNG làm mất tài nguyên
trên AWS, nhưng Terraform quên là mình đã tạo chúng: chạy lại sẽ báo "đã tồn tại", và muốn phá thì phải xoá tay từng thứ theo thẻ `Project = hue-rag`
(guide 7). Cách chữa ở mục 8.

## 5. Cấu hình

Bốn biến (`variables.tf`); chỉ MỘT biến bắt buộc phải sửa:

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `alert_email` | (không có — phải điền) | email nhận cảnh báo tiền và cảnh báo máy |
| `monthly_budget_usd` | `10` | mức ngân sách tháng. Mức 10 ⇒ thư ở 5, 8, 10 USD đã tiêu. Căn cứ: máy bật 60–100 giờ một tháng tốn khoảng 10–12 USD; để bật liên tục khoảng 42 USD [AWS — bảng giá công khai] ⇒ quên tắt máy thì thư đầu tới sau khoảng ba bốn ngày. Khoá học cũng đặt 10 USD, thư ở 80 % [khoá] |
| `aws_region` | `ap-southeast-1` | vùng; phải giống thư mục `2_may_chu` |
| `project_name` | `hue-rag` | tiền tố tên + giá trị thẻ. ĐỂ NGUYÊN: chính sách quyền ở guide 0 viết theo đúng tiền tố này |

## 6. Từng bước

Mỗi lệnh ghi rõ đang đứng ở thư mục nào — lỗi hay gặp nhất của kiểu nhiều thư mục Terraform là chạy `apply` nhầm thư mục [khoá].

**Bước 1 — Chọn hồ sơ, kiểm đúng người.**

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/1_nen_tang
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
aws sts get-caller-identity            # "Arn" phải kết thúc bằng  user/hue-rag-deploy
```

**Bước 2 — Tạo file giá trị.** (đang ở `deploy/terraform/1_nen_tang`)

```bash
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars                  # sửa dòng alert_email thành email thật; ba dòng còn lại để nguyên
git status --short .                   # KHÔNG được thấy terraform.tfvars trong danh sách
```

**Bước 3 — Tải bộ cắm.** (đang ở `deploy/terraform/1_nen_tang`)

```bash
terraform init                         # cuối cùng in: Terraform has been successfully initialized!
```

**Bước 4 — Đọc bản kế hoạch TRƯỚC khi dựng.** (đang ở `deploy/terraform/1_nen_tang`)

```bash
terraform plan                         # dòng cuối phải là:  Plan: 11 to add, 0 to change, 0 to destroy.
```

Đọc lướt 11 khối có dấu `+`: tên nào cũng bắt đầu `hue-rag-`; khối `aws_iam_role_policy.read_artifacts` chỉ có `s3:ListBucket` và `s3:GetObject`; khối
`aws_budgets_budget.monthly` có đúng email của mình. Con số khác 11, hoặc có dòng `destroy` ⇒ DỪNG, không `apply`, chép màn hình cho nhóm.

**Bước 5 — Dựng.** (đang ở `deploy/terraform/1_nen_tang`)

```bash
terraform apply                        # in lại bản kế hoạch, hỏi "Enter a value:" ⇒ gõ  yes
# cuối cùng in:  Apply complete! Resources: 11 added, 0 changed, 0 destroyed.   rồi bốn dòng Outputs
```

**Bước 6 — Bấm xác nhận email.** Trong vài phút hộp thư nhận một thư của "AWS Notifications", tiêu đề "AWS Notification - Subscription Confirmation" ⇒ bấm
"Confirm subscription". CHƯA bấm thì cảnh báo "máy hỏng" (đi qua chủ đề) không tới. Thư cảnh báo TIỀN thì AWS gửi thẳng tới địa chỉ, không cần bước xác
nhận này [AWS] — nhưng vẫn kiểm thư mục thư rác một lần.

**Bước 7 — Chép hai đầu ra sang tầng máy chủ.** (đang ở `deploy/terraform/1_nen_tang`) Hai thư mục Terraform không đọc state của nhau; giá trị đi bằng tay,
đúng cách đã làm ở tuần 2 [khoá]:

```bash
terraform output -raw artifact_bucket_name; echo        # ví dụ  hue-rag-artifacts-123456789012
terraform output -raw instance_profile_name; echo       # hue-rag-instance-profile
terraform output -raw alert_topic_arn; echo             # arn:aws:sns:ap-southeast-1:…:hue-rag-alerts
```

Ghi ba dòng này lại: guide 2 cần tên thùng; guide 3 điền cả ba vào `terraform.tfvars` của `deploy/terraform/2_may_chu`.

## 7. Kiểm

Mọi lệnh chạy với `AWS_PROFILE=hue-rag-deploy`, vùng `ap-southeast-1` **[chưa chạy]**.

| Kiểm gì | Lệnh | Phải thấy |
|---|---|---|
| State khớp thực tế | `terraform plan` (ở `deploy/terraform/1_nen_tang`) | `No changes. Your infrastructure matches the configuration.` |
| Thùng chặn công khai | `aws s3api get-public-access-block --bucket "$(terraform output -raw artifact_bucket_name)"` | bốn dòng đều `true` |
| Thùng rỗng, đọc được | `aws s3 ls "s3://$(terraform output -raw artifact_bucket_name)/"` | không in gì, không lỗi |
| Vai chỉ có hai quyền | `aws iam list-role-policies --role-name hue-rag-instance-role` và `aws iam list-attached-role-policies --role-name hue-rag-instance-role` | `read-artifacts`; `AmazonSSMManagedInstanceCore` |
| Email đã xác nhận | `aws sns list-subscriptions-by-topic --topic-arn "$(terraform output -raw alert_topic_arn)" --query 'Subscriptions[].SubscriptionArn'` | một ARN đầy đủ. Còn chữ `PendingConfirmation` ⇒ chưa bấm thư ở Bước 6 |
| Ngân sách có | `aws budgets describe-budgets --account-id "$(aws sts get-caller-identity --query Account --output text)" --query 'Budgets[].[BudgetName,BudgetLimit.Amount]'` | có dòng `hue-rag-monthly` với mức đã đặt |

Xem ngân sách trên TRANG WEB: người dùng IAM không thấy trang tiền khi tài khoản gốc chưa bật "IAM user and role access to Billing information" ⇒ dùng lệnh ở
bảng trên, hoặc đăng nhập tài khoản gốc ⇒ Billing and Cost Management ⇒ Budgets [AWS]. Ba ngân sách 1 / 5 / 10 USD tạo tay ở tuần 1 nếu còn thì vẫn gửi thư
của chúng — bình thường.

## 8. Gỡ lỗi

| Thấy gì | Vì sao | Làm gì |
|---|---|---|
| `AccessDenied` / `not authorized to perform: <dịch-vụ>:<thao tác>` lúc `apply` | chính sách ở guide 0 thiếu một quyền (chính sách CHƯA từng được thử trên tài khoản thật) | chép nguyên dòng lỗi cho nhóm; sửa chính sách theo guide 0 mục 8; chạy lại `terraform apply` — Terraform làm tiếp phần còn thiếu, không tạo trùng |
| `BucketAlreadyExists` / `BucketAlreadyOwnedByYou`, `EntityAlreadyExists`, `DuplicateRecordException` | tài nguyên cùng tên đã có: lần dựng trước dở dang mà file state đã mất, hoặc chạy ở một thư mục chép khác | KHÔNG đổi tên bừa. Còn file state cũ ⇒ quay về đúng thư mục có nó. Mất hẳn ⇒ báo nhóm: đưa từng tài nguyên vào state bằng `terraform import`, hoặc xoá tay rồi dựng lại |
| `Plan:` ra khác `11 to add` ở lần đầu | đang đứng nhầm thư mục, hoặc file bị sửa | `pwd` phải in `…/deploy/terraform/1_nen_tang`; `git status --short .` phải sạch trừ file bị chặn |
| `Error: No valid credential sources found` | chưa `export AWS_PROFILE` ở cửa sổ này | gõ lại Bước 1 |
| Không thấy thư xác nhận | thư rác, hoặc gõ sai email | sai email ⇒ sửa `terraform.tfvars` rồi `terraform plan` + `terraform apply` (kế hoạch sẽ thay đăng ký email và sửa ngân sách) |
| `Inconsistent dependency lock file` | bản bộ cắm trên máy khác bản ghim | `terraform init` lại; KHÔNG thêm `-upgrade` |

## 9. Ghi chú chi phí

- Ngân sách, chủ đề email, vai, hồ sơ gắn máy: 0 đồng. Theo dõi và thư cảnh báo của ngân sách không tính tiền [AWS].
- Thùng: tính theo dung lượng. Một gói khoảng 1 GB (ảnh nén 909 MB + bản chụp chỉ mục 78 MB — số đo của gói bản `e7193bd`) ⇒ khoảng 0,03 USD một tháng cho
  mỗi gói còn nằm trong thùng [ước theo giá lưu trữ chuẩn của S3 vùng Singapore khoảng 0,025 USD / GB / tháng — phiên B chưa mở lại bảng giá hôm nay].
  Gói cũ không dùng nữa thì xoá thư mục của nó trong thùng.
- **Ngân sách KHÔNG phải phanh.** AWS không có giới hạn cứng tự ngắt dịch vụ — ngân sách chỉ gửi email [khoá]. Số liệu tiền được cập nhật ít nhất một lần
  mỗi ngày, nên thư có thể tới chậm tới một ngày; mốc "dự báo" cần khoảng 5 tuần dữ liệu mới chạy, tháng đầu coi như chưa có [AWS]. Lưới chính chống
  "quên tắt máy" là dòng "tắt máy" trong danh sách cuối buổi ở guide 6; ngân sách là lưới thứ hai.

## 10. Dọn dẹp

Phá cả bản deploy: làm theo `7_pha_sach.md` — thứ tự NGƯỢC là bắt buộc: phá `2_may_chu` trước (máy đang dùng vai của tầng này), rồi mới tới tầng nền. Riêng
tầng nền, khi không còn máy nào:

```bash
cd /home/minhhieu/hue_rag/deploy/terraform/1_nen_tang
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
aws s3 rm "s3://$(terraform output -raw artifact_bucket_name)" --recursive    # Terraform không xoá được thùng còn file
terraform plan -destroy                # đọc: Plan: 0 to add, 0 to change, 11 to destroy.
terraform destroy                      # gõ  yes
```

Thùng không bật lưu phiên bản nên một lệnh `rm --recursive` là rỗng hẳn. Chỉ tạm nghỉ, còn định deploy lại: phá `2_may_chu`, ĐỂ tầng nền — tốn đúng tiền lưu
gói ở mục 9.

## 11. Guide kế

`2_dong_goi.md` — dựng ảnh từ đúng một commit, chạy thử trọn gói ở máy bằng khoá OpenAI, đẩy gói lên thùng vừa tạo.
