# Bài 17 — Trang người dùng thấy, và chờ bao lâu: giao diện và tốc độ

*Cập nhật lần cuối: 14:41, ngày 11/11/2026 · bài mới (bù phần đã làm mà bài 0–16 chưa kể kỹ); đã qua một lượt kiểm độc lập.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Trang cổng — **mới** | portal (React + Vite, thư mục `frontend/`) | Trang web du lịch nhiều mục (Trang chủ, Khám phá, Lên kế hoạch, Trợ lý), không chỉ một khung chat. |
| Chữ hiện dần | **streaming** (đường `/api/chat/stream`, kiểu **SSE**) | Máy chủ gửi từng mẩu chữ về trình duyệt ngay khi model đang viết. |
| Chữ đầu tiên — **mới** | **time to first text** (`first_text_ms`) | Thời gian từ lúc bấm gửi tới lúc chữ trả lời đầu tiên hiện ra. Đây là thước tốc độ chính. |
| Trung vị / câu chậm | **p50 / p95** | p50: một nửa số câu nhanh hơn số này. p95: 95 câu trên 100 nhanh hơn số này, tức là mức "câu chậm". |
| Chạy song song — **mới** | cờ **`song_song_tra_loi`** | Bắt đầu tìm và viết câu trả lời về Huế **cùng lúc** với bước xếp loại câu, thay vì đợi xếp loại xong. |
| Xếp loại câu | **router** (bài 12) | Một lần gọi model ngắn quyết câu đi đường nào. |
| Rào an toàn trình duyệt | **CSP** | Trình duyệt chỉ chạy mã, kiểu chữ, ảnh lấy từ chính máy chủ của chatbot. |

---

*Bài 8 có nhắc chữ hiện dần, bài 12 có nhắc chạy song song. Bài này gom lại phần **người dùng nhìn thấy và cảm thấy**: trang web trông thế nào, vì sao, và
chatbot bắt người dùng chờ bao lâu, đã làm gì để bớt chờ.*

## Quay lại người hướng dẫn viên

Một người hướng dẫn viên giỏi mà ngồi trong phòng kín, khách phải gõ cửa hỏi, thì ít ai biết họ làm được gì. Đặt họ ở **quầy thông tin** có bảng chỉ đường,
tờ gợi ý theo chủ đề, nút "nhờ lên lịch" thì khách thấy ngay việc nhờ được. Và khi khách hỏi, họ **mở miệng nói ngay** câu đầu ("để mình xem… món này có ở…"),
không im lặng mười giây rồi mới đọc một mạch. Khách chờ cùng một lúc, nhưng thấy người kia đang trả lời thì đỡ sốt ruột hơn nhiều.

## Phần 1: trang cổng du lịch

**Vì sao không chỉ là một khung chat.** Đề tài là ứng dụng hỗ trợ trải nghiệm Huế. Nếu chỉ có khung chat, người xem không biết trợ lý làm được gì (5 chủ đề
trong kho, lên lịch trình, thời tiết, hỏi bằng ảnh, tra web) cho tới khi gõ đúng câu. Nên giao diện được làm thành một **trang cổng**:

- **Trang chủ:** ảnh cầu Trường Tiền, dòng "Hỏi về Huế, như hỏi người bản xứ", một ô hỏi lớn gửi thẳng vào trợ lý, vài câu gợi ý bấm được, ô thời tiết nhỏ;
  bên dưới là **5 chủ đề** của kho (Ẩm thực, Di tích, Lễ hội, Nghệ thuật biểu diễn, Đi lại và tham quan).
- **Khám phá:** mỗi chủ đề là một trang danh sách thẻ. Thẻ **chỉ ghi điều kho có**, không sao đánh giá, không giá chung chung.
- **Lên kế hoạch:** biểu mẫu bằng nút (mấy ngày, đi cùng ai, thích gì). Code xếp lịch, model chỉ viết lời (bài 14).
- **Trợ lý Huế:** một nút nổi ở mọi trang, mở khung chat ở góc. Trong khung có dòng trạng thái ("Đang tìm trong kho…", "Đang viết câu trả lời…"), chữ hiện
  dần, nút **Dừng**, và dưới câu trả lời một dòng **"Nguồn: tên · tên"** bấm vào xem đoạn gốc.
