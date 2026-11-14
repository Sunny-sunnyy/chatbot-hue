# Bài 22 — Viết thêm vào sổ tay mà không làm hỏng trang cũ: hai lần ghi kho ngày 14/11

*Cập nhật lần cuối: 13:40, ngày 14/11/2026 · bài mới; đã sửa theo một lượt kiểm độc lập (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Ghi kho | (không có tên riêng; thư mục làm việc `data/sua_kho_…`) | Thêm bài hoặc sửa chữ trong kho, rồi dựng lại chỉ mục để chatbot tìm được chữ mới. |
| Đo trước ↔ sau — **mới** | **before / after** (paired comparison) | Chạy cùng bộ câu trên kho cũ và kho mới, cùng code, rồi so từng câu một. |
| Tiêu chí ghi trước | **pre-registered criteria** | Mức đạt viết ra **trước** khi xem kết quả, để không "dời cột gôn" sau khi thấy số. |
| Nhiễu sinh câu — **mới** | **generation noise** | Cùng một câu, cùng ngữ cảnh, model vẫn có lúc trả lời, có lúc từ chối. Khác biệt kiểu này không do kho. |
| Dòng "có thể đã thay đổi" | **may-have-changed notice** (`NOTICE_SOURCE_PREFIXES`) | Dòng nhắc code tự thêm khi câu trả lời trích bài có số dễ cũ (vé, giờ, hạng sao). |

---

*Bài 1 kể cuốn sổ tay gồm những gì và được giữ đúng ra sao. Bài này kể hai lần mình **viết thêm** vào sổ trong cùng một ngày, và cách mình chắc chắn
trang mới không làm hỏng những câu trả lời đang tốt.*

## Quay lại người hướng dẫn viên

Người hướng dẫn viên dán thêm vài trang vào sổ: một trang về bảo tàng, một trang "đi lại ở Huế", vài trang khách sạn. Trang mới có ích, nhưng cũng có rủi ro.
Khi khách hỏi một câu quen, họ lật sổ và **gặp trang mới trước**, có khi bỏ qua đúng trang lẽ ra phải đọc. Một người cẩn thận sẽ thử lại vài chục câu khách
hay hỏi, **trước và sau** khi dán, rồi so từng câu.

Mình làm đúng như vậy. Mỗi lần ghi kho có bốn bước cố định:
1. Đo "trước" trên kho cũ.
2. Sao lưu, ghi, chia đoạn thử, dựng lại chỉ mục. Một script làm cả chuỗi, và **tự trả kho về như cũ** nếu lỗi ở bất kỳ bước nào.
3. Đo "sau" với cùng bộ câu.
4. So từng câu theo tiêu chí đã ghi từ trước.

## Lần 1 (sáng 14/11): ba bài mới và bốn chỗ sửa

**Ghi gì:**
- Ba bài mới: một bảo tàng cổ vật cung đình, một không gian lưu niệm của một hoạ sĩ, và bài "Đi lại ở Huế" (sân bay, xe, xích lô, thuê xe máy…).
- Bốn chỗ sửa theo trang chính thức và Sở Du lịch. Ví dụ: số nhà của một khu trưng bày. Các chỗ sửa ở hai bài vé có thêm một dòng nguồn ghi ngày đối chiếu.
- Trước khi ghi, người kiểm thấy cùng số nhà sai đó còn ở **một bài thứ hai**, viết hơi khác, nên lần tìm của mình sót. Nếu chỉ sửa một bài thì sổ
  **tự nói hai điều trái nhau**. Mình sửa cả hai; đó là chỗ sửa thứ tư.
- Kho: **204 ⇒ 207 bài, 8.435 ⇒ 8.474 đoạn**.

**Đo ra sao:**

| Đo gì | Mốc (kho cũ) | Kho mới | Vì sao ổn / chưa ổn |
|---|---|---|---|
| Bước tìm: MRR (bài 10), 158 câu, không tốn tiền | 0,7216 | 0,7203 | Gần như không đổi. Đoạn mới chen vào top 10 ở 5 câu, đúng bằng mức cho phép đã ghi trước (≤ 5). |
| Câu trả lời: Đủ / Đúng (bài 11), chấm mù theo cặp, 129 câu chính | — | Đủ **+0,031**, Đúng **+0,039** | Mức sàn là "không tụt quá 0,1". Trung bình không tụt; chênh nhỏ này nằm trong nhiễu (khoảng tin cậy chạm 0), nên không nói là "tốt lên". Số câu thắng / hoà / thua: Đủ 4 / 123 / 2, Đúng 5 / 123 / 1. |
| Từ chối nhầm (bài 11) | 3 câu | 5 câu | **Trượt chữ** so với mức "≤ trước + 1". Xem chuyện thật bên dưới. |
| Câu hỏi đi lại (6 câu, mình tự đọc) | 2 / 6 dùng được | **4 / 6** (một câu chỉ được một phần) | Có bài mới nên trả lời được thêm câu sân bay. Hai câu hỏi giá xe vẫn từ chối, vì bài cố ý không ghi giá. Mình tự đọc, không chấm mù, nên chỉ là số tham khảo. |

## Lần 2 (trưa 14/11): năm bài khách sạn

**Ghi gì:**
- Năm bài "Lưu trú ở Huế": một bài khách sạn 3–5 sao, bốn bài theo khu (trung tâm hai bờ sông Hương, phía tây, ven biển – đầm phá – Lăng Cô, ngoài ba khu
  chính). Số liệu lấy từ **danh mục khách sạn mà Cục Du lịch Quốc gia công bố**.
- Bài do **code sinh** từ bảng, không ai gõ tay tên hay địa chỉ. Bài không có giá phòng, điện thoại, nhận xét hay link đặt phòng.
- Danh mục có chỗ ghi trùng: một khách sạn có hai dòng, một dòng 5 sao (tên tiếng Việt), một dòng 3 sao (tên tiếng Anh). Mình mở trang chi tiết của cả hai, thấy
  cùng email, cùng số phòng. Bản 3 sao là bản ghi từ trước khi nâng cấp, nên giữ bản 5 sao. Có thêm một cơ sở khác cũng bị ghi hai lần. Gộp cả hai cặp xong còn **139 cơ sở**.
- Thêm một khách sạn 4 sao được công nhận sau ngày lấy danh mục, ghi riêng nguồn là tin chính thức của thành phố.
- Câu trả lời nào trích bài khách sạn sẽ tự có **dòng "thông tin có thể đã thay đổi"**, vì hạng sao có hạn và có thể đổi.
- Kho: **207 ⇒ 212 bài, 8.474 ⇒ 8.522 đoạn**.

**Đo ra sao** (tiêu chí ghi lúc 12:52, trước khi xem số "sau"):

| Đo gì | Trước | Sau | Vì sao ổn / chưa ổn |
|---|---|---|---|
| Bước tìm: MRR, 158 câu | 0,7203 | 0,7188 | Gần như không đổi. Chỉ 2 câu (đều hỏi chi phí ở) thấy đoạn khách sạn trong top 10. |
| Hai câu đó, chấm mù trước ↔ sau | Đủ 5 / Đúng 5 | Đủ 5 / Đúng 5 | Không tụt. |
| Tổng số câu từ chối (176 câu, gồm cả câu từ chối đúng) | 23 | 23 | Có 4 câu mới từ chối, 4 câu thôi từ chối. Cả 8 câu có **lần tìm đầu giống hệt** trước, và không lần tìm nào có đoạn khách sạn, nên đó là nhiễu sinh câu. |
| Bộ an toàn, 32 câu | — | 0 câu chạm đoạn mới | Bài mới không làm lệch câu nào về cảnh báo an toàn. |
| 12 câu hỏi khách sạn (mình viết, một agent con chấm mù) | được trả lời 4 / 12 | được trả lời **11 / 12** | Mức đạt là ≥ 9. Không câu nào nêu giá, không tên hay hạng nào ngoài tài liệu. Câu hỏi giá phòng vẫn từ chối, đúng ý bài. Người chấm mù cho "trả lời đúng điều được hỏi": 9 câu trọn, 2 câu một phần, 1 câu không. |

Còn bốn chỗ chưa tốt, đều là cách model chọn ý từ ngữ cảnh, không phải dữ liệu sai:
- hỏi về homestay thì trợ lý chỉ nói khu phố Tây có homestay, mà không nói danh sách của kho **chưa gồm** homestay, dù tài liệu có ghi;
- câu hỏi khách sạn rẻ ở một khu bỏ sót 2 cơ sở có trong tài liệu;
- câu ven biển bỏ sót một khách sạn 5 sao cùng vùng;
- câu hỏi giá phòng chỉ từ chối, chưa gợi ý các khách sạn cùng hạng.

Mình ghi lại để theo dõi.

**Phần cố ý chưa ghi: giờ Đại Nội theo mùa.** Theo trích dẫn đọc được trên trang anh tìm, hai khung giờ anh chép có thể là **giờ bán vé**, không phải giờ mở cửa.
Mình không tự mở được trang đó, và không thấy trang chính thức nào ghi giờ theo mùa. Vì vậy mình giữ lại, chờ anh xem trang gốc.

## Một chuyện thật: hai lần "trượt chữ" mà vẫn giữ

**Từ chối nhầm 3 ⇒ 5 (lần 1).** Theo luật ghi trước, đây là trượt. Nhưng trước khi kết luận "bài mới làm hỏng", mình xem hai câu thêm vào:
- Lần tìm đầu của cả hai **giống hệt** trước; top 10 không có đoạn nào của bài mới. Kho mới không chạm tới chúng.
- Chạy lại mỗi câu 3 lần: một câu từ chối 1 / 3 lần (lượt đo giữa kỳ trên kho cũ cũng từng từ chối câu này), câu kia 0 / 3.
- Kết luận: nhiễu sinh câu, không phải do kho. Người điều phối đọc như vậy và giữ.

**Một câu nhiều nguồn bị chen (lần 1).** Ở một câu cần ghép hai bài, ba đoạn của bài "Đi lại" chen vào top 10 và đẩy ra một đoạn đúng của bài khác. Theo nhãn
thì câu này "mất đoạn đúng", phạm sàn. Đọc tay thì đoạn bài mới đang đứng hạng 3 mang **cùng ý** với đoạn bị đẩy ra. Điểm câu trả lời trước và sau đều
5 / 5. Giữ.

**Một câu đổi nhãn (lần 1).** Bộ an toàn có một câu trước đây được gắn "kho không có". Sau lần ghi, trợ lý trả lời được câu đó bằng đúng đoạn của bài "Đi lại".
Người kiểm đối chiếu: mọi ý và số đều nằm trong đoạn, không bịa thêm. Câu đó không còn là "ngoài kho", nên đổi nhãn thành "trong kho" từ lần đo này. Nhãn
đi theo kho, không giữ cứng.

Bài học chung: một con số trượt chưa đủ để kết luận. Phải xem **ngữ cảnh của chính câu đó có đổi không**. Ngữ cảnh không đổi mà câu trả lời đổi thì đó là
nhiễu của model. Ngữ cảnh có đoạn mới thì mới cần đọc kỹ.

## Khi nào hỏng

- **Bài mới chen vào câu nhiều nguồn**: đoạn mới hợp chữ có thể đẩy đoạn đúng của bài khác ra khỏi top 10. Lần này may là cùng ý; lần sau có thể không.
- **Nhãn đoạn đúng đi sau kho**: bộ nhãn chưa có bài mới, nên câu được trả lời bằng bài mới có thể bị bước tìm chấm là "trượt".
- **Số liệu khách sạn có hạn**: hạng sao công nhận có thời hạn. Danh mục lấy một ngày cụ thể; vì vậy mới có dòng "có thể đã thay đổi".
- **Nguồn không rõ thì không ghi**: giờ theo mùa chờ anh xác nhận, kho vẫn ghi một khung giờ chung kèm câu "giờ có thể đổi".

## Ba điều chính

1. Mỗi lần ghi kho là một thí nghiệm nhỏ: **đo trước ↔ sau trên cùng bộ câu, tiêu chí ghi trước**. Script làm cả chuỗi ghi và tự lùi nếu lỗi.
2. Hai lần ghi ngày 14/11 thêm **8 bài**: kho 204 ⇒ 212 bài, 8.435 ⇒ 8.522 đoạn. Điểm trung bình câu cũ không tụt; vài câu lệch nằm trong mức cho phép.
   Câu đi lại trả lời được nhiều hơn (2 ⇒ 4 / 6, mình tự đọc), câu khách sạn cũng vậy (được trả lời 4 ⇒ 11 / 12, chấm mù). Tổng tiền đo khoảng 0,45 USD.
3. Số trượt chữ thì xem **ngữ cảnh của câu đó có đổi không** rồi mới kết luận. Nhãn câu cũng phải đổi theo khi kho đã có câu trả lời.

**Bài sau:** Bài 23 — "Lên kế hoạch" bản 2: code xếp lịch theo luật, nghiệm thu lần đầu trượt rồi đạt.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Lần 1, ghi gì, số file / đoạn, đo T1 / K1 / K2 / K5, từ chối nhầm 3 ⇒ 5 và chạy lại 3 lần, câu 154 (nhiều nguồn), X03 đổi nhãn, tiền 0,2288 USD: `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md` [đã chạy]
- Sửa số nhà ở bài thứ hai (người kiểm bắt): `report_agent/2026-11-12_ra_khoang_cach/c_review_ghi_kho_14_11.md`; câu 154 so dãy 4 từ trùng 5 / 9: `c_review_e_ghi_kho_report.md` [đã chạy]
- Lần 2, bài lưu trú, gộp cặp trùng 141 ⇒ 139, thêm 1 khách sạn theo tin thành phố, dòng "có thể đã thay đổi" (`backend/llm/assistant.py` `NOTICE_SOURCE_PREFIXES`), đo T1 / K1 / K2 / K4, homestay, giờ Đại Nội giữ lại, tiền 0,2249 USD: `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_luu_tru_implementation.md`; tiêu chí ghi trước: `data/sua_kho_2026-11-14_ghi_kho_2/TIEU_CHI.md`; cặp trùng: `data/sua_kho_2026-11-13_luu_tru/BIEN_BAN.md`, `report_agent/…/c_review_bai_luu_tru.md` [đã chạy]
- "23 ⇒ 23" là tổng số câu có câu trả lời từ chối trong 176 câu Golden (trường `refusal`), gồm cả câu ngoài kho từ chối đúng; khác với "từ chối nhầm" của lần 1: `data/sua_kho_2026-11-14_ghi_kho_2/truoc|sau/golden.jsonl` [đã chạy]
- Tổng tiền đo hai lần ≈ 0,2288 + 0,2249 = 0,45 USD.
- **Sửa 13:40 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_24.md`): chỉ các sửa ở bài vé có dòng nguồn (bản trước ghi "chỗ nào cũng"); Đủ / Đúng là "không tụt, trong nhiễu" (bản trước ghi "nhích lên"); 139 là sau gộp 2 cặp; "giống hệt" chỉ lần tìm đầu; 4 chỗ chưa tốt thay vì 1, kèm 9 / 2 / 1; Ba điều chính nói rõ số nào tự đọc; bỏ số nhà.

</details>
