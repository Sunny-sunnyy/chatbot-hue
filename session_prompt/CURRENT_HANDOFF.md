# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 16:57 25/10/2026 (A — **8.2 TẠM DỪNG** (User 16:5x) để **rà code Phase 0–7** trước; quyền phiên ở mục "Quyền"). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9.
Chỉ giữ việc đang mở; chuyện phiên 25/10 ở `PROJECT_HISTORY.md` và `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`.
Bản handoff trước khi rút gọn: `git show 4b48e1e:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống lúc kết phiên:** `main` (commit cuối ghi trong `sessions/STATUS_A.md`); chatbot full-corpus chạy được, **hành vi
runtime không đổi suốt 8.1** (retrieval 176 câu giống byte `cefb2d1a…`, native `1fbb5c17…`, kiểm 15:17 25/10). Qdrant
`:6335` còn **1** collection `hue_full_corpus_7a2_e5_small_384` (8.459). GPU GTX 1650 4 GB; `.venv` có torch 2.13+cu130,
`sentencepiece` 0.2.2 (thêm 25/10). M1 `BAAI/bge-reranker-v2-m3` và M2 `AITeamVN/Vietnamese_Reranker` đã tải vào HF cache
(2,2 GB mỗi cái). Repo `chatbot-hue` **PUBLIC** (hook `.githooks/pre-commit`).

**Phase 8.1 ĐÓNG** (User 15:27 25/10). Kết luận: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_synthesis.md`;
bảng từng quyết định `phase_8_1_g5_decision_table_draft.md` (bảng chính thức); theo loại câu `phase_8_1_g5_by_category.md`.
- **Chỉ context 10 thắng** (Completeness dev +0,26 [+0,08; +0,48], test +0,27 [+0,02; +0,59]; lợi ở câu nhiều nguồn / so
  sánh). Giữ: chunker, cách trộn + pool 30, BM25 âm tiết, không rerank, prompt, reasoning mặc định, validator.
- Tín hiệu 8.2: pool rộng; rerank luna (MRR +0,17); H8 trả lời một phần (từ chối nhầm 13 → 1 nhưng 2 câu ngoài phạm vi bị
  trả lời); NFC; dọn chunker (H1, S1–S3 không khác) khi build lại; lỗi citation "thiếu `[n]`".
- **Câu không dấu: ngoài phạm vi** (User 15:15 — người dùng gõ có dấu; prompt nghiên cứu B21 không gửi).
- **Mốc người:** User 15:44 — chỉ **đọc câu hỏi / câu trả lời và nhận xét, không chấm điểm** ⇒ brainstorm 8.2 chọn cách dùng
  nhận xét làm kiểm chéo judge.
- **G0.6 khóa 15:22:** câu kín chính thức `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` (36 × 4 field);
  manifest `data/phase_8_1/baseline/g0_6_manifest.json` (`9ea480d0d083`, A tự kiểm 34/34 hash). Câu kín **mở ở mốc cuối
  8.2 do User quyết**; A đã thấy 3 câu (User trích) — ghi khi mở.
- Golden chính thức sửa `reference_answer` 10 câu (md5 `0f7dbf41b422`; backup `knowledge-base-hue/meta/golden_backup_2026-10-25/`)
  ⇒ 10 câu đó không so trực tiếp với 7B Run 1.
- Tiền 8.1: **0,1653 USD** (chỉ `gpt-6-luna`).

**Thứ tự việc phiên sau:**

1. Mở A/B/C bằng `START_SESSION.md`; A `ListAgents`; A **hỏi lại quyền phiên** (§9.8: điều phối rộng, trần tiền).
2. **Brainstorm Phase 8.2 với User** (skill `propose-options`, mỗi lần một câu) → **một** spec trong
   `docs/superpowers/specs/` → User duyệt một lần (sha). Đầu vào: `phase_8_1_g5_synthesis.md` §4 (đã bỏ mục câu không dấu):
   bước 0 = cách dùng nhận xét của User làm kiểm chéo judge + tách khâu dính (bảng G5 §4); rồi context 10, NFC, dọn
   chunker khi build lại (+ sửa mâu thuẫn Hải Vân), pool + luna, H8 có chặn câu ngoài phạm vi, lỗi citation, index 8B.
