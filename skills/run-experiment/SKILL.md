---
name: run-experiment
description: Dùng trước khi thử bất kỳ thay đổi nào ở discovery / chia đoạn / embedding / BM25 / Qdrant / tìm kiếm / rerank / context / prompt / model sinh / bộ chấm của hue_rag, hoặc khi so sánh phương án, đo chất lượng, quyết một thay đổi có vào chatbot hay không — kể cả khi quay lại Phase cũ. Các bước: tiêu chí ghi trước, mốc (baseline), đổi một thứ, đo theo cặp và theo tầng, xác nhận trên nhóm kiểm, giữ hồ sơ cả phương án bị bỏ, trần tiền/thời gian. Không dùng cho sửa lỗi nhỏ đã rõ nguyên nhân (dùng practical-project-coding).
---

# Thí nghiệm có kỷ luật — hue_rag (A, B, C)

Nguyên tắc thường trực của User (2026-10-24): **luôn thử, đánh giá, so với baseline rồi mới chọn**, không
chọn một giải pháp rồi làm luôn, kể cả khi quay lại các Phase trước. Luật gốc thắng skill này khi khác nhau:
`session_prompt/Session_Prompt.md` §6 (bằng chứng), §8 (test), `session_prompt/WORKFLOW.md` §3.5 (đo
trước–sau), §5 (review chéo). Code dùng skill `practical-project-coding`, đặc biệt mục "Ranh giới theo khâu
pipeline": thí nghiệm gọi code production qua tham số, không dựng đường thứ hai.

## 1. Trước khi đo — ghi vào report của đợt (giờ lấy bằng `date`)

1. **Lớp bài toán**, không phải một câu: "dòng bảng giá bị tách nên tìm không ra", không phải "câu số 81 sai".
2. **Một thay đổi mỗi biến thể** (H1, H1b…); ghi giả định của nó và **kiểm giả định bằng máy trước khi code**
   (ví dụ đếm xem đúng là có bao nhiêu bảng bị tách vì tokenizer cũ).
3. **Tiêu chí ghi trước khi thấy số** (khuôn YAML bên dưới): metric chính, metric phụ, và cả tiêu chí **không
   được tụt**: 0 câu mất đoạn đúng khỏi context, từ chối đúng `out_of_scope` giữ nguyên, lỗi citation không
   tăng, latency, tiền. Không đổi tiêu chí sau khi thấy số.
4. **Hợp đồng kiểm:** ai review chéo; người làm nộp bằng chứng gì; người kiểm tự chạy lại phần nào.
5. **Trần:** tiền API ghi trong việc (ước USD trước, User nhạy chi phí), thời gian, một việc nặng GPU một lúc
   (GTX 1650 4 GB: một model rerank/embedding một lúc).

```yaml
experiment_id: <gate>_<tên ngắn>
baseline: <cấu hình đang chạy, commit>
changed_variable: <đúng một thứ>
unchanged: [corpus, chunker, embedding, retrieval, prompt, model, judge]   # trừ thứ đổi
data: {split: knowledge-base-hue/evaluation/phase_8_1/split.json, group: dev}   # dev để chọn, test để xác nhận
primary_metric: <ví dụ đoạn đúng trong 5 đoạn đưa model>
guardrails: [<0 câu mất đoạn đúng>, <OOS 18/18>, <latency p95 ≤ …>, <USD ≤ …>]
result: {paired_delta: null, ci95: null, wins_ties_losses: null}
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ
```

## 2. Bộ câu và nhãn

- **Chọn trên nhóm thử `dev` (120), xác nhận trên nhóm kiểm `test` (56)**, file chia
  `knowledge-base-hue/evaluation/phase_8_1/split.json`. **Câu kín** (`phase_8_1/sealed*.jsonl`) chỉ mở ở mốc
  cuối do User quyết; người điều phối không đọc nội dung câu kín.
