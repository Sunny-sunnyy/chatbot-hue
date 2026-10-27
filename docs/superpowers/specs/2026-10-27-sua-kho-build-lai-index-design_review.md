# Review: spec đợt sửa kho + build lại index (bản sha `725bbe15d044`)

Decision: **changes_requested** (0 blocker / 2 major / 5 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-86`) · 15:25 27/10/2026 (`date`) · Việc: A giao C68. 0 USD, chỉ đọc. sha C tính lại từ file lúc đọc và lúc ghi: `725bbe15d044`.
Spec do A viết; Q1–Q5 §4 User đã chốt — review **không** bàn lại lựa chọn của User, chỉ kiểm quy trình / tiêu chí / quyền / dữ liệu.

## 1. Phạm vi đã review

- Spec: toàn bộ (106 dòng). Đối chiếu: `guides/full_corpus_rag.md` mục "Build lại index khi corpus đổi" (code làm gì + bước 1–7), `Project_Status.md` §8 (bẫy),
  `backend/tests/test_full_corpus_chunker.py` (test đếm file / đoạn).
- Kiểm bằng máy, chỉ đọc, **chỉ in số đếm** (script tạm, không ghi file): giao giữa 123 edit đợt 1 (41 mục B73 trừ K091 + 14 edit `diffs_them`) với (a) `data/phase_8_1/gold/gold_v3.jsonl`
  (offset), (b) `knowledge-base-hue/meta/full_corpus_conditions.json`, (c) `knowledge-base-hue/meta/chunker_acceptance_samples.json`. Không đọc Golden, câu kín.
- (4) Nội dung kho: đọc cả spec + `.githooks/overlap_scan.py` ⇒ **0 trùng**; spec chỉ có quy trình, số đếm, mã mục, đường dẫn private — **đạt**.

## 2. Findings

### M-1 (major) — nhãn đoạn đúng (gold v3) tính theo vị trí ký tự sẽ lệch sau khi sửa kho; spec không có bước xử lý

- **Vị trí:** §5 (không bước nào), §6 (tiêu chí), §8 (rủi ro chỉ có "Golden lệch kho").
- **Bằng chứng:** `gold_v3.jsonl` lưu `start` / `end` theo ký tự trong file kho; hàm đếm (`experiments/phase_8_1/g1_retrieval.py` `chunk_hits_quote`) so khoảng đó với
  `evidence_parts` của đoạn. Đếm của C: **24 câu** gold có trích dẫn trong file bị sửa; **66** trích dẫn nằm **sau** một edit đổi độ dài trong cùng file (lệch offset);
  **3** trích dẫn bị edit **chồng lên** (chữ trích dẫn đổi ⇒ không còn khớp nguyên văn).
- **Tác động:** sau build, mọi số `*_gold_*` (tầng tìm — kể cả plan Qwen3-8B ở bước 9, "đo tầng tìm trước") sai hoặc báo lỗi; T1 mới không đo được "đoạn đúng".
- **Tiêu chí đóng:** thêm một bước (sau bước 2, trước bước 6): dựng nhãn bản mới (`gold_v4`) bằng cách tìm lại trích dẫn nguyên văn trong file đã sửa (như `build_gold_v2/v3.py`:
  đúng 1 lần, offset đúng); 3 trích dẫn bị chồng ⇒ người khác người sửa đề xuất trích dẫn mới, User duyệt (như Q5); `GOLD_PATH` đổi cùng lúc; v3 giữ nguyên để tái lập
  số cũ. Ghi vào §6 tiêu chí ("nhãn bản mới 0 lỗi offset") và §8 rủi ro.

### M-2 (major) — mốc "trước" của phép so 176 câu chưa được định nghĩa, và với cách thay **tại chỗ** phải có **trước** khi xóa index

- **Vị trí:** §5 bước 6 ("chạy 176 câu + judge mù cùng lượt so trước ↔ sau"), §6 dòng 88–89, Q3 (tại chỗ).
- **Bằng chứng:** spec không nói câu trả lời "trước" lấy từ đâu (lượt B1 / lượt sau merge B1 / chạy lại); bước 5 xóa collection rồi build lại đúng tên ⇒ sau bước 5 không còn
  index cũ để sinh lại (chỉ còn snapshot). Nếu Golden đổi (Q5), câu trả lời "trước" chấm bằng Golden mới sẽ bị trừ ở đúng các câu mà kho đã sửa ⇒ "sau" thắng giả; chấm bằng
  Golden cũ thì "sau" thua giả.
- **Tác động:** tiêu chí "không làm hỏng" (§6) không tính được hoặc lệch có hệ thống.
- **Tiêu chí đóng:** ghi trước: (1) bộ "trước" = lượt sinh nào, commit / cấu hình nào (cùng context 10 sau merge B1), sinh **trước bước 5** nếu cần sinh mới; (2) cả hai bên chấm
  cùng lượt mù với **cùng** Golden (bản đã sửa theo Q5); (3) câu có Golden đổi hoặc chạm file đã sửa báo **riêng** (không tính vào "số câu tụt" chung, hoặc tính với luật riêng
  ghi trước); (4) con số A/A dùng cho "A/A + 3" và nguồn của nó.

### m-1 — mẫu test chunker đọc nguyên văn kho sẽ có chỗ không khớp

- **Bằng chứng:** `chunker_acceptance_samples.json` (private, `Project_Status.md` §8: 7 test mẫu chunker đọc chuỗi kỳ vọng từ file này) nhắc tên **3** file bị sửa; **2** edit có
  chuỗi cũ nằm trong file mẫu. `full_corpus_conditions.json`: 0 file / 0 edit chạm (đạt).
- **Tiêu chí đóng:** bước 3 / 4 thêm: chạy `tests/test_full_corpus_chunker.py` (mẫu) sau khi áp; mẫu lệch vì kho sửa ⇒ cập nhật file mẫu (private, có backup) — ghi quyền ở §7.

### m-2 — bước 5 chỉ nhắc xóa sparse state; guide yêu cầu xóa đủ ba

- **Bằng chứng:** guide bước 4(a): xóa collection + build record + sparse state; còn collection / record ⇒ build dừng ở bước kiểm đích; sparse state khác byte ⇒ dừng.
  Spec bước 5: "theo guide bước 4a–6; xóa sparse state cũ trước".
- **Tiêu chí đóng:** bước 5 liệt kê đủ ba đích xóa (đúng tên) + "liệt kê đích thật trước khi xóa, khác danh sách ⇒ dừng" (`WORKFLOW.md` §3.4).

### m-3 — thời điểm chatbot ngừng phục vụ ghi chưa đúng

- **Bằng chứng:** `Project_Status.md` §8: sửa corpus làm runtime **từ chối khởi động** (freshness) cho tới khi build lại ⇒ từ bước 2 (áp sửa), mọi lần khởi động lại API / harness đều
  lỗi 409, không chỉ "khi build" (§8 rủi ro).
- **Tiêu chí đóng:** §8 ghi "từ bước 2 tới hết bước 5"; bước 2–5 làm liền trong một phiên.

### m-4 — §7 quyền thiếu vài thao tác ghi đã có trong §5 / Q5

- Thiếu: sửa `backend/config/settings.yaml` + test (code — ai sửa, ai review, A commit); sửa Golden (Q5 — ai đề xuất, User duyệt, backup); sửa nhãn đoạn đúng (M-1) và file mẫu chunker
  (m-1); ghi `knowledge-base-hue/meta/` (backup); điều kiện dừng / khôi phục từ snapshot (build lỗi giữa chừng thì làm gì).
- Tiền: 176 câu context 10 ≈ 0,037 USD (C tính: 0,00021 × 176); nếu phải sinh lại bộ "trước" (M-2) ≈ +0,037 ⇒ ≈ 0,074; thêm một lượt A/A ⇒ ≈ 0,11 > trần 0,10. Ghi rõ có / không
  A/A và trần tương ứng.

### m-5 — mốc T1 mới cần ghi sha và thay chỗ đang dùng mốc cũ

- **Bằng chứng:** spec bước 6 "T1 mới làm mốc tìm mới"; nhiều plan / guide / handoff đang trỏ T1 `cefb2d1ad609` (B71, B3 plan §5 bước 3 dùng T1 giống byte làm điều kiện dừng).
- **Tiêu chí đóng:** bước 6 ghi sha T1 mới; bước 7 thêm: cập nhật chỗ trỏ T1 cũ (ít nhất `Project_Status.md`, `CURRENT_HANDOFF.md`, guide); T1 cũ giữ làm hồ sơ cho số trước đợt.

## 3. Đạt (không cần sửa)

- (1) Thứ tự bước khớp guide: backup kho vào `meta/` (guide 1) — bước 1; chia đoạn thử chỉ đọc + 3 tokenizer, huydang 256 (guide 2) — bước 4; snapshot + bản sao record / sparse state
  (guide 3) — bước 1; tại chỗ (guide 4a) — bước 5; lệnh build từ `backend/` (guide 5); kiểm sau build + 4 chỗ báo cáo + `Project_Status` §4 (guide 6) — bước 6–7; dọn khi User duyệt
  (guide 7) — bước 8. Test đếm file / đoạn (`test_full_corpus_chunker.py:941-949`) đọc số từ build record ⇒ tự khớp sau build (không ghi cứng 205 / 8.459).
- Thứ tự với 8.2 (§2) đúng lý do (B3 so cùng kho); K091 không áp vì file danh mục bị loại — nhất quán với C66.
- (4) Không chứa nội dung kho (trên).

## 4. Giới hạn

- Không kiểm từng câu Golden chạm fact đã sửa (Q5 là bước riêng; C không đọc Golden).
- Số M-1 / m-1 đếm theo chuỗi `old` ở file hiện tại; 16 câu User trả lời chưa có edit nên chưa tính — sẽ thêm chạm.

## 5. Decision và bước tiếp theo

`changes_requested`: A sửa thành bản mới (M-1, M-2 bắt buộc; minor nên gộp), báo sha ⇒ C kiểm phần sửa ⇒ User duyệt sha.

## Vòng 2 — kiểm phần sửa (bản 2, sha `cad3d25cffef`, commit `3d53370`)

Decision vòng 2: **ready_for_user_confirmation** (0 blocker / 0 major / 3 minor mới — không chặn; A sửa thì là bản mới, C kiểm lại phần đó)
Date: 15:28 27/10/2026 (`date`). C tính lại sha từ file: `cad3d25cffef`. Đọc `git diff fa192f8 3d53370` của spec (chỉ phần sửa + đường bị ảnh hưởng). Overlap scan spec bản 2: 0 trùng.

| Finding vòng 1 | Bản 2 | Kết quả |
|---|---|---|
| M-1 gold offset | Bước 5 gold v4 (tìm lại nguyên văn, đúng 1 lần, từ chối ghi đè; 3 trích dẫn bị chồng ⇒ đề xuất + session khác kiểm + User duyệt; `GOLD_PATH` ⇒ v4; v3 giữ); §6 "Gold v4: 0 trích dẫn mất"; §7 quyền; §8 rủi ro; bước 12 (8B) đo theo v4 | **đóng** |
| M-2 bộ "trước" | Bước 0: sinh 176 câu trên chatbot cuối 8.2 + index hiện tại **trước khi đụng kho**, plan đo ghi trước + review trước bước 0; bước 9: hai bộ chấm cùng lượt mù, **cùng Golden đã sửa**, câu chạm fact báo riêng; §6 A/A = 2 | **đóng** (luật cụ thể cho câu chạm fact để plan đo ghi trước — chấp nhận) |
| m-1 mẫu chunker | Bước 4 + §6 "test mẫu chunker đạt" + §7 quyền sửa file mẫu | **đóng** |
| m-2 xóa đủ ba | Bước 6 | **đóng** |
| m-3 ngừng phục vụ | Bước 1: từ bước 2 khởi động lại bị từ chối, làm 2–6 liền | **đóng** (bảng §8 vẫn ghi "Chatbot ngừng khi build" — xem n-3) |
| m-4 quyền / dừng / tiền | §7 đủ thao tác ghi; mục "Dừng + khôi phục"; hai lượt ≈ 0,074 USD, trần 0,15 (không A/A mới) | **đóng** (khôi phục thiếu một phần — n-2) |
| m-5 T1 | Bước 7: ghi sha mới, thay chỗ tracked trỏ `cefb2d1ad609`, plan B3 giữ (đã chạy trước) | **đóng** |

### n-1 (minor) — nguồn của "A/A = 2" ghi chưa đúng

- §6 ghi "A/A = 2 (cận trên đã dùng ở plan B3, cùng cấu hình context 10)". Số 2 của plan B3 là quy về **33 câu**, ghép nhiễu context 5 (7B Run 1 ↔ 2) với context 10. Phép so ở đây
  là context 10 ↔ context 10 trên **176 câu**: nguồn đúng là A/A B1 ↔ G2.1a 176 câu (`phase_8_2_b1_implementation.md` §4 trên `p82-b1`): câu tụt Completeness **1**, Accuracy **2**
  (câu đổi điểm 5 / 5). Con số 2 vẫn đứng được (= cận trên của hai chỉ số) — chỉ cần sửa câu dẫn nguồn (và ghi rõ đếm trên 176 hay trên tập số chính).

### n-2 (minor) — "khôi phục" chưa hoàn lại các thay đổi ngoài kho / Qdrant

- Mục "Dừng + khôi phục" chỉ nêu file kho từ `meta/` + snapshot + build record + sparse state. Nếu dừng sau bước 3–5 còn phải hoàn lại `settings.yaml` (`exclude_files` — nếu không,
  discovery ra 204 file trong khi build record khôi phục ghi 205 ⇒ runtime từ chối), file mẫu chunker (bước 4) và `GOLD_PATH` (bước 5).
- **Tiêu chí đóng:** thêm ba mục đó vào danh sách khôi phục (code: `git checkout` đúng file / revert commit; mẫu chunker: từ backup `meta/`).

### n-3 (minor) — bước 5 có User duyệt nằm trong cửa sổ "làm 2–6 liền"

- Bước 1 yêu cầu bước 2–6 làm liền (khởi động lại bị từ chối), nhưng bước 5 cần User duyệt 3 trích dẫn mới ⇒ có thể kéo dài thời gian không khởi động lại được. Build (bước 6)
  không phụ thuộc nhãn đoạn đúng.
- **Tiêu chí đóng:** cho phép bước 5 (phần User duyệt) làm sau bước 6 — chỉ cần xong trước mọi lần đo tầng tìm theo nhãn; hoặc ghi rõ User duyệt ngay trong phiên. Sửa dòng §8
  "Chatbot ngừng khi build" thành "không khởi động lại được từ bước 2 tới hết bước 6".

## Vòng 2 — kết luận

Hai major và năm minor vòng 1 đều đóng. Ba minor mới không đổi quy trình chính; A có thể sửa trước khi trình User (bản mới, C kiểm phần sửa) hoặc trình bản 2 kèm ghi chú.

## Vòng 3 — kiểm phần sửa (bản 3, sha `bc8ddfd80694`, commit `d1d6b96`)

Decision vòng 3: **ready_for_user_confirmation** (0 / 0 / 1 chữ — không cần vòng sửa riêng). Date: 15:30 27/10/2026 (`date`). C tính lại sha từ file: `bc8ddfd80694`. Đọc
`git diff 3d53370 d1d6b96` của spec. Overlap scan: 0 trùng.

| Finding vòng 2 | Bản 3 | Kết quả |
|---|---|---|
| n-1 nguồn A/A | §6: "B1 ↔ G2.1a, context 10 ↔ context 10 trên 176 câu — câu tụt Completeness 1, Accuracy 2; lấy số lớn" — khớp `phase_8_2_b1_implementation.md` §4 (`p82-b1`) | **đóng** |
| n-2 khôi phục | "Dừng + khôi phục" thêm `settings.yaml` (`exclude_files`), file mẫu chunker, `GOLD_PATH` (git / backup) + lý do 204 ≠ 205 | **đóng** |
| n-3 User duyệt trong cửa sổ | gold v4 thành bước 7 (sau build; "build không cần gold"; số `*_gold_*` chỉ tính sau bước này); bước 2–6 là sửa kho + exclude + chunk thử + build + kiểm sau build; bước 1 ghi "7–9 làm sau"; §8 dòng ngừng phục vụ sửa đúng; §7 "bước 7, 8" | **đóng** |

- Thứ tự mới vẫn đúng phụ thuộc: bước 6 (T1 mới) chỉ dùng kết quả tìm, không cần nhãn; bước 9 (đo "sau") chấm theo Golden (bước 8), không theo nhãn đoạn đúng; bước 12 (8B) đo theo v4.
- **Chữ còn sót (không chặn):** bảng §8 dòng "Nhãn đoạn đúng lệch offset ⇒ số tầng tìm sai" vẫn ghi "**bước 5** gold v4" — nay là bước 7. Sửa khi tiện (đổi chữ là bản mới; C không cần
  kiểm lại nếu chỉ đổi số bước này).

**Kết luận chung C68:** 3 vòng; bản `bc8ddfd80694` sẵn để A trình User duyệt sha.
