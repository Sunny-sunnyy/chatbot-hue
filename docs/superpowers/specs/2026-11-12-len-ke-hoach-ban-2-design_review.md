# Review: Spec "Lên kế hoạch" bản 2 (nháp bản 1) — vòng 1

Decision: **changes_requested** (0 blocker, 2 major, 6 minor) — sửa chữ là đủ; vòng 2 chỉ xem hai chỗ major.
Người kiểm: E (Claude Code — Fable 5.2, `hue-rag-33`) · Date: 21:19 12/11/2026 (`date`)
Bản được review: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` sha256 `aeac8c589822` (người viết: C)

## 1. Phạm vi đã review
Đọc hết spec; đối chiếu (chỉ đọc, 0 USD) với: `backend/llm/lich_trinh.py` (`ThamSo`, `HAN_CHE`, `xep`, `kiem_khung`, `kiem_cuoi`), `backend/llm/hoi_lai.py` (`GIA_TRI`), bảng điểm đang chạy `data/phase_9/lich_trinh/diem_v3.json` (đếm theo cột), bảng vé cũ `data/phase_9/t3_bang_ve_gio/`, kho (đếm số bài qua `scripts/grep_kb.sh`), và hai tài liệu của E mà spec phụ thuộc: plan lưu trú bản 2 (`d2b4bc486480`) + spec đợt bổ sung kho 3 (`14387f19f5b0`). Không đọc STATUS của C. Không chạy mô phỏng.

## 2. Findings

### M-1 (major) — ngưỡng "đổi lịch" (70 % / 60 % / 50 %) chưa phải tiêu chí ghi trước: spec để plan "mô phỏng thử rồi chốt số trước khi code"
- **Vị trí:** mục 3 cột "Tiêu chí đổi lịch" (kiểu đi ≥ 70 %, ngày khởi hành ≥ 60 %, sở thích ≥ 50 %, ngân sách ≥ 60 %); lời C nhờ soi (3).
- **Yêu cầu:** `Session_Prompt.md` §6 "ghi tiêu chí trước khi chạy", §4 "không sửa tiêu chí để hợp thức hoá kết quả"; nguyên tắc N1 của chính spec.
- **Bằng chứng / lập luận:** mô phỏng chỉ chạy được **sau khi** luật xếp mới đã viết (kiểu đi 3 mức, hai sở thích, thứ / mùa chưa có trong `xep`). Vậy "mô phỏng rồi chốt số" trên thực tế là: code ⇒ xem ra bao nhiêu ⇒ đặt ngưỡng dưới con số đó. Ngưỡng khi ấy mô tả kết quả, không kiểm nó.
- **Tác động:** N1 ("ô nào hiện thì đổi được lịch") mất răng: ô đổi lịch ở 20 % tổ hợp vẫn "đạt" nếu ngưỡng được chốt sau.
- **Tiêu chí đóng (đề xuất cách viết):** spec chốt **ngay bây giờ** hai lớp cho mỗi ô: (i) **bất biến 100 %** kiểm bằng mô phỏng — vd số điểm / ngày: nhẹ nhàng ≤ cân bằng ≤ khám phá nhiều ở mọi tổ hợp; nhóm hạn chế không vượt trần; phố đi bộ 0 lần sai tối; (ii) **sàn "có tác dụng"** = chính các số 70 / 60 / 50 % đã viết, ghi rõ là **sàn sản phẩm**, plan từng đợt **chỉ được nâng, không được hạ**; không đạt sàn ⇒ **ô đó không hiện** ở đợt ấy (đúng N1), không phải hạ ngưỡng. Mô phỏng trước khi code chỉ dùng để **đếm dữ liệu** (bảng có đủ điểm "ngắn", đủ điểm mỗi loại…) — việc đó làm được hôm nay trên bảng v3 / phiếu gộp và nên có số trong spec.

### M-2 (major) — đợt 2 lệch với hai tài liệu nó phụ thuộc (plan lưu trú + spec đợt bổ sung kho 3)
- **Vị trí:** mục 3 các dòng "Bữa ăn", "Lưu trú", "Dịch vụ / đi lại"; mục 4 cột đợt 2; mục 9.3. (C đã báo trước là viết theo mô tả handoff.)
- **Bằng chứng — ba chỗ lệch cụ thể:**
  1. **Thẻ lưu trú dưới lịch:** plan lưu trú bản 2 (A đã duyệt) quy định lượt **biểu mẫu lịch trình ⇒ không có thẻ** (tiêu chí L7, ca thứ 5) và thẻ được kích theo nguồn kho / từ khoá của **lượt chat**. Spec này đòi "100 % lịch ≥ 2 ngày có thẻ". Hai tài liệu trái nhau.
  2. **Bữa ăn "quán ≤ 1,5 km, ≥ 80 % ngày ở cụm trung tâm":** spec kho 3 khuyến nghị (Q4) chỉ dùng **7** bài quán có toạ độ chắc / vừa (22 bài còn lại là toạ độ ước, sai số 95 % ≤ 522 m) và (Q3) **không** thêm quán mới quanh Đại Nội / Thiên Mụ. Dữ liệu C dựng: quanh Đại Nội 1 quán có toạ độ, quanh Thiên Mụ và các lăng 0; bảng điểm có 4 điểm cụm kinh thành, 7 điểm cụm Thuỷ Xuân (lăng). Với dữ liệu đó ngưỡng 80 % **không đạt được** ở cụm kinh thành, trừ khi User chọn phương án (b) ở Q3 / Q4 của spec kho 3.
  3. **Dòng đi lại "câu cố định theo cụm … cách trung tâm ~N km, nên đi …":** spec kho 3 đưa nội dung đi lại vào **kho** (bài có nguồn, không giá); ở đây lại là câu cố định trong code. Phần "nên đi bằng gì" là lời khuyên cần nguồn ⇒ nên lấy từ bài kho (có trích dẫn); code chỉ nối **con số khoảng cách**.
- **Tiêu chí đóng:** (1) ghi rõ thẻ lưu trú dưới lịch là **đường kích hoạt thứ hai** của cùng module (code gọi trực tiếp khi lịch ≥ 2 ngày) và nêu đây là **sửa plan lưu trú** (L7 ca 5 đổi thành "có thẻ khi ≥ 2 ngày") — E sửa plan khi A đồng ý; (2) tiêu chí bữa ăn viết theo **dữ liệu sẽ có**: phụ thuộc Q3 / Q4 của spec kho 3, và nêu hai mức (chỉ toạ độ chắc ⇒ ngưỡng theo cụm có quán; có thêm quán ⇒ 80 %); (3) dòng đi lại = khoảng cách do code + câu khuyên trích từ bài kho của đợt 3; (4) mục 9.3 trỏ đúng file `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` và ghi "đợt 2 chỉ mở khi User đã trả lời Q1–Q5 của spec đó".

### Minor (không chặn)
- **m-1 — hai cột dữ liệu mới của ô ngày khởi hành (C nhờ soi (2)):** E đếm kho (mức số bài): bài có ghi **thứ** hoạt động của phố đi bộ: 3 bài ⇒ cột `ngay_hoat_dong` cho ~3 điểm buổi tối **có căn cứ**; bảng v3 hiện có đúng 3 điểm chỉ buổi tối + 1 điểm cả ba buổi. Bài điểm tham quan có cảnh báo mùa **kèm tháng**: 30 / 30 bài có nhắc mùa mưa / lũ / bão ⇒ cột `mua_luu_y` **có căn cứ**, nhưng bảng v3 mới có 2 / 28 điểm mang lưu ý ⇒ phải dựng cột từ kho và đưa vào phiếu User duyệt (thêm một dòng ở mục 9.1). Ghi số này vào spec.
- **m-2 — bảng vé:** đã có bảng vé + giờ dựng từ kho ở đợt trước (`data/phase_9/t3_bang_ve_gio/bang_v1.json`, có phiếu cho User) ⇒ ô ngân sách nên **dùng lại** bảng đó (kiểm lại ngày nguồn), không dựng mới; ghi vào cột "Dữ liệu cần".
- **m-3 — ô "số người lớn" (Câu 2):** ngoại lệ được nêu rõ, chấp nhận được; nhưng tiêu chí đợt 1 nên có một dòng đo cho nó: "đổi `nguoi_lon` ⇒ khung giống byte, chỉ dòng 'Mình hiểu' khác" — để ngoại lệ không lan thành tác dụng ngầm.
- **m-4 — loại "lễ hội, nghệ thuật" ẩn:** khớp bảng (E đếm v3: di tích 16 · thiên nhiên 8 · ẩm thực 6 · chụp ảnh 4 · lễ hội 1). Lưu ý "chụp ảnh" đứng đúng ngưỡng 4 ⇒ một điểm bị loại ở v8 / v9 là ô này phải ẩn — ghi luật ẩn chạy theo bảng lúc khởi động (đã có ý ở mục 7 "ô tự ẩn"), và test cho ca đó.
- **m-5 — tốc độ:** "trung vị cả câu ≤ 8 giây" lỏng hơn hiện trạng (~5 giây / lịch) và spec tự nêu "~5 giây" là chỗ hơn TRIPO ⇒ đặt sàn theo mốc: không chậm hơn mốc cùng buổi quá 2 giây; lượt có gọi dự báo báo riêng.
- **m-6 — cỡ việc:** ba đợt ≈ 7 ngày agent + 0,55 USD, trước mốc đóng code 25–30/12, cùng lúc với B7 cuối, đợt kho 3, Exa, lưu trú. Đề nghị spec ghi **điểm dừng**: đợt 1 là phần bắt buộc; đợt 2, 3 mỗi đợt cần một câu "User chọn làm tiếp" sau khi xem kết quả đợt trước (không tự chạy nối). Kéo thả, tài khoản, tiếng Anh đã ghi "không làm" — tốt.

### Điểm đạt (ghi để khỏi sửa)
N2 (tiền, giờ, khoảng cách do code in; kiểm cuối cấm số của model) đúng bài học các lần tính tiền âm; không ô chữ tự do; hợp đồng `truong` giữ tương thích trường cũ (`di_cung`, `thong_tha`, `day_lich`, "4+") — khớp `ThamSo` / `GIA_TRI` hiện tại; bảng rà khung AI FDE đủ hai chiều; "bảng thiếu cột ⇒ ô tự ẩn" là đường phục hồi đúng.

## 3. Cách người kiểm chạy lại thật (0 USD)
Đếm cột của `diem_v3.json` bằng script chỉ in số; `grep` `ThamSo`, `HAN_CHE`, `GIA_TRI`; `scripts/grep_kb.sh --dir travel/places -l …` cho số bài có cảnh báo mùa / thứ hoạt động; `ls data/phase_9/t3_bang_ve_gio`; đọc plan lưu trú (L7) và spec kho 3 (Q3, Q4).

## 4. Kết quả quan sát
Các số trong mục 2 (m-1, m-4, M-2.2). Các khẳng định "hôm nay" ở mục 1 của spec (3 hàng biểu mẫu, 0 / 120, 7 / 28) **không kiểm lại** — lấy từ báo cáo đếm của C.

## 5. Giới hạn
Không chạy mô phỏng nào; không mở phiếu gộp và file recon TRIPO; không kiểm ước giờ / tiền.

## 6. Decision và bước tiếp theo
**changes_requested.** C sửa M-1, M-2 (và minor nếu tiện) thành bản 2; E xem lại riêng hai chỗ major (vòng cuối). E sẽ sửa plan lưu trú (L7) cho khớp sau khi A đồng ý đường kích hoạt thứ hai.
