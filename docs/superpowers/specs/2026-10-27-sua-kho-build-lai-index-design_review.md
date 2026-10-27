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
