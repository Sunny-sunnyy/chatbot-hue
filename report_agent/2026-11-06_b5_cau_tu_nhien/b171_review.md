# Review: Phase 9 B5 — B171 sửa 2 loại lỗi lịch trình bằng code (L-a, L-b)

Decision: **changes_requested** (1 major, 2 minor) + 1 câu A chọn (T3, B đã nêu)
Người kiểm: C (Claude Code, Opus 5.5) — không viết code B5 / B171; **không** đọc `data/phase_9/b5/kin/`, `data/phase_9/b5_v2/`.
Date: 11:26 06/11/2026 (`date`)
Canonical guide: plan B5 bản 7 (D2, D2b, D4, D4b, D8); việc B171 trong `CURRENT_HANDOFF.md` mục "PHIÊN 06/11".
Implementation report: `report_agent/2026-11-06_b5_cau_tu_nhien/b171_implementation.md`

## 1. Phạm vi đã review

- Nhánh `origin/p9-b5-sua` **`d5028d4`**, gốc `main` `0a9e0f3` (1 commit). Exact diff 3 file: `lich_trinh.py` (+82 / −8), `assistant.py` (1 dòng), `test_b5_lich_trinh.py`. `git diff --check` sạch; không file ngoài phạm vi.
- Đọc hết `xep` trên nhánh (để kiểm `chon_sang` có đi qua đủ luật cũ), `kiem_khung`, `khung_chu`, `kiem_cuoi` + `_noi_nguoc_toi`.

## 2. Findings

### M-1 (major) — kiểm "nói ngược buổi tối" (`toi_ngoai_khung`) bắt nhầm lời hợp khung ⇒ cả câu trả lời bị rút lại

- **Vị trí:** `lich_trinh.py` `_noi_nguoc_toi`: (a) dòng mở bằng "tối" / "buổi tối" mà không có từ phủ định ⇒ bắt; (b) câu có "tối / đêm" + "được / có thể" mà không phủ định ⇒ bắt. Hỏng ⇒ rút lại như citation hỏng (người dùng thấy "Thử lại").
- **Bằng chứng [Chạy, ca dò C `/tmp/c207_tools/probe_b171.py` trên `d5028d4`]:** 10 câu **hợp khung** (không hứa hoạt động tối) ⇒ **5 bị bắt nhầm**: "Buổi tối: tự do." · "Tối về khách sạn sớm để bé ngủ." · "Buổi tối bạn có thể về khách sạn sớm." · "Tối hôm trước nên chuẩn bị nước và mũ." · "Ngày 2 có thể đi chậm, tối thư giãn ở khách sạn." 6 câu **nói ngược** ⇒ bắt đủ 6 / 6. Đúng loại lời model hay viết ở lịch có trẻ nhỏ / người lớn tuổi — chính nhóm mà luật này chạy.
- **Tác động:** "từ chối nhầm" cả lịch ở nhóm khách cần lịch nhẹ nhất. Report §5 (2) ghi rủi ro bắt nhầm nhưng lượt có phí chỉ có 4 câu áp dụng ⇒ chưa đủ thấy.
- **Tiêu chí đóng (B chọn cách trong phạm vi, A xem):** thu hẹp điều bắt về đúng "xếp / hứa một **hoạt động hay điểm** buổi tối" — đề xuất của C: chỉ bắt khi dòng / câu nhắc tối / đêm **và** có tên một điểm của bảng (`khop_diem`) hoặc nhãn buổi tối kèm tên điểm; dòng "Tối: nghỉ / tự do / về khách sạn" không bắt. Ca dò của C (16 câu) đưa vào test: 10 câu hợp khung ⇒ không bắt, 6 câu nói ngược ⇒ bắt. Chạy lại 4 câu xin buổi tối của lượt có phí × 1 (≈ 0,003 USD) ⇒ 0 rút nhầm.

### m-1 (minor) — bộ dò xin buổi tối bỏ sót vài cách nói thường gặp

- **Bằng chứng [Chạy, ca dò]:** "tối muốn đi nghe ca Huế" ⇒ không bắt ("tối" + "muốn" không có trong danh sách động từ); "đi chơi đêm" ⇒ không bắt ("đêm" chỉ tính sau buổi / ban / về / phố / chợ); "khuya đi đâu" ⇒ không bắt (B đã ghi). Đúng: "3 ngày 2 đêm", "tối đa 2 điểm" không bắt; "buổi tối đi đâu", "Huế về đêm", "chơi tối", "tối có gì vui" bắt.
- **Tác động:** bỏ sót ⇒ không có câu lý do và không bật kiểm (như trước B171) — không tệ hơn hiện tại.
- **Tiêu chí đóng:** thêm "tối muốn / tối thích", "chơi / đi … đêm", "khuya" nếu B thấy không bắt nhầm (kiểm lại 2 câu "N ngày N đêm", "tối đa"); 1 ca test mỗi dạng. Không cần lượt có phí.

