# Guide 7 — Phá sạch có kiểm: gỡ hết hạ tầng AWS của hue_rag, rồi chứng minh là không còn gì tính tiền

Viết: 20:25 23/11/2026, phiên đo. **Chưa lệnh `aws` / `terraform` nào của guide này từng chạy trên tài khoản AWS thật** — bộ deploy chưa dựng lần nào. Đã kiểm
ở máy chủ dự án, không gọi AWS: cú pháp của 20 lệnh `aws` trong guide (gọi vào một địa chỉ giả, lệnh nào cũng đi tới bước nối mạng — tức tên lệnh và
tham số hợp lệ với `aws-cli/2.36.25`); tên tài nguyên và số tài nguyên đối chiếu với hai thư mục Terraform (`1_nen_tang`: 13 tài nguyên; `2_may_chu`:
15 mặc định — 14 nếu không báo động, 12 nếu tắt lịch tự dừng, 11 nếu bỏ cả hai). Mọi dòng "Mong" là điều tài liệu AWS / Terraform nói sẽ xảy ra: **[chưa kiểm trên AWS]**. Sự thật về AWS ghi
nhãn [AWS] lấy từ bản tra cứu tài liệu chính thức ngày 23/11/2026 (riêng tư: `data/tra_cuu_cli/2026-11-23_aws-pha-sach-va-kiem-sau-deploy/ket_qua.md`);
phiên đo tự mở lại hai trang trong đó (cú pháp tìm của Resource Explorer; trang "xoá vai hoặc hồ sơ gắn máy" của IAM), các ý khác chưa tự mở. Buổi diễn tập ở guide 5
(mục 6b) đi qua Bước 3 của guide này một lần — lúc đó ghi số thật vào đây.

Guide này theo đúng khuôn sáu bước chủ dự án đã tự làm khi phá hạ tầng dự án cuối khoá ngày 11/07/2026: chốt phạm vi ⇒ kiểm trước ⇒ phá ngược thứ tự ⇒
làm rỗng thùng ⇒ kiểm bằng lệnh AWS chứ không tin state ⇒ xem hoá đơn sau một ngày. Thêm hai thứ ở dự án kia không có: Bước 0 (giữ lại thứ cần giữ)
và Bước 6 (dọn những thứ nằm NGOÀI Terraform).

Từ dùng: **tầng máy chủ** = thư mục `deploy/terraform/2_may_chu` (mạng, máy, IP tĩnh, báo động) · **tầng nền** = `deploy/terraform/1_nen_tang` (ngân
sách, chủ đề email, thùng chứa gói, vai gắn máy) · **state** = file `terraform.tfstate` trong mỗi thư mục, nơi Terraform nhớ nó đã dựng gì · **thùng** = thùng
S3 chứa gói deploy · **IP tĩnh** = Elastic IP · **thẻ** = nhãn `Project = hue-rag` mà mọi tài nguyên của bộ deploy đều mang · **tài khoản gốc** = tài
khoản đăng nhập bằng email, dùng để xem tiền.

## 1. Mục tiêu

Sau guide này: không còn tài nguyên AWS nào của hue_rag, có bằng chứng bằng lệnh (không chỉ bằng dòng "Destroy complete!"), và hoá đơn của ngày hôm
sau không còn dòng nào đang chạy. Hệ thống ở máy chủ dự án (bản local) KHÔNG bị đụng tới.

## 2. Sẽ phá gì, mất gì

Chọn đúng mức trước — ba mức khác nhau về tiền và về thứ mất:

| Mức | Làm gì | Còn tốn | Mất gì | Dùng khi |
|---|---|---|---|---|
| Dừng tạm | guide 6 mục 6.1 | đĩa 40 GB + IP tĩnh, khoảng 7,5 USD / tháng | mọi cuộc trò chuyện đang mở | giữa hai buổi demo cách nhau vài ngày |
| Phá tầng máy chủ | Bước 3 của guide này (hoặc guide 3 mục 10) | vài xu / tháng tiền lưu gói trong thùng | chỉ mục trên đĩa máy (nạp lại được từ gói), chứng chỉ HTTPS (Caddy xin lại), `hue.env` + `hue.khoa.env` gõ tay trên máy, mọi cuộc trò chuyện | không dùng trong vài tuần; lần sau làm lại guide 3 rồi guide 4 |
| **Phá sạch** | cả guide này | 0 | thêm: gói trong thùng (dựng lại được bằng guide 2), ngân sách + email cảnh báo, vai gắn máy | đồ án đã chấm xong, không cần bản deploy nữa |

