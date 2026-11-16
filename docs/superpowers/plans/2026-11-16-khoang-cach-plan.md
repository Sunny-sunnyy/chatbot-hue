# Plan mức nhẹ — công cụ khoảng cách giữa hai điểm (C, 14:19 16/11/2026)

A giao 16/11 (User duyệt đẩy nhanh). Mức nhẹ (`Session_Prompt.md` §7): A đọc rồi duyệt, không review plan; trần tiền **0,15 USD**.

## 1. Lỗi có thật (đếm trước khi xây — đã chạy)
Server 8010 (`main` `6012208`, đúng cấu hình User dùng), 6 câu "từ nơi này sang nơi kia bao xa / mất bao lâu", mỗi câu một cuộc mới, cả hai nơi đều có trong bảng lịch:
**4 / 6 bị kho từ chối** (rồi mới ra mục "Từ web"); 2 / 6 model ước từ câu "cách trung tâm … km" trong kho (một câu nói thẳng là nguồn không nêu riêng). Tiền 0,0103 USD (vượt mức ước ≤ 0,002 vì 4 câu từ chối đều tra web). Dữ liệu private: `data/khoang_cach_2026-11-16/dem_truoc.{py,json}`.

## 2. Thiết kế (theo khuôn công cụ thời tiết: code tính, model chỉ chọn)
- **Bảng số dựng một lần, không gọi gì lúc chạy:** từ toạ độ bảng lịch v9 (`diem_toa_do_v9.json`, 40 / 41 điểm có toạ độ) dựng `data/phase_9/lich_trinh/khoang_cach_v1.json` = với mỗi cặp điểm: km đường đi + phút ô tô / xe máy.
  - **Cách dựng — A chọn một:** (a) **đề xuất:** một lần gọi bảng khoảng cách của OSRM (máy chủ thử công khai, miễn phí; chỉ gửi toạ độ công khai của 40 điểm; ra km + phút theo đường thật) — đúng hơn rõ với cặp cách sông / đường vòng. (b) chỉ tính bằng code: đường chim bay (haversine) × 1,3, phút theo 30 km/h. Không cần dịch vụ ngoài, nhưng là phép ước thô. Nếu chọn (b) thì câu trả lời phải ghi rõ "đường chim bay".
  - Kiểm bảng (0 USD): mọi số > 0, đối xứng trong ±15 %, km đường đi ≥ km chim bay; 5 cặp đối chiếu tay với số trong kho hoặc trên web (ghi nguồn).
- **Công cụ `khoang_cach(diem_a, diem_b)`** — tham số là **id trong một danh sách cố định** (enum 41 id + `khac`); mô tả công cụ liệt kê `id: tên (tên khác)`. Model ánh xạ tên ⇒ id; code **không** đọc tên từ chữ người dùng. `khac` / điểm không có toạ độ ⇒ khối cố định "Mình chưa có số khoảng cách cho nơi này".
- **Chỉ đưa công cụ khi code dò thấy từ khoá** trong câu (hoặc câu hỏi liền trước): `bao xa`, `cách … bao`, `mấy km / cây số`, `mất bao lâu`, `đi … bao lâu`, `gần … không`, `xa không` (như `thoi_tiet.co_tu_khoa_luot`). Lượt khác ⇒ danh sách công cụ như cũ, chuỗi gửi model giống byte.
- **Kết quả là một nguồn do code dựng** trong sổ nguồn (khuôn như `ngay_lich_for_turn`: tiêu đề "Khoảng cách ước tính (bản đồ)", một dòng "Từ A đến B: khoảng X km đường đi, ô tô / xe máy khoảng Y phút (ước tính, chưa tính tắc đường / dừng nghỉ)") ⇒ model trích [n] như mọi nguồn. **Kiểm số bằng code:** lượt có gọi công cụ ⇒ số trong lời model ⊂ (số của nguồn khoảng cách ∪ số trong đoạn trích); hỏng ⇒ rút lại như citation hỏng — dùng lại `tt.tap_so` / `tt.kiem_so`. Không nối khối sau câu trả lời (đơn giản hơn khuôn thời tiết; câu chỉ có khoảng cách vẫn trích được [n]).
- **Cờ `khoang_cach: false`** (mặc định tắt), nhánh `p9-khoang-cach`; cần `tim_them`. Cờ tắt ⇒ chuỗi gửi model giống byte (Q1).

