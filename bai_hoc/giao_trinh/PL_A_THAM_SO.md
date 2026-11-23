# Phụ lục A — Mọi tham số cấu hình: giá trị đang chạy, dùng để làm gì, bài nào giảng

*Cập nhật 18:51, ngày 23/11/2026 · khớp hệ thống 17:35 23/11 (55 tính năng mở, 7 tắt, kho 267 bài); chưa có lượt cả bộ test sau các bản gộp từ 16:20; chưa gồm các việc từ 18:00 (chờ phiếu) · sửa hàng bảng điểm (bản 14, 45 dòng), phút đi, điểm tối đa một buổi, trần đoạn kho 25 ⇒ 35; năm hàng mới: thứ tự chọn buổi tối, giờ in buổi tối, chặng sang khu 60 phút, nghỉ trưa ngày sang khu, điểm thiếu bảng khoảng cách · các mốc trước: khối Nguồn.*

**Phụ lục này có gì.** Mọi tham số có giá trị số hoặc chữ trong file cấu hình của máy chủ, và các hằng số trong chương trình mà các bài đã nhắc. Dòng bật / tắt và bảy dòng chọn chế độ (model viết, cách tìm, xếp lại, bản chỉ mục, câu cho lần tìm đầu, cổng đưa công cụ) nằm ở phụ lục B.

**Đọc bảng thế nào.**
- Tên trong dấu `…` là tên dòng cấu hình (dạng `mục.tên`) hoặc tên hằng số trong chương trình, để tra.
- Cột *Đã thử giá trị khác chưa* chép từ các bài và bảng tổng các lần so sánh: "đã đo" (kèm kết quả ngắn), "chưa so" (đã tìm, không thấy phép thử nào), hoặc "—" (giá trị do quy ước / model quy định, không có gì để thử).
- Dấu **[khoá]**: chương trình kiểm cấu hình lúc bật và **chỉ nhận đúng giá trị này**; ghi giá trị khác thì máy chủ không bật. Muốn thử giá trị khác phải sửa cả chương trình kiểm. Có tất cả 8 giá trị như vậy: 5 ở phụ lục này, 3 ở phụ lục B (`candidate_id`, `retrieval_treatment`, `reranker`).
- Phép đo trước 09:41 ngày 21/11/2026 là với gpt-6-luna; sau đó là Claude Sonnet 5.5 (ghi "model đang chạy").

## 1. Chuẩn bị kho (chặng 2, bài 7–12)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Thư mục kho | `full_corpus.knowledge_base.root_dir` | thư mục kho của dự án | nơi đọc các bài | — | 7 |
| Các nhóm bài được đưa vào | `full_corpus.knowledge_base.include_globs` | 7 nhóm: món ăn, di sản, lễ hội, nghệ thuật trình diễn, địa điểm, dịch vụ, vé | chỉ bài trong các nhóm này mới được cắt đoạn và lập chỉ mục | — | 7, 9 |
| Thư mục bỏ qua | `full_corpus.knowledge_base.exclude_parts` | bộ câu chấm, bản thô tải về, thư mục mẫu và ghi chú soạn | không phải nội dung cho người dùng | — | 8 |
| File bỏ đích danh | `full_corpus.knowledge_base.exclude_files` | 3 file danh mục dùng lúc soạn | chỉ là danh sách tên | đã đo lúc loại: kết quả tìm không khác | 8 |
| File quy tắc gắn lưu ý | `full_corpus.conditions_file` | một file JSON trong thư mục ghi chú của kho; 3 quy tắc ở 2 bài | gắn câu lưu ý chung của bài vào đúng các đoạn giá đã khai | — | 7, 8 |
| Ba model dùng để tính giới hạn độ dài đoạn | `full_corpus.embedding_models` | e5-small (512 token, tiền tố `passage: `) · e5-base (512 token) · một model tiếng Việt cũ (256 token, có tách từ) | mỗi đoạn phải vừa cả ba giới hạn, nên không đoạn nào bị cắt cụt | đã thử chỉ giữ giới hạn 512: ít đi 61 đoạn (bài 10) | 8, 10 |
| Cách cắt | (chương trình cắt đoạn) | theo khối của bài: đoạn văn, mục danh sách, bảng, đoạn trích; không gối đầu | giữ ranh giới ý người soạn đặt | đã thử 12 cách khác; gối đầu chưa so | 8 |
| Kết quả cắt | — | 267 bài ⇒ 9.479 đoạn | — | — | 7, 8 |
| Model embedding | `DENSE_MODEL_SPECS` (mục `e5-small-384`) | `intfloat/multilingual-e5-small`, ghi cố định mã phiên bản | biến đoạn và câu hỏi thành dãy số | đã so 5 model khác (gồm Qwen3-8B 4.096 chiều: bỏ) | 10 |
| Số chiều vector | như trên | 384 | do model quy định | 768 và 4.096 qua model khác | 10, 12 |
| Độ dài tối đa model đọc | như trên | 512 token | giới hạn của model | — | 10 |
| Tiền tố | `prepare_query`, `full_corpus.embedding_models[].prefix` | `passage: ` cho đoạn, `query: ` cho câu hỏi | quy ước huấn luyện của họ e5 | chưa so việc bỏ tiền tố | 10 |
| Nơi chạy embedding | như trên | CPU, số thực 32 bit, lô 8 đoạn | không cần card đồ hoạ, không gửi câu hỏi ra ngoài | gọi model qua mạng: đã thử, bỏ; cỡ lô chưa so | 10 |
| Hằng số BM25 k1 | `scoring/bm25.K1` | 1,5 | mức "bão hoà" khi một từ lặp nhiều lần | đã thử 1,2 và 1,8 trên bản thử nhóm món ăn: giữ 1,5 | 11 |
| Hằng số BM25 b | `scoring/bm25.B` | 0,75 | mức trừ bớt cho đoạn dài | đã thử 0,5 (chưa rõ hơn) và 1,0 (mất đoạn đúng ở 1 câu) | 11 |
| Địa chỉ Qdrant | `vector_database.url` | máy này, cổng 6335 (bản Docker đổi bằng biến lúc chạy, phụ lục B mục 12) | nơi giữ vector | — | 12 |
| Hạn chờ một lời gọi Qdrant | `vector_database.timeout`, `QDRANT_TIMEOUT` (lệnh lập chỉ mục) | 30 giây | — | chưa so | 12 |
| Số điểm ghi mỗi lô lúc lập chỉ mục | `FULL_CORPUS_BATCH_SIZE` | 64 | chỉ ảnh hưởng tốc độ lập | chưa so | 12 |
| Ngưỡng coi hai vector là như nhau khi kiểm lệnh cập nhật riêng | `NGUONG_VECTOR_NGHIA` | 0,00001 | lệnh kiểm so vector mới tính với vector đã cất | chưa so | **chưa có bài** (12 giảng lệnh cập nhật riêng) |

