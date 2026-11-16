# Spec bản 2: deploy chatbot Huế lên AWS (một máy Lightsail, Docker Compose)

E viết bản 1, xong lúc 14:36 16/11/2026, theo việc A giao (User 16/11: mọi việc local và kế hoạch deploy phải xong trước 30/11; từ tháng 12 Codex / Gemini làm tiếp).
**Chỉ là tài liệu.** Viết spec này không tạo tài nguyên AWS nào và không gọi AWS. Reviewer: C. Trạng thái: **bản 2 sau review C vòng 1 — chờ C vòng 2, chưa duyệt.**

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

**Tổng tiền cả đợt** (để chọn Q1, Q2, Q3, Q10 cho có cơ sở; trước credit tài khoản mới). Một tháng = 24 USD máy + ~1 USD sao lưu + ≤ 5 USD OpenAI = ~30 USD.
Ba tháng (12/2026–02/2027) = máy 72 + sao lưu ~3 + OpenAI ≤ 15 + tên miền 10–15 (nếu Q2 = riêng) ⇒ **~90–105 USD**. Tạo máy từ 01/12 thay vì 15/12 ⇒ +~12 USD.
Tài khoản AWS mới được 100 USD credit (thêm tối đa 100 USD qua hoạt động) ⇒ phần máy có thể gần như 0 USD nếu credit trừ được vào Lightsail (nguồn nói được, chưa thử) [Nguồn] tra 16/11.
Số OpenAI là trần (Q3), không phải ước: demo thật thường ~0,0005 USD / câu [Đo] 16/11 ⇒ vài chục lượt chấm < 1 USD.

| # | Câu | Mặc định đề xuất | Hệ quả nếu chọn khác · khi nào mặc định sai |
|---|---|---|---|
| Q1 | Có tạo tài khoản AWS (hoặc dùng tài khoản có sẵn) và chấp nhận ~24 USD / tháng cho máy (thêm ~1 USD sao lưu) trong 2–3 tháng không | Có, gói 4 GB | Gói 2 GB rẻ hơn 12 USD nhưng dễ hết RAM; không có AWS ⇒ demo chạy trên máy User. Tài khoản mới: Free plan hết sau 6 tháng hoặc hết credit — chưa nâng lên Paid thì tài khoản bị đóng, dữ liệu giữ 90 ngày ⇒ **nâng lên Paid plan trước buổi chấm**; chưa có nguồn xác nhận gói 4 GB tạo được trên Free plan [Nguồn] docs.aws.amazon.com free-tier-plans, tra 16/11 |
| Q2 | Tên miền: mua tên miền riêng (~10–15 USD / năm, User tự mua) hay dùng `<IP>.sslip.io` miễn phí | `sslip.io` để thử; **tên miền riêng cho buổi chấm** | sslip.io miễn phí nhưng mọi người dùng chung một hạn mức chứng chỉ Let's Encrypt (50 chứng chỉ / tên miền / 7 ngày; sslip.io không nằm trong Public Suffix List — một báo lỗi 09/02/2026 cho thấy từng hết hạn mức) ⇒ ngày chấm có thể không xin được chứng chỉ [Nguồn] letsencrypt.org/docs/rate-limits + issue sslip.io #108, tra 16/11. Tên miền riêng thêm một bước trỏ DNS (bản ghi A ⇒ `<IP>`) |
| Q3 | Khoá OpenAI riêng cho bản công khai, có đặt giới hạn chi tiêu (User tạo ở trang OpenAI) | Có: project riêng ở OpenAI ⇒ Limits ⇒ Monthly spend limit ~5 USD + **bật "Enforce a hard limit"** (không bật thì chỉ cảnh báo, request vẫn chạy; áp không tức thời, có thể vượt nhẹ) [Nguồn] help.openai.com "Managing projects", tra 16/11 | Dùng chung khoá máy User ⇒ người ngoài dùng hết hạn mức của mọi việc khác |
| Q4 | Tra web (Serper) trên bản công khai: bật hay tắt | **Tắt** (`HUE_TRA_WEB=false`, như Docker nháp) | Bật ⇒ câu kho không có sẽ gửi câu hỏi (và câu model viết lại ở lượt hỏi tiếp — cờ `web_cau_noi_tiep`) ra Serper, tốn 0,001 USD / lượt, cần khoá Serper trả trước không tự nạp; tắt ⇒ câu ngoài kho chỉ nhận câu từ chối |
| Q5 | Số lượt gọi model / IP / ngày | 50 (`HUE_LUOT_MOI_NGAY=50`) | Cao hơn ⇒ một người có thể tốn nhiều tiền; thấp hơn ⇒ hội đồng thử nhiều có thể bị chặn. Sai khi cả hội đồng dùng chung một mạng (chung IP) ⇒ nâng lên ~200 trong ngày chấm |
| Q6 | Hỏi bằng ảnh trên bản công khai: bật (ảnh người dùng gửi sang OpenAI) hay tắt | Bật, kèm dòng báo cạnh nút ảnh (checklist cũ: bản công khai cần dòng báo) | Tắt ⇒ bớt một đường dữ liệu ra ngoài |
| Q7 | Ảnh lễ hội thật #5 (không giấy phép mở) | Không lên bản công khai (đã loại trong `.dockerignore`) | Muốn có ⇒ cần quyền dùng ảnh |
| Q8 | Sau demo: xoá máy (hết tiền) hay giữ | Xoá máy sau khi có bản chụp thủ công `available` (§10.5) | Giữ ⇒ 24 USD / tháng tiếp |
| Q9 | Agent (Codex / Gemini) có được chạy lệnh `aws …` bằng access key của User không | **Chỉ lệnh chỉ đọc** (`get-*`, `sts get-caller-identity`); mọi lệnh có nhãn [Tiền] hoặc xoá (C3, C4, 10.5) **User tự gõ** sau khi agent đưa lệnh | Cho agent chạy hết ⇒ nhanh hơn, nhưng một lệnh sai có thể tạo / xoá tài nguyên tính tiền hoặc mất dữ liệu; User tự gõ hết ⇒ chậm, User phải ngồi cùng. Sai khi User vắng cả tuần deploy ⇒ khi đó cho agent chạy C3 một lần, ghi lại |
| Q10 | Ngày tạo máy (= ngày bắt đầu tính tiền máy) | **Khoảng 1 tuần trước buổi chấm** (đủ thời gian sửa lỗi); thử tạo-xoá một lần sớm hơn chỉ tốn vài giờ máy (~0,03 USD / giờ) | Tạo từ 30/11 ⇒ +~24 USD mỗi tháng sớm hơn. User đã dặn không deploy sớm (12/11) — tài liệu xong trước 30/11, máy tạo theo ngày User chọn |
| Q11 | Giữ bản sao các file deploy (Dockerfile, compose, Caddyfile, `dung_dockerignore.py`) ở đâu — hiện chỉ trong `data/phase_12/deploy_nhap/` (không Git) | Đưa 4 file đó (không bí mật) vào repo `deploy/` qua một nhánh; **không** đưa `Dockerfile.dockerignore` (liệt kê tên 263 bài kho — sinh lại bằng script) | Giữ trong `data/` ⇒ máy User hỏng là mất; md5 ở §0 giúp phát hiện file bị sửa, không giúp khôi phục |

