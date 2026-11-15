# Đếm trước — sửa lịch bằng lời đổi ngày đi / hạng sao (C, 12:51 15/11/2026)

A nhận làm ứng viên 15/11. Đếm 10 câu **tự đặt** (không đo nhu cầu thật: log không lưu chữ — B nói đúng) trên một lịch thật 3 ngày có ngày đi + hạng sao "vừa". Gọi đúng lần "hiểu ý sửa" của hệ thống đang chạy + `sl.ap` (`data/sua_lich_truong_2026-11-15/tools/dem.py`, `dem_2012.py`). Tiền **0,0012 USD**.

| Loại câu | Lượt | Lần hiểu ý trả | Người dùng thấy |
|---|---|---|---|
| Đổi hạng sao (4 câu + 1 câu kèm ngày) | 5 | rỗng 5 / 5 | đi đường hỏi đáp thường; lịch không đổi, không có dòng "Chưa làm" |
| Đổi ngày đi (5 câu khác nhau) | 5 | rỗng 4 · **sai 1** | câu "đi từ ngày 20/12" ⇒ hành động **đổi số ngày 3 ⇒ 1**, code áp, báo "Đã đổi số ngày: 3 ngày → 1 ngày" |
| Lặp lại câu "đi từ (ngày) 20/12" | 8 | rỗng 6 · "đổi số ngày" không kèm số 2 | lịch không đổi; lượt sửa không có dòng nào |

**Đọc:**
- **Lỗi thật:** câu đổi ngày đi có thể bị hiểu thành đổi **số ngày** (1 / 1 lượt đầu, 0 / 8 lần lặp sau làm sai số ngày nhưng 2 / 8 ra hành động rỗng). Model đọc "20/12" thành số ⇒ lịch đổi sai mà vẫn báo "Đã đổi". Hiếm, nhưng là kiểu lỗi tệ: làm sai mà nói đã làm.
- Hai trường còn lại không sửa được, và hệ thống không nói "chưa làm được", mà lặng lẽ trả lời như một câu hỏi thường.
- **Không có số nhu cầu thật.** Việc này xây theo khoảng trống (3 / 8 trường biểu mẫu) + 1 lỗi làm sai, không theo lỗi người dùng đã gặp.

**Đề xuất (theo phản biện B):**
1. Bậc 1 — **hạng sao**: `doi_tham_so` thêm `ngan_sach`. Code chỉ ghi vào `tham_so`; đường giữ mức qua `sl.ap` đã có. "Rẻ hơn / sang hơn" mơ hồ ⇒ "Chưa làm", không đoán mức.
2. Bậc 2 — **ngày đi**:
   - code tính ngày từ chữ bằng công cụ ngày sẵn có (model chỉ trích cụm ngày);
   - lấy lại dự báo mưa; kiểm giới hạn ngày;
   - **chặn lỗi trên**: câu có cụm ngày ⇒ không nhận hành động "đổi số ngày" thiếu số.
3. Đo mỗi bậc (đổi schema đầu ra hiểu ý, chạy ở mọi câu trong cuộc có lịch): Q3 đã thấy + kín, **Q5 an toàn 0 / 64**, bộ trộn sửa + khẩn cấp 0 / 16. Ước ≈ 0,1–0,25 USD mỗi bậc.

## Sửa ngay lỗi "ngày tháng ⇒ đổi số ngày" (A giao, 12:58 15/11/2026) — nhánh `p9-rao-so-ngay` @ `62afeb7`
- **Rào bằng code sau lần hiểu ý** (`sua_lich_v2.so_ngay_co_trong_cau` / `loc_hanh_dong`, gọi ở `len_ke_hoach.py` ngay sau `hieu_sua`). Hành động đổi số ngày chỉ được nhận khi số mới có căn cứ trong chữ người dùng gõ:
  - tuyệt đối: số đứng TRƯỚC "ngày" hoặc dạng "4N3Đ";
  - tương đối: "thêm / bớt k ngày" ⇒ số hiện tại ± k.
  - Số trong ngày tháng ("ngày 20/12", "ngày 2") không tính. Thiếu số ⇒ bỏ.
  - Bỏ hết hành động ⇒ đi đường trả lời thường (như khi hiểu ý trả rỗng). Không đổi lời dặn ⇒ chuỗi gửi model giống byte ⇒ không lượt có phí.
- **Kiểm [đã chạy], 0 USD:**
  - `test_rao_so_ngay.py` 13 passed — các câu 20/12, 1/1, không kèm số ⇒ chặn; câu S03 của Q3, "hai ngày", "4N3Đ", "thêm một ngày", "bớt 1 ngày" ⇒ nhận; "chiều ngày 2" ⇒ chặn; hành động khác giữ nguyên.
  - Chạy rào trên hành động đã lưu: Q3 đã thấy (2 lượt chạy 14/11) có **16 lần đổi số ngày đã áp, rào chặn 0**; 18 lượt đếm của C có **3 hành động đổi số ngày sai, rào chặn 3**.
  - Cả `backend/tests`: **1078 passed, 253 s**.
- Lưu ý của E: `POST /api/chat` không stream không đi vào luồng sửa lịch. Lượt đếm của C gọi thẳng `generator.hieu_sua` + `sl.tin_nhan_hieu`, đúng hàm đường stream dùng (`len_ke_hoach.py:248`) ⇒ số đếm đúng đường.
- **Sau review E vòng 1** (`e_review_rao_so_ngay.md`, changes_requested 1 / 0 / 2):
  - **M-1:** rào bỏ ≥ 1 hành động đổi số ngày ⇒ lượt vẫn là **lượt sửa**: lịch không đổi + dòng code viết "Chưa làm: đổi số ngày — bạn nhắn tiếp nhé." Không còn rơi về đường trả lời thường (đường đó từng viết "đã rút" mà lịch không đổi). Test đi qua `hieu_va_ap` thật; phần "hiểu ý" thay bằng một lớp giả trả đúng hành động sai đã thấy — đây là test logic code, không phải bằng chứng về model.
  - **m-2:** "thứ hai / thứ ba ngày …" không đọc thành "hai / ba ngày".
  - **m-3:** nhận "hôm"; "bỏ ngày cuối", "bỏ ngày N" với N = ngày cuối ⇒ bớt 1 ("bỏ ngày giữa" không tính).
  - `test_rao_so_ngay.py` 20 passed; trên hành động đã lưu: Q3 16 đúng ⇒ chặn 0, 3 sai ⇒ chặn 3; suite **1085 passed**.
  - Luật nhận dạng: 29 dòng gồm chú thích, ~20 dòng code (ngưỡng A nêu).
