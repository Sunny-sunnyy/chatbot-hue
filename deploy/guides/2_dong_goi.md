# Guide 2 — Dựng ảnh, thử ở máy mình, đóng gói và đưa gói lên thùng

Viết: 19:50 23/11/2026, phiên C (đồng bộ mốc 26/11/2026). Các lệnh dựng ảnh, thử trọn gói, đóng gói ở guide này ĐÃ chạy thật ở máy chủ dự án ngày 23/11 (ba lượt — bảng ở
`deploy/docker/README.md` mục 5), nhưng mới với model Claude hoặc với khoá OpenAI giả. **Chưa có lượt nào chạy gói đầy đủ từ `s3://` lên AWS với khoá OpenAI thật**, và lệnh đẩy
lên thùng chưa ai chạy **[chưa kiểm trên AWS]**.

Từ dùng: **ảnh** = Docker image · **hộp** = container · **gói** = thư mục `~/hue_goi_<sha>/` chứa mọi thứ máy chủ cần · **thùng** = thùng S3 riêng tư của
tầng nền · **sha** = bảy ký tự đầu của mã commit · **bản chụp** = file Qdrant xuất ra chứa trọn chỉ mục · **hồ sơ** = bộ khoá + vùng của AWS CLI (guide 0).

## 1. Mục tiêu

Có MỘT gói dựng từ ĐÚNG MỘT commit, đã chạy thử trọn ở máy mình bằng chính model sẽ chạy trên máy chủ (OpenAI), nằm trong thùng riêng tư — sẵn cho
guide 4 tải về máy chủ.

## 2. Sẽ dựng gì

| Thứ | Ở đâu | Cỡ |
|---|---|---|
| Ảnh `hue-rag-app:<sha>` | Docker của máy mình | khoảng 3,6 GB |
| Gói `~/hue_goi_<sha>/` | máy mình | khoảng 1 GB |
| Bản chép của gói | `s3://<thùng>/<sha>/` | khoảng 1 GB |

Gói gồm: `app_<sha>.tar.gz` (ảnh app nén) · `qdrant.snapshot` (chỉ mục) · `compose.yml` · `Caddyfile` · `nap_chi_muc.sh` · thư mục con `cau_hinh/`
(`settings.yaml` đã ghi sẵn `provider: openai`, `logging.yaml`) · `SHA256SUMS` (băm của bảy file trên). Gói có THƯ MỤC CON ⇒ đẩy và tải phải dùng kiểu
đệ quy.

**Gói này RIÊNG TƯ.** Ảnh mang **11 file riêng tư** từ thư mục `data/` (**9 file cấu hình/bảng từ `settings.yaml` + 2 file bản ghi dựng chỉ mục và thống kê từ khoá**). Vì vậy: chỉ đẩy lên thùng của CHÍNH
mình (thùng của tầng nền đã chặn mọi truy cập công khai), không đẩy ảnh lên Docker Hub hay kho ảnh công khai nào. Khi chạy bước 6, dữ liệu riêng của
dự án rời máy mình lên tài khoản AWS của mình — đó là việc làm có chủ ý, không phải tác dụng phụ.

**Khác khoá học — không dùng kho ảnh ECR:** ở khoá học ảnh được đẩy lên ECR rồi dịch vụ chạy kéo về. Ở đây ảnh được nén thành một file đặt trong thùng,
máy chủ tải về rồi nạp (`docker load`): bớt một dịch vụ phải dựng, phải cấp quyền và phải phá; và ảnh có file riêng tư nên càng ít nơi giữ nó càng tốt.

## 3. Điều kiện trước

