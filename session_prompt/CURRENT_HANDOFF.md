# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 15:45 25/10/2026 (A, **kết phiên chiều 25/10 — Phase 8.1 ĐÓNG 15:27**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9.
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
3. Kho tự mâu thuẫn (B14): `travel/places/Đèo Hải Vân.md:84` (miễn phí từ 01/08/2024) vs phí 70.000 ở
   `travel/tickets/Vé tham quan Hải Vân Quan.md` — sửa khi build lại index ở 8.2; User biết thông tin đúng thì báo.
4. Tên dự án khác còn trong 15 file đã commit + lịch sử git (repo public) — A đề xuất để nguyên; gỡ khỏi lịch sử là thao tác
   phá hủy, chỉ khi User yêu cầu.
5. 3 câu kín A đã thấy: giữ (ghi chú khi mở) hay thay bằng câu mới (sub-agent mới) trước khi mở — quyết ở 8.2.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-c6` (chiều 25/10) | Claude Opus 5.5 | trực tiếp | điều phối 8.1; đóng 8.1; vòng cải tiến 2 | kết phiên 15:45 — xem `STATUS_A.md` |
| B — thực thi | `hue-rag-3f` (chiều 25/10) | Claude Opus 5.5 | trực tiếp | B16–B21 xong | kết phiên 15:27 — 8.1 đóng; 0,1653 USD |
| C — thực thi | `hue-rag-a1` (chiều 25/10) | Claude Opus 5.5 | trực tiếp | C23–C31 xong | kết phiên 15:28 — 8.1 đóng; 0 USD |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã
  duyệt: A tự duyệt, báo sau (User 25/10); Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report;
  code luôn `uv run` trong `.venv`; thư viện thừa giữ nguyên; luôn thử + so baseline trước khi chọn (User 24/10 20:49).
- **Phiên chiều 25/10 (hết hạn — hỏi lại):** A tự điều phối B/C rộng; API ≤ 1 USD (dùng 0,1653); GPU mỗi lượt 20–30 câu, kiểm
  GPU thật trước khi chạy (giữ làm luật kỹ thuật khi chạy GPU).
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

- A: không (phiên sau mục 1–3 ở trên). B: không. C: không.
- Sổ cải tiến `session_prompt/SO_CAI_TIEN_CACH_LAM.md` vòng 2 (15:44): W11 (review plan theo "Căn cứ để review"), W12 (giữ mù
  câu kín), W13 (skill review: correction ở file review), I4 (bẫy kỹ thuật ra `Project_Status.md` §8) — `đang thử`.
