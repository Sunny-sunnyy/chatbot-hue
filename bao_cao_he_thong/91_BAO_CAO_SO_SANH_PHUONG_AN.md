# Báo cáo so sánh phương án — phần đã đóng (Phase 0 → 8.2, sửa kho đợt 1 + 2, Qwen3-8B, thước lỗi nặng, câu theo ngày, đóng gói Phase 1–8)

**Cập nhật lần cuối: 14:33 01/11/2026 — bản 5: B0 (E7, S2, dòng #57, Phần B, §6, mã B0); Phase 8 bạn đóng 14:29 01/11/2026.** Bản 4: 13:41 01/11/2026 — thêm phần đóng gói Phase 1–8 (S18 streaming, S19 lõi chung, S20 giá đủ, T3-10 đo lại theo loại câu, E13 lượt đo cuối; dòng #63–#67; Phần B; §5; §6).** Bản 3: 11:29 01/11/2026 — A ghép vào `bao_cao_he_thong/` sau 2 lượt review độc lập vòng 2 đều đạt; sửa 3 chỗ nhỏ còn lại.** Bản 2: 11:23 01/11/2026 (sửa theo review vòng 1). Bản 1: 11:02 01/11/2026.
Người viết: agent con (việc gom so sánh phương án, 01/11/2026); review: 2 agent con ngữ cảnh mới (dòng 1–626 và 627 – hết), vòng 1 cả hai changes_requested ⇒ sửa ở bản 2 ⇒ vòng 2 cả hai **đạt** (01/11). Bản 4 (đóng gói): C viết nháp 5 khối từ các report gốc (R31), số bộ kín đối chiếu bản B đã sửa theo review; A duyệt.
Nguồn: 68 thẻ so sánh gom theo khâu. Đã đối chiếu với file gốc: 15 số khi gom + 100 khẳng định ở hai lượt review (số lệch đã sửa); các số còn lại chưa kiểm lại.
Phạm vi: mọi so sánh **đã đóng** từ Phase 0 tới hết Phase 8.2, hai đợt sửa kho, thử Qwen3-8B, thước lỗi nặng, đo câu theo ngày tương đối, đóng gói Phase 1–8 (streaming, giá đủ, lượt đo cuối).
**Chưa làm** (không có trong báo cáo này): Phase 9. Hội thoại nhiều lượt **dời sang Phase 9** (User 11:20 01/11/2026 — nghiên cứu cùng phần trợ lý / agent).

---

## 1. Cách đọc

### 1.1. Nhãn độ tin (mỗi khối có ít nhất một nhãn)

Định nghĩa đặt khi gom thẻ; người điều phối xác nhận dùng nguyên (01/11/2026).

| Nhãn | Nghĩa |
|---|---|
| `[rà lại 8.1]` | Quyết định Phase 0–7 đã được thí nghiệm lại ở Phase 8.1 (đợt rà 56 quyết định cũ). |
| `[chưa kiểm lại Phase 0–7]` | Kết luận từ Phase 0–7 (do các agent trước 24/10 làm) **chưa** được thử lại; số có thể đo bằng thước cũ. |
| `[kho, cấu hình cũ]` | Số đo trên kho hoặc cấu hình **khác** bản đang chạy (vd kho trước sửa đợt 1 / 2, đưa model 5 đoạn, nhãn đoạn đúng bản 1–4) và chưa đo lại. |
| `[một lần chạy]` | Chỉ một lượt, không có lượt đo nhiễu (A/A) hay lặp lại, hoặc cỡ mẫu rất nhỏ. |
| `[xác nhận nhóm kiểm]` | Kết quả đã xác nhận trên nhóm kiểm (56 câu) hoặc trên câu kín. |

### 1.2. Kết luận của từng phương án

Tài liệu gốc dùng chữ "tốt hơn / không khác / kém hơn / chưa rõ"; báo cáo này giữ nguyên chữ đó. Tương ứng:
**thắng** = "tốt hơn" (qua luật ghi trước) · **hoà** = "không khác" · **thua** = "kém hơn" (thường vì phạm một "sàn", xem dưới) ·
**chưa rõ** = có tín hiệu nhưng chưa qua luật (thường do ít câu) · **NOT RUN** = đã định nhưng không chạy (ghi lý do).
"Không khác" với cỡ mẫu nhỏ nghĩa là **chưa chứng minh được khác**, không phải chứng minh là bằng nhau.

### 1.3. Các thước đo

- **Đủ (Completeness), Đúng (Accuracy), Trúng ý (Relevance):** điểm 1–5 cho câu trả lời, do một LLM chấm ("judge") so với đáp án tham chiếu. Judge chính là Claude (xem E1); mốc người B0 (01/11) chỉ tham khảo (E7).
- **Đoạn đúng:** đoạn trong kho chứa đáp án, do agent gắn nhãn vị trí (agent khác kiểm, User xem mẫu). "**Đủ đoạn đúng**" = mọi ý của câu đều có ít nhất một đoạn đúng trong tầng đang xét
  (pool ứng viên → 10 đoạn đầu → các đoạn đưa model). Nhãn đã qua 5 bản (v1 → v5); số nào cũng phải đi kèm bản nhãn. Chỉ 55 / 176 câu có nhãn này (40 dev + 15 test).
- **Pool:** tập ứng viên lấy ra trước khi trộn / xếp (mặc định 30 đoạn gần nghĩa nhất theo vector).
- **MRR / nDCG / Keyword Coverage:** điểm xếp hạng theo vị trí đoạn đầu tiên chứa **keyword** đáp án (keyword chép nguyên văn từ kho). Là thước "thay thế" (proxy), không phải nhãn đoạn đúng. MRR tối đa 1.
- **Recall@k:** tỉ lệ câu có đoạn trúng trong k đoạn đầu (dùng ở thời bản món ăn).
- **Từ chối nhầm:** câu có đáp án trong kho mà chatbot trả lời "không có thông tin".
- **P0_sai / P0_thiếu / H:** nói sai cảnh báo hoặc điều kiện / bỏ sót cảnh báo hoặc điều kiện / bịa thêm ý không có trong ngữ cảnh model đọc (thước lỗi nặng, E9).
- **"x / y / z"** trong số đo theo cặp = số câu **tăng / bằng / tụt** so với mốc.
- **CI (khoảng tin cậy 95 %):** khoảng mà chênh thật có nhiều khả năng nằm trong, tính bằng **bootstrap** (lấy mẫu lại các câu 10.000 lần). CI chứa 0 ⇒ chưa chắc có khác.
- **Holm:** cách siết ngưỡng khi thử nhiều biến thể cùng lúc (tránh "thắng vì may"). "Holm 6" = siết cho họ 6 biến thể.
- **A/A:** hai lượt **cùng** cấu hình, để đo nhiễu (số câu đổi điểm khi không đổi gì).
- **Sàn "0 câu mất":** biến thể không được làm câu nào đang đủ đoạn đúng trở thành thiếu. Phần lớn các "kém hơn" ở khâu tìm là vì phạm sàn này, không phải vì CI âm.
- **Luật T3 (bước 2 Phase 8.2, K3 / K3b-m):** số câu tụt điểm Đủ ≤ A/A + 3. (Mã T1–T3 có nghĩa khác nhau giữa các plan — Phụ lục B.)
- **Tiêu chí ghi trước:** luật nhận / sàn / mức tụt viết trước khi chạy. **Không phải mọi phép đo đều có:** các phép đo hiện trạng (tốc độ qua API, số trong câu trả lời,
  luật kiểm sau sinh, kiểm sổ tiền) không có tiêu chí ghi trước — khối nào không có thì ghi rõ.

### 1.4. Bộ câu hỏi

- **Golden:** 176 câu do AI viết, người duyệt (Phase 7A, 23/10); 158 câu có đáp án trong kho + 18 câu ngoài kho. 5 loại câu: một dữ kiện, nhiều nguồn, có điều kiện, so sánh, ngoài kho.
- **Nhóm thử (dev) 120 câu / nhóm kiểm (test) 56 câu:** chia từ Golden ở 8.1 (24/10). Chọn phương án trên dev, xác nhận trên test.
- **Số chính:** bỏ 29 câu "không tự nhiên" (người thật ít hỏi). Trên dev còn **88 câu trong kho**; dev có nhãn đoạn đúng: 40 câu (số chính: **32 câu**, nhãn v1).
- **Câu kín:** 36 câu viết thêm, giữ kín tới phép kiểm cuối 8.2 (28/10). **Nay cả nhóm kiểm và câu kín đều đã dùng** ⇒ không còn bộ "chưa ai thấy".
- **Bộ an toàn 32 câu** (28 trong kho, 4 ngoài kho, agent viết; từ 29–30/10): đo sai cảnh báo / điều kiện.
- **Bản món ăn (Foods):** MVP cũ 08/2026, kho khác (572 đoạn, cách chia khác) — chỉ là lịch sử, số không áp cho toàn kho.

### 1.5. Bản chatbot đang chạy (để biết "mốc" hôm nay)

```text
Kho        204 file / 8.424 đoạn (sau sửa kho đợt 2, 30/10)                         [BKD:9-10; K6]
Chia đoạn  mỗi khối Markdown một đoạn, không gộp; bảng dài tách từng dòng;
           tiền tố tiêu đề đầy đủ; vẫn kiểm vừa 3 tokenizer                          [N2-01, N2-03..05]
Vector     e5-small 384 chiều (chạy trên máy) + BM25 tách âm tiết, k1 1,5 / b 0,75   [N2-09, N2-11, N2-12]
Lưu        Qdrant, 1 collection, HNSW mặc định, 7 trường thông tin điểm               [N2-15, N2-16]
Tìm        dense_bm25_rrf: pool 30 đoạn vector, BM25 chấm lại, trộn RRF k = 60;
           chuẩn hoá NFC câu hỏi (từ 28/10); không xếp hạng lại (rerank)              [T3-02, T3-03, T3-05, T3-08]
Sinh       gpt-6-luna; đưa 10 đoạn (từ 28/10), ngân sách 16.384 token; mức suy luận
           mặc định (không gửi); thiếu một vế ⇒ từ chối cả câu;
           bộ kiểm trích dẫn nhận [n] và [Nguồn n], lỗi ⇒ 500                        [S1, S2, S4, S7, S8]
API        /api/chat (cả câu) + /api/chat/stream (chữ hiện dần, từ 01/11); một lõi chung  [S18, S19]
Số hiện hành (lượt đo cuối 01/11, E13; số tìm = mốc 30/10 vì T1 giống byte)
  từ chối nhầm 12 / 158 câu; điểm TB Đúng / Đủ / Trúng ý 4,71 / 4,58 / 4,72         [E13]
  đoạn đúng (nhãn v5): dev 24 / 40 trong 10 đoạn, 33 / 40 trong 30 ứng viên; test 9 / 15;
  MRR 0,731 / 0,700                                                                  [BTK:15-17]
  tốc độ — ba thước khác nhau, ghi cả ba (01/11, một lần đo, suy luận ≈ 0 hôm đo):
    tới chữ đầu tiên trên trình duyệt (38 câu): p50 / p95 1.228 / 2.612 ms          [S18]
    cả câu qua API thật (22 câu tự viết, tuần tự): 2.340 / 3.800 ms                 [E13]
    trong harness (176 câu Golden, không HTTP): 1,76 / 3,42 s                        [E13]
    (trước: harness 30/10 2,19 / 4,90 s; API 27/10 3.068 / 6.039 ms tuần tự,
      3.410 / 6.432 ms khi 4 câu đồng thời — S13)
  tiền ≈ 0,00025 USD / câu (giá đủ, công cụ tính đúng từ 01/11)                     [S14, S20]
```

Yêu cầu tốc độ User chốt 28/10: p50 ≤ 3 s, p95 ≤ 5 s. Trước streaming đo cả câu: thước harness "đạt sát"; thước qua API (22 câu tự viết, kho cũ, 27/10) chưa đạt cả p50 (3,07 s) lẫn p95 (6,0 s). Từ khi có streaming (01/11) sàn áp cho "tới chữ đầu tiên trên trình duyệt" (User 31/10): **đạt** rộng, mục tiêu 1,5 / 3 s đạt sát (S18).

Viết tắt đường dẫn bằng chứng (BKD, BTK, TH82, R26/…): xem Phụ lục A. Mã nội bộ (G1, K3b-m, B65…): Phụ lục B.

---

## 2. Tóm tắt

### 2.1. Bảng mọi quyết định (một dòng / khối)

| # | Khâu | Mã khối | Vấn đề | Chọn gì | Kết quả một câu | Nhãn |
|---|---|---|---|---|---|---|
| 1 | Kho | K1 | Cấu trúc kho, phạm vi file vào chỉ mục | 5 mảng, nhánh `travel/` 3 nhánh con, 7 glob | Chọn bằng thiết kế, không đo; 8.1 NOT RUN | `[chưa kiểm lại Phase 0–7]` |
| 2 | Kho | K2 | Đọc bản đã biên soạn hay bản thô | Bản đã biên soạn ("kho đóng") | Không đo | `[chưa kiểm lại Phase 0–7]` |
| 3 | Kho | K3 | File danh mục biên soạn có vào chỉ mục | Loại (28/10) | 8.1 "không khác" (0 / 32 / 0); loại ở đợt 1 | `[rà lại 8.1]` `[kho, cấu hình cũ]` |
| 4 | Kho | K4 | Sửa kho 7A2 phần nào | 25 mục / 27 file đủ căn cứ | Smoke 4 / 5 như trước; PASS | `[chưa kiểm lại Phase 0–7]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 5 | Kho | K5 | Sửa kho đợt 1: phạm vi, có làm hỏng không | Mục có căn cứ trong kho; tra ngoài để đợt 2 | "Không làm hỏng"; không thấy "tốt hơn" | `[một lần chạy]` `[kho, cấu hình cũ]` |
| 6 | Kho | K6 | Đợt 2: câu không chắc xử lý sao | Sửa theo nguồn / làm yếu / không sửa | "Không làm hỏng" (cả bộ an toàn 32 câu) | `[một lần chạy]` |
| 7 | Kho | K7 | Dựng lại chỉ mục tại chỗ hay đích mới | Tại chỗ | Chọn bằng lập luận; đích mới NOT RUN | `[một lần chạy]` |
| 8 | Kho | K8 | Thước "trước ↔ sau" khi sửa kho | ≤ A/A + 3; dùng lại bộ "trước"; luật "câu chạm"; bộ an toàn | Dùng 2 lần; tiết kiệm ≈ 0,037 USD | `[một lần chạy]` |
| 9 | Kho | K12 | Giữ Golden khớp kho sau mỗi đợt sửa | Quét 3 lớp + lệnh `check` | `check` bắt 1 câu 3 lớp sót — chỉ khác chữ hoa / thường, không làm sai số chấm; User giữ nguyên (11:04 01/11) | `[một lần chạy]` |
| 10 | Golden | K9 | Cách soạn Golden toàn kho | Viết mới, 5 nhãn, không xáo | 176 câu, PASS; mức đại diện câu thật chưa đo | `[chưa kiểm lại Phase 0–7]` |
| 11 | Golden | K10 | Golden bản món ăn V1 → V3 | V3 (lịch sử) | V2 dừng sau 3 vòng; V3 duyệt; 7A viết mới | `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]` |
| 12 | Golden | K11 | Đáp án tham chiếu: giữ hay sửa | Sửa 10 đáp án | Điểm 7B của 10 câu không còn so được | `[rà lại 8.1]` |
| 13 | Chia đoạn | N2-01 | Cỡ đoạn: gộp hay không | Không gộp | Gộp 128 không khác; 256 / 384 / 512 kém hơn | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 14 | Chia đoạn | N2-02 | Mở rộng ra cả mục sau khi tìm | Không | Kém hơn (mất 8 câu) | `[kho, cấu hình cũ]` `[một lần chạy]` |
| 15 | Chia đoạn | N2-03 | Bảng dài: từng dòng hay nhóm dòng | Từng dòng | Gộp dòng liền nhau không khác | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 16 | Chia đoạn | N2-04 | Tiền tố tiêu đề trong text tìm | Đầy đủ | Hai cách rút gọn kém hơn (mất 7 / 8 câu) | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 17 | Chia đoạn | N2-05 | Ràng buộc 3 tokenizer hay 1 | Vẫn 3 (chưa dọn) | Không khác | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 18 | Chia đoạn | N2-06 | Ba sửa nhỏ dữ liệu | Chỉ bỏ file danh mục được áp | Cả ba không khác | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 19 | Vector | N2-07 | Model vector (bản món ăn) | e5-small | Không ứng viên nào "thắng rõ" | `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]` |
| 20 | Vector | N2-08 | Model vector toàn kho: 4 → 2 | e5-small + Qwen3-8B (ứng viên) | 4 model chưa từng được chấm; thu về 2 không ghi lý do | `[chưa kiểm lại Phase 0–7]` `[một lần chạy]` |
| 21 | Vector | N2-09 | Qwen3-Embedding-8B thay e5-small | Giữ e5-small | Kém hơn: mất đoạn đúng 3 câu dev + 3 câu test; chậm +2,2 s | `[xác nhận nhóm kiểm]` |
| 22 | Vector | N2-10 | Cách gọi Qwen3-8B qua API | Ghim Nebius, 4.096 chiều | Không ghim: trộn nhà cung cấp, cos min 0,99535 < 0,999 | `[một lần chạy]` `[chưa kiểm lại Phase 0–7]` |
| 23 | Từ khoá | N2-11 | BM25: cách tách từ | Âm tiết | Cặp âm tiết, pyvi kém hơn; giữ mã số không khác | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 24 | Từ khoá | N2-12 | BM25 k1 / b, k của RRF | 1,5 / 0,75 / 60 | Không biến thể nào tốt hơn | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 25 | Từ khoá | N2-14 | BM25 hay TF-IDF (bản món ăn) | BM25 | BM25 riêng cao hơn; không cách trộn nào qua rào | `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]` |
| 26 | Qdrant | N2-15 = T3-04 | Tìm gần đúng (HNSW) hay chính xác | HNSW | Giống hệt 108 / 108 câu | `[rà lại 8.1]` `[kho, cấu hình cũ]` |
| 27 | Qdrant | N2-16 | Tổ chức collection, thông tin điểm | 1 collection, 7 trường, không index phụ | Không có số chất lượng; xoá collection cũ PASS | `[chưa kiểm lại Phase 0–7]` |
| 28 | Tìm | T3-01 | Chỗ nghẽn khâu tìm (chẩn đoán) | — | Nghẽn chủ yếu ở **xếp hạng** | `[rà lại 8.1]` `[kho, cấu hình cũ]` |
| 29 | Tìm | T3-02 | Cách trộn vector + từ khoá | `dense_bm25_rrf`, k = 60 | Không biến thể nào qua luật | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[chưa kiểm lại Phase 0–7]` (phần món ăn) |
| 30 | Tìm | T3-03 | Cỡ pool 30 hay 100 / 200 | 30 | Pool 100 kém hơn (mất 1 câu) | `[rà lại 8.1]` `[kho, cấu hình cũ]` |
| 31 | Tìm | T3-05 | Chuẩn hoá Unicode NFC câu hỏi | Thêm NFC (28/10) | Câu NFD tụt, NFC phục hồi hoàn toàn | `[rà lại 8.1]` `[kho, cấu hình cũ]` |
| 32 | Tìm | N2-13 = T3-06 | Câu gõ không dấu | Ngoài phạm vi (User) | Tìm gần như hỏng; bỏ dấu cả kho kém hơn | `[kho, cấu hình cũ]` `[một lần chạy]` |
| 33 | Tìm | T3-07 | Reranker MiniLM (tiếng Anh) | Không rerank | Bằng chứng "làm giảm điểm" chỉ trên bản món ăn | `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]` |
| 34 | Tìm | T3-08 | Reranker chạy GPU (đa ngôn ngữ / tiếng Việt) | Không rerank | Kém hơn: mất đoạn đúng của 1–3 câu | `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` |
| 35 | Tìm + sinh | T3-09 = S11 | Dùng `gpt-6-luna` xếp lại / chọn đoạn | Không dùng | K3b-m: tầng tìm tốt hơn (tạm), tầng trả lời kém hơn theo luật T3 ⇒ gác | `[kho, cấu hình cũ]` `[một lần chạy]` `[xác nhận nhóm kiểm]` (chỉ tầng tìm) |
| 36 | Sinh | S1 | Model sinh câu trả lời | `gpt-6-luna` | **Chưa từng so có chấm điểm** | `[chưa kiểm lại Phase 0–7]` `[một lần chạy]` |
| 37 | Ngữ cảnh | S2 | Đưa model 5 hay 10 đoạn | 10 | **Thắng** dev + test; vào chatbot 28/10 | `[rà lại 8.1]` `[xác nhận nhóm kiểm]` `[kho, cấu hình cũ]` |
| 38 | Ngữ cảnh | S3 | Thứ tự đoạn trong ngữ cảnh | Theo thứ hạng | Không khác | `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 39 | Prompt | S4 | Thiếu một vế: từ chối cả câu hay trả phần có căn cứ | Từ chối cả câu | P1, R2 kém hơn (câu ngoài kho bị trả lời) | `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 40 | Prompt | S5 | Thêm 2 luật cũ của spec Phase 6 | Giữ prompt | Không khác | `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 41 | Prompt | S6 | Câu "nêu đủ chi tiết" | — | NOT RUN (trần 6 câu) | `[kho, cấu hình cũ]` |
| 42 | Sinh | S7 | Mức suy luận của model sinh | Mặc định (không gửi) | `none` / `low` kém hơn; `high` không khác | `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 43 | Sinh | S8 | Bộ kiểm trích dẫn `[n]` | Lỗi ⇒ 500; nhận thêm `[Nguồn n]` | "Một nguồn thì gán" không khác; nhận `[Nguồn n]` PASS | `[rà lại 8.1]` `[xác nhận nhóm kiểm]` |
| 44 | Sinh | S9 | Luật kiểm bằng code sau khi sinh | Không dùng | 7 / 10 cờ là câu có ích ⇒ bỏ | `[một lần chạy]` `[kho, cấu hình cũ]` |
| 45 | Sinh | S10 | Rào chặn sai con số | Chưa cần | 0 / 68 câu có số bị thấy sai | `[một lần chạy]` `[kho, cấu hình cũ]` |
| 46 | Prompt | S17 = E11 | Câu theo ngày tương đối | Không sửa prompt; Phase 9 thêm công cụ ngày | 0 / 12 đoán ngày sai; 6 / 14 bị từ chối | `[một lần chạy]` |
| 47 | API | S12 | Thiết kế API / UI / cách gọi model | Giữ thiết kế Phase 6 | Không có so sánh; sửa mã lỗi PASS | `[chưa kiểm lại Phase 0–7]` |
| 48 | Tốc độ | S13 | Đo ở đâu, khâu nào chậm | (đo hiện trạng) | ≈ 97–98 % thời gian là lúc model viết; harness p95 4,90 s, qua API p95 6,0 s | `[một lần chạy]` `[kho, cấu hình cũ]` |
| 49 | Tiền | S14 | Tiền / câu, lỗi công cụ đo | Sửa công thức ở bước đóng gói | `cost_usd` ghi thiếu ≈ 20 %; ~0,00025 USD / câu | `[một lần chạy]` |
| 50 | Tốc độ | S16 | Đo trước streaming | Hiện chữ ngay (User 31/10) | Lợi "rõ" 1.921,3 ms | `[một lần chạy]` |
| 51 | Đánh giá | E1 | Judge chính: Claude hay luna | Claude chính, luna phụ | Hai bên trùng 0,892–0,960 | `[rà lại 8.1]` `[một lần chạy]` |
| 52 | Đánh giá | E2 | So hai cấu hình thế nào | Bootstrap theo cặp + CI + Holm | Đối chứng âm / dương PASS | `[rà lại 8.1]` |
| 53 | Đánh giá | E3 | Chấm mốc + biến thể cùng lượt mù | Cùng lượt | Nhiễu cả đường 10 / 83 ≫ nhiễu chỉ chấm 2 / 88 | `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 54 | Đánh giá | E4 | Tách dev / test / câu kín | 120 / 56 + 36 câu kín | Cả hai bộ nay đã dùng | `[rà lại 8.1]` `[xác nhận nhóm kiểm]` |
| 55 | Đánh giá | K14 = E5 | Thước tầng tìm: keyword hay đoạn đúng | Thêm đoạn đúng (55 câu), keyword phụ | Đổi chẩn đoán từ chối nhầm (4 / 22 ⇒ 0 / 22) | `[rà lại 8.1]` `[kho, cấu hình cũ]` |
| 56 | Đánh giá | K13 = E6 | Số chính tính trên tập nào | Bỏ 29 câu không tự nhiên | Kappa 0,765; kết luận G1 không đổi | `[rà lại 8.1]` |
| 57 | Đánh giá | E7 | Mốc người chấm | Đọc cặp mù (B0, 01/11) | Chưa rõ (0 cặp quyết; 3 cặp bản 5 đoạn từ chối nhầm) ⇒ giữ 10 | `[một lần chạy]` `[kho, cấu hình cũ]` |
| 58 | Đánh giá | E8 | Câu lỗi 500 chấm thế nào | Điểm 1 | 3 cách tính đều "tốt hơn" | `[xác nhận nhóm kiểm]` `[một lần chạy]` |
| 59 | Đánh giá | S15 | Phép kiểm cuối 8.2 trên câu kín | (đóng 8.2) | "Không làm hỏng" và tốt hơn | `[xác nhận nhóm kiểm]` `[một lần chạy]` `[kho, cấu hình cũ]` |
| 60 | Đánh giá | E9 | Thước bịa thêm / sai điều kiện | Judge tách ý so ngữ cảnh | Thước nhận; H 1 / 145 | `[một lần chạy]` |
| 61 | Đánh giá | E10 | Sàn bộ 32 câu an toàn | A/A trước + sinh lại 3 lần | Sàn: mới ≤ 2, đảo cảnh báo 0 | `[một lần chạy]` |
| 62 | Nền tảng | E12 | Rà code: gỡ / giữ công cụ cũ, nội dung kho trong repo | Gỡ phần không dùng; chuyển nội dung kho ra private từ giờ | Code 8.345 ⇒ 6.218 dòng, hành vi giống byte | `[một lần chạy]` |
| 63 | API / tốc độ | S18 | Streaming: hiện chữ ngay hay chỉ tiến độ | PA1 hiện chữ ngay; giữ sàn 3 / 5 s | Chữ đầu p50 1,23 / p95 2,61 s (một lần đo) — đạt sàn rộng, mục tiêu đạt sát; lợi so đủ câu 0,44 s (chạm luật xem lại, User giữ PA1) | `[một lần chạy]` |
| 64 | API | S19 | Một lõi trả lời chung cho route + bộ đánh giá | Lõi chung | T1 giống byte; 5 khác biệt giữ nguyên | `[một lần chạy]` |
| 65 | Tiền | S20 | Giá phẳng hay giá đủ | Giá đủ từ 01/11 | Ví dụ thật +20 %; lượt cuối 0,000247 USD / câu | `[một lần chạy]` |
| 66 | Tìm kiếm | T3-10 | Lỗi đã biết còn lớn không (kho hiện tại) | Nhiều nguồn ⇒ Phase 9; không thử thêm | Nhiều nguồn Đủ 3,50 (8 câu yếu thiếu bằng chứng); bảng giá không còn lớn | `[một lần chạy]` |
| 67 | Đánh giá | E13 | Lượt đo cuối Phase 1–8 | (đo, không chọn) | Không làm hỏng: tụt 2 / 2 câu, 0 lỗi nặng mới; an toàn đúng ngưỡng; bộ kín: sàn đạt, điểm thấp hơn 0,3–0,4 (từ chối nhầm ở câu nhiều nguồn / so sánh **và** câu trả lời kém đủ ý hơn) | `[một lần chạy]` `[xác nhận nhóm kiểm]` (sàn) |

### 2.2. Điều rút ra (chỉ từ các khối dưới)

- **Phase 8.1 thí nghiệm lại các quyết định Phase 0–7: chỉ "10 đoạn thay vì 5" thắng** (S2) — đã vào chatbot 28/10 và qua phép kiểm cuối trên câu kín (S15). Mọi biến thể khác
  của chia đoạn, từ khoá, trộn, pool, rerank, prompt, mức suy luận ra "không khác", "chưa rõ" hoặc "kém hơn" — không biến thể nào qua luật thắng.
- **Chỗ nghẽn lớn nhất ở khâu tìm là xếp hạng** (đoạn đúng có trong 30 ứng viên nhưng bị xếp ra ngoài, T3-01), nhưng mọi cách sửa xếp hạng đã thử (pool rộng T3-03, reranker GPU T3-08,
  luna chọn đoạn T3-09) đều trượt luật — phần lớn vì làm mất đoạn đúng của 1–3 câu (sàn "0 câu mất") hoặc vì luật T3 ở tầng trả lời.
- **Bộ đo nhỏ quyết định nhiều kết luận:** 30–40 câu có nhãn đoạn đúng, nên nhiều kết quả là "chưa rõ" hoặc "không khác" theo nghĩa chưa chứng minh được (T3-02, N2-12, T3-09 ở 8.1).
- **Thước đo đã đổi kết luận một lần:** chẩn đoán từ chối nhầm theo keyword (4 / 22 câu "có đủ keyword mà vẫn từ chối") bị đảo khi dùng nhãn đoạn đúng (0 / 22) — gốc ở khâu tìm, không ở prompt (K14 = E5, T3-01).
- **Hai đợt sửa kho "không làm hỏng" chatbot nhưng không cho thấy "tốt hơn"** — thước không nhạy với loại sửa này (K5, K6).
- **Model sinh chưa từng được so có chấm điểm** (chỉ thử khói 5 lần gọi, S1); model vector toàn kho chỉ có một phép so có chấm: Qwen3-8B, kém hơn e5-small (N2-08, N2-09).
- **Judge Claude ổn định** (nhiễu chỉ chấm 2 / 88 câu) và khớp luna 0,892–0,960, **nhưng mốc người (B0, 01/11) chỉ tham khảo** — mọi kết luận về câu trả lời vẫn dựa judge Claude (E1, E3, E7).
- **Tốc độ:** ≈ 97–98 % thời gian là lúc model viết; thước harness (p95 4,90 s) và thước qua API (p95 6,0 s) cho hai con số khác nhau, cần ghi cả hai (S13); đo trước streaming: hiện chữ ngay rút thời gian tới chữ đầu ≈ 1,9 s (S16, `[một lần chạy]`); sau khi làm, lợi đo trên trình duyệt (đủ câu − chữ đầu, 38 câu dev ngắn, suy luận ≈ 0) chỉ ≈ 0,44 s — thước khác S16; User vẫn giữ hiện chữ ngay (S18).
- **Lượt đo cuối Phase 1–8 không làm hỏng** so với mốc 30/10 (E13); nhưng bộ kín mới 40 câu cho điểm thấp hơn Golden 0,3–0,4, cả ở câu được trả lời ⇒ **số Golden lạc quan**; câu cần ghép nhiều nguồn yếu nhất ⇒ Phase 9 (T3-10).

---

## 3. Phần A — theo khâu

Mỗi khối giữ đủ 11 trường. Khối gộp từ hai thẻ trùng ghi cả hai mã. Dòng "Suy ra" (nếu có) là ý **không có thẳng trong nguồn**, do agent gom thẻ suy ra.
Đường dẫn `data/…` là file private (không có trên repo); chỉ ghi để tra, không chép nội dung.

### A1. Kho dữ liệu + bộ câu hỏi Golden

(Hai thẻ Golden dính thước đo — K13 = E6 "số chính", K14 = E5 "keyword ↔ đoạn đúng" — nằm ở A8.)

#### K1 — Cấu trúc kho và phạm vi file vào chỉ mục
- **Vấn đề:** chia kho thành mảng / thư mục nào, file nào chatbot đọc; ảnh hưởng cách tìm, cách soạn Golden theo nhóm, cách báo cáo theo mảng.
- **Ngày / Phase:** 08/09/2026 (dời thư mục cũ sang `travel/` với 3 nhánh con); 11/09/2026 (phạm vi 5 mảng, 7 glob); trước Phase 2 toàn kho.
- **Phương án + mốc:** mốc = cấu trúc thư mục cũ; chọn = `travel/` 3 nhánh con, 47 file phân bổ lại (PH:514-518, :895-901). Phạm vi chỉ mục: 5 mảng, 7 glob (INV:86). Không thấy phương án thứ hai nào được ghi ("Phương án từng xét: Không ghi", INV:86).
- **Cách đo:** không đo. Đếm phụ: 6 file hướng dẫn (424 đoạn) xuất hiện trong top-5 tổng 30 lượt trên 158 câu (INV:86).
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước.
- **Kết quả số:** không có so sánh; 8.1 xếp "tác động thấp, không cần đo" ⇒ **NOT RUN** (G5:61). Chỉ mục hiện có 204 file / 8.424 đoạn (BKD:9-10).
- **Tiền + tốc độ:** chưa đo.
- **Quyết định + lý do:** User chỉ đạo cấu trúc 08/09/2026 (PH:514); phạm vi theo plan 11/09, User (INV:86). Lý do: cố định đường dẫn trước khi chia đoạn (PH:900-901).
- **Giới hạn:** không có số chất lượng cho cách chia mảng; báo cáo theo mảng phụ thuộc cấu trúc này.
- **Bằng chứng:** PH:514-518, :893-927; INV:86; G5:61; PS:195.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]`.

