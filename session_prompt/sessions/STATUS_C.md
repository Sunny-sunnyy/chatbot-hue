# STATUS C — cập nhật 2026-10-26 15:58 (phiên 26/10: **đợt 3 XONG** trên nhánh `dot3`, B review ready_for_user_confirmation; C đã về `main`)

Terminal: `hue-rag-87` (mở 26/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-b0`, B = `hue-rag-3e` (trực tiếp).
User 26/10: C làm việc trực tiếp với A; A giao việc = "làm đi". Quyền phiên 26/10 (User 14:1x): C commit / push nhánh `dot3` (chỉ đợt 3); paid đợt 3 ≤ 0,003 USD.

## Trạng thái (26/10 15:58)

- **Đợt 3 xong — chờ A merge** (`--no-ff`, giữ sha B đã review). `origin/dot3` = **`2c420aa`**: 12 commit code `3a37af4 … 8f0e5c4` + docs `210abd4` (B-18 guide
  + report), `782ea05` (m-1 review B), `2c420aa` (T-C cuối đợt). Report: `report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md`; review B:
  `sua_dot3_review.md` (0 / 0 / 3 minor; m-1, m-2 C đã sửa, m-3 để A). Working tree chung đã về `main` (`0ceeda2`). Không khai báo file nào nữa.
- Cổng cuối đợt (`8f0e5c4`): D1 8.459 / 0 / `60591acff422ece6` / identity = record; D2 `cefb2d1ad609`; D3 25 câu giống byte; D4 197 p / 1 f / 4 e (chỉ phần cần key;
  2 test generator có key 2 passed, 0 USD); D5 đạt; D6 0; D8 0 / 0; D9 0 lỗi; B-02 8.459 `PointStruct` giống byte; T-C (User `!`) 1 passed sau C6 và cuối đợt.
  Code `backend/` 8.345 → 6.218 dòng.
- Script + ghi chép đợt (private): `data/ra_soat_code_2026-10-25/tools/dot3/` (`notes_26_10.md`, `b12_move_samples.py`, `b02_points.py`, `gate.py`, d1/d4/d7/d8/d9).
  File private mới: `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json, backup_b12_2026-10-26/}`, `data/tools/huegov_converters/`.
  Tạm: `/tmp/c42/` (dense.npy 13 MB, points_*.jsonl 92 MB mỗi file — xóa khi B không cần chạy lại B-02).

## Phiên sau C làm gì đầu tiên

Chờ A giao việc. Còn treo từ trước: **C33 plan E1** (`phase_8_2_e1_plan.md` sha `f86240418ca1`) phải sửa khi 8.2 chạy lại (`paired_stats` + `false_refusal`,
citation v2 ⇒ sha mới); C32 rà kho chờ User.

## Việc đã xong phiên tối 25/10 (chi tiết trong report; đã commit trên `main` trừ khi ghi khác)

- C34 rà code luồng trả lời + đánh giá (`ra_soat_code_C.md`, 18 finding); kiểm chéo B25 (`kiem_cheo_C.md`); review B26 (`sua_4_review.md`); review plan 1b
  (`sua_1b_plan_review.md`) + review gói 1b (`sua_1b_review.md`, ready); C35 gói 1a citation `[Nguồn n]` (`9e6d371`); gói 3a / 3b `paired_stats` + `build_answer_input`
  (`47a4e32`); 3c phần free citation v2 (`sua_3c_citation_v2.md`, `data/ra_soat_code_2026-10-25/citation_v2/`); danh sách ứng viên (`ung_vien_cai_tien_C.md`); plan đợt 3
  (`sua_dot3_plan.md` bản 3).
- Còn treo từ trước: **C33 plan E1** (`phase_8_2_e1_plan.md` sha `f86240418ca1`) phải sửa khi 8.2 chạy lại — dùng `paired_stats` + `false_refusal` (C-02 / gói 3a), số
  citation theo v2 ⇒ sha mới. C32 rà kho: hồ sơ, chờ User.
- **C chưa đọc nội dung câu kín** (md5 `ddc59587b502`, manifest `9ea480d0d083`).

## Câu hỏi cho A / User

- 3c: xin lượt xác nhận reasoning `none` trên test (~0,007 USD ở context 5) — A đưa vào tài liệu thiết kế đợt cải tiến (A 20:5x).
- C32: `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index — loại ở lần build lại?
- E1 plan Q1–Q3 (§10 plan) — khi 8.2 chạy lại.

## File private C tạo phiên này (không commit)

