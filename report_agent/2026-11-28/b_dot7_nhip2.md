# Báo cáo Nhịp 2 — Đợt 7 (`Mũi 2.1`, `Mũi 2.2`, `Mũi 2.3`, `Cụm 3` và 3 sửa dọn nhẹ)

- **Thời điểm:** 22:03 28/11/2026 (giờ hệ thống từ `date`)
- **Nhánh:** `p24-b-dot7-nhip2` (từ `origin/main` `1e79ea0a`; phần Nhịp 2A đã commit tại `a0b95d1c`)
- **Hồ sơ số đo nguồn:** `data/thu_dot7_2026-11-28/KET_QUA_NHIP2A.md`, `data/thu_dot7_2026-11-28/KET_QUA_NHIP2B.md` (tổng chi phí đo thật của đợt thử nghiệm: `$0,996905`)
- **Chi phí model trả phí phía `builder`:** `0 USD` (chỉ chạy test offline `UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file`)

## 1. Người dùng làm được / chưa làm được sau Nhịp 2

| Hạng mục | Người dùng làm được / thấy khác trước | Chưa làm trong Nhịp 2 / Tự hoãn |
|---|---|---|
| `Mũi 2.1 — H2.1a` (`P_GPT6`: `full_corpus_prompt.py`, `assistant.py`) | Chuẩn hoá `ANSWER_SYSTEM_INSTRUCTIONS`, `_LUAT_TU_CHOI`, `_LUAT_NHIEU_Y`, `ASSISTANT_TOOL_NOTE` và `TIM_KHO_MO_TA` (gắn vào `tim_kho.__doc__`) theo ứng viên GPT-6; giữ `reasoning_effort` mặc định (không nâng lên `high`). | — |
| `Mũi 2.1 — H2.1b` (`CIT_CAU`: `citations.py`, `assistant.py`, `settings.yaml`) | Bổ sung `split_sentences_vi` và `check_sentence_citations` (`verdict_meta_exempt`) trong `citations.py` (0 phụ thuộc mạng/SDK); đấu `_viet_lai_trich_dan_cau` sau cờ `AssistantFlags.kiem_trich_dan_cau` (mặc định code `False`, bật `kiem_trich_dan_cau: true` trong `settings.yaml` — `assistant:` có `71 true` / `9 false`). Khi câu trả lời hợp lệ có `[n]` còn câu thiếu `[n]`, gọi tối đa 1 lần `_goi_viet_lai` để bổ sung/giới hạn đúng đoạn có nguồn; lỗi hoặc biến thành từ chối thì giữ nguyên bản gốc; đồng bộ cả `answer_query` lẫn `answer_turn_stream` (`cho_kiem` và `thay_chu`). | — |
| `Mũi 2.2 — H2.2a` (`full_corpus_prompt.py`, `test_bo_toi_hoi_lai.py`) | Cập nhật `SUA_LICH_LOI_DAN_TOI_HOI_BO` khớp ứng viên `SUA_LICH_LOI_DAN_GPT6` cho sửa lịch mức 1, giữ `reasoning_effort: low`. | — |
| `Mũi 2.3 — H2.3b` (`settings.yaml`, `slide_designer.py`, `assistant.py`, `test_dot5a_slide_designer.py`) | Đổi `slide_designer_cfg.reasoning_effort: low`, `timeout_seconds: 30`, và tách 2 tin nhắn retry `[user_goc, user_loi]` qua `tao_loi_slide_designer` (giữ system prompt `565t` & prefix cache). | Chưa sửa giới hạn độ dài mục buổi tối của Slide AI (5/10 ca dài vượt nhẹ 1–27 ký tự trước lớp cắt tầng 3 của `dung_pptx_v2`; đã ghi vào `RUNBOOK_BAN_GIAO.md`). |
| `Cụm 3` (`nhan_anh.py`, `app.py`, `settings.yaml`, `test_nang_cap_2b_3a.py`) | Áp `NHAN_ANH_INSTRUCTIONS` (`A0`, static-first `developer` + `detail="auto"`, `NHAN_ANH_CACHE_KEY_MD = "hue_nhan_anh_a0_v1"`) làm `mac_dinh` mới; thêm chế độ thứ 4 `"doi_chieu_canh_tranh"` (`tao_agent_doi_chieu_canh_tranh`, `chon_cap_doi_chieu`, `dau_vao_canh_tranh`) đấu qua `doan_ten` và `app.py`. | Giữ `che_do_tu_choi: mac_dinh` theo quyết định chọn phương án nền `A0`; chưa bật mặc định `doi_chieu_canh_tranh` và không tích hợp Tesseract OCR. |
| 3 sửa dọn nhẹ (`test_len_ke_hoach_v2.py`, `goi_y_luu_tru.py`, `thoi_tiet.py`) | Sửa chuỗi thông báo lỗi `test_v2_flag_needs_table_and_fails_loudly` khớp code thật; bổ sung dấu tiếng Việt đầy đủ cho nhãn hạng lưu trú (`"Cùng hạng"`, `"Cao hơn"`, `"Thấp hơn"`) + cập nhật `test_dot7_cum1.py`; nới regex `_BO_AN_TOAN_GUI_XE` `{0,50}/{0,80}` trong `thoi_tiet.py`. | — |
| `guides/RUNBOOK_BAN_GIAO.md` §10 (`10.2` dòng `397`) | Ghi đầy đủ cập nhật cấu hình và giới hạn Đợt 7 Nhịp 2 cho `H2.1a+H2.1b`, `H2.2a`, `H2.3b` và `Cụm 3`. | — |

