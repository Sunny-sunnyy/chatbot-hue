# Gói Docker của trợ lý Huế

Viết: 09:15 23/11/2026 (giờ `date`), phiên C, việc X14 phần (4). Người đọc: người (hoặc agent) sẽ dựng và chạy hệ thống trên một máy khác máy
chủ dự án. Đọc cùng bản thiết kế deploy (`docs/superpowers/specs/`) và thư mục `deploy/terraform/` — trang này chỉ nói về phần "hộp".

**Sửa 12:06 23/11/2026: đường deploy đã chốt (chủ dự án, 11:01 23/11/2026) = model viết của OpenAI (`gpt-6-luna`), một máy chỉ bật quanh ngày demo.** Vì vậy
`compose.yml` tự đủ, không cần file phủ nào; quyền gọi model là MỘT dòng `OPENAI_API_KEY=…` trong file `hue.khoa.env` trên máy đích. Đường Claude trên
Amazon Bedrock (hai file phủ, hộp `khoa`) được GIỮ làm đường tuỳ chọn — **bản deploy không dùng** — vì ở máy chủ dự án hệ thống vẫn chạy model đó và
mọi lượt thử có câu trả lời thật tới nay đều đi đường đó.

Từ dùng: **ảnh** = Docker image · **hộp** = container · **ngữ cảnh** = thư mục file gửi cho `docker build` · **file phủ** = file compose thứ hai
chồng lên `compose.yml` · **khoá tạm** = bộ ba khoá AWS có hạn dùng (vài giờ) · **vai gắn máy** = quyền AWS gắn thẳng vào máy ảo, không cần cất
khoá trên đĩa · **bản chụp** = file Qdrant xuất ra chứa trọn một collection.

## 1. Gói gồm gì

Ba hộp trên MỘT máy: `qdrant` (chỉ mục) · `app` (FastAPI + giao diện + kho + bảng dữ liệu) · `caddy` (cửa vào, HTTPS, trần cỡ yêu cầu 12 MB).

| File | Việc |
|---|---|
| `dung_anh.sh [commit]` | MỘT lệnh dựng ảnh `hue-rag-app:<sha>` từ đúng một commit, rồi tự kiểm ảnh |
| `dung_ngu_canh.py` | dựng ngữ cảnh: code + bài kho từ commit (so băm với chỉ mục), file bảng riêng tư theo `settings.yaml` |
| `Dockerfile` | hai tầng: dựng giao diện bằng Node, rồi ảnh Python 3.13 (torch bản CPU, model nhúng tải sẵn) |
| `compose.yml` | ba hộp + các chốt cho bản mở ra ngoài; TỰ ĐỦ cho đường deploy (model viết của OpenAI, khoá ở `hue.khoa.env`) |
| `Caddyfile` | cửa vào; không nén luồng trả lời để chữ ra ngay |
| `thu_o_may.sh len [openai\|bedrock] / kiem / don` | chạy thử trọn gói ở máy chủ dự án, cổng 8880, không đụng server 8010; mặc định `openai` = đúng bộ file của máy đích |
| `chup_chi_muc.sh <file ra>` | lấy chỉ mục ra một file bản chụp từ Qdrant đang chạy (tạo ⇒ tải ⇒ xoá ngay ở nguồn; chỉ đọc) |
| `nap_chi_muc.sh [file phủ]` | nạp bản chụp vào Qdrant của gói, so số điểm với bản ghi dựng trong ảnh — dùng ở máy thử LẪN máy đích |
| `dong_goi.sh <sha> [openai\|bedrock]` | gom mọi thứ máy đích cần vào `~/hue_goi_<sha>/` kèm `SHA256SUMS`; ghi sẵn dòng `provider` (mặc định `openai`) vào `cau_hinh/settings.yaml` |
| `compose.thu.yml` | ĐƯỜNG TUỲ CHỌN (Bedrock) — file phủ để thử ở máy chủ dự án: gắn file khoá tạm đang có, chỉ đọc |
| `compose.vai-may.yml` + `lam_moi_khoa.py` | ĐƯỜNG TUỲ CHỌN (Bedrock), **bản deploy không dùng** — file phủ cho máy AWS có vai gắn: hộp phụ `khoa` lấy khoá tạm của vai, tự làm mới mỗi phút |

