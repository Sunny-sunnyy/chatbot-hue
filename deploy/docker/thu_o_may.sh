#!/usr/bin/env bash
# Chạy thử TRỌN GÓI ở máy chủ dự án, không đụng hệ thống đang chạy (server 8010, Qdrant 6335 chỉ bị ĐỌC một bản chụp):
#   HUE_IMAGE=hue-rag-app:<sha> deploy/docker/thu_o_may.sh len [openai|bedrock]   bật ba hộp ở cổng 8880, nạp chỉ mục từ bản chụp của Qdrant 6335, chờ app sẵn sàng
#   deploy/docker/thu_o_may.sh kiem                                 các phép kiểm không gọi model + in lệnh hỏi MỘT câu thật
#   deploy/docker/thu_o_may.sh don                                  tắt, xoá hộp + volume + thư mục thử
# Tham số thứ hai của `len` = model viết của lượt thử, mặc định `openai` (đường deploy đã chốt 23/11/2026, như dong_goi.sh):
#   openai   ĐÚNG bộ file máy đích dùng — chỉ compose.yml, không file phủ; dòng `provider` của cau_hinh/settings.yaml được ghi thành `openai`.
#            Khoá: biến HUE_KHOA_ENV = đường dẫn MỘT file có dòng `OPENAI_API_KEY=…` (đúng khuôn file `hue.khoa.env` của máy đích); script chỉ đặt một
#            liên kết tới file đó, không chép, không in, và KHÔNG đọc `.env` của dự án. Không đặt biến ⇒ lượt thử là ca "thiếu khoá": app phải KHÔNG
#            sẵn sàng và lệnh phải báo đỏ — đó là kết quả ĐÚNG của ca này.
#   bedrock  model Claude đang chạy ở máy chủ dự án, qua file phủ compose.thu.yml. File khoá tạm Bedrock: biến HUE_KHOA_FILE, không đặt thì lấy dòng
#            đầu của `data/duong_dan_khoa_bedrock.txt` ở cây chính (như scripts/bat_he_thong.sh).
# Việc nặng (ba hộp, app ~1 GB RAM) — báo phiên điều phối trước; RAM khả dụng < 4 GB thì không bật.
set -euo pipefail
GOI=$(cd "$(dirname "$0")" && pwd)
CAY_CHINH=$(git -C "$GOI" worktree list --porcelain | head -n 1 | cut -d' ' -f2-)
THU=/tmp/hue_thu_goi
DU_AN=hue_thu_goi
COL=hue_full_corpus_7a2_e5_small_384
NGUON=http://127.0.0.1:6335
CONG=${HUE_HTTP_PORT:-8880}
# File phủ chỉ có trong thư mục thử khi lượt thử là `bedrock` ⇒ `kiem` và `don` tự theo đúng đường của lần `len` gần nhất.
dc() { docker compose -p "$DU_AN" --env-file "$THU/hue.env" -f "$THU/compose.yml" $([ -f "$THU/compose.thu.yml" ] && echo "-f $THU/compose.thu.yml") "$@"; }
dung() { echo "DỪNG: $1" >&2; exit 1; }

