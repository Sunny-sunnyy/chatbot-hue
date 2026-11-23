# Bản sửa số 2 — hết vòng công cụ ⇒ câu từ chối trống (nhánh `p9-c-sua-2-het-vong`)

Phiên C ghi 18:47 21/11/2026 (giờ `date`). Nhánh rẽ từ `cf1a70c3`. Hai cờ ĐỘC LẬP, đều TẮT — chưa đo lượt thật nào, chưa bật, chưa gộp.

**Quyết định chờ:** giữ hay gỡ từng cờ sau khi phiên đo đo (tiêu chí ghi trước: `data/thu_bedrock_2026-11-21/c_sua_2/TIEU_CHI_GHI_TRUOC.md`, riêng tư).

## Vì sao
Ở đường model cũ, câu nhiều ý có "bao xa" / một ngày cụ thể hay kết thúc bằng câu từ chối trống dù đã tìm được bằng chứng: model gọi công cụ hết số vòng cho phép (6 / 48 lượt trong 24 phiên người dùng mô phỏng ngày 21/11; model đang chạy 0 / 53). Hai cơ chế đếm được trên 6 lượt đó: gọi công cụ khoảng cách cho nơi không có trong bảng (4 / 6), gọi lại y nguyên một lời gọi (4 / 6); một lượt là câu thật sự nhiều ý.

## Đã làm
Chép hai cờ có sẵn từ nhánh `p9-b-vong-cuoi-chi-viet` (`e9a14c12`, phiên B viết) lên `cf1a70c3`:
- `vong_cuoi_chi_viet` — vòng gọi model cuối cùng của lượt không kèm công cụ ⇒ model viết từ bằng chứng đã có; kết quả công cụ của vòng sát cuối được nối một dòng báo.
- `khoang_cach_trang_thai` — công cụ khoảng cách không có số ⇒ kết quả mở đầu bằng dòng "đừng gọi lại cho cặp này; vẫn trả lời các ý khác".

Khác nhánh gốc ở BA chỗ (người đọc soi đúng ba chỗ này; phần còn lại là diff của nhánh gốc):
1. BỎ cờ thứ ba `bao_het_luot_tim` (dòng báo "hết lượt tìm kho") cùng hằng chữ, tham số và test của nó — phiên đo đã thấy cờ đó làm model đang chạy trả lời câu đối chứng ngoài tỉnh bằng kho (bản chữ 1: 4 / 5 lần; bản chữ 2: 2 / 5; cờ tắt 0 / 5).
2. Chữ của dòng báo vòng cuối lấy BẢN CHỮ 2 của nhánh gốc (`13efd6f3`: thêm vế "không nói về điều được hỏi ở ý nào cả thì trả câu không đủ thông tin") — bản duy nhất có số cho thấy đỡ phạm sàn hơn, dù số đó đo ở dòng báo kia.
3. THÊM một test cho đường stream (đường giao diện dùng): hai đường dựng công cụ ở hai chỗ, test của nhánh gốc chỉ chạy đường không stream.

Chưa viết: phần chặn lời gọi công cụ trùng — chỉ viết nếu số đo cho thấy hai cờ trên chưa đủ (ngưỡng ở trang tiêu chí).

## Lệnh kiểm + đầu ra (từ `backend/` của cây nhánh; 0 đồng, model là phản hồi dựng sẵn, tìm kho là Qdrant thật)
| Lệnh | Đầu ra |
|---|---|
| `pytest tests/test_vong_cuoi_chi_viet.py -q` | `7 passed` |
| cùng lệnh sau khi CỐ Ý gỡ dòng truyền cờ ở đường stream | `1 failed, 6 passed` (đúng test đường stream) ⇒ đã trả lại, `7 passed` |
| từng file: `test_het_luot_tim` · `test_b2_tool_loop` · `test_khoang_cach` · `test_liet_ke_bai` · `test_bedrock_model` · `test_phase6_settings` · `test_settings_env` | 7 · 12 · 101 · 17 · 21 · 5 · 6 passed |
| Cờ tắt giống từng byte: 180 loại lượt dựng sẵn (3 bộ cờ × 5 kịch bản gọi công cụ × 3 câu × có / không lịch sử × stream / không stream), so mã băm thân yêu cầu gửi model giữa cây `cf1a70c3` và cây nhánh | khác 0 / 180; đối chứng cây gốc chạy hai lần: khác 0 / 180 |

## Chưa làm · giới hạn
- Chưa có lượt model thật nào ⇒ chưa biết model viết gì ở vòng cuối, chưa biết sàn "câu ngoài kho phải bị từ chối" có giữ khi dòng báo hiện ra — là ô bắt buộc của phiên đo, trên cả hai model.
- Chưa chạy `test_chat_stream.py` và các file dựng cả app (gọi model thật theo cấu hình đang chạy).
- Test dùng phản hồi dựng sẵn ⇒ không phải bằng chứng cho hệ thống thật.
- Phép này KHÔNG cho biết: tần suất chạm trần ở người thật · hướng rộng hơn: nếu sàn không giữ ở model đang chạy thì cần chọn cờ theo nhà cung cấp (vài dòng, việc riêng) · đếm rẻ nhất: ô "chỉ `vong_cuoi_chi_viet`" trên 41 câu khó đường model cũ.

## Thêm 19:00 21/11/2026 — dấu đếm cho bộ đo + một điểm của người đọc
- **Dấu đếm `bao_vong_cuoi`** (phiên đo đề nghị: không có dấu thì không đếm chính xác được lượt nào dòng báo vòng cuối đã thật sự tới model): khi dòng báo được nối vào kết quả công cụ, mục công cụ chạy sau cùng của lượt trong sổ lượt (`tools`, có trong dòng số đo) mang `bao_vong_cuoi: true` — cả đường stream lẫn không stream; lượt model lờ dòng báo rồi xin tiếp công cụ cũng mang dấu (model ĐÃ được báo). Cờ tắt, hoặc lượt kết thúc trước vòng sát cuối ⇒ không mục nào có trường này.
  Kiểm: `pytest tests/test_vong_cuoi_chi_viet.py -q` ⇒ `7 passed`; cố ý gỡ dòng ghi dấu ⇒ `3 failed, 4 passed` ⇒ trả lại ⇒ `7 passed`; so lại cờ tắt giống byte: khác 0 / 180; `test_het_luot_tim` 7 · `test_b2_tool_loop` 12 · `test_khoang_cach` 101 · `test_liet_ke_bai` 17 · `test_bedrock_model` 21 passed.
- **Công cụ trả kết quả KHÔNG phải chuỗi ở vòng sát cuối** (điểm nhỏ của người đọc): chỉ có thẻ hỏi lại của công cụ lịch (một dict) — thẻ đó DỪNG lượt ngay, không còn lần gọi model nào ⇒ không có model nào cần được báo; năm công cụ còn lại (tìm kho, thời tiết, ngày, khoảng cách, liệt kê) luôn trả chuỗi [đọc code từng hàm `*_for_turn`]. Ca đó không ghi dấu.
