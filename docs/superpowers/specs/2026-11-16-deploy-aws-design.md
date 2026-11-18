# Spec bản 3: deploy chatbot Huế lên AWS (một máy Lightsail, Docker Compose)

E viết bản 1, xong lúc 14:36 16/11/2026, theo việc A giao (User 16/11: mọi việc local và kế hoạch deploy phải xong trước 30/11; từ tháng 12 Codex / Gemini làm tiếp).
**Chỉ là tài liệu.** Viết spec này không tạo tài nguyên AWS nào và không gọi AWS.
**Trạng thái:** bản 2 đã được A duyệt 14:53 16/11/2026 (mã `e847b47ad995`, sau review C hai vòng). **Bản 3 (B viết 08:46 18/11/2026) = bản 2 + một lượt sửa** theo đối chiếu với
bốn khoá học của User và bàn nhóm 17/11 (danh sách chỗ đổi ở "Lịch sử bản") — **chờ E đọc lại + A duyệt mã mới.** Ba câu ở §3 ghi **"chờ User"** (A đang hỏi lại): Q3, Q8, Q12.
**Chưa có lệnh AWS nào trong tài liệu này từng được chạy** (chưa có tài khoản) — xem nhãn [Chạy] / [chưa chạy] ở §0.

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

**Lệnh nào đã chạy thật, lệnh nào chưa** (bản 3 — người chạy đọc bảng này trước; lệnh [chưa chạy] có thể sai cú pháp / sai tên, gặp lỗi thì dừng theo "Dừng khi", không sửa đoán):

| Phần | Nhãn | Ghi chú |
|---|---|---|
| A2–A6 (trừ `SHA256SUMS` bản đủ) | **[Chạy]** 16/11 trên máy User, ảnh `a9d1674` (§13) | từ đó compose thêm một dòng `HUE_GIT_SHA` — [Chạy] 18/11 chỉ ở mức `docker compose config` (biến vào đúng container app) |
| A1, A7 | [chưa chạy] | lệnh git / soạn file thường |
| B1–B3 (tài khoản, ngân sách, người dùng IAM) | **[chưa chạy]** | làm trên trang web AWS; B3 đổi cách cấp quyền ở bản 3 — chưa thử trên tài khoản thật |
| C1–C4 (mọi lệnh `aws lightsail …`) | **[chưa chạy]** | tên gói / ảnh hệ điều hành lấy từ đầu ra C1, không tin tên ghi sẵn |
| D1–D4 (cài Docker, chuyển file, chạy trên máy AWS) | **[chưa chạy]** trên máy AWS | phần nạp bản chụp Qdrant + chạy cả bộ giống A5 đã [Chạy] ở máy User |
| §9 (kiểm sau khi lên) | **[chưa chạy]** qua https | các dòng hết lượt, `/docs` 404, log không nội dung đã [Chạy] ở máy User qua http (§13) |
| 10.2–10.5 (cập nhật, quay lại, dừng khẩn, kết thúc) | **[chưa chạy]** | 10.5 là bước phá huỷ — User tự gõ |

Muốn biến [chưa chạy] thành [Chạy] trước ngày cần demo: một buổi diễn tập "tạo ⇒ kiểm ⇒ xoá" (~0,03 USD / giờ máy, Q10) — User quyết có làm không và làm mức nào.

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

**User đã nhận cả 11 mặc định Q1–Q11 làm quyết định hiện tại (14:55 16/11/2026).** Bản 3 thêm Q12 và ghi "chờ User" ở ba câu A đang hỏi lại.

**Tổng tiền cả đợt** (để chọn Q1, Q2, Q3, Q10 cho có cơ sở; trước credit tài khoản mới). Một tháng = 24 USD máy + ~1 USD sao lưu + ≤ 5 USD OpenAI = ~30 USD.
Ba tháng (12/2026–02/2027) = máy 72 + sao lưu ~3 + OpenAI ≤ 15 + tên miền 10–15 (nếu Q2 = riêng) ⇒ **~90–105 USD**. Tạo máy từ 01/12 thay vì 15/12 ⇒ +~12 USD.
Tài khoản AWS mới được 100 USD credit (thêm tối đa 100 USD qua hoạt động) ⇒ phần máy có thể gần như 0 USD nếu credit trừ được vào Lightsail (nguồn nói được, chưa thử) [Nguồn] tra 16/11.
**Hệ quả của credit với cảnh báo ngân sách:** tiền thật = 0 trong lúc credit còn ⇒ cảnh báo tính theo "tiền sau khi trừ credit" sẽ im lặng dù máy đang chạy ⇒ B2 phải loại credit khỏi phép tính (Q12).
Số OpenAI là trần (Q3), không phải ước: demo thật thường ~0,0005 USD / câu [Đo] 16/11 ⇒ vài chục lượt chấm < 1 USD.

