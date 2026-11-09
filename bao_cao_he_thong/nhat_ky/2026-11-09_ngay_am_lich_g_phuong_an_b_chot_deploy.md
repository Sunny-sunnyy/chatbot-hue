# Nhật ký 09/11/2026 — ngày + âm lịch đo xác nhận, bảng vé đóng hồ sơ, định tuyến về phương án B, 4 chốt trước deploy

**Cập nhật lần cuối: 21:10 09/11/2026 (E viết, A đọc + cộng tiền).** Tiền paid trong ngày: **≈ 0,27 USD** (định tuyến G ≈ 0,18 + phương án B 0,036 · ngày + âm lịch 0,026 · bảng vé 0,028 · chốt deploy ≈ 0,0004 · A 0 — số từ report / log từng việc, chưa đối chiếu log tổng) (~6.800 đồng). Trần Phase 9: **4,0 USD** (bạn nâng 09/11).

## Tóm tắt
- Người dùng thấy đổi **một chỗ**: câu khẩn cấp không còn câu soạn sẵn (định tuyến phương án B vào `main`). Mọi thứ mới khác đều tắt hoặc chưa vào chatbot.
- **Ngày + âm lịch:** đo trên 14 câu mới. Bản có công cụ trả lời được 9 câu mà bản đang chạy từ chối, **không câu nào sai ngày**. Có 1 câu trượt: hỏi "Tết năm nay" vào tháng 11 thì trợ lý gọi Tết sắp tới là "năm nay". Đã sửa bằng code, đo lại sau.
- **Bảng vé + giờ có cấu trúc:** đóng hồ sơ, vì đo không thấy lợi.
- **Định tuyến "2 nhóm":** dừng sau hơn 3 vòng chỉnh, chuyển phương án B: giữ định tuyến 4 nhóm như cũ, chỉ bỏ câu khẩn cấp soạn sẵn.
- **4 chốt trước khi đưa link công khai** đã vào code. Chúng chỉ bật khi đặt biến môi trường; trên máy bạn mọi thứ chạy y như trước.
- **Cách làm:** từ hôm nay mỗi phiên có vòng tự soi bắt buộc. Lượt đo nào không chỉ ra được nó giữ sàn chất lượng nào thì không chạy.

## Bạn cần làm gì
- **Không có quyết định mới bắt buộc hôm nay.** Đã quyết trong ngày:
  - nhận câu ngoài phạm vi thỉnh thoảng có mục web là giới hạn đã biết;
  - nhận lỗi bỏ điều kiện mùa mưa lũ ở một câu an toàn là giới hạn (lỗi có cả ở bản đang chạy);
  - chọn phương án B cho bảng vé, rồi đóng hồ sơ.
- **Khi rảnh:** tick phiếu toạ độ bản đồ; thu 40 câu giọng nói.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Ngày + âm lịch (T1) — đo xác nhận 14 câu mới | từ chối nhầm −9 · sai ngày 0 · trượt 1 câu "Tết năm nay" | công cụ giúp thật, chưa bật; sửa câu "năm nay" bằng code (nhánh `p9-t1-sang-nam`), đo lại sau định tuyến mới |
| **Ngày + âm lịch — BẬT** (merge `99ea59a`, cờ `ngay_lich: true`, bạn duyệt 09/11) | lượt sau định tuyến mới: sai ngày 0 · câu ngày có nhắc Huế 3 / 3 (bản cũ 1 / 3) · an toàn 4 / 4; thử server thật: "rằm tháng Giêng tới" ⇒ đúng thứ Bảy 20/2/2027, câu ngoài phạm vi vẫn từ chối | khách hỏi lễ theo ngày nay được trả lời; giới hạn: câu lịch thuần không nhắc Huế vẫn ra ngoài phạm vi, "tháng tới / cuối tuần" model tự cộng |
| Tốc độ T1 (cùng lượt đo) | chữ đầu trung vị 3,35 s ↔ bản đang chạy 4,90 s | không chậm hơn; p95 vượt 5 s ở cả hai do câu đi qua tra web |
| Bảng vé + giờ (T3) | đúng 19 / 20, nhưng sàn điều kiện trượt 6 / 10; phương án B lợi ≈ 0 | **đóng hồ sơ** (tag `hoso/p9-t3-bang`), câu giá / giờ trả lời như cũ |
| Định tuyến 2 nhóm (G) | 2 / 44 câu ngoài phạm vi đã thấy bị gắn mục web (bản cũ 0 / 44) | **dừng** ⇒ phương án B: giữ 4 nhóm, bỏ câu khẩn cấp soạn sẵn — **đã vào `main`** (merge `3b52017`; đo 92 câu: 0 câu ngoài phạm vi / ngoài kho bị trả lời; test 842 đạt; thử trên server thật đạt). Người dùng thấy đổi một chỗ: câu khẩn cấp (vd vừa bị cướp) giờ được trợ lý trả lời như câu thường, không còn câu soạn sẵn có số 113 / 114 / 115 — đúng như bạn quyết 08/11 |
| 4 chốt trước deploy | merge `ccc9f4f` | giới hạn lượt / IP / ngày, cookie chỉ qua https, tắt `/docs`, log xoay vòng — bật bằng biến môi trường |
| Tra web thành công cụ (T2) | đo: câu hỏi kèm có mục web 4 / 10 = bản đang chạy 4 / 10 (cần hơn 2); 26 / 29 lần trợ lý xin tra web lại chính là câu nó từ chối cả câu — cổng cũ đã xử lý | **đóng hồ sơ** (tag `hoso/p9-t2-web`), tra web giữ như cũ (chỉ sau câu từ chối); 0,171 USD |
| Lịch trình từ câu gõ (T4) | 27 / 27 câu có lịch, hỏi lại thừa 0, từ chối thay lịch 0; nhưng "hợp người đi cùng" chỉ 21 / 27 và 15 / 27 (2 người chấm; cần ≥ 26) — gốc ở luật xếp / bảng điểm (đi dày vẫn 2 điểm / ngày, sở thích nói bằng lời chưa dùng, buổi tối cho người lớn tuổi, lo mưa vẫn xếp ven nước) | **đóng hồ sơ** (tag `hoso/p9-t4-lich`); lịch trình chỉ qua biểu mẫu "Lên kế hoạch" như hiện nay; 0,136 USD |

## Giải thích ngắn (để bạn tự nói lại được)
1. **Vấn đề:** chatbot không biết hôm nay là ngày nào, nên từ chối những câu như "tối nay", "rằm tháng Giêng tới".
2. **Cách làm:** cho trợ lý một công cụ để **code** tính ngày và đổi âm ↔ dương theo lịch Việt Nam. Model chỉ gửi số, không tự tính.
3. **Kết quả:** trên 14 câu mới, bản có công cụ trả lời thêm 9 câu và không câu nào sai ngày.
4. **Giới hạn:** câu mơ hồ kiểu "Tết năm nay" hỏi vào cuối năm. Sửa bằng cách bắt code đưa cả Tết đã qua lẫn Tết sắp tới. Cờ vẫn tắt tới khi đo lại đạt.

## Đọc thêm
- `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md` (bản 45 — mục 1, checklist, mục 4 "09/11")
- `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md` §4e (ngày + âm lịch)
- `report_agent/2026-11-08_phase_9_ban_13/` (định tuyến G, T2)
- `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` (bảng vé)
