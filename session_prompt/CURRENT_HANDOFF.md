# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 14:16 26/10/2026 (A, **mở phiên 26/10**: quyền phiên, giao C đợt 3, B40; kết phiên trước 22:3x 25/10). Cách dùng: `WORKFLOW.md` §3, §6,
§7, §9. Chỉ giữ việc đang mở; việc đã xong: `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`, `PROJECT_HISTORY.md` (mục 25/10 22:3x).
Bản handoff đầy đủ trước khi rút gọn lần này (chi tiết từng mục việc đợt 1–2, rà code B25 / C34): `git show 76ff419:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống (16:0x 26/10):** `main` (commit cuối `git log -1 main`). **Sửa code sau rà soát xong cả 5 gói** — đợt 3 merge `421c302` (`--no-ff`, giữ
sha B review), cổng ổn định trên `main` đạt (A 16:0x: 8.459 đoạn sha `60591acff422ece6` + identity = record; T1 158 dòng `cefb2d1ad609`; pytest
197 p / 1 f / 4 e = phần cần key; `/health` 5 / 5, 1 câu trong kho có nguồn, 1 câu ngoài kho từ chối, log 0 lỗi). Chatbot vẫn context 5, chưa NFC,
reasoning mặc định (`medium`, không gửi tham số). Qdrant `:6335` còn **1** collection (8.459). Repo `chatbot-hue` **PUBLIC**. File untracked
`báo cáo nghiên cứu github.txt` ở gốc: của User (Phase 9) — **không đụng**. 8 file `reports/artifacts/` chứa nguyên văn kho ⇒
`data/reports_artifacts_private_2026-10-26/` (User chọn (a) 26/10), gỡ khỏi repo.

**Nhánh đang mở:** `p82-b1` (`f23d396`) — B1 của 8.2 (context 10 + NFC), chưa review; rebase lên `main` mới sẽ xung đột thêm (đợt 3 gỡ Rep B ở
`settings.yaml` / `settings_loader.py` / `test_phase6_settings.py`, `minilm` + `REPO_ROOT` ở `retrieval/full_corpus.py` — `sua_dot3_review.md` §6) — B xử lý
khi 8.2 chạy lại. `dot3` đã merge (giữ nhánh trên origin tới khi User bảo xóa).

**Mạch việc:**
1. **Đợt tìm hướng tốt hơn từng khâu** (User 20:0x 25/10) — kết quả ChatGPT có; B40 đối chiếu xong (`report_agent/2026-10-26_cai_tien_tung_khau/`).
   Chờ User chọn phạm vi (A khuyên A: khâu trả lời trước). Thứ tự A đề xuất: B0 (User đọc cặp mù) ⇒ B1 context 10 vào chatbot ⇒ đợt cải tiến trên
   mốc context 10 (báo cáo ChatGPT §6.1 cũng lấy mốc 10) — **lệch handoff cũ** ("mốc = sau 5 gói, context 5") ⇒ chốt với User trong tài liệu thiết kế.
2. **Phase 8.2 — TẠM DỪNG**, nay đủ điều kiện chạy lại (5 gói xong + cổng ổn định). Điều mới: mục "Phase 8.2" dưới.

## Câu hỏi cho User (phiên sau)

1. ~~Quyền phiên~~ — User 14:1x 26/10 (mục Quyền). ~~Gửi ChatGPT~~ — kết quả có 26/10. Lệnh gỡ 8 artifacts — User chọn (a) 26/10.
2. **Phạm vi đợt cải tiến** (A khuyên: khâu trả lời trước — reasoning `none` / `low`, đa dạng nguồn; dựng kho / embedding mới để sau) và thứ tự
   B0 ⇒ B1 ⇒ đợt cải tiến trên mốc context 10.
   **80 report lịch sử** (`reports/` 70, `docs/superpowers/` 5, `handoff_prompt/` 4, `report_agent/` 1; 08–09/2026) còn dòng trùng kho ≥ 40 ký tự
   (~960 dòng, nhiều chỗ là tên file / tiêu đề; 1 dòng trùng cả đáp án Golden — report 06/09, trước khi có Golden): để nguyên hay xử lý.
3. **Sổ cải tiến** (A đề xuất 26/10: duyệt W14, W16, W17; W18 gộp vào W14; bác W15 — S23 lặp lại 26/10 ở C) (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`): duyệt / bác **W14** (nhắc lại ý User khi câu hỏi nhiều nghĩa), **W16** (quét trùng
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
| A — điều phối | `hue-rag-b0` (26/10) | Claude Opus 5.5 | trực tiếp | merge đợt 3 + cổng ổn định + báo cáo; trao đổi User về đợt cải tiến | đang làm |
| B — thực thi | `hue-rag-3e` (26/10) | Claude Opus 5.5 | trực tiếp | xong: B40, review `dot3` (ready); **kiểm phần A tự sửa** (gỡ 8 artifacts + tài liệu) | đang làm |
| C — thực thi | `hue-rag-87` (26/10) | Claude Opus 5.5 | trực tiếp | **đợt 3 xong** 15:5x: 12 / 12 commit + docs trên `dot3` (`origin/dot3` = `2c420aa`), report `sua_dot3_implementation.md`; B review ready (m-1, m-2 đã sửa); C về `main`; ~0,0024 USD ước | **chờ A merge** — `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit (trừ khi việc ghi rõ — đợt 3: C commit / push **nhánh `dot3`**); duyệt cho A =
  duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền
  trong report; code luôn `uv run` trong `.venv`; thư viện thừa giữ nguyên; luôn thử + so baseline trước khi chọn (User 24/10 20:49).
- **Luật User phiên đêm 25/10 (giữ cho tới khi xong việc sửa code):** báo cáo "nên sửa gì" trước, **chỉ sửa khi User đồng ý** (đã đồng ý 5 gói
  19:4x); **commit + push trước mỗi lần sửa code**; sau sửa hệ thống phải hoạt động bình thường, ổn định, tối ưu, đóng gói đầy đủ (cổng ổn định
  dưới); được thử nghiệm / so sánh / đánh giá để chọn cách tốt nhất; phase trước ổn định mới sang phase sau.
- **Phiên 26/10 (User 14:1x, hết hạn cuối phiên):** A tự điều phối B/C rộng như phiên trước; API ≤ 1 USD cả phiên; C commit / push nhánh `dot3`
  tiếp (chỉ đợt 3). Trần 8.2: 0,5 USD (spec; đã dùng 0,0369). Luật kỹ thuật giữ: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
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

### Đợt 3 sửa code — XONG 16:0x 26/10

C 12 commit + docs (`sua_dot3_implementation.md`), B review ready 0 / 0 / 3 minor (`sua_dot3_review.md`, sha `4ee8e5f90199`; m-1, m-2 C sửa; m-3 A sửa
trong commit tài liệu), A merge `421c302` + cổng ổn định trên `main` đạt + 4 chỗ báo cáo + `Project_Status.md`. Phần A tự sửa (gỡ 8 file artifacts,
tài liệu) ⇒ B kiểm. Tiền đợt ~0,0024 USD (C) + ~0,0004 (B) + ~0,0004 (A) — ước. Tạm `/tmp/c42` (~105 MB) giữ tới khi xong kiểm; xóa cần User `!`.

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
- **Kết quả ChatGPT đã có** (User 14:1x 26/10): `gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md`
  (private, 155 dòng; 10 câu C1–C6, D1–D4 + ma trận ưu tiên + giao thức đo). A đã WebFetch đối chiếu: ALCE 85,1 % / 77,6 % (khớp, phụ lục G.5);
  Anthropic contextual 5,7 → 3,7 → 2,9 → 1,9 % (khớp); trang model `gpt-6-luna`: effort `none / low / medium (mặc định) / high / xhigh / max` — không
  có `minimal`; runtime hiện **không gửi** reasoning ⇒ đang chạy `medium`.
- **B40 (B, chỉ đọc, A giao 14:1x 26/10):** đối chiếu kết quả ChatGPT với code + số đo thật của hệ thống: mỗi mục C1–C6, D1–D4 ghi (a) hệ thống đã có
  / chưa có (`file:dòng`), (b) chỗ báo cáo mô tả sai hệ thống (ví dụ D3 nói "BM25 tự viết, không dùng sparse Qdrant" — kiểm), (c) mục trùng /
  khác `ung_vien_cai_tien_{B,C}.md`, (d) dữ liệu sẵn có để đo (đoạn đúng 55 câu, nhãn loại câu…) và cỡ mẫu thật có được. Không đề xuất thiết
  kế thí nghiệm chi tiết (A làm). Không mở câu kín; không chép nội dung kho / Golden / nguyên văn báo cáo. Đầu ra:
  `report_agent/2026-10-26_cai_tien_tung_khau/doi_chieu_nghien_cuu_B.md`. 0 USD. Khi C báo xong đợt 3 ⇒ B dừng B40 (ghi chỗ dở) và review `dot3`.
- Bước: kết quả ChatGPT ⇒ A gộp ⇒ **một** tài liệu thiết kế `docs/superpowers/specs/` (tiêu chí ghi trước `run-experiment`, cỡ mẫu, trần tiền, mốc =
  hệ thống sau 5 gói) ⇒ session khác review ⇒ User duyệt một lần.

### Phase 8.2 — TẠM DỪNG (User 16:5x 25/10)

- Spec `dabae90b2b60`. B0 file đọc cặp mù ready (User đọc khi tiện). **B1** (B, T1–T5 đạt, 0,0369 USD; report `phase_8_2_b1_implementation.md` sha
  `bb5fea83aeb6` trên nhánh) **chưa A review**; nhánh `p82-b1` phải **rebase** lên `main` mới (xung đột import ở `retrieval/full_corpus.py`, đổi import
  ở `test_full_corpus_retrieval.py`, comment `b1.py:23` — `sua_1b_plan.md` §6) rồi **chạy lại T1–T2** (không dùng lại bằng chứng cũ).
- Điều mới từ rà code: lỗi citation đếm theo định nghĩa mới ⇒ A/A context 10 = 0 vs 0 (trước 12 vs 8); E2 có thể NOT RUN; plan E1 đổi sang
  `paired_stats` (mục "Câu hỏi A còn nợ"). Tiền 8.2: 0,0369 / 0,5 USD.
- Chi tiết việc 8.2 phiên tối 25/10 (B22, B23, B24, C32, C33): `git show bc568f1:session_prompt/CURRENT_HANDOFF.md`.
