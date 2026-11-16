# Cột lịch trang "Lên kế hoạch" đổi theo lịch đã sửa bằng lời — implementation report (E, 21:06 16/11/2026)

Việc: User chọn 16/11 tối (A giao, mức nhẹ, chỉ giao diện). Nhánh `p9-cot-lich-theo-sua` trên `origin/main` `6563c22`. Server không đổi, không cờ mới.

## 1. Đổi gì (3 file, +21 −1)
- `frontend/src/App.jsx`: `lichTurn` (lượt mà cột lịch của trang vẽ) = lượt biểu mẫu cuối, **hoặc** lượt sửa bằng lời đã XONG sau nó có ít nhất một thay đổi làm
  được (`lichV2.thay_doi[].duoc`). Lượt sửa đang chạy / bị dừng / lỗi / chỉ có chữ / không đổi được gì ⇒ không đủ điều kiện ⇒ cột giữ lịch tốt gần nhất.
- `frontend/src/LenKeHoach.jsx` (`CotLich`): đầu cột có nhãn "Đã sửa theo lời bạn: <các câu Đã …>" + dòng nhỏ "Biểu mẫu vẫn là bản gốc — xếp lại từ
  biểu mẫu sẽ thay bản đã sửa."; dưới lịch (khi xong) một dòng chỉ dẫn "Muốn sửa lịch bằng lời … bấm Trợ lý Huế rồi nhắn — lịch ở đây đổi theo."
- `frontend/src/lkh.css`: kiểu cho hai dòng trên; câu "Đã …" đã nằm trong nhãn nên không vẽ lần hai trong khung lịch của cột (câu "Không đổi được" vẫn hiện).

Quyết định nhỏ của E (tiêu chí 4): nút "Sửa — điền lại biểu mẫu" **giữ điền theo biểu mẫu gốc** (lượt sửa mượn `truong` của lượt biểu mẫu); bấm nút không làm
mất bản đã sửa — chỉ khi người dùng bấm "Xếp lịch" lại thì bản biểu mẫu mới thay, và nhãn đã nói trước điều đó. Không đồng bộ nút biểu mẫu theo lời (ngoài phạm vi).
Cột dùng khoá riêng (`<khoá lượt>-cot`) để id trong cột không trùng id của cùng lượt đang vẽ trong khung trợ lý.

## 2. Kết quả so 7 tiêu chí ghi trước
Ca chặn route, 0 USD: `data/cot_lich_theo_sua_2026-11-16/pw_cot.py` phát lại luồng SSE THẬT đã thu một lần (`thu_sse.py`) trên bản build của nhánh (server tạm
8043, đã kiểm thư mục chạy) — **20 / 20 phép kiểm đạt**, chạy 3 lần. Có đối chứng trong cùng kịch bản (trạng thái "lịch gốc 5 điểm" và "đã sửa 4 điểm" đều xuất hiện).

| # | Tiêu chí | Kết quả |
|---|---|---|
| 1 | Sửa làm được ⇒ cột = lịch mới, bản đồ đúng số ghim, chép / .ics lấy bản đang hiện | Đạt: ngày 2 còn 4 điểm, bản đồ 3 + 4 ghim, nhãn có câu "Đã bỏ …", chữ sao chép là bản đã sửa. **.ics: chưa đo được ở ca chặn route** (lịch thu không có ngày đi ⇒ giao diện không vẽ nút) ⇒ đo ở lượt thật: 6 sự kiện, không còn điểm đã bỏ |
| 2 | Lượt sửa đang chạy / bị Dừng / lỗi ⇒ cột giữ lịch tốt gần nhất | Đạt (4 ca: đang chạy, bấm Dừng, lỗi 500, đã sửa rồi lượt kế đang chạy) |
| 3 | Thẻ chọn / "không đổi được gì" ⇒ cột giữ nguyên | Đạt (2 lượt không đổi được thật + 1 lượt chỉ có chữ dựng tay; cả khi đứng sau một bản đã sửa). Lượt ra THẺ CHỌN thật: không thu được (câu thử ra "không đổi được") ⇒ thay bằng lượt chỉ có chữ — cùng đường code (lượt không có khung lịch) |
| 4 | Nút "Sửa — điền lại biểu mẫu" không làm mất bản đã sửa lặng lẽ | Đạt: bấm xong cột vẫn là bản đã sửa, nhãn nói biểu mẫu là bản gốc |
| 5 | Biểu mẫu mới ⇒ cột về lịch biểu mẫu mới, nhãn mất | Đạt |
| 6 | Script cũ chờ `.lkh-lich[data-phase="done"]` còn chạy | Đạt — không phải đổi |
| 7 | Khổ 1440 + 390 không tràn ngang | Đạt (390: sửa ở trang Trợ lý rồi quay lại Lên kế hoạch ⇒ cột là bản đã sửa) |

