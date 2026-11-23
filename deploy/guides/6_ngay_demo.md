# Guide 6 — Vận hành quanh ngày demo: dừng tạm, bật lại, cập nhật, lùi bản, nút khẩn cấp

Viết: 19:54 23/11/2026, phiên C. Dừng / bật ở guide này mới được GIẢ LẬP ở máy chủ dự án bằng cách dừng hẳn rồi bật lại ba hộp (ba hộp tự lên, trả
lời được sau 11–14 giây — `deploy/docker/README.md` mục 5). Dừng / bật MÁY thật, IP tĩnh giữ nguyên, chứng chỉ còn sau khi dừng lâu:
**[chưa kiểm trên AWS]**.

**Hai chuỗi lệnh "cập nhật bản mới" (6.3) và "lùi về bản trước" (6.4) ĐÃ CHẠY TRỌN ở máy chủ dự án, 20:11–20:15 23/11/2026** (một lượt, chép đúng từng
lệnh của guide; ảnh dựng từ main `d8d5c3a`, kho 269 bài): bật lần đầu bằng gói cũ ⇒ sửa tay một dòng `cau_hinh/settings.yaml` ⇒ cập nhật lên gói mới ⇒
lùi về gói cũ. Kết quả: mỗi lần đổi bản băm 7 / 7 OK, chỉ mục 9.533 = 9.533 điểm, ba hộp khoẻ, `/health` `ok`, hộp app chạy đúng ảnh của bản vừa đổi;
trang ngừng phục vụ 36 giây khi cập nhật, 29 giây khi lùi; dòng sửa tay bị gói mới ghi đè (đúng như mục 6.3 báo trước), còn trong `truoc/`, và trở
lại sau khi lùi. GIỚI HẠN của lượt đó: thư mục máy đứng thay thùng S3 và `/srv/hue` · hai gói khác mã bản nhưng CÙNG nội dung ảnh · http cổng 8880,
không HTTPS · khoá OpenAI GIẢ nên câu hỏi chỉ đi tới câu báo "Không thể tạo câu trả lời vào lúc này" (không lời gọi model nào) · máy chủ dự án
nhanh hơn máy `t3a.medium`. Script + đầu ra (riêng tư): `data/x14_deploy_2026-11-23/c_thu_chuoi_6_3/chay.sh`, `chay_ra.txt`.

Từ dùng: **dừng tạm** (stop) = tắt máy nhưng giữ đĩa và IP — đúng chữ đã học là "co về 0 bằng tay" · **khởi động lạnh / làm ấm** = bật máy lại và hỏi
thử trước giờ cần dùng · **phá** (destroy) = xoá hẳn tầng máy chủ · **gói**, **sha**, **hộp**, **hồ sơ**: như guide 2–4.

## 1. Mục tiêu

Biết và làm được sáu việc: dừng tạm sau mỗi buổi · bật lại và kiểm trước giờ demo · cập nhật bản mới · lùi về bản trước · bấm hai nút khẩn cấp · đi hết
danh sách cuối buổi (có dòng "tắt máy").

## 2. Sẽ dựng gì

Không dựng tài nguyên mới. Guide này chỉ đổi TRẠNG THÁI của máy và của ba hộp.

| Trạng thái | Còn gì | Mất gì | Tiền |
|---|---|---|---|
| Máy BẬT | mọi thứ | — | khoảng 0,047 USD / giờ + đĩa + IP |
| Máy DỪNG TẠM | đĩa (ảnh, chỉ mục, chứng chỉ, `hue.env`, `hue.khoa.env`), IP tĩnh, tên trang | mọi cuộc trò chuyện + lịch đang mở | khoảng 7,5 USD / tháng (đĩa + IP) |
| Đã PHÁ tầng máy chủ | tầng nền + gói trong thùng | cả máy; lần sau làm lại guide 3 + guide 4 | gần 0 (tiền lưu gói: vài xu / tháng) |

**Nói thẳng một điều:** dừng, bật, cập nhật hay khởi động lại hộp app đều làm MẤT mọi cuộc trò chuyện và mọi lịch đang mở. Cuộc trò chuyện, lịch đã xếp
và bộ đếm lượt nằm trong bộ nhớ của tiến trình app, không nằm ở cơ sở dữ liệu nào — đây cũng là lý do hệ thống không lên Lambda nếu không sửa lõi. Thẻ
lịch còn trên màn hình người dùng, nhưng lệnh sửa lịch sau đó sẽ được hiểu như câu hỏi thường. Vì vậy: không cập nhật, không khởi động lại giữa buổi demo.

