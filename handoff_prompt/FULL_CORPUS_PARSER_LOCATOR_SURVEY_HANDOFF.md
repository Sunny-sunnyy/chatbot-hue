# Handoff khảo sát parser/source locator cho full-corpus

Target role: implementer
Authored by: reviewer
Handoff kind: next_design
State: completed
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: low (script khảo sát local, không đổi runtime/data)
Git authorization: none
Sub-agent authorization: none

**Contract lịch sử, đã hoàn tất:** user approved kết quả sau correction lượt 3
ngày 2026-09-09; xem review mục 9–10. Không thực hiện lại chỉ dẫn dưới đây.
Nhiệm vụ mới chỉ nằm tại `session_prompt/CURRENT_HANDOFF.md`.

Đây là nhiệm vụ khảo sát do user cho phép trực tiếp để hỗ trợ thiết kế, không
phải implementation plan của full-corpus. User chuyển prompt này thủ công.
Reviewer giữ quyết định kiến trúc/spec/plan/guide. Không triển khai chunker.

## Đọc và xác định phạm vi

Nếu chưa đọc trong task hiện tại, đọc:
- `session_prompt/Session_Prompt.md`
- `session_prompt/Project_Status.md`
- `session_prompt/IMPLEMENTER_WORKFLOW.md`
- `session_prompt/CURRENT_HANDOFF.md`
- `skills/risk-gated-agent-review/SKILL.md`
- `skills/practical-project-coding/SKILL.md`

CURRENT_HANDOFF là closure curation cũ; nhiệm vụ trực tiếp này có hiệu lực.
Không thực hiện lại migration. Kiểm read-only HEAD/branch/worktree, giữ mọi
thay đổi có sẵn. Worktree có guides modified và docs/context/reports/artifacts
untracked; không gọi là sạch. Nếu HEAD khác, xác định ảnh hưởng trước khi làm.

Đọc thêm:
- `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`, nhất là
  đề xuất schema/locator và cách gắn điều kiện mới.
- `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`, mục 23–24.
- `reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md`, lượt 3.
- JSON khảo sát tương ứng chỉ khi cần đối chiếu mẫu/span. Không chạy script cũ.

## Câu hỏi duy nhất của khảo sát

`markdown-it-py` có giúp nhận diện các khối Markdown cần thiết và lấy lại
đúng spans nguyên văn từ corpus hiện tại bằng cách trực tiếp, dễ hiểu không?
Đồng thời phân định phần cấu trúc parser biết và quan hệ điều kiện cần
Reviewer/chỉ dẫn riêng quyết định. Không coi parser là bộ hiểu ngữ nghĩa.

## Cách thực hiện

1. Kiểm package/version cài thực tế bằng project runtime qua `uv run --no-sync`.
   Lockfile có markdown-it-py 4.2.0, không đồng nghĩa đã cài. Không sync/install.
   Đọc API/source package local khi cần; cấu hình rõ preset và table rule.
   Tài liệu chính thức:
   https://markdown-it-py.readthedocs.io/en/latest/api/markdown_it.token.html
   https://markdown-it-py.readthedocs.io/en/latest/using.html

2. Viết script khảo sát nhỏ: parse nguồn, xem heading nesting, block/list/table
   maps; chuyển line ranges thành Unicode character offsets trên bản LF.
   Trích evidence bằng slicing source, không dùng render hay token.content
   đã biến đổi. Không dùng source.find(text) lần đầu trên toàn file làm locator.
   Ghi rõ token nào không có map và cách trực tiếp giải quyết, nếu cần.

3. Chọn các vùng thật sau, đường dẫn tương đối `knowledge-base-hue/`:
   - `festivals/festival/Hội xuân Gia Lạc.md`: Thông tin chung, list cha/con.
   - `heritages/heritage/Đại Nội Huế.md`: heading cha, text giữa cấp heading,
     Ngọ Môn và một image-only block có thật nếu có.
   - `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`:
     H3 2.3/câu dẫn khảo sát, H4 A, header + từng hàng bảng, HTML `<br>`,
     Bao gồm/Không bao gồm; kiểm ranh giới H4 B để tránh lan điều kiện của A.
   - `travel/services/Chi phí du lịch Huế.md`: intro, bảng dự toán một ngày,
     hàng tổng và phạm vi áp dụng của intro.
   - Tìm đúng file Vé tham quan Hải Vân Quan trong `travel/tickets/`: đọc
     mục quản lý/chuẩn hóa lẫn answer content; trích vài vùng cần quyết định.
   - Một blockquote/cảnh báo và dòng chỉ chứa ảnh có thật trong những file
     trên; nếu không có, tìm thêm đúng một mẫu trong corpus, không quét rộng.

