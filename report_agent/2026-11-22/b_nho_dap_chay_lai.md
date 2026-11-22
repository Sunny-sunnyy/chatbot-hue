# Mục [8] — lượt bị rút vì lỗi trích dẫn khi đang nhớ câu trả lời liền trước: tự chạy lại một lần thay cho màn hình lỗi

Viết 10:49 22/11/2026 (giờ `date`), phiên B. Nhánh `p9-b-nho-dap-chay-lai`. Giao: phiên điều phối, sau cổng đóng của phiên đo. Không công tắc mới: bản sửa chỉ sống trong nhánh "đang nhớ câu trả lời liền trước" của `nho_cau_tra_loi` (đang mở). Chưa ai đọc lại.

**Từ dùng:** *bị rút* = câu trả lời model viết không qua bộ kiểm trích dẫn (ở đây: không trích nguồn nào) ⇒ hệ thống không cho nó là câu trả lời, giao diện xoá chữ và hiện lỗi "Thử lại" · *lịch sử* = phần cuộc trò chuyện gửi kèm cho model; khi tính năng mở, ô của lượt liền trước mang cả câu trả lời · *lịch sử để lùi* = chính lịch sử đó với ô cuối về dòng ghi chú / rỗng, như khi tính năng tắt.

## 1. Người dùng thấy gì khác
| Tình huống | Trước | Sau |
|---|---|---|
| "Lên kế hoạch tham quan Huế 2 ngày" (trợ lý trả một lộ trình bằng chữ) ⇒ "Bỏ Chợ Đông Ba đi", và model chép lại lời cũ không trích nguồn (phiên đo 22/11: 3 / 7 lần) | chữ hiện ra rồi bị xoá, màn hình "Câu trả lời không đáp ứng yêu cầu trích dẫn — Thử lại" | chữ hiện ra rồi bị gỡ, các dòng tiến độ hiện lại, khoảng 10 giây sau là kết quả của lần chạy lại: câu trả lời có nguồn, hoặc câu từ chối như khi chưa mở tính năng. Không màn hình lỗi |
| Lần chạy lại cũng bị rút | — | màn hình lỗi như cũ (chỉ chạy lại một lần) |
| Mọi lượt khác (không mang câu trả lời nhớ; không bị rút; câu cố định; cuộc có lịch đã lưu) | — | không đổi |

## 2. Một giả định bị lật khi đọc code
Lời giao giả định chữ chưa ra màn hình trước khi kiểm trích dẫn. Thực tế [đọc `llm/assistant.py` hàm stream + `api/routes/chat.py`]: lõi phát chữ ngay khi chữ tới, kiểm sau; kiểm hỏng thì route gửi lỗi kèm `after_text: true` và giao diện xoá chữ. Vì vậy bản sửa phải gỡ chữ đã hiện — dùng sự kiện `thay_chu` có sẵn (giao diện thay cả ô chữ, `frontend/src/chat.jsx`), không sửa giao diện. Phiên điều phối đồng ý; đường "giữ chữ tới khi kiểm xong" không chọn vì nó đổi cách phát chữ của mọi lượt hỏi tiếp.

## 3. Đổi gì
| File | Đổi gì |
|---|---|
| `backend/llm/assistant.py` | `answer_turn_stream_parallel` nay là vỏ: chạy thân cũ (đổi tên `_luot_stream`, không sửa chữ nào bên trong); nếu lượt bị rút VÀ route đã đưa lịch sử để lùi VÀ không phải câu cố định VÀ cuộc không có lịch lưu ⇒ phát `thay_chu` rỗng, chạy lại thân một lần trên một trace mới với lịch sử để lùi, rồi chép kết quả lần hai vào trace của lượt; lời gọi model của cả hai lần đều vào sổ tiền; thêm mục `chay_lai_khong_dap` (kèm đầu lời lỗi của lần đầu do code đặt) vào danh sách công cụ của lượt. Trường mới `AnswerTrace.lich_su_khong_dap` |
| `backend/api/conversations.py` | `history_khong_dap()`: lịch sử với ô cuối về dòng ghi chú; None khi ô cuối không mang câu trả lời |
| `backend/api/routes/chat.py` | lúc mở lượt: đặt `trace.lich_su_khong_dap` khi kho đang nhớ câu trả lời liền trước · sự kiện `thay_chu` từ lõi đi qua `StreamEvents.thay_chu` (sổ chữ đã phát về đúng) |
| `backend/tests/test_nho_dap_chay_lai.py` | 10 ca |
| `guides/RUNBOOK_BAN_GIAO.md` | một hàng giới hạn ở 10.1 |

Bẫy đã tránh: đường chạy song song gộp trace phụ vào trace chính và ghi đè mọi trường không phải đầu vào của route ⇒ lịch sử để lùi phải đọc TRƯỚC khi chạy lần đầu (phép thử ngược bên dưới bắt đúng chỗ này).

