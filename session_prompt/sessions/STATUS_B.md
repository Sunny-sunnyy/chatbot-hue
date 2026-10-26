# STATUS B — PHIÊN TỐI 2026-10-26 (mở 20:29 +0700; terminal `hue-rag-23`; A = `hue-rag-2d`, C = `hue-rag-b5`)

Agent: Claude Opus 5.5 · Vai: thực thi · User 26/10: B làm việc trực tiếp với A; việc A giao = User nói "làm đi".
Bản đầy đủ trước khi rút gọn (lịch sử phiên chiều + tối 25/10, bẫy cũ chi tiết): `git show 7b662c9:session_prompt/sessions/STATUS_B.md`.

## Phiên tối 26/10 — đang làm (A giao 20:35, `CURRENT_HANDOFF.md` mục "Việc giao phiên tối 26/10")
- **B41** (B1 8.2 rebase lên `main`, 0 USD): worktree `/tmp/b_p82b1`, nhánh `p82-b1`. Quyền: B commit + `push --force-with-lease` nhánh `p82-b1`
  (User 20:3x); không merge `main`. T2 cần gọi `gpt-6-luna` ⇒ dừng, báo A.
- **B41 XONG 20:5x — chờ A review.** `p82-b1` `f23d396` ⇒ rebase `e1e16b3` + report `811d25d` (push `--force-with-lease=p82-b1:f23d396`). Xung đột duy nhất:
  import `test_full_corpus_retrieval.py` (giữ import trần). Bỏ comment sai `b1.py:23`. Test 4 file: 41 p / 1 f / 1 e (main 40 p, cùng f / e cần key).
  T1 sha `cefb2d1ad609` 158 dòng; T2 offline (`data/phase_8_2/b1/rebase_2610/t2_offline.py`) 176 / 176 mọi trường, đối chứng `main` ctx5 bắt khác;
  T5 đạt; T3 / T4 NOT RUN (cần model). Worktree `/tmp/b_p82b1`, `/tmp/b_p82b1_old` đã gỡ (symlink gỡ trước). 0 USD.
- **B41 review: ready** (A, `phase_8_2_b1_rebase_review.md`, `2d56193`); T2 có phí: A quyết không chạy — bằng chứng model ở cổng ổn định khi merge (sau B0).
- **B42 XONG 20:54 — chờ review.** Report `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md` (untracked, A commit). Script + kết quả private
  `data/cai_tien_tung_khau_2026-10-26/tools/b42_{retrieval_errors,summary}.py`, `b42_{per_case.jsonl,summary.json}`. Kiểm chéo G1 `runtime.jsonl` 40 / 40.
  0 USD. B42 review ready 0/0/0 (A, `a7b61bb`).
- **B43 XONG 21:01 — chờ A** (A giao 20:57; khai báo: chỉ `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tim_B.md` mới). Bản nháp khâu tìm cho spec
  đợt cải tiến: V1 pool dense 100 / V2 native p30 k=2 (xác nhận test) / V3 luna pool 30; không chạy V4 cap file, V5 G4-B. 0 USD, không chạy tìm kiếm mới.
  **File đang khai báo sửa: không.**
- **B44** (A giao 21:0x, 0 USD, mức thấp): bỏ comment sai "import này cũng đưa gốc repo + backend/ vào sys.path". **Khai báo (main, working tree chung):**
  `backend/experiments/phase_8_1/{g1_retrieval,g2_generate,g3_chunking,g4_rerank}.py` (4 file — A ghi 3; `g3_chunking.py` cũng có). Không commit.
  **XONG 21:0x — chờ A commit:** 4 dòng, chỉ bỏ comment; `py_compile` 4 file đạt; `git diff --check` sạch. Hết file khai báo.
- **B45** (A giao 21:17, review hook quét câu kín, 0 USD): khai báo `report_agent/2026-10-26_cai_tien_tung_khau/hook_sealed_review.md` (mới). Script tạm `/tmp/b45_*`,
  worktree thử `/tmp/b45_wt` — gỡ khi xong. Giữ mù: không in / đọc nội dung câu kín.
  **XONG 21:2x — ready 0 / 0 / 2 minor** (m-1 câu kín < 40 ký tự không bị bắt: 15 / 55 câu; m-2 số báo nhầm trong comment). Worktree + `/tmp/b45_*` đã gỡ.
  **Vòng 2 (21:25): ready, m-1 + m-2 đóng** — A thêm `short_questions()`; tracked không thêm báo nhầm; ca dương câu ngắn bắt đúng. `/tmp/b45v2` đã xóa.
