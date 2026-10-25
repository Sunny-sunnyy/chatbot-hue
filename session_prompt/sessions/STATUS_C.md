# STATUS C — cập nhật 2026-10-25 21:28 (phiên tối; gói 3 đã commit 47a4e32; plan đợt 3 XONG, chờ B review sau 1b)

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
- **Review B26 (gói 4 tài liệu) — XONG 20:16.** `report_agent/2026-10-25_ra_soat_code/sua_4_review.md`: ready_for_user_confirmation; m1–m3 (3 câu
  mục build lại) nên sửa trước commit; m4 banner guide 5 / 6 (A quyết); o1 = C-21 mới: `build_candidate` ghi sparse state trước khi kiểm đích.
- **C35 gói 1a (C-09 citation `[Nguồn n]`) — ĐÓNG 19:59 (commit `9e6d371`).** Report `report_agent/2026-10-25_ra_soat_code/sua_1a_implementation.md`.
  File: `backend/llm/citations.py`, `backend/api/routes/chat.py`, `backend/tests/test_citations.py`, `backend/tests/test_api_chat.py` (A duyệt
  `chat.py` + `test_api_chat.py` 19:5x). Offline 1.600 câu: lỗi 69 → 14, 0 câu đạt hỏng / đổi nguồn; pytest 35 passed + test route; API thật 2 câu
  0,000427 USD. Chưa commit (A). Script `data/ra_soat_code_2026-10-25/tools/sua_1a/`.
- **Review plan 1b (sha `aa9bbf3650d6`) — XONG 20:25:** `sua_1b_plan_review.md` = changes_requested (P1 T-A tham chiếu tên chat.py không có;
  P2 T-C 503 có thể xanh giả — phải kiểm nguyên nhân) + m1–m4; số đếm (a)/(b) của B khớp; đồng ý (b). T-C với HF_HOME rỗng: auto mode chặn, NOT RUN.
- **Kiểm lại sua_4 — đóng 20:27** (m3: C sai, B đúng).
- **Gói 3a / 3b — XONG 20:37, chờ B review.** `report_agent/2026-10-25_ra_soat_code/sua_3_implementation.md`. 5 file (`evaluation/full_corpus_eval.py`
  `paired_stats`; `llm/full_corpus_prompt.py` `build_answer_input`; generator; 2 test). So cặp trên file thật giống byte; chuỗi gửi model 25 câu tự viết
  giống byte; cổng ổn định uvicorn đạt (2 câu, ~0,0004 USD ước — route không log usage). Chưa commit.
- **Review gói 1b — XONG 21:48:** `report_agent/2026-10-25_ra_soat_code/sua_1b_review.md` = ready (K1–K7 đạt khi chạy lại; m1 RetrievalConfigurationError ⇒ 409 không tới được; m2 REPO_ROOT).
- **Đang khai báo sửa:** không.
- **Plan đợt 3 (gói 2 + 5 + B-12) — bản 3 21:50 sha `7c8c660558e5`** (sửa M-1, m-1…m-6 theo review B): `report_agent/2026-10-25_ra_soat_code/sua_dot3_plan.md`; B kiểm phần sửa.
- **Gói 3c phần free — XONG 20:45:** `report_agent/2026-10-25_ra_soat_code/sua_3c_citation_v2.md`; file dẫn xuất `data/ra_soat_code_2026-10-25/citation_v2/`
  (14 lượt + meta sha nguồn). 69 → 14 lỗi; `none` +4 → +2 (hết vi phạm luật ≤ +2, chưa kết luận — cần test paid); `low` vẫn vi phạm; tín hiệu P2 mất;
  A/A context 10 = 0. 0 USD.
- **Danh sách ứng viên cải tiến — XONG 20:41:** `report_agent/2026-10-25_ra_soat_code/ung_vien_cai_tien_C.md` (12 dòng chính, 5 câu hỏi ChatGPT; 0 USD).
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

## Ý cải tiến (A xin danh sách sau 5 gói — chỉ là ý, chưa thử)
- **Route API ghi usage (token vào / ra, latency, số nguồn) mỗi câu vào log** — hiện không đo được tiền / độ trễ trên server thật (cổng ổn định gói 3
  phải ước). Một dòng `logger.info` sau bước sinh; không ghi nội dung câu hỏi (dữ liệu người dùng).
- **Prompt nói "[n]" nhưng context gắn "[Nguồn n]"** (C-09): sau gói 1a validator đã chịu cả hai; thử đổi nhãn context về "[n]" hoặc sửa câu prompt —
  thí nghiệm (đổi đầu vào model), đo lỗi "không ngoặc số" còn lại (14 / 1.600) + Completeness.
- **14 câu "không có ngoặc số"** còn lại sau 1a: xem có phải câu một nguồn / câu liệt kê (model bỏ citation) ⇒ chính sách "một nguồn thì gán" của 8.1
  G2.3 có thể đáng xét lại theo định nghĩa mới.
- **Bộ đếm token context nhận instructions** khi harness đổi prompt (C-03 phần 2) — làm khi 8.2 E1 cần.

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
