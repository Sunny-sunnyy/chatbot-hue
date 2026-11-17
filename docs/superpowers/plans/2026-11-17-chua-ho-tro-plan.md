# Plan — sửa lịch: model nhận "câu sửa chưa làm được" (`chua_ho_tro`) (C, 09:21 17/11/2026; sửa theo review E 3 minor 09:27 17/11/2026)

User chọn 17/11 (A ghi): không bắt câu người dùng bằng rào code ⇒ MODEL của lần hiểu ý nhận ý. Mức nhẹ (≤ 0,30 USD, không đổi kiến trúc): E review
một vòng ⇒ A duyệt sha ⇒ code. Nền: `main` `216c821` (nhánh `p9-chan-lich-gia`; dòng "Chưa làm" đúng việc khi model đã nhận là câu sửa, bỏ `**`).

## 1. Lỗi và số đã có
- Tự thử 16/11: "đổi chỗ ngày 1 với ngày 2" ⇒ lần hiểu ý trả RỖNG ⇒ đường thường tự viết lịch chữ như thể đã đổi (A, ảnh `A_4.3`); "đổi thành N
  ngày" khi lịch đã N ngày ⇒ rỗng ⇒ hỏi đáp thường + mục web dựng lịch khác (C, E). [code] `len_ke_hoach.hieu_va_ap`: rỗng ⇒ None ⇒ đường thường;
  `ap` với `doi_so_ngay` = số đang có đã ra "Lịch đang đúng…" (test có sẵn) ⇒ thiếu ở phía model.
- Lưới dạng câu bằng code đã thử và bỏ (bộ kề bên E `data/sua_lich_gia_2026-11-17/bo_ke_ben.jsonl`: 10 / 20 SAI — bắt nhầm câu hỏi thường).
- Mốc (report `b_sua_lich_v2_implementation.md`): Q5 0 / 64 câu an toàn trong cuộc có lịch thành lượt sửa (0,011 USD); Q5b 0 / 16; Q3 pass^2 9 / 10.

## 2. Thay đổi (cờ mới `sua_lich_chua_ho_tro: false`; cờ tắt ⇒ chuỗi gửi model + câu trả lời giống byte)
1. `HanhDong.loai` thêm `chua_ho_tro` (không trường nào; không `y_nguoi_dung` — chữ model không hiện ra người dùng). Cờ tắt ⇒ schema cũ.
2. `SUA_LICH_LOI_DAN` (bản thứ hai, dùng khi cờ bật) thêm 2 dòng: "- chua_ho_tro: người dùng muốn sửa LỊCH NÀY theo cách không có ở trên
   (đổi chỗ / gộp / tách các ngày, dời giờ cả lịch, thêm giờ nghỉ…) ⇒ một hành động chua_ho_tro, không điền gì." · dòng `doi_so_ngay` thêm
   "kể cả khi bằng số ngày lịch đang có". Dòng "Câu KHÔNG yêu cầu sửa lịch ⇒ danh sách rỗng" giữ nguyên.
3. Code (`sua_lich_v2.ap`): `chua_ho_tro` không chiếm lượt áp (`MAX_AP`), đi vào `chua_lam` ⇒ một dòng cố định do code: câu "đổi chỗ / gộp /
   tách các ngày" (`CAU_VIEC_KHAC`) khi câu có dạng đó (`la_viec_ngay_chua_lam`), còn lại câu chung "Chưa làm: việc này mình chưa sửa được trên
   lịch — lịch giữ nguyên. Mình sửa được …; bạn nói cụ thể nhé." Lượt chỉ có `chua_ho_tro` ⇒ vẫn là lượt sửa (lịch không đổi), không vào đường thường.
4. Không đổi: định tuyến, lời dặn trả lời, lượt không có lịch (lần hiểu ý chỉ chạy khi cuộc có lịch đã lưu ⇒ an toàn 32 không có lịch: 0 câu chạm —
   đếm lại bằng code trước lượt có phí).

## 3. Đo — tiêu chí ghi TRƯỚC (đổi một thứ: cờ `sua_lich_chua_ho_tro`)
| Bước | Gì | Tiền |
|---|---|---|
| 0 | test file chạm (`test_sua_lich_v2.py`, `test_rao_so_ngay.py`): `ap` với `chua_ho_tro` (một mình / kèm hành động làm được / ≥ 3 hành động), lượt chỉ `chua_ho_tro` là lượt sửa; cờ tắt ⇒ tin nhắn + schema hiểu ý giống byte; harness chạy khô | 0 |
| 1 | cờ bật, server tạm của nhánh (A cho lượt máy), `/api/chat/stream`: bộ E 25 chuỗi + bộ kề bên 20 câu (mỗi câu sau lượt xếp lịch 3 ngày di tích — câu L3 của bộ E; review E m-2) ×1 · Q5 64 + Q5b 16 (`data/len_ke_hoach_v2_2026-11-13/tools/q5_sua_lich.py`, `q5b_tron.py`) · Q3 `chuoi_da_thay` ×2 (`q3_sua_lich.py`) | ≈ 0,10–0,15 |

