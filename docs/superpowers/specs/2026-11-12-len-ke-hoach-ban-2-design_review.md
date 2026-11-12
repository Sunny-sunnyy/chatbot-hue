# Review: Spec "Lên kế hoạch" bản 2 (nháp bản 1) — vòng 1

Decision: **ready_for_user_confirmation** sau vòng 2 (21:26 12/11/2026; bản 2 sha `8969c7275346`: 0 major, 1 ghi chú). Vòng 1: changes_requested (0 blocker, 2 major, 6 minor) — sửa chữ là đủ; vòng 2 chỉ xem hai chỗ major.
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

---

# Vòng 2 — bản 2 sha256 `8969c7275346` (21:26 12/11/2026, `date`) — vòng cuối

Decision: **ready_for_user_confirmation** (trình User duyệt spec + 4 câu ở mục 8). Chỉ kiểm hai chỗ major + bảng "Chỗ đổi".

| Finding | Kiểm | Trạng thái |
|---|---|---|
| **M-1** ngưỡng chưa ghi trước | mục 3 có đoạn "Cách đọc cột Tiêu chí": lớp **bất biến 100 %** ghi ngay ở từng dòng (các câu "Luôn"), lớp **sàn sản phẩm** 70 / 60 / 50 % "chỉ được nâng, không được hạ; dưới sàn ⇒ ô không hiện"; mô phỏng trước code chỉ để đếm dữ liệu và **đã có số đếm** trong spec | **đóng** |
| **M-2** lệch plan lưu trú + spec kho 3 | dòng "Lưu trú": đường kích hoạt thứ hai, nêu rõ là sửa plan lưu trú (E đã sửa L7 — plan `b24020ed9dc9`, A đồng ý); dòng "Bữa ăn": hai mức theo Q3 / Q4 của spec kho 3, không đủ cụm ⇒ không hiện; dòng "Đi lại": code chỉ nối khoảng cách, lời khuyên trích kho; mục 4 + 9.3 trỏ đúng file spec kho 3 và điều kiện "User đã trả lời Q1–Q5" | **đóng** |
| m-1 … m-6 | có trong bảng "Chỗ đổi"; E xem lướt các dòng tương ứng, không kiểm sâu | nhận |

**Ghi chú (không chặn, để plan đợt 1 lưu ý):** số đếm C vừa thêm cho thấy 3 / 8 cụm **không có điểm "ngắn" nào** và chỉ 4 / 8 cụm có ≥ 2 điểm ngắn ⇒ ô "kiểu đi 3 mức" có nguy cơ **dưới sàn 70 %** ở các lịch rơi vào cụm đó. Theo luật vừa ghi thì khi ấy ô không hiện — nên plan đợt 1 đếm điều này **đầu tiên** (trước khi code giao diện cho ô đó).

---

# Kiểm phần đổi của bản 3 — sha256 `16e9f7f4fa19` (21:38 12/11/2026, `date`) — A giao: chỉ bảng "Chỗ đổi so với bản 2"

Decision: **ready_for_user_confirmation** (0 major; 3 sửa chữ nhỏ để khớp spec kho 3 mà User đã chốt Q1–Q5). E đọc bảng "Chỗ đổi" + các dòng buổi tối / ăn uống / lưu trú của mục 3.2; không đọc lại phần giữ nguyên.

- **Khớp với spec kho 3 bản 2:** tên hai bảng và tên trường (`quan_theo_cum.json`, `luu_tru_theo_cum.json`), nhãn "chưa kiểm" cho quán dữ liệu mở, toạ độ ước chỉ mức "cùng cụm", 0 homestay được nói rõ, thẻ / khối lưu trú là đường kích hoạt thứ hai, buổi tối lấy từ bài kho đã có (không cần thêm kho).
- **c-1 (sửa chữ):** User đã chọn Q3 (thêm quán dữ liệu mở) + Q4 (hai mức toạ độ) ⇒ sàn ăn uống áp **mức B**; bỏ nhánh "mức A" hoặc ghi "không áp". Và ghi **danh sách "cụm trung tâm"** được tính sàn 80 %; **các cụm lăng** (dữ liệu mở cũng 0 quán) không tính — ngày ở cụm đó dùng dòng nói thật.
- **c-2 (sửa chữ):** bất biến "≤ 1,5 km điểm / khu của buổi đó" chỉ kiểm được với toạ độ chắc / vừa; quán toạ độ ước ⇒ điều kiện là **"cùng cụm"** (không so mét) — viết thành hai vế.
- **c-3 (đã có chủ):** bảng ánh xạ 8 cụm ⇒ 3 khu cho khối "Ở đâu": E giữ trong `khu_v1.json` (trường `cum`) của plan lưu trú; spec chỉ cần trỏ tới đó.
- Ghi chú cỡ việc (không phải finding): bản 3 bỏ điểm dừng giữa các đợt theo chốt của A; đợt 3 (ăn uống + lưu trú) phụ thuộc đợt bổ sung kho 3 đã vào kho ⇒ thứ tự cắt nếu trễ nên đặt đợt 3 cắt trước đợt 2.