## 2. Dùng

```bash
deploy/docker/dung_anh.sh origin/main     # phải ghi rõ commit / nhánh lấy code + kho
# Thử đúng bộ file của máy đích (model viết của OpenAI). HUE_KHOA_ENV = một file riêng có dòng OPENAI_API_KEY=… (KHÔNG phải .env của dự án);
# không đặt ⇒ ca "thiếu khoá": lệnh PHẢI báo đỏ (app không sẵn sàng).
HUE_IMAGE=hue-rag-app:<sha> HUE_KHOA_ENV=<file khoá> deploy/docker/thu_o_may.sh len
# Thử với model đang chạy ở máy chủ dự án (Claude trên Bedrock) — đường duy nhất có câu trả lời thật khi tài khoản OpenAI chưa có tiền:
HUE_IMAGE=hue-rag-app:<sha> deploy/docker/thu_o_may.sh len bedrock
deploy/docker/thu_o_may.sh kiem           # không gọi model; in sẵn lệnh hỏi MỘT câu thật
deploy/docker/thu_o_may.sh don
```

Đưa sang máy đích: `deploy/docker/dong_goi.sh <sha>` ra thư mục `~/hue_goi_<sha>/` gồm `app_<sha>.tar.gz` (ảnh, khoảng 0,9 GB) ·
`qdrant.snapshot` (chỉ mục) · `compose.yml` · `Caddyfile` · `nap_chi_muc.sh` · `cau_hinh/` (`settings.yaml` ĐÃ ghi `provider: openai` + `logging.yaml`
của chính ảnh đó) · `SHA256SUMS`. Thư mục này riêng tư.
Trên máy đích (Linux x86-64 — ảnh dựng cho `amd64`, không chạy trên máy ARM; Docker có Compose từ 2.24), trong thư mục đó:

```bash
sha256sum -c SHA256SUMS && gunzip -c app_<sha>.tar.gz | docker load
nano hue.env                               # biến không bí mật — danh sách ở đầu compose.yml; ít nhất HUE_IMAGE, HUE_SITE, HUE_GIT_SHA (không đặt ⇒ log ghi "khong_ro")
nano hue.khoa.env && chmod 600 hue.khoa.env   # BÍ MẬT: dòng OPENAI_API_KEY=… (bắt buộc); SERPER_API_KEY, HUE_KHOA_THEO_DOI nếu dùng
bash nap_chi_muc.sh                        # bật Qdrant, nạp chỉ mục, đếm chính xác số điểm (gọi bằng `bash`: chép qua S3 làm mất quyền chạy của file)
docker compose --env-file hue.env -f compose.yml up -d --wait
```

**Sau khi `up --wait` báo xong, BẮT BUỘC hỏi MỘT câu thật** (lệnh `curl` mẫu: `thu_o_may.sh kiem` in ra; hoặc mở trang và hỏi "Vé tham quan Đại Nội
bao nhiêu?"). Lý do: app chỉ kiểm CÓ dòng `OPENAI_API_KEY` lúc bật, không kiểm khoá DÙNG ĐƯỢC (kiểm thật thì tốn một lời gọi model mỗi lần hỏi sức
khoẻ) ⇒ khoá gõ sai, khoá bị thu hồi, tài khoản hết tiền đều cho ba hộp `healthy`, `/health` `ok` — và mọi câu hỏi ra "Không thể tạo câu trả lời vào
lúc này". Thiếu hẳn dòng khoá, hoặc `provider` còn ghi `bedrock` mà không có file phủ, thì khác: `/health` `degraded`, `up --wait` báo lỗi ngay.

