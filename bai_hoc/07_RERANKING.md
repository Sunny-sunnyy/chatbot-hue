# Bài 7 — Xếp lại thẻ: reranking (đã thử, không dùng)

*Cập nhật lần cuối: 10:22, ngày 11/11/2026 · bài mới.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Xếp lại | **reranking** (trong code: `reranker: none`) | Sau khi tìm, dùng một model khác đọc kỹ từng cặp "câu hỏi – đoạn" rồi xếp lại thứ hạng. |
| Model xếp lại — **mới** | **cross-encoder** (`BAAI/bge-reranker-v2-m3`, `AITeamVN/Vietnamese_Reranker`) | Model nhỏ đọc câu hỏi và đoạn **cùng lúc**, cho điểm "đoạn này có trả lời câu hỏi không". |
| Để người viết tự xếp — **mới** | **listwise rerank** bằng **gpt-6-luna** | Đưa cả danh sách đoạn cho model lớn, nhờ nó chọn ra những đoạn tốt nhất. |
| Card đồ hoạ — **mới** | **GPU** (GTX 1650, 4 GB) | Phần cứng chạy model nhanh hơn CPU; máy anh có một card nhỏ. |
| Thứ hạng trung bình | **MRR@10** | Đoạn đúng đứng hạng 1 được 1 điểm, hạng 2 được 1/2… (đã gặp ở bài 6). |

---

*Bài 6 kể chỗ nghẽn của bước tìm là xếp hạng: đáp án đã được lấy về nhưng nằm ở hạng 11–30. Cách chữa "sách giáo khoa" cho chỗ này là xếp lại (reranking).
Bài này kể mình đã thử ba cách xếp lại, và vì sao chatbot hiện **không dùng** cách nào.*

## Quay lại người hướng dẫn viên

Rút ra 30 thẻ xong, người hướng dẫn viên có thể làm thêm một việc: **đọc kỹ từng thẻ một**, đặt cạnh câu hỏi của khách, rồi tự hỏi "thẻ này có thật sự trả lời
câu hỏi không?". Việc này chậm hơn nhiều so với nhìn lướt theo ý hay dò theo chữ, nhưng chính xác hơn. Rồi họ xếp lại 30 thẻ theo kết quả đọc kỹ đó, và lấy
10 thẻ đầu.

Nghe rất hợp lý. Nhưng có một cái bẫy. Xếp lại cho **thẻ tốt nhất lên đầu** chưa chắc giúp được câu trả lời, nếu câu hỏi cần **nhiều thẻ khác nhau** và cách xếp
mới lại đẩy mất một trong số đó ra khỏi 10 thẻ. Chuyện thật của bài này chính là cái bẫy đó.

## Reranking là gì

Ở bước tìm (bài 6), vector câu hỏi và vector đoạn được tính **riêng rẽ**, rồi so với nhau. Cách này nhanh, nhưng model chưa bao giờ "đọc" câu hỏi và đoạn cùng lúc.

Một **model xếp lại** (cross-encoder) thì đưa **cả câu hỏi lẫn đoạn vào cùng một lần đọc**, rồi cho một điểm "liên quan tới đâu". Đọc chung thì hiểu sát hơn,
nhưng phải đọc từng cặp một: 30 ứng viên là 30 lần đọc. Vì vậy reranking chỉ chạy trên vài chục ứng viên, không chạy trên cả kho.

Có hai kiểu xếp lại, và mình đã thử cả hai:
- **model xếp lại nhỏ**, chạy trên card đồ hoạ của máy anh;
- **để chính gpt-6-luna xếp**: đưa danh sách đoạn, nhờ nó chọn ra những đoạn tốt nhất.

## Lần thử 1: hai model xếp lại chạy trên máy (25/10)

Hai model được thử, đều chạy trên card đồ hoạ GTX 1650 của máy anh:
- **bge-reranker-v2-m3**: model xếp lại đa ngôn ngữ phổ biến;
- **Vietnamese_Reranker**: model xếp lại huấn luyện riêng cho tiếng Việt.

