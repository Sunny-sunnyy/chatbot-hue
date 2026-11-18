# Bản đồ dự án hue_rag — đọc trang này trước

*Cập nhật lần cuối: 10:18, ngày 18/11/2026 · trang mới: các khối hệ thống, cái gì đang chạy, đọc bài nào trước, nhóm đang làm gì.*

Trang này là **cửa vào**: đọc 5–10 phút là biết hệ thống gồm những khối nào, khối nào đang bật, và muốn hiểu sâu một khối thì mở bài nào. Mọi con số ở đây là
**số của hệ thống hôm nay**; các bài viết trước ngày 14/11 (bài 0–18) viết lúc kho còn 204 bài, nên anh sẽ gặp số nhỏ hơn ở đó, không phải lỗi.

## Bảng từ

| Tên trong trang | Tên gốc | Nghĩa ngắn |
|---|---|---|
| sổ tay | *knowledge base* | kho bài viết tự soạn — mọi thứ trợ lý được phép nói |
| Qdrant | Qdrant | cơ sở dữ liệu chuyên tìm đoạn văn theo nghĩa |
| RRF | *Reciprocal Rank Fusion* | cách trộn hai bảng xếp hạng: đoạn nào đứng cao ở cả hai bảng thì lên đầu |
| trợ lý | *agent* | chatbot biết nhờ code làm việc (tính ngày, tra thời tiết, xếp lịch…) rồi mới diễn đạt |
| lời dặn | *prompt* | đoạn chữ hướng dẫn gửi kèm cho model mỗi lần gọi |
| cờ | *feature flag* | một dòng bật / tắt một tính năng trong file cấu hình |
| p50 / p95 | *percentile* | p50: một nửa số câu nhanh hơn mức này; p95: 95 % số câu nhanh hơn mức này |
| câu thường | — | câu trả lời được ngay sau lần tìm đầu, không phải tìm thêm, không tra web |
| sổ bàn giao | *runbook* | sổ hướng dẫn từng lệnh cho người (hoặc agent) làm tiếp |
| lượt đo cuối | — | lần chấm toàn bộ trợ lý trên bản code đã đứng yên, trước khi đóng giai đoạn trợ lý |
| sàn (mức tối thiểu) | — | ngưỡng ghi trước khi đo; kết quả dưới ngưỡng thì thay đổi không được bật |
| luật ghi trước | — | tiêu chí đạt / trượt viết ra **trước** khi chạy đo, để không sửa tiêu chí theo kết quả |
| nghiệm thu | — | lượt kiểm cuối của một tính năng theo luật ghi trước, trước khi bật cho người dùng |
| sổ số đo | *log* | file ghi mỗi câu hỏi một dòng số (thời gian, tiền, đi đường nào) — không ghi nội dung câu |
| bộ câu kín | *held-out set* | bộ câu hỏi cất riêng, người làm không được xem, chỉ mở để chấm ở mốc cuối |
| chấm mù, so theo cặp | — | người chấm không biết câu trả lời nào của bản nào; hai bản trả lời cùng một câu được so trực tiếp |
| trung vị | *median* | giá trị đứng giữa khi xếp các số theo thứ tự (chính là p50) |
| bản đồ mở | OpenStreetMap | bản đồ do cộng đồng góp, dùng tự do — dữ liệu quán lấy từ đây chưa ai kiểm ngoài đời |

## Dự án trong 5 câu

1. hue_rag là **trợ lý du lịch và văn hoá Huế** trên một trang web: người dùng hỏi bằng tiếng Việt có dấu, trợ lý trả lời **chỉ từ cuốn sổ tay** (kho bài viết
   tự soạn) và ghi nguồn dưới mỗi câu, kho không có thì nói không có, giống người hướng dẫn viên tra sổ tay ở bài 0.
2. Sổ tay nay có **265 bài, cắt thành 9.436 đoạn** (tới 13/11 là 204 bài / 8.435 đoạn), cất trong **Qdrant**.
3. Mỗi câu hỏi: model **xếp loại câu**, code **tìm 10 đoạn** hợp nhất, model **gpt-6-luna** đọc rồi viết, code **kiểm nguồn** rồi mới hiện; thiếu thì trợ lý
   **tự tìm thêm** tối đa 2 lần, kho vẫn không có thì **tra web một lần** và để riêng mục "chưa kiểm".