- Guide 0, guide 1 xong (có hồ sơ deploy; có thùng). Từ 25/11/2026, cả máy mình lẫn bản deploy đều chạy mặc định `gpt-6-luna` (`provider: openai`), bộ kho hiện hành **269 bài / 9.540 điểm / 269/269 ảnh Khám phá**.
- Ở máy mình: Docker đang chạy; Qdrant của dự án đang chạy ở cổng 6335 và chỉ mục khớp kho của commit sẽ dựng (lệnh dựng tự so băm, lệch thì dừng).
- Một file khoá riêng cho lượt thử, KHÔNG phải `.env` của dự án, ví dụ `~/hue_khoa_thu.env`, quyền 600, có đúng một dòng `OPENAI_API_KEY=…`
  (khoá riêng của bản deploy, tạo ở guide 0). Tự gõ bằng `nano`; không dán khoá vào cửa sổ của agent nào. Tạo file rỗng với quyền 600 TRƯỚC rồi
  mới gõ khoá vào, để khoá không lúc nào nằm trong một file người dùng khác của máy đọc được:

  ```bash
  touch ~/hue_khoa_thu.env && chmod 600 ~/hue_khoa_thu.env
  nano ~/hue_khoa_thu.env          # gõ đúng MỘT dòng: OPENAI_API_KEY=<khoá lấy từ chỗ cất mật khẩu>  rồi lưu (Ctrl+O, Enter, Ctrl+X)
  ls -l ~/hue_khoa_thu.env         # mong: dòng bắt đầu bằng -rw-------
  ```

  File này chỉ sống trong lượt thử: thử xong thì xoá (mục 10).
- Không dựng ảnh trên máy chủ: máy chủ 4 GB RAM không đủ rộng để dựng, và ảnh đưa lên phải là ảnh ĐÃ thử.
- RAM khả dụng ở máy mình từ 4 GB trở lên (dựng ảnh lần đầu dùng khoảng 2 GB); không chạy cùng lúc với việc nặng khác.

## 4. File liên quan

| File | Việc |
|---|---|
| `deploy/docker/dung_ngu_canh.py` | gom code + bài kho từ commit, gom file bảng riêng tư theo `settings.yaml`; `--chi-kiem` = chỉ đối chiếu, không dựng |
| `deploy/docker/dung_anh.sh <commit>` | một lệnh dựng ảnh rồi tự kiểm ảnh |
| `deploy/docker/thu_o_may.sh len / kiem / don` | chạy thử trọn gói ở máy mình, cổng 8880, không đụng server 8010 |
| `deploy/docker/dong_goi.sh <sha>` | gom gói vào `~/hue_goi_<sha>/`, ghi sẵn `provider: openai`, tính băm |
| `deploy/docker/compose.yml`, `Caddyfile`, `nap_chi_muc.sh` | đi theo gói lên máy chủ |
| `deploy/docker/README.md` | giải thích gói + bảng các lượt đã thử |

## 5. Cấu hình

| Thứ | Giá trị | Ghi chú |
|---|---|---|
| Commit dựng | `origin/main` (hoặc một mã commit) | PHẢI ghi rõ — để mặc định thì ảnh mang code của nhánh đang đứng |
| `HUE_IMAGE` | `hue-rag-app:<sha>` | lệnh dựng in ra |
| `HUE_KHOA_ENV` | đường dẫn file khoá thử | chỉ cho lượt thử ở máy; không đi theo gói |
| Model viết của gói | `openai` | `dong_goi.sh` ghi sẵn vào `cau_hinh/settings.yaml` của gói — không sửa tay |
| Hồ sơ AWS | `hue-rag-deploy` (tên đặt ở guide 0) | chỉ dùng ở bước 6 |
| Tên thùng | `terraform output -raw artifact_bucket_name` ở `1_nen_tang` | — |

## 6. Từng bước

Mọi lệnh đứng ở gốc repo trừ khi ghi khác. `<sha>` = bảy ký tự lệnh dựng in ra ở bước 2 — thay vào mọi chỗ có `<sha>`. Bước 5, 6 và mục 7, 10 dùng biến
`THUNG` đặt ở bước 5 ⇒ gõ trong CÙNG một cửa sổ lệnh (mở cửa sổ mới thì chạy lại dòng `THUNG=…` của bước 5).

**Bước 1 — lấy code mới nhất và đối chiếu 0 đồng** (vài giây, không dựng gì): danh sách file riêng tư của gói sinh từ chính `settings.yaml` của commit,
nên cấu hình trỏ sang bảng mới thì gói tự theo; thứ có thể hỏng là file đó không có trên máy dựng.

```bash
cd /home/minhhieu/hue_rag
git fetch origin
uv run --project backend --no-sync python deploy/docker/dung_ngu_canh.py --ref origin/main --du-lieu data --chi-kiem
```

Mong: mỗi file một dòng `có`, dòng cuối ghi `thiếu 0`. Có dòng `THIẾU` ⇒ dừng (mục 8).

