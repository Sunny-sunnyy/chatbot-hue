# Báo cáo cho bạn: Kho dữ liệu — sửa dữ liệu và tạo lại chỉ mục (Phase 7A2 → đợt sửa kho 27–30/10)

**Cập nhật lần cuối: 14:19 30/10/2026 — bản 6: đợt sửa kho đợt 2 đã áp vào kho và chỉ mục đã dựng lại (30/10): 123 chỗ sửa trong 40 file (204 file,
8.424 đoạn); đo "trước ↔ sau" trên 176 câu Golden + 32 câu an toàn: không làm hỏng, 0 câu nói sai điều kiện mới; nhãn đoạn đúng bản 5; 2 đáp án Golden sửa
theo bạn chọn.** Trước đó 12:09 28/10/2026 — bản 5 (đợt 1: 123 chỗ sửa / 65 file, bỏ file danh mục; không làm hỏng).
Người viết: B (bản 4–6; bản 1–3: C) · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** giữ kho tri thức Huế đúng và đảm bảo chỉ mục chatbot dùng luôn khớp kho.
- **Đang chạy cách nào (từ 30/10):** chatbot dùng chỉ mục `hue_full_corpus_7a2_e5_small_384` dựng lại trên kho đã sửa hai đợt — **204 file, 8.424 đoạn**
  (đợt 1: 8.426; trước đó 205 / 8.459). "Phiếu build" ghi dấu vân tay từng file, kho lệch thì chatbot từ chối khởi động. File "danh mục biên soạn" của nghệ thuật
  biểu diễn **không còn** trong chỉ mục (từ đợt 1).