- **Giới thiệu:** trợ lý làm được gì, giới hạn, dữ liệu của người dùng được giữ thế nào, nguồn ảnh.

**Đã so gì trước khi chọn.** Hai lần:
1. **Công nghệ (01–02/11):** ba hướng. Viết lại bằng JavaScript thuần thì Phase 9 nhiều màn hình sẽ phải làm lại lần nữa ⇒ bỏ. Dùng React + Vite, dựng sẵn
   thành file tĩnh, máy chủ Python chỉ việc phục vụ ⇒ **chọn**. Thêm một bộ linh kiện giao diện có sẵn thì thử thật trên trình duyệt: 2 linh kiện vi phạm rào an
   toàn trình duyệt (tự chèn khối định dạng vào trang) ⇒ chỉ lấy Tailwind (bộ định dạng giao diện), linh kiện tự viết bằng thẻ HTML gốc.
2. **Hình thức (06–07/11):** trước khi vẽ, mình xem 6 trang du lịch thật, trong và ngoài nước, rút ra 15 điều nên học (nút trợ lý nổi mọi trang, thanh dưới
   trên điện thoại…) và các lỗi nên tránh thấy tận mắt: số đánh giá lệch giữa bản máy tính và điện thoại, nhiều chỗ "Đang cập nhật", sự kiện đã qua vẫn để "nổi
   bật". Có 3 bản mẫu, anh chọn bản **"Sông Hương"** (xanh ngọc, nước sâu, màu sen cho nút trợ lý).

**Hai lựa chọn đáng nhớ:**
- **Bỏ số `[n]` trong chữ**, thay bằng một dòng "Nguồn:" dưới câu (anh chọn). Ở tầng máy, `[n]` và bộ kiểm nguồn (bài 8) vẫn giữ nguyên. Cái giá: người đọc
  không còn thấy ý nào đến từ nguồn nào.
- **Ảnh:** kho gần như không có ảnh được dùng, nên 6 trong 7 ảnh trên trang lấy từ Wikimedia Commons (giấy phép mở), tải về đóng sẵn, có ghi công từng ảnh.
  Riêng ô Lễ hội, trên máy anh dùng một ảnh Festival 2024 không có giấy phép mở (anh duyệt dùng cho đồ án, không đưa lên Git); máy khác tự thay bằng ảnh Commons.

Trang nhẹ: phần mã tải về khoảng **107 KB** (đã nén), dưới mức tự đặt 200 KB.

## Phần 2: đo tốc độ thế nào

**Thước:** thời gian **tới chữ đầu tiên trên trình duyệt thật**. Một trình duyệt tự động chạy trên máy anh, bấm gửi, đo tới khung hình đầu có chữ. Không đo
"tới lúc xong cả câu", vì từ khi có chữ hiện dần, người dùng bắt đầu đọc từ chữ đầu tiên.

**Mốc:** anh chốt ngày 28/10: **p50 ≤ 3 giây, p95 ≤ 5 giây**. Từ 31/10 mốc này áp cho chữ đầu tiên.

**Vì sao nhìn p95, không chỉ trung bình.** Trung vị 2 giây nghe tốt, nhưng nếu 1 câu trong 20 phải chờ 10 giây thì người dùng gặp câu đó sẽ nghĩ trang bị
treo. p95 bắt đúng những câu đó. Lưu ý: mỗi nhóm thường chỉ đo khoảng 20 câu, nên p95 gần như là **câu chậm thứ hai** trong nhóm; một câu lạ là đủ đổi số.

## Phần 3: các lần làm nhanh, theo thứ tự thời gian

