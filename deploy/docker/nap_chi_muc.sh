#!/usr/bin/env bash
# Nạp chỉ mục vào Qdrant của gói:  bash nap_chi_muc.sh <file phủ>     — chạy TRONG thư mục có compose.yml, hue.env, qdrant.snapshot (máy thử lẫn máy đích)
# Bật riêng hộp qdrant ⇒ chép bản chụp vào ⇒ khôi phục ⇒ so số điểm với bản ghi dựng nằm trong ảnh app; lệch thì dừng (app sẽ không trả lời được).
# Chạy lại được: khôi phục đè lên collection đang có.
set -euo pipefail
PHU=${1:?dùng: nap_chi_muc.sh <file phủ, vd compose.vai-may.yml>}
COL=${HUE_COLLECTION:-hue_full_corpus_7a2_e5_small_384}
dc() { docker compose --env-file hue.env -f compose.yml -f "$PHU" "$@"; }
dc up -d --wait qdrant
dc cp qdrant.snapshot qdrant:/qdrant/snapshots/qdrant.snapshot
# Ảnh Qdrant không có curl ⇒ gọi từ một hộp dùng một lần của ảnh app (cùng mạng compose). `priority: snapshot` bắt buộc khi collection còn trống.
dc run --rm --no-deps --entrypoint python app -c "
import json, sys, urllib.request as u
goc = 'http://qdrant:6333/collections/$COL'
r = u.Request(goc + '/snapshots/recover', method='PUT', headers={'Content-Type': 'application/json'},
              data=json.dumps({'location': 'file:///qdrant/snapshots/qdrant.snapshot', 'priority': 'snapshot'}).encode())
u.urlopen(r, timeout=300).read()
# đếm CHÍNH XÁC: `points_count` của thông tin collection là số xấp xỉ khi Qdrant đang tối ưu
dem = u.Request(goc + '/points/count', method='POST', headers={'Content-Type': 'application/json'}, data=json.dumps({'exact': True}).encode())
co = json.load(u.urlopen(dem, timeout=60))['result']['count']
mong = json.load(open('/app/data/full_corpus_builds/$COL.json'))['qdrant']['point_count']
print(f'chỉ mục trong Qdrant của gói: {co} điểm · bản ghi dựng trong ảnh: {mong} điểm')
sys.exit(0 if co == mong else 'DỪNG: số điểm lệch — bản chụp và ảnh không cùng một lần dựng chỉ mục')"
dc exec -T qdrant rm -f /qdrant/snapshots/qdrant.snapshot   # bản chép của bản chụp trong hộp Qdrant không còn cần (75 MB)
