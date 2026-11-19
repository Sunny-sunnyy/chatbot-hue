# Implementation Report: nói thật giới hạn thay câu từ chối khuôn ở việc "làm thay" (cờ `noi_that_lam_thay`, mặc định TẮT)

Người viết: phiên E · 14:29 19/11/2026 (giờ `date`) · nhánh `p9-e-noi-that-gioi-han` từ `origin/main` `7a59b69` · worktree `/tmp/hr_e_noi_that`.
Trạng thái: **chờ review cả nhánh (B)**; CHƯA có lượt qua server, CHƯA chạy bộ dò của người khác, CHƯA chạy cả bộ test. Tiền API: 0 USD.
Plan (riêng tư, phiên điều phối duyệt theo sha `84669acd93a9`): `data/tu_choi_khuon_2026-11-19/PLAN.md`. Chủ dự án đã chọn: ba câu riêng theo loại, KHÔNG hiện mục web ở các lượt đó.

## 1. Phạm vi

Người dùng nhờ trợ lý TỰ LÀM một việc hệ thống không có — đặt phòng / bàn / vé, gửi thư hay tin nhắn, xem tình trạng phòng — hôm nay nhận câu "không tìm thấy đủ thông tin" rồi một mục web lạc đề. Với cờ bật: nếu câu người dùng là câu nhờ làm thay VÀ câu trả lời đã là câu từ chối khuôn, code thay bằng một câu nói thật (không làm được việc gì, người dùng tự làm tiếp bằng cách nào) và không tra web.
Không làm: sửa lời dặn nào · thêm lời gọi model · đặt phòng / gửi thư thật · rút ngắn thời gian chờ (trợ lý vẫn tìm kho rồi mới ra câu khuôn để bị thay) · câu không dấu.

## 2. Thay đổi chính

| File | Đổi gì |
|---|---|
| `backend/llm/lam_thay.py` (mới, 47 dòng) | Hàm thuần `nho_lam_thay(câu) → None / dat_cho / gui / tinh_trang`. Danh sách cho phép hẹp: phải có dấu nhờ trợ lý tự làm; câu hỏi thông tin (ở đâu, cách nào, số điện thoại…) và câu nhờ soạn / tóm / chép ⇒ None. |
| `backend/llm/full_corpus_prompt.py` | Ba câu `CAU_LAM_THAY` (hằng số, dễ đổi chữ); cả ba vào `REFUSAL_ANSWERS` ⇒ log và bộ đánh giá đếm chúng là TỪ CHỐI. |
| `backend/llm/assistant.py` | Cờ + trường `trace.lam_thay` (đặt ở `_before_model` khi cờ bật) · hàm `_noi_that_lam_thay` gọi ở HAI nơi câu từ chối khuôn hình thành: sau `prepare_answer` (ngữ cảnh rỗng) và đầu `_finish_generated` (model tự từ chối) — mọi đường (không stream, stream, stream song song) đều qua hai nơi này · đường stream: lượt hàm bắt được thì bật cơ chế giữ chữ sẵn có, thêm một nhánh giữ cả khi câu khuôn kèm khoảng trắng cuối. |
| `backend/api/routes/chat.py` | `lam_thay` vào danh sách lượt được nhớ; sự kiện `done` của lượt này không mang `tu_choi_kho` (giao diện không hiện khối "gợi ý cách hỏi"). |
| `backend/config/settings.yaml` | Một dòng `noi_that_lam_thay: false`. |
| `backend/tests/test_noi_that_lam_thay.py` (mới) | 39 test, mục 3. |

Cách đóng mục web: câu nói thật đặt kết thúc cố định `lam_thay`; `web_gate_open` sẵn có chỉ mở với kết thúc thường ⇒ không sửa cổng web. Không kiểm trích dẫn (câu do code viết, không có nguồn). Lượt có lịch, có dự báo, hoặc câu khớp lưới bão / lũ ⇒ KHÔNG thay (các lớp code nối ở đó giữ nguyên). Log: một mục `{"name": "lam_thay", "loai": …}` trong trường `tools` sẵn có — không chữ người dùng, không trường log mới.

Lệch so với plan (đã báo phiên điều phối, đã được nhận): câu loại "gửi" có thêm "Nếu bạn đã có lịch," trước phần chỉ nút — cuộc chưa có lịch thì không có nút nào dưới lịch; dùng một câu cho cả hai trạng thái thay vì đọc trạng thái lịch. Plan nói thêm nhánh ở `_chu_giu_lai`; thực tế không cần — kết thúc cố định đi qua nhánh "câu cố định thành một `delta`" sẵn có của đường stream.

## 3. Cách đã chạy thật

Mọi lệnh từ `backend/` của worktree, `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag/backend …`; `data/` và kho nối tạm bằng symlink (không commit).

