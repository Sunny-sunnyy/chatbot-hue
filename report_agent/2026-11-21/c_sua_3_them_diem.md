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
- Lệnh thêm chỉ làm được bằng cách thế chỗ ⇒ KHÔNG áp, lịch giữ nguyên, một dòng do code viết, ví dụ: "Chưa làm: thêm Đàn Nam Giao — buổi sáng ngày 1 đang có Đại Nội Huế; thêm vào đó thì lịch sẽ có buổi quá kín hoặc quá giờ. Muốn đổi, bạn nhắn đủ câu: thay Đại Nội Huế bằng Đàn Nam Giao." Nêu tối đa hai điểm, và chỉ điểm mà code đã thử thay được.
- Lệnh thêm bị luật xếp chặn ⇒ lý do cụ thể + tối đa hai cách làm được, ví dụ: "Chưa làm: thêm Lăng Khải Định vào buổi sáng ngày 2 — vì lịch sẽ có buổi quá kín hoặc quá giờ. Làm được, bạn nhắn đủ câu: thay Lăng Tự Đức bằng Lăng Khải Định (buổi chiều ngày 2)."; không còn cách nào ⇒ "Lịch này hiện không còn chỗ nào xếp được X."
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

## Thêm 19:37 21/11/2026 — số đo lần hiểu ý + phần lệnh THAY (phiên điều phối chốt sau khi thấy số)
**Ô "câu trả lời sau dòng gợi ý có được hiểu không"** — bộ mù 10 câu của phiên điều phối × 2 model × 3 lượt = 60 lời gọi lần hiểu ý, 0 lỗi gọi; luật chấm ghi trước (plan mục 8); 0,352 USD (model đang chạy) + 0,0025 USD (model cũ):

| Tiêu chí ghi trước | Model cũ | Model đang chạy |
|---|---|---|
| 7 câu nói rõ tên điểm: hiểu đúng ≥ 19 / 21 | 21 / 21 | 21 / 21 |
| hai câu không được đổi lịch ("thôi khỏi…", "sao lại không thêm được?"): 0 lượt đổi | 0 / 6 | 0 / 6 |
| 3 câu chỉ hiểu được khi thấy lượt trước (báo riêng; ngưỡng xét lại 6 / 9) | 2 / 9 | 3 / 9 |

- Trong ba câu cuối: "ok thay đi" và "ừ đổi luôn nhé" 0 / 6 mỗi model (lần hiểu ý không thấy lượt trước ⇒ trả danh sách rỗng ⇒ lượt đi đường hỏi đáp thường). **Giới hạn ghi nhận:** câu đồng ý cụt không được hiểu ⇒ dòng gợi ý đổi chữ thành "bạn nhắn đủ câu: thay Y bằng X". Nút bấm / đưa lượt trước vào lần hiểu ý: chỉ xét sau khi thấy người dùng nhận gì ở lượt đó trên đường chat thật.
- Các câu của bộ mù nhắc tới điểm mà code KHÔNG gợi ý (người dùng tự chọn điểm khác): hiểu đúng nhưng bộ áp từ chối bằng câu chung cũ của lệnh THAY (0 / 3 áp được) ⇒ thêm phần dưới.

**Lệnh THAY bị luật xếp chặn** (cùng cờ, cùng cách chữa, khoảng 10 dòng): "Chưa làm: thay Y bằng X — vì <lý do>. Làm được, bạn nhắn đủ câu: …" thay cho câu chung. Lệnh thay làm được ⇒ không đổi gì.

| Tiêu chí | Đầu ra sau phần thêm (mô phỏng 53.189 lệnh: ba hàng lệnh thêm + 13.680 lệnh thay) |
|---|---|
| S0 cờ tắt giống từng byte cây gốc ↔ nhánh | khác 0 / 53.189 |
| S1 lệnh thêm làm mất điểm · S2 lệnh thêm thật | 0 · 0 · 0 · như cũ 27 · 27 · 1.049 |
| S3 mọi cách nêu ra đều làm được | 4.941 / 4.941 · 21.074 / 21.074 · 12.194 / 12.194 · lệnh thay 9.504 / 9.504 |
| Lệnh thay: 13.680 lệnh | thay được 3.388 (như cờ tắt) · bị chặn 10.292 — có lý do 10.292 / 10.292 (trước: 0), kèm cách làm được 5.490 |
| test | `pytest tests/test_sua_lich_them.py -q` ⇒ `6 passed`; cố ý tắt nhánh lệnh thay ⇒ `1 failed, 5 passed` ⇒ trả lại ⇒ `6 passed`; `test_sua_lich_v2` 13 · `test_sua_lich_kem_hoi` 7 · `test_doi_cho_ngay` 26 passed |