## 3. Bộ đo + tiêu chí (ghi trước)
| Vai | Bộ | Ngưỡng |
|---|---|---|
| Bộ dò từ khoá (W82, 0 USD) | ≥ 20 câu do **người không viết code** soạn (A giao): câu phải bật + câu "giống mà không phải" (vd "cách làm", "xa hoa", "bao lâu thì chín") + câu ghép + câu ngoài phạm vi | **0 câu ra sai** = 0 câu không hỏi khoảng cách mà bật công cụ (bỏ sót câu khoảng cách ⇒ từ chối như cũ, được phép, ghi số) |
| Chạm đường đổi (có phí) | 6 câu ở mục 1 + ~10 câu mới (cặp trong bảng, một nơi ngoài bảng, câu hỏi tiếp "từ đó sang …", câu "gần không") | Sàn: **0 số sai** (số trong câu trả lời ≠ khối); **0 câu** model đưa số cho nơi ngoài bảng. Quyết: ≥ 12 / 14 câu trong bảng có khối số đúng cặp |
| An toàn 32 | chỉ nếu câu an toàn chạm từ khoá (đếm bằng code trước) | như luật hiện hành; 0 câu chạm ⇒ không chạy |
| Q1 | test cờ tắt + 4 loại lượt (đầu, hỏi tiếp, sau nút, có lịch sử) | giống byte / có-không đúng plan |
Đo 1 lượt (mức nhẹ) trên server tạm của C cổng 8041; 8010 để User.

## 4. Tiền
Dựng bảng 0 USD. Đo ≈ 16 câu × ~0,0007 ≈ **0,012 USD** (câu có khối không tra web); dự phòng chạy lại sau sửa ≈ 0,012 ⇒ ước **≤ 0,03**, trần 0,15.

## 5. A duyệt (tin nhắn A ngày 16/11/2026; giờ duyệt A ghi ở handoff)
1. **(a) OSRM MỘT lần, offline:** bảng lưu `data/phase_9/lich_trinh/khoang_cach_v1.json` (md5 `cb76ab72199c`, 40 điểm có toạ độ × 39 chiều = 1.560 cặp, OSRM trả đủ 1.560); runtime không gọi mạng; cặp OSRM lỗi ⇒ "chưa có số", không chèn chim bay. Chữ người dùng thấy: "khoảng … km đường đi, khoảng … phút đi xe (ước theo đường)" + "chưa tính kẹt xe hay dừng nghỉ".
2. **Công cụ này KHÔNG đổi lịch** — lịch vẫn dùng phút theo cụm (`_phut_di`).
3. Bộ dò từ khoá ≥ 20 câu: agent con của A soạn (`data/khoang_cach_2026-11-16/bo_do_tu_khoa.jsonl`, 27 câu). "Ra sai" = câu khoảng cách không bật / công cụ ra số cho cặp sai nơi; bật thừa ghi riêng.

## 6. Chi tiết C tự quyết trong phạm vi (ghi lúc code)
- **Phút hiện = 1,25 × phút OSRM + 5** (sửa theo review M1, 15:01 16/11/2026; bản đầu dùng sàn 40 km/h — chọn từ 2 cặp nội thành, đổi số ở 1.082 / 1.560 cặp, chặng dài chậm quá). Đối chiếu 6 cặp có nguồn công khai ở report.
- Cặp < 0,5 km (4 cặp OSRM ra 0 km vì cùng điểm bám đường) ⇒ "dưới 0,5 km".
- Bảng không đối xứng ở 62 cặp nội thành (đường một chiều) ⇒ dùng đúng chiều người hỏi; bỏ tiêu chí "đối xứng ±15 %" của mục 2.
- Kiểm số chấp nhận số làm tròn của số thập phân trong nguồn (lượt đo: "4,0 km" ⇒ model viết "4 km" bị rút lại oan 2 / 14); tách km ↔ thời gian (review m2); viết riêng `kc.tap_so` / `kc.kiem_so` thay vì dùng lại của thời tiết (khác đơn vị — review m4).
- Công cụ ăn một vòng ⇒ `max_turns` + 1 khi có đưa công cụ (như `ngay_lich`).
