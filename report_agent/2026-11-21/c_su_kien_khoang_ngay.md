# Bộ đọc khoảng ngày của tính năng "sự kiện theo ngày" — sửa ba lỗi đã tái hiện (nhánh `p9-c-su-kien-khoang-ngay`)

Phiên C ghi 20:10 21/11/2026 (giờ `date`). Từ main `7d2581dd`. Cờ `su_kien_theo_ngay` vẫn TẮT; chỉ đổi một hàm thuần (`llm/su_kien.py`, `khoang_hoi`) + test. Người đọc: phiên B.
**Quyết định chờ:** lượt đo 10 câu trên hai model của cờ này chạy trên bản đã sửa (phiên đo).

## Vì sao
Lượt mốc 12 vai tối 21/11: tin "ok thứ 2 23/11 nhé. Thế tuần này với tháng này ở Huế có lễ hội hay sự kiện gì không?" — bộ đọc ra "ngày 23/11" (phiên B dò ra). Tái hiện bằng hàm thuần, ba nguyên nhân: (i) đọc cả tin, con số ngày ở câu đệm thắng khoảng ngày ở câu hỏi; (ii) câu nêu hai khoảng chỉ lấy khoảng đứng trước trong danh sách luật (hẹp hơn); (iii) "từ 23/11 đến 25/11" chỉ lấy ngày đầu.

## Đã làm
- Đọc khoảng ngày trong CÂU có từ hỏi sự kiện trước; câu đó không nêu khoảng nào thì đọc cả tin Y NHƯ CŨ (cùng thứ tự ưu tiên).
- Trong câu hỏi nêu nhiều khoảng: mọi khoảng đều là một ngày ("từ 23/11 đến 25/11", "hôm nay với ngày mai") ⇒ từ ngày sớm nhất tới ngày muộn nhất; còn lại ("tuần này với tháng này") ⇒ khoảng rộng nhất. Thứ tự ưu tiên trong một cụm giữ nguyên ("cuối tuần này" không bị nới thành "tuần này").
- Đã thử rồi THU HẸP: bản đầu áp luật "khoảng rộng nhất" cho cả tin; chạy trên câu thật thấy một tin có "rằm tháng 10" ở câu khác bị kéo sang cả tháng 10 năm sau ⇒ luật mới chỉ áp trong câu hỏi (đã có test giữ ca này).

## Lệnh kiểm + đầu ra (hàm thuần, 0 đồng; "hôm nay" = thứ Bảy 21/11/2026)
| Phép | Đầu ra |
|---|---|
| `pytest tests/test_su_kien_theo_ngay.py -q` | `37 passed`; sáu ca mới ĐỎ trên hàm của main, 26 test cũ không đổi |
| Bộ dò MÙ 25 câu của phiên điều phối (mở sau commit đóng code đầu tiên `f33ec74`), số câu ra sai trước ⇒ sau | câu đệm có ngày 4 ⇒ 0 / 4 · hai khoảng 2 ⇒ 0 / 2 · từ–đến 3 ⇒ 0 / 3 · đối chứng đang đúng 0 ⇒ 0 / 7 · không được qua cổng 0 ⇒ 0 / 6 · ca khó 2 ⇒ 1 / 3 · TỔNG 11 ⇒ 1 / 25. Hai câu ra đáp án thứ hai được chấp nhận (khoảng rộng hơn 23–29/11; 23–24/11). Câu còn sai: "tháng Chạp âm lịch … có lễ gì?" — bộ đọc khoảng ngày ra đúng tháng Chạp âm, nhưng chữ "lễ gì" không qua cổng từ hỏi sự kiện (có từ trước, ngoài phạm vi bản sửa) |
| Bộ dò cũ của phiên đo (35 câu, 20/11) | 0 câu đổi kết quả; cổng mở 15 ⇒ 15 |
| Mọi câu người dùng đã gõ + ba lượt mốc (578 câu khác nhau) | cổng mở 30 ⇒ 30; 10 câu đổi kết quả, đọc tay cả 10: đều từ "ngày 23/11" / "cuối tuần" sang đúng khoảng được hỏi ("tuần này với tháng này" ⇒ 21–30/11; "tháng 11 này" ⇒ cả tháng; "cuối tuần này 21-22/11" ⇒ 21–22/11) |

Ghi rõ về bộ mù: bản thu hẹp được viết SAU khi đã mở bộ mù, nhưng lý do là ca tụt thấy trên câu thật, không phải một câu của bộ mù; số của bộ mù trước và sau khi thu hẹp giống nhau (11 ⇒ 1).

## Chưa làm · giới hạn
- Chưa có lượt model thật nào (đổi hàm thuần; lượt 10 câu trên hai model do phiên đo chạy).
- Còn giới hạn: "rằm tháng 10" (tháng âm không ghi chữ "âm") bị đọc là tháng 10 dương khi không có mốc nào khác; "23-25/11" (một tháng cho hai ngày) chỉ đọc được ngày sau; "lễ gì" không qua cổng từ hỏi.
- Phép này KHÔNG cho biết bảng sự kiện có đủ hay không, và model viết gì từ nguồn đó · hướng rộng hơn: không · đếm rẻ nhất: khi cờ bật, đếm trên log số lượt nhãn khoảng ("Khoảng được hỏi (…)") khác với chữ người dùng gõ.