## 4. Biến dùng trong tài liệu

| Biến | Nghĩa | Ví dụ / cách lấy |
|---|---|---|
| `<REPO>` | thư mục repo trên máy User | `/home/minhhieu/hue_rag` |
| `TAG` | biến shell: nhãn ảnh Docker = 7 ký tự đầu sha của `main` lúc build. **Trên máy User** đặt bằng `TAG=$(git -C <REPO> rev-parse --short=7 HEAD)`; **trên máy AWS** đặt tay `TAG=<7 ký tự đó>` ở dòng đầu D3 | `a9d1674` |
| `<IP>` | IP tĩnh của máy Lightsail | in ra ở bước C3 |
| `<SITE>` | tên miền dùng cho HTTPS | `<IP với dấu chấm thay bằng gạch>.sslip.io` (vd `13-250-1-2.sslip.io`) hoặc tên miền riêng |
| `<KEY>` | đường dẫn khoá SSH riêng trên máy User | `~/.ssh/hue-lightsail.pem` (bước C2) |
| `COL` | biến shell: tên collection Qdrant | `COL=hue_full_corpus_7a2_e5_small_384` |

Mọi lệnh trên máy AWS chạy với user `ubuntu`, thư mục làm việc `/srv/hue`. Mỗi cửa sổ shell mới phải đặt lại `TAG` và `COL`.

**File deploy và md5** (16/11, `md5sum` 12 ký tự đầu — lệch ⇒ file đã bị sửa sau bản spec này, đọc diff với bản sao lưu `data/phase_12/deploy_nhap/sao_luu_*` trước khi chạy):
`Dockerfile` `bd887103b463` · `compose.yml` `942d3527c413` · `Caddyfile` `da85ebea1915` · `dung_dockerignore.py` `98e0edaecfee` · `Dockerfile.dockerignore` `0c18e40a4fe6` (sinh lại ở A2; đổi khi kho đổi).
Kiểm: `cd <REPO>/data/phase_12/deploy_nhap && md5sum Dockerfile compose.yml Caddyfile dung_dockerignore.py | cut -c1-12`.

## 5. Giai đoạn A — chuẩn bị trên máy User (0 USD AWS)

Đã chạy thử A2–A6 ngày 16/11 trên `main` `a9d1674` — số ở §13.

**A1. main đúng bản sẽ lên.**
- Lệnh: `cd <REPO> && git switch main && git pull --ff-only && git status --short -- backend frontend pyproject.toml uv.lock`
- Mong đợi: lệnh cuối không in gì (không có sửa dở trong phần code đi vào ảnh; file tài liệu đang sửa không ảnh hưởng).
- Dừng khi: lệnh cuối in ra file, hoặc `git pull` báo xung đột.

**A2. File dữ liệu mà app đọc có trong ảnh.**
- Lệnh: `cd <REPO> && uv run python data/phase_12/deploy_nhap/dung_dockerignore.py`, rồi:
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
- Mong đợi: lệnh đầu in `ghi Dockerfile.dockerignore: <n> bài kho + 14 mục khác`; đoạn kiểm in toàn dòng `OK` (16/11: 8 / 8).
- Dòng `THIEU`: **ghi lại rồi đi tiếp** — đoạn kiểm xét mọi đường dẫn trong `settings.yaml`, kể cả file của cờ đang tắt (app không đọc). Phán quyết thật là A5:
  app thiếu file của cờ đang bật thì **không khởi động** (uvicorn thoát mã 3). A5 app không lên mà có dòng `THIEU` ⇒ dừng, báo User (cần thêm dòng `COPY` + dòng `CHUA` — sửa code, không tự sửa).

**A3. Build ảnh app.**
- Lệnh: `cd <REPO> && TAG=$(git rev-parse --short=7 HEAD) && docker build -f data/phase_12/deploy_nhap/Dockerfile -t hue-rag-app:$TAG . 2>&1 | tail -5`
- Kiểm: `docker images hue-rag-app:$TAG --format '{{.Size}}'`
- Mong đợi: dòng cuối có `naming to docker.io/library/hue-rag-app:<TAG> done`; cỡ ~3,6 GB. Thời gian: 8 s khi đã có cache (16/11), ~3–5 phút lần đầu (191 s ngày 10/11).
- Dừng khi: build lỗi.
- Ghi chú: build **từ thư mục repo chính**, không từ worktree `/tmp` (COPY không theo symlink `data/`, `knowledge-base-hue/` ra ngoài thư mục build). [Đọc] `Dockerfile` dòng đầu.

**A4. Ảnh không chứa thứ không được lên.**
- Lệnh: `docker run --rm --network none --entrypoint bash hue-rag-app:$TAG -c 'cd /app && find . -path ./.venv -prune -o -path ./backend -prune -o -type f -print | grep -ciE "sealed|\.env$|/rieng/|_source-dumps|golden"; find knowledge-base-hue -name "*.md" | wc -l'`
  và `cd <REPO> && uv run python -c "import json;print(len(json.load(open('data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json'))['corpus']['sources']))"`
- Mong đợi: dòng 1 là `0`; dòng 2 = số của lệnh thứ hai (16/11: 263 = 263). `backend/` bỏ qua vì là code công khai (có 2 file tên chứa `golden` — code chấm, không phải dữ liệu) [Đo] 16/11.
- Dừng khi: dòng 1 khác 0, hoặc hai số đếm khác nhau.

