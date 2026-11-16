# Spec bản 1: deploy chatbot Huế lên AWS (một máy Lightsail, Docker Compose)

E viết bản 1, xong lúc 14:36 16/11/2026, theo việc A giao (User 16/11: mọi việc local và kế hoạch deploy phải xong trước 30/11; từ tháng 12 Codex / Gemini làm tiếp).
**Chỉ là tài liệu.** Viết spec này không tạo tài nguyên AWS nào và không gọi AWS. Reviewer: C. Trạng thái: **NHÁP, chờ review vòng 1, chưa duyệt.**

## 0. Cách dùng tài liệu này (đọc trước khi chạy bất kỳ lệnh nào)

- Người chạy (Codex, Gemini, hay người) làm **đúng thứ tự** từ §5 đến §10. Mỗi bước có bốn phần:
  **Lệnh** (chép nguyên, chỉ thay biến `<…>` ở §4) · **Kiểm** (lệnh để xem kết quả) · **Mong đợi** (kết quả đúng phải trông thế nào) ·
  **Dừng khi** (gặp thì dừng hẳn, không sửa đoán, báo User kèm đầu ra).
- **Không tự phán đoán.** Lệnh lỗi hoặc kết quả khác "Mong đợi" mà bước không ghi cách xử lý ⇒ dừng và báo. Không thêm cờ, không đổi cổng,
  không chạy lại với `--force` / `sudo` khác bản ghi, không xoá gì ngoài đúng lệnh có trong tài liệu.
- Bước có nhãn **[User]** thì chỉ User làm (tài khoản, thẻ, tên miền, khoá). Người chạy chỉ đưa lệnh và chờ.
- Bước có nhãn **[Tiền]** là bước bắt đầu tính tiền AWS. Trước bước đó phải có câu trả lời "đồng ý" của User cho mục Q1 ở §3.
- **Không bao giờ** in, `cat` hay dán nội dung file khoá (`.env`, `.env.deploy`, khoá SSH) vào hội thoại, log hay commit. Chỉ kiểm bằng
  "có / không có tên biến" (lệnh ở từng bước).
- Ảnh Docker của app **chứa kho dữ liệu private** (kho bài viết, bảng điểm). Không đẩy ảnh lên Docker Hub / ECR công khai, không đẩy lên GitHub.
  Chỉ chuyển thẳng từ máy User sang máy AWS bằng `scp`.

Nhãn bằng chứng trong tài liệu: **[Đo]** = đã chạy hoặc đo thật (ghi ngày) · **[Đọc]** = đọc code / cấu hình · **[Nguồn]** = trang công khai (có URL,
ngày tra) · **[Suy]** = suy luận, chưa kiểm.

## 1. Mục tiêu và phạm vi

- **Mục tiêu:** một địa chỉ `https://…` công khai để User demo và hội đồng chấm thử chatbot, chạy khoảng 12/2026–02/2027. Lượng người dùng nhỏ:
  1 người demo + vài chục lượt chấm.
- **Trong phạm vi:** đóng gói (đã có Docker nháp `data/phase_12/deploy_nhap/`), chọn máy, tạo máy, HTTPS, khoá, sao lưu, log, giới hạn lượt,
  cập nhật bản mới, quay lại bản cũ, tắt máy khi hết demo.
- **Ngoài phạm vi:** nhiều máy, tự co giãn, CI/CD tự động, Kubernetes, cơ sở dữ liệu quản lý (RDS), CDN. Không cần cho vài chục người dùng.

## 2. Phương án chọn và vì sao

