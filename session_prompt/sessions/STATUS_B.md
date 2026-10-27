# STATUS B — PHIÊN 27/10 (B53 bắt đầu 08:48 27/10/2026; terminal `hue-rag-31`; A = `hue-rag-5f`, C = `hue-rag-5b`)

## Phiên 27/10 — đang làm

- A giao B53 → B54 (User duyệt quyền 08:47 27/10: B commit + push `p82-k3`, K3 ≤ 0,20 USD = tìm 0,08 / sinh 0,12).
- **B53 xong (08:52 27/10/2026):** review R2 = **ready_for_user_confirmation** (0 / 0 / 2 minor) — file `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_review.md`
  (sha `11368435edbd`, working tree chung, chờ A commit). Mọi số report R2 khớp tính lại; m-1 mục "Cho bạn" mô tả câu hỏi cụ thể hơn §4; m-2 thiếu dòng câu 115.
  Worktree `/tmp/b53_r2` + script `/tmp/b53/` đã gỡ.
- **B54 (đang làm, từ 08:55 27/10/2026):** chạy K3, plan sha `0a6370204c7d` (kiểm 08:5x). Nhánh `p82-k3` từ `811d25d`, worktree `/tmp/b_k3` (+ symlink
  `data/`, `knowledge-base-hue/` — gỡ khi xong). **File khai báo sửa:** `backend/experiments/phase_8_2/k3.py` (mới, trên nhánh),
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_implementation.md` (trên nhánh), dữ liệu `data/phase_8_2/k3/`. Trần (handoff, A chốt):
  0,20 USD = tìm 0,08 + sinh 0,12 (plan §5 ghi 0,06 / 0,14 — handoff thắng).
- Tiền paid phiên 27/10: 0 USD.

---

# (phiên trước) STATUS B — KẾT PHIÊN TỐI 2026-10-26 22:2x +0700 (mở 20:29; terminal `hue-rag-23`; A = `hue-rag-2d`, C = `hue-rag-b5`)

Agent: Claude Opus 5.5 · Vai: thực thi · User 26/10: B làm việc trực tiếp với A; việc A giao = User nói "làm đi".
Bản đầy đủ trước khi rút gọn:
- phiên tối 26/10, từng bước B41–B51: `git show 087cedd:session_prompt/sessions/STATUS_B.md`;
- phiên chiều 26/10 + 25/10: `git show 7b662c9:session_prompt/sessions/STATUS_B.md`.

## Trạng thái kết phiên

- **File đang khai báo sửa: không.** Không server, không GPU, không lượt nào đang chạy.
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