| # | Câu | Mặc định đề xuất | Hệ quả nếu chọn khác · khi nào mặc định sai |
|---|---|---|---|
| Q1 | Có tạo tài khoản AWS (hoặc dùng tài khoản có sẵn) và chấp nhận ~24 USD / tháng cho máy (thêm ~1 USD sao lưu) trong 2–3 tháng không | Có, gói 4 GB | Gói 2 GB rẻ hơn 12 USD nhưng dễ hết RAM; không có AWS ⇒ demo chạy trên máy User. Tài khoản mới: Free plan hết sau 6 tháng hoặc hết credit — chưa nâng lên Paid thì tài khoản bị đóng, dữ liệu giữ 90 ngày ⇒ **nâng lên Paid plan trước buổi chấm**; chưa có nguồn xác nhận gói 4 GB tạo được trên Free plan [Nguồn] docs.aws.amazon.com free-tier-plans, tra 16/11. **Bản 3:** hướng dẫn hiện hành của khoá AI Production (tuần 1 ngày 5, phần tạo tài khoản) bảo **không chọn gói miễn phí lúc đăng ký** ⇒ hai cách: (a) chọn Paid ngay lúc đăng ký (credit 100 USD vẫn có hay không: **chưa tra lại**); (b) giữ mặc định này. C1 là phép kiểm thật: tài khoản không thấy gói 4 GB ⇒ dừng, nâng Paid |
| Q2 | Tên miền: mua tên miền riêng (~10–15 USD / năm, User tự mua) hay dùng `<IP>.sslip.io` miễn phí | `sslip.io` để thử; **tên miền riêng cho buổi chấm** | sslip.io miễn phí nhưng mọi người dùng chung một hạn mức chứng chỉ Let's Encrypt (50 chứng chỉ / tên miền / 7 ngày; sslip.io không nằm trong Public Suffix List — một báo lỗi 09/02/2026 cho thấy từng hết hạn mức) ⇒ ngày chấm có thể không xin được chứng chỉ [Nguồn] letsencrypt.org/docs/rate-limits + issue sslip.io #108, tra 16/11. Tên miền riêng thêm một bước trỏ DNS (bản ghi A ⇒ `<IP>`) |
| Q3 **(chờ User — A hỏi lại 18/11; mặc định đang giữ)** | Khoá OpenAI riêng cho bản công khai, có đặt giới hạn chi tiêu (User tạo ở trang OpenAI) | Có: project riêng ở OpenAI ⇒ Limits ⇒ Monthly spend limit ~5 USD + **bật "Enforce a hard limit"** (không bật thì chỉ cảnh báo, request vẫn chạy; áp không tức thời, có thể vượt nhẹ) [Nguồn] help.openai.com "Managing projects", tra 16/11 | Dùng chung khoá máy User ⇒ người ngoài dùng hết hạn mức của mọi việc khác; và khi cần dừng khẩn (10.4) phải thu hồi khoá đang dùng cho mọi việc. Thêm ở bản 3: tắt tự nạp tiền (Auto recharge) ở trang Billing của OpenAI nếu đang bật — hard limit của project không chặn việc thẻ bị nạp thêm [Suy, chưa mở trang] |
| Q4 | Tra web (Serper) trên bản công khai: bật hay tắt | **Tắt** (`HUE_TRA_WEB=false`, như Docker nháp) | Bật ⇒ câu kho không có sẽ gửi câu hỏi (và câu model viết lại ở lượt hỏi tiếp — cờ `web_cau_noi_tiep`) ra Serper, tốn 0,001 USD / lượt, cần khoá Serper trả trước không tự nạp; tắt ⇒ câu ngoài kho chỉ nhận câu từ chối |
| Q5 | Số lượt gọi model / IP / ngày | 50 (`HUE_LUOT_MOI_NGAY=50`) | Cao hơn ⇒ một người có thể tốn nhiều tiền; thấp hơn ⇒ hội đồng thử nhiều có thể bị chặn. Sai khi cả hội đồng dùng chung một mạng (chung IP) ⇒ nâng lên ~200 trong ngày chấm |
| Q6 | Hỏi bằng ảnh trên bản công khai: bật (ảnh người dùng gửi sang OpenAI) hay tắt | Bật, kèm dòng báo cạnh nút ảnh (checklist cũ: bản công khai cần dòng báo) | Tắt ⇒ bớt một đường dữ liệu ra ngoài |
| Q7 | Ảnh lễ hội thật #5 (không giấy phép mở) | Không lên bản công khai (đã loại trong `.dockerignore`) | Muốn có ⇒ cần quyền dùng ảnh |
| Q8 **(chờ User — A hỏi lại 18/11; mặc định đang giữ)** | Sau demo: xoá máy (hết tiền) hay giữ | Xoá máy sau khi có bản chụp thủ công `available` (§10.5) | Giữ ⇒ 24 USD / tháng tiếp. Lưu ý: **tắt máy (stop) Lightsail vẫn tính tiền** như đang chạy ⇒ muốn hết tiền phải xoá [Nguồn] đoạn trích trang hỏi đáp Lightsail, B tra 17/11, chưa mở cả trang. Bản chụp `hue-cuoi` giữ lại có chứa file khoá `.env.deploy` ⇒ 10.5 bắt buộc thu hồi khoá OpenAI |
| Q9 | Agent (Codex / Gemini) có được chạy lệnh `aws …` bằng access key của User không | **Chỉ lệnh chỉ đọc** (`get-*`, `sts get-caller-identity`); mọi lệnh có nhãn [Tiền] hoặc xoá (C3, C4, 10.5) **User tự gõ** sau khi agent đưa lệnh | Cho agent chạy hết ⇒ nhanh hơn, nhưng một lệnh sai có thể tạo / xoá tài nguyên tính tiền hoặc mất dữ liệu; User tự gõ hết ⇒ chậm, User phải ngồi cùng. Sai khi User vắng cả tuần deploy ⇒ khi đó cho agent chạy C3 một lần, ghi lại |
| Q10 | Ngày tạo máy (= ngày bắt đầu tính tiền máy) | **Khoảng 1 tuần trước buổi chấm** (đủ thời gian sửa lỗi); thử tạo-xoá một lần sớm hơn chỉ tốn vài giờ máy (~0,03 USD / giờ) | Tạo từ 30/11 ⇒ +~24 USD mỗi tháng sớm hơn. User đã dặn không deploy sớm (12/11) — tài liệu xong trước 30/11, máy tạo theo ngày User chọn |
| Q12 **(mới ở bản 3 — chờ User)** | Cảnh báo ngân sách AWS: mấy ngưỡng, số tiền bao nhiêu | Ngân sách 30 USD / tháng, **loại credit và tiền hoàn** khỏi phép tính, **ba ngưỡng**: tiền thật 50 % (15 USD — về sớm, để biết cảnh báo còn sống) · tiền thật 100 % · dự báo 100 % | Bản 2 chỉ có một ngưỡng 80 % = 24 USD = đúng tiền máy một tháng ⇒ email chỉ về cuối tháng; và không loại credit ⇒ có thể không bao giờ kêu. Ít ngưỡng hơn ⇒ biết muộn; nhiều hơn ⇒ thêm email. Sai khi User muốn trần thấp hơn (đổi số 30) |
| Q11 | Giữ bản sao các file deploy (Dockerfile, compose, Caddyfile, `dung_dockerignore.py`) ở đâu — hiện chỉ trong `data/phase_12/deploy_nhap/` (không Git) | Đưa 4 file đó (không bí mật) vào repo `deploy/` qua một nhánh; **không** đưa `Dockerfile.dockerignore` (liệt kê tên 263 bài kho — sinh lại bằng script) | Giữ trong `data/` ⇒ máy User hỏng là mất; md5 ở §0 giúp phát hiện file bị sửa, không giúp khôi phục |