| Lúc | Đổi gì | Chữ đầu tiên p50 / p95 | Kết luận |
|---|---|---|---|
| trước 31/10 | chờ cả câu xong mới hiện | **3,1 / 6,0 giây** (đo ở máy chủ, cả câu) | câu chậm vượt 5 giây |
| 01/11 | **chữ hiện dần** | **1,23 / 2,61 giây** (38 câu, trình duyệt) | đạt rộng ⇒ giữ |
| 03/11 | thêm **xếp loại câu** (bài 12) | **3,57 / 6,57 giây** (10 câu) | chất lượng đạt nhưng vượt mốc tốc độ |
| 04/11 | thử **tắt phần "nghĩ"** của model ở bước xếp loại | riêng bước xếp loại nhanh hơn 0,2–0,35 giây (chữ đầu chưa đo vì dừng sớm) | **bỏ**: 2 câu an toàn bị xếp nhầm (chuyện thật dưới) |
| 04/11 (đo), 05/11 (bật) | **chạy song song** viết câu về Huế với xếp loại | nhanh hơn **1,37 giây** ở trung vị (20 cặp), khoảng tin cậy [0,34; 2,14] | khoảng không chứa 0 ⇒ lợi thật ⇒ **giữ** |
| 09/11 | đo chung bản đang chạy | câu về Huế **2,16 / 4,32 giây** (20 câu) | **đạt**, nhưng câu chậm chỉ dư 0,68 giây |
| 10/11 | **câu có ngày: code tính sẵn lịch** (bài 14) | 19 câu ngày: **5,60 / 10,14 ⇒ 2,35 / 4,56 giây**; riêng các câu thật sự đi qua trợ lý: trung vị 5,98 ⇒ 2,34 giây | bỏ một vòng gọi công cụ ⇒ **giữ** |
| 10/11 | thử chạy song song cả câu **chào hỏi** | trung vị 3,46 ⇒ 1,85 giây, nhưng câu chậm vẫn **5,74 giây** | **bỏ**: còn vượt mốc, câu ngoài phạm vi thành đắt hơn trần tiền |

**Đọc bảng thế nào:**
- Số 3,1 / 6,0 đo ở máy chủ và đo cả câu, nên **không cùng thước** với các số sau. Nó chỉ cho biết vì sao phải làm chữ hiện dần.
- Số đo 04/11 là **so theo cặp**: cùng 10 câu hỏi, hai bản chạy xen kẽ cùng lúc. Hôm đó nhà cung cấp model chậm, nên cả hai bản đều vượt mốc. Số "nhanh hơn
  1,37 giây" vẫn dùng được, vì hai bên chịu cùng một hôm chậm.
- Số câu ngày 10/11 đo ở máy chủ. Ngày 01/11 đã đo: trình duyệt chỉ chậm hơn máy chủ khoảng 22 phần nghìn giây, nên gần như bằng nhau. Gần nửa số câu
  trong nhóm này bị xếp "ngoài phạm vi" (nhanh vì chỉ một lần gọi), nên số "đi qua trợ lý" mới là số sát phần sửa.
- Sau chữ hiện dần, hai lần làm nhanh được giữ đều có chung một kiểu: **bỏ một bước phải đợi nối tiếp** (đợi xếp loại xong, đợi gọi công cụ xong). Hai lần
  bị bỏ **có vẻ** đều vấp ở bước xếp loại: bớt "nghĩ" thì xếp sai (đã thấy); với câu chào hỏi, report đoán câu chậm là do bước xếp loại xếp nhầm hoặc chậm
  (giả thuyết, chưa chứng minh).

## Một chuyện thật: nhanh hơn một chút, hỏng đúng câu khó

Ngày 04/11, bước xếp loại câu làm câu về Huế vượt mốc tốc độ. Ý đơn giản nhất: model đang "nghĩ" một chút trước khi xếp loại, vậy **tắt phần nghĩ** đi. Kết
quả: riêng bước xếp loại nhanh hơn 0,2–0,35 giây ở trung vị, mỗi lần gọi xếp loại rẻ hơn 16 %. Nhưng trong bộ 32 câu an toàn, **2 câu an toàn về Huế bị đẩy sang "ngoài phạm vi"** (mốc: 0 câu). Một
câu sai ở cả 2 lượt đo, một câu sai 1 trong 2 lượt. Luật ghi trước nói sai câu an toàn là dừng, nên mình dừng ngay, không đo tiếp.

Điều đáng chú ý: hai câu đó cũng là hai câu mà bản thường **nghĩ lâu nhất**, gấp 2–3 lần trung bình. Có vẻ phần "nghĩ" chính là chỗ model phân biệt câu khó.
Đây là giả thuyết, chưa chứng minh. Cách được giữ sau đó không bớt việc của model, mà **xếp lại thứ tự việc** (chạy song song): nhanh hơn 1,37 giây mà 90 lượt
an toàn không lỗi nào.