case "${1:-}" in
len)
  [ -n "${HUE_IMAGE:-}" ] || dung "đặt HUE_IMAGE=<ảnh do dung_anh.sh in ra>"
  DUONG=${2:-openai}
  case "$DUONG" in openai|bedrock) ;; *) dung "model viết của lượt thử phải là openai hoặc bedrock" ;; esac
  [ -e "$THU" ] && dung "còn thư mục của lượt thử trước ($THU) — chạy: $0 don"
  [ "$(free -m | awk '/^Mem:/{print $7}')" -ge 4000 ] || dung "RAM khả dụng dưới 4 GB"
  if [ "$DUONG" = bedrock ]; then
    if [ -z "${HUE_KHOA_FILE:-}" ]; then HUE_KHOA_FILE=$(head -n 1 "$CAY_CHINH/data/duong_dan_khoa_bedrock.txt"); fi
    [ -f "$HUE_KHOA_FILE" ] || dung "không thấy file khoá tạm Bedrock (biến HUE_KHOA_FILE)"
  elif [ -n "${HUE_KHOA_ENV:-}" ]; then
    [ -f "$HUE_KHOA_ENV" ] || dung "không thấy file khoá HUE_KHOA_ENV trỏ tới"
    case "$(basename "$HUE_KHOA_ENV")" in .env|.env.*) dung "HUE_KHOA_ENV không được là file .env của dự án — tạo một file riêng chỉ có dòng OPENAI_API_KEY=…" ;; esac
  fi
  ss -ltn | grep -q ":$CONG " && dung "cổng $CONG đang có người dùng"
  mkdir -p "$THU/logs" && cp "$GOI"/compose.yml "$GOI"/Caddyfile "$GOI"/nap_chi_muc.sh "$THU/"
  # Hộp app chạy dưới USER hue (UID 10001) ⇒ trao quyền thư mục logs gắn từ máy trước khi `up`.
  docker run --rm --network none -v "$THU":/x -u 0 --entrypoint chown "$HUE_IMAGE" 10001:10001 /x/logs
  PHU=""; [ "$DUONG" = bedrock ] && { cp "$GOI"/compose.thu.yml "$THU/"; PHU=compose.thu.yml; }
  mkdir -p "$THU/cau_hinh" && docker run --rm --network none --entrypoint tar "$HUE_IMAGE" -C /app/backend/config -cf - . | tar -xf - -C "$THU/cau_hinh"   # như dong_goi.sh
  # dòng `provider`: ghi đúng như dong_goi.sh ghi cho gói đưa lên máy đích
  sed -i "s/^\(  provider: \)[a-z]*/\1$DUONG/" "$THU/cau_hinh/settings.yaml"
  grep -q "^  provider: $DUONG\b" "$THU/cau_hinh/settings.yaml" || dung "không ghi được dòng provider vào cau_hinh/settings.yaml"
  if [ "$DUONG" = openai ]; then
    if [ -n "${HUE_KHOA_ENV:-}" ]; then ln -s "$(realpath "$HUE_KHOA_ENV")" "$THU/hue.khoa.env"
    else echo "CA THIẾU KHOÁ: không đặt HUE_KHOA_ENV ⇒ mong app KHÔNG sẵn sàng (/health degraded, generator not_ready) và lệnh này báo đỏ."; fi
  fi
  # hue.env: biến không bí mật của lượt thử — http (không TLS), cookie không đòi https, trần 4 lượt / địa chỉ (phép thử cỡ thân của `kiem` + một câu hỏi + một lịch + một lượt nữa; lượt thứ 5 phải ra câu báo hết lượt)
  printf '%s\n' "HUE_IMAGE=$HUE_IMAGE" ${PHU:+"HUE_KHOA_FILE=$HUE_KHOA_FILE"} "HUE_SITE=:80" "HUE_HTTP_PORT=$CONG" "HUE_HTTPS_PORT=8443" \
    "HUE_COOKIE_SECURE=0" "HUE_LUOT_MOI_NGAY=4" "HUE_GIT_SHA=${HUE_IMAGE##*:}" > "$THU/hue.env"
  # Chỉ mục: đúng hai lệnh máy đích cũng dùng — chụp từ Qdrant đang chạy (xoá bản chụp ở nguồn ngay), nạp vào Qdrant của gói + so số điểm
  "$GOI/chup_chi_muc.sh" "$THU/qdrant.snapshot"
  ( cd "$THU" && COMPOSE_PROJECT_NAME=$DU_AN bash nap_chi_muc.sh $PHU )
  dc up -d --wait || {
    dc logs --tail 40 app
    echo "/health nhìn từ trong hộp app: $(dc exec -T app python -c "import urllib.request as u; print(u.urlopen('http://127.0.0.1:8000/health', timeout=3).read().decode()[:300])" 2>&1 | tail -n 1)"
    dung "app không sẵn sàng (model viết: $DUONG) — xem log trên; dọn: $0 don"
  }
  echo "ĐÃ LÊN (model viết: $DUONG): http://127.0.0.1:$CONG  ·  kiểm: $0 kiem  ·  dọn: $0 don"
  if [ "$DUONG" = openai ]; then echo "LƯU Ý: app chỉ kiểm CÓ khoá OpenAI, không kiểm khoá DÙNG ĐƯỢC — khoá sai / tài khoản hết tiền vẫn ra 'ĐÃ LÊN'. Chỉ một câu hỏi thật mới cho biết (lệnh in ở: $0 kiem)."; fi
  ;;
