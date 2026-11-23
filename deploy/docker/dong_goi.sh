#!/usr/bin/env bash
# Gom MỌI thứ máy đích cần vào một thư mục:  dong_goi.sh <7 ký tự sha của ảnh đã dựng>      (ra: ~/hue_goi_<sha>, đổi bằng HUE_GOI_RA)
#   app_<sha>.tar.gz (ảnh app, `docker load` trên máy đích) · qdrant.snapshot (chỉ mục) · compose.yml · compose.vai-may.yml · Caddyfile ·
#   nap_chi_muc.sh · cau_hinh/ (settings.yaml + logging.yaml của chính ảnh đó) · SHA256SUMS. Thư mục này RIÊNG TƯ (ảnh mang file bảng của data/): chỉ đưa lên nơi lưu riêng (thùng S3 riêng tư, USB), không lên GitHub.
set -euo pipefail
GOI=$(cd "$(dirname "$0")" && pwd)
SHA=${1:?dùng: dong_goi.sh <sha của ảnh hue-rag-app:<sha>>}
RA=${HUE_GOI_RA:-$HOME/hue_goi_$SHA}
docker image inspect "hue-rag-app:$SHA" >/dev/null 2>&1 || { echo "DỪNG: chưa có ảnh hue-rag-app:$SHA — chạy dung_anh.sh trước" >&2; exit 1; }
mkdir -p "$RA" && cd "$RA"
docker save "hue-rag-app:$SHA" | gzip -1 > "app_$SHA.tar.gz"
"$GOI/chup_chi_muc.sh" "$RA/qdrant.snapshot"
cp "$GOI"/compose.yml "$GOI"/compose.vai-may.yml "$GOI"/Caddyfile "$GOI"/nap_chi_muc.sh .
# thư mục cấu hình app: lấy ĐÚNG bản nằm trong ảnh (compose gắn nó đè lên bản trong ảnh ⇒ sửa được trên máy đích mà không dựng lại ảnh)
mkdir -p cau_hinh && docker run --rm --network none --entrypoint tar "hue-rag-app:$SHA" -C /app/backend/config -cf - . | tar -xf - -C cau_hinh
sha256sum "app_$SHA.tar.gz" qdrant.snapshot compose.yml compose.vai-may.yml Caddyfile nap_chi_muc.sh cau_hinh/* > SHA256SUMS
ls -la "$RA"
echo "XONG: $RA — trên máy đích: sha256sum -c SHA256SUMS && gunzip -c app_$SHA.tar.gz | docker load   (script chạy bằng: bash nap_chi_muc.sh <file phủ>)"