#### K2 — Chatbot đọc Markdown đã biên soạn hay bản thô
- **Vấn đề:** chia đoạn thẳng từ bản thô thu thập hay chỉ từ Markdown đã biên soạn và thẩm định (curated).
- **Ngày / Phase:** từ MVP món ăn (Phase 0–2, 08/2026), giữ cho toàn kho (09/2026).
- **Phương án + mốc:** chọn bản curated làm "kho đóng" (closed-world source); "không chunk trực tiếp từ source dumps" (PH:377). Quy tắc viết: mẫu giả định "mỗi section đủ ngữ cảnh khi thành một chunk" (INV:91). Không thấy phương án bản thô được thử.
- **Cách đo:** không đo.
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước.
- **Kết quả số:** không có. Quy tắc viết curated "chưa so sánh" (INV:91); hệ quả lên cỡ đoạn được thử gián tiếp ở 8.1 qua biến thể gộp đoạn (N2-01, G5:22).
- **Tiền + tốc độ:** chưa đo.
- **Quyết định + lý do:** quyết định thời biên soạn 8–9/2026 (User + các đợt biên soạn, INV:91).
- **Giới hạn:** không có số chứng minh curated tốt hơn bản thô; kho curated vẫn có lỗi (139 mục rà kho 25/10, BKD:97).
- **Bằng chứng:** PH:362-377; INV:91.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]`.
- **Suy ra:** lý do "chỉ trả lời từ nguồn đã thẩm định" suy từ chữ "closed-world source" (PH:377); nguồn không ghi lý do dài hơn.

#### K3 — File "danh mục biên soạn" có vào chỉ mục không
- **Vấn đề:** kho có file danh mục thực thể dùng để kiểm soát lúc biên soạn, không phải bài trả lời; để trong chỉ mục có thể chen vào kết quả tìm.
- **Ngày / Phase:** 08/09/2026 (ghi "inventory bị loại"); 24/10 (phát hiện file danh mục của một mảng vẫn được index); 25/10 (8.1 G3 đo); 28/10 (đợt 1 loại).
- **Phương án + mốc:** mốc = chỉ loại 2 file danh mục của một mảng (`exclude_files`), file danh mục của mảng khác (33 đoạn) vẫn trong chỉ mục (INV:87). Phương án (biến thể S1 của G3, 8.1) = bỏ thêm 33 đoạn đó. Không có phương án thứ ba.
- **Cách đo:** 8.1 G3 §3.6, dev số chính: 32 câu có đoạn đúng (chỉ số đoạn đúng trong ngữ cảnh), 88 câu trong kho (keyword); so theo cặp.
- **Tiêu chí ghi trước:** luật chung của 8.1 (giữ / thay / chưa rõ theo luật ghi trước từng gate, G5:7-9); không thấy tiêu chí riêng.
- **Kết quả số:** **không khác**: 0 / 32 / 0 câu (đoạn đúng), keyword 0 / 88 / 0; file danh mục lọt top-10 ở 2 / 120 câu dev (G5:58). Trước đó 7B: top-1 ở 1 / 158, top-10 ở 3 / 158 (INV:87).
  Sau đợt 1 (loại thật): 205 ⇒ 204 file, 8.459 ⇒ 8.426 đoạn (BKD:54); đo chung trong "trước ↔ sau" đợt 1 (K5), không tách riêng.
- **Tiền + tốc độ:** 0 USD (build trên máy); latency chưa đo riêng.
- **Quyết định + lý do:** G5 "an toàn, đề xuất dọn" (G5:58); User đưa vào đợt 1 (spec sửa kho Q1, 15:21 27/10, spec sửa kho:44); áp 28/10 (BKD:54).
- **Giới hạn:** tác động nhỏ nên thước không phân biệt được; đo đợt 1 gộp chung với 123 chỗ sửa chữ.
- **Bằng chứng:** INV:87; G5:58; BKD:11, :54; `backend/config/settings.yaml:18–21` (theo BKD:54, chưa mở code); commit `6b59788` (BKD:146).
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` (số 8.1 đo trên kho trước sửa đợt 1, nhãn đoạn đúng bản cũ).

#### K4 — Sửa kho Phase 7A2: sửa những mục nào
- **Vấn đề:** lúc soạn Golden 7A phát hiện 53 mục mâu thuẫn trong kho (BG:94-95); quyết sửa phần nào trước khi đo chính thức 7B.
- **Ngày / Phase:** 23/10/2026 (gate 1 sửa kho), 24/10 (gate 2 dựng lại chỉ mục, đóng 7A2).
- **Phương án + mốc:** mốc = kho chưa sửa (205 file / 8.459 đoạn). Chọn = 21 mục nhóm A (đủ căn cứ) + chỉnh câu chữ 4 mục nhóm B, "không rà thêm" (spec 7A2:31); không chọn = sửa cả 28 mục nhóm C (gate 1 7A2:25-26). Giá trị chuẩn lấy từ một tổng hợp nghiên cứu private (spec 7A2:8-9).
- **Cách đo:** kiểm định dạng Golden trước / sau; tìm giá trị cũ trong 176 + smoke 10; smoke 5 câu thật (5 lần gọi `gpt-6-luna`); smoke tìm kiếm 10 câu (spec 7A2:33-35). Không có đo theo cặp trên 176 câu.
- **Tiêu chí ghi trước:** `check` trước / sau + sửa tối thiểu câu Golden bị ảnh hưởng; nghiệm thu chuyển chỉ mục = smoke 5 câu + smoke tìm kiếm 10 (spec 7A2:34-35).
- **Kết quả số:** sửa 25 mục / 27 file (BKD:49; gate 1 7A2:58, :67); Golden sửa 1 đáp án (gate 1 7A2:120-122); chỉ mục 8.459 / 8.459; smoke 4 / 5 đạt, 1 chưa đạt — giống trước khi sửa (lỗi cũ ở một câu hỏi giá) (BKD:101; gate 2 7A2:275). **PASS** (đóng 7A2).
- **Tiền + tốc độ:** gate 1 0 USD; smoke 5 lần gọi — số USD chưa thấy trong nguồn đã đọc (chưa kiểm).
- **Quyết định + lý do:** User 23/10/2026 (spec 7A2 §2); chỉ sửa mục đủ căn cứ.
- **Giới hạn:** không đo chất lượng theo cặp; mốc 7B đo trên kho đã sửa nên không có "trước" toàn bộ. Kho này sau đó bị thay bởi đợt 1 và 2.
- **Bằng chứng:** spec 7A2:27-43; gate 1 7A2:18-26, :58-67, :115-128; gate 2 7A2:275; BKD:49, :100-102.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[một lần chạy]` `[kho, cấu hình cũ]`.

#### K5 — Sửa kho đợt 1: phạm vi và có làm hỏng chatbot không
- **Vấn đề:** rà toàn kho 25/10 ra 139 mục (mâu thuẫn chắc 22, có thể 53, có thể cũ 37, khác 27; BKD:97); quyết sửa đợt đầu phần nào và chứng minh sửa không làm chatbot kém đi.
- **Ngày / Phase:** soạn 27/10, áp + đo 28/10/2026 (sau đóng 8.2), "phần tồn Phase cũ".
- **Phương án + mốc:** mốc = chatbot trước sửa (205 file / 8.459 đoạn, 10 đoạn ngữ cảnh). Q1: **chọn** = mục có căn cứ ngay trong kho + file danh mục + mục User trả lời; phần cần tra ngoài để đợt 2.
  **Không chọn** = gộp cả phần tra ngoài vào đợt 1; A ghi khuyến nghị của mình (tách đợt) sẽ sai nếu phần lớn lỗi User gặp nằm ở nhóm tra ngoài (spec sửa kho:44, :52-53). Q2: tra ngoài qua ChatGPT, chỉ gửi câu ngắn (:45, :54-55).
  Soạn: 41 mục (40 giữ + 1 có điều kiện, không áp vì file danh mục bị loại) + 11 chỗ sửa tên đơn vị sót (TH27:38-39). 16 câu User trả lời ghi trong Q1 rốt cuộc chuyển sang đợt 2 (TH27:58; BKD:51 — đợt 1 áp 51 mục = 40 + 11).
- **Cách đo:** 176 câu Golden, chatbot thật sinh "trước" và "sau", judge Claude chấm mù cùng lượt; số chính 129 câu (bỏ câu không tự nhiên, trong kho); Đủ / Đúng, từ chối nhầm, 4 sàn F1–F4 (F1 câu ngoài kho bị trả lời, F2 câu "nói chắc sai" mới, F3 lỗi kỹ thuật, F4 câu lỗi trích dẫn mới — nghĩa đủ ở Phụ lục B) (R27/sua_kho_b9_implementation.md:36-42).
- **Tiêu chí ghi trước:** spec sửa kho:107-112 + plan R27/sua_kho_do_truoc_sau_plan.md (A duyệt sha `41485782b39e`): 0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật / 500 mới; Đủ / Đúng TB ≥ −0,1; số câu tụt ≤ A/A + 3 với A/A = 2 (⇒ ≤ 5); từ chối nhầm "sau ≤ trước + 1".
- **Kết quả số** (R27/sua_kho_b9_implementation.md:36-44): F1 0 / 18; F2 0 ứng viên; F3 0 / 0; F4 0; Đủ 4 / 121 / 4, TB −0,0078 [−0,062; +0,039]; Đúng 1 / 127 / 1, TB 0,000 [−0,023; +0,023];
  từ chối nhầm 12 ⇒ 13 (đúng mức cho phép) ⇒ **"không làm hỏng"**. Câu chạm phần sửa (31 câu số chính): Đủ −0,032 [−0,194; +0,097] ⇒ **không "tốt hơn"** (:60).
  Áp 123 chỗ / 65 file / 51 mục; 204 file / 8.426 đoạn; 40 / 158 câu đổi top-10 (BKD:51, :61; TH27:84).
- **Tiền + tốc độ:** bộ "sau" 0,036454 USD; cả đợt ≈ 0,0730 / trần 0,15 USD (:90). p50 / p95 2.207,7 / 4.883,6 ⇒ 2.782,1 / 9.763,0 ms; p95 lượt "sau" **không đại diện** (chậm phía mạng / nhà cung cấp; phần trên máy trung vị 38 ⇒ 45 ms) (:64).
- **Quyết định + lý do:** User chọn Q1–Q5 15:21 27/10 (spec sửa kho:40-48); duyệt spec sha `937cf8969810` 15:40 27/10 (TH27:40); **User đóng đợt 1 13:26 28/10, giữ sao lưu** (PS:143; TH27:104).
- **Giới hạn:** thước không nhạy với loại sửa này (phần lớn chỉ thêm tên đơn vị hành chính mới) (R27/sua_kho_b9_implementation.md:12; BKD:22-23); F2 chỉ bắt "nói ngược", không bắt "bịa thêm" (:81); một lượt, judge Claude không có mốc người; 97 / 139 mục rà kho ban đầu chỉ có tự kiểm của sub-agent (TH27:50).
- **Bằng chứng:** spec sửa kho:40-112 (sha `937cf8969810`); R27/sua_kho_b9_implementation.md; review R27/sua_kho_b9_review.md (TH27:86); BKD:51, :55, :84-88; `report_agent/2026-10-25_ra_soat_noi_dung_kho/ra_soat_kho_implementation.md:66-72`.
- **Nhãn:** `[một lần chạy]` `[kho, cấu hình cũ]` (kho sau đợt 1 đã bị thay bởi đợt 2).

#### K6 — Sửa kho đợt 2: câu không chắc thì sửa theo nguồn, làm yếu, hay để nguyên
- **Vấn đề:** phần còn lại sau đợt 1 là mục **không đủ căn cứ trong kho** (cần nguồn ngoài); cần một luật xử lý câu không chắc mà không thêm khẳng định mới.
- **Ngày / Phase:** luật User 29/10/2026; áp + đo 30/10/2026.
- **Phương án + mốc:** mốc = kho sau đợt 1 (204 file / 8.426 đoạn, build record — file ghi chỉ mục khớp kho — `574b5d02088b`). Mỗi mục có các lựa chọn + gợi ý cho User (`data/sua_kho_2026-10-27/dot2/quyet_dinh_user.md` (private):3).
  Luật (User 29/10): có nguồn đọc được (session khác đọc lại khớp) ⇒ **sửa theo nguồn**; không có ⇒ **làm yếu** (bỏ con số / chi tiết không chắc) hoặc **không sửa**; không thêm khẳng định mới, không xoá câu cảnh báo an toàn (BKD:15-17, :53).
  Phân loại: bỏ cấp hành chính cũ và tên đơn vị hành chính cũ (104 chỗ) + 1 mục viết lại theo nguồn + 2 mục sửa theo nguồn + 11 mục làm yếu (2 dòng xoá hẳn); 8 mục không sửa (kho đã tự rào / không mâu thuẫn thật); 1 mục bỏ khỏi đợt (BKD:16-17; R27/sua_kho_dot2_do_plan.md:26-28).
  Ở 2 dòng, bỏ đơn vị cấp cũ thì đơn vị chỉ "phối hợp" sẽ thành đơn vị đứng tên (một khẳng định mới) ⇒ A chọn xoá cả dòng (R27/sua_kho_dot2_do_plan.md:151).
- **Cách đo:** 176 câu Golden + **32 câu an toàn** (mới thêm ở đợt 2), chấm mù cùng lượt; số chính 129; sàn F1–F4; mức tụt T1–T3 (T1 Đủ, T2 Đúng: số câu tụt ≤ 5 và trung bình ≥ −0,1; T3 từ chối nhầm tăng ≤ 1); bộ an toàn A1–A2 (A1 câu ngoài kho bị trả lời; A2 P0_sai — sai điều kiện — mới, đảo cảnh báo / điều kiện vào); cổng đối chứng 2 judge an toàn (câu chèn sai cố ý, judge phải bắt được); W9 "thiếu ý ở mục làm yếu" (R27/sua_kho_dot2_implementation.md:38-54; R27/sua_kho_dot2_do_plan.md:81-83).
- **Tiêu chí ghi trước:** plan đợt 2 bản 3 + §10 (A duyệt sha `2adef0d4e5fc`): F1–F4 = 0; T1 / T2 tụt ≤ 5 câu (và trung bình ≥ −0,1); T3 từ chối nhầm ≤ trước + 1; A1 = 0; A2 P0_sai mới ≤ 2, đảo cảnh báo 0; cổng judge recall ≥ 9 / 10, báo nhầm ≤ 1 / 5 (R27/sua_kho_dot2_implementation.md:42-52).
- **Kết quả số** (:42-54): F1 0 / 18; F2–F4 0; Đủ +0,008 [−0,031; +0,047], 4 / 122 / 3; Đúng 0,000, 1 / 127 / 1; từ chối nhầm 13 ⇒ 12; bộ an toàn: ngoài kho 0 / 4, P0_sai mới 0, đảo cảnh báo 0; judge an toàn 10 / 10 (cả hai) ⇒ **"không làm hỏng"**.
  Mục làm yếu: 5 câu Golden có ngữ cảnh chứa chỗ làm yếu, 0 câu tụt Đủ (:67). C đọc tay 8 câu: 0 lỗi nội dung kho, 1 câu thiếu một lời nhắc do thứ hạng đoạn đổi (:56-57). Chỉ mục 8.424 / 8.424; 25 / 158 câu đổi top-10 (:28-29).
- **Tiền + tốc độ:** ≈ 0,0471 USD / trần 0,10 (:15); ~0,0002086 USD / câu (:64); harness p50 / p95 "sau" 2,19 / 4,90 s (:65).
- **Quyết định + lý do:** luật = User 29/10; A duyệt bộ sửa bản 4b sha `c0b5876ea510` 11:15 30/10 (TH27:120); **User đóng đợt 2 14:39 30/10, giữ sao lưu cả hai đợt** (TH27:126; PS:142).
- **Giới hạn:** bộ "trước" là câu trả lời 28/10 ⇒ trôi theo ngày phía nhà cung cấp không tách được; judge Claude chưa có người đọc; bộ an toàn do agent viết, n 28 ⇒ cận P0_sai "sau" 0–12 % (R27/sua_kho_dot2_implementation.md:86-87);
  P0_thiếu đổi 5 câu, trên mức đổi 3 của A/A, "báo A, không quyết" (:69); vài mục còn chờ tra ngoài (BKD:130).
- **Bằng chứng:** R27/sua_kho_dot2_implementation.md; plan R27/sua_kho_dot2_do_plan.md; review R27/sua_kho_dot2_b2_6_review.md; BKD:15-19, :52-53, :56, :76-82; build record `51fb1ec63cbc`, sparse state (từ điển BM25) `c8134c49a648` (TH27:133).
- **Nhãn:** `[một lần chạy]`.

#### K7 — Thay chỉ mục sau khi sửa kho: dựng lại tại chỗ hay dựng đích mới
- **Vấn đề:** sửa kho xong phải dựng lại chỉ mục; chọn cách để chatbot không trả lời bằng chỉ mục cũ và quay lại được.
- **Ngày / Phase:** 27/10/2026 (spec sửa kho Q3); làm thật 28/10 và 30/10.
- **Phương án + mốc:** (a) **tại chỗ** — xoá collection + build record + sparse state rồi build lại đúng tên, chatbot ngừng trong lúc build, có snapshot trước; (b) đích mới rồi chuyển — cần code đọc tên đích từ cấu hình (spec sửa kho:56-58).
  (7A2 trước đó dùng kiểu (b): collection tên mới rồi xoá 13 collection cũ, spec 7A2:39, :43.)
- **Cách đo:** không so; chỉ đo thời gian build thật ~4–5,5 phút (BKD:64).
- **Tiêu chí ghi trước:** nghiệm thu chung: index khớp build record, chatbot khởi động, cổng ổn định đạt (spec sửa kho:106).
- **Kết quả số:** (a) chạy 2 lần: 8.426 / 8.426 (28/10), 8.424 / 8.424 (30/10) (BKD:61); lệnh xoá bị chặn ở terminal agent ⇒ User tự chạy (BKD:64). (b) **NOT RUN**.
- **Tiền + tốc độ:** 0 USD (e5 trên máy); build ~4–5,5 phút; chatbot ngừng trong thời gian đó.
- **Quyết định + lý do:** A khuyên (a) vì chatbot chạy trên máy User, ngừng ngắn chấp nhận được, (b) là code mới chưa có nhu cầu (chưa deploy); User chọn (a) 15:21 27/10 (spec sửa kho:46, :56-58).
- **Giới hạn:** lựa chọn đúng cho chạy trên máy.
- **Bằng chứng:** spec sửa kho:46, :56-58, :82; BKD:38, :64.
- **Nhãn:** `[một lần chạy]` (không có đo so sánh; chọn bằng lập luận).
- **Suy ra:** khi deploy thật thì lý do "ngừng ngắn chấp nhận được" có thể không còn (suy từ lý do A ghi, :57-58).

#### K8 — Cách đo "trước ↔ sau" khi sửa kho
- **Vấn đề:** sửa kho thường không làm điểm tăng; cần thước "không làm hỏng" rẻ, ghi trước, chịu được nhiễu và lỗi đo.
- **Ngày / Phase:** plan đợt 1 27–28/10; phụ lục đợt 2 29–30/10/2026.
- **Phương án + mốc:**
  - Mức tụt cho phép: ≤ A/A + 3 với **A/A = 2** lấy từ dữ liệu có sẵn (cặp lượt 10 đoạn ↔ 10 đoạn, 176 câu: tụt Đủ 1, Đúng 2), **không chạy A/A mới** (spec sửa kho:111).
  - Bộ "trước" đợt 2: **dùng lại** bộ "sau" đợt 1 nếu qua 4 kiểm "còn hiệu lực" (code không đổi, sha record / sparse khớp, T1 chạy lại giống byte, model / context khớp) ↔ chạy bộ "trước" mới (≈ 0,037 USD) (R27/sua_kho_dot2_do_plan.md:30-41).
  - Luật "câu chạm": đợt 1 (a)–(d); đợt 2 thêm (f) "chạm theo file" vì mã đoạn `file#số` dồn số khi xoá dòng — ghi **trước** khi thấy số "sau" (TH27:123; R27/sua_kho_dot2_implementation.md:75-76).
  - Bộ an toàn 32 câu (thước lỗi nặng, E9 / E10) thêm vào đợt 2 vì có mục làm yếu / điều kiện vào (R27/sua_kho_dot2_implementation.md:24, :49-52).
- **Cách đo:** như K5 / K6.
- **Tiêu chí ghi trước:** chính là nội dung khối này (plan đợt 1 sha `41485782b39e`, đợt 2 sha `2adef0d4e5fc`).
- **Kết quả số:** 4 / 4 kiểm "còn hiệu lực" đạt ⇒ bộ "trước" đợt 2 = bản sao giống byte, 0 USD (R27/sua_kho_dot2_implementation.md:22). Luật (f) đưa 3 câu vào tập chạm, 2 câu chỉ có (f) ⇒ C đọc hai bên (:75). Cả hai đợt qua thước (K5, K6).
- **Tiền + tốc độ:** tiết kiệm ≈ 0,037 USD bộ "trước" đợt 2 (R27/sua_kho_dot2_do_plan.md:39).
- **Quyết định + lý do:** A duyệt plan (đợt 1 `41485782b39e`; đợt 2 `2adef0d4e5fc`, TH27:124); luật (f) A đồng ý trước khi có số "sau" (TH27:123).
- **Giới hạn:** dùng lại bộ "trước" ⇒ trôi theo ngày phía nhà cung cấp không tách được (R27/sua_kho_dot2_implementation.md:86); A/A = 2 lấy từ cặp lượt khác mục đích; mã đoạn `file#số` vẫn chưa bền (BKD:57).
- **Bằng chứng:** spec sửa kho:107-112; R27/sua_kho_do_truoc_sau_plan.md; R27/sua_kho_dot2_do_plan.md:20-41; R27/sua_kho_dot2_implementation.md:22, :75-76, :86.
- **Nhãn:** `[một lần chạy]`.

#### K12 — Giữ Golden khớp kho sau mỗi đợt sửa: cách quét
- **Vấn đề:** sửa một dữ kiện trong kho có thể làm đáp án / keyword Golden lệch kho ⇒ điểm giả.
- **Ngày / Phase:** 7A2 (23/10), đợt 1 (28/10), đợt 2 (30/10), kiểm lại 31/10/2026.
- **Phương án + mốc** (các cách quét đã dùng):
  - 7A2: `check` trước / sau + tìm giá trị cũ của 25 mục trong câu hỏi / keyword / đáp án (gate 1 7A2:115-128).
  - Đợt 1: 2 lớp — (1) theo chữ cũ quanh chỗ sửa, (2) theo vị trí đoạn bị sửa trong ngữ cảnh — rồi 3 sub-agent đọc từng câu (R27/sua_kho_b7_8_implementation.md:35-40).
  - Đợt 2: thêm lớp (1b) **theo cụm chữ bị bỏ** (lớp 1a sót 2 câu) (BG:81; R27/sua_kho_dot2_implementation.md:31).
  - 31/10: chạy lại `golden_full_corpus check` (keyword nguyên văn trong kho) sau 2 đợt (BG:64).
- **Cách đo:** số câu bị chạm, số câu cần sửa; người khác kiểm; User chọn cách sửa.
- **Tiêu chí ghi trước:** spec sửa kho Q5 — quét + User duyệt sửa Golden trước khi đo lại (spec sửa kho:48, :62-63).
- **Kết quả số:** 7A2: 1 câu sửa đáp án (gate 1 7A2:120-122). Đợt 1: lớp 1 26 + lớp 2 40 ⇒ hợp 59 ⇒ sửa 0 (R27/sua_kho_b7_8_implementation.md:37-40). Đợt 2: 12 + 2 + 27 ⇒ hợp 39 ⇒ sửa 2 đáp án, md5 ⇒ `6331e88fb171` (R27/sua_kho_dot2_implementation.md:31).
  31/10: `check` 176 câu, **1 lỗi** — 1 câu có keyword không còn nguyên văn trong kho, 3 lớp quét sót; nguyên nhân: kho đổi một chữ hoa thành thường — `check` phân biệt hoa / thường, phép chấm thì không ⇒ không số chấm nào sai (BG:22-23, :64, :120-122).
- **Tiền + tốc độ:** 0 USD; `check` vài giây (BG:121-122).
- **Quyết định + lý do:** User duyệt "0 câu cần sửa" đợt 1 (28/10, TH27:75); User chọn 2 cách sửa đợt 2 (13:39–13:43 30/10, TH27:124); đề xuất sau mỗi đợt: quét 3 lớp **và** chạy `check` (BG:121-122). Câu lệch 31/10: **User giữ nguyên** (11:04 01/11/2026; `check` từ nay báo 1 lỗi đã biết — BG:23, :120).
- **Giới hạn:** quét 3 lớp vẫn sót (lớp quét không bắt lệch chữ hoa / thường) ⇒ luôn chạy thêm `check`.
- **Bằng chứng:** như trên; BKD:21, :59.
- **Nhãn:** `[một lần chạy]`.
- **Suy ra:** `check` không bắt đáp án sai nghĩa (suy từ mô tả lệnh: định dạng + keyword nguyên văn, BG:48, :64).

#### K9 — Golden toàn kho Phase 7A: cách soạn đề
- **Vấn đề:** cần đề chấm cho toàn kho (5 mảng); viết mới hay chép bộ món ăn, số nhãn loại câu, quy trình viết, cách gộp, có chia dev / test không.
- **Ngày / Phase:** 23/10/2026, Phase 7A (thay các quyết định cũ thời Codex).
- **Phương án + mốc** (quyết định cũ ⇒ mới, spec 7A:20-32):
  - Câu bản món ăn V3: chép, phân loại lại ⇒ **viết mới toàn bộ**, V2 / V3 giữ làm lịch sử.
  - Thứ tự: 7 nhóm tuần tự ⇒ **pilot 1 nhóm (~20 câu, User đọc hết) rồi 6 nhóm song song**.
  - Loại câu: 7 nhãn theo một bộ đề tham khảo cũ (nhãn không có định nghĩa; khoảng 50 % keyword nằm sẵn trong câu hỏi — khảo sát bộ đề tham khảo cũ, `reports/`, 23/10) ⇒ **5 nhãn** (một dữ kiện, nhiều nguồn, có điều kiện, so sánh, ngoài kho).
  - Số lượng: không quota 150–200 ⇒ **~175, tỉ lệ mềm ±20 %**. Keyword: thêm luật ≥ 1 keyword mang đáp án, không có trong câu hỏi. Thêm câu ngoài kho ~5–10 %.
  - Người duyệt: User + Reviewer đọc từng câu ⇒ Reviewer đối chiếu 100 %, User đọc mẫu 10–15 câu / nhóm. Gộp: nối rồi xáo seed 42 ⇒ **nối theo thứ tự cố định, không xáo**.
  - Dev / test: **không chia** (đã đổi ở 8.1 — E4).
- **Cách đo:** máy `check` (định dạng 4 phần + keyword nguyên văn trong kho) + người đối chiếu từng câu với file nguồn; không đo mức đại diện câu thật.
- **Tiêu chí ghi trước:** Reviewer đối chiếu 100 %; User đọc pilot + mẫu từng nhóm; smoke 10 User duyệt, giống từng dòng với file chính (spec 7A:194-196).
- **Kết quả số:** 180 câu nháp (76 / 29 / 32 / 25 / 18) (impl 7A:56) ⇒ duyệt: xoá 4, sửa 11 ⇒ **176 câu** = 75 / 29 / 29 / 25 / 18 (BG:17; impl 7A:230-246); `check` exit 0; **PASS** — User xác nhận 23/10 (review 7A:3, :58).
  Dùng ở 7B: chấm hai lần chênh ≤ 0,011 (BG:18); 121 / 176 câu đạt điểm tối đa ở mốc 7B (BG:25; INV:160). 8.1: hai dòng xét lại Golden (7.1, 7.2) **NOT RUN** (G5:61).
  Ghi chú số câu sửa: bảng GATE R (impl 7A:230-246) có 15 dòng = 4 xoá + 11 sửa, khớp impl 7A:253; câu "cả 14 case" ở impl 7A:224 đếm thiếu 1; báo cáo Golden đã sửa thành 11 (01/11).
- **Tiền + tốc độ:** 0 USD (không gọi API trả phí, spec 7A:17).
- **Quyết định + lý do:** User 23/10/2026 (spec 7A:4, §2).
- **Giới hạn:** câu do AI viết rồi người duyệt, không phải câu người dùng thật; ngoài kho chỉ 18 câu ⇒ khoảng tin cậy rộng; điểm tổng bị câu một dữ kiện (43 %) chi phối (INV:159-160; BG:24-25).
- **Bằng chứng:** spec 7A:20-36, :119-140; impl 7A:56, :124-137, :222-253; review 7A:3, :58, :67; INV:159-160; BG:17, :94.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]`.
- **Suy ra:** lý do bỏ quota cứng = bài học V2 (K10) — spec V3 ghi quota gây câu gượng ép (spec V3:15-19), spec 7A không ghi lý do này.

#### K10 — Golden bản món ăn V1 → V2 → V3 (lịch sử)
- **Vấn đề:** bộ đề cho MVP món ăn; V1 104 câu có lỗi, cần làm lại.
- **Ngày / Phase:** 24/08/2026 (Phase 7 món ăn chấm V1); 26/08 (V2); 27/08/2026 (V3, Gate 0).
- **Phương án + mốc:** mốc = V1 104 câu. **V2** = dựng lại có chọn lọc từ 104 câu, đúng 100 câu + smoke 20, có quota loại câu (spec V2:26-35). **V3** = bộ nhỏ theo "khả năng du khách hỏi thật", cỡ 50 → 45 → 40, User đọc mọi câu (spec V3:11-38).
- **Cách đo:** V1 chấm thử: MRR 0,83; Đúng / Đủ / Trúng ý 4,37 / 4,02 / 4,19 (BG:96). V2 / V3: review chất lượng (không đo điểm chatbot).
- **Tiêu chí ghi trước:** V3: "validator PASS không bao giờ là duyệt chất lượng", User + Reviewer quyết cỡ (spec V3:36-38).
- **Kết quả số:** V2 **dừng sau 3 vòng `changes_requested`** (spec V2:3-5); V3 45 + 10, `approved` (`reports/phase_8_golden_dataset_v3_codex_review.md:3-9`; PS:128). 7A không chép V3 (K9).
- **Tiền + tốc độ:** chưa đo.
- **Quyết định + lý do:** V3 thay V2 vì quota đúng 100 dòng / ma trận loại câu "đẻ ra câu lặp khuôn, gượng ép" (spec V3:15-19); User duyệt V3.
- **Giới hạn:** số bản món ăn không so trực tiếp với số toàn kho (cách chia đoạn khác ~2,9 lần, INV:60-61); code chấm bản món ăn đã gỡ 24/10 (BG:115).
- **Bằng chứng:** spec V2:1-35; spec V3:1-38; review V3:3-9; `reports/phase_7_golden_dataset_audit.md:5-15`; BG:96.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]`.

#### K11 — Đáp án tham chiếu Golden: giữ bản LLM viết hay sửa
- **Vấn đề:** đáp án tham chiếu do LLM viết; judge chỉ so với nó, đáp án thừa / thiếu thì điểm Đủ lệch (INV:162).
- **Ngày / Phase:** 25/10/2026, Phase 8.1.
- **Phương án + mốc:** mốc = đáp án 7A. Chọn = sửa theo nguyên tắc User 12:20 25/10: "đáp án chỉ trả lời điều câu hỏi hỏi; chỉ thêm điều kiện khi thiếu nó thì sai / hiểu lầm; chi tiết phụ đúng nguồn giữ" (R81/phase_8_1_golden_fix_review.md:6-7). Phương án giữ nguyên = các câu không sửa.
- **Cách đo:** review đối chiếu nguồn từng đáp án; không đo điểm.
- **Tiêu chí ghi trước:** nguyên tắc 12:20 như trên; chỉ đáp án tham chiếu đổi, keyword / smoke giữ (:87).
- **Kết quả số:** sửa 10 đáp án; 8 / 10 đạt nguyên tắc lần đầu, 1 câu vượt nguyên tắc ⇒ đã đóng (:103, :133); md5 ⇒ `0f7dbf41b422` (G5:55).
- **Tiền + tốc độ:** 0 USD (:127).
- **Quyết định + lý do:** User duyệt "sửa theo đề xuất" 12:20 25/10 (:6); review ready (:3).
- **Giới hạn:** điểm 7B của 10 câu này **không còn so trực tiếp** (:59; G5:55); độ đầy đủ đáp án chưa đo bằng mốc người.
- **Bằng chứng:** R81/phase_8_1_golden_fix_review.md:1-7, :87, :103, :121-133; G5:55; BG:88-90.
- **Nhãn:** `[rà lại 8.1]`.

### A2. Chia đoạn

Sáu khối N2-01 → N2-06 cùng một đợt đo (8.1 G3, 25/10/2026) và cùng một cách đo — ghi một lần ở đây, các khối sau ghi "như N2-01". Mã biến thể của G3: H1 = chỉ kiểm 1 tokenizer, H2 = gộp đoạn cùng mục tới T token, H3 = gộp dòng bảng liền nhau, B10 = ngân sách gấp đôi.
32 câu dev số chính có nhãn đoạn đúng (nhãn v1, sha `0b65d1c138d2`, kho cũ 8.459 đoạn); 88 câu cho chỉ số keyword. Chỉ số quyết `ctxB_gold_all` = câu có **đủ** đoạn đúng trong phần
đưa model, cắt theo **cùng ngân sách 750 token** (đếm bằng bộ tách token `o200k_base` của OpenAI) cho mọi cách để đoạn to không "tự thắng"; B10 = ngân sách 1.500 token (≈ cỡ 10 đoạn). So theo cặp, bootstrap 10.000, CI 95 %, Holm
(G3:64-67, :162-181). Không có judge (chỉ tầng tìm / đưa đoạn). Sàn ghi trước: **0 câu mất đoạn đúng**; keyword trong ngữ cảnh: cận dưới CI ≥ −2,0 điểm %; biến thể "tốt hơn" mới chạy bước câu trả lời
(G3:66-67; CD:90-92). Ngân sách 750 ghi lúc 12:59:42 trước mọi biến thể (G3:41).

