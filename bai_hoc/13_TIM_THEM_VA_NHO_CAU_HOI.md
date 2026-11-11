# Bài 13 — Rút thêm thẻ và nhớ câu hỏi

*Cập nhật lần cuối: 10:30, ngày 11/11/2026 · bài mới.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Tìm thêm | công cụ **`tim_kho`** (cờ `tim_them: true`) | Model tự đặt câu tìm mới, code tìm lại trong kho, tối đa 2 lần mỗi câu. |
| Lần tìm đầu — **mới** | **`lan_tim_dau: v0`** | Lần tìm đầu tiên luôn dùng **nguyên câu hỏi gốc** của người dùng. |
| Trần lượt — **mới** | **`ASSISTANT_MAX_TURNS = 4`** | Số lượt qua lại tối đa giữa model và code cho một câu. |
| Nhớ hội thoại — **mới** | **conversation memory** (cờ `nho_hoi_thoai: true`, `nho_cau_tra_loi: false`) | Gửi kèm tối đa 3 câu hỏi trước của cùng cuộc trò chuyện. Chỉ nhớ câu hỏi, không nhớ câu trả lời. |
| Mã cuộc trò chuyện — **mới** | **cookie** (HttpOnly, 30 phút) | Một mã ngẫu nhiên trình duyệt giữ, để máy chủ biết các câu thuộc cùng một cuộc. |

---

*Bài 12 kể trợ lý có hai thứ mới: xếp loại câu và công cụ. Bài này kể hai phần trợ lý dùng nhiều nhất cho câu về Huế: **tìm thêm** khi 10 đoạn chưa đủ, và
**nhớ câu hỏi** để hiểu câu hỏi tiếp theo.*

## Quay lại người hướng dẫn viên

Khách hỏi: *"So sánh ba món chè nổi tiếng nhất Huế."* Người hướng dẫn viên rút 10 thẻ, đọc, thấy có hai món mà món thứ ba chưa có thẻ nào. Họ không trả lời
thiếu, cũng không bỏ cuộc. Họ **rút thêm thẻ**, lần này dò đúng tên món thứ ba. Có đủ rồi mới trả lời.

Rồi khách hỏi tiếp: *"Còn ăn ở đâu thì ngon?"* Câu này đứng riêng thì không hiểu "ăn" cái gì. Nhưng người hướng dẫn viên **nhớ câu khách vừa hỏi** là về chè, nên
hiểu ngay.

Trợ lý của hue_rag làm đúng hai việc đó: **rút thêm thẻ** (tìm thêm) và **nhớ câu vừa hỏi** (nhớ hội thoại).

## Phần 1: tìm thêm

**Cách chạy:**
1. **Lần tìm đầu** do code làm, luôn bằng **nguyên câu hỏi gốc** (bài 6), lấy 10 đoạn.
2. Model đọc 10 đoạn đó. Nếu thấy **chưa đủ**, nó được gọi công cụ `tim_kho` với **một câu tìm do nó tự đặt**, ví dụ chỉ tên món thứ ba.
3. Code tìm lại trong kho bằng câu đó, theo đúng đường tìm cũ (theo nghĩa, chấm từ khoá, trộn). Đoạn mới được **đánh số tiếp** (11, 12…) để không lẫn với đoạn
   cũ, rồi đưa thêm cho model.
4. Model được tìm thêm **tối đa 2 lần**. Lần thứ 3 nhận câu "đã hết lượt tìm". Cả câu có trần **4 lượt** qua lại. Chạm trần thì trả câu từ chối cố định, không
   bao giờ lặp vô hạn.

**Vì sao lần tìm đầu dùng câu gốc, không để model viết lại câu tìm?** Đã thử (B2a): để model viết lại câu tìm cho lần đầu. Kết quả không qua luật ghi trước,
nên giữ câu gốc. Câu gốc của người dùng là thứ chắc chắn nhất. Model chỉ được đặt câu tìm khi **đã thấy** 10 đoạn đầu thiếu gì.

**Kết quả (03/11):**

| Đo gì | Trước tìm thêm | Sau tìm thêm | Nghĩa là |
|---|---|---|---|
| Từ chối nhầm (158 câu) | 12 | **4 và 6** (hai lượt) | giảm khoảng một nửa tới hai phần ba |
| Đủ ý, 18 câu nhiều nguồn | — | **+1,17** điểm [+0,44; +2,00] | tăng rất rõ đúng ở loại câu yếu nhất; khoảng tin cậy không chứa 0 |
| Bộ an toàn | — | 1 câu sai điều kiện kiểu mới | trong mức cho phép (tối đa 2 cho cả Phase) |
| Tiền | — | khoảng 0,00031 USD / câu lúc đó | vẫn dưới trần |

