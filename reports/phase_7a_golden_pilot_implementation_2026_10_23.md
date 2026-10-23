# Implementation Report: Phase 7A Golden full-corpus — Task 1–2 (GATE P)

Implementer: Claude Opus 5.5 (session `hue-rag-08`)
Date: 2026-10-23 (+07)
Base commit: `b688926` (Phase 7A spec/plan approved)
Head commit: worktree (Implementer Git authorization: none)
Risk level: medium
Canonical inputs:

```text
docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md
docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md
```

Sub-agent: không dùng (Task 1–2 không được phép). Paid call: không. Không sửa
curated Markdown, Foods V2/V3, retrieval, generation, API hay Qdrant.

## 1. Phạm vi

- **Task 1:** module kiểm tra và gộp Golden, kèm 8 test logic thuần.
- **Task 2:** pilot 20 case `heritages`, hướng dẫn viết và report này.

Dừng tại GATE P, chưa bắt đầu Task 3.

## 2. Thay đổi chính

| Path | Tracked | Nội dung |
|---|---|---|
| `backend/evaluation/golden_full_corpus.py` | có (mới, 183 dòng) | Module của plan Task 1 Step 3 |
| `backend/tests/test_golden_full_corpus.py` | có (mới, 93 dòng) | 8 test của plan Task 1 Step 1 |
| `reports/phase_7a_golden_pilot_implementation_2026_10_23.md` | có (mới) | Report này |
| `knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl` | private (gitignored) | 20 case pilot |
| `knowledge-base-hue/meta/golden-full-corpus-writing-guide.md` | private (gitignored) | Hướng dẫn viết |
| `session_prompt/CURRENT_HANDOFF.md` | có | Chuyển sang `final_review` |

Code Task 1 **giống hệt từng ký tự với plan**: tôi so bằng `diff` giữa khối
code trích từ plan và file thật, cả hai file đều không có khác biệt. Không có
chỉnh sửa nào nên không có trade-off cần ghi. Thư mục
`knowledge-base-hue/heritages/evaluation/` được tạo mới, đúng path ghi trong
spec §10.

## 3. Cách đã chạy thật

Mọi lệnh chạy từ `backend/`, không gọi mạng.

| Bước | Lệnh | Kết quả quan sát |
|---|---|---|
| T1 Step 2 (RED) | `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q` | collection error `ModuleNotFoundError: No module named 'evaluation.golden_full_corpus'` |
| T1 Step 4 (GREEN) | lệnh trên | `8 passed in 0.04s` |
| T1 Step 5 | CLI probe `/tmp/golden_cli_probe.jsonl` (đúng lệnh trong plan) | in `category: {'out_of_scope': 1}`, `partition: {'foods': 1}`, `total: 1`, một lỗi `line 1: out_of_scope reference_answer must equal INSUFFICIENT_ANSWER`, `exit=1` |
| T1 corpus | `load_corpus()` | 205 file curated; 29 file `heritages/` |
| T2 Step 4 | `HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl --authoring` | `category: {'direct_fact': 8, 'comparative': 4, 'conditional': 3, 'multi_source': 3, 'out_of_scope': 2}`, `partition: {'heritages': 20}`, `total: 20`, **exit 0** |
| Format | `git diff --check`; grep trailing whitespace trên 2 file untracked | exit 0; không có trailing whitespace |

## 4. Kết quả quan sát

### Task 2 Step 1: đọc corpus

Tôi đọc toàn văn đủ 29/29 file `heritages/` theo danh sách
`discover_full_corpus_files()`, gồm `heritage-guides.md` và 28 file trong
`heritage/`, trước khi viết case.

### Pilot: 20 case

| Category | Số case | Ghi chú |
|---|---:|---|
| `direct_fact` | 8 | 1 case có đáp án nằm trong bảng (bảng combo vé trong `heritage-guides.md`) |
| `multi_source` | 3 | mỗi case cần 2 file; không file nào tự trả lời đủ |
| `comparative` | 4 | mỗi case so sánh 2 thực thể từ 2 file |
| `conditional` | 3 | điều kiện về tuổi, trang phục và giai đoạn lịch sử |
| `out_of_scope` | 2 | thực thể ở địa phương khác, gần domain |
| **Tổng** | **20** | |

- Tên gọi khác có thật được dùng ở 2 case (10%); corpus xác nhận cả hai là cùng
  thực thể.
- Có 10 case với `sources` gồm 1 file, 8 case gồm 2 file, và 2 case
  `out_of_scope` có `sources: []`.
- Có 3 case dựa vào `heritage-guides.md` (vé, chính sách giảm giá, trang phục).
- Tôi đã đối chiếu lại từng `reference_answer` với file nguồn sau khi viết.

### Out-of-scope search ledger (chỉ ghi lệnh, không ghi nội dung)

Tôi tìm trên toàn bộ 205 file curated bằng `load_corpus()` và so khớp
casefold:

