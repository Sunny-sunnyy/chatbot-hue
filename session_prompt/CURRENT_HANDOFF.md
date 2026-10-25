# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 11:05 25/10/2026 (A, **kết phiên sáng 25/10** — phiên chỉ bàn cách làm). Phần dự án dưới đây vẫn là trạng
thái kết phiên 22:52 24/10; **phiên sau quay lại Phase 8.1** (User 25/10). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang
mở; việc xong ở `PROJECT_HISTORY.md` và `report_agent/<đợt>/`.

## Phiên 25/10 sáng — cải tiến cách làm (ĐÓNG, `report_agent/2026-10-25_cai_tien_cach_lam/TONG_HOP.md`)

Đợt `report_agent/2026-10-25_cai_tien_cach_lam/` (`KE_HOACH.md`, `de_xuat_cho_du_an.md`). Mới: skill `improve-workflow` +
sổ `session_prompt/SO_CAI_TIEN_CACH_LAM.md`; `run-experiment` nâng (sàn / mức tụt / chỉ số quyết, cỡ mẫu trước, nhiễu A/A,
kiểm người chấm); Session D (`WORKFLOW.md` §10); `AGENTS.md` (bản chính cho mọi agent) + `CLAUDE.md`; hook
`.githooks/pre-commit` (bật: `git config core.hooksPath .githooks`; kiểm khi mở phiên). **Khi tới G4/G2:** đọc
`de_xuat_cho_du_an.md` mục 1–8 trước khi A duyệt plan B16. Mục "Tạm gác" cũ đã hết hiệu lực (User gửi báo cáo 25/10).

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống lúc kết phiên:** `main` (commit cuối ghi trong `sessions/STATUS_A.md`); chatbot full-corpus chạy được,
**hành vi runtime không đổi trong cả phiên** (retrieval `dense_bm25_rrf` giống byte mốc `cefb2d1a…`). Qdrant
`:6335` (v1.18.3) còn **1** collection `hue_full_corpus_7a2_e5_small_384` (8.459). GPU GTX 1650 4 GB; `.venv` có
torch 2.13+cu130. Repo `chatbot-hue` **PUBLIC**: không commit nội dung/số đo/đường dẫn dự án khác của User,
corpus, câu Golden, câu kín (hook `.githooks/pre-commit` chặn phần máy kiểm được).