**Câu trả lời sẵn cho "người dùng tăng 100 lần thì nghẽn ở đâu":** (1) một tiến trình app trên một máy 2 CPU — mỗi lượt hỏi chờ model vài giây, nhiều
lượt cùng lúc thì xếp hàng; (2) trạng thái nằm trong bộ nhớ một tiến trình nên không thêm được máy thứ hai nếu chưa dời trạng thái ra ngoài; (3) hạn
mức và tiền của tài khoản OpenAI; (4) trần lượt của app (`HUE_LUOT_TONG_MOI_NGAY`) sẽ chặn trước — cố ý, vì đây là bản demo.

## 3. Điều kiện trước

- Guide 4 xong: ba hộp đã từng chạy và trả lời được một câu thật.
- Trong tay: `instance_id`, `site_name` (đầu ra guide 3), hồ sơ deploy.
- Cho việc cập nhật: gói `<sha mới>` đã ở trong thùng (guide 2).

## 4. File liên quan

| File | Việc |
|---|---|
| `/srv/hue/hue.env` trên máy | tên ảnh đang chạy (`HUE_IMAGE`), tên trang, hai trần lượt |
| `/srv/hue/hue.khoa.env` trên máy | khoá OpenAI |
| `/srv/hue/cau_hinh/settings.yaml` trên máy | cấu hình app: dòng `provider`, các công tắc tính năng |
| `/srv/hue/truoc/` trên máy | bản chép các file của bản TRƯỚC, do bước cập nhật tạo — dùng để lùi |
| `deploy/terraform/2_may_chu/` ở máy mình | nơi lấy `instance_id` (`terraform output -raw instance_id`) |

## 5. Cấu hình

Ở máy mình, đầu mỗi lần làm việc:

```bash
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
aws sts get-caller-identity                                   # NHÌN "Arn": phải kết bằng user/hue-rag-deploy
ID=$(cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu && terraform output -raw instance_id); echo "$ID"
SITE=$(cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu && terraform output -raw site_name); echo "$SITE"
```

Trên máy chủ, lệnh Compose nào cũng có cùng phần đầu — đặt tên tắt cho đỡ gõ (chỉ sống trong cửa sổ lệnh đó):

```bash
sudo -i
cd /srv/hue && dc() { docker compose --env-file hue.env -f compose.yml "$@"; }
```

## 6. Từng bước

### 6.1 Dừng tạm — "co về 0 bằng tay"

Từ máy mình:

```bash
aws ec2 stop-instances --instance-ids "$ID"
aws ec2 wait instance-stopped --instance-ids "$ID"
aws ec2 describe-instances --instance-ids "$ID" --query 'Reservations[0].Instances[0].State.Name' --output text    # mong: stopped
```

Không cần tắt ba hộp trước. Máy KHÔNG tự dừng: không gõ lệnh này thì máy chạy và tính tiền mãi. Ngân sách của tầng nền chỉ là lưới thứ hai — nó cảnh
báo, tới chậm, và không tắt hộ.

### 6.2 Bật lại trước giờ demo — "khởi động lạnh, làm ấm"

Bật TRƯỚC giờ cần dùng ít nhất 30 phút (đề nghị của nhóm; máy thật chưa đo): máy lên trong một hai phút, ba hộp tự lên không cần gõ gì (Docker được
bật sẵn cùng máy; app tự chờ Qdrant), phần thời gian còn lại là để kịp xử lý nếu có gì hỏng.

```bash
aws ec2 start-instances --instance-ids "$ID"
aws ec2 wait instance-status-ok --instance-ids "$ID"          # tự chờ tới khi máy qua hai phép kiểm trạng thái
curl -s "https://$SITE/health"                                # mong: "status":"ok"
```

`/health` chỉ là bước phụ. Phép kiểm THẬT trước giờ demo là một câu hỏi thật và một lượt xếp lịch thật:

```bash
curl -s -N -X POST "https://$SITE/api/chat/stream" -H 'Content-Type: application/json' \
  -d '{"query": "Vé tham quan Đại Nội bao nhiêu?"}' | tail -c 1500
```

