# Phase 7A — Golden full-corpus: Written Spec

**Date:** 2026-10-23 (+07)
**Status:** Approved by User 2026-10-23
**Owner:** Reviewer (Claude Opus 5.5, `hue-rag-66`)
**Design approved by User:** 2026-10-23 (brainstorming trong phiên Reviewer)
**Reference survey:** `reports/phase_7a_golden_reference_rag_old_0_survey_2026_10_23.md`
**Implementation authorization:** chỉ qua `CURRENT_HANDOFF.md`; plan User-approved 2026-10-23

## 1. Mục tiêu

Tạo một bộ câu hỏi Golden chuẩn cho toàn bộ corpus Hue (5 domain, 7 partition),
dùng cho official evaluation ở Phase 7B và benchmark ở Phase 8. Bộ câu hỏi phải
giống câu người thật hỏi chatbot, có đáp án khách quan kiểm chứng được trong
curated Markdown, và đo đúng các hành vi Phase 6 đã cam kết.

Phase 7A chỉ tạo dữ liệu Golden và một script kiểm tra không tốn phí. Không viết
evaluator, không gọi API có phí, không sửa corpus, retrieval hay generation.

## 2. Quyết định User ngày 2026-10-23 (supersede quyết định thời Codex)

| Chủ đề | Quyết định cũ | Quyết định mới |
|---|---|---|
| Câu Foods V3 | Copy, reclassify, review | Viết mới toàn bộ; V2/V3 giữ làm lịch sử, không copy |
| Người duyệt | User và Reviewer đọc từng case | Reviewer đối chiếu từng case với `.md`; User đọc mẫu 10–15 case mỗi partition cùng mọi case Reviewer đánh dấu |
| Thứ tự | 7 partition tuần tự, mỗi partition closure riêng | Pilot 1 partition, chốt hướng dẫn viết, rồi 6 partition song song |
| Category | 7 nhãn theo `rag_old_0` | 5 nhãn (§4) |
| Số lượng | Không quota, planning 150–200 | Khoảng 175, tỷ lệ mềm ±20% (§5) |
| Keywords | Nguyên văn, được reference hỗ trợ | Thêm: ≥1 keyword mang đáp án, không có trong câu hỏi (§3) |
| Không trả lời được | Không có | Thêm `out_of_scope` khoảng 5–10% |
| Dev/test | Không chia | Giữ không chia; Phase 8 không tune theo từng case (§8) |
| Merge | Concat rồi shuffle seed 42 | Concat theo thứ tự partition cố định, không shuffle |

Các quyết định còn hiệu lực: schema chính thức 4 field; không `case_id`,
claims, evidence spans hay chunk ID trong file chính thức; một canonical JSONL
cộng smoke 10 dòng deep-equal; smoke không thay full run; Foods V2/V3 không bị
sửa; Golden là dữ liệu private.

## 3. Schema

File chính thức: mỗi dòng là một JSON object có đúng 4 field.

```json
{"question": "...", "keywords": ["..."], "reference_answer": "...", "category": "direct_fact"}
```

- `question`: một câu hỏi tiếng Việt, một lượt, độc lập, không cần ngữ cảnh hội
  thoại trước.
- `keywords`: list string. Mỗi keyword xuất hiện nguyên văn (so khớp substring
  sau chuẩn hóa Unicode NFC, có phân biệt dấu) trong ít nhất một file curated
  Markdown của corpus. Bắt buộc có ít nhất một keyword **mang đáp án**: không
  xuất hiện trong `question` nhưng xuất hiện trong `reference_answer`. Được phép
  thêm tên thực thể trung tâm. Không dùng từ chung chung ("giá", "Huế", "năm").
  Không có số lượng keyword bắt buộc.
- `reference_answer`: câu trả lời ngắn, đủ ý, giọng tự nhiên, chỉ chứa thông tin
  có trong corpus. Câu `conditional` phải nêu đủ điều kiện và ngoại lệ liên quan.
- `category`: một trong 5 nhãn ở §4.
- Ngoại lệ `out_of_scope`: `keywords` là `[]`, `reference_answer` đúng nguyên văn
  `INSUFFICIENT_ANSWER` trong `backend/llm/full_corpus_prompt.py`:
  `Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.`

File authoring có thêm hai field, bị loại khi merge:

- `partition`: một trong `foods`, `heritages`, `festivals`, `performing_arts`,
  `travel_places`, `travel_services`, `travel_tickets`.