## 2. Trả lời một câu hỏi (chặng 3, bài 13–16)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Số ứng viên lấy theo nghĩa | `candidate_pool` (bộ tìm) | 30 | đầu vào cho bước chấm từ khoá và trộn | đã đo 100: mất đoạn đúng ở 1 câu, bỏ | 10, 13 |
| Hằng số trộn RRF | `rrf_k` (bộ tìm) | 60 | giữ chênh lệch giữa các hạng đầu không quá lớn | đã thử 2, 10, 30: không bản nào qua điều kiện | 13 |
| Số đoạn đưa model ở lần tìm đầu | `full_corpus_generation.max_context_documents` **[khoá]** | 10 | model thấy nhiều chỗ của kho hơn | đã so 5 với 10 (10 thắng); đã thử 15 đoạn, cả mục, cả bài: không khá hơn | 13, 15 |
| Đoạn thêm mỗi vế hỏi (tin nhiều ý) | `SO_DOAN_MOI_VE` | 2 | vế phụ có đoạn của nó trong ngữ cảnh | đếm 0 đồng 2, 3, 4 đoạn: cùng kết quả | 13, 23 |
| Số vế được tìm riêng tối đa | `TRAN_SO_VE_TIM` | 6 (thêm nhiều nhất 12 đoạn) | 65 tin nhiều ý của ba lượt mốc: nhiều nhất 6 vế | chưa so | 23 |
| Số phần tối đa của một câu tìm gộp do model viết | `TRAN_PHAN_CAU_TIM` | 3 (mỗi phần 2 đoạn ⇒ thêm nhiều nhất 6 đoạn mỗi lần tìm của model; phần dưới 6 ký tự bỏ); từ 14:47 22/11 | câu tìm "A và B" kéo được đoạn của từng nơi | chưa so | 23 |
| Hạn giờ phần viết của một lượt | `full_corpus_generation.timeout_seconds` **[khoá]** | 45 giây | quá hạn thì báo lỗi, không treo | chưa so | 6, 15, 33 |
| Giới hạn độ dài ngữ cảnh | (không có) | không có; mọi đoạn vào nguyên vẹn | — | trần 16.384 token có tới 19/11, bỏ vì chưa lần nào chạm (dài nhất 6.233) | 15 |
| Bộ đếm token | `full_corpus_generation.token_encoding` **[khoá]** | `o200k_base` | bộ đếm token của OpenAI, nạp lúc khởi động cho bước dựng ngữ cảnh | — | **chưa có bài** |
| Tên biến khoá OpenAI | `full_corpus_generation.api_key_env` **[khoá]** | tên một biến môi trường (không phải khoá) | đường gpt-6-luna và người chấm đọc khoá ở đó | — | **chưa có bài** (bài 37 giảng khoá nói chung) |
| Câu nguồn dài nhất được chép vào dòng "tạm ngừng…" | `luu_y_nguon.MAX_CAU` | 400 ký tự | dài hơn thì không chép (không cắt giữa câu) | chưa so | 15 (chỉ nhắc tính năng) |
| Nhóm bài nhận dòng "có thể đã thay đổi" | `NOTICE_SOURCE_PREFIXES` | bài vé, bài địa điểm, bài lễ hội, và đúng một bài "Lưu trú ở Huế" | giá và giờ có thể đổi mà kho chưa sửa | — | 16 |
| Giá model viết (mỗi 1 triệu token) | `llm/pricing.PRICES_PER_M` | Claude Sonnet 5.5: vào 2 · đọc đệm 0,1 · ghi đệm 2,5 · ra 10 USD. gpt-6-luna: vào 0,10 · đọc đệm 0,01 · ghi đệm 0,125 · ra 0,50 USD | sổ số đo tính tiền từng lần gọi; giá Claude "ghi sổ, chưa đối chiếu hoá đơn" | — | 15, 34 |

## 3. Trợ lý hỏi đáp (chặng 5, bài 21–23)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Số lần model được tự tìm kho | `assistant.so_lan_tim_kho` (mặc định `MODEL_SEARCH_LIMIT` = 2 khi cấu hình không ghi) | 3 từ 14:47 22/11; trước là 2 (lần tìm đầu của chương trình không tính) | ở tin dài nhiều ý, khi câu tìm gộp đã được tách, lần thứ ba tới được ý còn lại; tin thường, tin kho thiếu không dùng tới | đã đo 1: bỏ; đã đo 3 đứng riêng (21/11 hai model: như cũ; trưa 22/11: không có ích); 3 cùng tách câu tìm (22/11, một tin 4 ý: đủ hai ý 1 ⇒ 6 trên 6): mở. Áp chung cả hai model, model cũ chưa đo | 21, 23 |
| Trần vòng gốc của lượt có công cụ | `assistant.so_vong_cong_cu` (mặc định `ASSISTANT_MAX_TURNS`) | 5 từ 14:47 22/11 (trước là 4); +1 cho mỗi công cụ ngày, khoảng cách, gần một điểm, liệt kê bài được đưa ở lượt đó. Công cụ liệt kê bài được đưa ở mọi lượt, nên trần thực tế mỗi lượt là từ 6 vòng trở lên | mỗi lần tìm thêm ăn một vòng nên nâng cùng số lần tìm (số 4 cũ: 2 lần tìm + 1 lần bị nhắc + 1 vòng viết, đặt từ khi còn dòng nhắc) | đã thử 8 vòng (bài 21) | 21 |
| Hạn giờ bước xếp loại câu | `assistant.router_timeout_seconds` | 10 giây; quá hạn hoặc lỗi ⇒ coi là "về Huế" | không để tin bị treo ở bước đầu | chưa so | 22 |
| Đọc nốt khi người dùng bấm Dừng | `STREAM_DRAIN_SECONDS` | 0,5 giây | sau lệnh huỷ, đọc nốt chừng này rồi thôi | chưa so | **chưa có bài** |
| Số lượt giữ mỗi cuộc trò chuyện | `api/conversations.MAX_TURNS` | 3 | trợ lý nhớ 3 câu hỏi gần nhất | chưa so | 23 |
| Hết hạn cuộc trò chuyện | `api/conversations.TTL_SECONDS` | 30 phút từ lượt cuối | — | chưa so | 23, 35 |
| Số cuộc giữ cùng lúc | `api/conversations.MAX_CONVERSATIONS` | 500; quá thì bỏ cuộc cũ nhất | bộ nhớ máy chủ có giới hạn | chưa so | 23, 35 |
| Cắt câu trả lời liền trước | `api/conversations.CAT_LOI_TRUOC` | 4.000 ký tự | mục cuối của danh sách dài không bị mất | đã dùng 1.200 (20/11); với Claude 2 / 7 câu dài hơn 1.200 ⇒ nâng | 23 |
| Số tên nơi nhớ từ lượt trước | `ten_goi_y.TOI_DA` | 5 | dòng ghi chú tên nơi đã trích | chưa so | 23 |

