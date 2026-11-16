# Review spec deploy AWS bản 1 — vòng 1 (C, 14:42 16/11/2026)

Đối tượng: `docs/superpowers/specs/2026-11-16-deploy-aws-design.md` trên `origin/p12-deploy-aws-spec` `2900115`, sha256 đầu `caa023a1958e` (C tính lại, khớp).
Trọng tâm A giao: (1) mỗi bước có lệnh chạy được + kiểm + dừng khi, để agent yếu hơn làm theo được; (2) đường ra / khoá / dữ liệu private; (3) chi phí; (4) câu User quyết ở §3.
Cách kiểm: đọc hết spec; đối chiếu với `data/phase_12/deploy_nhap/{compose.yml,Caddyfile,Dockerfile}` và `backend/api/gioi_han.py`. Không chạy gì, không gọi AWS.

**Kết luận: `changes_requested` — 0 blocker · 3 major · 6 minor.** Phần nền vững: chọn một máy Lightsail có số đo kèm; ảnh không lên registry; khoá tách khỏi ảnh; `open-` thay vì `put-instance-public-ports`; `priority: snapshot`; app chạy `--proxy-headers` sau Caddy nên giới hạn lượt theo IP thật có tác dụng (`Dockerfile` CMD, `gioi_han.py:4`).

## Major

**M-1 — §10.5 xoá máy: bước phá huỷ mà chưa có kiểm / dừng.**
- Lệnh `create-instance-snapshot` rồi `delete-instance` liền nhau. Bản chụp chưa ở trạng thái `available` mà đã xoá máy ⇒ có thể mất cả máy lẫn bản chụp. §7.C4 cũng ghi "xoá máy là xoá luôn bản chụp tự động".
- Ba lệnh thiếu `--region` (trái luật §7 "mọi lệnh có `--region`"), và bước chưa có nhãn **[User]**.
- **Đóng khi:** bước có nhãn [User] và có `--region` ở mọi lệnh. Giữa hai lệnh có vòng chờ có trần, ví dụ `for i in $(seq 60); do s=$(aws lightsail get-instance-snapshot --region ap-southeast-1 --instance-snapshot-name hue-cuoi --query instanceSnapshot.state --output text); [ "$s" = available ] && break; sleep 20; done`. **Dừng khi** trạng thái chưa `available` sau vòng chờ. Sau khi xoá có lệnh kiểm `get-instances` không còn `hue-app`, và `get-static-ips` không còn `hue-ip`.

**M-2 — Nhiều bước chưa theo đúng khuôn 4 phần mà chính §0 đặt ra** (Lệnh · Kiểm · Mong đợi · Dừng khi). Agent yếu hơn gặp chỗ thiếu sẽ phải tự đoán, mà §0 lại cấm đoán.
- **A6:** thiếu Kiểm và Dừng khi. Nên thêm: `sha256sum -c SHA256SUMS` ra 2 dòng OK; thiếu file hoặc cỡ = 0 ⇒ dừng.
- **B3:** chỉ có Kiểm. Nên thêm: Dừng khi `get-caller-identity` ra tài khoản gốc (`:root`) hoặc sai tên.
- **C2:** thiếu Dừng khi. Nên thêm: file đã có sẵn ⇒ dừng (không ghi đè khoá cũ); `create-key-pair` báo tên đã tồn tại ⇒ dừng.
- **C4:** thiếu Kiểm. Nên thêm: `aws lightsail get-instance --region … --query 'instance.addOns'` có `AutoSnapshot` `Enabled`.
- **D1:** thiếu Dừng khi. Nên thêm: `apt` lỗi, hoặc `docker version` không in số ⇒ dừng.
- **D2:** thiếu Dừng khi. Nên thêm: `sha256sum -c` có dòng FAILED ⇒ dừng, chép lại file.
- **10.2 cập nhật:** không có Kiểm và không có điều kiện quay lại. Nên thêm: chạy lại §9; có dòng "không" ⇒ làm 10.3 ngay.
- **10.3 quay lại bản cũ:** thiếu Kiểm. Nên thêm: `docker compose … ps` cho thấy app chạy đúng `HUE_IMAGE` cũ.
- **Đóng khi:** mọi bước §5–§10 có đủ 4 phần, hoặc ghi rõ "không cần" kèm lý do.

