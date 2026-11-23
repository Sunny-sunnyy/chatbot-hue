# Guide 4 — Bật lần đầu trên máy chủ: tải gói, đặt khoá OpenAI, bật ba hộp, hỏi một câu thật

Viết: 19:50 23/11/2026, phiên C. Các lệnh `sha256sum`, `docker load`, `nap_chi_muc.sh`, `docker compose … up` ở guide này ĐÃ chạy thật ở máy chủ dự án
(lượt thử trọn gói 23/11 — `deploy/docker/README.md` mục 5). Chạy chúng trên máy AWS, tải gói bằng vai gắn máy, HTTPS thật và câu hỏi thật qua model
của OpenAI: **[chưa kiểm trên AWS]** — buổi diễn tập của guide 5 đổi các dòng đó thành "đã kiểm".

Từ dùng: **hộp** = container · **gói** = bộ file guide 2 đã đẩy lên thùng · **vai gắn máy** = quyền AWS gắn vào máy, máy tự xin khoá tạm · **máy chủ web /
cửa vào** = hộp Caddy, đứng trước app, nhận mọi yêu cầu từ internet · **chứng chỉ** = thứ để trình duyệt tin trang `https://…` · **chỉ mục** = dữ liệu
tìm kiếm của kho, nằm trong hộp Qdrant.

## 1. Mục tiêu

Trang `https://<site_name>` mở được từ máy bất kỳ, và MỘT câu hỏi thật được trả lời có nguồn bằng model của OpenAI.

## 2. Sẽ dựng gì

Trên máy, trong thư mục `/srv/hue`:

| Thứ | Từ đâu | Bí mật? |
|---|---|---|
| Bảy file của gói + `SHA256SUMS` | tải từ thùng | riêng tư (ảnh mang file bảng) |
| `hue.env` | tự gõ ở bước 4 | không |
| `hue.khoa.env` (quyền 600) | tự gõ ở bước 5 | **CÓ — khoá OpenAI** |
| Ba hộp: `qdrant` (chỉ mục) · `app` (trợ lý + giao diện) · `caddy` (cửa vào, HTTPS) | `docker compose` | — |
| Thư mục `qdrant_storage/`, `logs/` và một volume chứa chứng chỉ | hộp tự tạo | không |

**Lớp đứng trước ứng dụng — giảng từ đầu** (ở khoá học phần này do App Runner / CloudFront / Function URL lo hộ, chưa lần nào phải tự dựng):

- App (FastAPI) chỉ nghe ở cổng 8000 BÊN TRONG mạng riêng của Docker; không ai từ internet tới thẳng được.
- Hộp **Caddy** là máy chủ web đứng trước: nghe cổng 80 và 443 của máy, chuyển yêu cầu vào app, cắt yêu cầu quá 12 MB (trả 413), nén trang nhưng
  KHÔNG nén luồng câu trả lời để chữ ra ngay.
- **Chứng chỉ HTTPS** do Caddy TỰ xin từ tổ chức cấp chứng chỉ miễn phí Let's Encrypt lúc bật lần đầu: tổ chức đó gọi ngược vào cổng 80 / 443 của máy
  để kiểm rằng máy đúng là chủ của cái tên. Vì vậy cần ba thứ cùng đúng: tên trỏ về IP tĩnh của máy, nhóm bảo mật mở 80 và 443 (guide 3), và biến
  `HUE_SITE` đúng tên.
- **Cái tên lấy ở đâu khi không có tên miền:** dịch vụ công cộng `sslip.io` biến tên `13-250-1-2.sslip.io` thành địa chỉ `13.250.1.2`. Đầu ra `site_name`
  của guide 3 đã ghép sẵn tên này từ IP tĩnh.
- Mất bao lâu: thường vài giây tới một phút sau khi hộp Caddy lên **[chưa kiểm trên AWS]**. Chứng chỉ được cất trong volume `caddy_data` nên dừng /
  bật máy không phải xin lại.
- Hỏng thì thấy gì: trình duyệt báo "kết nối không riêng tư" hoặc không mở được trang ⇒ `docker compose --env-file hue.env -f compose.yml logs caddy`
  có dòng lỗi xin chứng chỉ (mục 8).

**Vì sao khoá nằm trong một file quyền 600 chứ không dùng Secrets Manager:** chỉ có một máy và một khoá; file do chính chủ dự án gõ trên máy nên khoá
không đi qua git, không đi qua gói, không nằm trong state Terraform; và đỡ một dịch vụ phải giải thích. Khoá học cũng giữ khoá OpenAI theo đúng lối
này: là biến môi trường của dịch vụ chạy máy chủ, không trong code, không ở giao diện.