## 4. Công cụ do chương trình tính (bài 24)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Năm đổi âm ↔ dương được | `ngay_lich.NAM_MIN`, `NAM_MAX` | 1976–2100 | trước 1976 hai miền dùng lịch âm khác nhau | — | 24 |
| Số ngày âm tính sẵn mỗi lượt | `ngay_lich.SO_NGAY_AM_TOI_DA` | 6 | — | chưa so | 24 |
| Số lần gọi công cụ ngày mỗi câu | (lõi trợ lý) | 2 | lần thứ ba nhận dòng "hãy viết câu trả lời" | chưa so | 24 |
| Số ngày dự báo thời tiết | `thoi_tiet.SO_NGAY` | 7 (hôm nay + 6 ngày) | — | — | 24 |
| Hạn giờ gọi dịch vụ thời tiết | `thoi_tiet.TIMEOUT_S` | 3 giây | — | chưa so | 24 |
| Giữ số dự báo | `thoi_tiet.CACHE_S` | 30 phút | dự báo không đổi từng phút | chưa so | 24 |
| Ngưỡng dòng "nếu mưa" | `thoi_tiet.NGUONG_MUA` | khả năng mưa từ 60 % | — | chưa so | 24, 28 |
| Luật số phút đi đường | `khoang_cach.HE_SO_OSRM`, `PHUT_CONG` | 1,25 × phút của dịch vụ chỉ đường + 5 | khớp 6 / 6 cặp đối chiếu có nguồn công khai | sàn 40 km/h: bỏ | 24 |
| Số lần gọi khoảng cách / gần một điểm mỗi câu | (lõi trợ lý) | 3 mỗi loại | — | chưa so | 24 |
| Bán kính "gần" | `gan_diem.KM_TOI_DA` | 2 km đường chim bay | cùng ngưỡng của mục quán ăn trong thẻ lịch | chưa so | 24 |
| Số kết quả "gần" tối đa | `gan_diem.SO_TOI_DA` | 5 | — | chưa so | 24 |
| Độ dài tối đa của chữ giờ quán | `quan_lich.GIO_TOI_DA` | 160 ký tự; qua cùng phép kiểm chữ sạch như tên quán | chữ giờ đi thẳng tới model và người dùng nên phải sạch như tên quán; kiểm lúc bật máy chủ (một dòng sai ⇒ máy chủ không bật), kể cả khi `gan_diem_gio` tắt; chỉ được in khi `gan_diem_gio` mở (phụ lục B). Dòng dài nhất của bảng bản 4: 72 ký tự | — | 24 |
| Khoảng ngày hỏi lễ hội dài nhất | `su_kien.KHOANG_TOI_DA` | 62 ngày | dài hơn thì danh sách thành "cả năm" | chưa so | 24 |
| Liệt kê bài: số bài tối đa một kết quả | `liet_ke.TOI_DA_DONG` | 40 (nhiều hơn ⇒ dòng "còn k bài nữa") | — | chưa so | **chưa có bài** (24 chỉ nhắc tính năng) |
| Liệt kê bài: dòng làm chứng | `liet_ke.DONG_DAI_NHAT` | 220 ký tự | — | chưa so | **chưa có bài** |
| Liệt kê bài: số lần mỗi câu | `liet_ke.SO_LAN_MOI_LUOT` | 2 | — | chưa so | 24 |
| Liệt kê bài: cụm từ | `liet_ke.TOI_DA_CUM_TU`, `CUM_TU_DAI_NHAT` | tối đa 3 cụm, mỗi cụm ≤ 40 ký tự | — | chưa so | **chưa có bài** |
| Bảng khoảng cách | `assistant.khoang_cach_bang` | bảng bản 1: 40 điểm có toạ độ, 1.560 cặp (riêng tư) | công cụ khoảng cách và "gần một điểm" tra ở đây | — | 24, 27, 28 |
| Bảng sự kiện theo ngày | `assistant.su_kien_bang` | bản 2: 27 dòng chép từ kho (riêng tư) | — | — | 24 |

## 5. Tra web (bài 25)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Hạn giờ một lần gọi dịch vụ tìm web | `assistant.tra_web_timeout_seconds` | 5 giây; một lần, không gọi lại | — | chưa so | 25 |
| Số kết quả lấy về | `tra_web.MAX_RESULTS` | 5 | — | chưa so | 25 |
| Độ dài câu gửi đi | `tra_web.MAX_QUERY_CHARS` | 120 ký tự | — | chưa so | 25 |
| Cắt tiêu đề / đoạn trích | `MAX_TITLE_CHARS`, `MAX_SNIPPET_CHARS` | 200 / 400 ký tự | — | chưa so | 25 |
| Giá một lần tìm web | `SERPER_USD_PER_CALL` | 0,001 USD | sổ số đo tính tiền | dịch vụ Exa: đã thử 12/11, không dùng | 25 |
| Hạn giờ lần viết mục web | (dùng hạn viết chung) | 45 giây riêng, không chung đồng hồ với các vòng của trợ lý | — | chưa so | 21, 25 |

## 6. Hỏi bằng ảnh (bài 26)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Danh sách tên được đoán | `anh.danh_sach` | 55 nơi / món từ 16:57 23/11 (52 từ 16:47; trước đó 42): 42 mục chủ dự án duyệt 05/11 giữ nguyên ở đầu, thêm 13 mục qua lượt ảnh thật 23/11 (riêng tư) | đầu ra chỉ được là mã trong danh sách | bản 42, bản 52: lùi được bằng dòng này | 26 |
| Dấu "xác nhận trước" | `xac_nhan_truoc` (trong mục của `anh.danh_sach`) | 3 mục: Cầu Trường Tiền, Nhà thờ chính tòa Phủ Cam, Chùa Từ Hiếu | model đoán một mình tên đó ⇒ giao diện hiện thẻ chọn, không tự hỏi | — (từ 16:57 23/11) | 26 |
| Dung lượng ảnh tối đa | `anh.max_bytes` | 10 MB | chặn trước khi đọc thân ảnh | — | 26, 37 |
| Số điểm ảnh tối đa | `anh.max_pixels` | 40 triệu | chặn ảnh "bom giải nén" trước khi giải mã | — | 26, 37 |
| Cạnh dài sau thu nhỏ | `anh.canh_dai` | 1.024 điểm ảnh; JPEG chất lượng 85, bỏ thông tin kèm ảnh | rẻ: khoảng 922 token cho ảnh 1.024 × 768 | chưa so | 26 |
| Hạn giờ một lần nhìn ảnh | `anh.timeout` | 20 giây; quá ⇒ "không đoán được", không gọi lại | đầu ra dài có thể quá 15 giây | bản đầu 15 giây | 26 |
| Số tên đoán tối đa | (lời dặn nhìn ảnh; `nhan_anh.kiem_lai`) | lời dặn xin 1–3; chương trình giữ ba mã đầu (từ 16:46 23/11 khuôn đầu ra không còn tự chặn ở 3) | 2–3 tên thì người dùng bấm chọn | vòng đầu model luôn trả 1 tên ⇒ thêm câu dặn | 26 |