## 2. Lệnh kiểm chứng và kết quả chạy thật (sau chỉnh sửa cuối)

- **Chứng minh ĐỎ trên gốc (`origin/main` `1e79ea0a`) trước khi sửa Nhịp 2B:** chạy `tests/test_dot7_nhip2b.py` trên worktree tạm `origin/main` bị lỗi `ImportError: cannot import name 'check_sentence_citations' from 'llm.citations'`.
- **Kiểm tra cấu hình & mã sạch:**
  - Kiểm đếm cờ boolean trong `backend/config/settings.yaml` dưới `assistant:`: `assistant_bools: 80 true: 71 false: 9`; `anh.che_do_tu_choi: mac_dinh`; `slide_designer_cfg`: `reasoning_effort: low`, `timeout_seconds: 30`.
  - `git diff --check`: `exit 0` (không lỗi khoảng trắng).
  - `git grep -n -E "TIM_KHO_MO_TA|check_sentence_citations|split_sentences_vi|kiem_trich_dan_cau|cit_cau_viet_lai|doi_chieu_canh_tranh|NHAN_ANH_CACHE_KEY_MD|SUA_LICH_LOI_DAN_TOI_HOI_BO" -- backend/ guides/`: khớp mọi điểm định nghĩa và gọi hàm mới.
- **Bộ pytest offline tuần tự (`cd backend && UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest <file> -q`):**
  - **Đạt 100% (20 file đầy đủ + 3 tập con `-k` không Qdrant/API):**
    - `tests/test_dot7_nhip2b.py`: `4 passed` (`2.81s`; chạy `-v` trước đó: `4 passed in 2.67s`)
    - `tests/test_dot7_nhip2a.py`: `4 passed` (`3.38s`)
    - `tests/test_dot7_cum1.py`: `15 passed` (`5.10s`)
    - `tests/test_assistant_boundary.py`: `4 passed` (`3.76s`)
    - `tests/test_bedrock_model.py`: `28 passed` (`3.47s`)
    - `tests/test_luoi_cuoi_bao.py`: `11 passed` (`2.77s`)
    - `tests/test_noi_dong_tam_ngung.py`: `32 passed` (`2.70s`)
    - `tests/test_chat_stream.py`: `29 passed` (`2.80s`)
    - `tests/test_r4_numbers.py`: `6 passed` (`10.17s`)
    - `tests/test_nang_cap_2b_3a.py`: `9 passed` (`10.67s`)
    - `tests/test_dot5a_slide_designer.py`: `5 passed` (`7.16s`)
    - `tests/test_dot6_local.py`: `8 passed` (`11.61s`)
    - `tests/test_p10_anh.py`: `39 passed` (`10.85s`)
    - `tests/test_bo_toi_hoi_lai.py`: `6 passed` (`11.61s`)
    - `tests/test_sua_lich_v2.py`: `19 passed` (`12.46s`)
    - `tests/test_sua_lich_buoi_toi.py`: `8 passed` (`13.54s`)
    - `tests/test_sua_lich_kem_hoi.py`: `7 passed` (`13.27s`)
    - `tests/test_rao_so_ngay.py`: `47 passed` (`16.23s`)
    - `tests/test_luu_tru_lich.py`: `19 passed` (`23.61s`)
    - `tests/test_lich_pptx.py`: `15 passed` (`3.79s`)
    - `tests/test_cau_nhieu_y.py -k test_instructions_change_only_the_refusal_paragraph`: `1 passed, 43 deselected` (`2.62s`)
    - `tests/test_len_ke_hoach_v2.py -k test_v2_flag_needs_table_and_fails_loudly`: `1 passed, 95 deselected` (`12.58s`)
    - `tests/test_openai_full_corpus_generator.py -k "not real_environment and not empty_or_blank"`: `7 passed, 2 deselected` (`2.64s`)
  - **Các test yêu cầu Qdrant `:6335` đang tắt trong phiên `builder` (chưa kiểm ở phiên này, bàn giao `@verifier` chạy với Qdrant bật):**
    - `tests/test_giu_chu_toi_kiem.py`: `5 errors` (setup `deps` → Qdrant `:6335` `[Errno 111] Connection refused`).
    - `tests/test_cong_dot_1.py`: `6 passed, 6 failed, 11 errors` (`deps` / `app_client` cần Qdrant `:6335`).
    - Các test dùng fixture `deps` / `full_corpus_documents` khác (`test_citations.py`, `test_het_luot_viet_lai.py`, `test_noi_that_lam_thay.py`, 43 ca còn lại của `test_cau_nhieu_y.py`) chưa chạy ở bước offline này.

- **Phép này KHÔNG cho biết gì · hướng rộng hơn · đếm rẻ nhất:** Bộ test offline dùng `FakeGenerator` / đồ giả nên chưa kiểm chứng Qdrant `:6335` thật hay tương thích với các prompt/chức năng ở `test_giu_chu_toi_kiem.py` và `test_cong_dot_1.py`; khi `@verifier` chạy lại với Qdrant `:6335` bật (chi phí `0 USD` nhờ client kịch bản) sẽ kiểm được toàn bộ đường truyền tìm kho thật qua cả `answer_turn` lẫn `answer_turn_stream`.
