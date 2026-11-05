# Review: nhánh `p9-b5` tại `5f0a1a3` (B5 + B5.1) — vòng 1

Decision: **changes_requested** (0 blocker · 1 major · 4 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-52`) — việc **C191**, A giao. Skill `risk-gated-agent-review`. 0 USD.
Date: 12:27 05/11/2026 (`date`)
Report: `report_agent/2026-11-02_phase_9_code/b160_b5_implementation.md` sha **`e8c5930438a2`** (working tree `main`). Plan B5 bản 7 `b572443dc9cd`.

## 1. Cổng tối thiểu

- Nhánh `b019aab..5f0a1a3`: 4 commit (`2c7acce` → `0970d96` → `908e93b` khoá → `5f0a1a3` B5.1), khớp report. `main` hiện `faab2e8` — **0 dòng đổi** ở `backend/`, `frontend/` so với `b019aab`.
- 15 file: 3 file mới (`lich_trinh.py`, `do_so.py`, `so_tien.py`), 1 test gỡ (`test_b4_hoi_lai.py`), 1 test mới (`test_b5_lich_trinh.py`), 10 file sửa — khớp bảng §1 report. Không có đổi ngoài phạm vi.
- `git diff --check`: 1 dòng trống thừa cuối `backend/llm/lich_trinh.py` (m-4).
- Gỡ `hoi_lai`: `git grep` không còn tham chiếu tới `Loai`, `TruongTen`, `MAX_TRUONG`, `loc_truong`, `HOI_LAI_NOTE`, `HOI_LAI_TOOL_OVERHEAD`, `StopAtTools`, `flags.hoi_lai`. Outcome `hoi_lai`, `the_hoi_lai`, `ghep_cau`, `TruongInput` vẫn dùng đúng chỗ.

## 2. Chạy lại độc lập (worktree riêng của C: `/tmp/c_b5kin` detach `5f0a1a3`, `/tmp/c_q1main` detach `b019aab`)

| Kiểm | Cách C làm | Kết quả |
|---|---|---|
| **Q1** cờ tắt | `capture_all.py` trên `b019aab` do C tự bắt (không dùng file của B) ↔ nhánh `5f0a1a3` | **228 / 228 giống byte**; file `main` của C cũng giống byte file của B |
| **Q1m** cờ bật | `capture_q1m.py` trên `5f0a1a3` ↔ bản bắt `main` của C | **228 / 228 giống byte** (sau khi bỏ mục công cụ `lich_trinh`); 228 lần bắt có mục này = số lần gọi trợ lý |
| pytest | toàn bộ, không nạp `.env` | 349 passed; 3 failed + 4 error **đều do môi trường**: 5 test cần khoá API, 2 test giao diện cần `dist` ⇒ C `npm ci && npm run build` rồi chạy lại `test_static_ui.py` + `test_b5_lich_trinh.py`: **77 passed** |
| D15 + "Trả lời luôn" | đọc `chot_so_ngay` + `lich_trinh_for_turn`; **ca dò route** `test_c191_route.py`: lượt có giá trị trường, model gửi `so_ngay` rỗng | đạt: `truong` khác None ⇒ không bao giờ trả thẻ (`{}` ⇒ 1 ngày tạm; có `so_ngay` ⇒ dùng); câu ghép "Thông tin thêm: 2 ngày; đi thong thả." có trong input gửi model; `clarify` None; trường lạ / giá trị lạ ⇒ 422 |
| D8 sau B5.1 | **ca dò** `d8.py`: khung thật từ `xep`, thêm 1 điểm ngoài khung theo 9 dạng dòng | xem M-1 |
| D14 tiến độ | **ca dò stream** `test_c191_stream.py`: lượt code hỏi lại số ngày | xem m-1 |
| Bản đồ | đọc `map_url` / `ban_do` + `LichExtras` | code dựng `MAP_BASE` + tên + ", Huế"; trình duyệt chỉ nhận link đúng gốc `google.com/maps/search/`; `rel="noopener noreferrer"`; test CSP đạt |
| Rút lại | `/api/chat` + stream khi `citation_error` | không gửi `lich_trinh` (bản đồ / Sửa) — đúng |

Ca dò của C để ở `data/phase_9/b5/c191_review_tools/` (private; `d8.py` `85317cdbf06b`, `test_c191_route.py` `62cff626844b`, `test_c191_stream.py` `6c51e54dd5f5`).

**Bất biến C kiểm:**
- Cờ `lich_trinh` tắt ⇒ chuỗi gửi model giống byte `main` — đạt (Q1).
- Lượt mang `truong` không bao giờ bị hỏi lần hai — đạt (ca dò route + `chot_so_ngay`).

## 3. Findings

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-1** | major | `lich_trinh.py` `_dau_dong_lich` / `_ten_da_xep` (B5.1) | `d8.py`: điểm ngoài khung **lọt** ở 5 / 9 dạng dòng mà luật cũ (`_ten_xuat_hien`) đều bắt: `### Tối: <điểm>` · `\| Tối \| <điểm> [9] \|` · `🌙 Tối: <điểm>` · nhãn `**Tối**` đứng riêng một dòng rồi `<điểm> [9]` ở dòng sau · `> Tối: <điểm>`. Lý do: `_GACH_DAU` / `_NHAN_DONG` chỉ khớp khi dòng bắt đầu bằng gạch đầu dòng hoặc chữ buổi / ngày (khác `_TIEU_DE_NGAY` có `^\W*`). Vẫn bắt: gạch đầu dòng, "Buổi tối, …". Dạng "sau dấu tách" B đã ghi là giới hạn | D8 (1) là rào **duy nhất** chặn lịch có điểm ngoài khung (Q2 dựa vào nó). Lời dặn yêu cầu "mỗi điểm một dòng mở bằng tên buổi", nhưng tiêu đề markdown / bảng là dạng model hay viết; B5.1 bớt báo nhầm nhưng mở 5 đường lọt mà luật cũ bắt được | (a) bỏ ký tự đầu dòng không phải chữ / số (`#`, `>`, `\|`, emoji…) trước khi khớp, và tách ô bảng theo `\|`; (b) nhãn buổi / ngày đứng riêng một dòng ⇒ dòng không rỗng kế tiếp cũng là dòng lịch. **Kiểm:** 5 dạng trên bị bắt; test B5.1 "lời tả" vẫn 0 lỗi; so luật mới trên 30 câu trả lời đã lưu (v1 / v2 / v3) vẫn khác 0 / 30. Thêm 5 ca vào `test_final_check_still_catches_scheduled_outside_frame`. Không cần chạy lại có phí (đổi chỉ ở kiểm cuối, cờ tắt không chạm) |
| m-1 | minor | `App.jsx` `LICH_BUOC.dang_xep` + `onEvent` | `test_c191_stream.py`: lượt code hỏi lại số ngày phát `{stage: lich_trinh, buoc: dang_xep}`, `buoc_lich` rỗng ⇒ giao diện đẩy "Đang xếp lịch…" vào danh sách bước, **giữ lại** phía trên thẻ hỏi lại (không có lịch nào được xếp). Ở lượt có lịch, "Đang xếp lịch…" cũng còn là mục đầu của danh sách đã xong | lệch ý "tiến độ chỉ hiện bước có thật" (D14) — nhỏ, chỉ là nhãn | `dang_xep` chỉ đổi nhãn trạng thái (`phase`), không vào `progress`; danh sách chỉ gồm bước code đã xong (`xep_xong`, `kiem_luat_*`, `bo_diem`, `lay_nguon`) |
| m-2 | minor | `test_b5_lich_trinh.py` (test thay `test_route_clarify_then_composed_turn` của B4) | test mới ở mức route chỉ có "Trả lời luôn" (`truong: {}`) + trường chi phí 422. Mất hai ý: lượt có **giá trị** ⇒ câu ghép tới model; trường lạ / giá trị lạ ⇒ 422 **ở route**. C đã dò: đạt | test không giữ được hành vi B4 đã có | thêm ca của `test_c191_route.py` (hoặc tương đương) vào test của nhánh |
| m-3 | minor | `lich_trinh.py` `kiem_ghi_chu` | chỉ harness `chay_b5.py` + test dùng; nó kiểm khối do chính code dựng từ cùng danh sách (`khoi_ghi_chu`) ⇒ gần như tự kiểm chính mình | code đo nằm trong module chạy thật (ý "không code thừa") | chuyển sang harness / test, hoặc giữ kèm 1 dòng lý do (B quyết) |
| m-4 | minor | cuối `lich_trinh.py` | `git diff --check`: dòng trống thừa cuối file | — | xoá |

## 4. Đã kiểm, khớp (không phải finding)

- **D15 / D12 (b):** thiếu số ngày ⇒ code trả thẻ, `_dung_khi_hoi_lai` dừng lượt (1 lần gọi model). Model gửi số lệch số dò trong câu ⇒ hỏi lại. Lượt ghép ⇒ không hỏi.
- **D7 + Q1m:** cờ bật không đổi lời dặn hệ thống, chỉ thêm 1 mục công cụ, mô tả không chứa tên điểm thật.
- **Vòng chỉnh 1:** sau khi có khung, `tim_kho` trả `TOOL_DA_DU_LICH`, không tìm thật. `lich_calls > 1` ⇒ không xếp lại.
- **D6:** đoạn nguồn đúng file mỗi điểm; vượt ngân sách ⇒ bớt ngày cuối; đếm `LICH_TRINH_TOOL_OVERHEAD` vào mọi lượt khi cờ bật (D16).
- **Log:** `lich_trinh_ok / so_diem / kiem / buoc` chỉ số và mã, không chữ.
- **Gỡ `hoi_lai`:** thẻ hỏi lại (`the_hoi_lai`), sự kiện `clarify`, `ghep_cau`, `TruongInput` (trường chi phí ⇒ 422) còn nguyên và có test. Nút "Sửa" mở `ClarifyCard` với `initial` = tham số đã dùng ("1 ngày tạm" không chọn sẵn).

## 5. Giới hạn

- Không chạy lượt có phí, không mở server thật / Playwright (B đã chạy Q8). Không chạy lại 5 test cần khoá API.
- M-1 chỉ xét dạng chữ; tần suất model thật viết tiêu đề / bảng chưa đo (13 + 5 câu đã lưu đều viết gạch đầu dòng).

## 6. Bước tiếp

B sửa M-1 (+ minor nếu muốn), báo sha. C kiểm lại vòng 2: chạy lại `d8.py` + test B5.1 + so 30 câu trả lời đã lưu. Q1 dùng lại bằng chứng vòng này (đổi chỉ chạm đường cờ bật).

## Vòng 2 — `5bc45cf` (C191 · 12:40 05/11/2026 `date`)

Report B5 sha **`1fa983e45fb1`** (§2b có thêm phần sửa). Chỉ kiểm phần sửa: `5f0a1a3..5bc45cf` = 1 commit, 3 file (`lich_trinh.py`, `test_b5_lich_trinh.py`, `App.jsx`). `git diff --check` sạch.

| Finding | Sửa | C kiểm (cách khác B) | Kết luận |
|---|---|---|---|
| **M-1** | `_bo_dau` (bỏ mọi ký hiệu không phải chữ / số + số thứ tự ở đầu dòng), `_dau_doan`, `_dau_dong_lich` (ô bảng có ô nhãn buổi / ngày; dòng ngay sau nhãn đứng riêng) | `d8.py` vòng 1: 5 / 5 dạng lọt nay bị bắt, "lời tả" 0 lỗi. **`d8_v2.py` (mới, `440c0f9b24d0`):** thêm 5 dạng lọt B chưa có test — nhãn thường `Tối:` đứng riêng · `**Buổi tối:**` rồi dòng sau · `1) Tối – <điểm>` · bảng 3 cột có cột "Buổi" · dòng trống giữa nhãn và điểm ⇒ **5 / 5 bị bắt**. C tự tính `kiem_cuoi` mới trên 30 câu trả lời đã lưu (v1–v3): **0 / 30 báo lỗi** | **đóng** |
| m-1 | `dang_xep` bỏ khỏi `LICH_BUOC` ⇒ chỉ đổi nhãn trạng thái | đọc diff `App.jsx`; `npm run build` đạt; test giao diện đạt | đóng |
| m-2 | test route lượt có giá trị + 422 | có trong 358 passed | đóng |
| m-3 | giữ `kiem_ghi_chu` + 1 dòng lý do (sàn Q2 ghi trước đo bằng hàm này) | — | đóng (B quyết, có lý do) |
| m-4 | bỏ dòng trống cuối | `git diff --check` sạch | đóng |

pytest toàn bộ trên `5bc45cf` (không nạp `.env`, có `dist`): **358 passed**; 1 failed + 4 error = đúng 5 test cần khoá API như vòng 1. Q1 / Q1m: **dùng lại bằng chứng vòng 1**, vì vòng 2 chỉ đổi `kiem_cuoi` (chạy sau khi sinh, chỉ khi cờ bật) và giao diện ⇒ chuỗi gửi model không đổi.

**Giới hạn ghi lại (không phải finding — đi theo chiều an toàn, rút lại chứ không đưa lịch sai):**
- `d8_v2.py` cho thấy 3 dạng **có thể báo nhầm**: tiêu đề nhắc tên điểm ngoài khung ("### Ngày 1 – quanh <điểm khác>") · ô ghi chú trong dòng bảng có nhãn buổi · dòng mở bằng "(" nhắc điểm khác. Luật trước B5.1 báo nhầm cả 3 dạng này; câu văn thường nhắc điểm khác vẫn 0 lỗi.
- Dạng "sau dấu tách" (B đã ghi) vẫn không bị D8 (1) bắt.
- 30 / 30 câu đã lưu không vướng dạng nào trong số trên.

**Decision vòng 2: ready_for_user_confirmation** — A merge theo kết quả Q3 của User (cờ tắt hay bật).