Chuyện nhỏ kèm theo: chữ hiện dần, đo trên trình duyệt ngày 01/11, chỉ làm chữ đầu tiên tới sớm hơn **0,44 giây** so với chờ cả câu, dưới mốc 0,5 giây mình tự
đặt trước (khoảng tin cậy [0,37; 0,54] chạm mốc). Lý do là câu trong bộ đo phần lớn ngắn, và hôm đó model gần như không nghĩ trước khi viết. Theo luật
thì phải xem lại cách đơn giản hơn. Agent làm việc này khuyên giữ, vì mã đã xong, tốc độ đạt rộng, câu dài lợi hơn chút (0,51 giây); anh chọn giữ.

## Chỗ còn chậm (số đo thật)

- **Câu chào hỏi:** câu chậm **7,73 giây** (20 câu, 09/11). Số này do hai câu chậm nhất quyết: một câu bị xếp nhầm sang đường về Huế (7,6 giây), một
  câu đi đúng đường nhưng lần gọi model trò chuyện mất 8,2 giây.
- **Hỏi bằng ảnh:** trung vị khoảng 3 giây, câu chậm **6–9 giây**. Gần hết thời gian là chờ model nhìn ảnh.
- **Mục "Từ web":** tới sau khoảng **13 giây** (trung vị). Chỉ xảy ra với câu kho không có.
- **Câu về Huế:** đạt mốc, nhưng p95 chỉ dư 0,68 giây, đo một lượt 20 câu. Một hôm nhà cung cấp chậm (như 04/11) là có thể vượt.
- **Chưa đo:** câu lịch chung (vào chatbot 10/11), các dạng ngày ít gặp, thời gian tới lúc **xong cả câu** của bản Phase 9.

## Khi nào hỏng

- **Nhà cung cấp model chậm hôm đó:** mọi số trên đều phụ thuộc OpenAI. Ngày 04/11, cùng bộ câu, bản chưa chạy song song lên 5,36 / 8,69 giây, bản
  chạy song song (bản đang dùng) cũng 3,53 / 7,72 giây, đều vượt mốc.
- **Câu đầu tiên sau khi bật máy chủ** chậm hơn (một lần thấy 5,1 giây so với 2,8 giây lần sau).
- **Máy đông việc:** đo khi máy đang chạy việc nặng khác thì số không dùng được. Vì vậy lúc đo tốc độ, các session khác phải dừng việc nặng.
- **Đưa lên mạng thật:** chưa đo trên máy AWS (bài 18).

## Ba điều chính

1. **Trang cổng** cho người xem thấy ngay trợ lý làm được gì (5 chủ đề, lên kế hoạch, trợ lý nổi mọi trang). Chọn React dựng sẵn thành file tĩnh, giữ rào an
   toàn trình duyệt; anh chọn bản "Sông Hương" sau khi so 3 bản mẫu.
2. **Thước tốc độ là chữ đầu tiên trên trình duyệt**, mốc p50 ≤ 3 / p95 ≤ 5 giây. Câu về Huế đạt **2,16 / 4,32 giây** (09/11) nhờ chữ hiện dần và chạy
   song song; từ 10/11 câu có ngày được code tính sẵn lịch nên còn 2,35 / 4,56 giây.
3. Chuyện thật: **tắt phần "nghĩ" cho nhanh thì hỏng câu an toàn**. Cách được giữ là xếp lại thứ tự việc, không bớt việc của model. Còn chậm: câu chào hỏi,
   ảnh, mục web.

