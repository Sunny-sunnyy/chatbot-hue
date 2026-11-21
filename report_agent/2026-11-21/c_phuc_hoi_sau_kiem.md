# Phép kiểm số trượt ⇒ gỡ câu, không rút cả câu trả lời (nhánh `p9-c-phuc-hoi-sau-kiem`)

Viết: 13:51 21/11/2026 (giờ `date`), phiên C. Giao: phiên điều phối (đợt cải thiện harness, việc (2)). Kế hoạch đã duyệt: `c_phuc_hoi_sau_kiem_plan.md` cùng thư mục.
Trạng thái: **code + test xong, đã chạy thật 15 lượt trên hai model; chờ review + MỘT lượt trình duyệt cho sự kiện thay chữ trước khi gộp.** Nền: main `3c3aadef`.

Từ dùng: *phép kiểm số* = sau khi model viết, code so mọi con số thời tiết / khoảng cách trong chữ model với tập số được phép · *rút lại* = người dùng thấy
"Câu trả lời không đáp ứng yêu cầu trích dẫn" + nút Thử lại, chữ đã hiện bị xoá · *nấc 1* = gỡ đúng câu / dòng chứa số lạ, giữ phần còn lại · *nấc 2* = không còn gì
dùng được ⇒ câu từ chối cố định (lượt có dự báo: câu dẫn cố định + khối số liệu của hệ thống) · *thay chữ* = sự kiện mới trên đường stream, mang cả chữ cuối để
giao diện thay ô chữ đang hiện.

## 1. Người dùng thấy gì khác

| Tình huống | Trước | Sau |
|---|---|---|
| Người dùng tự nêu một con số KÈM ĐƠN VỊ ("63 % thì mưa nhiều không", "25 mm là mưa to à", "đi 2 tiếng") và model nhắc lại con số đó | Cả câu trả lời bị rút, hiện lỗi | Trả lời bình thường |
| Người dùng nêu một con số SAI ("mai nóng 45 độ phải không") và model đính chính "không phải 45 °C, dự báo là 21–26 °C" | Cả câu trả lời (đúng) bị rút | Trả lời bình thường |
| Model viết giờ đồng hồ ("bạn vào từ 13h") trong lượt có khoảng cách | Bị đếm là thời lượng lạ ⇒ rút | Không tính là thời lượng |
| Model TỰ THÊM một con số không có ở nguồn nào ("buổi trưa lên tới 35 độ") | Cả câu trả lời bị rút | Chỉ câu / dòng chứa con số đó bị gỡ; phần còn lại + khối dự báo vẫn tới người dùng. Trên màn hình: chữ hiện xong rồi câu sai biến mất |
| Như trên nhưng không còn câu nào dùng được | Rút | Câu từ chối cố định (có dự báo: câu dẫn + khối số liệu hệ thống) — không còn màn hình lỗi |
| Lượt DỰNG / SỬA lịch trình có số lạ | Rút | **Không đổi** — vẫn rút (chữ lịch do code ghép với khung, không gỡ từng câu được) |

Con số model tự thêm vẫn không tới người dùng, TRỪ một lỗ đã biết và đã thu hẹp sau review (mục 8): model tự thêm đúng con số mà người dùng vừa gõ kèm cùng loại đơn vị. Mỗi lần phép kiểm
trượt vẫn được ghi để đếm (mục 4).

## 2. Đổi gì trong code

