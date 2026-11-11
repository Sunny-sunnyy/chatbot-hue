# Bài 12 — Từ chatbot thành trợ lý: xếp loại câu và công cụ

*Cập nhật lần cuối: 10:29, ngày 11/11/2026 · bài mới; mở đầu Phần 3 (trợ lý).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Trợ lý | **agent** | Chatbot biết tự quyết lúc nào nhờ code làm việc (đã gặp ở bài 0). |
| Bộ dựng trợ lý — **mới** | **OpenAI Agents SDK** (bản 0.19.4) | Thư viện lo phần "model gọi công cụ → code chạy → trả kết quả cho model → model viết tiếp". |
| Xếp loại câu | **router** / định tuyến (trong code: `_pick_route`) | Một lần gọi model ngắn để xếp câu hỏi vào 4 loại (đã gặp ở bài 0). |
| Bốn loại — **mới** | `tro_chuyen` · `tro_ly_hue` · `ngoai_pham_vi` · `khan_cap` | Chào hỏi · về Huế · ngoài chủ đề · khẩn cấp. |
| Công cụ | **tool** | Một việc code làm khi model yêu cầu: tìm thêm trong kho, tính ngày, lấy dự báo (đã gặp ở bài 0). |
| Chạy song song — **mới** | **`song_song_tra_loi`** | Bắt đầu tìm và viết câu trả lời về Huế ngay trong lúc đang xếp loại câu, để đỡ chờ. |
| Câu ngoài chủ đề cố định — **mới** | `OUT_OF_SCOPE_ANSWER` | "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" |

---

*Phần 1 kể chatbot hỏi đáp từ kho (RAG). Phần 2 kể nó được chấm ra sao. Phần 3 kể bước nâng cấp lớn nhất của đồ án: biến chatbot thành **trợ lý**. Bài này
kể vì sao cần, và hai thứ làm nên trợ lý: **xếp loại câu** và **công cụ**.*

## Quay lại người hướng dẫn viên

Người hướng dẫn viên ở Phần 1 chỉ biết một việc: nghe câu hỏi → lật sổ → đọc thẻ → trả lời. Ngoài đời, khách hỏi đủ thứ:
- *"Chào bạn!"* thì không cần lật sổ, chào lại là xong;
- *"Giá vàng hôm nay bao nhiêu?"* thì không phải chuyện Huế, lịch sự từ chối là đủ;
- *"Hôm nay âm lịch là ngày mấy?"* thì sổ không có, nhưng **mở lịch** ra là biết;
- *"Mai Huế có mưa không?"* thì sổ không có, nhưng **xem dự báo** là biết;
- *"So sánh ba món chè nổi tiếng"* thì 10 thẻ đầu chưa đủ, phải **rút thêm thẻ**.

Một hướng dẫn viên giỏi làm hai việc mà người ở Phần 1 không làm:
1. **nghe xem khách hỏi loại gì** rồi mới chọn cách xử lý;
2. **biết dùng dụng cụ**: cuốn lịch, điện thoại xem dự báo, hộp thẻ để rút thêm. Họ tự quyết lúc nào cần dụng cụ nào, nhưng **con số thì đọc từ dụng cụ**,
   không tự nhẩm.

Trợ lý của hue_rag là người hướng dẫn viên thứ hai này.

## Vì sao cần trợ lý (lý do của Phase 9)

Sau Phase 8, chatbot hỏi đáp từ kho đã khá tốt (Phần 2). Nhưng còn những chỗ RAG đơn thuần không làm được:
- **câu cần ghép nhiều nguồn** chỉ được 3,50 điểm đủ ý, vì 10 đoạn đầu không chứa đủ mảnh;
- **câu có ngày tháng** ("cuối tuần này", "rằm tháng Giêng năm nay") cần biết hôm nay là ngày nào và đổi âm ↔ dương lịch. Kho không có, model hay tính sai;
- **câu thời tiết, câu kho không có** cần thông tin bên ngoài, có kiểm;
- **câu chào hỏi, câu ngoài chủ đề** đi qua cả bước tìm và viết, vừa tốn tiền vừa trả lời gượng.

