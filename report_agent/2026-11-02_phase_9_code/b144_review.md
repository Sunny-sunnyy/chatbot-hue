# Review: Phase 9 B4 — hỏi lại `hoi_lai` + nút chọn nhanh (nhánh `p9-b4`, B144)

## Vòng sớm `86c311b` (C163 · 21:31 03/11/2026 `date`)

Người kiểm: C (Claude Opus 5.5, `hue-rag-40`) — viết bộ đo B4 (C143) + nhãn chuẩn bị (C158), review plan B4; không code. Đối chiếu plan B4 bản 2 **duyệt `42fa62d2425f`** + report `b144_b4_implementation.md` `4a751ef3ad6f`.
`risk-gated-agent-review` · 0 USD (B đang chạy pilot có phí song song, không đo latency) · worktree riêng `/tmp/c_b4` (detach `86c311b`, gỡ khi xong) · ca dò private `data/phase_9/c163_review/`.

### 1. Cổng tối thiểu

| Cổng | Kết quả |
|---|---|
| Git | 2 commit `c4f2b76` (backend), `86c311b` (giao diện) trên merge-base `ac46c96`; `main` đã đi tiếp (tài liệu) ⇒ so theo merge-base, không so thẳng `main` |
| Đường dẫn đổi (merge-base..`86c311b`) | `api/routes/chat.py`, `config/settings.yaml` (`hoi_lai: false`), `llm/assistant.py`, `llm/full_corpus_prompt.py` (`HOI_LAI_NOTE`), `llm/generator_openai_full_corpus.py`, `llm/hoi_lai.py` (mới), `tests/test_b4_hoi_lai.py` (mới), `frontend/src/{App.jsx, index.css, stream.js}` — khớp plan §3; 0 gói npm mới |
| `git diff --check` | sạch |
| Ngoài phạm vi | không: `ANSWER_SYSTEM_INSTRUCTIONS` không đổi; cờ tắt |

### 2. Kiểm theo rủi ro (điểm A dặn)

| Điểm | Cách kiểm (C) | Kết quả |
|---|---|---|
| **422 trường lạ** | ca dò `do_hoi_lai.py` qua `/api/chat`: giá trị ngoài tập, sai kiểu (số), trường lạ, chữ tự do, trường thừa, `truong` là chuỗi | **6 / 6 ⇒ 422** (trước mọi việc) |
| **Câu ghép (D4)** | gọi thẳng `ghep_cau` | "<câu gốc> (Thông tin thêm: 2 ngày; có người lớn tuổi.)" từ bảng nhãn code; tất định; `{}` ("Trả lời luôn") ⇒ **đúng câu gốc** |
| **Không hỏi lại lần hai** | đọc `_offer_hoi_lai` (cờ ∧ `not da_co_truong`), `_model_query` (có `truong` ⇒ `da_co_truong`, kể cả `{}`) | lượt ghép / "Trả lời luôn" **không** đưa `hoi_lai` (thường + stream). **Đạt** |
| **Lần tìm đầu = câu gốc (m-3)** | đọc `prepare_answer` (`trace.search_query or query`), `_model_query` | lượt ghép tìm bằng câu gốc, gửi model câu ghép. **Đạt** |
| **`StopAtTools` đọc `final_output` trước ép kiểu** | đọc `_tools_result` (dùng chung `generate_with_tools` + `finish_answer_stream` khi có `state`) | `final_output` là dict có `loai` ⇒ `clarify`, **không** qua `parse_structured_output(AnswerOutput)`; nhánh thường như cũ. **Đạt** (đúng spec §3) |
| Tham số thô (M-1) | đọc `hoi_lai_for_turn` | `trace.hoi_lai_raw` ghi **trước** `loc_truong`; `hoi_lai_d3` "dien" / "cat" — harness đếm được |
| D3 ca biên | gọi thẳng `loc_truong` | trường loại khác ⇒ điền bắt buộc ("dien"); rỗng ⇒ bắt buộc; trùng ⇒ bỏ trùng; > 3 ⇒ 3 theo bảng ("cat"); **chỉ trường không bắt buộc ⇒ giữ nguyên, thẻ `bat_buoc` rỗng** (m-2) |
| Log (D9) | đọc `_copy_trace_metrics` | `hoi_lai` = {loai, n, d3}, `co_truong` = số — không giá trị trường |
| Nhớ (D5) | đọc `_remember` | lượt hỏi lại lưu câu gốc (câu trả lời rỗng); lượt ghép lưu câu ghép |
| **Giao diện / CSP** | `npm ci && npm run build` ở `86c311b`; đọc diff `App.jsx` | thẻ dựng từ `clarify` (dữ liệu code), không `innerHTML` mới, không `style` inline; `dist/index.html` 0 `style=`, CSS 0 URL ngoài; `test_static_ui.py` 3 / 3 |
| Test | `test_b4_hoi_lai` `test_b3_memory` `test_b2_tool_loop` `test_chat_stream` `test_feedback` (không khoá) | **53 / 53** |

