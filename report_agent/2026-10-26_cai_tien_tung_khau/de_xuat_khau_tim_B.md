# B43 — Bản nháp phần khâu tìm cho tài liệu thiết kế đợt cải tiến

Người làm: B (Claude Opus 5.5, `hue-rag-23`) · 2026-10-26 21:00 +0700 (`date`) · Việc: `CURRENT_HANDOFF.md` mục "Việc giao phiên tối
26/10", dòng B43 · **0 USD**: chỉ đọc report và tính lại từ `data/cai_tien_tung_khau_2026-10-26/b42_per_case.jsonl`, không chạy tìm kiếm
mới · Đây là **đầu vào** cho tài liệu thiết kế của A, không phải plan để duyệt.

## 1. Ba điều cần biết trước

1. **Ở mốc context 10, "đủ đoạn đúng trong context" chính là "đủ đoạn đúng trong top-10"** (B42: mọi câu đóng đủ 10 đoạn). 8.1 đã đo
   đúng chỉ số này (`top10_gold_all`) cho 10 cách trộn (G1.3) và cho rerank pool 100 (G4-B). Vì vậy, với các biến thể đó, phần lớn số đo
   ở mốc mới **đã có sẵn**, không cần chạy lại trên dev.
2. **Rerank chỉ xếp lại trong top-10 thì không đổi gì ở mốc context 10**: tập 10 đoạn vẫn như cũ. Muốn có ích, rerank phải chọn 10 đoạn
   từ pool 30 hoặc rộng hơn. Vì vậy tín hiệu luna của 8.1 (rerank top-10, MRR +0,17) không chuyển thẳng sang mốc mới.
3. **Luật (a) của User chưa phủ biến thể khâu tìm.** Luật (a) nhận một thay đổi khi chất lượng không tụt quá mức cho phép **và** rẻ / nhanh
   hơn rõ. Luật này hợp với khâu trả lời (ví dụ hạ mức suy luận). Biến thể khâu tìm đi theo chiều ngược lại: tốn thêm (latency, có khi
   tiền) để chất lượng tăng. **Cần A / User chốt** khi nào nhận một thay đổi "chất lượng tăng, chi phí tăng". B đề xuất dùng luật mặc định
   của `run-experiment` (chỉ số quyết tăng vượt nhiễu, CI 95% > 0) kèm mức tụt cho phép ghi trước về latency / USD. B không tự chọn.

## 2. Nhóm câu B42 còn thiếu ở context 10 (dev 18 / 40; test 8 / 15, chỉ đếm)

| Nhóm (B42) | Câu dev | Cơ chế có thể sửa |
|---|---|---|
| A. ngoài pool 30, chỉ thiếu vì thế | 22, 68, 92, 97, 113, 120 | mở rộng pool |
| A+B. ngoài pool **và** xếp sau | 19, 168 | mở rộng pool + xếp lại |
| B. trong pool 30 nhưng ngoài top-10 | 17, 38, 48, 67, 70, 85, 156, 159, 167 | xếp lại trong pool |
| C. thước đo (dòng tiêu đề) | 143 | không phải lỗi tìm |

Câu 68 ở context 5 còn một fact bị cắt; fact đó đã nằm trong top-10, nên ở mốc context 10 câu 68 chỉ còn thiếu do fact ngoài pool.

## 3. Biến thể (không biến thể nào ghi Qdrant)

"Trần" là số câu dev mà **mọi** fact đang thiếu nằm trong vùng ứng viên của biến thể. Đây là giới hạn trên theo cơ chế, **chưa đo**: vào
được vùng ứng viên chưa có nghĩa là lên được top-10. Với V1 / V2, trần chỉ đếm câu có fact ngoài pool (dev 8, test 5).