Phá sạch gỡ hai nhóm tài nguyên, theo thứ tự NGƯỢC với lúc dựng:

| Thứ tự | Thư mục | Tài nguyên (tên đều bắt đầu `hue-rag-`) |
|---|---|---|
| 1 | `2_may_chu` | máy EC2 + đĩa gốc · IP tĩnh · báo động "máy không qua kiểm tra trạng thái" (nếu đã tạo) · lịch tự dừng máy `hue-rag-tu-dung-dem` + vai IAM `hue-rag-scheduler-role` + quyền (nếu `auto_stop_enabled = true`) · nhóm bảo mật + ba luật · mạng riêng (VPC), subnet, cổng internet, bảng định tuyến |
| 2 | `1_nen_tang` | thùng `hue-rag-artifacts-<mã tài khoản>` + bốn thiết lập của nó (gồm quy tắc vòng đời dọn mảnh upload dở) · vai `hue-rag-instance-role` + hồ sơ `hue-rag-instance-profile` + hai quyền · chủ đề `hue-rag-alerts` + đăng ký email + chính sách chủ đề cho CloudWatch · ngân sách `hue-rag-monthly` |

Thứ tự ngược ở đây là **BẮT BUỘC**, không chỉ "cho gọn" như ở dự án khoá học: máy đang dùng hồ sơ gắn máy của tầng nền, và báo động đang trỏ vào chủ
đề của tầng nền. Hai thư mục có state riêng nên Terraform KHÔNG tự biết quan hệ này và sẽ không cản. Trang IAM của AWS cảnh báo: xoá vai hoặc hồ sơ
gắn máy đang gắn vào một máy đang chạy sẽ làm hỏng thứ đang chạy trên máy [AWS] — với ta nghĩa là máy mất quyền tải gói và KHÔNG còn mở phiên Session
Manager vào được nữa, trong khi máy vẫn chạy và vẫn tính tiền (mục 8).

Thứ nằm NGOÀI Terraform — `terraform destroy` không đụng tới, phải tự dọn ở Bước 6: khoá OpenAI của bản deploy · khoá truy cập của người dùng IAM
`hue-rag-deploy` (và chính người dùng, nhóm `HueRagDeploy`, chính sách `HueRagDeployAccess`) · tên miền riêng nếu đã dùng · file trên máy mình
(`terraform.tfvars`, state, hồ sơ AWS CLI).

## 3. Điều kiện trước

- Đã chọn mức "Phá sạch" ở bảng trên. Chỉ muốn về gần 0 đồng mà còn dùng lại ⇒ chỉ làm Bước 0, 1, 2, 3 rồi dừng.
- Còn nguyên hai file state: `deploy/terraform/2_may_chu/terraform.tfstate` và `deploy/terraform/1_nen_tang/terraform.tfstate`. **Không xoá, không
  sửa tay hai file này trước khi Bước 5 ra sạch** — mất state thì Terraform không biết phải phá gì (mục 8).
- Hồ sơ AWS CLI `hue-rag-deploy` còn dùng được (guide 0). Đăng nhập được tài khoản gốc trên trình duyệt (cho Bước 5 phần trang web và Bước 7).
- Không ai đang dùng trang. Phá là mất mọi cuộc trò chuyện đang mở, không lấy lại được.

## 4. File liên quan

| File / thư mục | Vai trò ở guide này |
|---|---|
| `deploy/terraform/2_may_chu/` | phá trước; cần file state của nó |
| `deploy/terraform/1_nen_tang/` | phá sau; cần file state của nó |
| `deploy/guides/hue-rag-deploy-policy.json` | quyền của người dùng `hue-rag-deploy` — vì sao vài lệnh "liệt kê tất cả" bị từ chối (mục 8) |
| `deploy/guides/0_dieu_kien_truoc.md` mục 10 | cách xoá khoá truy cập, người dùng, nhóm, chính sách trên trang web |
| `deploy/guides/6_ngay_demo.md` mục 6.6 | cách thu hồi khoá OpenAI |

## 5. Cấu hình

