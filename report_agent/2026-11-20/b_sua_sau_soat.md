# Sửa sau soát khác hãng + lỗi "gõ lại câu cũ" — nhánh `p9-b-sua-sau-soat-2011` (B, 09:26 20/11/2026, giờ `date`)

Trạng thái (cập nhật 09:39 20/11/2026): **E review READY (0 blocker, 0 major, 3 minor ghi thành giới hạn); phép thật của phần 3 ĐẠT; tám file test 384 đạt; chờ phiên điều phối gộp.** Bảng đối chiếu đợt soát (riêng tư): `data/review_khac_hang/2026-11-19_diem_dung_buoc_5/DOI_CHIEU.md`.

| # | Sửa gì | Vì sao (đã tái hiện bằng hàm thật) | Code | Bằng chứng [máy kiểm] |
|---|---|---|---|---|
| 1 | Sửa lịch bằng lời: hai vế dời cùng MỘT đích (cùng ngày, cùng buổi) ⇒ code không đọc câu, trả câu "chưa làm" | Trước: lần dời sau tự đổi chỗ ngược lần dời trước ⇒ lịch y nguyên mà báo "đã dời" hai điểm (reviewer khác hãng nêu, nhóm tái hiện) | `backend/llm/sua_lich_v2.py` +3 dòng (`doi_buoi_tu_cau`) | test mới trong `tests/test_rao_so_ngay.py` đỏ trên code cũ, xanh sau sửa; file 44 đạt |
| 2 | Cờ `nho_ten_goi_y`: câu gõ có dấu ngắt câu ở GIỮA không được coi là câu xin liệt kê lại | Trước: "Liệt kê các chỗ đó. Đi được không?" bị nhận (dấu chấm bị bỏ trước khi khớp khuôn) ⇒ câu hỏi có / không về cả nhóm mất dòng tên nơi | `backend/llm/ten_goi_y.py` +2 dòng | test đỏ–xanh; hai bộ dò của việc 2 không đổi số (nhận 9 / 20 và 5 / 5 · bắt nhầm 0 / 32 · 0 / 3 · 0 / 10); lượt chạm 0 / 46 · 1 / 106 |
| 3 | Cờ `nho_ten_goi_y`: câu gõ lại NGUYÊN VĂN một câu hỏi cũ ⇒ lượt đó không nhận dòng ghi chú (lịch sử như cờ tắt) — CHỈ khi câu không có từ trỏ lại (đó / này / ấy / thứ…) VÀ lượt liền trước không có dòng ghi chú | Test trình duyệt 20/11: hỏi A ⇒ hỏi B ⇒ gõ lại A thì trợ lý trả lời câu B: cờ bật 0 / 3 đúng, cờ tắt 3 / 3; diễn đạt lại thì đúng 3 / 3; lượt giữa cũng có ghi chú thì đúng 3 / 3. Hai điều kiện hẹp: câu trỏ lại ngắn ("quán đó ở đâu?") hay bị gõ lại và CẦN ghi chú; lượt liền trước có ghi chú thì không lệch dạng | `backend/llm/ten_goi_y.py` (`la_cau_go_lai`, ~12 dòng), commit RIÊNG `b1ebb38` để gỡ được | test mới đỏ khi bỏ từng điều kiện (3 kiểu phá), xanh với bản đủ; 19 đạt; đếm trên bộ 17 chuỗi đích và bộ 80 kịch bản: 0 / 46 và 0 / 106 lượt trùng nguyên văn ⇒ không đo lại hai bộ đó |

**Lượt thật (E chạy bằng trình duyệt thật trên `470290a`, đọc tay 100 %, 0,0154 USD / 33 lượt; hồ sơ riêng tư `data/test_cuoi/chay_2026-11-20/LOI_GO_LAI_CAU_CU.md` mục 4):** phần 3 —
chuỗi gốc × 3 mỗi bên: bản sửa cờ bật đúng **3 / 3** (trước sửa 0 / 3), cờ tắt 3 / 3; lịch sử lượt 3 của cả 6 lượt giống nhau · chuỗi "câu trỏ lại gõ lại" × 3: lượt 4 nói về nơi mới **3 / 3**,
giữ đủ dòng ghi chú ⇒ giữ commit `b1ebb38`. Phần 1, 2 CHƯA có lượt thật (test bằng đồ giả + tái hiện bằng hàm thật).
**Test dựng app trên `470290a`, Python 3.13.15, từng file nối tiếp [máy kiểm]:** `test_b3_memory` 13 · `test_api_chat` 15 (nạp khoá) · `test_chat_stream` 23 · `test_sua_lich_v2` 11 · `test_rao_so_ngay` 44 ·
`test_nho_ten_goi_y` 19 · `test_b5_lich_trinh` 245 · `test_lich_vao_hoi_thuong` 14 ⇒ 384 đạt, 0 hỏng. Cả bộ test: một lượt trên `main` cuối (phiên điều phối xếp).
**Phép chụp chuỗi gửi model [máy kiểm, 0 USD, không mạng]:** 228 ca một lượt (bộ câu mẫu + bộ an toàn + ca khói qua hai đường chat), nhánh `470290a` so với `main` chạy cùng buổi: **228 / 228 giống từng byte** (`cmp`; mỗi ca 2 lần bắt). Các ca này không có lịch sử ⇒ phép này khoá "lượt không lịch sử không đổi"; lượt có lịch sử khoá bằng test + phép thật ở trên.
**Review E:** 3 minor, không sửa code — bộ từ trỏ thiếu "trước", "đây" · lỗ câu cụt · hai điểm cùng buổi nay ra "chưa làm" — cả ba đã ghi ở sổ tay bàn giao mục 10.
Lỗ đã biết của phần 3 (lập luận, chưa đo): câu hỏi CỤT không có từ trỏ ("địa chỉ ở đâu?") gõ lại nguyên văn sau một lượt KHÔNG có ghi chú ⇒ mất ghi chú của các lượt trước nữa.
Giới hạn ghi sổ tay bàn giao mục 10 trong cùng nhánh (chỉ chữ, không sửa code): câu trả lời hai nơi thiếu lưu ý của nơi thứ hai · câu trộn "nhờ làm thay + hỏi thông tin" · nút PowerPoint ở thẻ lịch cũ · file PowerPoint không có mục Nơi ở · số phút đi xe trùng thời lượng trong lịch · `usd_bo` là cận dưới · chuỗi A ⇒ B ⇒ C (kho thiếu) ⇒ gõ lại A.
Hai điểm sửa khác của đợt soát (stream thiếu phần đuôi · PowerPoint mất câu an toàn sau lượt sửa không đổi lịch) do phiên C viết trên nhánh `p9-c-sua-sau-soat-2011`.

Lệnh kiểm: `cd backend && uv run pytest tests/test_nho_ten_goi_y.py tests/test_rao_so_ngay.py -q` ⇒ 19 + 44 passed (hai tiến trình riêng: 19 passed · 44 passed).
