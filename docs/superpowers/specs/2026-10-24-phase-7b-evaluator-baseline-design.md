# Phase 7B — Evaluator full-corpus + baseline 176 case: Design

**Date:** 2026-10-24 (+07)
**Status:** Approved — User brainstorm D1–D3 với A; User ủy quyền A tự điều phối, tự quyết
chi tiết và dùng chi phí (2026-10-24, trước khi nghỉ). B review thiết kế này trước khi code
(không ai tự duyệt việc của mình).
**Owner:** A (`hue-rag-77`)
**Inputs:** Golden 7A (`docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md`),
contract evaluation trong `guides/full_corpus_rag.md` (metric, rubric 1–5), runtime 7A2
(`session_prompt/Project_Status.md` §4).

## 1. Mục tiêu

Dựng thước đo chính thức cho hệ thống full-corpus và lấy **mốc điểm (baseline)** của
runtime hiện tại trên 176 case Golden. Đồng thời đo **độ tin của thước đo** (judge có
khớp người không, điểm dao động bao nhiêu khi không đổi gì) để Phase 8 biết chênh lệch
nào là thật. Ràng buộc: chi phí thấp — User cho tổng 1 USD cho session (tối đa 1,5 USD),
"không cần dùng hết".

## 2. Quyết định

| # | Quyết định | Ai | Lý do | Cái giá |
|---|---|---|---|---|
| D1 | 7B gồm evaluator đúng contract **và** kiểm độ tin của thước đo (đo nhiễu + chấm tay so sánh) | User | Phase 8 cần biết chênh bao nhiêu là thật | Thêm việc so với chạy một lần |
| D2 | User chấm tay ~20 case; một session Claude chấm đủ 176 case | User | Mốc người là mạnh nhất; judge khác họ model gỡ nghi ngờ tự chấm | ~1–2 giờ của User |
| D3 | **Judge chính là Claude** (session Claude Code), không tốn API | User | Tiết kiệm; khác họ với model sinh | Chấm chậm hơn API, tốn quota Claude Code; phải đo nhiễu judge |
| D4 | Run 2 sinh lại **đủ 176 case** (không chỉ 30) | A (sau khi biết giá) | Nhiễu cả đường đo trên đủ case; thêm ~0,1–0,2 USD | Tiền sinh gấp đôi |
| D5 | Thêm `gpt-6-luna` làm **judge phụ**: chấm Run 1 (176) + chấm lại 30 | A (sau khi biết giá) | Nếu luna khớp User/Claude, Phase 8 có judge tự động, nhanh, rẻ; ~0,1 USD | Thêm một đường gọi API nhỏ |

Giá `gpt-6-luna` (User 2026-10-24): 0,1 USD / 1M token input; 0,5 USD / 1M token output.

D3 **thay** quyết định cũ "evaluation judge là `gpt-6-luna`"
(`docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`): điểm chính thức của
baseline là điểm Claude; điểm luna là judge phụ để so. Generation vẫn là `gpt-6-luna`.

Chi tiết A tự quyết: đường được chấm là đúng đường runtime API; thêm hai tỉ lệ từ chối cho
`out_of_scope`; module evaluator mới, không sửa evaluator Foods cũ; kết quả chi tiết lưu
private trong `data/`.

## 3. Phạm vi

**Làm:** module evaluator full-corpus; prompt judge cố định dùng chung cho Claude và luna;
retrieval eval 176 (local, 0 đồng) cho runtime `dense_bm25_rrf` và thêm `native_hybrid_rrf` để so (C đề xuất, 0 đồng); Run 1 + Run 2 sinh 176 case mỗi run; judge Claude
(Run 1, chấm lại 30, Run 2); judge luna (Run 1, chấm lại 30); User chấm ~20; tổng hợp +
report.

**Không làm:** sửa retrieval, prompt sinh, chunker, corpus, Golden, Qdrant; đặt ngưỡng
"đạt/không đạt" (7A: chưa đặt trước baseline); đổi provider/model; dọn evaluator/notebook
Foods cũ (việc dọn riêng); Phase 8.

## 4. Thiết kế

### 4.1 Luồng mỗi case

```text
Golden case -> retrieval (runtime e5-small + dense_bm25_rrf, top-10)
            -> retrieval metrics (keyword proxy, K=10)
            -> context builder (top-5 whole chunk, như API)
            -> gpt-6-luna sinh câu trả lời + citation (ghi usage token)
            -> ghi một dòng JSONL (private)
```

Dựng component **giống `create_app`** (`backend/api/app.py`): cùng
`build_full_corpus_retrieval_service`, `FullCorpusContextBuilder`,
`OpenAIFullCorpusGenerator.from_environment`, cùng `settings.yaml`. Không dựng pipeline
riêng, không đổi tham số sinh.

### 4.2 Metric