| File | Đổi gì |
|---|---|
| `backend/llm/assistant.py` | Hàm mới `kiem_so_sau_khi_viet` (phép kiểm số tách khỏi `_thoi_tiet_cuoi`, gọi trong `_finish_generated`) · `_so_la` (tập số được phép thêm số trong câu hỏi của lượt này + câu hỏi LIỀN TRƯỚC) · `go_cau_chua` (hàm thuần gỡ câu / dòng) · `_go_so_la` (nấc 1 ⇒ kiểm lại trích dẫn + kiểm lại số ⇒ nấc 2) · trường `AnswerTrace.kiem_so_go` · ba nơi gọi `_finish_generated` truyền thêm câu hỏi |
| `backend/llm/thoi_tiet.py` · `khoang_cach.py` | Hàm tìm số trả thêm VỊ TRÍ (`vi_tri_so_thoi_tiet`, `vi_tri_so_khoang_cach`); hàm cũ giữ nguyên kết quả. Khoảng cách: luật giờ đồng hồ, chỉ áp lên chữ model — tập số được phép dựng từ dòng code in không hẹp đi |
| `backend/api/routes/chat.py` | Số đo `kiem_so_go` (chỉ số đếm: nấc, số con số lạ theo loại, số ký tự gỡ) · sự kiện stream `thay_chu` + số đo `thay_chu`: chữ đã hiện không phải phần đầu của chữ cuối ⇒ gửi cả chữ cuối trước `sources` (trước đây: không gửi gì) |
| `frontend/src/chat.jsx` | 5 dòng: nhận `thay_chu` ⇒ thay ô chữ. **`frontend/dist` phải dựng lại khi gộp** — giao diện cũ bỏ qua sự kiện này, người dùng sẽ còn thấy câu đã bị gỡ |
| Test | Mới: `tests/test_phuc_hoi_sau_kiem.py` (21 ca). Sửa theo cách xử lý mới: `test_b5b_thoi_tiet.py`, `test_khoang_cach.py`, `test_lich_vao_hoi_thuong.py`, `test_chat_stream.py` |

Sự kiện `thay_chu` viết để dùng chung: bất kỳ chỗ nào code sửa chữ model sau khi đã phát (ví dụ bỏ câu từ chối thừa ở cuối của nhánh phiên B) đều đi qua nó, không cần thêm gì.
Ba ngày sổ vết 19–21/11: 0 / 303 lượt stream thành công có chữ đã hiện khác chữ cuối ⇒ trên main hôm nay sự kiện này không bật ở lượt nào.

## 3. Bằng chứng

`R` = `HF_HUB_OFFLINE=1 UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv run --no-sync`, chạy từ `backend/` của worktree.

**Test bằng chữ dựng tay (không gọi model) [máy kiểm]:**
- `R pytest tests/test_phuc_hoi_sau_kiem.py -q` ⇒ `21 passed`. Trong đó: 8 ca model tự thêm số (4 thời tiết, 4 khoảng cách) ⇒ 8 / 8 con số không còn trong chữ gửi đi;
  5 ca đối chứng ⇒ chữ giữ nguyên từng ký tự; số chỉ có ở câu hỏi cách hai lượt hoặc ở câu TRẢ LỜI trước ⇒ vẫn bị bắt; "mất 13h" vẫn bị bắt, "lúc 13h" thì không;
  lượt có lịch vẫn rút; lượt bão vẫn có câu bản tin chính thức; đường stream có `thay_chu` trước `sources`, lượt thường không có.
- Chín file test chạm đường này (`test_b5b_thoi_tiet`, `test_khoang_cach`, `test_luoi_cuoi_bao`, `test_chat_stream`, `test_cache_tra_loi`, `test_b2_tool_loop`, `test_b5_lich_trinh`,
  `test_lich_vao_hoi_thuong`, `test_cong_dot_1`) + năm file lịch / API: đạt hết, trừ một test cần khoá OpenAI khi không nạp `.env` (lỗi có sẵn, không thuộc nhánh).
- Đã thấy ĐỎ: chép bốn file test của nhánh sang cây ở commit nền `3c3aadef` ⇒ `32 failed`; trên nhánh đạt.
- Đường OpenAI không đổi: 10 lời gọi model chụp lại, mã băm `d71894d0e7265323` (29.112 byte) — trùng main.
- Giao diện: `vite build` vào thư mục tạm chạy được, bản dựng có `thay_chu` (thư mục tạm đã xoá; `dist` của cây chính không đụng).

**Lượt thật, hai model (luna và Sonnet 5.5 mức high), 15 lượt qua lõi `answer_turn` với đúng lịch sử câu hỏi [máy chạy, phiên C đọc tay]:**

