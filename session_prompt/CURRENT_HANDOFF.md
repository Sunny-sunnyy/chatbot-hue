# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 22:3x 25/10/2026 (A, **KẾT PHIÊN đêm 25/10** — User tắt máy: "session sau chúng ta sẽ tiếp tục"). Cách dùng: `WORKFLOW.md` §3, §6,
§7, §9. Chỉ giữ việc đang mở; việc đã xong: `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`, `PROJECT_HISTORY.md` (mục 25/10 22:3x).
Bản handoff đầy đủ trước khi rút gọn lần này (chi tiết từng mục việc đợt 1–2, rà code B25 / C34): `git show 76ff419:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống lúc kết phiên:** `main` (commit cuối `git log -1 main`). Chatbot **đã đổi** so với đầu phiên (đều đã review chéo + cổng ổn định):
validator nhận `[Nguồn n]` (`9e6d371`); import trần — **mọi lệnh chạy từ `backend/`** (`1e4acd0`), API 409 = cần dựng lại chỉ mục, 503 = Qdrant /
model lỗi tạm. Vẫn context 5, chưa NFC. Qdrant `:6335` còn **1** collection `hue_full_corpus_7a2_e5_small_384` (8.459). Repo `chatbot-hue`
**PUBLIC** (hook `.githooks/pre-commit`). File untracked `báo cáo nghiên cứu github.txt` ở gốc: của User (Phase 9) — **không đụng**.

**Nhánh đang mở:**
- **`dot3`** (C, đã push, `5e237bb`): đợt 3 sửa code — **3 / 12 commit** (C-21 `4f8c71c`, B-11 `749459d`, B-04 `5e237bb`); chưa review, chưa merge.
- **`p82-b1`** (`f23d396`): B1 của 8.2 (context 10 + NFC) — chưa review, chưa merge; dựng trên `main` cũ ⇒ rebase theo `sua_1b_plan.md` §6.

**Ba mạch việc:**
1. **Sửa code sau rà soát (User duyệt 19:4x cả 5 gói) — đang làm.** Xong: 1a, 1b, 3, 4 (+ 3c phần free). **Còn đợt 3** (gói 2 + 5 + B-12) trên
   `dot3` — mục "Việc đang mở" dưới. Sau đợt 3: cổng ổn định toàn hệ thống ⇒ coi như "Phase trước ổn định".
2. **Đợt tìm hướng tốt hơn từng khâu (User 20:0x) — chuẩn bị.** Ứng viên `ung_vien_cai_tien_{B,C}.md`; yêu cầu ChatGPT **đã viết, User chưa gửi**:
   `gửi chatgpt/2026-10-25/tìm thông tin/cai_tien_tung_khau_2026_10_25.md` (10 câu). Kết quả ⇒ A **một** tài liệu thiết kế (mốc = hệ thống sau 5 gói;
   ghép spec 8.2, không viết lại phần đã duyệt) ⇒ User duyệt ⇒ chạy.
3. **Phase 8.2 — TẠM DỪNG** (spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` sha `dabae90b2b60`). Chạy lại khi 5 gói xong +
   cổng ổn định đạt (User 20:0x: "phase trước ổn định mới tiếp phase sau"). Điều mới ảnh hưởng 8.2: mục "Phase 8.2" dưới.

**Thứ tự việc phiên sau:**
1. Mở A / B / C bằng `START_SESSION.md`; A `ListAgents`, cập nhật bảng Session; A **hỏi lại quyền phiên** (§9.8); kiểm `git branch --show-current` =
   `main`, `git log --oneline main..dot3` = 3 commit.
2. **C:** `git switch dot3` (working tree chung — báo A trước; B chỉ đọc) ⇒ `mkdir -p /tmp/c42` (script `d9.sh` ghi tạm ở đó) ⇒ chạy lại mốc D1 / D2
   bằng `data/ra_soat_code_2026-10-25/tools/dot3/` trước khi sửa ⇒ commit 4 … 12 theo plan ⇒ report `sua_dot3_implementation.md` (commit trên `dot3`)
   ⇒ `git switch main` ⇒ nhắn A.
