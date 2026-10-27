# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 08:47 27/10/2026 (A, **MỞ PHIÊN 27/10** — User duyệt quyền phiên, W21–W23, Q2 §10.6; trả lời mục tiêu sản phẩm; A giao B53 / B54 / C46). Trước: 22:31 26/10/2026 (A, **KẾT PHIÊN TỐI 26/10** — User chọn (b): "các nhiệm vụ, câu hỏi để session tiếp theo"). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9.
Chỉ giữ việc đang mở. Chi tiết phiên tối 26/10 (quyết định theo giờ, kết quả, tiền): `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`;
nhật ký cho User `bao_cao_he_thong/nhat_ky/2026-10-26_toi_cai_tien_tung_khau.md`. Bản handoff trước khi viết lại: `git show 087cedd:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống:** `main` (commit cuối `git log -1 main`). **Chatbot không đổi từ 26/10 16:0x:** context 5, chưa NFC, reasoning `medium` mặc định (không gửi
tham số). Qdrant `:6335` **1** collection `hue_full_corpus_7a2_e5_small_384` (8.459). Repo `chatbot-hue` **PUBLIC**. Untracked ở gốc **của User, không
đụng**: `báo cáo nghiên cứu github.txt` (Phase 9), `tham khảo 26_10/` (User nghiên cứu riêng, **không liên quan dự án**). Hook pre-commit quét trùng
Golden / kho / câu kín trên dòng thêm mới (`.githooks/overlap_scan.py`, < 1 s).

**Phase 8.2 đang chạy** (spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` — bản gốc `dabae90b2b60` + **§10 "Sửa đổi 26/10"**, bản
A duyệt hiện hành **`cd910c4c4169`**). Bước 2 = **đợt cải tiến từng khâu** (User 21:1x: phạm vi B — khâu trả lời + khâu tìm, không ghi Qdrant).
- **B0** (User đọc cặp mù, `data/phase_8_2/b0/nhan_xet_user.md`, 20 câu, ~30–45 phút): **chưa làm** — chặn merge B1 và chặn chốt mọi kết luận dựa judge.
- **B1** (context 10 + NFC): nhánh `p82-b1` `811d25d` (rebase lên `main` 26/10, T1 giống byte, T2 không gọi model 176 / 176) — review A ready
  (`phase_8_2_b1_rebase_review.md`); **merge sau B0** + luật dừng B0 + cổng ổn định (khi đó lần đầu có `/chat` thật context 10).
- **Kết quả Bước 2 (đóng 27/10)** (mốc B1 `811d25d`): K1, K3, K3b-n, R1, R2 **kém hơn**; K3b-m tầng tìm tốt hơn (tạm), khâu trả lời kém hơn theo luật; K2 / E2 / R3
  **NOT RUN**; R4 thước số xong (`2c7ecfd`). Bảng chi tiết ở mục "Phase 8.2 Bước 2" dưới và `TONG_HOP.md`.
- Tiền 8.2: **≈ 0,212 / 0,5 USD, cận trên ≈ 0,218** (B1 0,0369 + R2 0,0027 + K3 0,0251 + R1 0,0049 + K3b log 0,0592 + l1_rest n ước 0,0087 [cận trên ≈ 0,0142] + K3b-m answer 0,0749 — 27/10).
- **Dạng lỗi chung R1 / R2 / P1 8.1** (câu 160, 168): trả lời vòng (một câu có `[n]` cùng chủ đề) + một câu "nguồn không nêu…" không citation ⇒ validator nhận. Hướng mở
  (A cân nhắc, chưa giao): kiểm bằng code sau sinh cho dạng này, kiểm trước trên 160 / 168 — có thể mở lại R1 / R2.
  **C51 (09:32 27/10/2026, `c51_kiem_sau_sinh_kha_thi.md`):** luật L2 bắt 160 + 168 (sau khi chỉnh trên chính 2 câu đó ⇒ nguy cơ khớp quá mẫu), 0 cờ ở chatbot hiện tại;
  không tách được "lạc đề" với "một phần có ích" ⇒ không dùng cho R2. **A quyết: gác** R1 + L2 — lợi R1 nhỏ (USD ~0,95×, token ra ~0,72×), thêm một luật hình
  thức khớp từ 2 câu + đổi hợp đồng Phase 6; không thêm L2 vào chatbot hiện tại (0 cờ = chưa có vấn đề quan sát được, `Session_Prompt.md` §7). Mở lại khi cần
  bớt latency khâu sinh (ví dụ ghép với K3b).

