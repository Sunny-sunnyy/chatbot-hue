# Implementation Report: Phase 8.1 G0.6 — chuẩn bị khóa mốc (baseline freeze)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-a1`) · 2026-10-25 14:17 (`date`) · Việc: C31 · Spec 8.1 §5 G0 bước 6, §6.1, §6.4.
Review: B. Report không chép nội dung corpus / Golden / câu kín; chỉ ghi hash, số dòng, trạng thái.

**Trạng thái: PREPARED.** Mọi mục khóa mốc đã ghi hash và tái lập được. Còn **một** mục chờ: file câu kín chính thức 4 field
(chỉ tạo khi A nhắn "User đã duyệt mẫu bản 5"). Sau đó A khóa.

## 1. Đã làm

- Manifest private **`data/phase_8_1/baseline/g0_6_manifest.json`**:
  - sha 12 = `94859187080d`; schema `phase_8_1_g0_6_manifest:v1`; `git check-ignore` xác nhận private;
  - sha256 đầy đủ + số dòng cho từng mục bên dưới;
  - tạo bằng script `python -I` từ hash thật (lúc 14:15). Bổ sung số file / số point từ build record ngay sau đó.
- Chạy lại mốc retrieval 176 câu, cả hai cách trộn:
  - lúc 14:13, `HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --treatment <t> --golden full --out
    /tmp/c31/…` từ `backend/`;
  - so sha với mốc đã lưu: §2.
- `GET /collections`: chỉ `hue_full_corpus_7a2_e5_small_384`.
- Chuẩn bị (**chưa chạy trên câu kín**) script **`data/phase_8_1/tools/make_sealed_official.py`** (private, sha 12
  **`ce5ff542945b`**; bản đầu `4de4f31795ce`, sửa theo review B m1):
  - từ chối nếu md5 nguồn khác bản đã duyệt; từ chối ghi đè;
  - chỉ giữ 4 field `question`, `keywords`, `reference_answer`, `category`;
  - ghi `<đích>.tmp` trước, chạy `golden_full_corpus check` (không `--authoring`) trên file tạm, đọc exit code trực tiếp;
    **chỉ đổi tên thành đích khi check exit 0** (check lỗi thì đích không bị tạo dở; `.tmp` ghi đè được lần sau);
  - chỉ in md5, số dòng, phân bố loại câu, exit code và số dòng stderr. **Không in nội dung câu.**
  - **Thử trên file không kín** (`foods/evaluation/golden_full_corpus_authoring.jsonl`):
    - ra 37 dòng, đúng 4 field;
    - **giống từng dòng** 37 dòng đầu của Golden chính thức (cùng cách `merge` lọc field);
    - `check` exit 0;
    - đưa md5 sai thì script dừng, exit 1;
    - **nhánh lỗi** (file tạm 3 dòng, 1 keyword không có trong kho): check exit 1, chỉ còn `.tmp`, đích không tạo, script không
      in nội dung lỗi (`check_stderr_lines` 0; lỗi của check nằm ở stdout, script không in).

## 2. Nội dung manifest (hash 12 ký tự; đầy đủ trong file)