- **Retrieval** (bỏ qua `out_of_scope`, 7A §8): MRR@10, nDCG@10, Keyword Coverage@10 theo
  keyword substring (NFC, không phân biệt hoa/thường) — cùng công thức
  `backend/evaluation/eval.py` `score_retrieval`. Macro-average theo case; breakdown theo
  category. Chạy hai lần để xác nhận tất định.
- **Answer** (mọi case): Accuracy, Completeness, Relevance, số nguyên 1–5, rubric đúng bảng
  trong `guides/full_corpus_rag.md`. Macro-average theo case; breakdown theo category.
  Không composite.
- **Từ chối** (so khớp chữ): tỉ lệ từ chối đúng trên `out_of_scope` (câu trả lời là
  `INSUFFICIENT_ANSWER`); tỉ lệ từ chối nhầm trên case còn lại.
- **Lỗi kỹ thuật** (provider, mạng, timeout): ghi nguyên lỗi; run có lỗi là `incomplete`
  (7A). Chạy lại riêng case lỗi, tính vào giới hạn tiền.
- **Chi phí:** cộng `input_tokens`/`output_tokens` từ usage mỗi lượt gọi, nhân giá §2.

### 4.3 Judge

- Prompt judge cố định, tracked: `backend/evaluation/full_corpus_judge_prompt.md` (rubric,
  quy tắc "chỉ dựa vào câu hỏi, đáp án tham chiếu, câu trả lời; không dùng kiến thức ngoài,
  không đọc corpus", JSON đầu ra `{accuracy, completeness, relevance, feedback}`). Claude
  và luna dùng **cùng** prompt; Phase 8 dùng lại nguyên prompt.
- **Claude (chính):** C chấm (độc lập với B là người dựng pipeline). C dùng sub-agent, mỗi
  sub-agent một lô ≤10 case, chỉ nhận prompt judge + case của lô; mỗi case chấm độc lập.
  Lần chấm lại dùng lô xáo khác. Không cho judge thấy điểm lần trước, điểm User hay tên run.
- **Luna (phụ):** một lượt gọi mỗi case qua OpenAI, cùng model/provider như generation,
  structured output 3 số nguyên + feedback; không thêm tham số sampling.

### 4.4 Tập con chấm lại (30 case) và mẫu User (~20 case)

- A chọn **trước khi chạy Run 1**, ghi chỉ số dòng vào file private: phủ đủ 5 category theo
  tỉ lệ gần Golden, mỗi partition ≥1 case. Mẫu User phủ đủ 5 category.
- **Nhiễu judge** = điểm judge lần 1 so với lần chấm lại trên 30 câu trả lời Run 1 (Claude
  và luna riêng).
- **Nhiễu cả đường** = điểm Claude của 176 case giữa Run 1 và Run 2 (gồm nhiễu sinh + nhiễu
  judge): chênh trung bình theo metric, tỉ lệ case đổi điểm, tỉ lệ case đổi ≥2 điểm.
- **Khớp giữa các nguồn** trên mẫu User: User–Claude, User–luna, Claude–luna (và Claude–luna
  trên đủ 176): tỉ lệ trùng, tỉ lệ lệch ≤1, chênh trung bình có dấu, theo từng metric.
- A tạo file chấm cho User (Markdown private: câu hỏi, đáp án tham chiếu, câu trả lời,
  rubric, ô điểm); User không thấy điểm judge.

Tiêu chí ghi **trước** khi chạy: report đưa đủ các số trên; không đặt ngưỡng đạt/không đạt
ở 7B. Phase 8 dùng chúng để đặt luật "chênh bao nhiêu là thật". Nếu Claude lệch User có hệ
thống (chênh trung bình ≥1 điểm ở một metric), A báo User trước khi coi điểm Claude là
chính thức.

### 4.5 Lưu trữ

```text
backend/evaluation/full_corpus_eval.py          # tracked: retrieval + sinh + judge luna + tổng hợp
backend/evaluation/full_corpus_judge_prompt.md  # tracked: prompt judge cố định
data/evaluation/phase_7b/                       # private: run, judge, mẫu, điểm User
reports/phase_7b_*                              # tracked: chỉ số tổng hợp, không chép nội dung
```

B tự quyết tên file con và cách chia hàm, giữ gọn (một module, hàm có tên rõ; nên chép
hàm metric từ `eval.py` sang để không phụ thuộc evaluator Foods sẽ bị dọn). Test chỉ cho
logic thuần (metric keyword, kiểm từ chối, tổng hợp, tính tiền) với input nhỏ hợp lệ.

## 5. Bước

| Gate | Ai | Việc | Paid (ước, xấu nhất) |
|---|---|---|---|
| 0 | B | Kiểm sức khỏe các Phase trước (việc riêng trong `CURRENT_HANDOFF.md`) | 0 |
| 1 | B | Review thiết kế; viết module + prompt judge + test; retrieval eval 176 ×2 (`dense_bm25_rrf`) + 1 lần `native_hybrid_rrf`; smoke 10 (sinh + judge luna) → báo token thật và dự báo tiền | ~0,02 USD |
| — | A | Review Gate 1; chọn tập 30 + mẫu User; quyết theo dự báo tiền | 0 |
| 2 | B | Run 1 (176) + Run 2 (176) + judge luna Run 1 (176) + chấm lại 30 | ~0,6 USD |
| 3 | C | Claude chấm Run 1 (176), chấm lại 30, Run 2 (176) | 0 API |
| 3 | User | Chấm ~20 case (file A chuẩn bị) | 0 |
| 4 | B | Tổng hợp + implementation report | 0 |
| — | A + C | Review chéo; A trình User đóng Phase | 0 |

Ước lượng xấu nhất dựa trên giới hạn trong `settings.yaml` (sinh ≤~4k input + ≤2k output ≈
0,0014 USD/lượt; judge ≤~2k + ≤1k ≈ 0,0007 USD/lượt); số thật lấy từ smoke.

## 6. Quyền và giới hạn

- **Paid:** chỉ OpenAI `gpt-6-luna` (sinh + judge phụ), đúng `settings.yaml` hiện hành.
  **Giới hạn cứng 7B: 0,6 USD** tính từ usage token. Sau smoke, nếu dự báo Gate 2 vượt
  0,5 USD thì cắt theo thứ tự: bỏ chấm lại luna → Run 2 còn 30 case → bỏ judge luna. Chạm
  0,6 USD thì dừng ngay, báo A. Tổng session (gồm Phase 8) ≤1 USD; không bao giờ vượt 1,5 USD.
- **Dữ liệu ra ngoài:** câu hỏi Golden, 5 chunk ngữ cảnh, đáp án tham chiếu và câu trả lời
  gửi OpenAI — cùng provider runtime Phase 6 đã duyệt. Judge Claude chạy trong Claude Code
  như các session đang đọc dữ liệu private; không thêm provider.
- **Qdrant:** chỉ đọc. **Git:** B, C không commit; A commit/push.
- Chạy bằng `uv run --env-file .env …` từ `backend/` (`Session_Prompt.md` §10).

## 7. Tiêu chí nghiệm thu

1. Evaluator chạy đúng đường runtime (cùng component/config với API); thấy trong diff.
2. Retrieval metrics 176 case (bỏ `out_of_scope`) hai lần giống hệt nhau.
3. Run 1, Run 2 đủ case không lỗi kỹ thuật (hoặc ghi rõ `incomplete` kèm lỗi).
4. Claude chấm đủ; luna chấm đủ phần còn trong phạm vi sau cắt giảm; mọi điểm là số nguyên
   1–5 hợp lệ.
5. User chấm xong mẫu; report có mức khớp giữa các nguồn, nhiễu judge, nhiễu cả đường theo
   từng metric.
6. Report baseline: 6 metric + 2 tỉ lệ từ chối, tổng và theo category; tiền thật ≤0,6 USD;
   ghi giới hạn (Golden do LLM viết, keyword là proxy, judge là LLM, mẫu User nhỏ).
7. Không lộ nội dung private trong file tracked; `git diff --check` sạch.
8. Review chéo `ready_for_user_confirmation`; User đóng.

## 8. Rủi ro và điều kiện dừng

| Rủi ro | Cách giảm / điều kiện dừng |
|---|---|
| Token thật cao hơn ước lượng | Smoke đo trước; cắt giảm theo §6; giới hạn cứng 0,6 USD |
| Quota Claude Code hết giữa chừng | Chấm theo lô, ghi file sau mỗi lô; tiếp tục ở lô chưa có kết quả |
| Judge Claude dùng kiến thức ngoài / đọc corpus | Prompt cấm; sub-agent chỉ nhận dữ liệu của lô; A kiểm ngẫu nhiên feedback |
| Claude lệch User có hệ thống | Dừng coi Claude là chính thức; A trình User phương án |
| Lỗi provider lặp lại (timeout, 429) | Ghi nguyên lỗi; không thêm retry/fallback phòng xa; quá 10% case lỗi thì dừng, báo A |
| Runtime từ chối khởi động (freshness) | Dừng; không build lại index trong 7B |
| Gate 0 phát hiện nền hỏng | Dừng 7B Gate 2; A xem lại với User |

## 9. Liên quan

- Nghiên cứu bên ngoài: `gửi chatgpt/tìm thông tin/phase_7b_rag_evaluation_2026_10_24.md`
  (private, chờ User gửi). Kết quả có thể chỉnh chi tiết §4.4 trước khi tổng hợp; không
  đổi D1–D3 khi chưa hỏi User.
- Phase 8: giả thuyết của C ở `reports/phase_8_candidate_hypotheses_2026_10_24.md`. Lưu ý
  của C: chunk to hơn tự làm Keyword Coverage@10 tăng, nên Phase 8 không so chunker chỉ
  bằng keyword proxy. Phase 8 dùng baseline + ngưỡng nhiễu này; lọc ứng viên bằng
  retrieval metrics free trước, chỉ ứng viên tốt nhất mới chạy sinh + chấm.