**A5. Chạy thử cả bộ trên máy User (không đụng Qdrant 6335 của chatbot).**
- Lệnh (một shell, đã có `TAG` từ A3):
  ```bash
  COL=hue_full_corpus_7a2_e5_small_384
  mkdir -p /tmp/hue_thu && cd /tmp/hue_thu && cp <REPO>/data/phase_12/deploy_nhap/{compose.yml,Caddyfile} . && mkdir -p logs
  curl -s -X POST "http://127.0.0.1:6335/collections/$COL/snapshots" > snap.json
  SNAP=$(python3 -c "import json;print(json.load(open('snap.json'))['result']['name'])")
  curl -s -o qdrant.snapshot "http://127.0.0.1:6335/collections/$COL/snapshots/$SNAP"
  curl -s -X DELETE "http://127.0.0.1:6335/collections/$COL/snapshots/$SNAP"     # bản chụp không nằm lại trong Qdrant của chatbot
  ls -la qdrant.snapshot; curl -s "http://127.0.0.1:6335/collections/$COL/snapshots"
  grep -c '^OPENAI_API_KEY=' <REPO>/.env      # chỉ đếm, không in giá trị
  export HUE_IMAGE=hue-rag-app:$TAG HUE_ENV_FILE=<REPO>/.env HUE_SITE=:80 HUE_HTTP_PORT=8880 HUE_HTTPS_PORT=8443 HUE_COOKIE_SECURE=0 HUE_LUOT_MOI_NGAY=3
  docker compose -p hue_deploy_thu -f compose.yml up -d qdrant
  for i in $(seq 30); do [ "$(docker inspect -f '{{.State.Health.Status}}' hue_deploy_thu-qdrant-1)" = healthy ] && break; sleep 2; done
  docker compose -p hue_deploy_thu -f compose.yml cp qdrant.snapshot qdrant:/qdrant/snapshots/qdrant.snapshot
  docker compose -p hue_deploy_thu -f compose.yml run --rm --no-deps --entrypoint python app -c "
  import json, urllib.request as u
  r = u.Request('http://qdrant:6333/collections/$COL/snapshots/recover', method='PUT', headers={'Content-Type': 'application/json'},
                data=json.dumps({'location': 'file:///qdrant/snapshots/qdrant.snapshot', 'priority': 'snapshot'}).encode())
  print(u.urlopen(r, timeout=300).read().decode())
  print(json.load(u.urlopen('http://qdrant:6333/collections/$COL'))['result']['points_count'])"
  docker compose -p hue_deploy_thu -f compose.yml up -d
  ```
  Ảnh Qdrant **không có `curl`** [Đo] 16/11 ⇒ lệnh khôi phục chạy trong một container dùng một lần của chính ảnh app (có Python, cùng mạng compose, không mở cổng nào ra máy).
  `priority: snapshot` bắt buộc khi nạp vào collection mới / trống (mặc định `replica` giữ dữ liệu đang có ⇒ ra collection rỗng) [Nguồn] qdrant.tech/documentation/snapshots, tự mở 16/11.
  Bản chụp chỉ nạp được vào Qdrant cùng minor hoặc minor kế tiếp ⇒ hai bên cùng ảnh ghim v1.18.3 (`compose.yml` và `docker-compose.yml` của repo) [Nguồn] cùng trang.
- Kiểm (chờ `/health` trả lời, ~25 s): `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8880/` · `curl -s http://127.0.0.1:8880/health` · `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8880/docs` · `curl -s http://127.0.0.1:8880/api/tinh_nang` · `docker stats --no-stream`
- Mong đợi: `qdrant.snapshot` ~56 MB và danh sách snapshot của 6335 rỗng `"result":[]` · lệnh `run` in `{"result":true,…}` rồi số điểm = số ở Qdrant máy User (16/11: 9425) · `/` 200 · `/health` có `"status":"ok"` · `/docs` 404 · `tinh_nang` có `"tra_web":false` · app < 2 GiB, Qdrant < 768 MiB.
  Trình duyệt `http://127.0.0.1:8880`: hỏi một câu có trong kho ⇒ câu trả lời kèm nguồn, chữ hiện dần. Lượt gọi model thứ 4 trong ngày ⇒ câu báo hết lượt (vì `HUE_LUOT_MOI_NGAY=3`).
- Dừng khi: `/health` không trả lời sau 2 phút (`docker compose -p hue_deploy_thu -f compose.yml logs app | tail -30` — báo User), hoặc kết quả khác mong đợi.
- Dọn (thư mục Qdrant do container tạo thuộc root ⇒ xoá qua docker):
  ```bash
  cd /tmp/hue_thu && docker compose -p hue_deploy_thu -f compose.yml down -v
  docker run --rm -v /tmp/hue_thu:/x --entrypoint bash qdrant/qdrant@sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286 -c 'rm -rf /x/qdrant_storage /x/logs'
  cd / && rm -rf /tmp/hue_thu && docker ps --format '{{.Names}}' | grep -c hue_deploy_thu
  ```
  Mong đợi lệnh cuối in `0`.

**A6. Đóng gói để chuyển.**
- Lệnh (cùng shell, có `TAG`, `COL`):
  ```bash
  mkdir -p ~/hue_deploy_$TAG && cd ~/hue_deploy_$TAG
  docker save hue-rag-app:$TAG | gzip -1 > app_$TAG.tar.gz
  cp <REPO>/data/phase_12/deploy_nhap/{compose.yml,Caddyfile} .
  curl -s -X POST "http://127.0.0.1:6335/collections/$COL/snapshots" > snap.json
  SNAP=$(python3 -c "import json;print(json.load(open('snap.json'))['result']['name'])")
  curl -s -o qdrant.snapshot "http://127.0.0.1:6335/collections/$COL/snapshots/$SNAP"
  curl -s -X DELETE "http://127.0.0.1:6335/collections/$COL/snapshots/$SNAP" && rm snap.json
  sha256sum app_$TAG.tar.gz qdrant.snapshot compose.yml Caddyfile > SHA256SUMS
  ```
- Kiểm: `sha256sum -c SHA256SUMS && ls -la && curl -s "http://127.0.0.1:6335/collections/$COL/snapshots"`
- Mong đợi: 4 dòng `OK`; `app_<TAG>.tar.gz` ~0,9 GB (16/11: 0,90 GB, 32 s); `qdrant.snapshot` ~56 MB; danh sách snapshot của 6335 `"result":[]`.
- Dừng khi: có dòng `FAILED`, file nào cỡ 0, hoặc lệnh `docker save` lỗi.

**A7. File khoá cho máy AWS (không bao giờ commit).** [User]
- Lệnh (User tự gõ, giá trị không dán vào hội thoại): `nano ~/hue_deploy_$TAG/.env.deploy`, nội dung đúng 1 dòng (thêm `SERPER_API_KEY=…` chỉ khi Q4 = bật):
  ```
  OPENAI_API_KEY=<khoá OpenAI riêng của bản công khai — Q3>
  ```