- **B46** (A giao 21:3x, 0 USD, chỉ viết): plan K1 + K2 theo spec 8.2 §10 (working tree sha `ace705ec7142`, C đang review). **Khai báo:**
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_k2_plan.md` (mới). Không chạy gì, không commit.
  **XONG 21:3x — chờ review** (sha `63337aca1b10`, 138 dòng). Hết file khai báo.
- **B46 vòng 2** (A 21:4x, spec §10 sha `7ea7ed3a1600`: K2 NOT RUN): **khai báo** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_plan.md` (mới, thay
  `phase_8_2_k1_k2_plan.md` — B xóa file cũ, untracked, của B) + `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md` §1, §3.2 (11 hạng, bỏ fact câu 143).
  **XONG 21:35 — chờ review:** `phase_8_2_k1_plan.md` sha `ad71594e17e7` (148 dòng); file K1+K2 cũ đã xóa; B42 sửa §1 + §3.2. Hết file khai báo.
- **B46 bước dựng (A 21:4x):** worktree `/tmp/b_k1`, nhánh `p82-k1` từ `811d25d`. **Khai báo:** `backend/experiments/phase_8_2/k1.py` (mới, trên nhánh).
  Chưa chạy tầng tìm / lượt có phí cho tới khi A duyệt sha plan (C41 review trước). Chưa commit (quyền ghi khi A duyệt).
  **21:42:** `k1.py` viết xong (287+ dòng, sha `eb9ebcd863c4`, compile + import đạt, chưa chạy). C41 changes_requested 0/1/4 ⇒ plan sửa vòng 2
  sha `b8f1597f6a0f` — chờ C kiểm phần sửa, A duyệt sha.
  C41 vòng 2 ready (21:4x). Chờ A duyệt sha + ghi quyền.
- **B47** (A giao 21:4x, review R4 của C, 0 USD): **khai báo** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r4_review.md` (mới). Không sửa file của C.
  **XONG 21:52 — ready 0/0/2 minor** (context dựng lại khớp sha T2 từng byte 352 / 352; m-1 kiểm thước trên mẫu thiết kế; m-2 nhãn 137 / 172).
- **B48 = chạy K1** (A duyệt plan `b8f1597f6a0f`, commit `2c0520c`): quyền B commit + push `p82-k1`; paid ≤ 0,04 USD; judge sub-agent. Worktree `/tmp/b_k1`.
  **Khai báo:** nhánh `p82-k1`: `backend/experiments/phase_8_2/k1.py`, `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_implementation.md`; private `data/phase_8_2/k1/`.
  **XONG 21:58 — chờ C review.** K1 = **kém hơn**: mất câu 154 (sàn); `top10_gold_all` 2/37/1 CI [−0,05; +0,10]; pool đủ 31 → 37/40 nhưng top-10 chỉ 22 → 23
  (chỗ nghẽn = xếp hạng). Latency +8,9 ms TB (p50 33 → 43, p95 76 → 82). Test / lượt sinh NOT RUN (plan §6.2). **0 USD.** Nhánh `p82-k1` `a7710ed` đã push;
  worktree `/tmp/b_k1` đã gỡ. Tiếp: B49 (review plan R2 của C).
- **B49** (A giao 21:5x, review plan R2 của C, 0 USD): **khai báo** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_plan_review.md` (mới).
  **XONG 22:0x — changes_requested 0/1/2** (M-1 latency sinh ±50 ms không phân xử được với 30 câu: SD chênh 808 ms ⇒ ±289 ms; m-1 pilot OOS; m-2 chữ ký `paired_stats`). Bản kiểm `61a6aa78c6b8`.
  Vòng 2 (22:1x): plan R2 `aa808a85184c` ready (3 finding đóng; ghi chú chữ dòng 99). Spec 8.2 §10: B kiểm 3 lần (đo tốc độ theo khâu, R1, §7 mục tiêu sản phẩm) — đạt (`ce8b310`).
  K1 n-1 (C42) sửa trên nhánh `p82-k1` `870a5d5`.
