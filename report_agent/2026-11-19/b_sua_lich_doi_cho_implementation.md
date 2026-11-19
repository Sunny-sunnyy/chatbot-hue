# Implementation Report: Phase 9 bước 5 — sửa lịch bằng lời, ca "dời hai điểm trong một câu" do code đọc (cờ `sua_lich_doi_cho_code`)

Người làm: B (Claude Code — Fable 5.2). Bộ dò hàm thuần: C (B không xem trước khi code xong). Review code + đọc kết quả lượt thật: E. Duyệt plan, gộp, bật cờ: A (User chọn bật 19/11/2026 sau khi người thứ hai đọc đạt).
Date: 10:14 19/11/2026 (`date`). Lượt thật chạy 09:51–09:56 19/11/2026.
Plan (private): `data/phase_9/sua_lich_doi_cho/PLAN.md` (A duyệt bản sha `e41eb53cad14`). Chẩn đoán gốc: lượt đo cuối 18/11 (`b_do_cuoi_b7_implementation.md` mục 4.2).

> **Kết luận một dòng:** bộ 10 chuỗi sửa lịch đã thấy đạt **9 / 10** (cả hai lần chạy; 18/11: 7 / 10), **0 lượt sửa sai lịch**; cờ đã bật. Chỉ một mẫu câu hẹp được code đọc — mọi câu khác vẫn như trước.

Từ dùng: **chuỗi** = một cuộc nhiều lượt của bộ đo sửa lịch · **đạt cả hai lần** (pass^2) = chuỗi chỉ tính đạt khi cả hai lần chạy đều đạt · **"chưa hỗ trợ"** = hành động model trả khi cho rằng bộ hành động không làm được ⇒
lịch giữ nguyên + câu cố định "Chưa làm…" · **dời buổi** = đưa một điểm sang buổi / ngày khác.

## 1. Phạm vi
- Lớp bài toán: câu nêu HAI điểm đang có trong lịch, mỗi điểm kèm buổi đích ("cho A lên sáng ngày 1, còn B để sáng ngày 3"). Bước áp của code vốn làm được (kể cả đổi chỗ hai điểm) nhưng model gắn "chưa hỗ trợ" ổn định.
- Đếm trước khi xây: lớp này là 2 / 19 lượt sửa của bộ đã thấy, nằm ở 2 / 3 chuỗi trượt (một chuỗi trượt 4 / 4 lần trên bản đang chạy, một chuỗi 1 / 2). Chuỗi trượt thứ ba ("chỉ đi buổi sáng") là lớp khác — ngoài phạm vi, vẫn trượt.
- Không đổi lời dặn, mô tả công cụ, số lần gọi model.

## 2. Thay đổi chính
- `backend/llm/sua_lich_v2.py` — hàm thuần `doi_buoi_tu_cau`: đọc câu theo **danh sách cho phép**. Chỉ nhận khi câu có ĐÚNG hai vế, mỗi vế gồm: tên một điểm đang có trong lịch + một từ dời đứng giữa tên và buổi
  (lên / sang / để / về / xuống / qua / vào) + buổi sáng hoặc chiều + (tuỳ) "ngày <số>" trong lịch + vài từ đệm. Gặp bất kỳ chữ nào khác, câu có dấu hỏi, điểm ngoài lịch, hai vế cùng một điểm ⇒ trả rỗng ⇒ giữ câu "chưa hỗ trợ".
  Vế sau không nêu ngày thì lấy ngày của vế trước.
- `backend/llm/len_ke_hoach.py` (`hieu_va_ap`): hàm chỉ chạy khi model ĐÃ trả "chưa hỗ trợ" và KHÔNG trả hành động nào khác; đọc được ⇒ áp hai lần dời qua đúng bước áp sẵn có.
- `backend/llm/assistant.py` + `backend/config/settings.yaml`: cờ `sua_lich_doi_cho_code` (cần cờ `sua_lich_chua_ho_tro`), nay BẬT.
- Lệch plan (A đồng ý): bản đầu dùng danh sách từ CẤM ⇒ bị bắt áp sai (mục 4.1) ⇒ đổi sang danh sách cho phép, hẹp hơn plan.

## 3. Cách đã chạy thật
- Hàm thuần (0 USD): bộ dò của C chạy thẳng hàm trên bảng điểm thật; test trong `backend/tests/test_rao_so_ngay.py` (câu dựng từ tên bảng lúc chạy, không chép câu bộ đo).
- Lượt thật: server thật của bản có cờ bật, qua `/api/chat/stream`, 10 chuỗi đã thấy × 2 lần (thử một chuỗi trước); model + bộ xếp thật. Kết quả: `data/phase_9/sua_lich_doi_cho/luot_that/` (private).
- Chụp yêu cầu gửi model cùng ngày, cờ bật ↔ `main`: giống byte 228 / 228.

