# Thẻ lịch đã sửa giữ câu bão / lũ + 112 ở mọi nơi — nhánh `p9-e-the-lich-giu-112-2011` (E, 11:35 20/11/2026, giờ `date`)

Trạng thái: **code + test + một lượt trình duyệt xong; CHỜ một phiên khác review.** Chưa gộp. Chủ dự án đã duyệt sửa điểm này (hai model khác hãng cùng nêu ở lượt soát đợt sửa).
**Sau bản sửa này KHÔNG có lượt soát khác hãng nào nữa** — chỉ có test, một lượt trình duyệt của người viết và review của một phiên cùng hãng.

## 1. Người dùng thấy gì khác
Hỏi về bão ⇒ lập lịch (thẻ lịch có câu "theo dõi bản tin chính thức… gọi 112") ⇒ sửa lịch bằng lời và sửa được (ví dụ bỏ một điểm), câu sửa không nhắc bão.
- Trước: chỉ file PowerPoint của lịch đã sửa còn câu đó; thẻ lịch trên màn hình, bản in, "Sao chép lịch" / "Tải về (.txt)" và tệp lịch `.ics` đều MẤT.
- Sau: cả năm nơi đều có. Lịch lập khi chưa nhắc bão thì sau khi sửa vẫn không có câu đó (không thêm bừa).

## 2. Sửa gì (chỉ phía máy chủ, `backend/api/routes/chat.py`; không đổi giao diện)
- `an_toan_cua_luot` — MỘT hàm trả "câu an toàn của lượt": câu lưới cuối bão đã đặt cho chính lượt đó, hoặc — lượt SỬA lịch LÀM ĐƯỢC không có câu riêng — câu của bản lưu trước. Lượt biểu mẫu (lập lịch mới) không thừa hưởng.
- `an_toan_vao_ghi_chu` (mới, 4 dòng) — gọi một chỗ, ngay sau lưới cuối và TRƯỚC khi phát sự kiện ghi chú: đưa câu thừa hưởng vào ghi chú của lượt. Thẻ lịch, bản in, .txt, .ics đều đọc ghi chú an toàn của lượt nên tự có.
- `luu_lich_cua_luot` — bỏ nhánh thừa hưởng riêng (nay nằm trong hàm chung) ⇒ thẻ và bản lưu (file PowerPoint) không thể lệch nhau vì cùng hỏi một hàm.
Cỡ (theo `git show --numstat`): `chat.py` +16 −6 (kể chú thích); file test +11 −2, trong test chuỗi đã có.

## 3. Bằng chứng
| Phép | Kết quả | Nhãn |
|---|---|---|
| Test chuỗi `test_edit_turn_that_changes_nothing_keeps_the_saved_plan_and_its_storm_sentence` (mở rộng: sự kiện ghi chú của lượt sửa làm được có câu an toàn; bản trước không có ⇒ không có; lượt biểu mẫu ⇒ không thừa hưởng; lượt sửa không đổi gì ⇒ như đã gộp) | xanh | [máy kiểm] |
| Phá 1: hàm đưa câu vào ghi chú không làm gì | 1 hỏng (lỗi kiểu ở chỗ dựng sự kiện — đỏ, nhưng không phải đỏ ở dòng so sánh) | [máy kiểm] |
| Phá 2: bỏ thừa hưởng trong hàm chung | 1 hỏng ở dòng kiểm bản lưu có câu an toàn | [máy kiểm] |
| Từng file, Python 3.13: `test_len_ke_hoach_v2` · `test_lich_pptx` · `test_chat_stream` · `test_api_chat` (có nạp khoá) | 93 · 15 · 25 · 15 đạt | [máy kiểm] |
| Trình duyệt thật, MỘT lượt mỗi ca (máy chủ chạy từ nhánh này): hỏi bão ⇒ lập lịch có ngày đi ⇒ bỏ một điểm | thẻ lịch · bản in (3 trang, câu in đậm ở đầu — người viết đã mở file nhìn) · .txt · .ics · PowerPoint: CẢ NĂM có câu 112; lịch là lịch mới | [máy kiểm + người viết nhìn bản in] |
| Đối chứng: không hỏi bão ⇒ lập lịch ⇒ bỏ một điểm | cả năm KHÔNG có câu đó | [máy kiểm] |
Tiền lượt trình duyệt: khoảng 0,004 USD (5 lượt có phí, cộng từ sổ vết). Hồ sơ riêng tư (ảnh, tệp tải về): `data/test_cuoi/chay_2026-11-20/` khoá `e1a`, `e1b`.

## 4. Giới hạn / chưa làm
- Khung trợ lý của CHÍNH lượt sửa nay cũng hiện câu an toàn (trước không có) — hệ quả của việc ghi chú của lượt mang câu đó; lệch về phía an toàn.
- Câu an toàn đi theo lịch qua mọi lượt sửa làm được về sau, tới khi lập lịch mới bằng biểu mẫu.
- Lượt sửa KHÔNG đổi được gì và không nhắc bão: ghi chú của lượt đó không thừa hưởng (thẻ cũ trên màn hình vẫn còn câu của nó) — giữ như đã gộp.
- Đường không hiện chữ dần (`POST /api/chat`) không lưu lịch từ trước — ngoài phạm vi.
- Chưa chạy: cả bộ test; lịch 3 ngày; trình duyệt có màn hình. Chưa có người thứ hai mở các tệp tải về.

| Đã làm | Chưa làm | Lệnh kiểm (từ `backend/`) | Đầu ra |
|---|---|---|---|
| Sửa + test + lượt trình duyệt | cả bộ test | `HF_HUB_OFFLINE=1 uv run pytest -q tests/test_len_ke_hoach_v2.py` | 93 passed |
| | | `uv run pytest -q tests/test_chat_stream.py` | 25 passed |
