# Codex Review: khảo sát parser/source locator toàn corpus

Decision: approved
Reviewer: Codex
Date: 2026-09-09
Contract: `handoff_prompt/FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md`
Implementation report: `reports/full_corpus_parser_locator_survey_2026_09_09.md`

**Trạng thái mới nhất:** user đã xác nhận kết quả khảo sát sau correction lượt 3.
Khảo sát approved/completed, findings đã đóng. Mục 9 giữ technical review,
mục 10 ghi user confirmation và closure; các mục correction trước là lịch sử.

## 1. Phạm vi đã review

Đọc report, script khảo sát, các phần JSON phục vụ kiểm claim; đối chiếu vùng
Ca Huế, intro Chi phí, Hải Vân Quan và JSON tokenizer lượt 3 khi thấy chênh lệch.
HEAD `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`; worktree vốn có hai guides
modified và artifacts/docs/context untracked. Đã đọc diff hai guides có sẵn.
Đây là review khảo sát phục vụ thiết kế, chưa là nghiệm thu runtime full-corpus.

## 2. Findings

### F1 — major: mẫu cũ cắt sai hàng; claim khớp khảo sát lượt 3 che khuất lỗi

Report §1.2 nói spans khớp hoàn toàn khảo sát lượt 3, nhưng §4.3 và JSON parser
cho hàng Việt Nam `[10901,11141)`, quốc tế `[11142,11317)`. Kiểm trực tiếp bằng
`jq --rawfile` xác nhận hai spans mới đúng dòng nguồn (240 và 175 ký tự).

JSON tokenizer cũ có `ca_hue_p3b_lead_chunk_1a` dùng `[10901,11158)`, kết thúc
bằng `\n| **Khách quốc t`; `ca_hue_p3b_lead_chunk_1b` dùng `[11159,11317)`, bắt
đầu bằng `** | 150.000`, mất nhãn khách quốc tế. Hai mẫu P3A tương ứng cũng sai.
Đây là điểm Reviewer bỏ sót ở phiên trước, phát hiện từ chênh lệch parser mới.
Exact substring vẫn có thể đúng trong khi ranh giới/ngữ nghĩa sai.

Tác động: các counts 298/230/462 và 260/203/418 (E5/HuyDang/MiniLM long) của
hai mẫu lead không chứng minh độ dài của hai hàng hoàn chỉnh như đã diễn giải.
Không suy ra counts mới bằng cộng/trừ ký tự, không phủ nhận mọi số đo khác.

Đóng finding: report đính chính rõ lỗi cũ và ảnh hưởng; xuất hai ví dụ lead +
header + hàng hoàn chỉnh + Không bao gồm theo `evidence_parts` đề xuất. Ghi
token counts của input đã sửa là chưa đo. Chưa cần chạy tokenizer trong correction
parser; không sửa artifacts tokenizer lịch sử hay tuyên bố các counts cũ còn đúng.

### F2 — major: thiếu bằng chứng thực thi cho acceptance tái lập/kiểm mọi part

Report §7 khẳng định parse lại nhiều lần nhưng script chỉ có một `md.parse`
trong `parse_file`, gọi một lần mỗi file; JSON không có kết quả so hai lần parse.
Phép `deterministic_match` hiện chỉ so chuỗi LF với CRLF đã normalize.
Nhiều `exact_match` được gán `True` hoặc so lát cắt với biến vừa gán cùng lát cắt;
khối §11 mang tên xác thực toàn bộ nhưng thực tế chỉ ghi JSON. Chưa có ví dụ
chunk kết hợp header/row/condition đúng schema; các phần vẫn tách trong JSON.

Đóng finding: chạy lại parser hai lần cùng nguồn/cấu hình và so token maps cùng
spans đã chọn, xuất kết quả thực. Kiểm mọi part xuất có source, bounds hợp lệ,
text bằng slice nguồn; kiểm riêng boundaries có đúng khối mong muốn. Xuất ví dụ
kết hợp ở F1; ghi coverage các vùng mục tiêu gọn: giữ/heading metadata/whitespace/
bỏ và lý do. Không xây validator framework hoặc test suite. Ghi exact command,
version đọc từ package thật thay cho chỉ hardcode trong metadata.

### F3 — major: condition mapping chưa thỏa contract nguyên văn và scope

