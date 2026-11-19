# Hỏi tiếp về nơi vừa được nhắc tới: trợ lý nhớ TÊN nơi (cờ `nho_ten_goi_y`, mặc định TẮT) — code + lượt đo

Viết 20:05 19/11/2026 (giờ `date`). Phiên B viết plan + code + chạy đo · phiên C soạn bộ chuỗi đích (B không xem) và tính cột bộ đích · phiên E review nhánh và đọc tay đủ mọi lượt · phiên điều phối duyệt plan theo mã băm (`794384caf568`, khối sửa sau duyệt `3463b2509ee6`). Hồ sơ riêng tư đủ mã chuỗi, câu và từng ô: `data/hoi_tiep_goi_y_2026-11-19/` (`PLAN.md`, `KET_QUA.md`, `bo_dich_C/`, `do/doc_tay_E.md`). File này chỉ ghi ở mức loại câu.

Từ dùng: **lượt hỏi tiếp** = câu thứ hai trở đi trong một cuộc trò chuyện, nói "quán đó", "chỗ đầu tiên"… · **lịch sử** = thứ của các lượt trước được gửi kèm cho model · **bài riêng của một nơi** = bài kho nói về đúng một quán / quán cà phê / điểm đến / di tích · **bài tổng hợp** = bài cẩm nang nhắc nhiều nơi · **cờ** = một dòng bật / tắt trong `backend/config/settings.yaml` · **bộ bẫy** = 12 chuỗi soạn 03/11 để bắt lỗi "hỏi tiếp về ý kho không có thì mượn đoạn của nơi khác".

## 1. Người dùng thấy gì khác
**Từ khi cờ bật:** sau khi trợ lý nhắc tới một nơi có bài riêng trong kho, người dùng hỏi tiếp "cho địa chỉ quán đó" thì trợ lý trả đúng nơi vừa nhắc, thay vì tự tìm lại kho và có lúc trả địa chỉ một nơi khác.

**Quyết định (chủ dự án, tối 19/11/2026): BẬT.** Sàn bộ bẫy 5 / 6 không đạt theo chữ plan; chủ dự án chọn bật, hiểu sàn là "không trả lời bằng thông tin của nơi khác" — diễn giải sau khi thấy số, do chủ dự án quyết. Cờ được bật bằng một commit riêng (nhánh bật chung ba cờ, phiên E giữ); giới hạn ở sổ tay bàn giao mục 10.1.

## 2. Lỗi và cách sửa
- **Lỗi đã thấy thật** (lượt đo 80 kịch bản trưa 19/11): lịch sử chỉ có CÂU HỎI của các lượt trước, không có trợ lý đã trả lời gì. Lượt hỏi tiếp, model viết câu tìm kho từ câu hỏi cũ nên có lúc ra nơi khác. Trong lượt đo tối 19/11 bên cờ tắt: 10 lượt hỏi tiếp trả lời chắc chắn về SAI nơi.
- **Vì sao không bật lại "nhớ cả câu trả lời":** 03/11 cách đó làm lượt hỏi tiếp về ý kho không có bị trả lời bằng đoạn của nơi khác (phạm sàn), và chữ lịch trình (có tên quán từ bản đồ mở) sẽ vào lịch sử.
- **Cách sửa — code ghi, model chỉ đọc** (`backend/llm/ten_goi_y.py`): sau một lượt trả lời thường từ kho, code lấy tên bài của các nguồn câu trả lời ĐÃ TRÍCH là bài riêng của một nơi (thư mục kho: `foods/restaurants/`, `foods/cafes/`, `travel/places/`, `heritages/heritage/`; bỏ file tên có chữ "guide"), tối đa 5 tên, và đặt MỘT dòng vào chỗ tin trợ lý của lịch sử: "câu trả lời lượt này có trích bài kho của các nơi: …; danh sách có thể thiếu nơi đã được nêu và không theo thứ tự trong câu trả lời". Không lấy chữ model viết, không lấy mục web, không lấy lịch; lượt lịch / biểu mẫu / từ chối / câu cố định không để lại dòng nào. Không thêm câu dặn nào cho model.
- **File đổi:** `llm/ten_goi_y.py` (mới) · `api/conversations.py` (`append` nhận thêm dòng ghi chú) · `api/routes/chat.py` (`_remember`) · `evaluation/full_corpus_eval.py` (đường chạy chuỗi của bộ đo) · `llm/assistant.py` + `config/settings.yaml` (cờ) · `tests/test_nho_ten_goi_y.py` (mới).
- **Sửa thiết kế TRƯỚC lượt đo:** bản đầu của dòng ghi chú viết "đã gợi ý, theo thứ tự: 1. …; 2. …". Khi khoá bộ đích trên dữ liệu bên cờ tắt, phiên C thấy hai cơ chế làm dòng đó nói quá điều code biết: nơi chỉ được nêu qua bài tổng hợp không có trong danh sách nên số thứ tự lệch với thứ tự người dùng thấy; bài riêng được trích chỉ để nêu vị trí cũng bị gọi là "đã gợi ý". Đã bỏ đánh số và chữ "đã gợi ý"; plan được duyệt lại trước khi có số nào của bên cờ bật.