Gói cho đường tuỳ chọn Bedrock: `dong_goi.sh <sha> bedrock` (kèm `compose.vai-may.yml`), trên máy đích `bash nap_chi_muc.sh compose.vai-may.yml` rồi
`docker compose --env-file hue.env -f compose.yml -f compose.vai-may.yml up -d --wait`.

Thứ tự đủ cho AWS (tạo máy, mở cổng, lúc nào tính tiền, lùi thế nào) thuộc bản thiết kế deploy. Đừng dán đầu ra của `docker compose config` vào
chỗ công khai: lệnh đó in cả nội dung file bí mật `hue.khoa.env`.

**Đổi model viết / tắt một tính năng NGAY TRÊN MÁY ĐÍCH, không dựng lại ảnh.** `compose.yml` gắn thư mục `cau_hinh/` đè lên thư mục cấu hình trong
ảnh ⇒ sửa một dòng của `cau_hinh/settings.yaml` rồi `docker compose --env-file hue.env -f compose.yml restart app` (khoảng 13 giây).
Dòng `provider` do `dong_goi.sh` ghi sẵn (`openai`); đổi sang `bedrock` trên máy đích thì phải chạy kèm một file phủ Bedrock (mục 4), không thì app
báo chưa sẵn sàng. Đổi nội dung `hue.khoa.env` thì dùng `… up -d app` (để hộp nhận biến mới), `restart` không nạp lại file đó. Chi tiết hai model:
`guides/DOI_MODEL_VIET.md`. Lấy lại bản gốc của file cấu hình (bản TRONG ẢNH ghi `provider: bedrock` — nhớ ghi lại dòng `provider`):
`docker run --rm --entrypoint cat <ảnh> /app/backend/config/settings.yaml > cau_hinh/settings.yaml`.

## 3. Thứ gì riêng tư, thứ gì nằm trong ảnh

| Thứ | Trong ảnh? | Ghi chú |
|---|---|---|
| Code `backend/`, `frontend/`, 267 bài kho, bảng điều kiện của kho | có | đều đã công khai trên GitHub |
| 11 file bảng lấy từ `data/` (9 bảng theo `settings.yaml` + bản ghi dựng chỉ mục + thống kê từ khoá) | **có — riêng tư** | kê tên + băm ở `/app/DANH_SACH.txt` trong ảnh. Vì chúng: **không đẩy ảnh lên kho ảnh công khai** (Docker Hub công khai, ECR Public); chuyển bằng `docker save` hoặc kho ảnh riêng |
| Chỉ mục Qdrant | không | đi bằng bản chụp (~56 MB), nạp vào hộp `qdrant` lúc dựng máy |
| `.env` của máy chủ dự án | **không bao giờ** | gói không đọc file này |
| Khoá OpenAI (BẮT BUỘC ở đường deploy), khoá tra web, khoá trang theo dõi | **không bao giờ** | file `hue.khoa.env` cạnh `compose.yml` trên máy đích, quyền 600; thiếu dòng khoá OpenAI ⇒ app không sẵn sàng |
| File khoá tạm Bedrock / khoá của vai (đường tuỳ chọn) | **không bao giờ** | gắn vào lúc chạy ở `/run/hue-khoa/bedrock.json` (file phủ) |
| Cấu hình app (`settings.yaml`, `logging.yaml`) | có, và một bản NGOÀI ảnh ở `cau_hinh/` | công khai (có trong git); bản ngoài ảnh là bản app thật sự đọc |
| Bộ câu kín, bộ câu mẫu, `_source-dumps`, ảnh `frontend/public/anh/rieng`, phần còn lại của `data/` | **không bao giờ** | không vào ngữ cảnh; `dung_anh.sh` còn đếm lại trong ảnh, khác 0 thì dừng |
| Log, số đo từng lượt | không | thư mục `logs/` cạnh `compose.yml` trên máy đích |

## 4. Quyền gọi model đi vào hộp thế nào