Script phần 9 / JSON `condition_mapping_proposal.examples[1]` dùng signature
intro Chi phí nối thành một dòng. Source và part `[23,261)` có hai LF nội bộ.
Kiểm `jq` giữa signature và text nguồn đã xuất trả `false`: cơ chế equality
đề xuất sẽ từ chối ngay corpus chưa sửa. Giữ LF trong signature, không sửa nguồn
hoặc normalize whitespace evidence để làm phép kiểm qua.

Report §6.2 cũng khẳng định bất kỳ edit nào của file đều bị signature phát hiện.
Signature chỉ bảo vệ block được so; chưa kiểm target bị đổi, thiếu hoặc trùng.
Heading path đầy đủ vẫn có thể trùng; `block_index` không tự bảo vệ việc chọn
nhầm khi cấu trúc đổi. Mẫu Chi phí chỉ có dự toán 1/2 ngày dù source còn mục
3 ngày và phần mô tả nói tất cả bảng dự toán.

Đóng finding: ví dụ chỉ dẫn đúng nguyên văn và target có thật; nói rõ phạm vi
ví dụ, bao gồm ba mục dự toán nếu tuyên bố áp dụng tất cả. Nêu cách trực tiếp
resolve condition lẫn target duy nhất và dừng khi 0 hoặc nhiều kết quả; nếu cần
phân biệt bằng vị trí thì kèm kiểm nguyên văn target. Có mapping Không bao gồm
chỉ vào A, không sang B. Chỉ mô tả và kiểm trên mẫu; không triển khai rule engine.

### Ghi chú không mở correction riêng

- Không coi section đầu Hải Vân Quan là `pure_administrative_governance` để bỏ
  toàn bộ: nguồn có vị trí, ngày bắt đầu thu phí, thời hạn và cơ quan đón khách.
  Mục chuẩn hóa cũng có quyền lợi/điều kiện; chưa có đối chiếu đủ để loại cả mục.
  Reviewer giữ answer content, chưa quyết định lọc các section này.
- Claim ảnh hiện là minh họa một dòng với vị trí trước/sau cố định, chưa là bộ
  lọc ảnh tổng quát. Giữ phạm vi mẫu; không yêu cầu viết bộ lọc production.
- Worktree không sạch; sáu file được khảo sát nếu tính Mệ Kéo. Bỏ so sánh mistune
  thiếu evidence vì không cần parser dự phòng. Không biến chữ “100%” thành cam
  kết cho toàn corpus, byte offsets, semantic completeness hoặc chất lượng RAG.

## 3. Cách Reviewer kiểm thật

Read-only: `git status --short --untracked-files=all`, `git rev-parse HEAD`,
`git diff --check`, đọc diff guides; `sed`/`rg` đọc exact vùng nguồn/script;
`jq` chọn các chunks có span 11159/11158 trong JSON tokenizer cũ.

Kiểm độc lập bốn hàng parser bằng `jq --rawfile src <file Ca Huế>` rồi so
`.text == $src[.span.start:.span.end]`; kiểm signature Chi phí với
`.target_areas.chi_phi_du_lich_hue.intro[0].text` trong JSON parser.
Đây là đọc/đối chiếu artifact, không là fresh execution parser/tokenizer.

## 4. Kết quả quan sát

Bốn hàng parser đều source-match; signature Chi phí không match; hai chunks
lead cũ mất ranh giới hàng như F1. `git diff --check` đạt với tracked diff.
Không có tracked runtime/corpus diff được thấy; không có snapshot trước khảo
sát cho mọi untracked file nên không xác nhận tuyệt đối claim không mutation.

## 5. Giới hạn

Không rerun script, tokenizer, models, Qdrant, API hoặc full suite. Không kiểm
giá/chính sách hiện hành trên web: ở đây chỉ đánh giá nội dung và vị trí corpus.
Counts cũ là evidence lịch sử; hai mẫu sai chưa có counts cho input đã sửa.

## 6. Decision và bước tiếp theo

`changes_requested`, correction lượt 1 của khảo sát parser. Giữ markdown-it-py
với `MarkdownIt().enable('table')` làm lựa chọn thiết kế ưu tiên: bằng chứng mẫu
ủng hộ line maps → Unicode spans, chưa có lý do đổi parser. Giữ quy ước LF,
Unicode `[start,end)`, evidence từ source và tách search text.

Implementer sửa đúng ba artifacts khảo sát theo `CURRENT_HANDOFF.md`; Reviewer
kiểm delta rồi tiếp tục written spec. Không trình spec dựa trên mẫu sai. Spec
và plan vẫn có điểm duyệt riêng; Git authorization: none.