| # | Biến thể (đổi đúng một thứ) | 8.1 đã đo gì | Trần dev / test | Tốn | Rủi ro hỏng câu khác |
|---|---|---|---|---|---|
| V1 | **Pool dense 30 → 100**, giữ cách làm runtime (BM25 xếp lại trong pool, RRF k 60) | **Chưa đo**. G1 chỉ đo native p100/p200; "exact + pool 100" chỉ là thử khô 5 câu, không kết luận (`phase_8_1_g1_plan.md:117-118`) | 6 (19, 22, 92, 97, 113, 168) / 2 | 0 USD; latency: Qdrant `limit=100` + BM25 mã hóa 100 đoạn bằng Python, ước +10–30 ms (chưa đo; runtime p50/p95 31/44 ms, `phase_8_1_g4_implementation.md:179`) | BM25 chấm thêm 70 đoạn có thể đẩy đoạn đúng của câu đang đủ ra ngoài top-10 (G1.3: native p100 mất 1 câu, `phase_8_1_g1_implementation.md:72`) |
| V2 | **Native p30, RRF k=2** (dense 30 ∪ BM25 cả kho 30) | **Đã đo trên dev đúng chỉ số này**: `top10_gold_all` +0,100 [+0,025; +0,200], 4/36/0, MRR +0,009, không qua Holm trên 10 biến thể (`phase_8_1_g1_implementation.md:76`, `:82`) | 4 (19, 22, 68, 168) / 2 | 0 USD; latency thêm một truy vấn sparse Qdrant (bảng G5: native ~+10 ms, `phase_8_1_g5_decision_table_draft.md:70`) | 8.1 đo 0 câu mất. Chạy lại trên dev cùng 40 câu sẽ ra **đúng số cũ** (tất định) ⇒ không có thông tin mới; việc còn lại là xác nhận trên test |
| V3 | **Rerank luna listwise trên pool 30 → top-10** | Chỉ đo luna xếp lại **top-10** (3/27/0, MRR@10 +0,172 [+0,092; +0,261], `phase_8_1_g4_implementation.md:86`). Pool 30: **chưa đo** | 9 (nhóm B) / 3 | Ước ≈ 30 × ~100 token vào + ~270 ra ⇒ ~0,0004–0,0005 USD/câu (ước; 8.1 top-10: 0,0088 USD / 30 câu); latency +3,5–5 s/câu (8.1 p95 5,2 s với 10 đoạn) | LLM không tất định ⇒ cần A/A; đầu ra lỗi = lỗi kỹ thuật (`g4_rerank.luna_rank`); phụ thuộc API; **ngược chiều "nhanh hơn"** |
| V4 | Giới hạn đoạn mỗi file (≤ 3) khi chọn 10 từ pool 30 | Chưa đo (B40 C2 đề xuất từ báo cáo ChatGPT) | **1** (17) / 0 | 0 USD, ~0 ms | **17 / 22** câu dev đang đủ có file đúng chiếm > 3 chỗ trong top-10 (test 6) ⇒ giới hạn 3 dễ đẩy đoạn đúng ra ngoài. **B đề xuất không chạy**: ở context 10, dữ liệu đi ngược giả thuyết (B40 tính ở context 5) |
| V5 | Native p100 + rerank M1 (G4-B) | **Đã đo**: top-10 đủ đoạn đúng +0,200 [+0,067; +0,367], 6/24/0 so runtime (dev 30, `phase_8_1_g4_implementation.md:111`). Đây là tín hiệu mạnh nhất ở mốc context 10 | — | p50 / p95 10,6 / 13,8 s trên GPU (`:119`); production chạy CPU | **Không đề xuất** vì latency (chậm hơn hàng trăm lần). Ghi lại để không ai đề xuất lại khi chưa có lý do mới, ví dụ có GPU khi deploy |

Đã bác hoặc đã đo, **không đề xuất lại**: đổi k RRF / DBSF có trọng số (G1.3 `:73-79`, G4K `phase_8_1_g4_keyword_implementation.md:113-118`),
tách từ BM25 bigram / pyvi / mã (G4K `:85-90`), M1 / M2 xếp lại top-10 (`phase_8_1_g4_implementation.md:82-85`), exact thay HNSW (G1.2).

## 4. Tiêu chí đề xuất ghi trước (theo `run-experiment`; A chốt trong spec)

Áp chung cho V1 và V3 (V2 chỉ còn bước xác nhận trên test):

