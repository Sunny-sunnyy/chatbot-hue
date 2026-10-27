# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 13:50 27/10/2026 (A, **mở phiên 27/10 chiều**: quyền cấp lại như 27/10; B0 chưa; giao B71 / C62 — mục "Việc đang mở"). Trước: 13:30 27/10 (kết phiên sáng).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Chi tiết phiên 27/10: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md` (§2 quyết định
theo giờ, §3 kết quả, §7 việc sau khi đóng đợt); nhật ký User `bao_cao_he_thong/nhat_ky/2026-10-27_chot_dot_cai_tien.md`. Bản handoff trước khi viết lại:
`git show a819789:session_prompt/CURRENT_HANDOFF.md` (có bảng chi tiết từng thí nghiệm K1–K3b, R1–R4).

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống (`main`, commit cuối `git log -1 main`):**
- Chatbot: context **5**, chưa NFC, reasoning `medium` mặc định (không gửi tham số), không rerank. **Mới từ 27/10 (merge `5100b90`):** `/api/chat` ghi **một
  dòng `chat_metrics`** mỗi lần gọi (token vào / ra / suy luận, số nguồn, ms từng khâu; không ghi câu hỏi / câu trả lời / nguồn) vào logger `chat`
  (`backend/logs/application.log`, gitignore). Cổng ổn định trên `main` 13:25 27/10: `/` 200, `/health` 5 / 5, câu trong kho 200 + 2 nguồn, câu ngoài kho từ chối,
  1 dòng log / câu, grep câu hỏi trong log = 0, total_ms khớp client (1.903,6 / 1.912,6 ms).
- **Thước đo từ 27/10 (merge `a819789`):** nhãn đoạn đúng **`data/phase_8_1/gold/gold_v2.jsonl`** (`2f5a347a71ff`; = v1 + 3 khoảng câu 120, 156) + luật trúng dòng
  tiêu đề trong `heading_path` (câu 143), `backend/experiments/phase_8_1/g1_retrieval.py`. `gold_draft.jsonl` (v1, `bab707b9ab22`) **giữ nguyên** — manifest G0.6 khóa.
  Mọi số `*_gold_*` trước 27/10 là v1 (B1 dev: v1 22 / v2 24). **Không chạy `data/phase_8_1/tools/validate_gold.py`** (ghi đè `gold_draft`).
- Qdrant `:6335` **1** collection `hue_full_corpus_7a2_e5_small_384` (8.459). Repo `chatbot-hue` **PUBLIC**. Untracked ở gốc **của User, không đụng**:
  `báo cáo nghiên cứu github.txt`, `tham khảo 26_10/`. Hook pre-commit quét trùng Golden / kho / câu kín (`.githooks/overlap_scan.py`).
- Cổng: 27/10 cổng 8011 và 8015 bị tiến trình **của dự án khác** chiếm (có thể đổi) ⇒ trước khi chạy server: `ss -ltnp | grep ':80'`, chọn cổng trống (8013, 8014,
  8019 đã dùng được). Cổng bị chiếm ⇒ uvicorn khởi động xong rồi dừng, exit 3, log không ghi lỗi bind.

