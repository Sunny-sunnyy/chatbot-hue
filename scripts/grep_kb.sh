#!/usr/bin/env bash
# Tìm trong NỘI DUNG kho tri thức mà không lọt vào bộ đánh giá / câu kín / ghi chép meta / bản thô.
# Vì sao: 25/10 và 27/10 grep -r thẳng vào knowledge-base-hue/ đọc lọt evaluation/ (câu kín, Golden Foods cũ) và meta/
# (sổ cải tiến W27, Session_Prompt.md §5 "giữ mù"). Brief sub-agent: tìm trong kho CHỈ qua script này.
# Dùng: scripts/grep_kb.sh [--dir <thư mục con của kho>] [cờ grep, giá trị viết liền…] <mẫu>
#   ví dụ: scripts/grep_kb.sh --dir foods -n "Phú Xuân"
# Luôn quét trong kho (đích kiểm bằng realpath), loại evaluation/, meta/, _source-dumps/, *sealed*.
set -euo pipefail
KB="$(cd "$(dirname "$0")/.." && pwd)/knowledge-base-hue"
target="$KB"
if [ "${1:-}" = "--dir" ]; then
  [ $# -ge 2 ] || { echo "grep_kb: --dir cần tên thư mục con" >&2; exit 2; }
  target="$(realpath -e -- "$KB/$2")"
  case "$target/" in "$KB"/*) ;; *) echo "grep_kb: đích ngoài kho: $2" >&2; exit 2 ;; esac
  shift 2
fi
[ $# -ge 1 ] || { echo "grep_kb: thiếu mẫu tìm" >&2; exit 2; }
# Mẫu là tham số cuối; mọi tham số trước nó phải là cờ (bắt đầu bằng "-", giá trị viết liền: -A2, --max-count=5) — không nhận đường dẫn thừa.
for arg in "${@:1:$#-1}"; do
  case "$arg" in -*) ;; *) echo "grep_kb: chỉ nhận cờ trước mẫu (thư mục con: --dir): $arg" >&2; exit 2 ;; esac
done
exec grep -r --exclude-dir=evaluation --exclude-dir=meta --exclude-dir=_source-dumps --exclude='*sealed*' "$@" -- "$target"