**Bài sau:** Bài 18 — Đóng gói Docker: mang cả chatbot sang máy khác mà không mang theo dữ liệu kín.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Trang cổng, các mục, câu "Hỏi về Huế, như hỏi người bản xứ", "Khám phá theo chủ đề": `frontend/src/pages.jsx`; menu "Lên kế hoạch" theo cờ: `frontend/src/App.jsx`; nút "Dừng", dòng "Nguồn:", mục "Từ web (chưa kiểm)": `frontend/src/chat.jsx`; màu "Sông Hương": `frontend/src/index.css` [code, xem 11/11]
- Ba hướng công nghệ, 2 linh kiện vi phạm CSP, chỉ lấy Tailwind: `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md`, `report_agent/2026-11-02_giao_dien_moi_code/b121_giao_dien_implementation.md` §4.1 [đã chạy]
- 6 trang tham khảo, 15 điều nên học, lỗi thấy ở trang thật, 3 bản mẫu, anh chọn "Sông Hương" 07/11, bỏ `[n]` trong chữ, ảnh Commons: `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` [quyết định của anh]; mã gzip 106,90 KB: `report_agent/2026-11-06_giao_dien_cong/b_anh_cong_implementation.md` [đã chạy]
- Mốc tốc độ 28/10, áp cho chữ đầu từ 31/10: `session_prompt/Project_Status.md` §1 [quyết định của anh]
- Cả câu trước streaming 3,1 / 6,0 s (API 27/10): `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` [đã chạy]. Spec streaming ghi mốc khác (câu dài 4,6 / 7,6 s, 28/10) — hai mốc khác ngày, khác bộ câu.
- Chữ hiện dần 1,23 / 2,61 s, lợi 0,44 s [0,37; 0,54], trình duyệt chậm hơn máy chủ ~22,5 ms, anh giữ: `report_agent/2026-10-31_streaming_spec/s4_do_d2_implementation.md` §4, `TONG_HOP.md` [đã chạy]
- Xếp loại câu 3,57 / 6,57 s: `07_…` mục 03/11 [đã chạy]
- Tắt suy luận ở bước xếp loại, 2 câu an toàn, nhanh 0,2–0,35 s, rẻ 16 %: `report_agent/2026-11-02_phase_9_code/c156_toc_do_dinh_tuyen.md` [đã chạy]
- Chạy song song −1,37 s [0,34; 2,14], 15 / 20 cặp, hôm đó 5,36 / 8,69 ⇒ 3,53 / 7,72 s, 90 lượt an toàn 0 lỗi: `report_agent/2026-11-02_phase_9_code/c172_toc_do_song_song.md`; cờ `song_song_tra_loi: true`: `backend/config/settings.yaml` [đã chạy, code]
- Đo chung 09/11 (câu về Huế 2,16 / 4,32; câu chào hỏi 3,46 / 7,73; n = 20): `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` [đã chạy; agent con tính lại từ file đo 11/11, khớp]
- Câu ngày tính sẵn 5,60 / 10,14 ⇒ 2,35 / 4,56 s (19 câu, đo ở máy chủ): `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md` §4 [đã chạy]
- Câu chào hỏi song song 3,46 ⇒ 1,85, p95 5,74 s, câu ngoài phạm vi 0,00056 USD (so với lượt 09/11, khác ngày): `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_implementation.md` [đã chạy]
- Ảnh p95 6,3–9,1 s: `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md`; mục web ~13 s: `report_agent/2026-11-02_phase_9_code/b165_b6_implementation.md` [đã chạy]
- Câu đầu sau khởi động 5,1 ↔ 2,8 s (2 lần quan sát): `b121_giao_dien_implementation.md` §5 [đã chạy]
- Bản ghi số liệu cho bài này (agent con, chỉ đọc, 11/11): `data/hoc_cung_user_2026-11-10/fact_bai_17_giao_dien_toc_do.md` (riêng tư)
- Ví dụ quầy thông tin là ví dụ tự đặt.
- **Sửa 14:41 11/11/2026** (người kiểm độc lập bắt, mình đối chiếu nguồn): 2,16 / 4,32 s (09/11) có trước câu ngày tính sẵn (10/11) nên không "nhờ" nó; 5,36 / 8,69 s ngày 04/11 là bản chưa song song; ảnh ô Lễ hội không phải Commons trên máy anh; câu chào hỏi chậm do một câu xếp nhầm + một câu trò chuyện chậm (tính lại từ `data/phase_9/s5_chung/s5_main_r1.jsonl`); 0,2–0,35 s là riêng bước xếp loại (`c156`); nhận xét "vấp ở bước xếp loại" của câu chào hỏi là giả thuyết. Biên bản kiểm: `data/hoc_cung_user_2026-11-10/review_bai_17_19.md` (riêng tư).

</details>