## Thêm 19:45 21/11/2026 — ba điểm nhỏ của người đọc (phiên B) + chuỗi qua đường chat thật
Người đọc (phiên B, mô phỏng độc lập 81 lịch có cả ngày đi + mưa, 4.698 lệnh): sẵn gộp cờ tắt, 0 điểm chặn; ba điểm nhỏ đã xử lý ở commit này:
1. Lệnh thêm KHÔNG nói chỗ mà hết cách: câu không còn gán lý do riêng của một buổi ("vì đặt vào buổi nào lịch cũng phạm luật xếp…"); lý do cụ thể chỉ nêu khi người dùng nói rõ một buổi.
2. Thứ tự hai cách nêu ra: cùng ngày được xin trước · thêm thẳng trước · điểm bị thay là điểm không có thứ hạng ưu tiên trước, rồi điểm ngoài sở thích.
3. Script mô phỏng (riêng tư) nay chạy được trên đúng commit này; đầu ra chạy lại: cờ tắt giống byte khác 0 / 53.189 · lệnh thêm làm mất điểm 0 · 0 · 0 · thêm thật 27 · 27 · 1.049 · cách nêu ra làm được 4.941 / 4.941 · 21.074 / 21.074 · 12.194 / 12.194 · lệnh thay 9.504 / 9.504 · lệnh thêm có nói chỗ bị chặn 23.607, đều có lý do cụ thể, 12.821 kèm cách · lệnh thay bị chặn 10.292, đều có lý do, 5.490 kèm cách. `pytest tests/test_sua_lich_them.py -q` ⇒ `6 passed`.

**Chuỗi sáu lượt qua đường chat thật, mỗi model một chuỗi** (cờ bật bằng ghi đè cấu hình; 0,0024 USD + 0,151 USD):
- "Thêm Đàn Nam Giao vào sáng ngày 1" ⇒ lịch giữ nguyên + dòng gợi ý; nhắn đúng câu gợi ý ⇒ "Đã thay Đại Nội Huế bằng Đàn Nam Giao."; "Thêm Lăng Khải Định vào sáng ngày 2" ⇒ lý do + cách; nhắn câu đó ⇒ áp. Cả hai model như nhau, 5 / 6 lượt đúng thiết kế.
- Lượt "ok thay đi" (đồng ý cụt): model cũ ra lượt sửa với dòng nói thật "việc này mình chưa sửa được trên lịch — lịch giữ nguyên… bạn nói cụ thể nhé". **Model đang chạy đi đường hỏi đáp thường và viết "Mình đã thêm Đàn Nam Giao vào sáng ngày 1…" trong khi lịch KHÔNG đổi** — nói chắc mà sai.

| Thêm vào bảng "được / mất" | |
|---|---|
| Mất (cả hai model) | 36 % lệnh "thêm X" không nói chỗ kết thúc bằng "lịch này hiện không còn chỗ nào xếp được X" (1.637 / 4.489; mẫu của người đọc: 42 %) — hôm nay các lệnh đó cũng không thêm được, chỉ khác là nay nói thẳng |
| Rủi ro mới (model đang chạy), ĐANG CHỮA | câu khẳng định đã sửa lịch ở đường hỏi đáp thường: 0 / 451 lượt sổ thật, 0 / 290 lượt của ba lượt mốc, nhưng 1 / 1 ở lượt "ok thay đi" ngay sau dòng gợi ý ⇒ dòng gợi ý mời một câu trả lời mà lần hiểu ý không hiểu. Chưa chữa xong thì KHÔNG đề nghị bật cho model đang chạy. Cách chữa đã chọn: đưa câu gợi ý của lượt trước vào lần hiểu ý ở đúng lượt kế — làm ở commit sau, số ghi tiếp vào file này |