**Chọn: một máy Amazon Lightsail Linux 4 GB RAM (x86, Ubuntu 24.04, vùng Singapore `ap-southeast-1`)**, chạy 3 container bằng Docker Compose:
`qdrant` (cơ sở dữ liệu vector) + `app` (FastAPI) + `caddy` (HTTPS, tự xin chứng chỉ Let's Encrypt). Đây đúng là bộ đã chạy thử trên máy User.

| Số đo dùng để chọn | Giá trị | Nhãn |
|---|---|---|
| RAM tiến trình app (server thật, cổng 8010, sau nhiều lượt) | đỉnh 1.450 MB, lúc đo 1.306 MB | [Đo] 16/11 (`VmHWM` / `VmRSS`) |
| RAM app trong container lúc thử deploy cục bộ | 939 MiB (giới hạn compose 2 GiB) | [Đo] 10/11 (`docker stats`, report B) |
| RAM Qdrant | 178 MiB (16/11) · 230–378 MiB (07–10/11) | [Đo] |
| RAM Caddy | 18 MiB | [Đo] 10/11 |
| Dữ liệu Qdrant | 55 MB (collection `hue_full_corpus_7a2_e5_small_384`, 9.425 điểm) | [Đo] 16/11 `du -sh qdrant_storage` |
| Ảnh Docker app | 3,57 GB (bản 10/11) | [Đo] 10/11 |
| Kiến trúc CPU của ảnh | x86-64 (build trên máy WSL của User) | [Đọc] |

Cộng lại: app ~1,5 GB + Qdrant ~0,4 GB + Caddy + hệ điều hành và Docker ~0,6 GB [Suy] ≈ **2,5 GB** ⇒ gói 2 GB quá sát (có lúc hết RAM là
app bị tắt), gói **4 GB** còn dư khoảng 1,5 GB.

| Phương án | Giá / tháng (Singapore) | Vì sao không chọn |
|---|---|---|
| **Lightsail 4 GB** (chọn) | 24 USD, gồm 80 GB SSD, 4 TB truyền dữ liệu, IPv4 | [Nguồn] tra 07/11, đang tra lại 16/11 (§12). Giá cố định, dễ dự trù; ít khái niệm (không VPC, EBS, security group riêng) ⇒ người chạy ít chỗ sai |
| Lightsail 2 GB | 12 USD | thiếu RAM như phép cộng trên |
| EC2 t3.medium (4 GiB) | ~38 USD + đĩa EBS + IPv4 ~3,65 USD | đắt hơn, nhiều bước hơn (VPC, security group, EBS); không có lợi gì cho vài chục người dùng |
| EC2 t4g.medium (ARM, 4 GiB) | ~31 USD + đĩa + IPv4 | rẻ hơn t3 nhưng là máy ARM ⇒ phải build lại ảnh cho ARM (torch, ảnh node / python), chưa thử |
| ECS Fargate / App Runner / Lightsail container service | tính theo vCPU + RAM liên tục, thường > 24 USD cho 4 GB; cần đẩy ảnh lên registry (ECR) | ảnh chứa kho private ⇒ phải dùng ECR riêng tư + IAM; Qdrant cần đĩa bền ⇒ thêm EFS. Phức tạp hơn nhiều so với nhu cầu |

**Khi nào phương án này sai:** (a) lượng người dùng tăng lên hàng trăm cùng lúc (một tiến trình uvicorn, giới hạn lượt trong RAM); (b) cần chạy
liên tục nhiều năm với cập nhật thường xuyên (lúc đó nên có CI/CD + registry riêng tư); (c) AWS đổi giá / bỏ gói. Ba điều này không đúng với demo 2–3 tháng.

## 3. Câu cần User quyết (gom một chỗ — A hỏi từng câu bằng hộp chọn)

| # | Câu | Mặc định đề xuất | Hệ quả nếu chọn khác |
|---|---|---|---|
| Q1 | Có tạo tài khoản AWS (hoặc dùng tài khoản có sẵn) và chấp nhận ~24 USD / tháng cho máy (thêm ~1–2 USD sao lưu) trong 2–3 tháng không | Có, gói 4 GB | Gói 2 GB rẻ hơn 12 USD nhưng dễ hết RAM; không có AWS ⇒ demo chạy trên máy User. Tài khoản mới: 100 USD credit (thêm tối đa 100 USD qua hoạt động); Free plan hết sau 6 tháng hoặc hết credit — chưa nâng lên Paid thì tài khoản bị đóng, dữ liệu giữ 90 ngày ⇒ **nâng lên Paid plan trước buổi chấm**; chưa có nguồn xác nhận gói 4 GB tạo được trên Free plan [Nguồn] docs.aws.amazon.com free-tier-plans, tra 16/11 |
| Q2 | Tên miền: mua tên miền riêng (~10–15 USD / năm, User tự mua) hay dùng `<IP>.sslip.io` miễn phí | `sslip.io` để thử; **tên miền riêng cho buổi chấm** | sslip.io miễn phí nhưng mọi người dùng chung một hạn mức chứng chỉ Let's Encrypt (50 chứng chỉ / tên miền / 7 ngày; sslip.io không nằm trong Public Suffix List — một báo lỗi 09/02/2026 cho thấy từng hết hạn mức) ⇒ ngày chấm có thể không xin được chứng chỉ [Nguồn] letsencrypt.org/docs/rate-limits + issue sslip.io #108, tra 16/11. Tên miền riêng thêm một bước trỏ DNS (bản ghi A ⇒ `<IP>`) |
| Q3 | Khoá OpenAI riêng cho bản công khai, có đặt giới hạn chi tiêu (User tạo ở trang OpenAI) | Có: project riêng ở OpenAI ⇒ Limits ⇒ Monthly spend limit ~5 USD + **bật "Enforce a hard limit"** (không bật thì chỉ cảnh báo, request vẫn chạy; áp không tức thời, có thể vượt nhẹ) [Nguồn] help.openai.com "Managing projects", tra 16/11 | Dùng chung khoá máy User ⇒ người ngoài dùng hết hạn mức của mọi việc khác |
| Q4 | Tra web (Serper) trên bản công khai: bật hay tắt | **Tắt** (`HUE_TRA_WEB=false`, như Docker nháp) | Bật ⇒ câu kho không có sẽ gửi câu hỏi (và câu model viết lại ở lượt hỏi tiếp — cờ `web_cau_noi_tiep`) ra Serper, tốn 0,001 USD / lượt, cần khoá Serper trả trước không tự nạp; tắt ⇒ câu ngoài kho chỉ nhận câu từ chối |
| Q5 | Số lượt gọi model / IP / ngày | 50 (`HUE_LUOT_MOI_NGAY=50`) | Cao hơn ⇒ một người có thể tốn nhiều tiền; thấp hơn ⇒ hội đồng thử nhiều có thể bị chặn |
| Q6 | Hỏi bằng ảnh trên bản công khai: bật (ảnh người dùng gửi sang OpenAI) hay tắt | Bật, kèm dòng báo cạnh nút ảnh (checklist cũ: bản công khai cần dòng báo) | Tắt ⇒ bớt một đường dữ liệu ra ngoài |
| Q7 | Ảnh lễ hội thật #5 (không giấy phép mở) | Không lên bản công khai (đã loại trong `.dockerignore`) | Muốn có ⇒ cần quyền dùng ảnh |
| Q8 | Sau demo: xoá máy (hết tiền) hay giữ | Xoá máy + snapshot sau khi chấm xong (§10.5) | Giữ ⇒ 24 USD / tháng tiếp |

## 4. Biến dùng trong tài liệu

| Biến | Nghĩa | Ví dụ / cách lấy |
|---|---|---|
| `<REPO>` | thư mục repo trên máy User | `/home/minhhieu/hue_rag` |
| `<TAG>` | nhãn ảnh Docker = 7 ký tự đầu sha của `main` lúc build | `git -C <REPO> rev-parse --short=7 HEAD` |
| `<IP>` | IP tĩnh của máy Lightsail | in ra ở bước C3 |
| `<SITE>` | tên miền dùng cho HTTPS | `<IP với dấu chấm thay bằng gạch>.sslip.io` (vd `13-250-1-2.sslip.io`) hoặc tên miền riêng |
| `<KEY>` | đường dẫn khoá SSH riêng trên máy User | `~/.ssh/hue-lightsail.pem` (bước C2) |
| `<COL>` | tên collection Qdrant | `hue_full_corpus_7a2_e5_small_384` |

Mọi lệnh trên máy AWS chạy với user `ubuntu`, thư mục làm việc `/srv/hue`.

## 5. Giai đoạn A — chuẩn bị trên máy User (0 USD AWS)

**A1. main sạch, đúng bản sẽ lên.**
- Lệnh: `cd <REPO> && git switch main && git pull --ff-only && git status --short | grep -v '^??'`
- Mong đợi: lệnh cuối không in gì (không có file tracked đang sửa).
- Dừng khi: có file đang sửa, hoặc `git pull` báo xung đột.

**A2. Mọi file dữ liệu mà app đọc đều có trong ảnh.**
- Lệnh: `cd <REPO> && uv run python data/phase_12/deploy_nhap/dung_dockerignore.py`, rồi đoạn kiểm (đã chạy thử 16/11 — 8 / 8 OK):
  ```bash
  uv run python -I - <<'EOF'
  import re, pathlib
  s = pathlib.Path("backend/config/settings.yaml").read_text()
  d = pathlib.Path("data/phase_12/deploy_nhap/Dockerfile").read_text()
  ig = pathlib.Path("data/phase_12/deploy_nhap/Dockerfile.dockerignore").read_text().splitlines()
  for x in sorted(set(re.findall(r"\.\./((?:data|knowledge-base-hue)/[^\s\"'#]+)", s))):
      ok = (x in d or any(x.startswith(c) for c in re.findall(r"COPY (\S+/) ", d))) and ("!" + x in ig)
      print("OK" if ok else "THIEU", x)
  EOF
  ```
- Mong đợi: mọi dòng bắt đầu bằng `OK`.
- Dừng khi: có dòng `THIEU`. Cần thêm một dòng `COPY` trong `Dockerfile` **và** một dòng trong `CHUA` của `dung_dockerignore.py`. Đây là sửa code ⇒ báo User, không tự sửa.

**A3. Build ảnh app.**
- Lệnh: `cd <REPO> && TAG=$(git rev-parse --short=7 HEAD) && docker build -f data/phase_12/deploy_nhap/Dockerfile -t hue-rag-app:$TAG . 2>&1 | tail -5`
- Kiểm: `docker images hue-rag-app:$TAG --format '{{.Size}}'`
- Mong đợi: build xong (~3–5 phút), cỡ khoảng 3,5–4 GB.
- Dừng khi: build lỗi.
- Ghi chú: build **từ thư mục repo chính**, không từ worktree `/tmp` (COPY không theo symlink `data/`, `knowledge-base-hue/` ra ngoài thư mục build). [Đọc] `Dockerfile` dòng đầu.

**A4. Kiểm ảnh không chứa thứ không được lên.**
- Lệnh: `docker run --rm --network none --entrypoint bash hue-rag-app:$TAG -c 'cd /app && find . -path ./.venv -prune -o -type f -print | grep -ciE "sealed|\.env$|/rieng/|_source-dumps|golden"; find knowledge-base-hue -name "*.md" | wc -l'`
- Mong đợi: dòng 1 là `0`; dòng 2 bằng số bài trong build record (`uv run python -c "import json;print(len(json.load(open('data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json'))['corpus']['sources']))"`; 16/11: 263).
- Dừng khi: dòng 1 khác 0.

**A5. Chạy thử cả bộ trên máy User (không đụng Qdrant 6335 của chatbot).**
- Lệnh:
  ```bash
  mkdir -p /tmp/hue_thu && cd /tmp/hue_thu && cp <REPO>/data/phase_12/deploy_nhap/{compose.yml,Caddyfile} . && mkdir -p logs
  curl -s -X POST "http://127.0.0.1:6335/collections/<COL>/snapshots" | tee snap.json
  SNAP=$(python3 -c "import json;print(json.load(open('snap.json'))['result']['name'])")
  curl -s -o qdrant.snapshot "http://127.0.0.1:6335/collections/<COL>/snapshots/$SNAP"
  ls -la qdrant.snapshot
  grep -c '^OPENAI_API_KEY=' <REPO>/.env      # chỉ đếm, không in giá trị
  HUE_IMAGE=hue-rag-app:$TAG HUE_ENV_FILE=<REPO>/.env HUE_SITE=:80 HUE_HTTP_PORT=8880 HUE_HTTPS_PORT=8443 HUE_COOKIE_SECURE=0 HUE_LUOT_MOI_NGAY=3 \
    docker compose -p hue_deploy_thu -f compose.yml up -d qdrant
  ```
  rồi nạp bản chụp vào Qdrant thử. Ảnh Qdrant **không có `curl`** [Đo] 16/11 (`command -v curl` trong container Qdrant đang chạy ⇒ không có)
  ⇒ gọi API khôi phục từ một container dùng một lần của chính ảnh app (có Python, cùng mạng compose, không mở cổng nào ra máy):
  ```bash
  export HUE_IMAGE=hue-rag-app:$TAG HUE_ENV_FILE=<REPO>/.env HUE_SITE=:80 HUE_HTTP_PORT=8880 HUE_HTTPS_PORT=8443 HUE_COOKIE_SECURE=0 HUE_LUOT_MOI_NGAY=3
  docker compose -p hue_deploy_thu -f compose.yml cp qdrant.snapshot qdrant:/qdrant/snapshots/qdrant.snapshot
  docker compose -p hue_deploy_thu -f compose.yml run --rm --no-deps --entrypoint python app -c "
  import json, urllib.request as u
  r = u.Request('http://qdrant:6333/collections/<COL>/snapshots/recover', method='PUT', headers={'Content-Type': 'application/json'},
                data=json.dumps({'location': 'file:///qdrant/snapshots/qdrant.snapshot', 'priority': 'snapshot'}).encode())
  print(u.urlopen(r, timeout=300).read().decode())
  print(json.load(u.urlopen('http://qdrant:6333/collections/<COL>'))['result']['points_count'])"
  docker compose -p hue_deploy_thu -f compose.yml up -d
  ```
  `priority: snapshot` bắt buộc khi nạp vào collection mới / trống (mặc định `replica` giữ dữ liệu đang có ⇒ ra collection rỗng) [Nguồn] qdrant.tech/documentation/snapshots, mở 16/11.
  Bản chụp chỉ nạp được vào Qdrant cùng minor hoặc minor kế tiếp ⇒ hai bên cùng ảnh ghim v1.18.3 (`compose.yml` và `docker-compose.yml` của repo) [Nguồn] cùng trang.
- Kiểm: `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8880/` · `curl -s http://127.0.0.1:8880/health` · `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8880/docs` · `docker stats --no-stream`
- Mong đợi: lệnh `run` in `{"result":true,…}` rồi số điểm = số ở Qdrant máy User (16/11: 9425) · `/` 200 · `/health` báo ổn · `/docs` 404 · app < 2 GiB, Qdrant < 768 MiB. Mở trình duyệt `http://127.0.0.1:8880`, hỏi một câu có trong kho ⇒ có câu trả lời kèm nguồn; hỏi 4 câu ⇒ câu thứ 4 báo hết lượt (vì `HUE_LUOT_MOI_NGAY=3`).
- Dừng khi: app không lên sau 2 phút (`docker compose -p hue_deploy_thu logs app | tail -30`), hoặc kết quả khác mong đợi.
- Dọn: `docker compose -p hue_deploy_thu -f compose.yml down -v && rm -rf /tmp/hue_thu`.
- **Chưa chạy** (bản 1): cả bước A5 với lệnh khôi phục trên — phải chạy thử trước khi duyệt (§13).

**A6. Đóng gói để chuyển.**
- Lệnh: `mkdir -p ~/hue_deploy_$TAG && cd ~/hue_deploy_$TAG && docker save hue-rag-app:$TAG | gzip -1 > app_$TAG.tar.gz && cp <REPO>/data/phase_12/deploy_nhap/{compose.yml,Caddyfile} . && sha256sum app_$TAG.tar.gz > SHA256SUMS && ls -la`
- Tạo bản chụp Qdrant mới như A5 (2 lệnh `curl`) vào thư mục này với tên `qdrant.snapshot`, rồi `sha256sum qdrant.snapshot >> SHA256SUMS`.
- Mong đợi: file ảnh nén ~1–1,5 GB [Suy — chưa đo cỡ nén], `qdrant.snapshot` ~50–60 MB.

**A7. File khoá cho máy AWS (không bao giờ commit).** [User]
- Lệnh (User tự gõ, giá trị không dán vào hội thoại): `nano ~/hue_deploy_$TAG/.env.deploy`, nội dung đúng 1 dòng (thêm `SERPER_API_KEY=…` chỉ khi Q4 = bật):
  ```
  OPENAI_API_KEY=<khoá OpenAI riêng của bản công khai — Q3>
  ```
- Kiểm: `cut -d= -f1 ~/hue_deploy_$TAG/.env.deploy` (chỉ in tên biến) ⇒ `OPENAI_API_KEY`.

## 6. Giai đoạn B — tài khoản AWS [User]

**B1.** Tạo / đăng nhập tài khoản AWS, bật MFA cho tài khoản gốc. Không dùng tài khoản gốc để chạy lệnh.

**B2.** Tạo **cảnh báo ngân sách** 30 USD / tháng, email khi chi phí thật vượt 80 % (AWS Budgets: cảnh báo miễn phí [Nguồn] trang giá Budgets, tra 16/11).
Cảnh báo, **không phải trần cứng** — AWS không tự dừng máy. Cách dễ nhất: bảng điều khiển Billing ⇒ Budgets ⇒ Create budget. CLI (chạy sau B3, thay số tài khoản và email):
  ```bash
  aws budgets create-budget --account-id <số tài khoản 12 chữ số> \
    --budget '{"BudgetName":"hue-demo","BudgetLimit":{"Amount":"30","Unit":"USD"},"TimeUnit":"MONTHLY","BudgetType":"COST"}' \
    --notifications-with-subscribers '[{"Notification":{"NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN","Threshold":80,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"<email User>"}]}]'
  ```
  Quyền IAM ở B3 chỉ có Lightsail ⇒ lệnh này chạy bằng người dùng có quyền Billing, hoặc làm trên bảng điều khiển.

**B3.** Tạo một người dùng IAM riêng cho việc deploy, chỉ quyền Lightsail (`AmazonLightsailFullAccess` hoặc hẹp hơn), tạo access key, cài
AWS CLI v2 trên máy User, chạy `aws configure` (vùng `ap-southeast-1`). Kiểm: `aws sts get-caller-identity` in đúng tên người dùng IAM đó.
Không đưa access key cho agent bằng cách dán vào hội thoại. Agent chạy `aws …` trên máy User nếu User cho.

## 7. Giai đoạn C — tạo máy [Tiền]

Mọi lệnh có `--region ap-southeast-1`. Tên gói / ảnh hệ điều hành lấy từ đầu ra C1, không chép từ tài liệu này.

**C1. Kiểm tên gói và ảnh hệ điều hành hiện hành.**
- Lệnh:
  ```bash
  aws lightsail get-bundles --region ap-southeast-1 --query "bundles[?ramSizeInGb==\`4\`].[bundleId,price,cpuCount,diskSizeInGb,isActive,supportedPlatforms]" --output json
  aws lightsail get-blueprints --region ap-southeast-1 --query "blueprints[?contains(blueprintId,'ubuntu_24')].[blueprintId,name,isActive]" --output table
  ```
- Mong đợi: một gói 4 GB, giá 24, `LINUX_UNIX`, `isActive` true — tên dự kiến `medium_3_0` · một blueprint Ubuntu 24.04 `isActive` true — tên dự kiến `ubuntu_24_04`
  ([Nguồn] tra 16/11: hai tên này lấy từ ví dụ công khai + ví dụ CLI của AWS, **chưa** thấy đầu ra API Singapore; giá 24 USD / 4 GB / 2 vCPU / 80 GB / 4 TB đã tự mở trang giá aws.amazon.com/lightsail/pricing 16/11).
  Gói "chỉ IPv6" (20 USD) **không** dùng: IP tĩnh IPv4 không gắn được, người chấm không có IPv6 thì không vào được.
- Dừng khi: không có gói 4 GB Linux active, hoặc giá khác 24 ⇒ báo User (đổi giá ⇒ hỏi lại Q1). Tài khoản Free plan không thấy gói 4 GB ⇒ dừng, báo User (nguồn chưa xác nhận gói 4 GB tạo được trên Free plan).

**C2. Khoá SSH.**
- Lệnh: `aws lightsail create-key-pair --region ap-southeast-1 --key-pair-name hue-key --query privateKeyBase64 --output text > ~/.ssh/hue-lightsail.pem && chmod 600 ~/.ssh/hue-lightsail.pem`
- Kiểm: `head -c 30 ~/.ssh/hue-lightsail.pem` ⇒ bắt đầu bằng `-----BEGIN` (chỉ in 30 ký tự đầu).

**C3. Tạo máy, IP tĩnh, cổng.** [Tiền]
- Lệnh:
  ```bash
  aws lightsail create-instances --region ap-southeast-1 --instance-names hue-app --availability-zone ap-southeast-1a \
    --blueprint-id <blueprint C1> --bundle-id <bundle C1> --key-pair-name hue-key
  until [ "$(aws lightsail get-instance --region ap-southeast-1 --instance-name hue-app --query instance.state.name --output text)" = running ]; do sleep 10; done
  aws lightsail allocate-static-ip --region ap-southeast-1 --static-ip-name hue-ip
  aws lightsail attach-static-ip --region ap-southeast-1 --static-ip-name hue-ip --instance-name hue-app
  aws lightsail open-instance-public-ports --region ap-southeast-1 --instance-name hue-app --port-info fromPort=443,toPort=443,protocol=TCP
  aws lightsail open-instance-public-ports --region ap-southeast-1 --instance-name hue-app --port-info fromPort=80,toPort=80,protocol=TCP
  aws lightsail get-instance-port-states --region ap-southeast-1 --instance-name hue-app --query "portStates[].[fromPort,state]" --output text
  aws lightsail get-static-ip --region ap-southeast-1 --static-ip-name hue-ip --query staticIp.ipAddress --output text
  ```
- Mong đợi: cổng 22, 80, 443 đều `open`; lệnh cuối in `<IP>`. Dùng `open-instance-public-ports` (thêm từng cổng), không dùng `put-instance-public-ports` (lệnh đó thay cả danh sách — gõ thiếu 22 là mất SSH) [Nguồn] tài liệu CLI AWS, tra 16/11. Lightsail mặc định chỉ mở 22 / 80 ⇒ thiếu 443 thì HTTPS treo (review 07/11).
- Dừng khi: bất kỳ lệnh nào lỗi.
- [Suy, chờ §12] Giới hạn cổng 22 chỉ cho IP nhà User (`cidrs=<IP nhà>/32`) an toàn hơn nhưng IP nhà đổi thì mất SSH ⇒ bản 1 để mở, khoá SSH là rào chính.

**C4. Snapshot tự động hằng ngày** (sao lưu cả máy): `aws lightsail enable-add-on --region ap-southeast-1 --resource-name hue-app --add-on-request 'addOnType=AutoSnapshot,autoSnapshotAddOnRequest={snapshotTimeOfDay=19:00}'`
(giờ UTC, bước một giờ; 19:00 UTC = 02:00 giờ Việt Nam). Lightsail giữ 7 bản gần nhất; giá 0,05 USD / GB-tháng, tính trên dung lượng thật của bản chụp (các bản sau chỉ tính phần đổi)
[Nguồn] trang giá Lightsail tự mở 16/11 + tài liệu snapshot tự động. Ước: đĩa dùng ~15–20 GB [Suy] ⇒ ~1 USD / tháng. **Xoá máy là xoá luôn bản chụp tự động** ⇒ trước khi xoá phải tạo bản chụp thủ công (10.5).

## 8. Giai đoạn D — cài và chạy trên máy AWS

**D1. Vào máy, cài Docker** theo tài liệu chính thức docs.docker.com/engine/install/ubuntu ([Nguồn] Codex mở 16/11; chưa chạy trên máy thật). `ssh -i <KEY> ubuntu@<IP>` rồi:
  ```bash
  sudo apt update && sudo apt install -y ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
  Types: deb
  URIs: https://download.docker.com/linux/ubuntu
  Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
  Components: stable
  Architectures: $(dpkg --print-architecture)
  Signed-By: /etc/apt/keyrings/docker.asc
  EOF
  sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo usermod -aG docker ubuntu && sudo systemctl enable --now docker
  exit
  ```
  (`enable` để Docker tự chạy sau khi máy khởi động lại — không thì `restart: unless-stopped` vô tác dụng; `exit` để lần SSH sau nhận nhóm `docker`.)
- Kiểm: `ssh -i <KEY> ubuntu@<IP> 'docker version --format "{{.Server.Version}}" && docker compose version && free -m && df -h /'`
- Mong đợi: có số phiên bản Docker và compose; `free` tổng ~3.800–4.000 MB; đĩa trống > 60 GB.

**D2. Chuyển file.**
- Lệnh: `ssh -i <KEY> ubuntu@<IP> 'sudo mkdir -p /srv/hue && sudo chown ubuntu:ubuntu /srv/hue'` rồi
  `scp -i <KEY> ~/hue_deploy_$TAG/{app_$TAG.tar.gz,qdrant.snapshot,compose.yml,Caddyfile,SHA256SUMS,.env.deploy} ubuntu@<IP>:/srv/hue/`
- Kiểm: `ssh -i <KEY> ubuntu@<IP> 'cd /srv/hue && sha256sum -c SHA256SUMS && chmod 600 .env.deploy && stat -c "%a %n" .env.deploy'`
- Mong đợi: hai dòng `OK`; `600 .env.deploy`.

**D3. Nạp ảnh, đặt biến, nạp dữ liệu Qdrant.**
- Lệnh:
  ```bash
  ssh -i <KEY> ubuntu@<IP>
  cd /srv/hue && gunzip -c app_<TAG>.tar.gz | docker load && mkdir -p logs qdrant_storage
  cat > hue.env <<EOF
  HUE_IMAGE=hue-rag-app:<TAG>
  HUE_ENV_FILE=/srv/hue/.env.deploy
  HUE_SITE=<SITE>
  HUE_LUOT_MOI_NGAY=50
  EOF
  docker compose -p hue -f compose.yml --env-file hue.env up -d qdrant
  ```
  rồi nạp `qdrant.snapshot` bằng đúng lệnh `cp` + `run … python` ở A5 (thay `-p hue_deploy_thu -f compose.yml` bằng `-p hue -f compose.yml --env-file hue.env`; không `export` biến của A5).
- Mong đợi: dòng cuối lệnh `run` = số điểm ở máy User (16/11: 9425).
- Dừng khi: số điểm khác.
- `hue.env` chỉ chứa biến không bí mật. Khoá nằm riêng ở `.env.deploy` (quyền 600), compose nạp vào container app qua `env_file`, không nằm trong ảnh.

**D4. Chạy cả bộ.**
- Lệnh: `docker compose -p hue -f compose.yml --env-file hue.env up -d && sleep 60 && docker compose -p hue -f compose.yml --env-file hue.env ps`
- Mong đợi: 3 container `running`, qdrant `healthy`.
- Dừng khi: container nào thoát (`docker compose … logs <tên> | tail -40`, báo User).

## 9. Giai đoạn E — kiểm sau khi lên (từ máy User)

| Kiểm | Lệnh | Mong đợi |
|---|---|---|
| HTTPS | `curl -sI https://<SITE>/ \| head -1` | `HTTP/2 200` (lần đầu Caddy xin chứng chỉ có thể mất ~30 s) |
| http chuyển sang https | `curl -sI http://<SITE>/ \| head -3` | 308 sang `https://` |
| Trang API tắt | `curl -s -o /dev/null -w '%{http_code}' https://<SITE>/docs` | `404` |
| Tính năng | `curl -s https://<SITE>/api/tinh_nang` | `tra_web` đúng Q4; `anh` đúng Q6 |
| Câu trong kho | mở trình duyệt, hỏi một câu về một món / di tích có trong kho | câu trả lời có nguồn; chữ hiện dần (không đợi cả câu) |
| Câu ngoài kho | hỏi một câu không về Huế | câu từ chối |
| Cookie | trình duyệt: hỏi 2 câu liên tiếp, câu 2 dùng "ở đó" | câu 2 hiểu đúng nơi của câu 1 (nhớ hội thoại cần cookie Secure qua https) |
| RAM | `ssh … 'docker stats --no-stream'` | app < 2 GiB, tổng `free -m` còn > 500 MB |
| Log không ghi câu hỏi / IP | `ssh … 'grep -c "chat_metrics" /srv/hue/logs/application.log'` | số dòng = số lượt đã hỏi; người chạy không in nội dung log ra hội thoại |
| Sổ vết tắt | `ssh … 'docker compose -p hue -f /srv/hue/compose.yml --env-file /srv/hue/hue.env exec -T app env \| grep -c HUE_SO_VET'` | `0` |

Ghi kết quả từng dòng (đạt / không) vào report deploy. Có dòng "không" ⇒ dừng, không gửi link cho ai.

## 10. Vận hành

**10.1 Sao lưu.** Máy: snapshot tự động hằng ngày (C4). Dữ liệu Qdrant không đổi khi chạy (chatbot chỉ đọc) ⇒ bản `qdrant.snapshot` trên máy User
là bản sao lưu đủ. Log: `/srv/hue/logs` (xoay vòng 10 MB × 3 trong ảnh; log stdout Docker 10 MB × 3 mỗi container — `compose.yml`).

**10.2 Cập nhật bản mới.** Trên máy User làm lại A1–A4 + A6 (bản chụp Qdrant chỉ khi kho đổi), `scp` file ảnh mới, trên máy AWS:
`gunzip -c app_<TAG mới>.tar.gz | docker load`, sửa `HUE_IMAGE` trong `hue.env`, `docker compose -p hue -f compose.yml --env-file hue.env up -d app`, rồi làm lại §9.
Kho đổi (build lại chỉ mục) ⇒ ảnh mới **và** bản chụp Qdrant mới phải đi cùng nhau (app so hash kho với build record lúc khởi động).

**10.3 Quay lại bản cũ.** Ảnh cũ vẫn còn trên máy (`docker images hue-rag-app`) ⇒ đặt lại `HUE_IMAGE` = nhãn cũ, `up -d app`. Giữ tối đa 2 ảnh cũ (`docker image rm hue-rag-app:<nhãn quá cũ>`; đĩa 80 GB).

**10.4 Khi có sự cố.** App 503 / không trả lời: `docker compose … logs app | tail -50` (không chép vào chỗ công khai). Hết lượt OpenAI: trang OpenAI báo,
người dùng thấy lỗi ⇒ User nạp / nâng hạn mức. Máy hết RAM: `docker stats`, `dmesg | grep -i oom`.

**10.5 Kết thúc demo** [User quyết Q8]: tạo snapshot cuối `aws lightsail create-instance-snapshot --instance-name hue-app --instance-snapshot-name hue-cuoi`,
rồi `aws lightsail delete-instance --instance-name hue-app` và `aws lightsail release-static-ip --static-ip-name hue-ip` (IP tĩnh gắn máy thì miễn phí; không gắn quá một giờ ⇒ 0,005 USD / giờ [Nguồn] tài liệu static IP Lightsail, tra 16/11). Bản chụp thủ công ~0,05 USD / GB-tháng ⇒ xoá khi không cần nữa (`aws lightsail delete-instance-snapshot --instance-snapshot-name hue-cuoi`).

## 11. Bảng rà khung AI FDE (agent-security-review) cho bản công khai

| Mục | Hiện trạng | Mức | Đề xuất |
|---|---|---|---|
| Bộ ba chết người | (a) dữ liệu riêng tư: kho private trong ảnh, không có dữ liệu người dùng lưu lâu (hội thoại trong RAM); (b) nội dung không tin cậy: câu người dùng, ảnh người dùng, đoạn web (nếu Q4 bật); (c) đường ra: OpenAI (câu hỏi + 10 đoạn kho + ảnh), Serper (nếu bật), Open-Meteo (chỉ toạ độ Huế, không chữ người dùng) [Đọc] `backend/llm/thoi_tiet.py`, `tra_web.py` | minor | Đủ ba nhưng đường ra chỉ là API của nhà cung cấp model / tìm kiếm, không có công cụ ghi / gửi tin. Q4 tắt ⇒ bớt một đường. Không thêm công cụ ghi ra ngoài trên bản công khai |
| Chữ người dùng là dữ liệu | đã có rào chữ trong ảnh (model chỉ-ảnh không theo chữ dán), bộ an toàn 32 câu chạy ở mỗi đổi lời dặn | minor | Không đổi cho deploy |
| Giới hạn ở API | giới hạn lượt / IP / ngày trong RAM `backend/api/gioi_han.py` (đã thử 429, kể cả giả `X-Forwarded-For` — report B 10/11); hạn mức chi tiêu OpenAI (Q3) | major nếu Q3 = không | Khoá riêng + giới hạn chi tiêu ở trang OpenAI là lớp thứ hai bắt buộc; giới hạn lượt reset khi app khởi động lại (đếm trong RAM) — chấp nhận cho demo |
| Quyền hẹp | IAM riêng chỉ Lightsail (B3); khoá SSH riêng; cổng mở 22 / 80 / 443; app không mở cổng ra ngoài (chỉ Caddy) [Đọc] `compose.yml` | minor | Thêm `--forwarded-allow-ips '*'` chỉ an toàn khi app không có `ports` — giữ nguyên ghi chú trong compose |
| Khoá không vào ảnh / log | `.env` loại khỏi build (`**/.env` trong `.dockerignore`), khoá nạp lúc chạy; log không ghi câu hỏi / IP [Đo] 10/11 | minor | A4 kiểm lại mỗi lần build |
| Dữ liệu cá nhân | log `chat_metrics` không có câu hỏi / IP; sổ vết có nội dung TẮT trên bản công khai (không đặt `HUE_SO_VET`); ảnh người dùng không lưu ở server [Đọc] `backend/core/so_vet.py`, `compose.yml` | minor | Trang Giới thiệu đã nói câu hỏi / ảnh gửi sang nhà cung cấp model; nếu Q6 bật thì kiểm dòng báo cạnh nút ảnh có trên bản build |
| Kho private trong ảnh | ảnh không lên registry công khai; chỉ `scp` | major nếu ai đẩy ảnh lên Docker Hub | Luật ở §0; không tạo ECR công khai |
| Rào đo hai chiều | 429 đã thử 3 ca xấu + câu thường đi qua (report B 10/11) | — | §9 làm lại trên máy thật |

**Giả định an toàn:** chạy trên một máy Lightsail do User sở hữu; ai có link đều gọi được; giới hạn chi tiêu = giới hạn lượt / IP / ngày + hạn mức
OpenAI; chưa rào: một người dùng nhiều IP vẫn dùng được nhiều lượt (chặn bằng hạn mức OpenAI), lượt bị Dừng vẫn tính tiền phần đã chạy.

## 12. Tra cứu (16/11/2026)

- Codex: yêu cầu chỉ thông tin công khai ⇒ `data/tra_cuu_cli/2026-11-16_deploy-aws-2/ket_qua.md` (155 s, 34 trang mở được, 0 lệnh shell). Kết quả là dữ liệu ngoài.
- E tự mở kiểm 2 ý chính: trang giá Lightsail (2 GB 12 · 4 GB 24 · 8 GB 44 USD; snapshot 0,05 USD / GB-tháng) và tài liệu snapshot Qdrant
  (đường API, `file://` dùng được, `priority: snapshot`, tương thích minor). Còn lại ghi [Nguồn] theo Codex, chưa tự mở.
- Còn chưa chắc: tên `medium_3_0` / `ubuntu_24_04` (C1 lấy từ đầu ra thật); gói 4 GB có tạo được trên Free plan không; lệnh cài Docker chưa chạy trên máy thật.
- Tra cũ 07/11 (EC2, Secrets Manager 0,40 USD / khoá / tháng, Parameter Store bản thường miễn phí): `data/tra_cuu_cli/2026-11-07_e-dep-aws/`. Bản 1 chọn `.env.deploy` quyền 600 trên máy
  (đơn giản nhất, đủ cho một máy demo); Secrets Manager / Parameter Store chỉ đáng khi nhiều máy hoặc cần xoay khoá.

## 13. Việc phải chạy thử trước khi duyệt (0 USD, trên máy User)

1. A2–A5 trọn vẹn, nhất là lệnh nạp bản chụp Qdrant (curl có trong ảnh Qdrant không; đường `recover` từ file có chạy không).
2. Cỡ file ảnh nén ở A6 (ước thời gian `scp`).
3. Không chạy được trên máy AWS khi chưa có Q1 — §7–§9 chỉ được kiểm bằng đọc tài liệu.

## Lịch sử bản

- Bản 1 (E, xong 14:36 16/11/2026, đã điền kết quả tra): đủ các giai đoạn; §13 chưa chạy.