rồi mở `https://$SITE` bằng trình duyệt: trang Lên kế hoạch ⇒ xếp một lịch 2 ngày ⇒ đọc thẻ lịch (mỗi điểm có câu tả, bữa trưa / tối có quán) ⇒ gõ một
lệnh sửa lịch. Câu hỏi thật này cũng là phép kiểm rằng khoá OpenAI còn hiệu lực và còn tiền nạp.

IP tĩnh giữ nguyên nên tên trang và chứng chỉ không đổi. Chứng chỉ của Let's Encrypt có hạn; máy dừng lâu thì lúc bật Caddy tự xin lại, có thể mất
thêm một phút và phụ thuộc hạn mức dùng chung của tên dạng `sslip.io` **[chưa kiểm trên AWS]** — thêm một lý do để bật sớm.

### 6.3 Cập nhật bản mới

Làm NGOÀI giờ demo (mất mọi cuộc trò chuyện đang mở). Trước đó: guide 2 với commit mới ⇒ gói `<sha mới>` trong thùng. Vào máy (`aws ssm start-session
--target "$ID"`, rồi hai dòng ở mục 5), sau đó:

```bash
cd /srv/hue && set -a && . ./may.env && set +a
MOI=<sha mới>

# (1) giữ lại bản đang chạy để lùi được
rm -rf truoc && mkdir truoc && cp -a compose.yml Caddyfile nap_chi_muc.sh hue.env cau_hinh truoc/

# (2) tải gói mới, kiểm băm, nạp ảnh mới (ảnh cũ VẪN nằm trong Docker — đừng xoá)
aws s3 cp "s3://$HUE_THUNG/$MOI/" . --recursive
sha256sum -c SHA256SUMS                                       # mọi dòng OK
gunzip -c "app_$MOI.tar.gz" | docker load && rm "app_$MOI.tar.gz"

# (3) trỏ hue.env sang ảnh mới (HUE_SITE và hai trần lượt giữ nguyên)
sed -i "s/^HUE_IMAGE=.*/HUE_IMAGE=hue-rag-app:$MOI/; s/^HUE_GIT_SHA=.*/HUE_GIT_SHA=$MOI/" hue.env && cat hue.env

# (4) hai phép kiểm của guide 4: dòng provider (bước 6) và đủ file bảng (bước 7)
grep -n '^  provider:' cau_hinh/settings.yaml                 # mong: provider: openai
SHA=$MOI                                                      # rồi dán NGUYÊN khối lệnh bước 7 của guide 4 — mong: ĐỦ

# (5) đổi bản: dừng app + cửa vào, nạp chỉ mục của gói mới, bật lại
dc stop caddy app
bash nap_chi_muc.sh                                           # hai số điểm phải BẰNG nhau
dc up -d --wait
```

Rồi hỏi MỘT câu thật từ máy mình như mục 6.2. Trang ngừng phục vụ trong lúc làm bước (5): đo ở máy chủ dự án 36 giây (lùi bản: 29 giây); trên máy
`t3a.medium` sẽ lâu hơn **[chưa kiểm trên AWS]**.

Nếu trước đó đã sửa tay `cau_hinh/settings.yaml` trên máy (tắt một tính năng…): gói mới ghi đè file đó ⇒ sửa lại sau bước (2); bản cũ còn ở `truoc/cau_hinh/`.

### 6.4 Lùi về bản trước

Khi bản mới hỏng: quay về bộ file đã giữ ở `truoc/`. Ảnh cũ vẫn nằm trong Docker của máy; chỉ mục cũ tải lại từ thùng (gói cũ còn ở đó — guide 2 dặn
giữ gói liền trước).

```bash
cd /srv/hue && set -a && . ./may.env && set +a
dc stop caddy app
cp -a truoc/compose.yml truoc/Caddyfile truoc/nap_chi_muc.sh truoc/hue.env .
rm -rf cau_hinh && cp -a truoc/cau_hinh .
CU=$(grep '^HUE_GIT_SHA=' hue.env | cut -d= -f2); echo "lùi về: $CU"
docker image inspect "hue-rag-app:$CU" --format 'ảnh cũ còn: {{.Id}}'
aws s3 cp "s3://$HUE_THUNG/$CU/qdrant.snapshot" .
bash nap_chi_muc.sh
dc up -d --wait
```

