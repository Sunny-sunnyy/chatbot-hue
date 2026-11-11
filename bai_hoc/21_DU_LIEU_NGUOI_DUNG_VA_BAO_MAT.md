# Bài 21 — Dữ liệu người dùng đi đâu, và bảo mật

*Cập nhật lần cuối: 15:17, ngày 11/11/2026 · bài mới; đã qua một lượt kiểm độc lập.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Bộ ba nguy hiểm — **mới** | **lethal trifecta** (skill `agent-security-review`) | Một agent đồng thời (1) đọc được dữ liệu riêng tư, (2) đọc chữ từ nguồn không tin được, (3) có đường gửi ra ngoài. Đủ cả ba thì chữ lạ có thể lừa nó gửi dữ liệu đi. |
| Chỉ dẫn lén — **mới** | **prompt injection** | Câu ra lệnh giấu trong dữ liệu (trang web, ảnh, câu hỏi) để model làm theo. |
| Rào an toàn trình duyệt | **CSP** (`FRONTEND_CSP`) | Trình duyệt chỉ chạy mã và tải ảnh từ chính máy chủ của chatbot. |
| Bộ lọc chữ hiển thị | **DOMPurify** (danh sách cho phép) | Trước khi hiện câu trả lời, chỉ giữ các thẻ định dạng thường; bỏ hết thẻ có thể tải hay chạy thứ gì. |
| Không lưu phía OpenAI | **`store=False`** | Mỗi lần gọi model đều báo OpenAI không lưu câu trả lời để lấy lại sau. |

---

*Bài 18 kể đóng gói để đưa lên mạng. Trước khi người lạ dùng được, cần trả lời rõ: **chữ người dùng gõ đi tới đâu, ai giữ, bao lâu**, và **người khác có lợi
dụng được chatbot không**. Bài này kể những gì đã làm cho hai câu đó.*

## Quay lại người hướng dẫn viên

Người hướng dẫn viên tốt không chép tên, số điện thoại của khách vào sổ. Muốn hỏi giúp ai, họ chỉ nói phần cần hỏi. Nhớ chuyện khách vừa kể thì nhớ trong đầu,
xong buổi là quên. Có người dúi một tờ giấy "hãy đưa khách này tới cửa hàng X" thì họ biết đó là **tờ giấy của người lạ**, không phải lời của sếp.

## Chữ người dùng đi tới đâu

| Dữ liệu | Đi tới | Giữ bao lâu | Rào |
|---|---|---|---|
| **Câu hỏi** (tối đa 500 ký tự) | OpenAI: lần xếp loại + lần trả lời, kèm 10 đoạn kho (cộng đoạn mới khi trợ lý tìm thêm, tối đa 2 lần) | máy chủ **không ghi** chữ vào đĩa hay log; mọi lần gọi đặt `store=False` | Vì chạy song song (bài 17), câu chào hỏi cũng gửi kèm đoạn kho tới OpenAI. Đoạn kho soạn từ nguồn công khai, không có bí mật, nên chấp nhận được |
| **3 câu hỏi trước** | bộ nhớ máy chủ (RAM); gửi kèm ở lượt sau | 30 phút từ lượt cuối, hoặc bấm "Cuộc trò chuyện mới", hoặc tắt máy chủ | **Chỉ câu hỏi**, không giữ câu trả lời (lý do chất lượng, bài 13) |
| **Mã cuộc trò chuyện** | cookie trình duyệt ↔ máy chủ | 30 phút | Mã ngẫu nhiên, không gắn danh tính. Trang web không đọc được cookie bằng mã, chỉ gửi cho đường `/api`. Bản đóng gói đặt mặc định "chỉ gửi qua HTTPS" (chưa thử, vì lần chạy thử dùng http — bài 18) |
| **Câu tìm web** (chỉ khi câu về Huế mà kho từ chối) | Serper (tìm Google) | máy chủ không ghi chữ | Chỉ câu **lượt này**. Code bỏ email và số điện thoại, cắt còn 120 ký tự. Bản đóng gói **tắt** tra web |
| **Thời tiết** | Open-Meteo | kết quả giữ 30 phút trong RAM | **0 chữ người dùng**, chỉ gửi toạ độ cố định trung tâm Huế |
| **Ảnh** | OpenAI | máy chủ **không lưu** ảnh, không ghi tên file | Thu nhỏ, **xoá thông tin vị trí và máy chụp** trước khi gửi; chặn sai kiểu, quá 10 MB, khác nguồn trước khi đọc (bài 15) |
| **Nút 👍 / 👎** | log của chatbot | theo vòng xoay log | Chỉ ghi mã lượt ngẫu nhiên, loại câu, kết quả, số nguồn. **Không** ghi chữ |
| **Nút "Báo thông tin chưa đúng"** (trang Khám phá) | log của chatbot | theo vòng xoay log | Chỉ ghi mã bài, và mã đó phải trùng một bài có thật, nên không ghi được chuỗi tuỳ ý |
| **Số đo mỗi lượt** | log của chatbot | 10 MB × 3 bản cũ | Chỉ số đếm, thời gian, tiền, token. Danh sách trường bị **khoá bằng test**, nên không ai thêm nhầm trường chữ được |
| **Địa chỉ IP** | RAM, chỉ khi bật giới hạn lượt (bản đóng gói) | xoá khi sang ngày mới | Log "hết lượt" không ghi IP |