Mỗi cửa sổ lệnh mới gõ lại hai dòng này trước (biến chỉ sống trong cửa sổ đó):

```bash
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
GOC=/home/minhhieu/hue_rag/deploy/terraform
```

Mọi lệnh `aws` của guide chạy ở vùng Singapore (`ap-southeast-1`) bằng hồ sơ `hue-rag-deploy`. Lệnh nào phải dùng tài khoản gốc thì guide ghi rõ
"trên trang web, tài khoản gốc".

## 6. Từng bước

Đọc từng bước, gõ từng lệnh, NHÌN đầu ra rồi mới gõ lệnh kế. Đừng dán cả khối như một script.

**Bước 0 — Giữ lại thứ cần giữ** (phá tầng máy chủ là mất hẳn):

- Ảnh chụp màn hình trang đang chạy trên địa chỉ thật, số đo của buổi diễn tập / buổi demo — bằng chứng cho đồ án.
- Log của ba hộp, nếu cần xem lại: XEM ngay trên máy chủ (vào bằng lệnh ở guide 4 bước 1) và chép đoạn cần qua cửa sổ lệnh —
  `cd /srv/hue && docker compose --env-file hue.env -f compose.yml logs --no-color --tail 200 app` (thêm `| grep <chữ cần tìm>` cho gọn). Với quyền hiện có
  KHÔNG lấy được cả file về máy mình (máy chỉ ĐỌC được thùng, không mở cổng 22); log có câu người dùng đã hỏi ⇒ đoạn chép ra không đưa vào git.
- Sổ vết, nếu đã bật tạm trên máy chủ (guide 5).
- Ghi lại hai giá trị sẽ cần ở Bước 5 (sau khi phá thì không hỏi Terraform được nữa):

```bash
cd "$GOC/1_nen_tang" && THUNG=$(terraform output -raw artifact_bucket_name) && echo "$THUNG"
TK=$(aws sts get-caller-identity --query Account --output text) && echo "$TK"
```

**Bước 1 — Chốt phạm vi.** Chỉ phá thứ mang tiền tố `hue-rag-` và thẻ `Project = hue-rag`. Tài khoản này còn tài nguyên của các dự án khoá học — guide
này không có lệnh nào chạm vào chúng, và trong bản kế hoạch phá ở Bước 3, Bước 4 không được xuất hiện tên nào khác tiền tố đó. Gõ lại tiền tố để tự xác
nhận (thói quen của lệnh phá ở khoá học — bắt gõ tên môi trường):

```bash
read -r -p "Gõ lại tiền tố của bộ deploy sẽ bị phá: " T; [ "$T" = "hue-rag" ] && echo "ĐÚNG — làm tiếp" || echo "SAI — dừng lại"
```

**Bước 2 — Kiểm trước khi phá.**

```bash
cd /home/minhhieu/hue_rag && git status --short deploy/     # mong: không in gì (không có file Terraform nào đang sửa dở)
aws sts get-caller-identity --query Arn --output text       # NHÌN: phải kết bằng  user/hue-rag-deploy
aws configure get region                                    # mong: ap-southeast-1
ls -l "$GOC"/2_may_chu/terraform.tfstate "$GOC"/1_nen_tang/terraform.tfstate     # mong: hai file đều có, cỡ khác 0
```

Thiếu một file state ⇒ DỪNG, xem mục 8 dòng "mất file state". Ghi lại danh sách "trước khi phá" để lát nữa so:

```bash
aws resourcegroupstaggingapi get-resources --tag-filters Key=Project,Values=hue-rag \
  --query 'ResourceTagMappingList[].ResourceARN' --output text | tr '\t' '\n' | sort > /tmp/hue_rag_truoc_khi_pha.txt
wc -l /tmp/hue_rag_truoc_khi_pha.txt; cat /tmp/hue_rag_truoc_khi_pha.txt
```

Mong: khoảng mười mấy dòng — máy, đĩa, IP tĩnh, mạng, nhóm bảo mật, thùng, chủ đề, báo động… (vai và hồ sơ gắn máy là tài nguyên toàn cục của IAM,
có thể không hiện ở lệnh chạy theo vùng này — Bước 5 kiểm chúng bằng lệnh gọi đích danh).

**Bước 3 — Phá tầng máy chủ** (từ đây máy, IP tĩnh và trang web biến mất):

