# C207 — rebase `p9-sua-lich` lên `main` mới + Q1 + test (0 USD)

Người làm: C (Claude Code, Opus 5.5) · 11:00 06/11/2026 (`date`) · A giao sáng 06/11 (`CURRENT_HANDOFF.md` mục "PHIÊN 06/11", dòng C).
Plan gốc của nhánh: `docs/superpowers/plans/2026-11-05-phase-9-sua-lich-plan.md` bản 3 `5b68f3cb666a`. Code: B (B163 + B166), report `b163_sua_lich_implementation.md`.

## 1. Việc

`p9-sua-lich` `6543f82` đứng sau `main` 25 commit (trong đó merge B6 tra web: `assistant.py`, `chat.py`, `settings.yaml`… đổi) ⇒ rebase lên `main` `0a9e0f3`, kiểm lại cờ tắt / cờ bật bằng Q1 / Q1m, chạy test + build, rồi chạy thử 0 USD các công cụ đo đã có. Không đổi hành vi nào của nhánh.

## 2. Rebase

- Worktree `/tmp/c_sualich`, nhánh tạm `c207-rebase` (từ `6543f82`) — không đụng ref `p9-sua-lich` tới khi A cho push.
- **Xung đột 3 file, đều "hai bên cùng thêm":** `chat.py` (danh sách trường log: B6 thêm trường web, nhánh thêm trường sửa lịch; lời gọi `answer_turn_stream_parallel` ở đường stream: ghép thành `_model_query(..., _flags(state).bang_lich)` **và** đối số `_tim_web(state)`), `settings.yaml` (cờ `tra_web` + `tra_web_timeout_seconds` của `main` + cờ `sua_lich: false` của nhánh), `assistant.py` (import `tra_web` + `sua_lich`; cờ `tra_web` + `sua_lich`; kiểm cờ trong `__post_init__`). Giữ cả hai phía, không sửa dòng nào khác.
- Các file git tự ghép (`generator_openai_full_corpus.py`, `full_corpus_prompt.py`, `App.jsx`, `conversations.py`): đọc lại diff với `main` — chỉ phần của nhánh (công cụ `sua_lich_fn`, `SUA_LICH_MO_TA`, thẻ chọn).
- **`git range-diff`:** commit B166 giống hệt (`6543f82` = `09ddaf9`); commit B163 chỉ khác dòng ngữ cảnh do `main` thêm (B6) — mọi dòng `+` của nhánh không đổi.
- **Kết quả:** `5c2d486` (B163) · **`09ddaf9`** (B166) trên `main` `0a9e0f3`.

## 3. Kiểm [Chạy]

| Kiểm | Lệnh (từ `backend/` của cây cần đo) | Kết quả |
|---|---|---|
| **Q1** cờ tắt ⇒ chuỗi gửi model giống byte `main` | `env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python ../data/phase_9/b2_chay/tools/capture_all.py <out>` ở `main` `0a9e0f3` và ở nhánh | **228 / 228 giống byte**, sha `dba1f578eef1` cả hai (`data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl`, `nhanh_09ddaf9.jsonl`) |
| **Q1m** `lich_trinh` bật: `sua_lich` bật ↔ tắt | `…/capture_flags.py <out> lich_trinh=1 sua_lich=<0|1>` (bản sao settings, chạy `capture_all.py` nguyên; script tạm `/tmp/c207_tools/`, thay `/tmp/b164/capture_flags.py` đã mất khi máy khởi động lại) | **228 / 228 giống byte**, sha `ac53ea9046f3` cả hai (`q1m_lich1_sua{0,1}.jsonl`) — khác `main` đúng như mong đợi (có mục công cụ `lich_trinh`); sha trùng lần đo B166 hôm qua |
| Test (không khoá) | `HF_HUB_OFFLINE=1 uv run --project … python -m pytest -q tests/test_sua_lich.py test_b5_lich_trinh.py test_b2_tool_loop.py test_b3_memory.py test_toc_do_song_song.py test_assistant.py test_chat_stream.py test_assistant_boundary.py test_feedback.py test_b6_tra_web.py` | **239 passed** |
| Build giao diện + test tĩnh | `cd frontend && npm ci && npm run build`; `pytest tests/test_static_ui.py` | build xong (JS 319,29 kB); **3 passed** |
| Mô phỏng 0 USD (hành động nhãn ⇒ `ap_hanh_dong` thật) | `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project … python ../data/phase_9/sua_lich/tools/mo_phong.py` | **10 / 10 ok** (bộ đã thấy) |
| Kiểm bộ | `… python ../data/phase_9/bo_do_sua_lich/tools/kiem_bo.py --pha` | **OK**, ca phá **6 / 6** |

