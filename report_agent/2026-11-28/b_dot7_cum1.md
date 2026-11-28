# Báo cáo Nhịp 1 — Cụm 1 Đợt 7 (`P0–P18` trừ `P5`)

- **Thời điểm:** 18:57 28/11/2026 (giờ hệ thống từ `date`)
- **Nhánh:** `p24-b-dot7-cum1` (từ `origin/main` `7aaface2`)
- **Chi phí model trả phí:** `0 USD` (chỉ chạy test offline `--no-env-file` và build frontend)

## 1. Người dùng làm được / chưa làm được sau Cụm 1

| Hạng mục | Người dùng làm được / thấy khác trước | Chưa làm trong Nhịp 1 / Tự hoãn |
|---|---|---|
| `P0` (`thoi_tiet.py`) | Hỏi địa hình/đường đèo bị *"sạt"* kích hoạt kiểm tra bão/lũ và cảnh báo; đối chứng *"phí gửi xe qua đêm"* và *"an toàn gửi xe"* vẫn giữ `False`. | — |
| `P1` (`assistant.py`) | Lượt bão/lũ chặn `goi_y_luu_tru` & `goi_y_phuong_an_mua_nang` cả khi chạy lại (`bao_lu_lan_dau`) lẫn khi model gọi `goi_y_luu_tru` trước `thoi_tiet("bao_lu")` (dọn ngược cuối lượt). | — |
| `P2` (`mua_nang.py`) | Mưa lớn `>= 100mm` vẫn bị chặn dù `ngay=None` (kiểm ở `ngay_kiem=0`), đồng thời giữ `dong_du_bao=None`. | — |
| `P8` (`conversations.py`, `hoan_tac.py`, `chat.jsx`) | Hoàn tác lịch bảo toàn `an_toan` còn hiệu lực, trả ra JSON `/api/lich/hoan_tac`, cập nhật `noticeAnToan` trên UI và giữ vào PPTX/Sổ tay. | — |
| `P18` (`ho_so_chu_de.py`, `routes/ho_so.py`) | Sổ tay chỉ đánh dấu `bai_da_co` khi trích dẫn nằm đúng đoạn cảnh báo của chính bài đó, không bị bài khác che mất cảnh báo. | — |
| `P4+P3+P11` (`goi_y_luu_tru.py`, `assistant.py`, `conversations.py`, `routes/chat.py`, `chat.jsx`, `theKhachSan.js`) | Ghi rõ `da_noi_hang` khi nới hạng; chặn nhớ đáp (`dap_duoc_nho`) & hậu kiểm giá/phòng trống khi có `goi_y_luu_tru`; phát dữ liệu lưu trú có kiểu qua SSE `luu_tru` và `ChatResponse.luu_tru` để UI tự dựng thẻ + 3 link OTA từ dữ liệu hệ thống. | — |
| `P9` (`slide_designer.py`) | `hau_kiem_slide_deck` kiểm đủ `overview_summaries[*]` (số ngày + URL/từ cấm) và khớp `day_number` của từng `id_muc` với ngày gốc. | Chưa đổi `slide_designer_cfg.reasoning_effort` (thuộc Nhịp 2). |
| `P10` (`len_ke_hoach.py`, `xuat.py`, `hanh_trinh_chuan.py`, `lich_ics.py`, `lich_ics.js`) | Sinh `lich_id` độc lập, giữ qua sửa/hoàn tác/lưu lượt và nhúng vào `UID` `.ics` cả Python lẫn JS, không làm đổi `itinerary_hash` của cache PPTX. | — |
| `P12` (`generator_openai_full_corpus.py`) | `xin_cong_cu_da_an` chỉ kích hoạt với lỗi tool bị ẩn/tắt (`not found` / `disabled`), không phân nhầm `Invalid JSON input` của tool đang mở. | — |
| `P13+P14` (`routes/xuat.py`, `gioi_han.py`, `test_dot5a_slide_designer.py`) | Chỉ đọc/lưu cache AI khi `use_llm=True` & `used_llm=True`; `GET` chỉ đọc/sinh từ code; `POST` khi `use_llm=false` trả `409` (`slide_ai_disabled`) không trừ quota AI trọng số 3; gắn header `X-Slide-Source` (`ai` / `cache_ai` / `code`). | Đã cập nhật `tests/test_dot5a_slide_designer.py` khớp hợp đồng mới từ `KE_HOACH_DOT7.md` §2.2. |
| `P15` (`chat.jsx`) | Xoá `daTim`, `nSources`, `buoc`, `progress` khi gặp `thay_chu` rỗng hoặc sang `routing` mới sau đó. | — |
| `P17` (`ho_so_chu_de.py`, `routes/ho_so.py`) | Trả cờ `dung_du_phong` đồng nhất từ `kiem_dan_y_co_co`, chặn lưu cache khi dàn ý bị fallback rỗng. | — |
| `P6` (`HoiBangAnh.jsx`) | Phân biệt HTTP `429` (hết lượt) và HTTP `200` + `du.loi` với nhánh không nhận ra ảnh. | — |
| `P7` (`routes/chat.py`, `RUNBOOK_BAN_GIAO.md`) | `StreamEvents.finish` đối chiếu `"".join(self.shown)` nguyên trạng, không rstrip `\n` làm gãy bảng Markdown. | — |
| `P16` (`RUNBOOK_BAN_GIAO.md`) | Đã ghi rõ giới hạn hiện hành (`P0` không mở cho mọi chữ `"sạt"` ngoài ngữ cảnh địa hình/đường, `P7` dùng `StreamEvents`, `P16` giới hạn bản bàn giao). | — |

