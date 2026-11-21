# Mục "Từ web" chỉ mở khi CẢ câu bị từ chối (nhánh `p9-b-web-chi-khi-tu-choi`, từ main `c1253a66`)

Phiên B ghi 22:16 21/11/2026 (giờ `date`). Người đọc: phiên C (đọc nhánh), phiên điều phối (quyết mở). B là người viết ⇒ không tự duyệt.
Quyết định đang chờ: có mở thay đổi này cho người dùng không. Chỉ đo trên model đang chạy (Claude Sonnet 5.5, mức suy luận high); model cũ CHƯA ĐO (chủ dự án tạm gác).

Từ dùng: *tin nhiều ý* = tin mà bộ đếm ý hỏi của code ra từ 2 vế trở lên ⇒ trợ lý trả lời theo từng ý, ý nào kho không có thì ghi dòng "Tư liệu chưa có thông tin về: …" ·
*mục "Từ web"* = phần chữ nằm dưới câu trả lời, viết từ kết quả tìm web, có nhãn chưa kiểm · *lượt* = một tin người dùng gửi + thứ họ thấy.

## Bốn thứ cho chủ dự án
1. **Người dùng thấy gì khác:** với tin nhiều ý mà trợ lý đã trả lời được một phần, câu trả lời về NHANH hơn khoảng 6 giây và không còn kèm mục "Từ web" bên dưới. Dòng "Tư liệu chưa có thông tin về: …" vẫn còn nguyên. Khi trợ lý từ chối CẢ câu thì mục "Từ web" vẫn mở như trước.
2. **Số đo** (một lượt thật, 17 tin mỗi bên, qua đúng đường chat): 11 tin nhiều ý — bên cũ 11 / 11 lượt đi tra web; bên mới 0 / 11. Thời gian trung vị 19,8 ⇒ 15,6 giây; so từng cặp cùng tin: trung vị bớt 5,8 giây, 11 / 11 tin nhanh hơn (bớt từ 2,0 tới 11,8 giây). Mỗi lượt bớt đúng một lần gọi model và một lần gọi dịch vụ tìm web; tiền bớt khoảng 15 %.
   Vì sao bỏ được: trên ba lượt mốc 12 vai, mục web mở theo dòng "chưa có" đáp đúng điều thiếu ở 1 / 66 dòng mẫu; ở 5 cặp B đọc tay lần này, 0 / 5 mục web đáp được điều thiếu (3 mục chỉ ghi "chưa tra được / chưa xác minh được").
   Sàn: 4 / 4 câu ngoài phạm vi vẫn bị từ chối ở cả hai bên; 2 / 2 câu bão lũ vẫn có câu bản tin chính thức + số 112, không lặp; 0 lượt lỗi ở cả hai bên.
3. **Giới hạn:** mới MỘT lượt, 11 tin, một model. Hai nửa không chạy xen kẽ (cách nhau khoảng 12 phút, lý do ở mục "Sự cố") nên con số giây có thể lẫn dao động theo giờ; phần "bớt một lần gọi" thì thấy ở cả 11 cặp. Ở bên mới, 2 / 11 lượt không có dòng "chưa có" theo đúng khuôn (một lượt viết thiếu dấu hai chấm, một lượt nói điều thiếu ngay trong câu) — thay đổi này không đổi thứ gửi model nên B cho là dao động của model (số nền: 86 % lượt nhiều ý có dòng), nhưng một lượt không đủ để chắc. Chưa có lượt thật nào bị từ chối cả câu ở bên mới (mới có test). Chưa nhìn trên trình duyệt. Không biết người dùng thật có tiếc mục "Từ web" không.
4. **Cách lùi:** một dòng cấu hình — `web_chi_khi_tu_choi: false` trong `backend/config/settings.yaml` rồi khởi động lại server. Nhánh này để dòng đó là `false` (chưa mở); phiên điều phối mở bằng cách đổi thành `true`.

