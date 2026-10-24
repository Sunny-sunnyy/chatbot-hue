# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 tối (A). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở; việc
xong chuyển tóm tắt sang `PROJECT_HISTORY.md`. Đợt hiện tại: `report_agent/2026-10-24_to_chuc_bao_cao/`.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc hiện tại | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-77` | Claude Opus 5.5 | trực tiếp | Điều chỉnh cách làm việc theo MekongAI | đang làm |
| B — thực thi | `hue-rag-64` | Claude Opus 5.5 | trực tiếp | B9 dọn sau Phase 7 | đang làm |
| C — thực thi | `hue-rag-d9` | Claude Opus 5.5 | trực tiếp | — | rảnh |

User 2026-10-24: cả ba là Claude Code nên liên lạc `trực tiếp`.

## Quyền đang hiệu lực (User duyệt qua A)

- **User 2026-10-24 (trước khi nghỉ):** A được commit, push, tự điều phối, tự kiểm
  tra, tự tối ưu và phát triển hệ thống; tự dùng chi phí `gpt-6-luna` trong ngân sách.
- **Ngân sách `gpt-6-luna`:** giá 0,1 USD/1M input, 0,5 USD/1M output. Tổng session
  ≤1 USD (không bao giờ vượt 1,5 USD), "không cần dùng hết". Đã dùng ~0,087 USD (7B + thăm dò).
  Mỗi session gọi paid phải ghi usage token và báo tổng tiền trong report.
- Git: A commit/push `origin main`; B/C không commit.
- Qdrant: chỉ đọc.
- Duyệt cho A = duyệt cho B/C (User 2026-10-24). User đồng ý xóa những gì không còn
  cần/lỗi thời — A vẫn liệt kê đích và trình trước khi xóa thứ gì chưa có trong
  một việc đã duyệt.

## Việc chung — viết lại user report các Phase (User 2026-10-24, rủi ro thấp, free)

- **Mục tiêu:** User đọc để hiểu hệ thống từng Phase làm gì và **hôm nay còn đúng không**. 27 user
  report cũ ở `reports/user_reports/` (lịch sử) lẫn nhiều bản Foods, khó đọc thành mạch.
- **Nơi ghi (User 2026-10-24, theo MekongAI):** `bao_cao_he_thong/` ở gốc repo, mỗi khâu một file
  (tiêu đề ghi Phase tương ứng):

| Phase | File trong `bao_cao_he_thong/` | Ai |
|---|---|---|
| 0–1 | `BAO_CAO_NEN_TANG.md` | B |
| 2 | `BAO_CAO_CHIA_DOAN.md` | B |
| 3 | `BAO_CAO_EMBEDDING_TU_KHOA.md` | B |
| 4 | `BAO_CAO_LUU_TRU_QDRANT.md` | B |
| 5 | `BAO_CAO_TIM_KIEM.md` | C |
| 6 | `BAO_CAO_SINH_CAU_TRA_LOI_API.md` | C |
| 7, 7A | `BAO_CAO_BO_CAU_HOI_GOLDEN.md` | C |
| 7A2 | `BAO_CAO_KHO_DU_LIEU.md` | C |
| 7B | `BAO_CAO_DANH_GIA.md` | A (xong) |
| — | `LUONG_HOAT_DONG_HE_THONG.md` | A (xong) |

- **Mẫu:** `session_prompt/TEMPLATE_USER_REPORT.md`, tiếng Việt thường, ngắn (~60–120 dòng), thêm mục
  bắt buộc **"Hôm nay còn đúng không"**: mỗi kết quả/quyết định chính → *còn dùng* / *đã thay bởi …
  (Phase nào)* / *đã bỏ*, kiểm bằng code + `Project_Status.md` hiện tại (dẫn file:dòng), không chép
  report cũ. Đây cũng là bước "kiểm tra lại các Phase trước" User yêu cầu: chỗ nào tài liệu và code lệch
  thì ghi ở cuối file mục "Lệch phát hiện" và nhắn A.
- **Đọc:** `reference-only` report/spec/history của Phase đó (`PROJECT_HISTORY.md`, `reports/`,
  `docs/superpowers/specs/`), `guides/`; mở khi cần trả lời câu cụ thể. Không chép Golden/corpus.
- **Không làm:** sửa code, dữ liệu, Qdrant; gọi paid; sửa report cũ.
- **Xong:** cập nhật `STATUS_<X>.md` ngay sau mỗi file; nhắn A danh sách file; A review (người làm khác
  người kiểm).

## Việc của A

1. **A1:** `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` và `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md`;
   **Xong, chờ review** — B review A1 sau khi xong B8 (đối chiếu số với report 7B + code).
2. Khi User gửi `report_agent/2026-10-24_to_chuc_bao_cao/MO_TA_CACH_LAM_VIEC_MEKONGAI.md`: tối ưu
   governance/report cho hue_rag (đề xuất cho User trước khi đổi lớn).
3. B8, C8 A đóng 2026-10-24 (báo cáo Phase 0–7A2 trong `bao_cao_he_thong/`); C7 đóng. A1: B review
   `changes_requested` → A sửa → B kiểm lại: đóng cả 7 finding (A1 đóng). Sau đó: trình User danh sách dọn C2; brainstorm Phase 8.

## Việc của B

### B9 — Dọn sau Phase 7 (User duyệt 2026-10-24: "không còn cần thiết, xoá mà hệ thống vẫn chạy bình thường thì xoá")

Mức rủi ro: cao (xóa code + 2 collection). Đích = `reports/phase_7_cleanup_inventory_2026_10_24.md`
(C2) §2.1–2.5, §2.6 dòng `data/full_corpus_metadata_v2_*`, §2.7 `requirements.txt`; theo ràng buộc §3.

- **Trước khi xóa — tiêu chí ghi trước + mốc so sánh (free):** lưu output hiện tại của
  `full_corpus_eval retrieval --treatment dense_bm25_rrf` (đã có `retrieval_dense_bm25_rrf_1.jsonl`)
  làm mốc; sau dọn chạy lại phải **giống từng byte**. Liệt kê lại Qdrant collections; khác
  {2 Foods + 1 full-corpus} thì dừng.
- **Làm (một lượt code, rồi Qdrant):**
  1. Gỡ code/test/notebook/settings Foods theo C2 §2.2–2.5 (sửa `settings.yaml` + `settings_loader.py`
     cùng lúc; xóa module Foods cùng fixture Foods trong `conftest.py`; giữ `vector_database.url/timeout`;
     xóa `evaluation/{eval,evaluator,test,template,golden_dataset,retrieval_comparison,*_benchmark}.py`
     + 2 CSV; `embedding/dense_benchmark.py`). Notebook: xóa 02, 05, 07, 08a, 08b, 08c; sửa markdown 03,
     06; sửa notebook 04 (chỉ candidate có build record, sample id như `full_corpus_pipeline.py`) và Run
     All trên bản tạm (Qdrant chỉ đọc), outputs rỗng trong repo. Xóa `requirements.txt`.
  2. Sửa test chunker so với artifact 8.460 cũ (`test_full_corpus_chunker.py:984-996`) để so với số
     hiện hành hoặc bỏ phần so artifact — không đổi chunker.
  3. Kiểm (C2 §5) + so byte retrieval + API in-process `/health` 200 + 1 retrieval; smoke 10
     `generate --golden smoke` (paid ≤0,005 USD) để chắc đường sinh còn chạy.
  4. Đạt hết mới xóa 2 collection Foods (`hue_foods_e5_small_384`, `hue_foods_e5_small_384_dense`),
     liệt kê trước/sau. Xóa `data/full_corpus_metadata_v2_*.json` (5 file, liệt kê trước).
- **Không làm:** đụng `knowledge-base-hue/` (giữ Golden Foods V2/V3 và
  `foods/evaluation/golden_full_corpus_authoring.jsonl`); sửa chunker (overlap để Phase 8); sửa
  governance `session_prompt/` (A làm); `phase6_live_smoke.py`, `full_corpus_smoke.py` (C2 §4, giữ).
- **Quyền:** Qdrant xóa đúng 2 tên trên; paid ≤0,005 USD; không commit. Bị permission chặn `rm`/xóa
  Qdrant thì dừng, nhờ User chạy bằng `!` trong terminal B.
- **Dừng:** byte so retrieval khác; test full-corpus fail; API không lên.
- **Đầu ra:** `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` (danh sách
  xóa/sửa, lệnh kiểm + kết quả); `STATUS_B.md`; nhắn A → C review.

## Việc của C

### C7 — Cập nhật giả thuyết Phase 8 bằng nghiên cứu (free)

- Đọc `gửi chatgpt/2026-10-24/kết quả nghiên cứu/phase_8_rag_retrieval_2026_10_24.md` (+ phần liên
  quan của `phase_7b_rag_evaluation_2026_10_24.md`); WebFetch đối chiếu vài URL then chốt; cập nhật
  cột "Cách làm phổ biến" + nguồn trong `reports/phase_8_candidate_hypotheses_2026_10_24.md` (sửa tại
  chỗ, ghi mục "Cập nhật"); thêm input B4/B5 (từ chối nhầm, context 10) vào thứ tự ưu tiên nếu đổi.

### C8 — User report Phase 5, 6, 7/7A, 7A2 (theo "Việc chung")

- File: theo bảng ở "Việc chung" (C tự chuyển 4 file đang viết từ `report_agent/user_reports/`).

## Đang chờ User

- Gửi prompt `report_agent/2026-10-24_to_chuc_bao_cao/PROMPT_GUI_MEKONGAI.md` cho Claude ở MekongAI,
  lưu kết quả `MO_TA_CACH_LAM_VIEC_MEKONGAI.md` cùng folder.
- Quyết định Phase 8 khi brainstorm: trả lời phần có căn cứ hay từ chối cả câu (H8).
- Quyết định Phase 8: có tách Golden thành nhóm phát triển / giữ kín không (C7 §8: tối ưu trên cả 176
  rồi báo trên chính bộ đó là đo lạc quan; spec 7A §8 từng chốt không chia).
