# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 11:22 25/10/2026 (A, **phiên chiều 25/10 — quay lại Phase 8.1**; User trả lời quyền + G4, xem mục "Phiên
chiều 25/10" ngay dưới). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang
mở; việc xong ở `PROJECT_HISTORY.md` và `report_agent/<đợt>/`.

## Phiên 25/10 sáng — cải tiến cách làm (ĐÓNG, `report_agent/2026-10-25_cai_tien_cach_lam/TONG_HOP.md`)

Đợt `report_agent/2026-10-25_cai_tien_cach_lam/` (`KE_HOACH.md`, `de_xuat_cho_du_an.md`). Mới: skill `improve-workflow` +
sổ `session_prompt/SO_CAI_TIEN_CACH_LAM.md`; `run-experiment` nâng (sàn / mức tụt / chỉ số quyết, cỡ mẫu trước, nhiễu A/A,
kiểm người chấm); Session D (`WORKFLOW.md` §10); `AGENTS.md` (bản chính cho mọi agent) + `CLAUDE.md`; hook
`.githooks/pre-commit` (bật: `git config core.hooksPath .githooks`; kiểm khi mở phiên). **Khi tới G4/G2:** đọc
`de_xuat_cho_du_an.md` mục 1–8 trước khi A duyệt plan B16. Mục "Tạm gác" cũ đã hết hiệu lực (User gửi báo cáo 25/10).

## Phiên chiều 25/10 — quyết định của User (11:20)

- Quyền phiên: A tự điều phối B/C rộng; API ≤ 1 USD cả phiên (8.1 vẫn trần 0,5 USD); commit/push như thường trực.
- **12:27 User đi ngủ trưa:** "tiếp tục điều phối, cải thiện dự án, thực nghiệm, so sánh, phát triển" — A tự điều phối trong quyền trên; việc cần User (mẫu câu kín bản 5, khóa G0.6 nếu cần) gom lại báo khi User quay lại.
- **Duyệt G4-A và G4-B** (pool 100) — ghi vào spec 8.1 §5 G4 ("Sửa đổi User duyệt 25/10/2026").
- **GPU yếu: mỗi lượt chạy GPU chỉ 20–30 câu**; **trước khi chạy phải kiểm GPU thật đang dùng** (không để chạy nhầm CPU).
- B16 mục "STATUS_B.md chưa commit" là cũ: STATUS_B/C đã commit ở `6c168e6`.
- **11:33 — 9 câu độ tự nhiên bất đồng: User "ổn rồi" ⇒ giữ cả 9 (tính natural)** — bước 4 dưới xong về quyết định; cập
  nhật `golden_realism_final.jsonl` theo nhãn cuối trước G0.6 (tập số chính không đổi vì câu bất đồng đã tạm tính vào).