**Đường deploy — model của OpenAI.** Hộp app nhận biến `OPENAI_API_KEY` từ file `hue.khoa.env` (dòng `env_file` của `compose.yml`; file không nằm
trong ảnh, không nằm trong gói `dong_goi.sh` tạo ra — người deploy tự gõ trên máy đích). Máy không cần quyền AWS nào để gọi model. Chặn chi tiêu =
trần đặt ở trang quản lý của OpenAI + hai trần lượt của app (`HUE_LUOT_MOI_NGAY`, `HUE_LUOT_TONG_MOI_NGAY`). Ba kiểu hỏng và cái người deploy thấy:

| Hỏng gì | Lúc bật | Câu hỏi |
|---|---|---|
| Thiếu dòng `OPENAI_API_KEY` | `/health` `degraded` (`generator: not_ready`), `up --wait` báo lỗi | "Không thể tạo câu trả lời vào lúc này" |
| `provider` còn `bedrock`, không file phủ | như trên (từ 23/11; trước đó: xanh giả — đã tái hiện rồi chữa) | như trên |
| Có khoá nhưng khoá sai / bị thu hồi / tài khoản hết tiền | **xanh**: ba hộp `healthy`, `/health` `ok` | "Không thể tạo câu trả lời vào lúc này" ⇒ chỉ MỘT câu hỏi thật sau khi bật mới lộ (mục 2) |

**Đường tuỳ chọn — Claude trên Amazon Bedrock (bản deploy không dùng; phần dưới giữ cho lượt thử ở máy chủ dự án và cho ngày cần đổi lại).**
Lớp nối model (`backend/llm/bedrock_model.py`) KHÔNG dùng thư viện AWS: nó tự ký từ một file JSON ba khoá `accessKeyId`, `secretAccessKey`,
`sessionToken` (cả ba bắt buộc), đường dẫn ở biến `HUE_BEDROCK_CREDS_FILE`, đọc lại ở MỖI lời gọi. Gói giữ nguyên điều đó: app luôn đọc
`/run/hue-khoa/bedrock.json`; file tới từ đâu do file phủ quyết định, ảnh không đổi.

- `compose.thu.yml`: gắn file khoá tạm của máy chủ dự án (một file, chỉ đọc).
- `compose.vai-may.yml`: hộp `khoa` hỏi dịch vụ thông tin máy (IMDSv2) lấy khoá tạm của vai, đổi tên trường, ghi file kiểu "file tạm rồi đổi
  tên" vào một volume chung (app gắn cả thư mục, chỉ đọc ⇒ luôn thấy file mới). Không khoá dài hạn nào nằm trên máy. Khuôn hỏi – đáp đã đối
  chiếu tài liệu AWS (phiên B, 23/11): AWS đưa khoá mới ra ít nhất 5 phút trước khi khoá cũ hết hạn ⇒ hỏi MỖI PHÚT (5 phút một lần thì biên an toàn bằng 0).
  Hộp `khoa` dùng thẳng mạng của máy (`network_mode: host`) ⇒ bước nhảy IMDS để 1 vẫn chạy, và ba hộp còn lại (trong đó có hộp nhận yêu cầu từ
  internet) không tới được dịch vụ thông tin máy. Cần phía Terraform: vai có quyền gọi model, `http_tokens = "required"`.
  Hai điều biết trước: (a) máy khởi động lại thì Docker tự bật lại các hộp không theo thứ tự — đo ở máy này: hộp `khoa` ghi lại file sau 0,75 giây,
  app phải 13,8 giây mới nhận được câu đầu ⇒ thường không lượt nào gặp khoá cũ; chỉ khi dịch vụ thông tin máy trả lời chậm hơn app khởi động thì
  lượt hỏi đầu mới nhận lỗi "khoá Bedrock bị từ chối hoặc đã hết hạn" một lần; (b) hai sự cố cho người dùng CÙNG một lỗi đó nhưng nhìn khác nhau:
  vai bị GỠ khỏi máy ⇒ hộp `khoa` thành `unhealthy`, log của nó ghi "CHƯA lấy được khoá tạm của vai"; vai bị GẮN CHÍNH SÁCH CẤM gọi model (hành
  động tự cấm của ngân sách) ⇒ hộp `khoa` VẪN khoẻ, `/health` vẫn `ok`, chỉ các câu hỏi nhận 403 ⇒ "mọi thứ xanh mà câu nào cũng lỗi" thì xem
  ngân sách / chính sách của vai trước, đừng tìm ở hộp `khoa`.
  Volume chung chứa file khoá nằm trong RAM (`tmpfs`): khoá tạm không ghi xuống đĩa, máy dừng / bật thì thư mục trống.
