#!/usr/bin/env bash
# Lấy chỉ mục ra MỘT file:  chup_chi_muc.sh <file ra>     (Qdrant nguồn: HUE_QDRANT_NGUON, mặc định http://127.0.0.1:6335 của máy chủ dự án)
# Tạo một bản chụp collection ⇒ tải về ⇒ XOÁ đúng bản chụp vừa tạo ở nguồn. Chỉ đọc chỉ mục: số điểm trước = sau, không để lại gì ở nguồn.
set -euo pipefail
RA=${1:?dùng: chup_chi_muc.sh <file ra>}
NGUON=${HUE_QDRANT_NGUON:-http://127.0.0.1:6335}
COL=${HUE_COLLECTION:-hue_full_corpus_7a2_e5_small_384}
diem() { curl -sf "$NGUON/collections/$COL" | grep -o '"points_count":[0-9]*' | cut -d: -f2; }
TRUOC=$(diem) || { echo "DỪNG: Qdrant nguồn $NGUON không trả lời" >&2; exit 1; }
TEN=$(curl -sf -X POST "$NGUON/collections/$COL/snapshots" | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['name'])")
trap 'curl -sf -X DELETE "$NGUON/collections/$COL/snapshots/$TEN" >/dev/null' EXIT   # tải lỗi giữa chừng cũng xoá bản chụp ở nguồn
curl -sf -o "$RA" "$NGUON/collections/$COL/snapshots/$TEN"
trap - EXIT; curl -sf -X DELETE "$NGUON/collections/$COL/snapshots/$TEN" >/dev/null
echo "bản chụp: $RA ($(du -h "$RA" | cut -f1)) · nguồn trước $TRUOC điểm, sau $(diem) điểm · bản chụp còn ở nguồn: $(curl -sf "$NGUON/collections/$COL/snapshots")"
