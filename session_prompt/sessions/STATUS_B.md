# STATUS B — PHIÊN 27/10 (B53 bắt đầu 08:48 27/10/2026; terminal `hue-rag-31`; A = `hue-rag-5f`, C = `hue-rag-5b`)

## Phiên 27/10 — đang làm

- A giao B53 → B54 (User duyệt quyền 08:47 27/10: B commit + push `p82-k3`, K3 ≤ 0,20 USD = tìm 0,08 / sinh 0,12).
- **B53 xong (08:52 27/10/2026):** review R2 = **ready_for_user_confirmation** (0 / 0 / 2 minor) — file `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_review.md`
  (sha `11368435edbd`, working tree chung, chờ A commit). Mọi số report R2 khớp tính lại; m-1 mục "Cho bạn" mô tả câu hỏi cụ thể hơn §4; m-2 thiếu dòng câu 115.
  Worktree `/tmp/b53_r2` + script `/tmp/b53/` đã gỡ.
- **B54 xong (09:09 27/10/2026) — K3 kém hơn (phạm sàn):** lỗi đầu ra luna 1 / 40 (câu dev 173: 29 / 30 số, thiếu đoạn 5) ⇒ dừng ở L1 theo plan §6.3; NOT RUN L2 / test / sinh.
  Theo dõi (không kết luận) 39 câu hợp lệ: thắng 9 / 9 câu trần, mất 0; rerank p50 5,6 s / p95 8,6 s; ≈ 4× USD / câu. Nhánh `p82-k3`
  (`ff93703` harness, `80e7329` report) **đã push**; worktree `/tmp/b_k3` + symlink đã gỡ. Dữ liệu `data/phase_8_2/k3/` (+ `tools/k3_watch.py`). ⇒ chờ C review.
- **B55 xong (09:04):** review plan R1 = changes_requested (0 / 1 / 3), file `phase_8_2_r1_plan_review.md` (A commit `4e0f3ec`). Chờ C sửa ⇒ B kiểm phần sửa.
  Script tạm `/tmp/b55/` đã xóa.
- **B56 xong (09:16 27/10/2026):** plan K3b `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_plan.md` sha **`4f92e478cb65`** (working tree chung, 0 USD).
  Hai nhánh K3b-n (10 số + reasoning none, chạy trước) / K3b-m (10 số, mặc định; bỏ nếu n đạt 9/0 + luật giữ); hợp đồng đầu ra tất định + trần
  sai hợp đồng ≤ 4/95, bù RRF ≤ 2/95; quyết `context_gold_all`, Holm họ 4; trần đề xuất 0,10 USD. ⇒ chờ C review.
- **B57 xong (09:18 27/10/2026):** kiểm phần sửa plan R1 bản 2 (sha `8e76e77e0448`) ⇒ **ready** (M-1, m-1..m-3 đóng; không đổi tiêu chí / sàn / trần). Mục "Vòng 2"
  thêm vào `phase_8_2_r1_plan_review.md` (sha `fc971d9237c6`, A commit).
- **B58 (09:25 27/10/2026):** plan K3b **bản 2** sha `57dad7150322` (sửa C50 m-1..m-4 + 2 quyết định A; chờ C kiểm phần sửa ⇒ A duyệt). Harness
  `/tmp/b_k3b` (nhánh `p82-k3b` cục bộ từ `80e7329`, không upstream, **chưa commit**): `k3b.py` (sha `255d48174723`) + `tests/test_k3b_contract.py`
  (4 passed). Bước 0 miễn phí đã chạy: `data/phase_8_2/k3b/base_dev.jsonl`, M2' 40/40 khớp K3, 0 trường lệch. 0 USD.
  **File khai báo sửa:** `k3b.py`, `test_k3b_contract.py` (worktree), plan K3b (working tree chung).
- **B58b review R1 xong (09:32 27/10/2026):** ready (0 / 0 / 1 minor: `uncited_sentences` không tách câu khi `[n]` sau dấu chấm ⇒ đếm 0 ở 168 / R2 160).
  File `phase_8_2_r1_review.md` sha `f55c572f9b6f` (A commit). Script `/tmp/b58/` đã xóa.
