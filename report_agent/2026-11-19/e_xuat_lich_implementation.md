# Implementation Report: xuất lịch ra PowerPoint + bản in PDF (cờ `xuat_pptx`, mặc định TẮT)

Người viết: phiên E · 15:25 19/11/2026 (giờ `date`) · nhánh `p9-e-xuat-lich` (đã gộp `main` `26ccef9` vào, đầu nhánh `5692efa` lúc viết) · worktree `/tmp/hr_e_xuat_lich`.
Trạng thái: **chờ review cả nhánh + một lượt rà bảo mật ngắn cho đường GET mới**. CHƯA bật cờ, CHƯA chạy cả bộ test. Tiền API cả việc: ≈ 0,0005 USD (một lượt biểu mẫu khi thử giao diện).
Plan (riêng tư, phiên điều phối duyệt theo sha `7f0b39432419`): `data/xuat_lich_dep_2026-11-19/PLAN.md`. Chủ dự án đã chọn: PDF = in từ trình duyệt · PowerPoint = `python-pptx` · kiểu thiết kế "Di sản" (chọn bằng ảnh mẫu 19/11).

> **Đọc trước:** mục 1–4 viết TRƯỚC review. Mọi chỗ ở đó nói "chỉ ảnh có giấy phép", "trang Nguồn ảnh", "ẩn ảnh không giấy phép khi in" đã bị THAY bởi mục 5b (không ghi công ảnh, dùng đủ ảnh; thêm câu an toàn của lượt). Mục 5b + 5c là trạng thái hiện hành.

## 1. Phạm vi

Người dùng đã có lịch (từ trang Lên kế hoạch hoặc sau khi sửa bằng lời) có thêm hai nút dưới lịch: **In / Lưu PDF** và **Tải PowerPoint**. Lúc tải KHÔNG gọi model: code điền lịch vào trang. Mọi chữ trong file là chữ đã hiện trên trang (tên điểm, giờ, câu tả đã kiểm, ghi chú của lịch) hoặc hằng số của khuôn.
Không làm ở bản đầu: trang chi phí (chờ phần tiền vé của việc "lịch đã lưu") · bản đồ nền, mã QR · nút "tải PDF" một chạm ở server · in dòng dự báo thời tiết · 14 ảnh không có giấy phép ghi trong bảng ảnh.

## 2. Thay đổi chính

| File | Đổi gì |
|---|---|
| `backend/api/lich_pptx.py` (mới) | `trang_lich(lich, cau, …)` — hàm thuần: đối tượng lịch ⇒ danh sách trang (bìa · mỗi ngày ≥ 1 trang, ngày dài chia ĐỀU sang trang "tiếp" · lưu ý + link bản đồ · nguồn ảnh). `dung_pptx(trang, thu_muc_anh)` — vẽ kiểu "Di sản" bằng toạ độ (không file khuôn nhị phân). |
| `backend/api/routes/xuat.py` (mới) | `GET /api/lich/pptx`: không thân, không tham số. Đọc cookie cuộc trò chuyện ⇒ lịch server ĐÃ LƯU ⇒ dựng lại đối tượng lịch bằng đúng hai hàm của lượt trả lời ⇒ file. Không có lịch / hết hạn 30 phút ⇒ 404 có lời. |
| `backend/api/conversations.py` | `lay_lich` tự xét hạn của cuộc (đường chat không đổi: nó dọn cuộc hết hạn trước khi gọi). |
| `backend/llm/assistant.py`, `settings.yaml`, `api/app.py`, `api/routes/cong.py` | Cờ `xuat_pptx` (cần cờ lưu lịch + thư viện, kiểm lúc khởi động) · đăng ký route · khoá `xuat_pptx` trong `/api/tinh_nang` chỉ có khi cờ bật. |
| `frontend/src/LichV2.jsx`, `App.jsx`, `lkh.css` | Hai nút (chỉ hiện khi cờ bật, không hiện ở lịch mẫu) · bố cục IN bằng CSS: chỉ thẻ lịch đang in, mỗi ngày một trang, ẩn nút / bản đồ / ảnh không giấy phép / ảnh quán, tiêu đề + dòng cuối + nguồn ảnh chỉ hiện khi in, bảng màu + phông của kiểu "Di sản". |
| `pyproject.toml`, `uv.lock` | Thêm `python-pptx==1.0.2` (phiên điều phối duyệt). **Sau khi gộp phải `uv sync` một lần ở cây chính** — trước đó test đọc lại file tự bỏ qua và cờ không bật được. |
| `backend/tests/test_lich_pptx.py` (mới) | 12 test, mục 3. |

