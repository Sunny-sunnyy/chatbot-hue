#!/usr/bin/env bash
# Mở một ngày làm việc + kiểm "trí nhớ" của dự án. Cách làm việc theo thư mục từng ngày (User giao 19/11/2026, đang thử) — khối đầu
# `session_prompt/CURRENT_HANDOFF.md`. KHÔNG phải hook: người / agent tự chạy; không sửa file nào đang có.
#
#   scripts/mo_ngay.sh         — tạo (nếu chưa có) `report_agent/<hôm nay>/TONG_HOP.md` (khung) và `data/loi_user/<hôm nay>.md` (riêng tư; chỉ khi
#                                cây này có `data/`), rồi IN: khối "PHIÊN SAU ĐỌC TRƯỚC" của TONG_HOP gần nhất · `session_prompt/VIEC_DANG_MO.md` ·
#                                trạng thái máy thật · cỡ + ngày của từng `STATUS_<X>.md` (khuôn ghi đè ≤ 15 dòng / 4 KB). Tên thư mục ngày lấy bằng `date +%F`, không gõ tay.
#   scripts/mo_ngay.sh kiem    — CHỈ ĐỌC: mọi đường dẫn và tên nhánh nêu trong `HIEN_TRANG.md`, `VIEC_DANG_MO.md` và MỤC ĐẦU các `STATUS_<X>.md` phải
#                                tồn tại (nhánh: có trên origin hoặc đã gộp vào origin/main); `HIEN_TRANG.md` ≤ 14.000 byte; `VIEC_DANG_MO.md` ≤ 60 dòng.
#                                Thoát 1 khi có chỗ lệch (để ghép `scripts/mo_ngay.sh kiem && …`), 0 khi sạch.
#
# `kiem` KHÔNG thấy: số, tên hàm, lệnh, mẫu có < > * … $ { }, URL, đường dẫn ngoài repo, tên file trần không có "/", và chuỗi mà thư mục đầu không có
# ở gốc repo (gõ sai ngay tên thư mục đầu thì lọt). Thư mục riêng tư (`data/`, kho, `gửi chatgpt/`) vắng ở cây này ⇒ đếm "bỏ qua", không báo thiếu.
set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "mo_ngay: không ở trong repo git" >&2; exit 2; }
cd "$root" || exit 2
SP=session_prompt
hom_nay=$(date +%F)

muc_dau() {  # mục đầu của một STATUS: từ đầu file tới trước tiêu đề cấp 1 THỨ HAI (phần "(cũ)" nằm dưới đó)
  awk '/^# /{n++} n>=2{exit} {print}' "$1"
}

