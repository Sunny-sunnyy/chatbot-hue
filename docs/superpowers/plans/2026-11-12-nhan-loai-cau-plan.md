# Plan (mức nhẹ) — nhãn loại câu do code gắn vào `chat_metrics` · **NHÁP — chờ User chọn**

Người viết: C, 19:30 12/11/2026 (`date`), A giao. Chưa code, 0 USD.

## Căn cứ để review

- Lý do: `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` §2 (log không đếm được theo loại câu) · `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` dòng A6.
- Code: `backend/api/routes/chat.py` (`METRIC_FIELDS`, chỗ ghi dòng `chat_metrics`) · các bộ dò sẵn có: `backend/llm/ngay_lich.py` (`co_tu_ngay`), `backend/llm/tra_web.py` (dò câu thiên tai / lưu trú), `backend/llm/so_tien.py`.
- Ranh giới dữ liệu: `bai_hoc/21` + `Project_Status.md` §6 (log không ghi nội dung).

## 1. Vấn đề

Log mỗi câu có tuyến, từ chối, web, tiền, thời gian — **không** có "câu này hỏi về gì". Hôm nay muốn biết người hỏi lưu trú / ăn gần / sự kiện ra sao thì phải tự viết câu gửi thử.
Khi đưa lên mạng, không có nhãn này thì vẫn không biết người thật hỏi loại gì nhiều, loại nào hay bị từ chối ⇒ ưu tiên việc tiếp theo vẫn là đoán.

## 2. Việc đề xuất

Thêm **một trường** `loai_cau` vào `chat_metrics`: danh sách nhãn (0–3 nhãn) do **code** dò từ chữ câu hỏi bằng từ khoá; **chỉ ghi tên nhãn, không ghi chữ nào của câu**.
Không dùng model, không thêm lượt gọi, không đổi câu trả lời, không đổi chuỗi gửi model.

| Nhãn | Dò bằng (từ khoá có dấu, không phân biệt hoa thường) |
|---|---|
| `luu_tru` | khách sạn, homestay, nhà nghỉ, resort, chỗ ở, lưu trú, đặt phòng (dùng lại bộ dò lưu trú của mục web nếu trùng) |
| `an_uong` | ăn, quán, món, nhà hàng, cà phê, đặc sản |
| `gan_diem` | gần, quanh, cạnh, cách … bao xa, đối diện |
| `gia_ve` | vé, giá, bao nhiêu tiền, miễn phí + bộ dò số tiền sẵn có |
| `gio_mo_cua` | mấy giờ, giờ mở cửa, đóng cửa |
| `ngay_lich` | bộ dò từ chỉ ngày sẵn có (`co_tu_ngay`) |
| `su_kien` | lễ hội, sự kiện, festival, biểu diễn, chương trình |
| `di_chuyen` | đi bằng gì, xe, taxi, thuê xe, đường đi, bao xa |
| `thoi_tiet` | thời tiết, mưa, nắng, bão, lũ |
| `lich_trinh` | lịch trình, kế hoạch, đi mấy ngày + lượt từ biểu mẫu |
| `so_sanh` | so với, khác gì, nên chọn, hay là |
| (rỗng) | không khớp nhãn nào — vẫn ghi `[]` |

Danh sách cố định trong một hằng số; thêm / bớt nhãn = sửa hằng + test. Nhãn **không** dùng để quyết bất cứ điều gì lúc chạy (chỉ ghi log) ⇒ dò sai không làm hỏng câu trả lời.

- **Chỗ sửa:** file mới nhỏ `backend/llm/loai_cau.py` (một hàm thuần `loai_cau(query) -> list[str]`) · `backend/api/routes/chat.py` (thêm tên trường vào `METRIC_FIELDS`, gọi hàm ở chỗ dựng dòng số đo, cả đường thường lẫn đường stream).
- **Vì sao từ khoá mà không nhờ bước phân loại của model:** không thêm tiền / thời gian, không đổi lời dặn định tuyến (đổi lời dặn là một bậc đo đủ); nhãn thô là đủ để **đếm**.

## 3. Tiêu chí ghi trước

| | Mức | Đo bằng |
|---|---|---|
| Không lộ nội dung | dòng log chỉ chứa tên nhãn thuộc danh sách; grep chữ câu hỏi trong log = 0 | test + cổng ổn định (server thật, 2 câu tự viết) |
| Không đổi hành vi | chuỗi gửi model giống byte 228 / 228; câu trả lời không qua hàm mới | Q1 sẵn có |
| Dò đủ dùng | trên 18 câu tự viết của lượt đếm 12/11 (đã biết loại): ≥ 16 / 18 câu có đúng nhãn chính; trên 20 câu Golden lấy theo seed ghi trước: 0 câu bị gắn `luu_tru` / `su_kien` nhầm quá 2 câu | script 0 USD (đọc bộ câu private, in số đếm) |
| Test | hàm thuần: mỗi nhãn 2 câu có + 1 câu không; câu rỗng nhãn; câu nhiều nhãn; test khoá tập trường `chat_metrics` cập nhật | pytest file mới + file chạm |

## 4. Tiền · giờ · file chạm

- **Tiền ≈ 0,001 USD** (2 câu cổng ổn định). **Giờ:** ~1 giờ agent.
- **Chạm:** `backend/llm/loai_cau.py` (mới) · `backend/api/routes/chat.py` · `backend/tests/test_loai_cau.py` (mới) + test khoá trường log · bài học 21 (một câu: log có thêm nhãn loại câu, vẫn không có nội dung) · sổ ghi việc khâu API.
- Sàn phải giữ: ranh giới "log không ghi nội dung" (bài 21); giống byte chuỗi gửi model.

## 5. Khi nào sai · giới hạn

- Từ khoá bắt nhầm (chữ "ăn" trong từ khác, "vé" trong tên riêng) ⇒ số đếm theo nhãn là **ước thô**, dùng để xếp ưu tiên, không dùng làm số báo cáo chất lượng.
- Một nhãn hiếm + giờ gửi có thể gợi ra nội dung câu của một người trong log ít dòng ⇒ nhãn giữ ở mức rộng như bảng trên, không thêm nhãn theo tên địa danh.
- Chỉ có ích khi có người dùng thật ⇒ làm **trước khi deploy** thì từ ngày đầu đã có số; làm sau thì mất dữ liệu giai đoạn đầu.

## 6. Cần User chọn

Làm / không làm; có đồng ý ghi nhãn loại câu (không nội dung) vào log khi đưa lên mạng không — đây là thay đổi nhỏ về dữ liệu người dùng nên hỏi rõ.
