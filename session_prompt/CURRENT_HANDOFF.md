# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 15:54 25/10/2026 (A, **mở phiên tối 25/10** — quyền phiên ghi ở mục "Quyền"; đang brainstorm 8.2). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9.
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
- **C32 xong + A review ready 16:40** (`report_agent/2026-10-25_ra_soat_noi_dung_kho/ra_soat_kho_review.md`); chờ User xem. C: chờ việc.
- **C — C32: rà nội dung kho (chỉ đọc, 0 USD)** · User duyệt 16:1x 25/10. Đợt `report_agent/2026-10-25_ra_soat_noi_dung_kho/`.
  - **Trạng thái (C, 16:38 25/10): chờ review A.** 205/205 file; 139 mục; tự kiểm 42/42; report
    `ra_soat_kho_implementation.md`; 2 phát hiện cho A ở §4 (mẫu Hải Vân không phải mâu thuẫn thời gian; file inventory
    `performing_arts` tự ghi phải loại khỏi ingestion nhưng đang trong index).
  - **Mục tiêu:** danh sách chỗ kho **tự mâu thuẫn** (cùng thực thể, khác giá / giờ / năm / địa chỉ / số liệu giữa hai file hoặc
    trong một file — mẫu: vé Hải Vân, `CURRENT_HANDOFF` "Câu hỏi" mục 3) và **thông tin có thể đã cũ** (giá / giờ gắn năm cũ, "hiện
    nay", "sắp", lịch lễ hội theo năm cụ thể). Để User xem; sửa ở đợt build lại index.
  - **Đọc:** `knowledge-base-hue/{foods,heritages,festivals,performing_arts,travel}/` (205 file runtime; danh sách theo discovery
    `settings.yaml` `full_corpus.knowledge_base`). **Loại** `knowledge-base-hue/evaluation/`, `meta/`, mọi `*sealed*` (không
    grep vào đó). Template `meta/*-template.md` chỉ mở nếu cần hiểu quy ước.
  - **Làm:** C tự chọn cách (gợi ý: script `uv run python` gom câu có số / năm / giá theo thực thể → sub-agent rà theo nhóm; ≤ 8
    sub-agent, brief đọc lại trước khi gửi, mỗi sub-agent ghi file private). Mỗi mục: `file:dòng` hai phía, loại (mâu thuẫn / có thể
    cũ / khác), mức chắc (chắc / có thể), tách quan sát ↔ suy ra, đề xuất (User biết thì báo / tra ngoài qua ChatGPT / sửa khi build).
    C tự kiểm lại bằng file thật ≥ 10 mục chọn ngẫu nhiên (seed ghi) + mọi mục "chắc".
  - **Không làm:** không sửa kho, không tra web, không mở câu kín / Golden, không đổi chatbot, không gọi API trả phí.
  - **Đầu ra:** danh sách đầy đủ **private** `data/ra_soat_kho_2026-10-25/danh_sach.md` (+ script ở `data/ra_soat_kho_2026-10-25/tools/`);
    report tracked `report_agent/2026-10-25_ra_soat_noi_dung_kho/ra_soat_kho_implementation.md` (khuôn implementation) chỉ ghi
    cách làm, số file đã rà theo domain, số mục theo loại / mức chắc — **không chép nội dung kho** (repo public).
  - **Tiêu chí:** phủ đủ 205 file (bảng số file theo domain khớp discovery); mọi mục có `file:dòng` kiểm được; ghi rõ phần không
    rà được. **Review:** A. **Dừng** khi cần web hoặc thấy lỗi dữ liệu nghiêm trọng (báo A). Khai báo file trong `STATUS_C.md`.
- Sổ cải tiến `session_prompt/SO_CAI_TIEN_CACH_LAM.md` vòng 2 (15:44): W11 (review plan theo "Căn cứ để review"), W12 (giữ mù
  câu kín), W13 (skill review: correction ở file review), I4 (bẫy kỹ thuật ra `Project_Status.md` §8) — `đang thử`.