## 7. Re-review correction lượt 1 — 2026-09-09

### Phạm vi và kết quả đã đạt

Đã đọc report/script cập nhật và JSON liên quan F1–F3. HEAD không đổi; tracked
diff vẫn gồm hai guides và handoff của Reviewer. Không có snapshot đầy đủ của
ba artifacts untracked trước correction để khẳng định exact diff từng dòng;
đối chiếu code hiện tại với findings và bằng chứng trước đó trong cùng session.

- F1: hai hàng VN/QT đã nguyên vẹn. `jq --rawfile` kiểm cả 8 part của hai chunk
  kết hợp đều khớp slice nguồn; search_text lengths 931/866 khớp JSON. Counts
  mới được ghi `not_measured`, đã rút claim dùng counts cũ.
- F2: `run_reproducibility_test` thực sự gọi parse hai lần mỗi file và so
  type/tag/map; trên cùng source và phép chuyển offsets trực tiếp, đây là bằng
  chứng hữu ích cho tính tái lập trên mẫu. Validator hiện thực sự kiểm bounds
  và source slice cho các objects có `span` dict + `text`; JSON báo 40/40.
  Reviewer đọc code/evidence, không tự nhận đã chạy parser hoặc xác minh độc
  lập toàn bộ 40 parts. Không yêu cầu thêm lần parse/process hoặc test suite.
- F3: `jq --rawfile` xác nhận signature Chi phí bằng nguồn `[23,261)`; ba
  heading dự toán đã được liệt kê. Giới hạn bảo vệ signature đã đính chính.

### Findings còn lại, cùng một batch

**R1 — major, F3 chưa đóng: chưa kiểm selectors resolve trên nguồn thật.**
Script dòng 913–987 chỉ tạo object `condition_mapping_proposal` với chuỗi mô tả.
`expected_target_tables_count` và các selectors không được dùng để kiểm lookup;
không có result cho số condition/section/table khớp từng selector. Đoạn thu
`cp_table_samples` chỉ lấy các hàng Tổng tại Huế theo H2 hiện tại, chưa chứng
minh mỗi target section duy nhất và chứa đúng bảng. Việc mô tả fail-fast
không phải evidence đã chạy kiểm selectors như handoff yêu cầu.

Đóng: một probe nhỏ trên các rules đã có, lập heading path từ token stream;
kiểm condition theo path/type/signature và từng target section duy nhất, xuất
số match cùng spans bảng/hàng thực tìm được. Lead Ca Huế bao A/B; Không bao
gồm chỉ A; Chi phí resolve từng mục trong ba dự toán. Nếu thiếu/mơ hồ thì ghi
FAIL và dừng rõ. Không viết bộ nạp ingest hoặc rule engine production, không
tạo tình huống giả hoặc test suite. Count ba bảng đơn thuần không thay lookup
duy nhất cho từng heading. Có thể bỏ các trường chỉ mô tả trùng lặp.

**R2 — major, F1/F2 chưa đóng hết: composite không dùng output parser/schema
đã giao.** Script dòng 438–504 dựng lại `lead_part`, `header_part`, VN/QT và
exclusions bằng literal offsets dù đã có các samples từ parser; không kiểm
composite bằng chính kết quả boundaries parser. Parts vẫn có `span:{start,end}`
và roles `condition_lead/table_header/table_row/condition_exclusions`, khác
schema ví dụ đã yêu cầu `{role,start,end,text}` với body/header/condition.
Đây không là yêu cầu đổi schema của mọi diagnostic sample.

Đóng: tái sử dụng spans/text đã resolve từ parser để dựng đúng hai composites;
exclusions lấy từ list_item nguồn. Hai composites dùng schema yêu cầu; các
diagnostic records có thể giữ format cũ. Kiểm validator không bỏ qua các parts
dạng flat vừa đổi. Không hardcode mẫu mới để chỉ ra đúng kết quả lần này.