Quyết định thiết kế đáng biết:
- **Server không nhận dữ liệu lịch từ trình duyệt.** Lịch lấy từ trạng thái đã lưu ⇒ không chữ / đường dẫn tự do nào vào file. Cái giá: chỉ tải được trong 30 phút lịch còn lưu, và file là lịch MỚI NHẤT của cuộc (nút nằm dưới một thẻ lịch cũ vẫn tải lịch mới nhất — dòng báo sau khi tải nói rõ).
- **Hai thứ trạng thái lưu không có:** số nguồn [n] (file không in) và các dòng dự báo thời tiết ⇒ file in một dòng cố định "xem dự báo trước ngày đi" (phiên điều phối đồng ý).
- **Ảnh:** chỉ ảnh có tác giả + giấy phép trong bảng ảnh (26 / 40); mỗi ảnh dùng có dòng ghi công ở trang "Nguồn ảnh". Điểm không có ảnh được phép ⇒ ô hoạ tiết mang tên điểm.
- **Lệch plan:** plan ghi "một khuôn .pptx làm tay" — thực tế vẽ bằng code (phiên điều phối nhận); plan ghi 3 kiểu trang, bản này có thêm trang "Nguồn ảnh" tách riêng và khung link bản đồ trên trang lưu ý.

## 3. Cách đã chạy thật

| Việc | Loại bằng chứng | Kết quả |
|---|---|---|
| Cổng bước 1 (0 USD, không model): lịch dựng lại từ trạng thái lưu ↔ lịch giao diện đã nhận thật (lịch mặc định 2 ngày) và ↔ bản dựng lúc trả lời (1 ngày · 3 ngày có trẻ em + ngày đi · 3 ngày có ô nơi ở) | chạy code thật trên bảng thật | khác 0 trường ở cả bốn (trừ số nguồn + dòng dự báo đã loại trước) |
| `pytest tests/test_lich_pptx.py` (chạy bằng `uv run --with python-pptx==1.0.2`; không model, không bộ tìm; route test dùng bảng điểm thật) | test | 12 đạt |
| Phá code ba chỗ: in lại dòng dự báo cũ · chèn chữ lạ vào trang · bỏ phép xét hạn | thấy ĐỎ | 3 / 3 lần test tương ứng hỏng |
| Dựng file rồi cho **PowerPoint thật của Windows** xuất ra PDF ⇒ ảnh từng trang; người viết nhìn từng ảnh (lịch 2 ngày thật có câu tả · lịch 1 ngày · lịch 3 ngày có trẻ em, có dòng "tối để trống") | file thật, mắt người viết | sau ba vòng sửa: không tràn chữ, không trang gần trống, ảnh không méo, tên điểm không bị cắt |
| Giao diện thật (server của nhánh, cờ bật tạm, một lượt biểu mẫu qua model thật, trình duyệt không giao diện) | lượt thật | hai nút hiện dưới lịch · bấm "Tải PowerPoint" nhận file 518 KB tên `lich-trinh-hue.pptx` · bố cục in xuất ra PDF · 2 / 8 ảnh không giấy phép bị ẩn khi in |
| `npm run build` | — | dựng được |

## 4. Kết quả quan sát

- Lỗi bố cục chỉ lộ ra khi NHÌN ảnh do PowerPoint thật xuất, test không bắt: chữ dài chạy ra ngoài trang (thiếu xuống dòng) · ngày 5 điểm tách thành trang "tiếp" chỉ có 1 điểm · ảnh bìa tràn ngang bị nhoè (ảnh gốc ~640 px) · dòng "tối để trống" bị vẽ như một điểm tham quan · trang lưu ý tách hai trang thưa. Đều đã sửa.
- Bản in lần đầu (trước khi sửa CSS): nội dung chỉ chiếm ~60 % bề ngang trên nền xám, còn sót chú giải bản đồ và dòng "sai thì bấm Sửa". Đã sửa CSS; **CHƯA chụp lại sau khi sửa** (cần một lượt máy ngắn).

## 5. Lỗi và giới hạn

- **Bố cục in sau khi sửa chưa được nhìn lại**; mới thử một trình duyệt (Chromium không giao diện), chưa thử Edge, chưa thử điện thoại.
- File .pptx mới mở bằng PowerPoint trên Windows; CHƯA mở bằng Google Slides / điện thoại (phông Georgia + Arial có sẵn rộng rãi nhưng chưa kiểm).
- Chưa chạy cả `backend/tests`; chưa đo RAM / giây một lượt tải (quan sát: dựng file < 1 giây ở test).
- Ảnh của điểm không có giấy phép vẫn hiện TRÊN TRANG (việc cũ, ngoài nhánh này); nhánh chỉ loại chúng khỏi file tải và bản in.
- Ép trạng thái lưu qua JSON làm mất dòng "tối nghỉ" (khoá ngày là số) — hôm nay server giữ trong RAM nên không dính; ghi để người sau biết nếu lưu ra đĩa.
- Link bản đồ trong file gắn vào ô chữ (giữ màu của kiểu); trên vài ứng dụng xem slide link gắn vào ô có thể không bấm được — chưa thử.

