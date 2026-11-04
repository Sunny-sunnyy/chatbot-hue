# Review: B154 — dòng mở câu soạn sẵn khẩn cấp PA1 (`p9-chu-khan-cap` `e6a011c`)

Người kiểm: C (việc **C168**, A giao) · 20:29 04/11/2026 (`date`) · 0 USD (không server, không lượt có phí). Skill `risk-gated-agent-review`.

## 1. Phạm vi + cổng tối thiểu

- Nhánh `p9-chu-khan-cap` = 1 commit `e6a011c` trên `main` `7460b42` (merge-base); `git diff main...p9-chu-khan-cap`: **2 file** — `backend/llm/emergency.py` (+2 / −1), `backend/tests/test_emergency.py` (+6); `git diff --check` sạch; không file ngoài phạm vi.
- Yêu cầu (A, handoff "A quyết + duyệt" 04/11 + mục C162): đổi **chỉ dòng mở** `EMERGENCY_ANSWER` theo PA1 User chọn; 4 dòng còn lại giữ; test khoá chữ; tuyến không đổi.

## 2. Đối chiếu

| Tiêu chí | Kiểm | Kết quả |
|---|---|---|
| Dòng mở = nguyên văn PA1 | so chuỗi trong code với `data/phase_9/khan_cap_buoc0/chu_moi_phuong_an.md` (sha `a0bc71cbfaff`, tính từ file) dòng 19 — khớp nguyên văn (script so chuỗi) | đạt |
| 4 dòng còn lại byte giống `main` | diff `emergency.py` chỉ 1 dòng chuỗi `-` / 1 dòng chuỗi `+` (+ 1 dòng comment); `EMERGENCY_ANSWER` vẫn 5 dòng | đạt |
| Test khoá 5 dòng | `test_answer_is_exact_approved_text_with_four_numbers`: dòng 0 (PA1), dòng 1 (4 số, có sẵn), dòng 2–4 khoá nguyên văn | đạt |
| Test chạy | worktree tạm detach `e6a011c`: `test_emergency.py` + `test_assistant.py` (dùng `EMERGENCY_ANSWER` ở 2 test tuyến khẩn cấp / luật) + `test_assistant_boundary.py` — **16 / 16** | đạt |
| Chỗ khác dùng chữ cũ | `git grep` chữ dòng mở cũ trên nhánh (code, test, frontend; trừ `.md`): 0; `EMERGENCY_ANSWER` chỉ dùng ở `assistant.py:340, 359` (`_set_fixed`) + test | đạt |

## 3. Lập luận "dùng lại định tuyến B143 (24 / 24 khan_cap)"

**Hợp lệ.** Chữ `EMERGENCY_ANSWER` không nằm trong lời dặn nào gửi model (kiểm: dòng mở không có trong `ANSWER_SYSTEM_INSTRUCTIONS`; `ROUTER_INSTRUCTIONS` trên nhánh = **`164bd4a254e9`**, như `main` / B143); câu soạn sẵn được gắn **sau** khi định tuyến chọn `khan_cap` (`_set_fixed`), và chỉ nhớ câu hỏi (`nho_cau_tra_loi: false`) ⇒ chữ này cũng không quay lại lịch sử lượt sau ⇒ đổi chữ không đổi đầu vào của định tuyến ⇒ tỉ lệ tuyến không đổi. Bằng chứng mới hơn cùng lời dặn: mốc thí nghiệm tốc độ C165 hôm nay (`164bd4a254e9`) — 24 / 24 câu khẩn cấp đi `khan_cap` ở **2 / 2 lượt**, + 6 / 6 lượt khẩn cấp có lịch sử (`c156_toc_do_dinh_tuyen.md`). Mỗi lượt `khan_cap` ra đúng hằng `EMERGENCY_ANSWER` ⇒ chữ mới (test `test_assistant.py` tuyến `khan_cap` ⇒ `trace.answer == EMERGENCY_ANSWER`).

## 4. Findings

### m-1 — bản gốc private còn dòng mở cũ

- `data/phase_9/cau_khan_cap_soan_san.md` dòng 16 vẫn là dòng mở cũ; C162 / handoff ghi "đổi chữ ⇒ sửa `test_emergency.py` + bản gốc `cau_khan_cap_soan_san.md`". Tác động: người sau đọc bản gốc thấy chữ khác code. **Tiêu chí đóng:** sửa dòng đó (file private, ngoài nhánh) hoặc ghi một dòng "bản hiện hành = PA1, xem `emergency.py`".

**Ghi nhận (không finding):** không có implementation report riêng — commit message đủ cho đổi một dòng chữ đã duyệt; khi merge A cập nhật báo cáo khâu khẩn cấp / luồng hệ thống (chữ người dùng thấy đổi) và chạy cổng ổn định như A đã định (ngoài giờ đo chữ đầu).

## 5. Decision

**ready_for_user_confirmation** — 0B / 0M / 1m (m-1 ở file private, không chặn merge).
