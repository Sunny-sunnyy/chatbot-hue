#!/usr/bin/env bash
# Thử 2 hook giờ ước (bản hue_rag, theo khung_fde v1) bằng ca dương (phải bắt) + ca thường gần giống (không được bắt) — chạy: bash .claude/hooks/thu_hook.sh
# Chạy lại sau mỗi lần sửa hook hoặc đổi WATCH_DIRS. Cần: jq, git.
cd "$(dirname "$0")" || exit 1
pass=0; fail=0
check() {  # check <tên ca> <muốn: bắt|qua> <đầu ra hook>
  local got=qua; [ -n "$3" ] && got=bắt
  if [ "$got" = "$2" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "SAI: $1 — muốn $2, ra $got"; fi
}

# hue_rag (W37): không áp chan_python_c_container.sh (Docker chỉ chạy Qdrant) ⇒ bỏ 6 ca của nó; thêm ca `docs/` + `archive/`.

# --- canh_bao_gio_uoc.sh (PostToolUse Write / Edit) — dùng thư mục đầu tiên của WATCH_DIRS
d=$(sed -n 's/^WATCH_DIRS="\([^ "]*\).*/\1/p' canh_bao_gio_uoc.sh)
gw() { jq -n --arg f "$1" --arg s "$2" '{tool_input: {file_path: $f, new_string: $s}}' | bash canh_bao_gio_uoc.sh; }
check "giờ ước trong thư mục theo dõi"    bắt "$(gw "/repo/$d/a.md" 'xong lúc 15:4x')"
check "giờ thật trong thư mục theo dõi"   qua "$(gw "/repo/$d/a.md" 'xong lúc 15:42')"
check "giờ ước ngoài thư mục theo dõi"    qua "$(gw "/repo/src/a.py" 'x = "15:4x"')"
check "giờ ước trong docs/ (spec)"        bắt "$(gw "/repo/docs/superpowers/specs/a.md" 'duyệt 10:3x')"
check "giờ ước khi dời lịch sử archive/"  qua "$(gw "/repo/session_prompt/archive/a.md" 'cũ 16:3x')"
check "giờ ước trong chữ nghiêng _…_"      bắt "$(gw "/repo/$d/a.md" 'xong _15:4x_')"
check "giờ ước dính chữ (lúc15:4x)"        bắt "$(gw "/repo/$d/a.md" 'xong lúc15:4x')"
check "không phải giờ (v1:2x, 112:3x)"      qua "$(gw "/repo/$d/a.md" 'v1:2x 112:3x 12:3xy')"

# --- canh_bao_gio_uoc_bash.sh (PostToolUse Bash) — repo git tạm
t=$(mktemp -d); d2=$(sed -n 's/^WATCH_DIRS=(\([^ )]*\).*/\1/p' canh_bao_gio_uoc_bash.sh)
( cd "$t" && git init -q && mkdir -p "$d2" && printf 'cũ 10:1x\n' > "$d2/cu.md" && git add . && git -c user.email=t@t -c user.name=t commit -qm init )
gb() { CLAUDE_PROJECT_DIR="$t" bash canh_bao_gio_uoc_bash.sh < /dev/null; }
printf 'cũ 10:1x\nmới 11:00\n' > "$t/$d2/cu.md";  check "dòng mới giờ thật, dòng cũ có giờ ước" qua "$(gb)"
printf 'mới 16:2x\n' > "$t/$d2/moi.md";          check "file mới có giờ ước"                  bắt "$(gb)"
check "báo lại lần hai cùng chỗ"                  qua "$(gb)"
mkdir -p "$t/$d2/archive"; printf 'cũ 09:5x\n' > "$t/$d2/archive/ls.md"; check "file mới trong archive/"  qua "$(gb)"
rm -rf "$t" "/tmp/claude_gio_uoc_bash_$(id -u)_$(basename "$t").seen"

echo "ĐÚNG $pass / $((pass+fail))"
[ "$fail" = 0 ]