```bash
cd "$GOC/2_may_chu"
terraform plan -destroy        # ĐỌC HẾT: dòng cuối  Plan: 0 to add, 0 to change, 15 to destroy.  (14 nếu không báo động; 12 nếu tắt lịch tự dừng; 11 nếu bỏ cả hai)
                               # mọi tên trong bản kế hoạch phải bắt đầu  hue-rag-  ; thấy tên lạ ⇒ DỪNG
terraform destroy              # in lại bản kế hoạch, hỏi "Enter a value:" ⇒ gõ  yes
```

Mong dòng cuối: `Destroy complete! Resources: 15 destroyed.` (hoặc 14 / 12 / 11). Máy bị xoá mất một hai phút; lệnh trông như đứng yên ở dòng `Still destroying...` là
bình thường — đừng ngắt (lần phá dự án khoá học cũng có một bước đứng lâu như vậy rồi tự xong). Kiểm ngay, bằng lệnh AWS:

```bash
aws ec2 describe-instances --filters "Name=tag:Project,Values=hue-rag" \
  --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output text      # mong: không in gì, hoặc một dòng ghi  terminated
aws ec2 describe-addresses --filters "Name=tag:Project,Values=hue-rag" \
  --query 'Addresses[].[PublicIp,AllocationId,AssociationId]' --output text       # mong: KHÔNG in gì
```

Dòng `terminated` của máy tự biến mất sau khoảng một giờ; nó không tính tiền. IP tĩnh thì khác: còn in ra một dòng nghĩa là địa chỉ còn bị giữ và
**còn tính tiền theo giờ** — xem mục 8 dòng "IP tĩnh còn sót".

Chỉ muốn về gần 0 đồng mà giữ tầng nền ⇒ DỪNG Ở ĐÂY (làm thêm Bước 7 ngày hôm sau). Phá sạch ⇒ làm tiếp.

**Bước 4 — Làm rỗng thùng, rồi phá tầng nền.** Terraform không xoá được thùng còn file (thùng cố ý không đặt chế độ "xoá cả khi còn file"):

```bash
cd "$GOC/1_nen_tang"
THUNG=$(terraform output -raw artifact_bucket_name); echo "$THUNG"      # NHÌN: hue-rag-artifacts-<mã tài khoản>
aws s3 rm "s3://$THUNG" --recursive                                     # in từng dòng  delete: …
aws s3 ls "s3://$THUNG/" --recursive --summarize                        # mong: Total Objects: 0
aws s3api list-multipart-uploads --bucket "$THUNG" --query 'Uploads[].[Key,UploadId]' --output text    # mong: không in gì (hoặc None)
```

Thùng này KHÔNG bật lưu phiên bản nên một lệnh `rm --recursive` là rỗng hẳn — không có bước xoá phiên bản cũ và dấu xoá như ở thùng của dự án khoá
học. Ngoài ra tầng nền đã đặt quy tắc vòng đời tự huỷ mảnh upload dở sau 3 ngày, nhưng khi phá ngay lập tức thì lệnh thứ tư vẫn kiểm xem có lần `aws s3 cp` bị ngắt giữa chừng nào chưa hết hạn 3 ngày: lệnh `rm` KHÔNG dọn các mảnh dở này và chúng có
thể tính tiền lưu trữ [AWS]; có dòng nào thì xem mục 8.

```bash
terraform plan -destroy        # ĐỌC: Plan: 0 to add, 0 to change, 13 to destroy.  — mọi tên bắt đầu  hue-rag-
terraform destroy              # gõ  yes
```

Mong dòng cuối: `Destroy complete! Resources: 13 destroyed.`

**Bước 5 — Kiểm bằng lệnh AWS, không tin state.** "Destroy complete!" chỉ nói Terraform đã xoá những gì nó NHỚ. Phép kiểm thật là hỏi thẳng AWS từng
thứ. Người dùng `hue-rag-deploy` không có quyền "liệt kê tất cả" (mọi thùng, mọi vai, mọi ngân sách) nên các lệnh dưới gọi ĐÍCH DANH từng tên; với
kiểu gọi này, **một dòng lỗi "không tìm thấy" chính là kết quả đúng**.