## 5b. Sửa sau review nhánh (C) + một quyết định cũ của chủ dự án bị bỏ sót — 19/11/2026

- **Major của C — câu an toàn của LƯỢT không theo vào file .pptx.** Đúng: câu "bản tin chính thức + 112" của lượt bão / lũ chỉ nằm ở dòng ghi chú của lượt, không nằm trong trạng thái lưu. Sửa: lúc lưu lịch, route lưu kèm đúng HẰNG SỐ đó (`an_toan_cua_luot`); file in nó ở bìa và là dòng đầu (đậm) của trang "Lưu ý trước khi đi". Ba test mới đã thấy ĐỎ trước khi sửa; đã dựng một file thật có câu này và nhìn ảnh do PowerPoint xuất.
- **Bỏ ghi công ảnh, dùng đủ ảnh.** Chủ dự án đã quyết 14/11/2026 "gỡ mọi chữ ghi công khỏi hệ thống" — người viết và phiên điều phối bỏ sót khi làm plan. Nay: bỏ trang "Nguồn ảnh", bỏ bộ lọc "chỉ ảnh có giấy phép" (file dùng mọi ảnh tự host của bảng ảnh — 8 / 8 điểm của lịch mặc định có ảnh thật), bản in không ẩn ảnh nào và không in dòng nguồn ảnh. Đường ảnh vẫn bị kiểm (ngay dưới `/anh/lich/`, không thư mục con, không ".."). Plan có khối "Sửa sau duyệt".
- Minor của C: (m1) nút tải ở mọi thẻ lịch nhưng file là lịch mới nhất — GIỮ, dòng trạng thái đã nói rõ (C: đủ cho bản đầu) · (m2) **bản in giữ dòng dự báo thật của lượt, file .pptx thay bằng dòng chung** — ghi nhận là giới hạn · (m3) đã thêm `xuat_pptx: False` vào danh sách tắt của `tests/test_cong_dot_1.flags_from` (không thì commit bật cờ làm các test dùng hàm đó ném lỗi phụ thuộc) · (m4) **trước khi deploy:** `THU_MUC_ANH` trỏ `frontend/public` — bản deploy chỉ có `dist` thì mọi ảnh thành ô hoạ tiết; và chưa có giới hạn số lượt tải.
- Giới hạn của câu an toàn trong file: chỉ lưu câu bão / lũ của CHÍNH lượt tạo / sửa lịch; lượt sửa sau đó không hỏi về bão thì lịch lưu mới không còn câu này (màn hình cũng vậy). Vòng 2 của C: major đóng, ready về phía người đọc diff.
- Trạng thái test sau sửa: 15 test của nhánh đạt (chạy với `--with python-pptx`); giao diện dựng được. Lỗi trang cuối bản in (trang 3 chỉ có hai dòng) đã thêm luật CSS, CHƯA chụp lại.

## 5c. Đề xuất sau (KHÔNG làm ở nhánh này) — ý ngoài thẩm mỹ thấy ở bốn bài thi thiết kế

Cuộc thi bốn coding agent khác hãng (đề + bài + bảng sàn: riêng tư, `data/thi_thiet_ke_2026-11-19/`): chủ dự án giữ kiểu "Di sản" của nhóm. Hai ý đáng mượn về sau: (1) trang **"Tổng quan hành trình"** — mỗi ngày một cột, liệt kê điểm + giờ, để nhìn cả chuyến trong một trang (hai bài có); (2) dòng **"buổi tối để trống"** vẽ thành một ô có chủ ý (nhãn + lý do) thay cho một dòng chữ. Lưu ý từ lượt kiểm sàn: hai bài đó tự thêm nhãn / câu không có trong dữ liệu — nếu mượn bố cục thì chữ vẫn phải lấy từ lịch.

## 6. Bàn giao cho người kiểm

- Đọc diff: `git diff origin/main...origin/p9-e-xuat-lich -- backend frontend pyproject.toml` (13 file, ~670 dòng thêm; `uv.lock` 118 dòng do công cụ sinh).
- Rà bảo mật đường GET mới (skill `agent-security-review`): yêu cầu không thân / không tham số có thật không · lịch chỉ đến từ cookie cuộc của chính người gọi · file không chứa chữ tự do · không đọc file ngoài `frontend/public/anh/lich/` (đường ảnh lấy từ bảng ảnh của server, không từ yêu cầu) · chưa có giới hạn số lượt tải mỗi phút (người viết CHƯA thêm — nhờ cho ý kiến có cần ở bản local không).
- Nên tự kiểm bằng cách khác: mở `data/xuat_lich_dep_2026-11-19/buoc_2/anh/` (ảnh do PowerPoint xuất) và file mẫu; dựng một lịch khác (ví dụ 3 ngày nhiều điểm không trẻ em — người viết chưa nhìn ca ngày 5 điểm ở lịch 3 ngày) rồi nhìn.
- Việc còn lại: chụp lại bản in · thử ba lịch trên giao diện thật · `uv sync` sau gộp · bật cờ là việc hỏi chủ dự án.

