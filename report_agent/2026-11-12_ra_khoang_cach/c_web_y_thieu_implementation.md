# Mục web của câu nhiều ý chỉ viết cho ý thiếu (C, nhánh `p9-web-y-thieu` `c15517a`)

Cập nhật: 15:42 14/11/2026 (C). Plan `docs/superpowers/plans/2026-11-14-web-y-thieu-plan.md` (A duyệt sha `0be17d74b676`, mức nhẹ).

## Lỗi
Câu "ý kho có + ý ngoài kho" ⇒ mục "Từ web (chưa kiểm)" viết lại cả ý kho đã trả lời, với số khác kho.
- Thấy ở 4 / 4 lượt có mục web trong lượt đo trước (`data/so_y_va_2026-11-14/do_r.jsonl`).
- Ví dụ: kho ghi giờ mở cửa 7:00, mục web ghi 6:30 ngay bên dưới.

## Đổi gì
- `llm/assistant.py`: hàm mới `ve_y_thieu(query, answer)`.
  - Lấy các dòng "Tư liệu chưa có thông tin về: …", rồi chọn vế của câu người dùng có nhiều từ chung nhất với các dòng đó.
  - Tách vế cùng cách với `so_y`. Gặp hoà hoặc 0 từ chung ⇒ bỏ dòng đó.
  - Chọn hết các vế, hoặc không chọn được vế nào ⇒ trả "".
- `cong_web`: khi luật theo ý chạy và chọn được vế, câu hỏi đưa model viết mục web thành "<cả câu> (chỉ viết cho phần: <vế> — phần còn lại đã có câu trả lời từ kho)".
- **Lệch nhỏ so với plan (C tự quyết trong phạm vi):** Serper vẫn nhận **cả câu** như cũ, plan ghi là chỉ gửi vế. Lý do: vế như "gần đó có quán karaoke nào giá rẻ không" mất tên nơi, kết quả tìm sẽ kém. Lỗi nằm ở phần model viết, không ở phần tìm.
  - Đường ra ngoài không đổi gì: vẫn là câu người dùng.
  - Dòng ý thiếu do model viết chỉ dùng để chọn vế.
- Câu một ý, hoặc cờ tắt ⇒ `hoi_web = query`, giống hôm nay.
- Test `test_cau_nhieu_y.py`: thêm 5 ca `ve_y_thieu`; 34 đạt.

## Đo (theo luật "đo phần đổi")
Server thật của nhánh, `/api/chat`, 24 lượt, **0,0349 USD**. Dữ liệu: `data/web_y_thieu_2026-11-14/do_r.jsonl`.

| Bộ | Kết quả |
|---|---|
| An toàn 4 câu có `so_y ≥ 2` (S02, S05, S19, S27) × 2 | Cả 8 lượt không có dòng ý thiếu ⇒ không đi cổng web ⇒ đường không bị chạm. Tuyến / từ chối / web **giống hệt** 2 lượt của vòng 2 (8 / 8). |
| Hỏi kèm 10 × 1 | 10 / 10 luật theo ý chạy. 5 có mục web, 5 "chưa tra được tin đáng tin". **0 / 5** mục web nêu lại ý kho. |
| 3 câu kho + ngoài kho × 2 | 6 / 6 có mục web. **0 / 6** nêu lại ý kho (trước: 4 / 4). Ý ngoài kho: 0 lần trả lời bằng kho. |

**Sàn:** mục web nêu lại ý kho **0 / 11** (đạt) · an toàn không tệ hơn (đạt) · 0 câu ngoài kho bị trả lời bằng kho (đạt).

## Ghi nhận
- Mục web của câu ngoài kho phần lớn là "chưa xác minh được …". Lời này đúng (Serper không trả kết quả về loại nơi đó), nhưng ít giá trị cho người hỏi. Muốn tốt hơn thì phải đổi cách tìm (vd tìm riêng vế + tên nơi) — việc khác, chưa làm.