## 4. Biến dùng trong tài liệu

| Biến | Nghĩa | Ví dụ / cách lấy |
|---|---|---|
| `<REPO>` | thư mục repo trên máy User | `/home/minhhieu/hue_rag` |
| `TAG` | biến shell: nhãn ảnh Docker = 7 ký tự đầu sha của `main` lúc build. **Trên máy User** đặt bằng `TAG=$(git -C <REPO> rev-parse --short=7 HEAD)`; **trên máy AWS** đặt tay `TAG=<7 ký tự đó>` ở dòng đầu D3 | `a9d1674` |
| `<IP>` | IP tĩnh của máy Lightsail | in ra ở bước C3 |
| `<SITE>` | tên miền dùng cho HTTPS | `<IP với dấu chấm thay bằng gạch>.sslip.io` (vd `13-250-1-2.sslip.io`) hoặc tên miền riêng |
| `HUE_GIT_SHA` | biến môi trường của app: mã bản code ghi vào mỗi dòng log `chat_metrics` (ảnh Docker không có git; không đặt ⇒ log ghi `khong_ro`). Đặt **bằng đúng `$TAG`** trong `hue.env` ở D3 — script đếm log `scripts/dem_chat_metrics.py --sha` so đúng chuỗi, mã dài 40 ký tự sẽ không khớp mã ngắn | `HUE_GIT_SHA=a9d1674` |
| `<KEY>` | đường dẫn khoá SSH riêng trên máy User | `~/.ssh/hue-lightsail.pem` (bước C2) |
| `COL` | biến shell: tên collection Qdrant | `COL=hue_full_corpus_7a2_e5_small_384` |

