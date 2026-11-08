# Implementation Report: việc nhỏ lịch trình — (1) sao chép / tải lịch · (4) câu buổi tối · ~~(6) link Google Maps theo toạ độ~~ (đã bỏ)

Người làm: B (Claude Code, terminal `hue-rag-a1`)
Date: 08/11/2026 (report 10:14 — `date`)
Nguồn việc: User duyệt "Nhóm 1 + 2" (`data/ra_soat_tinh_nang_2026-11-08/`), A giao B các ý 1, 4, 6 (`CURRENT_HANDOFF.md` mục 2c).
Nhánh: `p11-lich-nho` **xếp chồng trên `p11-ban-do` `d0adf31`** (A đồng ý: (6) dùng bảng toạ độ nạp ở nhánh bản đồ) — rebase lên `main` sau khi bản đồ merge.
Tiền: **0,000435 USD** (1 lượt biểu mẫu + 1 câu ngoài kho).

## 0. Cập nhật 10:47 08/11/2026 (`date`) — sau review E (ready, 3 minor) + quyết định A

- **Nhánh hiện tại: `p11-lich-nho` = `de08454`**, rebase lên `main` `06dafb4` (bản đồ đã merge `a4fde29`; `origin/main` `dcd68f4` sau đó chỉ đổi tài liệu). 3 commit:
  `993bcf2` (1)(4)(6) · `9f7b036` 2 minor review bản đồ của E (m-1 số ghim chỉ nhận số nguyên dương — đi qua `innerHTML` của `divIcon`; m-2 một hàm `toaDoHopLe`
  dùng chung ở `frontend/src/toaDo.js`) · `de08454` **bỏ (6)**.
- **(6) bỏ (A quyết theo review E):** link toạ độ chỉ mở ghim trần, mất thẻ địa điểm của Google; vài toạ độ còn lệch ⇒ link Google Maps về **theo tên** như
  trước; toạ độ chỉ dùng cho bản đồ của mình và **chỉ nạp khi cờ `ban_do_lich` bật** (đúng plan bản đồ) ⇒ bật biểu mẫu không cần file toạ độ (m-3 của E).
  `assistant.py` / `settings.yaml` giờ giống hệt nhánh bản đồ; diff backend so với `main` chỉ còn (4) + chú thích `map_url` + test.
- Kiểm lại sau 3 commit + rebase: test rộng **735 đạt** (còn lại = 2 test cần khoá); m-1 / m-2: server cờ bản đồ bật, `kiem_ban_do.py` 6 / 6 ngày ghim đúng, 0 lỗi
  console / CSP, tile 68 / 68 (≈ 0,0015 USD); sau bỏ (6): server cờ như `settings.yaml`, `kiem_luu_lich.py` — clipboard = file tải, chữ lịch trọn trong file,
  4 / 4 link **theo tên**, 0 lỗi (0,00036 USD) — `data/phase_11/lich_nho/kiem_sau_bo_6.json`.
- Tiền cả việc: 0,000435 + 0,001532 + 0,00036 ≈ **0,0023 USD**.
- Các mục (6) bên dưới là hồ sơ bản đã bỏ.

## 1. Phạm vi

Ba việc nhỏ, B tự quyết chi tiết (`Session_Prompt.md` §7 cắt giảm (3)); không plan riêng, không bộ kín (hành vi tất định). Không đụng phần định tuyến
`assistant.py` (A dặn — User đang bàn đổi định tuyến).

## 2. Thay đổi chính

| Việc | File | Thay đổi |
|---|---|---|
| (1) sao chép / tải | `frontend/src/chat.jsx` (`LuuLich`, `vanBanLich`), `index.css` | Dưới lịch: nút "Sao chép lịch" (`navigator.clipboard.writeText`) + "Tải về (.txt)" (Blob ⇒ `lich-trinh-hue.txt`). Chữ = dòng câu hỏi + lựa chọn · chữ lịch **đúng như đang hiện** (`innerText` của khối trả lời đã qua DOMPurify — gồm "Ghi chú của lịch") · "Bản đồ từng điểm" (tên + link; cờ bản đồ bật ⇒ "Ngày n · k.") · dòng "có thể sai — kiểm lại trước khi đi". Không gọi server, không gửi đi đâu. Clipboard bị chặn (trang http không phải localhost) ⇒ báo "dùng nút Tải về" |
| (4) câu buổi tối | `backend/llm/lich_trinh.py` | mã mới `toi_chua_so_thich`: người dùng xin buổi tối mà **chưa nêu sở thích** ⇒ "Buổi tối mình chưa xếp vì bạn chưa nêu sở thích — nói mình biết bạn thích gì để mình xếp điểm buổi tối." (dòng khung: "…nên mình chưa xếp điểm buổi tối"); có sở thích ⇒ câu cũ `toi_khong_diem`. Thêm vào `MA_TOI` ⇒ kiểm cuối "nói ngược buổi tối" áp như 3 mã cũ. Lý do không dùng câu kiểu "bảng chỉ có điểm ăn uống buổi tối" (bảng thật: 4 điểm buổi tối, đều ẩm thực): câu gắn với nội dung bảng sẽ sai khi bảng đổi |
| (6) link theo toạ độ | `lich_trinh.map_url(ten, toa_do)`, `ban_do(…, chi_tiet)`, `assistant.py` (`from_settings`, `lich_cho_giao_dien`), `settings.yaml` (chú thích) | điểm có toạ độ ⇒ `…/maps/search/?api=1&query=<vĩ độ>%2C<kinh độ>`; thiếu ⇒ tên + ", Huế" như cũ. Toạ độ giờ **nạp cùng bảng lịch** (không chỉ khi cờ `ban_do_lich` bật); `chi_tiet` (cờ bản đồ) chỉ quyết thêm trường ngày / buổi / thứ tự / toạ độ |
| test | `test_ban_do_lich.py`, `test_b5_lich_trinh.py` | link theo toạ độ / theo tên + `from_settings` nạp toạ độ khi cờ bản đồ tắt; (4) chưa nêu sở thích ⇒ `toi_chua_so_thich`, câu không có "sở thích của bạn"; test cũ (dòng khung tối không có "gợi ý", không bị kiểm cuối bắt) phủ mã mới |

