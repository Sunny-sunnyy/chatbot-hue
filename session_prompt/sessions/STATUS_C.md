# STATUS C — cập nhật 2026-10-25 19:52 (phiên tối; C35 gói 1a XONG, chờ B review)

Terminal: `hue-rag-7f` (mở 18:2x 25/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi.
User 25/10 15:53 + 18:2x: C làm việc và báo cáo trực tiếp cho A; việc A giao = "làm đi"; xong báo cáo, nhắn A, chờ việc.
User 18:3x (qua A): rà code chỉ rà và đề xuất, chưa sửa gì; User đồng ý từng mục mới sửa.

## Đang làm / dở (phiên tối 25/10)
- **C34 rà code luồng trả lời + đánh giá — XONG 18:43, chờ kiểm chéo.** Report `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md`
  (top 10 đầu file). 18 finding: **C-09 cao** (validator citation chỉ bắt `[n]`, context gắn `[Nguồn n]` ⇒ 8 / 176 câu chatbot hiện tại
  ra 500; nguyên nhân 8.1 ghi chưa đúng; quyết định 8.1 reasoning có thể mở lại — A tự kiểm 18:3x, đúng), **vừa** C-01 (đã tái tạo index
  cũ ⇒ 503 thay 409; sửa phải kèm tách lỗi "model không nạp"), C-02, C-12 (guide 7 / 8); còn lại thấp. C-09 có cách đo M1–M3.
  - 3 sub-agent (S1 guide + nb06, S2 test, S3 harness + smoke) xong; C tự kiểm khẳng định chính bằng file thật. Đầu ra gốc `/tmp/c34/s*.md`.
- **Kiểm chéo 5 mục B25 (B-11, B-12, B-16, B-17, B-20) — XONG 18:55** (A "làm đi" 18:4x). `report_agent/2026-10-25_ra_soat_code/kiem_cheo_C.md`:
  4 đúng, B-17 một phần; `ready_for_user_confirmation` + R1–R4 minor. Script riêng `/tmp/c34x/` → `data/ra_soat_code_2026-10-25/tools/kiem_cheo_C/`.
  Không đọc STATUS_B, không chạy script của B. 0 USD.
- **C33 plan E1** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_e1_plan.md` sha `f86240418ca1` — chờ B review + A trả lời Q1–Q3
  (8.2 tạm dừng). **Phải sửa khi 8.2 chạy lại:** §4 / §5 dùng `g2_generate.paired(…'refusal')` + chữ "thắng / thua" theo nghĩa câu được
  cứu ⇒ ngược dấu (C-02); đổi sang `paired_compare` (`false_refusal`) hoặc ghi đảo dấu ⇒ sha mới.
- **C32 rà nội dung kho — xong**, A review `ready_for_user_confirmation` (`report_agent/2026-10-25_ra_soat_noi_dung_kho/`); chờ User xác
  nhận. (A: User hỏi về code, C32 là hiểu nhầm — giữ làm hồ sơ.)
- **C35 gói 1a (C-09 citation `[Nguồn n]`) — XONG 19:52, chờ B review.** Report `report_agent/2026-10-25_ra_soat_code/sua_1a_implementation.md`.
  File: `backend/llm/citations.py`, `backend/api/routes/chat.py`, `backend/tests/test_citations.py`, `backend/tests/test_api_chat.py` (A duyệt
  `chat.py` + `test_api_chat.py` 19:5x). Offline 1.600 câu: lỗi 69 → 14, 0 câu đạt hỏng / đổi nguồn; pytest 35 passed + test route; API thật 2 câu
  0,000427 USD. Chưa commit (A). Script `data/ra_soat_code_2026-10-25/tools/sua_1a/`.
- **Đang khai báo sửa:** 4 file trên (giữ tới khi A commit; sửa theo review của B nếu có).
- **C chưa đọc nội dung câu kín.** Câu kín chính thức md5 `ddc59587b502`, manifest `9ea480d0d083`; mở ở mốc cuối 8.2 do User quyết.

## Câu hỏi cho A / User
- C-01 = B-01 một finding chung; ai sửa quyết sau khi User chọn mục sửa (A 18:2x). Lệnh build chạy từ gốc repo, API từ `backend/` ⇒
  phải chọn một quy ước import cho cả hai.
- C-09 M2: có mở lại quyết định 8.1 reasoning `none` không (User quyết; xác nhận test ~0,007 USD, NOT RUN).
- C32: file `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index — loại ở lần
  build lại?
- E1 plan Q1–Q3 (§10 plan).

## File private C tạo phiên này (không commit)
- C32: `data/ra_soat_kho_2026-10-25/` (`files.txt`, `facts_*`, `g*_*.txt`, `sub_g*.md`, `danh_sach.md`, `self_check_ids.json`, `tools/`).
- C33: `data/phase_8_2/e1_plan/` (`count_p1.py`, `sample_size.py`, `p1_detail.md` — có câu hỏi Golden, private).
- C34: `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `brief_common.md`, `nguon_count.py`,
  `cite_shapes.py`, `recheck_both.py`, `c01_probe_stale.py`, `c01_probe_bogus_reranker.py`).
- File tạm: `/tmp/c34/` (đầu ra sub-agent S1–S3 + script tạm; chỉ số đếm, không nội dung kho) — xóa sau kiểm chéo; `rm` có thể bị chặn ⇒
  nhờ User `!rm -r /tmp/c34`.

## Đã học / bẫy gặp
- **Chỉ số lỗi do validator đếm: phân loại theo hình dạng output trước khi kết luận nguyên nhân** (C-09: 8.1 ghi "model quên `[n]`",
  thực tế model viết `[Nguồn n]` theo nhãn context; đếm lại trên file có sẵn, 0 USD, đổi được một quyết định).
- **Loại trừ theo danh sách discovery, không theo mẫu tên** (C32: brief cấm `*inventory*` làm sub-agent bỏ 1 file runtime; đính chính
  bằng vòng 2).
- **Import hai kiểu (`backend.X` / `X`) tạo hai bản module** ⇒ `except` / `isinstance` hụt. Script C chạy từ `backend/` với `python -I`
  phải thêm cả `..` và `.` vào `sys.path` (vì `ingestion/full_corpus_pipeline.py` chỉ import `backend.*`).
- **Hàm so cặp của harness 8.1 không đổi dấu cho chỉ số "càng thấp càng tốt"** — dùng `paired_compare` của evaluator.
- `grep` ở máy là ugrep: regex dài báo "exceeds complexity limits" ⇒ tách ngắn hoặc dùng Python.
- Kết phiên có thể tới giữa việc: dừng sub-agent ngay (`TaskStop`), ghi phần đã có kèm "DỞ — đã rà / chưa rà"; script bằng chứng
  chuyển từ `/tmp` sang `data/<đợt>/tools/`.
- Giữ từ trước: repo public (không chép nội dung kho / Golden / câu kín / dự án khác vào file tracked); giờ lấy bằng `date`; không báo
  "đã xong" trước khi lệnh ghi file trả kết quả; đọc tin mới trước bước đo / thay đổi; chạy GPU phải được A ghi rõ.

## Tiền
Paid API C phiên tối 25/10: **0,000427 USD** (C35, 2 lượt `gpt-6-luna`; C34 + kiểm chéo 0 USD).
Phiên chiều 25/10: paid **0 USD**. Quota Claude Code cho sub-agent: C32 ~2,1M token (8 sub-agent); C34 3 sub-agent bị dừng giữa chừng.