- Kiểm: `cut -d= -f1 ~/hue_deploy_$TAG/.env.deploy` (chỉ in tên biến).
- Mong đợi: đúng `OPENAI_API_KEY` (và `SERPER_API_KEY` nếu Q4 bật).
- Dừng khi: thiếu tên biến, hoặc có tên biến khác.

## 6. Giai đoạn B — tài khoản AWS [User]

**B1.** [User] Tạo / đăng nhập tài khoản AWS, bật MFA cho tài khoản gốc. Không dùng tài khoản gốc để chạy lệnh. Tài khoản mới đang ở Free plan ⇒ nâng lên Paid plan trước buổi chấm (Q1).

**B2.** [User] Tạo **cảnh báo ngân sách** 30 USD / tháng, email khi chi phí thật vượt 80 % (AWS Budgets: cảnh báo miễn phí [Nguồn] trang giá Budgets, tra 16/11).
Cảnh báo, **không phải trần cứng** — AWS không tự dừng máy. Cách dễ nhất: bảng điều khiển Billing ⇒ Budgets ⇒ Create budget. CLI (bằng người dùng có quyền Billing — người dùng IAM ở B3 chỉ có Lightsail):
  ```bash
  aws budgets create-budget --account-id <số tài khoản 12 chữ số> \
    --budget '{"BudgetName":"hue-demo","BudgetLimit":{"Amount":"30","Unit":"USD"},"TimeUnit":"MONTHLY","BudgetType":"COST"}' \
    --notifications-with-subscribers '[{"Notification":{"NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN","Threshold":80,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"<email User>"}]}]'
  ```
- Kiểm: `aws budgets describe-budgets --account-id <số tài khoản> --query "Budgets[].BudgetName"` (hoặc nhìn trang Budgets).
- Mong đợi: có `hue-demo`; email xác nhận đăng ký cảnh báo về hộp thư User.
- Dừng khi: lệnh báo lỗi quyền — làm trên bảng điều khiển thay vì CLI.

**B3.** [User] Tạo một người dùng IAM riêng cho việc deploy, chỉ quyền Lightsail (`AmazonLightsailFullAccess`), tạo access key, cài AWS CLI v2 trên máy User,
chạy `aws configure` (vùng `ap-southeast-1`, khuôn ra `json`). Không dán access key vào hội thoại. Agent chạy lệnh `aws` theo đúng Q9.
- Kiểm: `aws sts get-caller-identity --query Arn --output text`
- Mong đợi: `arn:aws:iam::<số tài khoản>:user/<tên người dùng IAM vừa tạo>`.
- Dừng khi: ARN kết thúc bằng `:root` (đang dùng tài khoản gốc) hoặc tên khác — sửa `aws configure` trước khi đi tiếp.

## 7. Giai đoạn C — tạo máy [Tiền]

Mọi lệnh có `--region ap-southeast-1`. Tên gói / ảnh hệ điều hành lấy từ đầu ra C1, không chép từ tài liệu này. Theo Q9: C1, C2 agent chạy được; C3, C4 User tự gõ (hoặc agent nếu Q9 cho).

**C1. Kiểm tên gói và ảnh hệ điều hành hiện hành** (chỉ đọc).
- Lệnh:
  ```bash
  aws lightsail get-bundles --region ap-southeast-1 --query "bundles[?ramSizeInGb==\`4\`].[bundleId,price,cpuCount,diskSizeInGb,isActive,supportedPlatforms]" --output json
  aws lightsail get-blueprints --region ap-southeast-1 --query "blueprints[?contains(blueprintId,'ubuntu_24')].[blueprintId,name,isActive]" --output table
  ```
- Mong đợi: một gói 4 GB, giá 24, `LINUX_UNIX`, `isActive` true — tên dự kiến `medium_3_0` · một blueprint Ubuntu 24.04 `isActive` true — tên dự kiến `ubuntu_24_04`
  ([Nguồn] tra 16/11: hai tên này lấy từ ví dụ công khai + ví dụ CLI của AWS, **chưa** thấy đầu ra API Singapore; giá 24 USD / 4 GB / 2 vCPU / 80 GB / 4 TB đã tự mở trang giá aws.amazon.com/lightsail/pricing 16/11).
  Gói "chỉ IPv6" (20 USD) **không** dùng: IP tĩnh IPv4 không gắn được, người chấm không có IPv6 thì không vào được.
- Dừng khi: không có gói 4 GB Linux active, hoặc giá khác 24 ⇒ báo User (đổi giá ⇒ hỏi lại Q1). Tài khoản Free plan không thấy gói 4 GB ⇒ dừng, báo User.

**C2. Khoá SSH.**
- Lệnh: `test ! -e ~/.ssh/hue-lightsail.pem && aws lightsail create-key-pair --region ap-southeast-1 --key-pair-name hue-key --query privateKeyBase64 --output text > ~/.ssh/hue-lightsail.pem && chmod 600 ~/.ssh/hue-lightsail.pem`
- Kiểm: `head -c 30 ~/.ssh/hue-lightsail.pem; echo; stat -c %a ~/.ssh/hue-lightsail.pem`
- Mong đợi: bắt đầu bằng `-----BEGIN` (chỉ in 30 ký tự đầu); quyền `600`.
- Dừng khi: file đã có từ trước (lệnh `test` chặn — không ghi đè khoá cũ, hỏi User), hoặc AWS báo tên `hue-key` đã tồn tại (khoá riêng của nó chỉ tải được một lần lúc tạo — hỏi User khoá đang ở đâu).

**C3. Tạo máy, IP tĩnh, cổng.** [Tiền] [User theo Q9]
- Lệnh:
  ```bash
  aws lightsail create-instances --region ap-southeast-1 --instance-names hue-app --availability-zone ap-southeast-1a \
    --blueprint-id <blueprint C1> --bundle-id <bundle C1> --key-pair-name hue-key
  for i in $(seq 60); do s=$(aws lightsail get-instance --region ap-southeast-1 --instance-name hue-app --query instance.state.name --output text); [ "$s" = running ] && break; sleep 10; done; echo "trạng thái: $s"
  aws lightsail allocate-static-ip --region ap-southeast-1 --static-ip-name hue-ip
  aws lightsail attach-static-ip --region ap-southeast-1 --static-ip-name hue-ip --instance-name hue-app
  aws lightsail open-instance-public-ports --region ap-southeast-1 --instance-name hue-app --port-info fromPort=443,toPort=443,protocol=TCP
  aws lightsail open-instance-public-ports --region ap-southeast-1 --instance-name hue-app --port-info fromPort=80,toPort=80,protocol=TCP
  ```
