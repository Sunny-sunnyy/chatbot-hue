#!/usr/bin/env bash
# W49 (User cho thử 03/11/2026): in các giờ "HH:MM DD/MM/YYYY" của HÔM NAY mà muộn hơn giờ hiện tại > 1 phút — giờ ở tương lai
# chắc chắn là gõ tay, không lấy bằng `date`. Vì sao: hook W30 / W37 chỉ bắt dạng "14:3x"; giờ gõ tay đủ phút vẫn lọt (sổ S63, S80 —
# 03/11: A ghi "09:24" khi `date` 09:19, "09:39" khi `date` 09:31; cả hai đều ở tương lai). Không bắt được giờ gõ tay sớm hơn thật.
# Dùng: <chữ> | bash .githooks/gio_tuong_lai.sh  ⇒ in danh sách giờ (cách nhau dấu cách), rỗng nếu không có. Gọi từ pre-commit + 2 hook Claude Code.
today=$(date +%d/%m/%Y)
now=$(( 10#$(date +%H) * 60 + 10#$(date +%M) ))
grep -oP "(?<![0-9])[0-2][0-9]:[0-5][0-9](?= ${today//\//\\/}(?![0-9]))" | sort -u | while IFS=: read -r h m; do
  [ $(( 10#$h * 60 + 10#$m )) -gt $(( now + 1 )) ] && printf '%s:%s ' "$h" "$m"
done
exit 0
