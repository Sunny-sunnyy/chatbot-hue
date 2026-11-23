# Gói Docker của trợ lý Huế

Viết: 09:15 23/11/2026 (giờ `date`), phiên C, việc X14 phần (4). Người đọc: người (hoặc agent) sẽ dựng và chạy hệ thống trên một máy khác máy
chủ dự án. Đọc cùng bản thiết kế deploy (`docs/superpowers/specs/`) và thư mục `deploy/terraform/` — trang này chỉ nói về phần "hộp".

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
| `compose.yml` | ba hộp + các chốt cho bản mở ra ngoài; chưa nói quyền gọi model tới từ đâu |
| `compose.thu.yml` | file phủ để thử ở máy chủ dự án: gắn file khoá tạm đang có, chỉ đọc |
| `compose.vai-may.yml` + `lam_moi_khoa.py` | file phủ cho máy AWS có vai gắn: hộp phụ `khoa` lấy khoá tạm của vai, tự làm mới 5 phút một lần |
| `Caddyfile` | cửa vào; không nén luồng trả lời để chữ ra ngay |
| `thu_o_may.sh len / kiem / don` | chạy thử trọn gói ở máy chủ dự án, cổng 8880, không đụng server 8010 |
| `chup_chi_muc.sh <file ra>` | lấy chỉ mục ra một file bản chụp từ Qdrant đang chạy (tạo ⇒ tải ⇒ xoá ngay ở nguồn; chỉ đọc) |
| `nap_chi_muc.sh <file phủ>` | nạp bản chụp vào Qdrant của gói, so số điểm với bản ghi dựng trong ảnh — dùng ở máy thử LẪN máy đích |
| `dong_goi.sh <sha>` | gom mọi thứ máy đích cần vào `~/hue_goi_<sha>/` kèm `SHA256SUMS` |

## 2. Dùng

```bash
deploy/docker/dung_anh.sh                 # ảnh từ HEAD; hoặc: dung_anh.sh origin/main
HUE_IMAGE=hue-rag-app:<sha> deploy/docker/thu_o_may.sh len
deploy/docker/thu_o_may.sh kiem           # không gọi model; in sẵn lệnh hỏi MỘT câu thật
deploy/docker/thu_o_may.sh don
```

Đưa sang máy đích: `deploy/docker/dong_goi.sh <sha>` ra thư mục `~/hue_goi_<sha>/` gồm `app_<sha>.tar.gz` (ảnh, khoảng 0,9 GB theo số đo 16/11) ·
`qdrant.snapshot` (chỉ mục) · `compose.yml` · `compose.vai-may.yml` · `Caddyfile` · `nap_chi_muc.sh` · `SHA256SUMS`. Thư mục này riêng tư.
Trên máy đích (Linux x86-64 — ảnh dựng cho `amd64`, không chạy trên máy ARM; Docker có Compose từ 2.24), trong thư mục đó:

```bash
sha256sum -c SHA256SUMS && gunzip -c app_<sha>.tar.gz | docker load
nano hue.env                               # biến không bí mật — danh sách ở đầu compose.yml; ít nhất HUE_IMAGE, HUE_SITE
./nap_chi_muc.sh compose.vai-may.yml       # bật Qdrant, nạp chỉ mục, so số điểm
docker compose --env-file hue.env -f compose.yml -f compose.vai-may.yml up -d --wait
```

Thứ tự đủ cho AWS (tạo máy, mở cổng, lúc nào tính tiền, lùi thế nào) thuộc bản thiết kế deploy.

## 3. Thứ gì riêng tư, thứ gì nằm trong ảnh

| Thứ | Trong ảnh? | Ghi chú |
|---|---|---|
| Code `backend/`, `frontend/`, 267 bài kho, bảng điều kiện của kho | có | đều đã công khai trên GitHub |
| 11 file bảng lấy từ `data/` (9 bảng theo `settings.yaml` + bản ghi dựng chỉ mục + thống kê từ khoá) | **có — riêng tư** | kê tên + băm ở `/app/DANH_SACH.txt` trong ảnh. Vì chúng: **không đẩy ảnh lên kho ảnh công khai** (Docker Hub công khai, ECR Public); chuyển bằng `docker save` hoặc kho ảnh riêng |
| Chỉ mục Qdrant | không | đi bằng bản chụp (~56 MB), nạp vào hộp `qdrant` lúc dựng máy |
| `.env` của máy chủ dự án | **không bao giờ** | gói không đọc file này |
| File khoá tạm Bedrock / khoá của vai | **không bao giờ** | gắn vào lúc chạy ở `/run/hue-khoa/bedrock.json` (file phủ) |
| Khoá tra web, khoá trang theo dõi | **không bao giờ** | file `hue.khoa.env` cạnh `compose.yml` trên máy đích, quyền 600; không có cũng chạy |
| Bộ câu kín, bộ câu mẫu, `_source-dumps`, ảnh `frontend/public/anh/rieng`, phần còn lại của `data/` | **không bao giờ** | không vào ngữ cảnh; `dung_anh.sh` còn đếm lại trong ảnh, khác 0 thì dừng |
| Log, số đo từng lượt | không | thư mục `logs/` cạnh `compose.yml` trên máy đích |