## 7. Lên kế hoạch và bộ xếp lịch (chặng 6, bài 27–29)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Bảng điểm bản 2 | `assistant.lich_trinh_bang_v2` | bảng điểm bản 14 (từ 17:14 23/11): 41 điểm + 4 quán cà phê chỉ dùng buổi tối = 45 dòng, kèm thứ tự chọn buổi tối và danh sách 6 mục tối nhẹ (riêng tư); thiếu file hay cột ⇒ máy chủ không bật | bộ xếp lịch đọc bảng này | bản 34 điểm tới 15/11; bản 10 (41 điểm) tới trưa 23/11; bản 12 từ 14:56; bản 13 từ 16:38 (Chợ Đông Ba bỏ buổi tối, thêm 4 quán; khác bản 14 ở giờ ghé, thứ tự Ca Huế / phố Tây và chữ ghi chú phố Tây); lùi buổi tối có chợ: trỏ lại bảng điểm bản 12, bảng toạ độ bản 9 và bảng ảnh bản 7 (bảng ảnh mới có ảnh ba quán; nạp với bảng điểm cũ thì máy chủ không bật) | 27, 28 |
| Bảng điểm bản đầu | `assistant.lich_trinh_bang` | bản 3 (riêng tư) | chưa thấy ghi lý do còn giữ. Điều thấy được: chương trình nạp bảng này khi `lich_trinh_bieu_mau` mở; bộ xếp bản 2 đọc `lich_trinh_bang_v2` | — | **chưa có bài** |
| Ô biểu mẫu đang hiện | `assistant.len_ke_hoach_o_hien` | 8 ô: số ngày, người lớn, trẻ em, người lớn tuổi, kiểu đi, sở thích, ngày đi, hạng chỗ ở | ô dưới sàn mô phỏng thì bỏ khỏi đây | — | 5, 27 |
| Sở thích bị ẩn | `assistant.len_ke_hoach_so_thich_an` | rỗng | ẩn loại dưới sàn "≥ 50 % suất của từng lịch 2 ngày" | 13/11 lễ hội 43 % ⇒ gắn thêm nhãn có căn cứ kho ⇒ 50 % | 27 |
| Số ngày tối đa | `lich_trinh_v2.SO_NGAY_TOI_DA`, `hoi_lai.SO_NGAY_TOI_DA` | 5 | chủ dự án chốt khi duyệt thiết kế | bản đầu nhận tới "4+" | 27, 28 |
| Số sở thích tối đa | `hoi_lai.SO_THICH_TOI_DA` | 2 | hai sở thích được xét xen kẽ | bản đầu nhận 1 | 27 |
| Ngày đi xa nhất | `hoi_lai.NGAY_DI_TOI_DA` | 180 ngày từ hôm nay | chưa thấy ghi lý do. Điều thấy được: thiết kế ghi con số này | chưa so | 27 |
| Ngưỡng hiện một loại sở thích | `lich_trinh_v2.NGUONG_LOAI` | ≥ 4 điểm trong bảng | chủ dự án chốt; hiện cả 5 loại đều đủ | — | 27, 28 |
| Thời lượng tham quan | `lich_trinh_v2.PHUT` | ngắn 75 phút · nửa buổi 150 phút | — | chưa thử số phút riêng từng điểm | 28 |
| Phút đi giữa hai điểm trong buổi | `DI_CUNG_CUM`, `DI_CUM_KE` | cùng cụm 15 · cụm kề 30 · cụm khác không ghép (trừ ngày người dùng tự xin thêm điểm ở khu không liền kề, từ 17:24 23/11: số phút của bảng khoảng cách, bài 31) | — | chưa thử số từ bảng khoảng cách cho mọi lịch | 28, 31 |
| Quỹ phút một buổi | `lich_trinh_v2.QUY` | nhẹ nhàng 1 điểm · cân bằng 210 · khám phá nhiều 240 | — | luật "đi dày" cũ: bỏ (3 / 120) | 28 |
| Điểm tối đa một buổi | `lich_trinh_v2.TOI_DA_BUOI` | 2 (4 một ngày); ngày người dùng tự xin thêm sau khi xếp: đoàn thường, 3 một buổi, không tính quỹ (từ 15:38 23/11, bài 31); đoàn có trẻ nhỏ / người lớn tuổi: từ 18:00 23/11 có trần riêng, kể ở đợt sau | ba điểm ngắn đã vượt quỹ 240 | — | 28, 31 |
| Giờ bắt đầu | `lich_trinh_v2.GIO_BAT_DAU` | sáng 8:00, chiều 13:30; khám phá nhiều 7:30, 13:00 | — | bản nháp: 8:00 – 11:00, 14:00 – 17:00 | 28 |
| Chừa giờ ăn trưa | `lich_trinh_v2.NGHI_TRUA` | 60 phút | — | không chừa: 26 ngày sát giờ trên 960 cách điền | 28 |
| Ngày mưa phải xếp lại | `NGUONG_MUA`, `MM_MUA_XEP` | khả năng mưa ≥ 60 % VÀ lượng mưa ≥ 6 mm | 6 mm theo lời chủ dự án 15/11 (đầu cấp "Mưa" của quy chuẩn) | chỉ 60 %: bỏ | 28 |
| Cụm có hoạt động buổi tối | `lich_trinh_v2.CUM_TOI` | Kinh thành và bờ nam | khách đã về khu trung tâm | — | 28 |
| Thứ tự chọn buổi tối (từ 16:38 23/11) | `thu_tu_toi` trong bảng điểm | phố đi bộ Nguyễn Đình Chiểu ⇒ Bến Trăng ⇒ Ca Huế ⇒ phố Tây ⇒ Hai Bà Trưng ⇒ The TIME ⇒ cầu Trường Tiền ⇒ HANOK ⇒ MoKa; mục hợp sở thích vẫn đứng trước | khi không mục nào hợp sở thích, hoặc giữa các mục cùng hợp; có khoá riêng vì các dòng quán nằm cuối bảng — chen giữa bảng làm lệch lượt xen kẽ hai sở thích của bộ xếp ban ngày | tới 17:14 23/11 Ca Huế đứng sau phố Tây và Hai Bà Trưng (đổi để lần "đổi" đầu không rơi vào khu phố quán bar); trước 16:38: thứ tự dòng của bảng, có Chợ Đông Ba | 28 |
| Giờ in của hoạt động buổi tối | bảng điểm bản 14 | bốn quán cà phê 19:00 – 20:30 (giờ đóng cửa ở dòng phụ); cầu Trường Tiền 19:00 – 20:15; đoàn có trẻ nhỏ / người lớn tuổi: 75 phút từ giờ đầu (phố đi bộ 18:30 – 19:45, quán và cầu 19:00 – 20:15), Ca Huế giữ suất đầu | giờ ghé do nhóm ước, không phải giờ của kho (kho không ghi giờ bật đèn cầu) | tới 17:14 23/11 thẻ cầu chỉ in "Tối" | 28 |
| Câu mô tả một điểm | `CAU_MUC_TOI_DA` | 30 từ; chỉ đếm để báo, không cắt | cắt chữ model là sửa chữ người khác viết | — | 29 |
| Số đoạn kho tối đa của lượt lập / sửa lịch | `len_ke_hoach.MAX_DOAN` | 35 (từ 17:22 23/11; trước 25); một đoạn mỗi điểm | (3 điểm × 2 buổi + 1 tối) × 5 ngày = lịch dày nhất bước kiểm khung cho phép, kể cả ngày người dùng xin thêm điểm | 25 (tới 17:22): lịch 5 ngày mất ngày cuối sau lệnh thêm thứ tư | 29, 31 |
| Mức suy luận lần viết câu lịch | `BIEU_MAU_REASONING` | thấp (đặt cứng) | không cần nghĩ ở việc này | đã đo ba mức: cùng kết quả | 27, 29, 33 |

