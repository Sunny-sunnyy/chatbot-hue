# Review: Phase 9 B5c — plan "tính tiền bằng code" (`tinh_tien`)

## Vòng 1 — plan bản 1 `65e43944e014` (B159, A giao; bản có dòng D5 "A quyết (a)" — A chỉ định review bản này, không review `d82e57a47174`)

Decision: **changes_requested** (0 blocker / 2 major / 6 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-48`)
Date: 10:15 05/11/2026 (`date`)
Người viết: C · file `docs/superpowers/plans/2026-11-05-phase-9-b5c-plan.md` (sha256 12 ký tự tính từ file lúc review)

### 1. Phạm vi đã review

Chỉ theo mục "Căn cứ để review" của plan; không đọc STATUS / tin nhắn của người viết.
- Plan: toàn bộ.
- Spec Phase 9 bản 12 (`77250689e605`, tính từ file): §11.1 dòng B5c + "Chi tiết để plan B5c" (§11.4), §11.2, §11.3, §11.5.
- `data/phase_9/tinh_tien/kiem_ke_gia.md` (`deb4a0eff9c8`, private) §1–§3; file chi phí du lịch (`travel/services`) **chỉ qua `scripts/grep_kb.sh --dir travel/services`** — các mục "Cách tính tổng", "Lưu trú", "Tham quan", 3 bảng dự toán, "Điều chỉnh theo quy mô nhóm". Không chép nội dung kho vào file này.
- Plan B4 bản 8 + report B4 §2e / §2f / §2g (B là người làm B4 / B4b — biết đường `hoi_lai`).
- Plan B5: căn cứ ghi **bản 5 `dff61a2db4e6`**; file hiện là **bản 6 `46c1ec1a8242`** (C182, User 10:07 05/11/2026) ⇒ B đọc D4b, D8 (3), D12, D14, **D15** của bản 6 (xem M-1, m-6).

### 2. Findings

| Mã | Mức | Vị trí | Vấn đề + bằng chứng | Tiêu chí đóng |
|---|---|---|---|---|
| **M-1** | major | D7, D11, §3 dòng `hoi_lai.py` / `conversations.py` / `full_corpus_prompt.py`, §8 dòng §4 | **Đi ngược quyết định của User lúc 10:07 "Merge cờ tắt + code tự hỏi", và lặp lại đúng kiểu đã làm B4b trượt.** D7 / D11 mở lại công cụ `hoi_lai` loại `chi_phi` để **model** quyết khi nào hỏi lại; cờ bật thì mọi lượt trợ lý được thêm công cụ `hoi_lai` + `tinh_tien` + `TINH_TIEN_TOOL_NOTE`. Bằng chứng: (1) plan B5 bản 6 D15 (User chọn 10:07) ghi "B4b cho thấy để model quyết hỏi (công cụ `hoi_lai` + lời dặn) làm đổi hành vi câu khác" ⇒ **code** quyết hỏi lại bên trong công cụ `lich_trinh`; B4b merge với `hoi_lai: false`; (2) report B4 §2g: B4b âm vì câu an toàn S03 / S09 thiếu cảnh báo nhiều hơn mốc sau khi thêm `HOI_LAI_NOTE` + công cụ vào mọi lượt. Plan B5c viết 10:06, trước quyết định đó, nên chưa theo kịp. Ngoài ra D7 phải lưu thêm `outcome` lượt vào `conversations.py` chỉ để chặn hỏi lần hai — việc này không cần nữa nếu code tự hỏi | Đổi D7 / D11 theo cách của B5 D15: **không** đưa công cụ `hoi_lai`. `tinh_tien` được gọi ⇒ code lấy `so_nguoi` / `so_ngay` theo D6 (nút ⇒ dò số trong câu hiện tại + câu gốc trong lịch sử) ⇒ thiếu ⇒ kết quả công cụ "cần hỏi" ⇒ dừng lượt (cùng cơ chế `tool_use_behavior` dạng hàm của B5 D12 (b) / D15) ⇒ route phát `clarify` loại `chi_phi` **chỉ với trường còn thiếu** ⇒ nút ⇒ lượt ghép có `truong` ⇒ không bao giờ hỏi lần hai. Bỏ phần `conversations.py` lưu `outcome` (D7), hoặc ghi rõ vì sao vẫn cần. §8 dòng §4 sửa theo. Q4 vẫn đo hồi quy vì `tinh_tien` + lời dặn công cụ vẫn thêm vào mọi lượt (xem m-5) |
| **M-2** | major | D1 (`loai = "ve"`, `diem`), D2 (bảng vé), D6 (người lớn / trẻ em), §3b ca vé | **Đường vé chưa được định nghĩa đủ để code và để kiểm**, trong khi luật cắt §7 (spec §11.4: "23/11 B5 chưa merge ⇒ B5c thu nhỏ còn vé") dựa đúng vào nó. `kiem_ke_gia.md` §1–§2: vé nằm ở **nhiều file** `travel/tickets` (6 file, 5 vào chỉ mục, ≈ 46 dòng bảng có số tiền nằm trong 4 file), mỗi file một dạng bảng. D2 chỉ ghi kiểm schema cho bảng dự toán. Plan thiếu: (a) danh sách file / bảng vé được nạp + cách kiểm schema lúc khởi động; (b) cách đổi tên điểm model gửi (`diem: list[str]`) sang đúng dòng bảng vé (khoá, bí danh, không khớp ⇒ làm gì); (c) **"trẻ em"**: điều kiện trẻ em / miễn vé khác nhau theo điểm (theo tuổi hoặc chiều cao — dòng "điều kiện" của bảng) ⇒ code không biết trẻ nào thuộc giá nào; D6 dò "2 người lớn 1 trẻ em" rồi nhân là đoán điều kiện | D2 thêm mục vé: liệt kê file / bảng nạp, schema (cột giá người lớn / trẻ em / miễn, ngày hiệu lực), lỗi ⇒ không khởi động. D1 thêm luật khớp tên (NFC + casefold + bí danh, giống B5 D2 `khop_diem`); không khớp ⇒ câu cố định, không đoán. Trẻ em: bảng vé **in nguyên điều kiện** của dòng; code chỉ nhân khi người dùng cho số trẻ **và** dòng chỉ có một mức giá trẻ em; còn lại thì liệt kê, không ra tổng. Thêm ca test cho từng ý |
| m-1 | minor | D2 "đủ 3 bảng × 6 hạng mục"; §7 điều kiện dừng 1 | Kho có **bảng 1 ngày 5 hạng mục** (không có lưu trú — kho ghi một ngày không bắt buộc lưu trú); bảng 2N1Đ, 3N2Đ có 6 hạng mục [đếm qua `grep_kb.sh`]. Kiểm "3 × 6" sẽ báo lỗi nhầm và làm dừng việc theo §7. **Tổng kho = tổng cộng từ hạng mục: khớp 9 / 9 ô** (3 bảng × 3 mức, cộng riêng cận thấp / cao — B tính 0 USD, chỉ in khớp / lệch) | sửa D2 thành 5 / 6 / 6 hạng mục; ca test parser dùng đúng số này |
| m-2 | minor | §3b ca "đi 3 ngày, ngày thứ 2 nghỉ" và "… 2 ngày 2 đêm" | Kỳ vọng không khớp mẫu dò D6: (a) mẫu `(\d+|một…mười) ngày` chỉ khớp "3 ngày" ("ngày thứ 2" không có dạng "2 ngày") ⇒ dò ra **3**, không phải "nhiều giá trị ⇒ không dò"; (b) D6 chỉ có mẫu đêm dạng viết tắt `NĐ`; dạng viết đủ "2 ngày 2 đêm" sẽ dò ra 2 ngày, không ra "ngoài phạm vi" | sửa kỳ vọng ca (a) (ngày 3) hoặc thêm mẫu cho "ngày thứ N"; thêm mẫu "X ngày Y đêm" vào D6 (đêm ≠ ngày − 1 ⇒ ngoài phạm vi) |
| m-3 | minor | D3, D6 (dự toán có trẻ em) | Kho (mục gia đình có trẻ nhỏ) dặn hỏi trực tiếp phụ thu trẻ em; bảng tính theo người. Plan chưa nói câu dự toán "2 người lớn 1 trẻ em" thì `so_nguoi` = 3 hay = 2 kèm câu lưu ý | ghi một luật (vd đếm đủ người + câu cố định "trẻ em có thể khác — kho không ghi số") + một ca test |
| m-4 | minor | §6 | Bảng tiền tự ghi: đủ 2 vòng chỉnh ≈ 0,09–0,12 USD, **vượt trần đề xuất 0,10**. B4b phải xin A hai lần giữa lượt vì dự phóng vượt trần | ghi sẵn điểm quyết A (như plan B4 bản 4 §6): (a) nới trần, hoặc (b) giữ trần và bớt lượt (nói rõ bớt lượt nào) — A chọn khi duyệt sha |
| m-5 | minor | Q4 "sai điều kiện / thiếu cảnh báo mới ≤ mốc (như B4b)" | Ở B4b luật thủ tục S-AT do A viết **giữa lượt** (sau khi thấy 2 > 1). Cờ bật vẫn thêm công cụ + lời dặn vào mọi lượt trợ lý (cùng loại rủi ro với B4b, kể cả sau khi sửa M-1) | ghi luật S-AT trước khi đo: câu an toàn mới bị sai điều kiện / thiếu cảnh báo ⇒ sinh lại 3 lần bản B5c + 3 lần mốc cờ tắt, 2 judge mới; đạt khi B5c ≤ mốc ở mọi câu; phạm ⇒ âm, không thêm vòng |
| m-6 | minor | "Căn cứ để review" dòng plan B5; §3 dòng `do_so.py` | (a) Căn cứ trỏ B5 **bản 5 `dff61a2db4e6`**, file hiện là **bản 6 `46c1ec1a8242`** (có D15 code tự hỏi). (b) §3 ghi `backend/llm/do_so.py` "(mới ở B5 D12)", nhưng bảng file của B5 (bản 6) **không có** `do_so.py` (B5 D12 dò số ngày; file mới chỉ có `lich_trinh.py`, `so_tien.py`) ⇒ chưa rõ ai tạo module dò số chung | sửa căn cứ theo bản B5 hiện hành; ghi rõ: B5c tạo `do_so.py` (chuyển hàm dò số ngày của B5 sang, test cũ giữ nguyên), hoặc nhờ B5 tạo — một chỗ dò số, không hai bản |

**Đã kiểm, khớp (không phải finding):**
- **Ánh xạ spec §11.2:** S1 ⇒ Q2, S2 ⇒ Q2, S3 ⇒ Q3 (g2 + ≥ 3 chuỗi mới, có chuỗi gõ chữ không số), S4 ⇒ Q4 (đủ 4 số, câu ngoài kho 0), S5 ⇒ Q1, quyết ⇒ Q5 (≥ n − 1 / n, đã thấy 8 / kín 4) — đủ.
- **Chữ kho cho D3 / D4 / D5** [đọc qua `grep_kb.sh`]: D3 — kho dặn tính riêng từng cận, không lấy trung bình; khoản tính theo người nhân đủ số người, chỉ chia khoản dùng chung ⇒ khớp. D4 — mục tham quan dặn dùng một khoản dự toán cho cả chuyến, không chép giá từng điểm ⇒ khớp ("một khoản một lần", spec §11.4). D5 — ô lưu trú một đêm mức tiêu chuẩn đúng bằng nửa khoảng giá phòng tầm trung; mức tiết kiệm **không** khớp nửa giá phòng bình dân; ghi chú dưới bảng 2N1Đ về chia tiền phòng; mục người đi một mình dặn không giả định có người chia ⇒ suy luận của C đúng với số kho, và (a) "giữ số kho + câu lưu ý do code nối" (A quyết) không đưa giả định ngầm vào số.
- Chặn hỏi lần hai chỉ `chi_phi` (spec §11.1) có trong plan (D7) — sau khi sửa M-1 thì tự có theo thiết kế (lượt ghép luôn có `truong`).
- D9 kiểm tiền bằng code (không dùng judge) — đúng bài học B4 (judge coi phép nhân là "có"); dùng chung `so_tien.py` của B5 (có trong bảng file B5 bản 6).
- Luật cắt (spec §11.4) và quỹ B7 (§11.5) có ở §6 / §7.

### 3. Cách người kiểm chạy lại thật

0 USD, chỉ đọc: `sha256sum` plan / spec / B5 plan / `kiem_ke_gia.md`; `scripts/grep_kb.sh --dir travel/services` (đầu mục, tên hàng bảng, các đoạn luật); một script tạm trong `/tmp` (đã xoá) đọc các dòng bảng do `grep_kb.sh` in ra rồi cộng từng cận, **chỉ in "khớp / lệch" + số hạng mục**. Không gọi API.

### 4. Kết quả quan sát

- Bảng 1 / 2 / 3: số hạng mục 5 / 6 / 6; tổng khớp 3 / 3 mức ở cả ba bảng.
- B5 plan hiện hành `46c1ec1a8242` (bản 6) có D15 "code tự hỏi khi thiếu số ngày".

### 5. Giới hạn hoặc phần chưa chạy

- Không đọc chi tiết các bảng vé trong `travel/tickets` (M-2 dựa trên số đếm của `kiem_ke_gia.md`); người sửa nên dùng `grep_kb.sh --dir travel/tickets` để liệt kê bảng thật.
- Không chạy được kiểm regex D6 (module chưa có) — m-2 suy từ mẫu ghi trong plan [Code, chưa chạy].

### 6. Decision và bước tiếp theo

**changes_requested.** C sửa M-1 (code tự hỏi như B5 D15, bỏ công cụ `hoi_lai` loại `chi_phi`), M-2 (định nghĩa đường vé) và các minor, rồi báo sha mới. B kiểm phần sửa. M-1 đổi thiết kế đường hỏi lại ⇒ A nên xem lại D7 / D11 trước khi duyệt sha.

## Vòng 2 — kiểm phần sửa, plan bản 2 `89b67bfb24a5` (= `549c2fe19a0d` + dòng A quyết tiền §6 + dòng trạng thái; C nhờ trực tiếp)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 0 minor mới)
Người kiểm: B (`hue-rag-48`) · Date: 10:25 05/11/2026 (`date`) · sha tính từ file lúc kiểm.

| Finding vòng 1 | Bản 2 | Kết quả |
|---|---|---|
| **M-1** mở lại `hoi_lai` cho model | D7 viết lại: `tinh_tien` được gọi ⇒ code lấy số người / ngày (D6) ⇒ thiếu ⇒ dấu "cần hỏi" ⇒ `tool_use_behavior` dạng hàm (chung với B5 D15) ⇒ `clarify` loại `chi_phi` chỉ trường thiếu; không công cụ `hoi_lai`, không lời dặn hệ thống (D1, D11); bỏ `conversations.py`; lượt mang `truong` không hỏi lần hai, "Trả lời luôn" ⇒ 1 người 1 ngày tạm + dòng giả định; Q1m (chỉ khác `main` một mục `tinh_tien`), Q2a (gọi công cụ ≥ 7 / 8, kín ≥ 3 / 4), Q3 thêm chuỗi "Trả lời luôn"; D11 có `TINH_TIEN_TOOL_OVERHEAD` như B5 D16 | **đóng** |
| **M-2** đường vé | D2b: chỉ bảng vé lẻ file vé Quần thể. B kiểm chữ kho qua `grep_kb.sh --dir travel/tickets` (chỉ tên cột / số dòng): bảng **12 dòng**, cột trẻ em có điều kiện **7–12 tuổi** ở tiêu đề, dòng **ngày có hiệu lực** ở đầu file — khớp chữ plan. Khớp tên: B so 11 điểm `quan_the` của `diem_v3.json` với ô tên của 12 dòng ⇒ **11 / 11 khớp được** bằng `ten` hoặc bí danh trong ngoặc của ô tên (vd ô "Lăng vua <tên> (<tên chữ>)" ↔ `ten_khac` cùng tên chữ); dòng còn lại không thuộc bảng điểm (không cần khớp). Trẻ em: chỉ nhân khi có số; không rõ ⇒ không tổng; vé gộp / ngoài Quần thể ngoài phạm vi, có câu cố định | **đóng** |
| m-1 5 / 6 / 6 hạng mục | D2 + §7 | **đóng** |
| m-2 ca dò lệch mẫu | D6 thêm mẫu "X ngày Y đêm"; §3b "ngày thứ 2" ⇒ 3; thêm ca nhiều giá trị thật ("3 ngày hay 4 ngày") | **đóng** |
| m-3 dự toán có trẻ em | D3: đếm đủ người + câu cố định theo mục gia đình có trẻ nhỏ của kho | **đóng** |
| m-4 tiền vượt trần | §6 điểm quyết; **A quyết (a) trần 0,14 / dừng 0,13** + A xin User trước lượt có phí đầu nếu (2,0 − đã dùng − quỹ B7) < 0,14 | **đóng** |
| m-5 S-AT ghi trước | Q4: 3 + 3, 2 judge mù, đạt ⇔ B5c ≤ mốc mọi câu, nhiều hơn ⇒ âm | **đóng** |
| m-6 căn cứ B5 cũ, `do_so.py` | căn cứ trỏ B5 bản 7 `b572443dc9cd`; B5c tạo `do_so.py` | **đóng** — ghi chú phối hợp: B đang code B5 (B160) sẽ đặt hàm dò số ngày **ngay trong `backend/llm/do_so.py`** từ đầu (B5 chỉ dùng số ngày; B5c thêm số người) để B5c khỏi phải chuyển; B ghi lệch nhỏ này trong report B5 |

**Kết luận:** mọi finding vòng 1 đóng, không finding mới ⇒ **ready_for_user_confirmation** — A duyệt sha `89b67bfb24a5`. Code B5c chỉ sau khi B5 merge (plan §1).

### Vòng 2b — 3 sửa nhỏ, `bab730a57798` (B, 10:28 05/11/2026)

**ready_for_user_confirmation** (0 / 0 / 0). (1) "Trả lời luôn" chỉ đặt tạm trường **vẫn thiếu sau D6** — đúng ý (câu gốc có số ngày thì giữ), khớp tinh thần B5 D15. (2) Chuỗi "cả nhà" (gõ chữ không số) thành theo dõi — đúng: spec §11.2 S3 nói về người dùng **gõ số** sau thẻ; không có số thì hỏi lại là hành vi đúng, không phải lỗi. (3) `do_so.py` do B5 tạo — khớp tin phối hợp của B. Không đổi chỗ khác.