## 3. Bằng chứng
**Test (0 đồng, model và bộ tìm là đồ giả hoặc không dùng):** `tests/test_nho_ten_goi_y.py` 15 đạt — thứ tự và lọc tên · chín loại lượt (chỉ lượt trả lời thường có trích bài riêng mới có dòng ghi chú) · cờ tắt ⇒ lịch sử y như cũ · đường chạy chuỗi của bộ đo truyền đúng dòng ghi chú. Thấy đỏ bốn cách phá. [máy kiểm] `test_b3_memory` 13 đạt và `test_api_chat` 15 đạt (có file khoá), chạy trên bản trước khi đổi chữ dòng ghi chú — đường cờ tắt không phụ thuộc chữ đó. [máy kiểm] Chụp 228 yêu cầu gửi model, nhánh so với nhánh chính cùng buổi: giống từng byte. [máy kiểm]

**Lượt thật (model thật, 19:41–19:59 19/11, mỗi bộ chạy bên cờ TẮT rồi bên cờ BẬT cùng buổi; 0 lỗi kỹ thuật):**
| Chỉ số (ngưỡng ghi trước) | Cờ TẮT | Cờ BẬT | Kết quả | Nhãn |
|---|---|---|---|---|
| **Dòng quyết** — 17 chuỗi đích hai lượt: lượt 2 nói đúng nơi lượt 1 vừa nêu (BẬT ≥ 13 / 17 và ≥ TẮT + 4) | 2 / 17 | **15 / 17** | **đạt** (tính trên cả 23 chuỗi của bộ đã khoá: 8 ⇒ 20, ngưỡng 18 — cũng đạt) | [hai người thứ hai đọc độc lập, khớp] |
| Sàn: nói chắc mà sai MỚI ở lượt hỏi tiếp (0) | (10 lượt nói sai nơi) | **0** | đạt | [người thứ hai đọc 100 %] |
| Sàn: bộ bẫy 03/11 — 6 lượt bẫy phải từ chối | 6 / 6 | **5 / 6** theo câu từ chối khuôn | **không đạt theo chữ plan** | [máy đếm; người thứ hai đọc] |
| Sàn: cờ tắt ⇒ chuỗi gửi model giống byte | — | 228 / 228 | đạt | [máy kiểm] |
| Sáu chuỗi "giống mà không phải" (lượt 2 hỏi sang nơi khác): trả lời đúng nơi mới · kéo tên nơi cũ vào | 6 / 6 · 0 | 5 / 6 · 0 | mất thật MỘT lượt (bên bật từ chối dù ngữ cảnh có câu trả lời) | [người thứ hai đọc] |
| Hai kịch bản đích của bộ 80 | một đúng · một từ chối | một đúng · một từ chối | kịch bản thứ nhất xong (bên tắt hôm nay cũng đúng nhờ tìm lại ra đúng bài); kịch bản thứ hai còn kẹt ở lỗi KHÁC: kho thiếu số điện thoại thì bỏ cả câu, dù bên bật đã tìm đúng tên nơi | [người thứ hai đọc] |
| Ba kịch bản buổi trưa xong nhờ may | hai nói sai nơi · một đúng | hai từ chối · một đúng | không tụt do cờ (bên tắt hôm nay tự hỏng); so với buổi trưa thì hai kịch bản chưa xong ở CẢ hai bên | [người thứ hai đọc] |
| Dòng ghi chú lọt ra câu trả lời / câu tìm kho · lượt đổi tuyến giữa hai bên | — | 0 / 0 · 0 | | [máy đếm; người thứ hai đọc khớp] |
| Theo kiểu lượt 2 trên 17 chuỗi: "quán đó" 9 · "đầu tiên" 3 · "thứ hai" 5 | 2 · 0 · 0 | 7 · 3 · 5 | chỉ báo | [người thứ hai đọc] |