## Đổi gì trong code
- `backend/llm/assistant.py`: thêm công tắc `web_chi_khi_tu_choi`; luật mở mục web (`web_gate_open`, một chỗ cho mọi đường) bỏ nhánh "tin nhiều ý có dòng chưa có" khi công tắc bật; hàm `so_y_thieu` đếm dòng "chưa có".
- `backend/api/routes/chat.py`: lượt nhiều ý còn dòng "chưa có" không được lưu vào bộ nhớ đệm câu trả lời khi công tắc bật (trước đây lượt đó có mục web nên vốn không lưu — giữ nguyên hành vi); dòng số đo của lượt nhiều ý thêm `n_y_thieu` (một con số, không chữ).
- `backend/config/settings.yaml`: một dòng, đang `false`.
- `backend/tests/test_web_chi_khi_tu_choi.py`: 13 test (tìm kho thật, model giả).

## Sự cố trong lượt đo — và thứ đã sửa
Lượt đo đầu (bản `cc06e8a`): bật công tắc ⇒ 23 / 23 lượt báo "Đã xảy ra lỗi trong hệ thống" sau 0,9 mili giây, chưa gọi model. Nguyên nhân: đường trả lời chạy song song với bước định tuyến (đang bật ở cấu hình thật) tự tạo một bản cấu hình tắt "tra web";
phép kiểm B thêm ("công tắc mới cần tra web bật") ném lỗi ở bản đó. 11 test ban đầu đi đường không song song nên không thấy. Sửa ở `a04e3a3`: bỏ phép kiểm chéo (không có "tra web" thì mục web vốn không mở, công tắc không có gì để đổi), thêm test đi đúng đường stream song song.
Sau sửa mới chạy 17 tin bên bật. Bài học B ghi: test của một thay đổi phải đi đúng đường người dùng đi; "một lượt thật trước khi mở" là mức không bỏ được.

## Lệnh kiểm + đầu ra
| Lệnh (0 đồng trừ dòng cuối) | Đầu ra |
|---|---|
| `pytest tests/test_web_chi_khi_tu_choi.py tests/test_cau_nhieu_y.py -q` | `57 passed` |
| test mới `test_live_stream_path_runs_with_the_flag_on` trên code TRƯỚC khi sửa | `1 failed, 1 passed` — đúng lỗi "needs assistant.tra_web" ở đường song song |
| `pytest tests/test_b6_tra_web.py tests/test_cache_tra_loi.py tests/test_chat_stream.py tests/test_noi_that_lam_thay.py -q` | `283 passed` |
| Gỡ điều kiện công tắc khỏi luật mở mục web (thử phá, trên `cc06e8a`) | 3 test đỏ; gỡ rào bộ nhớ đệm ⇒ 1 test đỏ |
| Công tắc tắt: thứ gửi model so với cây chính (228 lần gửi, trên `cc06e8a`) | giống từng byte |
| Lượt thật, 17 tin × 2 bên, model đang chạy (1,60 USD Bedrock, gồm cả lượt bị dừng) | bảng ở mục "Bốn thứ" |

| Người dùng làm được | Chưa làm được |
|---|---|
| (khi mở) hỏi tin nhiều ý, nhận câu trả lời nhanh hơn khoảng 6 giây, vẫn thấy rõ ý nào tư liệu chưa có | ý tư liệu chưa có vẫn chưa được trả lời — và một phần các dòng "chưa có" là SAI vì đoạn kho đúng không vào ngữ cảnh (khoảng 1 / 4 dòng mẫu); thay đổi này không chữa chuyện đó |

- **Chưa làm:** lượt lặp 2, 3 (chủ dự án bảo đo ít lại); model cũ; lượt có lịch sử thật; nhìn trình duyệt.
- **Tự hoãn + lý do:** không.
- **Phép này KHÔNG cho biết** người dùng thật có tiếc mục "Từ web" không · **hướng rộng hơn:** chữa gốc — cho lần tìm kho đầu tìm theo từng vế hỏi của tin nhiều ý; phép đếm 0 đồng tối 21/11: đoạn kho đúng vào ngữ cảnh ở 5 / 8 dòng sai thay vì 1 / 8, với ngữ cảnh không lớn hơn hiện nay (trần 12 đoạn) · **đếm rẻ nhất:** sau khi mở, đếm `n_y_thieu` trên dòng số đo của log thật.
