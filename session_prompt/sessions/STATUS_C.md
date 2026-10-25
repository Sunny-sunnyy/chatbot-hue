# STATUS C — cập nhật 2026-10-25 17:08 (kết phiên; C34 DỞ)

Terminal: `hue-rag-d6` (mở 15:50 25/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi.
User 25/10 15:53: C làm việc và báo cáo trực tiếp cho A; việc A giao = "làm đi"; xong báo cáo, nhắn A, chờ việc.

## Đang làm / dở (phiên chiều-tối 25/10)
- **C34 rà code luồng trả lời + đánh giá — DỞ** (User kết phiên 17:0x). Report `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md`
  (đầu file ghi đã rà / chưa rà). 8 finding: **C-01 vừa** (runtime nạp `core.schema` hai lần ⇒ API bắt hụt lỗi retrieval: 500 thay
  503, 503 thay 409 — gốc ở `ingestion/full_corpus_pipeline.py` import kiểu `backend.*`, phạm vi B25), **C-02 vừa** (`g2_generate.paired`
  ngược dấu với `refusal`), C-03 → C-07 thấp, C-08 đo latency tìm kiếm ổn.
  - **Còn phải rà:** `frontend/`, `reranking/`, `llm/evidence_recorder.py`, 2 file smoke, phần còn lại evaluator, test, notebook 06,
    guide `phase_5`–`phase_9` + `llm_rag_reference` + phần trả lời `full_corpus_rag.md`, `experiments/phase_8_1/`.
  - 3 sub-agent (guide / test / harness) đã dừng, chưa ghi kết quả; brief dùng lại: `data/ra_soat_code_2026-10-25/tools/brief_common.md`.
  - Sau khi xong: C kiểm chéo top 5 của B (B25).
- **C33 plan E1** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_e1_plan.md` sha `f86240418ca1` — chờ B review + A trả lời Q1–Q3
  (8.2 tạm dừng). **Phải sửa khi 8.2 chạy lại:** §4 / §5 dùng `g2_generate.paired(…'refusal')` + chữ "thắng / thua" theo nghĩa câu được
  cứu ⇒ ngược dấu (C-02); đổi sang `paired_compare` (`false_refusal`) hoặc ghi đảo dấu ⇒ sha mới.
- **C32 rà nội dung kho — xong**, A review `ready_for_user_confirmation` (`report_agent/2026-10-25_ra_soat_noi_dung_kho/`); chờ User xác
  nhận. (A: User hỏi về code, C32 là hiểu nhầm — giữ làm hồ sơ.)
- **Đang khai báo sửa:** không.
- **C chưa đọc nội dung câu kín.** Câu kín chính thức md5 `ddc59587b502`, manifest `9ea480d0d083`; mở ở mốc cuối 8.2 do User quyết.

## Câu hỏi cho A / User
- C-01 sửa chung với B25 (ingestion là phạm vi B): ai sửa, khi nào?
- C32: file `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index — loại ở lần
  build lại?
- E1 plan Q1–Q3 (§10 plan).

## File private C tạo phiên này (không commit)
- C32: `data/ra_soat_kho_2026-10-25/` (`files.txt`, `facts_*`, `g*_*.txt`, `sub_g*.md`, `danh_sach.md`, `self_check_ids.json`, `tools/`).
- C33: `data/phase_8_2/e1_plan/` (`count_p1.py`, `sample_size.py`, `p1_detail.md` — có câu hỏi Golden, private).
- C34: `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `brief_common.md`).
- File tạm: `/tmp/c34/` (bản sao các script trên, không nội dung private) — xóa được; `rm` có thể bị chặn ⇒ nhờ User `!rm -r /tmp/c34`.

## Đã học / bẫy gặp
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
Paid API C chạy phiên này: **0 USD**. Quota Claude Code cho sub-agent: C32 ~2,1M token (8 sub-agent); C34 3 sub-agent bị dừng giữa chừng.