```text
HF_HUB_OFFLINE=1 uv run python - <<EOF  (load_corpus(); đếm file chứa term.casefold())
term A (tên đầy đủ một di tích ở Hà Nội)      → 0 file
term B (tên rút gọn của địa danh chứa term A)  → 5 file (chỉ nhắc tên, không có thông tin được hỏi)
term C (một di tích Chăm ở tỉnh khác)          → 1 file (travel; chỉ nhắc tên, không có thông tin được hỏi)
6 term ứng viên khác (di tích/đô thị ở tỉnh khác) → 0, 0, 1, 1, 4 và 2 file; không dùng
lệnh in ngữ cảnh ±120 ký tự cho term C (chỉ xem trong session, không chép vào tracked file)
```

Hai case `out_of_scope` dùng term A và term C. Term A không xuất hiện trong
corpus. Term C chỉ được nhắc tên trong một câu ở partition `travel`, và corpus
không có thông tin mà câu hỏi hỏi. Tên thật của các term được ghi trong file
private `knowledge-base-hue/evaluation/phase_7a_review_notes.md`.

### Case đã tự loại hoặc sửa khi soạn (mô tả theo dạng, không chép câu)

1. Câu lồng hai câu hỏi (số tầng và ý nghĩa từng tầng của một đàn tế): sửa
   thành một câu hỏi.
2. Câu "kể tên ba nhà hát cung đình" gán nhãn `multi_source`, nhưng một đoạn
   đã liệt kê đủ: loại, vì sai nhãn.
3. Câu hỏi du khách có được đi qua một cửa lăng không: corpus không nói quy
   định cho du khách, đáp án phải suy diễn. Loại.
4. Câu dựa vào chữ "lăng duy nhất quay hướng Tây Bắc": corpus mâu thuẫn. Loại.
5. Câu về nơi lưu giữ hai di sản tư liệu: keyword dự định là chuỗi con của tên
   cơ quan khác, và một câu ở file Quần thể đã đủ đáp án. Loại.
6. Câu so sánh giá vé hai lăng: bỏ để hạn chế trùng chủ đề với partition
   `travel_tickets`. Pilot giữ 2 case về vé và 1 case về chính sách giảm giá.
7. Câu xin lời khuyên chọn combo vé: corpus có gợi ý, nhưng đây là câu lời
   khuyên nên bị cấm theo spec §6. Không viết.

### Lỗi và mâu thuẫn corpus phát hiện khi đọc (không sửa corpus, chỉ báo)

| # | Chủ đề | Mâu thuẫn |
|---|---|---|
| K1 | Mã thành phần UNESCO 678-0xx | File Đàn Nam Giao, Lăng Đồng Khánh, Lăng Khải Định và Điện Hòn Chén ghi mã khác danh sách 14 cụm trong file Quần thể Di tích Cố đô Huế |
| K2 | Hướng lăng | File Lăng Thiệu Trị nói đây là lăng vua duy nhất quay hướng Tây Bắc; file Lăng Dục Đức cũng ghi hướng Tây Bắc |
| K3 | MOWCAP 2016 và Lăng Tự Đức | File Thơ văn ghi Lăng Tự Đức không thuộc danh mục; file Lăng Tự Đức ghi thơ văn ở đó là "bộ phận trọng yếu" được vinh danh |
| K4 | Năm Nguyễn Tất Thành vào Quốc Học | File Trường Quốc Học ghi tháng 9/1907, học hai niên khóa; file Hệ thống di tích Hồ Chí Minh ghi năm 1908, niên khóa 1908–1909 |
| K5 | Năm ghi danh Bún bò Huế | `heritage-guides.md` ghi năm 2024; file riêng ghi Quyết định ngày 27/06/2025 |
| K6 | Số tấm Mộc bản | Các file ghi 34.618, 34.555 và khoảng 33.971–34.618 |
| K7 | Năm Trường Hành Nhơn | File Quốc Học ghi "Tự Đức thứ 2 – 1868"; năm 1868 không khớp niên hiệu Tự Đức thứ 2 |
| K8 | Hậu chẩm Kinh thành | File Kinh thành ghi núi Đột Sơn; file Quần thể ghi dãy Trường Sơn. Tên cồn cũng được viết hai cách, "Dã Viên" và "Giã Viên" |
| K9 | Năm đúc Cửu Đỉnh | File Hải Vân Quan ghi 1836; file Cửu Đỉnh và file Đại Nội ghi 1835–1837 |

Pilot không dùng dữ kiện nào thuộc K1–K9. Phase 7A không có quyền sửa
corpus, nên các mâu thuẫn này cần Reviewer/User quyết định có mở lifecycle sửa
corpus hay không.

### Hướng dẫn viết (Task 2 Step 5)

File `knowledge-base-hue/meta/golden-full-corpus-writing-guide.md`, khoảng 1
trang, gồm:
- quy tắc spec §6 viết gọn, cộng 3 điểm rút ra từ pilot: không dùng dữ kiện
  corpus tự mâu thuẫn; không chọn keyword là chuỗi con của thực thể khác;
  `multi_source` phải không có đoạn nào tự trả lời đủ;