#### N2-01 — Cỡ đoạn: không gộp hay gộp đoạn cùng mục
- **Vấn đề:** đoạn hiện rất nhỏ (trung vị 85 token, 1.787 đoạn dưới 50 token — đo 24/10 trên kho cũ, CD:17-18). Gộp các khối liền nhau cùng mục cho to ra có giúp đưa đúng đoạn vào ngữ cảnh không, hay giữ "mỗi khối Markdown một đoạn".
- **Ngày / Phase:** bản đầu 11–12/09/2026 (Phase 2 toàn kho); thử lại 25/10/2026 (8.1 G3).
- **Phương án + mốc:**
  - Mốc (đang chạy): một khối = một đoạn, không gộp, không gối đầu có chủ đích; khối quá dài thì tách bảng theo dòng / danh sách theo mục / đoạn văn theo câu (CD:12-15). Kho lúc thử: 8.459 đoạn.
  - Lịch sử 09/2026: bản đầu gộp cùng đường tiêu đề theo trần token → 3.318 đoạn; review Codex bắt bỏ "gộp lấp chỗ trống mù" → 8.460 đoạn (INV:98; `reports/full_corpus_rag_wave_1_codex_review_2026_09_12.md:47-70`). Bản 3.318 đoạn **chưa từng được tạo vector / đo** (INV:98).
  - Bản món ăn (08/2026): cắt theo 400 ký tự, bảng giữ nguyên — đã gỡ 24/10 (CD:120-121); không so với cách chia toàn kho.
  - 8.1 G3: H2 gộp đoạn cùng mục tới T = 128 / 256 / 384 / 512 token (dựng trên H1 — N2-05); B10: H2 384 / 512 với ngân sách gấp đôi.
- **Cách đo / tiêu chí ghi trước:** như mô tả đầu A2.
- **Kết quả số** (G3:95-115, :184-193):
  - T 128: 0,000, 0 / 32 / 0, p Holm 1,0 ⇒ **không khác** (keyword cận dưới −2,841, vượt mức tụt).
  - T 256: −0,125 [−0,250; −0,031], 0 / 28 / 4, p Holm 0,091 ⇒ **kém hơn** (mất 4 câu).
  - T 384: −0,156 [−0,312; 0,000], 1 / 25 / 6, p Holm 0,135 ⇒ **kém hơn** (mất 6 câu).
  - T 512: −0,188 [−0,312; −0,062], 0 / 26 / 6, **p Holm 0,018** ⇒ **kém hơn** (tụt có CI sau Holm).
  - B10: H2 384 so H1 0,500 → 0,344 (1 / 25 / 6, p 0,062); H2 512 0,500 → 0,312 (0 / 26 / 6, **p 0,009**) ⇒ **kém hơn**.
  - Theo dõi: đoạn to **tìm thấy** nhiều hơn (T 512: top-10 5 / 26 / 1, pool 3 / 29 / 0) nhưng chỉ ~4–5 đoạn vừa ngân sách thay vì ~9 (G3:111-115, :176-181).
  - Bước câu trả lời (§4, 2×2) **NOT RUN** — không có biến thể "tốt hơn" (G3:9-10).
- **Tiền + tốc độ:** 0 USD; "khoảng 1 giờ máy tính" cho cả G3 (G3:217). Latency đo khi máy chạy song song việc khác ⇒ chỉ theo dõi (G3:227).
- **Quyết định + lý do:** **giữ cách chia hiện tại**; User đóng 8.1 lúc 15:27 25/10/2026 (PS:84); bảng kết luận 8.1 dòng 1 (G5:22). Trước đó User 24/10 "Chunker giữ nguyên tới khi có baseline 7B" (PS:175).
- **Giới hạn:** 32 câu có nhãn (G3:222-223); chỉ đo tầng tìm / đưa đoạn, không đo câu trả lời, không xác nhận trên test; ngân sách đếm token khối bằng chứng, không gồm câu hỏi / prompt (G3:229-230);
  kho cũ 8.459 đoạn, nhãn v1; lúc đó đưa model 5 đoạn (nay 10 — B10 là phép thử gần nhất với cỡ 10).
- **Bằng chứng:** G3 §3.3, §3.7, §3.8 (G3:95-115, :162-218); CD:88-107; G5:22; plan `R81/phase_8_1_g3_plan.md` sha `9f00c460c3e9` (G3:3-4).
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]` (tầng tìm tất định nên không cần A/A; "một lần chạy" vì cỡ mẫu 32).
- **Suy ra:** "đoạn to tìm thấy nhiều hơn nhưng chiếm chỗ" là lời giải thích của G3 / G5 (G5:22 tự ghi *suy ra*), không phải phép đo riêng.

#### N2-02 — Small-to-big: mở rộng ra cả mục sau khi tìm
- **Vấn đề:** tìm bằng đoạn nhỏ rồi đưa model cả mục (tiêu đề lá) chứa đoạn đó có giúp đủ bằng chứng hơn không.
- **Ngày / Phase:** 25/10/2026, 8.1 G3 §3.4.
- **Phương án + mốc:** mốc = chỉ mục đang chạy, đưa từng đoạn; phương án = mở rộng đoạn tìm được tới cả mục lá (không build index mới, G3:117-120).
- **Cách đo / tiêu chí ghi trước:** như N2-01 (Holm 1).
- **Kết quả số:** `ctxB_gold_all` −0,250 [−0,406; −0,125], **0 / 24 / 8**; `ctxB_gold_frac` −0,183 [−0,281; −0,096]; keyword −15,53 [−23,49; −8,14] ⇒ **kém hơn** (G3:119-130). Token ngữ cảnh trung bình 674,9 (mốc 666,1).
- **Tiền + tốc độ:** 0 USD; tốc độ chưa đo riêng.
- **Quyết định + lý do:** bỏ; đoạn "anh em" của 1–2 đoạn đầu chiếm gần hết ngân sách (G3:129-130). User đóng 8.1 15:27 25/10 (PS:84); G5:22.
- **Giới hạn:** như N2-01.
- **Bằng chứng:** G3:117-130; CD:100.
- **Nhãn:** `[kho, cấu hình cũ]` `[một lần chạy]`.

#### N2-03 — Bảng dài: tách từng dòng hay nhóm dòng
- **Vấn đề:** bảng dài (bảng giá, lịch) bị tách từng hàng kèm dòng tiêu đề bảng ⇒ dòng giá đứng riêng, khó tìm (CD:21, CD:61). Có nên nhóm vài dòng?
- **Ngày / Phase:** 09/09/2026 (khảo sát token mẫu, trước khi chốt Phase 2); 25/10/2026 (8.1 G3 H3).
- **Phương án + mốc:**
  - Mốc: mỗi dòng một đoạn + dòng tiêu đề bảng (`full_corpus_chunker.py:400`, CD:61). Tài liệu quyết định 09/2026 lại ghi "nhóm hàng có nghĩa, **không đặt một hàng làm mặc định**" (INV:99).
  - 09/09/2026 (khảo sát trên 6 mẫu, gồm một bảng giá): P1 (gộp hàng + tách điều kiện ra đoạn riêng), P3a (mỗi hàng + lặp đủ cả hai đoạn điều kiện), P3b (nhóm hàng + lặp điều kiện loại trừ, lượt 3 thêm câu dẫn) — **chỉ đếm token**, tự ghi "không phải quality PASS" (khảo sát token 09/09:103-200, :321-344).
  - 8.1 H3: gộp các dòng liền nhau của cùng bảng (dựng trên H1): 100 đoạn dòng bảng → 61 (G3:52).
- **Cách đo:** 09/09 — số token theo 3 tokenizer + MiniLM; 8.1 — như N2-01.
- **Tiêu chí ghi trước:** 09/09 — vừa trần token + cắt đúng chữ (chỉ kỹ thuật); 8.1 — như N2-01.
- **Kết quả số:**
  - 09/09: P3a tràn trần ở 3 / 4 đoạn giá (HuyDang / MiniLM) (khảo sát token 09/09:110-115); gộp hai nhóm dòng + câu dẫn tràn HuyDang 264 > 256 (:141-143); P3b lượt 3 vừa trần nhưng 2 đoạn sát trần HuyDang (248, 245 / 256) (:197).
    Kiểm lại 2 đoạn ghép sau sửa ranh giới: vừa mọi trần (`reports/full_corpus_vn_qt_token_check_2026_09_09.md:100-123`).
  - 8.1 H3 so H1: `ctxB_gold_all` 0,000, 0 / 32 / 0; `ctxB_gold_frac` −0,010 [−0,031; 0]; keyword −0,284 [−0,852; 0]; `ctx5` +0,031 (1 / 31 / 0) ⇒ **không khác** (G3:83-93). Trần chỉ 7 câu có thể đổi (G3:222-223, G5:31).
- **Tiền + tốc độ:** 0 USD; chưa đo tốc độ riêng.
- **Quyết định + lý do:** giữ tách từng dòng (G5:31; PS:84). Gốc vấn đề "bảng giá khó tìm" chuyển sang khâu tìm / xếp đoạn (CD:144).
- **Giới hạn:** khảo sát 09/09 chỉ 6 mẫu, chỉ token; 8.1 trần thấp (7 câu); không đo câu trả lời.
- **Bằng chứng:** khảo sát token 09/09 (dòng như trên); G3:83-93; INV:99; G5:31; CD:61, CD:97.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.
- **Suy ra:** cách "mỗi dòng một đoạn" của code đi ngược ý "không đặt một hàng làm mặc định" của tài liệu 09/2026 (INV:99 có ghi lệch này); 8.1 chỉ thử "gộp dòng liền nhau", chưa thử đúng P1 / P3b của khảo sát 09/09.

#### N2-04 — Tiền tố tiêu đề trong text tìm kiếm
- **Vấn đề:** text đem tạo vector và đếm từ khoá = tên tài liệu + đường tiêu đề + các phần bằng chứng ("Representation A", CD:46). Với đoạn vụn, phần nhãn chiếm nhiều token và từ trong tiêu đề lặp ở mọi đoạn cùng file (INV:104). Có nên rút gọn?
- **Ngày / Phase:** chốt 11/09/2026 (User, spec chung §5 — INV:104; PS:194); thử lại 25/10/2026 (8.1 G3 §3.5).
- **Phương án + mốc:** mốc = tiền tố đầy đủ; `p_nearest` = chỉ tiêu đề mục gần nhất; `p_none` = không tiền tố. "Representation B" (thêm ngữ cảnh do model viết vào đoạn) **chưa build, chưa đo** (code đã gỡ 26/10).
- **Cách đo:** như N2-01 (Holm 2). Keyword / MRR không dùng để quyết vì tính trên chính `search_text` đã bị cắt (G3:141-145).
- **Tiêu chí ghi trước:** như N2-01.
- **Kết quả số** (G3:134-140): `p_nearest` −0,094 [−0,281; +0,094], 4 / 21 / **7**, p Holm 0,457 ⇒ **kém hơn** (vỡ sàn, mất 7 câu); `p_none` −0,156 [−0,344; +0,031], 3 / 21 / **8**, p Holm 0,317 ⇒ **kém hơn** (mất 8 câu). Top-10 đổi ở 120 / 120 câu.
- **Tiền + tốc độ:** 0 USD; chưa đo tốc độ riêng.
- **Quyết định + lý do:** giữ tiền tố đầy đủ (G3:145; G5:45); User đóng 8.1 15:27 25/10 (PS:84).
- **Giới hạn:** như N2-01; kết luận dựa vào sàn (mất câu), CI chứa 0.
- **Bằng chứng:** G3:132-145; CD:70, CD:101; G5:45; INV:104.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.

#### N2-05 — Ràng buộc 3 tokenizer hay chỉ e5-small
- **Vấn đề:** mỗi đoạn phải vừa cả 3 tokenizer (e5-small 512, e5-base 512, HuyDang 256) — lý do gốc "ba model vector ứng viên" đã hết vì chatbot chỉ dùng e5-small (CD:48-50, CD:167-168). 23 khối bị tách thành 90 đoạn chỉ vì HuyDang (INV:100).
- **Ngày / Phase:** chốt 11/09/2026 (User, spec chung §5 — INV:100); thử lại 25/10/2026 (8.1 G3 H1).
- **Phương án + mốc:** mốc = 3 tokenizer; H1 = chỉ kiểm e5-small 512 ⇒ 8.398 đoạn (−61), 14 file đổi (G3:51).
- **Cách đo / tiêu chí ghi trước:** như N2-01 (Holm 1).
- **Kết quả số:** `ctxB_gold_all` 0,000 [0,000; 0,000], 0 / 32 / 0; `ctx5` / `top10` 0 / 32 / 0; keyword trong ngữ cảnh −0,758 [−3,409; +1,136], 1 / 86 / 1 — cận dưới vượt −2,0 do đúng 1 câu ⇒ **không khác** (G3:69-81).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** "không khác — bỏ được, đề xuất dọn" (G5:33, G5:74) nhưng **chưa làm**: chỉ là lựa chọn nếu sau này build lại vì lý do khác (CD:141-142). Code vẫn kiểm 3 tokenizer (CD:133).
- **Giới hạn:** trần thấp (H1 ≤ 13 câu có thể đổi, G3:222-223); 1 câu tụt keyword cần nhắc khi đề xuất (G3:233).
- **Bằng chứng:** G3:69-81; G5:33; CD:96, CD:141-142, CD:164-168.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.

#### N2-06 — Ba sửa nhỏ dữ liệu (biến thể S1 / S2 / S3 của G3)
- **Vấn đề:** (S1) file danh mục của một mảng (không phải nội dung cho khách) vẫn được đưa vào chỉ mục; (S2) 2 khối code bị bộ đọc Markdown bỏ qua không báo; (S3) 3 cặp đoạn lặp một phần thân (trái với "không gối đầu") (CD:63-65; INV:87, :103).
- **Ngày / Phase:** 25/10/2026 (8.1 G3 §3.6); S1 áp ở đợt sửa kho 28/10/2026.
- **Phương án + mốc:** mốc = bộ chia đoạn đang chạy; S1 bỏ 33 đoạn danh mục; S2 thêm 2 đoạn code; S3 bỏ 3 đoạn lặp (G3:56-58).
- **Cách đo / tiêu chí ghi trước:** như N2-01 (Holm 3).
- **Kết quả số:** cả ba 0 / 32 / 0 ở `ctxB_gold_all`, keyword 0 / 88 / 0, `top10` / `ctx5` 0 / 32 / 0 ⇒ **không khác** (G3:147-160). Ở mốc, đoạn danh mục lọt top-10 ở 2 / 120 câu dev (G3:157).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** "an toàn, đề xuất dọn" (G5:58-60). S1 được áp trong đợt sửa kho 28/10 (205 → 204 file, bỏ 33 đoạn; CD:65, CD:79-80) — quyết định đó thuộc đợt sửa kho (User đóng đợt 1 lúc 13:26 28/10, PS:143; xem K3), không do 8.1. S2, S3: **chưa làm** (CD:141-142).
- **Giới hạn:** như N2-01; một phần "top-10 đổi" do mã đoạn bị đánh số lại (G3:155).
- **Bằng chứng:** G3:147-160; G5:58-60; CD:63-65, CD:102, CD:141-142.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.

### A3. Vector nghĩa + từ khoá (BM25)

#### N2-07 — Chọn model vector trên bản món ăn (Phase 8 cũ, notebook 08a)
- **Vấn đề:** chọn model tạo vector nghĩa cho tiếng Việt.
- **Ngày / Phase:** 29/08/2026, Phase 8 cũ (bản món ăn, do AGY / Codex làm), lịch sử.
- **Phương án + mốc:** mốc = e5-small 384; ứng viên e5-base 768, HuyDang DEk21 768; MiniLM-L12 và Qwen3-Embedding-0.6B (384 chiều cắt ngắn) chạy rồi bị loại (08a:28-37, :146-148).
- **Cách đo:** 45 câu bản món ăn, 572 đoạn; Recall@5 / MRR@5 / nDCG@5; 3 lần lặp; bootstrap 10.000, seed 42, CI 95 %; 9 nhóm câu có rào (spec 08a:302-333). Không judge.
- **Tiêu chí ghi trước:** "thắng rõ" = mọi rào nhóm đạt + chênh nDCG@5 ≥ 0,03 + cận dưới CI > 0 (spec 08a:325-331).
- **Kết quả số** (08a:91-100):
  - e5-small: 41 / 45 trúng, MRR@5 0,7748, nDCG@5 0,7425 (mốc).
  - HuyDang: 40 / 45, MRR@5 0,7211, nDCG@5 0,7164; chênh nDCG −0,0262 [−0,1270; +0,0749]; rào nhóm **FAIL** (6/9) ⇒ không thắng.
  - e5-base: 42 / 45, MRR@5 0,6985, nDCG@5 0,7061; chênh −0,0364 [−0,1002; +0,0219]; rào **FAIL** (7/9) ⇒ không thắng.
  - MiniLM-L12: cắt cụt 83 đoạn (14,5 %), nDCG@5 0,4709, trượt 7/9 rào ⇒ loại; Qwen3-0.6B: nDCG@5 0,6175, ~765 s / 572 đoạn trên CPU ⇒ loại (08a:146-148).
- **Tiền + tốc độ:** 0 USD (chạy máy). Tổng thời gian tìm p50 / p95: e5-small 27,40 / 39,75 ms; HuyDang 71,24 / 114,62 ms; e5-base 57,09 / 88,44 ms (08a:104-108).
- **Quyết định + lý do:** giữ e5-small làm mặc định (không ứng viên nào "thắng rõ"); User 29/08 rút về 3 cấu hình, loại MiniLM / Qwen (08a:28-35).
- **Giới hạn:** chỉ bản món ăn (45 câu, 572 đoạn), cách chia khác bản toàn kho; thước "trúng top-5" cũ; inventory xếp "chỉ đo trên Foods" (INV:112).
- **Bằng chứng:** 08a:28-37, :91-109, :146-148; spec 08a:302-333; INV:112.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]`.

#### N2-08 — Model vector toàn kho: 4 model → thu về 2
- **Vấn đề:** ở bản toàn kho, giữ những model vector nào làm ứng viên.
- **Ngày / Phase:** 12–13/09/2026 (Phase 3–4: 4 model); 23–24/10/2026 (Phase 7A2: thu về 2).
- **Phương án + mốc:**
  - 12/09: 4 model (e5-small, e5-base, HuyDang, Qwen-0.6B) chạy vector trên **mẫu 12 đoạn**, chưa chọn model thắng (EM:54, EM:98-100).
  - 12–13/09: dựng 4 collection toàn kho, mỗi model một cái, 8.460 điểm (QD:69); Qwen-0.6B chạy trên GPU GTX 1650: đỉnh VRAM ~1,26 GB (theo báo cáo đó; EM:55 ghi ~1,23 GB — xem Phụ lục C), ~65 phút (`reports/qwen3_gtx1650_embedding_execution_report_2026_09_13.md:44`, `:49`).
  - 7A2 (23/10): chỉ giữ e5-small (trên máy) + Qwen3-Embedding-8B (qua OpenRouter); bỏ e5-base, HuyDang, Qwen-0.6B (spec 7A2:30; PS:190).
  - Smoke 10 (24/10, 7A2): e5-small so 8B (index 8B lần 1 trộn 3 nhà cung cấp).
- **Cách đo:** 4 collection 09/2026 **chưa từng chấm Golden** (INV:113). Smoke 10: 10 câu smoke, keyword có trong top-10, không ngưỡng (gate 2 7A2:211-216).
- **Tiêu chí ghi trước:** thu về 2 model — **không ghi lý do** (INV:113); smoke 10 — "không ngưỡng" (gate 2 7A2:215).
- **Kết quả số:** smoke 10: e5 **18/19**, 8B **17/19** keyword; latency e5 ~22–31 ms, 8B ~1,1–1,5 s (một câu 8,8 s) (gate 2 7A2:230-233). Build 8B lần 2 (ghim Nebius) lỗi HTTP 504 ⇒ index 8B hoãn sang Phase 8 (gate 2 7A2:314; PS:171).
- **Tiền + tốc độ:** như trên; tiền build 8B ở 7A2 — chưa kiểm.
- **Quyết định + lý do:** User 23/10 (spec 7A2 §2) giữ 2 model, mặc định e5-small, "cutover 8B chờ bằng chứng" (PS:190); User 24/10 tối: vector Phase 8 chỉ e5-small + 8B (PS:182). Code e5-base / HuyDang / Qwen-0.6B / nhánh GPU gỡ 24/10 và 26/10 (EM:55, EM:113).
- **Giới hạn:** không có phép so chất lượng toàn kho giữa 4 model; smoke 10 quá nhỏ, index 8B lúc đó trộn nhà cung cấp.
- **Bằng chứng:** EM:54-55, EM:93-100; QD:69; INV:112-113; gate 2 7A2:211-233; spec 7A2:30.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[một lần chạy]`.
- **Ghi chú:** 8.1 **không** thử lại model vector (G5:28 "NOT RUN ở 8.1"); phép thử lại thật là N2-09.

#### N2-09 — Qwen3-Embedding-8B thay e5-small
- **Vấn đề:** model vector lớn (4.096 chiều, gọi qua mạng) có tìm được đoạn đúng nhiều hơn e5-small không.
- **Ngày / Phase:** 30/10/2026 (sau 8.2, kho sau sửa đợt 2, 8.424 đoạn); B chạy, C kiểm.
- **Phương án + mốc:** mốc = e5-small (đang chạy, kho đợt 2, 10 đoạn ngữ cảnh, pool 30, RRF k 60); phương án = chỉ đổi model vector sang `qwen3-embedding-8b-4096` (OpenRouter, ghim Nebius, `data_collection: deny`); mọi thứ khác giữ (R27/qwen3_8b_plan.md:138-139; EM:62-64).
- **Cách đo:** nhãn đoạn đúng **v5** (`33d16fd6b8f4`), dev 40 câu có nhãn (quyết), test 15 (xác nhận); chỉ số quyết `context_gold_all` (mọi ý có trong ngữ cảnh **10 đoạn**); A/A cho 8B (nhúng câu hỏi hai lần cùng index); bootstrap 10.000, seed `20261024` (R27/qwen3_8b_plan.md:46-70; R27/qwen3_8b_implementation.md:20). Bước câu trả lời **NOT RUN** (chỉ chạy nếu tầng tìm tốt hơn).
- **Tiêu chí ghi trước:** thắng ròng, CI 95 % > 0, vượt A/A 8B; **sàn 0 câu mất đoạn đúng** (spec 8.2 §10.2); theo dõi chênh `dense_ms` so +50 ms và p95 cả câu ước so trần 5 s của User; trần tiền 0,10 USD (plan:142-155; impl:3-4).
- **Kết quả số** (impl:32-45):
  - dev 40: 0,600 ⇒ 0,575; −0,025 [−0,125; +0,075]; **2 / 35 / 3**; 3 câu mất đoạn đúng, lượt A/A mất đúng 3 câu đó.
  - test 15: 0,600 ⇒ 0,533; [−0,333; +0,200]; 2 / 10 / 3 (3 câu mất).
  - pool vector dev 0,825 ⇒ 0,775 (4 / 30 / 6); MRR keyword 0,731 ⇒ 0,736 (n 108).
  - A/A 8B: cos min 0,99985; top-10 đổi 27 / 108 câu; `context_gold_all` đổi 0 / 40.
  - ⇒ **kém hơn** (vỡ sàn ở cả dev và test; CI chứa 0, nghiêng âm).
- **Tiền + tốc độ:** **0,0089 USD** (build ≈ 870.531 token ≈ 0,0087 USD; impl:14, :23). `dense_ms` p50 / p95: e5 21 / 28 ms ⇒ 8B **2.228 / 6.487 ms** (test p95 25.008 ms; 1 lần 504 sau ~62 s); p95 cả câu ước ≈ **11,4 s** (trần 5 s) (impl:39-41).
- **Quyết định + lý do:** **giữ e5-small** — vỡ sàn (luật quyết); thêm: quá chậm (chỉ theo dõi); User 30/10 16:12: không giữ bộ đệm vector, chỉ ghi kết quả; harness giữ ở tag `hoso/b92-qwen3-harness`, không merge (PS:140; EM:66-69). Collection thử đã xoá (QD:61-62).
- **Giới hạn:** nhãn chỉ 40 + 15 câu ⇒ chỉ thấy hiệu ứng lớn, "kém hơn" dựa trên sàn chứ không phải CI; một lần build (nhiễu phía index không đo); latency một khung giờ (impl:57-61). Không đo: 8B làm rerank, instruction khác, nhà cung cấp khác (impl:55).
- **Bằng chứng:** R27/qwen3_8b_implementation.md:8-45; review R27/qwen3_8b_review.md:9, :16-17 (ready, số khớp); plan sha `d6d6c7d51584`; EM:16-17, EM:53, EM:62-69, EM:136-138; QD:50, QD:61-62.
- **Nhãn:** `[xác nhận nhóm kiểm]` (test 15 câu cũng mất 3 câu). Đây là một trong ít so sánh **đo trên kho hiện tại**.
- **Suy ra:** EM:67-68 nói phần thiếu lớn hơn là xếp hạng (9 / 40 câu có đoạn đúng trong 30 ứng viên nhưng rơi khỏi 10 đoạn) — số này khớp impl:20 (pool vector 33, ngữ cảnh đủ 24 ⇒ 33 − 24 = 9, agent gom thẻ tự trừ).

#### N2-10 — Cách gọi Qwen3-8B qua OpenRouter (ghim nhà cung cấp, số chiều)
- **Vấn đề:** vector qua API phải lặp lại được giữa các lần gọi; chọn nhà cung cấp và số chiều.
- **Ngày / Phase:** khảo sát 23/10/2026; quyết định User 24/10/2026 (Phase 7A2).
- **Phương án + mốc:**
  - Không ghim (OpenRouter tự chọn) so ghim DeepInfra / Nebius / SiliconFlow (khảo sát OpenRouter:77-100).
  - `dimensions: 1024` (cắt MRL — Matryoshka: cắt bớt chiều vector mà vẫn dùng được) so 4.096 gốc (khảo sát OpenRouter:102-110).
- **Cách đo:** 10 lần gọi (8 embedding, 2 GET), 64 đoạn thật; cos giữa các lần gọi; build 8B lần 1 không ghim đo cos mẫu.
- **Tiêu chí ghi trước:** kiểm vector bằng cos ≥ 0,999 (spec 7A2:129-139); không thấy tiêu chí chọn nhà cung cấp ghi trước khảo sát.
- **Kết quả số:**
  - Nebius gửi lại cùng batch: cos 1,00000000 (không giống từng bit); khác batch cùng Nebius cos ≥ 0,99988; Nebius so SiliconFlow fp8 cos ≥ 0,99985 (khảo sát OpenRouter:121-134).
  - DeepInfra: HTTP 429 "Model busy", chưa có lần gọi thành công (:144-157).
  - Build lần 1 không ghim: trộn 3 nhà cung cấp, cos mẫu min 0,99535 < 0,999 (spec 7A2:131-133, :187-188).
  - `dimensions: 1024`: được chấp nhận, khớp cắt đầu + chuẩn hoá lại (cos 1,0), chỉ thử 1 giá trị / 1 nhà cung cấp / 4 input (:102-110, :160).
- **Tiền + tốc độ:** khảo sát 4,81e-4 USD (:74-75); p50 30 phút theo listing: Nebius 1.454,5 ms, DeepInfra 922 ms, SiliconFlow 1.521,5 ms (:81-85).
- **Quyết định + lý do:** **ghim Nebius**, không dự phòng, `data_collection: deny` (User 24/10, PS:172; spec 7A2:33, :129-133); 1.024 chiều "thăm dò 1 lần, không chọn" (INV:114). Index 8B lần 2 lỗi 504 ⇒ hoãn (PS:171).
- **Giới hạn:** số mẫu nhỏ; ổn định chỉ đo trên Nebius; latency là số đơn lẻ (:152-170).
- **Bằng chứng:** như trên; INV:117.
- **Nhãn:** `[một lần chạy]` `[chưa kiểm lại Phase 0–7]`.

#### N2-11 — BM25: cách tách từ
- **Vấn đề:** BM25 tách theo âm tiết (các âm tiết của một tên ghép bị tách rời) ⇒ có thể yếu với tên ghép tiếng Việt (EM:20; INV:118).
- **Ngày / Phase:** 30/08/2026 (08b, bản món ăn); 25/10/2026 (8.1 G4 phần từ khoá — B làm, C kiểm).
- **Phương án + mốc:**
  - 08b: `unicode_word` (regex `\w+`, âm tiết) so `underthesea_word` (tách từ ghép) (08b:67-71).
  - 8.1: mốc âm tiết (5.660 từ); T1 ghép cặp âm tiết (105.999 từ); T2 giữ mã số nguyên cụm (6.719); T3 `pyvi` (14.211) — mỗi cách × 2 cách trộn (đang chạy: BM25 chấm lại 30 đoạn của vector; mở rộng: native pool 100) (G4K:76-79, :81-92).
- **Cách đo:** 08b — 45 câu món ăn, Recall@30, nDCG@5, 3 lần lặp. 8.1 — 32 câu dev có đoạn đúng (nhãn `0b65d1c138d2`, kho cũ 8.459 đoạn), chỉ số "đủ đoạn đúng trong 5 đoạn"; 88 câu keyword; Holm 6; cổng tương đương với code đang chạy PASS (108 / 108 câu giống) (G4K:22-51).
- **Tiêu chí ghi trước:** 08b — không thấy trong phần đã đọc (chọn theo "đơn giản"); 8.1 — không câu nào mất đoạn đúng, keyword không tụt quá 2 điểm %, phải tốt lên có ý nghĩa (EM:80-81; G4K:14-15).
- **Kết quả số:**
  - 08b: âm tiết R@30 0,9519 / nDCG@5 0,6478 / p95 5,3 ms; underthesea 0,9556 / 0,6416 / 14,8 ms (08b:69-70) ⇒ chọn âm tiết vì đơn giản.
  - 8.1 (G4K:83-90): cặp âm tiết · đang chạy +0,000, 1 / 30 / 1 (mất 1) ⇒ **kém hơn**; · mở rộng −0,031, 2 / 27 / 3, keyword −2,65 ⇒ **kém hơn**; pyvi · đang chạy −0,031, 0 / 31 / 1 ⇒ **kém hơn**; · mở rộng −0,094, 1 / 27 / 4, keyword −2,27 ⇒ **kém hơn**;
    mã số nguyên cụm 0 / 32 / 0 cả hai ⇒ **không khác**. p Holm = 1,0 mọi dòng.
- **Tiền + tốc độ:** 0 USD; BM25 ms / câu: âm tiết 0,9 (đang chạy) / 9,0 (mở rộng); pyvi 1,8 / 8,4; fit pyvi chậm nhất 6,9 s (G4K:28, :57-63).
- **Quyết định + lý do:** giữ tách theo âm tiết (G5:40; EM:48); User đóng 8.1 15:27 25/10 (PS:84).
- **Giới hạn:** 32 câu, trần cứu được: đang chạy 11 / mở rộng 16 (G4K:141); kho cũ; 5 đoạn ngữ cảnh; nhãn v1.
- **Bằng chứng:** G4K:53-92, :123-137; 08b:67-71; G5:40; EM:48, EM:83-91.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.

#### N2-12 — BM25 tham số k1 / b (và k của trộn RRF, đo cùng đợt)
- **Vấn đề:** k1 1,5 / b 0,75 lấy từ bản món ăn; độ dài đoạn trung bình toàn kho khác hẳn (INV:119).
- **Ngày / Phase:** 30/08/2026 (08b); 25/10/2026 (8.1 G4K nhánh P).
- **Phương án + mốc:**
  - 08b: mốc k1 1,5 / b 0,75; k1 1,2; k1 1,8; b 0,5; b 1,0 (08b:60-65).
  - 8.1: đang chạy b 0,5 / 1,0; mở rộng k RRF 10 / 30 và b 0,5 / 1,0 (k RRF ở cách "đang chạy" đo ở G1.3 — T3-02) (G4K:109-121).
- **Cách đo:** như N2-11 (8.1: Holm chung 6).
- **Tiêu chí ghi trước:** 08b — rào nhóm câu + nDCG@5 phá hoà (08b:62-64); 8.1 — như N2-11.
- **Kết quả số:**
  - 08b: b 0,5 trượt rào nhóm; mốc và b 1,0 hoà R@30 0,9519; phá hoà nDCG@5 0,6478 so 0,6442 ⇒ giữ mốc (08b:62-65).
  - 8.1 (G4K:111-118): đang chạy b 0,5 +0,031, 1 / 31 / 0 ⇒ chưa rõ; b 1,0 1 / 30 / 1 (mất 1) ⇒ **kém hơn**; mở rộng k 10 +0,031, 1 / 31 / 0, keyword −2,27 ⇒ chưa rõ; k 30 0 / 32 / 0 ⇒ không khác; b 0,5 0 / 31 / 1, keyword −2,84 ⇒ **kém hơn**; b 1,0 1 / 29 / 2 ⇒ **kém hơn**.
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** giữ k1 1,5 / b 0,75 / k 60 (G5:41, G5:30; EM:51, EM:116); User đóng 8.1 (PS:84).
- **Giới hạn:** như N2-11; "chưa rõ" do cỡ mẫu.
- **Bằng chứng:** G4K:109-121; 08b:60-65; G5:30, :41; EM:51, EM:89.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.

#### N2-14 — BM25 hay TF-IDF cho phần từ khoá (bản món ăn)
- **Vấn đề:** chọn công thức chấm từ khoá.
- **Ngày / Phase:** 30/08/2026, notebook 08b (bản món ăn), lịch sử.
- **Phương án + mốc:** BM25 (âm tiết, k1 1,5 / b 0,75) so TF-IDF (log-TF, smoothed-IDF, chuẩn hoá L2, 2.093 từ) — riêng lẻ và trộn với 3 model vector (08b:75-92).
- **Cách đo:** 45 câu món ăn × 3 lần lặp; Recall@5 / nDCG@5 / MRR@5; rào nhóm câu.
- **Tiêu chí ghi trước:** rào nhóm (chênh nDCG@5 ≥ −0,02 cho nhóm n ≥ 6) (08b:180-184).
- **Kết quả số:** chỉ từ khoá: BM25 R@5 0,7889 / nDCG@5 0,6478 / MRR@5 0,5960 / p95 6,3 ms; TF-IDF 0,7667 / 0,6150 / 0,5599 / 5,1 ms (08b:130, :140). Ứng viên trộn tốt nhất của cả hai đều trượt rào một nhóm (−0,0279) ⇒ `bm25_finalist = None`, `tfidf_finalist = None` (08b:170-184).
- **Tiền + tốc độ:** 0 USD; như trên.
- **Quyết định + lý do:** TF-IDF bỏ ở Phase 4–5 (EM:103); không thấy ai chốt / ngày trong phần đã đọc.
- **Giới hạn:** chỉ bản món ăn; phần trộn (RRF / trọng số) ở T3-02.
- **Bằng chứng:** 08b:75-92, :130, :140, :170-184; EM:103.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]`.
- **Suy ra:** việc bỏ TF-IDF dựa trên số BM25-riêng cao hơn; nguồn chỉ ghi "bỏ ở Phase 4–5" không kèm lý do.

