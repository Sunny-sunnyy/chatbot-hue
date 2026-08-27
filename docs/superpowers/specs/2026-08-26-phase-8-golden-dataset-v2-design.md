# Phase 8 Golden Dataset V2 Design

> **Historical — superseded 2026-08-27:** V2 dừng sau ba vòng
> `changes_requested`. Golden Dataset V3 design là canonical Gate 0 hiện hành:
> `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md`.

**Status:** `historical_superseded`

**Purpose:** Xây một golden dataset tiếng Việt mới, rõ ràng và có bằng chứng
trực tiếp cho Phase 8. Dataset mới phục vụ so sánh retrieval và answer quality;
không thay thế hoặc ghi đè baseline Phase 7 gồm 104 case.

## Boundary

- Scope này chỉ gồm curated rebuild, validation, smoke subset và contract
  relevance cho retrieval.
- Không benchmark model, không chạy paid generation/judge, không đổi active
  Qdrant collection và không chuyển production pipeline.
- `knowledge-base-hue/foods/evaluation/tests.jsonl` tiếp tục là baseline Phase 7
  và phải giữ nguyên.
- Bộ câu hỏi từ chối/không đủ thông tin là một dataset riêng trong tương lai;
  không trộn vào benchmark chính.

## Curated rebuild

`golden_v2` được xây lại có chọn lọc, không sửa nối tiếp bộ 104 case cũ:

1. Đọc trực tiếp toàn bộ corpus trong bốn nhóm nguồn đã khóa.
2. Dùng 104 case cũ như danh sách ứng viên.
3. Tái sử dụng nguyên vẹn case cũ khi case đó đạt toàn bộ tiêu chuẩn mới.
4. Sửa hoặc thay case sai, mơ hồ, gượng ép, thiếu evidence hoặc sai category.
5. Tạo case mới chỉ để lấp coverage có nhu cầu thật và có nguồn đủ mạnh.
6. Audit lần hai mọi case mới/sửa và mọi case từng có finding.

Không bắt buộc giữ ID cũ. Dataset mới có đúng 100 case với ID tuần tự
`foods-0001` đến `foods-0100`.

## Question quality contract

- Chỉ giữ câu hỏi trả lời được từ curated corpus.
- Câu hỏi phải tự nhiên, rõ nghĩa, giống nhu cầu thực tế của người dùng.
- Cho phép direct fact và tổng hợp nhẹ; không dùng câu mẹo, trivia vụn vặt,
  suy diễn xa, cách nói cố tình gây nhiễu hoặc phép tính đánh đố.
- Không dùng câu chứa `hiện nay`, `mới nhất` hoặc ngụ ý dữ liệu thời gian thực.
- Giá, giờ mở cửa và địa chỉ được phép dùng khi corpus ghi rõ; benchmark xem
  curated corpus là closed-world source of truth tại thời điểm tạo dataset.
- Nếu các nguồn mâu thuẫn, không tự chọn một giá trị. Tạm loại case và báo user
  để sửa corpus hoặc xác nhận nguồn đúng trước.
- Nếu corpus không đủ case chất lượng cho quota, implementer phải báo số thiếu
  và loại thông tin cần bổ sung; không tạo case gượng ép để đủ số.

## Category distribution

| Category | Case |
|---|---:|
| `direct_fact` | 18 |
| `temporal` | 10 |
| `comparative` | 10 |
| `numerical` | 8 |
| `relationship` | 12 |
| `spanning` | 12 |
| `holistic` | 8 |
| `food_knowledge` | 12 |
| `guide_planning` | 10 |
| **Tổng** | **100** |

`numerical` chỉ dùng giá, số lượng hoặc định lượng được nguồn nêu rõ. Không đổi
giờ mở cửa thành `numerical`; loại đó vẫn là `temporal`.

## Source coverage

Dataset phải bao phủ:

| Primary authoring source | Target |
|---|---:|
| `foods/restaurants/*.md` | 40 |
| `foods/cafes/*.md` | 20 |
| `foods/local_specialties/*.md` | 20 |
| `foods/food-guides.md` | 20 |

Một case có thể có nhiều evidence source khi câu hỏi thực sự cần tổng hợp.
Source targets là authoring targets; validator báo coverage theo số case có ít
nhất một evidence source thuộc từng family. Không thêm `source_family` vào
schema chỉ để đếm quota.

Ma trận tuyển chọn dưới đây giúp implementer đạt đồng thời category và source
coverage mà không tự phân bổ:

| Source | direct | temporal | comparative | numerical | relationship | spanning | holistic | food knowledge | guide planning | Tổng |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| restaurants | 10 | 6 | 4 | 4 | 7 | 4 | 2 | 3 | 0 | 40 |
| cafes | 5 | 3 | 2 | 2 | 4 | 2 | 1 | 1 | 0 | 20 |
| local specialties | 3 | 1 | 4 | 2 | 1 | 3 | 1 | 5 | 0 | 20 |
| food guides | 0 | 0 | 0 | 0 | 0 | 3 | 4 | 3 | 10 | 20 |
| **Tổng** | **18** | **10** | **10** | **8** | **12** | **12** | **8** | **12** | **10** | **100** |

Ma trận là quality-first target. Nếu một ô không có câu hỏi tự nhiên và grounded,
implementer dừng tại reviewer checkpoint để user duyệt bổ sung corpus hoặc tái
phân bổ; không tự chuyển quota.