Anh nói lúc mở Phase 9: *"lên trợ lý mà không khác RAG mức 1 thì cần gì trợ lý"*. Nên Phase 9 làm trợ lý có công cụ thật, mỗi công cụ chữa đúng một chỗ ở trên.

## Thứ nhất: xếp loại câu (định tuyến)

Mỗi câu hỏi trước hết qua **một lần gọi gpt-6-luna rất ngắn**. Lời dặn riêng cho bước này bảo model chọn đúng một trong bốn loại:

| Loại | Ví dụ kiểu câu | Xử lý tiếp |
|---|---|---|
| **chào hỏi** (`tro_chuyen`) | "Chào bạn", "Cảm ơn nhé", "Bạn là ai?" | model đáp ngắn, không tìm kho, không ghi nguồn |
| **về Huế** (`tro_ly_hue`) | mọi câu về món ăn, di tích, lễ hội, đi lại ở Huế; cả câu chỉ hỏi về ngày tháng (âm ↔ dương, thứ mấy, lễ Tết ngày nào) | đi đường trợ lý đầy đủ: tìm kho, công cụ, viết, kiểm nguồn |
| **ngoài chủ đề** (`ngoai_pham_vi`) | giá vàng, xổ số, lập trình, nơi khác | trả **câu cố định**, không gọi thêm model |
| **khẩn cấp** (`khan_cap`) | vừa bị cướp, tai nạn, ốm nặng ở Huế | đi **đúng đường câu về Huế**, chỉ đánh dấu riêng trong nhật ký |

Vài chi tiết quan trọng:
- **Lỗi hoặc quá 10 giây ⇒ coi là câu về Huế.** Thà đi đường đầy đủ (vẫn có mọi rào chắn) còn hơn lỡ từ chối một câu quan trọng.
- **Câu khẩn cấp không có câu trả lời soạn sẵn.** Trước đây có một câu soạn sẵn kèm số điện thoại khẩn cấp. Ngày 09/11 câu soạn sẵn được bỏ: câu khẩn cấp đi
  đường câu về Huế, trả lời từ kho như mọi câu khác (kho không có thì từ chối rồi mở tra web, bài 15).
- **Chính xác tới đâu:** đúng **253 / 253** câu đã thấy và **20 / 20** câu kín (02/11). Chi phí thời gian khoảng 1,5 giây mỗi câu.

## Đỡ chờ: chạy song song

Xếp loại mất khoảng 1,5 giây. Nếu chờ xếp xong mới bắt đầu tìm và viết, câu về Huế chậm thêm đúng chừng đó. Nên trợ lý **bắt đầu luôn phần "về Huế"** (tìm +
viết) cùng lúc với bước xếp loại:
- xếp ra **về Huế** ⇒ phần đã chạy được giữ, người dùng thấy chữ sớm hơn;
- xếp ra **loại khác** ⇒ phần đã chạy bị **huỷ**, người dùng không thấy chữ nào của nó. Phần chạy song song cũng **không được tra web**; cổng web chỉ mở sau khi
  chắc chắn là câu về Huế.

Đo (04/11): chữ đầu tiên của câu về Huế nhanh hơn **1,37 giây**, khoảng tin cậy [0,34; 2,14] không chứa 0, nên chênh lệch là thật. 15 / 20 cặp nhanh hơn. 90
lượt chạy bộ an toàn: 0 vi phạm. Đổi lại, câu **không** về Huế tốn thêm khoảng 0,00023 USD cho phần bị huỷ. Bật từ 05/11.

## Thứ hai: công cụ

Ở đường "về Huế", trợ lý không chỉ đọc 10 đoạn rồi viết. Trong lúc viết, model **được phép yêu cầu** code làm vài việc. Mỗi việc là một **công cụ** có tên, có
mô tả, có tham số rõ ràng:

| Công cụ | Model yêu cầu khi | Code làm gì | Bài |
|---|---|---|---|
| `tim_kho` (tìm thêm) | 10 đoạn đầu chưa đủ | tìm lại trong kho bằng câu tìm model tự đặt; tối đa 2 lần | 13 |
| `ngay_lich` | cần đổi một ngày chưa có sẵn | tính ngày, đổi âm ↔ dương lịch | 14 |
| `thoi_tiet` | câu hỏi về thời tiết | lấy dự báo Huế từ Open-Meteo | 14 |

Ngoài ra có hai phần **code tự làm, không chờ model yêu cầu**: tính sẵn lịch khi câu có từ chỉ ngày (bài 14), và tra web khi kho không có (bài 15).

**Nguyên tắc chia việc giữa code và model.** Đây là nguyên tắc quan trọng nhất của Phase 9:
- **phép tính, luật tiền, trường bắt buộc, thứ tự bắt buộc ⇒ code làm**;
- model chỉ **chọn** lúc nào cần công cụ, và **diễn đạt** kết quả thành câu.

Lý do: những lần chỉ **dặn** model "đừng tự tính", "đừng cộng tổng" đều không đủ. Có lần dặn rõ "không cộng tổng tiền" mà model vẫn tự viết dòng "Tổng". Bài 14 kể kỹ.

**Công cụ chỉ đưa khi cần.** Mỗi công cụ thêm vào làm lời dặn dài ra và có thể đổi cách model trả lời cả những câu không liên quan. Nên code chỉ đưa công cụ
ngày khi câu có từ chỉ ngày, chỉ đưa công cụ thời tiết khi câu có từ thời tiết.

**Bộ dựng trợ lý.** Phần "model yêu cầu công cụ → code chạy → trả kết quả → model viết tiếp" do thư viện **OpenAI Agents SDK** lo. Mỗi câu có trần **4 lượt**
qua lại giữa model và code, để không bao giờ lặp vô hạn. Chạm trần thì trả câu từ chối cố định.

## Một chuyện thật: câu khẩn cấp đi nhầm đường

Ngày 03/11, thử một câu kiểu *"vừa bị giật túi xách ở Huế, phải làm sao"*. Bước xếp loại lúc đó xếp nó vào **ngoài chủ đề**, nên người dùng chỉ nhận câu từ chối
cố định, không có số điện thoại công an hay chỗ cần tới. Lỗ hổng có từ khi bước xếp loại ra đời, nhưng 10 câu khẩn cấp tự viết lúc đó **chưa từng được đưa vào
bộ đo**, nên không ai thấy.

Sửa ngay trong tối đó: lời dặn xếp loại thêm loại "vừa bị cướp, giật, trộm, hành hung cần báo công an" vào nhóm khẩn cấp. (Về sau, ngày 09/11, câu
khẩn cấp được chuyển hẳn sang đường câu về Huế như kể ở trên.) Bài học có hai
phần: **loại lỗi tệ nhất (an toàn) phải có trong bộ đo ngay từ đầu**, và **lỗi của bước xếp loại thì hỏng cả câu**, vì câu bị gửi sai đường thì phía sau làm tốt
mấy cũng vô ích.

Hai thử nghiệm tốc độ ở bước xếp loại đã bị bỏ:
- **tắt suy luận** của model ở bước xếp loại (04/11): nhanh hơn khoảng 0,2–0,35 giây, rẻ hơn 16 %, nhưng **2 câu an toàn về Huế bị xếp ngoài chủ đề** ⇒ bỏ;
- **chạy song song cho câu chào hỏi** (10/11): câu chậm vẫn 5,74 giây, vượt mức 5 giây, và câu ngoài chủ đề tốn 0,00056 USD, vượt trần ⇒ bỏ, giữ làm hồ sơ.

## Khi nào hỏng

