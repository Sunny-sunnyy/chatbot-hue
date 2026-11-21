# Bản sửa số 3 — lệnh "thêm điểm" khi sửa lịch không còn tự thế chỗ một điểm đang có (nhánh `p9-c-sua-3-them-diem`)

Phiên C ghi 19:25 21/11/2026 (giờ `date`). Nhánh rẽ từ main `ce0c4e6a`. Cờ `sua_lich_them_khong_the` mặc định TẮT — chưa bật, chưa gộp. Người đọc nhánh: phiên B.
Đây là bản hẹp của mục đã chốt "hỏi lại khi thiếu thông tin". **Quyết định chờ:** giữ hay gỡ; BẬT là đổi thứ người dùng thấy ⇒ chủ dự án chọn.
Plan + tiêu chí ghi trước (riêng tư): `data/thu_bedrock_2026-11-21/c_sua_3/PLAN.md`.

## Vì sao
Lượt mốc 12 vai tối 21/11, vai sửa lịch, CẢ HAI model: người dùng nhờ "thêm X vào sáng ngày 2" ⇒ code tự thế chỗ một điểm đang có rồi báo "Đã thêm X (…, thế chỗ Y)" ⇒ người dùng xin trả Y ⇒ code lại thế chỗ điểm kia; model cũ lặp ba lượt liền (5 / 8 lượt sửa lịch của lượt mốc). Khi chỗ được nêu bị luật xếp chặn thì chỉ có một câu chung, không lý do, không chỗ làm được.
Đếm trên bộ áp thật, 144 lịch mẫu (1–4 ngày × 3 kiểu đi × 6 sở thích × có / không người lớn tuổi) × 37 điểm ban ngày = 39.509 lệnh thêm:

| Lệnh | Số lệnh | Thêm được, không mất gì | Code tự thế chỗ | Từ chối bằng câu chung |
|---|---|---|---|---|
| "thêm X" (không nói chỗ) | 4.489 | 27 (0,6 %) | 2.825 (63 %) — điểm bị thế là điểm chính 84 % | 1.637 (36 %) |
| "thêm X vào <buổi> ngày <n>" | 21.592 | 27 (0,1 %) | 7.019 (33 %) — điểm chính 58 %; là điểm duy nhất của buổi 91 % | 14.546 (67 %) |
| bỏ một điểm rồi thêm vào đúng buổi đó | 13.428 | 1.049 (7,8 %) | 3.318 (25 %) | 9.061 (67 %) |

Lịch mới lập gần như luôn kín ⇒ "thêm" trên thực tế là "thay", và code chọn điểm bị mất — phần lớn là điểm chính.

## Đã làm (cờ bật)
- Lệnh thêm chỉ làm được bằng cách thế chỗ ⇒ KHÔNG áp, lịch giữ nguyên, một dòng do code viết, ví dụ: "Chưa làm: thêm Đàn Nam Giao — buổi sáng ngày 1 đang có Đại Nội Huế; thêm vào đó thì lịch sẽ có buổi quá kín hoặc quá giờ. Muốn đổi, bạn nhắn: thay Đại Nội Huế bằng Đàn Nam Giao." Nêu tối đa hai điểm, và chỉ điểm mà code đã thử thay được.
- Lệnh thêm bị luật xếp chặn ⇒ lý do cụ thể + tối đa hai cách làm được, ví dụ: "Chưa làm: thêm Lăng Khải Định vào buổi sáng ngày 2 — vì lịch sẽ có buổi quá kín hoặc quá giờ. Làm được: bạn nhắn thay Lăng Tự Đức bằng Lăng Khải Định (buổi chiều ngày 2)."; không còn cách nào ⇒ "Lịch này hiện không còn chỗ nào xếp được X."
- Lệnh thêm làm được mà không mất gì ⇒ y như cũ. Lời dặn và khuôn của lần hiểu ý sửa KHÔNG đổi (chỉ đổi phần code sau đó).
- Phạm vi: chỉ nhánh "thêm điểm" của `sua_lich_v2.ap`; lượt lập lịch, lệnh dời, lệnh thay, phần tự lấp sau khi bỏ điểm không đổi.