**M-3 — §3 thiếu ba câu chỉ User được quyết.**
- **(a) Agent có được chạy `aws …` bằng access key của User không.** B3 ghi "nếu User cho", nhưng §3 không có câu hỏi. Đây là quyền tiêu tiền và tạo / xoá tài nguyên ra bên ngoài. Cần một câu: cho agent chạy cả §7–§10, chỉ chạy lệnh chỉ đọc, hay User tự gõ.
- **(b) Ngày tạo máy**, tức ngày bắt đầu tính tiền. Spec ghi "chạy khoảng 12/2026–02/2027", nhưng không hỏi User tạo máy khi nào. Trước đây User đã dặn không deploy sớm. Tạo sớm từ 30/11 ⇒ thêm khoảng 24 USD.
- **(c) Tổng tiền cả đợt** (để User chọn có hiểu). Q1 chỉ ghi giá theo tháng. Nên ghi tổng: máy 24 × 3 = 72 USD, sao lưu ~3, tên miền ~10–15 / năm (nếu Q2 = riêng), trần OpenAI 5 / tháng ⇒ ~**90–100 USD trong 3 tháng** (trước credit tài khoản mới). Kèm số credit 100 USD nếu là tài khoản mới.
- **Đóng khi:** §3 có thêm 3 dòng này. Mỗi dòng có mặc định, hệ quả, và "khi nào sai".

## Minor

- **m-1 (A5, A6):** lệnh `POST …/snapshots` tạo file bản chụp trong Qdrant 6335 **đang chạy của chatbot** nhưng không có bước xoá. Mỗi lần deploy để lại ~55 MB trong kho Qdrant chung. Nên thêm `curl -s -X DELETE "http://127.0.0.1:6335/collections/<COL>/snapshots/$SNAP"` sau khi tải về, và Kiểm `GET …/snapshots` không còn tên đó.
- **m-2 (A2):** đoạn kiểm duyệt **mọi** đường dẫn `../data/…` trong `settings.yaml`, kể cả của cờ đang tắt. Nhánh `p9-khoang-cach` (chờ review) thêm `khoang_cach_bang` với cờ tắt. Merge rồi thì A2 in `THIEU` cho một file app không đọc ⇒ người chạy dừng oan. Nên chỉ xét đường dẫn mà app đọc lúc khởi động với cờ đang bật, hoặc ghi rõ cách xử lý khi `THIEU` thuộc cờ đang tắt.
- **m-3 (D3):** lệnh dùng chỗ giữ `<TAG>`, trong khi A3–A6 dùng biến shell `$TAG`. Trên máy AWS không có `$TAG` ⇒ agent gõ `$TAG` sẽ ra `app_.tar.gz`. Nên đặt `TAG=<7 ký tự>` ở dòng đầu D3 và dùng `$TAG` thống nhất.
- **m-4 (C3):** vòng `until … running` không có trần ⇒ treo mãi nếu máy không lên. Nên đặt trần (ví dụ 60 × 10 s), quá trần thì dừng.
- **m-5 (§9):** §11 ghi "rào đo hai chiều — §9 làm lại trên máy thật", nhưng bảng §9 không có dòng thử 429 (hết lượt). Nên thêm một dòng: tạm đặt `HUE_LUOT_MOI_NGAY=3` rồi `up -d app`, hỏi 4 câu, câu 4 phải bị chặn, rồi trả về 50. Nếu Q6 = bật thì thêm một dòng thử gửi ảnh qua https: route ảnh so Origin với scheme (`anh.py:78`), chỉ đúng khi qua https.
- **m-6 (giữ file):** Dockerfile, compose, Caddyfile, `dung_dockerignore.py` chỉ nằm trong `data/` (private, không có Git; đang sao lưu tay `sao_luu_2026-11-15*`). Agent từ tháng 12 chạy theo spec thì đây là điểm hỏng duy nhất. Nên ghi trong §0 nơi có bản sao lưu và cách kiểm (md5). Đưa các file không bí mật vào repo hay không là việc của A / User quyết.

## Đã đối chiếu, không có finding
- Khoá: `.env.deploy` quyền 600, kiểm chỉ in tên biến, khoá không vào ảnh (`**/.env` trong dockerignore, A4 kiểm lại). Sổ vết tắt, log không có nội dung.
- Đường ra: OpenAI, Serper (Q4, mặc định tắt), Open-Meteo. Bảng §11 khớp với code đã đọc.
- Cổng: app không có `ports` (`compose.yml`), chỉ Caddy mở 80 / 443; 22 mở, rào chính là khoá SSH (ghi rõ [Suy]).
- Chi phí theo tháng: 24 USD (E tự mở trang giá 16/11); cảnh báo ngân sách 30 USD, đã ghi rõ không phải trần cứng.