**Luật nhận của đợt (spec §10.2, User):** (a) chất lượng giữ (Completeness TB ≥ −0,1 **và** số câu tụt ≤ A/A + 3) + rẻ / nhanh hơn rõ; (i) chất lượng tăng
vượt nhiễu (CI 95 % > 0, Holm theo nhánh, cỡ mẫu ≥ 5 / 0) + khâu tìm ≤ +50 ms / khâu sinh `output_tokens` ≤ +20 % + không thêm lần gọi API, USD / câu
≤ +20 %; tốn hơn / chậm hơn (K3) ⇒ **trình User kèm số**. Ba nguyên tắc User dùng chung (`Session_Prompt.md` §7): **chất lượng cần thiết trước, tối ưu
sau**; **hiệu suất = tiền + tốc độ**; **đo theo mục tiêu sản phẩm cuối cùng** (`Project_Status.md` §1 "Mục tiêu sản phẩm" — chờ User 4 câu).

**Mã hay gặp:** B0 / B1 / B2 / B3 = bước spec 8.2; K1–K3 (khâu tìm), R1–R4 (khâu trả lời) = biến thể spec §10.3; T1 = kết quả tìm 158 câu (mốc sha
`cefb2d1ad609`); A/A = hai lượt cùng cấu hình đo nhiễu; S / W = sự cố / đề xuất trong `SO_CAI_TIEN_CACH_LAM.md`; Bxx / Cxx = việc của B / C.

**Thứ tự việc (cập nhật 11:18 27/10/2026 — đợt cải tiến ĐÓNG, User chọn (1) chốt đợt):**
1. ~~Bước 2 đợt cải tiến~~ — **đóng** (`report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`; bảng thí nghiệm dưới). Không thử thêm biến thể khi chưa có
   quyết định mới của User.
2. **B0** (User đọc cặp mù) — việc duy nhất còn chặn merge B1.
3. Sau B0: merge B1 (`p82-b1` `811d25d`; **B63 27/10: rebase lên `main` `e952fa3` không xung đột, 68 passed / 1 failed do thiếu key, T1 giống byte**) + luật dừng B0 + cổng ổn định ⇒ chatbot lên context 10 + NFC; 4 chỗ báo cáo.
4. Mốc cuối 8.2 (câu kín — User quyết mở) ⇒ đóng 8.2 ⇒ tính năng mới (User 27/10).
5. Hồ sơ hướng mở (không làm khi chưa có quyết định): K3b-m / K3c khi có luật nhận cho biến thể đổi context + thời gian chờ có số; streaming từng câu đã kiểm;
   sửa nhãn đoạn đúng "một chỗ / thông tin"; mở rộng bộ câu tự nhiên.

**Trong lúc User đi ăn (11:38 27/10/2026, User: "tiếp tục chỉnh sửa, điều phối, phát triển, cải thiện, so sánh, đánh giá"):** A giao việc 0 / ít tiền, không đổi chatbot:
- **C56 xong** (`report_agent/2026-10-26_cai_tien_tung_khau/c56_de_xuat_sua_nhan.md`; nháp private `data/phase_8_2/gold_fix_proposal_2710/`): đề xuất thêm 3 khoảng nhãn
  (120: 2, 156: 1); 143 là lỗi **cách đếm** (bỏ qua tiêu đề mục), không phải nhãn; 3 câu test chưa quyết. **B66 kiểm 11:48 27/10/2026: đồng ý cả ba** (3 khoảng đúng nguyên văn, mỗi khoảng 1 chunk; 156 không phải báo nhầm — B sửa nhận định B61;
  143 = lỗi cách đếm, nghiêng sửa hàm đếm tính `heading_path` cho lần đo sau) ⇒ **chờ User duyệt** áp 3 khoảng + đổi hàm đếm.