| | luna | Sonnet |
|---|---|---|
| Phát lại lượt từng bị rút vì phép kiểm số (6 lượt: 3 + 3) — không còn lỗi, giữ được câu trả lời của model | 3 / 3 | 3 / 3 |
| Lượt thứ 7 (Sonnet, phiên V10 lượt 2) | — | VẪN LỖI, nguyên nhân khác: model viết đúng một chữ "placeholder" ở vòng cuối ⇒ thiếu trích dẫn. Đây là lỗi "vòng cuối viết rác" phiên B đang xử ở nhánh riêng, không phải phép kiểm số |
| 4 câu người dùng đưa số SAI rồi hỏi "phải không" — số lượt model XÁC NHẬN con số sai | 0 / 4 | 0 / 4 |
| — trong đó model đính chính bằng số của hệ thống và nhắc lại số sai để phủ định | 4 / 4 | 3 / 4 (lượt còn lại: "không xác nhận được con số 500 mm", chỉ sang khối dự báo) |

Điều kiện phiên điều phối đặt ("≥ 2 / 4 lượt xác nhận số sai trên một model ⇒ lùi về chỉ gỡ câu") không chạm: 0 / 8. Cả tám câu trả lời này đều nhắc lại con số người dùng nêu
("45", "500", "1", "5") để phủ định hoặc để nói không xác nhận được ⇒ theo luật cũ chúng sẽ bị rút [suy luận từ luật cũ, chưa chạy tám câu này trên main] — phép nới tập số sửa
cả họ lỗi này, rộng hơn 6 lượt đã thấy.
Dữ liệu: `data/thu_bedrock_2026-11-21/c_nguoi_dung_mo_phong/phat_lai_nhanh.jsonl` (riêng tư). Bắt đầu chạy 13:40 (giờ `date`); sau đó chỉ sửa thêm một chỗ (luật giờ đồng hồ không áp lên tập
số được phép — tập đó trở về đúng như main) ⇒ bằng chứng 15 lượt dùng lại được, không chạy lại.

## 4. So với "xong khi" ghi trước

| # | Tiêu chí | Kết quả |
|---|---|---|
| 1 | Phát lại 7 lượt bị rút: 0 lỗi, ≥ 5 giữ câu trả lời của model | **Đạt một phần:** 6 / 7 không lỗi và giữ câu trả lời; 1 / 7 còn lỗi do nguyên nhân khác (dòng 2 bảng trên) |
| 2 | 8 ca số bịa bị gỡ 8 / 8; ca đối chứng giữ nguyên | Đạt (8 / 8; 5 / 5) |
| 3 | Đường không trượt giống main | Đạt (mã băm trùng; các file test hiện có đạt) |
| 4 | Stream: `thay_chu` trước `sources` khi có gỡ câu; lượt thường không có sự kiện mới | Đạt ở mức test ghép `StreamEvents`; CHƯA có lượt trình duyệt |
| Thêm | 4 câu số sai × 2 model: đếm lượt xác nhận số sai | 0 / 8 |

## 5. Chưa làm / giới hạn

- **[chưa đo trên đường thật] Nấc 1 / nấc 2 chưa bật ở lượt thật nào:** trong 15 lượt thật, phép nới tập số + luật giờ đồng hồ đã đủ, không lượt nào còn số lạ ⇒ việc gỡ câu
  mới chỉ được chứng minh bằng chữ dựng tay. Đúng như mong đợi (nó là lưới an toàn), nhưng chưa ai thấy nó chạy trên chữ model thật.
- **[chưa kiểm] Sự kiện `thay_chu` trên trình duyệt thật.** Model hiếm khi tự thêm số nên khó gọi ra bằng câu hỏi. Đề nghị: phiên có Playwright chặn phản hồi
  `/api/chat/stream` và trả một luồng dựng sẵn (`delta` × 2 ⇒ `thay_chu` ⇒ `sources` ⇒ `done`) để nhìn ô chữ được thay — kiểm nửa giao diện; nửa backend đã có test.
- Trên giao diện, câu bị gỡ HIỆN RA một thoáng rồi biến mất (chữ phát trước khi kiểm). Với Sonnet (stream giả, chữ ra một lần) khoảng này rất ngắn.
- Gỡ một câu có thể làm đoạn còn lại cụt ý; nấc 2 ở lượt khoảng cách bỏ luôn cả số đúng do code tính (người dùng nhận câu từ chối thay vì dòng khoảng cách của hệ thống).
  Có thể làm tiếp: nấc 2 của lượt khoảng cách in thẳng dòng do code dựng — chưa làm vì chưa thấy ở lượt thật nào.