Mọi lệnh trên máy AWS chạy với user `ubuntu`, thư mục làm việc `/srv/hue`. Mỗi cửa sổ shell mới phải đặt lại `TAG` và `COL`.

**File deploy và md5** ([Chạy] 08:46 18/11/2026, `md5sum` 12 ký tự đầu — lệch ⇒ file đã bị sửa sau bản spec này, đọc diff với bản sao lưu `data/phase_12/deploy_nhap/sao_luu_*` trước khi chạy):
`Dockerfile` `68a871655df2` · `compose.yml` `d85c24900f4b` · `Caddyfile` `da85ebea1915` · `dung_dockerignore.py` `27bbd5183a77` · `Dockerfile.dockerignore` `d49694790ca3` (sinh lại ở A2; đổi khi kho đổi).
(Bản 2 ghi md5 ngày 16/11; từ đó các file đổi theo bảng dữ liệu mới + 18/11 `compose.yml` thêm dòng `HUE_GIT_SHA` và sửa ghi chú đầu file cho khớp D3–D4.)
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

**B1.** [User] [chưa chạy] Tạo / đăng nhập tài khoản AWS, bật MFA (xác thực hai lớp) cho tài khoản gốc. Không dùng tài khoản gốc để chạy lệnh. Gói tài khoản: theo Q1.
- Điểm kiểm (User tự nhìn, không dán gì vào hội thoại): (1) lúc gắn ứng dụng xác thực, AWS đòi **hai mã liên tiếp** — nhập đủ hai mã mới xong; (2) trang Security credentials của tài khoản gốc
  hiện một thiết bị MFA và **không có access key nào** của tài khoản gốc; (3) **đăng xuất** tài khoản gốc, các bước sau đăng nhập bằng người dùng IAM (B3).
- Dừng khi: trang Security credentials của tài khoản gốc có access key ⇒ User xoá trước khi đi tiếp.

**B2.** [User] [chưa chạy] Tạo **cảnh báo ngân sách** (AWS Budgets — cảnh báo miễn phí [Nguồn] trang giá Budgets, tra 16/11). Đây là cảnh báo qua email, **không phải trần cứng** —
AWS không tự dừng máy; số liệu chi phí của AWS cập nhật chậm (cỡ nửa ngày [Suy, chưa mở lại trang]) ⇒ email về trễ so với lúc tiền thật phát sinh.
- Làm **trên trang web** (đăng nhập bằng tài khoản có quyền Billing): Billing and Cost Management ⇒ Budgets ⇒ Create budget ⇒ **Customize (advanced)** ⇒ Cost budget ⇒ Monthly,
  số tiền theo Q12 (mặc định 30 USD) ⇒ ở phần chọn loại chi phí tính vào ngân sách: **bỏ chọn Credits và Refunds** (tên mục có thể khác chút tuỳ giao diện — tìm chỗ liệt kê
  "Credits", "Refunds", "Discounts"…) ⇒ thêm **ba cảnh báo** gửi email User: chi phí **thật (Actual) > 50 %** · **thật > 100 %** · **dự báo (Forecasted) > 100 %**.
- Vì sao không ghi lệnh CLI: bản 2 có lệnh `aws budgets create-budget …` nhưng (a) lệnh đó chưa từng chạy, (b) nó không loại credit, (c) trường cấu hình cũ để loại credit (`CostTypes`)
  đã bị AWS ghi là lỗi thời [Nguồn] trang tham chiếu API Budgets, B mở 17/11 ⇒ không chép một lệnh chưa chạy cho việc liên quan tới tiền.
- Kiểm: trang Budgets hiện ngân sách `hue-demo` với 3 cảnh báo; mở ngân sách ra thấy Credits và Refunds **không** được tính; email xác nhận đăng ký cảnh báo về hộp thư User.
  Phép kiểm "cảnh báo còn sống": sau khi máy chạy vài ngày (hoặc đặt tạm ngưỡng đầu thật thấp), email ngưỡng 50 % phải về — không về ⇒ cảnh báo đang không hoạt động, báo User.