**Ô sàn không đạt, nguyên văn sự việc:** ở một lượt bẫy (hỏi một ý kho không có về nơi vừa nêu), bên cờ tắt trả câu từ chối khuôn; bên cờ bật viết rằng tìm được địa chỉ của nơi đó nhưng không tìm thấy thông tin cho ý được hỏi, kèm trích bài của chính nơi đó. Lượt lệch nói thật phần có / không có, không mượn nơi khác (điều cái bẫy nhắm tới). Nhưng plan ghi "phải từ chối" và máy đếm theo câu khuôn ⇒ 5 / 6 ⇒ **không đạt theo chữ plan**; luật ghi trước là "phạm sàn ⇒ không bật, không vòng hai". Nhận lượt này là "từ chối đúng nghĩa" thì là diễn giải SAU khi thấy số — việc của chủ dự án.

**Tiền thật:** lượt đo 0,0966 USD (ước ghi trước ≈ 0,25; trần 0,30), chưa gồm lượt khoá bộ đích của phiên C (ghi ở hồ sơ riêng tư).

## 4. Giới hạn
- Nơi chỉ được nêu qua bài TỔNG HỢP không được nhớ (ở lượt đo buổi trưa: 11 / 34 lượt đứng trước một lượt hỏi tiếp chỉ trích bài tổng hợp). Bộ đích được soạn để lượt 1 trích bài riêng nên KHÔNG đo phần này.
- Câu hỏi tiếp theo THỨ TỰ ("chỗ đầu tiên", "quán thứ hai"): dòng ghi chú tự khai không theo thứ tự. Lượt này đúng 8 / 8 vì ở cả 8 chuỗi mọi nơi đều có bài riêng — không phải bảo đảm.
- "Nơi nào gần X nhất trong các nơi vừa nêu" không được giải (thuộc việc "gần X").
- Mỗi chuỗi MỘT lượt mỗi bên; đo qua đường chạy chuỗi của bộ đo, KHÔNG qua server ⇒ không có mục "Từ web"; test cho đường đó chỉ khoá phần nối dây bằng đồ giả.
- Người đọc tay biết bên nào bật cờ (không mù). Chỉ 4 con số bên cờ bật được đối chiếu với chữ kho.
- Hai bài tổng hợp trong thư mục di tích không mang chữ "guide" vẫn được nhớ như một nơi; tên bài đi thẳng vào dòng ghi chú, không lọc ký tự (kho hôm nay không có tên chứa ký tự phá khuôn).
- Tên nơi vào câu tìm kho ⇒ có thể vào câu tra web khi cờ câu-nối-tiếp-web bật (tên bài kho là thông tin công khai).