- `sources`: list đường dẫn tương đối (trong `knowledge-base-hue/`) của file
  `.md` chứa đáp án, để Reviewer đối chiếu. Với `out_of_scope` là `[]`.

## 4. Category

| Nhãn | Định nghĩa | Ví dụ dạng câu |
|---|---|---|
| `direct_fact` | Một dữ kiện nằm trong một đoạn: giá, năm, địa chỉ, người xây, giờ mở cửa | "Lăng Tự Đức được xây dưới triều vua nào?" |
| `multi_source` | Phải ghép thông tin từ ≥2 đoạn hoặc ≥2 tài liệu khác nhau | "Những lễ hội nào ở Huế được tổ chức vào tháng Giêng âm lịch?" |
| `comparative` | So sánh hai hoặc nhiều thực thể theo một tiêu chí có trong corpus | "Vé lẻ Đại Nội và vé lẻ lăng Khải Định, cái nào đắt hơn?" |
| `conditional` | Đáp án phụ thuộc điều kiện hoặc có ngoại lệ: miễn giảm, giờ theo mùa, quy định | "Trẻ em dưới 7 tuổi vào Đại Nội có phải mua vé không?" |
| `out_of_scope` | Chắc chắn không có trong corpus, thường gần domain (nơi khác, chủ đề khác) | "Giá vé vào Văn Miếu Hà Nội là bao nhiêu?" |

Mỗi case đúng một nhãn, gán theo thao tác chính mà câu hỏi đòi hỏi. Ví dụ trong
bảng chỉ minh họa dạng câu, không phải case đã kiểm chứng.

## 5. Quy mô và phân bố (tỷ lệ mềm)

Theo category, cho phép lệch ±20%:

| `direct_fact` | `multi_source` | `conditional` | `comparative` | `out_of_scope` | Tổng |
|---:|---:|---:|---:|---:|---:|
| ~70 | ~35 | ~30 | ~25 | ~15 | ~175 |

Theo partition (dự kiến, tính cả khoảng 2 case `out_of_scope` gần domain mỗi
partition):

| foods | heritages | festivals | performing_arts | travel_places | travel_services | travel_tickets |
|---:|---:|---:|---:|---:|---:|---:|
| ~37 | ~37 | ~27 | ~17 | ~32 | ~12 | ~13 |

Ưu tiên bao phủ những câu có đáp án nằm trong bảng (giá vé, giờ mở cửa, lịch).
Đây là điểm yếu retrieval đã quan sát thật ở Phase 6 (F2). Không ép đủ số nếu
partition không cho ra câu tự nhiên; ghi lý do trong report.

## 6. Quy tắc viết câu hỏi

1. Người viết phải đọc các file `.md` liên quan trước khi viết; mọi đáp án phải
   kiểm chứng được trong `sources`.