**R3 — major, lỗi nội dung mới phát sinh khi sửa ghi chú Hải Vân Quan.**
Report §4.5, script dòng 745 và JSON `analysis_updated` ghi thời gian bắt đầu
thu phí `01/01/2025` và gán phối hợp vận hành cho UBND quận Liên Chiểu. Nguồn
đang review ghi bắt đầu `02/06/2026`; Trung tâm Bảo tồn Di tích Cố đô Huế trực
tiếp quản lý/đón tiếp/thu phí trong giai đoạn Huế quản lý. Liên Chiểu xuất hiện
trong chú thích địa giới cũ, không chứng minh vai trò vận hành được report gán.
Đây là mô tả sai corpus dùng cho quyết định giữ/bỏ evidence, không phải tranh
luận về luật/giá hiện hành. Không dùng web sửa corpus.

Đóng: sửa hoặc bỏ diễn giải sai trong cả ba artifacts, dẫn nguyên văn vài phần
nguồn chứng minh nội dung hữu ích. Không cần khảo sát lại cả file hay xác minh
luật ngoài corpus. Finding mới do nội dung sai được thêm ở correction này.

### Giới hạn F2 và ghi chú không chặn riêng

Bảng coverage hiện là các spans và tổng viết cứng, không phải phép kiểm động
mọi vị trí; validator 40 parts bỏ qua các records có `span` list như coverage.
Vì vậy chỉ gọi 40/40 là kết quả cho các source-text parts được validator duyệt,
không là xác thực mọi object/coverage hoặc tính đầy đủ toàn corpus. Bảng hạch
toán mẫu tĩnh được giữ như minh họa, cần ghi đúng giới hạn; không yêu cầu xây
validator coverage rộng. Version nên đọc thẳng package thay fallback `'4.2.0'`.

### Kiểm tra đã chạy và quyết định

Read-only `git status`, `git rev-parse HEAD`, `git diff --numstat`,
`git diff --check`; `rg`/`sed` source/script; `jq --rawfile` đối chiếu hai
composites và signature Chi phí. Các kiểm slice/length trên đạt; `rg` source
xác nhận ngày/cơ quan như R3; `git diff --check` đạt tracked diff. Không rerun
parser/tokenizer/model/API/Qdrant; không sửa artifacts Implementer.

Verdict lần thứ hai: `changes_requested`. Giữ lựa chọn parser và phần đạt,
chỉ correction R1–R3; chưa duyệt written spec hoặc runtime. Handoff hiện hành
đã cập nhật; user chuyển cho Implementer. Không cần mở lại khảo sát parser khác.

## 8. Re-review correction lượt 2 — 2026-09-09

### Phạm vi, evidence và phần đã đóng

Đọc delta thực hiện R1–R3 trong script/report/JSON; đối chiếu với nội dung
đã đọc ở lượt trước. HEAD vẫn `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`.
Ba artifacts untracked không có Git base riêng, không coi tracked diff là
bản diff đầy đủ của correction. Không thấy thêm đường dẫn thay đổi ngoài
những paths đã ghi nhận, nhưng không khẳng định mọi untracked file bất biến.

- **R2 đóng:** composite lấy spans từ token maps/header/list item, schema flat
  đúng `{role,start,end,text}` và roles condition/header/body. Validator nhận
  schema flat lẫn nested. `jq --rawfile` kiểm độc lập hai composites: schema
  đúng, cả 8 parts khớp nguồn. Giữ counts `not_measured`.
- **R3 đóng về lỗi factual ảnh hưởng quyết định:** ngày 02/06/2026 và Trung tâm
  Bảo tồn Di tích Cố đô Huế đúng nguồn đã đọc. Section đầu có answer content,
  không bỏ toàn bộ. Cách viết “UBND quận Liên Chiểu xuất hiện” còn chưa chính
  xác: nguồn chỉ có tên quận trong chú thích địa giới; sửa chữ trong cùng lượt,
  không tạo finding chặn riêng. Các quote report bỏ dấu Markdown, nên gọi
  trích nội dung; không dùng chúng làm literal source signature.
- **R1 tiến bộ:** probe đã duyệt tokens, đếm match, lấy bảng/hàng, kiểm mỗi
  target tìm được một section/một bảng và ba hàng tổng. Kết quả samples hiện
  tại hữu ích. `jq` xác nhận cả ba condition texts trong output bằng signatures
  trong rules. Đây là kiểm artifact độc lập, không chứng minh script đã kiểm
  đầy đủ selector khi chạy.

### R1 còn mở — major: phép kiểm không đủ bộ selector mà report tuyên bố

Trong `run_condition_mapping_probe`:

