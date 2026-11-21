# Khoá mức suy luận riêng cho lời gọi định tuyến + trò chuyện trên Bedrock (nhánh `p9-c-suy-luan-dinh-tuyen`)

Viết: 15:16 21/11/2026 (giờ `date`), phiên C. Giao: phiên điều phối. Nền: main `c6f64070`. Trạng thái: **code + test xong, mặc định KHÔNG đổi hành vi; chờ một phiên khác đọc diff; phiên đo chọn giá trị.**

Từ dùng: *định tuyến* = lời gọi model đầu tiên của mỗi lượt, chỉ trả một nhãn (trợ lý Huế / trò chuyện / ngoài phạm vi / khẩn cấp) · *mức suy luận* = `none | low | medium | high`, gửi
kèm mỗi lời gọi Claude; mức cao cho phép model nghĩ lâu hơn trước khi trả lời.

## 1. Người dùng thấy gì khác
Không gì cả khi gộp: khoá mới đặt `high`, đúng mức các lời gọi này đang chạy. Sau này nếu phiên đo chọn mức thấp hơn thì chỉ lời gọi định tuyến và lời đáp xã giao đổi mức.

## 2. Vì sao
Trang "model thấy gì" (21/11) cho thấy trên Sonnet, 19 / 21 lời gọi dùng chung `reasoning_default: high`, kể cả lời gọi định tuyến (đầu ra một nhãn) và lời đáp xã giao. Chưa có cách
đổi riêng hai loại này để đo.

## 3. Đổi gì
| File | Đổi gì |
|---|---|
| `backend/config/settings.yaml` | Khoá `full_corpus_generation.bedrock.reasoning_dinh_tuyen: high` |
| `backend/llm/generator_openai_full_corpus.py` | Tham số `dinh_tuyen_reasoning` (mặc định None = không gửi mức nào, đường OpenAI như trước); agent định tuyến + agent trò chuyện dùng chung một thiết lập mang mức này; các bản sao của agent định tuyến (có lịch sử, ba bản viết câu tìm) thừa hưởng. Đường Bedrock truyền giá trị của khoá |
| `backend/core/settings_loader.py` | Kiểm khoá mới như hai khoá mức suy luận đã có (thiếu / giá trị lạ ⇒ lỗi lúc nạp) |
| `backend/tests/test_bedrock_model.py`, `test_phase6_settings.py` | Test 4 mức + khoá hỏng bị từ chối |

## 4. Bằng chứng
`R` = `HF_HUB_OFFLINE=1 UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv run --no-sync`, từ `backend/` của worktree.

**[máy kiểm, không gọi model]**
- `R pytest tests/test_bedrock_model.py -q -k router_and_chat` ⇒ `4 passed`: thân gửi Bedrock của mọi agent định tuyến + trò chuyện mang đúng mức của khoá (`none` ⇒ không gửi mức, chỉ
  suy luận giữa các lần gọi công cụ); lời gọi trả lời vẫn theo `reasoning_default`; nhóm lịch giữ mức riêng; đường OpenAI không gửi mức nào. Đã thấy đỏ: cùng test với generator cũ ⇒
  `3 failed, 1 passed` (ca `high` trùng mặc định nên qua).
- Ba file test liên quan ⇒ 52 đạt + 1 ca cần khoá OpenAI khi không nạp `.env` (có sẵn). Mã băm 10 lời gọi đường OpenAI `d71894d0e7265323` = main.
- Chụp thân lời gọi qua route thật, 9 kịch bản / 21 lời gọi (script "trang model thấy gì"): main ↔ nhánh ở mặc định ⇒ **21 / 21 thân giống hệt**; khoá = `low` / `none` ⇒ chỉ lời gọi định tuyến
  và trò chuyện đổi mức, lời gọi có công cụ và nhóm lịch không đổi.

**[lượt thật trên Bedrock, 15 lời gọi, mỗi ô MỘT lượt — chỉ để biết đường chạy, không phải số so sánh]**

| Mức | 4 lời gọi định tuyến (giây) | token suy luận | đúng tuyến | 1 lời đáp xã giao (giây) |
|---|---|---|---|---|
| high | 0,9 · 0,6 · 0,6 · 0,7 | 0 | 4 / 4 | 1,5 |
| low | 0,7 · 0,8 · 0,6 · 0,5 | 0 | 4 / 4 | 1,4 |
| none | 0,7 · 0,6 · 0,7 · 0,6 | 0 | 4 / 4 | 1,9 |

Cả ba mức đều được Bedrock nhận (0 lỗi). **Điều phải nói thẳng:** ở bốn câu dễ này mức `high` KHÔNG chậm hơn — model không dùng token suy luận nào ở mức nào. Giả thuyết "thời
gian chờ thừa ở mọi lượt" của tôi chưa được số thật ủng hộ; lợi ích, nếu có, nằm ở câu ranh giới làm model nghĩ lâu (thước của phiên đo từng thấy lời gọi định tuyến lâu nhất
4,6 giây). Phải đo trên bộ ranh giới mới biết.

## 5. Chưa làm / giới hạn
- Chưa đo đúng tuyến + thời gian trên bộ ranh giới tuyến, rìa Huế, chuỗi — việc của phiên đo; cho tới lúc đó khoá để `high`.
- Lời gọi mục "Từ web", hỏi bằng ảnh KHÔNG thuộc khoá này (vẫn theo `reasoning_default`).
- Script đo dựng cấu hình bằng tay phải có khoá mới trong khối `bedrock` (lấy từ `load_settings` thì có sẵn).
- Cả bộ test chưa chạy.

## 6. Bảng kết
| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Khoá + nối vào agent định tuyến / trò chuyện | Xong | `R pytest tests/test_bedrock_model.py -q -k router_and_chat` ⇒ `4 passed` |
| Mặc định không đổi hành vi | Xong | so thân 21 lời gọi main ↔ nhánh: 0 khác |
| Chọn giá trị | Chưa — phiên đo | — |