### A4. Lưu trữ Qdrant

#### N2-15 = T3-04 — Qdrant: tìm gần đúng (HNSW) hay tìm chính xác
- **Vấn đề:** tìm gần đúng (HNSW mặc định) có làm rơi đoạn so với tìm chính xác không — "chưa từng so" trước 8.1 (INV:126).
- **Ngày / Phase:** 24/10/2026, 8.1 G1.2 (B làm).
- **Phương án + mốc:** mốc HNSW mặc định (m 16, ef_construct 100), pool 30; phương án `exact`.
- **Cách đo:** 108 câu dev; so top-10, tập 30 đoạn vector, `top10_gold_all`, MRR, latency (G1:62-65). 0 USD.
- **Tiêu chí ghi trước:** "trùng top-10 ≥ 99 % câu và gold_all không đổi ⇒ giữ HNSW" (`R81/phase_8_1_g1_plan.md:47-53`) (review 01/11 mở nguyên văn: khớp).
- **Kết quả số:** top-10 giống hệt **108 / 108**; tập 30 đoạn vector giống 108 / 108; `top10_gold_all`, MRR không đổi; vector p50 / p95 20,5 / 24,5 ms so 20,5 / 24,1 ms (G1:64-65) ⇒ **hoà / không khác**.
  Ghi chú: 30 đầu của `limit=100` ≠ `limit=30` ở 1 / 108 câu (HNSW phụ thuộc `limit`) (G5:51; G4K:44-50).
- **Tiền + tốc độ:** 0 USD; tốc độ như nhau (G1:64).
- **Quyết định + lý do:** giữ HNSW (G5:51; BTK:55); User đóng 8.1 (PS:84).
- **Giới hạn:** kho 8.459 điểm; chưa đo lại sau build 30/10 (8.424 điểm).
- **Bằng chứng:** G1:62-65; G1 plan:47-53; G5:51; INV:126; BTK:55.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]`.
- **Suy ra:** "kết quả còn đúng trên kho hiện tại" — suy ra (kho gần cùng cỡ: 8.459 ⇒ 8.424 đoạn, cùng cấu hình), chưa đo.

#### N2-16 — Tổ chức collection, thông tin điểm (payload), xoá collection cũ
- **Vấn đề:** mỗi ứng viên một collection hay chung; thông tin điểm gồm gì; có lọc / index phụ không; khi nào xoá collection cũ.
- **Ngày / Phase:** Phase 4 (12–13/09/2026: 4 collection, mỗi model một cái); metadata v2 (29–30/09/2026: 5 → 7 trường); 7A2 gate 3 + B9 (24/10/2026: xoá).
- **Phương án + mốc:** thông tin điểm 5 trường (cũ) so 7 trường (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`) (QD:78); subdomain / tags / filter **bị loại vì chưa có ai dùng** (INV:125); không payload index (QD:51, QD:83).
- **Cách đo:** không có phép so chất lượng ("Không áp dụng", INV:125). Xoá collection (B9): kiểm tìm giống từng byte, test, API lên (QD:65-67).
- **Tiêu chí ghi trước:** B9 có (tìm giống từng byte, test đạt, API lên — QD:65); metadata v2 / một collection mỗi ứng viên — không thấy tiêu chí so sánh.
- **Kết quả số:** B9 **PASS** — 191 test, giống từng byte, sức khoẻ 200; xoá 2 collection món ăn (mỗi cái 572 điểm) (QD:65-67). 7A2 gate 3: xoá 13 collection cũ (QD:68). Hiện: 1 collection `hue_full_corpus_7a2_e5_small_384`, 8.424 điểm (QD:11-15).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** thông tin điểm v2 7 trường, không index / filter (spec metadata v2, PS:193); xoá collection không dùng sau Phase 7 do A đề xuất, User đồng ý (PS:173), User tự chạy lệnh xoá 2 collection món ăn (QD:66-67).
- **Giới hạn:** quyết định kiến trúc, không có số chất lượng; inventory xếp "chưa so sánh (kiến trúc)" (INV:125).
- **Bằng chứng:** QD:11-15, QD:51, QD:65-69, QD:78, QD:83; INV:125; PS:173, :193.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]`.

### A5. Tìm kiếm + xếp hạng lại

#### T3-01 — Chỗ nghẽn của khâu tìm: thiếu ứng viên hay xếp sai (chẩn đoán)
- **Vấn đề:** trước khi chọn cách sửa khâu tìm, cần biết đoạn đúng bị rơi ở bước nào: không vào được pool ứng viên, hay vào rồi nhưng bị xếp ngoài 10 / 5 đoạn đưa model. Đây là phép **chẩn đoán**, không chọn phương án, nhưng là căn cứ cho T3-03, T3-08, T3-09.
- **Ngày / Phase:** 24/10/2026 (8.1 G1.1, G1.6); 26/10/2026 (B42 phân loại lỗi, đợt cải tiến từng khâu = bước 2 Phase 8.2).
- **Phương án + mốc:** mốc = `dense_bm25_rrf` pool 30 → top-10 → 5 đoạn (8.1) / 10 đoạn (B42). So với: native pool 30 / 100 / 200 (chỉ để đếm tầng).
- **Cách đo:** 40 câu dev có đoạn đúng (nhãn bản 1) cho G1.1 và B42; G1.6 trên 55 câu (dev 40 + test 15 — test đã bị nhìn ở bước chẩn đoán, G1 ghi rõ); thước "đủ đoạn đúng" ở từng tầng (pool / top-10 / ngữ cảnh). Không judge, 0 USD. Kho cũ (trước sửa đợt 1, 2).
- **Tiêu chí ghi trước:** G1.1 / G1.6 là chẩn đoán, không có rào (`R81/phase_8_1_g1_plan.md:42`); có "điều kiện dừng sớm" của spec 8.1 §5 — không chạm (G1:58-60).
- **Kết quả số:**
  - G1.1 (40 câu): pool 30 đủ 0,775, top-10 0,550, 5 đoạn 0,425; native pool 100 hợp hai nhánh **0,975**, top-10 0,600, 5 đoạn 0,500 (G1:50, :52). "9 câu đã đủ ngay trong pool 30 nhưng bị xếp ra khỏi top-10" (G1:60).
  - G1.6: 22 câu bị từ chối nhầm ở 7B — thiếu ở pool 10, rơi khỏi top-10 5, rơi khỏi 5 đoạn 7, đủ tới bước trả lời **0** (G1:111) ⇒ "lỗi tìm / xếp đoạn, chưa phải lỗi prompt" (G1:12-13).
  - B42 (10 đoạn, 40 câu / 101 ý): pool 30 / top-10 / 5 đoạn = 31 / **22** / 17 (R26/phan_loai_loi_B.md:61-63; TH26:40). 18 câu thiếu ở 10 đoạn: 11 ý ngoài pool (8 câu), 12 ý trong pool nhưng RRF xếp ngoài top-10 (11 câu), 1 ý do giới hạn thước (phan_loai_loi_B:13-18).
    5 ý vector đã xếp ≤ 10 nhưng trộn với BM25 đẩy ra ngoài (:16-17). Câu tự nhiên không lợi từ 10 đoạn: 6 / 12 ở cả hai mức (:22).
  - Theo loại câu (10 đoạn): nhiều nguồn 9 / 18, so sánh 8 / 13, có điều kiện 5 / 8 (:88-90).
  - Kết luận: "nghẽn ở xếp hạng" (BTK:99; G1:9-10); K1 sau đó củng cố (pool 100 đủ 37 / 40 nhưng top-10 23 / 40 — R82/phase_8_2_k1_review.md:46-47).
- **Tiền + tốc độ:** 0 USD (G1:115; phan_loai_loi_B:4). Tốc độ: không thuộc phép đo này.
- **Quyết định + lý do:** không phải quyết định chọn; B đề xuất (G1:133-135), A dùng làm căn cứ ưu tiên rerank (G4) và 10 đoạn (G2); B42 dẫn tới trình lại phạm vi đợt cải tiến (TH26:18).
- **Giới hạn:** 40 câu; mỗi ô theo loại câu 1–20 câu, "chỉ định hướng" (phan_loai_loi_B:151); nhãn của agent, mỗi ý chỉ đánh dấu một chỗ (BTK:67); kho cũ, nhãn bản 1. Trên kho hiện tại (30/10, nhãn v5) mới có số tổng: 24 / 40 trong 10 đoạn, 33 / 40 trong 30 ứng viên (BTK:15) — **chưa phân loại lại theo tầng**.
- **Bằng chứng:** G1 §4 G1.1, G1.6 (G1:46-115); R26/phan_loai_loi_B.md §1, §3; TH26:37-41; BTK:15-16, :99-100; K1 review :46-47, :54-55.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]`.
- **Suy ra:** "trên kho hiện tại vẫn nghẽn ở xếp hạng" là BTK:20 nói, dựa trên 33 so 24 (BTK:15) — chưa phân loại lỗi lại; "sửa tầng trả lời không cứu được" là B42 tự ghi là *suy ra* (phan_loai_loi_B:24-25).

#### T3-02 — Cách trộn vector + từ khoá
- **Vấn đề:** ghép kết quả vector (e5-small) với BM25 thế nào: BM25 chỉ chấm lại 30 đoạn vector (`dense_bm25_rrf`, đang chạy) hay hai bên tìm độc lập trong cả kho rồi trộn (`native_hybrid_rrf`); hệ số RRF k; trộn theo điểm (DBSF); thời bản món ăn: trộn trọng số min-max 0,6 / 0,4.
- **Ngày / Phase:** bản món ăn 30/08/2026 (08b, lịch sử); Phase 5 toàn kho 13–14/09/2026 (dựng cả hai cách, không đo chất lượng); 24/10/2026 (7B đo 158 câu); 24–25/10/2026 (8.1 G1.3, G4K phần P); 26/10/2026 (K2 — NOT RUN).
- **Phương án + mốc:** mốc = `dense_bm25_rrf` pool 30, k = 60. Đã thử: native p30; native p100; runtime k ∈ {2, 10, 30}; native p30 k ∈ {2, 10, 30}; DBSF trọng số từ khoá 0,2 / 0,3 (10 biến thể G1.3 — `R81/phase_8_1_g1_plan.md:60-62`);
  G4K: native k 10 / 30, runtime b 0,5 / 1,0, native b 0,5 / 1,0 (BM25 b ở N2-12); K2 = native p30 k = 2 (NOT RUN). Bản món ăn 08b: 20 cấu hình (vector, BM25, TF-IDF, rescore, RRF, trọng số) trên 3 model vector.
- **Cách đo:** G1.3 — 40 câu dev có đoạn đúng (`top10_gold_all`) + 108 câu dev (MRR@10), bootstrap 10.000, Holm trên 10 (G1:67-82); bảng phụ trên tập 32 / 88 câu sau khi bỏ câu không tự nhiên (G1:142-163). 7B — 158 câu trong kho, MRR / nDCG / Coverage keyword, **không theo cặp** (INV:133).
  Bản món ăn 08b — 45 câu Golden V3, Recall@5 / nDCG@5, bootstrap seed 42. Không judge, 0 USD.
- **Tiêu chí ghi trước:** G1.3 — "tốt hơn" = chỉ số chính CI > 0 sau Holm **và** đủ rào ("0 câu trong 40 mất đoạn đúng khỏi top-10", "nDCG@10 không tụt") (G1 plan:66-71). 08b — rào ΔnDCG@5 ≥ −0,02 cho mỗi loại câu có n ≥ 6 (08b:180). 7B: không có tiêu chí ghi trước cho chọn cách trộn.
  K2: spec 8.2 §10.3 bỏ vì "đã trượt Holm-10 ở 8.1; chọn lại trên cùng dev là chọn vì may" (TH26:48).
- **Kết quả số:**
  - 7B (158 câu): native MRR 0,726 / nDCG 0,761 / Coverage 93,41 so runtime 0,721 / 0,755 / 92,35 — "chưa kiểm theo cặp" (INV:133; `reports/phase_7b_gate_1_evaluator_implementation_2026_10_24.md:127`).
  - G1.3 (40 / 108 câu): native p30 +0,025, 3 / 35 / 2, **mất 2**; native p100 +0,050, 3 / 36 / 1, **mất 1**; runtime k = 2 +0,050, 2 / 38 / 0; runtime k = 10 MRR +0,004 [0,001; 0,008] qua Holm nhưng **mất 1**; **native p30 k = 2** +0,100 [0,025; 0,200], 4 / 36 / 0, không qua Holm; DBSF 0,2 +0,050, 2 / 38 / 0, MRR −0,007 (G1:71-78).
    Kết luận: "không biến thể nào tốt hơn" ⇒ chưa rõ; "hiệu ứng MRR mọi biến thể rất nhỏ (≤ 0,01)" (G1:82-84). Tập 32 / 88 câu: không đổi kết luận (G1:160-162).
  - G4K P: native k 10 chưa rõ (keyword tụt −2,27), native k 30 không khác (G4K:115-116).
  - K2: **NOT RUN** (TH26:48).
  - 08b (lịch sử): tốt nhất `hybrid-bm25-weighted` + HuyDang, Recall@5 +0,0741, nDCG@5 +0,0491, CI dương (08b:137, :200-203), nhưng một loại câu ΔnDCG@5 −0,0279 < −0,02 ⇒ không có finalist (08b:173-186). Cấu hình đang chạy (vector → BM25 → RRF) **chưa từng chạy trên bản món ăn** (INV:133).
  - Bản món ăn Phase 4.5 (104 câu, lịch sử): `dense_only` MRR 0,8250 / nDCG 0,8263 so `hybrid_no_rerank` (min-max 0,6/0,4) 0,8246 / 0,8327 (`reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md:26-29`).
- **Tiền + tốc độ:** 0 USD. BM25 trong pool: 0,9 ms / câu (runtime) so 9,0 ms (native pool 100) (G4K:57-58); vector câu hỏi 21–28 ms p50 / p95 (BTK:23).
- **Quyết định + lý do:** **giữ `dense_bm25_rrf`, pool 30, k = 60** (G5:30, :52; PS:47). Lý do: không biến thể nào qua luật; native mất 1–2 câu. B đề xuất giữ native p30 k = 2 làm ứng viên phụ khi có thêm câu (G1:140), A quyết; 8.2 không thử lại (K2 NOT RUN, A 26/10 — TH26:22). Ai chốt: A theo luật 8.1; User duyệt đóng 8.1 / 8.2 (PS:85).
- **Giới hạn:** 40 câu có đoạn đúng, CI rộng, Holm 10 khắt khe — "không khác" nghĩa là chưa chứng minh được (G1:119-120); kho cũ, nhãn bản 1; MRR là proxy keyword; số 7B không theo cặp; bản món ăn là kho khác (572 đoạn). **Chưa đo lại trên kho hiện tại.**
- **Bằng chứng:** G1:67-84, :160-162; G1 plan:56-71; G4K §4.4 (G4K:109-121); G5:30, :52; INV:133, :135; TH26:48; 08b:123-207; code `backend/retrieval/full_corpus.py:482`, `:521`, `:585` (BTK:42).
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]`; phần bản món ăn: `[chưa kiểm lại Phase 0–7]`.
- **Suy ra:** "native p30 k = 2 có tín hiệu rõ nhất" là G1 nói (G1:83); "BM25 xếp lại yếu vì với hạng ≤ 30 đóng góp mỗi nhánh chỉ 1/61–1/90" là INV:135 suy ra từ công thức, chưa đo riêng.

#### T3-03 — Cỡ pool ứng viên 30 hay 100 / 200
- **Vấn đề:** pool 30 là trần của mọi bước sau (kể cả rerank); có nên lấy rộng hơn để đoạn đúng vào được ứng viên?
- **Ngày / Phase:** 24/10/2026 (8.1 G1.1 / G1.3); 25/10/2026 (8.1 G4-B, mốc native pool 100 không rerank); 26/10/2026 (8.2 K1 pool vector 30 → 100).
- **Phương án + mốc:** mốc = runtime pool 30. Đã thử: native pool 100 / 200 (8.1); native pool 100 không rerank trên dev 30 (G4); K1 = pool **vector** 100, giữ cách trộn (8.2).
- **Cách đo:** 8.1 — 40 câu dev (`top10_gold_all`), 108 câu MRR; G4 — dev 30, đoạn đúng trong 5 đoạn; K1 — dev 40, `top10_gold_all`, 10 đoạn, so mốc B1 `811d25d`, Holm họ 2. 0 USD, tất định.
- **Tiêu chí ghi trước:** G1.3 như T3-02. K1: chỉ số quyết `top10_gold_all`; sàn "0 câu mất"; "K1 mất ≥ 1 câu ở dev ⇒ kém hơn; không chạy test, không lượt sinh" (plan K1 §6.2, dẫn ở R82/phase_8_2_k1_review.md:52); latency ≤ +50 ms (K1 review :50).
- **Kết quả số:**
  - 8.1: native p100 top-10 +0,050, 3 / 36 / 1 (mất 1) (G1:72); G4 dev 30: native pool 100 so runtime, đoạn đúng trong 5 đoạn +0,100 [−0,033; +0,233], 4 / 25 / 1 (mất 1) (G4:114-115).
  - K1: `top10_gold_all` +0,025 [−0,050; +0,100], 2 / 37 / 1, Holm 1,0; **mất 1 câu** ⇒ phạm sàn; pool vector đủ 31 → 37 / 40; top-10 22 → 23 / 40; 54 / 108 câu đổi tập top-10; latency TB +8,88 ms (K1 review:43-50) ⇒ **kém hơn** (K1 review:3; TH26:47).
- **Tiền + tốc độ:** 0 USD; K1 +8,9 ms (TH26:47).
- **Quyết định + lý do:** **giữ pool 30**. K1 "kém hơn" do phạm sàn; C review sẵn sàng cho User 26/10; đợt đóng 27/10 (User chọn (1), TH26:33).
- **Giới hạn:** 40 câu; nhãn bản 1, kho cũ; chỉ một biến thể pool rộng ở 8.2 (không kèm rerank vì rerank pool 100 ở 8.1 đã trượt — T3-08).
- **Bằng chứng:** G1:50-60, :72; G4:114-116; R82/phase_8_2_k1_review.md:3-11, :37-57; tag `hoso/p82-k1` (BTK:154); BTK:53.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]`.
- **Suy ra:** "pool rộng tự nó mang lại phần lớn mức tăng" là G4 nói (G4:115-116), trên dev 30, không qua luật; G5:70 ghi "chưa đo cùng 10 đoạn" cho pool 100 — K1 sau đó đã đo cùng 10 đoạn (pool vector, không phải native) và ra kém hơn.

#### T3-05 — Chuẩn hoá Unicode NFC câu hỏi
- **Vấn đề:** câu hỏi gõ từ một số máy ở dạng Unicode NFD (chữ có dấu tách thành chữ + dấu rời); trước 8.1 API / BM25 không chuẩn hoá (INV:90).
- **Ngày / Phase:** 24/10/2026 (8.1 G1.4); 28/10/2026 vào chatbot (merge `510e1a8`, cùng 10 đoạn).
- **Phương án + mốc:** mốc = câu gốc (NFC), runtime. Biến thể: NFD; NFD + NFC (bỏ dấu, kiểu dấu cũ — xem khối N2-13 = T3-06).
- **Cách đo:** 108 câu dev biến đổi bằng máy (MRR, `top10_gold_all`), Holm trên 6 (G1:85); bảng phụ 88 câu. Sau khi đưa vào chatbot: T1 = kết quả tìm 158 câu so từng byte.
- **Tiêu chí ghi trước:** G1.4 — "NFD tụt mà NFC phục hồi ⇒ đề xuất chuẩn hoá NFC câu hỏi ở 8.2" (G1:94-95 ghi "theo luật"); khi merge: T1 phải giống byte mốc.
- **Kết quả số:** NFD MRR −0,204 [−0,265; −0,144] (**kém hơn**), `top10_gold_all` −0,050 (không khác); NFD + NFC = giống hệt gốc (G1:89-90). Bảng phụ 88 câu: NFD −0,200 [−0,269; −0,132] (G1:165).
  Merge 28/10: T1 158 câu giống byte mốc (TH82:28); câu NFD đã lưu cho đúng 10 đoạn như câu NFC (BTK:81-82).
- **Tiền + tốc độ:** 0 USD (BTK:82); tốc độ chưa đo riêng (một bước chuẩn hoá chuỗi).
- **Quyết định + lý do:** **thêm NFC** — User chọn PA3 28/10 (đưa 10 đoạn + NFC vào chatbot, không chờ đọc cặp mù) (PS:146; BTK:145). Code `backend/retrieval/full_corpus.py:97-102`, gọi `:420` (BTK:42).
- **Giới hạn:** câu NFD là biến đổi máy, chưa biết tỉ lệ người dùng thật gửi NFD (G5:68); câu kín 0 câu ở dạng NFD ⇒ NFC chưa được câu kín thử (TH82:46); phép kiểm cuối B3 gộp ba thay đổi, không tách phần NFC (TH82:47).
- **Bằng chứng:** G1:85-97, :165; G5:42, :68; INV:90; TH82:28, :46-47; merge `510e1a8`; BTK:62, :81-82, :124.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]`.

#### N2-13 = T3-06 — Câu hỏi gõ không dấu (đo, và thử bỏ dấu cả kho cho BM25)
- **Vấn đề:** người dùng gõ không dấu thì khâu tìm còn dùng được không; bỏ dấu cả kho + câu hỏi cho BM25 có cứu không.
- **Ngày / Phase:** 24/10/2026 (8.1 G1.4 đo); 25/10/2026 (8.1 G4K nhánh E thử bỏ dấu cả kho + câu); User quyết 15:15 25/10/2026 "ngoài phạm vi".
- **Phương án + mốc:** mốc = câu có dấu, BM25 âm tiết có dấu. Đo: bỏ dấu; bỏ dấu + NFC; đổi kiểu dấu oa / oe / uy (G1:91-93). Thử sửa (E): bỏ dấu cả kho và câu hỏi (từ vựng 3.182) × 2 cách trộn (runtime / native pool 100) × 2 dạng câu (có dấu / không dấu do máy bỏ dấu) (G4K:94-107).
  Đề xuất chưa đo: chỉ dùng chỉ mục bỏ dấu khi câu hỏi không dấu (G4K:106-107).
- **Cách đo:** 108 câu dev (G1.4); 32 câu có đoạn đúng + 88 câu keyword (G4K). Câu không dấu là bản biến đổi máy (G4K:142). 0 USD.
- **Tiêu chí ghi trước:** G4K E, luật 2 phần — (1) câu **có dấu** không được kém; (2) câu **không dấu** quyết bằng Holm 2 (G4K:96-100); cộng luật chung của G4K như N2-11.
- **Kết quả số:**
  - Bỏ dấu (G1.4): MRR −0,543 [−0,616; −0,470], `top10_gold_all` 0,55 → 0,025 (**kém hơn**); NFC không cứu (G1:91-92). 88 câu: MRR 0,716 → 0,162 (G4K:57, :67); đủ đoạn đúng trong 5 đoạn 13 / 32 → **1 / 32** (G5:43; G4K:67, r0 0,406 ⇒ 0,031). Đổi kiểu dấu: không khác (G1:93).
  - Bỏ dấu cả kho (E): (1) có dấu: runtime **mất 2 câu** (0 / 30 / 2); native **mất 4 câu**, keyword −3,60 ⇒ **kém hơn**. (2) không dấu: runtime +0,031 (1 / 31 / 0, p 0,73); native +0,094 (3 / 29 / 0, p 0,18) ⇒ chưa rõ. Chỉ số phụ native, không dấu: sparse pool 0,250 → 0,812, MRR 0,209 → 0,414 (G4K:96-107).
- **Tiền + tốc độ:** 0 USD; BM25 native bỏ dấu 13,3–13,6 ms / câu (G4K:66, :70).
- **Quyết định + lý do:** bỏ hướng bỏ dấu cả kho (phạm luật (1)); **không xử lý — ngoài phạm vi**: "thiết kế giả định người dùng gõ có dấu; bỏ nghiên cứu ChatGPT về không dấu" (User 15:15 25/10, PS:162; EM:50); câu kín 8.1 thêm dấu cho mọi câu (PS:164). Hướng nếu mở lại: chỉ bật bản bỏ dấu khi câu hỏi không có dấu — **chưa đo** (G5:69; EM:124-125).
- **Giới hạn:** câu không dấu do máy tạo, không phải câu người dùng thật (G4K:142); 32 câu; nhánh vector e5 vẫn kém với câu không dấu (G4K:104-105); kho cũ, lúc đưa 5 đoạn.
- **Bằng chứng:** G1:85-97, :165-166; G4K:53-70, :94-107, :129, :135-137, :142; G5:43, :69; PS:26, :162; EM:20, :50, :88; BTK:61.
- **Nhãn:** `[kho, cấu hình cũ]` `[một lần chạy]`.
- **Suy ra:** "chỉ bật bỏ dấu khi câu không dấu tránh được thiệt cho câu có dấu" — G5:69 tự ghi *suy ra*, chưa đo. Hai tập câu cho số "không dấu" khác nhau (108 câu: MRR 0,73 → 0,19; 88 câu: 0,72 → 0,16) — cả hai đúng, khác tập.

#### T3-07 — Reranker MiniLM (tiếng Anh)
- **Vấn đề:** có giữ bước xếp hạng lại bằng cross-encoder MiniLM (model tiếng Anh, chạy CPU) không.
- **Ngày / Phase:** bản món ăn — Phase 5 12/08/2026 dựng (không đo chất lượng), Phase 4.5 (08/2026) đo 104 câu, 08c 30/08/2026 benchmark; toàn kho Phase 5 13–14/09/2026 (chỉ đo tốc độ); 8.1 G1.5 24/10/2026 (đếm cặp vượt 512 token); gỡ khỏi chatbot 26/10/2026 (BTK:125).
- **Phương án + mốc:** mốc = không rerank. Biến thể: MiniLM trên vector e5-small, trên vector HuyDang, trên trộn trọng số HuyDang (08c); `hybrid_rerank` so `hybrid_no_rerank` (4.5).
- **Cách đo:** bản món ăn 45 câu Golden V3 (08c: Recall@5, MRR@5, nDCG@5, bootstrap CI); bản món ăn 104 câu (4.5: MRR, nDCG, keyword coverage). Toàn kho: chỉ latency.
- **Tiêu chí ghi trước:** 08c có cột `Eligible` / `Clear Gain` (08c:81-85) — luật cụ thể trong spec 08c, **chưa kiểm**. Phase 5 món ăn: "không tuyên bố chất lượng tiếng Việt" (report Phase 5 :291-293).
- **Kết quả số:**
  - 08c: e5-small ΔnDCG@5 **−0,0703** [−0,1349; −0,0083]; HuyDang +0,0065 [−0,0891; +0,1057]; trộn trọng số HuyDang −0,0605 [−0,1496; +0,0243]; cả ba `Eligible False` (08c:83-85).
  - 4.5 (104 câu): `hybrid_rerank` MRR 0,7524 / nDCG 0,7772 / coverage 91,19 % so `hybrid_no_rerank` 0,8246 / 0,8327 / 97,12 % (4.5:28-31).
  - Toàn kho: MiniLM warm p95 1.007,95–1.331,49 ms (`reports/full_corpus_phase_5_retrieval_reranking_implementation_2026_09_13.md:84`); 8 / 8 tổ hợp chạy với `reranker=none` (:85).
  - 8.1 G1.5: 0 / 158 câu có cặp vượt 512 token (G1:101).
- **Tiền + tốc độ:** 0 USD; bản món ăn warm p50 / p95 ~231–248 / 481–539 ms (08c:83-85); toàn kho p95 1,0–1,3 s (INV:137).
- **Quyết định + lý do:** **không rerank** (`settings.yaml:44` `reranker: none` — BTK:63, :125). Nguồn quyết: phép thử khói Phase 6 + User "chọn A" (INV:137 dẫn file quyết định; file đó **chưa mở**). MiniLM gỡ khỏi chatbot 26/10 (BTK:125). Đính chính 24/10: "MiniLM làm điểm giảm" **chỉ đo trên bản món ăn** (BTK:110).
- **Giới hạn:** bằng chứng chất lượng chỉ trên bản món ăn (572 đoạn, kho khác); MiniLM không dành cho tiếng Việt; **chưa đo chất lượng trên toàn kho** — 8.1 thay bằng reranker đa ngôn ngữ (T3-08).
- **Bằng chứng:** 08c §4; 4.5 §2; Phase 5 toàn kho §5; G1:99-102; INV:137, :194, :239; BTK:63, :110, :114, :125.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[kho, cấu hình cũ]`.

#### T3-08 — Reranker chạy card đồ hoạ (bge-reranker-v2-m3, Vietnamese_Reranker)
- **Vấn đề:** reranker đa ngôn ngữ / tiếng Việt chạy máy (GPU GTX 1650) có đưa đoạn đúng lên đầu tốt hơn không, và chấm "đoạn trơn" hay "đoạn kèm cả mục" thì tốt hơn.
- **Ngày / Phase:** 25/10/2026, 8.1 G4-A (xếp lại top-10) và G4-B (chấm pool 100 rồi lấy top-10).
- **Phương án + mốc:** mốc = runtime (pool 30, không rerank) và mốc native pool 100 không rerank (cho G4-B). Đã thử: M1 `BAAI/bge-reranker-v2-m3` / M2 `AITeamVN/Vietnamese_Reranker` × đoạn trơn / đoạn kèm mục ở top-10 (4 biến thể); G4-B: M1 đoạn trơn trên pool 100 (chọn trước theo luật); "đoạn kèm mục" ở pool 100 dừng ở câu đầu (> 60 s).
- **Cách đo:** dev 30 câu có đoạn đúng (tập con seed 20261024), chỉ số chính `context5_gold_all` (đủ đoạn đúng trong 5 đoạn đưa model) **và** MRR@10 keyword, bootstrap 10.000, Holm trên 5 (G4:78-86); latency CPU / GPU. Không judge.
- **Tiêu chí ghi trước:** "tốt hơn = context5_gold_all VÀ MRR@10 đều CI > 0 sau Holm + đủ rào"; rào "0 câu mất đoạn đúng khỏi 5 đoạn đưa model", latency p95 GPU ≤ 3 s (ước; ghi số thật nếu vượt) (`R81/phase_8_1_g2_g4_plan.md:119-130`); G4-B thêm so với native pool 100 không rerank (:146-152).
  Ghi trước: G4-A không thể "tốt hơn" trên dev 30 vì chỉ có 3 câu cứu được (:129-130).
- **Kết quả số:**
  - G4-A: M1 trơn context5 +0,067, 3 / 26 / **1**, MRR@10 +0,105 [+0,024; +0,201] ⇒ **kém hơn** (mất 1); M1 kèm mục 2 / 25 / **3**; M2 trơn 2 / 25 / **3**; M2 kèm mục 2 / 25 / **3** ⇒ cả ba **kém hơn** (G4:82-85).
  - G4-B (M1 trơn pool 100): so runtime context5 +0,133 [+0,000; +0,300], 5 / 24 / **1**, MRR@10 +0,140 ⇒ **kém hơn** (mất 1); so native pool 100 không rerank: +0,033, 2 / 27 / 1 ⇒ **không khác** ⇒ "chưa thấy đóng góp của reranker ở đoạn đúng đưa model" (G4:111-112). Câu mất của G4-B là cùng câu M1 đẩy ra ở G4-A (tất định) (G4:117-118).
  - "Đoạn kèm mục" không giúp với M1 hay M2 (G4:92-93).