```yaml
baseline: chatbot context 10 sau B1 (nhánh p82-b1 811d25d; T1 cefb2d1ad609), retrieval dense_bm25_rrf pool 30
changed_variable: <một biến thể>
unchanged: [corpus, chunker, embedding, index, prompt, model, judge, context 10]
data: {split: split.json, group: dev, n_gold: 40 (101 fact), n_answer: 88 dev chính}   # test: 15 gold / 56 câu — đã nhìn ở G1.6, ghi giới hạn
metrics:
  - {name: đủ đoạn đúng trong context 10 (= top10_gold_all), fn: g1_retrieval.gold_coverage, role: decide, noise: 0 (V1 tất định; V3 lấy từ A/A)}
  - {name: câu mất đoạn đúng khỏi context 10 so với mốc, role: floor, floor: 0}
  - {name: từ chối đúng out_of_scope, role: floor, floor: 18/18}         # khi chạy lượt sinh
  - {name: Completeness dev chính (judge Claude, chấm mốc cùng lượt mù), role: tolerance, max_worse: -0.1 (luật (a)); noise A/A ctx10: 0,000 [−0,034; +0,034], 2/88 câu đổi (phase_8_2_b1 §4)}
  - {name: latency p95 retrieval CPU, role: tolerance, max_worse: <A/User chốt — V1 đề xuất +50 ms; V3 cần User nói có nhận +3–5 s không>}
  - {name: USD/câu đầu–cuối, role: tolerance, max_worse: <V1 0; V3 ≈ +0,0005>}
  - {name: MRR@10 (keyword), lỗi citation, từ chối nhầm, role: watch}
```

**Cỡ mẫu (tính trước):** để CI 95% của chỉ số quyết > 0 trên 40 câu thì cần khoảng **≥ 4 câu thắng, 0 câu thua** (G1.3 native p30 k=2:
4/36/0 → [+0,025; +0,200]). Nếu chạy ≥ 2 biến thể và áp Holm thì cần nhiều hơn.
- V1 có trần 6 câu, nhưng 2 trong số đó (19, 168) còn cần xếp lại ⇒ thực tế chỉ khoảng 4 câu "dễ cứu". **Ghi trước: kết quả V1 rất có thể
  chỉ là "chưa rõ"**, trừ khi V1 cứu gần hết và không làm mất câu nào.
- V3 có trần 9 câu nên đủ chỗ để đạt tiêu chí, nhưng LLM có nhiễu ⇒ chạy 2 lượt (A/A) trước.
- Test: V1 trần 2 / 8 câu, V2 2 / 8, V3 3 / 8. Test chỉ dùng để xác nhận và chỉ có 15 câu ⇒ yếu: xác nhận trên test gần như chỉ
  kiểm "không làm mất câu", khó cho thấy "tốt hơn".

**Luật giữ:** cả ba điều kiện của `run-experiment` §4 phải đạt trên dev, rồi xác nhận trên test. Sau đó mới chạy lượt sinh dev chính 88
câu để kiểm mức tụt Completeness. Ước tiền ≈ 88 × 0,000204 ≈ 0,018 USD; V3 cộng thêm phí rerank ≈ 0,04 USD.

## 5. Thứ tự B đề xuất

1. **V1 pool dense 100** (0 USD, harness G1 đã có tham số: `g1_retrieval run --treatment dense_bm25_rrf --pool 100`). Chỉ là một tham
   số, không đổi kiến trúc; chạy trên dev mất vài phút.
2. **V2: xác nhận trên test** bằng dữ liệu sẵn có hoặc lượt chạy test tất định (0 USD). Trên dev, V2 đã "gần qua" (4/36/0); không chạy
   lại dev.
3. **V3 luna trên pool 30**: chỉ làm khi V1 / V2 không đủ **và** User chấp nhận +3–5 s / câu cùng phí API. Pilot 10 câu và ước lại tiền
   trước (bẫy `Project_Status.md` §8: luna ra ~270 token / câu).
4. V4, V5: không chạy; ghi vào `BAO_CAO_TIM_KIEM.md` mục "Đã thử / không chọn" (V5) và "không đề xuất, vì sao" (V4).

Lý do đặt khâu tìm cạnh khâu trả lời (nối C36): khoảng 18 / 40 câu dev thiếu đoạn đúng ở context 10. Không cách sửa ở khâu trả lời nào
làm câu trả lời đủ được khi model không thấy fact.

## 6. Giới hạn

- Trần ở §3 tính theo cơ chế từ một lượt tìm kiếm. Hạng dense ở `limit=300` có thể lệch nhẹ khi đổi `limit` (HNSW, `Project_Status.md` §8).
- 40 câu có đoạn đúng do agent gắn. Mỗi nhóm chỉ có 1–9 câu.
- Ước latency của V1 / V3 và ước tiền của V3 **chưa đo** (NOT RUN). Hai số phải đo bằng pilot trước khi ghi vào spec.
- Số tính lại (trần, rủi ro V4): script dùng một lần, chạy trong `uv run`, đọc `b42_per_case.jsonl` (sha `79e4ba43b38e`). Kết quả in
  ra đã chép vào §2–§3; không lưu file mới.
