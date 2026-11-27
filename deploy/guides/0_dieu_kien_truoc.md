# Guide 0 — Điều kiện trước: tài khoản, quyền, công cụ, khoá OpenAI

Viết: 19:48 23/11/2026 (giờ `date`), phiên B. Người gõ lệnh: chủ dự án. Guide kế: `1_nen_tang.md`.

**Trạng thái của guide này:** các lệnh chạy ở máy (kiểm công cụ, kiểm file) đã chạy thật trên máy WSL của chủ dự án. Các bước trên trang AWS và trang OpenAI
CHƯA ai trong nhóm làm thật — nhóm không có quyền và không được gọi AWS. Chỗ nào chưa làm thật mang nhãn **[chưa chạy]**.

Từ dùng: **tài khoản gốc** (root) = tài khoản đăng nhập bằng email, toàn quyền, chỉ dùng cho việc cấp quyền và xem tiền · **người dùng IAM** = người dùng con
để làm việc hằng ngày · **chính sách** (policy) = một tờ quyền · **nhóm quyền** (user group) = nơi gắn chính sách, người dùng vào nhóm thì có quyền của nhóm ·
**khoá truy cập** (access key) = cặp mã để AWS CLI và Terraform đăng nhập thay người · **hồ sơ AWS CLI** (profile) = một bộ khoá + vùng có tên, cất ở
`~/.aws/` · **vùng** (region) = cụm trung tâm dữ liệu; cả bộ deploy dùng Singapore, mã `ap-southeast-1` · **Session Manager** = cách mở cửa sổ lệnh vào máy
chủ qua AWS, không cần SSH · **Terraform** = công cụ dựng hạ tầng từ file (đã dùng ở dự án tuần 2–4 của khoá học).

Nhãn nguồn: **[AWS]**, **[OpenAI]** = phiên B tự mở trang tài liệu chính thức ngày 23/11/2026 · **[khoá]** = theo bài của khoá AI Production ·
**[máy]** = đã chạy trên máy này · **[chưa chạy]** = chưa làm thật trên tài khoản.

## 1. Mục tiêu

Làm xong guide này thì mọi thứ KHÔNG tốn tiền nhưng bắt buộc phải có trước khi dựng đã sẵn: một người dùng AWS riêng cho việc deploy với đúng các quyền
cần, bộ công cụ trên máy, và một khoá OpenAI riêng có chốt tiền. Guide này không tạo tài nguyên nào tính tiền.

## 2. Sẽ có gì sau guide này

| Thứ | Tên dùng trong cả bộ guide | Ở đâu |
|---|---|---|
| Chính sách quyền tự viết | `HueRagDeployAccess` | tài khoản AWS |
| Nhóm quyền | `HueRagDeploy` | tài khoản AWS |
| Người dùng IAM MỚI, chỉ có khoá truy cập, không có mật khẩu đăng nhập trang web | `hue-rag-deploy` | tài khoản AWS |
| Hồ sơ AWS CLI riêng | `hue-rag-deploy`, vùng `ap-southeast-1` | máy WSL, `~/.aws/` |
| Công cụ | Terraform, AWS CLI, phần cắm Session Manager, Docker | máy WSL |
| Khoá OpenAI riêng cho bản deploy, trong một project riêng có trần chi tiêu cứng | project `hue-rag-deploy` | trang OpenAI; khoá chỉ nằm trong file trên máy chủ (guide 4) |

**Vì sao người dùng MỚI mà không dùng lại `aiengineer` của khoá học:** `aiengineer` đang mang ba nhóm quyền rộng của ba dự án khoá học (kiểu toàn quyền từng
dịch vụ). Người dùng mới chỉ mang MỘT chính sách viết riêng cho hue_rag, hẹp theo tên tài nguyên (`hue-rag-…`) và theo vùng. Ở tuần 2 khoá học dùng một vai
deploy gắn chín chính sách toàn quyền cho pipeline; ở đây không có pipeline, một người gõ lệnh từ máy mình [khoá].