- Nhóm đã dùng để quyết thì từ đó chỉ là bộ hồi quy. Ghi rõ trong report bộ nào **đã thấy**, bộ nào **kín**.
- Có **đoạn đúng** (vị trí trong file nguồn) thì đo theo đoạn đúng; keyword chỉ là metric phụ, vì đoạn to tự
  làm keyword coverage tăng. So các cách chia đoạn với **cùng ngân sách token context**.
- Thử nhanh/pilot: ≤ 20 câu chọn bằng máy, seed ghi trước; chạy đủ nhóm khi đáng.

## 3. Đo

1. **Mốc trước:** chạy lại baseline bằng code HEAD, cùng bộ, cùng cách đo. Retrieval baseline phải giống
   từng byte mốc đã lưu. Khác thì dừng: chạy lại baseline 2 lần bằng HEAD. Nếu hai lượt giống nhau mà vẫn
   khác mốc cũ thì tìm nguyên nhân (skill debugging). Nếu chính nó dao động giữa các lượt thì ghi mức dao
   động, và chỉ dùng lượt mới làm mốc sau khi A duyệt. Không so biến thể với một mốc không tái lập được.
2. **Đổi một thứ**, đo lại đúng đầu vào đó. Mỗi biến thể index có collection `hue_81_*` (hoặc tiền tố của
   đợt) **và build record + sparse state riêng**; không bao giờ ghi vào collection runtime.
3. **Theo cặp:** `full_corpus_eval compare` (paired bootstrap, CI 95%, thắng/hòa/thua, theo loại câu; Holm
   khi >1 biến thể "thắng"). "Không khác" = CI chứa 0.
4. **Theo tầng** khi lỗi có thể ở nhiều chỗ: có trong kho → vào pool ứng viên → top-10 → 5 đoạn đưa model →
   model dùng → trích đúng. Biết tầng hỏng rồi mới sửa đúng tầng.
5. **Chạy thật.** Không mock, không kết quả giả, không giá trị mong đợi làm PASS. Được phát lại câu trả lời
   `gpt-6-luna` đã ghi thật để đo các khâu *sau* bước sinh (ví dụ chính sách validator citation). Không dùng
   lượt phát lại làm bằng chứng cho thay đổi ở chính bước sinh (prompt, context, reasoning effort).
6. **Judge:** Claude (sub-agent), ghi model id; baseline và biến thể chấm **cùng model judge**; đổi judge thì
   chấm lại baseline.
7. Lỗi provider, mạng hay GPU là kết quả quan sát được. Ghi lại, không che bằng fallback.

## 4. Kết luận

- **Tốt hơn / không đổi / kém hơn / chưa rõ** theo tiêu chí đã ghi. Báo cả metric tụt (ví dụ MRR tăng nhưng
  từ chối đúng giảm).
- "Tốt hơn" chỉ đề xuất vào chatbot khi **đã xác nhận trên nhóm kiểm**. Đưa vào runtime là việc riêng (spec
  hoặc Phase sau), cần User duyệt.
- **3 vòng sửa cùng một biến thể không đạt ⇒ dừng**, ghi giới hạn, báo A/User. Không vá thêm cơ chế để bảo
  vệ cơ chế.
- Hết trần tiền hoặc thời gian ⇒ dừng, báo A.

## 5. Hồ sơ — kể cả phương án bị bỏ

- Phương án không dùng vẫn ghi đủ số đo, điều kiện, chi phí, latency; mục chưa đo ghi `NOT RUN` + lý do.
  Ghi vào report của đợt (`report_agent/<đợt>/`) và `BAO_CAO_<KHÂU>.md` (checklist thang 5 mức: "Đã thử,
  chưa áp dụng"), để không đề xuất lại mà không có lý do mới.
- Kết mỗi thí nghiệm bằng **3–5 dòng lời thường cho User**: thử gì, vì sao, kết quả (số kèm ý nghĩa), quyết
  định, giới hạn.
- Repo công khai: report tracked không chép corpus, câu Golden/câu kín, payload, hay số đo/đường dẫn của dự
  án khác (ghi chú private ở `data/`).
