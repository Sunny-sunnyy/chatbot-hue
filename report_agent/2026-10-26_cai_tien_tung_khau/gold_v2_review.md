# Review: nhãn đoạn đúng bản 2 (gold v2) + đếm cả tiêu đề mục — report B69

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 3 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-5b`) · Việc: C61 (A giao 27/10)
Date: 2026-10-27 13:18 +0700 (`date`)
Canonical guide: đề xuất C56 (`c56_de_xuat_sua_nhan.md`, `data/phase_8_2/gold_fix_proposal_2710/proposal.jsonl`) + User duyệt 27/10 (A báo); `practical-project-coding`
Implementation report: `origin/gold-v2` `b972b55` — `report_agent/2026-10-26_cai_tien_tung_khau/gold_v2_implementation.md`

File này không chép câu hỏi, fact hay nội dung kho — chỉ `case_index`, số đếm, sha.

## 1. Phạm vi đã review

- **Git:** `git diff --stat <merge-base e452e27>..origin/gold-v2` = 3 file: `backend/experiments/phase_8_1/g1_retrieval.py` (+28 / −5), `backend/tests/test_gold_coverage.py` (mới, 15),
  report. Không chạm `api/`, `llm/` (việc C60). `git diff --check` sạch.
- **Code** (đọc hết phần đổi): `GOLD_PATH` → `gold_v2.jsonl` (comment ghi bản 1 giữ vì G0.6); `KB_ROOT`; `source_text(source)` (`lru_cache`, CRLF → LF như `validate_gold.py`);
  `quote_is_chunk_heading(payload, quote_text)`; `chunk_hits_quote` giữ luật cũ, chỉ khi thân đoạn không trúng mới thử luật tiêu đề.
- **Dữ liệu private:** `data/phase_8_1/gold/{gold_draft.jsonl, gold_v2.jsonl, gold_v2_CHANGES.md}`, `proposal.jsonl` (C56), các lượt `data/phase_8_2/k3/base_{dev,test}.jsonl`,
  `k3b/{m_l1.merged, m_l2, m_test}.jsonl`.
- **Không chạy `validate_gold.py`** (ghi đè `gold_draft.jsonl` — A dặn). Không đọc câu test theo từng câu, không mở câu kín.

## 2. Findings

Không có blocker hoặc major.

### m-1 — đổi `GOLD_PATH` mặc định là đổi thước cho mọi harness 8.1 chạy lại sau merge — nên ghi ở chỗ người chạy sẽ thấy

- **Bằng chứng:** `git grep` trên nhánh: `GOLD_PATH` / `load_gold(GOLD_PATH)` dùng trong `g1_retrieval.py` (161, 188), `g2_generate.py` (47, 222), `g3_chunking.py` (50, 394),
  `g4_keyword.py` (26, 173), `g4_rerank.py` (41, 101, 178). Các file kết quả đã lưu (8.1, K1, K3, K3b) mang `*_gold_*` tính bằng **v1**. Sau merge, ai chạy lại một biến thể
  rồi so với file mốc cũ sẽ so v2 với v1 mà không biết.
- **Tác động:** không đổi kết luận nào đã đóng (report §5 đã nói "không so trực tiếp số mới với số cũ"). Rủi ro là ở lần dùng sau.
- **Tiêu chí đóng:** một dòng ở `Project_Status.md` §8 (bẫy) hoặc cạnh `GOLD_PATH`: "file kết quả trước 27/10 tính bằng v1; so biến thể mới thì chạy lại mốc bằng v2". A chọn chỗ.

### m-2 — report trỏ script tính lại ở `/tmp` thay vì script lưu lại

- **Vị trí:** report §3 dòng 64: `python /tmp/b75_recount.py`. Trong khi đó đã có `data/phase_8_1/tools/recount_gold_v2.py` (sha `aad629632518`).
- **Tiêu chí đóng:** đổi đường dẫn trong report sang script đã lưu (hoặc ghi rõ hai cái là một).
- **Đã sửa 27/10 (C62):** report §3 trỏ `data/phase_8_1/tools/recount_gold_v2.py`.

### m-3 — lệnh dựng v2 trong report chạy bằng `python3` hệ thống

- **Vị trí:** report §3: `python3 data/phase_8_1/tools/build_gold_v2.py`. Lệch `Session_Prompt.md` §10 (mọi lệnh Python của dự án qua `uv run`, kể cả script chỉ đọc — bẫy C36 26/10).
- **Tác động:** không đổi kết quả (C kiểm v2 độc lập ở mục 4).
- **Tiêu chí đóng:** ghi lệnh `uv run python …` cho lần sau; không cần chạy lại.
- **Đã sửa 27/10 (C62):** report §3 ghi `uv run python data/phase_8_1/tools/build_gold_v2.py`.

## 3. Cách người kiểm chạy lại thật

0 USD, chỉ đọc. Từ `backend/` working tree chính:
- `uv run python` inline so `gold_v2.jsonl` với `gold_draft.jsonl` và `proposal.jsonl` (không có trường `proposal`) theo từng câu.
- `/tmp/c61_recount.py` (`PYTHONPATH=. HF_HUB_OFFLINE=1 uv run python …`; bản giữ lại: `data/phase_8_1/tools/c61_recount_check.py` — sửa 27/10, C62) — **hàm đếm C tự viết**, không dùng `recount_gold_v2.py` của B: lấy payload Qdrant (`g1.load_payloads`, đọc),
  đếm "đủ đoạn đúng" cho 4 cách: v1 thân đoạn / v1 + tiêu đề / v2 thân đoạn / v2 + tiêu đề, trên context và top-10 của 5 lượt; kiểm chuỗi `quote` = văn bản file tại `[start, end)`.
- Worktree tạm `/tmp/c61_wt` (detached `origin/gold-v2`, đã gỡ): `pytest tests/test_gold_coverage.py`; gọi chính `g1.gold_coverage` + `load_gold(GOLD_PATH)` của nhánh trên 5 lượt.
- `sha256sum` hai file nhãn trước / sau.

## 4. Kết quả quan sát — năm điểm A hỏi

**(1) v2 chỉ thêm đúng 3 khoảng C56; bản cũ không đổi — ĐẠT.**
- `gold_draft.jsonl` = **`bab707b9ab22`** (kiểm cả sau khi chạy mọi lệnh); `gold_v2.jsonl` = **`2f5a347a71ff`**.
- 55 / 55 câu, cùng tập; chỉ **2 câu đổi** (120, 156). Ở cả hai: evidence cũ là **tiền tố** của evidence mới (thêm 2 và 1 khoảng), chữ fact giữ nguyên, `quote_ids` cũ ⊂ mới, các
  trường khác giữ nguyên; và hai dòng v2 **bằng đúng** hai dòng của `proposal.jsonl` (bỏ trường `proposal`).

**(2) Luật tiêu đề đúng và nhỏ nhất — ĐẠT.**
- Chỉ chạy khi cùng file mà thân đoạn không trúng; trúng khi chuỗi trích dẫn (đọc lại từ file theo offset) bắt đầu bằng `#` và phần chữ sau `#` khớp nguyên văn một mục `heading_path`
  của chunk — đúng điều model thấy (context dựng từ tiêu đề + mục + đoạn). Giữ bộ ba `(source, start, end)` nên 6 harness gọi `load_gold` / `gold_coverage` không phải sửa — hợp lý.