Đây là cách chữa **chỗ nghẽn xếp hạng** (bài 6, 7) mà không cần model xếp lại: thay vì xếp lại 30 đoạn cho đúng, để model **tự hỏi lại đúng cái nó còn thiếu**.

## Phần 2: nhớ câu hỏi

**Cách chạy:**
- Mỗi cuộc trò chuyện có **một mã ngẫu nhiên** trong cookie của trình duyệt. Trang web không đọc được mã này, nó hết hạn sau **30 phút** không hỏi.
- Máy chủ giữ trong **bộ nhớ (RAM)**, không ghi ra ổ đĩa, tối đa **3 lượt gần nhất** của mỗi cuộc (không quá 1.500 token), tối đa 500 cuộc cùng lúc. Khởi động
  lại máy chủ là mất hết. Bấm "Cuộc trò chuyện mới" là xoá ngay.
- Mỗi câu hỏi mới được gửi kèm **3 câu hỏi trước**, **chỉ câu hỏi, không kèm câu trả lời cũ**.
- Khi có câu hỏi trước, lời dặn có thêm một đoạn hẹp: lịch sử chỉ để **hiểu câu hỏi đang nói về đối tượng nào**; mỗi ý vẫn phải lấy từ bằng chứng nói
  đúng về đối tượng đó, **không gán thông tin của đối tượng khác**. Câu tìm thêm phải nêu đúng tên đối tượng lấy từ các câu trước.

**Vì sao chỉ nhớ câu hỏi mà không nhớ câu trả lời?** Nhớ cả câu trả lời nghe tự nhiên hơn, nhưng thử ra thì có rủi ro:
- **Lượt chạy bộ câu kín** của bản nhớ cả câu trả lời bắt được một câu nguy hiểm. Câu hỏi tiếp theo mang một tiền đề sai, và chatbot **mượn đoạn của một đối
  tượng khác** từ câu trả lời trước để trả lời. Vì vậy cờ nhớ chưa được bật.
- Sửa lời dặn rồi đo lại bản vẫn nhớ câu trả lời: điểm câu hỏi tiếp theo tăng +0,50, nhưng khoảng tin cậy [−0,15; +1,20] **chứa 0**, tức chưa chắc có lợi. Theo
  đúng hướng đã ghi trước cho trường hợp này, mình chọn **chỉ nhớ câu hỏi**.
- Có thêm một lý do kỹ thuật: số nguồn `[n]` được đánh lại mỗi lượt. Nhớ câu trả lời cũ kèm `[3]` sẽ làm lẫn `[3]` cũ với `[3]` mới.

**Kết quả của bản chỉ nhớ câu hỏi (03/11):**

| Đo gì | Kết quả | Nghĩa là |
|---|---|---|
| Điểm câu hỏi tiếp theo | **+0,80** [+0,25; +1,50] | tăng rõ, khoảng tin cậy không chứa 0 |
| Câu bẫy (câu hỏi tiếp có tiền đề sai) | từ chối đúng **6 / 6** (không có nhớ: 3 / 6) | nhớ câu hỏi còn giúp **từ chối đúng hơn** |
| Từ chối nhầm ở câu hỏi tiếp | **0 / 19** (không có nhớ: 5 / 19) | hiểu được câu hỏi tiếp, không từ chối oan |

Bật từ tối 03/11. Hồ sơ đợt đó cũng tự ghi rõ một giới hạn: chưa chứng minh được "chỉ nhớ câu hỏi" **tốt hơn** "nhớ cả câu trả lời". Chỉ biết bản chỉ nhớ câu
hỏi **qua được luật**, còn bản kia thì chưa.

## Một chuyện thật: thử tắt "lưu tạm" để tiết kiệm, hoá ra lại đắt hơn

OpenAI có cơ chế **lưu tạm** phần đầu chuỗi gửi đi (lời dặn, công cụ). Lần gọi sau trong vòng 30 phút đọc lại phần đó với giá rẻ hơn 10 lần, nhưng lần ghi đầu
thì đắt hơn. Ngày 05/11 có ý tưởng: tắt lưu tạm cho đỡ tiền ghi.

Đo trên log thật: **45 % số câu gọi model từ 2 lần trở lên** (vì có tìm thêm và công cụ), và các lần sau **đọc lại** được phần đã lưu. Tắt lưu tạm thì các lần đó
phải trả giá đầy đủ, nên **tổng tiền tăng**. Ý tưởng bị bỏ. Bài học: phần trợ lý làm thay đổi cả cách tính tiền. **Đo trên log của hệ thống đang chạy** rồi mới
quyết, không quyết theo số đo của bản cũ.