## 4. Bằng chứng
- **Test [máy kiểm; tìm kho thật, model theo kịch bản — "thấy câu trả lời nhớ thì viết không trích nguồn"]:** `tests/test_nho_dap_chay_lai.py` 10 passed. Gồm: bị rút ⇒ chạy lại ⇒ ra kết quả lần hai (đường thường và đường song song) · lần hai cũng bị rút ⇒ lỗi cũ, đúng hai lần gọi trả lời · không có lịch sử để lùi / không bị rút ⇒ chuỗi sự kiện GIỐNG HỆT thân cũ `_luot_stream` · cuộc có lịch lưu không chạy lại · kho trả lịch sử để lùi đúng lúc · route biến sự kiện thay chữ thành một bản chữ cuối sạch · MỘT ca qua cả route thật (hai lượt liền qua `/api/chat/stream`): không sự kiện `error`, đúng một `thay_chu`, kết `success`, sổ số đo có mục `chay_lai_khong_dap` và đủ 4 lời gọi, lượt được nhớ bằng câu trả lời của lần chạy lại.
- **Phép thử ngược (đã thấy đỏ):** tắt lần chạy lại ⇒ 4 ca đỏ · đọc lịch sử để lùi SAU lần chạy đầu ⇒ 2 ca đỏ, đúng hai ca đường song song · route không đưa lịch sử để lùi ⇒ ca qua cả route đỏ.
- **Lượt thật qua model đang chạy, một lần [máy kiểm]:** script của phiên đo `muc_8/chay_sua_chu.py bat` từ cây nhánh, ba chuỗi × hai lượt: 6 / 6 `success`, 0 lỗi hiện. Lần này KHÔNG lượt nào bị rút ⇒ lần chạy lại chưa được kích hoạt trên model thật; lượt này chỉ cho biết bản sửa không làm hỏng đường thường. Phép đo đúng chuỗi lỗi 5 lần + chuỗi "quán thứ hai" là của phiên đo.
- **Phiên đo đo lại trên model đang chạy, từ cây nhánh [người thứ hai kiểm]:** chuỗi "lộ trình bằng chữ ⇒ Bỏ Chợ Đông Ba đi" × 5: 0 / 5 màn hình lỗi (trước bản sửa: 3 / 7); lần chạy lại kích hoạt thật ở 2 / 5 lượt (sổ số đo có mục `chay_lai_khong_dap`, một sự kiện gỡ chữ, 5 và 6 lời gọi model) và cả hai kết bằng câu trả lời có chữ; chuỗi "quán thứ hai" vẫn đúng. Hồ sơ riêng tư: `data/thu_bedrock_2026-11-21/do/muc_8/luot_2211/sua_chu_sau_sua_x5.jsonl`.
- **Bảng test từng file [máy kiểm]:** 58 file có dùng lõi / route / kho cuộc trò chuyện, chạy từng file trên cây nhánh, không env: 1.881 ca đạt; 54 file đạt hết; 4 file có ca đỏ vì thiếu khoá OpenAI khi không nạp env (`test_api_chat` 14 + 1 lỗi · `test_openai_full_corpus_generator` 7 + 2 lỗi · `test_phase6_live_smoke` 18 + 1 lỗi · `test_phase6_settings` 4 + 1 đỏ) — đúng bốn file vẫn được ghi là bỏ khi không nạp env. Bảng riêng tư: `data/thu_bedrock_2026-11-21/b_muc_8_chay_lai/test_tung_file.tsv`. Đã gộp vào main `5be861af`; cả bộ test trên main sau gộp là của phiên đo.

## 5. Chưa làm · giới hạn
- Chưa ai nhìn trên trình duyệt dáng của lúc chữ lần đầu bị gỡ rồi chữ lần hai hiện lại (mới thấy qua chuỗi sự kiện; phiên đo nhìn ở cổng đóng).
- Tỉ lệ lần chạy lại CŨNG bị rút trên model thật: 0 / 2 ở lượt đo — mẫu quá nhỏ để nói gì.
- Cuộc có lịch đã lưu và đường `/api/chat` không stream: không có bản sửa.
- Dòng tiến độ riêng kiểu "đang kiểm lại nguồn" không làm: cần sửa giao diện; người dùng thấy lại các dòng tiến độ thường.
- Lượt chạy lại tốn gấp đôi lời gọi model và thêm khoảng 10 giây.
- Bản sửa không làm giảm số lần model viết không trích nguồn; nó đổi đoạn kết. Lỗi "không trích nguồn ⇒ rút cả câu" ở lượt KHÔNG mang câu trả lời nhớ (đã thấy 5 / 72 lượt ở bộ đo S2) vẫn ra màn hình lỗi như cũ.

Phép này KHÔNG cho biết: tỉ lệ lần chạy lại ra câu trả lời dùng được so với câu từ chối trên model thật · hướng rộng hơn: cùng cơ chế "bị rút ⇒ chạy lại một lần" áp được cho MỌI lượt bị rút vì không trích nguồn (không riêng lượt có câu trả lời nhớ) — đáng đếm trước trong sổ lượt thật · đếm rẻ nhất: số lượt `retracted` có `loi_kiem = khong_trich_dan` trong sổ lượt thật 15–22/11, chia theo có / không có lịch sử.
