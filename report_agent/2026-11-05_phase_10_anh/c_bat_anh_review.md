# Review: Phase 10 — bật hỏi bằng ảnh trên cổng (nhánh `p10-anh-bat`)

Decision: **ready_for_user_confirmation** — với điều kiện E rebase lên `main` `c9931be` theo cách gộp đã thử ở dưới (m-1). 0 blocker · 0 major · 2 minor.
Người kiểm: C (Claude Code, terminal `hue-rag-e9`)
Date: 08/11/2026 (bắt đầu khoảng 09:52, viết 10:01 — `date`)
Nhánh: `p10-anh-bat` = `ce89e42` (từ `main` `129ef30`, 1 commit, 3 file giao diện +11 / −3)
Implementation report: `report_agent/2026-11-05_phase_10_anh/e_bat_anh_implementation.md` (E)
Tiêu chí (A giao): cờ tắt ⇒ không nút, `POST` ảnh 404, Giới thiệu không có câu ảnh, chuỗi gửi model không đổi; cờ bật ⇒ nút đúng chỗ (máy tính: trang trợ lý +
khung nổi; điện thoại: trang trợ lý), thẻ không đè câu trả lời 1440 + 390, câu dữ liệu ảnh ở Giới thiệu đúng với `nhan_anh.py`, 0 CSP / console; test; rebase lên
`c9931be` không đụng.
Tiền: **≈ 0,0020 USD** (2 câu chat 0,001009 + 2 lần đoán ảnh 0,000994, từ `chat_metrics` / `anh_metrics`). Trần A ghi ≤ 0,002 — vượt ~0,000004 vì lượt 1 hỏng do
công cụ của C (xem §3), phải chạy lại. Tính vào Phase 10.

## 1. Phạm vi đã review

- Exact diff `129ef30..ce89e42`: `App.jsx` (truyền `anh` cho `GioiThieu`), `HoiBangAnh.jsx` (cuộn trang xuống đáy khi thẻ đổi trạng thái, chỉ khi nằm trong
  `.tro-ly-trang`), `pages.jsx` (2 dòng Giới thiệu hiện khi `anh`). **Backend: 0 file đổi** ⇒ chuỗi gửi model, route ảnh, cờ, log giữ nguyên theo cấu tạo.
  `git diff --check` sạch. Không có thay đổi ngoài phạm vi.
- Report E §1–§6.

## 2. Findings

- **m-1 (minor, phải làm trước merge) — nhánh XUNG ĐỘT với `main` `c9931be`.** `frontend/src/pages.jsx` `GioiThieu`: `main` (ảnh cổng) thêm mục "Nguồn ảnh"
  ở cuối hàm; nhánh thêm câu ảnh ở cùng chỗ ⇒ `git merge` báo CONFLICT 1 khúc. Cách gộp C đã thử: **giữ cả hai**, câu "Ảnh bạn gửi được thu nhỏ…" đứng
  **trước** `<h2 id="nguon-anh">` (nhóm với các câu riêng tư ở trên). Trên bản gộp đó mọi kiểm ở §4 đạt. Tiêu chí đóng: E rebase `p10-anh-bat` lên `c9931be`
  (hoặc mới hơn) đúng cách gộp này, `npm run build` + 3 file test đạt; người merge kiểm `git diff` khúc `GioiThieu` có cả hai phần. (`App.jsx` tự gộp được.)
- **m-2 (minor, giới hạn đo) — số đo "thẻ đè bong bóng" của C chỉ có 1 câu trả lời trên màn hình** (khổ 390 rồi đổi sang 1440 cùng trang). Kết quả 0 px đè (§4)
  đồng ý với E; không đo khung nổi khi đã có câu trả lời (E cũng ghi chưa đo). Không cần sửa.

Độ đơn giản: sửa che câu trả lời bằng một `useEffect` cuộn trang, giới hạn đúng trang trợ lý — trực tiếp, không thêm trạng thái. Câu Giới thiệu đọc cờ đã có từ
`/api/tinh_nang`. Không thấy over-engineering. Bảng rà AI FDE: không đổi agent / công cụ / đường ra (đường ảnh → OpenAI đã duyệt ở spec Phase 10), không cần bảng mới.

## 3. Cách người kiểm chạy lại thật

- Worktree tạm `git worktree add --detach /tmp/c_bat c9931be` ⇒ `git merge origin/p10-anh-bat` (CONFLICT ⇒ gộp như m-1, commit tạm không push) ⇒ symlink `data/`,
  `knowledge-base-hue/` ⇒ `npm ci && npm run build`.
- Test: `pytest tests/test_static_ui.py tests/test_cong_dot_1.py tests/test_p10_anh.py` trên bản gộp.
- Ca dò riêng tư (khác cách E đọc code): dựng JPEG 3000 × 2000 có **GPS EXIF + orientation + XMP chứa toạ độ** và PNG có **text chunk toạ độ**, đưa qua
  `llm.nhan_anh.chuan_bi_anh` thật, đọc lại metadata + tìm chuỗi toạ độ trong byte đầu ra.
- Cờ tắt (`settings.yaml` mặc định): `uvicorn` cổng 8894 ⇒ `/api/tinh_nang`, `curl -X POST /api/anh/ung_vien` ⇒ ca dò trình duyệt
  `data/phase_10/anh/c_bat_review/c_bat_probe.py <base> tat` (đếm nút "Hỏi bằng ảnh" ở trang trợ lý + khung nổi, chữ Giới thiệu, cuộn ngang, sự kiện
  `securitypolicyviolation` nghe trong trang, lỗi console; 1440 + 390).