## 3. Điều kiện trước

- Tài khoản AWS cá nhân đã làm các dự án khoá học, đăng nhập được bằng tài khoản gốc (email + mật khẩu + mã MFA).
- Tài khoản OpenAI đang dùng cho `gpt-6-luna`. Từ 25/11/2026, cả máy local lẫn bản deploy đều mặc định `provider: openai` (`gpt-6-luna`); lượt đo bù và bộ câu kín trên `gpt-6-luna` đã hoàn tất (23–25/11).
- Máy WSL này, thư mục dự án `/home/minhhieu/hue_rag`.

## 4. File liên quan

| File | Là gì |
|---|---|
| `deploy/guides/hue-rag-deploy-policy.json` | nội dung chính sách `HueRagDeployAccess` — dán nguyên văn ở Bước 2 |
| `deploy/terraform/1_nen_tang/`, `deploy/terraform/2_may_chu/` | hai thư mục Terraform mà người dùng mới sẽ chạy (guide 1 và 3) |

Ba loại file mang GIÁ TRỊ riêng của chủ dự án — không file nào vào git:

| File | Ai đọc | Nằm ở đâu | Chứa gì |
|---|---|---|---|
| `.env` | code hue_rag khi chạy ở máy | gốc dự án trên máy WSL | khoá gọi model lúc phát triển. Bản deploy KHÔNG dùng file này |
| `terraform.tfvars` | Terraform | từng thư mục `deploy/terraform/…` trên máy WSL | email cảnh báo, mức ngân sách, tên thùng… Không chứa khoá nào |
| `hue.env` + `hue.khoa.env` | ba hộp Docker trên máy chủ | `/srv/hue` trên máy chủ (guide 4) | `hue.env`: cấu hình không bí mật · `hue.khoa.env` (quyền 600): khoá OpenAI |

## 5. Cấu hình

Không có file cấu hình nào ở guide này. Hai giá trị dùng suốt bộ guide:

```bash
export AWS_PROFILE=hue-rag-deploy      # mọi lệnh aws / terraform của bộ guide chạy bằng hồ sơ này
export AWS_REGION=ap-southeast-1       # vùng Singapore
```

Hai dòng này phải gõ lại ở MỖI cửa sổ lệnh mới. Hồ sơ mặc định trên máy là người dùng `aiengineer` của khoá học, ở CÙNG tài khoản — quên chọn hồ sơ thì lệnh
vẫn chạy được một phần bằng nhầm người. Vì vậy mọi guide mở đầu bằng lệnh kiểm `aws sts get-caller-identity` và NHÌN tên người dùng in ra.

## 6. Từng bước

Bước 1–4 làm trên trang web AWS bằng **tài khoản gốc**; từ Bước 6 trở đi làm trên máy WSL bằng người dùng mới. Đây là đúng nhịp bảy bước cấp quyền của
guide 1 dự án tuần 3 [khoá], chỉ khác ở chỗ tạo người dùng mới. Tên nút trên trang AWS có thể đổi chữ so với lúc viết **[chưa chạy]**.

**Bước 1 — Đăng nhập tài khoản gốc, xem hai điều.** Vào <https://aws.amazon.com/console/> ⇒ "Root user". (a) Góc phải trên ⇒ "Security credentials": mục MFA
phải có một thiết bị đang gắn. (b) Tài khoản đang ở gói trả tiền, không phải gói miễn phí bị giới hạn dịch vụ — khoá học kể một học viên mất 24 giờ vì lỗi
này trông giống lỗi thiếu quyền [khoá].

**Bước 2 — Tạo chính sách.** IAM ⇒ Policies ⇒ Create policy ⇒ thẻ JSON ⇒ xoá nội dung có sẵn, dán NGUYÊN VĂN file
`deploy/guides/hue-rag-deploy-policy.json` ⇒ Next ⇒ tên `HueRagDeployAccess`, mô tả `Quyen deploy hue_rag` ⇒ Create policy. Chính sách cho phép gì:

