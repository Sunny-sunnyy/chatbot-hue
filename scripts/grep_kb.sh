#!/usr/bin/env bash
# Tìm trong NỘI DUNG kho tri thức mà không lọt vào bộ đánh giá / câu kín / ghi chép meta.
# Vì sao: 25/10 và 27/10 grep -r thẳng vào knowledge-base-hue/ đọc lọt evaluation/ (câu kín, Golden Foods cũ) và meta/
# (sổ cải tiến W27, Session_Prompt.md §5 "giữ mù"). Brief sub-agent: tìm trong kho CHỈ qua script này.
# Dùng: scripts/grep_kb.sh [cờ grep…] <mẫu> [thư mục con của kho, mặc định cả kho]
#   ví dụ: scripts/grep_kb.sh -n "Phú Xuân" foods
set -euo pipefail
KB="$(cd "$(dirname "$0")/.." && pwd)/knowledge-base-hue"
args=("$@")
target="$KB"
if [ ${#args[@]} -ge 2 ] && [ -d "$KB/${args[-1]}" ]; then
  target="$KB/${args[-1]}"
  unset 'args[-1]'
fi
exec grep -r --exclude-dir=evaluation --exclude-dir=meta --exclude='*sealed*' "${args[@]}" "$target"
