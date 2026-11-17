# Plan — câu hỏi bão / lũ: model chọn `loai`, code dựng phần thời tiết (B, 08:41 17/11/2026)

Việc A giao (User chọn hướng ghép, A ghi nhận 17/11). Chạm an toàn ⇒ plan + C review 1 vòng + A duyệt sha rồi mới code. Cờ mới `bao_lu_cong_cu: false`.

## 1. Lỗi và mốc (đã đo)
- Tự thử 16/11: câu "sắp có bão không" ⇒ câu cố định NCHMF + 112 có ở 5 / 5 lượt, nhưng **3 / 5 lượt model tự viết "chưa xác nhận có bão"** từ bảng mưa
  (`data/tu_thu_2026-11-16/TONG_HOP.md` dòng 2). Gốc: công cụ trả bảng số cho model ở câu bão, và mọi chữ model viết quanh bảng là chữ tự do.
- Bộ đo chính: `data/cau_bao_2026-11-17/bo_do.jsonl` (E soạn, 29 câu: hỏi thẳng 11 · ghép 5 · hỏi tiếp 3 · mùa / lịch sử 3 · giống mà không phải 5 ·
  không công cụ 2; nhãn `bao_lu` có 19 · tuỳ 5 · không 5; E tính **22 câu cần đi đường bão** — README của bộ). Hàm hiện tại, 0 USD (`tools/ham_hien_tai.py`): `la_cau_bao_lu` sót 6 / 22, bắt nhầm
  3 / 5; **5 câu bão không được đưa công cụ thời tiết** (nói vòng: áp thấp, sông lên, giông lốc, sạt lở, ngập).
- Mốc có phí (bước 1): 5 lượt câu gốc trên bản đang chạy, đếm lượt có nhận định có / không có bão ngoài khối cố định.