4. Việc dễ nhầm (ngày âm lịch, thời tiết, khoảng cách, xếp lịch, chọn khách sạn / quán) **code làm, model chỉ diễn đạt** — đó là phần "trợ lý".
5. Hệ thống chạy **trên máy anh**, chưa đưa lên mạng. Code đứng yên tối thứ Bảy 21/11, lượt đo cuối Chủ nhật 22/11. Trước cuối tháng 11: kế hoạch deploy
   và sổ bàn giao; **deploy chỉ bàn khi dự án xong**.

## Các khối của hệ thống

```mermaid
flowchart LR
    K["Sổ tay<br/>265 bài"] --> Q["Chia đoạn + chỉ mục<br/>9.436 đoạn trong Qdrant"]
    Q --> T["Trợ lý trả lời<br/>xếp loại · tìm · viết · kiểm nguồn"]
    T <--> C["Công cụ của trợ lý<br/>thời tiết · ngày · khoảng cách · web · ảnh"]
    L["Lên kế hoạch<br/>code xếp lịch đi – ăn – ở"] --> G["Giao diện 5 trang"]
    T --> G
```

Ngoài hình: **khối đo / chấm** đứng cạnh để kiểm mọi thay đổi, và **khối đóng gói** (Docker) để mang cả hệ thống sang máy khác.

| Khối | Nó làm gì | Đang chạy thế nào (số hôm nay) | Bài nên đọc |
|---|---|---|---|
| **Sổ tay** | Tất cả những gì trợ lý được nói: món ăn, di tích, lễ hội, nghệ thuật, đi lại / vé / chỗ ở | **265 bài** Markdown, 5 chủ đề (mốc: 204 bài tới 13/11; thêm 61 bài 14–16/11; mỗi lần ghi đều kiểm câu cũ không tụt — hai lần đầu chấm điểm, các lần sau đọc tay từng câu chạm bài mới) | 1, 22 |
| **Chia đoạn + chỉ mục** (*chunking*, *embedding*) | Cắt bài thành đoạn nhỏ, biến mỗi đoạn thành vector nghĩa (dãy số đại diện ý) và bảng từ khoá, cất vào Qdrant | **9.436 đoạn**; mỗi đoạn thành một dãy 384 con số (vector) từ model nhỏ **e5-small** chạy trên máy, 0 đồng; từ khoá **BM25** (chấm theo chữ trùng); lúc khởi động thấy kho lệch chỉ mục thì từ chối chạy | 2, 3, 4, 5 |
| **Tìm** (*retrieval*) | Chọn đoạn hợp câu hỏi | Theo nghĩa lấy 30 ứng viên ⇒ chấm lại theo từ khoá ⇒ trộn hai bảng xếp hạng (RRF) ⇒ giữ **10 đoạn**; **không xếp lại bằng model** | 6, 7 |
| **Trợ lý trả lời** | Xếp loại câu (chào hỏi / về Huế / ngoài chủ đề / khẩn cấp — loại cuối đi chung đường câu về Huế), viết bằng **gpt-6-luna**, kiểm số nguồn | Bật: xếp loại; chạy song song xếp loại với trả lời; **tìm thêm ≤ 2 lần** — đã tìm thêm đủ 2 lần thì trợ lý không được tìm nữa, phải trả lời hoặc nói không có; **nhớ 3 câu hỏi gần nhất** (không nhớ câu trả lời); câu nhiều ý | 8, 12, 13, 25 |
| **Công cụ của trợ lý** | Việc phải đúng thì code làm | Bật cả sáu: **ngày + âm lịch** (code tính) · **thời tiết** 7 ngày (Open-Meteo) · **câu bão / lũ** (model không nhận con số nào, code nối khối chỉ dẫn cố định) · **khoảng cách** hai điểm (bảng dựng sẵn, lúc chạy không gọi mạng) · **tra web** (Serper, một lần, 5 giây, mục "Từ web (chưa kiểm)") · **hỏi bằng ảnh** (model đoán tên trong danh sách 42 nơi / món, câu trả lời vẫn từ kho) | 14, 15 |
| **Lên kế hoạch** (lịch trình bản 2) + sửa lịch bằng lời | Biểu mẫu nút ⇒ code xếp lịch theo buổi; người dùng nhắn "đổi…" ⇒ model hiểu ý, code áp và kiểm | Bảng **41 điểm**; chỗ ở **136 cơ sở** (67 có ảnh); **468 quán** cho bữa ăn (phần lớn từ bản đồ mở, chưa kiểm ngoài đời); bản đồ ghim; file lịch .ics (mở được bằng Google Calendar / lịch điện thoại); lịch từ **câu gõ tự do** vẫn TẮT | 14, 23, 25 |
| **Giao diện 5 trang** | Trang chủ · Khám phá · Lên kế hoạch · Trợ lý · Giới thiệu (thêm trang Chỗ ở, chỉ mở từ ô Nơi ở của lịch) | Giao diện viết bằng React (thư viện làm trang web), dựng sẵn thành file tĩnh rồi server gửi cho trình duyệt; chữ hiện dần; câu thường: chữ đầu tiên **p50 2,10 / p95 4,32 giây** (đếm lại từ sổ số đo ngày 15/11 trên 55 câu, chủ yếu là câu thử của nhóm — chưa có người dùng thật; sàn anh đặt 3 / 5 giây ⇒ đạt) | 17, 24 |
| **Đo / chấm** | Kiểm mọi thay đổi trước khi bật | Bộ **176 câu mẫu** + bộ câu kín + bộ an toàn; Claude chấm mù, so theo cặp; sổ số đo ghi mỗi câu một dòng, không ghi nội dung | 9, 10, 11, 19 |
| **Đóng gói / deploy** | Mang hệ thống sang máy chủ thật | Gói Docker (cách đóng phần mềm vào hộp để chạy giống nhau ở mọi máy) gồm ba hộp: cửa HTTPS (nhận kết nối mã hoá từ trình duyệt) · app · Qdrant; đã chạy thử trên máy anh; **chưa deploy** | 18, 21 |