Rồi hỏi một câu thật. Lùi CODE ở máy mình (git revert) không tự chạy trên máy chủ: máy chủ chỉ đổi khi làm mục 6.3 hoặc 6.4 — đúng điều khoá học
dặn "đẩy bản mới không tự chạy".

### 6.5 Đổi một dòng cấu hình ngay trên máy (không dựng lại ảnh)

Tắt một tính năng, hoặc đổi model viết: sửa `/srv/hue/cau_hinh/settings.yaml` rồi `dc restart app` (khoảng 13 giây; mất các cuộc đang mở). Đổi số
trong `hue.env` hoặc nội dung `hue.khoa.env`: dùng `dc up -d app` — lệnh `restart` không nạp lại hai file đó.

### 6.6 Hai nút khẩn cấp

**Nút 1 — dừng máy** (trang ngừng ngay, không ai gọi được model qua trang nữa): lệnh `aws ec2 stop-instances` ở mục 6.1. Một dòng, làm được từ máy mình.

**Nút 2 — thu hồi khoá OpenAI** (khi nghi khoá bị lộ hoặc bị dùng ở nơi khác — dừng máy KHÔNG chặn được người đã cầm khoá): trên trang quản lý của
OpenAI vào Organization settings ⇒ chọn dự án của bản deploy ⇒ **API Keys** ⇒ xoá khoá đó (đường bấm theo trang trợ giúp "Managing projects in the API
Platform" của OpenAI, nhóm tra 23/11/2026; chưa ai tự bấm; trang đó không cam kết khoá ngừng dùng được trong bao lâu sau khi xoá ⇒ xoá xong hãy hỏi
một câu trên trang của ta để thấy nó báo lỗi). Sau đó tạo khoá mới (guide 0), sửa `hue.khoa.env` trên máy, `dc up -d app`, hỏi một câu thật. OpenAI
không có nút "tạm tắt" một khoá; lưu trữ (archive) cả dự án OpenAI là KHÔNG khôi phục được — đừng dùng làm nút tạm dừng.

Các lớp chặn tiền, từ nhanh tới chậm: trần lượt trong app (`HUE_LUOT_MOI_NGAY` mỗi địa chỉ, `HUE_LUOT_TONG_MOI_NGAY` cả máy — vượt thì trang trả 429 kèm
lời báo; tức thời) ⇒ dừng máy (một lệnh) ⇒ phía OpenAI: giới hạn chi tiêu cứng của dự án và số tiền nạp trước, không bật tự nạp (guide 0). Hai lớp phía
OpenAI là chốt cuối nhưng KHÔNG tức thời: trang trợ giúp của OpenAI viết "API access may not stop immediately after your credits run out" và số dư
có thể âm một ít; giới hạn cứng của dự án cũng "not instantaneous" (nhóm tự mở hai trang 23/11/2026). Khác với AWS — ngân sách AWS chỉ cảnh báo,
không chặn gì.

### 6.7 Danh sách cuối buổi

- [ ] Đã dừng máy: `aws ec2 stop-instances --instance-ids "$ID"`
- [ ] Đã KIỂM trạng thái: lệnh `describe-instances` ở mục 6.1 in `stopped`
- [ ] Nếu không dùng lại trong vài tuần: cân nhắc phá tầng máy chủ (mục 10 của guide 3) để về gần 0 đồng
- [ ] Xem trang sử dụng của OpenAI: số tiền còn lại khớp với số lượt đã hỏi

Tự dừng máy theo giờ (một lịch hẹn giờ của AWS): TUỲ CHỌN, CHƯA làm — hiện chỉ có danh sách này và ngưỡng ngân sách nhỏ.

### 6.8 Chủ ý thay máy (đổi ảnh hệ điều hành hoặc đoạn lệnh lúc máy bật) — hiếm khi cần

Terraform của tầng máy chủ cố ý bỏ qua thay đổi của ảnh hệ điều hành và của đoạn lệnh lúc bật, để một lần `apply` thường không bao giờ thay máy. Khi
THẬT SỰ muốn một máy mới (ảnh Ubuntu mới hơn, hoặc đã sửa `user_data.sh.tftpl`), nói thẳng với Terraform **[chưa kiểm trên AWS]**:

