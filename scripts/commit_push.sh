#!/usr/bin/env bash
# Commit đúng các file truyền vào, push nhánh hiện tại, rồi in sha ĐỌC TỪ origin (git ls-remote).
# Vì sao: 15/11 ba lần một session báo "đã push" trong khi hook pre-commit đã chặn commit (sổ cải tiến W81).
# Từ nay báo sha / "đã push" chỉ bằng dòng "ĐÃ PUSH …" script này in ra (WORKFLOW.md §5).
# Dùng: scripts/commit_push.sh "<lời commit>" <file> [<file> …]      (chạy trong cây làm việc của nhánh cần push)
#   - chỉ nhận file (không thư mục, không -A); file đã xoá vẫn truyền được nếu git đang theo dõi nó;
#   - đang có thứ khác nằm sẵn trong vùng stage ⇒ dừng (không thì commit dính file ngoài danh sách);
#   - commit bị hook chặn / không có gì đổi / push lỗi / sha origin khác sha máy ⇒ in "CHƯA PUSH …" và thoát 1.
set -uo pipefail
chua() { echo "CHƯA PUSH — $1" >&2; exit 1; }

[ $# -ge 2 ] || { echo 'Dùng: scripts/commit_push.sh "<lời commit>" <file> [<file> …]' >&2; exit 2; }
msg=$1; shift
[ -n "$msg" ] || chua "lời commit rỗng"
branch=$(git symbolic-ref --quiet --short HEAD) || chua "không ở trên nhánh nào (HEAD tách rời)"
git diff --cached --quiet || chua "vùng stage đang có sẵn thay đổi khác (xem: git diff --cached --stat); gỡ ra rồi chạy lại"
for f in "$@"; do
  [ -d "$f" ] && chua "'$f' là thư mục — truyền từng file"
  [ -e "$f" ] || git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || chua "không thấy file '$f'"
done

# Cách làm theo thư mục từng ngày (19/11/2026): report mới viết vào thư mục HÔM NAY; cập nhật ngày sau = file mới ⇒ CẢNH BÁO (không chặn) khi
# file thuộc `report_agent/<ngày>/` của một ngày khác hôm nay (bẫy hay gặp: ghi nhầm thư mục hôm qua).
hom_nay=$(date +%F)
for f in "$@"; do
  case "$f" in report_agent/20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]/*)
    d=${f#report_agent/}; d=${d%%/*}
    [ "$d" = "$hom_nay" ] || echo "CẢNH BÁO — '$f' nằm ở thư mục ngày $d, hôm nay là $hom_nay (không chặn; report mới thuộc thư mục hôm nay)" >&2 ;;
  esac
done

git add -- "$@" || chua "git add lỗi"
git diff --cached --stat
if ! git commit -m "$msg"; then
  git reset -q -- "$@"   # trả vùng stage về như trước; file trong cây làm việc giữ nguyên
  chua "commit không thành (hook chặn hoặc không có gì đổi); chưa có commit nào được tạo"
fi
may=$(git rev-parse HEAD)
git push origin "$branch" || chua "đã commit ${may:0:7} trên máy nhưng push lỗi"
xa=$(git ls-remote origin "refs/heads/$branch" | cut -f1)
[ "$xa" = "$may" ] || chua "origin/$branch đang ở '${xa:0:7}', máy ở ${may:0:7}"
echo "ĐÃ PUSH ${xa:0:7} origin/$branch"