- Cờ bật (chỉ sửa `settings.yaml` của worktree tạm): `uvicorn` cổng 8895 ⇒ cùng ca dò chế độ `bat` + **có phí**: ở 390 trang trợ lý hỏi 1 câu trong kho, chờ
  dòng Nguồn, chọn 1 ảnh từ bộ **đã thấy** `bo_do_anh/da_thay/khong_tin_cay/` (không mở bộ kín), chờ gợi ý, đo hộp bao thẻ ↔ mọi `.bubble` đang hiện, rồi đổi
  khổ sang 1440 đo lại. Lượt 1 hỏng ở bước chờ: `wait_for_function` của Playwright dùng chuỗi JS ⇒ **bị CSP `script-src 'self'` chặn** (đúng — trang không cho
  `eval`); C sửa sang chờ bằng Python rồi chạy lại cả lượt.
- Log: đọc `backend/logs/application.log` của worktree sau mốc dòng; chép 4 dòng số đo sang `data/phase_10/anh/c_bat_review/log_metrics.txt`.
- Dọn: tắt server (TaskStop / PID ghi từ `pgrep -f "[u]vicorn …"`), gỡ symlink, `git worktree remove --force /tmp/c_bat`.

## 4. Kết quả quan sát

| Tiêu chí | Kết quả | Ý nghĩa |
|---|---|---|
| Rebase lên `c9931be` | **CONFLICT** 1 khúc `GioiThieu` (`pages.jsx`); gộp giữ cả hai ⇒ build đạt | cần E rebase (m-1) |
| Test (bản gộp, cờ tắt) | **60 passed** (`test_static_ui` + `test_cong_dot_1` + `test_p10_anh`) | — |
| Cờ tắt | `/api/tinh_nang` `anh: false`; `POST /api/anh/ung_vien` ⇒ **404**; nút ảnh: trang trợ lý 0 / khung nổi 0 (1440), trang trợ lý 0 (390); Giới thiệu không có "Hỏi bằng ảnh" lẫn "Ảnh bạn gửi"; CSP 0, console 0, không cuộn ngang | cờ tắt = như trước |
| Chuỗi gửi model khi cờ tắt | backend 0 file đổi trong nhánh | **bất biến giữ** theo cấu tạo (không cần chạy lại 228 / 228) |
| Cờ bật — nút | 1440: trang trợ lý **1**, khung nổi **1**; 390: trang trợ lý **1**, nút trợ lý nổi **ẩn** (thiết kế cổng — vào trợ lý bằng thanh dưới) | đúng chỗ |
| Cờ bật — thẻ đè câu trả lời | 390: bong bóng câu trả lời hiện 213 px, **đè 0 px**; đổi sang 1440 cùng trang: hiện 268 px, **đè 0 px** (mục thứ hai trong số đo là chính thẻ gợi ý — thẻ cũng có lớp `bubble`) | sửa cuộn của E có tác dụng |
| Cờ bật — gợi ý | ảnh chùa ⇒ gợi ý "Chùa Thiên Mụ" + nút "Không phải các tên này — tôi gõ tên"; thẻ có câu "Ảnh được gửi tới OpenAI… máy chủ này không lưu ảnh" | — |
| Câu Giới thiệu ↔ `nhan_anh.py` | ca dò: đầu ra 683 × 1024 (đã xoay theo EXIF + thu cạnh dài 1024), EXIF **rỗng**, chỉ còn khối JFIF, **0** XMP, **0** chuỗi toạ độ; PNG có text chunk ⇒ JPEG, **0** chuỗi toạ độ; route `anh.py` không ghi file, log chỉ `anh_metrics` | câu "thu nhỏ, bỏ thông tin vị trí, gửi tới OpenAI, không lưu" **đúng với code** |
| CSP / console (cờ bật) | 0 / 0 ở 1440 + 390, mọi trang dò | — |
| Log | 4 dòng (2 `chat_metrics` + 2 `anh_metrics`); **0** dòng chứa chữ câu hỏi | không lộ nội dung |
| Thời gian đoán ảnh | 5,2 s · 8,4 s (`anh_metrics.ms_tong`, gần hết là chờ model) | cùng mức E đo (p50 3,5 s, cao nhất 9,1 s) — chưa đạt 5 s, đã biết |

## 5. Giới hạn hoặc phần chưa chạy

- Chỉ 1 ảnh, 1 câu trả lời trên màn hình (m-2); không đo khung nổi khi đã có câu trả lời; chỉ Chromium.
- Cổng ổn định "1 câu trong kho + 1 câu ngoài kho" với **cờ tắt**: NOT RUN — backend không đổi, giao diện cờ tắt không hiện phần mới (đã kiểm 0 nút, 404).
  Câu trong kho chạy ở lượt cờ bật (đi đúng đường hỏi thường).
- Bản gộp C thử là commit tạm trong worktree đã gỡ — không phải bản E sẽ rebase; người merge kiểm lại khúc `GioiThieu`.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation**, sau m-1 (E rebase lên `c9931be` giữ cả hai phần). Khi merge để bật: `settings.yaml` `anh.bat: true` + build lại giao diện +
báo cáo `BAO_CAO_HOI_BANG_ANH.md` / `LUONG_HOAT_DONG_HE_THONG.md` (E đã ghi ở report §6). Bằng chứng private: `data/phase_10/anh/c_bat_review/`.