## Thêm 20:01 21/11/2026 — chữa lượt "đồng ý cụt": câu gợi ý của lượt trước vào lần hiểu ý (cùng cờ)
**Cách làm:** câu code gợi ý ở một lượt ("thay Y bằng X") được nhớ cho ĐÚNG MỘT lượt kế (một ô trong kho cuộc trò chuyện, đọc là xoá; chỉ chữ do code dựng) và được đưa vào tin nhắn của lần hiểu ý ở lượt đó: một câu gợi ý + lời đồng ý ⇒ đúng hành động của câu đó; hai câu mà không rõ chọn câu nào ⇒ không tự chọn; từ chối / phân vân / hỏi chuyện khác ⇒ không coi là đồng ý. Lượt khác gửi model giống từng byte; bộ áp không đổi (53.189 lệnh mô phỏng, cờ tắt và cờ bật: khác 0).
Test: `pytest tests/test_sua_lich_them.py -q` ⇒ `9 passed`; cố ý không đưa câu gợi ý vào lần hiểu ý ⇒ `1 failed, 8 passed` ⇒ trả lại ⇒ `9 passed`; `test_nho_ten_goi_y` 19 · `test_cong_dot_1` 22 · `test_sua_lich_v2` 13 · `test_sua_lich_kem_hoi` 7 · `test_doi_cho_ngay` 26 passed.

**Ô hiểu ý, ngưỡng ghi trước** (bộ mù 10 câu + hai câu mặt trái của phiên điều phối = 12 câu × 2 model × 3 lượt = 72 lời gọi, 0 lỗi gọi; 0,416 USD + 0,0032 USD):

| Tiêu chí | Model cũ: trước ⇒ sau | Model đang chạy: trước ⇒ sau |
|---|---|---|
| 3 câu đồng ý cụt / dùng đại từ: hiểu đúng ≥ 6 / 9 | 2 / 9 ⇒ **9 / 9** | 3 / 9 ⇒ **9 / 9** |
| 7 câu nói rõ tên điểm: không tụt, ≥ 19 / 21 | 21 / 21 ⇒ 20 / 21 | 21 / 21 ⇒ 21 / 21 |
| "thôi khỏi…", "sao lại không thêm được?": 0 lượt đổi lịch | 0 / 6 ⇒ 0 / 6 | 0 / 6 ⇒ 0 / 6 |
| mặt trái: "ok để mình nghĩ đã", "ừ, mà … có gì hay vậy?": 0 lượt đổi lịch | 0 / 6 | 0 / 6 |

**Chuỗi tám lượt qua đường chat thật, BA lần mỗi model** (0,0085 USD + 0,506 USD):

| | Model cũ | Model đang chạy |
|---|---|---|
| "ok thay đi" NGAY SAU dòng gợi ý ⇒ thành lệnh thay thật ("Đã thay Đại Nội Huế bằng Đàn Nam Giao.") | 3 / 3 | 3 / 3 (bản trước: 0 / 1, viết "Mình đã thêm…" khi lịch không đổi) |
| "ok để mình nghĩ đã" / một câu hỏi khác ngay sau dòng gợi ý ⇒ lịch đổi | 0 / 6 | 0 / 6 |
| lượt đi đường hỏi đáp thường có câu "mình đã thêm / bỏ / thay / dời…" | 0 / 8 | 0 / 7 |

**Giới hạn còn lại (ghi nhận, chưa chữa):** câu gợi ý chỉ sống MỘT lượt. Người dùng hỏi một câu khác rồi mới nhắn "ok thay đi" (lượt 8 của chuỗi) thì lần hiểu ý không còn thấy câu gợi ý: model đang chạy 3 / 3 nói thật (hỏi lại "bạn muốn thay mục nào…", hoặc dòng "việc này mình chưa sửa được trên lịch… bạn nói cụ thể nhé"); model cũ 1 / 3 viết "Được, mình thay Lăng Đồng Khánh bằng Lăng Khải Định vào khung 9:45–11:00…" trong khi lịch không đổi — câu đó bị phép kiểm trích dẫn rút lại, người dùng thấy dòng lỗi "không đáp ứng yêu cầu trích dẫn" (không thấy câu sai), 2 / 3 còn lại hỏi lại / nói thật.