- Luật giờ đồng hồ hẹp có chủ ý; "sau 5 giờ đi xe" (thời lượng) sẽ bị coi là giờ đồng hồ và lọt phép kiểm. Trích dẫn đặt SAU dấu chấm ("… 35 độ. [2] Câu kế …") ⇒ gỡ
  rộng hơn một câu (hướng an toàn).
- Phần (iii) — cùng khuôn cho bộ kiểm trích dẫn (`Grounded answer has no citation`…) — chưa làm, chờ nhánh của phiên B vào main.
- Cả bộ test backend CHƯA chạy (việc nặng, để lúc gộp); đã chạy 15 file liên quan. `STATUS_C.md` không sửa ở nhánh này (nhánh `p9-c-cong-cong-cu` đang sửa dòng đầu của nó).
- Số đo `chat_metrics` thêm hai khoá (`kiem_so_go`, và `thay_chu` ở đường stream) — ai đọc log theo danh sách khoá cố định cần biết.

## 6. Cách thử trong 2 phút

`cd <worktree>/backend && R pytest tests/test_phuc_hoi_sau_kiem.py -q` ⇒ `21 passed`. Đọc nhanh hành vi: mở test `test_invented_weather_number_is_removed_not_retracted` — bốn
dòng tham số là bốn cặp "chữ model ⇒ chữ gửi người dùng".

## 7. Bảng kết

| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Nới tập số (câu hỏi lượt này + liền trước) | Xong | `R pytest tests/test_phuc_hoi_sau_kiem.py -q -k "control or older"` ⇒ `6 passed` |
| Gỡ câu hai nấc, lượt có lịch giữ cách cũ | Xong | `… -k "invented or itinerary or storm"` ⇒ `10 passed` |
| Luật giờ đồng hồ (chỉ chữ model) | Xong | `… -k "clock or duration"` ⇒ `2 passed` |
| Số đo + vết | Xong | `… -k stream` ⇒ `1 passed` |
| Sự kiện `thay_chu` backend + giao diện | Code xong; trình duyệt CHƯA kiểm | `R pytest tests/test_chat_stream.py -q` ⇒ `25 passed` |
| Lượt thật 15 lượt × hai model | Xong | xem `phat_lai_nhanh.jsonl` |
| Phần (iii) trích dẫn | Tự hoãn — chờ nhánh phiên B | — |
| Cả bộ test, dựng lại `dist`, đo bộ câu khó / an toàn / ngoài phạm vi | Chưa — thuộc lúc gộp và phiên đo | — |

## 8. Cập nhật 14:12 21/11/2026 (giờ `date`) — sửa theo review của phiên B trên `5936d16` (1 điểm lớn + 3 điểm nhỏ) và một điều thấy ở lượt thật

Cả bốn điểm của phiên B đều tái hiện được trên nhánh trước khi sửa (`gỡ=None` ở hai ca lớn; mảnh "Từ TP."; dòng "Hai cách đi [2]:" trơ trọi).

| Điểm | Lỗi | Sửa |
|---|---|---|
| Lớn | Tập số được phép nhận MỌI con số của câu hỏi ⇒ "Ngày 30/11 … trời thế nào?" mở cửa cho "khoảng 30 °C" model tự thêm; "đoàn 15 người" mở cửa cho "15 km". Main chặn được hai ca này | Phiên điều phối chốt THU HẸP: chỉ nhận số đứng kèm đơn vị của đúng phép kiểm. Thời tiết: `tt.so_kem_don_vi` (°C / độ / mm luôn nhận; "%" chỉ khi câu hỏi có chữ mưa / ẩm / khả năng / xác suất ở bất kỳ đâu). Khoảng cách: `kc.tap_so_theo_loai` trên câu hỏi, km và thời gian tách riêng |
| Nhỏ 1 | Cắt câu sau chữ viết tắt ⇒ còn mảnh "Từ TP." | Không cắt sau từ 1–3 chữ IN HOA + dấu chấm (và "Tp.", "Th."); "Huế." vẫn là hết câu |
| Nhỏ 2 | Mọi gạch đầu dòng bị gỡ ⇒ dòng dẫn "…:" còn một mình | Dòng dẫn vốn đứng trước danh sách mà không còn dòng danh sách theo sau ⇒ gỡ luôn |
| Nhỏ 3 | Lượt chỉ tìm kho bị gỡ câu nay là "success" ⇒ bản đã gỡ được LƯU vào bộ nhớ câu trả lời cho người sau | `luot_luu_duoc` thêm điều kiện `kiem_so_go is None` |

