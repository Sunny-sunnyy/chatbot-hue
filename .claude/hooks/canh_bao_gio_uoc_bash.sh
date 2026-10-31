#!/usr/bin/env bash
# Hook PostToolUse (Bash) — khung_fde v1: CẢNH BÁO (không chặn) khi một lệnh Bash vừa ghi giờ ước dạng "14:3x" vào file .md của thư mục
# tài liệu. Vì sao: hook Write / Edit không thấy chữ ghi bằng sed / python / heredoc (bài học từ một dự án khác của User). Xét file .md đổi trong 2 phút:
# dòng thêm so với git (file đã theo dõi) hoặc cả file (file mới); nhớ chỗ đã báo trong /tmp để không báo lại.
# Giới hạn đã biết: sửa lại một dòng cũ có trích giờ lịch sử ⇒ báo nhầm (chấp nhận — chỉ là cảnh báo).
# Cần: jq, git. Gỡ: xoá mục PostToolUse matcher "Bash" trong .claude/settings.json.

# Theo khung_fde v1, đã chỉnh cho hue_rag (W37, User duyệt 15:51 31/10/2026): thêm `bao_cao_he_thong`, `docs`; bỏ qua `*/archive/*`.
# Giới hạn thêm ở hue_rag: A / B / C dùng chung working tree ⇒ có thể báo cả file session khác vừa ghi trong 2 phút (chỉ cảnh báo);
# chỉ xét `.md`; lệnh vừa sửa vừa `git add` ⇒ không thấy (so với index); dòng mới bắt đầu bằng `+` bị bỏ qua — hook git W30 bắt lúc commit.
WATCH_DIRS=(report_agent session_prompt bao_cao_he_thong docs)

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$root" 2>/dev/null || exit 0
pat='(^|[^0-9])[0-2][0-9]:[0-5]x($|[^0-9A-Za-z])'   # chung với .githooks/pre-commit (W30)
seen="/tmp/claude_gio_uoc_bash_$(id -u)_$(basename "$root").seen"
touch "$seen"

hits=$(find "${WATCH_DIRS[@]}" -name '*.md' -not -path '*/archive/*' -mmin -2 2>/dev/null | while IFS= read -r f; do
  if git ls-files --error-unmatch -- "$f" >/dev/null 2>&1; then
    git diff -U0 -- "$f" 2>/dev/null | awk -v f="$f" '/^\+[^+]/{print f "\t" substr($0,2)}'
  else
    awk -v f="$f" '{print f "\t" $0}' "$f"
  fi
done | grep -E "$pat")
[ -z "$hits" ] && exit 0

new=""
while IFS= read -r line; do
  key=$(printf '%s' "$line" | md5sum | cut -c1-16)
  grep -q "$key" "$seen" && continue
  echo "$key" >> "$seen"
  f=${line%%$'\t'*}; g=$(printf '%s' "${line#*$'\t'}" | grep -oP '(?<![0-9])[0-2][0-9]:[0-5]x(?![0-9A-Za-z])' | sort -u | tr '\n' ' ')
  new="$new$f: $g; "
done <<< "$hits"
[ -z "$new" ] && exit 0

jq -n --arg g "$new" '{hookSpecificOutput: {hookEventName: "PostToolUse",
  additionalContext: ("Cảnh báo giờ ước (ghi qua Bash): " + $g + "— giờ phải lấy từ `date`. Mốc đã qua không rõ giờ thì ghi khoảng có nguồn hoặc bỏ giờ. Nếu là trích dẫn sự cố cũ thì bỏ qua.")}}'
exit 0