## Cái gì ĐANG chạy, cái gì TẮT hoặc đã bỏ

Mỗi tính năng của trợ lý là **một cờ**; tắt một cờ thì chỉ phần đó mất, phần khác giữ nguyên. Bảng dưới đúng với file cấu hình sáng 18/11.

| Tên người dùng thấy | Trạng thái | Vì sao (một dòng) |
|---|---|---|
| Xếp loại câu (chào hỏi / về Huế / ngoài chủ đề) | **bật** | câu chào đáp luôn, câu ngoài chủ đề từ chối lịch sự, chỉ câu về Huế đi tìm kho |
| Trả lời song song với xếp loại | **bật** | chữ đầu câu về Huế nhanh hơn 1,37 giây (trung vị 20 cặp câu, đo 04/11, so với chạy lần lượt) |
| Tìm thêm (tối đa 2 lần) + hết lượt thì dừng | **bật** | câu nhiều nguồn đủ ý hơn +1,17 điểm (thang 1–5, 18 câu, so bản không tìm thêm); 8 / 8 câu kho không có bớt được ít nhất một lần gọi model, nhanh hơn khoảng 6,7 giây cả câu |
| Nhớ 3 câu hỏi gần nhất | **bật** | câu hỏi tiếp bị từ chối nhầm 5 / 19 ⇒ 0 / 19 (so bản không nhớ) |
| Nhớ cả câu trả lời | **tắt** | bản thử từng mượn nhầm đoạn của nơi khác |
| Câu hỏi nhiều ý (ý kho có thì trả lời, ý thiếu mới ra web) | **bật** | từ 14/11 |
| Tra web khi kho từ chối · câu hỏi nối tiếp ra web | **bật** · **bật** | mục web tách riêng, code chặn link lạ / số tiền không có trong đoạn trích; câu nối tiếp: 8 / 8 nêu đúng nơi (mẫu nhỏ) |
| Thời tiết · câu bão / lũ | **bật** · **bật** (17/11) | số dự báo do code dựng; câu bão / lũ model không nhận số nào, code nối khối chỉ dẫn cố định |
| Ngày + âm lịch | **bật** | model hay tính nhầm ngày; câu theo ngày "dùng được" 27 / 28 ↔ 11 / 28 ở bản chưa có trợ lý (đo 12/11) |
| Khoảng cách hai điểm · tra sẵn khi câu nêu rõ hai nơi | **bật** · **bật** (16/11) | tra sẵn: chữ đầu p50 3,7 ⇒ 1,9 giây (13 câu, mẫu nhỏ; so lúc model tự gọi công cụ) |
| Dòng "thông tin có thể đã thay đổi" (vé, điểm đến, lễ hội, chỗ ở) | **bật** | giá / giờ có thể đổi mà kho chưa sửa |
| Hỏi bằng ảnh | **bật** | gợi ý tên kèm "có thể sai"; sai nơi 6 / 66 lượt ↔ 14 / 66 nếu lượt nào cũng trả lời thẳng (33 ảnh × 2 lượt, mẫu nhỏ) |
| Lên kế hoạch bản 2 · ảnh từng điểm · bản đồ ghim · chỗ ở · quán ăn | **bật** cả năm | bật 14/11 (bản đồ 16/11) sau nghiệm thu; chỗ ở chỉ hiện khi người dùng chọn hạng |
| Sửa lịch bằng lời · câu sửa chưa làm được ⇒ giữ lịch + câu cố định | **bật** · **bật** (17/11) | câu thường trong cuộc có lịch: chữ đầu p50 2,65 giây (20 câu) sau khi sửa tốc độ, trước đó 4,17 giây |
| Lịch trình từ câu gõ tự do | **tắt** | thử 2 lần chưa đạt luật ghi trước; chỉ dùng qua biểu mẫu nút |
| Dòng "hôm nay là ngày…" đầu mọi tin nhắn | **tắt** | không làm giảm từ chối nhầm |
| Sổ vết debug có nội dung | **tắt** mặc định | chỉ bật trên máy anh khi cần xem từng bước; bản công khai không bật |

