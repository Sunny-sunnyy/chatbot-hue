#!/usr/bin/env bash
# Dựng ảnh app bằng MỘT lệnh:  deploy/docker/dung_anh.sh <commit>      (phải ghi rõ commit / nhánh lấy code + kho, vd origin/main — đứng ở một nhánh
#   khác mà để mặc định HEAD thì ảnh mang code của nhánh đó chứ không phải bản định đưa lên)
#   1. dựng thư mục ngữ cảnh tạm từ đúng commit đó + file bảng riêng tư của `data/` (dung_ngu_canh.py — dừng nếu kho ở commit khác chỉ mục)
#   2. docker build ⇒ ảnh hue-rag-app:<7 ký tự sha>
#   3. kiểm trong ảnh: 0 file cấm ở phần dữ liệu, số bài kho = số bài của bản ghi dựng, model nhúng + bảng mã đếm token nạp được khi KHÔNG có mạng
#   4. xoá thư mục ngữ cảnh tạm (nó có bản chép file riêng tư)
# File gói (Dockerfile, lam_moi_khoa.py) lấy từ CÂY ĐANG ĐỨNG, code + kho lấy từ <commit> ⇒ dựng được cả một nhánh chưa gộp.
# Thư mục data/: mặc định của cây chính (cây đầu trong `git worktree list`); chỗ khác thì đặt HUE_DU_LIEU=<đường dẫn>.
# Việc nặng (lần đầu vài phút, ~2 GB RAM, ảnh ~3,6 GB) — máy dùng chung thì báo phiên điều phối trước.
set -euo pipefail
GOI=$(cd "$(dirname "$0")" && pwd)
cd "$GOI"
REF=${1:?dùng: dung_anh.sh <commit hoặc nhánh, vd origin/main>}
SHA=$(git rev-parse --short=7 "$REF^{commit}")
CAY_CHINH=$(git worktree list --porcelain | head -n 1 | cut -d' ' -f2-)
DU_LIEU=${HUE_DU_LIEU:-$CAY_CHINH/data}
NGU_CANH=$(mktemp -d /tmp/hue_ngu_canh.XXXXXX)
trap 'rm -rf "$NGU_CANH"' EXIT

UV_PROJECT_ENVIRONMENT=$CAY_CHINH/.venv uv run --no-sync python "$GOI/dung_ngu_canh.py" --ref "$REF" --du-lieu "$DU_LIEU" --ra "$NGU_CANH"
cp "$GOI/lam_moi_khoa.py" "$NGU_CANH/"
# linux/amd64: máy đích là máy x86-64 (họ t3a / m7i); dựng trên máy ARM mà không ghi rõ sẽ ra ảnh không chạy được ở đó
docker build --platform linux/amd64 -f "$GOI/Dockerfile" -t "hue-rag-app:$SHA" --label "hue.commit=$(git rev-parse "$REF^{commit}")" "$NGU_CANH"

MONG=$(grep -oE '^bai_kho: [0-9]+' "$NGU_CANH/DANH_SACH.txt" | cut -d' ' -f2)
read -r CAM CO < <(docker run --rm --network none --entrypoint bash "hue-rag-app:$SHA" -c \
  'cd /app && echo "$(find data knowledge-base-hue frontend/dist -type f | grep -ciE "sealed|\.env$|/rieng/|_source-dumps|/evaluation/") $(find knowledge-base-hue -name "*.md" | wc -l)"')
[ "$CAM" = 0 ] || { echo "DỪNG: ảnh có $CAM file cấm ở phần dữ liệu — không dùng ảnh này"; exit 1; }
[ "$CO" = "$MONG" ] || { echo "DỪNG: ảnh có $CO bài kho, bản ghi dựng có $MONG"; exit 1; }
# Thiếu file của model nhúng / bảng mã thì lúc bật trên máy đích app sẽ đi tải qua mạng (hoặc hỏng) — bắt ngay ở đây, trong một hộp không có mạng
docker run --rm --network none --entrypoint python "hue-rag-app:$SHA" -c "
import tiktoken; tiktoken.get_encoding('o200k_base').encode('Huế')
from huggingface_hub import snapshot_download
snapshot_download('intfloat/multilingual-e5-small', revision='614241f622f53c4eeff9890bdc4f31cfecc418b3', local_files_only=True)" >/dev/null 2>&1 \
  || { echo "DỪNG: ảnh không tự đủ model nhúng / bảng mã đếm token khi không có mạng"; exit 1; }
echo "XONG: hue-rag-app:$SHA · $(docker images "hue-rag-app:$SHA" --format '{{.Size}}') · $CO bài kho · 0 file cấm"
echo "Chạy thử ở máy này: HUE_IMAGE=hue-rag-app:$SHA $GOI/thu_o_may.sh len"