## 3. Điều kiện trước

- Guide 2 xong: gói `<sha>` nằm trong thùng. Guide 3 xong: máy `Online`, mục Kiểm của guide 3 đạt.
- Trong tay: `instance_id` và `site_name` (đầu ra của guide 3), `<sha>` của gói, khoá OpenAI riêng của bản deploy (guide 0) — đã nạp trước một số tiền
  nhỏ, không bật tự nạp.
- Khoá OpenAI tự gõ / tự dán trong cửa sổ lệnh của máy chủ; không dán vào cửa sổ của agent nào, không ghi vào file nào trong repo.

## 4. File liên quan

| File (trong `/srv/hue` trên máy) | Việc |
|---|---|
| `compose.yml` | khai ba hộp, các trần, thứ tự chờ nhau; tên dự án Compose cố định là `hue` |
| `Caddyfile` | cấu hình cửa vào |
| `nap_chi_muc.sh` | nạp bản chụp chỉ mục vào hộp Qdrant và so số điểm |
| `cau_hinh/settings.yaml` | cấu hình app thật sự đọc (gói đã ghi sẵn `provider: openai`) |
| `may.env` | tên thùng + vùng, do máy tự ghi lúc bật lần đầu |
| `hue.env`, `hue.khoa.env` | tự gõ ở guide này |

Ba loại file giá trị của cả bộ deploy — đừng lẫn: `.env` (code ở máy mình, không lên máy chủ) · `terraform.tfvars` (Terraform, ở máy mình) ·
`hue.env` + `hue.khoa.env` (chỉ có trên máy chủ).

## 5. Cấu hình

`hue.env` — KHÔNG bí mật:

| Biến | Giá trị | Ghi chú |
|---|---|---|
| `HUE_IMAGE` | `hue-rag-app:<sha>` | tên ảnh vừa nạp |
| `HUE_SITE` | `<site_name>` của guide 3, ví dụ `13-250-1-2.sslip.io` | có tên miền riêng thì điền tên miền (đã trỏ về IP tĩnh) |
| `HUE_GIT_SHA` | `<sha>` | ghi vào log; ảnh không có git |
| `HUE_LUOT_MOI_NGAY` | 50 (mặc định) | lượt gọi model mỗi địa chỉ mỗi ngày |
| `HUE_LUOT_TONG_MOI_NGAY` | 500 (mặc định) | trần tổng cả máy mỗi ngày |
| `HUE_TRA_WEB` | `false` (mặc định) | bật thì phải có `SERPER_API_KEY` |

`hue.khoa.env` — BÍ MẬT, quyền 600: dòng `OPENAI_API_KEY=…` (bắt buộc). Chỉ khi dùng: `SERPER_API_KEY=…` (tra web), `HUE_KHOA_THEO_DOI=…` (từ 16 ký
tự; mở trang theo dõi `#/theo-doi` — không đặt thì trang đó trả 404).

Hai con số trần lượt là lớp chặn hằng ngày của app. Chốt về tiền nằm ở phía OpenAI: số tiền nạp trước (không bật tự nạp) và giới hạn chi tiêu cứng
của dự án OpenAI (guide 0). Cả hai KHÔNG ngắt tức thời — trang trợ giúp của OpenAI (nhóm tự mở 23/11/2026) viết API có thể chưa ngừng ngay khi hết
tiền nạp và số dư có thể âm một ít — nên trần lượt trong app vẫn là lớp chặn đứng trước.

## 6. Từng bước

Thứ tự là BẮT BUỘC: kiểm băm ⇒ nạp ảnh ⇒ `hue.env` ⇒ `hue.khoa.env` ⇒ kiểm dòng `provider` ⇒ kiểm đủ file bảng ⇒ nạp chỉ mục ⇒ bật ⇒ hỏi một câu thật.

**Bước 1 — vào máy** (từ máy mình):

```bash
export AWS_PROFILE=hue-deploy AWS_REGION=ap-southeast-1
aws sts get-caller-identity                      # NHÌN "Arn": người dùng IAM của việc deploy
ID=$(cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu && terraform output -raw instance_id); echo "$ID"
cd /home/minhhieu/hue_rag/deploy/terraform/2_may_chu && terraform output -raw site_name; echo      # ghi lại: đây là <site_name> dùng ở bước 4 và bước 10
aws ssm start-session --target "$ID"
```