**Đã thử rồi bỏ** (giữ hồ sơ, để kể được "vì sao không dùng"):
- **Xếp lại bằng model** (*reranking*, ba cách, thử lúc còn đưa 5 đoạn): hai model trên máy làm mất đoạn đúng 1–3 câu; để gpt-6-luna tự chọn đoạn thì 5 câu tụt, chậm
  gấp đôi, đắt gần gấp 4 (bài 7).
- **Model embedding lớn Qwen3-8B** (lớn khoảng 70 lần): mất đoạn đúng ở 3 câu, chậm khoảng 100 lần (bài 4).
- **Lấy 100 ứng viên thay vì 30**: gần như không khá hơn mà làm mất đoạn đúng ở 1 câu (bài 6). **Trả lời một phần khi thiếu bằng chứng**: làm câu ngoài kho bị
  trả lời (bài 8).
- **Tắt phần "nghĩ" của model xếp loại cho nhanh**: 2 câu an toàn bị xếp nhầm "ngoài chủ đề" (bài 17).
- **Dịch vụ web Exa** thay Serper: thử 12/11, không bật (bài 15).
- **Cho model tìm hai lần cùng lúc** và **trần tìm thêm 1 lần** (để nhanh hơn): nhanh hơn chút nhưng phạm luật an toàn — một bản để lọt câu ngoài kho, một bản từ
  chối nhầm nhiều hơn — gác (15/11).
- **Giọng nói**, so ảnh bằng embedding: dẹp, không làm trong đợt này (anh chốt 16–17/11).

## Đọc bài nào

**5 bài nên đọc trước**, theo thứ tự (cộng lại khoảng 1.000 dòng):