- Kiểm:
  ```bash
  aws lightsail get-instance-port-states --region ap-southeast-1 --instance-name hue-app --query "portStates[].[fromPort,state]" --output text
  aws lightsail get-static-ip --region ap-southeast-1 --static-ip-name hue-ip --query "staticIp.[ipAddress,attachedTo]" --output text
  ```
- Mong đợi: vòng chờ in `trạng thái: running` (≤ 10 phút); cổng 22, 80, 443 đều `open`; lệnh cuối in `<IP>` và `hue-app`. Dùng `open-instance-public-ports` (thêm từng cổng), không dùng `put-instance-public-ports` (lệnh đó thay cả danh sách — gõ thiếu 22 là mất SSH) [Nguồn] tài liệu CLI AWS, tra 16/11. Lightsail mặc định chỉ mở 22 / 80 ⇒ thiếu 443 thì HTTPS treo (review 07/11).
- Dừng khi: vòng chờ in trạng thái khác `running`, hoặc bất kỳ lệnh nào lỗi. `allocate-static-ip` chạy rồi mà `attach` lỗi ⇒ IP tĩnh không gắn tính 0,005 USD / giờ ⇒ báo User ngay.
- [Suy] Giới hạn cổng 22 chỉ cho IP nhà User (`cidrs=<IP nhà>/32`) an toàn hơn nhưng IP nhà đổi thì mất SSH ⇒ bản này để mở, khoá SSH là rào chính.
- Nếu Q2 = tên miền riêng: [User] tạo bản ghi A `<tên miền>` ⇒ `<IP>` ở nơi mua tên miền. Kiểm: `getent hosts <tên miền>` in `<IP>` (có thể mất vài phút tới vài giờ). Chưa ra đúng IP thì chưa làm D4 (Caddy xin chứng chỉ sẽ lỗi).

**C4. Snapshot tự động hằng ngày** (sao lưu cả máy). [Tiền] [User theo Q9]
- Lệnh: `aws lightsail enable-add-on --region ap-southeast-1 --resource-name hue-app --add-on-request 'addOnType=AutoSnapshot,autoSnapshotAddOnRequest={snapshotTimeOfDay=19:00}'`
  (giờ UTC, bước một giờ; 19:00 UTC = 02:00 giờ Việt Nam).
- Kiểm: `aws lightsail get-instance --region ap-southeast-1 --instance-name hue-app --query "instance.addOns[].[name,status,snapshotTimeOfDay]" --output text`
- Mong đợi: `AutoSnapshot Enabled 19:00`.
- Dừng khi: không có dòng `AutoSnapshot`, hoặc status khác `Enabled`.
- Lightsail giữ 7 bản gần nhất; giá 0,05 USD / GB-tháng, tính trên dung lượng thật của bản chụp (các bản sau chỉ tính phần đổi) [Nguồn] trang giá Lightsail tự mở 16/11 + tài liệu snapshot tự động.
  Ước: đĩa dùng ~15–20 GB [Suy] ⇒ ~1 USD / tháng. **Xoá máy là xoá luôn bản chụp tự động** ⇒ trước khi xoá phải có bản chụp thủ công `available` (10.5).

## 8. Giai đoạn D — cài và chạy trên máy AWS

**D1. Vào máy, cài Docker** theo tài liệu chính thức docs.docker.com/engine/install/ubuntu ([Nguồn] Codex mở 16/11; chưa chạy trên máy thật). `ssh -i <KEY> ubuntu@<IP>` (lần đầu hỏi "Are you sure…" ⇒ gõ `yes`) rồi:
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
- Kiểm: `ssh -i <KEY> ubuntu@<IP> 'docker version --format "{{.Server.Version}}" && docker compose version && systemctl is-enabled docker && free -m && df -h /'`
- Mong đợi: một số phiên bản Docker; `Docker Compose version v…`; `enabled`; `free` tổng ~3.800–4.000 MB; đĩa trống > 60 GB.
- Dừng khi: một lệnh `apt` báo lỗi (`E:`), hoặc `docker version` không in số (thường do chưa `exit` rồi SSH lại), hoặc tổng RAM < 3.500 MB (sai gói).

**D2. Chuyển file.**
- Lệnh (máy User, shell có `TAG`):
  ```bash
  ssh -i <KEY> ubuntu@<IP> 'sudo mkdir -p /srv/hue && sudo chown ubuntu:ubuntu /srv/hue'
  scp -i <KEY> ~/hue_deploy_$TAG/{app_$TAG.tar.gz,qdrant.snapshot,compose.yml,Caddyfile,SHA256SUMS,.env.deploy} ubuntu@<IP>:/srv/hue/
  ```
- Kiểm: `ssh -i <KEY> ubuntu@<IP> 'cd /srv/hue && sha256sum -c SHA256SUMS && chmod 600 .env.deploy && stat -c "%a %n" .env.deploy'`
- Mong đợi: 4 dòng `OK`; `600 .env.deploy`. Thời gian `scp` tuỳ mạng nhà (0,96 GB).
- Dừng khi: có dòng `FAILED` ⇒ chép lại đúng file đó một lần; vẫn `FAILED` ⇒ dừng, báo User.

**D3. Nạp ảnh, đặt biến, nạp dữ liệu Qdrant.**
- Lệnh (trên máy AWS — `ssh -i <KEY> ubuntu@<IP>` rồi):
  ```bash
  TAG=<7 ký tự như máy User>; COL=hue_full_corpus_7a2_e5_small_384
  cd /srv/hue && gunzip -c app_$TAG.tar.gz | docker load && mkdir -p logs qdrant_storage
  cat > hue.env <<EOF
  HUE_IMAGE=hue-rag-app:$TAG
  HUE_ENV_FILE=/srv/hue/.env.deploy
  HUE_SITE=<SITE>
  HUE_LUOT_MOI_NGAY=50
  EOF
  docker compose -p hue -f compose.yml --env-file hue.env up -d qdrant
  for i in $(seq 30); do [ "$(docker inspect -f '{{.State.Health.Status}}' hue-qdrant-1)" = healthy ] && break; sleep 2; done
  docker compose -p hue -f compose.yml --env-file hue.env cp qdrant.snapshot qdrant:/qdrant/snapshots/qdrant.snapshot
  docker compose -p hue -f compose.yml --env-file hue.env run --rm --no-deps --entrypoint python app -c "
  import json, urllib.request as u
  r = u.Request('http://qdrant:6333/collections/$COL/snapshots/recover', method='PUT', headers={'Content-Type': 'application/json'},
                data=json.dumps({'location': 'file:///qdrant/snapshots/qdrant.snapshot', 'priority': 'snapshot'}).encode())
  print(u.urlopen(r, timeout=300).read().decode())
  print(json.load(u.urlopen('http://qdrant:6333/collections/$COL'))['result']['points_count'])"
  ```
