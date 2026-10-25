---
name: run-experiment
description: Dùng trước khi thử bất kỳ thay đổi nào ở discovery / chia đoạn / embedding / BM25 / Qdrant / tìm kiếm / rerank / context / prompt / model sinh / bộ chấm của hue_rag, hoặc khi so sánh phương án, đo chất lượng, quyết một thay đổi có vào chatbot hay không — kể cả khi quay lại Phase cũ. Các bước: tiêu chí ghi trước (sàn / mức tụt cho phép / chỉ số quyết), cỡ mẫu trước khi chạy, mốc (baseline; khâu có LLM đo nhiễu A/A), kiểm người chấm, đổi một thứ, đo theo cặp và theo tầng, luật giữ/gỡ vượt nhiễu, xác nhận trên nhóm kiểm, giữ hồ sơ cả phương án bị bỏ, trần tiền/thời gian. Không dùng cho sửa lỗi nhỏ đã rõ nguyên nhân (dùng practical-project-coding).
---

# Thí nghiệm có kỷ luật — hue_rag (A, B, C)

User (2026-10-24): **luôn thử, đánh giá, so với baseline rồi mới chọn**, kể cả khi quay lại Phase trước. Luật
gốc thắng skill này: `session_prompt/Session_Prompt.md` §5 (dữ liệu, câu kín), §6, §8; `WORKFLOW.md` §3.5, §5.
Code theo `practical-project-coding` ("Ranh giới theo khâu pipeline": gọi code production qua tham số).

## 1. Trước khi đo — ghi vào report của đợt (giờ lấy bằng `date`)

Kế hoạch có mục **"Căn cứ để review"** và được một session khác review trước khi A duyệt sha (`WORKFLOW.md` §9 mục 1).


1. **Lớp bài toán**, không phải một câu: "dòng bảng giá bị tách nên tìm không ra", không phải "câu số 81 sai".
2. **Một thay đổi mỗi biến thể** (H1, H1b…); ghi giả định của nó và **kiểm giả định bằng máy trước khi code**
   (ví dụ đếm xem đúng là có bao nhiêu bảng bị tách vì tokenizer cũ).
3. **Tiêu chí ghi trước khi thấy số** (khuôn YAML bên dưới), theo ba lớp:
   - **sàn** — không bao giờ được vi phạm (0 câu mất đoạn đúng khỏi context, từ chối đúng `out_of_scope` giữ
     nguyên);
   - **mức tụt cho phép** của từng chỉ số còn lại, ghi bằng **số câu** khi bộ nhỏ (lỗi citation, từ chối nhầm,
     latency p95, USD/câu tính đầu–cuối gồm cả rerank + sinh);
   - **1–2 chỉ số quyết** (phải tốt lên vượt nhiễu) tách khỏi **chỉ số theo dõi** (chỉ báo, không quyết).
   Mỗi chỉ số định nghĩa chính xác: hàm nào tính, đếm gì, không đếm gì, trên tập nào, n bao nhiêu. Không đổi
   tiêu chí sau khi thấy số.
4. **Hợp đồng kiểm:** ai review chéo; người làm nộp bằng chứng gì; người kiểm tự chạy lại phần nào.
5. **Trần:** tiền API ghi trong việc (ước USD trước, User nhạy chi phí), thời gian, một việc nặng GPU một lúc
   (GTX 1650 4 GB: một model rerank/embedding một lúc).
6. **Cỡ mẫu trước khi chạy:** đếm số câu thật sự có thể đổi kết quả (ví dụ câu có đoạn đúng ngoài top-5) và
   số câu phải thắng để CI 95% > 0 (kể cả Holm khi nhiều biến thể). Không đủ câu ⇒ ghi trước "kết quả có thể
   chỉ là chưa rõ", mở rộng bộ hoặc đổi câu hỏi thí nghiệm, đừng chạy rồi mới thấy (2026-10-25: G4 chỉ có
   khoảng 6–8 câu có thể đổi).

```yaml
experiment_id: <gate>_<tên ngắn>
baseline: <cấu hình đang chạy, commit>
changed_variable: <đúng một thứ>
unchanged: [corpus, chunker, embedding, retrieval, prompt, model, judge]   # trừ thứ đổi
data: {split: knowledge-base-hue/evaluation/phase_8_1/split.json, group: dev, n: null}   # dev chọn, test xác nhận
metrics:   # mỗi dòng: tên, hàm tính, chiều tốt, vai trò, ngưỡng, nhiễu (nguồn số)
  - {name: <đoạn đúng trong 5 đoạn>, fn: <module.hàm>, better: up, role: decide, noise: 0 (tất định)}
  - {name: <out_of_scope từ chối đúng>, better: up, role: floor, floor: <18/18>}
  - {name: <lỗi citation>, better: down, role: tolerance, max_worse: <+k câu>, noise: <từ A/A>}
  - {name: <latency p95 CPU>, better: down, role: watch}
result: {paired_delta: null, ci95: null, wins_ties_losses: null}
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ
```