| Kiểm gì | Lệnh | Mong |
|---|---|---|
| Thùng | `aws s3api head-bucket --bucket "$THUNG"` | lỗi `404` / `Not Found` |
| Vai gắn máy | `aws iam get-role --role-name hue-rag-instance-role` | lỗi `NoSuchEntity` |
| Vai lịch tự dừng | `aws iam get-role --role-name hue-rag-scheduler-role` | lỗi `NoSuchEntity` |
| Lịch tự dừng máy | `aws scheduler get-schedule --name hue-rag-tu-dung-dem` | lỗi `ResourceNotFoundException` |
| Hồ sơ gắn máy | `aws iam get-instance-profile --instance-profile-name hue-rag-instance-profile` | lỗi `NoSuchEntity` |
| Chủ đề email | `aws sns list-topics --query "Topics[?contains(TopicArn, 'hue-rag')].TopicArn" --output text` | không in gì |
| Ngân sách | `aws budgets describe-budget --account-id "$TK" --budget-name hue-rag-monthly` | lỗi `NotFoundException` |
| Báo động | `aws cloudwatch describe-alarms --alarm-name-prefix hue-rag- --query 'MetricAlarms[].AlarmName' --output text` | không in gì |
| Máy | lệnh `describe-instances` ở Bước 3 | không in gì, hoặc `terminated` |
| IP tĩnh | lệnh `describe-addresses` ở Bước 3 | không in gì |
| Đĩa | `aws ec2 describe-volumes --filters "Name=tag:Project,Values=hue-rag" --query 'Volumes[].[VolumeId,State,Size]' --output text` | không in gì |
| Mạng riêng | `aws ec2 describe-vpcs --filters "Name=tag:Project,Values=hue-rag" --query 'Vpcs[].VpcId' --output text` | không in gì |
| Nhóm bảo mật | `aws ec2 describe-security-groups --filters "Name=tag:Project,Values=hue-rag" --query 'SecurityGroups[].GroupId' --output text` | không in gì |
| Bản chụp đĩa (không do Terraform tạo — chỉ có nếu ai đó tạo tay) | `aws ec2 describe-snapshots --owner-ids self --query 'Snapshots[].[SnapshotId,VolumeSize,StartTime]' --output text` | không có bản nào tạo trong những ngày dùng bộ deploy |
| Mọi thứ mang thẻ, vùng Singapore | `aws resourcegroupstaggingapi get-resources --tag-filters Key=Project,Values=hue-rag --query 'ResourceTagMappingList[].ResourceARN' --output text` | không in gì. Còn in vài dòng ngay sau khi phá ⇒ chạy lại sau ít phút; còn mãi thì so với `/tmp/hue_rag_truoc_khi_pha.txt` và hỏi đích danh thứ đó |

`$THUNG` và `$TK` là hai giá trị đã ghi ở Bước 0 (mở cửa sổ lệnh mới thì gán lại bằng tay: `THUNG=hue-rag-artifacts-<mã tài khoản>`, `TK=<mã tài khoản>`).

Rồi soát ở MỌI VÙNG, trên trang web bằng **tài khoản gốc** (người dùng `hue-rag-deploy` không có quyền vào các trang này) — đúng các cách bài tuần 2
ngày 5 của khoá học đã dạy:

- **Tag Editor** (ô tìm kiếm trên cùng gõ `Tag Editor`, thuộc Resource Groups): ở ô Regions chọn MỌI vùng · Resource types chọn mọi loại tài nguyên ·
  Tags: khoá `Project`, giá trị `hue-rag` ⇒ Search resources. Mong: 0 kết quả. (Tên chính xác của từng ô trên trang hiện nay: chưa ai trong nhóm tự bấm.)
- **Resource Explorer**, CHỈ khi tài khoản đã bật từ trước: ô tìm gõ `tag:Project=hue-rag` (đây là cú pháp tài liệu ghi [AWS]; không phải
  `tag.Project:…`). Mong: 0 kết quả. Chưa bật thì bỏ qua: lập chỉ mục lần đầu có thể mất tới 36 giờ [AWS] — Tag Editor là đủ, không bật thêm một dịch
  vụ chỉ để kiểm.
- Cả hai cách tìm theo thẻ đều KHÔNG chứng minh được phần IAM đã sạch: thẻ của vai và người dùng IAM không được Resource Explorer lập chỉ mục [AWS], và
  lệnh `get-resources` chạy theo từng vùng. Bằng chứng cho vai và hồ sơ gắn máy là hai dòng gọi đích danh trong bảng trên.
