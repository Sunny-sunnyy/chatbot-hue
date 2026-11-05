# Implementation Report: Phase 9 — sửa lịch nhiều lượt (`sua_lich`, B163 + B164)

Người làm: B (Claude Code, Opus 5.5)
Date: 19:25 05/11/2026 (`date`) — code B163 commit 16:49 05/11; phần kiểm B164 tối 05/11
Plan: `docs/superpowers/plans/2026-11-05-phase-9-sua-lich-plan.md` bản 3 sha `5b68f3cb666a` (A duyệt 13:31 05/11, review E vòng 2 ready)
Nhánh: `p9-sua-lich` `1c53627` (đã push) — gốc `b1fcbc4`; `main` hiện `2693422` chỉ thêm tài liệu (`git diff b1fcbc4 main -- backend frontend` rỗng) ⇒ chưa cần rebase.
Worktree: `/tmp/b_sualich` (tạo lại tối 05/11 sau khi máy khởi động lại; symlink `data/`, `knowledge-base-hue/`).

## 1. Phạm vi

- **Đã làm (bước 2 của plan §6, 0 USD):** code D1–D11 + test, cờ `sua_lich: false`.
- **Chưa làm:** Q1 + Q1m (cần Qdrant — chờ C192 dựng lại chỉ mục), test đường nối dùng Qdrant, build giao diện; pilot + đã thấy ×2 + vòng chỉnh + khoá + kín + Q4 + Q8 (có phí — **chỉ sau khi `lich_trinh` bật**, tức sau khi User chấm Q3 của B5).

## 2. Thay đổi chính

