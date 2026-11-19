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

## 5b. Sửa sau review nhánh (B) và bộ dò lượt 1 (C) — một bản sửa, 19/11/2026

- **Review của B: 1 major + 3 minor, nhận hết.** Major — hai mẫu "đặt … giúp" và "bạn đặt …" quá rộng: 22 câu dò "nghe giống mà không phải" của B ra SAI 6. Sửa: thứ được đặt phải đứng gần động từ (≤ 3 từ, không vắt qua dấu phẩy); dấu nhờ đứng sau chỉ nhận ở cuối câu; câu kể việc đã đặt / hỏi kinh nghiệm / "đặt câu hỏi, đặt tên, đặt lịch" ⇒ không bắt. Sau sửa: SAI 1 / 22 (đúng câu B ghi là lành, không cần sửa), 10 / 10 câu nhờ thật bắt đúng loại.
  Minor 1 — ở nơi thay thứ nhất (ngữ cảnh rỗng) điều kiện "lượt bão – lũ không thay" chưa có hiệu lực vì ngữ cảnh thời tiết được đặt SAU bước đó ⇒ nay xét thẳng lưới bão / lũ trên câu người dùng; có test, đã thấy đỏ khi bỏ điều kiện. Minor 2 — phần chạy song song nay vẫn ghi dấu "từ chối trước model" khi câu từ chối do ngữ cảnh rỗng bị thay (một điều kiện). Minor 3 — ghi rõ ở đây: **lượt bị thay KHÔNG còn mục web và KHÔNG còn khối gợi ý cách hỏi** trên giao diện.
- **Bộ dò lượt 1 của C** (C chạy, người viết không xem trước; trên bản `ca6223e`): đúng loại 14 / 20 (ngưỡng ≥ 15) · ra SAI LOẠI 1 (sàn 0) · đối chứng bắt nhầm 0 / 20 ⇒ CHƯA đạt. Họ lỗi: loại "gửi". Sửa đúng một lần theo plan: xét "gửi" TRƯỚC "đặt chỗ" (câu nhờ gửi thư xác nhận đặt phòng từng ra "đặt chỗ"); thêm "gửi tin nhắn / thư … giúp", "nhắn … cho <nơi> … giúp", "email cho mình …"; bỏ luật coi "số điện thoại của …" là câu hỏi thông tin; câu gửi ĐỒ VẬT (bưu thiếp, hành lý, quà…) không bắt. Trên sáu câu trượt C gửi: 5 / 6 nay đúng loại; câu còn lại ("còn bàn trống không") là cách nói ngoài danh sách của plan — để sót có chủ ý vì câu nói thật loại "tình trạng" chỉ nói về phòng.
- Chạy lại sau sửa [máy kiểm]: phần test không nạp bộ tìm 70 đạt (gồm file test stream cũ) · quét hàm trên 252 câu đối chứng bắt 0, 4 / 4 lượt đích đúng loại. **CHƯA chạy lại 9 test nạp bộ tìm thật sau bản sửa** (máy đang có lượt đo; phần sửa không chạm đường stream, trừ một điều kiện ở bước gộp) và CHƯA có kết quả bộ dò chạy lại + bộ bù của C.

## 5c. Bản sửa CUỐI — thu hẹp hàm (phiên điều phối chốt sau bộ bù của reviewer), 19/11/2026

- Bộ bù 18 câu của B trên bản 5b: bắt nhầm 4 / 12 câu "không phải nhờ làm" (3 câu do các mẫu "gửi / nhắn … giúp" vừa nới, 1 câu "đặt cọc … giúp mình với"). Phiên điều phối chốt: THU HẸP, không chỉnh thêm mẫu — bắt nhầm một câu hỏi thông tin (mất câu trả lời + mục web) tệ hơn sót một câu nhờ làm thay (lượt sót chạy y như cờ tắt).
- Đã làm: bỏ ba mẫu "gửi tin nhắn … giúp", "nhắn … cho <nơi> … giúp", "nhắn giúp mình cho …" và chữ "nhắn" khỏi dấu người gửi; "giúp / hộ" chỉ là dấu nhờ khi kề đại từ hoặc ở cuối câu; "đặt cọc / tiền cọc" vào danh sách loại. Giữ: xét "gửi" trước "đặt chỗ", "tới số điện thoại của …", "email cho mình …".
- Kết quả trên MỌI bộ đã ghi [máy kiểm, người viết chạy]: 22 câu của B — bắt nhầm 1 (câu reviewer ghi là lành: hỏi còn phòng), sót 1 / 10 · 18 câu bù của B — bắt nhầm **0 / 12**, sót 3 / 6 · 252 câu đối chứng (câu mẫu, ngoài phạm vi, an toàn) — bắt **0** · 4 lượt đích của bộ kịch bản — 4 / 4 đúng loại · sáu câu trượt bộ dò lượt 1: 3 nay đúng loại (gồm câu từng ra sai loại), 3 sót có chủ ý. Phần test không nạp bộ tìm: 73 đạt.
- **Giới hạn nhận sau thu hẹp (sót, không bắt):** "nhắn / nhắn tin cho <khách sạn, nhà hàng…> giúp mình là …" · "gửi tin nhắn cho … báo giúp mình …" · "đặt … cho mình nhé" khi thứ được đặt đứng trước chữ "cho mình" · "gửi mail … cho mình" (kênh là tân ngữ, không sau giới từ) · "còn bàn / còn vé không". Các lượt đó vẫn ra câu từ chối khuôn + mục web như hôm nay.
- CHƯA có: kết quả chạy lại bộ dò gốc + bộ bù của C trên bản này; 9 test nạp bộ tìm thật chạy lại; lượt model thật.

## 6. Bàn giao cho người kiểm

- Đọc diff: `git diff origin/main...origin/p9-e-noi-that-gioi-han -- backend` (4 file sửa + 2 file mới).
- Nên tự kiểm bằng cách khác: (a) câu dò riêng cho hàm thuần, nhất là họ "nghe giống nhờ làm mà là hỏi thông tin / việc bằng chữ"; (b) hai chỗ gọi `_noi_that_lam_thay` đã đủ mọi đường chưa — `git grep -n 'INSUFFICIENT_ANSWER' -- backend/llm/assistant.py` (nơi câu khuôn được đặt: ngữ cảnh rỗng, chạm trần lượt, chỉ còn dòng ý thiếu, model tự viết); nhánh chạm trần lượt (`max_turns`) CỐ Ý không thay; (c) lượt bão / lũ: điều kiện chặn dựa vào `thoi_tiet_ctx` — có đủ không.
- Việc còn lại theo plan: bộ dò 20 + 20 (phiên khác soạn) ⇒ chạy thẳng hàm ⇒ lượt qua server ⇒ đọc kết quả ⇒ bật cờ là việc hỏi chủ dự án.