---

# Kiểm mục 5c + "Chỗ đổi bản 3.2" — sha256 `3ea9bcb8bc10` (21:59 12/11/2026, `date`) — A giao: một vòng

Decision: **changes_requested — sửa chữ / số, không cần vòng nữa** (0 blocker; 2 chỗ **mâu thuẫn số** phải sửa trước khi B code; 4 ghi chú). E đọc 5c.1–5c.8, đối chiếu `backend/llm/lich_trinh.py` (`CUM_KE`, `CUM_XA`, `HAN_CHE`), `backend/llm/thoi_tiet.py` (`NGUONG_MUA`); không chạy mô phỏng.

## Mâu thuẫn phải sửa
- **S-1 — "tối đa 3 điểm / buổi" không bao giờ xảy ra với chính các con số của 5c.3.** 3 điểm ngắn cùng cụm = 75 × 3 + 15 × 2 = **255 phút > quỹ 240** (spec tự tính và ghi "không vừa — đúng ý: không nhồi"). Vậy trần thật là **2 điểm / buổi = 4 điểm / ngày** (mô phỏng: trung bình 3,24). Ba chỗ khác trong spec còn nói theo trần 3: dòng giải thích trên nút ở mục 5 ("~2 / ~4 / ~6 điểm một ngày"), mục 3 dòng "kiểu đi" ("khám phá nhiều tới 3 điểm ngắn / buổi"), và **định nghĩa chấm (3) ở 5c.7 ("khám phá 3–6")**. Tiêu chí đóng: chọn một — (a) giữ số phút, sửa chữ thành "tối đa 2 điểm / buổi", nút ghi "~2 / ~3 / ~4 điểm một ngày", định nghĩa (3) "khám phá 2–4"; hoặc (b) nới quỹ khám phá lên 255 nếu thật sự muốn 3 điểm ngắn (khi đó chiều kết thúc 17:45 > giờ đóng 17:30 ⇒ không khả thi buổi chiều). **E khuyến nghị (a).**
- **S-2 — định nghĩa chấm (3) và (4) ở 5c.7 không đạt được ở một số lịch hợp lệ** (E là người viết bộ đo nên phải nêu trước): (3) "khám phá 3–6 điểm / ngày" — số đếm của chính spec cho thấy 3 / 8 cụm **không có điểm ngắn** ⇒ ngày rơi vào cụm đó chỉ có 2 điểm dù chọn "khám phá"; (4) "mỗi sở thích có ≥ 1 điểm ưu tiên trong lịch" — lịch 1–2 ngày không được vào cụm xa (luật cũ, giữ) ⇒ sở thích nào có điểm ưu tiên **chỉ ở cụm xa** sẽ luôn trượt; nhóm hạn chế 1 ngày + 2 sở thích chỉ có 2 suất. Tiêu chí đóng: (3) đổi thành phép **đếm bằng code theo cặp** — "số điểm cả lịch: nhẹ nhàng ≤ cân bằng ≤ khám phá, và khám phá > nhẹ nhàng" (đã là bất biến của mục 3), người chấm không chấm ý này; (4) thêm ngoại lệ ghi rõ: "trừ khi mọi điểm ưu tiên của sở thích đó không xếp được theo luật cứng (cụm xa với lịch < 3 ngày, điểm bị bỏ theo mùa, hết suất của nhóm hạn chế) — khi đó lịch phải có ghi chú `thieu_so_thich`". **E sẽ viết bộ đo theo bản đã sửa này** (ghi rõ trong file bộ đo); C / A không đồng ý thì báo trước khi B code bước (b).