| Người dùng ĐƯỢC gì | Người dùng MẤT gì |
|---|---|
| Không bao giờ mất một điểm mà mình không xin bỏ; biết buổi đó đang có gì, vì sao không thêm được, và đúng câu để nhắn nếu muốn đổi | Người sẵn lòng đổi phải nhắn thêm MỘT lượt ("thay Y bằng X") — hôm nay một lượt là xong |
| Lệnh thêm bị chặn có lý do + cách làm được (trước: một câu chung, lặp lại y nguyên) | Dòng dài hơn; câu trả lời cụt kiểu "ừ đổi đi" có thể không được hiểu (lần hiểu ý không thấy lượt trước) — đang đo |

## Lệnh kiểm + đầu ra (0 đồng, không gọi model; bảng điểm thật, bộ áp thật)
| Tiêu chí ghi trước | Lệnh | Đầu ra |
|---|---|---|
| S0 cờ tắt giống từng byte | mô phỏng 39.509 lệnh ở cây gốc ↔ cây nhánh cờ tắt, so mã băm (kết quả áp + chữ khối thay đổi) | khác 0 / 39.509 |
| S1 cờ bật: 0 lệnh thêm làm mất điểm | mô phỏng cờ bật | 0 · 0 · 0 (ba hàng) |
| S2 số lệnh thêm thật không đổi | như trên | 27 · 27 · 1.049 — như cờ tắt |
| S3 mọi câu gợi ý đều làm được khi áp | áp đúng lệnh được gợi ý, kiểm X vào đúng buổi nêu | 4.941 / 4.941 · 21.074 / 21.074 · 12.194 / 12.194 |
| L1 ca bị chặn có lý do hoặc cách làm được ≥ 95 % | như trên | 25.244 / 25.244 có lý do; có cách làm được 12.821 / 23.607 khi người dùng nói rõ chỗ |
| test | `pytest tests/test_sua_lich_them.py -q` | `5 passed`; cố ý tắt nhánh mới ⇒ `4 failed, 1 passed` ⇒ trả lại ⇒ `5 passed` |
| test lân cận, từng file | `test_sua_lich_v2` · `test_sua_lich_kem_hoi` · `test_doi_cho_ngay` · `test_cong_dot_1` · `test_phase6_settings` · `test_settings_env` | 13 · 7 · 26 · 22 · 5 · 6 passed |

## Chưa làm · giới hạn
- CHƯA có lượt model thật nào: ô "câu trả lời sau dòng gợi ý có được hiểu không" (bộ mù 10 câu của phiên điều phối × 2 model × 3 lượt) và chuỗi qua đường chat thật mỗi model — chạy sau commit này, số ghi vào file này.
- Chưa nhìn giao diện; chưa chạy các file test dựng cả app.
- Trong một tin có nhiều hành động, cách gợi ý được tính trên lịch tại lúc xét lệnh thêm; hành động đứng SAU nó trong cùng tin có thể làm một gợi ý hết đúng (chưa thấy ca nào; mỗi lượt áp tối đa hai hành động).
- Phép này KHÔNG cho biết người thật muốn "thêm mà giữ hết" hay chấp nhận "thêm = thay" (số lượt là của một vai mô phỏng) · hướng rộng hơn: lịch luôn kín là do bộ xếp lấp đủ quỹ giờ mỗi buổi — cho buổi dày hơn khi người dùng tự xin là đổi luật xếp, việc của chủ dự án · đếm rẻ nhất kế: khi cờ bật, đếm trên log bao nhiêu lượt có dòng "Chưa làm: thêm" được nối bằng một lệnh "thay" ở lượt sau.