### m-2 (minor) — câu "Kho chỉ có k điểm hợp sở thích" đếm cả điểm người dùng nêu

- **Vị trí:** `xep`: `hop_ngay` đếm trên `pool = them_ids + hop` ⇒ điểm người dùng tự nêu (có thể không hợp sở thích) được tính vào "k điểm hợp sở thích". Đọc code [Code, chưa chạy]; giống cách đếm cũ (`len(hop) + len(them_ids)`), nên không phải lỗi mới — nhưng L-a là "câu lý do đúng sự thật".
- **Tiêu chí đóng:** đếm `hop` (điểm hợp sở thích) riêng, hoặc ghi lý do giữ cách đếm; 1 test.

### Câu A chọn — T3 (B đã nêu, report §6)

Dạng "hỏi có / không về một hoạt động buổi tối" khi lịch không xếp tối ⇒ rút lại 7 / 7 lượt. Theo dữ liệu B, lỗi này **không** do B171 gây ra (bỏ dòng khung vẫn từ chối / nói ngược). C đồng ý hướng **(b)** (code dựng lời lịch tối thiểu khi chữ model đúng bằng câu từ chối) — cùng khuôn với B5b M-1 đã duyệt, tất định, 0 USD / câu — **sau khi** M-1 ở trên đóng (để không chồng hai thay đổi vào cùng một lượt đo).

### Không phải finding

- `chon_sang` chỉ chọn trong `pool` (đã qua `dung_duoc`: cụm xa, buổi hợp lệ với nhóm hạn chế) và kiểm `used` / buổi / cụm như `chon` ⇒ không lách luật cũ; không có cạnh khác lạ. Không thấy over-engineering.
- Ghi chú merge: `p9-sua-lich` (`09ddaf9`) đổi `xep(bang, ts, giu, loai)` và dựng lại `ThamSo` từ `tham_so` đã lưu — khi gộp, `tham_so` có thêm khoá `hoi_toi` ⇒ người gộp sau kiểm `ThamSo(**…)` / `luu_tu_lich` nhận khoá này, và `chon_sang` tôn trọng `giu` / `loai`.

## 3. Cách người kiểm chạy lại thật

Worktree `/tmp/c_b171` detach `d5028d4` (symlink `data/`, `knowledge-base-hue/`). Từ `backend/`, `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python …`:
- `../data/phase_9/b171/tools/tai_tao_la.py`; `../data/phase_9/b171/tools/so_khung_cu_moi.py /tmp/b171_cu/llm/lich_trinh_cu.py ../data/phase_9/lich_trinh/diem_v3.json` (bản `main` chép từ `git show main:backend/llm/lich_trinh.py`).
- `-m pytest -q tests/test_b5_lich_trinh.py tests/test_assistant_boundary.py tests/test_chat_stream.py`.
- Q1: `env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only … capture_all.py data/phase_9/b171/q1_c_review/nhanh_d5028d4.jsonl` ⇒ `cmp` với `data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl`.
- Ca dò: `/tmp/c207_tools/probe_b171.py` (16 câu cho `_noi_nguoc_toi`, 9 câu cho `hoi_buoi_toi` — câu C tự viết, không lấy từ bộ đo).

## 4. Kết quả quan sát

- `tai_tao_la.py`: 120 ca, L-a còn **6** (đều "thiên nhiên 4 ngày", câu lý do `khong_cung_huong`, `kiem_khung` 0) — khớp report [Chạy].
- `so_khung_cu_moi.py`: **1.728 ca, đổi 168, đều sở thích thiên nhiên** (lấp 1 ⇒ 0: 108 · 2 ⇒ 1: 36 · 1 ⇒ 1: 24) — khớp report. **Bất biến** "sở thích khác thiên nhiên ⇒ khung không đổi": đạt trên 1.728 ca [Chạy].
- Test **236 passed** [Chạy]. **Q1: 228 / 228 giống byte `main`** [Chạy].
- Ca dò: như M-1 / m-1.
- Dùng lại (không chạy lại): lượt có phí 17 câu + T3 7 lượt của B (0,0179 USD) — chỉ đọc số trong report.
- Tiền review: **0 USD**.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lượt có phí; không đọc chữ câu trả lời của lượt có phí (đánh giá rủi ro bắt nhầm bằng ca dò tự viết).
- Bảng v5 chưa duyệt ⇒ 6 ca "thiên nhiên 4 ngày" có thể đổi khi chuyển bảng.

## 6. Decision và bước tiếp theo

**changes_requested.** B sửa M-1 (thu hẹp kiểm nói ngược + 16 ca dò vào test + chạy lại 4 câu xin buổi tối × 1), m-1, m-2 trong một lượt. A chọn hướng T3 (C đồng ý (b), làm sau M-1). Kiểm lại: C chạy test + ca dò + Q1 (0 USD) và đếm lượt chạy lại.