Trong cửa sổ lệnh của máy:

```bash
sudo -i
cd /srv/hue
set -a; . ./may.env; set +a                      # có biến HUE_THUNG và AWS_DEFAULT_REGION
```

Phiên Session Manager để yên lâu thì tự ngắt. Mở lại phiên giữa chừng ⇒ gõ lại ba dòng trên và dòng `SHA=<sha>` của bước 2 (biến chỉ sống trong
cửa sổ lệnh), rồi làm tiếp từ bước đang dở — các bước đã xong không phải làm lại.

**Bước 2 — tải gói và kiểm băm.** Máy tải bằng khoá tạm của vai gắn máy; không có khoá AWS nào cần gõ.

```bash
cd /srv/hue
aws s3 ls "s3://$HUE_THUNG/"                     # thấy thư mục <sha>/
SHA=<sha>
aws s3 cp "s3://$HUE_THUNG/$SHA/" . --recursive
sha256sum -c SHA256SUMS                          # mong: 7 dòng, dòng nào cũng "OK"
```

Có dòng `FAILED` ⇒ DỪNG: tải lại; vẫn lệch thì gói trong thùng hỏng, làm lại guide 2.

**Bước 3 — nạp ảnh app** (khoảng một hai phút; file nén gần 1 GB, ảnh sau khi nạp 3,6 GB):

```bash
cd /srv/hue
gunzip -c "app_$SHA.tar.gz" | docker load        # mong dòng cuối: Loaded image: hue-rag-app:<sha>
rm "app_$SHA.tar.gz"                             # không còn cần; trả lại gần 1 GB đĩa
```

**Bước 4 — viết `hue.env`** (thay `<site_name>`):

```bash
cd /srv/hue
cat > hue.env <<EOF
HUE_IMAGE=hue-rag-app:$SHA
HUE_SITE=<site_name>
HUE_GIT_SHA=$SHA
EOF
cat hue.env
```

**Bước 5 — viết `hue.khoa.env`, quyền 600.** Dùng `nano` (không dùng `echo` — lệnh `echo` để lại khoá trong lịch sử lệnh):

```bash
cd /srv/hue
install -m 600 /dev/null hue.khoa.env            # tạo file rỗng đã ở quyền 600 TRƯỚC khi có khoá trong đó
nano hue.khoa.env                                # gõ đúng một dòng: OPENAI_API_KEY=<khoá>   rồi Ctrl+O, Enter, Ctrl+X
ls -l hue.khoa.env                               # mong: -rw------- 1 root root
grep -c '^OPENAI_API_KEY=' hue.khoa.env          # mong: 1   (lệnh này KHÔNG in khoá)
```

**Bước 6 — kiểm dòng model viết.** Gói đã ghi sẵn; ở đây chỉ KIỂM, không sửa:

```bash
grep -n '^  provider:' /srv/hue/cau_hinh/settings.yaml      # mong: provider: openai
```

**Bước 7 — kiểm đủ file bảng trước khi bật.** Cấu hình trỏ tới chín file bảng nằm trong ảnh; thiếu một file là hộp app hỏng ngay lúc khởi động —
lỗi mà `terraform validate` lẫn `/health` đều không thấy trước.

```bash
cd /srv/hue
docker run --rm --network none -v "$PWD/cau_hinh:/c:ro" --entrypoint sh "hue-rag-app:$SHA" -c '
  cd /app/backend; t=0
  for f in $(grep -o "\.\./data/[^\"[:space:]]*" /c/settings.yaml | sort -u); do
    [ -e "$f" ] || { echo "THIẾU trong ảnh: $f"; t=1; }
  done
  [ "$t" = 0 ] && echo "ĐỦ: mọi file bảng mà cấu hình trỏ tới đều có trong ảnh"; exit $t'
```

Mong: `ĐỦ: …`. (Lệnh này đã thử thật ở máy chủ dự án 23/11: cấu hình đúng của ảnh ⇒ `ĐỦ`; cấu hình của một commit mới hơn ảnh ⇒ in đúng năm file thiếu.)
In `THIẾU` ⇒ DỪNG: ảnh và cấu hình không cùng một commit — làm lại guide 2.

**Bước 8 — nạp chỉ mục.** Gọi bằng `bash` (file chép qua thùng mất quyền chạy):

```bash
cd /srv/hue
bash nap_chi_muc.sh
```