**Bước 2 — dựng ảnh** (lần đầu vài phút; lần sau vài giây nhờ bộ đệm):

```bash
cd /home/minhhieu/hue_rag
deploy/docker/dung_anh.sh origin/main
```

Mong dòng cuối: `XONG: hue-rag-app:<sha> · 3.6…GB · <số bài> bài kho · 0 file cấm`. Ghi lại `<sha>`. Lệnh tự kiểm trong ảnh: không có file cấm (bộ câu
kín, bộ câu mẫu…), số bài kho bằng bản ghi dựng chỉ mục, model nhúng nạp được khi KHÔNG có mạng, ảnh là `linux/amd64`.

**Bước 3 — chạy thử trọn gói ở máy mình BẰNG KHOÁ OPENAI.** Lượt thử phải chạy trên đúng model và cấu hình hộp sẽ lên máy chủ (`provider: openai`, `USER hue`).

```bash
cd /home/minhhieu/hue_rag
HUE_IMAGE=hue-rag-app:<sha> HUE_KHOA_ENV=$HOME/hue_khoa_thu.env deploy/docker/thu_o_may.sh len
deploy/docker/thu_o_may.sh kiem
```

`len` bật ba hộp ở cổng 8880, nạp chỉ mục từ Qdrant 6335 của dự án (chỉ đọc) và in `ĐÃ LÊN`. `kiem` không gọi model; mong: trang chủ 200 · `/health`
có `"status":"ok"` · `/docs` 404 · số bài bằng bản ghi dựng · thân 13 MB ⇒ 413. Cuối `kiem` in sẵn HAI lệnh `curl` có phí — chạy cả hai:

- **Một câu hỏi thật** ("Vé tham quan Đại Nội bao nhiêu?"): mong câu trả lời có nguồn. Thấy "Không thể tạo câu trả lời vào lúc này" ⇒ khoá sai, bị thu hồi
  hoặc tài khoản OpenAI hết tiền. Đây là phép kiểm DUY NHẤT cho biết khoá dùng được: app chỉ kiểm CÓ dòng khoá, `/health` không gọi model.
- **Một lượt xếp lịch thật**: mong HTTP 200 và mỗi điểm có câu tả thật (không phải câu dự phòng kiểu "— điểm di tích."). Chỉ đường xếp lịch đọc các
  file bảng riêng tư trong ảnh, nên đây là phép kiểm rằng ảnh mang đủ bảng.

Mở thêm `http://127.0.0.1:8880` bằng trình duyệt và hỏi một câu: kiểm chữ CHẠY DẦN ra qua cửa vào Caddy và không bị dồn cả đoạn một lần.

```bash
deploy/docker/thu_o_may.sh don          # dọn ba hộp thử; Qdrant 6335 của dự án không bị đụng
```

**Bước 4 — đóng gói:**

```bash
cd /home/minhhieu/hue_rag
deploy/docker/dong_goi.sh <sha>
cd ~/hue_goi_<sha>
sha256sum -c SHA256SUMS                          # mong: mọi dòng OK
grep -n '^  provider:' cau_hinh/settings.yaml    # mong: provider: openai
```

**Bước 5 — đúng người, đúng vùng** (hồ sơ mặc định trên máy là người dùng của khoá học, cùng tài khoản — quên `--profile` là đẩy bằng nhầm người):

```bash
aws sts get-caller-identity --profile hue-rag-deploy     # NHÌN "Arn": phải kết bằng user/hue-rag-deploy
THUNG=$(cd /home/minhhieu/hue_rag/deploy/terraform/1_nen_tang && terraform output -raw artifact_bucket_name); echo "$THUNG"
```

**Bước 6 — đẩy gói lên thùng** (khoảng 1 GB; đây là lúc dữ liệu riêng rời máy):

```bash
aws s3 cp ~/hue_goi_<sha>/ "s3://$THUNG/<sha>/" --recursive --profile hue-rag-deploy --region ap-southeast-1
```

## 7. Kiểm

```bash
aws s3 ls "s3://$THUNG/<sha>/" --recursive --human-readable --profile hue-rag-deploy --region ap-southeast-1
```