## 5d. Sau khi gộp main + lượt thử qua trình duyệt (phiên E, 19:24 19/11/2026, giờ `date`) — trạng thái HIỆN HÀNH của ba việc còn nợ

Nhánh đã gộp `origin/main` `79b0154` ⇒ `d1afba5` (hai chỗ xung đột: dòng cờ ở `backend/config/settings.yaml` — giữ mọi dòng; `flags_from` ở `backend/tests/test_cong_dot_1.py` — giữ cả `xuat_pptx` lẫn `lich_vao_hoi_thuong` trong danh sách tắt). Cờ `xuat_pptx` và `noi_that_lam_thay` vẫn TẮT trong file cấu hình; lượt thử bật tạm hai cờ trong worktree rồi trả lại (`git status` sạch).

| Việc | Kết quả | Nhãn |
|---|---|---|
| Ba file test, mỗi file một tiến trình, có và không file env | `test_lich_pptx.py` 15 đạt · `test_cong_dot_1.py` 22 đạt · `test_settings_env.py` 6 đạt — giống nhau ở cả hai cách chạy | [máy kiểm] |
| File PowerPoint tải qua giao diện thật ở lượt có câu hỏi về bão | 4 trang; câu "gọi 112" có ở bìa VÀ ở trang "Lưu ý trước khi đi"; không có trang hay chữ nguồn ảnh; thẻ lịch trên màn hình có câu an toàn | [máy kiểm — script đọc lại file tải về] |
| Bấm link "trang Chỗ ở" trong ô chat thật (nợ của việc "nói thật giới hạn") | chuỗi hai lượt ra câu nói thật "chưa đặt phòng thay bạn được…"; bấm link ⇒ địa chỉ `#/cho-o`, tiêu đề "Chỗ ở theo khu", vẫn một tab | [máy kiểm; có ảnh màn hình trong thư mục dữ liệu riêng] |
| Bản in PDF: trang cuối không còn chỉ hai dòng | **CHƯA ĐẠT** — bản in lịch mặc định 2 ngày vẫn ra 3 trang, trang 3 chỉ có hai dòng ghi chú (31 · 38 · 2 dòng chữ). Luật CSS thêm buổi chiều không có tác dụng: khối của ngày cuối không được phép ngắt giữa chừng nên hai dòng sau nó không có chỗ bám | [máy kiểm — đếm dòng chữ từng trang của file PDF] |
| Ảnh điểm trong bản in | 8 / 8 ảnh hiện | [máy kiểm] |

Tiền lượt thử: khoảng 0,004 USD (ước theo số lần gọi model; chưa đối chiếu sổ tiền). Lần chạy đầu của script thử hỏng ở hai bước vì chính script (phép chờ bị chính sách bảo mật của trang chặn) — đã sửa script, chạy lại ra bảng trên; bản in giống nhau ở cả hai lần.

Giới hạn / việc còn lại: (1) lỗi trang cuối bản in còn nguyên — hình thức, không sai nội dung; cách sửa nhỏ nhất chưa thử: cho riêng ngày cuối được ngắt trang giữa các điểm để điểm cuối đi cùng hai dòng ghi chú. (2) Chỉ thử lịch mặc định 2 ngày; lịch 1 ngày và 3 ngày chưa in lại sau khi gộp. (3) Sau khi nhánh vào main cần `uv sync` ở cây chính (thư viện `python-pptx`).

**Sửa tiếp lỗi trang cuối bản in (19:26 19/11/2026, một lần thử, một dòng CSS ở `frontend/src/lkh.css`):** cho riêng ngày CUỐI được ngắt trang giữa các điểm. Chạy lại đúng lượt thử trên: bản in vẫn 3 trang nhưng trang 3 nay là MỘT khối 8 dòng liền nhau (ghi chú của lịch · dòng Nguồn · hai dòng lưu ý), không còn hai dòng lẻ; trang 2 kết thúc gọn ở điểm cuối của ngày 2 (31 · 34 · 8 dòng chữ) [máy kiểm — đếm và đọc chữ từng trang; CHƯA có người thứ hai nhìn file PDF]. Hai việc kia của lượt thử ra y như bảng trên. Giới hạn còn lại: lịch 2 ngày vẫn in ra 3 trang; lịch 1 và 3 ngày chưa in lại. Dòng "CHƯA ĐẠT" ở bảng trên là kết quả TRƯỚC bản sửa này.