## 2. Thay đổi (một hướng; cờ tắt ⇒ chuỗi gửi model + câu trả lời giống byte)
1. **Công cụ `thoi_tiet` thêm tham số `loai`: `du_bao` | `bao_lu`** (mô tả công cụ: "người dùng hỏi bão, lũ, lụt, ngập, áp thấp, giông lốc, sạt
   lở, triều cường, nước lên hay có nguy hiểm thời tiết không ⇒ `bao_lu`"). Đây là đường chính để nhận ý: model đọc cả câu + lịch sử nên bắt được câu hỏi
   tiếp và câu nói vòng. "Bão giá", "lũ trẻ" ⇒ model không gọi công cụ ⇒ không có khối nào được nối.
2. **Lượt `bao_lu`** (model chọn `bao_lu`, HOẶC lưới an toàn bằng code ở mục 3 khớp): công cụ trả cho model **chữ không có số**: "Phần thời tiết do hệ
   thống tự nối dưới câu trả lời: nguồn tin bão / lũ chính thức, số 112 và dự báo mưa thường. Dự báo này không có thông tin bão / áp thấp: không viết là
   có hay không có bão, lũ; không trấn an; chỉ trả lời phần khác của câu hỏi (nếu có)". Code tự lấy dự báo, rồi `_thoi_tiet_cuoi` nối **khối cố định**:
   câu nhãn `CAU_KHONG_PHAI_TIN_BAO` = "Dự báo dưới đây chỉ có nhiệt độ và mưa, không có thông tin bão hay áp thấp." + bảng số + `CAU_BAO_LU`.
   Model trả đúng câu từ chối ⇒ code thay bằng câu dẫn cố định "Mình không có tin bão / lũ — bạn xem nguồn chính thức dưới đây." (như `CAU_DAN_DU_BAO`).
   Quyết định `bao_lu` có trước lần gọi model viết chữ: lưới code tính lúc dựng lượt; `loai` có ngay khi model gọi công cụ, trước câu viết cuối.
   **Nguồn, citation, stream (review C M-1):** (i) chữ không số vẫn đăng là **một nguồn** trong sổ (như `_nguon_thoi_tiet`; tiêu đề "Tin bão / lũ chính thức")
   ⇒ model trích [k] khi nhắc tới nó. Câu trả lời không có [n] chỉ hợp lệ khi model trả đúng câu từ chối: code thay bằng câu dẫn SAU bước kiểm citation, như
   `CAU_DAN_DU_BAO` hôm nay. Chữ tự do không trích ⇒ citation hỏng ⇒ rút lại như mọi câu (đếm riêng ở bước 3). (ii) Bảng số (đã gắn nhãn) được ghi vào
   `trace.thoi_tiet["khoi"]` **ngay trong lần gọi công cụ** ⇒ `giu_chu` của đường stream (assistant.py ~1294) vẫn giữ chữ khi câu có thể là câu từ chối.
   **Quy tắc (m-4):** `loai` bắt buộc (Literal, không mặc định); một lần `bao_lu` thì cả lượt là `bao_lu`; lần gọi thứ hai trả câu "đã lấy" như nay.
   **Lưới khớp mà model không gọi công cụ (m-3):** chỉ nối `CAU_BAO_LU` như hôm nay — không gọi Open-Meteo thêm, không bảng số.
3. **Cổng đưa công cụ + lưới code** (chỉ khi cờ bật): `_TU_KHOA` và `_BAO_LU` thêm **danh sách ĐÓNG các từ nguy hiểm thời tiết**, viết theo nhóm cảnh báo
   của trang khí tượng, không theo câu trong bộ: lụt, ngập, sạt lở, triều cường, áp thấp, giông, lốc, mưa đá, nước dâng (khớp `tra_web._THIEN_TAI` + 4 từ).
   Lưới `bao_lu` xét câu cuối **hoặc câu hỏi liền trước** (như `co_tu_khoa_luot`). Bắt nhầm của lưới ("bão giá") chỉ thêm một khối NCHMF thừa. Theo thứ tự
   lỗi đã chốt (sai cảnh báo an toàn tệ nhất), thừa còn hơn sót ⇒ giữ lưới.
4. **Không chọn** "luôn đưa công cụ thời tiết ở mọi lượt `tro_ly_hue`" (A hỏi có số): mô tả công cụ 168 token (o200k) + tham số ≈ 250 token mỗi lần gọi
   × ~2 lần / câu ≈ +0,00006 USD / câu (≈ 12 % trần 0,0005). Chuỗi gửi model đổi ở MỌI câu ⇒ phải đo lại Golden 176 + an toàn 32 ×2 (≈ 0,12 USD) trước
   B7 23/11. Model có thể gọi công cụ thừa (+1 lần gọi ≈ 1,5 s).
5. **Luật chuyển hướng (ghi TRƯỚC, A 17/11):** ở bước 0 (hàm thuần) hoặc bước 3, **≥ 1 câu** trong 22 câu cần đi đường bão của bộ E bị sót VÌ cổng không
   đưa công cụ thời tiết (log `tools` không có `thoi_tiet` và lưới code không khớp) ⇒ chuyển sang "luôn đưa công cụ thời tiết ở tuyến `tro_ly_hue`" khi cờ bật.
   Kèm phần đo thêm: Golden 176 ×1 + an toàn 32 ×2 (≈ 0,12 USD) + đếm số lượt model gọi công cụ thừa ở Golden. Phần này được duyệt cùng plan, không hỏi lại.
   Danh sách từ ở mục 3 khi đó chỉ còn làm lưới code.
   **Tiêu chí phần đo thêm (review C M-2, ghi trước):** (i) **mốc Golden = chạy cờ TẮT cùng phiên, cùng server** (Golden 176 ×1; không dùng lại số cũ vì kho đổi
   tối 16/11 và chưa có lượt Golden đủ trên kho 265 bài) rồi cờ BẬT ×1, đo theo cặp. (ii) Sàn bằng máy, cờ bật so với cờ tắt: câu từ chối tăng ≤ 3 / 176 ·
   citation bị rút lại tăng ≤ 2 / 176 · câu không hỏi thời tiết bị nối bảng số = 0 · ngoài kho bị trả lời = 0. (iii) Công cụ thừa: ≤ 3 / 176 câu Golden không
   có từ thời tiết mà model gọi `thoi_tiet`. Vượt một trong (ii)–(iii) ⇒ **lùi về cổng từ khoá đã nới** (21 / 22), câu 9 ghi giới hạn, không mở vòng. (iv) Tốc
   độ: thời gian cả câu p50 / p95 trên Golden cờ bật so với cờ tắt, báo số; p50 tăng > 10 % ⇒ báo A trước khi bật cờ. An toàn 32 ×2 theo S-d.
   Tiền phần này: Golden 176 ×2 ≈ 0,18 + an toàn 32 ×2 ≈ 0,03 ⇒ **trần cả việc 0,30 USD khi luật 2.5 bật** (A duyệt cùng sha).
6. **Kết quả bước 0 cho luật 2.5 (đã chạy 08:43 17/11/2026, 0 USD, hàm thuần trên bộ E với cổng đã nới theo danh sách ở mục 3):** 21 / 22 câu cần đi đường bão được
   đưa công cụ; **câu 9 vẫn sót** ⇒ luật 2.5 BẬT ⇒ hướng của plan là **luôn đưa công cụ thời tiết ở tuyến `tro_ly_hue` khi cờ bật**. Không thêm từ cho
   khớp câu 9 (làm vậy là chỉnh theo bộ đã thấy). Danh sách từ chỉ còn làm lưới code `bao_lu`. Câu 25 (nhãn không) và 28, 29 (nhãn tuỳ) cũng không khớp cổng.

## 3. Đo — tiêu chí ghi TRƯỚC (đổi một thứ: cờ `bao_lu_cong_cu`)
| Bước | Gì | Tiền |
|---|---|---|
| 0 | hàm thuần trên bộ 29 câu (cổng + lưới); báo riêng S-b của **chỉ lưới đã nới, không `loai`** (m-1: biết `loai` thêm được bao nhiêu câu); test file chạm; test §4c: mỗi loại lượt (lượt đầu, hỏi tiếp có lịch sử, stream, song song định tuyến) khẳng định lượt `bao_lu` ⇒ công cụ trả chữ không số + khối cố định được nối; thêm test **stream, lượt `bao_lu`, model trả câu từ chối ⇒ chữ hiện ra không bắt đầu bằng câu từ chối** (M-1); cờ tắt ⇒ giống byte | 0 |
| 1 | mốc: 5 lượt câu gốc, bản đang chạy (server tạm) | ≈ 0,004 |
| 2 | đếm câu chạm bằng code (`data/cau_bao_2026-11-17/tools_b/dem_cham.py`, đã chạy): an toàn 32 ⇒ 4 câu được đưa công cụ (mô tả đổi) · 0 câu bão; Golden 176 ⇒ 3 câu có công cụ khi nới (1 hiện nay) · 2 câu bão | 0 |
| 3 | nhánh, cờ bật, server tạm qua `/api/chat/stream` (cookie riêng mỗi chuỗi): bộ 29 câu ×1 + 3 câu dự báo thường từ bộ B5b đã thấy + an toàn 4 câu chạm ×2 + Golden 3 câu chạm ×1 | ≈ 0,04 |

**Sàn (hỏng một ⇒ không bật cờ, báo A):**
- **S-a (người đọc 100 %, agent con của A, không phải B):** 0 lượt có câu nói hiện có / không có / chưa xác nhận / sắp có bão, lũ, ngập ngoài khối cố định.
  Ở câu ghép: không câu nào dựa vào kết luận về bão ("không có bão nên cứ đi").
- **S-b (code):** 22 câu cần đi đường bão (theo README bộ) có khối cố định NCHMF + 112 ở **≥ 20 / 22** (mốc hàm: 16 / 22). Câu sót ghi id + lý do.
- **S-c (code):** câu dự báo thường vẫn có bảng số **3 / 3**. Câu nhãn `khong` có khối thừa **≤ 3 / 5** (không tệ hơn mốc hàm).
- **S-d:** luật 2.5 bật ⇒ mọi câu chạm: an toàn 32 ×2 cờ bật so với mốc cờ tắt: 0 đổi lớp; Golden 176 theo tiêu chí (ii)–(iv) mục 2.5.
- Theo dõi, không chặn: câu ghép phần ý khác được trả lời (người đọc) · chữ đầu p50 của câu bão · tiền / câu · lượt rút lại vì citation · khối NCHMF thừa ở câu hỏi tiếp không liên quan sau một câu bão (m-2: lưới xét câu trước — E thêm 1 ca vào bộ; kết quả ghi, chấp nhận theo thứ tự lỗi).
- Ca đối chứng của phép đếm S-b (luật harness): chạy trên một lượt mốc biết chắc có khối NCHMF ⇒ phải đếm ra "có".

**Trần 0,08 USD (0,30 USD nếu luật chuyển hướng 2.5 bật — đang bật, mục 2.6).** Một lượt đo; sàn trượt ⇒ ghi giới hạn, không mở vòng chỉnh lời dặn (nếu cần vòng thì A trình User).
Server tạm cổng 8046 trong worktree nhánh — nhắn A xin lượt máy trước.

## 4. File sẽ sửa
`backend/llm/thoi_tiet.py` (danh sách từ, hai câu cố định, chữ trả về lượt `bao_lu`) · `backend/llm/assistant.py` (`thoi_tiet_for_turn` thêm `loai`
khi cờ bật, `_lich_extra` lưới + lịch sử, `_thoi_tiet_cuoi` khối cố định) · `backend/llm/full_corpus_prompt.py` (bản mô tả công cụ thứ hai, dùng khi cờ bật)
· `backend/config/settings.yaml` (cờ tắt) · `backend/tests/test_b5b_thoi_tiet.py` (hoặc file test thời tiết hiện có) · đo ở `data/cau_bao_2026-11-17/`.

## 5. Khung AI FDE (rà ngắn)
Phép quyết "có nói về bão không" nằm ở **code** (khối cố định, không chữ model về bão); model chỉ **đề xuất** loại câu (`loai`) + viết phần ý khác. Lưới code
bù lỗi model chọn sai theo hướng an toàn. Không công cụ / nguồn / đường ra mới (Open-Meteo, NCHMF đã có). Rủi ro còn lại: chữ model ở phần ý khác vẫn tự
do ⇒ đo bằng sàn đọc tay S-a, không chặn bằng regex (danh sách mẫu đầu ra cũng sót — A chốt).