- Kiểm: `docker images hue-rag-app --format '{{.Tag}}'` có `$TAG`; `cat hue.env` (file không có khoá — in được).
- Mong đợi: `docker load` in `Loaded image: hue-rag-app:<TAG>`; lệnh `run` in `{"result":true,…}` rồi số điểm = số ở máy User (16/11: 9425).
- Dừng khi: `docker load` lỗi, Qdrant không `healthy` sau 60 s, `result` khác `true`, hoặc số điểm khác.
- `hue.env` chỉ chứa biến không bí mật. Khoá nằm riêng ở `.env.deploy` (quyền 600), compose nạp vào container app qua `env_file`, không nằm trong ảnh.

**D4. Chạy cả bộ.**
- Lệnh: `docker compose -p hue -f compose.yml --env-file hue.env up -d && sleep 60 && docker compose -p hue -f compose.yml --env-file hue.env ps`
- Mong đợi: 3 container `running` / `Up`, qdrant `healthy` (16/11 trên máy User: app trả lời sau 25 s).
- Dừng khi: container nào thoát (`docker compose -p hue -f compose.yml --env-file hue.env logs <tên> | tail -40`, báo User; không dán log có nội dung người dùng vào chỗ công khai).

## 9. Giai đoạn E — kiểm sau khi lên (từ máy User)

| Kiểm | Lệnh | Mong đợi |
|---|---|---|
| HTTPS | `curl -sI https://<SITE>/ \| head -1` | `HTTP/2 200` (lần đầu Caddy xin chứng chỉ có thể mất ~30 s; lỗi chứng chỉ sau 5 phút ⇒ `docker compose … logs caddy \| tail -20`, dừng) |
| http chuyển sang https | `curl -sI http://<SITE>/ \| head -3` | 308 sang `https://` |
| Trang API tắt | `curl -s -o /dev/null -w '%{http_code}' https://<SITE>/docs` | `404` |
| Tính năng | `curl -s https://<SITE>/api/tinh_nang` | `tra_web` đúng Q4; `anh` đúng Q6 |
| Câu trong kho | mở trình duyệt, hỏi một câu về một món / di tích có trong kho | câu trả lời có nguồn; chữ hiện dần (không đợi cả câu) |
| Câu ngoài kho | hỏi một câu không về Huế | câu từ chối |
| Cookie | trình duyệt: hỏi 2 câu liên tiếp, câu 2 dùng "ở đó" | câu 2 hiểu đúng nơi của câu 1 (nhớ hội thoại cần cookie Secure qua https) |
| Hỏi bằng ảnh (nếu Q6 bật) | trình duyệt: bấm dấu cộng, chọn một ảnh di tích, bấm Hỏi | có tên đoán hoặc thẻ chọn tên — route ảnh so `Origin` với scheme (`backend/api/routes/anh.py`), chỉ đúng khi qua https; báo lỗi ⇒ dừng |
| Hết lượt (rào hai chiều) | trên máy AWS: `sed -i 's/^HUE_LUOT_MOI_NGAY=.*/HUE_LUOT_MOI_NGAY=3/' hue.env && docker compose -p hue -f compose.yml --env-file hue.env up -d app`; trình duyệt hỏi đủ 4 lượt; rồi `sed -i 's/^HUE_LUOT_MOI_NGAY=.*/HUE_LUOT_MOI_NGAY=50/' hue.env && docker compose … up -d app` | lượt 1–3 trả lời bình thường, lượt 4 báo "đã dùng hết số lượt"; sau khi trả về 50: `grep LUOT hue.env` in `=50` |
| RAM | `ssh … 'docker stats --no-stream'` | app < 2 GiB (16/11 máy User: 1.021 MiB), `free -m` cột available > 500 MB |
| Log không ghi câu hỏi / IP | `ssh … 'grep -c "chat_metrics" /srv/hue/logs/application.log'` | số dòng = số lượt đã hỏi; người chạy không in nội dung log ra hội thoại |
| Sổ vết tắt | `ssh … 'docker compose -p hue -f /srv/hue/compose.yml --env-file /srv/hue/hue.env exec -T app env \| grep -c HUE_SO_VET'` | `0` |

Ghi kết quả từng dòng (đạt / không) vào report deploy. Có dòng "không" ⇒ dừng, không gửi link cho ai.

## 10. Vận hành

**10.1 Sao lưu.** Máy: snapshot tự động hằng ngày (C4). Dữ liệu Qdrant không đổi khi chạy (chatbot chỉ đọc) ⇒ bản `qdrant.snapshot` trong `~/hue_deploy_<TAG>/` trên máy User
là bản sao lưu đủ (giữ thư mục này tới khi xoá máy). Log: `/srv/hue/logs` (xoay vòng 10 MB × 3 trong ảnh; log stdout Docker 10 MB × 3 mỗi container — `compose.yml`).

**10.2 Cập nhật bản mới.**
- Lệnh: trên máy User làm lại A1–A7 (shell mới có `TAG` mới; bản chụp Qdrant cùng đi để ảnh và dữ liệu luôn khớp — app so hash kho với build record lúc khởi động),
  `scp` như D2 (thư mục `~/hue_deploy_<TAG mới>`). Trên máy AWS: `cd /srv/hue && sha256sum -c SHA256SUMS && TAG=<TAG mới> && gunzip -c app_$TAG.tar.gz | docker load`,
  ghi nhãn đang chạy `grep HUE_IMAGE hue.env > hue_image_cu.txt`, sửa `sed -i "s/^HUE_IMAGE=.*/HUE_IMAGE=hue-rag-app:$TAG/" hue.env`.
  Kho đổi ⇒ nạp lại bản chụp như D3 (lệnh `cp` + `run`) **trước** khi chạy app mới. Rồi `docker compose -p hue -f compose.yml --env-file hue.env up -d app`.
- Kiểm: `docker compose -p hue -f compose.yml --env-file hue.env ps app --format '{{.Image}}'` rồi làm lại toàn bộ bảng §9.
- Mong đợi: ảnh `hue-rag-app:<TAG mới>`; mọi dòng §9 đạt.
- Dừng khi: dòng nào §9 "không" ⇒ làm **10.3 ngay**, rồi báo User.