- Dừng khi: không tìm thấy chỗ bỏ Credits / Refunds ⇒ chụp màn hình cho User, **không** tạo ngân sách thiếu bước này rồi coi như xong.

**B3.** [User] [chưa chạy] Tạo một người dùng IAM riêng cho việc deploy, **chỉ quyền Lightsail**, tạo access key, cài AWS CLI v2 trên máy User,
chạy `aws configure` (vùng `ap-southeast-1`, khuôn ra `json`). Không dán access key vào hội thoại. Agent chạy lệnh `aws` theo đúng Q9.
- Cấp quyền (đổi ở bản 3): bản 2 ghi gắn chính sách có sẵn tên `AmazonLightsailFullAccess` — tên này **rất có thể không tồn tại** (E mở trang danh sách chính sách AWS quản lý sẵn
  17/11: không thấy mục nào chứa "Lightsail" trong phần đã đọc, còn ~20 % cuối trang chưa đọc). Làm theo trang AWS "Grant Lightsail access for an IAM user"
  (docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-managing-access-for-an-iam-user.html, E đọc trọn 17/11): IAM ⇒ Policies ⇒ Create policy ⇒ JSON, dán:
  ```json
  {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["lightsail:*"], "Resource": "*"}]}
  ```
  đặt tên `hue-lightsail`, gắn cho người dùng IAM deploy (trực tiếp hoặc qua một nhóm). Nếu trang IAM **có** sẵn chính sách tên chứa "Lightsail" thì dùng cái nào cũng được — ghi lại đã dùng cái nào.
- Nơi để khoá: access key chỉ nằm trong `~/.aws/credentials` trên máy User (do `aws configure` ghi); file `.csv` tải về lúc tạo khoá ⇒ xoá hoặc để ngoài mọi thư mục repo / thư mục đồng bộ.
  Kiểm không lọt vào repo: `cd <REPO> && git status --short | grep -ci -e credential -e accessKey` ⇒ mong đợi `0`.
- Kiểm: `aws sts get-caller-identity --query Arn --output text`
- Mong đợi: `arn:aws:iam::<số tài khoản>:user/<tên người dùng IAM vừa tạo>`.
- Kiểm quyền hẹp (hai chiều): `aws lightsail get-regions --query "regions[0].name" --output text` ⇒ in một tên vùng (được phép); `aws s3 ls` ⇒ **phải báo lỗi AccessDenied** (không được phép ngoài Lightsail).
- Dừng khi: ARN kết thúc bằng `:root` (đang dùng tài khoản gốc) hoặc tên khác — sửa `aws configure` trước khi đi tiếp; hoặc `aws s3 ls` **không** báo lỗi quyền (người dùng đang rộng quyền hơn dự định).

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
  HUE_GIT_SHA=$TAG
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
- Kiểm: `docker images hue-rag-app --format '{{.Tag}}'` có `$TAG`; `cat hue.env` (file không có khoá — in được) có dòng `HUE_GIT_SHA=<TAG>`.
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
| **Một câu hỏi thật đi hết đường** (phép kiểm chính — bản 3) | `curl -sN -m 90 -X POST https://<SITE>/api/chat/stream -H 'Content-Type: application/json' -d '{"query":"Chùa Thiên Mụ ở đâu?"}' > /tmp/hue_kiem.txt; grep -c '^event: delta' /tmp/hue_kiem.txt; grep -c '^event: done' /tmp/hue_kiem.txt` [chưa chạy] | dòng 1 > 0 (có chữ trả lời từ model), dòng 2 = `1`. **`/health` không thay được phép kiểm này**: nó chỉ đọc trạng thái lúc khởi động, không gọi OpenAI [Đọc] `backend/api/health.py` — khoá sai / hết hạn mức thì `/health` vẫn `ok`. Dùng lại lệnh này mỗi sáng ngày demo và sau mọi lần 10.2 / 10.3 (tốn ~0,0005 USD / lần; tính 1 lượt của IP máy User). Khi có script kiểm nhanh một lệnh (việc nhóm đã chốt, làm sau lượt đo cuối) thì dùng script thay dòng này |
| Log ghi đúng bản đang chạy | `ssh … 'grep "chat_metrics" /srv/hue/logs/application.log \| tail -1 \| grep -o "\"git_sha\": \"[^\"]*\""'` [chưa chạy] | `"git_sha": "<TAG>"` — ra `khong_ro` ⇒ `hue.env` thiếu dòng `HUE_GIT_SHA` (D3) |
| Tiền đi đúng project OpenAI | [User] mở trang Usage của **project riêng** (Q3) sau câu hỏi thật ở trên | số request của hôm nay tăng ở project đó, không tăng ở project máy User — sai ⇒ `.env.deploy` đang chứa khoá của project khác, dừng |
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
  (kho đã nạp lại ở 10.2 ⇒ `qdrant.snapshot` trên máy AWS đã bị bản mới đè ⇒ từ máy User `scp -i <KEY> ~/hue_deploy_<TAG cũ>/qdrant.snapshot ubuntu@<IP>:/srv/hue/` rồi nạp như D3, trước lệnh `up`).
