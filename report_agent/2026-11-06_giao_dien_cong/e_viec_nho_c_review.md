# Review: việc nhỏ trước đóng gói — phần C (3, 8, 10, m-1, 11, 13) — nhánh `p11-viec-nho-c`

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 3 minor). Merge cần **rebase** trước: xung đột 2 file giao diện (m-3).
Người kiểm: E (Claude Code, `hue-rag-22`)
Date: 10:55 08/11/2026
Implementation report: `report_agent/2026-11-06_giao_dien_cong/c_viec_nho_implementation.md`

## 1. Phạm vi đã review

- **Git:** `origin/p11-viec-nho-c` = `2c2c1bf`, 1 commit trên `1611d34`. `main` nay là `5d5edde` (đã có bản đồ, ảnh, lịch nhỏ, việc nhỏ E). 21 file +174 / −25 (7 ảnh `_nho` mới). `git diff --check`: sạch. Hook lúc C commit: 0 trùng (theo report).
- **Đọc exact diff:**
  - server: `feedback.py` (`/api/bao_sai`), `routes/chat.py` (`turn_id`), `routes/cong.py` (`_doan_dau`, `_tom_tat`), `tra_web.py` (`_CHUOI_SO`, `_chuoi_so`, `kiem_muc_web`);
  - giao diện: `pages.jsx` (`Anh`, `BaoSai`, `GioiThieu({ muc })`), `App.jsx`, `anh.js`, `route.js`, `index.css`, `vite.config.js`;
  - 4 file test.
- **Đối chiếu tiêu chí A giao:**
  - (3) 100 / 204 thẻ đổi đúng loại;
  - (8) chỉ nhận `bai_id` nguyên chuỗi, log không chữ tự do, rào như feedback;
  - (10) `<picture>` + đo byte;
  - m-1 cuộn đúng mục;
  - (11) chuỗi số ⊂ tiêu đề + trích, có test cố tình vi phạm;
  - (13) `turn_id` trong `chat_metrics`;
  - kiểm rebase.
- **Ngoài phạm vi:** không thấy. Không đổi lời dặn / tìm kho / cờ / CSP.

## 2. Findings

Không có blocker / major.

### m-1 (minor) — luật (11) so theo chữ số, không theo nghĩa

- Vị trí: `tra_web.py` `_chuoi_so` (bỏ mọi ký tự không phải chữ số rồi so).
- Bằng chứng (ca dò E, mục 4):
  - **nhận nhầm:** "Số nhà 123" khi đoạn trích chỉ có giờ "1:23" ⇒ đạt (cùng chữ số "123");
  - **bỏ nhầm:** "ngày 8/11" khi trích ghi "08/11" ⇒ `so_ngoai_trich` (số 0 đầu khác) ⇒ cả mục web bị bỏ.
- Tác động: ca nhận nhầm cần model ghép đúng dãy chữ số của một số khác loại — hiếm. Ca bỏ nhầm nằm ở phía an toàn (mất mục web, không nói sai). C đã ghi luật "chặt theo cách viết".
- Tiêu chí đóng: không cần sửa trước merge. Theo dõi `web_kiem` có `so_ngoai_trich` sau khi bật (như C đề xuất); thấy bỏ nhầm nhiều thì xét bỏ số 0 đầu khi so.

### m-2 (minor, build) — máy chính sẽ mất ảnh lễ hội thật ở lần build sau merge

- Vị trí: `vite.config.js` — ảnh riêng chỉ dùng khi có **cả** `lv_festivals.jpg` **và** `lv_festivals_nho.jpg`.
- Bằng chứng: `frontend/public/anh/rieng/` của thư mục chính hiện **chỉ có** `lv_festivals.jpg` (E `ls` 10:55).
- Tác động: sau merge, `npm run build` ở máy chính mà chưa chạy `anh_nho.py` ⇒ ô "Lễ hội" lặng lẽ đổi sang ảnh Commons (ghi công vẫn khớp, nên không sai; chỉ khác ảnh User đã chốt). C đã ghi bước này ở §5, nhưng dễ bị quên.
- Tiêu chí đóng: A chạy `data/phase_11/anh_cong/tools/anh_nho.py` (tạo bản nhỏ cho `rieng/`) **trước** build cổng sau merge, hoặc ghi bước này vào handoff / guide build.