- **EC2 ⇒ Elastic IPs** ở vùng Singapore: không còn địa chỉ nào của bộ deploy.

**Bước 6 — Dọn thứ nằm ngoài Terraform.** Tick từng dòng:

- [ ] **Khoá OpenAI của bản deploy**: thu hồi trên trang quản lý OpenAI (đường bấm ở guide 6 mục 6.6). Khoá này đã nằm trên một máy vừa bị xoá — không
      để nó sống tiếp. Số tiền nạp trước còn lại vẫn thuộc tài khoản OpenAI của chủ dự án.
- [ ] **Khoá truy cập của `hue-rag-deploy`**: tài khoản gốc ⇒ IAM ⇒ Users ⇒ `hue-rag-deploy` ⇒ Security credentials ⇒ khoá ⇒ **Deactivate** trước;
      sau khi Bước 7 sạch thì **Delete**. Vô hiệu trước, xoá sau: nếu Bước 7 lộ ra thứ còn sót thì chỉ cần bật lại khoá để dọn.
- [ ] Người dùng `hue-rag-deploy`, nhóm `HueRagDeploy`, chính sách `HueRagDeployAccess`: xoá sau khi Bước 7 sạch (guide 0 mục 10), hoặc để lại nếu sẽ
      deploy lần nữa — ba thứ này không tốn tiền; thứ nguy hiểm là KHOÁ còn hiệu lực, không phải người dùng.
- [ ] **Tên miền riêng**, nếu đã trỏ về IP tĩnh: xoá bản ghi đó ở nơi quản lý tên miền — IP ấy sau này thuộc về người khác. Dùng tên dạng `sslip.io`
      thì không có gì phải dọn.
- [ ] **Email cảnh báo**: không phải làm gì — xoá chủ đề thì các đăng ký của nó được AWS xoá theo; đăng ký chưa bấm xác nhận tự hết hạn sau 48 giờ [AWS]. Ba ngân sách 1 / 5 / 10 USD tạo tay ở tuần 1 của khoá học là của khoá học, guide
      này không đụng.
- [ ] **File trên máy mình**: giữ hai file `terraform.tfstate` tới khi Bước 7 sạch, rồi xoá cùng `terraform.tfvars` và thư mục `.terraform/` của hai
      thư mục (mục 10). Hồ sơ `hue-rag-deploy` trong `~/.aws/credentials`: xoá sau khi đã xoá khoá ở dòng trên.

**Bước 7 — Xem hoá đơn sau một ngày** (trên trang web, **tài khoản gốc**). Cost Explorer cập nhật ít nhất mỗi 24 giờ một lần và số liệu có thể tới muộn
hơn thế [AWS] — xem ngay sau khi phá thì chưa nói lên điều gì. Xem trên trang web không tốn tiền (gọi bằng lệnh thì mỗi lần 0,01 USD [AWS]).

Billing and Cost Management ⇒ **Cost Explorer** ⇒ khoảng ngày: 7 ngày gần nhất · Granularity: Daily · Group by: Service.

| Thấy gì ở ngày SAU ngày phá | Nghĩa là |
|---|---|
| Không còn cột nào, hoặc chỉ còn tiền của dự án khác | sạch — xong |
| "EC2 - Other" hoặc "VPC" còn tiền đều mỗi ngày | còn IP tĩnh hoặc đĩa sót ⇒ lệnh `describe-addresses` (không lọc thẻ) và `describe-volumes` ở mục 8 |
| "EC2-Instances" còn tiền | còn một máy đang chạy ⇒ `aws ec2 describe-instances` không lọc thẻ, xem cả máy không mang thẻ |
| "S3" còn vài phần nghìn USD | thùng chưa bị xoá, hoặc là thùng của dự án khác |
| Tiền của CHÍNH ngày phá (máy chạy tới giờ phá, lưu gói tới giờ phá) | bình thường — không phải dấu hiệu sót |

Sạch ⇒ quay lại Bước 6 tick nốt các dòng "sau khi Bước 7 sạch".

## 7. Kiểm