2. Chỉ dùng câu có **một đáp án khách quan**. Không dùng câu xin lời khuyên hoặc
   phụ thuộc sở thích ("nên dành bao lâu", "quán nào ngon nhất", "nên đi mùa
   nào"), kể cả khi corpus có viết gợi ý.
3. Người hỏi là du khách hoặc người thích tìm hiểu văn hóa/lịch sử. Giọng đời
   thường, câu ngắn đến vừa, rõ ràng, không đánh đố, không lồng nhiều câu hỏi.
4. Không viết kiểu "theo tài liệu", "trong nguồn dữ liệu", "hãy cho biết"; không
   chép nguyên tiêu đề mục làm câu hỏi.
5. Khoảng 10% câu dùng tên gọi khác có thật và phổ biến (ví dụ "Hoàng thành"),
   chỉ khi corpus xác nhận đó là cùng một thực thể. Mọi câu viết có dấu, đúng
   chính tả.
6. `multi_source` phải thực sự cần ≥2 nguồn; `sources` liệt kê đủ các file.
7. `out_of_scope` phải chắc chắn vắng mặt trong corpus; người viết kiểm bằng tìm
   kiếm văn bản trên corpus trước khi đưa vào.

Pilot (§7) tạo bản "hướng dẫn viết" ngắn có ví dụ tốt/xấu thật, dùng chung cho
mọi người viết song song.

## 7. Quy trình

1. **Pilot `heritages` (~20 case).** Implementer viết; Reviewer đối chiếu từng
   case; User đọc toàn bộ ~20 case của pilot để chỉnh văn phong. Kết quả: hướng
   dẫn viết đã chốt và ~20 case dùng tiếp.
2. **Viết song song** phần còn lại của `heritages` và 6 partition khác.
   Implementer được dùng sub-agent, mỗi sub-agent một partition, cùng hướng dẫn
   viết. Mỗi partition ghi vào file authoring riêng.
3. **Kiểm máy** bằng script §9 cho từng file authoring.
4. **Reviewer đối chiếu từng case** với `sources` và corpus: đáp án đúng, khách
   quan, tự nhiên, đúng nhãn, đúng luật keyword. Case nghi vấn được đánh dấu kèm
   lý do.
5. **User đọc mẫu** 10–15 case mỗi partition do Reviewer chọn ngẫu nhiên, cùng
   mọi case bị đánh dấu.
6. Implementer sửa theo findings; Reviewer kiểm lại phần sửa.
7. **Merge:** ghép các file authoring theo thứ tự partition ở §3, loại
   `partition` và `sources`, không shuffle.
8. **Smoke 10:** Reviewer đề xuất 10 case phủ đủ 5 nhãn và ít nhất 5 partition;
   User duyệt; smoke là bản sao deep-equal của 10 dòng trong file chính thức.
9. User xác nhận closure Phase 7A.

## 8. Ràng buộc cho Phase 7B/8 (ghi nhận, chưa quyết)

- Retrieval metrics bỏ qua case `out_of_scope` (không có gì để tìm); answer
  metrics vẫn chấm.
- Không chia dev/test. Phase 8 chỉ so các cấu hình định trước; không chỉnh
  prompt/config để chữa một case cụ thể. Lỗi mới phát hiện được thêm vào phiên
  bản Golden sau, theo lifecycle riêng.
- Judge model: bài học khuyên judge mạnh hơn thí sinh và cố định khi so sánh;
  hiện judge và generator cùng là `gpt-6-luna`. Phải xem lại khi thiết kế 7B.
- Neo thang điểm Accuracy (bản Codex khác `rag_old_0`) xem lại ở 7B.
- Golden do LLM viết rồi người review, không phải câu hỏi người dùng thật; đây
  là limitation khi báo cáo.

## 9. Script kiểm tra không tốn phí

Một module nhỏ trong `backend/evaluation/`, chạy bằng `uv run`, đọc một file
authoring hoặc file chính thức và báo lỗi theo dòng:

- JSON hợp lệ; đúng field (4 cho file chính thức, 6 cho authoring);
- `category` thuộc 5 nhãn; `partition` hợp lệ (authoring);
- `sources` tồn tại trong corpus (authoring);
- mỗi keyword xuất hiện nguyên văn (NFC) trong corpus curated;
- case không phải `out_of_scope` có ≥1 keyword không nằm trong `question` và nằm
  trong `reference_answer`;
- `out_of_scope`: `keywords == []`, `reference_answer == INSUFFICIENT_ANSWER`;
- không trùng `question`;
- báo phân bố theo category và partition so với §5 (chỉ thông tin, không fail).

Script không gọi mạng, không sửa file và không thay việc người đọc đối chiếu nội
dung. Test chỉ cho logic thuần với input nhỏ hợp lệ.

## 10. Vị trí lưu và quyền

```text
knowledge-base-hue/<domain>/evaluation/golden_full_corpus_authoring.jsonl   # mỗi partition
knowledge-base-hue/evaluation/golden_full_corpus.jsonl                      # chính thức
knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl                # smoke 10
```

`travel_*` dùng `knowledge-base-hue/travel/<places|services|tickets>/evaluation/`.
Toàn bộ `knowledge-base-hue/` là private, không commit. Report tracked không
chép câu hỏi, đáp án hay excerpt; chỉ ghi số lượng, phân bố và findings dạng
tóm tắt.

Không gọi API có phí. Không sửa curated Markdown; nếu phát hiện lỗi corpus, ghi
lại cho Reviewer/User.

## 11. Acceptance

- File chính thức khoảng 175 case (±20% theo category), đủ 7 partition, mỗi
  partition ≥10 case; script §9 không báo lỗi.
- Reviewer đã đối chiếu 100% case; User đã đọc pilot và mẫu từng partition; mọi
  case bị đánh dấu đã sửa hoặc xóa.
- Smoke 10 được User duyệt và deep-equal với file chính thức.
- Report implementation và review ghi số lượng, phân bố, findings, case bị xóa
  và limitation; không lộ nội dung private.
- Docs active (`guides/full_corpus_rag.md`, `Project_Status.md`) được cập nhật
  theo các quyết định ở §2.
