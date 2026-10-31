#!/usr/bin/env bash
# Hook PostToolUse (Write / Edit) — khung_fde v1: CẢNH BÁO (không chặn) khi chữ vừa ghi vào thư mục tài liệu có giờ ước dạng "14:3x".
# Vì sao: agent hay ghi giờ đoán cho việc đã qua ("15:4x") dù luật bảo lấy giờ từ `date`; sửa câu luật chưa đủ (hue_rag: sổ S57,
# W20, W30) ⇒ rào bằng máy. Chỉ xét chữ MỚI ghi (new_string / content), không xét cả file — file cũ còn mốc lịch sử.
# Cần: jq. Gỡ: xoá mục PostToolUse matcher "Write|Edit" trong .claude/settings.json.

# Theo khung_fde v1, đã chỉnh cho hue_rag (W37, User duyệt 15:51 31/10/2026): thêm `bao_cao_he_thong`, `docs` (lịch sử git: giờ ước
# có ở report_agent 209 · session_prompt 349 · bao_cao_he_thong 29 · docs 15 dòng); bỏ qua `*/archive/*` vì dời lịch sử chép nguyên giờ cũ.
# Lớp thêm cho Claude Code — hook git `.githooks/pre-commit` (W30) vẫn là rào chung cho mọi agent; mẫu giờ dùng CHUNG với hook đó.
# Giới hạn đã biết (review 31/10): so thư mục trên đường dẫn tuyệt đối, không neo `$CLAUDE_PROJECT_DIR` (file `…/docs/…` ngoài dự án
# cũng bị báo); xét mọi đuôi file; không xét MultiEdit (`edits[]`). Chỉ là cảnh báo ⇒ chấp nhận.
WATCH_DIRS="report_agent session_prompt bao_cao_he_thong docs"

input=$(cat)
file=$(echo "$input" | jq -r '.tool_input.file_path // ""')
case "$file" in */archive/*) exit 0 ;; esac

hit=0
for d in $WATCH_DIRS; do
  case "$file" in */"$d"/*) hit=1 ;; esac
done
[ "$hit" = 1 ] || exit 0

text=$(echo "$input" | jq -r '(.tool_input.new_string // "") + "\n" + (.tool_input.content // "")')
# Báo hay không: mẫu -E chung với pre-commit; in danh sách: -P lookaround để hai giờ sát nhau ("10:3x,11:4x") không mất giờ sau.
found=$(echo "$text" | grep -E '(^|[^0-9])[0-2][0-9]:[0-5]x($|[^0-9A-Za-z])' | grep -oP '(?<![0-9])[0-2][0-9]:[0-5]x(?![0-9A-Za-z])' | sort -u | tr '\n' ' ')
[ -z "$found" ] && exit 0

jq -n --arg f "$file" --arg g "$found" '{hookSpecificOutput: {hookEventName: "PostToolUse",
  additionalContext: ("Cảnh báo giờ ước: chữ vừa ghi vào " + $f + " có " + $g + "— giờ phải lấy từ `date`. Mốc đã qua không rõ giờ thì ghi khoảng có nguồn (vd \"giữa 15:52 và 15:56\") hoặc bỏ giờ. Nếu đây là trích dẫn sự cố cũ thì bỏ qua.")}}'
exit 0