- Kiểm: `docker compose -p hue -f compose.yml --env-file hue.env ps app --format '{{.Image}}'` + 4 dòng đầu §9.
- Mong đợi: ảnh = nhãn trong `hue_image_cu.txt`; 4 dòng đạt.
- Dừng khi: app không lên ⇒ báo User (còn đường cuối: khôi phục máy từ snapshot tự động của đêm trước — bảng điều khiển Lightsail ⇒ Snapshots ⇒ Create new instance).
- Dọn đĩa: giữ tối đa 2 ảnh cũ (`docker image rm hue-rag-app:<nhãn quá cũ>`; đĩa 80 GB).

**10.4 Khi có sự cố.** App 503 / không trả lời: `docker compose -p hue -f compose.yml --env-file hue.env logs app | tail -50` (không chép vào chỗ công khai). Hết hạn mức OpenAI
(hard limit Q3): người dùng thấy lỗi, `/health` vẫn `ok` ⇒ phát hiện bằng dòng "Một câu hỏi thật" của §9 ⇒ User nâng hạn mức ở trang OpenAI. Máy hết RAM: `docker stats --no-stream`,
`sudo dmesg | grep -i oom`. Các trường hợp này: báo User, không tự đổi cấu hình.

**Dừng khẩn** (nghi bị lạm dụng: tiền OpenAI tăng lạ, số dòng log tăng vọt, link lọt ra ngoài) — người chạy **được làm ngay bước 1 không cần hỏi**, rồi báo User:
1. Tắt app, giữ nguyên dữ liệu và log [chưa chạy trên máy AWS]: `ssh -i <KEY> ubuntu@<IP> 'cd /srv/hue && docker compose -p hue -f compose.yml --env-file hue.env stop app'`
   - Kiểm: `curl -s -o /dev/null -w '%{http_code}\n' -m 10 https://<SITE>/api/tinh_nang` ⇒ mong đợi `502` (Caddy còn, app tắt) — không còn `200`.
   - Lệnh này chỉ chặn **tiền OpenAI và việc lạm dụng**; **máy vẫn tính tiền AWS** (tắt cả máy Lightsail cũng vẫn tính — Q8).
2. [User] Thu hồi khoá OpenAI của project công khai ở trang OpenAI (API keys ⇒ revoke) nếu nghi khoá lộ; tạo khoá mới, sửa `.env.deploy` trên máy AWS bằng `nano` (không dán vào hội thoại).
3. Xem lưu lượng lạ mà không in nội dung: `ssh … 'grep -c "chat_metrics" /srv/hue/logs/application.log; grep -c "Rate limited" /srv/hue/logs/application.log'` (chỉ số đếm); log Caddy có địa chỉ IP —
   chỉ User xem (`docker compose … logs caddy | tail -50`), không chép ra ngoài.
4. Chạy lại: `docker compose -p hue -f compose.yml --env-file hue.env up -d app` rồi làm dòng "Một câu hỏi thật" của §9.

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
- Kiểm (sau khi xoá) — **mong đợi danh sách RỖNG, không phải "không còn tên `hue-app`"** (máy dựng lại từ bản chụp ở 10.3 mang tên khác):
  ```bash
  aws lightsail get-instances --region ap-southeast-1 --query "instances[].name" --output text          # mong đợi: không in gì
  aws lightsail get-static-ips --region ap-southeast-1 --query "staticIps[].name" --output text         # mong đợi: không in gì
  aws lightsail get-instance-snapshots --region ap-southeast-1 --query "instanceSnapshots[].[name,state]" --output text   # mong đợi: đúng một dòng `hue-cuoi available`
  ```
- Dừng khi: vòng chờ in trạng thái khác `available` (sau ~20 phút) ⇒ **không xoá máy**, báo User. Danh sách máy / IP còn dòng nào ⇒ chưa sạch, báo User (không đoán tên để xoá).
- IP tĩnh gắn máy thì miễn phí; không gắn quá một giờ ⇒ 0,005 USD / giờ [Nguồn] tài liệu static IP Lightsail, tra 16/11 ⇒ `release-static-ip` ngay sau khi xoá máy.