3. Chưa giao việc thực thi cho B/C trước khi spec 8.2 được duyệt (`WORKFLOW.md` §9.4); A được nhờ B/C **review bản nháp spec**
   (chỉ đọc) trước khi trình User. Kế hoạch thí nghiệm 8.2 theo luật mới
   `WORKFLOW.md` §9.1: mục "Căn cứ để review" + session khác review trước khi A duyệt sha.

## Câu hỏi cho User (phiên sau)

1. Quyền phiên (điều phối rộng, trần tiền ≤ 1 USD?).
2. Phạm vi 8.2 (brainstorm): mục nào làm, thứ tự; cách dùng nhận xét của User thay chấm tay.
3. ~~Kho tự mâu thuẫn Hải Vân (B14)~~ — **sửa 16:40 (C32):** không phải mâu thuẫn thời gian; file đèo :86–88 cũng có mốc thu
   phí mới. Rủi ro còn: chunk chứa :84 (miễn phí cũ) mà thiếu :86. Rà kho C32: **139 mục** (mâu thuẫn chắc 22, …) trong
   `data/ra_soat_kho_2026-10-25/danh_sach.md` — đầu vào đợt build lại index (không sửa ở 8.2).
4. Tên dự án khác còn trong 15 file đã commit + lịch sử git (repo public) — A đề xuất để nguyên; gỡ khỏi lịch sử là thao tác
   phá hủy, chỉ khi User yêu cầu.