**10.3 Quay lại bản cũ.**
- Lệnh: `cd /srv/hue && cat hue_image_cu.txt && sed -i "s|^HUE_IMAGE=.*|$(cat hue_image_cu.txt)|" hue.env && docker compose -p hue -f compose.yml --env-file hue.env up -d app`
  (kho đã nạp lại ở 10.2 ⇒ nạp lại bản chụp cũ trong `~/hue_deploy_<TAG cũ>/` như D3 trước lệnh `up`).
- Kiểm: `docker compose -p hue -f compose.yml --env-file hue.env ps app --format '{{.Image}}'` + 4 dòng đầu §9.
- Mong đợi: ảnh = nhãn trong `hue_image_cu.txt`; 4 dòng đạt.
- Dừng khi: app không lên ⇒ báo User (còn đường cuối: khôi phục máy từ snapshot tự động của đêm trước — bảng điều khiển Lightsail ⇒ Snapshots ⇒ Create new instance).
- Dọn đĩa: giữ tối đa 2 ảnh cũ (`docker image rm hue-rag-app:<nhãn quá cũ>`; đĩa 80 GB).

**10.4 Khi có sự cố.** App 503 / không trả lời: `docker compose -p hue -f compose.yml --env-file hue.env logs app | tail -50` (không chép vào chỗ công khai). Hết hạn mức OpenAI
(hard limit Q3): người dùng thấy lỗi ⇒ User nâng hạn mức ở trang OpenAI. Máy hết RAM: `docker stats --no-stream`, `sudo dmesg | grep -i oom`. Mọi trường hợp: báo User, không tự đổi cấu hình.

**10.5 Kết thúc demo.** [User] (theo Q8; bước phá huỷ — User tự gõ, agent chỉ đưa lệnh)
- Lệnh:
  ```bash
  aws lightsail create-instance-snapshot --region ap-southeast-1 --instance-name hue-app --instance-snapshot-name hue-cuoi
  for i in $(seq 60); do s=$(aws lightsail get-instance-snapshot --region ap-southeast-1 --instance-snapshot-name hue-cuoi --query instanceSnapshot.state --output text); [ "$s" = available ] && break; sleep 20; done; echo "bản chụp: $s"
  ```
  **Chỉ khi** dòng trên in `bản chụp: available`:
  ```bash
  aws lightsail delete-instance --region ap-southeast-1 --instance-name hue-app
  aws lightsail release-static-ip --region ap-southeast-1 --static-ip-name hue-ip
  ```
- Kiểm: `aws lightsail get-instances --region ap-southeast-1 --query "instances[].name" --output text` · `aws lightsail get-static-ips --region ap-southeast-1 --query "staticIps[].name" --output text` · `aws lightsail get-instance-snapshots --region ap-southeast-1 --query "instanceSnapshots[].[name,state]" --output text`
- Mong đợi: không còn `hue-app`; không còn `hue-ip`; còn `hue-cuoi available`.
- Dừng khi: vòng chờ in trạng thái khác `available` (sau ~20 phút) ⇒ **không xoá máy**, báo User.
- Sau đó: IP tĩnh gắn máy thì miễn phí; không gắn quá một giờ ⇒ 0,005 USD / giờ [Nguồn] tài liệu static IP Lightsail, tra 16/11 ⇒ `release-static-ip` ngay sau khi xoá máy. Bản chụp thủ công ~0,05 USD / GB-tháng ⇒ khi không cần nữa:
  `aws lightsail delete-instance-snapshot --region ap-southeast-1 --instance-snapshot-name hue-cuoi`. Xoá luôn người dùng IAM / access key ở B3 nếu không dùng nữa.

## 11. Bảng rà khung AI FDE (agent-security-review) cho bản công khai

| Mục | Hiện trạng | Mức | Đề xuất |
|---|---|---|---|
| Bộ ba chết người | (a) dữ liệu riêng tư: kho private trong ảnh, không có dữ liệu người dùng lưu lâu (hội thoại trong RAM); (b) nội dung không tin cậy: câu người dùng, ảnh người dùng, đoạn web (nếu Q4 bật); (c) đường ra: OpenAI (câu hỏi + 10 đoạn kho + ảnh), Serper (nếu bật), Open-Meteo (chỉ toạ độ Huế, không chữ người dùng) [Đọc] `backend/llm/thoi_tiet.py`, `tra_web.py` | minor | Đủ ba nhưng đường ra chỉ là API của nhà cung cấp model / tìm kiếm, không có công cụ ghi / gửi tin. Q4 tắt ⇒ bớt một đường. Không thêm công cụ ghi ra ngoài trên bản công khai |
| Chữ người dùng là dữ liệu | đã có rào chữ trong ảnh (model chỉ-ảnh không theo chữ dán), bộ an toàn 32 câu chạy ở mỗi đổi lời dặn | minor | Không đổi cho deploy |
| Giới hạn ở API | giới hạn lượt / IP / ngày trong RAM `backend/api/gioi_han.py` — [Đo] 16/11 trên ảnh `a9d1674`: lượt 4 ⇒ 429, giả `X-Forwarded-For` ⇒ vẫn 429; hạn mức chi tiêu OpenAI (Q3) | major nếu Q3 = không | Khoá riêng + hard limit ở trang OpenAI là lớp thứ hai bắt buộc; giới hạn lượt reset khi app khởi động lại (đếm trong RAM) — chấp nhận cho demo |
| Quyền hẹp | IAM riêng chỉ Lightsail (B3); agent chỉ chạy lệnh chỉ đọc (Q9); khoá SSH riêng; cổng mở 22 / 80 / 443; app không mở cổng ra ngoài (chỉ Caddy) [Đọc] `compose.yml` | minor | `--forwarded-allow-ips '*'` chỉ an toàn khi app không có `ports` — giữ nguyên ghi chú trong compose |
| Khoá không vào ảnh / log | `.env` loại khỏi build (`**/.env` trong `.dockerignore`), khoá nạp lúc chạy; log không ghi câu hỏi / IP [Đo] 16/11: 1 dòng `chat_metrics`, 0 chữ câu hỏi, 0 IP | minor | A4 kiểm lại mỗi lần build |
| Dữ liệu cá nhân | log `chat_metrics` không có câu hỏi / IP; sổ vết có nội dung TẮT trên bản công khai (không đặt `HUE_SO_VET`); ảnh người dùng không lưu ở server [Đọc] `backend/core/so_vet.py`, `compose.yml` | minor | Trang Giới thiệu đã nói câu hỏi / ảnh gửi sang nhà cung cấp model; nếu Q6 bật thì kiểm dòng báo cạnh nút ảnh có trên bản build |
| Kho private trong ảnh | ảnh không lên registry công khai; chỉ `scp` | major nếu ai đẩy ảnh lên Docker Hub | Luật ở §0; không tạo ECR công khai |
| Rào đo hai chiều | [Đo] 16/11 trên máy User: 1 câu thường đi qua + 3 ca xấu bị chặn (lượt 4, `/api/chat` không stream, giả `X-Forwarded-For`) | — | §9 dòng "Hết lượt" làm lại trên máy thật |

