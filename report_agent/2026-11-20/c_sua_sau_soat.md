# Sửa sau soát khác hãng — hai điểm C viết (ghi 09:31 20/11/2026, giờ `date`; nhánh `p9-c-sua-sau-soat-2011`; phiên điều phối chốt SỬA, phiên E review)

Nguồn: lượt soát của model khác hãng trên bản code `a1f4df59`; C tái hiện cả hai điểm trước khi sửa (hồ sơ tái hiện + script: riêng tư).

**1. Đường stream — chữ cuối dài hơn chữ đã hiện.**
- Người dùng thấy gì khác: khi model phát hai khối chữ mà khối đầu là một câu trả lời ngắn đã đóng, trước đây màn hình chỉ có câu đầu (phần thiếu có thể là câu cảnh báo của nguồn) dù lượt vẫn báo thành công. Nay phần đuôi được phát nốt trước danh sách nguồn.
- Sửa: `backend/api/routes/chat.py` `StreamEvents.finish` — chữ đã phát là TIỀN TỐ của chữ cuối đã qua kiểm ⇒ phát thêm phần đuôi. Không phải tiền tố ⇒ như cũ (không ghép hai bản khác nhau; cờ `delta_matches_final` vẫn ghi để đếm).
- Bằng chứng [máy kiểm, test bằng đồ giả stream — KHÔNG phải lượt thật]: `tests/test_chat_stream.py::test_tail_of_final_answer_is_sent_when_the_shown_text_is_only_its_beginning` ĐỎ trên code cũ, xanh trên code mới; cả file 24 đạt.
- Giới hạn: [chưa đo trên đường thật] — trong log, 0 / 1.488 lượt stream thành công từng gặp ca này (3 lượt lệch đều là ca "chưa phát mảnh nào", đã sửa 19/11); sửa vì hệ quả thuộc hạng nặng nhất (thiếu cảnh báo) và chỉ vài dòng. Ca cùng họ CHƯA sửa ở nhánh này: mảnh duy nhất đã phát là khối do code nối (dự báo thời tiết) còn chữ model bị ẩn hết — chỗ sửa nằm ở lõi (`llm/assistant.py`), không phải `finish`; chờ phiên điều phối quyết.

**2. Lượt sửa lịch không đổi được gì ghi đè bản lưu ⇒ file PowerPoint mất câu bão / lũ + 112.**
- Người dùng thấy gì khác: hỏi về bão ⇒ lập lịch (thẻ + file có câu bản tin chính thức + 112) ⇒ gõ một câu sửa mà trợ lý chưa làm được. Trước đây thẻ lịch trên màn hình vẫn còn câu đó nhưng file tải về thì mất; nay file vẫn còn.
- Sửa: `backend/llm/len_ke_hoach.py` `luu_sau_luot` — lượt SỬA mà không ý nào làm được ⇒ không trả bản lưu mới ⇒ route giữ bản lưu cũ (khớp điều kiện giữ thẻ của `frontend/src/App.jsx`). Lượt biểu mẫu và lượt sửa làm được: như cũ.
- Bằng chứng [máy kiểm]: `tests/test_len_ke_hoach_v2.py::test_edit_turn_that_changes_nothing_keeps_the_saved_plan_and_its_storm_sentence` — hàm thật (hiểu ý ⇒ áp ⇒ dựng lịch với bộ tìm thật ⇒ `luu_sau_luot` ⇒ route tải thật), giả: câu trả của lần gọi hiểu ý + câu tả của bản lưu; ĐỎ trên code cũ đúng ở dòng "không trả bản lưu", xanh trên code mới; đối chứng trong cùng test: lượt sửa làm được thì bản lưu là lịch mới.
- Giới hạn: test KHÔNG đi qua `POST /api/chat/stream` (từ bản bổ sung dưới đây test gọi đúng hàm `luu_lich_cua_luot` mà route gọi sau lượt đạt, không còn lặp tay) — dựng chuỗi ba lượt qua route cần kịch bản model giả cho ba kiểu lời gọi, C không làm; [chưa đo trên đường thật]. Lượt sửa LÀM ĐƯỢC vẫn lưu bản mới không có câu an toàn — lúc đó thẻ mới trên màn hình cũng không có, hai bên khớp nhau (không đổi ở nhánh này).