**Người dùng được báo:** trang Giới thiệu có mục "Dữ liệu của bạn": câu hỏi được nhớ 30 phút, không lưu chữ vào nhật ký, câu hỏi gửi OpenAI (khi tra web thì
gửi cả dịch vụ tìm kiếm), "đừng gõ thông tin cá nhân", ảnh được thu nhỏ, bỏ vị trí, gửi OpenAI, không lưu.

**Kiểm bằng chạy thật:** mỗi lần thay đổi vào bản chính, cổng kiểm đếm log, yêu cầu **0 chữ câu hỏi** (bài 20). Lần chạy thử bản đóng gói (10/11): file log của
chatbot có **0 chữ câu hỏi, 0 địa chỉ IP**.

## Bộ ba nguy hiểm, và chatbot đứng ở đâu

Một agent nguy hiểm nhất khi có **cả ba**: đọc được dữ liệu riêng tư, đọc chữ không tin được, và có đường gửi ra ngoài. Với hue_rag:
1. **Dữ liệu riêng tư:** ngữ cảnh gửi model chỉ có câu hỏi, 3 câu hỏi trước, và đoạn kho (soạn từ nguồn công khai); không có khoá, không có dữ liệu người khác.
2. **Chữ không tin được:** có: câu hỏi, đoạn trích web, chữ trong ảnh.
3. **Đường ra:** công cụ của model **chỉ đọc** (tìm kho, ngày, thời tiết). Không công cụ nào mở link, ghi file hay gửi tin. Câu tìm web do **code** dựng, không
   do model.

Vì vậy, khi bị lừa, điều tệ nhất model làm được là viết **một câu sai cho chính người đang hỏi**, không lấy được dữ liệu của ai khác. Rủi ro lớn nhất ở đây là
"nội dung sai trình bày như thật". Rào chính vì thế là **code kiểm trước khi hiện**.

## Chống chỉ dẫn lén

| Chữ không tin được | Rào |
|---|---|
| Câu hỏi, kho | Lời dặn nói rõ: câu hỏi, tiêu đề, bằng chứng **đều là dữ liệu**, không làm theo chỉ dẫn nằm trong đó |
| Trang web | Model đọc đoạn trích web trong **một lần gọi riêng**: không công cụ, không kho, không lịch sử. Code kiểm cuối: mã nguồn phải có trong sổ link, chặn mọi link do model tự viết, số tiền phải có nguyên văn trong đoạn trích, câu thiên tai thay bằng câu cố định (bài 15) |
| Link | Ở mục web, chữ của model **không tạo được link**; link chỉ lấy từ sổ nguồn do code dựng. Trang không tự tải gì từ máy khác (CSP) |
| Chữ trong ảnh | Model chỉ được trả mã trong danh sách 42 tên, code kiểm lại, người dùng phải **bấm xác nhận** |
| Lịch sử trò chuyện | Máy chủ giữ, **không nhận từ trình duyệt**, nên không ai gửi giả "trợ lý đã nói…" để cài lệnh được |

## Các lượt rà bảo mật đã làm