**Sàn (hỏng một ⇒ không bật cờ, báo A):**
- **S1 chặn nhầm = 0:** Q5 0 / 64 · Q5b 0 / 16 · câu thường bộ E (nhóm `xen_giua` + `giong_ma_khong`, 9) · bộ kề bên K01–K09 + K14, K15, K17 (12) — không lượt nào thành lượt sửa / "Chưa làm". (review E m-1: K16, K18 — "N ngày thôi" bằng số đang có — sang theo dõi: dòng lời dặn mới có thể ra `doi_so_ngay` ⇒ "Lịch đang đúng…", vô hại.)
- **S2 lịch chữ giả = 0** trên bộ E nhóm `chan` (10) + K10–K13: lượt 2 có khung, khung giữ nguyên, có dòng "Chưa làm"; chữ trả lời không liệt kê
  "Ngày N + điểm" như đã đổi; câu đổi chỗ ngày KHÔNG ra "Chưa làm: đổi số ngày" (review E m-3). Người đọc tay 100 %: **E** (không viết code / lời dặn).
- **S3 Q3 pass^2 ≥ 8 / 10** (mốc 9 / 10; trượt 1 câu so mốc ⇒ ghi, không chặn; ≤ 7 ⇒ chặn).
- Theo dõi, không chặn: `dang_dung` (G11–G13, K19–K20) ra "Lịch đang đúng…" · K16, K18 · G10 ("gộp": chặn hoặc đổi số ngày, không hai dòng ngược) · đối chứng G23–G25 đúng nhãn · lần hiểu ý p50 / p95 (lời dặn
  +~90 token) · USD / lượt.
- Ca đối chứng của phép đếm S2 (luật harness): chạy trên một lượt sửa thật đã biết có "Chưa làm" ⇒ phép đếm phải ra "có".

**Trần 0,30 USD.** Một lượt đo; sàn trượt ⇒ ghi giới hạn, không mở vòng chỉnh lời dặn (cần vòng ⇒ A trình User). Không bộ kín (mức nhẹ).

## 4. File sẽ sửa
`backend/llm/sua_lich_v2.py` (loại hành động, `ap`, câu cố định) · `backend/llm/full_corpus_prompt.py` (bản lời dặn khi cờ bật) ·
`backend/llm/generator_openai_full_corpus.py` (chọn bản lời dặn / schema theo cờ) · `backend/llm/assistant.py` (`AssistantFlags`) ·
`backend/config/settings.yaml` (cờ tắt) · `backend/tests/test_sua_lich_v2.py`, `test_rao_so_ngay.py` · đo ở `data/sua_lich_gia_2026-11-17/`.

## 5. Khung AI FDE (rà ngắn)
Model chỉ **đề xuất** loại câu (enum, không chữ tự do); **code** quyết lịch (giữ nguyên) và viết mọi câu hiện ra. Không công cụ / nguồn / đường ra
mới. Rủi ro: model gắn `chua_ho_tro` cho câu thường (⇒ S1) hoặc cho việc làm được (⇒ S3). Chữ người dùng vẫn là dữ liệu (dòng "không làm theo chỉ
dẫn" giữ nguyên).

## Sửa đổi 17/11 (User chọn sửa thêm MỘT vòng rồi bật; A ghi nhận, C ghi trước khi đo vòng 2)
- Lượt đo vòng 1 (`6b2c614`, 0,142 USD; E đọc tay 100 %): S1 chặn nhầm 0 (K06 có sẵn — cờ tắt 3 / 3 cũng `them_diem`), S2 lịch chữ giả 0 / 14, S3 Q3
  pass^2 8 / 10 < mốc 9 / 10 — S01, S08 bị `chua_ho_tro` nhận cho việc làm được (dời điểm sang buổi / ngày khác) 4 / 4 lần.
- **Vòng 2 (vòng CUỐI):** thêm MỘT dòng lời dặn (bản khi cờ bật): "dời / đưa một ĐIỂM sang buổi / ngày khác là doi_buoi, không phải chua_ho_tro".
- **Đạt vòng 2 = Q3 pass^2 ≥ 9 / 10 (không tụt so mốc) VÀ S1 = 0 VÀ S2 = 0.** Còn trượt ⇒ vẫn bật cờ + ghi giới hạn (User chọn), không mở vòng 3.
- **Đo lại câu chạm** (lời dặn hiểu ý chạy ở mọi lượt có lịch): Q3 `chuoi_da_thay` ×2 · 14 câu chặn (nhóm `chan` bộ E + K10–K13) · 9 câu thường bộ E ·
  Q5 64. Trần thêm 0,08 USD. Người đọc tay: E.