kiem)
  G=http://127.0.0.1:$CONG
  echo "model viết của lượt thử: $(grep -o '^  provider: [a-z]*' "$THU/cau_hinh/settings.yaml" | cut -d' ' -f4)   ·  file phủ: $([ -f "$THU/compose.thu.yml" ] && echo compose.thu.yml || echo 'không (đúng bộ file của máy đích)')"
  echo "trang chủ:        $(curl -s -o /dev/null -w '%{http_code}' $G/)   (mong 200)"
  echo "UID hộp app:      $(dc exec -T app id -u)   (mong 10001)"
  echo "security headers:"
  curl -sD - -o /dev/null "$G/" | grep -iE '^(x-content-type-options|x-frame-options|referrer-policy|content-security-policy):' | sed 's/^/  /'
  ASSET=$(curl -s "$G/" | grep -oE '/static/assets/[^"]+' | head -n 1 || true)
  if [ -n "$ASSET" ]; then
    echo "cache-control ($ASSET): $(curl -sI "$G$ASSET" | grep -i '^cache-control:' | tr -d '\r')"
  else
    echo "cache-control (/static/anh/dau_trang_ngo_mon.jpg): $(curl -sI "$G/static/anh/dau_trang_ngo_mon.jpg" | grep -i '^cache-control:' | tr -d '\r')"
  fi
  echo "/health:          $(curl -s $G/health | cut -c1-200)"
  echo "/docs:            $(curl -s -o /dev/null -w '%{http_code}' $G/docs)   (mong 404)"
  echo "/api/tinh_nang:   $(curl -s $G/api/tinh_nang | cut -c1-300)"
  echo "/api/kham_pha:    $(curl -s $G/api/kham_pha | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d["bai"]), "bài")' 2>&1 | tail -n 1)   (mong số bài của bản ghi dựng)"
  # Trần 12 MB của Caddy chỉ cắt khi thân được ĐỌC (đường trả lời trước khi đọc thân, vd sai kiểu ảnh ⇒ 415, thì Caddy không chen vào) ⇒ thử trên
  # /api/chat là đường đọc trọn thân. Phần đầu yêu cầu đã tới app trước khi Caddy cắt ⇒ phép thử này VẪN tính một lượt vào giới hạn lượt của địa chỉ gọi.
  echo "thân JSON 13 MB:  $( (printf '{"query": "'; head -c 13000000 /dev/zero | tr '\\0' 'a'; printf '"}') | curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' --data-binary @- $G/api/chat)   (mong 413 — trần của Caddy)"
  echo "nguồn 6335 sau lượt thử: $(curl -s $NGUON/collections/$COL/snapshots)   (mong \"result\":[])  ·  $(curl -s $NGUON/collections/$COL | grep -o '"points_count":[0-9]*')"
  dc ps --format '{{.Service}} {{.Status}}'
  docker stats --no-stream --format '{{.Name}} {{.MemUsage}}' $(dc ps -q)
  echo "Một lượt XẾP LỊCH thật (có phí; chỉ xếp lịch mới đọc các file bảng riêng tư trong ảnh) — mong HTTP 200, 0 câu dự phòng do thiếu file:"
  echo "  curl -s -X POST $G/api/chat -H 'Content-Type: application/json' -d '{\"query\": \"lên lịch\", \"bieu_mau\": true, \"truong\": {\"so_ngay\": \"2\", \"nguoi_lon\": 2, \"tre_em\": 0, \"lon_tuoi\": false}}' | head -c 1200"
  echo "Một câu THẬT qua model (có phí; trên đường openai đây là phép kiểm DUY NHẤT cho biết khoá dùng được — /health không gọi model). Mong: câu trả lời có nguồn, không phải 'Không thể tạo câu trả lời vào lúc này':"
  echo "  curl -s -N -X POST $G/api/chat/stream -H 'Content-Type: application/json' -d '{\"query\": \"Vé tham quan Đại Nội bao nhiêu?\"}' | tail -c 1500"
  ;;
don)
  [ -d "$THU" ] || { echo "không có gì để dọn"; exit 0; }
  dc down --remove-orphans
  # chỉ các volume mang nhãn của ĐÚNG dự án compose của lượt thử này (không `down -v`, không đụng volume của ai khác)
  docker volume ls -q --filter "label=com.docker.compose.project=$DU_AN" | xargs -r docker volume rm >/dev/null
  # thư mục Qdrant + log do hộp tạo thuộc root ⇒ xoá qua docker
  docker run --rm -v "$THU":/x --entrypoint bash qdrant/qdrant@sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286 -c 'rm -rf /x/qdrant_storage /x/logs'
  rm -rf "$THU"
  echo "hộp thử còn lại: $(docker ps -a --format '{{.Names}}' | grep -c "^$DU_AN" || true)   (mong 0)"
  ;;
*) echo "dùng: $0 len | kiem | don"; exit 2 ;;
esac