| Khối trong file | Cho phép | Giới hạn ở |
|---|---|---|
| `ThungGoi` | tạo, cấu hình (gồm quy tắc vòng đời dọn mảnh upload dở), đẩy file lên, xoá thùng chứa gói | thùng tên `hue-rag-artifacts-…` |
| `VaiGanMay` + `ChiGanChinhSachSessionManagerVaoVai` + `GiaoVaiChoMayEC2` | tạo vai và hồ sơ gắn máy; gắn vào vai đúng MỘT chính sách có sẵn của Session Manager; giao vai cho máy EC2 | vai / hồ sơ tên `hue-rag-…` |
| `GiaoVaiChoScheduler` + `LichTuDungMayEC2` | giao vai cho EventBridge Scheduler; tạo / sửa / xoá lịch tự dừng máy ban đêm | vai `hue-rag-…`, lịch `default/hue-rag-…` vùng Singapore |
| `ChuDeEmailCanhBao` + `DangKyEmailVaoChuDe` | tạo chủ đề gửi email cảnh báo, gắn chính sách cho CloudWatch gửi tin vào chủ đề, đăng ký email | chủ đề tên `hue-rag-…`, vùng Singapore |
| `NganSach` | tạo, xem, sửa, xoá ngân sách | ngân sách tên `hue-rag-…` |
| `MayChuMangDiaChiIP` | mọi thao tác máy ảo, mạng, nhóm bảo mật, địa chỉ IP (dựng, dừng, bật, xoá) | chỉ vùng Singapore |
| `BaoDongMayHong` | tạo, xoá báo động "máy hỏng"; đặt TAY trạng thái của nó để thử xem email báo động có tới không (buổi diễn tập ở guide 5) | báo động tên `hue-rag-…` |
| ba khối Session Manager + `XemTrangThai` | mở phiên vào máy mang thẻ `Project = hue-rag`; đóng phiên của chính mình; xem trạng thái và chỉ số `CPUCreditBalance` | theo thẻ của máy (riêng thao tác liệt kê / đọc chỉ số dùng `"*"`) |

Không có: quyền gọi model của AWS, quyền xem tiền, quyền tạo người dùng. Nói thật một giới hạn: chính sách này hẹp theo TÊN tài nguyên và theo vùng, không
phải rào chống leo quyền — người giữ khoá này tạo được vai `hue-rag-…` với quyền tự chọn rồi giao cho một máy. Với một tài khoản cá nhân, một người dùng,
mức này là đủ; lộ khoá thì xoá khoá ngay (mục 10).

**Bước 3 — Tạo nhóm quyền.** IAM ⇒ User groups ⇒ Create group ⇒ tên `HueRagDeploy` ⇒ ở phần gắn chính sách, tìm và tick `HueRagDeployAccess` ⇒ Create group.

**Bước 4 — Tạo người dùng mới và khoá truy cập.** IAM ⇒ Users ⇒ Create user ⇒ tên `hue-rag-deploy` ⇒ KHÔNG tick ô cấp quyền vào trang web (người dùng này chỉ
dùng từ dòng lệnh) ⇒ "Add user to group" ⇒ tick `HueRagDeploy` ⇒ Create user. Mở người dùng vừa tạo ⇒ thẻ "Security credentials" ⇒ Create access key ⇒ chọn
"Command Line Interface (CLI)" ⇒ tạo. Trang hiện hai chuỗi (mã khoá và khoá bí mật) MỘT lần duy nhất — để nguyên trang đó, sang Bước 6 rồi mới đóng.
**Khoá bí mật không dán vào cửa sổ agent nào, không lưu vào file trong thư mục dự án.**