## 2. Lệnh kiểm chứng và kết quả chạy thật (sau chỉnh sửa cuối)

- **Chứng minh ĐỎ trên gốc (`origin/main` `7aaface2`) trước khi sửa:** `tests/test_dot7_cum1.py` chạy `15 failed` (toàn bộ 15 ca `P0–P18`).
- **Chạy mới trên nhánh `p24-b-dot7-cum1` (`UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest <file> ...`):**
  - `tests/test_dot7_cum1.py -v`: **`15 passed`** (`5.37s`)
  - `cd frontend && npm run build`: **`✓ built in 663ms`** (`72 modules transformed`)
  - `git diff --check`: **exit 0** (không lỗi khoảng trắng)
  - `git grep -n -E 'co_dau_hieu_thoi_tiet_hoac_nguy_hiem|_la_luot_nguy_hiem_bao_lu|ket_qua_co_kieu|luu_tru_cho_giao_dien|hau_kiem_slide_deck|kiem_dan_y_co_co|bai_canh_bao_da_co|xin_cong_cu_da_an|lich_id' -- backend/ frontend/`: khớp đầy đủ các điểm gọi đã sửa.
- **Các file test hiện có chạy tuần tự từng file (mỗi file 1 tiến trình):**
  - **Đạt 100% (19 file):**
    - `test_assistant_boundary.py`: `4 passed`
    - `test_dot5a_slide_designer.py`: `5 passed`
    - `test_dot5a_ics_deeplink.py`: `5 passed`
    - `test_dot6_local.py`: `8 passed`
    - `test_mua_nang.py`: `8 passed`
    - `test_hoan_tac.py`: `5 passed`
    - `test_ho_so_chu_de.py`: `13 passed`
    - `test_chat_stream.py`: `29 passed`
    - `test_the_khach_san.py`: `1 passed`
    - `test_luoi_cuoi_bao.py`: `11 passed`
    - `test_lich_pptx.py`: `15 passed`
    - `test_luu_tru_lich.py`: `19 passed`
    - `test_sua_lich_v2.py`: `19 passed`
    - `test_cong_cong_cu.py`: `39 passed`
    - `test_nguon_bao_lu.py`: `2 passed`
    - `test_so_tay.py`: `41 passed`
    - `test_static_ui.py`: `5 passed`
    - `test_noi_dong_tam_ngung.py`: `32 passed`
    - `test_r4_numbers.py`: `6 passed`
  - **Lỗi môi trường cục bộ do Qdrant `:6335` chưa bật (`Connection refused` / FastAPI `503 retrieval_unavailable`) và chạy `--no-env-file` thiếu `OPENAI_API_KEY`:**
    - `test_b5b_thoi_tiet.py`: `90 passed, 30 errors` (Qdrant `:6335`)
    - `test_cache_tra_loi.py`: `20 passed, 5 failed` (`503 retrieval_unavailable`)
    - `test_len_ke_hoach_v2.py`: `85 passed, 7 failed, 4 errors` (`503 retrieval_unavailable` & Qdrant `:6335`)
    - `test_api_chat.py`: `10 passed, 4 failed, 1 error` (`503 retrieval_unavailable` & `require_openai_key`)
    - `test_b2_tool_loop.py`: `1 passed, 11 errors` (Qdrant `:6335`)
    - `test_nho_dap_chay_lai.py`: `2 passed, 1 failed, 11 errors` (`503` & Qdrant `:6335`)
    - `test_het_luot_tim.py`: `1 passed, 6 errors` (Qdrant `:6335`)
    - `test_dot4a_harness.py`: `2 passed, 6 errors` (Qdrant `:6335`)
    - `test_openai_full_corpus_generator.py`: `7 passed, 2 errors` (`require_openai_key`)

- **Phép này KHÔNG cho biết gì · hướng rộng hơn · đếm rẻ nhất:** Các phép test offline không kiểm chứng luồng gọi OpenAI thật (GPT-6-luna / Slide AI / sửa lịch LLM) hay truy vấn Qdrant `:6335` đang tắt; khi `@verifier` kiểm với Qdrant bật sẽ phủ được 8 file `503`/Qdrant nêu trên mà không tốn API key (trừ 2 ca `require_openai_key`), còn chất lượng model GPT-6 thực tế đo ở Nhịp 2 theo `KE_HOACH_DOT7.md` §3.