- mẫu `reference_answer`;
- 5 ví dụ tốt và 5 ví dụ xấu lấy từ chính pilot, kèm lý do.

## 5. Lỗi và giới hạn

- Script §9 chỉ kiểm cấu trúc và luật keyword, không kiểm đúng sai nội dung.
  Độ đúng của 20 case do tôi tự đối chiếu; Reviewer cần đối chiếu độc lập 20/20
  ở GATE P.
- Keyword proxy vẫn có nhiễu: một vài keyword dạng số hoặc ngày cũng xuất hiện
  ở đoạn không liên quan trong corpus. Mỗi case đã kèm tên thực thể trung tâm
  để giảm nhiễu, nhưng không loại hết được.
- Một case `multi_source` có dạng "những lăng nào". Đáp án đầy đủ chỉ đúng theo
  corpus hiện tại; tôi đã tìm và chỉ thấy 2 lăng thỏa điều kiện.
- 3 case dựa vào `heritage-guides.md` (vé, giảm giá, trang phục) có thể trùng
  chủ đề với `travel_tickets` ở Task 3; cần kiểm ở Task 3 Step 4.
- Dữ liệu vé có mốc "tham khảo tháng 09/2026", nên có thể lỗi thời.
- Golden do LLM viết rồi người review, không phải câu hỏi người dùng thật (spec
  §8).

## 6. Handoff cho Reviewer

- **Đọc trước:** report này; sau đó file private authoring (20 dòng) và hướng
  dẫn viết.
- **Chạy lại** (Review Contract):
  - `git status`, `git diff --check`;
  - đọc 2 file Task 1 (giống hệt plan);
  - `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q`;
  - `check --authoring` cho file `heritages`;
  - đối chiếu 20/20 case với `sources`;
  - tìm text độc lập cho 2 case `out_of_scope`.
- **Cần quyết định:**
  - User đọc toàn bộ 20 case và hướng dẫn viết, rồi xác nhận hướng dẫn trước
    khi mở Task 3;
  - cách xử lý mâu thuẫn corpus K1–K9.
- **Deviation:** không có.

## 7. Correction GATE P (P1–P4)

Theo correction handoff ngày 2026-10-23 và review
`reports/phase_7a_golden_pilot_review_2026_10_23.md`. User đã đọc 20 case
pilot, thấy văn phong ổn và đồng ý cả 4 điểm sửa.

| # | Sửa đã làm | Tiêu chí đóng |
|---|---|---|
| P1 (major) | Mẫu `reference_answer` trong hướng dẫn đổi thành "chỉ trả lời đúng điều được hỏi, cộng điều kiện/ngoại lệ bắt buộc; không thêm dữ kiện phụ, không thêm mốc thời gian nếu câu không hỏi", kèm lý do liên quan Completeness ở Phase 7B. Thêm ví dụ xấu thứ 6 về đáp án thừa ý, nên giờ có 6 ví dụ xấu. Đã cắt gọn answer của case #1, #3, #6, #8, #13, #16, #17, #19; #6 bỏ keyword dạng năm | Hướng dẫn không còn "thêm chi tiết" hoặc "ghi mốc" (grep: 0); mỗi answer chỉ chứa điều được hỏi |
| P2 | Case #18 viết lại thành câu hỏi giống/khác; answer mở đầu "Không." rồi nêu hai hướng. Định nghĩa `comparative` trong hướng dẫn thêm "so sánh thật (hơn/kém, trước/sau, giống/khác)" | `comparative` thật |
| P3 | Hướng dẫn thêm quy tắc: keyword số phải là chuỗi nguyên văn dài hơn có kèm ngữ cảnh, hoặc đi cùng tên thực thể. #8 đổi keyword số sang chuỗi có "hơn"; #9 dùng chuỗi nguyên văn có kèm "trung tâm thành phố" và thêm tên lăng | `check` exit 0 |
| P4 | Ledger §4 thay tên thực thể và search term bằng mô tả chung (term A/B/C, có loại địa danh), giữ nguyên số file đếm được | Report tracked không còn tên hai thực thể `out_of_scope` (grep: 0) |
| Thêm | Quy tắc 5 của hướng dẫn trỏ tới `knowledge-base-hue/meta/corpus-contradictions-2026-10-23.md` (K1–K10; Reviewer bổ sung K10) và cấm dùng các dữ kiện đó | |

**Phạm vi thay đổi.** So sánh file authoring trước và sau sửa: chỉ 10 dòng
thay đổi (#1, #3, #6, #8, #9, #13, #16, #17, #18, #19), đúng danh sách
correction; 10 case còn lại giữ nguyên. Không sửa module/test Task 1, curated
Markdown hay case nào khác.

**Chạy lại.**
- `check --authoring` cho file `heritages`: category và partition giữ nguyên
  (`total: 20`), **exit 0**.
- `git diff --check`: exit 0.
- Reuse: test `8 passed` của GATE P vẫn hợp lệ vì module Task 1 không đổi.