**Bước 5 — Đăng xuất tài khoản gốc** (sau khi xong Bước 6). Từ đây chỉ quay lại tài khoản gốc cho hai việc: xem tiền (guide 1, 7) và sửa quyền khi thiếu.

**Bước 6 — Cất khoá vào một hồ sơ AWS CLI riêng.** Trên máy WSL:

```bash
aws configure --profile hue-rag-deploy
# AWS Access Key ID:      <dán mã khoá>
# AWS Secret Access Key:  <dán khoá bí mật>
# Default region name:    ap-southeast-1
# Default output format:  json
```

**Bước 7 — Kiểm đúng người, đúng vùng.**

```bash
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
aws sts get-caller-identity            # dòng "Arn" phải kết thúc bằng  user/hue-rag-deploy
aws configure get region               # phải in  ap-southeast-1
```

Dòng `Arn` kết thúc bằng `user/aiengineer` nghĩa là chưa chọn hồ sơ. Vùng in ra khác `ap-southeast-1` thì sửa bằng `aws configure set region ap-southeast-1`
— khoá học ghi nhận vùng mặc định lệch là nguồn của nhiều lỗi lúc deploy [khoá].

**Bước 8 — Công cụ trên máy.** Ba thứ đã có sẵn [máy, kiểm 23/11/2026]; thứ tư phải cài:

```bash
terraform version                      # đã có: Terraform v1.17.2 — cần từ 1.17 trở lên
aws --version                          # đã có: aws-cli/2.36.25
docker --version && docker compose version    # đã có: Docker 29.7.2, Compose v5.4.0
session-manager-plugin --version       # CHƯA có trên máy này — cài bằng hai lệnh dưới
```

```bash
# Phần cắm Session Manager cho Ubuntu máy x86_64 — lệnh của trang hướng dẫn AWS [AWS]; tải về thư mục tạm, không tải vào thư mục dự án
cd /tmp && curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o session-manager-plugin.deb
sudo dpkg -i session-manager-plugin.deb && session-manager-plugin --version
```

**Bước 9 — Khoá OpenAI riêng cho bản deploy, có chốt tiền.** Làm trên <https://platform.openai.com> **[chưa chạy]**:

1. Tạo một project riêng tên `hue-rag-deploy` (ô chọn project ở góc trái trên ⇒ Create project). Project riêng thì trần chi tiêu và số liệu sử dụng của bản
   deploy tách khỏi mọi việc khác.
2. Trong project đó ⇒ API keys ⇒ tạo một khoá. Chép khoá vào chỗ cất mật khẩu của riêng mình; nó chỉ được gõ vào HAI file, cả hai do chính bạn tự gõ: file thử
   `~/hue_khoa_thu.env` ở máy mình (guide 2 mục 3 — để thử gói trước khi đưa lên) và `hue.khoa.env` trên máy chủ (guide 4). Không dán khoá vào cửa sổ của agent nào.
   Không dùng lại khoá đang nằm trong `.env` của máy.
3. Đặt TRẦN CỨNG cho project: Project settings ⇒ Limits ⇒ mục Spend ⇒ Edit spend limit ⇒ nhập "Monthly spend limit" ⇒ bật **"Enforce a hard limit"** ⇒ Save.
   Không bật thì con số chỉ là cảnh báo, lời gọi vẫn chạy. Chạm trần thì mọi lời gọi của project trả lỗi 429 mã `project_spend_limit_exceeded` — người dùng
   thấy "Không thể tạo câu trả lời vào lúc này". Trần áp không tức thời, có thể vượt nhẹ [OpenAI].