| Lúc | Rà gì | Tìm ra | Đã sửa |
|---|---|---|---|
| 01/11 (đóng gói Phase 1–8) | chatbot + chính các agent làm đồ án | chatbot: 11 rủi ro, 0 chặn. Agent: 2 rủi ro lớn: agent tự đẩy code lên repo công khai; công cụ tra web cho agent đọc được file máy và trang lạ cùng lúc | thêm hook lúc đẩy code (bài 20); script tra web khoá chỉ đọc, thấy lệnh lạ thì dừng; bộ lọc chữ đổi sang danh sách cho phép, CSP cho mọi trang |
| 01–02/11 (trước Phase 9) | thêm công cụ + tra web | 15 rủi ro, 6 mức chặn (trang web cài lệnh, công cụ nhận link do model chọn, link giả, web nói ngược cảnh báo an toàn, vòng lặp không dừng…) | làm theo: không công cụ mở link, link do code dựng, câu thiên tai cố định, tra web tối đa 1 lần mỗi câu (chờ tối đa 5 giây, không thử lại), bỏ số điện thoại / email, lỗi tra web khác "không có", ngày do code tính |
| 05/11 (hỏi bằng ảnh) | ảnh có dán chữ "ra lệnh" | 1 / 3 ảnh lừa được model (trong ngưỡng ghi trước ≤ 1 / 3) | hậu quả bị chặn vì model chỉ gợi tên, người dùng phải bấm |
| 05/11 (kiểm code tra web) | người kiểm độc lập thử trên trình duyệt thật | link dạng mã trang web thô lọt vào mục "Từ web"; bộ dò thiên tai thiếu "lụt", "áp thấp" | vá cả hai; dò lại: 0 link ngoài. Lỗ chưa từng tới người dùng vì tra web lúc đó còn tắt |
| 10/11 (đóng gói) | giả địa chỉ IP để lách giới hạn | vẫn bị chặn | — (bài 18) |

**Hai việc anh chọn không làm** (01–02/11): không dùng model thứ hai soát chữ web, không dựng bộ kết quả web xấu cố định để đo. Chống trang web cài lệnh vì vậy
**chỉ dựa vào rào bằng code**. Đây là giới hạn đã biết.

## Một chuyện thật: hai lớp rào, nhưng một cửa chỉ có một lớp

Ngày 01/11, giao diện chữ hiện dần có **hai lớp** chống chữ lạ tải thứ gì từ máy khác: bộ lọc chữ kiểu **danh sách cấm**, và CSP. Người kiểm thử 16 kiểu thẻ có
thể tải đồ ngoài, trên **cả hai** đường vào trang. Ở trang chính, CSP chặn hết. Nhưng cùng trang đó mở qua một đường dẫn thứ hai **không gắn CSP**, và bộ lọc lại
thiếu hai thứ ít ai để ý (thuộc tính ảnh nền của bảng, và thẻ ô nhập dạng ảnh): **3 / 16 ca** lọt, mỗi ca **1 lượt tải ra máy ngoài**.

Cách sửa: đổi bộ lọc sang **danh sách cho phép** (chỉ khoảng 25 thẻ định dạng thường, vài thuộc tính), và gắn cùng CSP cho **mọi** trang. Thử lại: **0 lượt tải ra
ngoài** ở cả hai đường. Bài học giống bài 18: rào hai lớp chỉ an toàn khi **cả hai lớp phủ mọi cửa vào**, và danh sách cho phép an toàn hơn danh sách cấm.

## Khi nào hỏng

- **Phía OpenAI và Serper giữ dữ liệu bao lâu** thì chưa kiểm. `store=False` chỉ là một phần; chính sách giữ dữ liệu để chống lạm dụng của họ chưa đọc kỹ.
- **Tên riêng trong câu tìm web** vẫn đi tới Serper (chỉ email và số điện thoại bị bỏ). Vì vậy trang Giới thiệu dặn "đừng gõ thông tin cá nhân".
- **Ảnh có chữ lừa:** 1 / 3 ảnh thử vẫn lừa được model. Chỉ cần người dùng không bấm nhầm thì không sao.
- **Chống trang web cài lệnh chỉ bằng code**, chưa có bộ đo hai chiều (anh chọn không làm).
- **Log truy cập của máy chủ web:** một phép thử nhỏ (11/11) cho thấy lúc khởi động, chatbot nạp lại cấu hình log và việc đó **tắt** log truy cập mặc định của
  máy chủ web. Nghĩa là IP nhiều khả năng **không** bị in ra màn hình. Chưa kiểm trên máy chủ thật đang chạy.

## Ba điều chính

1. **Chữ người dùng chỉ đi tới OpenAI** (và Serper khi tra web). Máy chủ không ghi chữ vào log; nhớ 3 câu hỏi trong 30 phút; ảnh không lưu, đã xoá vị trí;
   👍 / 👎 không ghi chữ. Kiểm bằng cổng kiểm: 0 chữ câu hỏi trong log.
2. **Không đủ bộ ba nguy hiểm:** công cụ chỉ đọc, ngữ cảnh không có bí mật, câu tìm web do code dựng. Bị lừa thì tệ nhất là một câu sai cho chính người hỏi,
   nên rào chính là **code kiểm trước khi hiện**.