### m-3 (minor, merge) — xung đột khi rebase

- E rebase thử lên `main` `5d5edde` (worktree tách rời, đã huỷ rebase): **xung đột `frontend/src/App.jsx` + `frontend/src/pages.jsx`**. Lý do: `GioiThieu` nay nhận `anh` (ảnh) + `banDo` (bản đồ), nhánh này thêm `muc`.
- Các file khác tự gộp. Riêng `routes/chat.py` `StreamEvents.done` gộp đúng cả hai thay đổi (`tu_choi_kho` của E + `turn_id` của C) — E đọc hàm sau gộp.
- Tiêu chí đóng: C rebase, gộp thành `GioiThieu({ anh, banDo, muc })` + `<GioiThieu anh=… banDo=… muc={route.muc} />`; build + chạy lại test chạm. Sau rebase, `test_b6_tra_web.py::test_web_section_renderer_uses_filter_without_links` (hỏng sẵn trên `1611d34`, B đã sửa trên `main`) phải đạt.

### Ghi nhận (không phải finding)

- `/api/bao_sai` không có trần số lượt — giống `/api/feedback`. Vào chung mục "giới hạn lượt" của checklist deploy.
- `GioiThieu` cuộn theo `getElementById(muc)` với `muc` từ hash: id lạ ⇒ không làm gì (không có đường chèn).

## 3. Cách người kiểm chạy lại thật

Worktree `/tmp/e_vnc` (detached tại `2c2c1bf`), symlink `data/` + kho, `npm ci && npm run build`, server thật cổng 8856 (`--env-file`).

1. **(11) ca dò 0 USD, khác ca C:** `data/phase_11/viec_nho_c/e_review/do_so_web.py` — gọi đúng `kiem_muc_web` của nhánh với 15 ca biên:
   - số ghép qua ranh giới tiêu đề / trích; điện thoại nhiều cách viết; "7h30" ↔ "7:30"; khoảng giờ có "-"; "8/11" ↔ "08/11"; thập phân "3,5" ↔ "3.5";
   - số đơn lẻ bịa; tiền thật / tiền bịa; mã `[w 1]`; năm; chữ số dính chữ; "1:23" ↔ "123"; câu thời gian thực.
2. **(3) 0 USD, khác cách C:** `do_tom_tat.py` chạy hàm production `nap_kham_pha` trên `main` (thư mục chính) và trên nhánh. So **từng bài** và kiểm tóm tắt mới có **nguyên văn trong bài** (bỏ dấu đậm / nghiêng). Chỉ in số đếm.
3. **(8) thử phá trên server thật:**
   - bài thật; id có dấu dạng NFC ↔ NFD; dấu cách cuối; chèn xuống dòng + chuỗi giả `chat_metrics`;
   - kiểu số / mảng; trùng khoá JSON; thân 1 MB; không phải JSON; GET.
   - Đếm dòng `chat_bao_sai` + tìm dòng log giả sau mốc.
4. **(10) + m-1 0 USD, khác cách C** (C cộng byte phản hồi): `ui_anh.py` đọc `currentSrc` của mọi `img.hero-anh` / `img.kp-anh` ở 390 @1×, 390 @3×, 1440; độ rộng thật ↔ hiện; mở **thẳng** `#/gioi-thieu/nguon-anh` lúc tải trang, đo vị trí mục ↔ đáy thanh đầu trang.
5. **(13):** 1 lượt stream thật (câu trong kho tự viết), so `turn_id` ở sự kiện `done` ↔ dòng `chat_metrics`.
6. **Rebase thử:** `git rebase --onto main 1611d34` trong worktree (huỷ sau khi xem), lần 1 lên `b50d9c0`, lần 2 lên `5d5edde`.
7. **Test 8 file** của C (bỏ `test_api_chat.py` vì cần khoá).