- **B65 xong** (`b65_latency_dau_cuoi.md`): e2e thật p50 / p95 — main context 5: 3,3 / 5,7 s tuần tự, 3,6 / 6,2 s đồng thời 4; B1 context 10: 3,1 / 6,0 s, 3,4 / 6,4 s;
  chênh cặp không thấy khác; 0 lỗi, OOS 2 / 2; ≈ 0,016 USD (ước, API không trả usage). C57 review ready sau sửa (11:52 27/10/2026): K3b-m thêm chọn đoạn ≈ 4,6–5 s p50
  (đo trực tiếp) ⇒ ước ≈ 8 s p50 qua API (suy ra); **bản đang chạy p95 qua API 5,7–6,2 s — đã vượt mức theo dõi 5 s** (khâu sinh chiếm phần lớn).
- Vòng cải tiến 7: W24–W26 đề xuất (`SO_CAI_TIEN_CACH_LAM.md`) — chờ User.
- **C58 xong** (`c58_latency_theo_khau.md`, B67 ready sau sửa nhãn; 0,0075 USD): gọi model ≈ 98 % thời gian chờ — đã chứng minh khoảng dư ở bước sinh, không ở
  HTTP / tìm / ngữ cảnh / citation; giải thích được bằng token ra (≈ 11,5 ms / token, r 0,97), chưa can thiệp. Không có chỗ thừa ở đường API.
- **C59 plan** log token + thời gian theo khâu mỗi câu ở `/api/chat`: bản 2 **`7f1456a1ae55`** (B68 vòng 1 changes_requested ⇒ vòng 2 **ready** 12:19 27/10/2026; m-4, m-5 ghi khi code);
  đổi code main ⇒ **chờ User duyệt** (đề xuất: C code, B review, cổng ổn định, ≈ 0,0003 USD).

## Câu hỏi cho User (phiên sau — gói trong báo cáo mở phiên, mỗi câu có khuyến nghị)

1. **Quyền phiên** (như bước 2 trên). A khuyên: giữ như tối 26/10 + K3 ≤ 0,20 USD.
2. **Mục tiêu sản phẩm** (`Project_Status.md` §1): người dùng chính là ai; câu trả lời "dùng được" là gì; lỗi nào tệ nhất; yêu cầu phi chức năng bằng số
   (chờ tối đa — A tạm theo dõi p95 ≤ 5 s; tiền tối đa / câu; chạy ở đâu). Cần để chọn thước đo sát mục tiêu (nguyên tắc User 22:0x).
3. **Q2 spec §10.6:** xác nhận trên test = "không làm hỏng" (sàn + mức tụt), không đòi "tốt hơn" — A khuyên đồng ý (test 41 câu quá nhỏ).
4. **Sổ cải tiến vòng 6:** W21 (sha duyệt tính từ file), W22 (bẫy lệnh ghép bị auto mode chặn), W23 (trần đếm trên đúng mốc + harness chặn ghi đè) — A
   khuyên duyệt cả ba (mỗi cái 2 lần trong phiên tối 26/10).
5. **B0** khi tiện (chỉ User làm được).
6. ~~Xóa nhánh `dot3`~~ — **xong 08:54 27/10/2026** (User `!`: xóa cả local `2c420aa` lẫn `origin`).
7. Giữ từ trước (không gấp): `/api/chat` chưa log token / tiền; mâu thuẫn kho Hải Vân Quan (STATUS_B); rà kho C32 139 mục (gửi ChatGPT tra nguồn = đưa
   dữ liệu ra ngoài — hỏi khi tới); tên dự án khác trong lịch sử git — để nguyên; 3 câu kín A đã thấy (spec 8.2 §3.7); hướng mở: viết thêm câu tự nhiên
   cho bộ đo (R3 thiếu câu; B42: câu tự nhiên không lợi từ context 10).

## Câu hỏi A còn nợ (phiên sau A trả lời, không cần User)