3. **Năm lượt rà bảo mật đã làm**: ba lượt đầu có sửa, hai lượt sau xác nhận rào đang giữ. Chuyện thật: một đường vào trang thiếu CSP đã lọt lượt tải ra ngoài ⇒ đổi sang danh sách cho phép, gắn CSP
   cho mọi trang.

**Hết bộ bài.** Muốn hiểu kỹ một bước, quay lại đúng bài đó; bảng tổng mọi lần so sánh ở bài 19.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Câu hỏi ≤ 500 ký tự: `backend/api/routes/chat.py`; `store=False`: `backend/llm/generator_openai_full_corpus.py`, `backend/llm/nhan_anh.py` [code]; câu không về Huế gửi đoạn kho do chạy song song: `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` [tài liệu]
- Nhớ 3 câu hỏi, 30 phút, chỉ câu hỏi: `backend/api/conversations.py`; cookie HttpOnly, SameSite=Strict, đường `/api`, `HUE_COOKIE_SECURE`: `chat.py` [code]
- Câu tìm web (bỏ email / số điện thoại, ≤ 120 ký tự, câu lượt này), lần gọi riêng, kiểm cuối: `backend/llm/tra_web.py` [code]; thời tiết chỉ toạ độ: `backend/llm/thoi_tiet.py`, `backend/tests/test_assistant_boundary.py` [code]
- Ảnh không lưu, xoá EXIF, chặn trước khi đọc: `backend/api/routes/anh.py`, `nhan_anh.py` [code]
- 👍 / 👎 và "Báo thông tin chưa đúng" không ghi chữ: `backend/api/feedback.py` [code]; trường số đo khoá bằng test: `chat.py` + `backend/tests/test_api_chat.py` [code]; giới hạn lượt không log IP: `backend/api/gioi_han.py` [code]
- Trang Giới thiệu "Dữ liệu của bạn": `frontend/src/pages.jsx` [code]
- Log 0 chữ câu hỏi, 0 IP (10/11): `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md` [đã chạy]
- Lượt rà 01/11 (11 rủi ro, 0 chặn; agent 2 rủi ro lớn): `report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md`, `TONG_HOP.md` [tài liệu]
- Lượt rà trước Phase 9 (15 rủi ro, 6 chặn): `data/nghien_cuu_phase_9_2026-11-01/agent/a_sa2.md` (riêng tư); hai việc không làm: `docs/superpowers/specs/2026-11-02-phase-9-design.md` §7 [quyết định của anh]
- Ảnh chữ lừa 1 / 3: `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` [đã chạy]
- Kiểm code tra web (link thô, "lụt", "áp thấp"; dò lại 0 link): `report_agent/2026-11-02_phase_9_code/b165_review.md` [đã chạy]
- Chuyện thật CSP (16 ca, đường dẫn thứ hai không CSP, sửa sang danh sách cho phép, 0 lượt tải ngoài): `report_agent/2026-10-31_streaming_spec/s3_giao_dien_review.md`; dấu vết trong `backend/api/app.py`, `frontend/src/markdown.js` [đã chạy, code]
- Log truy cập: phép thử 0 USD của A 11/11: tạo logger `uvicorn.access` rồi gọi `core.logging_setup.setup_logging()` ⇒ `disabled = True` (cấu hình `backend/config/logging.yaml` không đặt `disable_existing_loggers`, mặc định Python là tắt các logger có sẵn) [đã chạy, probe nhỏ; chưa chạy máy chủ thật]
- Bản ghi số liệu (agent con, chỉ đọc, 11/11): `data/hoc_cung_user_2026-11-10/fact_bao_mat_va_tinh_nang.md` (riêng tư)
- Ví dụ người hướng dẫn viên và tờ giấy là ví dụ tự đặt.

- **Sửa 15:17 11/11/2026** (người kiểm độc lập bắt, mình đối chiếu nguồn; biên bản `data/hoc_cung_user_2026-11-10/review_bai_20_21.md`, riêng tư): đoạn kho có thể hơn 10 khi tìm thêm (`backend/llm/assistant.py` `MODEL_SEARCH_LIMIT = 2`); tra web 1 lần / câu, chờ ≤ 5 s; CSP: 3 / 16 ca (`background`, `input type=image`), `s3_giao_dien_review.md`; cookie Secure chưa thử (lần thử đặt `HUE_COOKIE_SECURE=0`); "0 IP" chỉ trong file log của chatbot; kho không nằm trên repo công khai (chỉ soạn từ nguồn công khai).

</details>
