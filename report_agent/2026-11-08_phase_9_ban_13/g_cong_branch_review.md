# Review: Phase 9 bậc G — cổng 2 nhóm (review sớm, phần code — NHÁP)

Decision (phần code, chờ sha cuối): **không có blocker / major** — nghiêng `ready_for_user_confirmation` cho phần code; **phần lời dặn chưa review** (A còn quyết S1 / S2b)
Người kiểm: E (Claude Code, `hue-rag-ea`)
Date: 20:44 09/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-08-phase-9-g-cong-plan.md` bản 2
Implementation report: `report_agent/2026-11-08_phase_9_ban_13/b_g_cong_implementation.md`

## 1. Phạm vi đã review

- Nhánh cục bộ `p9-g-cong` **`f8bfc69`** (4 commit trên `main` `5c982a0` — đã rebase, có T1). `origin/p9-g-cong` `87d6798` là bản trước rebase: diff hai bản
  chỉ khác số dòng hunk (đã so). B sẽ push `f8bfc69` khi khoá.
- Đọc hết diff 16 file (191 + / 187 −): `assistant.py`, `full_corpus_prompt.py` (phần cấu trúc, không chấm chữ lời dặn), `generator_openai_full_corpus.py`,
  `api/routes/chat.py`, `full_corpus_eval.py`, `settings.yaml`, xoá `emergency.py` + `test_emergency.py`, test mới `test_g_cong.py`, test sửa, giao diện 3 file.
- Đối chiếu plan §1 (đổi gì), §4.1 (test mỗi loại lượt). Phần đo (§2 sàn, kín, S1 / S4 / S5) là việc của B, không chạy lại.

## 2. Findings

Không có blocker. Không có major.

### m-1 (minor) — câu ngoài phạm vi viết lệch một chút ⇒ lỗi trích dẫn, giao diện rút chữ
- **Vị trí:** `assistant._finish_generated` — so `text.strip() == OUT_OF_SCOPE_ANSWER` (khớp đúng chuỗi).
- **Bằng chứng (ca dò của E, 0 USD):** chuẩn / thêm xuống dòng ⇒ `out_of_scope` (đúng). Thiếu câu hỏi cuối, đặt dấu "hóa" thay "hoá", Unicode dạng tách dấu (NFD)
  ⇒ `CitationIntegrityError` ⇒ stream phát `error` "Câu trả lời không đáp ứng yêu cầu trích dẫn", giao diện rút chữ. Câu chuẩn + "[1]" ⇒ câu trả lời thường có nguồn.
- **Tác động:** trước G câu ngoài phạm vi do code trả nguyên văn (tất định); sau G phụ thuộc model chép đúng. **Quan sát thật: 0** — E đếm trên kết quả đã thấy của B
  (`khoa_r1/r2`, `cacau_g3_r1`, `cacau_g4_r1`, `cacau_g_khancap_r1`, 388 lượt; không mở file kín): `oos_lech` 0, `citation_error` 0.
- **Đóng khi:** B báo `oos_lech` + `citation_error` của lượt kín / S5 (plan "Theo dõi m-5" đã có). Nếu muốn rẻ: so sau `unicodedata.normalize("NFC", …)` — 1 dòng,
  không bắt biến thể chữ. Không chặn merge.

### m-2 (minor) — log `route` của câu ngoài phạm vi đổi nghĩa
- Câu ngoài phạm vi giờ có `route = tro_ly_hue` + `outcome = out_of_scope` (trước: `route = ngoai_pham_vi`). Script phân tích cũ lọc theo `route == "ngoai_pham_vi"`
  (vd `data/phase_9/b143/tools/`) sẽ đếm 0. **Đóng khi:** report / `LUONG_HOAT_DONG_HE_THONG.md` ghi "đếm câu ngoài phạm vi theo `outcome`". Không cần sửa code.

### m-3 (minor) — `bieu_mau_agent` bỏ qua tham số `answer_instructions`
- `generator_openai_full_corpus.py`: trước dùng `answer_instructions` (tham số cho harness 8.1 thử lời dặn), nay dùng hằng `ANSWER_BIEU_MAU_INSTRUCTIONS`. Đúng ý
  M-4 (biểu mẫu giữ lời dặn trước G giống byte — E kiểm: `ANSWER_BIEU_MAU_INSTRUCTIONS` == `ANSWER_SYSTEM_INSTRUCTIONS` của `main`, sha `81d3040cf53f`). Chỉ harness
  thử lời dặn mới bị ảnh hưởng (biểu mẫu không nhận lời dặn thử). **Đóng khi:** 1 dòng chú thích, hoặc nhận như vậy.

### Ghi nhận (không phải finding)
- Gỡ khẩn cấp sạch: `git grep "emergency|khan_cap|ngoai_pham_vi"` trong `backend` + `frontend/src` chỉ còn chú thích lịch sử và test khẳng định nhãn cũ bị schema từ chối.
  `emergency_rule` không còn ở `.py` / `.yaml` nào (kể cả `data/phase_12`).
- Đơn giản: một chỗ nhận câu ngoài phạm vi (`_finish_generated`), 3 nhánh chết bị gỡ, không thêm cờ — đúng plan §1, không thấy phần phòng xa.
- T1 sau G: câu ngày đi agent Huế; lời dặn mới ghi "kể cả câu về ngày tháng" là câu về Huế — khớp ý T1. Nhánh `p9-t1-sang-nam` (E) chạm `assistant.py` 2 dòng ⇒ E rebase sau G.
- Rủi ro đã được User chấp nhận (không review lại): bỏ câu soạn sẵn khẩn cấp; câu khẩn cấp giờ đa số ra "không đủ thông tin" + mục web (câu hỏi 3b chờ User).

## 3. Cách người kiểm chạy lại thật

- Worktree `/tmp/e_g` detached `f8bfc69`; `cd frontend && npm ci && npm run build` (đạt, bundle 109,6 KB gzip).
- `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests -q --ignore=tests/test_phase6_live_smoke.py` (không khoá).
- Ca dò `/tmp/e_g_probe/probe.py` (chạy với `PYTHONPATH=backend`): 7 biến thể chữ qua `_finish_generated` + so lời dặn biểu mẫu với `main` bằng `git show`.
- Đếm `oos_lech` / `citation_error` / `lop` trên 5 file kết quả đã thấy của B (chỉ in số).
- `git diff --check main...HEAD`: sạch.

## 4. Kết quả quan sát

- pytest: **825 passed**, 1 failed + 3 error = đúng 4 test cần `OPENAI_API_KEY` (bẫy đã biết). `test_static_ui.py` (CSP, bản build) đạt.
- Ca dò: như m-1; bất biến "lời dặn biểu mẫu giống byte `main`" **đúng**.
- **Bất biến đã kiểm:** câu ngoài phạm vi chuẩn ⇒ `out_of_scope`, không kiểm citation, không mở cổng web (test `test_g_cong.py` của B + ca dò của E cùng kết quả bằng
  đường khác).

## 5. Giới hạn hoặc phần chưa chạy

- **Chưa review chữ lời dặn** (`ROUTER_INSTRUCTIONS`, khối ngoài phạm vi) — chờ sha cuối sau khi A quyết S1 / S2b.
- Không chạy lượt có phí (0 USD theo việc giao); không chạy server / Playwright (giao diện chỉ gỡ thẻ khẩn cấp; bản build + test CSP đạt).
- Không mở câu kín, không chấm S1 / S4 (việc B).

## 6. Decision và bước tiếp theo

- Phần code: **không chặn merge**; 3 minor không mở vòng sửa riêng.
- Khi B khoá sha cuối: E đọc diff lời dặn (chỉ phần đổi so với `f8bfc69`) + số sàn trong report B ⇒ kết luận cuối.