- Máy KHÔNG gắn được vai: phải chọn giữa (i) khoá dài hạn chỉ có quyền đổi lấy khoá tạm + một hộp phụ khác, hoặc (ii) sửa lớp nối cho
  `sessionToken` thành tuỳ chọn. Chưa viết, và không còn cần cho bản deploy (đường deploy không gọi Bedrock).

## 5. Đã kiểm ↔ chưa kiểm

**Lượt chạy thử trọn gói ở máy chủ dự án — 10:15 23/11/2026, ảnh `hue-rag-app:e7193bd` (= main có giao diện mới), model viết qua Bedrock:**

| Bước | Kết quả | |
|---|---|---|
| `dung_anh.sh origin/main` | ngữ cảnh 603 file code · 267 bài kho khớp băm · 11 file riêng tư · 0 file cấm; dựng 2 phút 38 giây (lần đầu, có kéo ảnh nền); ảnh 3,62 GB; kiểm trong ảnh: 267 bài, 0 file cấm | chạy thật |
| Chỉ mục (`chup_chi_muc.sh` + `nap_chi_muc.sh`) | bản chụp 75 MB; Qdrant nguồn trước / sau 9.479 điểm, không còn bản chụp nào ở nguồn; Qdrant của gói 9.479 điểm = bản ghi dựng trong ảnh | chạy thật |
| `thu_o_may.sh len` | ba hộp lên trong 31 giây, cả ba `healthy` | chạy thật |
| `kiem` | trang chủ 200 · `/health` ok (app, qdrant, retrieval, tokenizer, generator) · `/docs` 404 · tra web tắt · Khám phá 267 bài | chạy thật |
| Trần cỡ yêu cầu ở Caddy | thân JSON 13 MB tới `/api/chat` ⇒ 413, thân rỗng (Caddy cắt) · 11 MB ⇒ 422 của app (đi qua). Đường trả lời TRƯỚC khi đọc thân (ảnh sai kiểu ⇒ 415; `POST /health` ⇒ 405) thì Caddy không chen vào — trần chỉ cắt khi thân được đọc | chạy thật |
| MỘT câu hỏi đáp thật | "Vé tham quan Đại Nội bao nhiêu?" ⇒ 200, 6,8 giây, 7 nguồn, đúng giá của kho | chạy thật |
| MỘT lượt xếp lịch thật (đường duy nhất đọc các file bảng riêng tư) | lịch 2 ngày mặc định ⇒ 200, 8,4 giây, đủ câu tả | chạy thật |
| Giới hạn lượt | trần 3 lượt / địa chỉ: lượt thứ 4 ⇒ 429 kèm lời báo tiếng Việt. Yêu cầu bị Caddy cắt vì quá cỡ VẪN tính một lượt (phần đầu yêu cầu đã tới app) | chạy thật |
| Khởi động lại hộp app (dừng hẳn rồi bật, hai lần) | 12,0–13,0 giây tới `/health` ok: khoảng 9,6 giây nạp thư viện Python (torch…), 1,4 giây nạp model nhúng + nối Qdrant (lần bật đầu tiên sau khi dựng ảnh: 3,3 giây); câu trả lời đầu sau đó 6,0–6,3 giây, trong đó model 5,0–5,3 giây ⇒ không có độ trễ riêng của câu đầu | chạy thật |
| RAM | app 886–933 MiB / 2 GiB (sau câu hỏi lẫn sau xếp lịch) · Qdrant 186–196 MiB / 768 MiB · Caddy 12 MiB. Server ngoài hộp sau 59 lượt: 1.526 MB (phiên đo) ⇒ trần 2 GiB của hộp app còn dư nhưng không rộng | chạy thật |
| Volume chung cho file khoá | hộp A ghi "file tạm rồi đổi tên" ⇒ hộp B đang chạy (gắn chỉ đọc) đọc ngay nội dung mới; hộp B không ghi được | chạy thật |
| `dong_goi.sh e7193bd` | 28 giây; `app_e7193bd.tar.gz` 909 MB · `qdrant.snapshot` 78 MB · bốn file cấu hình; `sha256sum -c` 6 / 6 OK | chạy thật |
| Dừng hẳn cả ba hộp rồi bật CÙNG LÚC (như Docker tự bật lại khi máy mở) | 11,4 giây tới `/health` ok; Qdrant của gói vẫn 9.479 điểm (chỉ mục nằm ở thư mục `qdrant_storage/` trên đĩa) | chạy thật |
| Ca xấu: app + Caddy bật TRƯỚC, Qdrant sau 25 giây | bản đầu của gói: `/health` trả HTTP 200 nhưng `degraded`, Docker vẫn coi hộp app là `healthy`, mọi câu ra "Hệ thống tra cứu tạm thời không khả dụng", KHÔNG tự hồi ⇒ ĐÃ SỬA trong `compose.yml`: hộp app chờ Qdrant trả được collection rồi mới chạy server, và chỉ `status: ok` mới tính là khoẻ. Sau sửa: trong lúc chờ Caddy trả 502, log app "chờ Qdrant có collection…", 19 giây sau khi Qdrant bật là ok | chạy thật, trước và sau sửa |
| Qdrant khởi động lại GIỮA CHỪNG khi app đang chạy | app tự chạy tiếp: 6 giây sau `/health` ok, câu hỏi thật trả lời được | chạy thật |
| `compose.vai-may.yml` chạy trọn với một máy chủ ĐỨNG THAY dịch vụ thông tin máy (không phải AWS) | hộp `khoa` ghi file, app chỉ lên sau khi `khoa` khoẻ; app đọc được file (đủ ba khoá), không ghi được vào volume. Dừng hẳn BỐN hộp rồi bật cùng lúc: `khoa` ghi lại file sau 0,75 giây, app in dòng log đầu sau 9,9 giây và `/health` ok sau 13,8 giây ⇒ file khoá luôn mới TRƯỚC khi app nhận được câu đầu | chạy thật (khoá giả ⇒ không gọi model ở ca này) |
| `don` | 0 hộp, 0 volume của lượt thử còn lại; Qdrant của dự án không bị đụng | chạy thật |