4. Xuất ví dụ table header + row + condition với spans tách riêng theo schema
   đề xuất. Đây là minh họa locator, không final chunks hoặc đo token mới.
   Nếu dòng chỉ có ảnh bị bỏ, thể hiện hai spans xung quanh, không mất chữ.
   Nếu có paragraph cần chia theo câu, minh họa đúng một ranh giới từ nguồn
   thật để kiểm offset con; chưa viết bộ tách câu tiếng Việt tổng quát.

5. Kiểm exact-match trên mọi part được xuất; phân biệt điều này với completeness
   và semantic sufficiency. Mỗi vùng mục tiêu nêu phần giữ, metadata, whitespace,
   phần bỏ cùng lý do. Không yêu cầu output toàn bộ file hoặc cả corpus.
   Parse lại cùng input/cấu hình để kiểm vị trí ổn định, không gọi là quality test.
   Nếu source chỉ có LF, có thể tạo bản CRLF tạm trong bộ nhớ từ đúng text đó
   để kiểm quy ước normalization; ghi đây là biến thể deterministic kiểm locator,
   không phải file corpus thật hay integration evidence. Không sửa nguồn.

6. Từ Ca Huế/Chi phí, đề xuất một cách chỉ dẫn tối thiểu ngoài corpus:
   định vị vùng điều kiện và vùng đích qua source + heading path/vị trí block
   có kiểm tra nguyên văn; nêu cách phát hiện sai target khi source đổi hoặc
   heading trùng. Chỉ mô tả/ví dụ trong report, không xây registry/rule engine.
   Phân biệt quan hệ suy từ cấu trúc và quan hệ Reviewer phải quyết định.
   Không mở rộng điều kiện chỉ để mọi chunk chứa toàn tài liệu.

7. Chỉ nếu markdown-it-py có thiếu sót cụ thể, xem một lựa chọn đã cài sẵn
   (ví dụ mistune) để giải quyết đúng thiếu sót; không benchmark nhiều parser.
   Nếu thiếu dependency, báo phần chưa kiểm và blocker; không tự tải/cài.

## Quyền và giới hạn

Được đọc source/corpus/cache/package local; viết/chạy script khảo sát trong
`/tmp` và tạo đúng artifacts báo cáo dưới đây. Không nhập module runtime có
side effects. Không chạy tokenizer, model inference, test suite, ingestion,
Qdrant/API, không nạp `.env`. Không sửa backend/tests/corpus/settings/lockfile,
guides/specs/plans/context hoặc reports cũ. Không Git mutation/subagent.
Nếu tool cần escalation, tuân thủ cơ chế approval của môi trường.

## Kết quả bàn giao và Review Contract

Tạo:
- `reports/full_corpus_parser_locator_survey_2026_09_09.md`
- `reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py`
- `reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json`

Nếu file tồn tại, đọc trước và bảo toàn phần ngoài task. Script tái lập từ
source thật và package đã có; JSON lưu text/spans cùng kết quả kiểm thực tế.
Report ngắn: version/config/lệnh thực chạy, bảng các cấu trúc hỗ trợ hoặc
thiếu, ví dụ đáng chú ý và chỉ dẫn điều kiện đề xuất, limits/failed/not verified.
Không dựng ví dụ rồi gọi là data thật hoặc lấy số đo cũ làm fresh evidence.

Acceptance của khảo sát: vị trí tái lập và exact-match cho các parts đã xuất;
map được list/table/heading bằng evidence cụ thể hoặc báo giới hạn trung thực;
tách rõ cú pháp với quyết định ngữ nghĩa; không mutation ngoài artifacts.
Không bắt buộc parser phải PASS mọi ca để report có giá trị.

Tự đọc diff/artifacts, kiểm `git diff --check`, ghi đúng worktree còn modified/
untracked. Không chạy thêm full suite. Reviewer sẽ đọc report và kiểm chọn lọc
source/output khi có mâu thuẫn, không mặc định chạy lại script.

Khảo sát này không còn next action thực thi. Parser đã được chọn và user đã
approved kết quả; theo `session_prompt/CURRENT_HANDOFF.md` cho nhiệm vụ mới.
