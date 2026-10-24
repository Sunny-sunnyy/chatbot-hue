# Review: Phase 7A2 Gate 1 — Sửa corpus

Decision: ready_for_user_confirmation → approved (User 2026-10-24)
Reviewer: Claude Opus 5.5
Date: 2026-10-23
Spec: `docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md` (§4)
Plan: `docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md` (Task 1–3)
Implementation report: `reports/phase_7a2_gate_1_corpus_correction_implementation_2026_10_23.md`

Report này không chép nội dung corpus hay Golden (dữ liệu private).

## 1. Phạm vi đã review

- Đọc toàn bộ implementation report và handoff `final_review`.
- Worktree: chỉ có file tracked mới/sửa của Phase 7A2 (spec, plan, survey
  report, Gate 1 report, handoff). Không có thay đổi code. Corpus và Golden
  nằm trong `knowledge-base-hue/` (ignored).
- Word-diff toàn bộ 27 file corpus so với backup
  `knowledge-base-hue/meta/backup_7a2_2026_10_23/` (27 file).
- Đối chiếu từng thay đổi với giá trị chuẩn trong
  `gửi chatgpt/kết quả nghiên cứu/TONG_HOP_REVIEWER_2026_10_23.md` và ba quyết
  định giữa chừng: K27 = B (User), K37 tối thiểu và K24 thêm VK:296–297
  (Reviewer, trong phạm vi mục đã duyệt).
- Golden dòng 139: so `reference_answer` trước/sau (bản trước lấy từ authoring
  `travel/places/evaluation/golden_full_corpus_authoring.jsonl:22`).

## 2. Findings

Không có blocker hoặc major.

Minor (không chặn):

- **m1 — Golden authoring lệch canonical.** Vị trí:
  `knowledge-base-hue/travel/places/evaluation/golden_full_corpus_authoring.jsonl:22`
  vẫn ghi giá trị cũ của K44. Tác động: chạy lại `merge` sẽ ghi đè sửa ở dòng
  139. Đề xuất đóng: khi User đóng Gate 1, Implementer đồng bộ đúng
  `reference_answer` của dòng authoring này với dòng 139 (cơ học, một dòng).

Ghi nhận ngoài phạm vi (không đưa vào correction):

- `Vé tham quan Quần thể Di tích Cố đô Huế.md` (QT) :27, :30, :187 và phần đầu
  :43 vẫn ghi Lăng Minh Mạng/Gia Long thuộc "phường Long Hồ", trong khi cùng
  dòng :43 nay ghi Hòn Chén thuộc Kim Long. K37 chỉ có một nguồn (R2), R1 ghi
  "không xác minh được", nên Reviewer không mở rộng. Ứng viên cho đợt sửa
  corpus sau.
- `Ca Huế trên sông Hương.md:40` và `performing_arts_guides.md:65` giữ câu về
  số nhạc cụ theo quyết định K27 = B; văn bản gốc QĐ 104/2025 chưa ai mở được
  (vbpl PDF trả 404 ngày 2026-10-23).
- K11: các địa chỉ "phường An Đông" không thuộc AEON MALL (Bánh ép 1992, Bún
  thịt nướng Bà Tý cơ sở 2, `foods/local_specialties/banh ep.md:87`) giữ nguyên.
- K32: số liệu khách "trong thời gian tuần lễ" đổi khoảng ngày sang 7/6–12/6;
  khoảng ngày của báo cáo gốc chưa kiểm.
- K4: `Trường Quốc Học Huế.md:106` (tháng 4/1908 biểu tình) giữ nguyên, không
  mâu thuẫn trực tiếp với mốc vào trường năm 1908.

Đánh giá từng nhóm sửa (đã đọc diff):

- K1: danh sách 14 mã khớp 001–014 của file tổng hợp; Trấn Bình Đài (không có
  mã riêng) bỏ khỏi danh sách, Hòn Chén chuyển vào mã 009. Hợp lý, làm số chunk
  của file giảm 51 → 50.
- K4, K5, K6, K9, K10, K16, K25, K32, K39, K40, K41, K44, K45, K50, K51, K52:
  đúng giá trị chuẩn, câu văn tự nhiên.
- K11 (5 file foods), K24 (VK:101, 295–297), K37 (QT:34, :43): đúng phạm vi đã
  chốt.
- K27: chỉ CH:76 đổi số văn bản, đúng quyết định B; dòng nguồn ghi rõ văn bản
  gốc chưa được Reviewer tự mở.
- Nhóm B (K30, K33, K34, K48): chỉ làm rõ ngữ cảnh, không đổi sự kiện.
- `## Nguồn dữ liệu`: 22 file được tạo mới mục này ở cuối file, 5 file foods
  nối thêm dòng. Phù hợp quy tắc curated data (source tracking tối giản trong
  mục này); chunker loại mục này.

## 3. Cách Reviewer chạy lại thật

```bash
# Diff 27 file với backup
cd knowledge-base-hue && git diff --no-index --word-diff=plain -U0 "meta/backup_7a2_2026_10_23/<f>" "<f>"
# Golden check (từ backend/)
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl
# Chunker thật (repo root)
HF_HUB_OFFLINE=1 PYTHONPATH=. uv run python -c "discover_full_corpus_files + chunk_full_corpus(load_settings())"
```

## 4. Kết quả quan sát

| Kiểm tra | Kết quả fresh của Reviewer |
|---|---|
| `check` golden_full_corpus.jsonl | exit 0, total 176 |
| `check` golden_full_corpus_smoke.jsonl | exit 0, total 10 |
| Chunker | 205 file, 0 file dưới `meta/`, 8.459 chunk, 0 error |
| Chunk có heading `Nguồn dữ liệu` | 0 |
| Diff 27 file | chỉ 25 mục đã giao + dòng nguồn |
| Golden dòng 139 | chỉ `reference_answer` bỏ giá trị cũ của K44; `question` và `keywords` không đổi |

Khớp với số liệu trong implementation report.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không tự mở lại các URL nguồn mới thêm; căn cứ dựa trên file tổng
  hợp đã được User chấp nhận khi duyệt spec.
- Corpus không có Git; bằng chứng duy nhất là backup + diff.

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`.

**Approval Closure Contract — Gate 1:**

1. User đọc Golden dòng 139 (Reviewer trình bày trước/sau trong phiên) và xác
   nhận đóng Gate 1.
2. Sau xác nhận, Implementer sửa cơ học m1 (đồng bộ authoring
   `travel/places/.../golden_full_corpus_authoring.jsonl:22` với dòng 139),
   chạy lại `check --authoring` cho file đó, báo kết quả.
3. Reviewer cập nhật `Project_Status.md` (Gate 1 closed) và thay
   `CURRENT_HANDOFF.md` bằng handoff Gate 2 (Task 4–8 của plan) với quyền paid
   đúng spec §5.6.
4. Git: `none`. Backup Gate 1 giữ tới khi User đóng toàn Phase.

**Closure (2026-10-24):** User xác nhận đóng Gate 1 sau khi xem dòng 139
trước/sau. m1 đã được Implementer đồng bộ (authoring travel_places dòng 22,
chỉ `reference_answer`; `check --authoring` exit 0, total 32); Reviewer kiểm
độc lập: khớp dòng 139, không còn giá trị cũ trong file authoring. Gate 1
`approved`.