Mong TÁM dòng: sáu file ở gốc (`app_<sha>.tar.gz` gần 1 GB, `qdrant.snapshot`, `compose.yml`, `Caddyfile`, `nap_chi_muc.sh`, `SHA256SUMS`) và hai
file trong `cau_hinh/` (`settings.yaml`, `logging.yaml`) — tức bảy file được băm + chính file băm. Băm sẽ được kiểm lại trên máy chủ ở guide 4, nên ở đây chỉ cần đủ file và cỡ hợp lý.

Thùng không mở công khai: `aws s3api get-public-access-block --bucket "$THUNG" --profile hue-rag-deploy --region ap-southeast-1` phải in bốn dòng `true`.

## 8. Gỡ lỗi

| Thấy gì | Vì sao | Làm gì |
|---|---|---|
| Bước 1 in `THIẾU data/…` | cấu hình của commit trỏ tới một bảng không có trên máy này | tìm file đó (thường do một phiên vừa đổi bảng); không sửa `settings.yaml` cho qua |
| `dung_anh.sh` dừng "kho lệch băm với chỉ mục" | bài kho của commit khác bài đã dựng chỉ mục | cập nhật chỉ mục trước (runbook mục 5b) rồi dựng lại |
| `len` báo đỏ sau khoảng ba phút, `/health` `degraded`, `generator: not_ready` | không có dòng `OPENAI_API_KEY` (quên đặt `HUE_KHOA_ENV`) | đặt biến trỏ đúng file khoá rồi `don`, `len` lại |
| `len` xanh, `kiem` xanh, nhưng câu hỏi ra "Không thể tạo câu trả lời vào lúc này" | khoá sai / bị thu hồi / hết tiền nạp — "xanh giả" | xem trang quản lý OpenAI; sửa file khoá; `don`, `len` lại |
| `len` dừng vì `HUE_KHOA_ENV` là `.env` | script từ chối đọc `.env` của dự án | tạo file riêng chỉ có dòng khoá |
| Cổng 8880 đang bận | một lượt thử trước chưa dọn | `deploy/docker/thu_o_may.sh don` |
| `aws s3 cp` báo `AccessDenied` | hồ sơ sai, hoặc chính sách của người dùng deploy thiếu quyền ghi thùng | xem lại bước 5; bổ sung quyền ở guide 0 |
| `s3 ls` thiếu `cau_hinh/` | quên `--recursive` | chạy lại lệnh đẩy |

## 9. Ghi chú chi phí

- Lưu khoảng 1 GB trong thùng: vài xu một tháng. Mỗi gói cũ để lại là thêm khoảng 1 GB — xoá gói không còn dùng (mục 10).
- Lượt thử ở bước 3 gọi OpenAI hai ba lần: vài xu, trừ vào số tiền đã nạp trước.
- Đẩy lên thùng không tốn tiền lưu lượng; tải từ thùng về máy chủ cùng vùng cũng không.

## 10. Dọn dẹp

```bash
aws s3 rm "s3://$THUNG/<sha cũ>/" --recursive --profile hue-rag-deploy --region ap-southeast-1    # xoá một gói cũ khỏi thùng
rm -rf ~/hue_goi_<sha cũ>                                                                     # gói cũ ở máy mình
docker image rm hue-rag-app:<sha cũ>                                                          # ảnh cũ ở máy mình
```

Giữ lại ít nhất gói ĐANG chạy trên máy chủ và gói liền trước nó — guide 6 dùng gói liền trước để lùi bản. Chỉ xoá thư mục, ảnh do chính lượt này tạo.

File khoá thử — XOÁ ngay khi lượt thử ở bước 3 đã xong và các hộp thử đã tắt (không chờ tới lúc dọn gói cũ):

```bash
rm ~/hue_khoa_thu.env
ls ~/hue_khoa_thu.env            # mong: No such file or directory
```

Khoá vẫn còn ở chỗ cất mật khẩu của mình (guide 0 bước 9); lần cập nhật bản mới cần thử lại thì tạo lại file theo mục 3. Để file nằm lại là để khoá
gọi model tốn tiền thật nằm thêm ở một nơi không ai cần tới nó.

## 11. Guide kế

`3_may_chu.md` — dựng máy (bắt đầu tính tiền). Nếu máy đã có sẵn và đây là lần cập nhật bản mới: sang thẳng mục "Cập nhật bản mới" của `6_ngay_demo.md`.