- `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `brief_common.md`, `nguon_count.py`, `cite_shapes.py`, `recheck_both.py`,
  `c01_probe_*.py`; thư mục `kiem_cheo_C/`, `review_4/`, `review_1b_plan/`, `review_1b/`, `sua_1a/`, `sua_3/`, `citation_v2/`, `dot3_plan/`); `data/ra_soat_code_2026-10-25/citation_v2/`.
- Trước đó: `data/ra_soat_kho_2026-10-25/` (C32), `data/phase_8_2/e1_plan/` (C33).
- Tạm: `/tmp/c34`, `/tmp/c34x`, `/tmp/c35`–`/tmp/c42` (mất khi tắt máy; không nội dung private ngoài số đếm).

## Ý cải tiến (A xin danh sách sau 5 gói — chỉ là ý, chưa thử; bản đầy đủ `ung_vien_cai_tien_C.md`)

- **Route API ghi usage (token, latency, số nguồn) mỗi câu vào log** — cổng ổn định gói 3 / 1b / đợt 3 đều phải **ước** tiền; không ghi nội dung câu hỏi.
- **Nhãn context `[Nguồn n]` ↔ prompt `[n]`** (C-09): thử khớp nhãn — thí nghiệm, đo lỗi "không ngoặc số" (14 / 1.600) + Completeness.
- **14 câu "không có ngoặc số"** còn lại sau 1a đều ở context 5 nguồn — xem có phải câu liệt kê / một ý.
- **Bộ đếm token context nhận instructions** khi harness đổi prompt (C-03 phần 2) — khi 8.2 E1 cần.
- **Kiểm token mỗi đoạn tốn gấp đôi thời gian chia nếu không nhớ kết quả** (đợt 3 commit 2) — đã cache; nếu sau này đổi chunker, đo lại thời gian.

## Đã học / bẫy gặp (đầu vào vòng cải tiến)

- **26/10 C4: nối lệnh quét trùng với `git commit` bằng `;` ⇒ commit chạy dù quét exit 1** (dòng bị cờ là chuỗi có sẵn, không lộ thêm — nhưng là may).
  Quét là một bước riêng: chạy, đọc kết quả, rồi mới `git add` / commit; nếu nối thì dùng `&&`.
- **Đổi literal hàng loạt trong test: viết script AST + kiểm ngược round-trip** (thay lại ⇒ đúng file gốc từng byte) thay vì sửa tay 58 chỗ; đánh số theo
  vị trí trong file (lần đầu theo thứ tự `ast.walk` ra `S[7]` trước `S[4]`).
- **So "trước / sau" cho thay đổi đường build: tách khâu đắt ra dùng chung** (B-02: mã hóa e5 một lần 201 s, dựng điểm hai lần từ cùng ma trận) — đổi một thứ, đo một thứ.
- **`git diff --stat main..dot3` (hai chấm) đếm cả commit `main` đi sau nhánh** ⇒ số kích thước nhánh ghi theo `git diff --shortstat <gốc>..<đỉnh>` (m-1 review B).
- **Plan ghi thông điệp lỗi phải đối chiếu đúng dòng ném đầu tiên** (đợt 3 commit 1: plan m-4 ghi `"Target collection already exists"`, thực tế
  `require_fresh_full_corpus_target` ném trước với `"target is non-empty"`) ⇒ khi viết test "đúng lý do", chạy thử một lần để thấy thông điệp thật trước khi ghi vào plan.
- **Thêm một phép kiểm vào vòng lặp nóng: đo thời gian trước / sau** (B-11 gấp đôi thời gian chia đoạn cho tới khi cache) — plan có ghi "đo giây" nên thấy ngay.
- **`git mv` sang thư mục bị gitignore vẫn đưa file vào index** (B tìm, M-1 plan đợt 3) ⇒ chuyển dữ liệu sang chỗ private bằng `cp` + `git rm`, kiểm `git ls-files`.
- **Script đo đọc `HEAD` chỉ đúng sau khi commit** (`usage.py` dùng `git grep <rev>`): D6 chạy sau commit, hoặc grep working tree.
- **Lệnh với `HF_HOME` rỗng bị auto mode chặn** trong session C (và B) ⇒ test kiểu đó để User chạy `!` (WORKFLOW §3.6), ghi rõ "dùng lại kết quả User" khi review.
- **Chỉ số lỗi do validator đếm: phân loại theo hình dạng output trước khi kết luận nguyên nhân** (C-09: 8.1 ghi "model quên `[n]`", thực tế viết `[Nguồn n]`).
- **Đọc đúng tài liệu trước khi phản biện** (sua_4 m3: C đọc nhầm plan G3, B đúng — H1 mới là bước bỏ huydang).
- **Import hai kiểu (`backend.X` / `X`) tạo hai bản module** ⇒ `except` / `isinstance` hụt — đã sửa ở gói 1b (quy ước import trần, chạy từ `backend/`).
- **Hàm so cặp của harness 8.1 không đổi dấu cho chỉ số "càng thấp càng tốt"** — từ gói 3a dùng `paired_stats` với tên `false_refusal`.
- `grep` ở máy là ugrep: regex dài báo "exceeds complexity limits" ⇒ tách ngắn hoặc dùng Python.
- Giữ từ trước: repo public (không chép nội dung kho / Golden / câu kín / dự án khác vào file tracked); giờ lấy bằng `date`; không báo "đã xong" trước khi lệnh ghi
  file trả kết quả; đọc tin mới trước bước đo / thay đổi; chạy GPU phải được A ghi rõ.

## Tiền

Paid API C phiên 26/10: **≈ 0,0020 USD ước** — 5 lượt cổng ổn định D5 × 2 câu `gpt-6-luna` (~0,0002 / câu; route không ghi usage). Cả đợt 3 ≈ 0,0024 (trần 0,003).
2 test generator có key: 0 USD (không gọi mạng). Quota Claude Code: không dùng sub-agent.


Paid API C phiên tối 25/10: **≈ 0,0016 USD** — đo: 0,000427 (C35, 2 lượt `gpt-6-luna`); ước (route không log usage): 3 lượt cổng ổn định × 2 câu × ~0,0002
(gói 3, review 1b, đợt 3 commit 2) ≈ 0,0012. Trần chung gói 1–5: 0,05 USD; đợt 3: ≤ 0,003 (đã dùng ~0,0004). Phiên chiều 25/10: 0 USD.
Quota Claude Code cho sub-agent: C34 3 sub-agent (S1–S3) phiên tối; C32 ~2,1M token phiên chiều.