- **User đã đọc `sealed_user_sample.md`** và trích nguyên văn 2 câu kín (không dấu) cho A ⇒ A đã thấy 2 câu đó; A không
  đề xuất biến thể nhắm vào chúng. User hỏi vì sao câu kín có câu không dấu (trả lời: spec §4 G0.4 dặn soạn "văn nói, không
  dấu, gõ sai nhẹ"; G1.4 cho thấy không dấu làm tìm kiếm sập) — chờ User chọn giữ / đổi.
- C23 vòng 1 (11:31): B16 code + G1 §7 đạt; plan `43086f053db8` changes_requested (3 major, chỉ sửa chữ). A quyết M2 =
  **theo spec** (giữ MRR@10 trong decision rule G4).

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT (viết 11:05 25/10; bước 1–2 đã làm ở phiên chiều)

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

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-c6` (chiều 25/10) | Claude Opus 5.5 | trực tiếp | điều phối 8.1 | xem `STATUS_A.md` |
| B — thực thi | `hue-rag-3f` (chiều 25/10) | Claude Opus 5.5 | trực tiếp | B17 (sửa plan → G4 → G2) | 11:36 vòng sửa 1 xong — plan sha `a4adfc8eedd9`, chờ C review vòng 2 + A duyệt |
| C — thực thi | `hue-rag-a1` (chiều 25/10) | Claude Opus 5.5 | trực tiếp | C25 đáp án câu kín; review G4/G2 khi B nhắn | 12:13 C25 xong: 4 đáp án sửa (11 theo User, 18, 26, 36; lặp, ảnh hưởng thấp), kiểm độc lập ĐẠT, check exit 0, kín v5 md5 `6d413c8d98fa` (backup v4 `a095e08bd7ac`) — `phase_8_1_g0_4_sealed_review.md` §9; chờ User: 2/21/33, dòng 6 + dữ kiện phụ (3/19/24/29/33). C24 xong (§8) |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã
  duyệt: A tự duyệt, báo sau (User 25/10 — `sentencepiece` cho M2); Qdrant chỉ đọc trừ
  đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run` trong `.venv`; thư viện thừa
  giữ nguyên (chỉ gỡ khi xung đột); luôn thử + so baseline trước khi chọn (User 20:49).
- **Phiên tối 24/10 (hết hạn — hỏi lại):** A tự điều phối rộng; API ≤1 USD (dùng ~0,0013 USD: smoke B9).
- **Phiên chiều 25/10 (hết hạn cuối phiên):** A tự điều phối B/C rộng; API ≤ 1 USD cả phiên; GPU mỗi lượt 20–30 câu,
  kiểm GPU thật trước khi chạy.
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

### B17 — G4 + G2 theo kế hoạch B16 (giao 11:22 25/10; A trả lời 6 câu của B)

**Bước 1 — sửa kế hoạch (chỉ sửa file `phase_8_1_g2_g4_plan.md`; chưa chạy GPU / paid).** Bản trước duyệt: sha
`c29b547b7417` (bản nháp, chưa duyệt). Sửa:
- **G4-B được User duyệt** (spec §5 G4 đã ghi sửa đổi): bỏ chữ "chỉ khi A/User sửa spec". G4-B không bắt buộc chờ G4-A
  thắng: nếu G4-A chưa rõ, B tự chọn M1 hay M2 (hoặc cả hai, Holm trên 2) theo số phụ + latency, ghi lý do trước khi chạy.
- **Giới hạn GPU của User: mỗi lượt GPU 20–30 câu.** Ghi trước cách chọn tập câu (đề xuất: ≤ 30 câu dev số chính có đoạn
  đúng, chọn theo seed 20261024, cố định cho mọi nhánh G4 kể cả luna; pilot latency 10 câu lấy trong tập đó). Xác nhận
  trên test: 15 câu test có đoạn đúng. Ghi trước "cỡ mẫu nhỏ ⇒ kết quả có thể **chưa rõ**" (đề xuất mục 1).
- **Kiểm GPU trước mỗi lượt GPU** (User): `torch.cuda.is_available()`, model thật ở `cuda` (device của tham số model),
  `nvidia-smi` thấy tiến trình + VRAM; một câu thử có thời gian cỡ GPU. Không phải `cuda` thì **dừng**, không chạy tiếp
  trên CPU. Lượt CPU duy nhất là đo latency CPU 5 câu, ghi rõ là CPU. Dòng "đang giữ GPU" trong `STATUS_B.md`.
- Áp `report_agent/2026-10-25_cai_tien_cach_lam/de_xuat_cho_du_an.md` mục 1–5 (bắt buộc cả 5) và mục 8 (kiểm
  `is_refusal` trước G2.2). Mục 2: "lỗi citation không tăng" → mức tụt cho phép theo số câu, đã trừ nhiễu 7B Run 1↔2.
- **G2.3 chính sách validator (A chọn):** phát lại validator hiện tại + **một** chính sách thay thế: câu trả lời mà
  context chỉ có **một nguồn** (hoặc mọi câu thiếu `[n]` đều thuộc đúng một nguồn duy nhất được trích) thì gán nguồn đó
  thay vì báo lỗi. Chỉ đo, không đổi chatbot.
- G4 **được chạy trước khi khóa G0.6** (chỉ retrieval, không dùng câu kín); số chính tính lại khi User quyết 9 nhãn tự
  nhiên. M1/M2 đã có trong HF cache ⇒ giữ `HF_HUB_OFFLINE=1`; thiếu file mới bỏ biến đó cho lần tải đầu, ghi lại.
- Xong bước 1: ghi `sha256sum` (12) bản đã sửa vào report, nhắn **C** (review) và A.
- **B 11:29: bước 1 xong** — `phase_8_1_g2_g4_plan.md` sha `43086f053db8` (mục "Thay đổi so với bản nháp" đầu file);
  kèm sửa C23 m1/m2 ở report G1 §7. Chờ C review phần 2 + A duyệt.
- **B 11:36: vòng sửa 1 (C23 M1–M3, m3–m6; M2 theo spec như A quyết)** — plan sha `a4adfc8eedd9`. Chờ C review vòng 2 + A
  duyệt.
- **A 11:40: duyệt bản sha `a4adfc8eedd9`** (C23 vòng 2 ready, `phase_8_1_b16_review.md` §7). B16 + plan + review đã commit.
  B làm bước 2. Sửa plan sau mốc này là bản mới ⇒ nhắn C + A trước khi chạy phần đổi.

**Bước 2 — chạy (sau khi A ghi "duyệt bản sha …" ở đây, A commit B16).** Thứ tự plan §4: mốc byte → G4.0 → G4-A → G4-B
→ G2 (pilot 10 câu mỗi lượt có phí). Mỗi gate: report + C review.

- **Tiền:** chỉ `gpt-6-luna`, B17 ≤ 0,25 USD; lượt nào vượt ước 50% thì dừng, báo A. Ghi token + USD từ log.
- **Không làm:** đổi chatbot / settings runtime; ghi Qdrant ngoài `hue_81_*`; mở câu kín; commit.
- **Dừng khi:** GPU không dùng được; mốc byte retrieval không khớp; lỗi provider lặp lại; tiền vượt.
- Chưa commit (B16): `backend/experiments/phase_8_1/g1_retrieval.py` (`--realism main`), report G1 §7, file kế hoạch.

## Việc của C

- C9–C22 xong (chi tiết `STATUS_C.md`).
- **C23 (giao 11:22 25/10) — review B16 + plan B17 đã sửa** theo skill `risk-gated-agent-review`: diff
  `g1_retrieval.py` + report G1 §7; plan `phase_8_1_g2_g4_plan.md` bản B ghi sha (đối chiếu mục B17 bước 1, spec 8.1 §5
  G4 bản sửa đổi 25/10, `de_xuat_cho_du_an.md` mục 1–5, 8; cỡ mẫu 20–30 câu có ghi trước "có thể chưa rõ"; cách kiểm
  GPU có dừng thật khi không phải `cuda`). Đầu ra: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_b16_review.md`;
  nhắn A + B. Chỉ đọc, không chạy GPU / paid. Bắt đầu khi B nhắn plan đã sửa (trước đó có thể review phần G1 §7).
- C23 đóng 11:40 (plan duyệt `a4adfc8eedd9`, commit `b9789f4`). Tiếp: review từng gate G4/G2 khi B nhắn.
- **C24 (giao 11:40 25/10) — thêm dấu cho mọi câu kín** (User 11:40: "thêm dấu cho mọi câu"; thay chỉ dẫn "không dấu"
  của spec 8.1 §5 G0.4 bước 4). C **không đọc nội dung**; mọi việc qua sub-agent **mới**:
  1. C sao bản hiện tại (`cp`, không đọc) → `knowledge-base-hue/evaluation/phase_8_1/sealed_authoring_v3_backup.jsonl`, ghi md5.
  2. Sub-agent sửa (mới): thêm dấu tiếng Việt chuẩn cho mọi chỗ viết không dấu trong `question` (và field khác nếu cũng
     không dấu); **không** đổi ý, cách hỏi, văn nói, độ dài, số dòng, thứ tự, field; lỗi gõ cố ý ngoài dấu giữ nguyên.
     Trả về C chỉ số dòng đã đổi + số đếm, không chép câu.
  3. Sub-agent kiểm (mới, khác người sửa): so với bản backup — mọi câu đủ dấu, ý không đổi, không đổi gì ngoài dấu;
     `check --authoring` exit 0 (C đọc exit riêng, không qua pipe).
  4. Làm lại `sealed_user_sample.md` (bản 4, cùng 15 dòng) để User xem lại; `sealed_realism.jsonl` giữ nhãn.
  5. 3 dòng `capability_only` (2, 21, 33): **chờ User**; User trả lời trước bước 2 thì gộp vào cùng lượt sửa.
  - Đầu ra: thêm §8 vào `phase_8_1_g0_4_sealed_review.md` (chỉ số đếm, md5, không chép câu); nhắn A. 0 USD.
- **C25 (giao 12:05 25/10) — sửa / rà `reference_answer` câu kín** (User duyệt mẫu bản 4: câu hỏi ổn; một đáp án lặp
  chủ ngữ, thiếu tự nhiên). Nhận xét nguyên văn của User: `knowledge-base-hue/evaluation/phase_8_1/sealed_user_feedback_private.md`
  (**C không đọc**; chỉ sub-agent đọc). Như C24: C `cp` backup (`sealed_authoring_v4_backup.jsonl`, md5) → sub-agent mới
  sửa đúng dòng User nêu theo đề xuất của User **và** rà cả 36 `reference_answer` (sai / thiếu so với nguồn, mơ hồ, lặp,
  thiếu tự nhiên), chỉ sửa chỗ rõ lỗi, ghi mức ảnh hưởng tới chấm → sub-agent mới khác kiểm so với backup + `check
  --authoring` exit 0 → §9 trong `phase_8_1_g0_4_sealed_review.md` (số dòng, loại lỗi, md5; không chép câu) → nhắn A.
  Chỉ sửa `reference_answer` (câu hỏi giữ bản 4). 3 dòng 2/21/33 vẫn chờ User. 0 USD.
- A song song (12:05): sub-agent chỉ đọc rà `reference_answer` của Golden 176 cùng loại lỗi → `data/phase_8_1/golden_reference_audit.md`;
  **không sửa Golden** — A trình User danh sách rồi mới quyết.
- **12:20 User duyệt "sửa theo đề xuất"** (phương án 1 của A + 3 dòng kín 2/21/33): nguyên tắc — đáp án chỉ trả lời điều
  câu hỏi hỏi; chỉ thêm điều kiện khi thiếu nó thì sai / gây hiểu lầm; chi tiết phụ đúng nguồn giữ nguyên.
  - **Golden (A qua sub-agent; C review sau):** sửa `reference_answer` 10 câu 23, 41, 46, 92, 93, 141, 151, 157, 165, 174
    ở file authoring → `merge` → `smoke 3 24 42 44 55 82 114 141 155 163`; 5 câu "chưa chắc" (19, 88, 115, 124, 152) giữ.
    Backup: `knowledge-base-hue/meta/golden_backup_2026-10-25/` (official md5 `c30b56f22bd3`, smoke `fae56cd0515f`).
    Báo cáo: `data/phase_8_1/golden_reference_fix_2026-10-25.md`. 7B Run 1 không còn so trực tiếp trên 10 câu này.
    **Xong 12:3x** (A tự kiểm: đúng 10 dòng, chỉ `reference_answer`, `check` exit 0; official md5 `b40ca15ef5f8`, smoke
    `d80b58c50f38`). 46/157 còn lặp cụm "trung tâm thành phố" vì keyword chứa cụm đó — giữ. **C27: C review** →
    `phase_8_1_golden_fix_review.md`.
  - **C26 câu kín:** dòng 2, 21, 33 sửa theo đề xuất v3 (`sealed_review_notes_private_v3.md`); dòng 6 bỏ quy định ngoài
    điều câu hỏi hỏi; dòng 3/19/24/29/33 giữ chi tiết phụ. Quy trình như C24/C25 (backup v5, sub-agent sửa, sub-agent khác
    kiểm, `check --authoring`), cập nhật `sealed_realism.jsonl` (2/21/33 → natural nếu người kiểm đồng ý), rồi mẫu
    `sealed_user_sample.md` bản 5 (đánh dấu dòng đổi câu hỏi / đáp án) để User xem lần cuối → §10 report.

## Việc của A

- Phiên chiều 25/10: chờ C23 → duyệt plan kèm sha → commit B16; câu kín + 9 nhãn chờ User; ghi phát hiện "22/22 từ chối nhầm thiếu fact trong context" vào bảng rà C11
  (dòng 6.4) khi viết G5.
- **Khi duyệt B16, trả lời rõ trong mục B17** (B nêu khi thử mở phiên 25/10): (1) ai sửa plan theo
  `de_xuat_cho_du_an.md` mục 1–5 — đề xuất: B sửa, C review, A duyệt **sau** C và ghi `sha256sum` bản duyệt (WORKFLOW
  §9.1); mục nào bắt buộc / tùy; (2) G4 có chạy trước khi khóa G0.6 không (G4 chỉ retrieval, không dùng câu kín);
  (3) G4-B pool 100 đổi phạm vi spec ⇒ **trình User duyệt**, không chỉ báo; (4) số chính G4/G2 tính lại khi User quyết
  9 nhãn tự nhiên; (5) lần tải M1/M2 đầu tiên chạy không `HF_HUB_OFFLINE`, sau đó bật lại; (6) dòng "đang giữ GPU" trong
  `STATUS_<X>.md` khi chạy GPU.