5. 3 câu kín A đã thấy: giữ (ghi chú khi mở) hay thay bằng câu mới (sub-agent mới) trước khi mở — quyết ở 8.2.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-00` (tối 25/10) | Claude Opus 5.5 | trực tiếp | brainstorm 8.2 với User | mở phiên 15:50 |
| B — thực thi | `hue-rag-de` (tối 25/10) | Claude Opus 5.5 | trực tiếp | chờ việc (review nháp spec 8.2) | mở phiên 15:50; 0 USD |
| C — thực thi | `hue-rag-d6` (tối 25/10) | Claude Opus 5.5 | trực tiếp | chờ việc (review nháp spec 8.2) | mở phiên 15:50; 0 USD |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã
  duyệt: A tự duyệt, báo sau (User 25/10); Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report;
  code luôn `uv run` trong `.venv`; thư viện thừa giữ nguyên; luôn thử + so baseline trước khi chọn (User 24/10 20:49).
- **Phiên tối 25/10 (User 15:5x, hết hạn cuối phiên):** A tự điều phối B/C rộng như phiên trước; API ≤ 1 USD cả phiên.
  Luật kỹ thuật giữ từ phiên trước: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- File untracked `báo cáo nghiên cứu github.txt` (gốc repo): của User, dùng cho Phase 9 — **không đụng, không commit**.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra.

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024 | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_draft.jsonl` | đoạn đúng 55 câu (40 dev / 15 test) | `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (82 / 65 / 29) | `0b65d1c138d2` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín chính thức — **không đọc** tới mốc cuối 8.2 | md5 `ddc59587b502` |
| `data/phase_8_1/baseline/g0_6_manifest.json` | manifest khóa G0.6 (hash mọi file mốc) | `9ea480d0d083` |
| `data/phase_8_1/{g1,g2,g3,g4,g4k}/` | kết quả từng câu của các gate | — |
| `data/phase_8_1/tools/` | script dùng lại (`make_sealed_official.py`, `select_gold.py`, …) | — |
| `data/phase_8_1/external_lessons_private.md` | bài học dự án khác của User | — |

## Việc đang mở

### Rà code các Phase trước (User 16:5x 25/10: dừng 8.2, rà code trước khi đi tiếp)

User hỏi về **code** (file, folder, guide của các Phase), không phải dữ liệu kho (C32 là A hiểu nhầm — giữ làm hồ sơ).
Đợt `report_agent/2026-10-25_ra_soat_code/`. Chỉ đọc, 0 USD. Rà trên `main` sạch (`f4353e2`; code B1 cất ở nhánh `p82-b1`).

**Chung cho B25 và C34:**
- **Tiêu chí** (skill `practical-project-coding` + `Session_Prompt.md` §7): (1) code thừa / không còn được gọi / sót Foods-Phase cũ —
  **chứng minh bằng grep** import + lời gọi (cả gọi động, CLI, notebook, test); (2) dễ đọc, theo được data flow, phức tạp quá nhu cầu
  (abstraction, wrapper, cấu hình, fallback, validator phòng xa); (3) hằng ẩn, đọc settings sâu, khâu dính; (4) test: bảo vệ hành vi
  thật hay không, còn mock / stub, test thừa, test paid / ghi Qdrant nằm lẫn; (5) guide / notebook / docstring lệch code đang chạy;
  (6) hiệu năng (khởi động, độ trễ mỗi câu) — chỉ đo khi cần cho một finding, chạy thật không paid; (7) cơ hội phát triển / so sánh —
  ghi **giả thuyết**, cách thử (theo `run-experiment`), không kết luận.
- **Không lặp cái đã biết:** đối chiếu `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md` §4 (khâu dính)
  và `phase_8_1_decision_inventory.md` §6 (lệch tài liệu–code); trùng thì ghi "đã biết (nguồn)" kèm điều mới nếu có.
- **Được:** đọc mọi code / test / guide / notebook / `settings.yaml`; chạy test **không paid, không ghi Qdrant** (liệt kê file, không
  `--deselect` — `Project_Status.md` §8); script đo trong `/tmp`; ≤ 3 sub-agent mỗi session (brief đọc lại trước khi gửi; tự kiểm 2–3
  khẳng định chính của sub-agent bằng file thật). **Không:** sửa code / test / guide; gọi API trả phí; ghi Qdrant; mở câu kín; chép nội
  dung kho / Golden vào report.
- **Mỗi finding:** id (`B-xx` / `C-xx`), khâu, `file:dòng`, loại (1–7), mức (cao / vừa / thấp: tác động × rủi ro khi để nguyên), quan sát
  (bằng chứng: lệnh grep / test / số đo), *suy ra* tách riêng, đề xuất sửa (nhỏ nhất đủ), cách kiểm khi sửa (đường thật), rủi ro khi sửa.
  Đầu file: **top 10** theo mức; cuối: phần **không rà được** / chưa chắc.
- **Đầu ra:** `report_agent/2026-10-25_ra_soat_code/ra_soat_code_<B|C>.md` (tracked — repo public, không nội dung private). Xong nhắn A.
- **Kiểm chéo:** khi cả hai xong, B kiểm top 5 của C, C kiểm top 5 của B (chạy lại bằng chứng) ⇒ A gộp `TONG_HOP.md`, trình User chọn sửa gì.

- **B — B25: rà luồng dựng index + nền** · `backend/ingestion/`, `embedding/`, `vectorstore/`, `scoring/`, `core/` (gồm
  `settings_loader.py`), `scripts/`, `backend/config/settings.yaml`, `pyproject.toml` (dependency không dùng: chỉ ghi — User giữ thư viện
  thừa), `docker-compose.yml`; test của các phần đó; notebook `03`, `04`; guide `phase_0`–`phase_4`, phần index của
  `guides/full_corpus_rag.md`, `guides/README.md`.
- **C — C34: rà luồng trả lời + đánh giá** · `backend/retrieval/`, `reranking/`, `llm/`, `api/`, `evaluation/`, `frontend/`; test của các
  phần đó; notebook `06`; guide `phase_5`–`phase_9`, `llm_rag_reference_for_hue_rag.md`, phần trả lời của `full_corpus_rag.md`;
  `backend/experiments/phase_8_1/` chỉ hỏi "còn cần giữ / chạy lại được không".

### Phase 8.2 — TẠM DỪNG 16:5x (User)

- Đã xong: spec duyệt (`dabae90b2b60`); B0 file đọc cặp mù ready (User đọc khi tiện: `data/phase_8_2/b0/nhan_xet_user.md`); **B1 xong**
  (B, T1–T5 đạt, 0,0369 USD — report `phase_8_2_b1_implementation.md` sha `bb5fea83aeb6`, **chưa A review**); code B1 ở nhánh
  **`p82-b1`** (`f23d396`, đã push, chưa merge main). Plan E1 (C, sha `f86240418ca1`) chờ B review + A trả lời Q1–Q3 (§10 plan).
- Chạy lại: A review B1 → (B0 xong) → merge `p82-b1` → E1. Tiền 8.2 đã dùng: **0,0369 USD** / 0,5.


- **User chốt brainstorm 8.2 (15:5x–16:0x 25/10):** hai bước không build lại index; mốc người = đọc cặp mù; Bước 2 cả ba
  (E1 → E2 → E3 luna có luật bỏ sớm); A tự đưa vào chatbot khi qua luật + review (E1 chờ User); trần 0,5 USD.
- **Spec 8.2 APPROVED** — User 16:21 25/10 duyệt bản sha `dabae90b2b60`
  (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`); B22 review 3 vòng ready
  (`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_spec_review.md`). Đợt `report_agent/2026-10-25_phase_8_2_ap_dung/`.
  Tiền 8.2: trần 0,5 USD; đã dùng 0.