## Minimal schema

Mỗi JSONL row có đúng sáu field:

```json
{
  "case_id": "foods-0001",
  "question": "DeChill nằm ở đâu?",
  "keywords": ["DeChill", "Huyền Trân Công Chúa"],
  "reference_answer": "DeChill nằm tại 102 Huyền Trân Công Chúa, phường Thủy Xuân, Thành phố Huế.",
  "category": "direct_fact",
  "evidence": {
    "foods/cafes/dechill.md": ["Thông tin"]
  }
}
```

Source trong `evidence` là identifier repo-relative đã có trong chunk metadata,
không phải absolute filesystem path. Không thêm UUID, run ID, timestamp, version
registry, generated labels hoặc metadata kỹ thuật khác.

## Field rules

### `case_id`

- Stable, unique và tuần tự từ `foods-0001` đến `foods-0100`.
- Dùng để join case với smoke subset và kết quả giữa nhiều configuration.
- Không suy ra category hoặc source từ ID.

### `question`

- Unique trong `golden_v2`.
- Ngắn, tự nhiên và chỉ có một cách hiểu hợp lý trong phạm vi corpus.
- Không cần khác mọi câu trong bộ Phase 7; case tốt được phép tái sử dụng.

### `keywords`

- Có 2-4 keyword/cụm từ cụ thể.
- Mỗi keyword xuất hiện trong `reference_answer` và ít nhất một evidence section.
- Ưu tiên tên món, tên quán, địa điểm, con số hoặc đặc điểm phân biệt.
- Không dùng từ quá chung như `Huế`, `quán`, `món`, `ngon`, `ăn`, `gì`, `nào`.
- Keywords hỗ trợ Phase 7/diagnostic; không phải relevance ground truth Phase 8.

### `reference_answer`

- Ngắn gọn, đủ dữ kiện cốt lõi và được evidence hỗ trợ trực tiếp.
- Không yêu cầu generated answer exact-match theo chữ hoặc thứ tự trình bày.
- Với open-ended categories, đây là một đáp án mẫu tốt, không phải đáp án duy
  nhất. Alternative answer vẫn đúng nếu thỏa câu hỏi và grounded trong evidence.

### `category`

- Phải thuộc đúng chín category đã khóa.
- Chọn theo năng lực chính mà câu hỏi kiểm tra, không chọn theo từ khóa bề mặt.

### `evidence`

- JSON object không rỗng: mỗi key là source identifier đang tồn tại; value là
  danh sách H2 section không rỗng.
- Liệt kê mọi source/section trong curated corpus có thể cung cấp bằng chứng hợp
  lệ, không chỉ section đầu tiên người viết case nhìn thấy.
- Không lưu chunk ID vì chunk có thể khác giữa các model/index configuration.

## Deterministic retrieval relevance

Phase 8 dùng binary relevance:

```text
relevant(document, case) =
  document.metadata.source có trong case.evidence
  AND document.metadata.section có trong case.evidence[source]
```

- Đúng source nhưng sai section không được tính relevant.
- Không dùng keyword substring hoặc LLM judge làm relevance ground truth.
- Không precompute chunk IDs.
- Rule áp dụng giống nhau cho mọi isolated index đại diện cùng canonical corpus.

## Smoke subset

`golden_v2_smoke.jsonl` chứa đúng 20 row được copy nguyên vẹn từ
`golden_v2.jsonl`:

- đủ chín category;
- chạm đủ restaurants, cafes, local specialties và food guides;
- không có question/reference/evidence riêng;
- chỉ dùng để kiểm tra pipeline và integration;
- không được dùng làm bằng chứng chọn model cuối cùng.

Mọi kết luận benchmark và winner decision phải chạy trên đủ 100 case.

## Files

```text
knowledge-base-hue/foods/evaluation/tests.jsonl              # Phase 7, unchanged
knowledge-base-hue/foods/evaluation/golden_v2.jsonl          # 100-case benchmark
knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl    # exact 20-case subset
```

## Acceptance gates

1. Cả hai file parse được từng dòng JSON và chỉ có sáu field đã khóa.
2. Full dataset có đúng 100 ID tuần tự, question unique và exact category counts.
3. Keywords đạt chuẩn 2-4 và xuất hiện trong reference + evidence text.
4. Mọi evidence source/section tồn tại trong bốn nhóm corpus đã khóa.
5. Smoke có đúng 20 row, mỗi row deep-equal row cùng ID trong full dataset, đủ
   chín category và bốn source families.
6. Reviewer đối chiếu trực tiếp source/section cho toàn bộ 100 case; case mới,
   case sửa và finding cũ nhận lượt review thứ hai.
7. Real dense retrieval trên smoke set xác nhận runtime trả metadata
   `source`/`section` dùng được với binary relevance rule. Retrieval miss được
   báo như baseline evidence, không được che bằng fake result hoặc sửa gold để
   chiều theo model.
8. Không dùng fake data, mocked provider output hoặc fabricated result làm
   implementation hay completion evidence.

## Non-goals

- Không xây semantic validator, LLM auto-labeler, annotation UI, audit package,
  dataset registry, checksum manifest hoặc versioning framework.
- Không thay Phase 7 keyword metrics trong scope này.
- Không tạo refusal dataset trong scope này.
- Không chạy model benchmark, generation hoặc judge trong scope này.