3. **B:** trong lúc C làm — chờ / việc chỉ đọc A giao (W17); C xong ⇒ **review toàn nhánh `dot3`** (`git log main..dot3`, từng commit; trọng tâm D1 sha
   đoạn `60591acff422ece6`, D2 T1 `cefb2d1ad609`, D3 chuỗi gửi model 25 câu, D8 `git ls-files knowledge-base-hue` rỗng; T-C nếu cần: User `!` ở terminal B).
4. **A:** review đạt ⇒ (`main` có commit docs sau khi tách `dot3`: `76ff419`→`683f38d`+, chỉ tài liệu ⇒ C `git rebase main` trên `dot3` trước khi B review) ⇒ merge fast-forward `dot3` vào `main` + push + 4 chỗ `bao_cao_he_thong/` + `Project_Status.md` ⇒ cổng ổn định trên `main` ⇒ báo
   User "5 gói xong". Khi User đã gửi ChatGPT: đọc kết quả, WebFetch URL đối chiếu ⇒ tài liệu thiết kế đợt cải tiến.
5. Rồi mới: 8.2 (A review B1 sau rebase + chạy lại T1–T2 → B0 User đọc → merge → E1 …).

## Câu hỏi cho User (phiên sau)

1. **Quyền phiên** (điều phối rộng? trần tiền ≤ 1 USD?).
2. **Gửi ChatGPT** file yêu cầu nghiên cứu trên (deep research), lưu kết quả vào `gửi chatgpt/<ngày gửi>/kết quả nghiên cứu/`.
3. **Sổ cải tiến** (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`): duyệt / bác **W14** (nhắc lại ý User khi câu hỏi nhiều nghĩa), **W16** (quét trùng
   Golden / kho vào hook pre-commit — thay **W15**), **W17** (session rảnh ⇒ A giao việc không chồng file), **W18** (đề xuất có thứ tự ⇒ đối chiếu spec).
4. **Đọc cặp mù (B0)** khi tiện: `data/phase_8_2/b0/nhan_xet_user.md`, 20 câu, ~30–45 phút — cần trước khi đưa context 10 vào chatbot.
5. (Sẽ hỏi trong tài liệu thiết kế đợt cải tiến) model dense chạy máy mới (`bge-m3` / `Qwen3-Embedding-0.6B` — ngoài danh sách đã duyệt); gửi danh
   sách mâu thuẫn kho C32 ra ChatGPT tra nguồn (đưa dữ liệu ra ngoài); xác nhận "suy luận none" trên test (~0,007 USD).
6. Giữ từ trước (không gấp): rà kho C32 139 mục để đợt build lại index; tên dự án khác trong lịch sử git — để nguyên (gỡ lịch sử là phá hủy);
   3 câu kín A đã thấy — đã ghi trong spec 8.2 §3.7.

## Câu hỏi A còn nợ (phiên sau A trả lời, không cần User)

- Plan E1 (C, `phase_8_2_e1_plan.md` sha `f86240418ca1`) khi 8.2 chạy lại: **phải đổi** sang `paired_stats` + `false_refusal` (gói 3, C-02) và định nghĩa
  citation mới (1a) ⇒ sha mới ⇒ B review; §10 Q1 (test không đủ câu cho CI — "xác nhận hướng"?), Q2 (E1b hay thêm E1a), Q3 (A/A lấy từ B1 sau khi
  rebase + chạy lại).
- E2 (spec 8.2): sau 1a, mốc G2.0 và B1 còn **0** lỗi citation (`sua_3c_citation_v2.md`) ⇒ áp luật bỏ sớm ⇒ có thể NOT RUN — A ghi khi 8.2 chạy lại.
- Ghi chú B (vòng 3 spec 8.2): plan E3b thêm mức tụt Completeness / lỗi citation như E3a.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-77` (đêm 25/10) | Claude Opus 5.5 | trực tiếp | điều phối rà code + sửa 5 gói; duyệt plan 1b, đợt 3; 4 chỗ báo cáo; yêu cầu ChatGPT; sổ cải tiến vòng 4 | **kết phiên 22:3x** — `STATUS_A.md` |
| B — thực thi | `hue-rag-c3` (đêm 25/10) | Claude Opus 5.5 | trực tiếp | **kết phiên 22:28** — xong: B25, kiểm chéo, B26, review 1a / 3, gói 1b (`1e4acd0`), review plan đợt 3 (bản 3 ready), `ung_vien_cai_tien_B.md`; **phiên sau: review nhánh `dot3`** khi C xong; ~0,0004 USD | xem `STATUS_B.md` |
| C — thực thi | `hue-rag-7f` (đêm 25/10) | Claude Opus 5.5 | trực tiếp | **kết phiên 22:29** — xong: C34, kiểm chéo B25, review B26 / plan 1b / gói 1b, C35 gói 1a (`9e6d371`), gói 3 (`47a4e32`), 3c free, ứng viên, plan đợt 3; **đợt 3 DỞ 3 / 12 commit trên `dot3` (`5e237bb`, đã push)** | `STATUS_C.md`; ~0,0016 USD (0,000427 đo + ước cổng) |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit (trừ khi việc ghi rõ — đợt 3: C commit / push **nhánh `dot3`**); duyệt cho A =
  duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền
  trong report; code luôn `uv run` trong `.venv`; thư viện thừa giữ nguyên; luôn thử + so baseline trước khi chọn (User 24/10 20:49).
- **Luật User phiên đêm 25/10 (giữ cho tới khi xong việc sửa code):** báo cáo "nên sửa gì" trước, **chỉ sửa khi User đồng ý** (đã đồng ý 5 gói
  19:4x); **commit + push trước mỗi lần sửa code**; sau sửa hệ thống phải hoạt động bình thường, ổn định, tối ưu, đóng gói đầy đủ (cổng ổn định
  dưới); được thử nghiệm / so sánh / đánh giá để chọn cách tốt nhất; phase trước ổn định mới sang phase sau.
- **Phiên đêm 25/10 (User 18:2x) — HẾT HẠN, hỏi lại:** A tự điều phối B/C rộng; API ≤ 1 USD cả phiên (dùng ~0,003). Trần 8.2: 0,5 USD (spec;
  đã dùng 0,0369). Luật kỹ thuật giữ: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra (~0,000133 USD / câu context 5; ~0,000204 context 10).

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024 | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_draft.jsonl` | đoạn đúng 55 câu (40 dev / 15 test) | `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (82 / 65 / 29) | `0b65d1c138d2` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín chính thức — **không đọc** tới mốc cuối 8.2 | md5 `ddc59587b502` |
| `data/phase_8_1/baseline/g0_6_manifest.json` | manifest khóa G0.6 (hash mọi file mốc) — kiểm lại 22:3x: không đổi | `9ea480d0d083` |
| `data/phase_8_1/{g1,g2,g3,g4,g4k}/`, `data/phase_8_1/tools/` | kết quả từng câu các gate; script dùng lại | — |
| `data/phase_8_2/b0/` | đọc cặp mù: `doc_cap_mu.md` (`37b66efb3499`), `nhan_xet_user.md` (User ghi), **`khoa.json` chỉ A** (`5b9240842b7b`) | — |
| `data/phase_8_2/b1/` | kết quả chạy B1 | — |
| `data/ra_soat_kho_2026-10-25/` | rà kho C32: `danh_sach.md` 139 mục | — |
| `data/ra_soat_code_2026-10-25/citation_v2/` | lỗi citation tính lại theo validator mới, 14 lượt + `summary.json` (3c) | — |
| `data/ra_soat_code_2026-10-25/tools/` (gồm `dot3/`: D1, D4, D7, D8, D9 + mốc `t1_base.jsonl`, `3b_base.json`), `data/ra_soat_code/` | script + ghi chú rà / sửa code của C / B | — |
| `data/tools/overlap_scan.py` | quét trùng Golden / kho (cửa sổ 40 ký tự, exit 1 khi trùng) — **chạy trước mỗi commit file người khác viết** | — |
| `gửi chatgpt/2026-10-25/tìm thông tin/cai_tien_tung_khau_2026_10_25.md` | yêu cầu nghiên cứu đợt cải tiến (10 câu) | — |

## Việc đang mở

### Đợt 3 sửa code — gói 2 + gói 5 + B-12 (nhánh `dot3`, C làm, B review)

- **Plan duyệt:** `report_agent/2026-10-25_ra_soat_code/sua_dot3_plan.md` bản 3 sha **`7c8c660558e5`** (A 21:53; B review bản 2 changes_requested — M-1
  `git mv` vào thư mục ignore vẫn vào index — bản 3 B kiểm ready). Review: `sua_dot3_plan_review.md`. A quyết: ghi vào `knowledge-base-hue/meta/` được
  (= lựa chọn User câu 4); **không** thêm fixture `private_corpus` (§7).
- **12 commit theo plan:** 1 C-21 ✔ · 2 B-11 ✔ · 3 B-04 ✔ · **4 B-20** (identity + sparse bytes + discovery theo record) · 5 B-12 (`cp` + `git rm`, sao lưu
  `meta/backup_b12_<ngày>/`, sha bản gốc = bản mới; `git ls-files knowledge-base-hue` rỗng) · 6 gỡ smoke Phase 5 + nhánh `minilm` · 7 gỡ Representation B
  (+ `make_fits_all_checker`, notebook 06, guide 6) · 8 gỡ code chết nhỏ · 9 test (C-17, C-18) · 10 dọn chunker (B-14, B-15) · 11 kiểm điểm Qdrant một
  lần (B-02) · 12 chuyển 2 converter ra `data/tools/` (B-13). Gỡ chỉ khi 0 nơi gọi (grep cả CLI, notebook, harness, `p82-b1`) — luật User (2).
- **Cổng D mỗi nhóm (plan §5):** D1 sha đoạn toàn kho `60591acff422ece6` giống hệt; D2 T1 retrieval `cefb2d1ad609` (158 dòng); D3 chuỗi gửi model 25
  câu giống byte; D4 15 / 16 file test, lỗi C-17 không tăng (T-C: User `!`); D5 cổng ổn định; D6 0 nơi gọi; D7 số dòng code (trước 8.518); D8 0 chuỗi
  kho trong file tracked. Paid ≤ 0,003 USD cả đợt (đã ~0,0004).
- **Lệch plan đã ghi:** test C-21 assert `"target is non-empty"` (lý do dừng thật). B-11 thêm cache kiểm token mỗi tài liệu (chia toàn kho 23,8 s; không
  cache 50,7 s). Chi tiết dở: `STATUS_C.md`.
- **Đóng:** C report `sua_dot3_implementation.md` ⇒ B review toàn nhánh ⇒ A merge ff + 4 chỗ báo cáo (`LUONG`, `BAO_CAO_CHIA_DOAN`, `BAO_CAO_KHO_DU_LIEU`
  / `BAO_CAO_SINH…` nếu hành vi đổi, nhật ký) + `Project_Status.md` + cổng ổn định trên `main`.

### Luật chung khi sửa code (User 18:3x, 19:4x, 20:0x)

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê
  file, không `--env-file` trừ khi mục ghi; report `sua_<gói>_implementation.md`; review chéo (người kia); plan có tiêu chí ghi trước ⇒ session khác
  review **trước** khi A duyệt sha (§9.1). Dừng khi: đường thật đổi ngoài dự kiến; phải đụng file người kia đang khai báo; vượt tiền.
- **Cổng ổn định sau mỗi gói:** (1) test các file chạm, lỗi cũ C-17 ghi rõ; (2) chạy thật `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env
  uvicorn api.app:app --port 8011`: `/` 200, `/health` 5 / 5 ready, 1 câu trong kho (200, marker = `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết,
  không Golden, body `{"query": …}`; log sạch; tắt server; (3) chạm tìm kiếm / chia đoạn: T1 giống byte, sha đoạn giống hệt; (4) 4 chỗ báo cáo nếu
  hành vi đổi; (5) quét `data/tools/overlap_scan.py` trước commit; A commit + push.
- Test cần key OpenAI (không chạy mặc định): `test_api_chat.py` (3 test — C-17 sẽ sửa ở commit 9), `test_openai_full_corpus_generator.py`,
  `test_phase6_live_smoke.py`. Test thiếu model `tests/test_startup_model_missing.py`: auto mode chặn ⇒ User chạy `!` ở terminal session cần.

### Đợt tìm hướng tốt hơn từng khâu (User 20:0x) — chuẩn bị

User: "dựa vào kiến thức, tham khảo, trao đổi với B, C xem có thể thử nghiệm, so sánh, đánh giá để xem có hướng nào tốt hơn, tối ưu hơn, ổn định
hơn; giữ mốc hiện tại làm base; A, B, C được so sánh, thử nghiệm, rồi đưa ra kết luận; có thể nhờ ChatGPT nghiên cứu".
- Ứng viên: C 12 dòng (trả lời / đánh giá — top: reasoning `none` xác nhận test ~0,007 USD; bỏ sớm E2; đo bám nguồn bằng code; log usage + độ trễ ở API;
  đa dạng nguồn / MMR; tách câu so sánh), B 10 dòng (dựng kho — sửa 22 mâu thuẫn chắc rồi build lại; câu hóa hàng bảng; dòng ngữ cảnh tất định; bỏ
  huydang; trọng số tiêu đề BM25; dense local mới — cần User; build không ngừng phục vụ…). Ước ~0,08–0,09 USD mỗi bên nếu làm phần đầu.
- Bước: kết quả ChatGPT ⇒ A gộp ⇒ **một** tài liệu thiết kế `docs/superpowers/specs/` (tiêu chí ghi trước `run-experiment`, cỡ mẫu, trần tiền, mốc =
  hệ thống sau 5 gói) ⇒ session khác review ⇒ User duyệt một lần.

### Phase 8.2 — TẠM DỪNG (User 16:5x 25/10)

- Spec `dabae90b2b60`. B0 file đọc cặp mù ready (User đọc khi tiện). **B1** (B, T1–T5 đạt, 0,0369 USD; report `phase_8_2_b1_implementation.md` sha
  `bb5fea83aeb6` trên nhánh) **chưa A review**; nhánh `p82-b1` phải **rebase** lên `main` mới (xung đột import ở `retrieval/full_corpus.py`, đổi import
  ở `test_full_corpus_retrieval.py`, comment `b1.py:23` — `sua_1b_plan.md` §6) rồi **chạy lại T1–T2** (không dùng lại bằng chứng cũ).
- Điều mới từ rà code: lỗi citation đếm theo định nghĩa mới ⇒ A/A context 10 = 0 vs 0 (trước 12 vs 8); E2 có thể NOT RUN; plan E1 đổi sang
  `paired_stats` (mục "Câu hỏi A còn nợ"). Tiền 8.2: 0,0369 / 0,5 USD.
- Chi tiết việc 8.2 phiên tối 25/10 (B22, B23, B24, C32, C33): `git show bc568f1:session_prompt/CURRENT_HANDOFF.md`.
