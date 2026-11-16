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

## Vòng 2 (C, 14:50 16/11/2026 `date`) — bản 2 `origin/p12-deploy-aws-spec` `7634117`, sha256 đầu `fa5b42fdcb96` (C tính lại, khớp)

**Kết luận: `ready_for_user_confirmation` — 0 blocker · 0 major · 1 minor.** Chỉ đọc lại các mục của vòng 1 + phần E thêm từ lần chạy thử.

| Mục vòng 1 | Đóng? | Chỗ trong bản 2 |
|---|---|---|
| M-1 xoá máy | **đóng** | §10.5: nhãn [User]; vòng chờ `available` có trần (60 × 20 s); chỉ xoá khi in `available`; mọi lệnh có `--region`; có kiểm sau khi xoá (máy, IP, bản chụp) |
| M-2 khuôn 4 phần | **đóng** | A6, A7, B2, B3, C2 (thêm `test ! -e` chặn ghi đè khoá), C3, C4, D1, D2, D3, 10.2, 10.3 đều có Kiểm / Mong đợi / Dừng khi; 10.2 hỏng ⇒ 10.3 ngay |
| M-3 câu User | **đóng** | §3: tổng tiền ~90–105 USD / 3 tháng (trước credit), Q9 (agent chỉ chạy lệnh chỉ đọc; [Tiền] / xoá User tự gõ), Q10 (ngày tạo máy, nhắc dặn "không deploy sớm"), Q11 (giữ file deploy) |
| m-1 bản chụp 6335 | đóng | A5, A6 xoá ngay sau khi tải + kiểm danh sách rỗng; §13 đo: 6335 vẫn 9.425 điểm |
| m-2 A2 `THIEU` | đóng | ghi lại rồi đi tiếp; phán quyết ở A5 (app không lên) |
| m-3 `TAG` | đóng | §4 + dòng đầu D3 |
| m-4 vòng chờ C3 | đóng | trần 60 × 10 s, in trạng thái |
| m-5 §9 | đóng | thêm dòng hết lượt (3 ⇒ 4 lượt ⇒ trả về 50) + dòng ảnh qua https |
| m-6 file deploy | đóng | §4 md5 — C chạy `md5sum`: 4 / 4 khớp (`bd887103b463` · `942d3527c413` · `da85ebea1915` · `98e0edaecfee`); Q11 |

**Minor mới (sửa khi tiện, không chặn):**
- **n-1 (10.3, khi kho đổi ở 10.2):** 10.2 chép `qdrant.snapshot` mới đè lên file cùng tên ở `/srv/hue`. Quay lại bản cũ thì cần **chép lại** bản chụp cũ từ `~/hue_deploy_<TAG cũ>/` (máy User) bằng `scp` rồi mới nạp như D3. Bản 2 chỉ ghi "nạp lại bản chụp cũ trong `~/hue_deploy_<TAG cũ>/`" ⇒ agent có thể nạp nhầm file mới đang nằm trên máy AWS. Đóng khi: thêm một dòng `scp` vào 10.3, hoặc 10.2 lưu bản chụp theo tên `qdrant_$TAG.snapshot`.

Ghi nhận phần thêm từ chạy thử (§13, [Đo] 16/11): A4 bỏ qua `backend/` (bản 1 bắt nhầm 2 file code) đúng; lệnh dọn thư mục Qdrant thuộc root qua `docker run` hợp lý; số đo (8 s build có cache, 0,90 GB ảnh nén, app 1.021 MiB, 429 cả khi giả `X-Forwarded-For`) có nhãn. Phần AWS (B–E, 10.x) vẫn NOT RUN như spec ghi.