## 8. Quanh một lịch (bài 30)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Bảng chỗ ở | `assistant.lich_trinh_bang_luu_tru` | bản 6: 136 cơ sở, 67 có ảnh (riêng tư) | khối "Nơi ở" | bản 3: 137 cơ sở | 30 |
| Ngưỡng chọn khu ven biển / phía tây | `luu_tru_lich.NGUONG_BIEN`, `NGUONG_TAY` | ≥ 60 % / > 50 % điểm ban ngày (phía tây thêm điều kiện không trẻ em, không người lớn tuổi) | ngày ra biển thường là đi trong ngày | — | 30 |
| Số cơ sở theo hạng | `luu_tru_lich.SO_THEO_MUC` | 2 (4–5 sao) · 2 (2–3 sao) · 1 (1 sao); tối đa 5 | để khách tự chọn hạng | trước: xếp theo tên làm 5 sao không bao giờ hiện (0 / 6.108); đã sửa | 30 |
| Bảng quán | `assistant.lich_trinh_bang_quan` | bản 4 (23/11): 467 quán (kho 41, dữ liệu mở 4, bản đồ mở 422; riêng tư); 6 quán kho mang dấu bữa không hợp (có từ bản 3; đánh dấu khi giờ trong bài riêng của quán không phủ khung trưa 11:00 – 13:30 hay tối 18:00 – 20:30); 30 quán kho mang dòng giờ chép từ kho, chỉ công cụ "gần một điểm" đọc | quán mỗi bữa và công cụ "gần một điểm"; bộ chọn quán của lịch bỏ quán khỏi bữa mang dấu | bản 1 còn một quán đã đóng cửa; bản 2 chưa có dấu bữa (766 / 960 tổ hợp có quán lệch bữa) | 24, 30 |
| Số quán mỗi bữa / bán kính | `quan_lich.SO_QUAN`, `KM_TOI_DA` | ≤ 2 quán; ≤ 2 km chim bay, cùng cụm | — | không giới hạn: bỏ | 30 |
| Bảng ảnh | `assistant.lich_trinh_bang_anh` | bản 7: 40 / 41 điểm có ảnh (riêng tư) | ảnh từng điểm | bản 6, bản 7 đổi hai ảnh | 30 |
| Bảng toạ độ | `assistant.lich_trinh_toa_do` | bản 9: 41 dòng, 40 có vị trí (riêng tư) | ghim bản đồ, quán gần, "gần một điểm" | bản cũ 18 điểm | 30 |
| Bề rộng bố cục khi in lịch | luật in của `frontend/src/lkh.css` (`html.in-lich body { min-width }`) | 860 px từ 16:58 23/11 (trước 1.019 px) | trình duyệt thu vào phần in của A4 (688 px) còn 80 % ⇒ câu tả 9,3 pt trên giấy (trước 7,8); chủ dự án chọn "khoảng 9–10 pt" | 840, 880, 900 px: in thử, đều 3 trang; 1.019: 2 trang | 30 |
| PowerPoint: điểm tối đa một trang ngày | `lich_pptx.MUC_MOI_TRANG` | 5 | — | chưa so | 30 |
| PowerPoint: câu tả một điểm | `lich_pptx.CAU_TOI_DA` | 170 ký tự (câu thật dài nhất đã thấy: 109) | — | chưa so | 30 |
| Lượt tải PowerPoint mỗi địa chỉ mạng | `gioi_han.TRAN_TAI_FILE` | 30 mỗi ngày, chỉ khi bộ giới hạn lượt bật | một lịch thường tải một hai lần | — | 30, 37 |
| Hạn giữ lịch đã lưu | (theo cuộc trò chuyện) | 30 phút từ lượt cuối | — | — | 27, 31 |