| Việc | Loại bằng chứng | Kết quả |
|---|---|---|
| `python -m pytest tests/test_noi_that_lam_thay.py -q` | test — hàm thuần (21 ca) + chỗ thay dựng tay (9) + **lõi thật với MODEL GIẢ và bộ tìm THẬT** (9: không stream, stream, stream song song) | 39 đạt (28 s; lần đầu 94 s) |
| Phá code lần 1: bỏ điều kiện giữ chữ ở lượt nhờ làm thay | thấy ĐỎ | 4 / 4 test stream hỏng (câu khuôn lọt ra màn hình) |
| Phá code lần 2: bỏ nhánh "khoảng trắng cuối" | thấy ĐỎ | 2 / 4 hỏng (đúng hai ca có xuống dòng cuối) |
| `tests/test_chat_stream.py`, `tests/test_settings_env.py` (file cũ chạm chỗ sửa, không nạp bộ tìm) | test cũ | đạt (chạy chung phần nhẹ: 59 đạt) |
| Quét hàm trên các bộ ĐÃ THẤY (công cụ riêng tư `data/tu_choi_khuon_2026-11-19/tools/quet_ham.py`, 0 USD, chỉ in số đếm) | chạy thẳng hàm thật trên dữ liệu thật | 176 câu mẫu: bắt 0 · 44 câu ngoài phạm vi: 0 · 32 câu an toàn: 0 · 106 lượt gõ của bộ kịch bản phổ thông: bắt 4, đúng 4 lượt đích của plan, đúng loại; 0 lượt ngoài đích |
| `git diff --check` | — | sạch |

## 4. Kết quả quan sát

- Cờ bật, câu nhờ làm thay, model (giả) trả câu khuôn: người dùng chỉ nhận MỘT mảnh chữ = câu nói thật; không mảnh nào của câu khuôn; không trạng thái "đang tra web"; 0 lần gọi dịch vụ tìm web.
- Cùng câu đó mà model trả lời được từ kho: chữ model ra nguyên, kể cả khi mở đầu trùng chữ đầu của câu khuôn.
- Cờ bật ↔ tắt trên cùng một câu: mọi yêu cầu gửi model (lời dặn, đầu vào, công cụ) của định tuyến và trợ lý giống nhau; bên tắt chỉ thừa đúng lần gọi viết mục web.
- Lượt hàm không bắt (và mọi lượt khi cờ tắt): `trace.lam_thay` là None ⇒ không nhánh mới nào chạy.

## 5. Lỗi và giới hạn

- **Chưa có bằng chứng trên model thật.** Mọi test dùng model giả trả đúng câu khuôn; lượt qua server (4 kịch bản đích × 3 + 5 lượt từ chối đúng, ước 0,03 USD) chưa chạy — chờ lượt máy.
- **Hàm được viết khi người viết đã biết 4 câu đích** ⇒ "4 / 4 bắt đúng" không phải phép thử độc lập. Phép thử thật là bộ dò 20 + 20 do phiên khác soạn (người viết không xem).
- Chưa chạy cả `backend/tests` trên nhánh (việc nặng, cần lượt máy). Ba câu mới nằm trong `REFUSAL_ANSWERS` — test nào khoá đúng hai phần tử của tập đó sẽ lộ ở lượt cả bộ.
- Chưa đo "chuỗi gửi model giống byte" bằng công cụ chụp của lượt đo cuối — mới có test model giả so yêu cầu ở một câu.
- Phần chạy song song: khi câu từ chối do ngữ cảnh rỗng bị thay, bước gộp không còn ghi dấu "từ chối trước model" vào bộ ghi số đo (kết thúc đã đổi tên). Chỉ ảnh hưởng một con số log; chưa sửa — nhờ người review cho ý kiến.
- Sót theo thiết kế: câu không dấu, cách nói lạ, câu nhiều ý có dòng "Tư liệu chưa có thông tin về:" ⇒ như hôm nay. Người dùng vẫn chờ đủ thời gian trợ lý tìm kho.
- Câu "đặt chỗ" nhắc mục Chỗ ở; câu "gửi" nhắc nút "Sao chép lịch" / "Tải về" — đổi tên trên giao diện thì phải sửa hằng số.

## 6. Bàn giao cho người kiểm

- Đọc diff: `git diff origin/main...origin/p9-e-noi-that-gioi-han -- backend` (4 file sửa + 2 file mới).
- Nên tự kiểm bằng cách khác: (a) câu dò riêng cho hàm thuần, nhất là họ "nghe giống nhờ làm mà là hỏi thông tin / việc bằng chữ"; (b) hai chỗ gọi `_noi_that_lam_thay` đã đủ mọi đường chưa — `git grep -n 'INSUFFICIENT_ANSWER' -- backend/llm/assistant.py` (nơi câu khuôn được đặt: ngữ cảnh rỗng, chạm trần lượt, chỉ còn dòng ý thiếu, model tự viết); nhánh chạm trần lượt (`max_turns`) CỐ Ý không thay; (c) lượt bão / lũ: điều kiện chặn dựa vào `thoi_tiet_ctx` — có đủ không.
- Việc còn lại theo plan: bộ dò 20 + 20 (phiên khác soạn) ⇒ chạy thẳng hàm ⇒ lượt qua server ⇒ đọc kết quả ⇒ bật cờ là việc hỏi chủ dự án.