**Lượt thử thứ hai — 10:43 23/11/2026, ảnh `hue-rag-app:e38b55c`, sau đợt sửa theo hai bản soát khác hãng (mỗi dòng là một thay đổi được thấy chạy):**

| Bước | Kết quả | |
|---|---|---|
| Dựng lại | 6 giây (có bộ đệm); ảnh `linux/amd64`; kiểm mới trong `dung_anh.sh`: model nhúng + bảng mã đếm token nạp được trong hộp KHÔNG có mạng | chạy thật |
| Nạp chỉ mục | đếm CHÍNH XÁC 9.479 = bản ghi dựng; bản chép của bản chụp trong hộp Qdrant đã xoá | chạy thật |
| Luồng `/api/chat/stream` qua Caddy | `text/event-stream`, không nén; ba sự kiện trạng thái tới ngay ở giây 0,0, câu trả lời + nguồn ở giây 5,7 ⇒ Caddy không gom luồng | chạy thật (gọi bằng script, chưa qua trình duyệt) |
| Log của hộp app | 0 dòng truy cập, 0 địa chỉ IP; giờ ghi theo giờ Việt Nam; `logs/application.log` nằm ngoài hộp | chạy thật |
| `compose.vai-may.yml` bản mới (file khoá trong RAM, hộp `khoa` gốc chỉ đọc + bỏ hết quyền đặc biệt, chu kỳ 60 giây) với máy chủ đứng thay | bốn hộp khoẻ; app thấy thư mục khoá kiểu `tmpfs`, chỉ đọc; dừng hẳn rồi bật: file khoá ghi lại sau 1 giây, `/health` ok sau 12,9 giây; 80 giây sau đã có hai lần ghi | chạy thật (khoá giả) |
| Đổi model bằng một dòng của `cau_hinh/settings.yaml` | ⇒ `openai` khi KHÔNG có khoá: app lên, `/health` `degraded` (`generator: not_ready`), log "Generator startup failed", câu hỏi ra "Không thể tạo câu trả lời vào lúc này", Docker không tính hộp là khoẻ · đổi ngược ⇒ `bedrock`: ok, câu hỏi thật trả lời được, băm file = bản trong ảnh | chạy thật; KHÔNG gọi model cũ (đang gác) |
| Bản đầu gắn riêng FILE `settings.yaml` | sau khi file bị thay bằng file mới (`sed -i`) hộp app không khởi động lại được (lỗi gắn file của Docker Desktop) ⇒ đổi sang gắn cả thư mục `cau_hinh/` | chạy thật, trước và sau sửa |
| `dong_goi.sh e38b55c` | thêm `cau_hinh/`; `sha256sum -c` 8 / 8 | chạy thật |

