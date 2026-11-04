# Review: Phase 9 — plan B4 (hỏi lại `hoi_lai`), bản 1

Decision: **changes_requested** (0 blocker · 2 major · 5 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-40`) · việc **C155** (A giao) · 19:22 03/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` sha **`a6d4140690d9`** (B140, untracked lúc review)
Cách review: chỉ dựa trên gói "Căn cứ để review" + lệnh chỉ đọc (`WORKFLOW.md` §9.1); không đọc STATUS / tin của B. 0 USD.
**Vai:** C là người viết bộ đo B4 (C143) ⇒ phần plan dùng bộ đo là C kiểm việc của chính mình ở chỗ đó — A lưu ý khi duyệt; phần thiết kế / tiêu chí của plan là việc B.

## 1. Phạm vi đã review

- Plan bản 1, cả 9 mục. Căn cứ, sha tính lại: spec `169c2dd5f86a` §3 (đoạn `hoi_lai`), §4, §5 B4 · `data/phase_9/bo_do_b4/README.md` **`c8b746bd3a29`** + `luat_ghi_truoc.md` `ec0fec8ebe64` + `chi_phi_hai_cach.md` `cad3697d014e` · plan B5 nháp `42afc1c7bc64` (dòng "Mã" + D1). Không mở `cau_sealed.jsonl`.
- Đếm bộ đã thấy (chỉ trường nhãn): 20 câu = `thieu` 10 · `du` 7 · `gan_giong` 3; `ky_vong` `hoi_lai` 10 / `tra_loi_thang` 10; trường `thieu_bat_buoc`, `truong_co` có — khớp plan §4.

## 2. Đối chiếu spec §5 B4

| Spec | Plan | Kết quả |
|---|---|---|
| danh sách trường cố định trong code; model chọn trường thiếu; `StopAtTools`; code dựng nút | D1, D2, D8, D10 | khớp |
| chi phí chỉ liệt kê giá có nguồn; chọn lại sau tra web + User đọc mẫu | D7 (Cách A, User 13:13) | khớp |
| quyết ≥ 8 / 10 đã thấy, ≥ 4 / 5 kín | Q2 | khớp con số; **cách đếm — M-1** |
| sàn: hỏi lại nhầm câu đủ ≤ 1 / 10; tỉ lệ trả lời thẳng trên bộ tuyến không giảm | Q3, Q4 | khớp (Q4 cần nhãn C — §4) |
| mức tụt lượt sau: **Đúng ≥ −0,1; 0 "nói chắc sai" mới** | Q6 (a) thước an toàn, (b) regex tổng | **đổi thước, không ghi "Lệch" — M-2** |
| giá trị trường chỉ nhận trong danh sách; không trường dữ liệu cá nhân | D4 (`Literal`, `extra="forbid"` ⇒ 422), §8 | khớp |
| hồi quy B3–B6: bộ riêng + 32 an toàn + mẫu Golden 30 | Q5 | khớp; m-1 |

## 3. Findings

### M-1 (major) — Q2 đếm "hỏi lại đúng" **sau** bước code tự điền trường bắt buộc (D3) ⇒ chỉ số quyết bị thổi lên
- **Vị trí:** D3 ("danh sách sau lọc rỗng ⇒ dùng trường bắt buộc của `loai`"); §4 dòng định nghĩa ("Hỏi lại đúng = có `clarify`, `loai` đúng, trường hỏi ⊇ `thieu_bat_buoc`"); Q2.
- **Tác động:** model gọi `hoi_lai` với trường sai (không thuộc `loai`) hoặc rỗng ⇒ code lọc hết ⇒ điền trường bắt buộc ⇒ `clarify` luôn ⊇ `thieu_bat_buoc` ⇒ Q2 tính **đúng** dù model chọn sai. Với câu lịch trình, trường bắt buộc chỉ có `so_ngay` ⇒ hầu như mọi lời gọi `hoi_lai(loai=lich_trinh, …)` đều "đúng". Chỉ số quyết đo code, không đo model.
- **Tiêu chí đóng:** Q2 đếm trên **tham số model gửi (trước D3)**: `loai` đúng **và** trường model chọn ⊇ `thieu_bat_buoc`; báo kèm số sau D3 và số lần D3 phải điền / cắt. Harness ghi cả hai (thô + sau lọc).

### M-2 (major) — Q6 thay thước mức tụt của spec mà không ghi "Lệch"; so "ý không có ≤ H0" giữa hai câu trả lời khác dạng không có nghĩa
- **Vị trí:** Q6 (a); §9 dòng "Q6 không có đáp án mẫu".
- **Bằng chứng:** spec §5 B4 "mức tụt lượt sau khi chọn: Đúng ≥ −0,1; 0 'nói chắc sai' mới" (bản 5 §5.4: "Accuracy TB theo cặp ≥ −0,1, judge cùng lượt mù"). Plan dùng thước an toàn (ý có / không có / trái so đoạn được trích) — hợp lý vì bộ C143 không có đáp án mẫu, nhưng là **đổi thước** và chỉ ghi ở §9, không nhãn **Lệch** / A quyết.
- **Tác động:** (1) người duyệt không thấy đây là chỗ lệch spec; (2) "ý không có ≤ H0": H0 gửi câu thiếu nguyên văn thường ra câu ngắn chung chung hoặc từ chối (ít ý), lượt ghép ra lịch / danh sách giá dài (nhiều ý) ⇒ đếm tuyệt đối gần như luôn ngược bên ghép, hoặc vô nghĩa khi H0 từ chối (0 ý) — sàn không đo được "nói chắc không nguồn" tăng hay không.
- **Tiêu chí đóng:** ghi **Lệch** + lý do (không đáp án mẫu ⇒ Accuracy theo reference không chấm được) để A quyết; sàn (a) đặt **không phụ thuộc độ dài**: vd "0 ý `trái`" + "0 ý `không có` về **giá / giờ / điều kiện** ở lượt ghép" (loại nói chắc sai nguy hiểm, thứ tự lỗi `Project_Status` §1), hoặc tỉ lệ ý `không có` / tổng ý ≤ tỉ lệ của mốc so sánh được — chọn một, ghi trước.

### m-1 — Q5 "câu bị hỏi lại ≤ 1 / 62" chưa loại câu hỏi lại **hợp lệ**
- Mẫu Golden 30 + an toàn 32 có thể có câu lịch trình / chi phí thiếu trường bắt buộc theo D2 (ví dụ câu dự trù chi phí không nêu số người) ⇒ `hoi_lai` đúng thiết kế nhưng bị đếm "bắt nhầm".
- **Đóng:** như Q4 — C gắn nhãn `can_hoi_lai` trên 62 câu **trước** khi chạy (chỉ nhãn), Q5 đếm câu bị hỏi lại ngoài nhãn.

### m-2 — Q3: câu `du` bị hỏi **trường không bắt buộc** có tính là hỏi nhầm không
- D1 cho model chọn mọi trường của `loai` (kể cả `di_cung`, `kieu_di`, `so_thich`); câu `du` (đã có `so_ngay`) mà model hỏi thêm sở thích ⇒ spec "hỏi lại nhầm câu đủ trường". Plan không nói rõ.
- **Đóng:** ghi một câu: mọi `clarify` ở câu `du` = hỏi nhầm (theo spec), kể cả chỉ hỏi trường không bắt buộc.

### m-3 — D4: câu ghép đi vào lần tìm đầu
- `lan_tim_dau: v0` tìm bằng câu gửi tới ⇒ câu ghép "<câu gốc> (Thông tin thêm: 2 ngày; 2 người; …)" vào `tim_kho` (BM25 + dense) ⇒ tầng tìm của lượt ghép khác câu gốc. Có thể có lợi hoặc hại; chưa có chỗ đo.
- **Đóng:** chọn và ghi trước: lần tìm đầu dùng **câu gốc** (phần ghép chỉ vào lời dặn / tin người dùng) — hoặc giữ ghép + theo dõi top-10 lượt ghép ↔ câu gốc trên 10 câu Q6.

### m-4 — Căn cứ để review ghi sha chung cho README + luật
- `ec0fec8ebe64` là sha của `luat_ghi_truoc.md`; README là `c8b746bd3a29`. **Đóng:** tách hai sha.

### m-5 — nhớ đã bật ở B3b (review C154 ready) ⇒ D5 / Q7 không còn "nếu"
- Với chỉ nhớ câu hỏi, lượt hỏi + lượt ghép đều lưu câu hỏi ⇒ lịch sử chứa câu gốc hai lần (lượt hỏi lại + câu ghép) — không sai, nhưng tốn token lịch sử và có thể làm định tuyến lượt sau lệch. **Đóng:** Q7 thành bắt buộc (3 chuỗi) khi mở nhánh sau B3b merge; ghi theo dõi `history_tokens` lượt sau.

### Đối chiếu nghiên cứu (A nhờ thêm, 19:23 03/11/2026 `date`) — câu hỏi cho A / User, **không** phải finding bắt B sửa

Nguồn: `data/nghien_cuu_phase_9_2026-11-01/báo cáo nghiên cứu github.txt` báo cáo 2 §4.1–§4.2 (dòng 370–400) + `data/nghien_cuu_tinh_nang_2026-11-03/tripo_v2/bao_cao_tripo_v2.md` (dòng 39, 55, 72). Hai ý là **dữ liệu** của nghiên cứu, không phải yêu cầu.

| Ý nghiên cứu | Plan B4 bản 1 | Nhận xét C |
|---|---|---|
| (Q-a) đầu vào tối thiểu **2 yếu tố** (thời lượng + sở thích), còn lại mặc định hợp lý, không hỏi | 4 trường lịch trình, **bắt buộc chỉ `so_ngay`** (D2); model *được* hỏi thêm trường khác | thực chất **gần** nghiên cứu (1 bắt buộc; sở thích không bắt buộc — B5 nháp D2 đã có mặc định công khai "di tích tiêu biểu"). Chỗ khác: model có thể hỏi thêm 2 trường không bắt buộc ⇒ đúng điều nghiên cứu cảnh báo (hỏi nhiều gây ức chế). Lựa chọn nhỏ: giới hạn `hoi_lai` lịch trình chỉ hỏi trường bắt buộc **+ tối đa 1** trường khác — ghi trước nếu A chọn; đo bằng "hỏi thừa" (Q2 theo dõi) |
| (Q-b) thiếu thông tin ⇒ **đưa ngay lịch / bảng mẫu + mời chỉnh** ("zero-friction"); TRIPO vòng 2: c05 lịch trình, c06 chi phí **đều trả lời trước rồi hỏi 2–3 ý cuối** | **không** trả lời tạm (D6 — `StopAtTools` dừng ngay; có nút "Trả lời luôn") | lý do D6 của B có căn cứ (trả lời tạm = thêm một lần sinh + đổi đường stream; chữ tạm không nguồn là lỗi TRIPO). Hệ quả cho người dùng: câu "lên lịch Huế giúp tôi" chỉ ra thẻ nút, chưa có gì để đọc. Hai đường cho A / User: (1) giữ D6 bản 1, đo tỉ lệ bấm "Trả lời luôn" khi chạy thật rồi mới quyết; (2) sau B5: lượt hỏi lại kèm **lịch mẫu do code dựng từ bảng điểm** (B5, có nguồn, mặc định công khai) — không cần thêm lần sinh tự do. C nghiêng (1) cho B4 + ghi (2) làm ứng viên sau B5 |

Ghi kèm cho plan B5 (không thuộc B4): báo cáo 2 §4.3 khuyên **không cam kết** "dự báo thời tiết thời gian thực" trong đề cương ⇒ củng cố đề xuất B5 nháp §2c (thời tiết tách bậc nhỏ sau B5, hoặc không làm).

## 4. Hai việc plan giao C trước khi chạy (B nhờ xem có hợp lý)

- **`chon_da_thay.json` (Q6):** hợp lý — giá trị chọn cho 10 câu thiếu do người không code đặt trước ⇒ B không chọn giá trị "dễ". C đề xuất luật: mỗi câu một bộ giá trị **hợp với câu** (vd câu nói "đi với bố mẹ" ⇒ `di_cung: nguoi_lon_tuoi`), trường bắt buộc luôn có, trường không bắt buộc chỉ điền khi câu gợi ý; phủ mỗi giá trị `so_ngay` ≥ 1 lần.
- **Nhãn `can_hoi_lai` trên bộ tuyến (Q4):** hợp lý và cần (B1 bộ tuyến viết trước khi có `hoi_lai`). Luật gán ghi trước: câu nhãn `tro_ly_hue` **là** câu lịch trình / chi phí **và** thiếu trường bắt buộc theo D2 ⇒ `can_hoi_lai`; còn lại không. Mở rộng cùng luật cho 62 câu Q5 (m-1). C làm sau khi plan bản 2 chốt D2 / D3 (để luật khớp trường cuối).

## 5. Cách người kiểm chạy lại

- `sha256sum` plan + 4 căn cứ (khớp, trừ m-4). Python chỉ đọc `data/phase_9/bo_do_b4/cau_da_thay.jsonl`: đếm `loai`, `ky_vong`, có trường `thieu_bat_buoc` / `truong_co`.
- Đọc spec §3 (đoạn `hoi_lai` + `StopAtTools`, `finish_answer_stream` ép `AnswerOutput`), §5 B4; spec bản 5 §5.4 (`git show 077e3cb:…`).

## 6. Độ đơn giản

Một công cụ enum + bảng nhãn trong code + ghép câu tất định; không trả lời tạm ở bản 1 (D6) — gọn, đúng spec. D3 (lọc / cắt / điền) là luật ranh giới cần thiết; chỉ cần tách khỏi phép đo (M-1). Không thấy over-engineering.

## 7. Decision và bước tiếp theo

**changes_requested** — B sửa M-1, M-2 (+ minor nếu muốn) thành bản 2, báo sha; C kiểm phần sửa; rồi A duyệt sha. Sau bản 2: C làm `chon_da_thay.json` + nhãn `can_hoi_lai` (§4).

## Vòng 2 — bản 2 `42fa62d2425f` (C155 · 19:42 03/11/2026 `date`)

Kiểm phần sửa (sha tính từ file; đọc mục "Chỗ đổi bản 2" + từng dòng sửa):

| Finding | Sửa | Kết luận |
|---|---|---|
| M-1 | §4 định nghĩa "hỏi lại đúng" = tham số **thô** của model trước D3; Q2 đếm theo đó, báo kèm số sau D3 + số lần D3 điền / cắt; D3 ghi harness lưu cả thô lẫn sau lọc | **đóng** |
| M-2 | Q6 nhãn **Lệch spec** + lý do (không đáp án mẫu), "A quyết"; sàn (a) 0 ý "trái" + 0 ý "không có" loại giá / giờ / điều kiện (2 judge, một trong hai — judge gắn loại ý), H0 chỉ báo kèm; (b) giữ | **đóng** (chờ A quyết Lệch) |
| m-1 | Q5 đếm ngoài nhãn `can_hoi_lai` C gắn trên 62 câu | đóng |
| m-2 | Q3: mọi `hoi_lai` ở câu đủ là nhầm | đóng |
| m-3 | D4: lần tìm đầu = câu gốc, câu ghép chỉ là tin người dùng | đóng |
| m-4 | căn cứ tách sha README `c8b746bd3a29` | đóng |
| m-5 | Nền + D5 (câu gốc lưu hai lần) + Q7 bắt buộc (3 chuỗi gõ chữ + 1 chuỗi bấm nút = 4, khớp bảng tiền) + `history_tokens` | đóng |

§10 (Q-a, Q-b) khớp đối chiếu nghiên cứu; A đã trả lời trong tin (giữ bắt buộc chỉ `so_ngay` + đếm "hỏi trường không bắt buộc"; giữ D6). Không thấy chỗ đổi ngoài các dòng trên.

**Decision vòng 2: ready_for_user_confirmation** — A duyệt sha `42fa62d2425f` (gồm quyết Lệch Q6). Sau duyệt: C làm `chon_da_thay.json` + nhãn `can_hoi_lai` (bộ tuyến 60 + 62 câu Q5) theo luật §4 của review này.

## Vòng 3 — bản 3 `507bd5b72ae9` (C166 · 19:49 04/11/2026 `date`)

Chỉ kiểm phần đổi so với bản 2 `42fa62d2425f` (A đã duyệt): sha tính từ file = `507bd5b72ae9`, `git show HEAD:<plan>` = `42fa62d2425f`; `git diff` 21+ / 6−, mọi hunk nằm trong danh sách "Chỗ đổi bản 3" (đầu file, căn cứ, D3, Q2, Q6k, theo dõi, §5 bước 5, §6, §7, mục cuối) — không thấy sửa ngoài danh sách. Căn cứ: `b144_review.md` §3 m-2 / m-3 + handoff dòng "C163 xong" / "C164 xong" (đọc), code `p9-b4` `c76934c` (đọc, 0 USD), dữ liệu `data/phase_9/b4/` (tính lại, 0 USD). **Không mở câu kín** (việc này chỉ kiểm phần đổi).

**Đã kiểm, khớp:**
- D3 đúng quyết định A (m-2): luôn thêm trường bắt buộc còn thiếu, kể cả danh sách rỗng; cắt > 3 theo thứ tự bảng ⇒ `so_ngay` (đầu bảng lịch trình) / `so_nguoi` + `so_ngay` (chi phí, chỉ 3 trường) không bao giờ bị cắt.
- "Dùng lại bằng chứng" đúng: trên `p9-b4` D3 chạy **trong** hàm công cụ, sau lời gọi của model; tham số thô ghi trước D3 (`backend/llm/assistant.py:249–250`); `StopAtTools` dừng ngay ⇒ kết quả D3 không quay lại model ⇒ Q2 / Q3 thô không đổi. C tính lại từ `hoi_lai_raw`: lượt hỏi có thô thiếu trường bắt buộc pilot **1 / 3**, v0 **2 / 9**, v1 **3 / 10** — **khớp** B. Q1 không bị chạm (D3 chỉ có khi cờ bật).
- Q6k đúng quyết định A (thước Q6: 0 ý "trái" + 0 ý "không có" loại giá / giờ / điều kiện, 2 judge "một trong hai"; (b) 0 con số tổng); §5 bước 5 + §7 "kín ngược chiều" nối đúng.
- Ngân sách token (m-3): harness `chay_b4.py` `9d0fb8d8a946` đã có `usage_tru_builder` (ghi mỗi dòng + `dem` in max / min); file v0 / v1 cũ không có trường ⇒ số đầu tiên ở lượt có phí kế. Ngưỡng 512 = mức B3 Q8 — hợp lý.
- Giá trị chọn đã thấy `chon_da_thay.json`: **10 / 10** câu thiếu có giá trị cho mọi trường bắt buộc thiếu ⇒ lượt ghép Q6 vẫn đủ ý khi thẻ D3 mới luôn có trường bắt buộc. Phần kín (`chon_sealed.json`): C kiểm ở bước 0 của việc kín, không ở đây.
- Tiền tới bản 3 tính lại: pilot 0,001625 + v0 0,012439 + v1 0,011549 = **0,0256** — khớp "≈ 0,026".

### M-1 (major) — §6: dự phóng theo giá thật đã chạm / vượt mốc dừng 0,11 trước khi B4 đo xong

- **Vị trí:** §6 dòng "Số thật tới bản 3" (mới ở bản 3) + bảng tiền.
- **Bằng chứng (tính lại từ `data/phase_9/b4/*.jsonl`, 0 USD):** lượt **trả lời** khi cờ bật ≈ **0,00075–0,00079 USD / câu** (v0 / v1; pilot 0,00044) ⇒ gần gấp đôi mức 0,0004 / câu bảng dùng cho Q4 / Q5; lượt **hỏi lại** ≈ 0,0004 (đúng ước). Dự phóng phần còn lại cộng 0,026 đã dùng:
  - thấp (Q4 / Q5 / Q6 / kín / Q7 / cổng theo bảng, thêm 1 lượt đã thấy 0,012): 0,026 + 0,012 + 0,024 + 0,025 + 0,008 + 0,006 + 0,004 + 0,005 ≈ **0,110** = đúng mốc dừng;
  - cao (lượt trả lời theo 0,00075; thêm 2 lượt đã thấy — handoff B145 định đo câu đủ v0 ↔ v1 × 2–3 lượt): ≈ 0,026 + 0,024 + 0,045 + 0,047 + 0,015 + 0,008 + 0,006 + 0,005 ≈ **0,176** > trần 0,12.
  - [Suy luận] câu đủ của bộ B4 là câu lịch trình / chi phí (trả lời dài) nên có thể đắt hơn câu Q4 / Q5 trung bình ⇒ số thật nằm giữa hai mức; chưa đo.
- **Tác động:** theo §6 "dừng > 0,11", lượt đo nhiều khả năng dừng giữa Q5 / trước kín ⇒ B4 dở, tiền đã chi không ra kết luận. Câu "báo A sau mỗi lượt" không thay một quyết định trước khi chạy.
- **Tiêu chí đóng:** §6 ghi dự phóng theo giá thật (lượt hỏi / lượt trả lời tách riêng) + một điểm quyết **trước** lượt có phí kế: A nới trần (ghi số) **hoặc** bớt phạm vi (ví dụ số vòng đo câu đủ thêm; thứ tự chạy để mọi sàn — Q3 / Q4 / Q5 / kín — xong trước phần báo kèm). Không đổi sàn / quyết.

### m-1 — Q6k "H0 chỉ báo kèm" nhưng không có lượt H0 kín trong bảng tiền / lệnh

- Q6 đã thấy có "10 ghép + 10 H0"; dòng "kín (C)" chỉ "10 câu + 5 ghép"; lệnh kín C164 không có lượt H0. **Tiêu chí đóng:** ghi rõ một trong hai: (a) **không** chạy H0 kín (đề xuất — Q6k là sàn tuyệt đối, H0 không vào quyết, tiết kiệm ≈ 0,004 + judge), hoặc (b) chạy 5 H0 kín (cờ tắt) + thêm vào dòng tiền.

### m-2 — D3: cờ `dien` / `cat` không ghi được khi cả hai cùng xảy ra

- Lịch trình có 4 trường: model chọn `[di_cung, kieu_di, so_thich]` ⇒ bản 3 thêm `so_ngay` ⇒ 4 ⇒ cắt còn 3 (bỏ `so_thich` model đã chọn). Code bản 2 `loc_truong` trả **một** giá trị `"dien" | "cat" | None` (`backend/llm/hoi_lai.py:48–56` trên `p9-b4`) ⇒ nếu giữ kiểu đó, số "D3 điền" báo kèm Q2 đếm thiếu. **Tiêu chí đóng:** plan ghi cờ là tập (`dien` + `cat` cùng lúc được) hoặc ghi rõ luật ưu tiên; test D3 có ca này.

**Ghi nhận (không phải finding):** `dem` hiện đếm "hỏi thừa" chỉ theo thô; Q2 bản 3 thêm "sau D3" ⇒ phần code harness, kiểm ở review nhánh.

**Decision vòng 3: changes_requested** — 0B / 1M / 2m. M-1 chỉ cần một dòng dự phóng + điểm quyết của A trong §6; m-1 / m-2 một câu mỗi cái. Sửa xong ⇒ C kiểm phần sửa.

## Vòng 4 — bản 4 `ca0a9f2faace` (C166 · 19:52 04/11/2026 `date`)

Sha tính từ file = `ca0a9f2faace`. Kiểm phần sửa theo mục "Chỗ đổi bản 4" + `git diff` với bản 2.

| Finding | Sửa | Kết luận |
|---|---|---|
| M-1 | §6 bảng dự phóng tách lượt hỏi / trả lời; C cộng lại: thấp 0,0256 + 0,081 = **0,106**, cao 0,0256 + 0,153 = **0,179** (khớp ≈ 0,106 / ≈ 0,178); (b) bớt lượt chọn + H0 Q6 ⇒ ≈ 0,098 / 0,146 (khớp); điểm quyết A (a) / (b) / (c) trước lượt có phí kế, A ghi trong handoff (sha giữ) | **đóng** |
| m-1 | Q6k: không chạy H0 kín | đóng |
| m-2 | D3: cờ là tập ⊂ {`dien`, `cat`}, ca vừa thêm vừa cắt có test | đóng |

### m-3 — thứ tự mới (kín trước Q4 / Q5) mâu thuẫn §5 và cần câu "sau khoá không chỉnh"

- §6 (dòng "Thứ tự chạy bản 4"): khoá ⇒ **kín** ⇒ Q6 ⇒ Q4 ⇒ Q5; nhưng §5 bước 4–5 vẫn "khoá ⇒ Q4, Q5, Q6 trên bản khoá" rồi mới "Kín".
- Đưa kín lên trước chỉ an toàn khi **sau khoá không chỉnh ghi chú nữa**. Bảng Q4 / Q5 ghi "Không đạt ⇒ âm" (đúng), nhưng §7 "Q3 / Q4 / Q5 phạm sàn sau 3 vòng chỉnh" đọc như được chỉnh sau khi Q4 / Q5 phạm ⇒ nếu chỉnh, bản cuối khác bản đã chạy kín, mà bộ kín chỉ mở một lần.
- **Tiêu chí đóng:** §5 bước 4–5 theo thứ tự §6; một câu "sau khoá không chỉnh; Q4 / Q5 / Q6 phạm ⇒ kết quả âm" (§7 sửa cho khớp: chỉnh chỉ trước khoá, trên đã thấy).

### m-4 — §7 "tiền > 0,11 USD" chưa theo điểm quyết §6

- Nếu A chọn (a) (dừng 0,17), §7 vẫn ghi dừng 0,11. **Tiêu chí đóng:** §7 ghi "tiền > mốc dừng A chọn ở §6".

**Decision vòng 4:** M-1, m-1, m-2 đóng; còn **2 minor câu chữ** (m-3, m-4) ⇒ **ready_for_user_confirmation sau khi B sửa m-3 + m-4** (chỉ §5 bước 4–5 + §7) — C kiểm nhanh phần sửa, rồi A duyệt sha + ghi lựa chọn (a) / (b) / (c).

## Vòng 5 — bản 5 `acfaf8ca0df5` (C166 · 19:54 04/11/2026 `date`)

Sha tính từ file = `acfaf8ca0df5`. `git diff -U0` với bản 2 (A duyệt): hunk chỉ ở đầu file, căn cứ, D3, Q2, Q6k, theo dõi, §5 bước 4–5, §6, §7 (2 dòng), mục "Chỗ đổi" — đúng các chỗ đã kiểm ở vòng 3–4 + phần sửa vòng này.

| Finding | Sửa | Kết luận |
|---|---|---|
| m-3 | §5 bước 4 "sau khoá không chỉnh nữa; một sàn phạm ⇒ âm"; bước 5 kín ngay sau khoá rồi Q6 ⇒ Q4 ⇒ Q5 (khớp §6); §7 tách: Q3 chỉnh ≤ 3 vòng trước khoá, sau khoá Q3 kín / Q4 / Q5 / Q6 / Q6k phạm ⇒ âm | đóng |
| m-4 | §7 "tiền > mốc dừng A chọn ở §6" | đóng |

**Decision vòng 5: ready_for_user_confirmation** — A duyệt sha `acfaf8ca0df5` + ghi lựa chọn tiền (a) / (b) / (c) của §6 vào `CURRENT_HANDOFF.md`.