## 9. Sửa lịch bằng lời (bài 31)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Hạn giờ lần hiểu ý sửa lịch (đường Claude) | `full_corpus_generation.bedrock.sua_lich_timeout_seconds` | 10 giây (đường gpt-6-luna dùng chung hạn xếp loại) | lâu nhất đã đo ở mức suy luận cao 7,1 giây | — | 31, 33 |
| Mức suy luận lần hiểu ý sửa lịch | `full_corpus_generation.bedrock.reasoning_sua_lich` | `high` | — | đã đo 21/11 (model đang chạy): lệnh khó đúng 5 / 6 cao, 2 / 6 thấp, 0 / 6 vừa | 31, 33 |
| Số lệnh model trả / chương trình áp mỗi lượt | `sua_lich_v2.MAX_HANH_DONG`, `MAX_AP` | ≤ 3 / ≤ 2; lệnh thứ 3 ⇒ "Chưa làm" | — | chưa so | 31 |
| Số lựa chọn trên thẻ chọn | `sua_lich_v2.MAX_LUA_CHON` | ≤ 3 + "Bỏ điểm này" | — | chưa so | 31 |
| Trần một buổi của ngày dày (ngày người dùng tự xin thêm điểm khi sửa lịch, từ 15:38 23/11, đoàn không có trẻ nhỏ / người lớn tuổi; đoàn đó từ 18:00 23/11 có trần riêng, kể ở đợt sau) | `TOI_DA_BUOI + 1` trong `lich_trinh_v2.kiem_khung_v2` | 3 điểm (thường: 2), kể cả kiểu "nhẹ nhàng"; không tính quỹ phút | chưa thấy ghi lý do; trần thường cộng một | — | 31, 28, 29 |
| Buổi sáng của ngày dày kết muộn nhất | `lich_trinh_v2.GIO_KET_SANG_DAY` | 13:30 | bữa trưa không bắt đầu sau 13:30; không có trần này thì có buổi sáng ba điểm 7:30 – 14:15 | không trần: 340 thay vì 319 / 1.116 lệnh làm được (bảng điểm trước 16:38 23/11) | 31, 29 |
| Buổi chiều của ngày dày kết muộn nhất | `lich_trinh_v2.GIO_KET_CHIEU_DAY` | 18:00 | sau đó là bữa tối và hoạt động tối | — | 31, 29 |
| Nghỉ trưa giữa hai buổi của ngày dày | `lich_trinh_v2.NGHI_TRUA` | ≥ 60 phút; buổi chiều lùi theo buổi sáng | cùng mốc 60 phút của bộ xếp (bài 28) | — | 31, 29 |
| Chặng sang khu không liền kề dài nhất (lệnh thêm, từ 17:24 23/11) | `lich_trinh_v2.TRAN_PHUT_KHU` | 60 phút | chú thích chương trình: giữ 907 / 916 lệnh làm được trên 108 lịch; chặng dài nhất của bảng 130 phút (người đọc code đếm sau khi bù cặp thiếu: 140) | không trần: 916 lệnh (theo chú thích); trần khác 60: chưa thấy ghi | 31, 29 |
| Nghỉ trưa của ngày sang khu | `lich_trinh_v2._nghi_trua` | 60 phút ăn + trọn số phút của chặng qua bữa trưa | lượt trình duyệt 23/11: luật "60 phút cộng phần vượt 30" in ra lịch chỉ còn 30 phút ăn | luật cũ đó: bỏ (15:20 23/11, trên nhánh) | 31 |
| Điểm thiếu trong bảng khoảng cách (ngày sang khu) | `lich_trinh_v2.bu_phut_khu` | lấy chặng dài nhất đã biết giữa hai khu đó (ước dư) | 1 / 37 điểm ban ngày (Không gian lưu niệm Lê Bá Đảng) không có toạ độ; thiếu thì lệnh bỏ kế tiếp kẹt (1 / 2.752 lệnh) | — | 31 |
| Số tên nêu trong câu báo xếp lại | `sua_lich_v2.MAX_TEN_XEP_LAI` | 6; nhiều hơn chỉ nêu số điểm | đổi sở thích ở lịch 5 ngày từng ra 27 tên | chưa so | **chưa có bài** |

## 10. Máy móc bên dưới (chặng 7, bài 33–38)

| Tham số | Tên | Giá trị đang chạy | Dùng để làm gì | Đã thử giá trị khác chưa | Bài |
|---|---|---|---|---|---|
| Model của đường OpenAI | `full_corpus_generation.model` **[khoá]** | `gpt-6-luna` | chỉ đọc khi chọn đường OpenAI; người chấm của bộ đo luôn là model này | — | 33 |
| Model và vùng của Bedrock | `full_corpus_generation.bedrock.model`, `.region` | Claude Sonnet 5.5 · Singapore | model viết đang chạy | đã chạy cả hai model | 33 |
| Trần chữ đầu ra của Claude | `full_corpus_generation.bedrock.max_tokens` | 128.000 | trường bắt buộc; để mức tối đa = coi như không trần (lời chủ dự án 21/11) | không đặt nhỏ hơn | 15, 33 |
| Mức suy luận mặc định của Claude | `full_corpus_generation.bedrock.reasoning_default` | `high` (từ 21/11, mức cuối chọn sau lượt đo) | cho mọi lời gọi không tự đặt mức | đã đo bốn mức trên 66 câu | 33, 34 |
| Tên biến trỏ tới file khoá Bedrock | `full_corpus_generation.bedrock.creds_file_env` | tên một biến môi trường; đường dẫn không ghi vào repo | — | — | 33, 37 |
| Bộ nhớ câu trả lời: hạn | `api/cache_tra_loi.SONG_GIAY` | 24 giờ | — | chưa so | 34 |
| Bộ nhớ câu trả lời: trần | `api/cache_tra_loi.TRAN_SO_MUC` | 500 câu | — | chưa so | 34 |
| Câu hỏi dài nhất | `ChatRequest.query` | 500 ký tự (chặn ở cả giao diện và máy chủ) | — | — | 5, 37 |
| Sổ số đo | `config/logging.yaml` | 10 MB mỗi file, giữ 3 file cũ | — | — | 34 |
| Sổ đánh giá lượt (khi được gọi) | `api/feedback.MAX_TURNS` | 2.000 lượt trong bộ nhớ; bỏ lượt cũ nhất | — | chưa so | **chưa có bài** (35 nhắc đường gọi) |
| Trang theo dõi: số ngày | `api/theo_doi.SO_NGAY` | 14 | — | — | 34 |
| Trang theo dõi: khoá | `KHOA_DAI_TOI_THIEU`, `SAI_TOI_DA`, `KHOA_TAM_GIAY` | khoá ≥ 16 ký tự; 5 lần sai liền ⇒ khoá 15 phút | dò khoá 16 ký tự ở tốc độ này là vô vọng (lý do ghi trong chương trình) | — | 37 |
| Cổng của máy chủ | `CONG_SERVER` (lệnh cập nhật riêng) | 8010 | lệnh cập nhật riêng thử nối cổng này; còn nối được (máy chủ đang chạy) thì dừng, chưa ghi gì | — | 12, 36 |

## 11. Tham số KHÔNG bài nào nhắc (để bổ sung)

Soát bằng cách tìm tên dòng, tên hằng và con số trong các bài đã có ở thư mục giáo trình (1–38).

**Có trong file cấu hình:**

| Tham số | Giá trị | Bài hợp nhất để thêm |
|---|---|---|
| `full_corpus_generation.token_encoding` | `o200k_base` [khoá] | bài 15 (bộ đếm token, nạp lúc khởi động) |
| `full_corpus_generation.api_key_env` | tên biến khoá OpenAI [khoá] | bài 33 hoặc 37 |
| `assistant.lich_trinh_bang` | bảng điểm bản đầu (bản 3) | bài 27 (vì sao còn nạp khi bộ xếp đã dùng bản 2) |
| `full_corpus.knowledge_base.root_dir` | thư mục kho | bài 7 (nhắc nội dung, không nhắc tên dòng — đủ để tra) |

**Hằng số trong chương trình:**

| Hằng | Giá trị | Bài hợp nhất để thêm |
|---|---|---|
| `STREAM_DRAIN_SECONDS` | 0,5 giây đọc nốt khi bấm Dừng | bài 5 hoặc 35 |
| `liet_ke.TOI_DA_DONG`, `DONG_DAI_NHAT`, `TOI_DA_CUM_TU`, `CUM_TU_DAI_NHAT` | 40 bài · 220 ký tự · 3 cụm · 40 ký tự | bài 24 (mục công cụ liệt kê bài) |
| `sua_lich_v2.MAX_TEN_XEP_LAI` | 6 tên | bài 31 |
| `api/feedback.MAX_TURNS` | 2.000 lượt | bài 35 |
| `NGUONG_VECTOR_NGHIA` | 0,00001 | bài 12 (lệnh kiểm cập nhật riêng) |