1. **Bài 0 — hue_rag trong 3 phút**: bức tranh người hướng dẫn viên tra sổ tay và hai giai đoạn của RAG; mọi bài sau đều quay lại hình ảnh này.
2. **Bài 5 — Qdrant**: khối anh sẽ tự bật sáng thứ Bảy 21/11; hiểu vì sao hệ thống báo lỗi và không chịu chạy khi kho lệch chỉ mục.
3. **Bài 12 — Vì sao cần trợ lý**: từ chatbot thường thành trợ lý — xếp loại câu, công cụ, và luật "phép tính thì code làm".
4. **Bài 16 — Kể đồ án và chỗ còn yếu**: cả hệ trên một hình, lượt đo giữa kỳ 12/11 (trợ lý so với bản RAG trước khi có trợ lý), bảng chỗ yếu; đây là bài để trình bày.
5. **Bài 23 — "Lên kế hoạch" bản 2**: tính năng người xem thấy nhiều nhất; cách code xếp lịch theo luật và vì sao nghiệm thu trượt rồi đạt nhờ sửa dữ liệu và ba sửa nhỏ.

**Muốn đào sâu khối nào thì đọc bài nào:**

| Khối | Bài |
|---|---|
| Sổ tay và cách thêm bài không làm hỏng trang cũ | 1, 22 |
| Chia đoạn, tên bài trên đoạn, vector + từ khoá | 2, 3, 4 |
| Qdrant và phiếu chuẩn bị | 5 |
| Tìm, xếp lại (đã bỏ) | 6, 7 |
| Viết câu trả lời và kiểm nguồn | 8 |
| Đo / chấm: bộ câu mẫu, chấm bước tìm, chấm câu trả lời, bảng mọi lần so sánh | 9, 10, 11, 19 |
| Trợ lý: xếp loại, tìm thêm, nhớ câu hỏi | 12, 13 |
| Công cụ: ngày, thời tiết, bão / lũ, khoảng cách · tra web, hỏi bằng ảnh | 14 · 15 |
| Lên kế hoạch, sửa lịch bằng lời, câu nhiều ý, chỗ ở, quán ăn, ảnh dưới câu trả lời | 23, 25 |
| Giao diện và tốc độ | 17, 24 |
| Đóng gói Docker · dữ liệu người dùng và bảo mật | 18 · 21 |
| Đồ án được làm thế nào (nhiều agent, rào bằng máy, tiền) · cách làm việc với coding agent chốt 18/11 (bảng quyền, báo cáo bốn ý, giám khảo khác hãng) | 20 · 26 |

Lưu ý khi đọc bài 0–18: số kho trong đó (204 bài, 8.435 đoạn) là số lúc viết; số hôm nay ở trang này.

## Nhóm đang làm gì, xong tới đâu

*Mục này cập nhật mỗi lần kết phiên (anh đã duyệt giữ mục này để biết ai đang làm gì — nó là ngoại lệ của luật "bài học chỉ viết việc đã xong").*
Nhóm là bốn phiên Claude Code chạy song song: A điều phối và nói chuyện với anh; B, C, E làm và kiểm chéo nhau (người viết không tự kiểm).

**Mốc sắp tới** (anh chốt theo thứ trong tuần, sáng 18/11):

| Ngày | Việc | Xong chưa |
|---|---|---|
| Sáng thứ Bảy 21/11 | **Buổi tự tay của anh** (45–60 phút): tự bật hệ thống theo sổ bàn giao mục 1–3 (bật Qdrant · dựng giao diện + chạy server · chạy test), hỏi mươi câu của chính anh, xem sổ vết debug; A ngồi cạnh, chỗ anh vấp thì sửa sổ bàn giao | chưa — trang này là bước chuẩn bị |
| Tối thứ Bảy 21/11 | **Code đứng yên**; trước đó chạy toàn bộ test một lượt trên bản chính | chưa |
| Chủ nhật 22/11 | **Lượt đo cuối** cả trợ lý (bộ câu mẫu + an toàn + ngoài chủ đề + web; trần 0,45 USD); bộ câu đã từng đo phải chạy lại vì lời dặn và nhiều cờ đã đổi sau lượt giữa kỳ | chưa |
| Khoảng thứ Hai 23/11 | Kiểm kết quả lượt cuối ⇒ **anh đóng giai đoạn trợ lý** (Phase 9) | chưa |
| Tối thứ Ba 24/11 | **Codex rồi Antigravity chạy thử thay Claude**, anh lái: đọc tài liệu từ đầu ⇒ làm theo sổ bàn giao mục 1–3 ⇒ một việc thật nhỏ ⇒ đọc kế hoạch deploy. Mục đích: thử xem cách làm việc và tài liệu có dùng được với công cụ khác không | chưa |
| Trước cuối tháng 11 | **Kế hoạch deploy** + **sổ bàn giao** đủ mục (đã có mục 0–7 và nháp mục 10 "giới hạn đã biết"; mục 8 "deploy" và mục 9 "quyết định không hỏi lại" chưa viết). Deploy chỉ bàn khi dự án xong | đang làm |

