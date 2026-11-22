#!/usr/bin/env bash
# Bật hệ thống hue_rag ở máy local bằng MỘT lệnh: Qdrant ⇒ chỉ mục đủ điểm ⇒ khoá model ⇒ server cổng 8010 ⇒ in "SẴN SÀNG" hoặc ĐÚNG MỘT dòng
# "thiếu gì ⇒ làm gì". Thay cho các bước gõ tay ở `guides/RUNBOOK_BAN_GIAO.md` mục 1–2 (các bước đó vẫn đúng).
#
# Vì sao có (thử thật 12:07–12:16 22/11/2026): bật server khi Qdrant chưa bật thì server VẪN lên, mọi câu ra "Hệ thống tra cứu tạm thời không khả
# dụng." và bật Qdrant sau đó cũng KHÔNG tự hết — phải khởi động lại server; thiếu biến trỏ file khoá model thì mọi câu ra "Không thể tạo câu trả
# lời vào lúc này." mà màn hình không nói vì sao; máy mở lại là Qdrant tắt.
#
# Dùng (từ đâu cũng được):   HUE_BEDROCK_CREDS_FILE=<đường dẫn file khoá Bedrock> scripts/bat_he_thong.sh
#   - Ctrl+C ở cửa sổ này để tắt server; Qdrant để nguyên. Log server: /tmp/hue_rag_server_8010.log
#   - Model viết là `openai` (dòng `provider` của `backend/config/settings.yaml`) thì không cần biến file khoá.
#   - Lệnh KHÔNG đọc nội dung `.env` hay file khoá — chỉ xem file có tồn tại.
# `HUE_RAG_GOC=<gốc cây chính>`: chỉ để thử script này từ một cây khác (worktree không có `data/`, `.env`).
set -uo pipefail
GOC=${HUE_RAG_GOC:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
CONG=8010
QDRANT=http://127.0.0.1:6335
BAN_GHI=data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json   # bản ghi dựng chỉ mục: tên collection + số điểm phải có
LOG=/tmp/hue_rag_server_$CONG.log

dung() { echo "CHƯA BẬT ĐƯỢC — $1" >&2; exit 1; }

cd "$GOC" 2>/dev/null || dung "không vào được thư mục dự án $GOC"
[ -f .env ] || dung "thiếu file .env ở gốc dự án ⇒ đặt lại file .env (khoá các dịch vụ) rồi chạy lại"
[ -f frontend/dist/index.html ] || dung "giao diện chưa được dựng ⇒ chạy: cd $GOC/frontend && npm ci && npm run build, rồi chạy lại"
[ -f "$BAN_GHI" ] || dung "thiếu bản ghi dựng chỉ mục $BAN_GHI ⇒ chỉ mục chưa được dựng trên máy này (sổ tay bàn giao mục 5)"

# 1. Khoá model — kiểm TRƯỚC khi bật gì, để lỗi này không lẫn với lỗi khác
if [ "$(grep -m1 -E '^  provider:' backend/config/settings.yaml | awk '{print $2}')" = bedrock ]; then
  [ -n "${HUE_BEDROCK_CREDS_FILE:-}" ] || dung "thiếu biến HUE_BEDROCK_CREDS_FILE ⇒ chạy lại kèm biến: HUE_BEDROCK_CREDS_FILE=<đường dẫn file khoá Bedrock> scripts/bat_he_thong.sh (guides/DOI_MODEL_VIET.md mục 3)"
  [ -f "$HUE_BEDROCK_CREDS_FILE" ] || dung "biến HUE_BEDROCK_CREDS_FILE trỏ tới một file không tồn tại ⇒ sửa lại đường dẫn rồi chạy lại"
fi

# 2. Qdrant: bật, rồi chờ tới khi số điểm bằng số bản ghi dựng ghi (tối đa 30 giây)
command -v docker >/dev/null || dung "không có lệnh docker ⇒ bật Docker Desktop trên Windows rồi chạy lại"
docker compose up -d qdrant >/dev/null 2>&1 || dung "docker không bật được Qdrant ⇒ bật Docker Desktop trên Windows (chờ nó chạy xong) rồi chạy lại"
read -r TEN MONG < <(uv run python -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['collection_name'], d['qdrant']['point_count'])" "$BAN_GHI") \
  || dung "không đọc được bản ghi dựng chỉ mục $BAN_GHI"
CO=
for _ in $(seq 1 30); do
  CO=$(curl -s -m 2 "$QDRANT/collections/$TEN" | grep -o '"points_count":[0-9]*' | cut -d: -f2)
  [ "$CO" = "$MONG" ] && break
  sleep 1
done
[ -n "$CO" ] || dung "Qdrant không trả lời ở cổng 6335 sau 30 giây ⇒ xem: docker compose logs --tail 20 qdrant"
[ "$CO" = "$MONG" ] || dung "chỉ mục có $CO điểm, bản ghi dựng ghi $MONG ⇒ chỉ mục lệch kho: làm theo sổ tay bàn giao mục 5b"

# 3. Server. Cổng đã có server: nó ổn thì dùng luôn, không ổn thì phải tắt nó trước (server bật lúc Qdrant tắt KHÔNG tự hồi)
if H=$(curl -s -m 3 "http://127.0.0.1:$CONG/health"); then
  case "$H" in
    *'"status":"ok"'*) echo "SẴN SÀNG (server đã chạy sẵn) — mở http://127.0.0.1:$CONG"; exit 0 ;;
    *) dung "cổng $CONG đang có một server chạy nhưng nó báo chưa sẵn sàng ⇒ tắt server đó (Ctrl+C ở cửa sổ của nó) rồi chạy lại lệnh này" ;;
  esac
fi
( cd backend && HF_HUB_OFFLINE=1 exec uv run --env-file "$GOC/.env" uvicorn api.app:app --port "$CONG" ) >"$LOG" 2>&1 &
PID=$!
tat() { pkill -INT -P "$PID" 2>/dev/null; kill -INT "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; }
trap 'tat; echo; echo "Đã tắt server. Qdrant vẫn chạy (tắt: docker compose stop qdrant)."; exit 0' INT TERM
H=
for _ in $(seq 1 90); do
  kill -0 "$PID" 2>/dev/null || dung "server tự thoát lúc khởi động ⇒ xem: tail -20 $LOG"
  H=$(curl -s -m 2 "http://127.0.0.1:$CONG/health") && break
  sleep 1
done
case "$H" in
  *'"status":"ok"'*) echo "SẴN SÀNG — mở http://127.0.0.1:$CONG   (Ctrl+C ở cửa sổ này để tắt server · log: $LOG)" ;;
  "") tat; dung "server không trả lời sau 90 giây ⇒ xem: tail -20 $LOG" ;;
  *) tat; dung "server lên nhưng chưa sẵn sàng ($(echo "$H" | grep -o '"[a-z]*":"not_ready"' | tr -d '"' | tr '\n' ' ')) ⇒ xem: tail -20 $LOG" ;;
esac
wait "$PID"