- **Tiền + tốc độ:** 0 USD (G4:156). GPU top-10 trơn p50 / p95 ~848 / 1.186 ms; kèm mục 2.731 / 4.758 ms; pool 100 trơn 8.835 / 12.875 ms (pilot); lượt G4-B dev 30 10.637 / 13.824 ms; pool 100 kèm mục 165.272 ms một câu (dừng); CPU top-10 ~4,9 / 6,6 s (G4:64-73, :119, :197).
- **Quyết định + lý do:** **giữ không rerank** (G5:32): mọi biến thể làm mất đoạn đúng của 1–3 câu khỏi 5 đoạn; lợi ở pool 100 đến từ pool rộng chứ không từ reranker (G4:114-116). A theo luật 8.1; 8.2 không thử lại.
- **Giới hạn:** dev 30, G4-A tối đa 3 câu cứu được (G4:160); không xác nhận test (không biến thể nào tốt hơn — G4:97, :122); đo lúc chatbot đưa **5 đoạn** (nay 10) — kết luận "mất khỏi 5 đoạn" **chưa đo lại ở 10 đoạn**; kho cũ, nhãn bản 1; GPU yếu (GTX 1650).
- **Bằng chứng:** G4 §4.0–4.5, §7 (G4:49-135, :165-202); plan `R81/phase_8_1_g2_g4_plan.md` (sha `a4adfc8eedd9`, G4:4); G5:32; BTK:64, :103-104.
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` `[một lần chạy]`.
- **Suy ra:** "ở 10 đoạn các reranker GPU có thể không còn phạm sàn" và "trên máy mạnh hơn tốc độ khác" — suy ra của agent gom thẻ, chưa đo.

#### T3-09 = S11 — Dùng `gpt-6-luna` xếp lại / chọn đoạn (gồm phần trả lời của K3b-m)
- **Vấn đề:** dùng chính model sinh (`gpt-6-luna`, gọi API) để xếp lại hoặc chọn 10 đoạn trong ứng viên, nhằm sửa chỗ nghẽn xếp hạng (T3-01: đoạn đúng có trong pool 30 nhưng xếp ngoài top-10) — đổi lại tốn tiền và chậm hơn.
- **Ngày / Phase:** 25/10/2026 (8.1 G4-A luna xếp lại top-10); 27/10/2026 (8.2 bước 2: K3, K3b-n, K3b-m).
- **Phương án + mốc:**
  - 8.1: mốc runtime top-10 (5 đoạn); biến thể luna sắp lại thứ tự **10** đoạn (đoạn trơn).
  - 8.2: mốc B1 `811d25d` (10 đoạn + NFC). K3 = luna xếp đủ **30** đoạn pool → top-10; K3b-n = luna chỉ trả 10 số, suy luận `none`; K3b-m = luna chỉ trả 10 số, suy luận mặc định.
  - Hướng chưa làm: "pool 100 + luna" (chỉ khi K3 thắng — R82/phase_8_2_k3_plan.md:147); K3c bản nhanh chịu chữ thừa (TH26:88-89).
- **Cách đo:** 8.1 dev 30 như T3-08. 8.2 tầng tìm: dev 40 có đoạn đúng, hai lượt L1 + L2 (thắng phải giữ cả hai lượt), test 15 một lượt. Tầng trả lời (chỉ K3b-m): 120 câu dev, số chính 88 câu (bỏ câu không tự nhiên + ngoài kho), judge **Claude** mù (tạm tới khi có mốc người), so theo cặp với B1 cùng lượt; test NOT RUN.
- **Tiêu chí ghi trước:**
  - 8.1: như T3-08 + luật đầu ra luna (đúng 10 id; lỗi = lỗi kỹ thuật, không thay bằng thứ tự gốc) (R81/phase_8_1_g2_g4_plan.md:121-127).
  - 8.2 K3 (dùng lại cho K3b): thắng ≥ 5 / 0 thua ổn định (Holm họ {K1, K3}); sàn 0 câu mất khỏi 10 đoạn; sàn **0 lỗi đầu ra luna**; tầng trả lời: câu ngoài kho bị trả lời 0; Đủ tụt ≤ 4 câu (dev) / 6 câu (test) (**luật T3 = A/A + 3 = 4** ở dev); Đúng tụt ≤ 4 (dev) / 5 (test); từ chối nhầm ≤ +1; lỗi trích dẫn ≤ +2 (R82/phase_8_2_k3_plan.md:80-92);
    `rerank_ms` p95 chỉ **theo dõi** mức 5 s (:94). K3b: nới sàn "hoán vị" thành mức tụt có trần (ghi trước, TH26:30). Luật (a) đợt: nhận khi chất lượng không tụt quá mức **và** rẻ / nhanh hơn rõ; luật (i) cho "chất lượng tăng nhưng tốn hơn" (TH26:17, :19).
- **Kết quả số:**
  - 8.1 luna top-10: context5 +0,100 [+0,000; +0,233], 3 / 27 / 0; MRR@10 **+0,172** [+0,092; +0,261], Holm < 0,001; 0 / 30 lỗi đầu ra ⇒ **chưa rõ** (trần 3 câu chặn chỉ số chính) (G4:86-90).
  - K3: phạm sàn — **1 lỗi đầu ra / 40 lần gọi** (thứ tự thiếu một đoạn) ⇒ **kém hơn**; theo dõi 39 câu: 9 thắng / 0 thua, MRR@10 0,442 → 0,706 (không dùng để kết luận) (R82/phase_8_2_k3_review.md:3, :85-88; TH26:49).
  - K3b-n: **kém hơn** — lỗi kỹ thuật (chữ thừa sau JSON dù structured output strict); pilot 9 / 10 như m (TH26:50).
  - K3b-m tầng tìm: dev 40 mốc 22 → **31** cả L1 và L2, 9 thắng / 0 thua, CI [+0,10; +0,35], Holm ⇒ 0 < 0,05; test 15: 7 → **10**, 0 mất (một lượt) ⇒ **tầng tìm tốt hơn (tạm)** (R82/phase_8_2_k3b_review.md:3, :63-71). Nhãn v2 (27/10 chiều): 24 → 33 (TH26:99; PS:66).
  - K3b-m tầng trả lời: Đủ thua **5** câu > ngưỡng 4 ⇒ **kém hơn theo luật T3** (số câu tụt điểm Đủ); chỉ báo: Đủ +0,216 [+0,023; +0,443], Đúng +0,250, Trúng ý +0,227; từ chối nhầm 7 → 2 / 88; câu ngoài kho bị trả lời 0 / 12; sàn ngoài kho / 500 đạt (R82/phase_8_2_k3b_m_answer_review.md:3, :51-57, :69-70; TH26:51).
    C phân loại 5 câu tụt: 1 tụt rõ, 3 tụt nhỏ, 1 nhiều khả năng do judge (:28-32).
- **Tiền + tốc độ:**
  - 8.1: 0,0088 USD / 30 câu; ~+3,5 s / câu (G4:141, :150); p95 cả luồng 5,2 s (G4:86).
  - K3: 0,0251 USD; rerank p50 5,6 / p95 8,6 s (TH26:49). K3b-n: ≈ 0,012 USD (cận tuyệt đối 0,048), rerank p95 2,1 s (TH26:50).
  - K3b-m: 0,0557 USD (tầng tìm) + 0,0749 (trả lời); cả câu p50 **6,5** / p95 **9,1** s (gọi đồng thời 4); bước chọn đoạn p50 4.620 / p95 6.892 ms (R26/b65_latency_dau_cuoi.md:66-69); ≈ **3,8×** USD / câu (0,00078 USD / câu nếu chạy thật) (TH26:51; K3b-m answer review:37-40, :74).
  - Tổng ba bản 27/10 ≈ 0,168 USD (BTK:90).
- **Quyết định + lý do:** 8.1 — giữ không rerank, ghi "tín hiệu" cho 8.2 (G4:133-135; G5:32). 8.2 — K3, K3b-n kém hơn (lỗi kỹ thuật); K3b-m kém hơn **theo luật T3** ⇒ **User 27/10 chọn (1) chốt đợt, chatbot không đổi, K3b-m gác làm hồ sơ** (TH26:33; PS:153; TH82:18).
  Lý do quyết lúc đó **chỉ là luật T3 (số câu tụt điểm Đủ)** (5 câu tụt > 4); tốc độ chỉ là mức theo dõi. Sàn tốc độ p50 ≤ 3 / p95 ≤ 5 s User chốt **sau** đó (28/10, PS:145) — không phải tiêu chí ghi trước của K3b-m.
  Câu hỏi "luật nhận cho biến thể đổi ngữ cảnh ở gần mọi câu" để cho lần sau, không áp ngược (TH26:79-80); hướng mở: chờ luật đó + yêu cầu thời gian chờ có số (TH26:88).
- **Giới hạn:** bộ nhỏ (40 / 88 câu); nhãn đoạn đúng của agent (bản 1 lúc chạy); judge Claude chưa có mốc người; một lượt sinh; tầng tìm test 15 chỉ một lượt; tầng trả lời test NOT RUN; latency đo khác phiên với mốc (TH26:51); luna không tất định, chưa có A/A cho luna xếp 30 đoạn (K3 review:95); luật T3 phạt nặng biến thể đổi ngữ cảnh ở gần mọi câu (TH26:79). Kho cũ (trước sửa đợt 1, 2), 10 đoạn.
- **Bằng chứng:** G4:86-96, :133-156; R82/phase_8_2_k3_plan.md (sha `0a6370204c7d`), phase_8_2_k3_review.md, phase_8_2_k3b_plan.md bản 2 (`57dad7150322`), phase_8_2_k3b_review.md, phase_8_2_k3b_m_answer_plan.md bản 3 (`2a3b22b38ab6`), phase_8_2_k3b_m_answer_review.md; tag `hoso/p82-k3`, `hoso/p82-k3b` (BTK:150-153); commit `a6f609c` (trong tag `hoso/p82-k3b`); TH26:43-56, :79-89; BTK:65, :85-90, :129; BSA:66, :105-106.
- **Nhãn:** `[kho, cấu hình cũ]` `[một lần chạy]` `[xác nhận nhóm kiểm]` — chỉ cho tầng tìm K3b-m (15 câu, một lượt); tầng trả lời test NOT RUN.

#### T3-10 — Lỗi đã biết trên kho hiện tại: câu nhiều nguồn / so sánh / bảng giá còn lớn không (Q3a)
- **Vấn đề:** trước lượt đo cuối, có nên "thử thêm có giới hạn" cho 3 lỗi đã biết không (plan đo cuối §4).
- **Ngày / Phase:** 01/11/2026 (Q3a, User chọn đo lại trước — 0 USD).
- **Phương án + mốc:** đo lại theo loại câu trên kho hiện tại (bộ "sau" đợt 2, 30/10) ⇒ chọn lỗi đáng thử / để lại.
- **Cách đo:** tầng tìm (MRR, keyword @10, đoạn đúng v5) + điểm judge đã chấm, theo loại câu; số chính 129 câu (R31/q3a_theo_loai_cau_implementation.md:31-46).
- **Tiêu chí ghi trước:** lỗi "còn lớn" khi (a) Đủ thấp hơn câu một dữ kiện ≥ 0,3 **và** (b) ≥ 5 câu Đủ ≤ 3 kèm thiếu bằng chứng; bảng giá: keyword lọt top-10 thấp hơn ≥ 15 điểm % hoặc Đủ thấp hơn ≥ 0,3 (R31/q3a_theo_loai_cau_implementation.md:50-54).
- **Kết quả số:** nhiều nguồn: Đủ **3,50** ↔ 4,92 (một dữ kiện), MRR 0,510, **8** câu Đủ ≤ 3 — cả 8 thiếu bằng chứng ở tầng tìm ⇒ **còn lớn**; so sánh: Đủ 4,35 (−0,57), chỉ 2 câu yếu ⇒ theo luật không phải hướng tìm; bảng giá: 8 câu, keyword lọt 80 % ↔ 90,3 %, Đủ 4,50 ↔ 4,53 ⇒ **không còn lớn** (R31/q3a_theo_loai_cau_implementation.md:33-54). MRR so sánh / nhiều nguồn gần như không đổi so với 24/10 (R31/q3a_theo_loai_cau_implementation.md:39).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** User để **câu nhiều nguồn sang Phase 9** (không mở thí nghiệm ở Phase 8); không "thử thêm" nào trước đo cuối (PS:138).
- **Giới hạn:** 18 câu nhiều nguồn, 20 câu so sánh, 8 câu bảng ⇒ cỡ mẫu nhỏ; đoạn đúng chỉ có cho một phần câu.
- **Bằng chứng:** R31/q3a_theo_loai_cau_implementation.md.
- **Nhãn:** `[một lần chạy]`.

### A6. Sinh câu trả lời, prompt, ngữ cảnh

#### S1 — Chọn model sinh câu trả lời
- **Vấn đề:** model nào viết câu trả lời từ các đoạn kho (chất lượng, tiền, độ ổn định). Phase 6 đã hứa so Qwen với GPT ở Phase 8.
- **Ngày / Phase:** 09/09/2026 chọn Qwen 3.5-9B (OpenRouter); 01/10/2026 đổi sang `gpt-5.4-nano`; 23/10/2026 đổi sang `gpt-6-luna`; 24/10/2026 User giữ luna, bỏ so model ở Phase 8.
- **Phương án + mốc:** (a) `qwen/qwen3.5-9b` qua OpenRouter (spec Phase 6:34, :106-122); (b) `gpt-5.4-nano` — "baseline ổn định trước khi đánh giá Qwen trong Phase 8" (amendment 10-01:11-13); (c) `gpt-6-luna` — lý do User: "rẻ hơn và mạnh hơn" nano / mini (amendment 10-23:27-30). Không có mốc chung.
- **Cách đo:** chỉ phép thử khói 5 lần gọi thật của Phase 6, mỗi model một lượt, khác thời điểm, **không chấm điểm** (INV:149). Qwen: thay trước khi chạy (INV:149).
- **Tiêu chí ghi trước:** tiêu chí đạt / không của phép thử khói (trích dẫn hợp lệ, từ chối đúng câu ngoài kho); **không có tiêu chí ghi trước để chọn model**.
- **Kết quả số:** nano 3 đạt / 2 không — 1 lỗi 502 do runner, 1 câu có điều kiện bị từ chối (`reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md:218-224`); luna 4 / 5 đạt, câu có điều kiện vẫn từ chối; latency 1.902–4.218 ms mỗi lần gọi (`reports/full_corpus_phase_6_gpt_6_luna_implementation_2026_10_23.md:149-155, :195-198`).
  So Qwen ↔ GPT cùng điều kiện: **NOT RUN** (G5:25).
- **Tiền + tốc độ:** giá luna 0,1 / 0,5 USD mỗi 1M token vào / ra (PS:168), giá đủ thêm ghi đệm (S14). Giá Qwen / nano trên toàn kho: chưa đo.
- **Quyết định + lý do:** User 23/10 đổi mọi model OpenAI sang luna; User 24/10 tối: giữ luna, không so model sinh ở Phase 8, "tối ưu sang model nhỏ để sau khi hệ thống ổn"; thay cam kết của amendment 10-01 §5 / 10-23 R6 (PS:181, :191).
- **Giới hạn:** **không có phép đo chất lượng nào so các model**; 5 câu khói khác thời điểm; luna là tên gọi trôi, không ghim bản cố định (amendment 10-23:49).
- **Bằng chứng:** các file trên; BSA:142-143; INV:149, :189.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]` `[một lần chạy]`.

#### S2 — Đưa model 5 hay 10 đoạn ngữ cảnh
- **Vấn đề:** từ chối nhầm 22 / 158 là chỗ mất điểm lớn nhất của mốc 7B; giới hạn 5 đoạn đặt từ 09/09 vì lo "thêm nguồn làm mơ hồ, đặc biệt với Qwen3.5 9B" — model đã bỏ (INV:143).
- **Ngày / Phase:** thăm dò 24/10 (B5); 8.1 G2.1a 25/10; vào chatbot 28/10 (8.2 B1, merge `510e1a8`); kiểm cuối câu kín 28/10 (B3, S15).
- **Phương án + mốc:** mốc = 5 đoạn (G2.0, sinh lại); thử 10 đoạn nguyên vẹn, cùng ngân sách 16.384 token. Ngân sách token: giữ, không thử biến thể ("không chạm": vào TB ≈ 1.660 token / câu, G5:54).
- **Cách đo:** thăm dò — sinh lại 22 câu đã từ chối nhầm, chưa chấm (`reports/phase_8_probe_context_top10_2026_10_24.md:1-12`); G2.1a — 120 câu dev (số chính 88 câu trong kho + 12 ngoài kho), Đủ / Đúng theo cặp, bootstrap, Holm trên 2; judge mù Claude; xác nhận trên 56 câu test (41 câu trong kho) (G2:50-52, :104-113).
- **Tiêu chí ghi trước:** plan `R81/phase_8_1_g2_g4_plan.md` §2.1 sha `a4adfc8eedd9`: tốt hơn trên dev có CI + Holm; rào 0 câu ngoài kho bị trả lời, Đúng cận trên CI ≥ 0, lỗi trích dẫn ≤ +2, USD / câu ≤ 2×; xác nhận test = cùng dấu + đủ rào (G2:65-66, :111).
- **Kết quả số:** thăm dò: 12 / 22 còn từ chối (10 hết), token vào ×1,73 (probe:64-68). Dev: Đủ **+0,261** [+0,080; +0,477], 9 / 77 / 2, p Holm 0,007; Đúng +0,273 [+0,091; +0,500]; từ chối nhầm 13 → 7; lỗi trích dẫn 4 → 4 (G2:62); nhóm đã đủ đoạn đúng 0 / 13 / 0 (không làm hỏng) (G2:66).
  Test: Đủ **+0,268** [+0,024; +0,585], 6 / 34 / 1 (G2:108) ⇒ **thắng (tốt hơn)**. Sau khi vào chatbot (B1, 176 câu): từ chối nhầm 22 / 158 ⇒ 12 / 158 (TH82:28); câu tự nhiên không lợi từ 10 đoạn (6 / 12 cả hai mức, TH26:41).
- **Tiền + tốc độ:** USD / câu 0,000204 (1,53×) dev, 0,000207 (1,49×) test, giá phẳng (G2:62, :108); B1 ≈ 0,00021 USD / câu (TH82:28). Latency qua API (22 câu tự viết, 27/10): 10 đoạn TB +130 ms so 5 đoạn, CI [−318; +565] (R26/b65_latency_dau_cuoi.md:52).
- **Quyết định + lý do:** User 28/10 chọn PA3 — đưa vào theo judge Claude, không chờ mốc người (TH82:19-20); A merge `510e1a8`. B0 01/11 ⇒ User giữ 10 (E7).
- **Giới hạn:** mốc người B0 (01/11) chỉ tham khảo (E7); judge có thể đoán bên qua trích dẫn `[6]`–`[10]` (TH82:47-48); số 8.1 và B3 đo trên kho trước sửa đợt 1 / 2; B1 / B3 gộp 3 thay đổi (10 đoạn, NFC, bộ kiểm trích dẫn v2) — không tách (TH82:47).
  Muốn về 5 phải sửa cả `settings.yaml:56` và chốt kiểm `core/settings_loader.py:75` (BSA:59).
- **Bằng chứng:** G2:58-68, :104-113; G5:23; TH82:28, :30; R82/phase_8_2_b1_merge_implementation.md; commit `510e1a8`.
- **Nhãn:** `[rà lại 8.1]` `[xác nhận nhóm kiểm]` `[kho, cấu hình cũ]`.
- **Suy ra:** "lợi nằm nhiều ở câu nhiều nguồn / so sánh" — BSA:68 và thăm dò nói (câu so sánh 5 / 8 hết từ chối, probe:71); G2 chỉ báo theo nhóm, không theo loại câu (G2:198 "chưa báo").

#### S3 — Thứ tự đoạn trong ngữ cảnh
- **Vấn đề:** giữ thứ tự theo thứ hạng tìm kiếm (RRF) hay gom các đoạn cùng tài liệu đứng cạnh nhau ("lost in the middle").
- **Ngày / Phase:** 25/10/2026, 8.1 G2.1b.
- **Phương án + mốc:** mốc G2.0 (5 đoạn, thứ tự RRF); biến thể gom theo tài liệu, giữ nguyên tập 5 đoạn (120 / 120), đổi thứ tự ở 47 / 120 câu (G2:45).
- **Cách đo:** như S2 (88 câu dev, Holm trên 2); không xác nhận test vì không thắng.
- **Tiêu chí ghi trước:** như S2 (plan §2.1).
- **Kết quả số:** Đủ −0,023 [−0,068; +0,023], 1 / 84 / 3, p Holm 0,432; lỗi trích dẫn 4 → 6 (6 mới / 4 hết) ⇒ **không khác** (G2:63, :69-70).
- **Tiền + tốc độ:** 0,000134 USD / câu (1,00×) (G2:63); latency chưa đo.
- **Quyết định + lý do:** giữ thứ tự RRF (G5:53); A / G5 chốt 25/10.
- **Giới hạn:** chỉ đo ở 5 đoạn.
- **Bằng chứng:** G2:63, :69-70; G5:53; BSA:67, :128.
- **Nhãn:** `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]`.
- **Suy ra:** "chưa đo lại ở 10 đoạn" — suy ra vì không thấy lượt nào khác trong các nguồn đã đọc.

#### S4 — Thiếu một vế: từ chối cả câu hay trả lời phần có căn cứ
- **Vấn đề:** prompt bắt từ chối cả câu khi bằng chứng không đủ (tất-cả-hoặc-không); spec chung cho phép "trả phần có căn cứ" (lệch tài liệu, BSA:189-190).
- **Ngày / Phase:** 25/10/2026 (8.1 G2.2 P1); 26/10/2026 (8.2 R2, chữ siết hơn).
- **Phương án + mốc:** mốc = từ chối cả câu (`backend/llm/full_corpus_prompt.py:14`); P1 "trả lời phần có căn cứ, nói rõ phần thiếu" (5 đoạn); R2 chữ siết hơn (10 đoạn, mốc B1).
- **Cách đo:** P1 — 88 câu dev + 12 ngoài kho, judge mù, nhãn loại câu trả lời (đủ / một phần / từ chối) do sub-agent gắn (G2:74-85); R2 — bước 1 chỉ chạy 12 câu ngoài kho (R82/phase_8_2_r2_review.md:59, :66).
- **Tiêu chí ghi trước:** sàn "0 câu ngoài kho bị trả lời" (P1: plan §2.1; R2: plan §2 + §3 bước 1, R2 review:69).
- **Kết quả số:** P1 — từ chối nhầm 13 → 1, 17 câu trả lời một phần, Đủ +0,114 [−0,023; +0,250], nhưng **2 câu ngoài kho bị trả lời** ⇒ **kém hơn** (G2:77, :80-82); R2 — **1 / 12** câu ngoài kho bị trả lời ⇒ **kém hơn**, dừng ở bước 1 (R2 review:59, :69; TH26:53).
- **Tiền + tốc độ:** P1 token ra +25 % (98,8 so 78,8 / câu) (G2:81-82); R2 0,0027 USD (R2 review:64).
- **Quyết định + lý do:** giữ từ chối cả câu (G5:24); A gác hướng R2 sau khi phạm sàn (26/10, TH26:25); hướng đã gác "chỉ mở lại khi có ý mới đã kiểm trước" (BSA:175).
- **Giới hạn:** R2 kết luận từ một lượt, một câu (R2 review:81); nhãn loại câu trả lời không có người kiểm (G2:203). G1.6: 22 / 22 câu từ chối nhầm 7B thiếu ≥ 1 đoạn đúng ⇒ gốc ở khâu tìm, không ở prompt (G5:24).
- **Bằng chứng:** G2:74-85; G5:24; R82/phase_8_2_r2_review.md; tag `hoso/p82-r2` `aec9ab8` (TH26:53; nhánh đã đổi thành tag — TH27:144).
- **Nhãn:** `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]`.

#### S5 — Prompt: thêm 2 luật cũ của spec Phase 6 (P2)
- **Vấn đề:** prompt đang chạy viết cho Qwen (01/10), thiếu 2 luật của spec Phase 6 §10 ("không dùng tiêu đề làm bằng chứng", luật đoạn / danh sách) (INV:43, :147).
- **Ngày / Phase:** 25/10/2026, 8.1 G2.2.
- **Phương án + mốc:** mốc G2.0 (prompt hiện tại); P2 = thêm 2 luật.
- **Cách đo:** như S2 (88 câu dev, Holm trên 2 cùng P1).
- **Tiêu chí ghi trước:** như S2 (plan §2.1).
- **Kết quả số:** Đủ +0,000 [−0,068; +0,068], 2 / 84 / 2, p Holm 1,0; Đúng +0,023 [−0,045; +0,114]; lỗi trích dẫn 4 → 1 (phụ, n nhỏ); token ra −12 % ⇒ **không khác** (G2:78, :83).
- **Tiền + tốc độ:** 0,0148313 USD lượt 110 câu (G2:172); latency chưa đo.
- **Quyết định + lý do:** giữ prompt (G5:26).
- **Giới hạn:** lỗi trích dẫn 4 → 1 là tín hiệu phụ chưa qua thước.
- **Bằng chứng:** G2:78, :83; G5:26.
- **Nhãn:** `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]`.
- **Suy ra:** tín hiệu lỗi trích dẫn hết ý nghĩa sau khi sửa bộ kiểm (S8) — suy ra (bộ kiểm cũ đếm `[Nguồn n]` là lỗi, R82/c65_citation_138_check.md:7-10), nguồn không nói.

#### S6 — Prompt "nêu đủ chi tiết" cho câu trả lời quá gọn (R3)
- **Vấn đề:** 9 / 88 câu mất điểm Đủ vì bỏ chi tiết có ngay trong đoạn đã trích (phân loại trên mốc 10 đoạn, R82/phase_8_2_r3_plan.md:23-24).
- **Ngày / Phase:** 26/10/2026, 8.2 bước 2.
- **Phương án + mốc:** mốc B1 (10 đoạn); R3 = câu prompt "nêu đủ chi tiết", chèn trước luật từ chối (R3 plan:43).
- **Cách đo:** dự kiến 88 câu dev chính + test 41 câu, Holm họ {R2, R3}.
- **Tiêu chí ghi trước:** CI 95 % > 0 và Holm họ 2 cố định; mức tụt Đúng ≤ 4 / 5, Đủ test ≤ 6 (R3 plan:63-66).
- **Kết quả số:** **NOT RUN** — trên mốc B1 chỉ 6 / 9 câu còn chỗ tăng (3 câu đã 5 điểm); cần ≥ 5 thắng / 0 thua, không thể đạt khi trần 6–7 (R82/phase_8_2_r3_plan_review.md:26-37; TH26:25, :54).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** A 26/10 ghi NOT RUN (trần 6 câu) (TH26:25). Còn mở: "cần thêm câu tự nhiên để đo" (BSA:174).
- **Giới hạn:** hướng chưa được thử, không phải đã thua.
- **Bằng chứng:** R82/phase_8_2_r3_plan.md, R82/phase_8_2_r3_plan_review.md; BSA:63, :116.
- **Nhãn:** `[kho, cấu hình cũ]`.

#### S7 — Mức suy luận (reasoning effort) của model sinh
- **Vấn đề:** chatbot không gửi tham số suy luận (khoá từ amendment 10-01); suy luận ít có thể rẻ / nhanh hơn, nhiều có thể đúng hơn.
- **Ngày / Phase:** 25/10/2026 (8.1 G2.4, 5 đoạn); 27/10/2026 (8.2 R1, `none` ở 10 đoạn).
- **Phương án + mốc:** mốc = mặc định (không gửi); G2.4 thử `none`, `low`, `high`; R1 thử lại `none` trên mốc B1.
- **Cách đo:** G2.4 — 120 câu dev, Holm trên 3, chấm mù cùng lượt với mốc; nhiễu chỉ chấm: Đủ đổi 2 / 88 (G2:115-120). R1 — pilot chọn có chủ đích, dừng khi phạm sàn.
- **Tiêu chí ghi trước:** G2.4 như S2 (rào lỗi trích dẫn ≤ +2). R1: sàn "2 câu lẽ ra từ chối vẫn từ chối"; nhận khi USD ≤ 0,95× **hoặc** token ra ≤ 0,9× (User 26/10, TH26:24).
- **Kết quả số:** `none` Đủ **+0,136** [+0,034; +0,261] p Holm 0,031 nhưng lỗi trích dẫn 4 → **8** ⇒ **kém hơn**; `low` lỗi trích dẫn 4 → 9 ⇒ **kém hơn**; `high` +0,023, không khác, token ra +36 % (G2:125-135).
  R1: một câu lẽ ra phải từ chối bị "trả lời vòng" ⇒ phạm sàn ⇒ **kém hơn**, dừng ở pilot (R82/phase_8_2_r1_review.md:3, :48, :65).
- **Tiền + tốc độ:** USD / câu: `none` / `low` 0,000121 (0,91×), `high` 0,000148 (1,11×) (G2:125-127); R1 token ra ~0,72×, USD ~0,95× (TH26:55), tiền lượt 0,0049030 USD (R1 review:52); p50 trong phạm vi 2.356 / 2.250 ms (mốc / R1, pilot) (R1 review:54).
- **Quyết định + lý do:** giữ mặc định, không gửi (G5:27); A 27/10 gác R1 (TH26:29).
- **Giới hạn:** lỗi trích dẫn ở G2.4 đếm theo bộ kiểm cũ (chưa nhận `[Nguồn n]`) (BSA:131); R1 chỉ pilot, không có Đủ / test (NOT RUN, R1 review:65-66). Mức mặc định của luna: INV:150 ghi "chưa rõ", plan R1 ghi `medium` — chưa kiểm.
- **Bằng chứng:** G2:115-135; G5:27; R82/phase_8_2_r1_review.md; tag `hoso/p82-r1` `63a472f`; code `generator_openai_full_corpus.py:98-99, :120` (BSA:62).
- **Nhãn:** `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]`.
- **Suy ra:** lý do "kém hơn" của `none` / `low` ở G2.4 dựa vào lỗi trích dẫn đếm bằng bộ kiểm cũ; đếm bằng bộ kiểm mới số lỗi có thể khác — chưa có nguồn đếm lại. `none` được thử hai lần (5 đoạn, 10 đoạn), cả hai kém hơn.

#### S8 — Bộ kiểm trích dẫn `[n]`: chính sách lỗi và định dạng nhận
- **Vấn đề:** câu trả lời không có `[n]` hợp lệ ⇒ người dùng nhận lỗi 500 (2,3–3,4 % câu ở 7B); 4 câu lỗi vẫn được chấm 5 / 4,75 / 5 (INV:148).
- **Ngày / Phase:** 25/10/2026 (8.1 G2.3; rà code gói 1a); 27/10 (C65); 30/10 (C89 đếm lại); E2 của 8.2 NOT RUN.
- **Phương án + mốc:** mốc = lỗi ⇒ 500, không sửa, không thử lại; (a) "ngữ cảnh chỉ có một nguồn thì gán nguồn đó" (A chọn thử); (b) nhận cả `[Nguồn n]` và đổi về `[n]`; (c) E2 "sửa thiếu `[n]`" (TH26:56).
- **Cách đo:** phát lại bộ kiểm trên câu trả lời đã lưu, 0 USD — 7B Run 1 / 2 (176 câu mỗi lượt) + 5 lượt G2 (G2:89-94); (b) phát lại trên 1.600 câu đã sinh + 2 câu API thật.
- **Tiêu chí ghi trước:** (a) số câu đổi (plan G2 §2); (b) "0 câu đạt bị đổi" (rà code gói 1a); không thấy ghi riêng hơn trong nguồn đã đọc.
- **Kết quả số:** (a) 0 câu đổi ⇒ **không khác** — mọi lỗi là "không có `[n]` nào" khi có 5 (10) nguồn, chính sách không bao giờ áp (G2:96-101; G5:44); (b) lỗi 69 → 14, 0 câu đạt bị đổi ⇒ **PASS, giữ** (THRC:60);
  đưa 12 / 176 câu lỗi của B1 qua bộ kiểm mới: cả 12 qua (R82/c65_citation_138_check.md:8-9); đếm lại trên mọi lượt đã lưu: bản đang chạy **0 / 489** lần sinh, bản 5 đoạn cũ 2 / 528 (BSA:86-87; TH27:142); (c) **NOT RUN** — mốc bộ kiểm v2 đã 0 lỗi (TH26:56).
- **Tiền + tốc độ:** 0 USD; bộ kiểm ~0 ms (R26/c58_latency_theo_khau.md:8).
- **Quyết định + lý do:** giữ "lỗi ⇒ 500" (G5:44); thêm nhận `[Nguồn n]` từ 25/10 (commit `9e6d371`, BSA:121-122, :183); lỗi còn lại chỉ biết khi câu đã viết xong ⇒ căn cứ cho streaming "kiểm cuối" (BSA:86-87).
- **Giới hạn:** số "lỗi trích dẫn" trước 25/10 đếm theo bộ kiểm cũ (BSA:122); "bỏ 4 câu 500" ở B3 vẫn tốt hơn (S15).
- **Bằng chứng:** như trên; code `backend/llm/citations.py:11-16`, `backend/api/routes/chat.py:177-188` (BSA:156).
- **Nhãn:** `[rà lại 8.1]` `[xác nhận nhóm kiểm]`.

#### S9 — Luật kiểm bằng code sau khi sinh để chặn "trả lời vòng"
- **Vấn đề:** sau R1, một dạng lỗi là câu trả lời có `[n]` cùng chủ đề nhưng không trả lời đúng ý; một luật bằng code có chặn được không.
- **Ngày / Phase:** 27/10/2026, 8.2 (C51, đo khả thi).
- **Phương án + mốc:** không có luật (mốc) ↔ luật kiểm sau sinh (đổi câu bị cờ thành câu từ chối).
- **Cách đo:** chạy luật trên câu trả lời đã lưu; đọc tay mẫu 10 cờ; 0 USD.
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước (việc đo khả thi).
- **Kết quả số:** luật bắt được 2 câu lỗi đã biết sau khi chỉnh trên chính 2 câu đó; 0 cờ ở chatbot hiện tại; trong mẫu, 7 / 10 cờ là câu có ích, chỉ 1–3 / 10 chặn đúng ⇒ **bỏ** (TH26:62; R26/c51_kiem_sau_sinh_kha_thi.md:72).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** A 27/10 gác cùng R1 (TH26:29); BSA:65, :109-110.
- **Giới hạn:** luật chỉnh trên đúng 2 câu dùng để kiểm (quá khớp); mẫu 10 cờ, một người đọc.
- **Bằng chứng:** R26/c51_kiem_sau_sinh_kha_thi.md; TH26:62.
- **Nhãn:** `[một lần chạy]` `[kho, cấu hình cũ]`.