**2b. Bổ sung sau review của phiên E (ghi 09:48 20/11/2026, giờ `date`; phiên điều phối chốt sửa).**
- Lỗi review tìm ra ở bản sửa 2 [C tái hiện bằng máy trước khi sửa: main có câu 112 trong file, bản sửa 2 thì mất]: lịch lập khi CHƯA nhắc bão ⇒ người dùng gõ một câu sửa CÓ chữ bão mà trợ lý chưa làm được ⇒ khung trợ lý có câu bản tin chính thức + 112, nhưng vì bản sửa 2 không ghi bản lưu nữa nên file tải về không có câu đó (trước bản sửa 2 thì có).
- Sửa: phần ghi bản lưu của route gom vào MỘT hàm `backend/api/routes/chat.py` `luu_lich_cua_luot`; thêm một luật: lượt sửa không đổi được gì mà chính lượt đó có câu an toàn ⇒ giữ bản lưu cũ, chỉ thêm câu an toàn vào nó. Không chạm `api/conversations.py`.
- Bằng chứng [máy kiểm]: cùng test ở mục 2, thêm ca ngược — bỏ hai dòng luật mới thì ĐỎ đúng ở dòng ca ngược, có thì xanh; bản lưu sau lượt = bản cũ + đúng một trường câu an toàn.
- Giới hạn: [chưa đo trên đường thật] — phiên E sẽ thử một lần qua giao diện trên mã cuối. Thẻ lịch CŨ trên màn hình vẫn không có câu đó (câu nằm ở khung trợ lý của lượt vừa gõ); file thì có.

| Đã làm | Lệnh kiểm (từ `backend/`, từng file) | Đầu ra |
|---|---|---|
| Sửa 1 + test | `uv run pytest -q tests/test_chat_stream.py` | 24 passed |
| Sửa 2 + test | `HF_HUB_OFFLINE=1 uv run pytest -q tests/test_len_ke_hoach_v2.py` | 93 passed |
| File chạm quanh | `test_lich_pptx` 15 · `test_sua_lich_v2` 11 · `test_rao_so_ngay` 44 · `test_luoi_cuoi_bao` 10 · `test_noi_dong_tam_ngung` 31 | đều đạt |
| `test_api_chat` có nạp khoá (`--env-file .env`), sau khi gộp main `5945b78` | `uv run --env-file ../.env pytest -q tests/test_api_chat.py` | 15 passed (ca gọi model thật ≈ 0,0007 USD mỗi lần chạy, cận trên) |

Chưa làm: cả bộ test (một lượt trên main cuối, theo điều phối) · lượt thật qua server · dòng giới hạn cho hai điểm "ghi giới hạn" của đợt soát (phiên B gom) · ca cùng họ nêu ở mục 1. Tiền: ≈ 0,0015 USD (hai lần chạy `test_api_chat` có khoá). Mọi dòng bảng trên chạy lại sau bản bổ sung 2b và sau khi gộp main, từng file.

**3. Lịch đã sửa giữ câu an toàn của lịch gốc (ghi 10:02 20/11/2026, giờ `date`; nhánh `p9-c-sua-sau-soat-2-2011`; phiên điều phối chốt SỬA thay vì ghi giới hạn).**
- Người dùng thấy gì khác: hỏi về bão ⇒ lập lịch (file có câu bản tin chính thức + 112) ⇒ một lượt sửa LÀM ĐƯỢC mà câu sửa không nhắc bão (ví dụ bỏ một điểm). Trước đây file tải về sau đó mất câu 112 (phiên E thấy khi thử qua giao diện); nay file của lịch đã sửa vẫn còn.
- Sửa: `backend/api/routes/chat.py` `luu_lich_cua_luot`, 2 dòng — lượt sửa làm được mà lượt đó không có câu an toàn riêng ⇒ bản lưu mới thừa hưởng câu an toàn của bản lưu trước. Lượt biểu mẫu lập lịch mới ⇒ KHÔNG thừa hưởng (lịch khác).
- Bằng chứng [máy kiểm]: test chuỗi ở mục 2 mở rộng — ĐỎ trên code cũ đúng ở dòng thừa hưởng, xanh sau sửa; hai đối chứng trong cùng test: bản trước không có câu an toàn ⇒ bản mới cũng không; lượt có dạng biểu mẫu ⇒ không thừa hưởng. Từng file: `test_len_ke_hoach_v2` 93 · `test_lich_pptx` 15 · `test_chat_stream` 24 · `test_sua_lich_v2` 11 · `test_api_chat` (có khoá) 15 — đều đạt.
- Giới hạn: [chưa đo trên đường thật]. Thẻ lịch MỚI trên màn hình vẫn KHÔNG có câu đó (câu trên thẻ đi theo lượt, không theo bản lưu) ⇒ file có câu an toàn mà thẻ mới không có — lệch về phía an toàn, không sửa giao diện ở nhánh này. Câu an toàn theo lịch tới khi người dùng lập lịch mới bằng biểu mẫu hoặc cuộc hết hạn, kể cả khi bão đã qua trong cùng cuộc (30 phút). Ca đối chứng "biểu mẫu" trong test dựng bằng cách bỏ khối `thay_doi` khỏi một lượt sửa, không phải một lượt biểu mẫu chạy thật. Tiền thêm ≈ 0,0007 USD.