- **B59 K3b (đang, dừng chờ A từ 09:3x):** plan duyệt `57dad7150322` (`765f45a`); harness `7c0467d` trên `p82-k3b` (chưa push). M1 ✓, M2' ✓. Pilot n:
  0 lỗi, 0 sai hợp đồng, 0,0035036 USD, rerank p50 1,76 / p95 2,09 s. **L1 rest n: luna viết chữ sau JSON ⇒ SDK ném pydantic ValidationError ⇒
  lỗi kỹ thuật (plan §2 loại 1) ⇒ nhánh n kém hơn; harness chỉ bắt OpenAIError + ghi file ở cuối ⇒ mất dòng + usage của lượt** (ước ~21 lần ≈ 0,0074,
  ≤ 0,0105 USD). Đề xuất A: sửa bắt lỗi + ghi từng dòng rồi chạy nhánh m. Worktree `/tmp/b_k3b` còn (+ symlink).
- **B59 xong (10:00 27/10/2026):** report K3b `phase_8_2_k3b_implementation.md` trên `origin/p82-k3b` `806e8ad` (đã push; harness `7c0467d` + sửa `f4d3225`).
  **n kém hơn** (lỗi kỹ thuật: chữ thừa sau JSON strict, reasoning none); **m tầng tìm tốt hơn (tạm)**: dev 9 / 0 ổn định L1 + L2, p Holm ≈ 0,
  test 3 / 0, sai hợp đồng 0 / 95; giá rerank p50 5,0 / p95 7,0 s, ≈ 3,9× USD / câu; lượt sinh NOT RUN (cần trần riêng ≈ 0,11). Trần con m
  A dời lên 0,065 (B nhận 09:51:39). Worktree `/tmp/b_k3b` + symlink đã gỡ. ⇒ chờ C review.
- **B60 xong (10:05 27/10/2026; A gọi B59):** phụ lục plan `phase_8_2_k3b_m_answer_plan.md` sha **`84d4aaf0ad04`** (working tree chung, 0 USD). Tiêu chí
  = K3 plan §4 dòng 85–92, 98 nguyên văn; phát lại thứ tự L1 / test cho 55 câu, gọi mới 121; ghi từng dòng; ước ≈ 0,107, trần đề xuất 0,13;
  W1 ghi trước trần lợi câu trả lời = 6 câu dev chính. ⇒ chờ review (C sau C52).
- **B61 (10:13 27/10/2026):** phụ lục plan **bản 2** sha `92a8a7eb4177` (C53 M-1 T2 = error hoặc citation_error, T6 theo dõi; m-1; m-2 120 thành sàn; m-3 429 /
  timeout; W2 regex bản 1 nuốt `[n]` — B bắt khi kiểm harness, đã sửa). Chờ C kiểm phần sửa ⇒ A duyệt. Harness `k3b_answer.py` (sha `c92d572af51e`)
  + `tests/test_k3b_answer_text.py` ở `/tmp/b_k3b`, **chưa commit**; kiểm 0 USD: phát lại 55 / 55 khớp top-10, 0 sai hợp đồng; pilot 3 phát lại / 7
  gọi mới; 6 test passed. **File khai báo sửa:** `k3b_answer.py`, `test_k3b_answer_text.py` (worktree), plan phụ lục (working tree chung).