```bash
export AWS_PROFILE=hue-rag-deploy AWS_REGION=ap-southeast-1
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu
terraform plan -replace=aws_instance.app -out=thay_may.tfplan      # ĐỌC: đúng MỘT máy bị thay (1 to add, 1 to destroy); IP tĩnh chỉ được gắn lại, không bị xoá
terraform apply thay_may.tfplan
```

IP tĩnh giữ nguyên nên `site_name` không đổi. Máy mới là máy TRỐNG: làm lại guide 4 từ bước 1 (tải gói, hai file `hue*.env`, nạp chỉ mục, bật, hỏi
một câu thật); chứng chỉ HTTPS được xin lại. Mất mọi thứ trên đĩa máy cũ.

## 7. Kiểm

| Việc | Kiểm bằng | Mong |
|---|---|---|
| Dừng tạm | `describe-instances … State.Name` | `stopped`; trang không mở được |
| Bật lại | `curl -s https://$SITE/health` rồi một câu hỏi thật + một lượt xếp lịch | `"status":"ok"`; câu trả lời có nguồn; lịch đủ câu tả |
| Cập nhật | trên máy: `dc ps` và `grep HUE_IMAGE hue.env`; từ ngoài: một câu hỏi thật | ba hộp khoẻ; đúng `<sha mới>` |
| Lùi | như trên | đúng `<sha cũ>` |

## 8. Gỡ lỗi

| Thấy gì | Vì sao | Làm gì |
|---|---|---|
| Bật máy xong `/health` không trả lời | hộp chưa lên xong, hoặc Docker không tự bật | chờ một phút; vào máy: `systemctl is-active docker` (mong `active`), `dc ps`, `dc up -d --wait` |
| `/health` `ok` nhưng câu hỏi ra "Không thể tạo câu trả lời vào lúc này" | khoá OpenAI hết tiền / bị thu hồi | trang quản lý OpenAI; mục 6.6 nút 2 |
| Trình duyệt báo chứng chỉ sau khi dừng lâu | Caddy đang xin lại chứng chỉ, hoặc bị từ chối vì hạn mức | `dc logs --tail 50 caddy`; chờ vài phút; guide 4 mục 8 |
| Sau cập nhật `nap_chi_muc.sh` báo số điểm lệch | bản chụp và ảnh không cùng một lần dựng (tải thiếu file, hoặc `hue.env` chưa trỏ ảnh mới) | xem lại bước (2), (3) của 6.3; không được thì lùi (6.4) |
| Sau cập nhật app không lên | cấu hình mới trỏ tới file bảng ảnh không có | bước 7 của guide 4; lùi (6.4) rồi làm lại guide 2 |
| Đĩa đầy | giữ quá nhiều ảnh cũ | `docker image ls hue-rag-app`; xoá ảnh cũ HƠN bản liền trước: `docker image rm hue-rag-app:<sha>` |
| `stop-instances` / `start-session` báo `AccessDenied` | sai hồ sơ | `aws sts get-caller-identity` |

## 9. Ghi chú chi phí

- Bật 60–100 giờ một tháng: khoảng 10–12 USD; bật liên tục: khoảng 41,95 USD; dừng tạm cả tháng: khoảng 7,5 USD (giá Singapore, phiên B mở bảng giá
  AWS ngày 23/11/2026). So với ba con số đã học ở khoá: Lambda gần 0, App Runner 5–6, ECS kèm cân bằng tải 16–20 USD / tháng — ở đây không chọn Lambda
  vì phải sửa lõi (guide 3 mục 2).
- Phá tầng máy chủ, giữ tầng nền: còn tiền lưu gói trong thùng — mỗi gói khoảng 1 GB, vài xu một tháng.
- Mỗi lần "làm ấm" tốn hai ba lời gọi model: vài xu.

## 10. Dọn dẹp

- Sau khi bản mới chạy ổn vài ngày: trên máy `rm -rf /srv/hue/truoc` và xoá ảnh cũ hơn bản liền trước; ở thùng xoá gói cũ hơn bản liền trước (guide 2
  mục 10).
- Hết đợt demo: phá tầng máy chủ (guide 3 mục 10); phá sạch cả hai tầng có kiểm: guide 7.

## 11. Guide kế

`7_pha_sach.md` — phá cả hai tầng theo sáu bước có kiểm.