## Khi nào hỏng

- **Không nhớ câu trả lời.** Câu kiểu *"quán thứ hai bạn vừa kể mở mấy giờ?"* chatbot **chưa hiểu được**, vì nó không biết lần trước đã kể những quán nào. Đây
  là giới hạn đã chọn, chưa đo riêng.
- **Cookie hết hạn sau 30 phút**, hoặc máy chủ khởi động lại ⇒ chatbot âm thầm sang cuộc mới, quên các câu trước.
- **Bộ câu bẫy nhỏ** (6 câu) ⇒ kết quả "6 / 6" là tín hiệu tốt nhưng chưa phải bằng chứng mạnh.
- **Tìm thêm làm câu chậm hơn và tốn hơn** ở những câu model quyết định tìm. Trên 158 câu vẫn trong mức cho phép, nhưng câu nhiều nguồn chậm hơn câu thường.
- **Model có thể không tìm thêm khi nên tìm**: nó tự quyết, không có luật bắt buộc. Từ chối nhầm còn 4–6 câu là phần nó chưa tự cứu được.

## Ba điều chính

1. **Tìm thêm:** lần đầu luôn tìm bằng câu gốc; model thấy thiếu thì **tự đặt câu tìm**, tối đa 2 lần. Từ chối nhầm **12 → 4–6**, câu nhiều nguồn **+1,17** điểm đủ ý.
2. **Nhớ câu hỏi:** gửi kèm **3 câu hỏi trước** (không kèm câu trả lời), giữ trong RAM 30 phút. Câu hỏi tiếp **+0,80**, từ chối nhầm ở câu hỏi tiếp **5 / 19 → 0 / 19**.
3. Không nhớ câu trả lời vì bản nhớ cả câu trả lời từng **mượn nhầm đoạn của đối tượng khác**, và đo lại chưa chắc có lợi. Giới hạn: chưa hiểu được "quán thứ
   hai bạn vừa kể".

**Bài sau:** Bài 14 — Việc dễ nhầm thì code làm: ngày âm lịch, dự báo thời tiết, và biểu mẫu lên lịch trình.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- `MODEL_SEARCH_LIMIT = 2`, hết lượt ⇒ câu "hết lượt": `backend/llm/assistant.py`; `ASSISTANT_MAX_TURNS = 4`: `backend/llm/generator_openai_full_corpus.py`; chạm trần ⇒ từ chối cố định: `assistant.py` `_finish_generated` [code]
- Cờ `tim_them`, `lan_tim_dau: v0`, `nho_hoi_thoai: true`, `nho_cau_tra_loi: false`: `backend/config/settings.yaml` [code, xem 11/11]
- Đánh số tiếp đoạn mới: `backend/retrieval/full_corpus_context.py` `build` (`first_id`) [code]
- Từ chối nhầm 12 → 4 / 6; 18 câu nhiều nguồn +1,17 [+0,44; +2,00]; 1 câu an toàn sai mới; B2a giữ câu gốc: `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `report_agent/2026-11-02_phase_9_code/b134_b2_implementation.md` (03/11) [đã chạy]; khoảng 0,00031 USD / câu: `session_prompt/Project_Status.md` §4 [đã chạy]
- Đoạn dặn khi có lịch sử: `backend/llm/full_corpus_prompt.py` `ASSISTANT_HISTORY_NOTE` [code, xem 11/11]
- Bộ nhớ RAM, cookie HttpOnly 30 phút, 500 cuộc, 3 lượt, 1.500 token, không ghi đĩa; cắt `[n]` khỏi câu trả lời được nhớ: `backend/api/conversations.py` [code]
- Lượt kín B3 (K-N2) mượn đoạn của đối tượng khác; vòng 1 B3b +0,50 [−0,15; +1,20] ⇒ chọn (a); bản (a): +0,80 [+0,25; +1,50], bẫy 6 / 6 ↔ 3 / 6, từ chối nhầm 0 / 19 ↔ 5 / 19; hồ sơ tự ghi "không kết luận được (a) tốt hơn": `07_…`, `report_agent/2026-11-02_phase_9_code/b138_*` [đã chạy]
- Lưu tạm: 45 % lượt gọi model ≥ 2 lần, tắt lưu tạm đắt hơn (05/11): `07_…` [đã chạy]
- "So sánh ba món chè", "quán thứ hai bạn vừa kể" là câu tự đặt.

</details>