4. Tiền nạp trước: Billing ⇒ xem số dư. Tài khoản kiểu nạp trước hết tiền thì lời gọi trả lỗi mã `credit_balance_exhausted`. Xem mục **tự nạp lại**
   ("Use auto-reload"): lúc thiết lập nạp tiền nó BẬT sẵn — tắt đi, nếu không số dư sẽ tự được mua thêm khi xuống thấp. Lần mua ít nhất 5 USD [OpenAI].
   Hết tiền nạp cũng KHÔNG ngừng tức thời: trang OpenAI ghi rõ lời gọi còn chạy thêm một lúc, số dư có thể âm nhẹ và phần âm bị trừ vào lần nạp sau [OpenAI]
   ⇒ lớp chặn đứng TRƯỚC hai chốt này là trần lượt mỗi ngày trong chính ứng dụng (guide 4, 6).

Số tiền của trần là việc chủ dự án chọn. Căn cứ để chọn: một câu hỏi trên `gpt-6-luna` tốn khoảng 0,0004–0,002 USD [số đo của nhóm]; gói đang giới hạn 500
lượt mỗi ngày cho cả máy ⇒ ngày nặng nhất khoảng 1 USD. Ví dụ: trần 5 USD một tháng.

Hai lớp chốt này khác nhau ở đâu, và khác AWS ở đâu: OpenAI có chốt CỨNG (hết tiền nạp hoặc chạm trần cứng là ngừng); AWS thì không — ngân sách của AWS chỉ
gửi email (guide 1). Khoá học dạy đúng cặp này ở tuần 1 [khoá]. Một điều ngược với tuần 3 của khoá: ở đó khoá OpenAI chỉ để xem vết chạy của agent và không
tốn tiền; ở hue_rag nó là khoá GỌI MODEL, tốn tiền thật, và vết chạy của agent không được gửi lên OpenAI (code đặt `tracing_disabled=True`).

Vì sao bản deploy dùng MỘT khoá API mà không dùng vai như khoá học dạy cho production: model nằm ngoài AWS nên không có vai nào cấp được quyền gọi. Ba nhược
điểm khoá học nêu cho cách dùng khoá và cách hue_rag chặn: lộ khoá ⇒ khoá chỉ nằm trong một file quyền 600 trên máy chủ, không trong ảnh, không trong git ·
không tự xoay khoá ⇒ khoá riêng cho bản deploy, thu hồi là xong, không ảnh hưởng máy phát triển · bị gọi cạn tiền ⇒ trần lượt trong app + trần cứng của
project + số tiền nạp trước.

## 7. Kiểm

| Lệnh / chỗ nhìn | Phải thấy |
|---|---|
| `AWS_PROFILE=hue-rag-deploy aws sts get-caller-identity` | `Arn` kết thúc `user/hue-rag-deploy` |
| `AWS_PROFILE=hue-rag-deploy aws configure get region` | `ap-southeast-1` |
| `AWS_PROFILE=hue-rag-deploy aws iam list-users` | LỖI "AccessDenied" — đúng: người dùng này không có quyền quản lý người dùng |
| `AWS_PROFILE=hue-rag-deploy aws ec2 describe-vpcs --region ap-southeast-1 --query 'Vpcs[].VpcId'` | một danh sách (có thể rỗng), không lỗi |
| `AWS_PROFILE=hue-rag-deploy aws ec2 describe-vpcs --region us-east-1` | LỖI "UnauthorizedOperation" — đúng: quyền máy chỉ có ở vùng Singapore |
| `session-manager-plugin --version` | một số phiên bản |
| Trang OpenAI, project `hue-rag-deploy` ⇒ Limits | trần tháng có số, "Enforce a hard limit" đang bật; tự nạp lại đang tắt |

Bốn dòng lệnh `aws` trên **[chưa chạy]** — kết quả ghi theo cách chính sách được viết.

## 8. Gỡ lỗi