- K3 thắng thì "làm nhanh / rẻ hơn" bằng cách nào (luna N nhỏ hơn? reranker CPU — 8.1 M1 / M2 chỉ đo GPU) — A đề xuất sau khi có số K3.
- Hướng R2: chỉ mở lại khi có cách chặn dạng lỗi câu 160 (câu ý chung có `[n]` + "nguồn không có…") **được kiểm trước** (ví dụ kiểm bằng code sau sinh).
- `CURRENT_HANDOFF.md` còn dài (~150 dòng): giữ vì User muốn đủ chi tiết; mục File private + Cổng ổn định là tham chiếu.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-5f` (27/10) | Claude Opus 5.5 | trực tiếp | mở phiên 08:47 27/10/2026: quyền User có; giao B53 → B54, C46 (plan R1); bàn mục tiêu sản phẩm với User | `STATUS_A.md` |
| B — thực thi | `hue-rag-31` (27/10) | Claude Opus 5.5 | trực tiếp | **B53** review R2 → **B54** chạy K3 (`p82-k3`, ≤ 0,20 USD) | `STATUS_B.md` |
| C — thực thi | `hue-rag-5b` (27/10) | Claude Opus 5.5 | trực tiếp | **C46** plan R1 (working tree chung, 0 USD) → review K3 khi B xong; sửa report R2 nếu B53 có finding | `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho
  việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run` trong `.venv`;
  luôn thử + so baseline trước khi chọn (User 24/10 20:49); commit trước sửa code + cổng ổn định sau mỗi gói (User 20:4x 26/10, câu 5); "báo trước, chờ
  User đồng ý" chỉ áp ngoài phạm vi đã duyệt.
- **Phiên 27/10 (User 08:47 27/10/2026, hết hạn cuối phiên):** như tối 26/10 — A tự điều phối B/C + tự thử / chọn trong luật nhận của đợt; API ≤ 1 USD cả phiên;
  **B commit + push `p82-k3`, K3 ≤ 0,20 USD** (con: tìm 0,08 / sinh 0,12). Q2 spec §10.6: xác nhận trên test = "không làm hỏng" (User đồng ý).
  A giao (08:55 27/10/2026, trong quyền tự điều phối + trần 1 USD): **C commit + push `p82-r1`** (không merge), worktree `/tmp/c_r1`, R1 ≤ 0,05 USD, judge sub-agent — chỉ sau khi
  plan R1 qua B review và A ghi duyệt sha.
- Phiên tối 26/10 (User 20:3x, 21:1x) — đã hết hạn: A tự điều phối B/C + tự đề xuất / thử / chọn trong luật; API ≤ 1 USD cả phiên (dùng 0,0027);
  B commit + push `p82-b1`, `p82-k1`, `p82-k3` (K3 ≤ 0,20 USD — chưa dùng); C commit + push `p82-r2` (R2 ≤ 0,06 USD).
- Trần 8.2: 0,5 USD (spec D5). Luật kỹ thuật giữ: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra (~0,000133 USD / câu context 5; ~0,000204 context 10; luna xếp 10 đoạn ~0,00029 / lần).

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
| `data/phase_8_2/b1/` | kết quả chạy B1 (+ `rebase_2610/` B41: T1, T2 offline) | — |
| `data/phase_8_2/{k1,r2,r4}/` | K1 (tầng tìm + latency), R2 (`r2_oos_dev.jsonl` bước 1), R4 (cờ số theo câu) — mỗi harness từ chối ghi đè | — |
| `data/cai_tien_tung_khau_2026-10-26/` | B42 `b42_per_case.jsonl` (`79e4ba43b38e`), C36 `phan_loai_loi_C/{cases,labels}.jsonl`, script `tools/` | — |
| `data/ra_soat_kho_2026-10-25/` | rà kho C32: `danh_sach.md` 139 mục | — |
| `data/ra_soat_code_2026-10-25/citation_v2/` | lỗi citation tính lại theo validator mới, 14 lượt + `summary.json` (3c) | — |
| `data/ra_soat_code_2026-10-25/tools/` (gồm `dot3/`: D1, D4, D7, D8, D9 + mốc `t1_base.jsonl`, `3b_base.json`), `data/ra_soat_code/` | script + ghi chú rà / sửa code của C / B | — |
| `.githooks/overlap_scan.py` (tracked, không chứa dữ liệu; thay `data/tools/overlap_scan.py`) | quét trùng Golden / kho 40 ký tự — **hook pre-commit tự chạy** trên dòng thêm mới (W16); quét cả file: `uv run python .githooks/overlap_scan.py <file>` | — |
| `gửi chatgpt/2026-10-25/tìm thông tin/cai_tien_tung_khau_2026_10_25.md` | yêu cầu nghiên cứu đợt cải tiến (10 câu) | — |
| `gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md` | kết quả ChatGPT (C1–C6, D1–D4, ma trận ưu tiên, giao thức đo) | `601b49a025ac` |
| `data/cai_tien_tung_khau_2026-10-26/tools/{counts,cover}.py` | script đếm của B40 (đa dạng nguồn, đoạn bảng, cỡ mẫu theo loại câu) | — |
| `data/reports_artifacts_private_2026-10-26/` | 8 file gỡ khỏi `reports/artifacts/` 26/10 (sha bằng bản trong git `421c302`) | — |
| `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json, backup_b12_2026-10-26/}` | quy tắc điều kiện chunker (runtime đọc ở đây) + 55 chuỗi mẫu test chunker + sao lưu B-12 | conditions `b84a0a637bfc` |
| `data/tools/huegov_converters/` | 2 converter HueGov gỡ khỏi `backend/scripts/` (B-13) | — |

## Việc đang mở

### Luật chung khi sửa code (User 18:3x, 19:4x, 20:0x 25/10 — đợt 3 đã xong: `TONG_HOP.md` rà code; giữ mục này làm mẫu cổng ổn định)

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê
  file, không `--env-file` trừ khi mục ghi; report `sua_<gói>_implementation.md`; review chéo (người kia); plan có tiêu chí ghi trước ⇒ session khác
  review **trước** khi A duyệt sha (§9.1). Dừng khi: đường thật đổi ngoài dự kiến; phải đụng file người kia đang khai báo; vượt tiền.
- **Cổng ổn định sau mỗi gói:** (1) test các file chạm, lỗi cũ C-17 ghi rõ; (2) chạy thật `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env
  uvicorn api.app:app --port 8011`: `/` 200, `/health` 5 / 5 ready, 1 câu trong kho (200, marker = `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết,
  không Golden, body `{"query": …}`; log sạch; tắt server; (3) chạm tìm kiếm / chia đoạn: T1 giống byte, sha đoạn giống hệt; (4) 4 chỗ báo cáo nếu
  hành vi đổi; (5) quét trùng Golden / kho: hook pre-commit tự chạy (`.githooks/overlap_scan.py`, W16) — quét cả file người khác viết trước khi stage: `uv run python .githooks/overlap_scan.py <file>`; A commit + push.
