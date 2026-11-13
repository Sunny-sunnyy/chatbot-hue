# Bài 19 — Bảng tổng các lần so sánh

*Cập nhật lần cuối: 20:37, ngày 13/11/2026 · sửa theo kiểm độc lập; thêm dòng 35–37 (hết lượt tìm thì dừng, thử Exa, lượt đo giữa kỳ) và ý "đếm lỗi trước khi xây".*

## Bảng từ

Bài này không có từ mới; mọi từ đã gặp ở bài 0–18. Ba cách ghi số dùng lại nhiều lần:

| Cách ghi | Nghĩa |
|---|---|
| **+0,26 [+0,08; +0,48]** | Điểm trung bình (thang 1–5) tăng 0,26 so với mốc. Trong ngoặc là **khoảng tin cậy 95 %**: rút lại bộ câu nhiều lần (bootstrap) thì mức tăng gần như chắc nằm trong khoảng này. Khoảng **không chứa 0** ⇒ tăng thật, không do may. |
| **2 / 35 / 3** | Số câu **tốt lên / như cũ / tụt** so với mốc. Ở bước tìm: "tụt" = câu đang tìm đủ đoạn đúng thì nay thiếu. |
| **22 ⇒ 31** | Số trước ⇒ số sau. |

---

*Mỗi bài 0–18 kể kỹ một lần thử. Bài này đặt **mọi lần thử chính** lên một trang, xếp theo đường RAG từ kho tới trợ lý, để khi cần trả lời "đã so sánh những
gì" thì không phải lật lại cả bộ. Muốn hiểu kỹ dòng nào, mở bài ghi ở cột cuối.*

## Đọc bảng thế nào