- **B62 (10:19 27/10/2026):** A duyệt phụ lục bản 2 `92a8a7eb4177` (`c313d29`); harness `9ff6ebb` (m-4 sửa, 7 test passed; chưa push). Pilot dev 10:
  **dừng ở sàn T8: câu 120 bị trả lời** ⇒ theo luật: K3b-m kém hơn. Nhưng câu trả lời khớp đáp án tham chiếu và cả hai fact có trong context
  (chunk #11, #7); nhãn đoạn đúng chỉ đánh dấu lần xuất hiện đầu ⇒ giả định "120 có 0 fact" sai. Đã báo A, chờ quyết. Tiền pilot 0,0047854 USD.
  Tiền B phiên: log 0,0891159 + ước ≈ 0,0074 (≤ 0,0105) ⇒ **≈ 0,0965 (≤ 0,0996) USD**.
- **B63 xong (10:23 27/10/2026; A gọi B61):** quét nhãn đoạn đúng 55 câu (`data/phase_8_2/k3b/gold_scan/`: `scan.py`, `per_case.jsonl`, `summary.json`). Nguyên văn:
  chỉ câu 17 có quote lặp (file khác), không đổi số nào. Lặp gần (heuristic, có báo nhầm): B1 22 → 24, K3b-m 31 → 33 / 34; vẫn 9 thắng / 0 thua,
  test 0 mất. 120 ở B1: context không có fact ⇒ B1 từ chối đúng với context; lỗi là xếp hạng (fact ở pool 30), không phải khâu sinh.
  Tiền pilot answer K3b-m (log): **0,0047854 USD**.
- **B64–B65 xong (10:47 27/10/2026):** phụ lục bản 3 `2a3b22b38ab6` duyệt (`c46019f`); harness `6b4114e`; chạy v3 dev 120 + judge mù 215 câu (5 sub-agent, Opus 5.5).
  **K3b-m answer = kém hơn theo luật: T3 Completeness thua 5 > 4** (26, 66, 93, 134 −1; 112 −2); test NOT RUN. Sàn đạt hết; chỉ báo: Completeness
  +0,22 [+0,02; +0,44], Accuracy +0,25, từ chối nhầm 7 → 2; C51 0 / 0; 168 / 120 trả lời đúng, không "vòng". e2e p50 6,5 / p95 9,1 s (đồng thời 4), 3,8× USD.
  Report `phase_8_2_k3b_m_answer_implementation.md` trên `origin/p82-k3b` `a6f609c` (đã push). Worktree `/tmp/b_k3b` đã gỡ. ⇒ chờ C review.
- **B66 xong (10:49 27/10/2026; A gọi B62):** `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md` bản 8 (working tree chung, chưa commit): dòng cập nhật, Tóm tắt, checklist
  (luna + dòng mới "thước đoạn đúng"), §4 mục 27/10, §5, §6, Phụ lục. Chatbot ghi "chưa đưa vào". ⇒ A review + commit.
- **Còn nợ (sửa ở commit tiếp trên `p82-k3b`, chờ A đồng ý):** (a) report K3b §4.2: ước lượt n mất usage 0,0074 → ≈ 0,0087, cận trên 0,0105 → ≈ 0,0142; (b) report K3b-m answer dòng 27 ghi "Ba trong 5 câu" có 7–9 / 10 đoạn trùng — đúng là **4 / 5**
  (9, 8, 7, 7; câu 93 là 5 / 10). A đã sửa ở `BAO_CAO_TIM_KIEM.md` (`2936165`). Bài học: số đếm trong lời thường phải đếm lại từ bảng, không gõ tay.
- **B67 xong (11:19 27/10/2026; A gọi B63):** thử rebase `p82-b1` `811d25d` lên `main` `e952fa3` (nhánh tạm, không push): **không xung đột**. range-diff: nội dung
  B1 giữ nguyên (chỉ bớt `phase_8_2/__init__.py` rỗng, đã có trên main). Pytest không key: 6 file (retrieval, phase6_settings, context, eval, citations,
  r4) **68 passed / 1 failed** — failed = `test_openai_api_key_exists_without_leaking` cần key, **trên main cũng failed y hệt** (đối chứng); test này
  chưa có trong danh sách "cần key" của Project_Status §8. **T1 giống từng byte** `cefb2d1ad609`. Nhánh tạm + worktree `/tmp/b_b1chk` đã xóa; `p82-b1` vẫn `811d25d`.
- **B68 xong (11:22 27/10/2026; A gọi B64):** review tài liệu đóng đợt của A (tin nhắn, không file): changes_requested — F1 cận trên tiền sai ở 4 chỗ
  (TONG_HOP:50/70/71, HISTORY:15, nhật ký:4; đúng ≈ 0,014 / 0,175 / 0,214 / +0,003); F2 thiếu "gọi đồng thời 4"; F3 thiếu "(tạm)"; F4 chỉ báo. Số khác khớp.
- **B69 (đang làm, từ 11:27 27/10/2026):** trả nợ trên `p82-k3b` (A đồng ý): report K3b §4.2 (ước 0,0087 / cận trên 0,0142) + report K3b-m answer "Ba trong 5" → 4.
  **File khai báo sửa:** 2 report trên nhánh, worktree `/tmp/b_k3b`.
- **File đang khai báo sửa: không** (ngoài B69). Tiền paid phiên 27/10 (log): K3 0,0251129 + K3b 0,0592176 + phụ lục 0,0749297 = **0,1592602 USD**,
  + ước lượt n mất usage **≈ 0,0087 (cận trên ≈ 0,0142)** — tính lại 27/10 từ token vào thật của đúng 30 câu (`m_l1_rest`; số cũ 0,0074 / 0,0105 lấy
  giá / lần của pilot nên thấp) ⇒ **≈ 0,168 (≤ 0,174) USD**.
- **Sự cố (27/10, cho vòng cải tiến):** harness paid chỉ bắt lỗi của provider (`OpenAIError`), không bắt lỗi parse của SDK; và chỉ ghi kết quả
  ở cuối lượt ⇒ một exception làm mất usage đã trả tiền. Bài học: harness gọi API trả phí ghi từng dòng ngay (append) và bắt mọi lỗi của một lần gọi
  thành dòng lỗi; `responses.parse` có thể ném `pydantic.ValidationError` (chữ thừa sau JSON) ở `reasoning none`. Không server, không GPU, không lượt nào đang chạy.
- **Worktree của B: không còn.** Đã gỡ `/tmp/b_p82b1`, `/tmp/b_p82b1_old`, `/tmp/b45_wt`, `/tmp/b_k1` (gỡ symlink trước). File tạm `/tmp/b45*`,
  `/tmp/b47`, `/tmp/k3_before.md` đã xóa.
- Các mục `/tmp/b_*` còn trên máy **không phải của B phiên này**: `b_vong1..4`, `b_moc*`, `b_promo*`, `b_ghep`, `b_b1_final`, `b_low_final`, `b_p5`,
  `b_url`, `b_fake_grade.txt`; tạo 18:27–22:03. B không đụng.
- **Nhánh của B:**
  - `p82-b1` `811d25d` = origin (B1 rebase, A review ready; **merge chỉ sau B0**);
  - `p82-k1` `870a5d5` = origin (K1 kém hơn; nhánh giữ làm hồ sơ, **không merge**).
  - `p82-k3` **chưa tạo**.
- Mọi file B viết trên `main` đã được A commit (tới `087cedd`). Riêng STATUS_B này và dòng B trong `CURRENT_HANDOFF.md`: A commit trong gói kết phiên.
- **Tiền paid phiên tối 26/10: 0 USD.** Không lượt nào gọi `gpt-6-luna`; K1 dừng trước lượt sinh.

## Phiên sau B làm gì đầu tiên

Nguồn sự thật: mục "Mục việc của B phiên sau" trong `CURRENT_HANDOFF.md`. Nếu lệch với file này, handoff thắng. Chỉ làm sau khi A hỏi lại quyền
User và nhắn "làm đi". Thứ tự:

1. **B53 — review report R2 của C** (0 USD).
   - Đọc: `git show origin/p82-r2:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_implementation.md`; `git diff 811d25d..origin/p82-r2`;
     `data/phase_8_2/r2/`.
   - Đối chiếu plan R2 sha `b70ea775efb2`; tự kiểm sàn OOS + tiền từ usage log. Không đọc từng câu test / câu kín.
   - Đầu ra: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_review.md`, ở working tree chung, B không commit.
2. **B54 — chạy K3** (paid, cần quyền mới).
   - Plan `phase_8_2_k3_plan.md` sha **`0a6370204c7d`**: chạy `sha256sum` trước. Dòng 3 ghi "bản nháp chờ C review" là chữ cũ; plan **đã
     duyệt** ⇒ không sửa.
   - Nhánh `p82-k3` từ `811d25d`, worktree `/tmp/b_k3` + symlink `data/`, `knowledge-base-hue/`.
   - Harness `k3.py` theo plan §3. Dùng lại `k1.py` qua `git show p82-k1:backend/experiments/phase_8_2/k1.py`, và `g4_rerank.luna_rank`
     (`max_output_tokens` 2048).
   - **Trần (A chốt):** tổng **0,20 USD**, gồm tầng tìm luna **0,08** và lượt sinh **0,12**. Pilot 10 câu trước; vượt ước pilot > 50 % ⇒
     dừng, báo A. p95 rerank gần chắc vượt mức theo dõi 5 s: đó không phải sàn, ghi số để A trình User.
   - Không: merge `main`, ghi Qdrant, sửa plan, đổi tiêu chí.
   - Đầu ra: `phase_8_2_k3_implementation.md` trên nhánh (B commit + push `p82-k3`) ⇒ C review.
3. Việc khác theo A.

## Việc phiên tối 26/10 (tóm tắt; chi tiết ở file report)

| Việc | Kết quả | File / sha |
|---|---|---|
| B41 rebase B1 lên `main` | ready (A). Xung đột duy nhất: import 1 test. T1 giống byte `cefb2d1ad609`; T2 không gọi model 176 / 176 (+ đối chứng dương) | nhánh `p82-b1` `811d25d`; `phase_8_2_b1_rebase_review.md` |
| B42 phân loại lỗi tầng tìm (40 câu dev) | ready 0/0/0. Context 5 đủ 17 / 40, context 10 đủ 22 / 40; còn thiếu: ngoài pool 30 (11 fact / 8 câu) ≈ xếp sau trong pool (12 fact / 11 câu) | `phan_loai_loi_B.md` (`a5cace6`); private `data/cai_tien_tung_khau_2026-10-26/b42_*` |
| B43 bản nháp khâu tìm cho spec | V1 pool 100 / V2 native k2 / V3 luna; không chạy V4 cap file, V5 G4-B | `de_xuat_khau_tim_B.md` |
| B44 bỏ comment `sys.path` sai | 4 file `experiments/phase_8_1/` (A ghi 3) | commit A |
| B45 review hook quét câu kín | ready, 2 vòng. m-1 câu kín < 40 ký tự ⇒ A thêm `short_questions()` | `hook_sealed_review.md` (`6cb12e6`) |
| B46 plan K1 (bỏ K2) | 2 vòng C41 ⇒ A duyệt `b8f1597f6a0f` | `phase_8_2_k1_plan.md` |
| B47 review R4 (thước số) của C | ready 0/0/2. Context dựng lại khớp sha T2 352 / 352 | `phase_8_2_r4_review.md` |
| **B48 chạy K1** (pool dense 100) | **kém hơn**: mất câu 154 (sàn); 2 / 37 / 1; pool đủ 31 → 37 / 40 nhưng top-10 22 → 23 ⇒ **chỗ nghẽn = xếp hạng**. Latency +8,9 ms (p50 33 → 43, p95 76 → 82). 0 USD | nhánh `p82-k1` `870a5d5`, `phase_8_2_k1_implementation.md`; private `data/phase_8_2/k1/` |
| B49 review plan R2 của C | 2 vòng ⇒ ready (bản `b70ea775efb2`). M-1 ⇒ spec §10.2 "Đo tốc độ theo khâu" (khâu sinh đo bằng `output_tokens`) | `phase_8_2_r2_plan_review.md` |
| Kiểm spec §10 (3 lần) | đạt (`ce8b310`, spec `cd910c4c4169`) | tin nhắn A |
| B50 plan K3 | C44 ready ⇒ **A duyệt `0a6370204c7d`** — chưa chạy (User chọn kết phiên) | `phase_8_2_k3_plan.md` |
| B51 plan R3 | C45 changes_requested (trần thật 6 câu) ⇒ **A: R3 NOT RUN** | `phase_8_2_r3_plan.md` (hồ sơ) |

## Câu hỏi còn treo (cho A / User)

- Kết luận dựa judge (K3 nếu chạy, R2) là **tạm** tới khi B0 xong. B0 (User đọc cặp mù) vẫn chưa làm, và B1 merge cũng chờ B0.
- Pool 100 + luna (trần 14 câu, đổi hai thứ): chỉ làm khi K3 thắng, cần plan riêng (A 22:1x).
- Từ trước (giữ):
  - route API không ghi usage token ⇒ tiền ở cổng ổn định chỉ là ước;
  - dense local mới (`bge-m3`, `Qwen3-Embedding-0.6B`) ngoài danh sách duyệt;
  - mâu thuẫn kho Hải Vân Quan — sửa khi build lại index.

## Đã học / bẫy gặp

- **26/10 tối (mới):**
  - `g1_retrieval run` ghi `data/phase_8_1/g1/<name>.jsonl` **không chặn ghi đè**. `r4_numbers.main()` lúc B review cũng chưa chặn (A đã thêm sau).
    ⇒ harness mới luôn từ chối ghi đè. Khi review, gọi hàm chứ không gọi `main()` nếu `main()` ghi vào file của người khác.
  - Ở `811d25d` (context 10), cột `context5_gold_*` của harness G1 thật ra là context 10 ⇒ không so với file G1 cũ.
  - Latency khâu sinh dao động mạnh: SD chênh theo câu 808 ms ⇒ ngưỡng ±50 ms không đo được với vài chục câu. Dùng `output_tokens` (A/A ±6,6 %
    với n 120). Khâu tìm đo ms được.
  - **Giả định "trần" phải kiểm trên đúng mốc** (C45: 9 câu U lấy ở G2.1a, nhưng ở B1 chỉ 6 câu còn điểm 4) ⇒ trước khi viết cỡ mẫu, đọc điểm
    mốc thật từ `data/phase_8_2/b1/judge/`. `b1.py` chỉ có trên nhánh `p82-b1` ⇒ đọc bằng `git show` hoặc worktree.
  - Ca kiểm thước trùng ca dùng để thiết kế thước ⇒ "đạt" chỉ là đạt trên mẫu đã thấy (B47 m-1).
  - Sha plan đổi khi người viết sửa trong lúc người kiểm đọc (R2 ad9ef9 → aa808a → b70ea7) ⇒ người kiểm ghi sha **ngay lúc đọc xong**, báo A đúng
    bản đã đọc.
  - Script ngoài `backend/` chạy bằng `python <file>` cần `PYTHONPATH=.` (từ `backend/`). Đoạn đúng là dòng tiêu đề `#` thì không bao giờ khớp
    `evidence_parts` (câu 143).
- **Từ 26/10 (giữ):**
  - worktree: `uv run --project /home/minhhieu/hue_rag`; symlink `data/` + `knowledge-base-hue/` gỡ khi xong; push từ working tree chung;
  - auto mode chặn `nbconvert --execute` / `HF_HOME` rỗng ⇒ NOT RUN + lệnh `!`;
  - đối chiếu mô tả hệ thống với code trước khi gửi nghiên cứu ngoài;
  - người review tự tạo mốc độc lập;
  - quét public trên mọi file text tracked.
- **Từ 25/10 (giữ):**
  - mọi Python bằng `uv run`;
  - pytest liệt kê file, không `--deselect`;
  - chạy lệnh paid mới không `--env-file` trước;
  - giờ ghi file lấy bằng `date`;
  - đọc code trước khi khẳng định;
  - kiểm citation phải bắt cả `[n]` lẫn `[Nguồn n]`;
  - HNSW phụ thuộc `limit`;
  - pilot 10 câu cho lượt paid;
  - chấm baseline cùng lượt mù.
  - **B đã thấy khóa X / Y của B0 ⇒ B không làm người tóm nhãn B0.**