| Kiểm | Bằng gì | Mong |
|---|---|---|
| Tầng máy chủ đã phá | dòng cuối của `terraform destroy` ở Bước 3 | `Destroy complete! Resources: 15 destroyed.` (hoặc 14 / 12 / 11) |
| Tầng nền đã phá | dòng cuối ở Bước 4 | `Destroy complete! Resources: 13 destroyed.` |
| AWS không còn gì mang tên / thẻ của bộ deploy | bảng mười lăm dòng ở Bước 5 | dòng nào cũng đúng cột "Mong" |
| Không sót ở vùng khác | Tag Editor, All regions, tài khoản gốc | 0 kết quả |
| Trang không còn mở được | `curl -m 10 -s -o /dev/null -w '%{http_code}\n' https://<site_name>/health` | `000` (không kết nối được) |
| Khoá OpenAI của bản deploy đã chết | trang quản lý OpenAI: khoá không còn trong danh sách | — |
| Hoá đơn | Cost Explorer ngày hôm sau, tài khoản gốc | bảng ở Bước 7: "sạch" |

## 8. Gỡ lỗi

Quy tắc chung, rút từ lần phá dự án khoá học: lệnh phá hỏng giữa chừng ⇒ ĐỌC dòng lỗi, sửa đúng chỗ đó, rồi **chạy lại chính lệnh `terraform destroy`**
— Terraform phá tiếp phần còn lại, không phá trùng. Không xoá file state, không chuyển sang bước kế khi bước này chưa xong.

| Thấy gì | Vì sao | Làm gì |
|---|---|---|
| Bước 4: `BucketNotEmpty` | thùng còn file — bỏ qua lệnh `aws s3 rm`, hoặc có gói mới đẩy lên sau đó | chạy lại ba lệnh làm rỗng thùng ở Bước 4, rồi `terraform destroy` lại |
| Lệnh `list-multipart-uploads` có in dòng | một lần đẩy gói bị ngắt để lại các mảnh dở; chúng không hiện trong `aws s3 ls` | với từng dòng: `aws s3api abort-multipart-upload --bucket "$THUNG" --key "<Key>" --upload-id "<UploadId>"`, rồi chạy lại lệnh liệt kê |
| Lỡ phá tầng nền TRƯỚC khi phá tầng máy chủ (lệnh có thể chạy xong không báo lỗi gì, hoặc dừng ở bước xoá vai — chưa kiểm trên AWS) | sai thứ tự: máy còn sống nhưng đã mất vai ⇒ không mở được phiên Session Manager, không tải được gói; báo động trỏ vào một chủ đề không còn | KHÔNG dựng lại tầng nền. Làm ngay Bước 3 — phá `2_may_chu` không cần vào máy và không cần vai đó; lệnh ở tầng nền còn dở thì chạy lại `terraform destroy` ở `1_nen_tang` sau đó; rồi làm đủ Bước 5 |
| `Error: Plugin did not respond` hoặc lỗi lạ của bộ cắm ngay lúc đầu | lỗi tạm của bộ cắm AWS (đã gặp đúng lỗi này ở Part 6 của dự án khoá học) | chạy lại y nguyên lệnh |
| `Still destroying...` rất lâu ở máy hoặc ở cổng internet | AWS đang gỡ thật; cổng internet chỉ gỡ được sau khi IP tĩnh được trả | chờ; mở cửa sổ lệnh thứ hai chạy lệnh `describe-instances` ở Bước 3 để thấy tiến độ. Không ngắt |
| `AccessDenied` / `not authorized to perform …` khi phá | chính sách của `hue-rag-deploy` thiếu một quyền xoá (chính sách chưa từng được thử trên tài khoản thật) | chép nguyên dòng lỗi cho nhóm; sửa chính sách theo guide 0 mục 8; chạy lại `terraform destroy` |
| `aws s3 ls` (không kèm tên thùng), `aws iam list-roles`, `aws budgets describe-budgets` báo `AccessDenied` | đúng thiết kế: người dùng này chỉ có quyền trên thứ tên `hue-rag-…`, không được liệt kê cả tài khoản | dùng lệnh gọi đích danh ở Bước 5; cần nhìn cả tài khoản thì dùng trang web bằng tài khoản gốc |
| Mất file state mà tài nguyên còn trên AWS | Terraform không còn biết phải phá gì | KHÔNG `apply` lại (sẽ đụng tên đã có). Lấy danh sách bằng lệnh `get-resources` ở Bước 2 + bảng ở mục 2, rồi báo nhóm: hoặc đưa từng thứ vào state bằng `terraform import` rồi phá, hoặc xoá tay trên trang web theo thứ tự máy ⇒ IP tĩnh ⇒ mạng ⇒ thùng ⇒ vai ⇒ chủ đề ⇒ ngân sách |
| `terraform destroy` báo một tài nguyên "not found" | thứ đó đã bị xoá tay trước | `terraform plan -destroy` lần nữa (Terraform tự nhận ra thứ đã mất); vẫn kẹt ⇒ báo nhóm trước khi dùng `terraform state rm` |
| IP tĩnh còn sót (Bước 3 còn in một dòng, hoặc hoá đơn còn "EC2 - Other") | lệnh phá bị ngắt sau khi xoá máy nhưng trước khi trả địa chỉ | chạy lại `terraform destroy` ở `2_may_chu`. Vẫn còn: `aws ec2 describe-addresses --query 'Addresses[].[PublicIp,AllocationId,InstanceId]' --output text` (không lọc thẻ) để thấy mọi địa chỉ của vùng — chỉ trả địa chỉ mà dòng của nó khớp `/tmp/hue_rag_truoc_khi_pha.txt`: `aws ec2 release-address --allocation-id <AllocationId>` |
| Bước 5 còn thấy đĩa (`describe-volumes` in dòng) | đĩa gốc được đặt xoá theo máy nên không nên xảy ra; nếu có là đĩa ai đó gắn thêm bằng tay | xem `State`: `available` (không gắn vào máy nào) thì xoá trên trang EC2 ⇒ Volumes sau khi chắc không cần dữ liệu |