**Lượt thử thứ ba — 12:24–12:31 23/11/2026, ảnh `hue-rag-app:0367e77` (= main lúc đó), ĐƯỜNG DEPLOY: chỉ `compose.yml`, `provider: openai`. Không lời gọi
nào tới OpenAI (tài khoản đang gác): hai ca dưới chỉ trả lời câu "gói báo gì khi khoá thiếu / khoá không dùng được".**

| Bước | Kết quả | |
|---|---|---|
| `thu_o_may.sh len` KHÔNG có khoá (ca "thiếu khoá") | Qdrant của gói 9.479 điểm; app lên nhưng `/health` `degraded` (`generator: not_ready`), log "Generator startup failed"; Docker tính hộp app `unhealthy`, hộp Caddy không được bật; lệnh thoát mã 1 sau 3 phút (36 lần hỏi sức khoẻ × 5 giây) | chạy thật |
| `thu_o_may.sh len` với khoá GIẢ (file riêng, kèm `OPENAI_BASE_URL` trỏ một cổng đóng để không gì đi tới OpenAI) | **xanh giả**: ba hộp lên trong 38 giây, `/health` `ok` (cả `generator: ready`), `kiem` đạt mọi dòng (trang chủ 200 · `/docs` 404 · 267 bài · thân 13 MB ⇒ 413); MỘT câu hỏi ⇒ sau 1,3 giây sự kiện lỗi "Không thể tạo câu trả lời vào lúc này." (`generation_failed`), `/health` sau đó VẪN `ok` ⇒ chỉ câu hỏi thật mới lộ khoá hỏng | chạy thật (lỗi ở đây là lỗi kết nối; khoá sai thật / hết tiền cho CÙNG câu báo theo code, chưa chạy với OpenAI thật) |
| `dong_goi.sh 0367e77` (mặc định `openai`) | 29 giây; `sha256sum -c` 7 / 7 OK; `cau_hinh/settings.yaml` của gói ghi `provider: openai` (bản trong ảnh vẫn `bedrock`); gói KHÔNG kèm `compose.vai-may.yml`; không bản chụp nào để lại ở Qdrant nguồn | chạy thật |
| Nhiều mảnh chữ nhỏ sát nhau qua Caddy (đường model của OpenAI phát chữ DẦN; mọi lượt thử trước là trên Claude — chữ ra một lần) | Chỉ Caddy của gói + một hộp giả phát đúng khuôn sự kiện của app, phía gọi gửi `Accept-Encoding: gzip` như trình duyệt: 50 mảnh × 40 ms ⇒ tới ở 50 thời điểm khác nhau, khe lớn nhất 42 ms (thẳng hộp giả: 44 ms); 150 mảnh × 10 ms ⇒ 147 thời điểm, khe lớn nhất 11 ms; không nén. Đối chứng (hộp giả dồn mọi mảnh rồi mới phát): thước thấy ngay — mọi mảnh tới cùng lúc ở giây 2,0 ⇒ Caddy KHÔNG dồn chữ | chạy thật với luồng GIẢ (không phải app thật trên đường OpenAI) |

