# Review: Đợt 7 Cụm 1 (`P0–P18` trừ `P5`)

Decision: ready_for_user_confirmation
Người kiểm: E (verifier)
Date: 19:15 28/11/2026
Canonical guide: `data/thu_dot7_2026-11-28/KE_HOACH_DOT7.md` §2
Implementation report: `report_agent/2026-11-28/b_dot7_cum1.md` (nhánh `origin/p24-b-dot7-cum1` @ `937cf3777eaab1b234ccba005de950c7477754e1`, vòng 1 @ `db2ec618754b8ad735f293386fce9e55c6bf3025`, từ `origin/main` `7aaface284f5f53254d89003d9be070311ff17d7`)

## 1. Phạm vi đã review

- **Vòng 1 (`db2ec618`):** Đọc toàn bộ exact diff `origin/main..db2ec618` (24 file, +1002/-96 dòng) và `report_agent/2026-11-28/b_dot7_cum1.md`; chứng minh ĐỎ trên gốc `7aaface2` (`15 failed`); chạy lại 10 file test chạm (`97 passed`), `frontend` build (`607ms`), `git diff --check`, các ca dò biên 0 USD, và 1 lượt Playwright Chromium thật `1536×695` trên `uvicorn` cổng tạm `8017`.
- **Vòng 2 (`937cf377`):** Đọc exact delta `db2ec618..937cf377` (`backend/llm/assistant.py`, `backend/tests/test_dot7_cum1.py`, `report_agent/2026-11-28/b_dot7_cum1.md`); kiểm tra đóng Finding 1 (`major` `P1`) và minor #3 (`P3`); chạy lại toàn bộ các file test chịu ảnh hưởng của delta (`65 passed`) và `git diff --check`; dọn sạch `/tmp/hr_e_dot7_cum1` và tắt cổng `8017`.

## 2. Findings

- **Không còn `blocker` hay `major`.**
- **Finding 1 (`major` — An toàn `P1`, ĐÃ ĐÓNG ở `937cf377`):**
  - *Bản sửa:* `_finish_generated` (`backend/llm/assistant.py:2177–2185`) khi gặp `trace.goi_y_luu_tru` trên lượt nguy hiểm bão/lũ luôn xoá `trace.goi_y_luu_tru`, lọc `gylt.NGUON_SOURCE` khỏi cả `trace.so_nguon` và `trace.cited`, gán `text = trace.answer = tt.CAU_DAN_BAO_LU`, đặt `trace.citation_error = None` và đánh dấu `trace.vet["p1_xoa_luu_tru"] = True` trước `kiem_so_sau_khi_viet` / `_kiem_tra_luu_tru`; `answer_turn_stream` (`2831–2835`) phát `chu_cua_model(trace)` thay cho `cho_kiem` cũ khi `p1_xoa_luu_tru` bật.
  - *Kiểm chứng:* `tests/test_dot7_cum1.py::test_p1_bao_lu_lan_dau_va_dao_thu_tu_tool_chan_luu_tru_va_giu_112` đã sửa `q_dao` và kiểm đủ cả Ca A (trích `[99]` KB), Ca B (số lạ `"35°C"` kèm `NGUON_SOURCE`) và Ca C (`cho_kiem` stream).
- **2 `minor` còn lại (không chặn, đúng nguyên tắc không mở vòng sửa riêng):**
  1. `P4` (`backend/llm/goi_y_luu_tru.py:167–171`): `ghi_chu_noi_hang` hiển thị `"hạng vua"` / `"binh_dan"` thay vì chữ tiếng Việt có dấu (`"vừa"`, `"bình dân"`).
  2. `P0` (`backend/llm/thoi_tiet.py:144`): `_BO_AN_TOAN_GUI_XE` giới hạn `{0,35}` ký tự giữa `gửi xe` và `an toàn` nên câu dài > 35 ký tự ở giữa vẫn trả `True`.

## 3. Cách người kiểm chạy lại thật