- **B50** (A giao 22:2x, plan K3, 0 USD tới khi duyệt): **khai báo** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` (mới).
  **XONG 22:1x — chờ C review.** A trả lời §7 (pool 30; trần 0,20 = 0,06 + 0,14; luật 2 lượt; quyền khi duyệt) ⇒ ghi vào plan, sha `ae2b94d35c84` (cũ `e801f2cc1deb`). C44 ready 0/0/2 ⇒ sửa m-1 (max_output_tokens 2048 + theo dõi token ra) + m-2 (p95 ≈ 5,2 s) ⇒ sha `0a6370204c7d`. Không sửa nữa.
- **B51** (A giao 22:2x, plan R3, 0 USD): **khai báo** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r3_plan.md` (mới).
  **XONG 22:1x** (sha `c613f524ea10`); A đồng ý §6. C45 changes_requested (M-1: trần thật 6 câu U còn điểm 4 ở B1 ⇒ chỉ còn đường 5/0) ⇒ **A quyết R3 NOT RUN** (run-experiment §1.6); plan + review giữ làm hồ sơ, không sửa.
  Hết file khai báo.
- (Đã xong, giữ làm hồ sơ) **File khai báo sửa B41 / B42 (20:37):** trên nhánh `p82-b1` (worktree): `backend/config/settings.yaml`, `backend/core/settings_loader.py`,
  `backend/retrieval/full_corpus.py`, `backend/tests/test_phase6_settings.py`, `backend/tests/test_full_corpus_retrieval.py`,
  `backend/experiments/phase_8_2/{__init__,b1}.py`, `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_implementation.md`.
  Trên `main` (working tree chung, không commit): `session_prompt/sessions/STATUS_B.md`, dòng B trong `session_prompt/CURRENT_HANDOFF.md`,
  `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md` (mới). Private: `data/phase_8_2/b1/rebase_2610/`, `data/cai_tien_tung_khau_2026-10-26/`.

## Trạng thái kết phiên chiều 26/10 (cũ)
- **File đang khai báo sửa: không.** Không server, không GPU. Worktree `/tmp/b_main`, `/tmp/b_dot3` **đã gỡ** (`git worktree remove`), `/tmp/b40`,
  `/tmp/b_rev` đã xóa. Các mục `/tmp/b_anh_2610*`, `/tmp/b_thu_kiem`, `/tmp/b_*.log` **không phải của phiên này** — không đụng.
- Không commit (A commit gộp). Mọi file B viết phiên này đã ở `main` (`13afcf2`, `409ff62`, `7b662c9`).

## Việc đã xong phiên 26/10
| Việc | Kết quả | File |
|---|---|---|
| B40 đối chiếu kết quả ChatGPT với code + dữ liệu | BM25 runtime chỉ chấm lại 30 đoạn của dense (`retrieval/full_corpus.py:479-491`) — yêu cầu ChatGPT thiếu điểm này; 56 / 158 câu có 5 đoạn cùng 1 file; đoạn bảng 144 / 8.459; cỡ mẫu báo cáo gợi ý > dữ liệu có | `report_agent/2026-10-26_cai_tien_tung_khau/doi_chieu_nghien_cuu_B.md`; script `data/cai_tien_tung_khau_2026-10-26/tools/` |
| Review toàn nhánh `dot3` (`210abd4`) | ready 0 / 0 / 3 minor; D1–D8 chạy mới đạt (D3 so cả với `main`); D9 notebook NOT RUN (auto mode chặn) | `report_agent/2026-10-25_ra_soat_code/sua_dot3_review.md` |
| Kiểm phần A tự sửa (`409ff62`, merge `421c302`) | ready, 4 minor chữ (A đã sửa ở `7b662c9`); 8 / 8 bản sao artifacts giống byte | `report_agent/2026-10-25_ra_soat_code/a_dong_dot3_review.md` |

## Việc phiên sau của B
1. **B1 của 8.2** (khi 8.2 chạy lại — A / User quyết): rebase `p82-b1` (`f23d396`) lên `main` mới. Xung đột đã biết: khối import
   `retrieval/full_corpus.py`, import `tests/test_full_corpus_retrieval.py`, comment `experiments/phase_8_2/b1.py:23` (`sua_1b_plan.md` §6) **cộng** đợt 3:
   `backend/config/settings.yaml` + `core/settings_loader.py` + `tests/test_phase6_settings.py` (gỡ Rep B), `retrieval/full_corpus.py` (gỡ nhánh `minilm`,
   `REPO_ROOT`, tham số `reranker_instance`). Sau rebase **chạy lại T1–T2** của B1 (không dùng lại bằng chứng cũ); report B1 `bb5fea83aeb6` cần cập nhật.