- **Luật ghi trước.** Mỗi lần thử ghi trước khi chạy: thước nào, mốc nào, thế nào là "tốt hơn", và các **sàn không được vỡ** (ví dụ "không câu nào đang tìm đủ
  đoạn đúng thì nay thiếu", "0 câu ngoài kho bị trả lời", "câu an toàn không sai thêm"). Vỡ sàn thì **bỏ**, dù trung bình tốt hơn. Ngoại lệ duy nhất (dòng 35):
  chỗ vỡ được chứng minh là không do thay đổi, và bảng ghi rõ điều đó.
- **Kết quả âm cũng là kết quả.** Hơn một nửa số dòng dưới là "bỏ". Đó là lý do giải thích được vì sao bước nào cũng đang dùng cách hiện tại.
- **Bối cảnh.** Phần lớn thử nghiệm ở bước tìm và xếp lại (24–27/10) chạy trên kho **trước hai đợt sửa** và lúc chatbot còn đưa **5 đoạn**. Nếu một dòng có thể
  khác đi ở cấu hình hiện nay, cột kết quả ghi rõ.

## Phần 1 — Đường RAG (Phase 1–8)

| # | Thử gì | So với | Kết quả | Giữ / bỏ | Bài |
|---|---|---|---|---|---|
| 1 | **Gộp khối cùng mục thành đoạn to** (128–512 token) | mỗi khối một đoạn | đoạn to tìm thấy nhiều hơn, nhưng chỉ ~4–5 đoạn vừa ngân sách thay vì ~9. Ở 512 token: **0 / 26 / 6** (32 câu), tụt có ý nghĩa thống kê | bỏ | 2 |
| 2 | **Qwen3-Embedding-8B** (8 tỉ tham số, lớn hơn e5-small khoảng 70 lần, gọi qua mạng) thay e5-small | e5-small, kho hiện tại | **2 / 35 / 3** (40 câu), kiểm lại trên nhóm test cũng tụt 3 câu; tìm từ 21 ms lên khoảng 2,2 giây | bỏ | 4 |
| 3 | Đổi cách tách từ cho BM25 (cặp âm tiết, thư viện tách từ tiếng Việt) | tách theo âm tiết | mỗi cách làm mất 1 câu | bỏ | 4 |
| 4 | **Chuẩn hoá Unicode** câu hỏi (NFC) | không chuẩn hoá | câu gõ bằng bảng mã khác làm điểm thứ hạng tụt 0,20; có chuẩn hoá thì giống hệt câu gốc | **giữ** | 4 |
| 5 | 10 cách trộn vector với từ khoá | cách đang dùng | không cách nào thắng rõ; tìm độc lập toàn kho mất 1–2 câu | bỏ | 6 |
| 6 | **Lấy 100 ứng viên** thay vì 30 | 30 ứng viên | ứng viên chứa đủ đoạn đúng 31 ⇒ 37 câu, nhưng 10 đoạn đưa model chỉ 22 ⇒ 23; mất 1 câu | bỏ | 6 |
| 7 | **Chẩn đoán**: đoạn đúng lạc ở đâu | — | 30 ứng viên đủ ở 31 / 40 câu, 10 đoạn đầu chỉ 22 / 40 ⇒ **nghẽn ở xếp hạng**, không ở lấy ứng viên | căn cứ cho dòng 8–9 | 6, 10 |
| 8 | **Model xếp lại chạy trên máy** (2 model, 4 bản) | không xếp lại | mọi bản làm mất đoạn đúng 1–3 câu | bỏ (mới thử ở 5 đoạn) | 7 |
| 9 | **gpt-6-luna chọn 10 trong 30 đoạn** | 10 đoạn theo thứ hạng | bước tìm **22 ⇒ 31 / 40**; trả lời TB +0,22 [+0,02; +0,44], nhưng **5 câu tụt** (ngưỡng 4); chậm 6,5 / 9,1 giây; tốn 3,8 lần | bỏ (giữ hồ sơ) | 7, 11 |
| 10 | **Đưa model 10 đoạn thay vì 5** | 5 đoạn | Đủ ý **+0,26 [+0,08; +0,48]** (88 câu), nhóm test +0,27; từ chối nhầm 22 ⇒ 12 / 158; tiền × 1,5 | **giữ (28/10)** | 0, 6 |
| 11 | Thiếu một vế ⇒ **trả lời phần có căn cứ** | từ chối cả câu | từ chối nhầm 13 ⇒ 1, nhưng **2 câu ngoài kho bị trả lời** | bỏ | 8 |
| 12 | Thước bước tìm: **từ khoá** hay **nhãn đoạn đúng** | từ khoá | 22 câu từ chối nhầm: theo từ khoá 4 câu "có đủ mà vẫn từ chối", theo nhãn **0 câu** ⇒ lỗi ở bước tìm, không phải lời dặn | đổi thước | 10 |

Dòng 10 là **lần thắng duy nhất** của cả đợt rà soát 25/10. Khi kiểm lại trên bộ câu kín, nó cùng với dòng 4 và một sửa nhỏ ở bộ kiểm nguồn cho Đủ ý +0,82, 0 câu tụt.

**Mốc cuối Phase 1–8 (01/11):** Đúng / Đủ / Trúng ý **4,71 / 4,58 / 4,72** trên bộ câu mẫu; trên bộ câu kín mới thấp hơn khoảng 0,3–0,4. Đây là mốc mà Phase 9
không được làm tụt (bài 9, 11).

## Phần 2 — Từ chatbot thành trợ lý (Phase 9–10)

| # | Thử gì | So với | Kết quả | Giữ / bỏ | Bài |
|---|---|---|---|---|---|
| 13 | **Xếp loại câu** 4 đường (trò chuyện / về Huế / ngoài phạm vi / khẩn cấp) | không xếp loại | xếp đúng **253 / 253** câu đã thấy, **20 / 20** câu kín; chậm thêm (bài 17) | **giữ** | 12 |
| 14 | Cổng "2 nhóm" (bỏ đường khẩn cấp và ngoài phạm vi) | 4 đường | 2 / 44 câu ngoài phạm vi có mục web ⇒ vỡ sàn. Chuyển sang **phương án B** (giữ 4 đường, bỏ câu khẩn cấp soạn sẵn): 0 câu ngoài phạm vi bị trả lời (lượt đo giữa kỳ 12/11 thấy 2 / 44 câu vẫn bị đem đi tra web, người dùng chỉ thấy câu cố định; xem dòng 37, bài 16) | bỏ G, **giữ B** | 12 |
| 15 | **Tìm thêm ≤ 2 lần** | một lần tìm | câu nhiều nguồn Đủ ý **+1,17 [+0,44; +2,00]** (18 câu); từ chối nhầm 12 ⇒ 4–6 / 158; nhưng có 1 câu an toàn sai mới (sửa ở dòng 16) | **giữ** | 13 |
| 16 | Câu dặn chống **tự thêm lời khuyên chung** | không có câu dặn | dặn rộng: từ chối nhầm **7** (ngưỡng 5) ⇒ bỏ; dặn hẹp: 4, lỗi an toàn hết ⇒ giữ | **giữ bản hẹp** | 11 |
| 17 | **Nhớ hội thoại** | không nhớ | nhớ cả câu trả lời: 1 / 2 lượt kín câu ngoài kho bị trả lời ⇒ tắt. **Chỉ nhớ câu hỏi**: câu hỏi tiếp **+0,80 [+0,25; +1,50]**, câu bẫy từ chối đúng 6 / 6 (không nhớ: 3 / 6) | **giữ "chỉ nhớ câu hỏi"** | 13 |
| 18 | **Tắt lưu tạm** để đỡ tiền ghi | lưu tạm tự động | 45 % câu gọi model ≥ 2 lần và đọc lại phần đã lưu ⇒ tắt thì phần tiền gửi vào **đắt hơn khoảng 21 %** (ước từ số token đã đo) | bỏ | 13 |
| 19 | **Hỏi lại bằng nút** (số ngày, số người) | không hỏi lại | model vẫn tự viết dòng "Tổng" (luật cấm); vòng 2 có 2 câu an toàn mới thiếu cảnh báo (ngưỡng ≤ 1) | bỏ phần model tự hỏi lại; thẻ hỏi lại do code giữ trong lịch trình (chưa bật) | 14 |
| 20 | **Code tính tiền chuyến đi** | liệt kê giá có nguồn | phép tính đúng **8 / 8**, nhưng câu miễn vé bỏ mất điều kiện **3 / 3** lần (bản đang chạy: 1 / 3) | bỏ | 14 |
| 21 | **Biểu mẫu "Lên kế hoạch"**: nút chọn ⇒ code xếp lịch | — | sàn của code **24 / 24**; câu chậm 4,25 giây | **giữ** | 14 |
| 22 | Lịch trình từ **câu gõ tự do** (2 lần) | biểu mẫu | lần 2: 27 / 27 câu có lịch, nhưng "hợp người đi cùng" chỉ 21 và 15 / 27 (cần ≥ 26) | chưa bật | 14 |
| 23 | **Ngày và âm lịch do code tính**, rồi **tính sẵn** | model tự tính / tự gọi công cụ | bớt 9 câu từ chối nhầm, 0 sai ngày; tính sẵn: 5,60 / 10,14 ⇒ **2,35 / 4,56 giây** | **giữ** | 14, 17 |
| 24 | **Tra web** khi kho từ chối, kèm luật bằng code | không tra web | vòng đầu 2 câu khẳng định tin chưa kiểm ⇒ thêm luật code ⇒ bộ kín **0 / 7** câu khẳng định, 7 / 7 trả lời được | **giữ** | 15 |
| 25 | **Hỏi bằng ảnh**: luna gợi 3 tên, người dùng bấm xác nhận | — | đúng trong 3 gợi ý **22 / 25** (ngưỡng 22); gán tên Huế cho **2 / 5** ảnh không phải Huế (ngưỡng ≤ 1) ⇒ âm theo thước | **giữ dạng chờ xác nhận** | 15 |
| 26 | Model nhận ảnh **chạy trên máy** (SigLIP 2) | luna | 20 / 25, nhưng gán tên Huế cho **5 / 5** ảnh không phải Huế | bỏ | 15 |
| 27 | **Chạy song song** câu về Huế với xếp loại | chạy nối tiếp | chữ đầu nhanh hơn **1,37 giây [0,34; 2,14]**; 90 lượt an toàn 0 lỗi | **giữ** | 12, 17 |
| 28 | **Tắt phần "nghĩ"** ở bước xếp loại | mức mặc định | riêng bước xếp loại nhanh hơn 0,2–0,35 giây, nhưng **2 câu an toàn** bị xếp "ngoài phạm vi" | bỏ | 17 |
| 29 | Chạy song song cả **câu chào hỏi** | lượt đo 09/11 | trung vị 3,46 ⇒ 1,85 giây, nhưng câu chậm vẫn **5,74 giây** | bỏ | 17 |
| 30 | **Để trợ lý tự quyết khi nào tra web** | cổng web (chỉ khi kho từ chối) | câu hỏi kèm có phần web **4 / 10, bằng mốc** (cần ít nhất 6 / 10); 26 / 29 lần model đòi tra web rơi đúng vào lượt kho đã từ chối, tức cổng cũ đã mở rồi | bỏ | chỉ ở bài này |
| 31 | **Bảng vé + giờ có cấu trúc** (60 điểm) | trả lời từ đoạn kho | vòng 3 đúng **19 / 20**, nhưng sàn "model không tự nêu điều kiện ngoài phần code nối" trượt **6 / 10**; bản chỉ dùng bảng để kiểm số: 52 câu thật, **không bắt được số sai nào** | bỏ: lợi gần 0, thêm khoảng 120 dòng code và một bảng phải giữ khớp kho | chỉ ở bài này |
| 32 | **Luật từ khoá** cho câu khẩn cấp | chỉ model xếp loại | **14 / 14** câu đã thấy, nhưng câu kín **0 / 8** và chặn nhầm 2 / 8 ⇒ học thuộc câu đã thấy | bỏ | 12 |
| 33 | Thêm dòng "hôm nay là ngày …" vào lời dặn | không có | từ chối nhầm 5,0 ⇒ 4,5 (cần giảm ít nhất 3) | bỏ (sau đó ngày do code tính, dòng 23) | chỉ ở bài này |
| 34 | **Model viết lại câu tìm** trước lần tìm đầu (3 cách) | tìm bằng câu gốc | không cách nào qua luật: chỉ thêm 0–1 / 12 câu đủ từ khoá (cần ít nhất 3) | bỏ | 13 |
| 35 | **Hết lượt tìm thì dừng**: sau 2 lần tìm thêm, code cất công cụ tìm kho | lần xin thứ ba nhận "đã hết lượt" | 8 câu kho thiếu: **8 / 8** bớt lượt gọi model (cần 5), trung vị cả câu **22,85 ⇒ 16,15 giây**, tiền không tăng; sàn bộ câu mẫu **phạm theo chữ** (3 câu đổi sang từ chối); vẫn giữ vì chạy lại bản cờ tắt cũng đổi chiều đúng 3 câu, và cả 3 chỉ tìm 1 lần nên không chạm chỗ cờ; người kiểm độc lập đồng ý | **giữ kèm theo dõi** (bật 13/11; thấy 1 câu bịa thì tắt) | 13 |
| 36 | **Exa trước, Serper dự phòng** cho tra web | Serper | đo riêng bước tra (42 câu, 2 người chấm cùng gắn): Exa **25**, Serper **17** (cần 22) ⇒ đạt, nhưng bỏ 5 mục trích trang tổng hợp của Exa thì còn 20; qua máy chủ thật: Exa **14**, Serper **13** (cần 16) | bỏ (giữ hồ sơ) | 15 |
| 37 | **Lượt đo giữa kỳ**: cả trợ lý | bản RAG Phase 1–8, cùng bộ câu, cùng kho | tốt hơn ở **3 / 3 nhóm**: câu nhiều nguồn +1,0 [+0,28; +1,83], câu theo ngày dùng được 27 so với 11, câu hỏi tiếp +1,64 [+0,64; +2,71]; bộ câu mẫu tụt **4** câu (ngưỡng 4); từ chối nhầm 13 ⇒ 3 / 158; **3 chỗ phạm sàn** | không phải giữ / bỏ: số đo của bản đang chạy; trước lượt cuối anh quyết từng sàn phạm là sửa hay nhận là giới hạn | 16 |

## Nhìn cả bảng thấy gì

1. **Các lần thắng về chất lượng phần lớn có hai kiểu:** đưa model **thêm bằng chứng** (10 đoạn, tìm thêm), hoặc **giao việc dễ sai cho code** (ngày,
   lịch trình, luật tra web). Model lớn hơn, xếp lại thông minh hơn đều chưa thắng; dặn dò thêm chỉ giữ được một bản dặn hẹp (dòng 16).
2. **Phần lớn lần bỏ là vì vỡ sàn**, không phải vì trung bình kém (dòng 1, 2, 9, 11, 14, 28). Luật ghi trước giữ chatbot khỏi những thay đổi "trung bình tốt
   hơn nhưng có câu tệ đi".
3. **Mỗi thứ thêm vào lời dặn hay công cụ đều có thể làm hỏng câu an toàn ở chỗ khác** (dòng 15, 19, 20). Vì vậy ở phần trợ lý, mọi lần thử đều có tầng an toàn: chạy lại bộ 32 câu an toàn, hoặc chứng minh chuỗi gửi model không đổi rồi
   dùng lại số cũ.
4. **Còn đáng thử lại:** dòng 8 mới thử khi còn 5 đoạn; dòng 9 đã thử ở 10 đoạn nhưng trên kho cũ và chậm, cần một cách để luna chọn đoạn nhanh hơn (bài 16).
5. **Đo riêng một bước có thể đánh lừa.** Dòng 36 đạt khi đo riêng bước tra, nhưng qua đường người dùng thật (cổng web, luật kiểm phía sau) thì lợi biến mất.
6. **Có những thứ không cần thử.** Ngày 12/11, ba ý tưởng bị hạ ngay ở bước **đếm lỗi trước khi xây**: đếm trên kết quả đã có thì lỗi tưởng có không đủ nhiều
   (bài 20). Vì không chạy thử nên chúng không có dòng trong bảng.

Ngoài 37 dòng này còn khoảng 55 lần thử nhỏ hơn: đổi hằng số, sửa kho, đổi cách đo. Chúng nằm trong sổ ghi việc của các agent. Anh không cần đọc để kể đồ án.

**Bài sau:** Bài 20 — Làm đồ án thế nào. Muốn hiểu kỹ một dòng ở trên, mở bài ghi ở cột cuối.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Phần 1 (dòng 1–12, mốc 01/11): `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` §2.1 và các khối N2-01, N2-09, N2-11, T3-05, T3-02, T3-03, T3-01, T3-08, T3-09, S2, S4, K14 = E5, E13 [đã chạy; số chép từ báo cáo, agent con không đếm lại từ hồ sơ gốc]
- Câu kín +0,82, 0 câu tụt: `session_prompt/Project_Status.md` §3 dòng Phase 8.2 [đã chạy]
- Phần 2 (dòng 13–24, 27–29): `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` §1, §4 theo ngày 02–10/11; `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md` §4 (dòng 15); câu dặn dòng 16: `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md` bảng Q2; dòng 18: `report_agent/2026-11-02_phase_9_code/c202_ghi_dem.md`; dòng 28: `c156_toc_do_dinh_tuyen.md`; dòng 29: `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_implementation.md` [đã chạy]
- Dòng 25–26 (ảnh, Phase 10): `bao_cao_he_thong/08_BAO_CAO_HOI_BANG_ANH.md` §1, §3 [đã chạy]
- Bản ghi số liệu đủ 86 dòng (agent con, chỉ đọc, 11/11): `data/hoc_cung_user_2026-11-10/fact_trang_tong_so_sanh.md` (riêng tư)
- Phần "Nhìn cả bảng thấy gì" là nhận xét của mình từ bảng, không phải số đo riêng.
- Qwen3-Embedding-8B 8 tỉ tham số (theo tên model); multilingual-e5-small khoảng 118 triệu ⇒ khoảng 70 lần [kiến thức công khai, chưa tra lại trong phiên]
- **Sửa 14:41 11/11/2026** (người kiểm độc lập bắt, mình đối chiếu nguồn): dòng 9 (luna chọn đoạn) đã so với mốc 10 đoạn + NFC (`91` T3-09) — bản trước ghi "mới thử ở 5 đoạn"; lần thử chạy song song / xã giao song song dùng lại số an toàn khi chuỗi gửi model không đổi (`c172`) — bản trước ghi "mọi lần thử chạy lại bộ 32 câu"; 21 % là phần tiền gửi vào, ước (`c202` §4). Biên bản kiểm: `data/hoc_cung_user_2026-11-10/review_bai_17_19.md` (riêng tư).

- Dòng 35 (thêm 20:22 13/11/2026): `report_agent/2026-11-12_ra_khoang_cach/b_het_luot_tim_implementation.md` §4, §4.1; `b_het_luot_tim_review.md`; bật: `c_review_bat_co_het_luot.md` [đã chạy]
- Dòng 36: `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` §6, §6b, §7; `e_exa_review.md` [đã chạy]
- Dòng 37 (và ghi chú thêm ở dòng 14): `report_agent/2026-11-08_phase_9_ban_13/b7_implementation.md` §4, §8; `b7_review.md` [đã chạy]; ý 6: `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` §3b, §3d [đã chạy]. Bản ghi số liệu: `data/hoc_cung_user_2026-11-10/fact_viec_12_11.md` (riêng tư)
- Dòng 30–34 (thêm 15:03 11/11/2026): `report_agent/2026-11-08_phase_9_ban_13/e_t2_web_implementation.md` (dòng 30), `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` (dòng 31), `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` mục 02/11 (dòng 32, 33) và mục 03/11, `06_BAO_CAO_TIM_KIEM.md` (dòng 34) [đã chạy]

- **Sửa 15:17 11/11/2026** (người kiểm độc lập bắt, mình đối chiếu nguồn; biên bản `data/hoc_cung_user_2026-11-10/review_bai_20_21.md`, riêng tư): dòng 30 cần ≥ 6 / 10 (`e_t2_web_implementation.md` §4); dòng 30, 31, 33 không có bài riêng kể kỹ ⇒ "chỉ ở bài này".
- **Sửa 20:37 13/11/2026** theo kiểm độc lập (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_13_11.md`, riêng tư): dòng 35 ghi rõ sàn bộ câu mẫu phạm theo chữ và vì sao vẫn giữ kèm theo dõi (HLi §4, §4.1; HLr §5); "Đọc bảng thế nào" thêm ngoại lệ đó; dòng 37: sàn phạm do anh quyết sửa hay nhận giới hạn.

</details>