Ghi chú Q1: không nạp `.env` (khoá giả) ⇒ cổng tra web B6 (đang bật trong `settings.yaml`) không có khoá Serper, không mở kết nối nào; giống nhau ở hai bên nên so byte vẫn đúng. 0 USD.

Không chạy: `test_api_chat.py`, `test_openai_full_corpus_generator.py` (cần khoá — `Project_Status.md` §8); bộ kín (không cần ở bước này; chạy kín qua User `!` trên khoá ở plan bước 5).

## 4. Push

`git push --force-with-lease=p9-sua-lich:6543f82 origin c207-rebase:p9-sua-lich` (A cho phép 06/11): **`6543f82` → `09ddaf9`** — đã push (`+ 6543f82...09ddaf9 (forced update)`); ref cục bộ `p9-sua-lich` = `origin/p9-sua-lich` = `09ddaf9`; worktree `/tmp/c_sualich` nay giữ nhánh `p9-sua-lich` (gỡ trước khi session khác cần chuyển sang nhánh này); nhánh tạm `c207-rebase` đã xoá.

## 5. Chạy thử lượt có phí (WORKFLOW §4 (4b)) — phát hiện thiếu công cụ

- Công cụ đã có cho lượt đo sửa lịch đều 0 USD và đã chạy đạt ở §3 (`mo_phong.py`, `kiem_bo.py`); `mo_phong_kin.py` (bộ kín) chỉ chạy qua User `!` ở bước 5.
- **(Đã viết 21:08 06/11/2026 — xem §7.)** Lúc rebase **chưa có harness lượt có phí** cho plan bước 3–5: không có script nào gửi chuỗi nhiều lượt (cookie cuộc, lượt bấm nút `sua_chon`) tới server thật với `lich_trinh` + `sua_lich` bật, ghi khung trước / sau mỗi lượt và chấm Q2 (a)–(i) / Q3 pass^2 theo nhãn. Script tạm của B (`/tmp/b164/`) đã mất và chỉ gồm bắt chuỗi gửi (Q1 / Q1m). ⇒ Báo A; đề xuất C viết harness + bộ chấm (0 USD, chạy thử bằng khoá giả + OpenAI trỏ cổng đóng như B5b `app_thoi_tiet.py`) trong lúc chờ B5 bật.

## 6. Trạng thái (sửa 21:08 06/11/2026)

- Nhánh `p9-sua-lich` = `09ddaf9` trên `main` `0a9e0f3`. Cờ `sua_lich: false`. `main` nay `8fc790f` (đã có B5b `db77f32`) ⇒ rebase khi gộp, sau B171 (A: không cần làm ngay).
- Tiền C207 + harness: **0 USD**.
- Harness lượt có phí: **xong phần 0 USD** (§7); review E vòng 1 changes_requested ⇒ **đã sửa** ⇒ chờ E kiểm phần sửa.
- Còn: lượt có phí chờ `lich_trinh` bật (B5 — bộ kín v2 do E chạy); trước lượt đó rebase lại lên `main` (gồm B171 ⇒ `tham_so.hoi_toi` + `chon_sang`) + Q1.

## 7. Harness lượt có phí sửa lịch (C, phiên tối 06/11 — A giao, 0 USD)

Theo plan bản 3 `5b68f3cb666a` §4–§6 và luật chấm ghi trước ở `data/phase_9/bo_do_sua_lich/README.md` (không đổi tiêu chí). File private (có chữ người dùng / model khi chạy):

| File | md5 (12) | Gì |
|---|---|---|
| `data/phase_9/sua_lich/tools/chay_sua_lich.py` | `b68e7c970782` (sau sửa review E; bản review vòng 1 `c4dee2ccf654`) | 3 lệnh: `kiem` (0 USD) · `chay` (có phí) · `cham` (0 USD) |
| `data/phase_9/bo_do_sua_lich/chuoi_q4.jsonl` | `d35f8d9c5027` | bộ Q4: 5 chuỗi TD của B5 (`b5/chuoi_v2.jsonl`) + 2 chuỗi an toàn sau lịch (C tự viết: một câu khẩn cấp, một câu ngoài phạm vi) |