1. Rule Không bao gồm dùng `li_text.startswith('- **Không bao gồm:**')`, chưa
   so **toàn bộ** text với exact_text_signature. Thay nội dung sau nhãn vẫn
   có thể qua; đây chính là contract signature đang khảo sát, không phải edge
   case mới thêm.
2. Rule Chi phí tính `path` nhưng không dùng trong điều kiện match; `sig3` lấy
   lại từ `cp_text[23:261]`. Probe chưa kiểm condition thuộc intro `heading_path=[]`
   như rule công bố, và expected signature không độc lập với slice đang so.
3. Lookup H4 A/B chỉ dùng tên H4 trên toàn file; chưa đối chiếu ancestor path
   H2/H3 của target như mapping. Việc condition lead có path đúng không tự
   chứng minh target A/B thuộc cùng H3. Bổ sung kiểm path vào lookup đã có.

Đóng bằng sửa trực tiếp probe: dùng các literals/giá trị rule đã khai báo làm
expected selectors, so cả path/type/full signature từ source slice; lọc từng
target theo full path. Dùng cùng quy ước bỏ H1 cho rule và path so sánh.
Không cần resolver tổng quát, registry, test giả, nhiều process hoặc benchmark.
Các checks phải chạy trước khi ghi PASS, nêu rõ counts quan sát được.

`stop_boundary_matched_rows_count=0`/`boundary_respected=True` hiện là constants.
Danh sách A lấy từ section đã cắt riêng nên trên mẫu hiện tại không có B; ghi
đây là kết quả suy từ cách chọn section, hoặc tính giao spans A/B trực tiếp nếu
vẫn gọi là phép kiểm đã chạy. Không yêu cầu thêm cơ chế ranh giới thứ hai.

### Sai số report cần sửa cùng lượt, không chặn riêng

Report §8.1 ghi hàng B `[12836..13264)` nhưng JSON cho hai spans
`[12617,12968)` / `[12969,13386)`. `jq --rawfile` xác nhận cả hai spans JSON
khớp nguồn. Dùng số thực từ artifact, không sửa boundaries đúng để khớp report.
Validator 40 parts không bao các probe records có span list; không gọi 40/40
là xác thực mọi output probe. Giới hạn coverage tĩnh đã ghi đúng, giữ nguyên.

### Kiểm đã chạy, giới hạn, verdict

Read-only git status/HEAD/diff-check; rg/sed code và report; jq kiểm schema,
source slices hai composites và hàng B, đối chiếu ba signatures với probe text.
Lần jq đầu tra key cũ `examples` trả null/false; đã đọc keys và chạy lại với
`rules`, cả ba trả true. Không dùng kết quả tra key sai làm finding. Không
rerun parser/tokenizer/model/API/Qdrant. `git diff --check` đạt tracked diff.

Verdict lần thứ ba: `changes_requested`, chỉ R1 còn mở. Không khởi động lại
F1/F2/R2/R3 hoặc khảo sát parser khác. Correction lượt 3 chỉ hoàn thiện các phép
so trong probe và đồng bộ report; không thêm requirement ngoài contract đã giao.

## 9. Re-review correction lượt 3 — kết quả kỹ thuật đạt

### Phạm vi và findings

Đọc phần R1 sửa trong script, constants signatures, selectors/path, boundary
calculation; đối chiếu JSON và phần report được sửa. R2/R3 giữ kết luận đạt
từ lượt trước; kiểm thêm source-match hai composites để xác nhận phần evidence
vẫn nguyên vẹn. HEAD không đổi, worktree vẫn có thay đổi đã ghi nhận.

**R1 đóng:** expected signatures khai báo độc lập và dùng chung với rules.
Rule Không bao gồm so toàn văn và slice nguồn; Chi phí lọc path rỗng trước
H2, giữ LF; lookup các target so full ancestor path theo quy ước bỏ H1.
Kiểm số matches duy nhất diễn ra trước output RESOLVED_UNIQUE. Probe có tính
ranh giới từ spans A/B thay vì chỉ mô tả. JSON ghi condition count 1 mỗi rule,
2 bảng/6 hàng Ca Huế, 3 bảng/3 hàng tổng Chi phí, boundary_respected=true.

Report đã đồng bộ spans B, câu chữ Liên Chiểu và giới hạn validator. Không còn
blocker/major trong phạm vi khảo sát. Không mở correction khác.

### Kiểm độc lập đã thực hiện