- **Vòng 2 (`937cf377`):**
  - `git diff --check origin/main..HEAD`
  - `UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest tests/test_dot7_cum1.py tests/test_luoi_cuoi_bao.py tests/test_chat_stream.py tests/test_assistant_boundary.py tests/test_r4_numbers.py -v`
- **Vòng 1 (`db2ec618` — bằng chứng dùng lại cho phần không đổi):**
  - `UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest tests/test_dot7_cum1.py tests/test_assistant_boundary.py tests/test_dot5a_slide_designer.py tests/test_dot5a_ics_deeplink.py tests/test_dot6_local.py tests/test_mua_nang.py tests/test_hoan_tac.py tests/test_ho_so_chu_de.py tests/test_chat_stream.py tests/test_static_ui.py -v`
  - `cd frontend && npm run build`
  - Playwright Chromium `1536×695` trên `uvicorn` cổng `8017` (`HUE_LUOT_MOI_NGAY=3`, `slide_designer_cfg.use_llm=True`).

## 4. Kết quả quan sát

- **Fresh ở vòng 2 (`937cf377`):** `65 passed` trong `14.08s` (`test_dot7_cum1.py` 15, `test_luoi_cuoi_bao.py` 11, `test_chat_stream.py` 29, `test_assistant_boundary.py` 4, `test_r4_numbers.py` 6); `git diff --check` sạch (`exit 0`).
- **Evidence reuse hợp lệ từ vòng 1 (`db2ec618`):** Vòng 2 chỉ sửa `backend/llm/assistant.py` (phần `_finish_generated`/`cho_kiem`/`_GIA_TIEN_LUU_TRU`), `backend/tests/test_dot7_cum1.py` và `b_dot7_cum1.md`, không chạm `frontend/` hay các module tách biệt (`thoi_tiet.py`, `mua_nang.py`, `ho_so_chu_de.py`, `slide_designer.py`, `lich_ics.py`, `xuat.py`, `hoan_tac.py`, `gioi_han.py`, `conversations.py`). Vì vậy các kết quả đạt từ `db2ec618` (`frontend` build `607ms`, Playwright `1536×695` kiểm OTA + PPTX AI→nhanh + hoàn tác giữ 112 + 429 ảnh với `0` tràn khung / `0` page error, và `test_dot5a_*`, `test_dot6_local.py`, `test_mua_nang.py`, `test_hoan_tac.py`, `test_ho_so_chu_de.py`, `test_static_ui.py`) giữ nguyên giá trị.

## 5. Giới hạn hoặc phần chưa chạy

- Qdrant `:6335` tắt trong sandbox và chạy `--no-env-file`, nên chưa chạy lại 8 file test phụ thuộc Qdrant/route retrieval và chưa gọi live OpenAI (`0 USD` đúng kỷ luật Nhịp 1).
- Trong Playwright, lượt SSE chat dùng payload sinh trực tiếp từ `goi_y_luu_tru_for_turn` + `StreamEvents.finish`, còn `/api/lich/hoan_tac`, `/api/lich/pptx` và `/api/anh/ung_vien` (429) chạy trên FastAPI thật.

## 6. Decision và bước tiếp theo

- **Decision:** `ready_for_user_confirmation` — toàn bộ `P0–P18` (trừ `P5` thuộc Nhịp 2) trong phạm vi Nhịp 1 đã đạt, có thể gộp vào bước tiếp theo / mở Nhịp 2 theo điều phối của `@coordinator`.

Một dòng cuối: Lượt review này KHÔNG cho biết hành vi thật của `gpt-6-luna` và 8 file test phụ thuộc Qdrant `:6335`; hướng rộng hơn là tách 4 nguyên tắc prompt & hậu kiểm ở Nhịp 2 theo đúng `KE_HOACH_DOT7.md` §3; phép đếm rẻ nhất tiếp theo là chạy A/A baseline hậu Nhịp 1 khi Qdrant và `.env` được bật ở Nhịp 2.