<details>
<summary>Nguồn (để giữ phụ lục đúng — anh không cần đọc)</summary>

- Giá trị trong file cấu hình: `backend/config/settings.yaml`, đọc 13:20 22/11/2026 trên cây chính (HEAD `f359d89f`; lần sửa cuối của file `e4e06f9d`) [code]. Hai dòng `so_lan_tim_kho` (3), `so_vong_cong_cu` (5) đọc lại 15:09 22/11/2026 trên main `2ddd6dc2` (lần sửa cuối của file `ca25c4fe`) [code]. Hai khoá này chỉ bị kiểm KIỂU (số nguyên ≥ 1) trong `validate_phase6_settings`, không bị khoá giá trị ⇒ 8 giá trị [khoá] vẫn đúng (đọc lại cùng giờ) [code].
- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml`; hằng `TRAN_PHAN_CAU_TIM` trong `backend/llm/assistant.py` [code; số đo: đã chạy, phiên đo; người viết không chạy lại].
- Dấu [khoá]: `backend/core/settings_loader.py` hàm `validate_phase6_settings` (`model`, `api_key_env`, `token_encoding`, `timeout_seconds`, `max_context_documents`; cùng hàm khoá `candidate_id`, `retrieval_treatment`, `reranker` ở phụ lục B) [code].
- Hằng số: `backend/retrieval/full_corpus.py` (`candidate_pool=30`, `rrf_k=60`, `fused[:10]`); `backend/scoring/bm25.py` (`K1`, `B`); `backend/embedding/full_corpus.py` (`DENSE_MODEL_SPECS`, `prepare_query`); `backend/vectorstore/points.py`; `backend/ingestion/full_corpus_pipeline.py`, `kiem_cap_nhat_rieng.py`, `cap_nhat_rieng.py`; `backend/ingestion/chunking/full_corpus_chunker.py` (`ConditionManager`); `backend/llm/assistant.py` (`MODEL_SEARCH_LIMIT`, `STREAM_DRAIN_SECONDS`, `NOTICE_SOURCE_PREFIXES`, `SO_DOAN_MOI_VE`, `TRAN_SO_VE_TIM`, ngưỡng 2 / 3 lần ở các công cụ ngày, khoảng cách, gần một điểm); `generator_openai_full_corpus.py` (`ASSISTANT_MAX_TURNS`, `BIEU_MAU_REASONING`); `pricing.py`; `ngay_lich.py`; `thoi_tiet.py`; `khoang_cach.py`; `gan_diem.py`; `su_kien.py`; `liet_ke.py`; `tra_web.py`; `nhan_anh.py` (JPEG 85); `lich_trinh_v2.py`; `len_ke_hoach.py`; `hoi_lai.py` (các trần biểu mẫu, dùng ở `api/routes/cong.py`); `luu_tru_lich.py`; `quan_lich.py`; `luu_y_nguon.py`; `ten_goi_y.py`; `sua_lich_v2.py`; `backend/api/conversations.py`; `cache_tra_loi.py`; `feedback.py`; `theo_doi.py`; `gioi_han.py`; `lich_pptx.py`; `routes/chat.py` (`ChatRequest`); `backend/config/logging.yaml` [code].
- Cột "Đã thử giá trị khác chưa": các bảng "Cấu hình đang chạy" của bài 8, 10–16, 21–31, 33–35, 37 (đã qua lượt đối chiếu riêng của từng bài) và `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` dòng 6–7 (100 ứng viên) [chép]. Các dòng ghi "chưa so" không có trong các bảng đó: người viết phụ lục đã tìm tên hằng và con số trong các bài và bảng tổng, không thấy phép thử [đã chạy grep].
- Đợt trưa 23/11/2026: hàng "Bảng quán" chép từ bài 30 bảng "Cấu hình đang chạy" hàng `lich_trinh_bang_quan` và "Chi tiết để tra" (khung bữa 11:00 – 13:30 / 18:00 – 20:30), bài 24 hàng `gan_diem_gio`; người gom đọc lại `backend/config/settings.yaml` dòng 130 (`bang_quan_lich_v4.json`, bản 4 = bản 3 + `gio_kho` cho 30 quán kho) và `backend/llm/quan_lich.py` dòng 59 (`GIO_TOI_DA = 160`) trên main `0367e775`, 12:25 23/11 [code]. Dòng `gan_diem_gio` (bật / tắt) ở phụ lục B. Khung bữa là của lần dựng bảng, không phải hằng số của chương trình.
- 6 mm theo lời chủ dự án 15/11: chú thích tại `MM_MUA_XEP` trong `lich_trinh_v2.py` [code].
- Cột "Bài": tìm tên dòng cấu hình, tên hằng và con số trong các bài đã có ở thư mục giáo trình, 13:20–13:28 22/11/2026 [đã chạy].
- Các mục mới đã qua một lượt đối chiếu độc lập (một agent khác chỉ đọc, 22/11/2026), các dòng sai / lệch đã sửa lúc 14:17: `data/hoc_cung_D/kiem/muc_moi_02_07_11_va_phu_luc.md` [riêng tư]. Trần vòng cộng 1 cho mỗi công cụ được đưa: `backend/llm/generator_openai_full_corpus.py` (`max_turns_for`); công cụ liệt kê bài đưa ở mọi lượt khi tính năng mở: `backend/llm/assistant.py` (`_lich_extra`) [code].

- Lượt áp cuối (13:25 23/11/2026; biên bản `data/hoc_cung_D/kiem/dot_2311_trua_k2_phu_luc_kiem.md` hàng 37 [riêng tư]): `backend/llm/quan_lich.py` `nap_bang_quan` (docstring "Lúc khởi động (cờ `quan_lich`) … Sai một dòng ⇒ không khởi động"; vế `gio_kho` dùng `GIO_TOI_DA` và `_ten_sach`, không phụ thuộc `gan_diem_gio`) [code, đã mở main `a3938538`]; in giờ: `backend/llm/gan_diem.py` `_chu_gio(q) if in_gio` [code]. 72 ký tự: người áp đếm `len(gio_kho)` trên `data/phase_9/lich_trinh/bang_quan_lich_v4.json` (72 ký tự, 86 byte); chú thích code ghi "81" — không khớp số đếm, chưa rõ đếm theo cách nào [riêng tư; tự đếm].
- Đợt cuối chiều 23/11/2026 (16:55, người gom phụ lục): bốn hàng ngày dày ở mục 9 chép từ bài 31 bảng "Cấu hình đang chạy" (hàng "trần một buổi của ngày dày", "buổi sáng của ngày dày kết muộn nhất", "buổi chiều…", "nghỉ trưa…") và bài 29 bảng "Năm nhóm mã lỗi" hàng độ dày; tên hằng `GIO_KET_SANG_DAY`, `GIO_KET_CHIEU_DAY`, `TOI_DA_BUOI`, `NGHI_TRUA` và vế `TOI_DA_BUOI + (1 if day else 0)` trong `kiem_khung_v2`: người gom đọc `git show origin/main:backend/llm/lich_trinh_v2.py` dòng 33–36, 584 (nhánh chính `afeb0e8c`, 16:54 23/11) [code]. Hàng "Điểm tối đa một buổi" (mục 7) chép bài 28 bảng "Cấu hình đang chạy" hàng "số điểm tối đa" [chép từ bài].
- Đồng bộ 17:10 23/11/2026 (người gom phụ lục, lượt hai): sau biên bản kiểm `data/hoc_cung_D/kiem/dot_2311_chieu2_k1_kiem.md` [riêng tư] và lượt ÁP của hai agent viết, các hàng của đợt cuối chiều chép lại theo CÂU HIỆN TẠI của bài 31, 26, 7, 4, 28, 29, 30 (bản 16:55–17:04): mốc "bảng điểm trước 16:38 23/11" cho 319 / 1.116, 10 / 30, 16 / 31, 20 / 30 và số trên bảng đang chạy (341 / 1.143, 11 / 31, 17 / 32, 20 / 31 — "một người kiểm độc lập chạy lại, chưa có người thứ hai"); "đoàn thường" cho «…» và ngày dày; hai câu chung trước 16:21; ca 17:45 là ca 14:21 khi chợ Đông Ba còn là hoạt động tối; quán trưa (2 km, "số của sổ"); hướng "dời một điểm" thành lớp chọn chỗ của bản "sang khu"; nhãn "đo trên bản đầu, trước hai bản sửa"; hỏi bằng ảnh ("model quyết; 2 / 2 lượt", ghi chú chỉ gắn khi gõ lúc khung còn mở, mục web chỉ có câu cố định, phím Enter theo ca, "42 tên tới 16:47 23/11"); hai mảng kho (trình tự 21/11 ⇒ 23/11, câu hỏi chung ↔ dòng lẻ trong kho) [chép từ bài]. Mốc của đợt theo lời phiên D: khớp hệ thống 16:21 23/11; các bản gộp từ 16:38 chưa viết. Bảng từng hàng: báo cáo `data/hoc_cung_D/viet/dot_2311_chieu2_g1_phu_luc.md` mục "ĐỒNG BỘ" [riêng tư].

- Đợt đầu tối 23/11/2026 (người viết của đợt, 17:33): ba hàng sửa / hai hàng mới chép bài 26 "Cấu hình đang chạy" (danh sách, dấu xác nhận trước, số tên tối đa) và bài 30 "Cấu hình đang chạy" (bề rộng bố cục khi in) bản đầu tối 23/11 [chép từ bài; bài đã mở code `settings.yaml` dòng `anh.danh_sach`, `nhan_anh.py`, `lkh.css`].
- Đợt tối 23/11/2026 (người gom phụ lục, 18:51; khớp hệ thống 17:35 23/11, nhánh chính `7693f0b0`): hàng bảng điểm: bài 28 "Cấu hình đang chạy" hàng `lich_trinh_bang_v2` (bản 18:32, sau áp biên bản k1b: bản 12 từ 14:56, khác giữa bản 13 và 14, lùi kèm bảng ảnh bản 7) và bài 27 hàng cùng tên (bản 10 tới trưa 23/11); phút đi: bài 28 hàng "phút đi trong một buổi"; điểm tối đa: bài 28 hàng "số điểm tối đa" (chỉ ghi mốc 18:00, không kể); thứ tự chọn buổi tối, giờ in buổi tối: bài 28 "Chi tiết để tra" gạch "Chín hoạt động tối", "Thứ tự chọn buổi tối", "Tối nhẹ" (tên khoá `thu_tu_toi`: `backend/llm/lich_trinh_v2.py` dòng 87–89 ở `7693f0b0` [code]); trần đoạn: bài 29 "Cấu hình đang chạy" hàng "trần số đoạn của lượt" + bài 31 hàng "trần đoạn kho" (`len_ke_hoach.MAX_DOAN` = (TOI_DA_BUOI + 1) × 2 × 5 + 5 ở `7693f0b0` [code]); chặng 60 phút, nghỉ trưa ngày sang khu, điểm thiếu bảng khoảng cách: bài 31 "Cấu hình đang chạy" ba hàng cùng tên (tên hàm `TRAN_PHUT_KHU`, `_nghi_trua`, `bu_phut_khu`: `git grep` trên `7693f0b0` [code]); hàng trần một buổi của ngày dày: chỉ thêm mốc 18:00 [chép bài 31 "Ý chính" gạch 3]. Không sửa hàng bảng ảnh (bản 7) và bảng toạ độ (bản 9): bài 30 còn ghi như vậy, cấu hình `7693f0b0` trỏ bảng ảnh v8 và toạ độ v10 — lệch ghi ở báo cáo người gom. Báo cáo từng hàng: `data/hoc_cung_D/viet/dot_2311_toi_g1_phu_luc.md` [riêng tư].
- Dòng Cập nhật trước (chuyển xuống 18:51 23/11/2026): "Cập nhật 17:40, ngày 23/11/2026 · hàng danh sách tên 55 + hàng dấu "xác nhận trước" + hàng bề rộng khi in (mới) + hàng số tên đoán tối đa, theo bài 26, 30 bản đầu tối · 17:10, ngày 23/11/2026 · khớp hệ thống 16:21 23/11 (51 tính năng mở, 7 tắt, kho 267 bài) + số lệnh thêm trên bảng điểm từ 16:38; chưa gồm các bản gộp khác từ 16:38 (chờ phiếu) · đồng bộ theo câu hiện tại của bài gốc sau khi hai agent viết áp biên bản kiểm độc lập · 16:55: đợt gom đầu · thêm bốn hàng của ngày dày (lệnh "thêm" vượt nhịp đi, bài 31): trần 3 điểm một buổi, sáng kết ≤ 13:30, chiều ≤ 18:00, nghỉ trưa ≥ 60 phút; hàng "Điểm tối đa một buổi" ghi ngoại lệ · 13:25, ngày 23/11/2026 · khớp hệ thống 13:25 23/11 (49 tính năng mở, 5 tắt, kho 267 bài) · lượt áp cuối: hàng độ dài chữ giờ quán · bản 12:28: bảng quán bản 4 (dấu bữa không hợp cho 6 quán, dòng giờ cho 30 quán kho); thêm hằng độ dài chữ giờ quán · bản 17:11, ngày 22/11/2026: chép từ cấu hình và chương trình lúc đó (sau bộ thay đổi mở 14:47 22/11: hai tham số của vòng công cụ đổi, thêm hằng số tách câu tìm gộp); hệ thống đổi thì phụ lục phải chép lại."
</details>