Lần đầu máy phải kéo ảnh Qdrant từ Docker Hub (vài chục giây). Mong dòng cuối: `chỉ mục trong Qdrant của gói: N điểm · bản ghi dựng trong ảnh: N điểm` —
hai số BẰNG nhau (kho ngày 23/11: 9.533). Lệch ⇒ lệnh tự dừng.

**Bước 9 — bật ba hộp:**

```bash
cd /srv/hue
docker compose --env-file hue.env -f compose.yml up -d --wait
docker compose --env-file hue.env -f compose.yml ps          # mong: ba hộp, cột STATUS đều có chữ healthy / running
```

`up --wait` chỉ trả về khi hộp app báo khoẻ (khoảng 15–40 giây: app nạp thư viện và chờ Qdrant). Báo lỗi ⇒ mục 8.

**Bước 10 — BẮT BUỘC: hỏi MỘT câu thật.** `up --wait` xanh KHÔNG có nghĩa là trả lời được: app chỉ kiểm CÓ dòng `OPENAI_API_KEY`, không kiểm khoá
DÙNG ĐƯỢC. Khoá gõ sai, khoá bị thu hồi, tài khoản hết tiền đều cho ba hộp khoẻ và `/health` `ok` — trong khi mọi câu hỏi ra "Không thể tạo câu trả
lời vào lúc này". Từ MÁY MÌNH (một cửa sổ lệnh khác, không phải trong máy chủ):

```bash
curl -s https://<site_name>/health                           # mong: {"status":"ok", … "generator":"ready"}
curl -s -N -X POST https://<site_name>/api/chat/stream -H 'Content-Type: application/json' \
  -d '{"query": "Vé tham quan Đại Nội bao nhiêu?"}' | tail -c 1500
```

Mong: chữ của câu trả lời có giá vé và phần nguồn. Câu thật đầu tiên có thể chậm hoặc hỏng một lần — thử lại MỘT lần rồi mới sang gỡ lỗi (ở khoá học
lượt đầu sau deploy cũng từng hỏng rồi lần hai mới được). Sau đó mở `https://<site_name>` bằng trình duyệt: ổ khoá HTTPS hợp lệ, hỏi một câu, chữ CHẠY
DẦN ra; rồi sang guide 5 để kiểm đủ từ ngoài (xếp lịch, sửa lịch, tải file, hỏi bằng ảnh).

Thoát máy: `exit` (thoát root) rồi `exit` (thoát phiên). Ba hộp vẫn chạy.

## 7. Kiểm

| Kiểm | Lệnh / thao tác | Mong |
|---|---|---|
| Ba hộp khoẻ | trên máy: `docker compose --env-file hue.env -f compose.yml ps` | `qdrant`, `app`, `caddy` đều `healthy` / `running` |
| App sẵn sàng | từ máy mình: `curl -s https://<site_name>/health` | `"status":"ok"`, năm thành phần `ready` / `alive` |
| Chứng chỉ thật | mở trang bằng trình duyệt | ổ khoá hợp lệ, không cảnh báo |
| Trả lời được | bước 10 | câu trả lời có nguồn, không phải "Không thể tạo câu trả lời vào lúc này" |
| Trang tài liệu API đã tắt | `curl -s -o /dev/null -w '%{http_code}\n' https://<site_name>/docs` | 404 |
| File khoá kín | trên máy: `ls -l /srv/hue/hue.khoa.env` | `-rw-------` |
| Cổng app không mở ra ngoài | từ máy mình: `curl -m 5 http://<public_ip>:8000/health` | không kết nối được |

`/health` của app không in tên model. Muốn biết máy đang chạy model nào: `grep -n '^  provider:' /srv/hue/cau_hinh/settings.yaml` trên máy.

## 8. Gỡ lỗi

Lệnh xem log (trên máy, trong `/srv/hue`; log mỗi hộp xoay 3 file × 10 MB — khác khoá học: không có gì ở CloudWatch, xem thẳng trên máy):
`docker compose --env-file hue.env -f compose.yml logs --tail 80 app` (thay `app` bằng `caddy` / `qdrant`).