#### S10 — Rào chặn sai con số + thước "số có trong nguồn"
- **Vấn đề:** lỗi "nói chắc sai" xếp nặng hơn từ chối nhầm (PS:32); câu trả lời có sai số (giá, giờ, năm) không, có cần rào chặn.
- **Ngày / Phase:** 26/10/2026 (R4 làm thước); 27/10/2026 (C48 đo hiện trạng).
- **Phương án + mốc:** không rào (hiện tại) ↔ thêm rào chặn; thước R4 "số trong câu trả lời có trong nguồn được trích".
- **Cách đo:** R4 — kiểm thước trên mẫu ngoài; C48 — chạy thước trên mốc B1, dev 68 câu có số + đọc tay; 0 USD.
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước cho C48 (đo hiện trạng); R4 có plan / review (R82/phase_8_2_r4_implementation.md, chưa mở mục tiêu chí).
- **Kết quả số:** R4 "ngoài mẫu đúng 0 / 5" ⇒ **chỉ dùng làm danh sách đọc lại** (TH26:52; chép nguyên chữ, chưa kiểm nghĩa trong report R4); C48: **0 / 68** câu có số bị thấy sai (4 cờ đều là phép tính đúng) (R26/c48_so_trong_cau_tra_loi.md:55; TH26:62).
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** chưa cần rào chặn lúc này (BSA:107); sai về chữ (tên, sự kiện) chưa có cách đo rẻ (BSA:174).
- **Giới hạn:** đo ở cấu hình B1 trên kho trước sửa; chỉ bắt được sai số mà máy thấy.
- **Bằng chứng:** như trên; BSA:64, :107-108.
- **Nhãn:** `[một lần chạy]` `[kho, cấu hình cũ]`.

#### S17 = E11 — Câu hỏi theo ngày tương đối: sửa prompt ở Phase 8 hay để Phase 9
- **Vấn đề:** prompt không có ngày hôm nay (`full_corpus_prompt.py:7-16`, BSA:71); câu kiểu "tối nay", "tháng sau" có thể làm model tự đoán ngày rồi nói chắc sai.
- **Ngày / Phase:** 30/10/2026 (C93, plan B96), phần tồn trước Phase 9.
- **Phương án + mốc:** mốc = prompt hiện tại (không đưa ngày). Hướng sửa đã nêu: P1 / P2 (đưa ngày giờ vào tin nhắn), P3 ("không giả định ngày; nêu lịch kèm điều kiện hoặc hỏi lại") — **NOT RUN** (luật ghi trước: không lỗi ⇒ không sửa) (R27/ngay_hien_tai_implementation.md:54-55).
- **Cách đo:** 15 câu tự viết (12 câu quyết, 1 ngoài kho, đối chứng) + 11 câu bộ an toàn; 2 judge Claude không biết ngày chạy, kiểm người chấm bằng 6 phiếu khoá nhãn (6 / 6 cả hai) (:10, :27).
- **Tiêu chí ghi trước** (plan §5): chỉ số quyết `n_L1L2` (đoán ngày rồi nói sai) trên 12 câu; sàn câu ngoài kho bị trả lời = 0; không lỗi đoán ngày ⇒ không sửa prompt; từ chối = chỉ số theo dõi (:14, :32-41).
- **Kết quả số:** `n_L1L2` **0 / 12**, 0 / 11 câu an toàn; câu ngoài kho từ chối đúng; bất đồng judge 0 / 26; **từ chối câu có trong kho 6 / 14**, 4 trong đó lịch đúng nằm ngay trong ngữ cảnh (:10-12, :34-40, :48). Cỡ mẫu chỉ nói được tần suất < ~25 % (luật ba, n = 12) (:43-44).
- **Tiền + tốc độ:** 0,0037029 USD (trần 0,01) (:25); tốc độ chưa đo.
- **Quyết định + lý do:** User 30/10 14:44 — không sửa prompt ở Phase 8 (luật ghi trước); Phase 9 thêm công cụ "hôm nay là ngày nào", bộ câu này làm mốc; từ chối nhầm loại câu này để Phase 9 (BSA:83-85; BDG:91, :111).
- **Giới hạn:** 15 câu tự viết; một lượt sinh, không đo nhiễu; judge Claude; ngày chạy là thứ Sáu nên vài câu "có" đúng ngẫu nhiên (:59-62). Báo cáo User ghi gộp "15 câu: 0 câu đoán ngày rồi nói sai" — số quyết thật là trên 12 câu.
- **Bằng chứng:** R27/ngay_hien_tai_implementation.md:7-62; R27/ngay_hien_tai_review.md; BDG:22, :91, :110-111.
- **Nhãn:** `[một lần chạy]`.
- **Suy ra:** lý do model từ chối (coi câu "tối nay" là thiếu bằng chứng) là *suy ra* của chính nguồn (:52-53), chưa chứng minh.

### A7. API, tốc độ, tiền

#### S12 — Thiết kế API / giao diện / cách gọi model
- **Vấn đề:** hình dạng API, mã lỗi, có thử lại / đổi model dự phòng không, gọi model bằng gì, ghi log gì.
- **Ngày / Phase:** spec Phase 6 14/09; amendment 30/09, 01/10, 23/10; sửa mã lỗi 25/10 (rà code gói 1b); log `chat_metrics` 27/10.
- **Phương án + mốc:** `POST /api/chat` `{query}` 1–500 ký tự ⇒ `{answer, sources}`; mã 422 / 409 / 503 / 500 (502 khi model lỗi) (BSA:31-36; INV:153); không thử lại, không model dự phòng, timeout 45 s, ra tối đa 2.048 token (amendment 10-01:25-43);
  cách gọi: gọi thẳng `AsyncOpenAI` (bản Qwen 30/09) → OpenAI Agents SDK một lượt, không tool (01/10) (BSA:191-192).
- **Cách đo:** không có so sánh phương án; kiểm bằng test + chạy thật (rà code: 1 module nạp hai lần làm lỗi Qdrant ra 500 thay 503, kho đổi ra 503 thay 409) (BSA:119-120).
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước để chọn thiết kế.
- **Kết quả số:** nhánh "không có nguồn thì từ chối, không gọi model" xảy ra 0 / 352; câu Golden dài nhất 129 ký tự (INV:153); sửa mã lỗi **PASS** (BSA:119-120); log `chat_metrics`: một dòng mỗi lần hỏi, không nội dung, không USD, merge `5100b90` (TH26:100; BSA:157).
- **Tiền + tốc độ:** HTTP ~2 ms (R26/c58_latency_theo_khau.md:8); log ≈ 0,0003 USD (TH26:100).
- **Quyết định + lý do:** INV:151, :153 xếp "mặc định không lý do", tác động thấp ⇒ 8.1 NOT RUN (G5:61); User duyệt log 27/10 13:05 (TH26:100).
- **Giới hạn:** con số 500 ký tự, timeout 45 s, structured output một trường — chưa đo ảnh hưởng (INV:151).
- **Bằng chứng:** như trên.
- **Nhãn:** `[chưa kiểm lại Phase 0–7]`.

#### S13 — Tốc độ: đo ở đâu, khâu nào chậm, có đạt yêu cầu
- **Vấn đề:** User chốt 28/10 p50 ≤ 3 s, p95 ≤ 5 s cả câu (PS:32, :145); bản đang chạy đạt chưa, chậm ở khâu nào.
- **Ngày / Phase:** 27/10 (B65 qua API, C58 theo khâu); 28/10 (bộ "trước" / "sau" sửa kho đợt 1); 30/10 (sau đợt 2).
- **Phương án + mốc:** không phải so phương án sinh — so **cách đo** (qua API ↔ trong harness) và **cấu hình** (5 ↔ 10 đoạn).
- **Cách đo:** B65 — 22 câu tự viết qua API thật, tuần tự và 4 câu đồng thời, một lượt mỗi ô (R26/b65_latency_dau_cuoi.md:37, :87); C58 — tách thời gian theo khâu, 44 câu; harness — 176 câu Golden tuần tự, không HTTP (R27/sua_kho_dot2_implementation.md:65).
- **Tiêu chí ghi trước:** B65 **không có plan duyệt** (b65:4) — đây là đo hiện trạng; mức theo dõi 5 s (spec 8.2 §10.2) rồi sàn User 28/10.
- **Kết quả số:** B65 5 đoạn tuần tự p50 3.304 / p95 5.700 ms; 10 đoạn tuần tự p50 3.068 / p95 6.039 ms; đồng thời 4: 3.568 / 6.249 và 3.410 / 6.432 ms (b65:46-49);
  C58: gọi model ≈ 97–98 %, ≈ 1,16 s + 11,5 ms × token ra (r 0,97); tìm ~40 ms, dựng ngữ cảnh ~2 ms (R26/c58_latency_theo_khau.md:8, :39);
  harness 176 câu: 2,21 / 4,88 s (trước đợt 1) ⇒ 2,78 / **9,76** s (sau đợt 1, "không đại diện") ⇒ **2,19 / 4,90 s** (sau đợt 2) (R27/sua_kho_b9_implementation.md:14, :64; R27/sua_kho_dot2_implementation.md:65);
  câu trả lời dài (8 câu tự viết, 28/10): đợi đủ câu p50 4,6 / p95 7,6 s (R27/streaming_ttft_implementation.md:77, :91).
- **Tiền + tốc độ:** B65 ≈ 0,0155 USD (b65:81); C58 0,0075 USD (TH26:98).
- **Quyết định + lý do:** thước harness: Golden "đạt sát"; câu dài "chưa đạt" (BSA:21-22). **Thước qua API (10 đoạn): p95 6,0 s tuần tự / 6,4 s đồng thời 4 — chưa đạt p95 ≤ 5 s.** Hai thước khác nhau (bộ câu, có / không HTTP, kho trước / sau sửa) nên cần ghi cả hai;
  C58 cho thấy p50 qua API ≈ harness, p95 chưa so (R26/c58_latency_theo_khau.md:10), và muốn nhanh hơn phải làm model viết ít hơn hoặc hiện chữ dần (c58:11); streaming là tính năng User chọn ưu tiên 27/10 (PS:151). User 31/10: khi streaming chạy, sàn áp cho "tới chữ đầu tiên trên trình duyệt" (PS:32); User 01/11 thêm mục tiêu báo cáo p50 ≤ 1,5 / p95 ≤ 3 s (không chặn — spec streaming bản 5, commit `74a6082`).
- **Giới hạn:** p95 trên 22 câu ≈ câu chậm thứ hai (b65:87); p95 harness dao động 4,9 ↔ 9,8 s giữa các lượt cùng code (khác kho; nguồn cho là do mạng / nhà cung cấp, b9:14-16); latency qua API của 10 đoạn trên Golden sau sửa kho: **chưa đo**.
- **Bằng chứng:** như trên.
- **Nhãn:** `[một lần chạy]` `[kho, cấu hình cũ]`.
- **Suy ra:** "p95 dao động do mạng / nhà cung cấp" — nguồn ghi "không đại diện (phía mạng / provider)" (TH27:86); nguyên nhân chưa được chứng minh.

#### S14 — Tiền / câu và lỗi công cụ đo `cost_usd`
- **Vấn đề:** trần User ≤ 0,0005 USD / câu (PS:145); số USD trong mọi report tính theo giá phẳng — có đúng tiền thật không.
- **Ngày / Phase:** 24/10 (giá phẳng 0,1 / 0,5 USD / 1M, PS:168); 30/10 15:07 (User dán bảng giá đủ; B95 kiểm log).
- **Phương án + mốc:** công thức giá phẳng (đang dùng ở `backend/evaluation/full_corpus_eval.py:167`, BSA:160) ↔ giá đủ (vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M).
- **Cách đo:** B95 đọc `cache_write_tokens` / `cached_tokens` trong log; 0,0008 USD (TH27:148).
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước (kiểm sổ sách).
- **Kết quả số:** mỗi câu `cache_write_tokens` ≈ toàn bộ phần vào, `cached_tokens` = 0 ⇒ `cost_usd` **ghi thiếu ≈ 20 %**: ~0,00021 ⇒ **~0,00025 USD / câu**, vẫn dưới trần (PS:141; BSA:19, :88-89).
  Tham chiếu: 7B 5 đoạn ≈ 0,00014 USD / câu (giá phẳng, `bao_cao_he_thong/01_LUONG_HOAT_DONG_HE_THONG.md:86`); sau đợt 2: 0,0002086 USD / câu giá phẳng (R27/sua_kho_dot2_implementation.md:64).
- **Tiền + tốc độ:** như trên.
- **Quyết định + lý do:** sửa công thức + ghi `cache_write_tokens` ở bước đóng gói Phase 1–8 (BSA:171; PS:141).
- **Giới hạn:** **mọi số USD cũ trong báo cáo này đếm theo giá phẳng** (BSA:89); chưa đối chiếu hoá đơn thật ("chờ User xem billing", TH27:141).
- **Bằng chứng:** như trên.
- **Nhãn:** `[một lần chạy]`.

#### S16 — Đo trước streaming: hiện chữ ngay hay chỉ hiện câu đã có `[n]` (C73)
- **Vấn đề:** streaming có rút thời gian chờ đáng kể không, và kiểu hiện chữ nào (hiện ngay ↔ chỉ hiện câu đã có nguồn).
- **Ngày / Phase:** 28/10/2026 (C70 / C73), trước khi viết spec streaming.
- **Phương án + mốc:** N10 (không stream, như hôm nay) ↔ S10 (stream, hiện chữ ngay) ↔ D10; chỉ số phụ "chỉ câu có `[n]`" (kiểu B, ước).
- **Cách đo:** 10 câu tự viết (7 câu trong kho có trả lời hợp lệ cho chỉ số quyết), trong script, không qua trình duyệt; bootstrap CI trên câu (R27/streaming_ttft_implementation.md:20, :59).
- **Tiêu chí ghi trước:** plan sha `9683641b6c38`: `gain_visible` ≥ 1.500 ms và CI > 0 ⇒ "rõ"; 500–1.500 ⇒ "vừa"; < 500 ⇒ "nhỏ" (R27/streaming_ttft_plan.md:174-178).
- **Kết quả số:** `gain_visible` trung vị **1.921,3 ms** [1.608,2; 4.309,9] ⇒ **rõ**; `gain_cited` 1.014,3 ms [144,2; 3.040,8] ⇒ **vừa**, chưa chắc (impl:61-64); tới chữ đầu p50 2.441,8 / p95 4.802,8 ms; đợi đủ câu p50 4.621,9 / p95 7.649,2 ms; stream không làm xong chậm hơn (−180,5 ms, CI [−956,9; +1.606,1]) (:75-77).
- **Tiền + tốc độ:** 0,010291 USD (vượt ước +45 % cả lượt, +70 % ở pilot) (:100-104); ≈ 0,00029 USD / lần gọi (:84, :95).
- **Quyết định + lý do:** đủ để bàn spec streaming; User 31/10 chốt hiện chữ ngay + tiến độ, kiểm trích dẫn ở cuối (PS:138).
- **Giới hạn:** 7 câu, p95 ≈ giá trị lớn nhất; kiểu B chỉ ước (không tách câu thật) (:108-110). Số lần gọi ghi lệch trong cùng file (30 / 31 / 35) — có lẽ do lần khởi động + pilot, chưa kiểm.
- **Bằng chứng:** R27/streaming_ttft_implementation.md; tag `hoso/c70-ttft` `1f70095`.
- **Nhãn:** `[một lần chạy]`.

#### S18 — Streaming: hiện chữ ngay (PA1) hay chỉ hiện tiến độ rồi cả câu (PA3); sàn tốc độ đo ở đâu
- **Vấn đề:** chờ cả câu vượt yêu cầu tốc độ ở câu trả lời dài (S13, S16); chọn cách hiện chữ và thước tốc độ cho bản có streaming.
- **Ngày / Phase:** 31/10 – 01/11/2026 (đóng gói Phase 1–8).
- **Phương án + mốc:** mốc = chờ đủ câu (route JSON). PA1 = chữ hiện ngay khi model viết + tiến độ thật, kiểm trích dẫn lúc cuối; PA3 = chỉ hiện tiến độ, câu trả lời hiện một lần (nháp v3 private); PA0 / PA2 bỏ ở nháp.
- **Cách đo:** S4 — trình duyệt thật (Playwright, Chromium), server thật, 38 câu dev có trả lời + 21 câu từ chối; tới chữ trả lời đầu tiên được vẽ (C1), câu từ chối (C2), đủ câu (C3), chữ stream = chữ cuối (C5), tiền (C6) (R31/s4_do_d2_implementation.md:39-49).
- **Tiêu chí ghi trước:** D2 — sàn p50 ≤ 3 s / p95 ≤ 5 s cho "tới chữ đầu tiên trên trình duyệt" (SPEC:32); Q1 — thêm mục tiêu báo cáo 1,5 / 3 s, không chặn (SPEC:33); D5 — lợi "đủ câu − chữ đầu" < 0,5 s ⇒ A xem lại PA3 (SPEC:36).
- **Kết quả số:** C1 p50 **1.228** / p95 **2.612** ms (n = 38) ⇒ đạt sàn rộng; mục tiêu đạt **sát** (dư 0,27 / 0,39 s); C2 1.476 / 2.930 ms ⇒ đạt; C3 đủ câu 1.725 / 3.807 ms; lợi "đủ câu − chữ đầu" trung vị **441 ms** [371; 535] ⇒ **chạm luật D5**; C5 0 / 59 lệch; C6 TB 0,000247 USD (R31/s4_do_d2_implementation.md:39-49).
- **Tiền + tốc độ:** S4 0,015802 USD (64 lần gọi, giá đủ) (R31/s4_do_d2_implementation.md:59).
- **Quyết định + lý do:** D1 = PA1 (User 31/10 11:26, SPEC:31); sau S4 User **giữ PA1 và giữ sàn 3 / 5 s** (không nâng — dư nhỏ, hôm đo model gần như không suy luận trước khi viết) (BSA:22; nhật ký `bao_cao_he_thong/nhat_ky/2026-11-01_streaming_va_dong_goi.md:7`). D3 = lỗi cuối ⇒ rút lại, lỗi giữa chừng ⇒ xoá + "Thử lại" (SPEC:34).
- **Giới hạn:** một lần đo trên máy cá nhân `127.0.0.1`, không điện thoại / mạng yếu; n = 38 ⇒ p95 gần câu chậm thứ hai; lợi nhỏ vì câu dev ngắn và suy luận ≈ 0 hôm đo (token suy luận trung vị 0 ↔ 81 ở S16) (R31/s4_do_d2_implementation.md:54-56, :63-65); CI của lợi chứa 500 ms.
- **Bằng chứng:** SPEC §2, §6; R31/s4_do_d2_implementation.md; merge `a80e12d` (`streaming-final`); review cả nhánh R31/streaming_final_branch_review.md (ready, 0 major).
- **Nhãn:** `[một lần chạy]`.

#### S19 — Lõi trả lời chung cho route API và bộ đánh giá (streaming S1)
- **Vấn đề:** route `/api/chat` và hàm của bộ đánh giá (`answer_case`) có hai bản cùng luồng "tìm → ngữ cảnh → sinh → kiểm" (SPEC §3) ⇒ thêm route stream sẽ thành ba bản, dễ lệch nhau.
- **Ngày / Phase:** 01/11/2026 (S1).
- **Phương án + mốc:** mốc = hai bản riêng; S1 = một lõi chung (`backend/llm/grounded_answer.py`) mà mỗi nơi gọi tự giữ cách xử lý riêng (5 khác biệt SPEC §4.8: chuẩn hoá `[Nguồn n]`, giữ chữ khi trích dẫn hỏng, mã lỗi, recorder, log id).
- **Cách đo:** T1 158 câu trước ↔ sau (so byte); test file chạm; cổng ổn định; `answer_case` vài câu nhánh ↔ `main` (R31/s1_loi_chung_implementation.md:27, :41-42).
- **Tiêu chí ghi trước:** SPEC §5 hàng S1 — T1 **giống byte**, 5 khác biệt còn nguyên, cổng ổn định đạt.
- **Kết quả số:** T1 giống byte `4d5bbe9e0edc`; 5 khác biệt còn nguyên; review ready 0 major (R31/s1_loi_chung_review.md:3, :49-50).
- **Tiền + tốc độ:** ≈ 0,0007 USD (cổng ổn định 2 câu) (R31/s1_loi_chung_review.md:49).
- **Quyết định + lý do:** giữ lõi chung (A, theo spec) — S2 / S3 xây trên đó; đường tìm không đổi nên chất lượng không đổi (T1).
- **Giới hạn:** "không đổi hành vi" kiểm bằng T1 + test + vài câu; không chạy lại 176 câu có judge riêng cho S1 (lượt đo cuối E13 bao phủ).
- **Bằng chứng:** R31/s1_loi_chung_implementation.md; R31/s1_loi_chung_review.md; commit `9c83003`.
- **Nhãn:** `[một lần chạy]`.

#### S20 — Tính tiền / câu: giá phẳng hay giá đủ (ghi đệm, đọc đệm)
- **Vấn đề:** `cost_usd` tính giá phẳng 0,10 USD / 1M vào, trong khi nhà cung cấp tính ghi đệm 0,125 / đọc đệm 0,01 USD / 1M ⇒ mọi số tiền cũ ghi thiếu (S14).
- **Ngày / Phase:** 01/11/2026 (B108, đóng gói).
- **Phương án + mốc:** mốc = giá phẳng; B108 = giá đủ từ token thật (`cache_write_tokens`, `cached_tokens` ghi vào dòng kết quả + `chat_metrics`).
- **Cách đo:** test giá từng loại token + một lần gọi thật tính tay (R31/b108_cost_usd_implementation.md:24; R31/b108_cost_usd_review.md:25, :34, :39).
- **Tiêu chí ghi trước:** dòng cũ thiếu trường đệm ⇒ tính đúng như giá phẳng; dòng mới ⇒ khớp tính tay (R31/b108_cost_usd_review.md:34).
- **Kết quả số:** ví dụ thật 1.916 vào (1.913 ghi đệm) / 85 ra: phẳng 0,0002341 ⇒ đủ **0,000281925** (+20 %) (R31/b108_cost_usd_implementation.md:24); lượt đo cuối: TB **0,000247** USD / câu (E13).
- **Tiền + tốc độ:** 0 USD (test) + lần gọi thật trong cổng.
- **Quyết định + lý do:** dùng giá đủ từ 01/11 (A, theo giá User dán 30/10 — PS §5 dòng 2026-10-30 15:07); số USD cũ **không sửa lại**, ghi chú "giá phẳng" (R31/b108_cost_usd_implementation.md:55).
- **Giới hạn:** chưa đối chiếu hoá đơn thật của nhà cung cấp.
- **Bằng chứng:** R31/b108_cost_usd_implementation.md; R31/b108_cost_usd_review.md (ready); commit `bbbdbf9` (gộp ở `6a0c842`).
- **Nhãn:** `[một lần chạy]`.

### A8. Đánh giá (thước đo, bộ đo) + nền tảng

#### E1 — Người chấm chính: Claude hay `gpt-6-luna`
- **Vấn đề:** cần một người chấm tự động, rẻ, lặp lại được cho mọi so sánh câu trả lời. Amendment Phase 6 (23/10) đặt judge là `gpt-6-luna` — cùng model với model sinh (tự chấm bài mình). Dùng ai làm điểm chính thức.
- **Ngày / Phase:** 24/10/2026, Phase 7B; xét lại ở 8.1 (dòng 7B.3), 25/10/2026.
- **Phương án + mốc:** mốc = quyết định cũ "judge là `gpt-6-luna`" (spec 7B:32-34). (1) **Claude** (session Claude Code, quota, không USD) làm chính — D3; (2) `gpt-6-luna` làm judge phụ chấm cùng prompt — D5 (spec 7B:26, :28); (3) User chấm ~20 câu làm mốc người — D2 (:25) — **không chạy** (E7). 8.1 xét thêm "ghim model judge" (INV:171).
- **Cách đo:** Golden 176 câu, Run 1 (5 đoạn); prompt chấm cố định dùng chung (`backend/evaluation/full_corpus_judge_prompt.md`); Claude chấm lại 30 câu (nhiễu judge), luna chấm lại 30 câu, Claude Run 1 ↔ Run 2 (176, nhiễu cả đường), Claude ↔ luna (176).
- **Tiêu chí ghi trước:** spec 7B §4.4 — nếu Claude lệch User có hệ thống (chênh TB ≥ 1 điểm ở một chỉ số) thì A báo User trước khi coi điểm Claude là chính (gate 4 7B:165-167); không có ngưỡng ghi trước cho độ khớp Claude ↔ luna.
- **Kết quả số** (gate 4 7B:126-143):
  - Nhiễu judge Claude (30): Đúng chênh 0,000, trùng 1,000; Đủ +0,033, trùng 0,967; Trúng ý −0,033, trùng 0,967; lệch ≥ 2: 0.
  - Nhiễu judge luna (30): Đúng 0,000 / trùng 1,000; Đủ 0,000 / 0,933; Trúng ý −0,067 / 0,933; lệch ≥ 2: 0.
  - Khớp Claude → luna (176): Đúng +0,057, trùng 0,949, lệch ≥ 2 0,006; Đủ +0,080, trùng 0,892, ≥ 2 0,006; Trúng ý −0,006, trùng 0,960 (luna chấm cao hơn một chút; lệch ≥ 2 điểm ở 1 câu).
  - Khớp với User: **NOT RUN** (:151-152).
  - 8.1: "giữ, có số nhiễu" — mọi gate dùng cùng model Claude kế thừa; nhiễu chỉ chấm Đủ đổi 2 / 88 câu, chênh TB 0,000 (G5:56).
  - Kết luận: Claude chính — **chọn**; luna phụ — **giữ để so** (chỉ đo độ khớp, không thắng / thua); User chấm — **NOT RUN**.
- **Tiền + tốc độ:** Claude 0 USD (quota Claude Code); luna chấm Run 1 0,02651 USD + chấm lại 30 câu 0,00474 USD (`reports/phase_7b_review_2026_10_24.md:82`). Tốc độ chấm: chưa đo.
- **Quyết định + lý do:** User (D3, 24/10) chọn Claude "tiết kiệm; khác họ với model sinh" (spec 7B:26); A thêm luna phụ sau khi biết giá (:28). 8.1 giữ Claude.
- **Giới hạn:** chưa có mốc người chặt (B0 01/11 chỉ tham khảo — E7) ⇒ độ tin chủ yếu dựa "Claude tự ổn định + khớp một LLM khác họ" (gate 4 7B:152-154); model judge "kế thừa" theo session, không ghim tên bản cố định; nhiễu đo trên một cặp lượt.
- **Bằng chứng:** spec 7B:24-34; gate 4 7B:122-167; review 7B:79, :82, :93; G5:56; BDG:162.
- **Nhãn:** `[rà lại 8.1]` (dòng 7B.3) `[một lần chạy]` (một cặp lượt nhiễu, 30 câu chấm lại).

#### E2 — So hai cấu hình: "độ khớp" hay so theo cặp + CI + Holm
- **Vấn đề:** 7B chỉ có lệnh `compare` đo **độ khớp** hai file điểm, không có khoảng tin cậy, không ngưỡng ⇒ không phân biệt được cải tiến thật với nhiễu.
- **Ngày / Phase:** 7B (24/10/2026) → 8.1 G0.2 (24–25/10/2026).
- **Phương án + mốc:** mốc = `compare_scores` 7B (chỉ khớp; INV:173). (1) bootstrap theo cặp 10.000 lần + CI 95 % + thắng / hoà / thua + Holm khi > 1 biến thể — **chọn**; (2) thêm permutation test — **bỏ** ("một phép là đủ", spec 8.1:58); (3) bootstrap theo cụm tài liệu — **chưa làm** (R81/phase_8_1_g0_1_2_measure_implementation.md:134).
- **Cách đo (tự kiểm thước):** đối chứng âm = hai lượt 7B như nhau (cùng code, cùng input) phải ra "không khác"; đối chứng dương = xáo thứ tự top-10 (seed 81) phải ra "kém hơn" ở MRR / nDCG; trên nhóm all / dev / test; Holm thử với 2 biến thể.
- **Tiêu chí ghi trước:** âm ⇒ mọi chỉ số `no_difference`; dương ⇒ MRR, nDCG `worse` (report G0.1-2 §4; spec 8.1 tiêu chí 1 "tự kiểm thống kê" — `R81/phase_8_1_g5_synthesis.md:23`).
- **Kết quả số:** đối chứng âm: mọi chỉ số "không khác" ở tổng + từng loại câu, cả 3 nhóm — **PASS** (G0.1-2:88-89); đối chứng dương: MRR / nDCG "kém hơn" rõ, Keyword Coverage@10 không đổi (n = 158, CI [0; 0], đúng kỳ vọng vì cùng tập 10 đoạn) — **PASS** (:100-101);
  ví dụ dev (108): MRR 0,731 → 0,431, CI [−0,364; −0,238] (:106); Holm: xáo p Holm 0 ⇒ `worse`, chạy lại p Holm 1 ⇒ `no_difference` (:118-119).
- **Tiền + tốc độ:** 0 USD (dữ liệu 7B có sẵn). Tốc độ: chưa đo.
- **Quyết định + lý do:** spec 8.1 §5 G0.2 (User duyệt 20:49 24/10); G5 dòng 5 "thay một phần" (G5:29). Sau đó sửa chiều thắng / thua cho chỉ số "càng ít càng tốt" và gộp một hàm so cặp chung (rà code gói 3, `47a4e32`, THRC:62).
- **Giới hạn:** p bootstrap là xấp xỉ (nhỏ nhất ~0,0002); bootstrap theo câu, chưa theo cụm tài liệu; đối chứng dương mới kiểm phía tầng tìm, phía điểm câu trả lời chưa có (G0.1-2:132-137).
- **Bằng chứng:** G0.1-2:10-18, :30, :88-119, :132-137; code `backend/evaluation/full_corpus_eval.py` `bootstrap_mean_diff` :590, `paired_stats` :634, 10.000 vòng :55 (theo BDG:65-66, chưa mở code để kiểm).
- **Nhãn:** `[rà lại 8.1]`.

#### E3 — Chấm mốc và biến thể cùng một lượt mù hay so với điểm cũ
- **Vấn đề:** khi so biến thể với mốc, dùng lại điểm mốc đã chấm trước, hay sinh lại + chấm mốc cùng lúc với biến thể, trộn mù.
- **Ngày / Phase:** 8.1, 25/10/2026 (G2 §4.5); áp tiếp ở 8.2 và hai đợt sửa kho.
- **Phương án + mốc:** (1) dùng lại điểm 7B làm mốc; (2) mỗi biến thể có mốc chạy lại cùng lúc, trộn mù trong một lượt chấm — **chọn**.
- **Cách đo:** nhiễu chỉ chấm (cùng chữ trả lời, hai lượt chấm) so nhiễu cả đường (sinh lại + chấm lại, G2.0 so 7B Run 1).
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước (phép đo nhiễu để chọn cách làm).
- **Kết quả số:** nhiễu chỉ chấm: Đủ đổi 2 / 88, Đúng 1 / 88, Trúng ý 3 / 88 (BDG:146; G5:56 ghi Đủ 2 / 88, chênh TB 0,000); nhiễu cả đường: 10 / 83 câu đổi điểm Đủ (BDG:147; G5:56) ⇒ phương án (2).
  A/A ở 10 đoạn (176 câu): Đủ tụt 1 câu, Đúng tụt 2 câu (BDG:34), dùng làm nhiễu nền cho luật "số câu tụt ≤ A/A + 3" (spec sửa kho:109-110).
- **Tiền + tốc độ:** chấm bằng quota Claude; sinh lại mốc tốn tiền model sinh mỗi thí nghiệm — số riêng: chưa đo.
- **Quyết định + lý do:** A, theo số nhiễu 8.1; spec 8.2 §7 ghi "Người chấm Claude, mù, cùng lượt" (BDG:175).
- **Giới hạn:** A/A 10 đoạn đo trên kho cũ và dùng lại cho đợt sửa kho, không chạy A/A mới (spec sửa kho:110); một cặp lượt.
- **Bằng chứng:** G5:56; BDG:34, :146-147, :175; R81/phase_8_1_g2_implementation.md §4.5 (không mở trực tiếp).
- **Nhãn:** `[rà lại 8.1]` `[một lần chạy]` `[kho, cấu hình cũ]` (A/A = 2 đo trước sửa kho).
- **Suy ra:** "dùng lại điểm cũ lẫn nhiễu sinh vào chênh ⇒ phương án (2)" là lời diễn giải theo BDG:147 ("lý do mỗi biến thể có mốc chạy lại cùng lúc").

#### E4 — Có tách nhóm thử / nhóm kiểm / câu kín không
- **Vấn đề:** Golden 7A không tách tập phát triển và tập giữ kín ⇒ chọn và xác nhận trên cùng câu ("tự chấm bài mình chọn").
- **Ngày / Phase:** 7A (23/10/2026, không tách) → 8.1 G0.1 (24/10/2026, chia) + G0.4 / G0.6 (câu kín khoá 15:22 25/10/2026).
- **Phương án + mốc:** mốc = không tách (spec 7A, INV:163, "mặc định không lý do"). (1) chia phân tầng 120 dev / 56 test theo loại câu, seed cố định — **chọn**; (2) thêm 30–40 câu mới kiểu người dùng thật, giữ kín tới cuối 8.2 — **chọn** (spec 8.1 D5:24); (3) giữ không tách, ghi rõ "thăm dò" — **bỏ**.
  Câu kín: bản "không dấu" — **bỏ**, thay bằng thêm dấu cho mọi câu (User 11:40 25/10, TH81:18; câu không dấu ngoài phạm vi :24).
- **Cách đo:** kiểm file chia (dev 120, test 56, khoá câu = SHA-256 câu hỏi NFC, lệch khoá ⇒ báo lỗi) — G0.1-2:28, :149.
- **Tiêu chí ghi trước:** nhóm kiểm có đủ các loại câu; câu kín duyệt mẫu (spec 8.1 tiêu chí 1, R81/phase_8_1_g5_synthesis.md:23).
- **Kết quả số:** nhóm kiểm có đủ các loại (một dữ kiện, nhiều nguồn, có điều kiện, so sánh, ngoài kho) (BDG:141); câu kín 36 câu × 4 trường, manifest `9ea480d0d083` (TH81:25). Dùng: 10 đoạn xác nhận trên test 41 câu (+0,268 [+0,024; +0,585], G5:23); câu kín dùng ở B3 28/10 (S15, E8).
  Hiện cả nhóm kiểm 56 và 36 câu kín **đã dùng** (BDG:40).
