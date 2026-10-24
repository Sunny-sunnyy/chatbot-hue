# Implementation Report: Phase 7A2 Gate 1 — Sửa corpus

Implementer: Claude Opus 5.5
Date: 2026-10-23
Canonical inputs:

```text
docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md
docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md
gửi chatgpt/kết quả nghiên cứu/TONG_HOP_REVIEWER_2026_10_23.md (private)
```

Report này chỉ ghi mã mục, path, số dòng và kết quả lệnh. Không chép nội dung
corpus hay Golden.

## 1. Phạm vi

Gate 1 gồm Task 1–3 của plan:

- Task 1: backup và baseline.
- Task 2: sửa 21 mục nhóm A và chỉnh câu chữ 4 mục nhóm B (K30, K33, K34,
  K48).
- Task 3: Golden.

Không đổi code, không đụng Qdrant, không gọi API trả phí, không commit. Không
sửa 28 mục nhóm C.

Có ba quyết định phạm vi được chốt giữa chừng qua tin nhắn với Reviewer, đều
ngày 2026-10-23:

- **K27:** User chọn phương án B. CH:76 đổi số văn bản sang QĐ 104/2025 và
  ghi rằng văn bản này thay thế QĐ 21/2024. Câu về số nhạc cụ ở CH:40 và
  PG:65 giữ nguyên. Lý do: bảng chia "thính phòng ≥4/5, trên sông ≥3/4"
  trong file tổng hợp là cách R1 tự diễn giải, và mâu thuẫn với VBD:86–87
  (thuyền đơn ≥3/4, thuyền đôi ≥4/5).
- **K37:** Reviewer đồng ý cách tối thiểu. Sửa QT:34. Ở QT:43 chỉ tách riêng
  Điện Hòn Chén; Lăng Minh Mạng và Lăng Gia Long giữ nguyên.
- **K24:** Reviewer đồng ý sửa thêm VK:296 và VK:297. Hai dòng này ghi cùng
  địa điểm Alba Thanh Tân nên thuộc cùng mục K24.

Viết tắt dùng trong report (theo `meta/corpus-contradictions-2026-10-23.md`):

| Viết tắt | File |
|---|---|
| QT | `travel/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md` |
| HD | `travel/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md` |
| VK | `travel/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md` |
| VBD | `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` |
| CH | `performing_arts/arts/Ca Huế trên sông Hương.md` |
| PG | `performing_arts/performing_arts_guides.md` |

Mọi path trong report tính từ `knowledge-base-hue/`.

## 2. Thay đổi chính

### 2.1 Backup (Task 1)

Thư mục backup là `knowledge-base-hue/meta/backup_7a2_2026_10_23/`. Gồm 27 file
copy nguyên bản bằng `cp -p --parents`, giữ đường dẫn tương đối. Ngay sau khi
copy đã kiểm `cmp` byte-identical cho cả 27 file. Danh sách file đúng bằng cột
"File" ở bảng 2.2.

Có thêm một xác nhận gián tiếp: bản corpus dựng lại trong `/tmp` gồm corpus
hiện tại cộng 27 file backup có corpus identity khớp hằng số Phase 4
`0e5c0595…f223`. Nghĩa là backup đúng là bản trước khi sửa.

### 2.2 Sửa 25 mục (Task 2)

Số dòng trước và sau trùng nhau trừ K1 (xem cột Ghi chú), vì phần nguồn được
nối ở cuối file.