| File | Việc |
|---|---|
| `backend/llm/sua_lich.py` (mới) | Hành động có tên (`HanhDong`, enum 6 loại, `extra="forbid"`, ≤ 3 / lần gọi); `ap_hanh_dong` áp **≤ 2** theo thứ tự (D4), hành động thứ 3 ⇒ "Chưa làm"; phạm luật B5 ⇒ "Không đổi được … vì …"; `_xep_lai` gộp tham số chỉ nhận trường **khác** giá trị đã lưu (D5); `_lua_chon_thay` + `the_chon` (D6: 2–3 điểm cùng cụm + nút "Bỏ điểm này"); `khoi_sua` (khối D7 do code nối); `luu_tu_lich` (D1). |
| `backend/llm/lich_trinh.py` | `xep(bang, ts, giu=None, loai=frozenset())` — điểm giữ chỗ đặt trước khi lấp, điểm đã bỏ không bao giờ chọn lại; mặc định = B5. |
| `backend/llm/assistant.py` | `ROUTE_INPUTS` thêm `lich_cu`, `sua_chon` (#6 — điều kiện dừng §8 của plan); công cụ `sua_lich` chỉ dựng khi trace có `lich_cu` (D2); `sua_lich` ghi `trace.lich_moi`, không đụng `lich_cu`; trần ≤ 1 / lượt, không cùng `lich_trinh` (D10). |
| `backend/llm/generator_openai_full_corpus.py`, `full_corpus_prompt.py` | Công cụ thứ ba `sua_lich` (mô tả ngắn `SUA_LICH_MO_TA`, **không** thêm lời dặn hệ thống — D8); dừng lượt khi `sua_lich` trả thẻ chọn (như thẻ hỏi lại B5). |
| `backend/api/conversations.py` | `Conversation.lich` + `lich()` / `set_lich()` — luôn bản sao sâu (D1, review E M-1). |
| `backend/api/routes/chat.py` | Đặt `trace.lich_cu` từ khung đã lưu; lưu khung **chỉ** sau lượt có lịch qua kiểm cuối, tuyến cuối `tro_ly_hue`; nhận `sua_chon` từ nút, kiểm `moi` ∈ danh sách code đã đưa (sai ⇒ 422). |
| `backend/retrieval/full_corpus_context.py` | `SUA_LICH_TOOL_OVERHEAD = 400` — số ước, pilot đo lại (như B5 D16). |
| `backend/config/settings.yaml` | `sua_lich: false`. |
| `frontend/src/App.jsx`, `stream.js` | Thẻ chọn điểm thay, bước tiến độ `da_doi` / `khong_doi` / `chua_lam`. |
| `backend/tests/test_sua_lich.py` (mới) | 13 test: mỗi hành động + một ca cố tình vi phạm; bất biến D5; ca 3 hành động; ca Travel-AI ×2 (điền lại tham số cũ ⇒ 0 dòng "Đã đổi"; bỏ sở thích); khung đã lưu không bị sửa tại chỗ; 4 test đường nối qua `create_app` / SDK thật + client kịch bản (test (i)–(iv) của plan §3, `sua_chon` sai ⇒ 422, cờ tắt / chưa có khung ⇒ yêu cầu như B5). |

## 3. Cách đã chạy thật (B164, 0 USD)

Từ `/tmp/b_sualich/backend`:

```bash
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest -q -p no:cacheprovider \
  <9 test thuần của tests/test_sua_lich.py> <15 test thuần của tests/test_b5_lich_trinh.py> tests/test_assistant_boundary.py
# xep() nhánh ↔ main: cùng script, chạy ở backend/ của main (/home/minhhieu/hue_rag/backend) và của nhánh
HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python /tmp/b164/xep_dump.py <out.txt>; cmp main.txt nhanh.txt
```

`xep_dump.py`: mọi tổ hợp 4 số ngày × 6 người đi cùng (gồm trống) × 3 kiểu đi × 6 sở thích × 29 lựa chọn thêm điểm (không thêm + từng điểm
trong 28 điểm của bảng) = 12.528 lần `xep` (gọi kiểu B5, không `giu` / `loai`), sha từng khung.

Chỉ chọn test **không đọc Qdrant** vì C192 có thể đang dựng lại chỉ mục (A cấm đọc Qdrant tới khi báo xong).

## 4. Kết quả quan sát

- **Test thuần: 72 passed** (9 sua_lich + 15 B5 (gồm các ca tham số hoá) + `test_assistant_boundary.py`) [Chạy].
- **`xep` mặc định = B5: 12.528 / 12.528 khung giống hệt `main`**, sha tổng `f05d8a49514e` cả hai bên [Chạy] ⇒ điều kiện dừng §8 "`xep(giu, loai)` làm đổi kết quả lượt lịch đầu" **không xảy ra** (tập này chứa mọi tham số của 13 câu đã thấy, trừ câu thêm ≥ 2 điểm — chưa phủ).
  Commit B163 ghi "2.160 tổ hợp giống" — đó là lần kiểm lúc code, không để lại file; lần này thay bằng tập lớn hơn.
- **Sau C192 (19:50 05/11/2026, chỉ mục mới 8.435 điểm, build record `9921888f2030`) [Chạy]:**
  - **Q1 ĐẠT: 228 / 228 giống byte** — `capture_all.py` chạy ở `main` `2693422` và nhánh `1c53627`, cùng chỉ mục; `cmp` giống; sha file `dba1f578eef1` cả hai (`data/phase_9/sua_lich/q1/main_2693422.jsonl`, `nhanh_1c53627.jsonl`; mỗi ca 2 lần bắt).
  - **Q1m ĐẠT: 228 / 228 giống byte** — trên nhánh, `lich_trinh` bật + `sua_lich` bật ↔ `lich_trinh` bật + `sua_lich` tắt (script `/tmp/b164/capture_flags.py` bật cờ trong bản sao settings rồi chạy `capture_all.py` nguyên, không bỏ mục nào); sha `ac53ea9046f3` cả hai (`q1m_lich1_sua0.jsonl`, `q1m_lich1_sua1.jsonl`). Kiểm chéo: bản `lich_trinh` bật **khác** `main` (đúng — có mục công cụ `lich_trinh`). Lượt đơn không có khung đã lưu ⇒ công cụ `sua_lich` không được đưa (D2).
  - **Test: 165 passed** — `test_sua_lich.py` (cả 4 test đường nối), `test_b5_lich_trinh.py`, `test_b2_tool_loop.py`, `test_b3_memory.py`, `test_toc_do_song_song.py`, `test_assistant.py`, `test_static_ui.py`, `test_chat_stream.py`, `test_assistant_boundary.py`, `test_feedback.py`.
  - **Build giao diện** `npm ci && npm run build` ở worktree: xong (dist 314,55 kB JS).
  - Không chạy: `test_api_chat.py`, `test_openai_full_corpus_generator.py` (cần khoá OpenAI — `Project_Status.md` §8).
- **NOT RUN (chờ `lich_trinh` bật):** Q2–Q5, Q8 (có phí, trần 0,20 / dừng 0,19).
- Tiền B163 + B164: **0 USD**.

## 5. Lỗi và giới hạn

- `SUA_LICH_TOOL_OVERHEAD = 400` là số ước; pilot đo lại chênh token lược đồ công cụ (Q5).
- `Conversation.lich` lưu `cau_goc` (câu người dùng của lượt lịch) — đúng D1 của plan, nhưng §1 plan ghi "không lưu chữ tự do của người dùng". Câu này chỉ nằm trong RAM của cuộc (cùng TTL 30 phút với câu hỏi đã nhớ ở B3), không log, không ghi đĩa. Người review xem có cần đổi thành câu do code dựng hay không.
- Khung lưu trong RAM mất khi khởi động lại server (plan §10 đã ghi).
- Test đường nối dùng client kịch bản ⇒ không phải bằng chứng model chọn đúng hành động (phần đó là Q3, có phí).

## 6. Bàn giao cho người kiểm

- Đọc trước: plan bản 3 (D1–D11, §3 danh sách test, §8 điều kiện dừng), rồi `backend/llm/sua_lich.py` `ap_hanh_dong`, `assistant.py` chỗ dùng `lich_cu`, `chat.py` chỗ lưu khung.
- Q1 / Q1m / test / build đã chạy (§4). C chạy `data/phase_9/sua_lich/tools/mo_phong.py` + `kiem_bo` trên code nhánh (đã thấy 10 + kín 5, chỉ số đếm).
- Review cả nhánh sau khi đo xong (plan §6 bước 5).
