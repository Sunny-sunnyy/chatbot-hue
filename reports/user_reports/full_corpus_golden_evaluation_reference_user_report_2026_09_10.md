# Báo cáo User — Khảo sát reference Golden / Evaluation toàn corpus

**Ngày:** 2026-09-10

**Trạng thái:** Hoàn tất — User xác nhận ngày 2026-09-10

**Phạm vi:** khảo sát các reference do User cung cấp để rút evidence thiết kế
Golden/evidence/evaluation cho Huế

## 1. Kết quả User nhận được

Implementer đã hoàn tất báo cáo khảo sát reference và ba lượt correction.
Reviewer đã kiểm độc lập correction cuối cùng theo Review Contract. Các findings
R1–R4 đều đã đóng; không còn finding kỹ thuật trong phạm vi khảo sát.

Báo cáo hiện phân biệt đúng hành vi retrieval metrics trong code reference,
giới hạn chất lượng ground truth, mức attribution của tài liệu khóa học, schema
thật của Foods V3 và ranh giới giữa evidence quan sát được với đề xuất cho Huế.

## 2. Bài học thiết kế đã đủ evidence

- Không mặc định một `reference_answer` có text là đáp án đúng hoặc đầy đủ; mỗi
  câu hỏi, đáp án và bằng chứng cần được audit trước khi vào Golden.
- Retrieval relevance phải dựa trên evidence thật và cutoff được định nghĩa rõ;
  không dùng keyword matching như ground truth canonical.
- nDCG/IDCG chỉ có ý nghĩa theo relevance judgments đã biết; implementation
  reference không biết các relevant documents trong corpus nhưng ngoài kết quả
  retrieval đang xét.
- LLM judge cần rubric, prompt, model/version và điều kiện chạy được chốt trong
  spec; seed và temperature không bảo đảm API hoàn toàn tất định.
- Các ca negative, partial evidence, alternative evidence và mâu thuẫn nguồn cần
  được biểu diễn có chủ đích trong Golden của Huế.

## 3. Các quyết định User đã chốt và được giữ nguyên

- **Evidence C:** mỗi expected claim gắn với `evidence_groups` chứa exact source
  spans `{source, heading_path, start, end, text}` trên nguồn chuẩn hóa LF;
  chunk IDs được phân giải động theo candidate chunking khi evaluation.
- **Một canonical file đích:** soạn và review theo partition trước, rồi merge
  thành một full-corpus JSONL duy nhất; official evaluator chỉ dùng file đã merge
  và smoke check bảo đảm merge tương đương các partition.
- **P7:** bảy partition gồm `foods`, `heritages`, `festivals`,
  `performing_arts`, `travel_places`, `travel_services`, `travel_tickets`.
- Foods V3 lịch sử được giữ nguyên; 45 records được copy và enrich trong Golden
  mới, không sửa file lịch sử tại chỗ.

## 4. Evidence để kiểm tra

- Báo cáo khảo sát:
  `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`
- Review chi tiết và closure contract:
  `reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`
  §§11–12
- Canonical design decisions:
  `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`

User không cần chạy lại code hoặc kỹ thuật để xác nhận kết quả khảo sát.

## 5. Giới hạn và bước kế tiếp

Khảo sát không chứng minh chất lượng của toàn bộ 150 reference records và không
phải benchmark của Huế. Nó chưa chốt full Golden schema, identifiers, paths,
case-type representation, validation rules, quotas, split, metrics, thresholds
hoặc exact judge rubric/prompt.

User đã xác nhận và đóng khảo sát reference ngày 2026-09-10. Việc xác nhận chỉ
áp dụng cho khảo sát này; written spec và implementation plan vẫn chưa approved.
Reviewer tiếp tục hoàn thiện thiết kế Golden/evidence/evaluation từ các quyết
định C, một canonical file đích và P7.
