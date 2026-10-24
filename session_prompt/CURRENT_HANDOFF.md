# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 (A, mở lại phiên). Cách dùng: `WORKFLOW.md` §3, §7, §9. Chỉ giữ
việc đang mở; việc xong chuyển tóm tắt sang `PROJECT_HISTORY.md`.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc hiện tại | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-77` | Claude Opus 5.5 | trực tiếp | Điều phối Phase 7B; review C | đang làm |
| B — thực thi | `hue-rag-64` | Claude Opus 5.5 | trực tiếp | B1 kiểm sức khỏe Phase trước → B2 Phase 7B Gate 1 | đang làm |
| C — thực thi | `hue-rag-d9` | Claude Opus 5.5 | trực tiếp | C1 rà soát Phase 8 (chờ review A) → C2 danh sách dọn | C1 chờ review |

User 2026-10-24: cả ba là Claude Code nên liên lạc `trực tiếp`. Nếu User đổi một
session sang Codex/AGY thì cột "Liên lạc" của nó là `qua User` (`WORKFLOW.md` §7).

## Quyền đang hiệu lực (User duyệt qua A)

- **User 2026-10-24 (trước khi nghỉ):** A được commit, push, tự điều phối, tự kiểm
  tra, tự tối ưu và phát triển hệ thống; tự dùng chi phí `gpt-6-luna` trong ngân sách.
- **Ngân sách `gpt-6-luna`:** giá 0,1 USD/1M input, 0,5 USD/1M output. Tổng session
  ≤1 USD (không bao giờ vượt 1,5 USD), "không cần dùng hết". Phase 7B ≤0,6 USD (spec 7B §6).
  Mỗi session gọi paid phải ghi usage token và báo tổng tiền trong report.
- Git: A commit/push `origin main`; B/C không commit.
- Qdrant: chỉ đọc.
- Duyệt cho A = duyệt cho B/C (User 2026-10-24). User đồng ý xóa những gì không còn
  cần/lỗi thời — A vẫn liệt kê đích và trình trước khi xóa thứ gì chưa có trong
  một việc đã duyệt.

## Việc của A

1. Review C1; giao C2.
2. Review B1, B2; chọn tập chấm lại 30 + mẫu User ~20 trước Run 1 (spec 7B §4.4).
3. Điều phối các Gate còn lại của 7B; chuẩn bị file chấm cho User.

## Việc của B

### B1 — Kiểm sức khỏe các Phase trước (free, rủi ro thấp)

- **Mục tiêu:** trước khi lấy baseline 7B, xác nhận hệ thống thật khớp tài liệu (User
  2026-10-24: "kiểm tra các phase trước đó, nhớ ghi báo cáo"). Nền hỏng thì baseline
  vô nghĩa.
- **Đọc:** `targeted-read` `Project_Status.md` §4, §8; `guides/full_corpus_rag.md` mục
  cập nhật 7A2.
- **Làm (chỉ đọc + chạy free):**
  1. Corpus: số file 205, số chunk 8.459 (chunker hiện hành, không ghi file).
  2. Build record khớp corpus (freshness); Qdrant point count, payload 7 field, có
     dense + sparse; sparse state vocabulary 5.660.
  3. Runtime: dựng app in-process (`create_app` + lifespan + `httpx.ASGITransport`),
     `/health` 200; một lượt retrieval thật không gọi generation.
  4. Golden: `golden_full_corpus.py` kiểm file chính thức + smoke không lỗi.
  5. Test suite free trong `backend/tests/` (bỏ test có paid call, ví dụ
     `test_llm_generator_openai.py`): ghi pass/fail/skip; test gãy vì tên Foods/collection
     cũ thì ghi lại, **không sửa** (thuộc việc dọn).
  6. Đối chiếu nhanh `Project_Status.md` §4 với số đo; ghi mọi chỗ lệch.
- **Không làm:** sửa code/dữ liệu/Qdrant; gọi paid; build lại index.
- **Đầu ra:** `reports/phase_7b_gate_0_health_audit_2026_10_24.md` (bảng mục kiểm →
  PASS/PARTIAL/FAIL/NOT RUN + bằng chứng; lệch; đề xuất); `STATUS_B.md`; nhắn A.
- **Dừng:** runtime không khởi động hoặc freshness fail → báo A ngay.

### B2 — Phase 7B Gate 1 (sau B1, trung bình, paid ≤0,02 USD)

- **Đọc:** `full-read` `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`;
  `targeted-read` `backend/api/app.py` (`create_app`), `backend/evaluation/eval.py`
  (metric), `backend/llm/generator_openai_full_corpus.py`, rubric trong
  `guides/full_corpus_rag.md`.
- **Làm:** review thiết kế trước (gửi A finding nếu có, rồi mới code); làm Gate 1 theo spec
  §5: module `backend/evaluation/full_corpus_eval.py`, prompt
  `backend/evaluation/full_corpus_judge_prompt.md`, test logic thuần; retrieval eval 176
  ×2 `dense_bm25_rrf` + 1 lần `native_hybrid_rrf`; smoke 10 (sinh + judge luna) ghi token
  thật, dự báo tiền Gate 2.
- **Không làm:** chạy Run 1/Run 2 (chờ A chọn tập con); sửa runtime/prompt sinh/Golden.
- **Quyền:** paid `gpt-6-luna` ≤0,02 USD cho smoke; Qdrant chỉ đọc; không commit.
- **Đầu ra:** `reports/phase_7b_gate_1_evaluator_implementation_2026_10_24.md`; kết quả
  private trong `data/evaluation/phase_7b/`; `STATUS_B.md`; nhắn A.

## Việc của C

### C1 — Rà soát lựa chọn Phase 2–6 cho Phase 8 (xong, chờ review A)

Report `reports/phase_8_candidate_hypotheses_2026_10_24.md`. Yêu cầu ChatGPT
`gửi chatgpt/tìm thông tin/phase_8_retrieval_improvements_2026_10_24.md` chờ User gửi.

### C2 — Danh sách dọn sau Phase 7 (chỉ đọc, rủi ro thấp)

- **Mục tiêu:** liệt kê đích dọn để A trình User (`Project_Status.md` §5: sau Phase 7 xóa
  mọi collection không dùng kèm gỡ code/test/notebook Foods cũ).
- **Làm:** với mỗi đích (2 collection Foods; code/test/notebook/settings tham chiếu Foods
  cũ hoặc collection/model đã xóa — notebook 03, 04, 06, 08a, 08b; evaluator Foods
  `backend/evaluation/{eval,evaluator,test,golden_dataset,…}.py`; file trỏ cũ trong
  `session_prompt/`): đường dẫn/tên chính xác, ai đang tham chiếu (grep), xóa có làm gãy
  gì đang dùng không, đề xuất xóa/giữ/sửa. **Không** đụng các file Phase 7B đang khai báo
  (`backend/evaluation/full_corpus_*`), và ghi rõ hàm metric `eval.py` đang được 7B chép.
- **Không làm:** xóa/sửa bất cứ gì.
- **Đầu ra:** `reports/phase_7_cleanup_inventory_2026_10_24.md`; `STATUS_C.md`; nhắn A.
- Sau C2: C chờ 7B Gate 3 (Claude judge, spec 7B §4.3).

## Đang chờ User

- Gửi ChatGPT hai file trong `gửi chatgpt/tìm thông tin/`:
  `phase_7b_rag_evaluation_2026_10_24.md`, `phase_8_retrieval_improvements_2026_10_24.md`.
- Chấm tay ~20 case 7B khi A báo file chấm sẵn sàng.