**Sáng 18/11 đã xong:**
- Sổ số đo ghi được mỗi câu chạy bằng **bản code nào**, cả khi chạy trong Docker (trước đó Docker ghi "không rõ") — một chỗ đổi nhỏ, không đổi cách trả lời.
- Bộ đo câu ngoài kho của lượt cuối có thêm cột đếm câu được tính "từ chối" **chỉ vì hết lượt tìm** (ở lượt giữa kỳ: 1 / 18 câu).
- **Soát chỗ các tính năng gặp nhau** (lần đầu làm): ra 11 điểm, đã sửa 3 — xem mục "Chỗ còn yếu" số 8.
- Trang "khi chỉ có một agent" (cách làm việc khi chỉ còn một công cụ) và bảng **quyền thường trực** cho mọi coding agent (tự làm / hỏi trước / không bao giờ) — anh
  đã duyệt, từ nay không hỏi quyền mỗi lần mở phiên.
- Ghi chép bốn khoá học + một buổi chia sẻ: B, C, E báo xong (A chưa kiểm lại).

**Đang làm:**
- **A:** trò chuyện với anh về cách làm việc với coding agent (mỗi lần một chủ đề); gộp ba bản đề xuất của B, C, E thành một.
- **B:** trang bản đồ này; kế hoạch deploy bản 3 đã viết xong, **chờ** tới khi giai đoạn trợ lý đóng mới bàn.
- **C:** soát xem các test có thật sự bắt được lỗi không (39 test đã xem, 1 test thay hẳn phần lõi bằng đồ giả — bốn hành vi nó giữ đã được chạy thật); viết trang hiện trạng ngắn cho agent.
- **E:** viết bản gộp "cách làm việc với coding agent" dùng cho mọi công cụ.
- **Chờ anh:** gói "giám khảo khác hãng" đầu tiên — một file nhóm đã soạn để anh tự gửi cho Codex / Antigravity đọc và đánh giá độc lập.

## Chỗ còn yếu đã biết

1. **Từ chối nhầm**: kho có đáp án mà trợ lý nói không có — **3 / 158 câu** (khoảng 2 %) ở lượt đo giữa kỳ 12/11, so với **13** ở bản RAG trước khi có trợ lý.
   Gốc ở **bước tìm** (đoạn đúng không lọt vào 10 đoạn). Ví dụ còn mở: hỏi quán gần chùa Thiên Mụ, kho có mà trợ lý không tìm ra — để sau lượt đo cuối.
2. **Kiểm nguồn mới kiểm số, chưa kiểm nghĩa**: code biết nguồn [3] có thật, chưa biết đoạn 3 có nói đúng điều câu trả lời viết.
3. **Ba chỗ phạm mức tối thiểu** ở lượt giữa kỳ (2 / 44 câu ngoài chủ đề bị đem đi tra web; 1 câu an toàn thiếu một điều kiện cảnh báo; 1 lượt hỏi tiếp kín bị
   máy đếm là trả lời câu ngoài kho) và hai chỉ số **vừa đúng ngưỡng** (4 câu tụt / ngưỡng 4; web 6 / 10 / ngưỡng 6) — lượt cuối Chủ nhật 22/11 có thể trượt.
4. **Câu phải tìm thêm thì chậm**: chữ đầu tiên p50 **5,78 giây**, trượt sàn 3 giây — nhưng số này chỉ từ **5 lượt** đếm được trong sổ số đo ngày 15/11, rất ít;
   câu tìm thêm + tra web chiếm khoảng 11,5 % số lượt thử. Câu thường đạt (2,10 giây).