## 9. Ghi chú chi phí

- Bản thân việc phá không tốn tiền. Xoá sớm trong tháng không được hoàn tiền của những giờ đã chạy.
- Thứ hay bị quên nhất là **IP tĩnh**: AWS tính 0,005 USD mỗi giờ cho mọi địa chỉ IPv4 công khai (khoảng 3,6 USD / tháng), kể cả khi máy đã dừng hoặc địa
  chỉ không gắn vào máy nào; tiền chỉ ngừng khi địa chỉ được TRẢ lại (release), gỡ khỏi máy là chưa đủ [AWS] —
  vì thế Bước 3 và Bước 5 kiểm riêng nó, và bảng hoá đơn ở Bước 7 có một dòng riêng cho nó.
- Sau khi phá tầng máy chủ mà giữ tầng nền: chỉ còn tiền lưu gói trong thùng (mỗi gói khoảng 1 GB — vài xu một tháng); ngân sách, chủ đề email, vai gắn
  máy không tốn tiền ở mức dùng này.
- Tiền gọi model của OpenAI không nằm trên hoá đơn AWS: xem ở trang sử dụng của OpenAI; thu hồi khoá ở Bước 6 là điểm chấm dứt.

## 10. Dọn dẹp

Sau khi Bước 7 sạch, dọn phần còn lại trên máy mình (không còn gì trên AWS để các file này trỏ tới):

```bash
cd /home/minhhieu/hue_rag/deploy/terraform
ls 1_nen_tang/terraform.tfstate* 2_may_chu/terraform.tfstate* 1_nen_tang/terraform.tfvars 2_may_chu/terraform.tfvars    # NHÌN danh sách trước khi xoá
rm -f 1_nen_tang/terraform.tfstate* 2_may_chu/terraform.tfstate* 1_nen_tang/terraform.tfvars 2_may_chu/terraform.tfvars
rm -rf 1_nen_tang/.terraform 2_may_chu/.terraform          # bộ cắm đã tải (mỗi thư mục gần 800 MB); `terraform init` tải lại được
git status --short deploy/                                  # mong: không in gì — các file trên vốn không nằm trong git
```

Hai file `.terraform.lock.hcl` GIỮ (chúng nằm trong git). Gói ở máy mình (`~/hue_goi_<sha>/` của guide 2) xoá được bất cứ lúc nào.

## 11. Guide kế

Không còn guide nào sau guide này. Muốn dựng lại từ đầu: guide 0 (nếu đã xoá người dùng và khoá) ⇒ 1 ⇒ 2 ⇒ 3 ⇒ 4 ⇒ 5. Muốn dựng lại chỉ tầng máy chủ
(đã dừng ở Bước 3): guide 3 ⇒ 4.