Read-only `git status --short`, `git rev-parse HEAD`, `git diff --stat`,
`git diff --check`; rg/sed đọc code/report và jq đọc JSON. Với
`jq --rawfile` nạp Ca Huế/Chi phí, đã đối chiếu:

- ba condition texts bằng signatures khai báo, bằng source slices và path
  trong output bằng path trong rules: tất cả true;
- toàn bộ 8 composite parts vẫn khớp nguồn;
- các hàng A kết thúc trước offset 12289; slice `[12289,12365)` đúng heading B.

`git diff --check` đạt tracked diff. Các artifacts untracked vẫn không có Git
base riêng để chứng minh exact diff đầy đủ; không khẳng định kiểm formatting
tracked đồng nghĩa kiểm mọi artifact. Không rerun parser/tokenizer/model/API/
Qdrant; 2-pass, 40/40 và 3 rules là evidence thực thi Implementer cung cấp,
Reviewer kiểm code cùng output có mục tiêu, không gọi là fresh rerun độc lập.

### Giới hạn và lựa chọn thiết kế

Chọn `markdown-it-py` với `MarkdownIt().enable('table')` làm parser cho bản
thiết kế tiếp theo. Giữ UTF-8 strict, CRLF/CR → LF, zero-based Unicode code
points `[start,end)`, lấy evidence từ source và tách search_text.

Khảo sát chứng minh khả năng định vị các mẫu hiện có; không là chunker hay
resolver production. Các trường PASS trong probe không phải bảo đảm mọi
thay đổi corpus sẽ được phát hiện: cụ thể boundary bool được xuất nhưng chưa
chặn PASS nếu false, lookup phụ heading B dùng tên; trên nguồn hiện tại đã
kiểm đúng. Không cần mở rộng script khảo sát để production-harden các nhánh
này. Written spec phải mô tả lookup thống nhất và xử lý mismatch riêng.

40/40 chỉ dành cho source-text parts validator duyệt, không bao probe records
span-list/coverage tĩnh hay toàn corpus. Hai composites chưa có token counts
mới; các số cũ trên ranh giới sai không được phục hồi làm PASS. Chưa quyết định
lọc cả section Hải Vân Quan; không dùng exact-match làm bằng chứng đủ ngữ nghĩa.

### Decision và Approval Closure Contract

Technical verdict: `ready_for_user_confirmation` cho khảo sát parser/locator.
User xác nhận chấp nhận kết quả khảo sát với các giới hạn trên; không cần tự
chạy lại kỹ thuật. Xác nhận này không duyệt toàn bộ spec/plan hoặc runtime.

Sau xác nhận, Reviewer được cập nhật verdict khảo sát thành approved và
CURRENT_HANDOFF thành completed; đồng bộ các ghi chú trạng thái đầu context/
prompt/spec nháp. Reviewer tiếp tục thiết kế theo quyền đã cấp, chốt schema,
condition mapping, oversized groups và nhu cầu đo hai input đã sửa. Written
spec và implementation plan vẫn cần user duyệt riêng. Không giao Implementer
closure cơ học hoặc chạy thêm khảo sát khi chưa có nhiệm vụ mới.

Checks closure: links/status nhất quán và git diff --check. Git authorization:
none. Không sửa runtime/corpus/index/dependencies hoặc các artifacts Implementer.

## 10. User confirmation và closure — 2026-09-09

User xác nhận: “Tôi xác nhận kết quả khảo sát ... sau khi cập nhật thì tiếp
theo chúng ta tiếp tục hoàn thiện written spec”. User đồng thời cho phép sửa/
xóa nội dung Markdown lỗi thời và lưu đầy đủ ngữ cảnh session.

Đã thực hiện Approval Closure Contract: verdict khảo sát approved; correction
series completed; đồng bộ context, next-session prompt, trạng thái dự án và
spec/experiment notes/guides liên quan. CURRENT_HANDOFF chuyển sang next_design
cho Reviewer theo chỉ đạo tiếp tục written spec, không còn correction active.

Approval giới hạn ở khảo sát parser/locator và evidence mẫu đã review. Written
spec/implementation plan chưa approved; token counts VN/QT đúng vẫn chưa đo.
Không sửa ba artifacts Implementer hoặc runtime/corpus/index/dependencies,
không chạy tokenizer/model/API/Qdrant, không Git mutation hoặc subagent.
Kiểm closure: trạng thái/links nội bộ và git diff --check, giữ giới hạn của
tracked diff đối với artifacts untracked. Next action: hoàn thiện written spec.