- **Mới (30/10) — đợt 2:**
  - **Luật bạn đặt 29/10:** câu nào không chắc thì sửa theo nguồn đọc được (một session khác đọc lại khớp) hoặc làm yếu / bỏ chi tiết; không thêm khẳng định mới,
    không xóa câu cảnh báo an toàn.
  - **Đã sửa kho đợt 2:** **123 chỗ thay chữ** trong **40 file**, **20 mục**: bỏ cấp "quận" và tên phường cũ (theo nghị quyết sắp xếp, đọc nguyên văn); một mục
    cây cầu viết lại theo nguồn; 2 mục sửa theo nguồn đọc được; **11 mục làm yếu** (bỏ con số / chi tiết không chắc: giờ, khoảng cách, năm, số nhà; 2 dòng "đơn vị
    quản lý" bị xóa hẳn). 8 mục khác **không sửa** (kho đã tự rào, hoặc không mâu thuẫn thật). Kho còn **8.424 đoạn** (2 dòng bị xóa vốn là 2 đoạn riêng).
  - **Đã dựng lại chỉ mục tại chỗ** (bạn chạy lệnh xóa ở terminal B) có sao lưu đủ để quay lại. Chatbot chạy lại bình thường: kiểm sức khỏe 5 / 5, câu trong
    kho có nguồn, câu ngoài kho từ chối đúng.
  - **Đo "trước ↔ sau"** (176 câu Golden + 32 câu an toàn, chấm mù cùng lượt): **không làm hỏng** — 0 câu ngoài kho bị trả lời, 0 lỗi, 0 lỗi trích dẫn, 0 câu
    "nói chắc sai" mới; đủ ý / đúng gần như y hệt (4 câu tăng / 3 câu tụt); từ chối nhầm 13 → 12. Bộ an toàn: **0 câu nói sai điều kiện mới**, 0 câu đảo cảnh báo;
    2 câu từng sai ở lượt cũ nay không sai (sinh lại 3 lần trên kho cũ cũng không sai ⇒ "lúc có lúc không"). Câu bị làm yếu: không câu nào mất điểm đủ ý.
  - **Nhãn "đoạn đúng" bản 5:** 173 / 174 trích dẫn tìm lại nguyên văn (38 chỉ dời vị trí), 1 đổi chữ — **bạn đã duyệt**. **Golden:** quét 39 câu ⇒ **2 câu sửa
    đáp án mẫu** theo bạn chọn (bỏ tên phường cũ; thêm "khoảng" trước số nhà).
- **Đợt 1 (28/10, bản 5):**
  - **Đã sửa kho đợt 1:** **123 chỗ thay chữ** trong **65 file**, thuộc **51 mục** đã review (40 mục rà kho có căn cứ ngay trong kho + 11 chỗ tên phường cũ
    còn sót). Phần lớn là địa chỉ ghi tên phường mới, giữ tên cũ trong ngoặc (sau đợt sắp xếp đơn vị hành chính 01/07/2025); còn lại là vài con số mâu thuẫn
    giữa hai chỗ trong kho (mùa, khoảng cách, hạn vé, mốc năm…). Một mục (sửa chính file danh mục) không áp vì file đó đã bị bỏ.
  - **Đã dựng lại chỉ mục tại chỗ** có sao lưu đủ để quay lại (bản gốc 65 file, phiếu build, từ điển từ khóa, ảnh chụp Qdrant 51 MB). Chatbot chạy lại bình
    thường: kiểm sức khỏe 5 / 5, câu thử trong kho trả lời kèm nguồn, câu ngoài kho từ chối đúng.
  - **Đo chất lượng "trước ↔ sau"** (176 câu, chấm mù cùng lượt; C kiểm lại ra giống hệt): **không làm hỏng** — không câu ngoài kho nào bị trả lời, không lỗi,
    không lỗi trích dẫn, không câu "nói chắc sai" mới; điểm đủ ý / đúng gần như y hệt (4 câu tụt, 4 câu tăng); từ chối nhầm 12 → 13 (đúng mức cho phép).
  - **Nhãn "đoạn đúng" bản 4:** 172 / 174 trích dẫn tìm lại được nguyên văn; 2 trích dẫn đổi chữ — **bạn đã duyệt**. **Golden:** quét 59 câu có thể chạm phần
    sửa ⇒ **0 câu cần sửa** (bạn đã duyệt).
- **Giới hạn chính:** hai đợt làm kho **đúng hơn / thận trọng hơn** nhưng **không làm điểm tăng** — thước đo không nhạy với loại sửa này (tên phường, bỏ chi tiết
  không chắc). Vài mục vẫn chờ tra ngoài (kho đã tự rào). Kho còn thiếu vài thông tin hay được hỏi (ví dụ giờ mở cửa một điểm tham quan lớn). **Bài học kỹ thuật:**
  mã đoạn dạng "tên file + số thứ tự" bị dồn số khi xóa một dòng giữa file — đợt 2 đã thêm luật đo bù trước khi có số.
- **Chi phí:** đợt 2 ≈ **0,047 USD** (≈ 1.200 đồng) / trần 0,10 USD — lượt 176 câu "sau" (0,037) + bộ an toàn "sau" (0,008) + sinh lại mốc 6 câu (0,0017) + 2 câu
  thử (0,0005); chấm bằng Claude 0 USD. Đợt 1 ≈ 0,073 USD.
- **Bạn cần quyết gì:** (1) **đóng đợt 2** (A trình kết quả); (2) **xóa bản sao lưu** đợt 1 + đợt 2 khi bạn yên tâm (mỗi đợt ~51 MB ảnh chụp Qdrant + vài MB);
  (3) thí nghiệm Qwen3-8B (bạn đã duyệt 29/10) chạy sau khi đóng đợt 2.

## 2. Hoạt động thế nào (bản đang chạy)

```text
Markdown đã sửa → chia đoạn (không đổi so với Phase 2) → e5-small (chạy trên máy) + BM25
 → Qdrant (chỉ mục mới) → "phiếu build" ghi dấu vân tay từng file dữ liệu
khi chatbot khởi động: so dấu vân tay với dữ liệu hiện tại → khác thì từ chối chạy
```

"Phiếu build" (build record) là nguồn sự thật duy nhất cho câu hỏi "chỉ mục có khớp dữ liệu không".
Sửa một chữ trong kho mà chưa build lại thì chatbot không khởi động — để không trả lời bằng chỉ mục cũ.
Sửa dữ liệu về sau chỉ cần chạy lại lệnh build, không phải sửa code.

Code: `backend/ingestion/full_corpus_pipeline.py` (lệnh build), `backend/ingestion/source_state.py`
(phiếu build), `backend/retrieval/full_corpus.py` (kiểm khi khởi động).

Tự kiểm (không bắt buộc): hỏi chatbot một câu về thông tin vừa sửa (ví dụ diện tích đầm Cầu Hai), hoặc
mở `http://localhost:6335/dashboard` để xem các collection.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Sửa mâu thuẫn có căn cứ trong kho (Phase 7A2) | **Đã xử lý, đóng gói** | 25 chỗ / 27 file; Golden sửa 1 đáp án; Golden 176 + smoke 10 đạt sau khi sửa |
| Rà toàn kho tìm mâu thuẫn / thông tin cũ (25/10) | **Đã xử lý** | 139 mục / 205 file (8 sub-agent + C tự kiểm 42 mục: 42 / 42 trích đúng); danh sách private |
| Sửa 139 mục — phần có căn cứ trong kho (đợt 1) | **Đã xử lý, đóng gói** (28/10; đang chạy, đã kiểm) | **123 chỗ / 65 file / 51 mục** (40 mục rà kho + 11 tên phường sót; 1 mục không áp vì file danh mục bị bỏ); áp bằng máy, chuỗi cũ khớp đúng 1 lần; C kiểm diff với bản sao lưu từng mục (C75 đạt) |
| Mục không đủ căn cứ trong kho | **Xử lý một phần** | 12 mục đọc lại ⇒ 9 sang tra ngoài (8 vì hai nguồn trong kho ngang nhau), 3 "không cần sửa" |
| Sửa kho đợt 2 — theo luật "không chắc ⇒ sửa theo nguồn / làm yếu" (bạn 29/10) | **Đã xử lý, đóng gói** (30/10; đang chạy, C kiểm từng bước) | **123 chỗ / 40 file / 20 mục**: bỏ cấp quận / tên phường cũ, 1 mục viết lại theo nguồn, 2 mục theo nguồn, 11 mục làm yếu (2 dòng xóa hẳn); nguồn đọc nguyên văn, session khác đọc lại khớp; áp bằng máy, kho = bản sao lưu + chỗ sửa từng byte |
| Mục chỉ người địa phương biết | **Xử lý một phần** (đợt 2, theo luật bạn đặt 29/10) | không còn hỏi từng câu: câu có nguồn ⇒ sửa theo nguồn; không nguồn ⇒ làm yếu hoặc không sửa (kho đã rào / không mâu thuẫn thật — 8 mục) |
| Mục cần tra nguồn ngoài | **Xử lý một phần** (đợt 2) | kết quả ChatGPT đã về và đối chiếu link; phần có nguồn đọc được đã vào đợt 2; vài mục còn "tra ngoài" (kho đã tự rào) |
| Loại file "danh mục biên soạn" nghệ thuật biểu diễn khỏi chỉ mục | **Đã xử lý, đóng gói** (28/10) | 33 đoạn; **205 → 204 file, 8.459 → 8.426 đoạn**; thêm vào `exclude_files` (`backend/config/settings.yaml`) + test kiểm file bị loại |
| Đo "trước ↔ sau" đợt 2 (176 câu Golden + 32 câu an toàn) | **Đã xử lý** (30/10; C đang đọc các câu cần đọc tay) | không làm hỏng: 0 câu ngoài kho bị trả lời, 0 lỗi, 0 lỗi trích dẫn, 0 "nói chắc sai" mới; đủ ý +0,008 / đúng 0,000 trên 129 câu chính (3 / 1 câu tụt, mức cho phép 5); từ chối nhầm 13 → 12; bộ an toàn 0 câu sai điều kiện mới, 0 đảo cảnh báo; câu bị làm yếu: 0 câu mất điểm đủ ý |
| Mã đoạn bền khi xóa dòng giữa file | **Chưa thực hiện** (phát hiện 30/10) | mã "file#số" dồn số ở 2 file khi xóa 1 dòng ⇒ đợt 2 đo bù bằng luật "chạm theo file"; đợt sau: ghi trước hoặc đổi mã theo nội dung (đổi chunker ⇒ cần thí nghiệm) |
| Đo chất lượng "trước ↔ sau" đợt sửa kho (176 câu) | **Đã xử lý, đóng gói** (28/10; C kiểm đạt) | không làm hỏng: 0 câu ngoài kho bị trả lời, 0 lỗi, 0 lỗi trích dẫn, 0 "nói chắc sai" mới; đủ ý −0,008 / đúng 0,000 trên 129 câu chính (4 / 1 câu tụt, mức cho phép 5); từ chối nhầm 12 → 13; không thấy "tốt hơn" ở 31 câu chạm phần sửa |
| Nhãn "đoạn đúng" sau đợt 2 (bản 5) | **Đã xử lý** (30/10; code đo đổi sang bản 5, chờ commit) | 174 trích dẫn: 173 tìm lại nguyên văn (38 dời vị trí), 1 đổi chữ ⇒ bạn duyệt; bản 1–4 giữ nguyên; tỉ lệ đoạn đúng trong ngữ cảnh không đổi |
| Câu Golden lệch kho sau đợt 2 | **Đã xử lý** (30/10) | quét 39 câu (theo chữ + theo cụm bị bỏ + theo vị trí) ⇒ 3 agent đọc + B kiểm + C quét độc lập ⇒ **2 câu sửa** đáp án mẫu theo bạn chọn (có sao lưu) |
| Nhãn "đoạn đúng" sau khi kho đổi (bản 4) | **Đã xử lý, đóng gói** (28/10) | 174 trích dẫn: 172 tìm lại nguyên văn (42 chỉ dời vị trí), 2 đổi chữ ⇒ bạn duyệt trích dẫn mới; bản 1–3 giữ nguyên; code đo dùng bản 4 |
| Câu Golden lệch kho sau khi sửa | **Đã xử lý** (28/10) | quét 59 câu có thể chạm phần sửa (theo chữ + theo vị trí) ⇒ 3 agent đọc + B kiểm lại + C quét độc lập 176 câu ⇒ **0 câu cần sửa** (bạn duyệt); 1 câu ghi sang đợt 2 |
| Tìm trong kho mà không lọt bộ đánh giá / câu kín | **Đã xử lý, đóng gói** | `scripts/grep_kb.sh`: danh sách cờ trắng, chỉ quét trong kho, loại thư mục đánh giá / meta / bản thô / tên chứa sealed; B thử phá 4 vòng ⇒ đạt |
| Qwen3-8B | **Chưa thực hiện** (plan duyệt; công cụ sẵn, C review đạt) | bạn duyệt 29/10 gửi kho ra OpenRouter + collection thử; chạy sau đợt 2, đo lại mốc e5 trên kho mới trước |
| Chỉ mục e5-small trên dữ liệu đã sửa | **Đã xử lý, đóng gói** (dựng lại 30/10, đợt 2) | **8.424 / 8.424** đoạn (dense + sparse), kiểm từng payload + vector mẫu; `/health` 5 / 5; kết quả tìm 158 câu: 133 giống hệt, 25 đổi danh sách 10 đoạn (11 chỉ đổi thứ tự) — 24 có đoạn của file đã sửa, 1 chỉ đổi đoạn thứ 10. Đợt 1 (28/10): 8.426, 40 câu đổi |
| Phiếu build: dữ liệu lệch → từ chối khởi động | **Đã xử lý, đóng gói** | Phiếu `v3`, `complete`, **204 file** (dựng 30/10); `source_state.py:133`; `full_corpus.py:353,415` |
| Một lệnh build cho mọi lần sửa dữ liệu | **Đã xử lý, đóng gói** | `full_corpus_pipeline.py:232–244` |
| Build lại sau khi sửa kho (từ điển BM25) | **Đã xử lý** (làm thật 28/10 và 30/10) | Xóa đủ ba đích (collection + phiếu build + từ điển) rồi build, ~4–5,5 phút; từ điển 5.660 → 5.631 từ (đợt 2 giữ 5.631). Lệnh xóa bị chặn ở terminal agent ⇒ bạn chạy bằng `!`. `full_corpus_pipeline.py:121–131` |
| Chỉ mục Qwen3-8B qua OpenRouter (7A2) | **Đã thử, chưa áp dụng** | Lần 1 trộn 3 nhà cung cấp (vector không đồng nhất); lần 2 chỉ Nebius lỗi 504; hoãn ⇒ 27/10: thí nghiệm sau đợt sửa kho (dòng trên) |
| Dọn collection cũ trong Qdrant | **Đã xử lý, đóng gói** | 16 → 3 collection (7A2) → 1 (24/10), đúng danh sách duyệt |
| Xóa 2 collection món ăn không dùng | **Đã xử lý, đóng gói** | Đã xóa 24/10 (liệt kê trước/sau); Qdrant chỉ còn `hue_full_corpus_7a2_e5_small_384`. Không có bản sao lưu (theo danh sách dọn) |
| Đoạn bị giữ nhỏ vì kiểm tokenizer model đã bỏ | **Chưa thực hiện** | 6 bảng bị tách chỉ vì HuyDang 256; Phase 8 xử lý |
| Notebook 03, 04 mô tả/gọi tên cũ | **Đã xử lý, đóng gói** | Đã sửa khi dọn (commit `1832201`); Run All 0 lỗi (kiểm lại ở review dọn) |
| Notebook 06 mô tả tên cũ | **Đã xử lý** | Chỉ sửa phần chữ; chưa chạy lại vì có gọi API trả phí |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 30/10/2026 — Áp đợt sửa kho đợt 2 + dựng lại chỉ mục + đo "trước ↔ sau" (bản 6)
- **Soạn (29–30/10):** theo luật bạn đặt 29/10, bộ sửa bản 4b (20 mục, 123 chỗ) — mỗi chỗ sửa theo nguồn có một session khác đọc lại nguyên văn; mục làm yếu
  chỉ bớt khẳng định. C review 3 vòng, A duyệt; plan đo có tiêu chí ghi trước (C review 3 vòng, A duyệt).
- **Bộ "trước":** dùng lại bộ "sau" đợt 1 sau khi qua 4 kiểm "còn hiệu lực" (code chạy, kết quả tìm, phiếu build, cấu hình không đổi) ⇒ không tốn tiền chạy lại.
  Bộ an toàn: sinh lại mốc 3 lần cho 2 câu từng dao động (lúc chỉ mục cũ còn).
- **Áp + dựng lại:** sao lưu 40 file + ảnh chụp Qdrant (khớp checksum); áp bằng máy; chia đoạn thử 0 lỗi (đoạn dài nhất vẫn 255 / 256); bạn chạy lệnh xóa 3 đích ⇒
  build ~4 phút ⇒ 8.424 / 8.424; chatbot chạy lại đạt (2 câu thử).
- **Phát hiện:** 2 dòng bị xóa làm mã đoạn dồn số ở 2 file ⇒ thêm luật "chạm theo file" trước khi đo "sau" (A đồng ý; không phải nới tiêu chí — câu bị chạm được C
  đọc tay).
- **Nhãn + Golden:** như checklist (bạn duyệt 1 trích dẫn mới + chọn cách sửa 2 đáp án mẫu).
- **Đo "sau" + chấm mù cùng lượt:** Golden 300 câu trả lời khác nhau (7 người chấm Claude); bộ an toàn 77 mục mỗi người chấm × 2 người chấm, có 15 câu đối chứng
  để kiểm người chấm (cả hai bắt 10 / 10 câu chèn sai). Thời gian chờ: trung vị 2,19 s, câu chậm 4,90 s.
- **Kết quả:** **không làm hỏng** (chờ C đọc xong các câu cần đọc tay + bạn đóng) · kho + chỉ mục **đã đổi** · tiền đợt 2 ≈ 0,047 USD.

### 28/10/2026 — Áp đợt sửa kho đợt 1 + dựng lại chỉ mục + đo "trước ↔ sau" (bản 5)
- **Đo "trước" (trước khi đụng kho):** 176 câu trên chatbot đang chạy (10 đoạn ngữ cảnh) — 0 lỗi, 0 câu ngoài kho bị trả lời; 0,036 USD. Trước khi sửa kiểm lại
  "còn hiệu lực" (code chạy, kết quả tìm, phiếu build không đổi).
- **Sao lưu:** 65 file kho + file mẫu chia đoạn vào thư mục sao lưu trong kho; phiếu build, từ điển từ khóa và ảnh chụp Qdrant (tải về, khớp checksum).
- **Áp sửa:** 123 chỗ thay chữ, 65 file, 51 mục (bằng máy, theo đúng thứ tự đã kiểm; giữ nguyên xuống dòng). Loại file danh mục khỏi chỉ mục; sửa 1 chuỗi mẫu
  của test chia đoạn theo đúng chỗ sửa. Chia đoạn thử: 204 file, 8.426 đoạn, 0 lỗi; đoạn dài nhất vẫn trong giới hạn tokenizer (sát nhất 255 / 256).
- **Dựng lại tại chỗ:** liệt kê đúng 3 đích trước khi xóa (bạn chạy lệnh xóa vì terminal agent bị chặn) ⇒ build ~5,5 phút ⇒ kiểm 8.426 / 8.426 điểm; test chia
  đoạn 44 / 44; chatbot chạy lại đạt (2 câu thử, 0,0004 USD). C kiểm từng bước (C75): đạt; C còn tách bằng thí nghiệm 4 câu đổi thứ tự kết quả tìm (1 câu do từ
  điển từ khóa mới, 3 câu do đoạn của file đã sửa nằm trong 30 ứng viên).
- **Nhãn đoạn đúng bản 4 + Golden:** như checklist (bạn duyệt 2 trích dẫn mới và "0 câu Golden cần sửa").
- **Đo "sau" + chấm mù cùng lượt** (303 câu trả lời khác nhau, 7 người chấm Claude): **không làm hỏng** (C kiểm đạt). Thời gian chờ của lượt "sau" có câu chậm
  9,8 s (trước 4,9 s) — chậm ở phía mạng / nhà cung cấp trong vài phút cuối lượt (không tách được hai bên; cùng lúc có một việc nặng khác chạy trên máy), phần tìm
  kiếm trên máy không đổi ⇒ số câu chậm của lượt này **không đại diện**.
- **Kết quả:** PASS (C kiểm từng bước: C75, C76, C80) · kho + chỉ mục **đã đổi** · tiền đợt 1 ≈ 0,073 USD.

### 27/10/2026 — Soạn và kiểm đợt sửa kho (bản 4; chưa áp vào kho)
- **Cách làm:** 7 sub-agent đọc lại dòng gốc của 52 mục "sửa khi build" (B làm 1 mục), chỉ dựa vào căn cứ trong kho; mục không chắc thì chuyển nhóm, không
  đoán. Bản sửa dựng bằng máy: chuỗi cũ phải khớp đúng 1 lần, không hai mục chồng nhau. B tự kiểm mẫu (ví dụ cộng lại 12 giá vé lẻ = 1.200.000 đồng, số
  trong kho 1.050.000 là sai).
- **Review C:** vòng 1 tìm 3 bản sửa phải sửa (một câu đúng bị sửa thành sai hướng, hai câu làm mất thông tin) ⇒ B sửa ⇒ vòng 2 đạt; áp thử toàn bộ trong bộ nhớ
  0 lỗi. 11 bản tên phường sót (B tự làm, căn cứ duy nhất là ghi chú sắp xếp phường trong kho) — C review đạt.
- **Sự cố:** một sub-agent nhóm món ăn tìm cả thư mục nên đọc nhầm bộ câu đánh giá món ăn cũ (không phải câu kín). Các bản sửa của nhóm đó được đánh dấu
  riêng; C đối chiếu từng bản với căn cứ trong kho, giữ cả 9. Rút kinh nghiệm: sub-agent chỉ được tìm trong kho bằng `scripts/grep_kb.sh` (rào bằng máy,
  B thử phá 4 vòng tới khi kín).
- **Kết quả:** PASS (soạn + review) · kho, chỉ mục, chatbot **không đổi** · tiền: 0 USD.

### 25/10/2026 — Rà toàn kho (C, chỉ đọc)
Script gom mọi dòng có số / từ chỉ thời điểm (3.901 dòng) ⇒ 8 sub-agent rà theo nhóm, đối chiếu chéo giữa file ⇒ 162 mục thô ⇒ bỏ trùng ⇒ **139 mục**
(mâu thuẫn chắc 22, mâu thuẫn có thể 53, có thể cũ 37, khác 27). Đề xuất: tra ngoài 69, sửa khi build lại 53, bạn biết thì báo 16, đã biết 1. C tự kiểm 42
mục: 42 / 42 trích đúng file / dòng / giá trị · PASS · tiền: 0 USD. Kho **không sửa** ở Phase 8.2 (spec 8.2 để ngoài).

### 24/10/2026 — Dọn code và collection món ăn sau Phase 7 (bản 3)
Xóa 2 collection món ăn và 5 file dữ liệu metadata cũ; gỡ code/test/notebook món ăn. Kiểm lại sau dọn
(C, chỉ đọc): Qdrant còn 1 collection, 8.459 điểm, cả 8.459 điểm đúng 7 trường; 205 file khớp phiếu
build; chunker vẫn ra 8.459 đoạn; kết quả tìm kiếm giống hệt từng byte mốc 7B; chatbot `/health` 200 ·
**PASS** · tiền: 0 (lượt sinh thử 10 câu của B ~0,0013 USD).

### 24/10/2026 — Kiểm lại hiện trạng (C, chỉ đọc)
Kết quả: **PASS** — Qdrant 3 collection; chỉ mục 7A2 có 8.459 điểm (dense + sparse); phiếu build `v3`,
`complete`, 205 file · hiện trạng đúng như lúc đóng · tiền: 0.

### 24/10/2026 — Đóng Phase 7A2
Golden 176 + smoke 10 sau khi sửa kho: **PASS** · chỉ mục mới 8.459 / 8.459, không lỗi: **PASS** ·
chatbot khởi động HTTP 200 · 5 câu thật với `gpt-6-luna`: 4 đạt / 1 chưa đạt — giống hệt trước khi sửa
(câu chưa đạt là lỗi bảng giá cũ) · dọn Qdrant còn đúng 3 collection · code dựng chỉ mục cũ (kiểm thử
trước, migration metadata…) **đã bỏ**; backup kho **đã xóa** khi đóng.
Chỉ mục Qwen3-8B qua OpenRouter: lần 1 trộn 3 nhà cung cấp → vector không đồng nhất; lần 2 chỉ Nebius
→ lỗi 504 · **FAIL** (chưa có chỉ mục dùng được) · bạn chọn **hoãn** sang Phase 8.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`, sau dọn), Qdrant (GET) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026. Hai dòng cuối thêm 27/10/2026 (bản 4); bản 5 (28/10) và bản 6 (30/10, Qdrant GET 8.424 điểm) sửa các dòng số file / đoạn.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Chỉ mục `hue_full_corpus_7a2_e5_small_384` là chỉ mục chatbot dùng (8.459 đoạn tới 27/10; **8.426** từ 28/10, dựng lại tại chỗ) | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:66–69`; `backend/config/settings.yaml:41`; Qdrant GET |
| Phiếu build `full_corpus_build:v3` là nguồn sự thật; dữ liệu lệch thì từ chối chạy | **còn dùng** | `backend/ingestion/source_state.py:133`; `backend/retrieval/full_corpus.py:353,415` |
| Một lệnh build `cd backend && uv run python -m ingestion.full_corpus_pipeline build --candidate <id>` (từ 25/10, gói 1b: chạy từ `backend/`; lệnh cũ `python -m backend.ingestion…` từ gốc không còn chạy) | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:232–244` |
| Sparse state (từ điển BM25) chung, ghi một lần; dữ liệu đổi thì phải xóa file cũ trước khi build | **còn dùng** (bẫy đã ghi ở `Project_Status.md` §8) | `full_corpus_pipeline.py:121–131` |
| Hai model dense: e5-small (chạy máy) và Qwen3-Embedding-8B (OpenRouter, pin Nebius) | **còn trong code**; 8B **chưa có chỉ mục** → thí nghiệm sau đợt sửa kho | `backend/embedding/full_corpus.py:41–66` |
| Chia đoạn giữ nguyên từ Phase 2 | **còn dùng**, tới khi Phase 8 đổi (có số liệu ủng hộ đổi) | `backend/ingestion/chunking/full_corpus_chunker.py`; [R1] |
| Payload 7 trường (metadata v2) | **còn dùng** | `backend/retrieval/full_corpus.py` `REQUIRED_PAYLOAD_FIELDS` |
| 13 collection cũ (4 legacy, 4 metadata v2, 3 món ăn 08a, 2 TF-IDF 08b) | **đã xóa** | Qdrant GET 24/10 |
| Hai collection món ăn (572 điểm mỗi cái) | **đã xóa** 24/10 khi dọn sau Phase 7 (bạn duyệt) | [R2] §2.1; Qdrant GET sau dọn |
| Backup Gate 1 của kho | **đã xóa** khi đóng Phase | `Project_Status.md` §4 |
| 205 file / 8.459 đoạn trong chỉ mục | **đã thay** 28/10 bởi **204 file / 8.426 đoạn** (đợt 1, loại file danh mục), rồi 30/10 bởi **204 / 8.424** (đợt 2) | build record `corpus.file_count` 204; Qdrant 8.424 điểm (GET 30/10) |
| Hai model dense, 8B "Phase 8 xử lý" | **đã thay** bởi: 8B = thí nghiệm sau đợt sửa kho (bạn chọn 15:21 27/10) | spec đợt sửa kho §4 Q4 |

## 6. Việc còn lại / cần quyết

- **Đóng đợt 2:** C đọc tay các câu cần đọc (câu chạm theo file, câu tụt "nhiễu", 1 câu an toàn nhóm vé, 1 câu an toàn thiếu điều kiện mới) ⇒ A trình ⇒ bạn đóng.
- **Xóa bản sao lưu khi bạn duyệt** (đợt 1 + đợt 2: mỗi đợt ảnh chụp Qdrant ~51 MB, bản gốc file kho, phiếu build + từ điển cũ); giữ thì quay lại được bất cứ lúc nào.
- **Thí nghiệm Qwen3-8B** (bạn duyệt 29/10): chạy sau khi đóng đợt 2, đo lại mốc e5 trên kho mới trước.
- Vài mục còn "tra ngoài" (kho đã tự rào); kho thiếu giờ mở cửa của một điểm tham quan lớn (cần nguồn ngoài).
- Bộ chia đoạn vẫn kiểm cả 3 tokenizer (gồm HuyDang 256 đã bỏ) → đoạn bị giữ nhỏ; chưa có số ủng hộ đổi (8.1: bỏ ràng buộc này "không khác").
- Lỗi bảng giá và tổng hợp nhiều nguồn: xem `BAO_CAO_DANH_GIA.md`, `BAO_CAO_TIM_KIEM.md`.

## Phụ lục — hồ sơ kỹ thuật

- **Bản 6 (B93 / B97, 30/10):** report `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` (plan `sua_kho_dot2_do_plan.md` bản 3 + §10, A duyệt
  `2adef0d4e5fc`; review C85 3 vòng, `sua_kho_dot2_b2_6_review.md`); bộ sửa `dot2.jsonl` `c0b5876ea510`; phiếu build `51fb1ec63cbc`, từ điển `c8134c49a648`, kết quả tìm mốc mới
  `4d5bbe9e0edc`; nhãn đoạn đúng bản 5 `33d16fd6b8f4`; Golden md5 `6331e88fb171` (trước `0f7dbf41b422`); dữ liệu private `data/sua_kho_2026-10-27/dot2/`,
  `data/loi_nang_2026-10-28/an_toan/{sau_dot2,moc_regen,dot2}_2026-10-30/`.
- **Bản 5 (B85, 28/10):** report `report_agent/2026-10-27_phan_ton_phase_cu/` — `sua_kho_do_truoc_sau_plan.md` (A duyệt `41485782b39e`, review C72),
  `sua_kho_b1_6_implementation.md` (B81, review C75), `sua_kho_b7_8_implementation.md` (B82, review C76), `sua_kho_b9_implementation.md` (B83, review C80 ready);
  code `6b59788` (loại file danh mục, chỉ mục dựng lại: phiếu build `574b5d02088b`, kết quả tìm mốc mới `23c58c47635d`), `e08a126` (nhãn đoạn đúng bản 4
  `927bae1bf201`); dữ liệu private `data/sua_kho_2026-10-27/` (`applied_edits.jsonl`, `eval_truoc/`, `eval_sau/`, `judge/`, `backup/`).
- **Bản 4 (B77, 27/10):** spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (bạn duyệt sha `937cf8969810`, 15:39 27/10; review C68 3 vòng);
  rà kho C32 `report_agent/2026-10-25_ra_soat_noi_dung_kho/`; soạn đợt sửa B73 / B74, review C66 / C67 (private `data/sua_kho_2026-10-27/`, mục lục `README.md`);
  yêu cầu ChatGPT B76; script `scripts/grep_kb.sh` (W27, commit cuối `77ac6ec`); sự cố S42 (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`). Mã: Kxxx = mục rà kho C32.
- Mã: lỗi bảng giá = **F2**; tổng hợp nhiều nguồn = **F1**; việc dọn sau Phase 7 = **B9** (B làm, C
  review); 8B hoãn theo review Gate 2 (`reports/phase_7a2_gate_2_review_2026_10_24.md` §6).
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C13): sau dọn B9 (commit `1832201`); số đo ở
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md` §4.
- **Lệch phát hiện (24/10):**
  - `Project_Status.md` §4 ghi "mỗi chunk vừa cả 3 tokenizer e5-small / e5-base / huydang" — đúng với
    code (`backend/config/settings.yaml:22–34`), nhưng e5-base và HuyDang không còn là model ứng viên
    từ 7A2; ràng buộc này chỉ còn tác dụng làm đoạn nhỏ đi (6 bảng bị tách chỉ vì HuyDang). Đã báo ở C1.
  - **Đã xử lý:** notebook `04_qdrant_ingestion.ipynb` (bản commit `54670a0`) từng lặp qua cả 2 model và
    gọi trường không tồn tại (`prepared.sample_chunk_ids`). B9 đã sửa (chỉ kiểm candidate có phiếu
    build, lấy mẫu như `full_corpus_pipeline`); Run All 0 lỗi.
