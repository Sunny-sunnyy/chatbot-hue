# Review: Đợt 7 Nhịp 2 (`H2.1a+H2.1b`, `H2.2a`, `H2.3b`, Cụm 3 `A0 + doi_chieu_canh_tranh`, `RUNBOOK §10`)

Decision: ready_for_user_confirmation
Người kiểm: E (verifier)
Date: 22:14 28/11/2026
Canonical guide: `data/thu_dot7_2026-11-28/KE_HOACH_DOT7.md` §3, `data/thu_dot7_2026-11-28/KET_QUA_NHIP2A.md`, `data/thu_dot7_2026-11-28/KET_QUA_NHIP2B.md`
Implementation report: `report_agent/2026-11-28/b_dot7_nhip2.md` (nhánh `origin/p24-b-dot7-nhip2` @ `4d382775fbda65beddc485bf0fe9e6dae4449719`, gồm `a0b95d1c`, từ `origin/main` `1e79ea0a`)

## 1. Phạm vi đã review

- Đọc toàn bộ exact diff `origin/main..4d382775` (`18` file, `+896/-74` dòng, `git diff --check` sạch), `report_agent/2026-11-28/b_dot7_nhip2.md`, `data/thu_dot7_2026-11-28/KET_QUA_NHIP2A.md`, `data/thu_dot7_2026-11-28/KET_QUA_NHIP2B.md`, `data/thu_dot7_2026-11-28/ung_vien_prompt_gpt6.py`, `tools/cit_cau.py`, `tools/serve_dot7_variant.py`, `tools/do_slide_dot7.py`, `backend/tests/test_dot7_nhip2a.py`, `backend/tests/test_dot7_nhip2b.py`, các đoạn chạm ở `backend/llm/assistant.py`, `backend/llm/slide_designer.py`, `backend/llm/nhan_anh.py`.
- Đối chiếu riêng 3 điểm trọng tâm theo giao việc:
  1. `0` giá trị `"none"` trong cấu hình/fallback của `slide_designer`: `backend/config/settings.yaml:70` (`low`), `backend/llm/assistant.py:490` (`low`, `timeout_seconds: 30`), `backend/llm/slide_designer.py:312` (fallback `"low"`).
  2. `H2.1b` khớp `tools/serve_dot7_variant.py`: `_viet_lai_trich_dan_cau` (`backend/llm/assistant.py:1859-1975`) kiểm `flags.kiem_trich_dan_cau and flags.uses_tools`, bỏ qua `fixed_outcome`/`citation_error`/`lich`/`lich_v2`/`REFUSAL_ANSWERS`/`not trace.cited`/`_la_luot_nguy_hiem_bao_lu`/`p1_xoa_luu_tru`, chụp `13` trường trước khi gọi `_goi_viet_lai` tối đa `1` lần, hoàn nguyên khi lỗi/từ chối/rỗng/mất trích dẫn/tăng `missing_count`, gán `trace.vet["cit_cau_viet_lai"] = True`, và đồng bộ cả `answer_query` (`2347`) lẫn đường stream (`2928-2947`: cập nhật `cho_kiem` qua `chu_cua_model(trace)` và nhánh không `cho_kiem` qua `thay_chu`).
  3. `guides/RUNBOOK_BAN_GIAO.md` §10 (`:397`) ghi đủ `H2.1a+H2.1b`, `H2.2a`, `H2.3b`, Cụm 3 (`A0` giữ mặc định `anh.che_do_tu_choi: mac_dinh` + `doi_chieu_canh_tranh`).
- Chạy chứng minh ĐỎ trên `origin/main` (`1e79ea0a`), chạy lại `14` file test offline chạm, chạy `5` ca dò biên `0 USD` + kiểm đếm cờ, và chạy tuần tự `12` file test phụ thuộc Qdrant `:6335` (`0 USD`, `--no-env-file`).

## 2. Findings