**Dọn nốt — theo đúng thứ tự** [User] [chưa chạy] (bản 3; khoá AWS xoá SAU CÙNG vì các lệnh trên cần nó):
1. **Thu hồi khoá OpenAI của project công khai** (trang OpenAI ⇒ API keys ⇒ revoke) — **bắt buộc**: file `.env.deploy` nằm trong bản chụp `hue-cuoi`, ai dựng lại máy từ bản chụp là có khoá.
   Kiểm: trang API keys của project không còn khoá đang hoạt động.
2. Nếu Q2 = tên miền riêng: xoá bản ghi A trỏ `<IP>` ở nơi mua tên miền (IP đã trả có thể được cấp cho người khác). Kiểm: `getent hosts <tên miền>` không còn in `<IP>`.
3. Xoá cặp khoá SSH trên AWS và trên máy: `aws lightsail delete-key-pair --region ap-southeast-1 --key-pair-name hue-key` rồi `rm ~/.ssh/hue-lightsail.pem`.
   Kiểm: `aws lightsail get-key-pairs --region ap-southeast-1 --query "keyPairs[].name" --output text` không in gì.
4. Bản chụp `hue-cuoi` (~0,05 USD / GB-tháng): khi chắc không dựng lại nữa ⇒ `aws lightsail delete-instance-snapshot --region ap-southeast-1 --instance-snapshot-name hue-cuoi`;
   kiểm bằng lệnh `get-instance-snapshots` ở trên ⇒ không in gì.
5. **Kiểm bằng tài khoản gốc / tài khoản có quyền Billing** (người dùng IAM deploy chỉ thấy Lightsail ở một vùng): trang Billing ⇒ Bills ⇒ xem **chi phí theo dịch vụ** của tháng —
   chỉ có Lightsail (và thuế); xem vào **ngày hôm sau** và **2–3 ngày sau** khi xoá: không còn dòng nào tăng. Có dịch vụ lạ / vùng lạ ⇒ báo User ngay.
6. Sau cùng: xoá access key rồi người dùng IAM deploy (IAM ⇒ Users); giữ ngân sách `hue-demo` thêm một tháng để còn email nếu sót tài nguyên.
   Kiểm: `aws sts get-caller-identity` trên máy User **báo lỗi** (khoá đã bị xoá).

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

| Kiểm sức khoẻ không gọi ra ngoài | `/health` chỉ đọc trạng thái lúc khởi động [Đọc] `backend/api/health.py` ⇒ khoá OpenAI hỏng / hết hạn mức không hiện ở `/health` | minor | Phép kiểm sau deploy và hằng ngày = một câu hỏi thật (§9) |
| Biết bản nào đang chạy | ảnh không có git ⇒ log ghi `khong_ro` nếu không đặt biến; nhánh `p9-git-sha-env` cho đọc `HUE_GIT_SHA` [Đo] 18/11: test hàm đọc biến đạt; `docker compose config` đưa biến vào app | minor | D3 ghi `HUE_GIT_SHA=$TAG`; §9 có dòng kiểm |

**Mỗi câu "đã chặn / đã an toàn" ở bảng trên kiểm lại bằng:** giới hạn lượt ⇒ §9 dòng "Hết lượt" · khoá / dữ liệu cấm không vào ảnh ⇒ A4 · log không nội dung ⇒ §9 dòng "Log không ghi câu hỏi / IP" ·
sổ vết tắt ⇒ §9 dòng "Sổ vết tắt" · trang API tắt ⇒ §9 dòng "Trang API tắt" · quyền IAM hẹp ⇒ B3 "Kiểm quyền hẹp" · hạn mức OpenAI đúng project ⇒ §9 dòng "Tiền đi đúng project OpenAI" ·
ngân sách loại credit ⇒ B2 "Kiểm". Dòng nào chưa có nhãn [Đo] trên máy AWS thì **chưa được coi là đã chặn ở bản công khai** cho tới khi §9 chạy xong.

**Giả định an toàn:** chạy trên một máy Lightsail do User sở hữu; ai có link đều gọi được; giới hạn chi tiêu = giới hạn lượt / IP / ngày + hard limit
OpenAI; chưa rào: một người dùng nhiều IP vẫn dùng được nhiều lượt (chặn bằng hạn mức OpenAI), lượt bị Dừng vẫn tính tiền phần đã chạy.

## 12. Tra cứu (16/11/2026)