## Bất biến chưa đo được bằng mô phỏng đã chạy (180 lịch) — và cách đo
| Bất biến / sàn | Vì sao chưa đo | Cách đo (0 USD) |
|---|---|---|
| Mùa / mưa đổi khung hoặc ghi chú ≥ 60 % | 180 lịch **không có chiều "ngày đi"**; cột `mua_luu_y`, `ngay_hoat_dong` chưa có (v9) | mô phỏng 3.840 tổ hợp của 5c.7 sau khi có v9; **mưa** không mô phỏng được bằng dự báo thật ⇒ truyền hàm dự báo ghi sẵn (code đã nhận hàm dự báo làm tham số): 3 kịch bản — không mưa · mưa ngày 1 · mưa mọi ngày |
| 0 hoạt động tối sai thứ / sai giờ | cần v9 | cùng mô phỏng; đếm theo `thu` của từng ngày |
| Giờ in không vượt giờ đóng, các điểm trong buổi không chồng giờ | spec không nói 180 lịch đã kiểm | kiểm bằng code trên mọi tổ hợp: giờ kết thúc ≤ giờ đóng của bảng; giờ bắt đầu điểm sau ≥ giờ kết thúc điểm trước + phút đi |
| **"Điểm ưu tiên ở cụm xa xếp ngày 2" (C chưa mô phỏng; bản thử đang đặt ngày 1)** | luật mới | ba phép đếm trên mọi tổ hợp ≥ 3 ngày: (i) ngày 1 không có điểm cụm xa — 100 %; (ii) với sở thích có điểm ưu tiên ở cụm xa: điểm đó có mặt đúng **một** ngày trong {2…n} — đếm tỉ lệ, kỳ vọng 100 % trừ ngày bị bỏ theo mùa; (iii) **0 ngày rỗng** sau khi dời (ngày 1 phải được lấp bằng cụm gần) — so số điểm cả lịch trước / sau khi sửa luật, không được giảm |
| Sàn ≥ 80 % tối có hoạt động | cần v9 + phiếu nhỏ | mô phỏng theo hai phương án phiếu (User giữ đề xuất / User siết) — spec đã ước, cần số thật |

## Ghi chú (không chặn)
- **g-1 — hai luật mùa có thể đụng nhau:** (iii) "điểm ưu tiên không bị hạ" và (i) "`bo_khoi_lich: true` ⇒ không xếp". Điểm vừa ưu tiên vừa tạm dừng theo mùa ⇒ phải ghi rõ **(i) thắng** (không xếp điểm đang đóng) + ghi chú do code.
- **g-2 — "8:00 – 11:30 / 14:00 – 17:30" khớp nhau** (E tính lại: cân bằng 8:00 + 210 = 11:30; khám phá 7:30 + 240 = 11:30; chiều kết thúc 17:30). Lưu ý dữ liệu: kho ghi quần thể di tích mở 07h00 – 17h30 nhưng **không ghi giờ ngừng bán vé** ⇒ xếp tham quan kết thúc đúng 17:30 là sát; nên trừ 30 phút cho điểm cuối buổi chiều ở quần thể, hoặc ghi vào giới hạn.
- **g-3 — tốc độ:** sự kiện `lich_khung` đi trước lần gọi model ⇒ số "chữ đầu" trong `chat_metrics` đổi nghĩa ở lượt biểu mẫu; ghi rõ lượt biểu mẫu đo bằng hai mốc mới (khung · đủ câu) và không so với số chữ đầu cũ.
- **g-4 — kiểm "câu không chứa tên điểm khác":** cần danh sách tên + tên khác của mọi điểm; tên con nằm trong điểm lớn (một điện trong quần thể) sẽ bị bắt nhầm ⇒ lượt thử có phí sớm đếm thêm **tỉ lệ câu bị thay nhầm**, không chỉ thiếu / lặp / gộp.
- Khớp code hiện tại: ngưỡng mưa 60 % = `NGUONG_MUA`; ≤ 2 cụm kề / ngày và cụm xa từ 3 ngày = luật đang chạy; 3.840 tổ hợp = 5 × 2 × 2 × 3 × 16 × 4 (đúng).