| Thấy gì | Vì sao | Làm gì |
|---|---|---|
| `aws s3 ls` báo `AccessDenied` | vai gắn máy thiếu quyền đọc thùng, hoặc `HUE_THUNG` sai | `cat may.env`; so tên thùng với đầu ra của tầng nền; quyền của vai sửa ở `1_nen_tang` |
| `sha256sum` có dòng `FAILED` | tải dở / gói hỏng | tải lại; còn lệch ⇒ làm lại guide 2 |
| `up --wait` báo lỗi, `/health` `degraded`, `generator: not_ready` | thiếu dòng `OPENAI_API_KEY`, hoặc dòng `provider` không phải `openai` | bước 5, bước 6; sửa file khoá xong dùng `docker compose --env-file hue.env -f compose.yml up -d app` (lệnh `restart` KHÔNG nạp lại file khoá) |
| Mọi thứ xanh mà câu nào cũng "Không thể tạo câu trả lời vào lúc này" | khoá sai / bị thu hồi / hết tiền nạp | trang quản lý OpenAI: khoá còn hiệu lực không, còn tiền không; sửa `hue.khoa.env`, `up -d app` |
| Log app lặp "chờ Qdrant có collection…" | chưa nạp chỉ mục | bước 8 |
| Hộp app chết ngay khi bật, log có `FileNotFoundError … ../data/…` | ảnh và cấu hình lệch nhau | bước 7; làm lại guide 2 |
| Trình duyệt báo chứng chỉ không hợp lệ / không mở được trang | `HUE_SITE` sai tên; tên không trỏ về IP tĩnh; cổng 80 / 443 chưa mở; hoặc tổ chức cấp chứng chỉ tạm từ chối | `docker compose … logs caddy`; `nslookup <site_name>` phải ra IP tĩnh; nhóm bảo mật ở guide 3. Tên dạng `sslip.io` dùng CHUNG hạn mức cấp chứng chỉ với mọi người dùng dịch vụ đó — bị từ chối vì hết hạn mức thì chờ, hoặc dùng tên miền riêng **[hai bản nghiên cứu khác hãng nêu, chưa kiểm]** |
| Trang mở được nhưng hỏi đáp báo hết lượt (429) | chạm `HUE_LUOT_MOI_NGAY` / `HUE_LUOT_TONG_MOI_NGAY` | đổi số trong `hue.env` rồi `up -d app` (mất các cuộc trò chuyện đang mở) |
| Chữ không chạy dần mà hiện cả câu một lần | cửa vào đang gom luồng | dòng `flush_interval -1` của `Caddyfile` phải còn nguyên |
| Sửa `cau_hinh/settings.yaml` xong app không lên | bộ nạp cấu hình kiểm chặt | lấy lại bản gốc: `docker run --rm --entrypoint cat hue-rag-app:$SHA /app/backend/config/settings.yaml > cau_hinh/settings.yaml` rồi ghi lại dòng `provider: openai` (bản trong ảnh ghi `bedrock`) |

Đừng dán đầu ra của `docker compose config` vào đâu cả: lệnh đó in cả nội dung `hue.khoa.env`.

## 9. Ghi chú chi phí

- Máy đang bật: khoảng 0,047 USD / giờ + đĩa + IP (bảng ở guide 3).
- Mỗi câu hỏi gọi model của OpenAI, trừ vào số tiền nạp trước. Hai trần lượt trong `hue.env` giới hạn số lượt mỗi ngày. Hết tiền nạp thì lời gọi nhận
  lỗi 429 (`credit_balance_exhausted`) và người dùng thấy "Không thể tạo câu trả lời vào lúc này".
- Tải gói từ thùng về máy cùng vùng: không tính tiền lưu lượng.

## 10. Dọn dẹp

Tắt ba hộp mà giữ máy (chỉ mục, chứng chỉ, hai file `hue*.env` còn nguyên):

```bash
cd /srv/hue && docker compose --env-file hue.env -f compose.yml down
```

KHÔNG dùng `down -v`: cờ `-v` xoá luôn volume chứa chứng chỉ. Dừng máy cho đỡ tiền: guide 6. Phá hẳn máy: mục 10 của guide 3.

**Khi dựng lại máy từ đầu** (đã phá tầng `2_may_chu` rồi `apply` lại) phải gõ lại: tải gói + nạp ảnh (bước 2–3) · `hue.env` (bước 4 — `HUE_SITE` đổi
nếu IP tĩnh là IP mới) · `hue.khoa.env` (bước 5) · nạp chỉ mục + bật (bước 8–9) · rồi hỏi một câu thật (bước 10).

## 11. Guide kế

`5_kiem_va_go_loi.md` — danh sách kiểm từ ngoài + buổi diễn tập. `6_ngay_demo.md` — dừng tạm, bật lại, cập nhật, lùi bản, nút khẩn cấp.