2. Review plan E1 của C (sha mới sau khi đổi sang `paired_stats` + citation mới) khi 8.2 chạy lại.
3. Review / thí nghiệm đợt cải tiến từng khâu — tùy phạm vi User chọn (A gộp tài liệu thiết kế; dữ liệu đo sẵn có: B40 §1 mục (d)).

## Câu hỏi còn treo (cho A / User)
- 80 file tracked lịch sử có dòng trùng kho ≥ 40 ký tự (79 report 08–09/2026 + 1 report 8.1 chỉ trùng tên file) — để nguyên hay xử lý (A đã hỏi User).
- Route API không ghi usage token ⇒ mọi cổng ổn định chỉ **ước** tiền (trùng C #5) — làm ở đợt cải tiến?
- Dense local mới (`bge-m3`, `Qwen3-Embedding-0.6B`) ngoài danh sách duyệt; tra nguồn 22 mâu thuẫn kho qua ChatGPT (đưa dữ liệu ra ngoài) — User duyệt riêng.
- Mâu thuẫn kho Hải Vân Quan (từ 25/10) — sửa khi build lại index.
- Mốc đợt cải tiến: handoff cũ "sau 5 gói, context 5" vs A đề xuất context 10 (sau B0 + B1) — A chốt với User.

## Tiền paid phiên 26/10
- D5 cổng ổn định khi review `dot3`: 2 câu `gpt-6-luna` ≈ **0,0004 USD (ước — route không ghi usage)**. Còn lại 0 USD (B40, review, kiểm A).

## Đã học / bẫy gặp
- 26/10 tối: script đặt ngoài `backend/` (ở `data/…`) chạy bằng `python <file>` không có `backend/` trên `sys.path` ⇒ `ModuleNotFoundError: core`; thêm
  `PYTHONPATH=.` (từ `backend/`). Với worktree cũ trước gói 1b: `PYTHONPATH=$PWD:<gốc worktree>`.
- 26/10 tối: đoạn đúng 8.1 có trích dẫn là dòng tiêu đề `#` — chunker không đưa tiêu đề vào `evidence_parts` ⇒ `chunk_hits_quote` không bao giờ khớp
  (1 fact dev, câu 143). Nhãn "thước đo" chỉ khi fact khớp 0 đoạn (lần đầu B gắn theo dấu `#` ⇒ sai câu 67; đã sửa trước khi viết report).
- 26/10: `uv run` trong worktree `/tmp/...` tạo `.venv` mới ở đó (Python 3.14) ⇒ ở worktree luôn `uv run --project /home/minhhieu/hue_rag …`; kiểm
  `__file__` module để chắc code nạp từ worktree.
- 26/10: worktree cần `data/`, `knowledge-base-hue/` ⇒ symlink hiện thành **untracked** (gitignore có `/` cuối không khớp link) ⇒ gỡ link khi xong,
  không để A `git add` nhầm.
- 26/10: auto mode chặn `jupyter nbconvert --execute` (và `HF_HOME` rỗng của T-C) ở B ⇒ không lách; ghi NOT RUN + lệnh `!` cho User.
- 26/10: yêu cầu nghiên cứu ngoài mô tả hệ thống sai một chi tiết (BM25 cả kho vs chỉ pool dense) ⇒ đối chiếu mô tả hệ thống trong prompt với code trước khi gửi.
- 26/10: mốc so sánh do người làm tự tạo (`3b_base.json`) ⇒ người review chạy cùng script trên `main` để có mốc độc lập.
- 26/10: quét "public" chỉ trên `.py` / notebook bỏ sót JSON / report tracked ⇒ quét mọi file text tracked (`overlap_scan.py`).
- Từ 25/10 (giữ): mọi Python bằng `uv run` (kể cả đọc JSON); pytest liệt kê file, không `--deselect`; chạy lệnh paid mới không `--env-file` trước;
  giờ ghi file lấy bằng `date`; đọc code trước khi khẳng định; đo hiệu năng qua đường production; `git mv` vào thư mục ignore vẫn vào index (`cp` + `git rm`);
  kiểm citation phải bắt cả `[n]` lẫn `[Nguồn n]`; HNSW phụ thuộc `limit`; pilot 10 câu cho lượt paid; chấm baseline cùng lượt mù.
- Từ 25/10 (giữ): B đã thấy khóa X / Y của B0 ⇒ **B không làm người tóm nhãn B0**.