Mỗi model thử hai kiểu: đọc đoạn trơn, và đọc đoạn kèm tên mục. Lúc đó chatbot còn đưa **5 đoạn** cho người viết.

Kết quả:
- bge với đoạn trơn **xếp đúng hơn rõ**: MRR tăng khoảng +0,1. Nhưng ở 1 câu, nó đẩy đoạn đúng ra khỏi 5 đoạn đưa người viết.
- Ba bản còn lại mỗi bản làm mất đoạn đúng ở **3 câu**.
- Luật là không được làm mất câu nào ⇒ **cả bốn bản đều bị loại**.
- Thử thêm: lấy 100 ứng viên rồi để model xếp lại chọn 10. So với lấy 100 mà không xếp lại thì **không khác**. Phần lợi (nếu có) đến từ lấy rộng, không đến từ
  việc xếp lại.
- Tốc độ: khoảng 1 giây cho 10 đoạn; 11–14 giây cho 100 ứng viên. Với yêu cầu chữ đầu tiên dưới 3 giây, cách lấy 100 ứng viên không thể dùng.

## Lần thử 2: để gpt-6-luna tự chọn đoạn (25/10 và 27/10)

Đầu tiên (25/10), luna xếp lại 10 đoạn: MRR tăng **+0,17**, 0 câu mất. Tốt, nhưng bộ thử chỉ có tối đa 3 câu có thể "cứu" được, nên kết quả để "chưa rõ".

Sau đó (27/10) thử bản mạnh hơn: luna **chọn 10 đoạn trong 30 ứng viên**. Bản này được đo đầy đủ cả hai tầng, đúng như cách đánh giá hai giai đoạn:

| Tầng | Kết quả | Nghĩa là |
|---|---|---|
| Bước tìm | câu có đủ đoạn đúng trong phần đưa người viết: **22 → 31 / 40**; nhóm kiểm 7 → 10 / 15; 0 câu mất | **tốt hơn hẳn**: gần như chữa đúng chỗ nghẽn xếp hạng |
| Câu trả lời (trung bình) | đủ ý +0,22, đúng +0,25, từ chối nhầm 7 → 2 (trên 88 câu) | trung bình cũng tốt lên |
| Câu trả lời (từng câu) | **5 câu tụt điểm đủ ý**, trong khi luật chỉ cho tối đa 4 | **vỡ luật** ⇒ không nhận |
| Tốc độ cả câu | trung vị **6,5 s**, câu chậm **9,1 s** (riêng bước chọn đoạn 4,6 / 6,9 s) | chậm gấp đôi mức cho phép |
| Tiền | khoảng **3,8 lần** | đắt gần gấp 4 |

Ngày 27/10 anh chốt **gác lại** bản này. Hai bản khác cùng ý tưởng (luna xếp đủ 30, luna không suy luận) thì hỏng vì model trả sai định dạng.

## Vì sao "xếp đúng hơn" mà câu trả lời vẫn có thể tệ đi

Đây là điều đáng nhớ nhất của bài:

- **Thước của bước tìm và thước của câu trả lời không phải một.** MRR thưởng cho việc đưa **một** đoạn đúng lên đầu. Câu trả lời tốt lại cần **đủ mọi mảnh**.
  Câu nhiều nguồn cần 3–4 đoạn khác nhau cùng có mặt. Model xếp lại có thể đẩy đoạn tốt nhất lên đầu nhưng làm rơi mảnh thứ ba ra khỏi danh sách.
- **Trung bình tốt lên vẫn có thể giấu vài câu tệ đi.** K3b-m tốt hơn ở trung bình, nhưng 5 câu bị tụt. Luật "không làm hỏng" được đặt ra để bắt đúng chuyện
  này: người dùng gặp câu bị tụt, chứ không gặp con số trung bình.