## 4. Quyền gọi model đi vào hộp thế nào

Lớp nối model (`backend/llm/bedrock_model.py`) KHÔNG dùng thư viện AWS: nó tự ký từ một file JSON ba khoá `accessKeyId`, `secretAccessKey`,
`sessionToken` (cả ba bắt buộc), đường dẫn ở biến `HUE_BEDROCK_CREDS_FILE`, đọc lại ở MỖI lời gọi. Gói giữ nguyên điều đó: app luôn đọc
`/run/hue-khoa/bedrock.json`; file tới từ đâu do file phủ quyết định, ảnh không đổi.

- `compose.thu.yml`: gắn file khoá tạm của máy chủ dự án (một file, chỉ đọc).
- `compose.vai-may.yml`: hộp `khoa` hỏi dịch vụ thông tin máy (IMDSv2) lấy khoá tạm của vai, đổi tên trường, ghi file kiểu "file tạm rồi đổi
  tên" vào một volume chung (app gắn cả thư mục, chỉ đọc ⇒ luôn thấy file mới). Không khoá dài hạn nào nằm trên máy. Khuôn hỏi – đáp đã đối
  chiếu tài liệu AWS (phiên B, 23/11): AWS đưa khoá mới ra ít nhất 5 phút trước khi khoá cũ hết hạn ⇒ hỏi 5 phút một lần.
  Hộp `khoa` dùng thẳng mạng của máy (`network_mode: host`) ⇒ bước nhảy IMDS để 1 vẫn chạy, và ba hộp còn lại (trong đó có hộp nhận yêu cầu từ
  internet) không tới được dịch vụ thông tin máy. Cần phía Terraform: vai có quyền gọi model, `http_tokens = "required"`.
  Hai điều biết trước: (a) máy khởi động lại thì Docker tự bật lại các hộp không theo thứ tự — vài giây đầu app có thể còn đọc file khoá cũ đã
  hết hạn, lượt hỏi đúng lúc đó nhận lỗi "khoá Bedrock bị từ chối hoặc đã hết hạn" một lần; (b) vai bị gỡ khỏi máy / bị gắn chính sách cấm thì
  lỗi người dùng thấy cũng là dòng đó, còn nguyên nhân nằm ở log hộp `khoa` ("CHƯA lấy được khoá tạm của vai") và trạng thái `unhealthy` của nó.
- Máy KHÔNG gắn được vai: phải chọn giữa (i) khoá dài hạn chỉ có quyền đổi lấy khoá tạm + một hộp phụ khác, hoặc (ii) sửa lớp nối cho
  `sessionToken` thành tuỳ chọn. Chưa viết — chờ phương án hạ tầng được chốt.

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
| `don` | 0 hộp, 0 volume của lượt thử còn lại; Qdrant của dự án không bị đụng | chạy thật |

Đã chạy thật trước đó, không tốn gì: ca đối chứng của `dung_ngu_canh.py` (commit có kho cũ `2f7b56e4` ⇒ DỪNG, báo 3 bài lệch băm + 2 bài thiếu) ·
`docker compose config` cho cả hai tổ hợp file · `lam_moi_khoa.py` với máy chủ ĐỨNG THAY dịch vụ thông tin máy (đúng khuôn tài liệu AWS): file quyền 600 đủ
ba khoá, hàm ký thật của app nhận, 0 giá trị khoá lọt log; máy chủ tắt / `Code` khác `Success` / thiếu trường ⇒ không đụng file. Phiên B đọc gói và tự chạy lại
ba phép 0 đồng (cùng số).

CHƯA kiểm:
- Mọi thứ trên AWS: hộp `khoa` ở mạng của máy hỏi được dịch vụ thông tin máy với bước nhảy 1, khoá của vai gọi được model, HTTPS thật qua Caddy,
  `docker load` + bốn lệnh trên máy đích, `compose.vai-may.yml` chạy cùng app (ở máy này mới thử từng phần của nó).
- Luồng trả lời `/api/chat/stream` qua Caddy và trình duyệt mở cổng 8880 (lượt thử gọi `/api/chat`, không qua trình duyệt).
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