| Mục | Giá trị | Ghi chú |
|---|---|---|
| Commit HEAD | `8a909e0` | working tree chỉ dở tài liệu + harness thí nghiệm (danh sách trong manifest); không có file code runtime |
| Corpus | `corpus_identity` `5869d3cc2391…`, 205 file, 8.459 đoạn | từ build record runtime |
| Build record runtime | sha256 `03829ed641f7` | `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`; point_count 8.459 |
| Sparse state | sha256 `dbd5f7bc538d` | `full_corpus_sparse_state.json` |
| Nhóm chia thử / kiểm | sha256 `e2b1788dfbbc` | `split.json` (120 / 56) |
| Đoạn đúng | sha256 `bab707b9ab22`, 55 dòng | `gold_draft.jsonl` |
| Nhãn độ tự nhiên | sha256 `0b65d1c138d2`, 176 dòng | 82 / 65 / 29 |
| Golden chính thức | md5 `0f7dbf41b422`, 176 dòng | đổi `reference_answer` ở **10 dòng**: 23, 41, 46, 92, 93, 141, 151, 157, 165, 174 (case_index 22, 40, 45, 91, 92, 140, 150, 156, 164, 173); bản 7A sao lưu md5 `c30b56f22bd3` |
| Golden smoke | md5 `d80b58c50f38`, 10 dòng | |
| Golden authoring (7 file, md5) | foods `8c5ece0974a7` (37) · heritages `a96c27db4c9b` (36) · festivals `8244bf99fef2` (27) · performing_arts `658f56bca906` (17) · travel/places `815e8f848b96` (32) · travel/services `fb57cc1fd2ea` (13) · travel/tickets `d932c662a315` (14) | tổng 176 |
| 7B Run 1 câu trả lời | sha256 `32e2fb6d7035`, 176 dòng | `data/evaluation/phase_7b/run1_answers.jsonl` |
| 7B Run 1 điểm Claude | sha256 `c277f807ae20`, 176 dòng | `claude_run1.jsonl`. **10 câu ở trên chấm theo đáp án cũ** ⇒ không so trực tiếp |
| Câu kín bản soạn v6 | md5 `631334704fdd` | chỉ hash, C không đọc |
| Nhãn câu kín | md5 `d1f7c235b83c`, 36 dòng | 36/36 tự nhiên |
| Câu kín chính thức 4 field | **chưa có** | chờ User duyệt mẫu bản 5 |
| Collection Qdrant | chỉ `hue_full_corpus_7a2_e5_small_384` | |

## 3. Mốc retrieval tái lập

| Cách trộn | Mốc đã lưu | Chạy lại 14:13 | Kết quả |
|---|---|---|---|
| `dense_bm25_rrf` (runtime) | `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl` `cefb2d1a…` | `cefb2d1a…` | **PASS** (giống từng byte) |
| `native_hybrid_rrf` | `data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl` `1fbb5c17…` | `1fbb5c17…` | **PASS** (giống từng byte) |

## 4. Kiểm cuối tiêu chí spec §6.1 và §6.4

| Tiêu chí | Kết quả | Căn cứ |
|---|---|---|
| §6.1 tự kiểm thống kê (đối chứng âm + dương) | đạt | `phase_8_1_g0_1_2_measure_implementation.md` §4 |
| §6.1 tham số mặc định-như-cũ không đổi runtime | đạt; mốc byte giữ nguyên sau mọi sửa production của 8.1 (B11, G4 `cross_encoder.py`, G3 `full_corpus_pipeline.py`) | review G0.5 / G4 / G3 |
| §6.1 baseline tái lập byte | đạt (§3) | lần chạy 14:13 |
| §6.1 file chia, đoạn đúng, câu kín tồn tại và được duyệt | chia + đoạn đúng: đạt. Câu kín: soạn xong và kiểm, **chờ User xem mẫu bản 5** | §2 |
| §6.4 runtime giống byte mốc 7B | đạt (§3) | |
| §6.4 Qdrant chỉ còn collection runtime | đạt; mọi `hue_81_*` của G3 (11) đã xóa, có danh sách trước / sau. G4 / G4K không tạo collection | report G3 §4; G4K report |

## 5. Bước tiếp (khi A nhắn "User đã duyệt mẫu bản 5")

```bash
cd backend
HF_HUB_OFFLINE=1 uv run python -I ../data/phase_8_1/tools/make_sealed_official.py \
  --src ../knowledge-base-hue/evaluation/phase_8_1/sealed_authoring.jsonl \
  --out ../knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl --expect-md5 631334704fdd
```

Sau đó:
- ghi md5 / số dòng / phân bố / exit code vào manifest (`evaluation_sets.sealed_official`) và vào §2 report này;
- **cập nhật manifest** `git.head` + `dirty_paths_not_in_runtime` theo HEAD lúc khóa (bản ghi 14:15 là `8a909e0`; nay đã có
  commit mới), và thêm sha script câu kín `ce5ff542945b` (review B m2);
- A khóa G0.6.

Nếu User yêu cầu sửa thêm câu kín, bản soạn sẽ đổi md5 và script tự dừng. Khi đó làm lại quy trình sửa / kiểm như C24–C26.

## 6. Giới hạn

- Câu kín chính thức chưa tạo, nên G0.6 chưa khóa.
- Manifest ghi trạng thái working tree lúc 14:15. Nếu A commit thêm trước khi khóa thì `git.head` đổi; khi khóa nên ghi lại
  HEAD (các hash dữ liệu không phụ thuộc commit).

Tiền: **0 USD**.