- **Tốc độ và tiền là giới hạn thật.** Một bước chọn đoạn mất 4–7 giây thì đẩy cả câu vượt mức chờ cho phép, dù chất lượng có tốt.

Vì vậy chatbot đi đường khác để chữa chỗ nghẽn xếp hạng: **đưa 10 đoạn thay vì 5** (bài 6), và cho trợ lý **tìm thêm** khi thiếu (bài 13). Cả hai đều rẻ, nhanh,
và đã đo là giúp.

## Khi nào nên xét lại

- Các lần thử trên đều làm khi chatbot còn đưa 5 đoạn, hoặc trên kho cũ. Với 10 đoạn như bây giờ, model xếp lại chạy trên máy có thể không còn làm rơi đoạn
  đúng. **Chưa đo lại.**
- Nếu chạy trên máy mạnh hơn (ví dụ khi đưa lên máy chủ có card đồ hoạ tốt), thời gian xếp lại sẽ khác.
- Nếu có một bản gpt-6-luna chọn đoạn đủ nhanh để vừa mức chờ cho phép, thì K3b-m đáng thử lại, vì tầng tìm của nó tốt hơn hẳn.

## Ba điều chính

1. Chatbot hiện **không xếp lại** (`reranker: none`). Đã thử **ba cách**: hai model xếp lại chạy trên máy, và để gpt-6-luna tự chọn đoạn.
2. Model xếp lại trên máy **làm mất đoạn đúng ở 1–3 câu**. Luna chọn đoạn **chữa gần đúng chỗ nghẽn** (22 → 31 / 40) nhưng **5 câu tụt**, **chậm gấp đôi**, **đắt
   gần gấp 4**, nên gác lại.
3. Bài học: **xếp đúng hơn chưa chắc trả lời tốt hơn**. Câu trả lời cần đủ mọi mảnh, nên chatbot chọn đưa 10 đoạn và cho tìm thêm.

**Bài sau:** Bài 8 — Đọc thẻ rồi trả lời (generation): lời dặn cho người viết, ghi nguồn, câu từ chối cố định, code kiểm nguồn, và chữ hiện dần trên trang.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- `reranker: none`: `backend/config/settings.yaml`; lớp xếp lại chỉ còn cho bộ thử: `backend/reranking/cross_encoder.py` [code]
- Lần thử G4 (25/10, GTX 1650, 5 đoạn): bge đoạn trơn MRR@10 +0,105, mất 1 câu; ba bản còn lại mất 3 câu mỗi bản; lấy 100 rồi xếp lại = không khác so với lấy 100; khoảng 0,85 / 1,19 s cho 10 đoạn, 11–14 s cho khoảng 100 ứng viên: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ T3-08, `06_BAO_CAO_TIM_KIEM.md` [đã chạy]
- Luna xếp lại 10 đoạn (25/10): MRR@10 +0,172 [+0,092; +0,261], 0 câu mất, "chưa rõ": 91 thẻ T3-09 [đã chạy]
- K3b-m (27/10): 22 → 31 / 40 (nhãn bản 1; bản 2 là 24 → 33), nhóm kiểm 7 → 10 / 15; Đủ +0,216, Đúng +0,250, từ chối nhầm 7 → 2 / 88; 5 câu tụt Đủ, vượt mức 4; p50 6,5 / p95 9,1 s (gọi đồng thời 4); khoảng 3,8 lần tiền; User gác 27/10: 91 thẻ T3-09, `06_BAO_CAO_TIM_KIEM.md` §4, `session_prompt/Project_Status.md` §2 [đã chạy]
- Lưu ý thứ tự: lúc gác K3b-m, lý do chính là luật "số câu tụt"; mức chờ 3 / 5 giây được anh chốt sau đó (28/10).
- "Khi nào nên xét lại" là suy ra từ báo cáo, chưa đo.

</details>