## 4. Kết quả quan sát (lần chạy mới của E)

| Kiểm | Kết quả |
|---|---|
| (11) 15 ca | **15 / 15 đúng dự đoán**: bắt số ghép qua ranh giới, số đơn lẻ bịa, chữ số dính chữ, "8/11"↔"08/11" (bỏ nhầm — m-1); nhận các cách viết khác của cùng số, khoảng giờ, thập phân, năm, mã `[w n]`; tiền bịa ⇒ chỉ `tien_ngoai_trich` (không trùng mã); thời gian thực ⇒ chỉ `so_thoi_gian_thuc`; "1:23"↔"123" ⇒ nhận (m-1) |
| (3) thẻ | 100 / 204 đổi; **cả 100 trước có nhãn**, 0 bài có nhãn không đổi; sau đổi 0 rỗng, **100 / 100 là câu có nguyên văn trong bài**, dài 131–200 ký tự; 104 bài còn lại giống byte; 2 thẻ còn khớp mẫu nhãn (C giải thích: câu văn xuôi có ngoặc chữ Hán) |
| (8) | bài thật 200 · id dấu **NFC 200 / NFD 404** (so nguyên chuỗi) · dấu cách cuối 404 · chèn xuống dòng 404 · số / mảng 422 · thân 1 MB 422 · không JSON 422 · GET 405 · trùng khoá JSON (giá trị sau là id thật) 200 = đúng hành vi JSON. Log: đúng 3 dòng `chat_bao_sai` cho 3 yêu cầu hợp lệ, 0 dòng giả |
| (10) | 390 @1× và @3×: **mọi** ảnh đầu trang + 5 ảnh tròn ở trang chủ và Khám phá chọn bản `_nho`; 1440: mọi ảnh bản lớn; mọi ảnh giải mã. Byte ảnh hai trang (cùng phiên): **390: ~175 KB · 1440: ~513 KB**. Ảnh tròn 240 px cho khung 64 px (đủ cho màn 3×) |
| m-1 | mở thẳng link sâu: 390 mục ở 88 px > đáy thanh đầu trang 57 px; 1440 mục 281 px > 69 px (trang ngắn); 0 lỗi CSP |
| (13) | `done.turn_id` = `chat_metrics.turn_id`; 0 chữ câu hỏi trong log |
| Rebase | xung đột `App.jsx`, `pages.jsx` (m-3); `chat.py` gộp đúng |
| Test 8 file | **234 passed**, 1 failed = test B6 hỏng sẵn trên `1611d34` (đã sửa trên `main`) |

**Tiền E: 0,0004066 USD** (1 lượt stream). Còn lại 0 USD.

**Dùng lại bằng chứng của C, không chạy lại:**
- (11) lượt thật với Serper (3 câu, 1 ca bỏ nhầm "24/7" ⇒ sửa so cả tiêu đề) — E kiểm ca tiêu đề bằng ca dò 0 USD;
- (8) bấm nút trên giao diện;
- ảnh riêng có / không bản nhỏ;
- `/api/chat` không stream cho (13).

## 5. Giới hạn hoặc phần chưa chạy

- E không chạy lượt Serper thật cho (11) — dùng hàm production với đầu vào tự dựng.
- Không kiểm sau rebase (nhánh chưa rebase). Sau khi C rebase, A / C chạy lại build + test chạm.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** sau khi C rebase (m-3).
- A nhớ m-2 trước build cổng: chạy `anh_nho.py` cho ảnh riêng, không thì ô Lễ hội đổi sang ảnh Commons.
- m-1 theo dõi sau khi bật, không chặn.