- **Tiền + tốc độ:** 0 USD; công User duyệt mẫu câu kín. Tốc độ: không áp dụng.
- **Quyết định + lý do:** User duyệt spec 8.1 (D5) 20:49 24/10; khoá câu kín 15:22 25/10 (TH81:14, :25).
- **Giới hạn:** nhóm kiểm nhỏ ⇒ xác nhận ở nhóm kiểm chỉ nghĩa là "không làm hỏng" (BDG:59); 15 câu test có đoạn đúng đã bị nhìn ở G1.6 (G5:95); A đã thấy 3 câu kín (TH81:42); phép kiểm cuối sau cần bộ mới (BDG:192).
- **Bằng chứng:** G0.1-2:10, :28, :65-66, :73; TH81:18, :24-25, :34-35; BDG:11, :40, :80, :84.
- **Nhãn:** `[rà lại 8.1]` `[xác nhận nhóm kiểm]`.

#### K14 = E5 — Thước tầng tìm: keyword nguyên văn hay nhãn đoạn đúng (v1 → v5)
- **Vấn đề:** Golden 7A dùng keyword chép nguyên văn từ kho làm nhãn chấm tìm đoạn (≥ 1 keyword mang đáp án, không có trong câu hỏi; INV:161). Chỉ số 7B (MRR, nDCG, Keyword Coverage@10) chấm trên `search_text` top-10, trong khi model chỉ thấy bằng chứng của top-5 ⇒ "proxy chưa từng kiểm với nhãn người" (INV:161, :169); có thể trượt khi đoạn đúng diễn đạt khác, hoặc "trúng" đoạn chưa đủ ý.
- **Ngày / Phase:** 7A / 7B (23–24/10) → 8.1 G0.3 (bản 1, 25/10) → v2 / v3 (27/10) → v4 (28/10, kho đợt 1) → **v5** (30/10, kho đợt 2).
- **Phương án + mốc:** mốc = keyword @10. (1) nhãn **đoạn đúng** (vị trí trong file nguồn) cho câu khó, đo "đoạn có đáp án có lọt vào N đoạn đưa model" theo tầng (pool → top-10 → N đoạn) — **chọn, thêm vào**; keyword giữ làm chỉ số phụ, miễn phí.
  Biến thể nhãn: v2 thêm chỗ kho nói lại cùng ý + luật "trúng dòng tiêu đề"; cách đếm "loose" (B61) thử để xem đếm thiếu.
- **Cách đo:** 55 câu khó (40 dev / 15 test); agent gắn, agent khác kiểm (55 / 55 đúng nguồn), User xem mẫu (BG:91-92; BDG:144); thước theo đoạn đúng trong các đoạn đưa model dùng từ G1 (G5:29).
- **Tiêu chí ghi trước:** G0.3 PASS theo spec 8.1 D6 (agent gắn, agent khác kiểm, User duyệt ~10 câu — spec 8.1:25); v5 ghi "173 / 174 trích dẫn tìm lại nguyên văn; 1 đổi chữ, User duyệt" (BDG:108). Không có tiêu chí ghi trước cho việc chọn loại nhãn.
- **Kết quả số:**
  - Chẩn đoán từ chối nhầm 7B: theo keyword, 4 / 22 câu "có đủ keyword đáp án" mà vẫn từ chối (`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md:87`); theo đoạn đúng, **0 / 22** đủ đoạn đúng tới bước trả lời (10 thiếu ở pool 30, 5 rơi khỏi top-10, 7 rơi khỏi 5 đoạn) — G1:111-113 ⇒ **chẩn đoán cũ sai** (BDG:149-150).
  - v1 → v2 (+ luật tiêu đề): mốc B1 dev 40 câu đủ đoạn đúng 22 → **24**; kết luận tầng tìm không đổi (K3b-m vẫn thắng 9 / thua 0, CI [+0,10; +0,35]) (R26/gold_v2_review.md:72-82).
  - Đếm "loose" (B61): 1 / 55 lặp nguyên văn ⇒ thước đếm thiếu ít, kết luận không đổi (TH26:63-64).
  - Hiện hành (v5, chatbot 10 đoạn): dev 24 / 40, cả 55 câu 33 / 55, tỉ lệ ý có trong ngữ cảnh 0,76 (BDG:32).
  - Kết luận: đoạn đúng **thắng** keyword về khả năng chẩn đoán (đổi chẩn đoán từ chối nhầm); các bản nhãn v2–v5 **không đổi** kết luận đã đóng.
- **Tiền + tốc độ:** 0 USD (công agent + User xem mẫu).
- **Quyết định + lý do:** spec 8.1 D6 (User 24/10); thước "thay một phần" (G5:29): keyword vẫn giữ cho 176 câu, đoạn đúng có cho 55 / 176 (BG:25, :70); v2 / luật tiêu đề User duyệt (gold_v2_review:94); v5 mặc định từ 30/10 (BDG:178).
- **Giới hạn:** chỉ 55 / 176 câu có nhãn ⇒ nhiều kết quả tầng tìm "chưa rõ" (BDG:39; BG:123); keyword chưa từng kiểm với nhãn người trên toàn bộ (INV:161); mọi số đoạn đúng phải ghi bản nhãn (BDG:17); số trước 27/10 là v1 (:212); Keyword Coverage dễ tăng "miễn phí" khi đoạn to (INV:169).
- **Bằng chứng:** INV:161, :169; chẩn đoán 7B:80-92; G1:12, :105-113; R26/gold_v2_review.md:57-82; G5:29; BG:10, :25, :70, :123-124; BDG:16-17, :62-63, :108, :129-130, :149-150, :208-212; code `backend/experiments/phase_8_1/g1_retrieval.py:48`, `:77-94` (theo BDG:68).
- **Nhãn:** `[rà lại 8.1]` `[kho, cấu hình cũ]` (số 0 / 22 đo trên kho trước sửa, 5 đoạn, nhãn v1).

#### K13 = E6 — Số chính tính trên cả 176 câu hay bỏ câu người thật ít hỏi
- **Vấn đề:** Golden do AI viết; một số câu không giống câu người thật hỏi ⇒ số trung bình có thể phản ánh câu "đề thi" hơn câu thật. Tính số chính trên tập nào để kết luận không bị câu gượng ép chi phối.
- **Ngày / Phase:** 8.1, User 21:40 và 21:58 24/10/2026 (TH81:15); 9 câu bất đồng User giữ 11:33 25/10 (TH81:17).
- **Phương án + mốc:** (a) tính cả 176 câu (mốc 7B); (b) **chỉ câu tự nhiên** (User 21:40, PS:184); (c) **bỏ câu không tự nhiên** = tự nhiên + chỉ đo năng lực (User 21:58, PS:183) — **chọn**; "chỉ tự nhiên" thành số phụ; tách 3 nhãn dùng kèm.
- **Cách đo:** 2 agent gắn nhãn độc lập, đo kappa; bất đồng ⇒ User quyết (PS:164, :183; BG:91-92).
- **Tiêu chí ghi trước:** không có tiêu chí ghi trước (quyết định của User; ngưỡng kappa không thấy trong nguồn).
- **Kết quả số:** kappa **0,765**; 9 câu bất đồng User giữ là tự nhiên ⇒ **82 tự nhiên / 65 chỉ đo năng lực / 29 không tự nhiên** (BG:16; BDG:145; G1:144-146). Tính lại G1 theo (c) từ dữ liệu có sẵn: dev còn 88 câu trong kho, 32 câu có đoạn đúng; **"không đổi kết luận đã ghi ở mục 4"** (G1:142-148).
  Không thấy bảng so số giữa (a), (b), (c) cho cùng thí nghiệm.
- **Tiền + tốc độ:** 0 USD.
- **Quyết định + lý do:** User 21:58 24/10 chọn (c) — "câu hỏi đánh giá phải tự nhiên; số chính = bỏ câu không tự nhiên" (PS:183; TH81:15); từ đó mọi thí nghiệm dùng số chính bỏ 29 câu (BG:16).
- **Giới hạn:** nhãn do agent gắn (không phải log người dùng thật), User chỉ quyết câu bất đồng; (b) chỉ 40 câu dev tự nhiên (11 có đoạn đúng) (G1:149); số "natural" ở G1 mục 3–4 tính theo nhãn người gắn thứ nhất cũ (47 câu), file nhãn cuối cho dev tự nhiên 40 câu — G1 không tính lại (G1:147-150).
- **Bằng chứng:** PS:164, :183-184; G1:39-40, :142-150; BG:16, :71, :91-92; TH81:15, :17, :34; `R81/phase_8_1_g0_6_baseline_lock.md:45` (nhãn sha `0b65d1c138d2`, 82 / 65 / 29; G5:12).
- **Nhãn:** `[rà lại 8.1]`.
- **Suy ra:** "(b) quá nhỏ" suy từ cỡ 40 / 11 câu (G1:149); nguồn không ghi đó là lý do User đổi 21:40 ⇒ 21:58.

#### E7 — Mốc người: chấm điểm tay, đọc cặp mù hay để sau
- **Vấn đề:** mọi kết luận về câu trả lời (gồm chọn 10 đoạn) dựa người chấm Claude; cần ít nhất một mốc người để biết judge có lệch người không.
- **Ngày / Phase:** 7B D2 (24/10) → 8.2 D2 (25/10) → 8.2 §11 (28/10) → B0 làm 01/11.
- **Phương án + mốc:**
  - 7B D2: User chấm điểm ~20 câu (spec 7B:25) — User **bỏ** 24/10 (gate 4 7B:151-152);
  - 8.2 D2: **đọc cặp mù** 15–20 câu, mỗi câu 2 trả lời X / Y (5 so 10 đoạn), nhận xét tự do, không chấm điểm (spec 8.2:26) — **chọn** 25/10;
  - 28/10 khi việc này (B0) chặn chuỗi việc: PA1 chờ B0 / PA2 B0 rút 10 câu / **PA3 gộp B1 trước, B0 làm sau** (spec 8.2:253-255) — **chọn PA3**.
- **Cách đo:** 20 cặp đã chuẩn bị (`data/phase_8_2/b0/` (private)); luật dừng: User ngược judge nhiều hơn cùng chiều, ≥ 5 cặp quyết ⇒ A trình giữ 10 / về 5 (spec 8.2:259-261).
- **Tiêu chí ghi trước:** luật dừng spec 8.2 §3 mục 4 (spec 8.2:44, :142); spec 7B §4.4 ngưỡng chênh TB ≥ 1 điểm (gate 4 7B:165-166).
- **Kết quả số:** B0 01/11, 20 cặp: phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được (judge cũng chấm 10 hơn ở cả 3); User không chọn bên theo cặp ⇒ 0 cặp quyết ⇒ luật dừng "chưa rõ" (`data/phase_8_2/b0/ket_qua_b0_2026-11-01.md` (private)).
- **Tiền + tốc độ:** 0 USD; ~30–45 phút công User (spec 8.2:26, :253).
- **Quyết định + lý do:** User 24/10 bỏ chấm tay; User 25/10 chọn đọc cặp mù, không chấm điểm (PS:52); User 09:29 28/10 chọn PA3 vì chưa rảnh và muốn xong phần tồn sớm; căn cứ: 10 đoạn có lợi theo judge, đổi ngược được bằng một cấu hình (spec 8.2:253-258). Sau B0: User chọn giữ 10 (14:23 01/11/2026).
- **Giới hạn:** B0 là mốc tham khảo, không phải phép đo chặt — câu trả lời sinh trên kho cũ (trước 2 đợt sửa kho), User không chọn bên theo cặp; kết luận vẫn dựa judge Claude.
- **Bằng chứng:** spec 7B:25; gate 4 7B:151-167; spec 8.2:26, :251-264; PS:52, :146; BDG:38, :85, :184, :188.
- **Nhãn:** `[một lần chạy]` `[kho, cấu hình cũ]`.

#### E8 — Câu bị lỗi trích dẫn (API trả 500) chấm thế nào khi so
- **Vấn đề:** 7B đưa chữ của câu lỗi trích dẫn cho judge ⇒ 4 câu người dùng thấy lỗi 500 vẫn được chấm 5 / 4,75 / 5 (INV:44) ⇒ điểm không phản ánh người dùng thấy gì.
- **Ngày / Phase:** 7B (24/10, lỗi không trừ điểm — inventory dòng 7B.4) → plan B3 8.2 (28/10, câu 500 = điểm 1) → hai đợt sửa kho.
- **Phương án + mốc:** (1) điểm judge thô (như 7B); (2) câu 500 chấm Đủ = Đúng = 1 — **chọn** (số chính B3); (3) bỏ câu 500 khỏi phép so — báo kèm.
- **Cách đo:** B3, câu kín, 33 câu trong kho, chatbot đầu 8.2 ↔ cuối 8.2, bootstrap 10.000 vòng.
- **Tiêu chí ghi trước:** plan B3 §4 — Đủ / Đúng trung bình ≥ −0,1 và số câu tụt ≤ A/A + 3 = 5; câu 500 chấm 1 (R82/phase_8_2_b3_plan.md:125-128).
- **Kết quả số** (R82/phase_8_2_b3_implementation.md, chỉ số tổng hợp): (2) Đủ **+0,818** [+0,394; +1,333], 12 / 21 / 0; Đúng +0,697 [+0,273; +1,212] (:93-94); (1) thô: Đủ +0,364 [+0,091; +0,727]; Đúng +0,242 [+0,030; +0,545] (:112); (3) bỏ 4 câu: Đủ +0,448 [+0,138; +0,828]; Đúng +0,276 [+0,034; +0,621] (:114).
- **Tiền + tốc độ:** B3 ≈ 0,014 USD (BDG:123).
- **Quyết định + lý do:** luật ghi trong plan B3 (A duyệt sha `27e75be5ed44`); dùng tiếp ở câu kín và hai đợt sửa kho, **chưa** vào bộ chấm chung `full_corpus_eval` (BDG:86).
- **Giới hạn:** n = 33; luật chưa nằm trong code bộ chấm chung.
- **Bằng chứng:** INV:44; plan B3:125-128; B3 impl:88-114; BDG:18, :86, :122-123.
- **Nhãn:** `[xác nhận nhóm kiểm]` (câu kín) `[một lần chạy]`.
- **Suy ra:** "cả 3 cách đều tốt hơn — kết luận không đảo theo cách tính" suy từ 3 CI cùng nằm trên 0; nguồn chỉ nói "lợi không chỉ do bộ kiểm mới" (BDG:123).

#### S15 — Phép kiểm cuối 8.2 trên câu kín (B3)
- **Vấn đề:** chatbot cuối 8.2 (10 đoạn + NFC + bộ kiểm trích dẫn v2) có "không tệ hơn" chatbot đầu 8.2 trên câu chưa ai dùng để chọn không.
- **Ngày / Phase:** 28/10/2026, 8.2 B3 (User cho mở câu kín cho người chạy).
- **Phương án + mốc:** nhánh đầu 8.2 (5 đoạn, bộ kiểm cũ) ↔ nhánh cuối (đang chạy).
- **Cách đo:** 36 câu kín (33 trong kho + 3 ngoài kho), chấm theo cặp, judge Claude; câu 500 trích dẫn chấm 1 (R82/phase_8_2_b3_plan.md:125-126; E8).
- **Tiêu chí ghi trước:** "không làm hỏng" = qua 2 sàn và 3 mức tụt (Đủ / Đúng: TB ≥ −0,1 và số câu tụt ≤ A/A + 3 = 5); "tốt hơn" chỉ báo, không quyết (plan B3:125-126, :151, :154).
- **Kết quả số:** Đủ **+0,818** [+0,394; +1,333] (12 tốt / 21 như nhau / 0 tụt); Đúng **+0,697** [+0,273; +1,212] (8 / 25 / 0); ngoài kho bị trả lời 0 / 3; lỗi kỹ thuật 0; từ chối nhầm 4 ⇒ 2; câu 500 trích dẫn 4 ⇒ 0; bỏ 4 câu 500 vẫn Đủ +0,448 [+0,138; +0,828], 0 tụt ⇒ **không làm hỏng và tốt hơn** (TH82:30).
- **Tiền + tốc độ:** 0,0138 USD (TH82:41); latency không đo trong B3.
- **Quyết định + lý do:** User đóng 8.2 lúc 10:23 28/10 (TH82:1).
- **Giới hạn:** gộp 3 thay đổi; 0 câu kín dạng NFD ⇒ NFC chưa được câu kín thử; câu kín đã mở ⇒ không còn "chưa ai thấy" (TH82:46-50); chưa có mốc người.
- **Bằng chứng:** TH82:30, :46-50; R82/phase_8_2_b3_review.md (review sẵn sàng, tái lập byte) — không mở file câu kín.
- **Nhãn:** `[xác nhận nhóm kiểm]` `[một lần chạy]` `[kho, cấu hình cũ]`.

#### E9 — Đo "bịa thêm / sai điều kiện": judge cũ, kiểm số bằng code hay judge tách ý
- **Vấn đề:** User chốt 28/10 thứ tự lỗi (sai cảnh báo > nói chắc sai / bịa > …); prompt chấm cũ so với đáp án mẫu, không chấm bám nguồn ⇒ không bắt bịa trong câu có trích dẫn hợp lệ (INV:170).
- **Ngày / Phase:** 27/10 (C48, C51) → 28/10 (B89 thước lỗi nặng), User nhận 29/10.
- **Phương án + mốc:** mốc = judge Đúng / Đủ / Trúng ý (không đo bịa). (1) **kiểm số bằng code** (số trong câu trả lời có trong 10 đoạn ngữ cảnh không — C48, xem S10); (2) **luật kiểm sau sinh** (C51, xem S9);
  (3) **judge Claude tách từng ý, so với chính ngữ cảnh model đọc** ⇒ đếm H và P0 — **chọn**; số chính P0_sai theo "một trong hai judge gắn" (thận trọng) thay vì đa số (R27/do_loi_nang_plan.md:159).
- **Cách đo:** (1) dev 99 câu được trả lời, 68 câu có số; (3) 145 câu Golden thật + 42 câu đối chứng (chèn số sai, chèn câu lạc đề, chèn điều kiện sai, chép nguyên văn), 2 lượt judge độc lập, kiểm chéo số bằng code.
- **Tiêu chí ghi trước** (R27/do_loi_nang_implementation.md:42-55, plan §4): recall chèn bịa ≥ 18 / 20; báo nhầm chép nguyên văn ≤ 1 / 10; báo nhầm câu âm giống thật ≤ 1 / ≥ 10; recall chèn điều kiện sai ≥ 90 %; kiểm chéo số ≤ 5 % ý có số; kappa H ≥ 0,6.
- **Kết quả số:**
  - (1) 0 câu sai số thấy được trên 68; 4 cờ đều là phép tính đúng (R26/c48_so_trong_cau_tra_loi.md:9-11) ⇒ "chưa cần kiểm bằng code" (BDG:90) — **đã thử, chưa áp dụng**;
  - (2) bắt được 2 / 2 câu lỗi đã biết (sau khi chỉnh luật trên chính 2 câu đó), 0 cờ ở chatbot, không tách được "lạc đề" với "một phần có ích" ⇒ **gác** (TH26:62-63);
  - (3) cả 2 judge: chèn bịa 20 / 20, chèn điều kiện sai 12 / 12, báo nhầm 0 / 10 và 0 / 15, kiểm chéo số 0 / 162 và 0 / 158, kappa H 1,0 ⇒ **thước nhận** (impl:46-54, :60). Trên 145 câu thật: H 1 / 145 (0,7 %, Wilson [0,1 %; 3,8 %]); P0_sai 0 / 65 ([0 %; 5,6 %]); P0_thiếu 7 / 65 (:66-71).
- **Tiền + tốc độ:** 0 USD phần Golden (judge quota ~1,6 M token Claude, :96); bộ an toàn sinh 0,0079 USD (:5).
- **Quyết định + lý do:** A duyệt plan (sha `d69481b2addb`), User nhận thước 29/10 (BDG:88); code kiểm số giữ làm **thước kiểm judge**, không làm thước chính (plan:146).
- **Giới hạn:** người chấm Claude, chưa người đọc (mẫu 20 câu chờ User); câu chèn lạc đề quá dễ (còn dấu Markdown, `[n]` lạ) ⇒ 10 / 10 loại này nói ít (impl:57-58); kappa 1,0 ở tỉ lệ H rất thấp chủ yếu chỉ nói hai lượt nhất quán (:83); P0 trên Golden yếu (chủ yếu giờ / giá) ⇒ cần bộ an toàn (E10).
- **Bằng chứng:** plan:65, :146, :157-160; impl:9-25, :42-71, :80-87; C48:9-11; TH26:62-63; BDG:19-21, :88, :90.
- **Nhãn:** `[một lần chạy]` (một lượt sinh; hai lượt chấm).

#### E10 — Đặt sàn cho bộ 32 câu an toàn: đo A/A trước hay sinh lại khi bị bắt
- **Vấn đề:** bộ 32 câu an toàn (28 trong kho, 4 ngoài kho, agent viết) lượt 28/10 có 2 / 27 câu P0_sai; muốn đặt sàn "không thêm câu sai" cho thay đổi sau mà không báo động giả.
- **Ngày / Phase:** 28/10 (đề xuất) → 29/10 (C84 đo A/A) → 30/10 (áp ở đợt 2 sửa kho).
- **Phương án + mốc:** đề xuất ban đầu "P0_sai mới = 0" (R27/do_loi_nang_implementation.md:153-155). (a) đo nhiễu trước: chạy lại mốc 32 câu một lần, đặt sàn theo số câu đổi — B và C khuyến nghị (:156-157); (b) không đo trước, câu bị bắt thì sinh lại cả mốc lẫn biến thể 3 lần (:158-159).
  **Chọn (a) + vẫn giữ bước sinh lại 3 lần cho mỗi câu mới** (R27/do_loi_nang_aa_implementation.md:61-62).
- **Cách đo:** lượt 2 cùng code, kho, ngữ cảnh (32 / 32 giống từng chữ); 2 judge mới chấm trộn mù lượt 1 + lượt 2 + 15 đối chứng ⇒ tách nhiễu sinh và nhiễu chấm (aa:24-30).
- **Tiêu chí ghi trước:** cổng đối chứng như B89 — recall chèn điều kiện sai ≥ 9 / 10, báo nhầm ≤ 1 / 5, tách lô 0 (aa:34-38).
- **Kết quả số:** cổng đạt (10 / 10, 0 / 5, 0 — aa:36-38); P0_sai lượt 1 → lượt 2: 2 → 0, **2 câu đổi, 0 câu mới**; H 2 → 0; nhiễu chấm 0 câu đổi (aa:44-49); P0_thiếu đổi 3 câu (aa:47).
  ⇒ sàn: P0_sai mới ≤ 2 và H mới ≤ 2 (đếm hai chiều), mỗi câu mới sinh lại 3 lần; **đảo cảnh báo = 0**; 0 câu ngoài kho bị trả lời (aa:60-64). Áp ở đợt 2 (30/10): P0_sai mới 0; 2 câu cũ sinh lại 3 lần đều 0 / 3 (R27/sua_kho_dot2_implementation.md:50).
- **Tiền + tốc độ:** A/A 0,0081144 USD (trần 0,02); trung vị 3,3 s / câu (aa:4, :24).
- **Quyết định + lý do:** A nhận theo review (cách (a)); dùng bắt buộc cho mọi thay đổi từ 29/10 (BDG:89).
- **Giới hạn:** 1 cặp lượt, 28 câu ⇒ "2 câu dao động" là ước thô, không có CI; gồm cả trôi theo ngày của nhà cung cấp; câu do agent viết có thể dễ hơn câu thật (aa:68-72); 0 lỗi trên 28 câu chỉ nói tỉ lệ sai điều kiện dưới ~12 % (BDG:42).
  Mẫu số ghi lệch nhỏ giữa các file (28 câu trong kho ↔ 27 / 26 câu judge gắn "liên quan") — kết luận 0 không đổi.
- **Bằng chứng:** R27/do_loi_nang_implementation.md:129-160; R27/do_loi_nang_aa_implementation.md:7-72; R27/sua_kho_dot2_implementation.md:49-52; BDG:25, :88-89.
- **Nhãn:** `[một lần chạy]`.

#### E12 — Rà code: gỡ hay giữ công cụ cũ; nội dung kho trong repo public; cách sửa hướng dẫn
- **Vấn đề:** rà code Phase 0–7 (25/10, 39 phát hiện, 5 gói) đặt 3 câu hỏi có phương án cho User ngoài việc "sửa lỗi" (các sửa lỗi thường không có so sánh phương án, không ghi khối).
- **Ngày / Phase:** 25/10/2026 (đề xuất, User duyệt tối 25/10 — sổ gốc chỉ ghi giờ ước) → 26/10/2026 (đợt 3, merge `421c302`).
- **Phương án + mốc** (bản đề xuất `git show 0663676:bao_cao_he_thong/94_DE_XUAT_SUA_CODE.md` §4, dòng 78–86):
  - Công cụ cũ: (a) đường "Representation B" (chatbot không dùng) giữ / gỡ; (b) 2 bộ kiểm khói Phase 5 / 6. A nghiêng: gỡ (a) + Phase 5, giữ Phase 6 bỏ phần thừa — **chọn như A nghiêng**.
  - Hướng dẫn Phase 0–4: (a) thêm dòng "lịch sử"; (b) viết lại phần hiện hành; (c) chuyển vào `guides/history/` — **chọn (a)**.
  - Repo public (nội dung kho nguyên văn trong cấu hình / test / script; đường dẫn tới một dự án khác của User trong hướng dẫn): để nguyên / chuyển sang private từ giờ, không xoá lịch sử / xoá cả lịch sử git — **chọn chuyển từ giờ, không xoá lịch sử**; 80 report lịch sử còn trích kho: User chọn để nguyên (26/10).
- **Cách đo:** không đo chất lượng; bằng chứng "không đổi hành vi" = sha toàn bộ đoạn, mốc kết quả tìm, chuỗi gửi model giống byte trước ↔ sau + test + cổng ổn định.
- **Tiêu chí ghi trước:** plan đợt 3 D1–D8 (THRC:65).
- **Kết quả số:** D1 sha đoạn `60591acff422ece6`; D2 mốc tìm `cefb2d1ad609`; D3 25 câu giống byte; D4 197 đạt / 1 hỏng / 4 lỗi (phần cần khoá API); code **8.345 → 6.218 dòng**; 0 chuỗi kho trong code (THRC:65); đường dẫn dự án khác 48 → 0, đường dẫn chết 34 → 1 (THRC:61).
- **Tiền + tốc độ:** cả đợt ~0,003 USD (phần lớn ước) (THRC:69).
- **Quyết định + lý do:** User tối 25/10 "gỡ code không dùng nếu không ảnh hưởng hệ thống; hướng dẫn 0–4 thêm dòng lịch sử; nội dung kho + đường dẫn dự án khác ra khỏi file tracked từ giờ, không xoá lịch sử git" (PS:158).
- **Giới hạn:** một số tác động chỉ suy từ code (vd Qdrant lỗi giữa lúc hỏi); test cần khoá OpenAI không chạy (`bao_cao_he_thong/94_DE_XUAT_SUA_CODE.md:40-41`).
- **Bằng chứng:** THRC:26-35, :56-69; `bao_cao_he_thong/94_DE_XUAT_SUA_CODE.md:25-33`; PS:158.
- **Nhãn:** `[một lần chạy]`.
- **Suy ra:** "chọn như A nghiêng" ở mục công cụ cũ ghép từ `94_DE_XUAT_SUA_CODE.md:32` (gỡ Representation B, smoke Phase 5, giữ smoke Phase 6 còn 4 câu) với bản đề xuất — nguồn không có một dòng "User chọn (a)…" riêng cho câu hỏi này.


#### E13 — Lượt đo cuối Phase 1–8: bản cuối có "làm hỏng" so với mốc 30/10 không
- **Vấn đề:** sau streaming + giá đủ, chatbot có giữ chất lượng không; số tuyệt đối cuối của "RAG mức 1".
- **Ngày / Phase:** 01/11/2026 (đóng gói; commit đo `89c988e`, code = `6a0c842`).
- **Phương án + mốc:** mốc = bộ "sau" đợt 2 sửa kho (30/10, `751b352`); bản cuối "sau"; lượt lặp cùng ngày A/A (User Q2).
- **Cách đo:** Golden 176 (ba bên trong một lượt chấm mù, 6 judge Claude mới; số chính 129); bộ an toàn 32 (2 judge, thước lỗi nặng); 15 câu theo ngày (2 judge); 22 câu qua `/api/chat`; S4 dùng lại (R31/do_cuoi_implementation.md §3).
- **Tiêu chí ghi trước:** plan `ae8d42d520d4` §3 — F1–F4 = 0; T1 / T2 tụt ≤ 5 câu và TB ≥ −0,1; T3 ≤ mốc + 1; A1 = 0; A2 P0_sai mới ≤ 2, đảo cảnh báo 0; câu theo ngày 0 "đoán ngày rồi nói sai"; ≤ 0,0005 USD / câu.
- **Kết quả số:** Golden: F1–F4 = 0; T1 tụt **2**, TB **+0,016** [−0,023; +0,054]; T2 tụt **2**, TB **+0,008** [−0,023; +0,039]; T3 12 = 12; A/A không sát ngưỡng ⇒ **không làm hỏng**. Điểm TB số chính: Đúng 4,713 · Đủ 4,581 · Trúng ý 4,721.
  An toàn: A1 0 / 4; A2 vế 1 **2** (đúng ngưỡng; sinh lại 3 lần: bản mới và bản mốc đều sai 1 / 3 ⇒ không thấy kém đi so với mốc — 3 lần mỗi bên chỉ phát hiện khác biệt lớn); 0 đảo cảnh báo. Câu theo ngày: 0 / 12 đoán ngày sai; từ chối nhầm 5 câu trong kho (mốc 6 / 14).
  Qua API (22 câu): p50 2.340 / p95 3.800 ms (mốc 27/10: 3.068 / 6.039) — một lần đo (01/11); hôm đo model gần như không suy luận trước khi viết (token suy luận trung vị 0 — 28/10: 81) ⇒ có thể nhanh hơn ngày thường; chênh với 27/10 / 30/10 chủ yếu do phía nhà cung cấp, không phải do code (cùng đường tìm, T1 giống byte); sàn 3 / 5 s đạt rộng, mục tiêu 1,5 / 3 s đạt sát (dư 0,27 / 0,39 s). Tiền TB **0,000247** USD / câu (R31/do_cuoi_implementation.md §4; R31/do_cuoi_b_an_toan_ngay.md §4).
- **Tiền + tốc độ:** §4–§7 **0,1122** USD + S4 0,0158 + bộ kín 0,0112 ⇒ **0,139 / trần 0,20** (R31/do_cuoi_b_bo_kin.md §4).
- **Quyết định + lý do:** không làm hỏng ⇒ dùng số này làm số cuối Phase 1–8.
- **Giới hạn:** judge Claude, chưa mốc người; "không làm hỏng" chỉ bắt được tụt lan rộng; A2 vế 1 chạm đúng ngưỡng; Golden / an toàn đo đường không stream (dựa C5 của S4); mốc khác ngày (A/A cùng ngày cho nhiễu rất nhỏ).
  Bộ kín mới (40 câu chưa ai thiết kế hệ thống thấy; 34 trong kho + 6 ngoài kho; một lượt, mở một lần): sàn **đạt** — 0 / 6 câu ngoài kho bị trả lời, 0 / 40 lỗi kỹ thuật, 0 / 30 sai điều kiện / đảo cảnh báo; báo (không phải sàn): 0 bịa thêm;
  điểm TB **thấp hơn** Golden số chính: Đủ **4,18** [3,74; 4,59] ↔ 4,58 (−0,40), Đúng 4,38 ↔ 4,71. Khoảng cách đến từ **cả hai**: từ chối nhầm **4 / 34** (12 %) ↔ 12 / 158 (8 %) — cả 4 ở loại nhiều nguồn / so sánh; **và** câu được trả lời kém đủ ý hơn — cùng thước "chỉ câu được trả lời": Đủ 4,60 [4,40; 4,80] (30 câu) ↔ Golden **4,82** (121 câu) ⇒ **−0,22**, Đúng 4,83 ↔ 4,96 (−0,13); rõ nhất ở câu một dữ kiện: 4,42 (12 câu, 0 từ chối nhầm, Đúng 5,00) ↔ Golden câu được trả lời 4,97 (≈ −0,55) — trả lời đúng nhưng thiếu ý. Không do thành phần bộ kín: trộn lại theo tỉ lệ loại câu của Golden ⇒ Đủ ≈ 4,20 (R31/do_cuoi_b_bo_kin.md §4; R31/do_cuoi_review.md M-1).
- **Bằng chứng:** R31/do_cuoi_implementation.md; R31/do_cuoi_b_an_toan_ngay.md; R31/do_cuoi_b_bo_kin.md; plan `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` (`ae8d42d520d4`); kết quả private `data/do_cuoi_2026-11-01/` (private).
- **Nhãn:** `[một lần chạy]`; sàn an toàn `[xác nhận nhóm kiểm]` (bộ kín mới); chất lượng: bộ kín cho thấy số Golden **lạc quan** (−0,3 đến −0,4 toàn bộ, −0,22 ở câu được trả lời, ≈ −0,55 ở câu một dữ kiện; n nhỏ, CI toàn bộ chạm số Golden).

---

## 4. Phần B — theo Phase

Bảng này chỉ trỏ về các khối ở Phần A (không lặp số). Trạng thái Phase chính thức: `session_prompt/Project_Status.md` §3.
Mã khối: K = kho + Golden · N2 = chia đoạn / vector / Qdrant · T3 = tìm kiếm · S = sinh / API · E = đánh giá. "X = Y" là khối gộp từ hai thẻ trùng.