- Codex: yêu cầu chỉ thông tin công khai ⇒ `data/tra_cuu_cli/2026-11-16_deploy-aws-2/ket_qua.md` (155 s, 34 trang mở được, 0 lệnh shell). Kết quả là dữ liệu ngoài.
- E tự mở kiểm 2 ý chính: trang giá Lightsail (2 GB 12 · 4 GB 24 · 8 GB 44 USD; snapshot 0,05 USD / GB-tháng) và tài liệu snapshot Qdrant
  (đường API, `file://` dùng được, `priority: snapshot`, tương thích minor). Còn lại ghi [Nguồn] theo Codex, chưa tự mở.
- Còn chưa chắc: tên `medium_3_0` / `ubuntu_24_04` (C1 lấy từ đầu ra thật); gói 4 GB có tạo được trên Free plan không; credit có trừ vào Lightsail không; lệnh cài Docker chưa chạy trên máy thật.
- Tra cũ 07/11 (EC2, Secrets Manager 0,40 USD / khoá / tháng, Parameter Store bản thường miễn phí): `data/tra_cuu_cli/2026-11-07_e-dep-aws/`. Spec chọn `.env.deploy` quyền 600 trên máy
  (đơn giản nhất, đủ cho một máy demo); Secrets Manager / Parameter Store chỉ đáng khi nhiều máy hoặc cần xoay khoá.

**Bổ sung 17–18/11/2026 (bản 3):**
- B mở trang tham chiếu AWS Budgets 17/11: ngân sách mặc định **có tính** credit; trường `CostTypes` ghi lỗi thời ⇒ B2 làm trên trang web. E mở 2 trang AWS 17/11 về quyền Lightsail ⇒ B3.
- **Còn chưa chắc (thêm):** tắt máy Lightsail vẫn tính tiền (mới đọc đoạn trích) · Lightsail 4 GB là 2 nhân (trang giá 16/11 ghi 2 vCPU; chưa thấy đầu ra C1) · chọn Paid ngay lúc đăng ký có
  còn credit 100 USD không · tên mục "Credits / Refunds" trên giao diện Budgets hiện hành.
- **Chưa đo: nhiều người hỏi cùng lúc.** Lần đo đồng thời duy nhất là 27/10 (trước khi có định tuyến, công cụ, hiện chữ dần); bản công khai là một tiến trình trên máy 2 nhân ⇒
  hội đồng 5–10 người hỏi cùng lúc chậm tới đâu là **chưa biết**. Đo được ngay trên máy AWS sau §9 (5 rồi 10 câu đồng thời, ước ~0,006 USD) — chưa có lệnh, chưa ai duyệt; ghi ở đây như giới hạn đã biết.

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
- Bản 3 (B, 08:46 18/11/2026; bản 2 đã duyệt mã `e847b47ad995`): sửa một lượt theo đối chiếu bốn khoá học + bàn nhóm 17/11. Không đổi phương án (một máy Lightsail 4 GB + Compose), không đổi giai đoạn A.
  (1) §0 bảng [Chạy] / [chưa chạy] cho từng phần; dòng trạng thái sai "chưa duyệt" sửa. (2) B2 ngân sách: làm trên trang web, loại credit + tiền hoàn, ba ngưỡng; bỏ lệnh CLI chưa chạy; Q12 mới.
  (3) B3: tự tạo chính sách `lightsail:*` thay tên chính sách có thể không tồn tại; kiểm quyền hai chiều; nơi để khoá. (4) B1: điểm kiểm MFA hai mã, không access key gốc, đăng xuất gốc.
  (5) `HUE_GIT_SHA=$TAG` ở D3 + §4 + dòng kiểm §9. (6) §9: phép kiểm chính là một câu hỏi thật (không phải `/health`) + bằng chứng trang Usage đúng project. (7) 10.4: lệnh dừng khẩn + đổi khoá + xem lưu lượng.
  (8) 10.5: mong đợi danh sách rỗng; thứ tự dọn (thu hồi khoá OpenAI bắt buộc, DNS, cặp khoá SSH, bản chụp, kiểm hoá đơn bằng tài khoản gốc hôm sau + 2–3 ngày, access key sau cùng).
  (9) Q1 ghi lời khuyên "không chọn gói miễn phí" của khoá; Q3 / Q8 ghi chờ User + tự nạp tiền OpenAI + tắt máy vẫn tính tiền. (10) §4 md5 file deploy tính lại; ghi chú đầu `compose.yml` sửa khớp D3–D4.
  (11) §11 thêm hai dòng + bảng "câu đã chặn ⇒ lệnh kiểm". (12) §12 giới hạn chưa đo nhiều người cùng lúc. **Chưa làm ở bản 3:** chưa chạy lệnh AWS nào; runbook bàn giao mục 8 (trỏ vào spec này) viết riêng.