**Phase 8.2** (spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`, bản A duyệt `cd910c4c4169`):
- **Bước 2 (đợt cải tiến từng khâu) ĐÓNG 27/10** — User chọn (1) "chốt đợt": K1, K3, K3b-n, R1, R2 kém hơn; **K3b-m** (luna chọn 10 / 30 đoạn) tầng tìm tốt hơn
  (tạm) — đoạn đúng trong context 22 → 31 / 40 (v1), 9 thắng / 0 thua ổn định 2 lượt — nhưng khâu trả lời **kém hơn theo luật** T3 (5 câu Completeness tụt > 4;
  chỉ báo: Completeness +0,216, Accuracy +0,250, từ chối nhầm 7 → 2 / 88), chọn đoạn thêm ≈ 4,6–5 s p50, ≈ 3,8× USD ⇒ **gác làm hồ sơ**. R3, K2, E2 NOT RUN.
- **B0** (User đọc cặp mù, `data/phase_8_2/b0/nhan_xet_user.md`, 20 câu, ~30–45 phút): **chưa làm** — việc duy nhất chặn merge B1.
- **B1** (context 10 + NFC): `p82-b1` vẫn là `811d25d` (gốc `43cdcd6`). B63 27/10 **chỉ thử** rebase lên `main` `e952fa3` trên nhánh tạm (đã xóa, không push): không xung
  đột, 68 passed / 1 failed (thiếu key), T1 giống byte. Latency thật
  qua API (B65): context 10 **không chậm hơn** context 5. Sau B0: rebase lên `main` mới (gồm log + gold v2) ⇒ cổng ổn định ⇒ merge ⇒ 4 chỗ báo cáo.
- Tiền 8.2: **≈ 0,212 / 0,5 USD** (cận trên ≈ 0,218). Phiên 27/10 cả nhóm ≈ **0,197 USD** (log 0,172 + ước 0,025: K3b-n mất usage ≈ 0,0087, B65 ≈ 0,0155, cổng A ≈ 0,0005).

**Hiện trạng đo được 27/10 (để quyết yêu cầu phi chức năng):** latency đầu–cuối qua API (22 câu tự viết, B65): context 5 p50 **3,3 s** / p95 **5,7 s**
tuần tự, 3,6 / 6,2 s đồng thời 4 — **đã vượt mức theo dõi 5 s**. C58: gọi model ≈ 98 % (đã chứng minh phần dư không ở HTTP / tìm / ngữ cảnh / citation);
thời gian sinh ≈ 1,2 s + 11,5 ms / token ra (giải thích được, chưa can thiệp). C48: B1 dev 0 / 68 câu có số bị sai.

**Mục tiêu sản phẩm (User 27/10):** đồ án tốt nghiệp, xem như sản phẩm kinh doanh thật; người dùng = User, du khách, người dân. Yêu cầu phi chức năng chưa có
số ⇒ "so sánh, đánh giá, chỗ nào tối ưu được thì tối ưu". Thứ tự lỗi A đề xuất (chưa chốt): nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.
Ba nguyên tắc User (`Session_Prompt.md` §7): chất lượng cần thiết trước; hiệu suất = tiền + tốc độ; đo theo mục tiêu sản phẩm cuối cùng.

**Mã hay gặp:** B0 / B1 = bước spec 8.2; K1–K3b (khâu tìm), R1–R4 (khâu trả lời) = biến thể spec §10.3; T1 = kết quả tìm 158 câu (mốc `cefb2d1ad609`); T3 = mức
tụt "số câu Completeness tụt ≤ A/A + 3"; A/A = hai lượt cùng cấu hình; S / W = sự cố / đề xuất `SO_CAI_TIEN_CACH_LAM.md`; Bxx / Cxx = việc A giao (phiên 27/10:
B53–B70, C46–C61 — STATUS_B / STATUS_C dùng đúng mã này).

**Thứ tự việc phiên sau:**
1. Mở A / B / C bằng `START_SESSION.md`; A `ListAgents`, cập nhật bảng Session; kiểm `main` sạch (trừ 2 mục untracked của User), Qdrant 1 × 8.459.
2. **A hỏi lại quyền phiên** (quyền 27/10 hết hạn): điều phối + tự thử / chọn trong luật? trần ≤ 1 USD? (User có thể nói "quyền như phiên 27/10").
3. **B0** khi User làm (file đọc `data/phase_8_2/b0/doc_cap_mu.md`, User ghi `nhan_xet_user.md`) ⇒ A mở `khoa.json` (chỉ A), tóm nhãn + áp **luật dừng spec 8.2
   §3 mục 4 (dòng 44–)** ⇒ không dừng: B rebase `p82-b1` lên `main` mới (gồm log + gold v2) + cổng ổn định + push nhánh (**cần quyền**) ⇒ C review ⇒ A merge ⇒
   chatbot context 10 + NFC ⇒ 4 chỗ báo cáo.
4. Mốc cuối 8.2: câu kín (36 câu; User quyết lúc mở; A **không** đọc nội dung — giao một session / sub-agent riêng chạy + chấm, báo số đếm, theo `Session_Prompt.md`
   §5 "giữ mù") ⇒ đóng 8.2 ⇒ **tính năng mới** (User 27/10: "xong sớm thì mới bổ sung được tính năng mới") — brainstorm với User
   theo `propose-options`, một tài liệu thiết kế (WORKFLOW §9.1). Ứng viên A ghi nhận (chưa bàn): streaming từng câu đã kiểm (nghiên cứu 26/10 C5), hội thoại
   nhiều lượt, Phase 9 (agentic / recommender — `báo cáo nghiên cứu github.txt` của User), deploy.
5. Trong lúc chờ User: B / C chỉ làm việc 0 USD không đổi chatbot, **do A giao** (giao việc là vai thường trực của A, WORKFLOW §1; quyền hết hạn là quyền
   *tự quyết thử nghiệm / tiền / push*). Mục việc cụ thể: dưới "Mục việc phiên sau".

## Câu hỏi cho User (phiên sau — gói trong báo cáo mở phiên, mỗi câu có khuyến nghị)

1. **Quyền phiên** (bước 2 trên). A khuyên: như 27/10 (điều phối + tự thử trong luật; ≤ 1 USD; B / C commit + push nhánh riêng khi việc ghi rõ — gồm **B rebase
   + force-push `p82-b1`** sau B0, vì rebase đổi lịch sử nhánh).
2. **B0** — khi tiện (chỉ User làm được); sau đó chatbot lên context 10.
3. **Nghiên cứu ChatGPT** `gửi chatgpt/2026-10-27/tìm thông tin/muc_tieu_san_pham_2026_10_27.md` (C47 đã đối chiếu code, A sửa) — chưa gửi; kết quả lưu
   `gửi chatgpt/2026-10-27/kết quả nghiên cứu/`. Cần để chốt yêu cầu phi chức năng (chờ tối đa, tiền / câu) và thứ tự lỗi.
4. **Ngày bảo vệ đồ án** — để xếp lúc dừng cải tiến / chuyển tính năng mới / chuẩn bị demo + báo cáo đánh giá.
5. **Thứ tự lỗi nặng → nhẹ** A đề xuất (trên) — đồng ý? Đồng ý ⇒ A đưa "nói chắc sai" thành sàn cho các lần đo sau (không áp ngược).
6. **Hướng K3b-m** (hồ sơ): mở lại chỉ khi User muốn đặt **luật nhận riêng cho biến thể đổi context** (áp cho lần sau) và / hoặc thử bản nhanh **K3c** (`none` +
   chịu chữ thừa sau JSON) — A khuyên để sau B0 + kết quả nghiên cứu thời gian chờ.
7. **Xóa nhánh đã merge** `c59-log`, `gold-v2` (auto mode chặn A): `! git push origin --delete c59-log gold-v2 && git branch -d c59-log gold-v2`.
8. (Không bắt buộc) Usage OpenAI `gpt-6-luna` 27/10 khoảng 09:30–09:31 và 11:38–11:44 — thay 2 số ước (0,0087; 0,0155 USD) bằng số thật.
9. Giữ từ trước (không gấp): mâu thuẫn kho Hải Vân Quan (sửa khi build lại index); `performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng
   đang trong index (C32); rà kho C32 139 mục (gửi ChatGPT tra nguồn = đưa dữ liệu ra ngoài — hỏi khi tới); 3 câu test C56 (95, 130, 138) chưa quyết nhãn; tên dự
   án khác trong lịch sử git — để nguyên; 3 câu kín A đã thấy (spec 8.2 §3.7).

## Câu hỏi A còn nợ (phiên sau A trả lời / xử lý, không cần User)

- Log `FileHandler` không xoay vòng (~400 byte / câu) — xem lại khi deploy.
- Sổ cải tiến: theo dõi W24–W26 (`đang thử` từ 27/10); `CURRENT_HANDOFF` nên ≤ ~150 dòng.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-51` (27/10 chiều) | Claude Opus 5.5 | trực tiếp | điều phối B71 / C62; review C62; brainstorm tính năng mới với User (chỉ bàn); kế hoạch mốc cuối 8.2 | `STATUS_A.md` |
| B — thực thi | `hue-rag-2d` (27/10 chiều) | Claude Opus 5.5 | trực tiếp | B71 xong (C ready); B72 plan B3 duyệt `27e75be5ed44`; C64 review ready; **B73 xong** (`data/sua_kho_2026-10-27/README.md`) — rảnh, chờ việc | `STATUS_B.md` |
| C — thực thi | `hue-rag-86` (27/10 chiều) | Claude Opus 5.5 | trực tiếp | **C62** sửa guide / report cũ (dưới) ⇒ review B71 | `STATUS_C.md` |

Phiên trước (27/10 sáng, kết 13:30): A `hue-rag-5f`, B `hue-rag-31`, C `hue-rag-5b` — B53–B70 / C46–C61 xong; tiền ≈ 0,197 USD.

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt:
  A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run` trong `.venv`; luôn thử + so baseline
  trước khi chọn (User 24/10 20:49); commit trước sửa code + cổng ổn định sau mỗi gói (User 26/10); "báo trước, chờ User đồng ý" chỉ áp ngoài phạm vi đã duyệt.
- **Phiên 27/10 chiều (User 13:46 27/10: "cấp lại như phiên 27/10") — hết hạn cuối phiên:** A tự điều phối B/C + tự thử / chọn trong luật; API ≤ 1 USD cả phiên;
  B / C commit + push nhánh riêng theo việc — B71: B commit + **force-push `p82-b1`** (`--force-with-lease`). User chọn PA3 (13:4x): chuẩn bị B1 + dọn nợ + A **bàn**
  tính năng mới với User trước khi đóng 8.2 (chỉ bàn, không viết spec / giao làm — lệch `WORKFLOW.md` §9.4 do User duyệt). B0: User chưa rảnh.
- Phiên 27/10 sáng (hết hạn): API dùng ≈ 0,197 USD; B push `p82-k3`, `p82-k3b`, `gold-v2`; C push `p82-r1`, `c59-log`.
- Trần 8.2: 0,5 USD (spec D5). Luật kỹ thuật giữ: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra (~0,000133 USD / câu context 5; ~0,000204 context 10; luna chọn 10 / 30 đoạn ~0,0006 / lần).

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024 | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v2.jsonl` (+ `gold_v2_CHANGES.md`) | **nhãn đoạn đúng dùng từ 27/10** (55 câu; v1 + 3 khoảng) | `2f5a347a71ff` |
| `data/phase_8_1/gold/gold_draft.jsonl` | nhãn v1 — G0.6 khóa, không sửa / không chạy `validate_gold.py` | `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (82 / 65 / 29) | `0b65d1c138d2` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — **không đọc** tới mốc cuối 8.2 | md5 `ddc59587b502` |
| `data/phase_8_1/baseline/g0_6_manifest.json` | manifest khóa G0.6 | `9ea480d0d083` |
| `data/phase_8_2/b0/` | đọc cặp mù: `doc_cap_mu.md`, `nhan_xet_user.md` (User ghi — **chưa ghi**), **`khoa.json` chỉ A** (`5b9240842b7b`), `mau.json` (mẫu 20 câu), `tools/` | — |
| `data/phase_8_2/{b1,k1,k3,k3b,r1,r2,r4}/` | kết quả từng thí nghiệm (harness từ chối ghi đè); `k3b/gold_scan/` B61; `k3b/answer/` K3b-m answer | — |
| `data/phase_8_2/latency_2710/` | B65: 22 câu tự viết (`questions.jsonl` `bac5c91db005`), kết quả, `c58/` (C58 + diff đo tạm) | — |
| `data/phase_8_2/gold_fix_proposal_2710/` | đề xuất nhãn C56 (đã áp thành gold v2) | — |
| `data/phase_8_1/tools/{build_gold_v2,recount_gold_v2}.py` | dựng + kiểm gold v2 (chỉ đọc), đếm lại `*_gold_*` | — |
| `data/cai_tien_tung_khau_2026-10-26/` | B42, C36, C48 (`c48/`), C51 (`c51/`), script `tools/` | — |
| `gửi chatgpt/2026-10-27/tìm thông tin/muc_tieu_san_pham_2026_10_27.md` | yêu cầu nghiên cứu mục tiêu sản phẩm (chưa gửi) | — |
| `gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md` | kết quả ChatGPT đợt cải tiến (C5 streaming) | `601b49a025ac` |
| `data/ra_soat_kho_2026-10-25/`, `data/ra_soat_code_2026-10-25/`, `data/reports_artifacts_private_2026-10-26/` | rà kho C32 (139 mục), rà / sửa code, 8 artifacts gỡ | — |
| `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json}` | điều kiện chunker (runtime đọc) + mẫu test chunker | conditions `b84a0a637bfc` |

## Việc đang mở

### Luật chung khi sửa code (mẫu cổng ổn định — dùng cho merge B1)

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file,
  không `--env-file` trừ khi mục ghi; report `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha
  (§9.1, sha tính từ file). Dừng khi: đường thật đổi ngoài dự kiến; phải đụng file người kia đang khai báo; vượt tiền.
- **Cổng ổn định sau mỗi gói:** (1) test các file chạm (lỗi thiếu key ghi rõ); (2) chạy thật `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn
  api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho (200, `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết, body `{"query": …}`;
  **đếm dòng `chat_metrics` mới = số câu**, grep câu hỏi trong log = 0; đo thời gian client bằng Python `perf_counter` (không dựa `curl -w time_total`); tắt
  server (TaskStop); (3) chạm tìm kiếm / chia đoạn: T1 giống byte; (4) 4 chỗ báo cáo nếu hành vi đổi; (5) hook quét trùng tự chạy; A commit + push.
- Test cần key OpenAI (không chạy mặc định): `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan` (+ các test `require_openai_key`),
  `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. Test thiếu model
  `tests/test_startup_model_missing.py`: User `!`.

### B71 — rebase B1 lên `main` trước B0 (giao 13:50 27/10; mức trung bình; khớp spec 8.2 §5: merge vẫn **sau** B0)

- **Mục tiêu:** `p82-b1` (context 10 + NFC) nằm trên `main` `473f61e` (gồm log `chat_metrics` + gold v2), đã kiểm, để sau B0 A chỉ còn tóm nhãn + merge.
- **Đọc:** full-read `phase_8_2_b1_implementation.md` (trên `p82-b1`) + `phase_8_2_b1_rebase_review.md`; targeted spec 8.2 §4 (phạm vi B1); mục "Luật chung khi sửa code" ở trên.
- **Làm:** worktree riêng `/tmp/b71_b1` (C sửa tài liệu trên `main` trong working tree chung — bẫy worktree `Project_Status.md` §8); rebase; pytest các file chạm
  (không key); **T1 giống byte** `cefb2d1ad609`; **cổng ổn định context 10** (2 câu tự viết; đếm `chat_metrics` = 2; xem log có ghi số nguồn ≤ 10); report
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_rebase2_implementation.md` commit trên nhánh; `git push --force-with-lease origin p82-b1` (từ working
  tree chung nếu worktree bị chặn). Gỡ worktree khi xong.
- **Không làm:** merge `main`; đổi hành vi ngoài B1; chạy thí nghiệm; mở `khoa.json` / câu kín.
- **Tiền:** ≤ 0,005 USD (cổng 2 câu ≈ 0,0005). **Dừng + báo A:** xung đột ngoài file B1; T1 khác byte; test hỏng ngoài nhóm cần key; latency / log lạ.
- **Xong:** nhắn A + C (C review theo `risk-gated-agent-review`).

### C62 — sửa guide / report cũ cho khớp hiện trạng 27/10 (giao 13:50 27/10; mức thấp–trung bình; 0 USD)

- **Làm** (trong working tree chung, nhánh `main`; **không commit** — A review diff rồi commit; khai báo file trong `STATUS_C.md` trước):
  1. `guides/phase_8_benchmark_model_selection.md` mục "Hiện hành": còn ghi "8.2 — tạm dừng" ⇒ cập nhật theo `Project_Status.md` §2 (8.2 chạy lại 26/10, đợt cải
     tiến đóng 27/10, B0 chờ, B1 trên nhánh, chatbot context 5).
  2. `guides/phase_6_generation_api.md` (+ `guides/full_corpus_rag.md` nếu có mục API / log): thêm dòng log `chat_metrics` (merge `5100b90`) — mỗi khẳng định kèm
     `file:dòng` code đã đối chiếu.
  3. `guides/full_corpus_rag.md:179` mã "B-06" (trùng nghĩa với mã việc khác) ⇒ ghi rõ nghĩa bằng lời.
  4. `report_agent/2026-10-26_cai_tien_tung_khau/gold_v2_{implementation,review}.md`: `/tmp/b75_recount.py` ⇒ `data/phase_8_1/tools/recount_gold_v2.py`; `python3` ⇒
     `uv run python` (C61 m-2 / m-3) — ghi "(sửa 27/10, C62)".
  5. `data/phase_8_1/tools/validate_gold.py` (private): cảnh báo đầu file + dừng nếu `gold_draft.jsonl` đã có (không ghi đè file G0.6 khóa) — không chạy script.
  6. Xác nhận `guides/phase_5_retrieval_profiles_reranking.md:65` đã ghi MiniLM gỡ 26/10 (A thấy đã có) ⇒ A gỡ mục khỏi "Câu hỏi A còn nợ".
- **Không làm:** sửa code backend; sửa governance; chọn một phía khi guide ↔ code mâu thuẫn (báo A). **Xong:** nhắn A (danh sách file + diff stat); rồi review B71.
- **Trạng thái (13:59 27/10/2026, A): XONG** — A review đạt (đối chiếu 3 chỗ `file:dòng` guide 6 với code; `gold_draft` vẫn `bab707b9ab22`), commit. Trước: 13:57 C chờ review — 5 file tracked (chưa commit) + `validate_gold.py` private (diff `data/phase_8_1/tools/validate_gold_c62.diff`); chi tiết `STATUS_C.md`.
- Không ai: chạy thí nghiệm mới, mở câu kín, chạy `validate_gold.py`.

- **B71 review (C, 14:04): `ready_for_user_confirmation`** 0 / 0 / 2 minor — `phase_8_2_b1_rebase2_review.md`. **Khi merge sau B0** (m-2): sửa context 5 ⇒ 10 ở guide 6
  "Hiện hành" (~dòng 45), guide 8 (~dòng 18), `Project_Status.md` (~dòng 17, 100) + 4 chỗ báo cáo. m-1: log cổng giữ ở `data/phase_8_2/b1/rebase_2710/c_review/`.

### B72 — plan mốc cuối 8.2 (B3, câu kín) (giao 14:1x 27/10; 0 USD; chỉ viết plan, **không mở câu kín**)

- **Mục tiêu:** plan B3 sẵn sàng để khi User quyết mở câu kín (sau B0 + merge B1) chạy ngay. Spec 8.2 §5 "B3", §3 mục 7 (báo 36 + 33 câu), §6 mục 4, §7 (≈ 0,015 USD).
- **Viết** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md` theo `run-experiment` §1 (tiêu chí ghi **trước**: so chatbot cuối 8.2 vs chatbot đầu 8.2
  `f26485b`; chỉ số; sàn closed-world; thế nào là "làm hỏng"; judge Claude chấm mù cùng lượt), có mục "Căn cứ để review" (WORKFLOW §9.1). Ghi rõ: ai mở câu kín
  (một session / sub-agent được giao, không phải A); A đưa 3 số dòng câu A đã thấy cho người chạy (riêng, private); báo cáo giữ mù theo `Session_Prompt.md` §5;
  harness ghi từng dòng ngay (W23); trần tiền + pilot. Chỉ đọc metadata câu kín (số dòng, md5 `ddc59587b502`), **không đọc nội dung**.
- **Không làm:** chạy; commit (A commit sau review). **Xong:** nhắn A + báo sha ⇒ A giao session khác review trước khi duyệt sha.
- **Bản 1** `9d60b16b63da` ⇒ C review (C64) `changes_requested` 0 / 2 / 4. **A quyết (14:20):** M-1 — bỏ luật riêng "500 +1": câu 500 vì citation = câu hỏng (Completeness /
  Accuracy 1) ở cả hai bên, tính vào số câu tụt + TB, số 500 báo riêng; sàn = 0 câu ngoài kho bị trả lời + 0 lỗi kỹ thuật mạng / provider (chạy lại câu đó 1 lần, còn lỗi ⇒
  "chưa đủ") — §10.2 viết cho biến thể Bước 2 vs mốc B1, B3 so đầu ↔ cuối trên đường production. M-2 — A không đọc câu kín / file ghi câu; **người chạy (B)** đọc
  `sealed_user_feedback_private.md`, khớp số dòng ⇒ `data/phase_8_2/b3/a_seen_lines.json`; không đủ 3 ⇒ chỉ báo S36 + ghi chú. Không nhánh main ctx 5, không A/A câu kín.
  B sửa bản 2 ⇒ C kiểm phần sửa ⇒ A duyệt sha.
- **A DUYỆT bản 2 sha `27e75be5ed44` (14:26 27/10/2026)** sau C kiểm vòng 2 `ready_for_user_confirmation` 0 / 0 / 1 (m-5 giờ dòng 3 cũ — để nguyên, sửa = bản mới). A chấp nhận có ý thức
  hệ quả C nêu: n ≈ 33 ⇒ **một câu 500 citation mới** ở chatbot cuối gần như đủ "làm hỏng" (đúng ý: người dùng thấy lỗi); câu 500 ở chatbot đầu (validator v1) là phần
  thắng của citation v2 — plan đã ghi "cuối − đầu" đo gộp. **Chạy B3 khi:** B0 xong + B1 merge + User quyết mở câu kín. Người chạy: B.

### Phần tồn Phase cũ (User 14:15 27/10/2026: "xong phần tồn càng sớm càng tốt, xong phần tồn mới yên tâm đi tiếp các phase tiếp theo")

A chọn: nhóm 1 (nợ nhỏ, 0 USD) làm xong phiên này; nhóm 3 (sửa kho + build lại index) **soạn sẵn** phiên này, **áp ngay sau đóng 8.2** (sửa kho trước B3 làm mốc cuối
lẫn hai thay đổi). Chặn chính: B0 (User). Index Qwen3-8B (tồn từ 7A2, spec 8.2 để ngoài): quyết cùng đợt sửa kho.

### B73 — soạn đợt sửa kho (giao 14:15 27/10/2026; 0 USD; **không sửa `knowledge-base-hue/`**, không build, không ghi Qdrant)

- **Đầu vào:** `report_agent/2026-10-25_ra_soat_noi_dung_kho/` (C32 implementation + review: 97 / 139 mục chỉ có tự kiểm sub-agent ⇒ đọc lại từng mục trước khi đề
  xuất sửa); `data/ra_soat_kho_2026-10-25/danh_sach.md`; luật curated `Session_Prompt.md` §5; `knowledge-base-hue/meta/foods-template.md`; `backend/config/settings.yaml`
  `exclude_files` (file inventory `performing_arts` tự ghi phải loại).
- **Đầu ra (private, `data/sua_kho_2026-10-27/`):** (1) `de_xuat_sua.md` + một bản sửa dạng diff cho mỗi mục "sửa khi build lại" (53) sau khi đọc lại — mục không chắc
  thì chuyển nhóm, không đoán; (2) `cau_hoi_user.md`: 16 mục "User biết thì báo" bằng lời thường, mỗi câu có đáp án gợi ý từ kho; (3) `tra_ngoai.md`: 69 mục cần tra
  ngoài — đếm theo loại + nháp yêu cầu ChatGPT (gửi đi = đưa dữ liệu ra ngoài ⇒ User quyết); (4) đề xuất thêm file inventory `performing_arts` vào `exclude_files`
  (đếm chunk bị gỡ, `heading_path` / file nào khác còn trỏ tới nó). Report tracked (nếu có) chỉ số đếm, không nội dung kho.
- Được dùng sub-agent (≤ 3 file / sub-agent, grep loại `evaluation/`, `meta/`, `*sealed*`). **Dừng + báo A:** mục nào đòi chọn một phía khi nguồn trong kho ngang nhau.
- **Xong:** nhắn A (số mục theo nhóm, đường dẫn). A viết spec đợt sửa kho từ đó.

- **B73 XONG (14:31):** 41 sửa (diff) / 12 chuyển nhóm / 16 câu User / 78 tra ngoài / inventory 33 đoạn (`data/sua_kho_2026-10-27/README.md`); sự cố s7 (Golden Foods
  cũ) ⇒ edit đánh dấu `[s7-golden]`. A kiểm: kho không đổi (0 file mới từ 14:14), 41 diff. Spec nháp `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md`.

### B74 — kiểm độc lập đề xuất nhãn 3 câu test (C64 mục 3) + soạn diff tên hành chính sót (giao 14:33; 0 USD)

1. Kiểm `data/phase_8_2/gold_fix_proposal_2710/proposal_test_c64.jsonl` theo cách C61 kiểm C56 (quote = văn bản file tại offset; chunk trúng; hiệu ứng); ghi
   `report_agent/2026-10-26_cai_tien_tung_khau/c64_de_xuat_nhan_test_review.md`. **Không sửa `gold_v2.jsonl`.**
2. Phần "phát hiện ngoài mục" B73 (~15 tên hành chính cũ, cấp chưa thống nhất): soạn diff cùng cách (`data/sua_kho_2026-10-27/diffs_them/`), chỉ căn cứ trong kho;
   grep **chỉ** bằng `grep_kb.sh` (bẫy s7). Không sửa kho.

### C66 — review đề xuất sửa kho B73 (giao 14:33; 0 USD; không sửa kho)

- `data/sua_kho_2026-10-27/de_xuat_sua.md` + `diffs/` (41): mỗi diff đối chiếu file kho thật — căn cứ có trong kho, sửa đúng phạm vi mục, luật curated `Session_Prompt.md` §5.
  Ưu tiên: edit `[s7-golden]` (đặc biệt loại căn cứ ngoài ghi chú :39-44 và loại suy 2 bước), 4 chỗ "edit vượt dòng". **Không đọc `evaluation/`, Golden, câu kín**;
  grep loại `evaluation/`, `meta/`, `*sealed*`. Ghi `data/sua_kho_2026-10-27/review_c66.md` (giữ / bỏ / sửa từng mục) + report tracked ngắn (chỉ số đếm)
  `report_agent/2026-10-25_ra_soat_noi_dung_kho/sua_kho_de_xuat_review.md`.

### C64 — review plan B3 + nợ nhỏ (giao 14:15 27/10/2026; 0 USD trừ cổng ổn định ≈ 0,0005)

1. **Review plan B3** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md` (sha `9d60b16b63da`) theo WORKFLOW §9.1: **chỉ dựa trên mục "Căn cứ để review"**
   (không đọc STATUS_B / tin của B); không mở câu kín. Ghi `phase_8_2_b3_plan_review.md`. Ưu tiên trước.
2. `dense_ms` làm tròn 1 chữ số như các trường `*_ms` (B70 m-2) — sửa nhỏ `api/routes/chat.py` + test ghim; khai báo file; cổng ổn định; báo A (B review). B70 m-1
   (test danh sách trường chưa đi qua generator): **không viết code** — đóng bằng ghi bẫy (cổng ổn định đã kiểm), A ghi.
   **Mục 2 XONG (14:25):** A review đạt (diff 3 dòng, thử ngược đỏ, cổng 2 câu ≈ 0,000379 USD; guide 6 sửa theo); commit. B70 m-1 ⇒ bẫy `Project_Status.md` §8.
3. Đề xuất nhãn đoạn đúng cho 3 câu test C56 (95, 130, 138) theo cách C56 (`c56_de_xuat_sua_nhan.md`) ⇒ file đề xuất private trong `data/phase_8_2/gold_fix_proposal_2710/`;
   **không sửa `gold_v2.jsonl`** (User duyệt). Report tracked mô tả mức loại câu.

- **C64 XONG** (mục 1–3). Mục 3: đề xuất nhãn 3 câu test (`data/phase_8_2/gold_fix_proposal_2710/proposal_test_c64.jsonl`; report `c64_de_xuat_nhan_test.md`;
  test B1 7 ⇒ 9, K3b-m 10 ⇒ 11 / 15; kết luận đã đóng không đổi) ⇒ **B kiểm độc lập** (sau B73) ⇒ A trình User áp vào `gold_v2` (bản v3).

### C65 — kiểm câu 138 B1 test: `citation_error` "no citation" dù có `[Nguồn n]` (giao 14:31; 0 USD, chỉ đọc)

- Lượt B1 chạy với validator nào (so `9e6d371`); chuỗi trả lời đã lưu qua validator `main` hiện tại (offline) có lỗi không (lỗi ⇒ production trả 500 ⇒ ảnh hưởng B3);
  đếm dòng giống vậy trong `b1_{dev,test}.jsonl`. Report `report_agent/2026-10-25_phase_8_2_ap_dung/c65_citation_138_check.md` (mức loại câu).

### C63 — căn cứ cho brainstorm tính năng mới (giao 14:0x 27/10; 0 USD, chỉ đọc; review B71 ưu tiên hơn)

- User 27/10 chiều: ưu tiên **hội thoại nhiều lượt + streaming**; gợi ý / lịch trình ⇒ Phase 9; deploy khi ổn định; bảo vệ ~tháng 1/2027, xong càng sớm càng tốt.
- Đọc: `guides/phase_9_agentic_rag_roadmap.md` mục memory / conversation / multi-turn (~dòng 179–335); kết quả ChatGPT 26/10 phần streaming (C5); code `api/routes/chat.py`,
  `llm/generator_openai_full_corpus.py`, UI gọi `/api/chat`. Đầu ra `data/tinh_nang_moi_2026-10-27/c63_can_cu.md` (≤ 120 dòng: hiện trạng `file:dòng`; đã chốt + nguồn,
  chỗ đã cũ; câu thiết kế mở; rủi ro + cách đo; tách nguồn nói / suy ra). Không sửa file tracked.

### Hồ sơ thí nghiệm 8.2 (đã đóng — chỉ tra cứu)

Plan / implementation / review ở `report_agent/2026-10-25_phase_8_2_ap_dung/` (K1, K3, K3b, K3b-m answer, R1–R4); nhánh hồ sơ **không merge**: `p82-k1`, `p82-k3`
`80e7329`, `p82-k3b` `4c85195`, `p82-r1` `63a472f`, `p82-r2` `aec9ab8`. Bảng đủ: `TONG_HOP.md` §3 và handoff cũ (`git show a819789:session_prompt/CURRENT_HANDOFF.md`).
Đo hiện trạng 27/10 (0 / ít USD): C48 (số), C51 (kiểm sau sinh — gác), B65 (latency API), C58 (latency theo khâu), C56 / B69 (nhãn v2), C59 / C60 (log) —
`report_agent/2026-10-26_cai_tien_tung_khau/`.