**Cách chạy (đúng đường giao diện):** app thật **trong tiến trình** (`TestClient(create_app(<bản sao settings bật `lich_trinh` + `sua_lich`>))`, không sửa `settings.yaml`), gọi `/api/chat/stream` (đường #6 song song như giao diện), cookie thật, mỗi chuỗi một cuộc mới. Mỗi lượt ghi: sự kiện SSE, dòng `chat_metrics` (đọc `backend/logs/application.log` sau mốc dòng — không gắn handler), trace (bọc `_remember` của route — hàm thật vẫn chạy), hành động model gửi (bọc `ap_hanh_dong` — hàm thật vẫn chạy), khung đã lưu của cuộc trước / sau lượt (`app.state.conversations.lich`). Lượt bấm thẻ: body như giao diện (`query` = câu gốc của thẻ, `sua_chon` = điểm đầu code đưa hoặc `bo`). `--tran <USD>` dừng trước chuỗi kế khi chạm trần; chuỗi đã có ở cùng lần trong file ⇒ bỏ qua (không chạy lại), gọi lại cùng lệnh = chạy tiếp.

**Chấm (`cham`):** Q2 (a)–(i) mọi lượt sửa / bấm, mọi lần; Q3 pass^k trên các lần đưa vào = **hành động code áp đúng nhãn** (lượt lịch đầu cũng phải đúng `tham_so` nhãn; không có khung ⇒ "không đo được", chuỗi không đạt); lượt bị kiểm cuối rút lại / có mã kiểm cuối liệt kê riêng để đọc tay (A chốt, sửa theo review E); Q4 tuyến + `sua_lich` không gọi nhầm; Q5 (rút lại, thẻ chọn, USD / lượt, token vào có / không có công cụ `sua_lich`). `--so` ⇒ chỉ in số (bộ kín, lệnh `!`).

**Chỗ C tự quyết trong phạm vi plan (ghi để review):** (1) Q3: hành động nhãn mà trường điền lại **đúng giá trị cũ** ⇒ không tính là phải áp (D5); câu ngoài bảng ⇒ chỉ so mã luật `Không đổi được` (model có thể viết hoa khác chữ người dùng); dư một dòng "Không đổi được" ngoài nhãn ⇒ không trừ (chỉ hiện trong file kết quả). (2) Q2 (b) sau lượt **xếp lại** (đổi số ngày / tham số) chỉ kiểm (d) + điểm đã thêm, như `mo_phong.py` (D5 cho xếp lại có giữ, không bắt buộc giữ chỗ); dời buổi vào ô có một điểm ⇒ điểm kia được phép đổi chỗ (code đổi chỗ hai điểm). (3) Q4: TD1 (đổi người đi cùng) nay **là** câu sửa ⇒ gọi `sua_lich` là đúng ⇒ chỉ theo dõi; TD3 lượt 2 là lịch đầu (chưa có khung). Bộ Q4 chưa có ở bộ đo (plan §5 có ghi) ⇒ C bổ sung 2 chuỗi an toàn.

**Kiểm 0 USD [Chạy] trên `p9-sua-lich` `09ddaf9`:**

| Kiểm | Kết quả |
|---|---|
| `kiem chuoi_da_thay.jsonl` — mô phỏng đúng nhãn bằng code thật ×2 | Q3 **10 / 10**, Q2 **0 / 42** lượt vi phạm |
| ca phá (dời điểm không chạm · điểm đã bỏ quay lại · thiếu "Đã đổi" · thiếu "Chưa làm" · thẻ lần hai · khung đổi sau rút lại · nút lạ · áp khác nhãn · không qua `sua_lich`) | **9 / 9** bắt đúng chỗ |
| `chay` khoá giả + `OPENAI_BASE_URL=http://127.0.0.1:9` (S06, S09 + cả bộ Q4) | 22 lượt: mỗi lượt đúng **1** dòng `chat_metrics`; trace + khung trước / sau ghi đủ; `lich_trinh` được đưa, `sua_lich` chưa được đưa (chưa có khung — đúng D2); lượt bấm không có thẻ ⇒ ghi "bỏ qua"; mỗi chuỗi giữ một cuộc; chuỗi đã có ở cùng lần không chạy lại; câu hỏi trong log **0**; 0 USD |
| `cham` trên file chạy thử | chạy hết, đếm đúng (lượt lỗi sinh ⇒ Q3 không đạt, khung không đổi ⇒ Q2 (g) 0) |

**Chưa kiểm được ở 0 USD (NOT RUN):** đường thành công (khung lưu sau lượt đạt, công cụ `sua_lich` được đưa, thẻ chọn thật ⇒ lượt bấm, 422) — cần model thật ⇒ lộ ở **pilot** (plan bước 3: 2 chuỗi đầu lần 1, ≈ 0,007 USD); đọc file pilot trước khi chạy tiếp. S06 (chuỗi duy nhất có thẻ chọn) nằm ngoài pilot ⇒ đề xuất pilot = S01 + S06 (đổi so với "2 chuỗi đầu" — A quyết).

**Sửa theo review E** (`c207_harness_review.md`, changes_requested 1 major + 6 minor; A chốt m-1, m-5 — 21:27 06/11/2026):

| Finding | Sửa |
|---|---|
| M-1 Q4 đạt rỗng khi chưa có khung | `cham_q4` ⇒ "không đo được" khi `luu_truoc` None, hoặc tuyến `tro_ly_hue` có khung mà `sua_lich` không được đưa; đếm `q4_khong_do`, liệt kê `khong_do` |
| m-1 (A: Q3 = hành động đúng nhãn) | Q3 không gộp Q2; lượt `retracted` vẫn chấm hành động đã áp; `rut_lai_kiem_cuoi` = (chuỗi, lần, lượt, mã) in cả khi `--so` |
| m-2 `n_metrics` ≠ 1 | lượt đó "không đo được" (liệt kê), chuỗi không đạt |
| m-3 tóm tắt sau DỪNG | in `da_chay` / `chua_chay` |
| m-4 trần cả đợt | `--dung` (mặc định 0,19): cộng `usd` + `usd_bo` của mọi `*.jsonl` trong thư mục kết quả + lệnh này; in tiền cả đợt sau mỗi chuỗi ⇒ **thư mục kết quả chỉ chứa file kết quả của đợt này** |
| m-5 (A: thêm kiểm nếu chưa có test) | `test_sua_lich.py` không có test khẳng định giữ chỗ trên đường xếp lại của `ap_hanh_dong` (chỉ `test_xep_keeps_positions…` gọi `xep` trực tiếp 1 điểm; `test_day_change…` chỉ kiểm điểm đã thêm / đã bỏ) ⇒ harness kiểm Q2 (b) sau xếp lại theo chữ D5 (`_giu_khi_xep_lai`: ngày còn trong lịch, hợp sở thích mới / người dùng thêm, nhóm hạn chế không tối, ≤ 2 / ngày); trừ điểm bị hành động trực tiếp cùng lượt chạm. Đường dự phòng của code ("giữ làm khung phạm luật ⇒ xếp lại không giữ") sẽ hiện thành vi phạm (b) — đọc tay khi gặp |
| m-6 chuỗi dở | dòng "bỏ qua" tách "đủ lượt" / "DỞ (k / n lượt)"; không còn chuỗi ⇒ thoát, không nạp app |

[Chạy] sau sửa: `kiem` Q3 10 / 10, Q2 0 / 42 (kiểm (b) sau xếp lại không báo nhầm trên mô phỏng đúng nhãn); ca phá + ca ngược **13 / 13** (thêm: xếp lại không giữ chỗ · 2 dòng `chat_metrics` · kiểm cuối ở lượt đúng nhãn ⇒ Q3 vẫn đạt + liệt kê · Q4 chưa có khung ⇒ không đo được). Khoá giả: TD2 + AT1 ⇒ `khong_do` 3 (2 lượt lịch hỏng + TD2 lượt 2 "chưa có khung"), `q4_loi 0 / 0`; xoá dòng cuối AT1 ⇒ "DỞ: AT1 (1 / 2 lượt)"; `--tran 0` / `--dung 0` ⇒ dừng, `da_chay []`, `chua_chay` đúng. 0 USD.

**Lệnh (worktree nhánh đo, từ `backend/`):**
```bash
H=/home/minhhieu/hue_rag/data/phase_9/sua_lich/tools/chay_sua_lich.py; B=/home/minhhieu/hue_rag/data/phase_9/bo_do_sua_lich; K=/home/minhhieu/hue_rag/data/phase_9/sua_lich/do
# pilot (lần 1)
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python $H chay $B/chuoi_da_thay.jsonl $K/da_thay.jsonl --lan 1 --chi S01,S06 --tran 0.02   # --dung 0.19 mặc định (cả đợt, mọi file trong $K)
# phần còn lại lần 1, rồi lần 2; Q4 ×2
… chay $B/chuoi_da_thay.jsonl $K/da_thay.jsonl --lan 1 --tran <phần trần còn>   # chuỗi đã có ở lần 1 (pilot) tự bỏ qua, không chạy lại
… chay $B/chuoi_da_thay.jsonl $K/da_thay.jsonl --lan 2 --tran <…>
… chay $B/chuoi_q4.jsonl $K/q4.jsonl --lan 1 …; --lan 2
# chấm
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python $H cham $B/chuoi_da_thay.jsonl $K/da_thay.jsonl
# kín (User `!`, chỉ in số): chay $B/chuoi_sealed.jsonl $K/kin.jsonl --lan 1 / --lan 2 rồi cham … --so
```