- Test cần key OpenAI (không chạy mặc định): `test_api_chat.py` (C-17 đã sửa ở đợt 3: 3 test dừng trước generator chạy không key), `test_openai_full_corpus_generator.py`,
  `test_phase6_live_smoke.py`. Test thiếu model `tests/test_startup_model_missing.py`: auto mode chặn ⇒ User chạy `!` ở terminal session cần.

### Phase 8.2 Bước 2 — đợt cải tiến từng khâu (spec §10, bản `cd910c4c4169`)

**Mục việc của B phiên sau** (chỉ làm sau khi A hỏi lại quyền User + nhắn "làm đi"; thứ tự: B53 trước, B54 sau — handoff thắng STATUS_B nếu lệch):
- **B53 — review report R2 của C (0 USD).** Đọc `git show origin/p82-r2:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_implementation.md`, code
  `git diff 811d25d..origin/p82-r2`, dữ liệu `data/phase_8_2/r2/`; đối chiếu plan R2 sha `b70ea775efb2` (tiêu chí ghi trước) theo `risk-gated-agent-review`;
  tự kiểm sàn OOS (câu bị trả lời, chỉ số câu) + tiền từ usage log. **Không** đọc từng câu test / câu kín. Đầu ra: file review ở **working tree chung**
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_review.md` (A commit trên `main`; B không commit). Xong nhắn A.
- **B54 — chạy K3 (paid, cần quyền mới).** Plan `phase_8_2_k3_plan.md` sha `0a6370204c7d` (`sha256sum` trước khi chạy; dòng 3 ghi "bản nháp chờ C review" là
  cũ — plan **đã duyệt**, không sửa để giữ sha). Nhánh `p82-k3` từ `811d25d`, worktree `/tmp/b_k3` (chưa tồn tại; các `/tmp/b_*` khác không rõ chủ — không đụng);
  harness: `k1.py` chỉ có trên `p82-k1` ⇒ lấy bằng `git show p82-k1:backend/experiments/phase_8_2/k1.py` nếu dùng lại; report K1 cũng trên `p82-k1`.
  **Trần (A chốt khi giao):** tổng **0,20 USD**; con: tầng tìm luna **0,08** (plan ước 0,057 sát trần 0,06 — A nâng, tổng không đổi), lượt sinh **0,12**;
  pilot 10 câu trước, vượt ước pilot > 50 % ⇒ dừng báo A. Không làm: merge `main`, ghi Qdrant, sửa plan, đổi tiêu chí. Dừng: theo plan §6 + khi phải đụng file
  người khác khai báo. Lưu ý: rerank luna ước +4–8 s / câu ⇒ p95 gần chắc vượt mức theo dõi 5 s (không phải sàn — ghi số, A trình User). Đầu ra: report
  `phase_8_2_k3_implementation.md` trên nhánh (B commit + push `p82-k3`) ⇒ C review.
- **C46 — plan R1 (`none`, luật (a); 0 USD).** File `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md` ở working tree chung (không commit);
  mốc so = B1 `811d25d`; đầu file mục "Căn cứ để review" (WORKFLOW §9.1); tiêu chí theo spec §10.2 (a) + §10 R1 (USD ≤ 0,95× **hoặc** `output_tokens`
  ≤ 0,9×, mặt còn lại không tệ hơn) + sàn OOS; cỡ mẫu + nhiễu A/A ghi trước (W23: đếm trên đúng mốc). Không chạy paid. Xong ⇒ báo sha ⇒ B review khi rảnh
  (sau B53, xen lúc chờ luna). Sau đó C review report K3.
- **B55 — review plan R1 (0 USD).** Chỉ dựa trên mục "Căn cứ để review" của plan (sha `0a702b4ac1e4`; WORKFLOW §9.1: không đọc STATUS_C / tin của C),
  được chạy lệnh chỉ đọc / tính lại mốc. Làm xen lúc chờ luna của K3. Đầu ra `phase_8_2_r1_plan_review.md` ở working tree chung (A commit). A trả lời Q1–Q3
  của plan: Q1 giữ mức tụt chặt hơn (Accuracy, từ chối nhầm, citation — sát "lỗi tệ nhất" A đề xuất 27/10), B đánh giá có hợp lý không; Q2 quyền như dòng
  trên; Q3 chạy sau pilot K3. Đưa R1 vào chatbot phải sửa `settings_loader.py` + hợp đồng Phase 6 ⇒ **trình User** dù luật (a) cho A tự đưa.
- **C47 xong** (đối chiếu yêu cầu ChatGPT 27/10 với code: 1 sai, 2 hiểu lầm, 4 thiếu — A đã sửa). Harness R1 viết sẵn ở `/tmp/c_r1` (`p82-r1` cục bộ,
  chưa commit, 0 USD), chờ B55.
- **C48 — đo hiện trạng "số trong câu trả lời có nằm trong đoạn được trích không" (0 USD, dữ liệu B1 dev đã có).** Đo tần suất lỗi "nói chắc sai" (A đề
  xuất là lỗi tệ nhất). Đầu ra private `data/cai_tien_tung_khau_2026-10-26/c48/` + report ngắn `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md`
  (chỉ số đếm). Không phải biến thể ⇒ không cần plan. K3 xong ⇒ C ưu tiên review K3.
  **Xong 09:11 27/10/2026:** B1 dev 68 câu có số ⇒ 0 câu sai số thấy được (4 cờ = 6 / 6 phép tính đúng; mẫu 10 / 10 đúng); G2.1a từng có 2 lỗi thật ⇒ dao động giữa lượt.
- **K3 report** `origin/p82-k3` `80e7329` (B): lỗi luna 1 / 40, CI [0,06 %; 13,2 %]; theo dõi 39 câu: top10 gold 21 → 30, MRR 0,44 → 0,71; rerank p95 8,6 s; USD / câu
  đầu–cuối ≈ 4×. **C49** review. **B56** plan K3b (pool 30 → luna trả 10 số; cân nhắc `none` cho lần rerank; luật tất định cho đầu ra sai, ghi trước) — 0 USD,
  chạy chỉ sau review + A duyệt; vào chatbot chậm / tốn hơn ⇒ trình User.
- Ước tổng 8.2 (A, để so trần 0,5): đã dùng 0,0396 + K3 0,20 + R1 ~0,034 + ghép ~0,04 + dự phòng pilot ⇒ **≈ 0,31–0,35 USD** (con số "0,41" trong plan K3 §7 tính cả
  R2 0,06 + R3 0,04 trước khi hai việc đó dừng / NOT RUN).

| # | Plan (`report_agent/2026-10-25_phase_8_2_ap_dung/`) | sha duyệt | Trạng thái | Việc phiên sau |
|---|---|---|---|---|
| K1 | `phase_8_2_k1_plan.md` | `b8f1597f6a0f` | **kém hơn** (câu 154 mất đoạn đúng; 2 / 37 / 1); `p82-k1`; C42 ready | — (hồ sơ) |
| K3 | `phase_8_2_k3_plan.md` | `0a6370204c7d` | **DỪNG 09:05 27/10/2026 — kém hơn (phạm sàn: lỗi đầu ra luna 1 / 40, câu 173, thứ tự thiếu 1 đoạn)**; pilot rerank p50 5,7 s / p95 8,2 s; 0,0251 USD | **đóng 09:13 27/10/2026** — C49 review ready (`phase_8_2_k3_review.md`, 0 / 0 / 3 minor); hồ sơ `p82-k3` `80e7329`; số theo dõi 9 thắng / 0 thua trên 39 (câu 173 không đo được), một lượt, dev đã thấy |
| R2 | `phase_8_2_r2_plan.md` | `b70ea775efb2` | **kém hơn — đóng** (OOS câu 160); `p82-r2` `aec9ab8`; 0,0027 USD; B53 review ready (`phase_8_2_r2_review.md` `11368435edbd`); A đóng 27/10: m-1 giữ (mô tả chung, 0 trùng); m-2 ghi hồ sơ: câu 115 (P1 phạm dạng không `[n]`) R2 từ chối nhưng B1 cũng từ chối ⇒ chưa tách được tác dụng E1b | — (hồ sơ) |
| R3 | `phase_8_2_r3_plan.md` | — | **NOT RUN** (C45: trần 6 câu) | — (hồ sơ) |
| K3b | `phase_8_2_k3b_plan.md` | `57dad7150322` | xong 10:01 27/10/2026, `origin/p82-k3b` `806e8ad`: **K3b-n kém hơn** (lỗi kỹ thuật: chữ thừa sau JSON dù strict); **K3b-m tầng tìm TỐT HƠN (tạm)**: dev 9 / 0 ổn định L1 + L2 (CI [+0,10; +0,35]), 22 → 31 / 40; test 3 / 3, 0 mất; sai hợp đồng 0 / 95; rerank p50 5,0 / p95 7,0 s; USD / câu ≈ 0,00079 (3,9×); tiền K3b ≈ 0,068 (log 0,0592 + ước 0,0087, cận trên ≈ 0,0142) | C52 review **ready** (10:05 27/10/2026, `phase_8_2_k3b_review.md`, 0 / 0 / 3 minor; tự tính lại từ payload Qdrant: 22 → 31 L1 = L2); m-1: cận trên tiền l1_rest n theo 2048 token ra ≈ 0,044 ⇒ K3b tệ nhất ≈ 0,103 (sát trần — số thật chỉ có ở usage OpenAI 09:30:04–09:30:53); **B59** phụ lục lượt sinh (bản 1 `84d4aaf0ad04` — C53 10:10 27/10/2026 changes_requested 0 / 1 / 3: M-1 T6 chồng T2 vì `chat.py` trả 500 cho mọi lỗi citation; A chọn 120 lên sàn, 429 / timeout = lỗi kỹ thuật; trần 0,13, 176 câu) ⇒ bản 2 **`92a8a7eb4177` A duyệt 10:15 27/10/2026** (sha tính từ file; C53 vòng 2 ready; m-4 sửa trong harness: tách câu W2 giữ `[n]` có khoảng trắng + IGNORECASE) ⇒ **DỪNG ở pilot 10:20 27/10/2026: sàn T8 "120 vẫn từ chối" phạm** — K3b-m trả lời 120 **khớp đáp án tham chiếu**; fact có trong context nhưng nhãn đoạn đúng chỉ đánh dấu lần xuất hiện đầu (B kiểm) ⇒ tiền đề "0 fact" của sàn (A chọn, không kiểm) sai; 0,0048 USD; e2e p50 ≈ 5,4 s / max 10,2 s (9 câu). Kết luận lượt giữ theo luật; sửa nhãn / mở lượt mới = **User quyết**. **B61** quét nhãn 55 câu xong 10:23 27/10/2026 (`data/phase_8_2/k3b/gold_scan/`): lặp nguyên văn 1 / 55; 120 = fact diễn đạt lại ở chỗ khác; tầng tìm 22 → 31 **đứng vững** cả cách đếm loose (24 → 33 / 34, 9 / 0); B1 từ chối 120 đúng với context của nó (lỗi xếp hạng) ⇒ **User chọn (1) 10:26 27/10/2026:** phụ lục bản 3 chỉ đưa 120 về theo dõi (ghi "đổi sau khi thấy số"), lượt mới chạy lại từ đầu, không sửa nhãn ⇒ bản 3 **`2a3b22b38ab6` A duyệt 10:33 27/10/2026** (sha tính từ file; C vòng 3 ready + xác nhận độc lập context 120) ⇒ v3 chạy xong dev 10:45 27/10/2026: **kém hơn theo luật** (T3: 5 câu Completeness tụt > 4; không chạy test). Chỉ báo: Completeness +0,216 [+0,023; +0,443], Accuracy +0,250 [+0,068; +0,466], Relevance +0,227; sàn OOS / 500 / từ chối mới đạt; 168 không phải dạng vòng; e2e p50 6,5 / p95 9,1 s (B1 sinh 1,8 / 3,3), 3,8× USD; tiền phụ lục 0,0749 ⇒ report `a6f609c` ⇒ C54 review ready 10:52 27/10/2026 (0 / 0 / 2 minor: 5 câu tụt = 1 rõ (112), 3 thiếu chi tiết nhỏ, 1 nhiều khả năng nhiễu judge (66); A/A biến thể giá trị thấp — câu thật là luật nhận cho biến thể đổi context, áp cho lần sau) ⇒ **K3b-m đóng: kém hơn theo luật** ⇒ trình User hướng tiếp ⇒ + judge (ước ~0,11) ⇒ C review ⇒ A duyệt ⇒ chạy ⇒ trình User |
| R4 | (implementation `phase_8_2_r4_implementation.md`) | — | xong `2c7ecfd`; B47 ready | dùng làm chỉ số theo dõi |
| R1 | `phase_8_2_r1_plan.md` | **`8e76e77e0448`** (A duyệt 09:18 27/10/2026, sha tính từ file; bản 1 `0a702b4ac1e4` changes_requested) | **DỪNG ở pilot 09:25 27/10/2026 — kém hơn (phạm sàn: câu 168 bị trả lời vòng + câu "nguồn không nêu…" không citation; cùng dạng R2 / 160)**; 172 / 173 có `[n]`; 0,0049 USD; `origin/p82-r1` `63a472f` | **đóng 09:33 27/10/2026** — B58 review ready (`phase_8_2_r1_review.md`, 0 / 0 / 1 minor: tách câu trong `r1.py` bỏ sót `[n]` sau dấu chấm — C51 đã xử lý) |
| K2, E2 | — | — | NOT RUN (spec §10.3) | — |

Đầu vào: `report_agent/2026-10-26_cai_tien_tung_khau/` (`phan_loai_loi_{B,C}.md`, `de_xuat_khau_{tim_B,tra_loi_C}.md`, review). Nhánh thí nghiệm **không merge**
`main`; chỉ biến thể thắng mới đưa vào runtime theo spec §10.4.