## 4. Kết quả quan sát
### 4.1 Hàm thuần — bộ dò độc lập bắt lỗi của bản đầu
| Bản | Bộ dò của C | Kết quả |
|---|---|---|
| Bản đầu (danh sách từ cấm) | 43 câu | đúng 37 · trả rỗng nhầm 2 · **áp SAI 4** (câu hỏi thông tin, câu nhờ viết, hai câu nêu ngày bằng chữ bị đọc thành "cùng ngày"); review của E tái hiện thêm 2 họ áp sai (câu tả chỗ đang đứng / hoán đổi "cho nhau"; ngày không viết dạng "ngày <số>") |
| Bản danh sách cho phép | 43 câu | đúng 39 · trả rỗng nhầm 4 · áp SAI 0 |
| + bộ bù duy nhất | 20 câu | đúng 19 · áp SAI 1 (câu kết bằng dấu hỏi) ⇒ thêm luật "có dấu hỏi ⇒ không áp" (A chốt) |
| Bản cuối | 63 câu (hai bộ đã ghi, không bộ mới) | **áp SAI 0** · trả rỗng nhầm 4 (được phép) |
13 câu từ chối do chính B đặt ở bản đầu KHÔNG bắt được lỗi nào trong số trên — lỗi do người không viết hàm tìm ra.

### 4.2 Lượt thật (tiêu chí ghi trước)
| Tiêu chí | Ngưỡng | Kết quả |
|---|---|---|
| Lượt sửa SAI lịch | 0 | **0** / 42 lượt sửa (E so vị trí từng điểm trước ↔ sau với nhãn ở cả 42 lượt) |
| 7 chuỗi đang đạt ở 18/11 | giữ nguyên | 7 / 7 đạt cả hai lần |
| Hai chuỗi đích | đạt 2 / 2 mỗi chuỗi | đạt 2 / 2 và 2 / 2 (+ 2 / 2 ở lượt thử); khối thay đổi ghi đúng hai dòng "Đã dời…", 0 điểm khác xê dịch |
| Cả bộ, đạt cả hai lần | — | **9 / 10** (18/11: 7 / 10; mốc trước cờ "chưa hỗ trợ": 9 / 10) |
| Câu sửa chưa làm được / câu không phải sửa (bộ chặn 17/11) | 0 áp nhầm | 0 / 45 câu × 20 lịch thật — chạy THẲNG hàm (0 USD) thay cho lượt có phí 14 câu của plan: hàm trả rỗng thì dù model trả gì code cũng không áp (lệch plan, A nhận) |
Chuỗi còn trượt: lượt "chỉ đi buổi sáng" — "Chưa làm", lịch giữ nguyên, 2 / 2 lần (ngoài phạm vi). Tiền thật: **0,0297 USD** (72 lượt, đọc log).

## 5. Lỗi và giới hạn
- **Mẫu hẹp, cố ý:** câu ba vế, câu không có từ dời ("ngày 3 A sáng, ngày 1 B sáng"), buổi tối, ngày nói bằng chữ ("ngày đầu", "hôm sau"), câu kết bằng dấu hỏi ("… ạ?"), câu có lời chào ngăn bằng dấu phẩy ⇒ vẫn "chưa hỗ trợ". Từ chối nhầm được chấp nhận để không áp sai.
- Chỉ cứu ca model ĐÃ trả "chưa hỗ trợ"; model trả hành động sai khác thì hàm không chạy.
- **Không đếm trực tiếp được** hai lượt đích được sửa nhờ code hay do model tự trả hai lần dời: khoá `doc_cau` chỉ nằm ở sổ vết (lượt đo không bật). Suy ra gián tiếp: chuỗi đó trượt 4 / 4 lần trước thay đổi, đạt 4 / 4 lần sau.
- Bộ đã thấy (đã dùng > 10 lượt đo) ⇒ "ca này hết trượt trên bộ đã thấy", không phải ước lượng trên câu mới; bộ chuỗi kín không mở.
- Test nối dây dùng model thay thế; hành vi model thật chỉ có ở lượt thật 4.2.

## 6. Bàn giao cho người kiểm
| Kiểm gì | Lệnh (ở gốc repo, chỉ đọc) | Phải ra |
|---|---|---|
| Kết quả lượt thật | `python3 -c "import json;c=json.load(open('data/phase_9/sua_lich_doi_cho/luot_that/ca_bo/cham.json'));print(sum(v['pass_k'] for v in c.values()),len(c),[k for k,v in c.items() if not v['pass_k']])"` | `9 10 ['S08']` |
| Cờ đang bật | `grep -c "sua_lich_doi_cho_code: true" backend/config/settings.yaml` | `1` |
| Test của hàm | `cd backend && uv run python -m pytest tests/test_rao_so_ngay.py -q` | `44 passed` |