- **Không có `blocker` hay `major`.**
- **2 `minor` (không chặn chức năng thật):**
  1. `backend/llm/assistant.py:785-789` — Còn dư 1 dòng `return tim_kho` trùng lặp không tới được sau dòng `return tim_kho` đầu tiên (`#6` / dọn dẹp Nhịp 2A). Không ảnh hưởng hành vi runtime; có thể xoá ở lượt dọn sau.
  2. `report_agent/2026-11-28/b_dot7_nhip2.md:17` — Báo cáo ghi nhãn `("Cùng hạng", "Cao hơn", "Thấp hơn")`, trong khi code thật trong `backend/llm/goi_y_luu_tru.py:167-172` đặt `_HANG_NHAN = {"binh_dan": "bình dân", "vua": "vừa", "cao": "cao"}` (khớp `test_dot7_nhip2a.py:143-145`). Không ảnh hưởng code; chỉ là lỗi gõ nhầm trong báo cáo.
- **Ghi chú lỗi sẵn có ngoài phạm vi Đợt 7 Nhịp 2 (đã kiểm đối chứng trên `origin/main` `1e79ea0a`):**
  - `backend/tests/test_cong_dot_1.py::test_weather_and_feature_routes` ném `ValueError: assistant.goi_y_mua_nang needs assistant.tim_them, assistant.thoi_tiet and assistant.len_ke_hoach_v2` khi gọi `dataclasses.replace(OFF, thoi_tiet=False, bao_lu_cong_cu=False)` vì `backend/config/settings.yaml:117` đã bật `goi_y_mua_nang: true` từ Đợt 2 nhưng `CO_SUA_LICH_TAT` (`backend/tests/test_b5_lich_trinh.py:36`) chưa thêm `"goi_y_mua_nang": False`. Chạy đối chứng trực tiếp trên `1e79ea0a` cho cùng lỗi (`MAIN_EC=1`).

## 3. Cách người kiểm chạy lại thật

- **Diff & kiểm tra `reasoning_effort`:**
  - `git diff --check origin/main..HEAD`
  - `git grep -n 'reasoning' -- 'backend/config/settings.yaml' 'backend/llm/slide_designer.py' 'backend/llm/assistant.py'`
- **Chứng minh ĐỎ trên gốc `origin/main` (`1e79ea0a`):**
  - `UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest -o cache_dir=/tmp/pytest_cache_e tests/test_dot7_nhip2a.py tests/test_dot7_nhip2b.py -q`
- **Offline test chạm (`4d382775`):**
  - `UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest -o cache_dir=/tmp/pytest_cache_e tests/test_dot7_nhip2b.py tests/test_dot7_nhip2a.py tests/test_dot7_cum1.py tests/test_assistant_boundary.py tests/test_bedrock_model.py tests/test_luoi_cuoi_bao.py tests/test_noi_dong_tam_ngung.py tests/test_chat_stream.py tests/test_r4_numbers.py tests/test_nang_cap_2b_3a.py tests/test_dot5a_slide_designer.py tests/test_dot6_local.py tests/test_p10_anh.py tests/test_bo_toi_hoi_lai.py -q`
- **Dò biên `0 USD` (`check_sentence_citations`, `AssistantFlags`, `DOI_THU_MAC_DINH`):**
  - Chạy trực tiếp trên code `4d382775` bằng `uv run --no-sync --no-env-file python -c ...` kiểm `assistant_bools`, `5` ca biên `check_sentence_citations` và `DOI_THU_MAC_DINH`.
- **Qdrant `:6335` (tuần tự từng file trong `/tmp/hr_e_dot7_nhip2/backend`, `--no-env-file`, `0 USD`):**
  - `for f in tests/test_giu_chu_toi_kiem.py tests/test_cong_dot_1.py tests/test_citations.py tests/test_het_luot_viet_lai.py tests/test_noi_that_lam_thay.py tests/test_cau_nhieu_y.py tests/test_len_ke_hoach_v2.py tests/test_b2_tool_loop.py tests/test_nho_dap_chay_lai.py tests/test_het_luot_tim.py tests/test_dot4a_harness.py tests/test_api_chat.py; do UV_OFFLINE=1 HF_HUB_OFFLINE=1 uv run --no-sync --no-cache --no-env-file python -m pytest -o cache_dir=/tmp/pytest_cache_e "$f" -q; done`
  - Đối chứng `test_cong_dot_1.py -k test_weather_and_feature_routes` trên `origin/main` (`1e79ea0a`).

## 4. Kết quả quan sát