**Phase 8.1** (spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md`, **approved** 20:49
24/10, bản 4 + M1 `BAAI/bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker`). Đợt
`report_agent/2026-10-24_phase_8_1_ra_soat/`. Không đổi chatbot; trần paid 0,5 USD cả 8.1 (đã dùng 0 USD ở 8.1).

**Đã xong (đều review chéo + commit):** C11 bảng rà 56 quyết định; G0.1 split 120 dev / 56 test (C16); G0.2
evaluator so theo cặp + đối chứng âm/dương (C16); G0.5 tham số mặc định-như-cũ (B11); B12/B13 sửa phá hòa sparse
native + mốc native mới `1fbb5c17…`; G0.3 đoạn đúng 55 câu (A qua sub-agent, B14 review, áp m1–m8); **G1 chẩn
đoán retrieval** (B15 + C21 review): nghẽn ở **xếp hạng** (union@100 đủ fact 97,5%, top-10 55–60%, context-5
42–50%); 22/22 từ chối nhầm 7B thiếu fact trong context (0 câu đủ bằng chứng mà vẫn từ chối — ngược chẩn đoán
keyword B4); không biến thể trộn nào qua luật; HNSW = exact; NFD tụt, NFC phục hồi; không dấu sập 0,73→0,19.

**Thay đổi CHƯA commit (cố ý, chờ review):** B16 — `backend/experiments/phase_8_1/g1_retrieval.py` (`--realism
main`), `phase_8_1_g1_implementation.md` §7, `phase_8_1_g2_g4_plan.md` (mới), `STATUS_B.md`. C cần review §7 + plan
(A duyệt plan) rồi A commit. File `báo cáo nghiên cứu github.txt` ở gốc là của User — giữ nguyên.

**Thứ tự việc phiên sau:**

1. User copy **khối mới** trong `START_SESSION.md` (đổi 25/10: thêm D, `improve-workflow`). Mở A/B/C bằng `START_SESSION.md`; A `ListAgents`; A **hỏi lại quyền phiên** (§9.8: điều phối rộng, trần
   tiền, commit/push).
2. **A duyệt B16/B17:** `phase_8_1_g2_g4_plan.md` (ước 0,14–0,23 USD) + quyết **lệch spec G4**: spec §5 G4 ghi
   "rerank chỉ xếp lại top-10", nhưng G1 cho thấy 7–9 câu có đoạn đúng ngoài top-10 ⇒ B đề xuất G4-B rerank chọn
   top-10 từ pool 100, guardrail "0 câu mất đoạn đúng khỏi context-5". **A đề xuất:** duyệt G4-A + G4-B như sửa đổi
   spec có lý do (chỉ thí nghiệm, GPU free), báo User; G4 trước (free) rồi G2 (paid nhỏ). Quyết chính sách validator
   cho G2.3. C review §7 G1 + plan; A commit B16.
3. **Câu kín (G0.4) — chờ User:** C22 xong: 36 câu, check exit 0, phân bố direct 15 / multi 6 / cond 7 / comp 5 /
   OOS 3; độ tự nhiên 33 natural / 3 capability_only (dòng 2, 21, 33; đề xuất sửa ở
   `knowledge-base-hue/evaluation/phase_8_1/sealed_review_notes_private_v3.md`). **User chọn:** sửa 3 dòng (sub-agent
   mới, rồi sub-agent khác kiểm) hay giữ; rồi User duyệt mẫu `knowledge-base-hue/evaluation/phase_8_1/sealed_user_sample.md`
   (15 dòng). Cập nhật `sealed_realism.jsonl` theo nhãn cuối. Sau đó A tạo file chính thức 4 field và **khóa**. A và
   C **chưa đọc nội dung câu kín** — giữ như vậy (mọi việc với câu kín qua sub-agent mới).
4. **User duyệt 9 câu độ tự nhiên bất đồng:** `data/phase_8_1/realism_disputed_user.md` (#1, 28, 100, 112, 113,
   125, 133, 137, 148; ghi giữ/loại). Tới lúc đó tính vào số chính.
5. **G0.6 khóa baseline** (sau 3 và 4): ghi commit, hash corpus/build record/split/gold/realism/sealed, mốc
   retrieval 2 treatment, 176 câu trả lời + điểm 7B Run 1; rồi A đóng G0.
6. Tiếp G4 → G2 → G3 → G5 theo spec; mỗi thí nghiệm theo skill `run-experiment` (tiêu chí ghi trước, dev chọn /
   test xác nhận, **số chính = bỏ câu không tự nhiên**, "chỉ tự nhiên" là số phụ). G2.2 đo tách nhóm "có/thiếu
   fact trong context" (C21).

## Câu hỏi cho User (phiên sau)

1. Quyền phiên (điều phối rộng, trần tiền ≤1 USD?, commit/push).
2. Câu kín: sửa 3 dòng capability_only (2, 21, 33) hay giữ; duyệt mẫu 15 dòng.
3. 9 câu độ tự nhiên bất đồng: giữ/loại.
4. Kho tự mâu thuẫn (B14): `travel/places/Đèo Hải Vân.md:84` (miễn phí từ 01/08/2024) vs phí 70.000 ở
   `travel/tickets/Vé tham quan Hải Vân Quan.md` — A đề xuất ghi lại, sửa ở 8.2 khi dựng lại index (có thể nhờ
   ChatGPT tra); User biết thông tin đúng thì báo.
5. Tên dự án khác (MekongAI) còn trong 15 file đã commit + lịch sử git của repo public (tài liệu cách làm việc User
   cho học) — A đề xuất để nguyên; gỡ khỏi lịch sử là thao tác phá hủy, chỉ khi User yêu cầu.
6. H8 (trả lời phần có căn cứ): 8.1 chỉ thử ở G2.2; **G1 làm yếu lập luận H8** — quyết ở 8.2 trên số đo. Trước
   quyết định 8.2 dựa vào điểm câu trả lời: nhắc chấm tay 20 câu (D6).
7. Mẫu đoạn đúng: User đã nhận xét 3 câu (độ tự nhiên); các câu khác trong `data/phase_8_1/gold/user_review_sample.md`
   coi là đồng ý nếu User không nói thêm.

## Session

| Vai | Terminal (tối 24/10) | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-2c` (25/10) | Claude Opus 5.5 | trực tiếp | 25/10: cải tiến cách làm; 8.1 tiếp phiên sau | xem `STATUS_A.md` |
| B — thực thi | `hue-rag-b0` | Claude Opus 5.5 | trực tiếp | B17 (G4 + G2) | kết phiên 22:47 — chờ A duyệt `phase_8_1_g2_g4_plan.md` + quyết G4-B; B16 chưa commit (xem STATUS_B) |
| C — thực thi | `hue-rag-a3` | Claude Opus 5.5 | trực tiếp | câu kín: 3 dòng capability_only (2, 21, 33) chờ A/User; review G2/G4 khi B nhắn | kết phiên 22:48 — C9–C22 xong, 0 USD; xem `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C; Qdrant chỉ đọc trừ
  đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run` trong `.venv`; thư viện thừa
  giữ nguyên (chỉ gỡ khi xung đột); luôn thử + so baseline trước khi chọn (User 20:49).
- **Phiên tối 24/10 (hết hạn — hỏi lại):** A tự điều phối rộng; API ≤1 USD (dùng ~0,0013 USD: smoke B9).
- **Phiên 25/10 sáng (hết hạn cuối phiên):** chỉ bàn cách làm; A tự quyết chi tiết cách làm (User "làm những gì bạn cho
  là tốt nhất"); commit/push như thường trực; 0 USD API.
- **Spec 8.1 §8:** Qdrant tạo/ghi/xóa chỉ `hue_81_*`; paid chỉ `gpt-6-luna`, trần 0,5 USD cả 8.1; file private mới ở
  `knowledge-base-hue/evaluation/phase_8_1/` và `data/phase_8_1/`; M1/M2 tải HF cache, GPU fp32 (một model một lúc).
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra.

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024, khóa SHA câu | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_draft.jsonl` | đoạn đúng 55 câu (40 dev / 15 test), đã áp m1–m8 | `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (2 rater, kappa 0,765; 29 unnatural; 9 chờ User) | `6916a29a1dee` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_authoring.jsonl` | 36 câu kín (chưa khóa) — A/C không đọc | — |
| `data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl` | mốc native mới `1fbb5c17…` | — |
| `data/phase_8_1/g1/` | kết quả G1 từng câu | — |
| `data/phase_8_1/tools/` | `select_gold.py`, `validate_gold.py`, `user_sample.py` (bản sao từ /tmp) | — |
| `data/phase_8_1/external_lessons_private.md` | bài học dự án khác của User (không đưa lên repo) | — |

## Khâu còn dính (gom cho G3/G5 — skill "Ranh giới theo khâu pipeline")

`build_candidate` chưa nhận chunk từ harness (G3 cần — B/C đồng ý thêm tham số `chunks`); prepare/build tự đọc
settings + tự tạo client; top-10 `fused[:10]` là hằng; `run_retrieval_eval`/`context_keyword_coverage` gọi
`load_settings` bên trong; harness G1 lấy context = tiền tố top-10 (G3 nên lấy từ `packed.sources`, C21 m1);
harness ghi đè theo `--name` (C21 m3).

## Việc của B

B11–B15 đã commit (`b8dbe95`, `0131afb`, `8156395`); B12/B14 là điều tra/review. Chi tiết: `sessions/STATUS_B.md`.

### B17 — G4 + G2 theo kế hoạch B16 (CHỜ A DUYỆT ở phiên sau; không chạy gì kể cả GPU/paid trước đó)

- Kế hoạch có tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` (ước ≈ 0,14–0,23 USD).
- Cần A/User quyết: G4-B pool 100 lệch spec 8.1 §5 G4 ("chỉ xếp lại top-10"); chính sách validator cho G2.3.
- Chưa commit (B16): `backend/experiments/phase_8_1/g1_retrieval.py` (`--realism main`), report G1 §7, file kế hoạch.

## Việc của C

- C9–C22 xong (chi tiết `STATUS_C.md`). Phiên sau: review G1 §7 + plan G2/G4 (B16); review G2/G4 khi B chạy; câu
  kín theo bước 3 (luôn qua sub-agent mới, C không đọc nội dung).

## Việc của A

- Phiên sau: bước 1–6 mục "Phiên sau"; ghi phát hiện "22/22 từ chối nhầm thiếu fact trong context" vào bảng rà C11
  (dòng 6.4) khi viết G5.
- **Khi duyệt B16, trả lời rõ trong mục B17** (B nêu khi thử mở phiên 25/10): (1) ai sửa plan theo
  `de_xuat_cho_du_an.md` mục 1–5 — đề xuất: B sửa, C review, A duyệt **sau** C và ghi `sha256sum` bản duyệt (WORKFLOW
  §9.1); mục nào bắt buộc / tùy; (2) G4 có chạy trước khi khóa G0.6 không (G4 chỉ retrieval, không dùng câu kín);
  (3) G4-B pool 100 đổi phạm vi spec ⇒ **trình User duyệt**, không chỉ báo; (4) số chính G4/G2 tính lại khi User quyết
  9 nhãn tự nhiên; (5) lần tải M1/M2 đầu tiên chạy không `HF_HUB_OFFLINE`, sau đó bật lại; (6) dòng "đang giữ GPU" trong
  `STATUS_<X>.md` khi chạy GPU.