5. **Đề toàn câu AI soạn**, chưa có câu người dùng thật; trên bộ kín điểm đủ ý thấp hơn khoảng 0,4 (thang 1–5) so với bộ quen — đo 01/11 trên bản RAG trước khi có
   trợ lý; trợ lý chưa đo lại trên bộ kín đủ — nên số đẹp còn lạc quan. Mọi giám khảo hiện đều là Claude.
6. **Chưa lên mạng**: chỉ chạy trên máy anh, một nhà cung cấp model (OpenAI); quán từ bản đồ mở trong lịch **chưa kiểm ngoài đời**.
7. **Tài liệu điều phối quá dài** (sổ việc đang mở khoảng 176 KB, sổ hiện trạng khoảng 101 KB — đo sáng 18/11) và sổ bàn giao còn thiếu mục 8–9: nhóm đánh giá đây là
   rủi ro lớn nhất khi giao cho người hoặc công cụ khác làm tiếp (anh chưa duyệt nhận định này).
8. **Chỗ các tính năng gặp nhau** (soát sáng 18/11, sau khi từng tính năng đều đã được kiểm riêng và đạt): ra **11 điểm**. Nặng nhất: câu hỏi về bão / lũ mà trợ lý
   đã dùng hết lượt tìm thì chỉ còn câu từ chối, **mất câu chỉ dẫn xem bản tin chính thức và số 112** — đã sửa; trong sổ số đo chưa lần nào thấy xảy ra (0 / 11 lượt hỏi
   về bão). Đã sửa thêm 2 điểm nhỏ; **8 điểm còn lại ghi vào sổ bàn giao như giới hạn**, trong đó hai điểm (một câu về thời tiết bị nối nhầm vào câu hỏi tiếp không về
   thời tiết, làm mất mục web) sẽ sửa chung sau lượt đo cuối. Ba điểm đã sửa đều có test; hai điểm nhỏ đã có thêm một lượt chạy thật trên server sáng 18/11 (mỗi ý mới một lượt), riêng điểm câu bão chưa đo trên hệ thống thật.

---

<details>
<summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

Bảng đối chiếu từng số / khẳng định ⇒ `file:dòng` và biên bản kiểm độc lập 93 ý (77 đúng, 4 sai, 11 lệch — đã sửa hết vào bản này): `data/ban_do_2026-11-18/NGUON.md`,
`BIEN_BAN_KIEM.md` (riêng tư). Tóm tắt:
- 265 bài / 9.436 đoạn: `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`corpus.file_count`, `corpus.chunk_count`, đọc 18/11) [đã chạy]; `session_prompt/Project_Status.md` mục 4 [Project_Status]
- Mô hình, cách tìm, 10 đoạn, không xếp lại, mọi cờ trong bảng "đang chạy": `backend/config/settings.yaml` (từng dòng ở NGUON.md) [settings]
- Bốn loại câu: `backend/llm/assistant.py`; năm trang + Chỗ ở: `frontend/src/route.js` [code]
- 41 điểm / 136 cơ sở / 468 quán / 42 tên ảnh: đếm các bảng trong `data/phase_9/lich_trinh/`, `data/anh_user_2026-11-15_ghep/`, `data/phase_10/anh/` (18/11) [đã chạy]
- Số đo (tốc độ, từ chối nhầm, giữa kỳ): `session_prompt/Project_Status.md` mục 2 + 4, `report_agent/2026-11-12_ra_khoang_cach/`, `bai_hoc/13`–`16` [số của phiên trước, chưa đo lại]
- Mốc ngày, việc sáng 18/11, soát 11 điểm: `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN SÁNG 18/11"; sổ bàn giao `guides/RUNBOOK_BAN_GIAO.md` mục 1–3, 8–10 [đã đọc 18/11]
- Cỡ hai sổ: `wc -c` 10:14 18/11 — 175.884 và 101.162 byte [đã chạy]; 0 / 11 lượt bão, 1 / 18 câu hết lượt: B đếm 18/11 [đã chạy, chưa ai tính lại]

</details>