| Phase / đợt | Ngày | Việc chính | So sánh phương án đã đo (khối) | Không đo / chỉ quyết bằng thiết kế (khối) | Ghi chú độ tin |
|---|---|---|---|---|---|
| 0–1 Nền tảng, khung backend | 08/2026 | luật đơn giản, khung backend, 3 cấu hình tìm | — (không có phép so) | K2 (curated ↔ bản thô) | `[chưa kiểm lại Phase 0–7]`; nhóm đánh giá không lập thẻ cho Phase 0–1 |
| Biên soạn kho | 08–09/2026 | 5 mảng, cấu trúc `travel/` | — | K1 (cấu trúc kho, phạm vi file) | `[chưa kiểm lại Phase 0–7]` |
| 2 Chia đoạn (món ăn → toàn kho) | 08–09/2026 (toàn kho 11–12/09) | chia theo cấu trúc Markdown, không gối đầu, 3 tokenizer | N2-01, N2-03, N2-04, N2-05 (đo lại ở 8.1 G3) | — | quyết định gốc không đo; số so ở 8.1 |
| 3 Vector + từ khoá | 09/2026 (12/09) | e5-small + BM25; 4 model vector | N2-07 (08a, món ăn), N2-11 / N2-12 / N2-14 (08b, món ăn; N2-11, N2-12 đo lại 8.1) | N2-08 (4 model toàn kho chưa chấm) | bản món ăn ≠ toàn kho |
| 4 Qdrant | 09/2026 (12–13/09) + metadata v2 29–30/09 | collection, thông tin điểm 7 trường | N2-15 = T3-04 (HNSW, đo ở 8.1) | N2-16 (tổ chức collection, xoá cũ) | — |
| 5 Tìm kiếm + rerank | 08/2026 (món ăn) · 13–14/09 (toàn kho) | `dense_bm25_rrf`, không rerank | T3-02 (08b), T3-07 (MiniLM, món ăn 4.5 / 08c) | Phase 5 toàn kho: chỉ code / test / latency | chất lượng so ở 8.1 |
| 6 Sinh câu trả lời, API, UI | 09/09 → 23/10 | OpenAI baseline ⇒ `gpt-6-luna`; API + UI một lượt | — | S1 (model sinh: chỉ thử khói, không chấm), S12 (API / UI) | `[chưa kiểm lại Phase 0–7]` |
| 7 (món ăn, lịch sử) + Golden món ăn V1–V3 | 08/2026 | đánh giá bản món ăn | K10 | — | lịch sử, kho khác |
| 7A Golden toàn kho | 23/10 | 176 câu + smoke 10 | — | K9 (cách soạn đề), K14 = E5 (keyword làm proxy) | mức đại diện câu thật chưa đo |
| 7A2 Sửa kho + build lại | 23–24/10 | 25 mục / 27 file; thu về 2 model vector | N2-10 (ghim nhà cung cấp 8B) | K4, K12 (quét Golden), N2-08 | `[một lần chạy]` |
| 7B Bộ chấm + mốc 176 câu | 24/10 | judge Claude, mốc 176 câu | E1 (Claude ↔ luna) | — | chưa có mốc người (E7) |
| 8 cũ (món ăn: 08a / 08b / 08c) | 29–30/08 | benchmark model vector / trộn / rerank trên bản món ăn | N2-07, N2-11, N2-12, N2-14, T3-02, T3-07 | — | lịch sử; số món ăn không áp cho toàn kho |
| 8.1 Rà 56 quyết định Phase 0–7 | 24–25/10 | thí nghiệm lại; **chỉ 10 đoạn thắng** | E2, E3, E4, K14 = E5, K13 = E6, K3, K11, N2-01…N2-06, N2-11, N2-12, N2-13 = T3-06, N2-15 = T3-04, T3-01, T3-02, T3-03, T3-05, T3-08, T3-09 (luna 8.1), S2, S3, S4 (P1), S5, S7, S8 | — | `[rà lại 8.1]` + `[kho, cấu hình cũ]` (kho 8.459 đoạn, nhãn v1, 5 đoạn) |
| 8.2 Áp dụng + đợt cải tiến từng khâu | 25–28/10 | 10 đoạn + NFC vào chatbot; bước 2 không biến thể nào vào | S2 (B1), S4 (R2), S6 (R3 NOT RUN), S7 (R1), S9 (C51), S10 (R4 / C48), T3-09 = S11 (K3, K3b), T3-03 (K1), S15 (B3 câu kín), E8 | E7 (mốc người dời — PA3) | B3 `[xác nhận nhóm kiểm]` |
| Phần tồn: thước lỗi nặng | 27–30/10 | judge tách ý, bộ an toàn 32 câu, A/A | E9, E10 | — | bộ an toàn do agent viết |
| Sửa kho đợt 1 | 27–28/10 | 123 sửa / 65 file; loại file danh mục | K5, K8, K12, K3 | K7 (build lại tại chỗ) | "không làm hỏng", không đo "tốt hơn" |
| Sửa kho đợt 2 | 29–30/10 | 123 sửa / 40 file | K6, K8, K12 | — | bộ "trước" dùng lại câu trả lời 28/10 |
| Phần tồn: tốc độ / tiền | 27–30/10 | B65, C58, B95 | S13, S14 | — | thước harness ↔ thước qua API khác nhau (S13) |
| Phần tồn: đo trước streaming | 28/10 | C73 | S16 | — | `[một lần chạy]` |
| Phần tồn: câu theo ngày | 30/10 | 15 câu (12 câu quyết) | S17 = E11 | — | ⇒ Phase 9 |
| Phần tồn: Qwen3-8B | 30/10 | thử thay e5-small | N2-09 | — | đo trên kho hiện tại, `[xác nhận nhóm kiểm]` |
| Rà code 5 gói | 25–26/10 | sửa code sau 8.1 | — | E12 | phần lớn là sửa lỗi, không phải so phương án (trừ R1 ở S7) |
| Đóng gói Phase 1–8 (streaming, giá đủ, đo cuối) | 31/10 – 01/11 | streaming vào chatbot (`a80e12d`); `cost_usd` giá đủ; đo lại theo loại câu; lượt đo cuối | S18 (S4), T3-10 (Q3a), E13 (đo cuối) | S19 (lõi chung — kiểm bằng T1), S20 (giá đủ — kiểm bằng test + tính tay) | `[một lần chạy]`; bộ kín: sàn đạt, số Golden lạc quan (cả câu được trả lời); B0 tham khảo (E7); **Phase 8 User đóng 14:29 01/11/2026** |
| Hội thoại nhiều lượt | dời Phase 9 (User 11:20 01/11) | nháp thiết kế giữ làm tư liệu | **không làm ở Phase 1–8** | — | — |
| 9 | chưa mở | nghiên cứu rộng trước | **chưa làm** | — | — |

---

## 5. Chỉ mục chéo: khối ⇒ Phase

| Khối | Phase / đợt |
|---|---|
| K1, K2 | biên soạn kho, 0–2 |
| K3 | 8.1 ⇒ sửa kho đợt 1 |
| K4 | 7A2 |
| K5, K7 | sửa kho đợt 1 |
| K6 | sửa kho đợt 2 |
| K8, K12 | 7A2, đợt 1, đợt 2 |
| K9 | 7A |
| K10 | 7–8 cũ (món ăn) |
| K11 | 8.1 |
| K13 = E6 | 8.1 |
| K14 = E5 | 7A / 7B ⇒ 8.1 G0.3 ⇒ nhãn v2–v5 (27–30/10) |
| N2-01 … N2-06 | 2 ⇒ 8.1 G3 |
| N2-07 | 8 cũ 08a (món ăn) |
| N2-08 | 3–4 ⇒ 7A2 |
| N2-09 | phần tồn 30/10 |
| N2-10 | 7A2 |
| N2-11, N2-12 | 3 / 08b ⇒ 8.1 G4K |
| N2-13 = T3-06 | 8.1 G1.4 + G4K |
| N2-14 | 08b (món ăn) |
| N2-15 = T3-04 | 4 ⇒ 8.1 G1.2 |
| N2-16 | 4, metadata v2, 7A2 / B9 |
| T3-01 | 8.1 G1 + 8.2 B42 |
| T3-02 | 5 / 08b ⇒ 7B ⇒ 8.1 G1.3 / G4K ⇒ 8.2 K2 |
| T3-03 | 8.1 G1.1 / G4-B ⇒ 8.2 K1 |
| T3-05 | 8.1 G1.4 ⇒ 8.2 B1 |
| T3-07 | 5 (món ăn 4.5) / 08c ⇒ 8.1 G1.5 |
| T3-08 | 8.1 G4 |
| T3-09 = S11 | 8.1 G4 ⇒ 8.2 K3 / K3b |
| S1, S12 | 6 |
| S2 | 8.1 G2.1a ⇒ 8.2 B1 / B3 |
| S3, S5 | 8.1 G2 |
| S4 | 8.1 P1 ⇒ 8.2 R2 |
| S6, S9, S10 | 8.2 bước 2 |
| S7 | 8.1 G2.4 ⇒ 8.2 R1 |
| S8 | 8.1 G2.3 ⇒ rà code 1a |
| S13, S14 | phần tồn 27–30/10 |
| S15 | 8.2 B3 |
| S16 | phần tồn 28/10 |
| S17 = E11 | phần tồn 30/10 |
| E1 | 7B |
| E2, E3, E4 | 7A / 7B ⇒ 8.1 G0 |
| E7 | 7B ⇒ 8.2 §11 |
| E8 | 7B ⇒ 8.2 B3 |
| E9, E10 | phần tồn 27–30/10 |
| E12 | rà code 25–26/10 |
| S18, S19, S20 | đóng gói Phase 1–8 (streaming S1–S4, B108 giá đủ) |
| T3-10 | đóng gói (Q3a đo lại theo loại câu) |
| E13 | đóng gói (lượt đo cuối) |

---

## 6. Giới hạn chung

- **Gần như chưa có so sánh nào đo lại trên kho hiện tại** (204 file / 8.424 đoạn, nhãn v5, 10 đoạn ngữ cảnh) — chỉ có Qwen3-8B (N2-09), hai đợt "trước ↔ sau" sửa kho (K5, K6), streaming (S18) và lượt đo cuối (E13, đo, không chọn). Mọi kết luận 8.1 và bước 2 của 8.2 là `[kho, cấu hình cũ]`
  (kho 8.459 đoạn, nhãn v1, nhiều phép đo lúc đưa 5 đoạn). Thống kê đoạn (trung vị token, đoạn vụn…) cũng là số kho cũ.
- **Mốc người chỉ tham khảo** (E7): mọi kết luận về câu trả lời dựa judge Claude — ổn định với chính nó và khớp luna (E1, E3); B0 (01/11) không có cặp nào User ngược judge (0 cặp quyết; 3 cặp cùng chiều 10 đoạn), nhưng trên kho cũ và không chọn bên theo cặp.
- **Bộ đo nhỏ:** 32–40 câu dev có nhãn đoạn đúng, 15 câu test; chỉ 55 / 176 câu có nhãn này. Nhiều "không khác" / "chưa rõ" nghĩa là chưa chứng minh được, không phải đã chứng minh bằng nhau; phần lớn "kém hơn" ở khâu tìm là do sàn "0 câu mất", không phải CI.
- **Không còn bộ kiểm chưa ai thấy:** nhóm kiểm 56 câu, 36 câu kín (E4, S15) và bộ kín mới 40 câu (E13, 01/11) đều đã dùng; bộ mới cho thấy số Golden **lạc quan** (điểm thấp hơn 0,3–0,4, cả ở câu được trả lời) ⇒ lần kiểm tổng quát sau cần bộ mới nữa. Golden và bộ an toàn do AI viết rồi người duyệt — mức đại diện câu người dùng thật chưa đo (K9, E10).
- **Model sinh chưa từng được so có chấm điểm** (chỉ thử khói 5 lần gọi, S1); model vector toàn kho chỉ có một phép so có chấm (Qwen3-8B, N2-09); reranker MiniLM chỉ có bằng chứng trên bản món ăn (T3-07).
- **Phase 0–1 và Phase 5 không có phép so phương án đo được** (chỉ dựng khung / code / latency); nhiều lựa chọn Phase 0–7 là "mặc định không lý do", chọn bằng thiết kế (K1, K2, N2-16, S12).
- **Không phải phép đo nào cũng có tiêu chí ghi trước:** các phép đo hiện trạng (tốc độ qua API B65, số trong câu trả lời C48, luật kiểm sau sinh C51, kiểm sổ tiền B95) không có — báo cáo User từng ghi "mọi thí nghiệm có luật ghi trước" là nói quá (đã sửa 01/11).
- **Số tiền và tốc độ cần đọc kèm thước:** mọi USD trước 01/11 tính theo giá phẳng (thiếu ≈ 20 %, S14; từ 01/11 giá đủ — S20); tốc độ có hai thước (harness ↔ qua API) cho p95 khác nhau (S13); p95 harness dao động 4,9 ↔ 9,8 s giữa các lượt cùng code (khác kho; nguồn cho là do mạng / nhà cung cấp).

**Chưa làm** (không có so sánh nào trong báo cáo này; streaming, lượt đo cuối và B0 đã làm — S18–S20, E13, E7):
- Hội thoại nhiều lượt: **dời sang Phase 9** (User 11:20 01/11/2026); nháp thiết kế giữ làm tư liệu.
- Từ nhận xét B0 (đề xuất A, chờ User): câu dự trù chi phí theo mức ⇒ để trợ lý hỏi lại người dùng (Phase 9); `[n]` chen trong câu khó đọc ⇒ đổi cách hiển thị nguồn ở giao diện mới.
- Phase 9: chưa mở (mở bằng nghiên cứu rộng trước).
- Còn mở trong các khối: R3 "nêu đủ chi tiết" (S6, cần thêm câu), chỉ bật bỏ dấu khi câu không dấu (N2-13 = T3-06), dọn ràng buộc 3 tokenizer (N2-05), câu nhiều nguồn (T3-10 ⇒ Phase 9). (Công thức tiền S14 đã sửa — S20.) (Câu Golden lệch kho K12: User giữ nguyên 01/11 — đã đóng.)

---

## 7. Phụ lục

### Phụ lục A — Viết tắt đường dẫn bằng chứng

Số sau dấu hai chấm là số dòng trong file đó (vd `BKD:54`). Mọi file dưới đây đều có trên repo, trừ đường dẫn ghi "(private)".

| Viết tắt | Đường dẫn |
|---|---|
| BKD | `bao_cao_he_thong/02_BAO_CAO_KHO_DU_LIEU.md` |
| BG | `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` |
| CD | `bao_cao_he_thong/03_BAO_CAO_CHIA_DOAN.md` |
| EM | `bao_cao_he_thong/04_BAO_CAO_EMBEDDING_TU_KHOA.md` |
| QD | `bao_cao_he_thong/05_BAO_CAO_LUU_TRU_QDRANT.md` |
| BTK | `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md` |
| BSA | `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` |
| BDG | `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` |
| PS | `session_prompt/Project_Status.md` |
| PH | `session_prompt/PROJECT_HISTORY.md` |
| R81/ | `report_agent/2026-10-24_phase_8_1_ra_soat/` |
| TH81 | `R81/TONG_HOP.md` |
| INV | `R81/phase_8_1_decision_inventory.md` (56 quyết định Phase 0–7) |
| G5 | `R81/phase_8_1_g5_decision_table_draft.md` (bảng kết luận 8.1) |
| G0.1-2 | `R81/phase_8_1_g0_1_2_measure_implementation.md` |
| G1 / G2 / G3 / G4 / G4K | `R81/phase_8_1_g1_implementation.md` / `…_g2_implementation.md` / `…_g3_implementation.md` / `…_g4_implementation.md` / `…_g4_keyword_implementation.md` |
| R82/ | `report_agent/2026-10-25_phase_8_2_ap_dung/` |
| TH82 | `R82/TONG_HOP.md` |
| R26/ | `report_agent/2026-10-26_cai_tien_tung_khau/` |
| TH26 | `R26/TONG_HOP.md` |
| b65 | `R26/b65_latency_dau_cuoi.md` |
| phan_loai_loi_B | `R26/phan_loai_loi_B.md` |
| R27/ | `report_agent/2026-10-27_phan_ton_phase_cu/` |
| TH27 | `R27/TONG_HOP.md` |
| impl / plan / aa (trong khối N2-09, S16, S17 = E11, E9, E10) | file `…_implementation.md` / `…_plan.md` / `do_loi_nang_aa_implementation.md` cùng tên việc trong `R27/` |
| THRC | `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md` |
| R31/ | `report_agent/2026-10-31_streaming_spec/` (streaming, giá đủ, Q3a, lượt đo cuối) |
| SPEC | `docs/superpowers/specs/2026-10-31-streaming-design.md` (bản 5 `00fb57ee01b2`) |
| spec 7A | `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` |
| spec 7A2 | `docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md` |
| spec 7B | `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` |
| spec 8.1 | `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` |
| spec 8.2 | `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` |
| spec sửa kho | `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` |
| spec V2 / spec V3 | `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md` / `…2026-08-27-phase-8-golden-dataset-v3-design.md` |
| spec 08a | `docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md` |
| spec Phase 6 | `docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md` |
| amendment 10-01 / 10-23 | `docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md` / `…2026-10-23-phase-6-gpt-6-luna-amendment.md` |
| impl 7A / review 7A | `reports/phase_7a_golden_implementation_2026_10_23.md` / `reports/phase_7a_golden_review_2026_10_23.md` |
| gate 1 7A2 / gate 2 7A2 | `reports/phase_7a2_gate_1_corpus_correction_implementation_2026_10_23.md` / `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md` |
| gate 4 7B / review 7B | `reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md` / `reports/phase_7b_review_2026_10_24.md` |
| chẩn đoán 7B | `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md` |
| 08a / 08b / 08c | `reports/phase_8_08a_embedding_benchmark_implementation_report.md` / `reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md` / `reports/phase_8_08c_reranker_benchmark_implementation_report.md` |
| 4.5 | `reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md` |
| khảo sát token 09/09 | `reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md` |
| khảo sát OpenRouter | `reports/phase_7a2_openrouter_embedding_survey_2026_10_23.md` |
| probe | `reports/phase_8_probe_context_top10_2026_10_24.md` |

### Phụ lục B — Mã nội bộ (một dòng mỗi mã)

Chú ý trùng tên: biến thể "S1 / S2 / S3" của G3 (N2-06) **khác** khối S1–S3; việc "E2 sửa thiếu `[n]`" của 8.2 (S8) **khác** khối E2; "T1–T3" của BM25 (N2-11) **khác** luật T1–T3 đo sửa kho.

| Mã | Nghĩa |
|---|---|
| G0 (G0.1–G0.6) | Phần thước đo của 8.1: G0.1 chia dev / test, G0.2 thống kê so cặp, G0.3 nhãn đoạn đúng, G0.4 câu kín, G0.5 tham số "mặc định như cũ" cho code production để harness gọi chung, G0.6 khoá mốc. |
| G1 (G1.1–G1.6) | 8.1 khâu tìm: đếm tầng, HNSW, cách trộn, NFC / không dấu, MiniLM, chẩn đoán từ chối nhầm. |
| G2 (G2.0–G2.4) | 8.1 khâu sinh: mốc, 5 ↔ 10 đoạn (2.1a), thứ tự đoạn (2.1b), prompt P1 / P2 (2.2), bộ kiểm trích dẫn (2.3), mức suy luận (2.4). |
| G3 | 8.1 chia đoạn: H1 (chỉ 1 tokenizer), H2 (gộp đoạn cùng mục), H3 (gộp dòng bảng), B10 (ngân sách gấp đôi), small-to-big, tiền tố, S1–S3 (sửa nhỏ). |
| G4 / G4-A / G4-B / G4K | 8.1 rerank: xếp lại top-10 / chấm pool 100 / phần từ khoá BM25 (tách từ, k1 / b, bỏ dấu). |
| G5 | Bảng kết luận 8.1 (giữ / thay / chưa rõ / NOT RUN cho từng quyết định cũ). |
| P1 / P2 | 8.1: prompt "trả lời phần có căn cứ" / thêm 2 luật cũ của spec Phase 6. |
| B0 | 8.2: mốc người — User đọc cặp mù 5 ↔ 10 đoạn (làm 01/11 — E7). |
| B1 | 8.2: gộp 10 đoạn + NFC + bộ kiểm trích dẫn v2 vào chatbot (merge `510e1a8`, 28/10). Cũng là mốc của bước 2. |
| B3 | 8.2: phép kiểm cuối trên 36 câu kín (28/10). |
| B5 | 24/10: thăm dò sinh lại 22 câu từ chối nhầm với 10 đoạn. |
| B9 | 24/10: xoá collection không dùng (2 collection bản món ăn). **Khác** "b9" trong tên file `R27/sua_kho_b9_implementation.md` (= bước 9 của đợt sửa kho 1). |
| K1 / K2 / K3 / K3b-n / K3b-m / K3c (mã việc 8.2) | Bước 2 Phase 8.2, khâu tìm: pool vector 100 / native p30 k = 2 (NOT RUN) / luna xếp 30 đoạn / luna chọn 10 số với suy luận `none` / với suy luận mặc định / bản nhanh (chưa làm). Khác các khối K1–K3 của kho. |
| R1 / R2 / R3 / R4 | Bước 2 Phase 8.2, khâu sinh: suy luận `none` ở 10 đoạn / trả lời một phần chữ siết hơn / "nêu đủ chi tiết" (NOT RUN) / thước "số có trong nguồn". |
| E1b | Tên khác của R2 trong spec 8.2. |
| B42 | 26/10: phân loại lỗi tầng tìm ở 10 đoạn (T3-01). |
| B61 | 27/10: thử cách đếm "loose" cho nhãn đoạn đúng (K14 = E5). |
| B65 | 27/10: đo tốc độ đầu cuối qua API thật, 22 câu tự viết (S13). |
| B89 | 28/10: thước lỗi nặng (judge tách ý, bộ an toàn) (E9). |
| B92 | 30/10: harness thử Qwen3-8B (tag `hoso/b92-qwen3-harness`) (N2-09). |
| B95 | 30/10: kiểm log tiền (`cache_write_tokens`) (S14). |
| B96 | 30/10: plan đo câu theo ngày (S17 = E11). |
| C11 / C27 / C36 | Các việc rà / phân loại của C ở 8.1–8.2 (phát hiện file danh mục còn trong chỉ mục; review sửa đáp án; phân loại câu thiếu chi tiết). |
| C48 | 27/10: đo số trong câu trả lời có trong nguồn không (S10, E9). |
| C51 | 27/10: đo khả thi luật kiểm sau sinh (S9). |
| C58 | 27/10: tách thời gian theo khâu (S13). |
| C59 | 27/10: log `chat_metrics` (S12). |
| C65 / C89 | 27/10 / 30/10: kiểm và đếm lại lỗi trích dẫn với bộ kiểm mới (S8). |
| C70 / C73 | 28/10: đo trước streaming (S16). |
| C84 | 29/10: A/A bộ an toàn (E10). |
| C93 | 30/10: đo câu theo ngày tương đối (S17 = E11). |
| C95 | 30/10: C kiểm việc thử Qwen3-8B (N2-09). |
| C74 / C80 / C85 | Các review của C cho B3 / sửa kho đợt 1 / A/A bộ an toàn. |
| F1–F4 | Bốn sàn của đo sửa kho (K5, K6), định nghĩa ở `R27/sua_kho_do_truoc_sau_plan.md:124-127`: F1 = câu ngoài kho bị trả lời (0 / 18); F2 = câu "nói chắc sai" **mới** (câu trong phạm vi được trả lời mà judge cho Đúng ≤ 3, có ở "sau" mà không ở "trước", chấm lại mù xác nhận); F3 = lỗi kỹ thuật / 500 không do trích dẫn (0 mỗi bên sau một lần chạy lại); F4 = câu 500 vì trích dẫn **mới** (0). |
| T1–T3 (luật đo) | Nghĩa khác nhau theo plan: ở K3b-m (8.2, nhãn T1–T7 ở `R82/phase_8_2_k3b_m_answer_plan.md:47-53`) **T3 = số câu tụt Đủ ≤ 4 (dev) / 6 (test)** (= A/A + 3); ở **cả hai đợt** sửa kho (định nghĩa `R27/sua_kho_do_truoc_sau_plan.md:128-130`, đợt 2 giữ nguyên) T1 = Đủ, T2 = Đúng: số câu tụt ≤ 5 / 129 **và** trung bình ≥ −0,1 (trên 129 và trên tập không chạm), T3 = từ chối nhầm trong phạm vi ≤ trước + 1; "T1" cũng là phép kiểm kết quả tìm 158 câu giống byte (T3-05, K8). |
| A1–A2 | Sàn bộ an toàn: A1 câu ngoài kho bị trả lời; A2 P0_sai mới, đảo cảnh báo. |
| W9 | Theo dõi "thiếu ý ở mục làm yếu" (đợt 2 sửa kho). |
| PA1–PA3 | Ba phương án 28/10 khi mốc người chặn việc; PA3 = gộp B1 trước, mốc người sau. |
| D1–D8 (rà code) | Các kiểm "không đổi hành vi" của đợt 3 rà code (E12). |
| D2 / D3 / D5 (spec 7B, 8.1, 8.2) | Các mục quyết định trong spec (vd 7B D2 = User chấm tay, D3 = judge Claude, D5 = luna phụ; 8.1 D5 = chia 120 dev / 56 test + thêm 30–40 câu kín; 8.1 D6 = nhãn đoạn đúng; 8.2 D2 = đọc cặp mù). |
| Representation A / B | A = text tìm kiếm = tên tài liệu + đường tiêu đề + phần bằng chứng (đang dùng); B = thêm ngữ cảnh do model viết (chưa từng build, code gỡ 26/10). |
| harness | Script chạy chatbot trực tiếp trên 176 câu, không qua HTTP. |
| `check` | Lệnh kiểm Golden: định dạng 4 phần + keyword có nguyên văn trong kho. |
| native / runtime | `native_hybrid_rrf` (vector và BM25 tìm độc lập rồi trộn) / `dense_bm25_rrf` (BM25 chấm lại pool vector — đang chạy). |
| Bản món ăn (Foods), 08a / 08b / 08c, 4.5 | MVP cũ 08/2026 (572 đoạn) và các notebook benchmark của nó: model vector / cách trộn / reranker; 4.5 = rà đơn giản Qdrant + tìm kiếm. |

### Phụ lục C — Chỗ tài liệu lệch nhau (không lệch nào làm đổi quyết định đã chốt)

| Ý | Tài liệu 1 nói | Tài liệu 2 nói | Có vẻ đúng |
|---|---|---|---|
| Tốc độ bản đang chạy (**đã sửa 01/11**: BSA nay ghi cả số qua API) | BSA:18, :21: p95 4,90 s "đạt sát" (harness, không HTTP) | b65:48, :62: qua API 10 đoạn p95 6,0 s tuần tự / 6,4 s đồng thời 4 | Hai thước khác nhau; cần ghi cả hai (S13) |
| Lý do gác K3b-m (**đã sửa 01/11** ở BTK) | BTK:65: 5 câu tụt **và** "vượt sàn 3 / 5 s chốt 28/10", ≈ 3,8× tiền | TH26:33, :51; R82/phase_8_2_k3_plan.md:94: lúc chốt 27/10 chỉ luật T3 quyết, p95 chỉ theo dõi; sàn tốc độ chốt 28/10 (PS:145) | TH26 / PS đúng về thứ tự (T3-09 = S11) |
| "Mọi thí nghiệm có luật ghi trước" (**đã sửa 01/11** ở BSA) | BSA:80 | b65:4 "không có plan duyệt"; C48 / C51 / B95 là đo hiện trạng | Câu ở BSA nói quá |
| "10 đoạn chưa đo p50 / p95" | TH82:49 | b65:48-49: có số qua API (27/10) | Có lẽ TH82 muốn nói "chưa đo trên Golden 176" (suy ra) |
| Số câu sửa khi đóng Golden 7A (**đã sửa 01/11** ở BG) | BG:65, :94 (bản cũ): 4 xoá, 10 sửa | impl 7A:253: 15 dòng cũ không còn (4 xoá, 11 sửa) | Bảng GATE R impl 7A:230-246 có 4 xoá + 11 sửa ⇒ 11 đúng; "cả 14 case" ở impl 7A:224 đếm thiếu 1 (K9) |
| File danh mục có bị loại trước 28/10 | PS:195: "inventory bị loại khỏi discovery" (08/09) | INV:87: file danh mục một mảng vẫn được index (33 đoạn) | INV đúng cho 08/09 → 28/10; đã sửa 28/10 (K3) |
| 16 câu User trả lời thuộc đợt nào | spec sửa kho:44: đợt 1 gồm "+ 16 câu User trả lời" | TH27:58, :90: chuyển đợt 2 ("15 câu chờ User") | Có vẻ chuyển sang đợt 2; 16 ↔ 15 chưa kiểm |
| Đỉnh VRAM Qwen-0.6B | EM:55: ~1,23 GB | `reports/qwen3_gtx1650_embedding_execution_report_2026_09_13.md:44`: ~1,26 GB (1.323.238.400 bytes) | Số byte = 1,23 GiB; "1,26" không khớp cách đổi nào (agent gom thẻ tự tính) |
| Cos vector 8B khi không ghim | PS:259: "cos ~0,996" | spec 7A2:132 min 0,99535; :188 0,9954 | Spec ghi số đo cụ thể (N2-10) |
| 4 model vector toàn kho chạy tới đâu | EM:54, :99: chỉ mẫu 12 đoạn | QD:69: 4 collection toàn kho 8.460 điểm; INV:113: chưa từng chấm | Cả hai đúng một phần: có index đủ nhưng không chấm (N2-08) |
| Bảng: một dòng hay nhóm dòng | code / CD:61: tách từng dòng | INV:99: tài liệu 09/2026 "không đặt một hàng làm mặc định" | Code là thứ đang chạy; 8.1 H3 không khác (N2-03) |
| Ngày bỏ MiniLM (bản món ăn) | BTK:112-114: gắn mốc 12/08 | report Phase 5 món ăn :245-249: không có benchmark chất lượng ở Phase 5; số "giảm điểm" ở 4.5 / 08c (30/08) | Ngày ở BTK có vẻ không chính xác (chưa kiểm ngày report 4.5) |
| MRR@5 e5-small món ăn không rerank | 08b:127: 0,7088 | 08c:83: 0,7748 (cùng Recall@5, nDCG@5) | Chưa rõ; có thể hai notebook tính MRR khác nhau (chưa kiểm code) |
| Latency reranker GPU ~150 đoạn | BTK:64: 11–14 s / câu | G4:119: p50 / p95 10,6 / 13,8 s; pilot 8,8 / 12,9 s | G4 là số gốc |
| Mức suy luận mặc định của luna | INV:150: chưa rõ | R82/phase_8_2_r1_plan.md:24, TH26:66: `medium` | Chưa kiểm |
| Vì sao câu có điều kiện trượt ở thử khói Phase 6 | BSA:141: không tìm ra đoạn bảng giá | report luna Phase 6:189-193: đoạn giá không vào top-5 **và** luật từ chối tất-cả-hoặc-không; "chưa phải nguyên nhân đã chứng minh" | Report luna đủ hơn |
| Cam kết so Qwen ở Phase 8 | amendment 10-01:86-101: "Qwen là benchmark bắt buộc" | PS:181: User 24/10 bỏ so model ở Phase 8 | PS là quyết định mới hơn; amendment chưa đánh dấu đã thay (chưa kiểm) |
| Cỡ dev có đoạn đúng | TH81:41: 32 câu | BDG:39, :82: 40 câu dev / 15 test | Cả hai đúng: 32 = sau khi bỏ câu không tự nhiên |
| Mẫu số câu theo ngày | BDG:91: "15 câu: 0 câu đoán ngày rồi nói sai" | R27/ngay_hien_tai_implementation.md:34, :43-44: chỉ số quyết trên 12 câu | Report nguồn đúng hơn (S17 = E11) |
| Mẫu số P0_sai bộ an toàn | BDG:88: 0 / 28 | R27/do_loi_nang_implementation.md:135: 27 câu liên quan; aa:44: 26 / 28 | Lệch cách ghi; kết luận 0 không đổi |
| Nhiễu chỉ chấm | BDG:146: Đủ 2 / 88, Đúng 1 / 88, Trúng ý 3 / 88 | G5:56: chỉ ghi Đủ 2 / 88 | G5 ghi thiếu, không phải mâu thuẫn |

### Phụ lục D — Bằng chứng chung

- Trạng thái và quyết định: `session_prompt/Project_Status.md` §3 (bảng Phase), §5 (quyết định).
- Kết luận 8.1: G5 (`R81/phase_8_1_g5_decision_table_draft.md`); danh sách 56 quyết định Phase 0–7: INV (`R81/phase_8_1_decision_inventory.md`).
- Tổng hợp từng đợt: TH81, TH82, TH26, TH27, THRC (Phụ lục A).
- Commit / tag chính: `510e1a8` (10 đoạn + NFC vào chatbot), `9e6d371` (nhận `[Nguồn n]`), `6b59788` (loại file danh mục), `5100b90` (log `chat_metrics`), `421c302` (rà code đợt 3), `47a4e32` (hàm so cặp chung);
  hồ sơ phương án bị bỏ: tag `hoso/p82-k1`, `hoso/p82-k3`, `hoso/p82-k3b`, `hoso/b92-qwen3-harness`, `hoso/p82-r1` (`63a472f`), `hoso/p82-r2` (`aec9ab8`), `hoso/c70-ttft` (`1f70095`) — các nhánh cũ đã đổi thành tag (TH27:144); `a6f609c` nằm trong `hoso/p82-k3b`.
- Nháp gốc của báo cáo này (private, còn chi tiết không đưa lên repo): `data/so_sanh_phuong_an/` (private) — 68 thẻ theo khâu, bảng theo Phase, chỗ mâu thuẫn; bảng giới hạn đã biết: `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` (private).