**Thêm ngoài review, từ lượt thật:** lần chạy lại 15 lượt sau khi thu hẹp, nấc 1 BẬT lần đầu trên chữ model thật (Sonnet, phiên V03 lượt 2): model tự tính "mức dự phòng chỉ còn khoảng
10–40 phút" (17h30 trừ giờ tham quan xong) — phép tính đúng nhưng "40" không có ở nguồn nào ⇒ bị gỡ. Lúc đó code gỡ CẢ gạch đầu dòng ba câu, mất hai câu có nguồn đứng trước. Đã
sửa: gạch đầu dòng nhiều câu chỉ mất đúng câu có số lạ (ký hiệu đầu dòng + các câu còn lại ở lại); gạch đầu dòng một câu vẫn mất cả dòng. Trên main lượt này bị rút cả câu trả lời.
Giới hạn nói thẳng: phép kiểm không kiểm được phép tính, nên một con số model TÍNH ĐÚNG từ số có nguồn vẫn bị gỡ.

**Chạy lại sau khi sửa:**
- [máy kiểm] `R pytest tests/test_phuc_hoi_sau_kiem.py -q` ⇒ đạt hết (có 4 ca "số không kèm đơn vị trong câu hỏi" phải bị gỡ, gồm hai ca của phiên B; ca "TP."; ca dòng dẫn; ca bộ nhớ câu
  trả lời); chín file test chạm đường này đạt.
- [lượt thật, C đọc tay — chạy 14:05, TRƯỚC bản sửa gạch đầu dòng] 15 lượt × hai model: 0 lỗi; 6 / 6 lượt từng bị rút vì phép kiểm số vẫn giữ câu trả lời (5 lượt nguyên chữ model, 1
  lượt mất một gạch đầu dòng như kể trên); lượt thứ 7 (V10 lượt 2) lần này model tự trả câu từ chối khuôn; 4 câu số sai × 2 model: model xác nhận số sai 0 / 8 (7 đính chính bằng số
  hệ thống, 1 nói không xác nhận được). Dữ liệu: `phat_lai_nhanh_2.jsonl` cùng thư mục riêng tư.
- Lỗ còn lại sau thu hẹp (chấp nhận, ghi để đếm): người dùng gõ "45 độ", model tự khẳng định "mai 45 độ" ⇒ qua phép kiểm. 0 / 8 lượt thật model làm vậy.
- Giới hạn phiên B nêu khi soát lại `f85fed7` (READY): người dùng nêu số KHÔNG kèm đơn vị ("mai nóng 45 phải không?") và model đính chính "không phải 45 độ đâu" ⇒ câu đính chính
  bị gỡ; người dùng nhận câu dẫn cố định + khối dự báo (không lỗi, không số sai, nhưng mất lời đính chính). Cái giá của việc thu hẹp; để thước đếm.

## 9. Ghi 14:17 21/11/2026 (giờ `date`) — nhánh này (`p9-c-phuc-hoi-kiem-so`) CHỈ có phần kiểm SỐ; phần (iii) trích dẫn TREO

Phiên điều phối quyết gộp phần kiểm số (đã có review READY) và treo phần (iii) — đổi lượt trượt bộ kiểm TRÍCH DẪN thành câu từ chối cố định. Lý do: với chữ rác của model
(`placeholder`, `tim_kho`), câu "không tìm thấy đủ thông tin" nói một điều chưa chắc đúng, và số "lượt lỗi hoặc từ chối" của thước không giảm (lượt chỉ chuyển cột); hai gốc của
chữ rác đang được chữa ở nhánh khác. Commit (iii) được giữ làm hồ sơ trên nhánh `p9-c-phuc-hoi-sau-kiem` (`70c9f44`), không nằm trong nhánh này (đã hoàn nguyên). Ở nhánh này, lượt
trượt bộ kiểm trích dẫn vẫn như main: bị rút + nút Thử lại.