Bất biến đã kiểm: cờ `hoi_lai` tắt ⇒ `_offer_hoi_lai` False ⇒ lời dặn + công cụ như trước (đọc code; Q1 giống byte là việc của B ở lượt đo).

### 3. Findings (vòng sớm)

**0 blocker · 0 major · 3 minor.**

- **m-1 — stream phát nhãn "đã tìm" sau lần gọi `hoi_lai`.** `answer_turn_stream` lọc `tool_called` của `hoi_lai` (không "đang tìm") nhưng nhánh `tool_output` **không lọc** ⇒ trước thẻ hỏi lại vẫn có `status: searched` + `n_sources`. Tác động: thứ tự nhãn D9 (b) lệch một nhịp ("đã tìm kho" khi không tìm thêm). Đóng: lọc `tool_output` của `hoi_lai` như `tool_called` (hoặc ghi lý do giữ) + một test thứ tự sự kiện.
- **m-2 — thẻ chỉ có trường không bắt buộc ⇒ "Gửi" bật ngay = "Trả lời luôn".** `loc_truong("lich_trinh", ["so_thich"])` ⇒ thẻ `bat_buoc` rỗng (ca dò); `Clarify.ready = bat_buoc.every(…)` ⇒ true khi chưa chọn gì; lượt ghép sau đó **không** hỏi lại lần hai ⇒ câu lịch trình thiếu `so_ngay` đi tiếp không số ngày. Đúng chữ D3 ("code không tự thêm trường") nhưng hệ quả này chưa ghi. Q2 (đếm thô ⊇ `thieu_bat_buoc`) **bắt** được về mặt đo. Đóng: ghi rõ hệ quả trong report (hoặc A chọn: code thêm trường bắt buộc khi model hỏi `loai` đó mà thiếu bắt buộc — đổi D3, cần A).
- **m-3 — đếm ngân sách token chưa tính lược đồ công cụ thứ hai.** `_token_count` cộng đệm đường công cụ hiệu chỉnh khi chỉ có `tim_kho` (B2 / C145); khi đưa `hoi_lai`, lược đồ công cụ + `HOI_LAI_NOTE` vào thân yêu cầu (ghi chú đã được đếm qua lời dặn, lược đồ thì không) ⇒ `usage − builder` tăng. Đóng: báo `usage − builder` (max) trên pilot / đã thấy với cờ bật, < 512 như B3 Q8.

### 4. Giới hạn

- Không chạy lượt có phí, không chạy server / Playwright (B đang pilot); không kiểm chuỗi gửi model thật (Q1) — việc của B.
- `_tools_result` kiểm bằng đọc code + test của B (client giả SDK); C không dựng kết quả SDK giả riêng.

### 5. Kết luận vòng sớm

**Không có finding chặn** ở `86c311b`. m-1, m-2, m-3 sửa hoặc ghi lại trước review cuối. Review cuối: phần thêm sau `86c311b` + bằng chứng có phí (Q1–Q8) + phần kín B4 (C chạy, 10 câu).