## 2. Bộ câu và nhãn

- **Chọn trên nhóm thử `dev` (120), xác nhận trên nhóm kiểm `test` (56)**, file chia
  `knowledge-base-hue/evaluation/phase_8_1/split.json`. Câu kín: `Session_Prompt.md` §5.
- Nhóm đã dùng để quyết thì từ đó chỉ là bộ hồi quy. Ghi rõ trong report bộ nào **đã thấy**, bộ nào **kín**.
- Có **đoạn đúng** (vị trí trong file nguồn) thì đo theo đoạn đúng; keyword chỉ là metric phụ, vì đoạn to tự
  làm keyword coverage tăng. So các cách chia đoạn với **cùng ngân sách token context**.
- Thử nhanh/pilot: ≤ 20 câu chọn bằng máy, seed ghi trước; chạy đủ nhóm khi đáng. Số pilot không gộp vào số
  của cả bộ.
- **Kiểm người chấm** trước khi chấm hàng loạt bằng judge / rubric / model id mới (kể cả khi Claude Code tự
  nâng model): cho chấm 4 phiếu đã biết mức — đáp án tham chiếu của chính câu; đáp án của câu khác; câu từ
  chối trên câu có trong kho; đúng ý nhưng sai citation. Lệch thứ tự mong đợi ⇒ sửa thước trước.
- Câu có **số** (giá, giờ, năm, khoảng cách) chấm bằng code khi được: giá trị + đơn vị + dung sai ghi trước;
  Claude chỉ chấm phần lời. Judge hiện tại không chấm citation và không trừ chi tiết thêm
  (`backend/evaluation/full_corpus_judge_prompt.md`) ⇒ độ bám nguồn phải đo bằng code riêng.
- Bảng số trong report do script in ra, không gõ lại tay; n = 0 cho một lớp câu ⇒ `NOT RUN`, không ghi "đạt".

## 3. Đo

1. **Mốc trước:** chạy lại baseline bằng code HEAD, cùng bộ, cùng cách đo. Retrieval baseline phải giống
   từng byte mốc đã lưu. Khác thì dừng: chạy lại baseline 2 lần bằng HEAD. Nếu hai lượt giống nhau mà vẫn
   khác mốc cũ thì tìm nguyên nhân (skill debugging). Nếu chính nó dao động giữa các lượt thì ghi mức dao
   động, và chỉ dùng lượt mới làm mốc sau khi A duyệt. Không so biến thể với một mốc không tái lập được.
   **Khâu có LLM** (sinh, judge, rerank `gpt-6-luna`): **nhiễu** = chênh theo từng câu giữa hai lượt baseline
   không đổi gì — dùng lại A/A sẵn có khi đầu vào không đổi (7B Run 1↔2: 16/176 câu đổi điểm, lỗi citation 4→6),
   chưa có thì chạy 2 lượt (ước USD trước); ghi **trước** khi đo biến thể. Khâu tất định không cần A/A.
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
- **Luật giữ / gỡ** — đủ cả ba mới là "tốt hơn": (1) không vi phạm sàn; (2) không chỉ số nào xấu quá mức tụt
  cho phép (đã trừ nhiễu); (3) ít nhất một chỉ số quyết tốt lên **vượt nhiễu và CI 95% > 0**. Câu chỉ đổi ở
  một lượt không tính. Đây là ngưỡng thực dụng, không viết "đã chứng minh". Chỉ số theo dõi tụt mạnh ⇒ báo
  dù luật nói giữ.
- "Tốt hơn" chỉ đề xuất vào chatbot khi **đã xác nhận trên nhóm kiểm**; đưa vào runtime là việc riêng, User duyệt.
- **3 vòng sửa cùng một biến thể không đạt ⇒ dừng**, ghi giới hạn, báo A/User; không vá cơ chế bảo vệ cơ chế.
  Hết trần tiền / thời gian ⇒ dừng, báo A.

## 5. Hồ sơ — kể cả phương án bị bỏ

- Phương án không dùng vẫn ghi đủ số đo, điều kiện, chi phí, latency; mục chưa đo ghi `NOT RUN` + lý do.
  Ghi vào report của đợt (`report_agent/<đợt>/`) và `BAO_CAO_<KHÂU>.md` (checklist thang 5 mức: "Đã thử,
  chưa áp dụng"), để không đề xuất lại mà không có lý do mới.
- Kết mỗi thí nghiệm bằng **3–5 dòng lời thường cho User**: thử gì, vì sao, kết quả (số kèm ý nghĩa), quyết
  định, giới hạn. Report tracked theo `Session_Prompt.md` §5 (repo public).