- **A — B0 chuẩn bị đọc cặp mù** (spec §3.3–3.4, §5 B0): xong 16:24 — 20 câu, kiểm mù đạt; report
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md`; file private `data/phase_8_2/b0/`. B24 review 2 vòng
  ready (`phase_8_2_b0_prep_review.md`); **đưa User 16:4x** — file ghi nhận xét `data/phase_8_2/b0/nhan_xet_user.md` (bản sao của
  `doc_cap_mu.md` sha `37b66efb3499`). Chờ User đọc ⇒ sub-agent mới tóm nhãn ⇒ A ghép khóa ⇒ luật dừng §3.4.
- **B — B24: review B0 prep (chỉ đọc, 0 USD)** · Theo mục 6 của report B0; đầu ra `phase_8_2_b0_prep_review.md` (không chép câu
  hỏi / câu trả lời). Làm sau khi gửi plan B23.
  **Trạng thái 16:29 (B):** xong — `changes_requested`: F1 major (câu 17: `[Nguồn n]` không được đánh số lại ⇒ lộ bên context 10), F2 / F3 minor.
  **Vòng 2 16:32 (B):** F1 đóng (`doc_cap_mu.md` `37b66efb3499`) ⇒ **ready_for_user_confirmation**.
- **B — B23: Bước 1 context 10 + NFC** (spec §5 B1, §3.2, §4) · Giao 16:2x. **Plan duyệt 16:27** (A, sha `1a5ac660bd5d`,
  review `phase_8_2_b1_plan_review.md`: NFC đầu `search`; T5 theo cách hiểu B; minor a / b) ⇒ B sửa code + chạy.
  - **Trước tiên** viết plan ngắn `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_plan.md`: đầu file mục "Căn cứ để review"
    (2–4 file); chỗ đặt NFC (một chỗ API + evaluator cùng đi qua) và lý do; file sửa; lệnh chạy; tiêu chí B1.2 chép đúng spec
    (158 câu byte `cefb2d1a…`; 176 / 176 `top_chunk_ids`, `context_sources`, `input_tokens` = G2.1a; judge chấm lại G2.1a cùng lượt
    mù; 0 OOS bị trả lời; live `/chat` + câu NFD); ước USD từ pilot 10 câu. Nhắn A — **A review + duyệt sha rồi mới sửa code**.
  - **Sau khi duyệt:** sửa `backend/config/settings.yaml` (`max_context_documents: 10`), `backend/core/settings_loader.py:77`,
    `backend/tests/test_phase6_settings.py:25`, chỗ NFC + test nhỏ; chạy theo plan. Dữ liệu chạy `data/phase_8_2/b1/`.
  - **Quyền:** paid `gpt-6-luna` ≤ 0,06 USD cho B1 (pilot 10 trước; vượt ước pilot > 50% ⇒ dừng báo A); judge Claude sub-agent;
    Qdrant chỉ đọc; không commit (A commit); không mở câu kín. Khai báo file trong `STATUS_B.md`.
  - **Dừng:** một tiêu chí B1.2 lệch ⇒ dừng, tìm nguyên nhân, báo A (không sửa tiêu chí).
  - **Đầu ra:** `phase_8_2_b1_implementation.md` (khuôn implementation), trạng thái "chờ review", nhắn A. Người kiểm: A (C đang C32).
  - **Trạng thái 16:27 (B):** plan `phase_8_2_b1_plan.md` (sha `1a5ac660bd5d`) gửi A — chờ A duyệt sha; chưa sửa code.
  - **Trạng thái 16:46 (B):** xong — T1–T5 đạt; **chờ review** (A). Report `phase_8_2_b1_implementation.md`. Paid 0,0369 USD (+ live ≈ 0,0004 ước). Chưa commit; B1.3: commit chờ B0.
- **C32 xong + A review ready 16:40** (`report_agent/2026-10-25_ra_soat_noi_dung_kho/ra_soat_kho_review.md`); chờ User xem. C: chờ việc.
  Chi tiết việc C32: `git show f4353e2:session_prompt/CURRENT_HANDOFF.md`.
- **C — C33: viết plan E1 "trả lời một phần, vẫn từ chối câu ngoài phạm vi"** (spec 8.2 §5 B2, §3.5) · Giao 16:4x. **Chỉ viết
  plan**, không sửa code, không chạy, 0 USD.
  - **Trạng thái (C, 16:49 25/10): plan xong, chờ B review rồi A duyệt sha.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_e1_plan.md` sha `f86240418ca1`; 0 USD. 3 câu cho A ở §10 (test không đủ câu cho CI; 1 hay 2 biến thể; số A/A lấy từ B1 chờ review).
  - **Đọc:** spec 8.2 (full); `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md` §4.2 (P1: từ chối nhầm 13 → 1,
    2 câu OOS bị trả lời) + `phase_8_1_g2_review.md` (targeted P1); `backend/experiments/phase_8_1/g2_generate.py:55-80` (prompt P1);
    hợp đồng `docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md` §10; skill `run-experiment`.
    Được đọc kết quả từng câu P1 trong `data/phase_8_1/g2/` (vì sao 2 câu OOS bị trả lời) — **không** mở câu kín, **không** đọc
    `data/phase_8_2/b0/` (khóa mốc người).
  - **Plan gồm:** mục "Căn cứ để review"; lớp bài toán; 1–2 biến thể prompt (một thay đổi mỗi biến thể) và giả định, kiểm giả định
    bằng máy trên dữ liệu P1; khuôn YAML (`run-experiment` §1): sàn 0 OOS bị trả lời (dev + test), chỉ số quyết = số câu trong phạm vi
    bị từ chối nhầm, mức tụt Completeness / Accuracy / lỗi citation **bằng số câu**; nhiễu = A/A context 10 của B1 (ghi "chờ số B1");
    cỡ mẫu trước khi chạy; mốc = chatbot sau B1; ước USD (pilot 10); cách chấm judge cùng lượt mù; ~10 câu đổi từ chối → trả lời một
    phần để User đọc khi E1 thắng (spec §5 B2).
  - **Đầu ra:** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_e1_plan.md`, nhắn A sha. Review: B (sau B1), theo §9.1.
- Sổ cải tiến `session_prompt/SO_CAI_TIEN_CACH_LAM.md` vòng 2 (15:44): W11 (review plan theo "Căn cứ để review"), W12 (giữ mù
  câu kín), W13 (skill review: correction ở file review), I4 (bẫy kỹ thuật ra `Project_Status.md` §8) — `đang thử`.
