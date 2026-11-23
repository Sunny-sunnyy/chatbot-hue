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

## 2. Dùng

```bash
deploy/docker/dung_anh.sh                 # ảnh từ HEAD; hoặc: dung_anh.sh origin/main
HUE_IMAGE=hue-rag-app:<sha> deploy/docker/thu_o_may.sh len
deploy/docker/thu_o_may.sh kiem           # không gọi model; in sẵn lệnh hỏi MỘT câu thật
deploy/docker/thu_o_may.sh don
```

Trên máy đích: chép `compose.yml`, file phủ hợp với máy, `Caddyfile`, ảnh (`docker save | gzip` ⇒ `docker load`) và bản chụp Qdrant vào một thư
mục; viết `hue.env` (biến không bí mật — danh sách ở đầu `compose.yml`); nạp bản chụp như `thu_o_may.sh` làm; rồi
`docker compose --env-file hue.env -f compose.yml -f <file phủ> up -d --wait`. Thứ tự lệnh đủ cho AWS thuộc bản thiết kế deploy.

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
  tên" vào volume chung. Không khoá dài hạn nào nằm trên máy. Cần phía Terraform: vai có quyền gọi model + bước nhảy IMDS = 2.
- Máy KHÔNG gắn được vai: phải chọn giữa (i) khoá dài hạn chỉ có quyền đổi lấy khoá tạm + một hộp phụ khác, hoặc (ii) sửa lớp nối cho
  `sessionToken` thành tuỳ chọn. Chưa viết — chờ phương án hạ tầng được chốt.

## 5. Đã kiểm ↔ chưa kiểm (23/11/2026)

Đã chạy thật, không tốn gì:
- `dung_ngu_canh.py` trên `origin/main` `c2579fad`: 595 file code · 267 bài kho khớp băm với bản ghi dựng (9.479 điểm) · 11 file riêng tư · 0 file
  cấm · 23 MB. Ca đối chứng: commit có kho cũ `2f7b56e4` ⇒ DỪNG, báo 3 bài lệch băm + 2 bài thiếu.
- `docker compose config` cho cả hai tổ hợp file: hợp lệ; thiếu `HUE_IMAGE` ⇒ dừng với lời báo rõ.
- `lam_moi_khoa.py` với một máy chủ ĐỨNG THAY dịch vụ thông tin máy (đúng khuôn tôi nhớ của AWS, không phải AWS): ghi file quyền 600 đủ ba khoá,
  hàm ký thật của app (`sign_headers`) nhận file đó, không giá trị khoá nào lọt ra log; máy chủ tắt ⇒ giữ file cũ, in tên lớp lỗi.

CHƯA kiểm:
- **Dựng ảnh và chạy thử trọn gói** (việc nặng, chờ làn máy) — kể cả: Dockerfile mới chép cả thư mục `data/`, cú pháp `request_body` của Caddy,
  `env_file` không bắt buộc, phép chờ `--wait`, một câu thật qua Bedrock từ trong hộp.
- Mọi thứ trên AWS: khuôn trả lời thật của IMDSv2, bước nhảy 2, khoá của vai có gọi được model không, HTTPS thật qua Caddy.
- Hộp chạy bằng người dùng root (như bản 16/11); chưa hạ quyền.

## 6. Khác bản nháp 16/11 (`data/phase_12/deploy_nhap/`, riêng tư)

Bản nháp lệch hệ thống hôm nay ở 4 file bảng (`diem_v9` ⇒ `diem_v10`, `bang_quan_lich_v1` ⇒ `v2`, thiếu `khoang_cach_v1`, thiếu
`su_kien_theo_ngay_v2`) và 4 bài kho (263 ⇒ 267) — dựng lại sẽ không khởi động được; và không có chỗ đưa quyền Bedrock vào hộp. Bản này: danh
sách file sinh từ `settings.yaml` + bản ghi dựng (hết chép tay hai chỗ) · code lấy từ một commit thay cho cây đang sửa · quyền Bedrock qua file
phủ · thêm trần tổng lượt mỗi ngày, trần cỡ yêu cầu ở Caddy, phép kiểm sức khoẻ của app · gói nằm trong git (kho đã công khai từ 20/11).
Giữ nguyên từ bản nháp (đã chạy thật 16/11): torch bản CPU, model nhúng tải lúc dựng, liên kết `public` ⇒ `dist`, một tiến trình, cách nạp chỉ
mục bằng bản chụp.