## 5. Cách thử 2 phút
Nhờ trợ lý gợi ý một quán hoặc một điểm đến bất kỳ có bài riêng trong kho, rồi hỏi tiếp "cho địa chỉ quán đó": địa chỉ phải là của đúng nơi vừa được nhắc ở câu trên.

## 6. Bảng "xong"
| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Code + cờ mặc định tắt | XONG (nhánh `p9-b-nho-ten-goi-y`) | từ `backend/`: `HF_HUB_OFFLINE=1 uv run pytest tests/test_nho_ten_goi_y.py -q` ⇒ `15 passed` |
| Review nhánh (phiên E) | XONG — ready, 2 điểm nhỏ ghi thành giới hạn | |
| Lượt đo cặp tắt / bật trên ba bộ | XONG | `grep -c '' data/hoi_tiep_goi_y_2026-11-19/do/dich/BAT.jsonl` ⇒ `46` |
| Đọc tay 100 % (phiên E) + cột bộ đích (phiên C) | XONG | hồ sơ riêng tư |
| Cả bộ test trên nhánh đã gộp nhánh chính (`9b13a80`, chứa main `4dbbaca`) | XONG — 55 file, mỗi file một tiến trình, có file khoá: **1.542 đạt · 0 hỏng**; tổng thời gian pytest in 567 giây (theo đồng hồ khoảng 12 phút) (mốc trước: 1.512 trên bản bật cờ lịch) [máy kiểm] | log riêng của lượt chạy; chạy lại: từ `backend/`, từng file `HF_HUB_OFFLINE=1 uv run --env-file ../.env pytest tests/<file> -q` |
| Bật cờ | Chủ dự án chọn BẬT tối 19/11 — commit bật ở nhánh bật chung ba cờ | `grep -c "nho_ten_goi_y: true" backend/config/settings.yaml` ⇒ `1` |
| Đo lại hai kịch bản đích qua server thật (có mục web) | XONG sau khi bật — mục 7 | hồ sơ riêng tư `data/hoi_tiep_goi_y_2026-11-19/do/server/ket_qua.json` |
| Mục `bai_hoc/` | XONG — `bai_hoc/VIEC_MOI_XONG.md` mục 15 | |

## 7. Sau khi bật cờ — hai kịch bản đích qua server thật, có mục "Từ web" (ghi 22:00 19/11/2026, giờ `date`)
Bản chính `b71e1e9`, cờ bật từ file cấu hình; server riêng của lượt đo (log tách khỏi lượt đo lại bộ 80 đang chạy song song); 2 kịch bản, 4 lượt, 0 lỗi kỹ thuật, **0,0044 USD**. [máy chạy; người viết code đọc — chưa có người thứ hai; mỗi kịch bản MỘT lượt]
| Kịch bản | Buổi trưa 19/11 (cờ tắt) | Sau khi bật | Kết quả |
|---|---|---|---|
| Thứ nhất: được gợi ý một quán rồi xin địa chỉ | đưa địa chỉ hai quán KHÁC | trả đúng địa chỉ của quán vừa được nhắc, trích bài của chính quán đó | **xong** |
| Thứ hai: được gợi ý một nhà hàng rồi xin địa chỉ kèm số điện thoại | phần kho từ chối; mục "Từ web" đưa địa chỉ và số của một nhà hàng KHÁC | phần kho vẫn là câu từ chối khuôn; mục "Từ web" nay nói về ĐÚNG nhà hàng vừa nhắc và tự khai chỗ đoạn trích không xác nhận | **chưa xong theo chữ kịch bản** (địa chỉ không được nêu lại) — còn kẹt ở giới hạn "kho có một phần thì bỏ cả câu", chủ dự án đã chọn ghi giới hạn; lỗi "mục web lạc sang nơi khác" hết ở lượt này |
Số điện thoại mà mục web nêu là thông tin từ web, chưa ai kiểm; mục đó vẫn mang nhãn "chưa kiểm" như mọi lượt tra web.