| Mã | File | Dòng đã sửa | Ghi chú |
|---|---|---|---|
| K1 | `heritages/heritage/Quần thể Di tích Cố đô Huế.md` | 42–50; xóa dòng 57 cũ | Danh sách 14 mã xếp lại theo UNESCO 001–014. Bỏ Trấn Bình Đài (không có mã riêng, vẫn được mô tả ở `Kinh thành Huế.md` và file khác). Điện Hòn Chén (678-009) được chuyển từ mục "di tích liên quan" vào danh sách. Đã rà mọi file có mã `678-0xx`: các file lăng/di tích riêng (Đàn Nam Giao, Lăng Đồng Khánh, Lăng Khải Định, Điện Hòn Chén, Kinh thành, Thiên Mụ, Hổ Quyền, Đại Nội) đều đã khớp chuẩn, không sửa |
| K4 | `heritages/heritage/Trường Quốc Học Huế.md` | 104, 105 | |
| K5 | `heritages/heritage-guides.md` | 33 | |
| K6 | `heritages/heritage-guides.md` | 24 | Ghi "theo hồ sơ ghi danh UNESCO năm 2009" |
| K9 | `heritages/heritage/Hải Vân Quan.md` | 18, 114 | |
| K10 | `heritages/heritage/Lăng Tự Đức.md` | 54 | |
| K11 | `foods/restaurants/texas chicken hue.md`; `foods/restaurants/lotteria hue.md`; `foods/cafes/koi the hue.md`; `foods/cafes/highlands coffee hue.md`; `foods/cafes/cat cafe mocha hue.md` | 9; 12; 10; 12; 9 | Chỉ sửa dòng địa chỉ AEON MALL |
| K16 | HD | 135 | |
| K24 | VK | 101, 295, 296, 297 | Ghi tên mới, giữ tên cũ trong ngoặc. Dòng 296–297 được Reviewer xác nhận thuộc K24 |
| K25 | CH | 29 | |
| K27 | CH | 76 | Phương án B do User quyết. Dòng nguồn ghi rằng văn bản gốc chưa được Reviewer tự mở |
| K32 | `performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md` | 114 | |
| K37 | QT | 34, 43 | Ở :43 chỉ tách Hòn Chén (xem mục 5) |
| K39 | `travel/places/Bãi biển Phú Diên.md` | 7 | |
| K40 | `travel/places/Chợ Đông Ba.md` | 37 | |
| K41 | `travel/places/Bãi biển Hàm Rồng.md` | 47 | |
| K44 | `travel/places/Bãi biển Hàm Rồng.md`; `travel/places/Đầm Cầu Hai.md` | 61; 10 | |
| K45 | `travel/places/Đầm Chuồn.md` | 6, 9, 15, 201 | |
| K50 | `travel/places/Vịnh Lăng Cô.md` | 203 | |
| K51 | `travel/places/Hệ đầm phá Tam Giang – Cầu Hai.md` | 194 | |
| K52 | `heritages/heritage/Hải Vân Quan.md`; `travel/tickets/Vé tham quan Hải Vân Quan.md` | 8, 16; 19 | |
| K30 (B) | `performing_arts/arts/Huế Wonderverse Music Fest.md` | 90 | Tách kỳ 2026 mùa Hạ khỏi kỳ đầu 12/2023 mùa Đông. Hai thông tin này đều đã có sẵn trong `Tuần lễ Âm nhạc Quốc tế Huế.md` |
| K33 (B) | PG | 136, 181 | Thêm "thuộc cung Khôn Thái" |
| K34 (B) | `festivals/festival-guides.md` | 46 | Phân biệt lễ lịch sử cuối năm âm lịch với bản tái hiện ngày 1/1 Dương lịch. Thông tin tái hiện đã có sẵn trong `Lễ Ban Sóc triều Nguyễn.md` |
| K48 (B) | `travel/places/Đầm Lập An.md` | 171 | |

Phần nguồn (căn cứ) như sau:

- Mỗi file có thêm dòng nguồn trong `## Nguồn dữ liệu`, gồm URL lấy từ file
  tổng hợp/R1/R2 và chữ "đối chiếu ngày 23/10/2026".
- 5 file foods đã có sẵn mục này; dòng mới được nối vào cuối mục.
- **22 file còn lại chưa có `## Nguồn dữ liệu`, nên Implementer tạo mới mục
  này ở cuối file.** Chunker loại mục này
  (`backend/ingestion/chunking/markdown_blocks.py:16`, `EXCLUDED_SECTIONS`).
  Đã kiểm bằng chunker thật: 0 chunk có heading `Nguồn dữ liệu`, 0 chunk chứa
  dòng nguồn mới.

Self-review diff: đã đọc `diff -u` và word-diff của cả 27 file so với backup.
Các token đổi chỉ thuộc 25 mục ở bảng trên và các dòng nguồn. Cả 27 file vẫn
bắt đầu bằng `# ` và không có frontmatter.

### 2.3 Golden (Task 3)

Cách làm: tìm giá trị cũ và từ khóa của 25 mục trong `question`, `keywords` và
`reference_answer` của cả hai file, rồi đọc từng dòng trúng.

- **Case bị ảnh hưởng: dòng 139** của `evaluation/golden_full_corpus.jsonl`
  (K44). `reference_answer` còn giá trị cũ "đến 112 km²", tôi sửa tối thiểu,
  bỏ phần đó. `keywords` không đổi. Diff Golden chỉ có đúng 1 dòng.
- Các dòng còn lại trúng từ khóa đều đã đọc và không chứa giá trị cũ: 3, 7, 8,
  17, 18, 21, 25, 27, 29, 30, 50, 51, 57, 58, 68, 73, 75, 76, 78, 91, 93, 104,
  107, 111, 126, 129, 136, 141, 142, 166, 169.
- Smoke 10 không đổi (`cmp` giống hệt). 10 dòng smoke vẫn deep-equal với các
  dòng canonical 3, 24, 42, 44, 55, 82, 114, 141, 155, 163. Dòng 139 không
  thuộc smoke.

## 3. Cách đã chạy thật