## 3. Cách đã chạy thật

- Build `cd frontend && npm ci && npm run build` (worktree `/tmp/b_nho`).
- Test: 5 file chạm (`test_ban_do_lich`, `test_b5_lich_trinh`, `test_static_ui`, `test_cong_dot_1`, `test_b5b_thoi_tiet`); test rộng không khoá (chạy nền — kết quả ở §4).
- Q1 `capture_all.py` trên nhánh, so `data/phase_11/ban_do/q1/main_2a2a40e.jsonl` (**dùng lại mốc**: `main` `2a2a40e` → `1611d34` không đổi `backend/` ngoài
  `tests/test_static_ui.py` — `git diff --stat`).
- Server thử **cờ như `settings.yaml`** (bản đồ tắt — giống production): `uvicorn api.app:app --port 8874` từ `backend/` của worktree; tắt bằng TaskStop.
- `uv run python data/phase_11/lich_nho/tools/kiem_luu_lich.py http://127.0.0.1:8874/ <thư mục> /tmp/b_nho/backend` — 1 lượt biểu mẫu (2 ngày · Di tích),
  bấm 2 nút, đọc clipboard + file tải, so link với `lt.map_url` + bảng toạ độ thật.
- Câu ngoài kho: `curl POST /api/chat` (câu tự viết).

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Test 5 file chạm | đạt (lần đầu 363 đạt / 1 hỏng do test gọi `ban_do` kiểu cũ ⇒ sửa test, file đó 11 / 11 đạt) |
| Test rộng (không khoá) | **735 đạt**; 1 hỏng + 1 lỗi = đúng 2 test cần khoá (như sổ tay) |
| Q1 chuỗi gửi model | **228 / 228 giống byte** với mốc. Lưu ý: bộ Q1 không có lượt lịch câu gõ tự do (cờ `lich_trinh` tắt) ⇒ (4) chỉ kiểm bằng test đơn vị |
| (1) | tên file `lich-trinh-hue.txt`; báo "Đã sao chép lịch."; **clipboard = file tải**; chữ lịch đang hiện nằm trọn trong file; dòng đầu = câu + lựa chọn; dòng cuối = câu "có thể sai"; 0 lỗi console / CSP |
| (6) | 4 / 4 link đúng như code tính (3 theo toạ độ, 1 theo tên — điểm thiếu toạ độ) và có trong file tải |
| Cổng ổn định | `/health` 5 / 5; CSP cờ tắt = chuỗi cũ; câu trong kho (lượt biểu mẫu) + câu ngoài kho (`ngoai_pham_vi`, 0 nguồn); `chat_metrics` mới = 2 = số câu; chữ câu hỏi trong log = 0 |

Dữ liệu: `data/phase_11/lich_nho/` (`kiem_tat_ban_do.json`, `tat_ban_do/lich_tai_ve.txt` + `luot_lich.png`, `q1/nhanh.jsonl`, `chat_metrics.log`, `tools/`).

## 5. Lỗi và giới hạn

- **(6) toạ độ chưa ai kiểm bằng mắt** (C197 dặn mở 17 link trước khi đổi). Quan sát: "Kinh thành Huế (Ngọ Môn – Kỳ Đài)" có toạ độ 16,4694; 107,5822 — phía đông
  bắc Đại Nội, có thể là toạ độ cả khu Kinh thành chứ không phải Ngọ Môn / Kỳ Đài ⇒ link mới có thể mở lệch. Danh sách để User mở:
  `data/phase_11/lich_nho/kiem_17_link.md` (17 dòng: link mới ↔ link cũ, cột "Đúng chỗ?"). Điểm sai ⇒ bỏ toạ độ điểm đó (về link tên) — việc dữ liệu, A / User quyết.
- (4) chỉ đổi đường câu gõ tự do (biểu mẫu không có trường buổi tối ⇒ `hoi_toi` luôn tắt); cờ `lich_trinh` đang tắt ⇒ người dùng hiện chưa thấy.
- (1) clipboard chỉ chạy trên https / localhost (giới hạn của trình duyệt); bản deploy có https.
- Toạ độ giờ nạp khi cờ `lich_trinh_bieu_mau` bật (đang bật) ⇒ máy deploy **phải có** `data/phase_9/lich_trinh/diem_toa_do_v5.json`, không thì không khởi động (A đã
  ghi allow-list vào checklist deploy).
- Ảnh chụp từng phần tử có thanh đầu trang (cố định) đè lên giữa ảnh — do cách chụp, không phải lỗi giao diện.

## 6. Bàn giao cho người kiểm

- Đọc: `git diff d0adf31..098a710` (nhánh `p11-lich-nho`; phần dưới là nhánh bản đồ đang review riêng).
- Rủi ro cần chạy lại: (1) chữ file = chữ đang hiện, không lấy HTML thô; (4) câu mới không bị kiểm cuối "nói ngược" bắt; (6) link điểm thiếu toạ độ giữ như cũ,
  link mới không có chữ model.
- Script: `data/phase_11/lich_nho/tools/kiem_luu_lich.py` (≈ 0,0004 USD / lần). Worktree `/tmp/b_nho` giữ tới khi review xong.
