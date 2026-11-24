#!/usr/bin/env bash
# Gom MỌI thứ máy đích cần vào một thư mục:  dong_goi.sh <7 ký tự sha của ảnh đã dựng> [openai|bedrock]      (ra: ~/hue_goi_<sha>, đổi bằng HUE_GOI_RA)
# Tham số thứ hai = model viết của bản đưa lên, mặc định `openai` (đường deploy đã chốt 23/11/2026). Lệnh GHI SẴN dòng `provider` đó vào
# cau_hinh/settings.yaml rồi mới băm ⇒ trên máy đích không còn bước sửa tay nào để quên; `bedrock` thì gói kèm compose.vai-may.yml.
#   app_<sha>.tar.gz (ảnh app, `docker load` trên máy đích) · qdrant.snapshot (chỉ mục) · compose.yml · compose.vai-may.yml · Caddyfile ·
#   nap_chi_muc.sh · cau_hinh/ (settings.yaml + logging.yaml của chính ảnh đó) · SHA256SUMS. Thư mục này RIÊNG TƯ (ảnh mang file bảng của data/): chỉ đưa lên nơi lưu riêng (thùng S3 riêng tư, USB), không lên GitHub.
set -euo pipefail
GOI=$(cd "$(dirname "$0")" && pwd)
SHA=${1:?dùng: dong_goi.sh <sha của ảnh hue-rag-app:<sha>> [openai|bedrock]}
PROVIDER=${2:-openai}
case "$PROVIDER" in openai|bedrock) ;; *) echo "DỪNG: model viết phải là openai hoặc bedrock" >&2; exit 1 ;; esac
RA=${HUE_GOI_RA:-$HOME/hue_goi_$SHA}
docker image inspect "hue-rag-app:$SHA" >/dev/null 2>&1 || { echo "DỪNG: chưa có ảnh hue-rag-app:$SHA — chạy dung_anh.sh trước" >&2; exit 1; }
mkdir -p "$RA" && cd "$RA"
docker save "hue-rag-app:$SHA" | gzip -1 > "app_$SHA.tar.gz"
"$GOI/chup_chi_muc.sh" "$RA/qdrant.snapshot"
cp "$GOI"/compose.yml "$GOI"/Caddyfile "$GOI"/nap_chi_muc.sh .
PHU=""; [ "$PROVIDER" = bedrock ] && { cp "$GOI"/compose.vai-may.yml .; PHU=compose.vai-may.yml; }
# thư mục cấu hình app: lấy ĐÚNG bản nằm trong ảnh (compose gắn nó đè lên bản trong ảnh ⇒ sửa được trên máy đích mà không dựng lại ảnh)
mkdir -p cau_hinh && docker run --rm --network none --entrypoint tar "hue-rag-app:$SHA" -C /app/backend/config -cf - . | tar -xf - -C cau_hinh
sed -i "s/^\(  provider: \)[a-z]*/\1$PROVIDER/" cau_hinh/settings.yaml
grep -q "^  provider: $PROVIDER\b" cau_hinh/settings.yaml || { echo "DỪNG: không ghi được dòng provider vào cau_hinh/settings.yaml" >&2; exit 1; }
# Ba công tắc chỉ định bật ở máy demo — bản đưa lên GHI SẴN tắt (ảnh dựng từ commit cũ chưa có dòng nào thì bỏ qua dòng đó):
#   vi_sao — nút "Vì sao trả lời vậy?" · so_tay — sổ tay cho chuyến đi (một sổ tay 9–10 lời gọi model mà tính một lượt; chưa có trần riêng — 24/11/2026)
#   ho_so_chu_de — hồ sơ theo chủ đề (một hồ sơ 4–8 lời gọi model mà tính một lượt; chưa có trần riêng — 24/11/2026)
for cong_tac in vi_sao so_tay ho_so_chu_de; do
  if grep -q "^  $cong_tac:" cau_hinh/settings.yaml; then
    sed -i "s/^\(  $cong_tac: \)true/\1false/" cau_hinh/settings.yaml
    grep -q "^  $cong_tac: false" cau_hinh/settings.yaml || { echo "DỪNG: không ghi được dòng $cong_tac: false vào cau_hinh/settings.yaml" >&2; exit 1; }
  fi
done
sha256sum "app_$SHA.tar.gz" qdrant.snapshot compose.yml $PHU Caddyfile nap_chi_muc.sh cau_hinh/* > SHA256SUMS
ls -la "$RA"
echo "model viết của gói: $PROVIDER$([ "$PROVIDER" = openai ] && echo ' — máy đích cần OPENAI_API_KEY trong hue.khoa.env')"
echo "XONG: $RA — trên máy đích: sha256sum -c SHA256SUMS && gunzip -c app_$SHA.tar.gz | docker load   (rồi: bash nap_chi_muc.sh $PHU)"