**Giả định an toàn:** chạy trên một máy Lightsail do User sở hữu; ai có link đều gọi được; giới hạn chi tiêu = giới hạn lượt / IP / ngày + hard limit
OpenAI; chưa rào: một người dùng nhiều IP vẫn dùng được nhiều lượt (chặn bằng hạn mức OpenAI), lượt bị Dừng vẫn tính tiền phần đã chạy.

## 12. Tra cứu (16/11/2026)

- Codex: yêu cầu chỉ thông tin công khai ⇒ `data/tra_cuu_cli/2026-11-16_deploy-aws-2/ket_qua.md` (155 s, 34 trang mở được, 0 lệnh shell). Kết quả là dữ liệu ngoài.
- E tự mở kiểm 2 ý chính: trang giá Lightsail (2 GB 12 · 4 GB 24 · 8 GB 44 USD; snapshot 0,05 USD / GB-tháng) và tài liệu snapshot Qdrant
  (đường API, `file://` dùng được, `priority: snapshot`, tương thích minor). Còn lại ghi [Nguồn] theo Codex, chưa tự mở.
- Còn chưa chắc: tên `medium_3_0` / `ubuntu_24_04` (C1 lấy từ đầu ra thật); gói 4 GB có tạo được trên Free plan không; credit có trừ vào Lightsail không; lệnh cài Docker chưa chạy trên máy thật.
- Tra cũ 07/11 (EC2, Secrets Manager 0,40 USD / khoá / tháng, Parameter Store bản thường miễn phí): `data/tra_cuu_cli/2026-11-07_e-dep-aws/`. Spec chọn `.env.deploy` quyền 600 trên máy
  (đơn giản nhất, đủ cho một máy demo); Secrets Manager / Parameter Store chỉ đáng khi nhiều máy hoặc cần xoay khoá.

## 13. Chạy thử trên máy User — 16/11/2026 (E, ảnh `hue-rag-app:a9d1674` = `main` có nút Huỷ ảnh)

| Bước | Kết quả | Nhãn |
|---|---|---|
| A2 | dockerignore sinh lại: 263 bài + 14 mục, giống hệt bản cũ; đoạn kiểm 8 / 8 `OK` | [Đo] |
| A3 | build đạt, **8 s** (tầng phụ thuộc Python + model e5 dùng cache; giao diện, code, kho build mới); ảnh 3,6 GB | [Đo] |
| A4 | 0 file cấm (sau khi bỏ qua `backend/` — bản 1 bắt nhầm 2 file code `*golden*.py`); 263 bài = 263 trong build record | [Đo] |
| A5 bản chụp | tạo 56,5 MB trong 0,35 s trên Qdrant 6335, tải về, **xoá lại** (danh sách rỗng, 6335 vẫn 9.425 điểm) | [Đo] |
| A5 khôi phục | ảnh Qdrant không có `curl` ⇒ chạy qua container dùng một lần của ảnh app: `{"result":true}`, **9.425 điểm**, ~1 s | [Đo] |
| A5 chạy cả bộ | `/health` trả lời sau **25 s**: `/` 200 · `/health` ok (qdrant, retrieval, tokenizer, generator ready) · `/docs` 404 · `tra_web` false · `anh` true | [Đo] |
| A5 câu thật | 1 câu trong kho (luồng stream): 4,5 s cả câu, 157 mảnh chữ, có nguồn đúng bài; **≈ 0,00045 USD** | [Đo] |
| A5 hết lượt | 2 lượt POST ảnh sai kiểu (415, không gọi model nhưng vẫn tính lượt) ⇒ lượt 4 **429** · `/api/chat` **429** · giả `X-Forwarded-For` **429** | [Đo] |
| A5 log | 1 dòng `chat_metrics` · 3 dòng "Rate limited" · 0 dòng có chữ câu hỏi · 0 IP | [Đo] |
| RAM | app 1.021 MiB / 2 GiB · Qdrant 222 MiB / 768 MiB · Caddy 18 MiB. Máy User `free -m` available: 8.765 MB trước ⇒ 8.702 lúc chạy ⇒ 8.769 sau | [Đo] |
| A6 | `docker save \| gzip -1` = **0,90 GB**, 32 s | [Đo] |
| Dọn | thư mục Qdrant thử thuộc root ⇒ xoá qua `docker run … rm -rf` (lệnh ở A5); 0 container thử còn lại | [Đo] |
| A6 bản đủ (`SHA256SUMS` 4 file), A7, B–E, 10.x | **chưa chạy** — A6 bản đủ chạy lúc deploy thật; B–E cần tài khoản AWS (Q1) | NOT RUN |

## Lịch sử bản

- Bản 1 (E, xong 14:36 16/11/2026, đã điền kết quả tra): đủ các giai đoạn; §13 chưa chạy.
- Bản 2 (E, xong 14:47 16/11/2026): sửa theo review C vòng 1 (`2026-11-16-deploy-aws-design_review.md`, 3 major + 6 minor) + chạy thử A2–A6 (§13).
  M-1: 10.5 chờ bản chụp `available` có trần, mọi lệnh `--region`, nhãn [User], kiểm sau khi xoá. M-2: A6, A7, B2, B3, C2, C3, C4, D1, D2, D3, 10.2, 10.3 đủ Kiểm / Mong đợi / Dừng khi.
  M-3: §3 thêm tổng tiền cả đợt + Q9 (agent chạy `aws`) + Q10 (ngày tạo máy) + Q11 (giữ file deploy). m-1: xoá bản chụp khỏi 6335 ngay sau khi tải (A5, A6). m-2: A2 `THIEU` ghi lại, phán quyết ở A5.
  m-3: `TAG` / `COL` là biến shell, đặt lại trên máy AWS ở D3. m-4: vòng chờ C3 có trần 10 phút. m-5: §9 thêm dòng hết lượt + dòng ảnh qua https. m-6: §4 md5 file deploy + Q11.
  Thêm từ chạy thử: A4 bỏ qua `backend/`; lệnh dọn thư mục root; A1 chỉ xét phần code đi vào ảnh.