kiem_duong_dan() {  # $1 = nhãn file · stdin = nội dung cần quét ⇒ in chỗ thiếu; cộng vào thieu / rieng
  local nhan=$1 n s p dau
  while IFS= read -r dong; do
    n=${dong%%:*}; s=${dong#*:}; s=${s#\`}; s=${s%\`}
    [[ $s == *" "* || $s != */* ]] && continue
    p=${s%%[#:]*}; p=${p%[.,;]}; p=${p#./}; p=${p%/}
    case "$p" in ""|*'<'*|*'>'*|*'*'*|*'…'*|*'$'*|*'{'*|*'://'*|*.env*|'~'*|origin/*) continue ;; esac
    case "$p" in "$root"/*) p=${p#"$root"/} ;; /*) continue ;; esac
    dau=${p%%/*}
    case "$dau" in data|knowledge-base-hue|"gửi chatgpt") [ -e "$dau" ] || { rieng=$((rieng + 1)); continue; } ;; esac
    case "$p" in frontend/dist|frontend/dist/*|frontend/node_modules*) [ -e "$p" ] || { rieng=$((rieng + 1)); continue; } ;; esac  # bản dựng, không vào git
    [ -e "$dau" ] || [ -e "$SP/$dau" ] || continue          # thư mục đầu không có ở gốc repo / session_prompt ⇒ không phải đường dẫn của repo
    [ -e "$p" ] || [ -e "$SP/$p" ] || [ -e "$SP/sessions/$p" ] && continue
    echo "  THIẾU $nhan:$n: \`$s\`"
    thieu=$((thieu + 1))
  done < <(grep -n -o '`[^`]*`')
}

kiem_nhanh() {  # $1 = nhãn file · stdin = nội dung ⇒ tên nhánh dạng p<số>-… trong dấu ` phải có trên origin hoặc đã gộp vào origin/main
  local nhan=$1 b
  while IFS= read -r b; do
    b=${b#\`}; b=${b%\`}; b=${b#origin/}
    git rev-parse -q --verify "refs/remotes/origin/$b" >/dev/null && continue
    git rev-parse -q --verify "refs/heads/$b" >/dev/null && continue
    [ -n "$(git log origin/main -1 --format=%h --grep="merge $b" 2>/dev/null)" ] && continue
    echo "  NHÁNH KHÔNG THẤY $nhan: \`$b\` (không có trên origin, không có ở máy, không thấy commit gộp trên origin/main)"
    thieu=$((thieu + 1))
  done < <(grep -o '`\(origin/\)\?p[0-9]\+[a-z]*-[a-z0-9-]\+`' | sort -u)
}

lenh_kiem() {
  thieu=0; rieng=0
  local f co
  for f in "$SP/HIEN_TRANG.md" "$SP/VIEC_DANG_MO.md"; do
    [ -f "$f" ] || { echo "  THIẾU FILE: $f"; thieu=$((thieu + 1)); continue; }
    kiem_duong_dan "$f" < "$f"; kiem_nhanh "$f" < "$f"
  done
  for f in "$SP"/sessions/STATUS_*.md; do
    [ -f "$f" ] || continue
    kiem_duong_dan "$f (mục đầu)" < <(muc_dau "$f"); kiem_nhanh "$f (mục đầu)" < <(muc_dau "$f")  # không dùng ống: vòng lặp trong ống mất bộ đếm
  done
  if [ -f "$SP/HIEN_TRANG.md" ]; then
    co=$(wc -c < "$SP/HIEN_TRANG.md"); [ "$co" -le 14000 ] || { echo "  QUÁ CỠ: $SP/HIEN_TRANG.md $co byte (> 14.000)"; thieu=$((thieu + 1)); }
  fi
  if [ -f "$SP/VIEC_DANG_MO.md" ]; then
    co=$(wc -l < "$SP/VIEC_DANG_MO.md"); [ "$co" -le 60 ] || { echo "  QUÁ DÀI: $SP/VIEC_DANG_MO.md $co dòng (> 60)"; thieu=$((thieu + 1)); }
  fi
  echo "— kiểm trí nhớ: $thieu chỗ lệch · bỏ qua $rieng đường dẫn riêng tư / bản dựng không có ở cây này"
  [ "$thieu" -eq 0 ]
}

if [ "${1:-}" = "kiem" ]; then lenh_kiem; exit $?; fi
[ $# -eq 0 ] || { echo "Dùng: scripts/mo_ngay.sh [kiem]" >&2; exit 2; }

# ---------- 1. thư mục ngày + khung ----------
thu=(x "thứ Hai" "thứ Ba" "thứ Tư" "thứ Năm" "thứ Sáu" "thứ Bảy" "Chủ nhật")
ngay_vn=$(date +%d/%m/%Y); ten_thu=${thu[$(date +%u)]}
D="report_agent/$hom_nay"
mkdir -p "$D"
if [ ! -e "$D/TONG_HOP.md" ]; then
  cat > "$D/TONG_HOP.md" <<EOF
# Tổng hợp ngày $ngay_vn ($ten_thu)

Người giữ: phiên điều phối. Report của từng phiên nằm cùng thư mục (tiền tố \`b_\` / \`c_\` / \`e_\`). Lời User nguyên văn: \`data/loi_user/$hom_nay.md\` (riêng tư).

## PHIÊN SAU ĐỌC TRƯỚC (GHI ĐÈ lúc kết phiên; ≤ ~60 dòng)

(chưa viết)

## 1. Việc trong ngày và kết quả

## 2. Quyết định của chủ dự án trong ngày (đủ ở \`session_prompt/HIEN_TRANG.md\` mục 4)

## 3. Đang mở khi viết file này (nguồn duy nhất: \`session_prompt/VIEC_DANG_MO.md\`)

## 4. Tiền API trong ngày (số từng phiên báo)
EOF
  echo "ĐÃ TẠO $D/TONG_HOP.md (khung)"
else
  echo "đã có $D/TONG_HOP.md — không đụng"
fi
if [ -d data ]; then
  mkdir -p data/loi_user
  [ -e "data/loi_user/$hom_nay.md" ] || { printf '# Lời User ngày %s — NGUYÊN VĂN + lựa chọn ở từng hộp hỏi (riêng tư, không commit)\n\n' "$ngay_vn" > "data/loi_user/$hom_nay.md"; echo "ĐÃ TẠO data/loi_user/$hom_nay.md"; }
else
  echo "cây này không có data/ ⇒ không tạo file lời User (chạy ở cây chính)"
fi

# ---------- 2. khối phiên sau của TONG_HOP gần nhất ----------
echo; echo "===== PHIÊN SAU ĐỌC TRƯỚC — TONG_HOP gần nhất có khối này ====="
co_khoi=0
for f in $(ls -d report_agent/20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]/TONG_HOP.md 2>/dev/null | sort -r); do
  khoi=$(awk '/^## PHIÊN SAU ĐỌC TRƯỚC/{in_k=1; print; next} in_k && /^## /{exit} in_k{print}' "$f")
  if [ -n "$khoi" ] && ! grep -q '^(chưa viết)$' <<<"$khoi"; then echo "($f)"; echo "$khoi"; co_khoi=1; break; fi
done
[ "$co_khoi" -eq 1 ] || echo "(chưa TONG_HOP nào có khối \"PHIÊN SAU ĐỌC TRƯỚC\" đã viết — đọc khối đầu $SP/CURRENT_HANDOFF.md)"

# ---------- 3. việc đang mở ----------
echo; echo "===== VIỆC ĐANG MỞ ($SP/VIEC_DANG_MO.md) ====="
[ -f "$SP/VIEC_DANG_MO.md" ] && cat "$SP/VIEC_DANG_MO.md" || echo "(chưa có file)"

# ---------- 4. trạng thái máy thật ----------
echo; echo "===== TRẠNG THÁI MÁY THẬT ($(date '+%H:%M %d/%m/%Y')) ====="
echo "nhánh: $(git branch --show-current) · HEAD $(git rev-parse --short HEAD) · origin/main $(git rev-parse --short origin/main 2>/dev/null || echo '?') (chưa fetch)"
git log --oneline -3 | cut -c1-110
echo "file theo dõi đang sửa: $(git status --short | grep -vc '^??')"
echo "hooksPath: $(git config --get core.hooksPath || echo 'CHƯA ĐẶT — chạy: git config core.hooksPath .githooks')"
diem=$(curl -s -m 3 http://127.0.0.1:6335/collections/hue_full_corpus_7a2_e5_small_384 2>/dev/null | grep -o '"points_count":[0-9]*')
echo "Qdrant 6335: ${diem:-KHÔNG TRẢ LỜI (đang tắt? docker compose up -d qdrant — báo phiên điều phối trước)}"
free -m | awk 'NR==2{printf "RAM: khả dụng %d MB / %d MB%s\n", $7, $2, ($7 < 4000 ? "  ⇐ DƯỚI 4 GB: không bật việc nặng" : "")}'
cong=$(ss -ltn 2>/dev/null | grep -oE ':(80[0-9][0-9]|88[0-9][0-9])\b' | sort -u | tr '\n' ' ')
echo "cổng server đang nghe (80xx / 88xx): ${cong:-không có}"
echo "worktree:"; git worktree list | sed 's/^/  /'

# ---------- 5. sổ từng phiên ----------
# Khuôn GHI ĐÈ (chốt 19/11 sau ca thử đầu): cả file là MỘT khối ≤ 15 dòng / 4 KB; phần cũ dời nguyên văn sang session_prompt/archive/.
echo; echo "===== SỔ TỪNG PHIÊN — khối ghi đè: ≤ 15 dòng / 4 KB ====="
ngay_ngan=$(date +%d/%m)
for f in "$SP"/sessions/STATUS_*.md; do
  [ -f "$f" ] || continue
  co=$(wc -c < "$f"); dong=$(wc -l < "$f"); ngay=$(muc_dau "$f" | head -4 | grep -oE '[0-9]{1,2}/[0-9]{1,2}(/20[0-9]{2})?' | head -1)
  canh=""
  [ "${ngay%/20*}" = "$ngay_ngan" ] || canh="$canh  ⇐ ghi ngày ${ngay:-?}, hôm nay $ngay_ngan: ghi đè khi nhận việc"
  { [ "$dong" -le 15 ] && [ "$co" -le 4096 ]; } || canh="$canh  ⇐ vượt 15 dòng / 4 KB: ghi đè theo khuôn, dời phần cũ sang archive/"
  echo "$(basename "$f"): $dong dòng · $co byte · ngày ${ngay:-?}$canh"
done
cat <<'KHUON'
Khuôn sổ phiên (ghi đè cả file; tiền: trỏ nhật ký ngày `report_agent/<ngày>/<vai>_nhat_ky.md`):
  1. đang dở + sha / nhánh / worktree   2. đã soạn / đã review CHƯA gộp (file ở đâu)   3. việc kế + "xong khi" + lệnh (hoặc trỏ nhật ký ngày)
  4. ai chờ mình ↔ mình chờ ai          5. câu treo cho phiên điều phối / User          6. thứ đang chạy / rác          7. bẫy phiên này
KHUON
echo; echo "Kiểm đường dẫn + nhánh + cỡ: scripts/mo_ngay.sh kiem"
