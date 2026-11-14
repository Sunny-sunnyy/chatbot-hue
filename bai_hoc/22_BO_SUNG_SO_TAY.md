# Bài 22 — Viết thêm vào sổ tay mà không làm hỏng trang cũ: ba lần ghi kho ngày 14/11

*Cập nhật lần cuối: 16:17, ngày 14/11/2026 · thêm lần ghi kho thứ ba (bốn nơi chưa có bài + giờ Đại Nội theo mùa); bản đầu đã sửa theo một lượt kiểm độc lập (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Ghi kho | (không có tên riêng; thư mục làm việc `data/sua_kho_…`) | Thêm bài hoặc sửa chữ trong kho, rồi dựng lại chỉ mục để chatbot tìm được chữ mới. |
| Đo trước ↔ sau — **mới** | **before / after** (paired comparison) | Chạy cùng bộ câu trên kho cũ và kho mới, cùng code, rồi so từng câu một. |
| Tiêu chí ghi trước | **pre-registered criteria** | Mức đạt viết ra **trước** khi xem kết quả, để không "dời cột gôn" sau khi thấy số. |
| Nhiễu sinh câu — **mới** | **generation noise** | Cùng một câu, cùng ngữ cảnh, model vẫn có lúc trả lời, có lúc từ chối. Khác biệt kiểu này không do kho. |
| Dòng "có thể đã thay đổi" | **may-have-changed notice** (`NOTICE_SOURCE_PREFIXES`) | Dòng nhắc code tự thêm khi câu trả lời trích bài có số dễ cũ (vé, giờ, hạng sao). |
| Câu chạm — **mới** | **touched cases** | Câu đo mà 10 đoạn tìm được có đoạn của bài mới hoặc của bài vừa sửa. Câu không chạm thì bài mới không có mặt trong ngữ cảnh của nó. |

---

*Bài 1 kể cuốn sổ tay gồm những gì và được giữ đúng ra sao. Bài này kể ba lần mình **viết thêm** vào sổ trong cùng một ngày, và cách mình chắc chắn
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

**Phần cố ý chưa ghi ở lần 2: giờ Đại Nội theo mùa.** Theo trích dẫn đọc được trên trang anh tìm, hai khung giờ anh chép có thể là **giờ bán vé**, không phải giờ mở cửa.
Mình không tự mở được trang đó, và không thấy trang chính thức nào ghi giờ theo mùa, nên giữ lại. Lần 3 đã ghi, theo cách đọc đã thống nhất (xem dưới).

## Lần 3 (chiều 14/11): bốn nơi nổi tiếng mà sổ chưa có trang riêng

**Vì sao chọn bốn nơi này — đếm trước rồi mới viết.** Mình tự liệt kê 50 địa danh nổi tiếng mà khách dễ hỏi (theo hiểu biết chung, không lấy từ câu hỏi thật — log không lưu chữ câu hỏi), rồi đếm xem kho đã có bài riêng chưa: **26 nơi chưa có**. Nhiều
nơi trong đó là một phần của bài lớn (ví dụ các công trình trong Kinh thành), nên không cần bài riêng. Mình hỏi thử trợ lý 6 câu về những nơi còn lại:
cầu Trường Tiền và Ga Huế **bị từ chối**, chùa Từ Hiếu, nhà vườn An Hiên và Cồn Hến chỉ được một hai câu mỏng, làng hương Thủy Xuân thì trả lời được.
Vì vậy mình viết bốn bài: **cầu Trường Tiền, Ga Huế, chùa Từ Hiếu, nhà vườn An Hiên**. Lượt hỏi thử này tốn chưa tới 0,01 USD.

**Viết bài ra sao.** Hai agent con tra trang công khai (báo, trang du lịch của thành phố, Cục Văn thư và Lưu trữ…), mỗi ý ghi nguồn và ngày, rồi tự mở lại vài
trang chính để đối chiếu. Nhiều chỗ các nguồn **ghi khác nhau**: năm xây cầu (1897–1900), chiều dài cầu (khoảng 400 m, tư liệu lưu trữ ghi 402,6 m), năm xây
nhà ga (1906 hay 1908), năm vua ban tên chùa (1848 hay 1849). Gặp chỗ như vậy, bài ghi khoảng hoặc "nguồn ghi A hoặc B", không tự chọn một bên. Ý không có
nguồn thì bỏ. Một người kiểm khác đọc bốn bài và chỗ sửa giờ Đại Nội trước khi ghi, bắt bốn chỗ cần sửa: chỗ lớn nhất là khung giờ tham quan đêm của Đại Nội chưa có nguồn chắc; các chỗ còn lại như đợt sửa cầu năm 2026 chưa có tin là đã xong, hay ghi thêm "một số nguồn ghi số 1" cho số nhà của nhà ga.

**Giờ Đại Nội theo mùa.** Bài Đại Nội nay chia hai mùa. Từ giữa tháng 3 tới giữa tháng 10 là mùa hè: cửa mở lúc 6 giờ 30, đóng lúc 18 giờ, quầy vé
thôi bán khoảng nửa tiếng trước đó. Phần còn lại của năm là mùa đông: cửa mở lúc 7 giờ, đóng lúc 17 giờ 30, quầy vé thôi bán sớm hơn nửa tiếng. Như vậy hai khung anh chép được đọc là **giờ ngừng bán vé**, còn giờ mở cửa thì dài hơn nửa tiếng. Nguồn là một trang hướng dẫn
du lịch, không phải trang của chính cơ quan quản lý di tích, nên bài **viết nhẹ**: với tham quan buổi tối, bài chỉ nói là có theo
từng đợt, trang hướng dẫn ghi chừng 7 giờ tới 10 giờ tối, và khuyên khách xem lịch trước. Mười một bài lăng, điện khác vẫn ghi khung 07h00 – 17h30 chung, vì nguồn chỉ
nói giờ của Đại Nội.

- Kho: **212 ⇒ 216 bài, 8.522 ⇒ 8.603 đoạn** (bốn bài mới thêm 81 đoạn).

**Đo ra sao — chỉ đo câu bị chạm.** Hai lần trước mình chạy lại cả 176 câu Golden. Lần này mình đếm trước, không tốn tiền: so 10 đoạn tìm được của từng câu
trên kho cũ và kho mới. Có **9 / 158 câu** đổi top 10, nhưng chỉ **2 câu** thật sự gặp đoạn của bài mới hoặc bài Đại Nội. 7 câu còn lại chỉ đổi thứ tự hoặc đổi một đoạn cũ lấy một đoạn cũ khác, không có đoạn nào của bài mới; câu trả lời của
chúng có thể lệch đôi chút do ngữ cảnh khác, nhưng không phải do nội dung mới, nên mình không chạy lại. Vì vậy mình chạy lại 2 câu đó, thêm 18 câu "ngoài kho" (bước tìm đo
riêng không có các câu này, mà bài mới có thể làm trợ lý trả lời nhầm), và bộ an toàn 32 câu.

| Đo gì | Kết quả | Vì sao ổn |
|---|---|---|
| 2 câu chạm | Cả hai vẫn trả lời, **cùng ý**, chỉ đổi cách viết | Tiêu chí ghi trước nói "câu trả lời đổi thì một agent con chấm mù"; hai cặp quá ngắn và cùng ý nên mình đọc tay thay vì chấm mù — lệch nhỏ so với tiêu chí, ghi ra ở đây. |
| 18 câu ngoài kho | **0 câu bị trả lời** | Sàn "0 câu ngoài kho bị trả lời" giữ nguyên. |
| Bộ an toàn, 32 câu | 0 câu đổi lớp; 0 câu gặp đoạn bài mới | Một câu gặp dòng giờ Đại Nội mới, câu trả lời vẫn cùng lớp. |
| 7 câu hỏi thử (6 câu hỏi trước khi ghi + 1 câu giờ Đại Nội) | Cầu và nhà ga **hết bị từ chối**, trích đúng bài mới; câu năm xây nhà ga trả lời "các nguồn không thống nhất" rồi nêu cả hai; chùa và nhà vườn đủ ý hơn; giờ Đại Nội trả lời theo mùa | Mình tự đọc: không con số nào trái với bài. |

Cả lần 3 tốn khoảng **0,03 USD**, khoảng một phần bảy mỗi lần trước (0,22–0,23 USD), vì chỉ đo câu bị chạm.

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
- **Nguồn không rõ thì viết nhẹ, không viết chắc**: giờ Đại Nội lấy từ trang hướng dẫn du lịch nên ghi kèm "kiểm lịch trước khi đi"; giờ quầy vé nhà ga, lịch
  bật đèn cầu không có nguồn mới nên bài nói rõ là có thể đã đổi.
- **Đếm câu chạm chỉ dựa trên bước tìm**: nếu đoạn mới chen vào lần tìm thêm của trợ lý (không phải lần tìm đầu), cách đếm này không thấy.

## Ba điều chính

1. Mỗi lần ghi kho là một thí nghiệm nhỏ: **đo trước ↔ sau trên cùng bộ câu, tiêu chí ghi trước**. Script làm cả chuỗi ghi và tự lùi nếu lỗi.
2. Ba lần ghi ngày 14/11 thêm **12 bài**: kho 204 ⇒ 216 bài, 8.435 ⇒ 8.603 đoạn. Điểm trung bình câu cũ không tụt; vài câu lệch nằm trong mức cho phép.
   Câu đi lại trả lời được nhiều hơn (2 ⇒ 4 / 6, mình tự đọc), câu khách sạn cũng vậy (4 ⇒ 11 / 12, chấm mù), câu về cầu và nhà ga hết bị từ chối.
   Tổng tiền đo khoảng 0,48 USD; lần 3 chỉ 0,03 USD nhờ đếm câu chạm trước.
3. Số trượt chữ thì xem **ngữ cảnh của câu đó có đổi không** rồi mới kết luận. Cùng ý đó, trước khi đo hãy đếm câu nào bị chạm: không chạm thì không cần chạy lại.

**Bài sau:** Bài 23 — "Lên kế hoạch" bản 2: code xếp lịch theo luật, nghiệm thu lần đầu trượt rồi đạt.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Lần 1, ghi gì, số file / đoạn, đo T1 / K1 / K2 / K5, từ chối nhầm 3 ⇒ 5 và chạy lại 3 lần, câu 154 (nhiều nguồn), X03 đổi nhãn, tiền 0,2288 USD: `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md` [đã chạy]
- Sửa số nhà ở bài thứ hai (người kiểm bắt): `report_agent/2026-11-12_ra_khoang_cach/c_review_ghi_kho_14_11.md`; câu 154 so dãy 4 từ trùng 5 / 9: `c_review_e_ghi_kho_report.md` [đã chạy]
- Lần 2, bài lưu trú, gộp cặp trùng 141 ⇒ 139, thêm 1 khách sạn theo tin thành phố, dòng "có thể đã thay đổi" (`backend/llm/assistant.py` `NOTICE_SOURCE_PREFIXES`), đo T1 / K1 / K2 / K4, homestay, giờ Đại Nội giữ lại, tiền 0,2249 USD: `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_luu_tru_implementation.md`; tiêu chí ghi trước: `data/sua_kho_2026-11-14_ghi_kho_2/TIEU_CHI.md`; cặp trùng: `data/sua_kho_2026-11-13_luu_tru/BIEN_BAN.md`, `report_agent/…/c_review_bai_luu_tru.md` [đã chạy]
- "23 ⇒ 23" là tổng số câu có câu trả lời từ chối trong 176 câu Golden (trường `refusal`), gồm cả câu ngoài kho từ chối đúng; khác với "từ chối nhầm" của lần 1: `data/sua_kho_2026-11-14_ghi_kho_2/truoc|sau/golden.jsonl` [đã chạy]
- Tổng tiền đo hai lần ≈ 0,2288 + 0,2249 = 0,45 USD.
- Lần 3: 50 địa danh / 26 chưa có bài / 6 câu hỏi thử trước (`data/bai_kho_moi_2026-11-14/dia_danh_dem.json`, `hoi_thu_truoc.json`); nguồn từng ý, chỗ mâu thuẫn (`…/*_tom_tat.md`); người kiểm 1 major + 3 minor (`data/sua_kho_2026-11-14_ghi_kho_3/c_review_kho_3.md`); 216 bài / 8.603 đoạn, T1 9 / 158 đổi, 2 câu chạm (46, 154), 18 ngoài kho 0 bị trả lời, an toàn 0 đổi lớp, 7 câu thử, 0,030 USD: `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_3_implementation.md`; tiêu chí ghi trước: `data/sua_kho_2026-11-14_ghi_kho_3/TIEU_CHI.md` [đã chạy]
- Giờ Đại Nội theo mùa: trang Vinpearl hướng dẫn tham quan Đại Nội (10/06/2025), anh tra 14/11 [tài liệu]; cách đọc "ghi cả hai, theo mùa: mở 6:30 / 7:00, ngừng bán vé ~17:30 / ~17:00" là anh chọn lúc 14:58 14/11 (`session_prompt/CURRENT_HANDOFF.md`).
- Kiểm độc lập lần 3 (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_lan3.md`): 40 mục — 31 đúng, 1 sai (tỉ lệ tiền), 7 dễ hiểu nhầm, 1 không kiểm được; đã sửa cả 8.
- Cập nhật 16:17, ngày 14/11/2026: thêm lần 3, sửa tiêu đề, bảng từ, Khi nào hỏng, Ba điều chính.
- **Sửa 13:40 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_24.md`): chỉ các sửa ở bài vé có dòng nguồn (bản trước ghi "chỗ nào cũng"); Đủ / Đúng là "không tụt, trong nhiễu" (bản trước ghi "nhích lên"); 139 là sau gộp 2 cặp; "giống hệt" chỉ lần tìm đầu; 4 chỗ chưa tốt thay vì 1, kèm 9 / 2 / 1; Ba điều chính nói rõ số nào tự đọc; bỏ số nhà.

</details>
