# STATUS C — cập nhật 2026-10-25 15:27 (kết phiên; Phase 8.1 User đóng)

Terminal: `hue-rag-a1` (25/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi.
User 25/10: việc A giao = "làm đi"; xong báo cáo, nhắn A, chờ việc.

## Đang làm / chờ
- **Kết phiên 15:27.** User đóng Phase 8.1 (15:2x, "đóng 8.1"). G0.6 A đã khóa (commit `292e0fb`, A tự kiểm 34/34 hash).
  - Việc cuối của C: C31 câu kín chính thức `sealed_official.jsonl` md5 `ddc59587b502`; manifest `9ea480d0d083`; B kiểm đạt.
  - Không có việc dở.
- **Đang khai báo sửa:** không.
- **C chưa đọc nội dung câu kín.** Mọi việc câu kín qua sub-agent mới hoặc script không in nội dung. A đã thấy 3 câu do User
  trích.
- **Phiên sau (8.2):** chờ A giao. Câu kín chính thức chỉ mở để chấm ở mốc cuối 8.2 do User quyết (`Session_Prompt.md` §5).

## Xong hôm nay 25/10 (đều 0 USD; quota Claude cho sub-agent)
| Việc | Kết quả | File |
|---|---|---|
| C23 review B16 + plan G2/G4 | 2 vòng, ready | `phase_8_1_b16_review.md` |
| Review G4 (rerank) | ready; lượt GPU kiểm lại 10/10 giống B | `phase_8_1_g4_review.md` |
| C24 / C25 / C26 câu kín | đủ dấu; sửa 4 + 1 đáp án; 2 / 21 / 33 thành tự nhiên; kín v6 `631334704fdd`; mẫu bản 5 `4f7fe6df5cca` | `phase_8_1_g0_4_sealed_review.md` §8–§10 |
| C27 review sửa 10 đáp án Golden | ready; official `0f7dbf41b422` | `phase_8_1_golden_fix_review.md` |
| C28 + C29 G3 chia đoạn | không biến thể nào tốt hơn; 11 collection tạo / xóa | plan `phase_8_1_g3_plan.md` (`d89a919067ba`), report `phase_8_1_g3_implementation.md` (`834342d24899`) |
| Review G2, plan B18, B18, B20, B21 | ready (G2 m1 đóng; B20 m1 / m2 đóng) | `phase_8_1_g2_review.md`, `…g4_keyword_plan_review.md`, `…g4_keyword_review.md`, `…b20_user_reports_review.md`, `…b21_research_prompt_review.md` |
| C30 báo cáo User | DANH_GIA b2, GOLDEN b5, EMBEDDING b3; commit `23e0cbf` | `bao_cao_he_thong/` |
| C31 chuẩn bị khóa G0.6 | PREPARED; mốc runtime `cefb2d1a` / native `1fbb5c17` giống byte; B review ready | `phase_8_1_g0_6_baseline_lock.md` (`14a1eb0dbe1e`) |

Code C viết (A đã commit): `backend/ingestion/full_corpus_pipeline.py` (`chunks=None`),
`backend/experiments/phase_8_1/g3_chunking.py`.

## File private C tạo hôm nay (không commit)
- **Câu kín, sao lưu:** `knowledge-base-hue/evaluation/phase_8_1/sealed_authoring_v{3,4,5}_backup.jsonl`,
  `sealed_realism_v5_backup.jsonl`, `sealed_user_sample_v{3,4}_backup.md`.
- **G3:** `data/phase_8_1/g3/` (JSONL / meta, `budget.json` B = 750, `budget10.json` B10 = 1.500, `gate750_*`, `b10_*`) và
  `data/phase_8_1/builds/<biến thể>/` (record, sparse, `variant.json`).
- **G4:** `data/phase_8_1/g4/c_rerun_m1.*`. **G4K:** `data/phase_8_1/g4k/c_check_bigram_native.jsonl`.
- **G0.6:** `data/phase_8_1/baseline/g0_6_manifest.json`, `data/phase_8_1/tools/make_sealed_official.py`.

## Script tạm ở /tmp
- **Đã dọn hết lúc kết phiên (15:27):**
  - `/tmp/c23`, `/tmp/c28`, `/tmp/c29`, `/tmp/c31` và các file `/tmp/c23_*` … `/tmp/c31_*`, `/tmp/c27b.txt` (một số chứa dòng
    Golden dùng để thử);
  - trước đó đã xóa `/tmp/c24_*`, `/tmp/c25_*`, `/tmp/c26_*` (script sub-agent).
- Bản cần giữ đều ở `data/phase_8_1/` (private).

## Đã học / bẫy gặp
- **Repo public:** file tracked không chép tên / số / đường dẫn dự án khác của User, câu Golden, câu kín, số liệu corpus.
- **Giữ mù câu kín:**
  - brief sub-agent cấm cả **tên file nguồn** trong báo cáo cuối (C24: lộ chủ đề);
  - grep corpus phải loại `evaluation/` (C26: người sửa lỡ in 1 dòng của file mẫu);
  - xóa thư mục script tạm của sub-agent sau mỗi việc;
  - so dòng bằng md5 / byte, chỉ in số dòng và đúng / sai.
- **Giờ trong file luôn lấy bằng `date`.** 14:2x C lỡ ghi giờ ước ở review B20, đã đính chính ngay trong file.
- **Tin nhắn có thể tới khi lệnh đang chạy:** build H1 xảy ra trong lúc A / B chốt §9. Trước một bước "đo / thay đổi" nên
  đọc tin mới; nếu đã lỡ thì báo rõ "đã build, chưa đo".
- **Không báo "đã xong" trước khi lệnh ghi file trả kết quả:** 14:24 C nhắn A "STATUS_C đã cập nhật" cùng lượt với lệnh ghi
  bị từ chối (file đổi từ lần đọc trước), nên phải ghi lại và đính chính.
- **Thước đo:**
  - so biến thể chia đoạn phải cùng ngân sách token;
  - keyword trong context tính trên `search_text`, nên lệch với biến thể đổi tiền tố / gộp đoạn ⇒ quyết bằng đoạn đúng
    (offset);
  - ngưỡng keyword là điểm % (0–100);
  - chỉ số nhị phân + sàn "0 câu mất" làm điều kiện "không kém có CI" trở thành thừa.
- **Harness:**
  - `compare` của G3 phải bỏ câu out_of_scope (n = 88);
  - runtime gọi tầng sparse là `bm25`;
  - `PackedSource` không có `chunk_id` ⇒ dùng `packed_chunk_ids`;
  - script ghi file đích nên ghi `.tmp` rồi mới đổi tên.
- **Quyền:** chạy GPU phải được A ghi rõ; trước khi chạy kiểm `nvidia-smi` + dòng "đang giữ GPU" trong file này.
- Chạy script import `backend.*` từ repo root, hoặc thêm `.` / `..` vào `sys.path` khi chạy từ `backend/` với `python -I`.
  Sửa text nhiều dòng thì dùng `uv run python -I` hoặc Edit, không dùng system python.

## Tiền
Paid API do C chạy hôm nay: **0 USD**. Quota Claude Code cho sub-agent câu kín: ~46k + 62k (C24), ~103k + 56k (C25),
~76k + 75k (C26) token.
