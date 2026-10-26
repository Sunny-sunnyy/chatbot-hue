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
- **B42** (phân loại lỗi tầng tìm, 0 USD): đang làm (20:5x).
- **File khai báo sửa (20:37):** trên nhánh `p82-b1` (worktree): `backend/config/settings.yaml`, `backend/core/settings_loader.py`,
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