```bash
# Golden check, trước và sau sửa (từ backend/)
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl
# Chunker thật: discover_full_corpus_files + chunk_full_corpus(load_settings()), PYTHONPATH=. uv run python
# So sánh trước/sau: chạy chunk_full_corpus trên bản sao /tmp (corpus hiện tại + backup), root_dir trỏ /tmp
# Sửa corpus: script tạm /tmp/phase7a2_survey/gate1_edit.py (mỗi chuỗi cũ phải khớp đúng 1 lần, không khớp thì dừng trước khi ghi)
diff -u meta/backup_7a2_2026_10_23/<file> <file>      # cho từng file trong 27 file
```

## 4. Kết quả quan sát

| Kiểm tra | Trước | Sau |
|---|---|---|
| `check` golden_full_corpus.jsonl | exit 0, total 176 | exit 0, total 176 |
| `check` golden_full_corpus_smoke.jsonl | exit 0, total 10 | exit 0, total 10 |
| Số file discover | 205 (0 file dưới `meta/`) | 205 (0 file dưới `meta/`) |
| Số chunk / chunking errors | 8.460 / 0 | **8.459** / 0 |

- Chunk giảm 1 do `heritages/heritage/Quần thể Di tích Cố đô Huế.md`: 51 → 50
  chunk, vì danh sách UNESCO bớt mục Trấn Bình Đài và mục Hòn Chén bị trùng
  được gộp vào danh sách.
- Chunk có `search_text` đổi chỉ nằm ở đúng 27 file đã sửa; không file nào
  khác đổi.
- Lần chạy đầu của script sửa dừng trước khi ghi file nào. Lỗi là điều kiện
  `endswith` khớp nhầm QT với file K1. Tôi sửa thành so sánh đường dẫn đúng
  rồi chạy lại. Sau lần chạy đầu đã kiểm `cmp` cả 27 file: không file nào bị
  đổi.

## 5. Lỗi và giới hạn

- **Mâu thuẫn còn lại ngoài phạm vi (K37):** QT:27, :30, :187 và phần còn lại
  của :43 vẫn ghi Lăng Minh Mạng và Lăng Gia Long thuộc "phường Long Hồ".
  Giá trị chuẩn K37 lại nói Long Hồ cũ đã nhập vào Kim Long. Reviewer quyết
  không mở rộng sửa vì K37 chỉ có một nguồn (R2).
- **K27:** CH:40 và PG:65 vẫn giữ câu về số nhạc cụ ("3 đến 5", "3 đến 4")
  theo quyết định B. Câu này chưa được đối chiếu với văn bản gốc vì vbpl
  không mở được.
- **K32:** `Tuần lễ Festival Nghệ thuật Quốc tế Huế.md:114` là số liệu khách du lịch "trong thời gian tuần lễ". Tôi đổi
  khoảng ngày sang 7/6–12/6 theo giá trị chuẩn, nhưng chưa kiểm báo cáo gốc
  của số liệu đó tính theo khoảng ngày nào.
- **K4:** `Trường Quốc Học Huế.md:106` (không thuộc dòng được giao) viết
  rằng vào tháng 4/1908 "người học trò Nguyễn Tất Thành" tham gia biểu tình.
  Câu này không sai trực tiếp, nhưng giờ đứng trước mốc vào trường năm 1908
  (niên khóa 1908–1909). Tôi giữ nguyên.
- **K11:** Hai dòng "phường An Đông" ở địa chỉ khác (Bánh ép 1992, Bún thịt
  nướng Bà Tý cơ sở 2, `foods/local_specialties/banh ep.md:87`) không phải
  AEON nên ngoài phạm vi, giữ nguyên.
- **Golden authoring:** `travel/places/evaluation/golden_full_corpus_authoring.jsonl:22`
  vẫn còn câu cũ của dòng 139. Handoff chỉ cho sửa hai file official. Nếu sau
  này chạy lại `merge`, chỗ sửa ở dòng 139 sẽ bị ghi đè.
- Không có Git cho corpus/Golden (`.gitignore:25`). Bằng chứng duy nhất cho
  phần sửa là backup và diff.
- Script tạm `/tmp/phase7a2_survey/gate1_edit.py` và các file so sánh trong
  `/tmp` không thuộc repo.

## 6. Handoff cho Reviewer

- Đọc report này trước. Sau đó diff từng file trong 27 file với backup:
  `cd knowledge-base-hue && diff -u "meta/backup_7a2_2026_10_23/<f>" "<f>"`.
- Đọc dòng Golden 139 cùng User. Bản trước khi sửa Golden không có trong
  backup corpus; xem bản gốc trong authoring `travel/places/...:22` hoặc
  `/tmp/phase7a2_survey/golden_before.jsonl`.
- Reviewer chạy lại theo Review Contract: `check` hai file Golden (lệnh mục 3)
  và chunker đếm file/chunk. Kết quả kỳ vọng là 205 / 8.459 / 0 error.
- Sub-agent: không dùng.