Lượt THẬT cuối (`pw_that.py`, bản build của nhánh, biểu mẫu 2 ngày có ngày đi ⇒ "Bỏ điểm đầu tiên của ngày 2"): cột đổi theo, nhãn đúng, .ics 6 sự kiện
không còn điểm đã bỏ, 0 lỗi console, không tràn. E đã NHÌN 6 ảnh (`data/cot_lich_theo_sua_2026-11-16/anh/`).

Kèm theo yêu cầu của A: ảnh khổ 1440 ngày có ghim sát mép dưới sau khi lề dưới bản đồ lên 60 (`anh/that_1440_ban_do_ngay_2.png`) — ghim không bị dòng ghi công
che, mức phóng không khó coi.

## 3. Test + thời gian + tiền
- `npm run build` đạt (0,5 s); `test_static_ui.py` 4 passed (7,5 s); `pw_cot.py` ≈ 1 phút / lần. Test rộng backend: KHÔNG chạy (nhánh không đổi backend).
- Tiền: lượt thật trên 8043 2 lượt = 0,0006 USD (log server tạm); thu SSE trên 8010 4 lượt ≈ 0,002 USD (ước theo cỡ lượt, chưa tách khỏi log chung).

## 4. Giới hạn / chưa làm
- Cột đổi khi lượt sửa XONG (không đổi dần lúc đang chạy). Tải lại trang = cuộc mới ⇒ cả lịch gốc lẫn bản đã sửa đều mất (như trước).
- Sửa hai lần liền: nhãn chỉ nêu thay đổi của lượt sửa GẦN NHẤT (lịch thì đã gồm mọi thay đổi trước đó).
- Câu đầu trang "Muốn đổi lịch thì điền lại biểu mẫu." chưa sửa (không nằm trong việc giao) — nay có thêm đường sửa bằng lời; A quyết có đổi chữ không.
- Dòng chỉ dẫn hiện cả khi cờ `sua_lich_v2` tắt (giao diện không nhận cờ này từ `/api/tinh_nang`); hiện cờ đang bật.
- Sau review B (READY, 3 minor — đã sửa m-1, m-2 trên nhánh): cột mượn thêm `question` + `summary` của lượt biểu mẫu ⇒ dòng đầu của chữ sao chép / .txt là tóm tắt biểu mẫu;
  nhãn bỏ chữ "bên cạnh" (khổ 390 biểu mẫu nằm phía trên). Ca phá của B: `data/review_cot_lich_2026-11-16/pha.py` (9 / 9).
- Biểu mẫu mới bị LỖI sau một bản đã sửa ⇒ cột chỉ còn dòng lỗi (hành vi sẵn có của lượt biểu mẫu lỗi), bản đã sửa không còn trên cột.
- **Checklist bản công khai:** `Array.prototype.findLast` / `findLastIndex` (ES2023) không được hạ cấp khi build ⇒ trình duyệt rất cũ (Safari < 15.4, Chrome < 97) lỗi ở trang này — thêm polyfill hoặc viết lại bằng vòng lặp trước khi công khai nếu cần hỗ trợ các bản đó.
- Quan sát ngoài phạm vi: ở khổ 1440 khối "Nếu mưa ngày N: …" trong thẻ ngày bị bó thành cột chữ rất hẹp (`anh/that_1440_ban_do_ngay_2.png`, góc trên) — có từ trước, chưa sửa.

**Giải thích ngắn:** trước đây sửa lịch bằng lời trong khung trợ lý thì chỉ khung đó có lịch mới, cột lịch của trang vẫn là bản cũ. Nay cột lịch luôn vẽ bản mới
nhất đã sửa xong, có dòng nhãn nói rõ vừa sửa gì, và nhắc rằng biểu mẫu bên cạnh vẫn là bản gốc.
