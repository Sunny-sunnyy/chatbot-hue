# Ghép main vào nhánh "đổi chỗ ngày 1 với ngày 2" (nhánh `p9-b-doi-cho-ngay-gop`, cờ `sua_lich_doi_cho_ngay` vẫn TẮT)

Viết: 18:59 21/11/2026 (giờ `date`), phiên B — KHÔNG phải người viết tính năng (phiên C viết ngày 20/11 trên nhánh `p9-c-doi-cho-ngay` `d12c42e`, phiên E đã review; report gốc:
`report_agent/2026-11-20/c_doi_cho_ngay_implementation.md`). Việc của trang này: nhánh gốc chậm main 252 commit và cùng sửa `backend/llm/sua_lich_v2.py` với hai bản sửa lịch của ngày 21/11
(buổi tối, tin vừa sửa vừa hỏi) ⇒ ghép main vào, giải xung đột, kiểm lại. Quyết định đang chờ: nhánh này gộp được vào main với cờ tắt chưa. Nhánh gốc của phiên C không bị đụng.

Từ dùng: *cờ* = một dòng bật / tắt trong `backend/config/settings.yaml` · *lần hiểu ý* = lời gọi model riêng đọc tin sửa lịch, trả danh sách hành động có tên · *khối thay đổi* = mấy dòng đầu thẻ lịch do code viết.

## 1. Xung đột và cách giải

Hai lần ghép (main `7fe99821`, rồi main `15b9d193` sau khi bản sửa "tin vừa sửa vừa hỏi" vào main). Mọi xung đột đều là hai bên thêm / sửa dòng KỀ nhau; không chỗ nào hai bên sửa cùng một logic.

| File | Hai bên | Giải |
|---|---|---|
| `backend/config/settings.yaml` | dòng cờ `sua_lich_buoi_toi`, `sua_lich_kem_hoi` (main) ↔ `sua_lich_doi_cho_ngay` (nhánh) | giữ cả ba dòng |
| `backend/llm/assistant.py` | ba trường cờ đó trong lớp cờ | giữ cả ba |
| `backend/llm/sua_lich_v2.py` | từ điển lý do `CAU_LY_DO`: main thêm mục `ban_ngay`; nhánh thêm từ điển `CAU_LY_DO_NGAY` ngay sau | mục của main, rồi từ điển của nhánh |
| `guides/RUNBOOK_BAN_GIAO.md` | hai dòng bảng kề nhau, mỗi bên sửa một dòng | mỗi dòng lấy bản đã sửa của nó |

Git tự ghép phần còn lại, gồm `backend/llm/len_ke_hoach.py`. Chỗ hai tính năng gặp nhau, phiên B đọc lại: trong `hieu_va_ap`, dòng gắn dấu "tin còn có câu hỏi" đứng SAU chỗ tính năng đổi chỗ ngày thay cả kết quả áp
(`kq = sl.doi_cho_ngay(...)`) ⇒ dấu đó không bị mất; `_cau_khong_doi` tra `CAU_LY_DO | CAU_LY_DO_NGAY` — mục `ban_ngay` mới không trùng khoá nào.
Bản ghép = main `15b9d193` + đúng 8 file của nhánh gốc (+291 −6, cùng con số với nhánh gốc so gốc chung).

## 2. Lệnh kiểm trên bản ghép [máy kiểm, 0 đồng; từ `backend/`, từng file một]

| Lệnh | Đầu ra |
|---|---|
| `uv run pytest tests/test_doi_cho_ngay.py -q` | `26 passed` |
| `tests/test_sua_lich_kem_hoi.py` · `tests/test_sua_lich_v2.py` · `tests/test_sua_lich_buoi_toi.py` · `tests/test_rao_so_ngay.py` · `tests/test_len_ke_hoach_v2.py` | `7 passed` · `13 passed` · `7 passed` · `44 passed` · `93 passed` |
| Cờ tắt giống từng byte so với main: mã băm của sáu lời dặn sửa lịch, năm khuôn hành động, chữ gửi lần hiểu ý cho lịch 2 và 3 ngày, cả file lời dặn và cả file generator | 15 / 15 giống |
| `git diff --check origin/main` | sạch |

## 3. Chưa làm · giới hạn

- CHƯA có lượt thật nào trên bản ghép (lượt thật khoảng 4 lượt + bật cờ: xếp vào làn đo sau, như sổ việc ghi). CHƯA chạy cả bộ test. CHƯA nhìn giao diện.
- **Giới hạn khi cờ `sua_lich_doi_cho_ngay` và `sua_lich_kem_hoi` cùng bật:** tin "đổi chỗ ngày 1 với ngày 2, mà vé … bao nhiêu?" ⇒ lịch KHÔNG đổi; khối thay đổi có dòng "Chưa làm: đổi chỗ, gộp hay tách các ngày…"
  cộng dòng báo câu hỏi chưa được trả lời. Lý do: bộ đọc câu đổi chỗ ngày chỉ nhận câu đúng khuôn (danh sách chữ cho phép), gặp chữ lạ thì từ chối — đúng thiết kế "từ chối nhầm được phép, áp sai thì không".
  Người dùng gửi riêng lệnh đổi chỗ thì được. Chưa có lượt thật cho tình huống này.
- Nhánh gốc mang theo bốn dòng runbook đổi chữ "để sau lượt đo cuối" thành "GIỮ GIỚI HẠN (phiên điều phối chốt 20/11)" — không thuộc tính năng đổi chỗ ngày, giữ vì đúng quyết định ngày 20/11.

**Một dòng cuối:** phép này KHÔNG cho biết model có còn trả đúng tín hiệu "đổi chỗ ngày" sau các thay đổi lời dặn ngày 21/11 hay không (chỉ lượt thật cho biết) · hướng rộng hơn: không · đếm rẻ nhất: không.