- **ĐỎ trên `origin/main` (`1e79ea0a`):** thất bại `ORIG_EXIT=2` với `ImportError: cannot import name 'check_sentence_citations' from 'llm.citations'`.
- **Offline test chạm trên `4d382775`:** `200 passed` trong `26.41s`; `git diff --check` sạch (`exit 0`).
- **Dò biên & đếm cờ trên `4d382775`:**
  - `assistant_bools`: `80` (`71 true / 9 false`), cộng `anh.bat: true` = `72 MỞ / 9 TẮT`.
  - `check_sentence_citations`: đạt `5/5` ca dò biên (`abbreviations_and_decimals -> True`, `meta_question_exempt -> True`, `meta_missing_info_with_number_NOT_exempt -> False`, `short_verdict_at_end_NOT_exempt -> False`, `domain_name_not_split -> True`).
  - `DOI_THU_MAC_DINH`: `21` cặp hợp lệ.
- **Test phụ thuộc Qdrant `:6335` (`0 USD`, `--no-env-file`):** `308 passed` trên `10/12` file sạch + `2` ca lỗi có giải thích rõ:
  - `test_giu_chu_toi_kiem.py`: `5 passed` (`17.25s`)
  - `test_cong_dot_1.py`: `22 passed, 1 failed` (`50.36s`; lỗi `test_weather_and_feature_routes` là lỗi sẵn có trên `origin/main @ 1e79ea0a`, đã chạy đối chứng xác nhận `MAIN_EC=1`)
  - `test_citations.py`: `10 passed` (`9.71s`)
  - `test_het_luot_viet_lai.py`: `13 passed` (`12.74s`)
  - `test_noi_that_lam_thay.py`: `63 passed` (`12.77s`)
  - `test_cau_nhieu_y.py`: `44 passed` (`14.12s`)
  - `test_len_ke_hoach_v2.py`: `96 passed` (`23.93s`)
  - `test_b2_tool_loop.py`: `12 passed` (`14.52s`)
  - `test_nho_dap_chay_lai.py`: `14 passed` (`18.91s`)
  - `test_het_luot_tim.py`: `7 passed` (`14.74s`)
  - `test_dot4a_harness.py`: `8 passed` (`16.75s`)
  - `test_api_chat.py`: `14 passed, 1 error` (`44.81s`; `ERROR` tại setup `test_health_is_cached_and_ready_after_real_lifespan` vì cố ý chạy `--no-env-file` thiếu `OPENAI_API_KEY`)
- Đã xoá sạch thư mục clone kiểm `/tmp/hr_e_dot7_nhip2`.

## 5. Giới hạn hoặc phần chưa chạy

- Mọi lượt kiểm trong review chạy với `0 USD` (`--no-env-file`, không gọi OpenAI thật); hành vi sinh thật của `H2.1a+H2.1b`, `H2.2a`, `H2.3b` và Cụm 3 căn cứ trên kết quả đo trong `KET_QUA_NHIP2A.md` và `KET_QUA_NHIP2B.md` kèm các unit/contract test xác định.
- Test cuối `test_health_is_cached_and_ready_after_real_lifespan` trong `test_api_chat.py` không chạy phần setup có key OpenAI do giữ kỷ luật `--no-env-file` (`0 USD`).

## 6. Decision và bước tiếp theo

- **Decision:** `ready_for_user_confirmation` — nhánh `origin/p24-b-dot7-nhip2` (`4d382775`) đạt toàn bộ tiêu chí nghiệm thu của Đợt 7 Nhịp 2 (`0 blocker`, `0 major`, `2 minor` không chặn), đủ điều kiện để `@coordinator` báo tổng kết Đợt 7 cho User xác nhận/gộp.

Một dòng cuối: Lượt review này KHÔNG gọi API OpenAI thật để kiểm `test_health_is_cached_and_ready_after_real_lifespan` hay sinh lại từ model; hướng rộng hơn là thêm `"goi_y_mua_nang": False` vào `CO_SUA_LICH_TAT` (`test_b5_lich_trinh.py`) để phục hồi `test_weather_and_feature_routes` ở nhánh dọn nhỏ tách riêng; phép đếm rẻ nhất tiếp theo là `0` đồng — kiểm `pytest tests/test_cong_dot_1.py` sau khi vá `CO_SUA_LICH_TAT`.