| Thấy gì | Xem gì | Làm gì |
|---|---|---|
| `Arn` in ra `user/aiengineer` | chưa `export AWS_PROFILE` ở cửa sổ này | gõ lại hai dòng `export` ở mục 5 |
| "Unable to locate credentials" / "InvalidClientTokenId" | khoá chưa cất, hoặc dán thiếu ký tự | chạy lại `aws configure --profile hue-rag-deploy`; vẫn lỗi thì tạo khoá mới ở Bước 4 và xoá khoá cũ |
| Guide 1 hoặc 3 báo "AccessDenied" / "UnauthorizedOperation" ở một thao tác | dòng lỗi in tên quyền bị thiếu (dạng `dịch-vụ:TênThaoTác`) | chép nguyên dòng lỗi cho nhóm ⇒ nhóm thêm quyền vào file chính sách ⇒ bằng tài khoản gốc: IAM ⇒ Policies ⇒ `HueRagDeployAccess` ⇒ Edit ⇒ dán bản mới. Khoá học cũng dặn trước chuyện này: lần dựng đầu có thể lộ quyền thiếu [khoá] |
| `AccessDenied` ở `cloudwatch:PutMetricAlarm`, `cloudwatch:DeleteAlarms` hoặc `cloudwatch:SetAlarmState` (guide 3, 5, 7) | khối `BaoDongMayHong` của tờ quyền giới hạn các thao tác này theo TÊN báo động (`hue-rag-…`); AWS có nhận kiểu giới hạn đó cho báo động hay không thì **[chưa kiểm trên AWS]** | báo nhóm; cách sửa: trong khối `BaoDongMayHong` đổi dòng `Resource` thành `"*"`, rồi dán lại chính sách bằng tài khoản gốc như hàng trên |
| `AccessDenied` ở `scheduler:CreateSchedule` (guide 3) | khối `LichTuDungMayEC2` đang khoanh tài nguyên tới tiền tố `schedule/default/hue-rag-*`; EventBridge Scheduler có thể đòi mức nhóm `schedule/default/*` cho thao tác tạo mới **[chưa kiểm trên AWS]** | báo nhóm; cách sửa: trong khối `LichTuDungMayEC2` đổi `Resource` thành `"arn:aws:scheduler:ap-southeast-1:*:schedule/default/*"`, rồi dán lại chính sách bằng tài khoản gốc |
| Dán chính sách báo lỗi cú pháp | dán thiếu dấu ngoặc đầu / cuối | dán lại cả file, từ dấu `{` đầu tới dấu `}` cuối |
| Trang OpenAI không có ô "Enforce a hard limit" | trang đã đổi so với 23/11/2026 | báo nhóm; trong lúc chờ, chốt cứng còn lại là số tiền nạp trước với tự nạp lại đã tắt |

## 9. Ghi chú chi phí

AWS: 0 đồng — người dùng, nhóm, chính sách, khoá truy cập không tính tiền. OpenAI: chỉ số tiền chủ dự án đã nạp; tạo project và khoá không tính tiền.

## 10. Dọn dẹp

Khi không deploy nữa, hoặc nghi lộ khoá (bằng tài khoản gốc): IAM ⇒ Users ⇒ `hue-rag-deploy` ⇒ Security credentials ⇒ xoá khoá truy cập (nghi lộ: làm NGAY bước
này) ⇒ xoá người dùng ⇒ xoá nhóm `HueRagDeploy` ⇒ xoá chính sách `HueRagDeployAccess`. Trên máy: xoá khối `[hue-rag-deploy]` trong `~/.aws/credentials` và khối
`[profile hue-rag-deploy]` trong `~/.aws/config`. OpenAI: thu hồi khoá = xoá khoá của project `hue-rag-deploy` ở trang API keys; không có nút tạm tắt một khoá, và lưu trữ (archive) cả project thì không
khôi phục được [theo bản tra cứu của nhóm ngày 23/11/2026, phiên B chưa tự mở trang này]. Phần AWS của mục này làm SAU guide 7 (phá hạ tầng) — phá cần chính người dùng này.

## 11. Guide kế

`1_nen_tang.md` — dựng tầng nền gần 0 đồng: ngân sách + email cảnh báo, thùng chứa gói, vai gắn máy.