- **Xếp loại có thể dao động.** Đã thấy 2 câu đổi loại giữa hai lần chạy dù chuỗi gửi đi giống hệt từng byte.
- **Xếp loại quá 10 giây đúng vào câu khẩn cấp** thì câu đi đường thường. Đã gặp 1 / 246 lần. Đường thường vẫn trả lời từ kho, nhưng không được đánh dấu khẩn cấp.
- **Câu ngoài chủ đề bị xếp nhầm là khẩn cấp** (ví dụ câu y tế không liên quan Huế) thì trợ lý từ chối rồi mở tra web. Anh đã nhận giới hạn này.
- **Chạy song song gửi đoạn kho sang OpenAI cả với câu ngoài chủ đề**, vì phần "về Huế" đã bắt đầu trước khi biết loại. Chỉ là đoạn kho công khai, nhưng nên biết.
- **Câu chào hỏi vẫn chậm** ở câu chậm (7,73 giây, vượt mức 5 giây).

## Ba điều chính

1. Trợ lý = **xếp loại câu** (4 loại, một lần gọi model ngắn) + **công cụ** (tìm thêm, ngày, thời tiết) + phần **code tự làm** (lịch tính sẵn, tra web).
2. **Phép tính, luật tiền, thứ tự bắt buộc thì code làm; model chỉ chọn và diễn đạt.** Công cụ chỉ đưa khi code thấy đúng loại câu.
3. Bước xếp loại đúng 253 / 253 câu đã thấy. **Chạy song song** làm chữ đầu nhanh hơn 1,37 giây. Chuyện thật: câu khẩn cấp từng đi nhầm đường, vì loại câu đó
   chưa có trong bộ đo.

**Bài sau:** Bài 13 — Rút thêm thẻ và nhớ câu hỏi: hai thứ đã giảm từ chối nhầm từ 12 xuống 4–6 và giúp hỏi tiếp trong một cuộc trò chuyện.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- OpenAI Agents SDK 0.19.4: `uv.lock` [code, xem 11/11]
- Xếp loại 4 tuyến; `khan_cap` đi `tro_ly_hue` (log `emergency_by="router"`); lỗi / quá 10 s ⇒ `tro_ly_hue`: `backend/llm/assistant.py` `_pick_route`; `backend/config/settings.yaml` `router_timeout_seconds: 10` [code, xem 11/11]
- Câu ngoài chủ đề cố định: `backend/llm/full_corpus_prompt.py` `OUT_OF_SCOPE_ANSWER` [code, xem 11/11]; câu chỉ hỏi ngày tháng ⇒ về Huế (10/11): lời dặn định tuyến trong cùng file [code]
- 253 / 253 câu đã thấy, 20 / 20 câu kín (02/11); khoảng 1,5 s: `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `session_prompt/Project_Status.md` §4 [đã chạy; con số token "~580 vào" của Project_Status chưa xác minh lại được nên không đưa vào bài]
- Chạy song song: `answer_turn_stream_parallel` trong `assistant.py`; cờ `song_song_tra_loi: true`; −1,37 s [0,34; 2,14], 15 / 20 cặp, 90 lượt an toàn 0 vi phạm, +0,00023 USD câu không về Huế (đo 04/11, bật 05/11): `07_…` [code + đã chạy]
- Công cụ `tim_kho` (≤ 2 lần), `ngay_lich`, `thoi_tiet`; trần 4 lượt: `assistant.py` (`MODEL_SEARCH_LIMIT`), `backend/llm/generator_openai_full_corpus.py` (`ASSISTANT_MAX_TURNS`) [code]
- Bỏ câu khẩn cấp soạn sẵn (09/11): `session_prompt/Project_Status.md` §4 [đã chạy]
- Câu "bị giật túi" đi nhầm (03/11) và sửa: `07_…`, `Project_Status.md` §4 (B143) [đã chạy]
- Tắt suy luận ở xếp loại (04/11, hồ sơ `hoso/p9-toc-do-1`); xã giao song song (10/11, p95 5,74 s, 0,00056 USD, hồ sơ `hoso/p9-xa-giao-song-song`): `07_…`, nhật ký 10/11 [đã chạy]
- Dao động 2 câu đổi tuyến; 1 / 246 lần quá giờ: `07_…` [đã chạy]
- Câu anh nói khi mở Phase 9: `session_prompt/Project_Status.md` §5 (02/11)
- Các câu ví dụ là câu tự đặt.

</details>