- Trong v2 chỉ **2** trích dẫn là dòng tiêu đề (câu 67, 143). C đếm: luật tiêu đề chỉ đổi **câu 143** ở cả B1, L1, L2; câu 67 không đổi số nào (đã đủ / chưa đủ vì fact khác).
  ⇒ không có trúng nhầm thêm.
- Tách hai thay đổi (C tự đếm): v1 + tiêu đề ⇒ B1 22 → 23 (143); v2 thân đoạn ⇒ B1 22 → 23 (156), K3b-m 31 → 32 (120); cả hai ⇒ 24 / 33 — khớp report §4 "Tách hai thay đổi".

**(3) Test `test_gold_coverage.py` — ĐẠT.** 2 passed (worktree `origin/gold-v2`). Logic thuần, chuỗi tự viết, bảo vệ đúng ranh giới "dòng tiêu đề trúng / cùng chữ nhưng không phải
tiêu đề, hoặc tiêu đề khác, không trúng". Đường đọc offset từ file (`source_text`) không có test riêng — được kiểm bằng lần tính lại trên dữ liệu thật (mục 3), đủ cho thay đổi này.

**(4) Tính lại 22 → 24 và 31 → 33, thắng 9 / thua 0 — ĐẠT.**

| Lượt (context = top-10 ở mọi lượt) | v1 thân đoạn | v2 + tiêu đề |
|---|---:|---:|
| Mốc B1 dev 40 | 22 | **24** |
| K3b-m L1 / L2 dev 40 | 31 / 31 | **33 / 33** |
| Mốc B1 test 15 | 7 | 7 |
| K3b-m test 15 | 10 | 10 |

- Hàm của C ở "v1 thân đoạn" tái lập đúng `context_gold_all` đã lưu của B1 và L1 ở mọi câu; hàm `gold_coverage` của nhánh cho cùng 24 / 33 / 33 / 7 / 10.
- K3b-m dev theo v2 + tiêu đề: thắng ổn định **9** (17, 38, 48, 67, 70, 85, **120**, 159, 167 — 156 ra vì mốc nay đủ), thua **0**, CI [+0,10; +0,35] ⇒ kết luận tầng tìm không đổi.

**(5) W26 — ĐẠT.** Test dùng chuỗi tự viết chung chung (đường dẫn và tiêu đề giả); report tả câu ở mức loại câu (`direct_fact`, `comparative`, `conditional`), không nêu chủ đề, tên file
hay `case_index`. Commit message chỉ có số câu.

## 5. Giới hạn

- C không chạy `build_gold_v2.py` (kiểm v2 bằng so trực tiếp với v1 + `proposal.jsonl`, tương đương).
- 3 câu test C56 "chưa quyết" (95, 130, 138) vẫn chưa ai đọc — ngoài phạm vi B69.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Nhãn v2 và luật tiêu đề đúng như User duyệt; số tính lại khớp ở mọi ô; bản khóa G0.6 không đổi. 3 minor không chặn: m-1 nên ghi trước khi merge (một dòng
bẫy); m-2, m-3 sửa chữ trong report ở commit kế hoặc A ghi hồ sơ. A merge `gold-v2` khi tiện (không xung đột C60: hai nhánh không chung file).