Đã chạy thật trước đó, không tốn gì: ca đối chứng của `dung_ngu_canh.py` (commit có kho cũ `2f7b56e4` ⇒ DỪNG, báo 3 bài lệch băm + 2 bài thiếu) ·
`docker compose config` cho cả hai tổ hợp file · `lam_moi_khoa.py` với máy chủ ĐỨNG THAY dịch vụ thông tin máy (đúng khuôn tài liệu AWS): file quyền 600 đủ
ba khoá, hàm ký thật của app nhận, 0 giá trị khoá lọt log; máy chủ tắt / `Code` khác `Success` / thiếu trường ⇒ không đụng file. Phiên B đọc gói và tự chạy lại
ba phép 0 đồng (cùng số).

CHƯA kiểm:
- Mọi thứ trên AWS: hộp `khoa` ở mạng của máy hỏi được dịch vụ thông tin máy với bước nhảy 1, khoá của vai gọi được model, HTTPS thật qua Caddy,
  `docker load` + bốn lệnh trên máy đích. Máy dừng / bật thật (ở đây giả lập bằng dừng / bật các hộp; Docker tự bật lại hộp sau khi máy mở cần
  `sudo systemctl enable docker` — việc của bước dựng máy).
- Đường deploy với khoá OpenAI THẬT trong hộp: chưa có lượt nào (tài khoản đang gác) — câu trả lời thật, chữ chạy dần của app thật qua Caddy, lỗi 401 / hết tiền nhìn ra sao.
- Trình duyệt: phiên đo đã mở gói qua Caddy bằng Playwright MCP sáng 23/11 (đường Bedrock: dòng tiến độ hiện dần, lịch ví dụ + ảnh nạp được); chưa có lượt trình duyệt trên đường OpenAI.
- Hộp chạy bằng người dùng root (như bản 16/11); chưa hạ quyền.
- Đã xét, KHÔNG đổi (kết quả tra cứu 23/11 nêu): bỏ `flush_interval -1` ở Caddy (Caddy tự đẩy ngay luồng `text/event-stream`; giữ vì cấu hình
  này đã chạy thật 16/11) · thêm hạn giờ đọc / ghi ở Caddy (lượt dài nhiều vòng công cụ có thể bị cắt; chưa thấy sự cố nào cần nó).
- Sau `docker load` trên máy đích nên xoá `app_<sha>.tar.gz` (0,9 GB) cho nhẹ đĩa.

## 6. Khác bản nháp 16/11 (`data/phase_12/deploy_nhap/`, riêng tư)

Bản nháp lệch hệ thống hôm nay ở 4 file bảng (`diem_v9` ⇒ `diem_v10`, `bang_quan_lich_v1` ⇒ `v2`, thiếu `khoang_cach_v1`, thiếu
`su_kien_theo_ngay_v2`) và 4 bài kho (263 ⇒ 267) — dựng lại sẽ không khởi động được; và không có chỗ đưa quyền Bedrock vào hộp. Bản này: danh
sách file sinh từ `settings.yaml` + bản ghi dựng (hết chép tay hai chỗ) · code lấy từ một commit thay cho cây đang sửa · quyền Bedrock qua file
phủ · thêm trần tổng lượt mỗi ngày, trần cỡ yêu cầu ở Caddy, phép kiểm sức khoẻ của app · gói nằm trong git (kho đã công khai từ 20/11).
Giữ nguyên từ bản nháp (đã chạy thật 16/11): torch bản CPU, model nhúng tải lúc dựng, liên kết `public` ⇒ `dist`, một tiến trình, cách nạp chỉ
mục bằng bản chụp.
