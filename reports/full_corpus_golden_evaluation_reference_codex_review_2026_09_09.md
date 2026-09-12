# Codex Review: reference Golden/evaluation

Decision: approved
Reviewer: Codex
Date: 2026-09-09; correction 1–3 re-review: 2026-09-10
User confirmation: 2026-09-10
Contract: `handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`
Implementation report: `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`

## 1. Phạm vi đã review

Đọc report/handoff và contract; kiểm chọn lọc evaluation/test.py, các hàm
metrics/judge của rag_old_0/evaluation/eval.py và rag_old/evaluation/eval.py;
bốn records report trích, saved code/output cells day4.ipynb, đoạn day4.txt
55–110 và độ dài day5.txt. Không đọc lại toàn reference hoặc chạy project code.
HEAD ea87d3ed52851f6b6ab5c47b138540ebc8ff8340; worktree có thay đổi sẵn.

## 2. Findings — correction lượt 1, một batch

### R1 — major: mô tả cutoff và đơn vị relevance chưa đúng code

Report §3/§4.3 gộp MRR/coverage/nDCG thành đo Top-K. Trong
`/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py:81–106`, k không
được truyền vào fetch_context; MRR duyệt toàn retrieved_docs, coverage dùng
các MRR đó; chỉ nDCG cắt retrieved_docs[:k]. IDCG sắp lại relevance ngay trong
list đã truy xuất, không biết các evidence liên quan bị bỏ sót ngoài list.
`rag_old/evaluation/eval.py:51–115` có cùng khác biệt cutoff; relevance chỉ
ghép parent_headline + parent_chunk + child_chunks[0], không mọi child_chunks.

Tác động: dễ thiết kế/so metric có cùng tên nhưng khác phạm vi đo. Đóng R1:
sửa data flow/bảng/§4.3, nêu rõ từng metric, k thực tác động đâu, IDCG biết gì;
phân biệt current import PRO với Basic lịch sử. Không sửa code reference hoặc
đặt metric/threshold Huế từ reference này.

### R2 — major: đánh đồng reference_answer có nội dung với Golden đúng/đầy đủ

Report §1.2/§6 khẳng định 100% 150 câu có đáp án đầy đủ. Chính records thật
được trích ở §5 phản chứng: tests.jsonl dòng 101 hỏi sản phẩm người thắng
IIOTY làm việc, đáp án chỉ nêu chức danh; dòng 141 hỏi số lượng nhân viên,
đáp án chỉ nói “several” và nêu hai ví dụ. Bốn records trích đều khớp file;
lỗi ở cách đánh giá chất lượng, không phải ví dụ bị bịa.

Đóng R2: chỉ rõ hai lỗi khớp question–answer, rút claim mọi đáp án đầy đủ;
phân biệt chưa thấy ca negative được thiết kế/gán nhãn với chứng minh mọi
câu đều trả lời được từ corpus. Nêu cần kiểm đáp án/evidence trước dùng làm
ground truth. Không cần audit toàn corpus reference hoặc sửa dataset.

### R3 — major: attribution và khuyến nghị vượt bằng chứng/phạm vi

- Handoff nói đọc đầy đủ mọi file, trong khi reading map ghi nhiều file chỉ
  quét/tìm từ khóa. Sửa phạm vi về mức thực đã đọc, không đọc lại toàn bộ để
  hợp thức hóa claim. Không có loader sinh Golden trong các file đã kiểm
  không chứng minh cả codebase không có công cụ đó.
- day4.txt:55–110 là ghi chú tổng hợp có cả “Kiến thức liên quan & mở rộng”,
  câu “Dù bạn chưa cung cấp file code cụ thể…”; không coi mọi câu là trích
  nguyên văn giảng viên. Ghi là nội dung tài liệu phiên âm/tổng hợp được cung
  cấp, phân biệt code thật. Không yêu cầu user tìm lại audio/transcript gốc.
- Report §4.5 dẫn day5.txt L1333, nhưng file chỉ có 745 newline (có thể 746
  dòng nếu dòng cuối không LF). Sửa hoặc bỏ pointer sai. day4.ipynb cell 9/13
  lưu scores 4/3/4; nếu ghi lời tổng hợp 5/4 ở tài liệu khác, tách hai mốc,
  không ghép làm cùng run hoặc coi saved output là kết quả current code.
- Rủi ro summary tạo keyword false positives chưa chứng minh MRR PRO thực
  tế đã bị thổi phồng hoặc mức đóng góp. Seed/temperature là cấu hình kiểm
  soát, không bảo đảm API/judge deterministic. Sửa cách khẳng định ở §1.2/§6.
- §6 dùng khác thời điểm/nhà cung cấp làm ca mâu thuẫn dù user đã phân biệt
  phạm vi. Tách ca cùng phạm vi mâu thuẫn với ca khác điều kiện. Bỏ “buộc phải
  Agentic/router” ở §5: đó không phải lựa chọn duy nhất và không scope MVP Huế.
  Không đề xuất lấy ngưỡng màu reference làm gate nghiệm thu khi chưa thiết kế.

Đóng R3 bằng chỉnh report/handoff và dẫn vị trí đủ hỗ trợ claim; không thêm
research web, model runs, dashboard hoặc framework. Quotas 10–15%, split và
judge rubric chỉ là đề xuất, không requirement. Gom sửa cả summary/bảng/kết
luận liên quan để không còn câu trái với phần đã đính chính.

## 3. Cách Reviewer kiểm thật

Read-only git status/HEAD/name-only/untracked list và diff-check; sed/nl/rg
đọc các vùng kể trên; cmp hai tests.jsonl (không khác); jq đọc notebook JSON
cells/outputs, không thực thi cells. Tìm vài từ chỉ thiếu thông tin trong
dataset không có match; kết quả đó không chứng minh mọi câu answerable.
Không chạy Python, tests, tokenizer, model, API hoặc Qdrant.

## 4. Kết quả quan sát

Đã xác nhận TestQuestion có question/keywords/reference_answer/category;
metrics dựa substring keyword; judge nhận question/generated/reference mà
không nhận retrieved context/citation. Bốn sample records và saved retrieval
output cell 7 khớp report. Hai datasets cmp bằng nhau. Các sai lệch R1–R3
ảnh hưởng việc dùng báo cáo làm căn cứ thiết kế nên chưa ready_for_confirmation.
Git diff --check đạt tracked diff; không gọi worktree sạch.

## 5. Giới hạn

Không kiểm mọi claim/file/record trong ba roots; không xác minh thực thi của
reference hoặc mọi nguồn metrics PRO. Report mới untracked không có base
diff riêng; đã đọc toàn văn thay vì gọi Git diff là kiểm toàn bộ report.
Không có snapshot trước task cho mọi untracked artifact. Các dữ kiện đã kiểm
ở mục 4 được giữ khi correction không đổi nguồn; không mặc định lặp đọc.

## 6. Decision và next action

changes_requested: Implementer sửa đúng report và CURRENT_HANDOFF theo R1–R3,
tự review rồi chuyển final_review. Không mở lại khảo sát parser/VN-QT, không
đổi source/reference/Golden/runtime hoặc tự viết spec. User chỉ chuyển prompt,
không cần duyệt correction trong scope. Reviewer dùng các kết luận đã kiểm
để tiếp tục thiết kế độc lập; chưa chốt số câu/quotas/split/threshold.

## 7. Re-review correction lượt 1 — 2026-09-10

### Phạm vi và evidence dùng lại

Reviewer đọc toàn văn report hiện hành và CURRENT_HANDOFF, đối chiếu từng điểm
R1–R3 cùng các phần tóm tắt, data flow, bảng kế thừa và câu hỏi mở. Report vẫn
là file untracked nên không có base diff riêng; bản hiện hành được đọc trực
tiếp, không dùng diff rỗng làm PASS. HEAD vẫn là
`ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`; worktree có thay đổi sẵn.

Evidence đã xác minh ở mục 3–5 được dùng lại vì reference inputs, code và data
flow không đổi. Reviewer chỉ đọc lại hai vùng metric của
`rag_old_0/evaluation/eval.py:45–106` và `rag_old/evaluation/eval.py:50–115`
để giải quyết cách diễn đạt IDCG/relevance; không chạy code, model, notebook,
test, API hoặc audit lại ba thư mục reference.

### R1 — major, còn mở: executive summary đảo phạm vi mà IDCG không biết

Report hiện hành §1.2 dòng 28 và CURRENT_HANDOFF nói IDCG không biết tài liệu
liên quan bị bỏ sót “ngoài corpus”. Code tạo `relevances` chỉ từ
`retrieved_docs[:k]`, rồi sắp xếp chính danh sách đó để tính IDCG. Giới hạn cần
nêu là IDCG không biết relevant evidence **trong corpus nhưng nằm ngoài
`retrieved_docs[:k]`**; evidence ngoài corpus không phải ground truth retrieval
của closed-world benchmark. §4.3 dòng 188–192 đã nêu đúng hơn, nên report đang
tự mâu thuẫn ở kết luận quan trọng.

Đóng R1 khi sửa đồng bộ executive summary, handoff và mọi bảng/kết luận liên
quan thành đúng `retrieved_docs[:k]` so với toàn bộ relevant evidence trong
corpus. Giữ nguyên phân định: `k` không truyền vào retrieval; MRR/Coverage duyệt
toàn list trả về; nDCG mới cắt `[:k]`; rag_old chỉ dùng `child_chunks[0]`.

### R2 — major, còn mở: vẫn khẳng định vắng các loại case chưa được chứng minh

§1.2 dòng 33 đã phân biệt đúng “150 dòng có text” với chất lượng ground truth,
và §5 đã sửa đúng records 101/141. Nhưng dòng 35 và §7 dòng 353 vẫn nói
reference “thiếu hoàn toàn” negative/partial/conflict cases. Việc schema không
có label riêng và mọi dòng có `reference_answer` chỉ chứng minh chưa phát hiện
ca **được thiết kế/gán nhãn có chủ đích** trong phạm vi đã kiểm; nó không chứng
minh mọi câu answerable hoặc không có case tình cờ mang đặc điểm đó. Hai lỗi
101/141 chính là lý do không thể suy rộng như vậy.

Đóng R2 khi thay các kết luận tuyệt đối bằng phạm vi quan sát được: không có
field/category riêng và chưa xác minh case intentional cho negative,
partial-evidence hoặc same-scope conflict; Huế vẫn cần tạo và audit có chủ đích.
Không audit lại 150 records hay corpus reference để giữ câu “thiếu hoàn toàn”.

### R3 — major, còn mở: attribution và ranh giới khuyến nghị chưa nhất quán

- §1 dòng 15 vẫn gọi báo cáo là “phân tích toàn diện”, trái reading map chỉ đọc
  sâu một số file/vùng; đổi thành khảo sát có mục tiêu trong phạm vi đã liệt kê.
- §4.1 dòng 135 và §4.5 dòng 244 tiếp tục gán trực tiếp nội dung `day4.txt` cho
  “Giảng viên”, dù §2.3 đã xác định đây là tài liệu ghi chép/tổng hợp, không
  phải transcript nguyên văn. Gán claim cho chính tài liệu tổng hợp; không suy
  người nói khi chưa có audio/transcript gốc.
- §4.4 dòng 236 quy chênh lệch 5/4 và 4/3/4 cho “độ biến thiên tự nhiên” dù hai
  mốc khác bối cảnh và không có controlled repetition. Chỉ kết luận hai saved
  observations khác nhau; nguyên nhân chưa được cô lập.
- §4.4 dòng 239 và bảng §6 dòng 332 dùng “bắt buộc” cho exact judge inputs/rubric,
  trong khi §7 dòng 355–356 vẫn ghi đây là vấn đề mở. Groundedness/citation/
  refusal phải được thiết kế, nhưng số tiêu chí, thang điểm và prompt chưa được
  report reference tự chốt. Đổi thành đề xuất để Reviewer/user quyết định.

Pointer `day5.txt:648` + study-guide HTML `:1333`, giới hạn summary keyword,
seed/temperature, phân biệt same-scope conflict với khác điều kiện, và ranh giới
Agentic/dashboard đã sửa đạt. Dòng 5 còn trỏ file chuyển tiếp
`session_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`; đổi sang
canonical `handoff_prompt/...` trong cùng correction để tài liệu nhất quán,
nhưng riêng pointer chuyển tiếp này không làm tăng severity.

## 8. Verdict correction lượt 1 và next action

Decision: `changes_requested`.

Correction lượt 1 đóng được phần lớn nội dung, nhưng R1–R3 chưa đóng vì các
claim còn lại nằm ngay executive summary/bảng khuyến nghị và có thể dẫn thiết
kế Golden/evaluator sai. Correction lượt 2 chỉ sửa các câu được chỉ rõ ở mục 7,
không đọc lại reference, không thêm research hoặc đổi recommendation thành
requirement. Implementer sửa report + CURRENT_HANDOFF, tự kiểm consistency rồi
trả `final_review`. Parser/source locator và Ca Huế VN/QT giữ completed; written
spec và implementation plan vẫn chưa approved.

## 9. Re-review correction lượt 2 — 2026-09-10

### Kết quả R1–R3

Correction lượt 2 sửa đạt toàn bộ delta mục 7:

- R1 đóng: executive summary, §4.3 và bảng §6 đều mô tả IDCG chỉ biết nhãn
  trong `retrieved_docs[:k]`, không biết relevant evidence trong corpus nằm
  ngoài slice đó; cutoff MRR/Coverage/nDCG và `child_chunks[0]` giữ đúng.
- R2 đóng: các absence claims đã giới hạn thành không có field/category riêng
  và chưa xác minh case intentional; records 101/141 vẫn được dùng đúng để
  chứng minh text answer không bảo đảm ground-truth quality.
- R3 đóng: reading scope, attribution day4/day5, hai saved score contexts và
  trạng thái mở của judge rubric đã được sửa nhất quán. Các giới hạn đã đạt ở
  correction 1 tiếp tục được giữ.
- Contract pointer đầu report đã trỏ canonical `handoff_prompt/...`.

Reviewer đọc toàn văn report hiện hành và CURRENT_HANDOFF. Evidence source ở
mục 3–5 được reuse vì inputs/code/data flow không đổi. Không chạy code, model,
notebook, tests, API hoặc audit lại reference. HEAD vẫn là
`ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`; report untracked được đọc trực
tiếp và tracked `git diff --check` sạch.

### R4 — major mới: schema Foods V3 bị ghi sai và quyết định C vẫn bị hỏi lại

Finding này không phải R1–R3 chưa sửa. Nó được phát hiện khi user hỏi liệu
full-corpus Golden chỉ cần giống
`knowledge-base-hue/foods/evaluation/golden_v3.jsonl` và Reviewer đối chiếu
trực tiếp canonical Foods design/data.

Report §7 dòng 347 mô tả Foods V3 là
`{case_id, domain, category, query, relevant_sources, reference_answer}`.
Canonical design
`docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md:131–143`
và mỗi row thật của `golden_v3.jsonl` dùng đúng sáu fields:
`{case_id, question, keywords, reference_answer, category, evidence}`;
`evidence` ánh xạ source path tới exact H2 headings. Report vì thế đang dùng
sai field names và sai representation của baseline được đem ra so sánh.

Ngoài ra, §7 dòng 348 vẫn hỏi source+section hay evidence parts, dù user đã
chọn phương án C ngày 2026-09-10: JSONL đơn giản theo tinh thần Foods V3,
nhưng từng expected claim gắn với `evidence_groups` dùng exact source spans;
chunk IDs không là canonical ground truth. §4.2 dòng 174 và bảng §6 dòng 331
cũng còn recommendation trước quyết định C nên report không nhất quán với
CURRENT_HANDOFF và decision spec.

Tác động: report là input thiết kế Golden; schema baseline sai và câu hỏi cũ
có thể khiến Implementer tạo sai fields hoặc hỏi lại quyết định đã chốt. Đóng
R4 bằng một correction tài liệu hẹp:

1. sửa §7 về đúng sáu fields và semantics `evidence` của Foods V3;
2. ghi rõ user đã chọn C, không hỏi lại source+section hay exact spans;
3. đồng bộ §4.2, bảng §6 và §7: full-corpus vẫn là JSONL đơn giản, evidence
   canonical là claim-level groups + exact source spans, không phải chunk IDs;
4. giữ đúng giới hạn: chỉ đơn vị evidence đã chốt; exact full field set,
   validation, case types, split, quotas, metrics/threshold và judge rubric
   vẫn chưa approved;
5. không tạo/sửa Golden, spec, plan, runtime hoặc đọc thêm reference.

## 10. Verdict correction lượt 2 và next action

Decision: `changes_requested` vì R4 major; R1–R3 đã đóng và không được mở lại.

Implementer sửa đúng ba vùng report nêu trên cùng self-review §8, rồi trả
CURRENT_HANDOFF `final_review`. Evidence R1–R3 và toàn bộ phần reference không
đổi được reuse. Parser/source locator và Ca Huế VN/QT giữ completed; written
spec và implementation plan vẫn chưa approved.

## 11. Re-review correction lượt 3 — 2026-09-10

Correction lượt 3 đạt toàn bộ tiêu chí R4:

- §7 mô tả đúng Foods V3 gồm sáu fields `{case_id, question, keywords,
  reference_answer, category, evidence}` và đúng semantics `evidence`: ánh xạ
  từ relative source path tới danh sách H2 headings chính xác;
- câu hỏi lựa chọn giữa source + section và exact spans đã được bỏ, thay bằng
  quyết định Phương án C của User;
- §4.2, bảng §6 và §7 thống nhất claim-level `evidence_groups` dùng exact source
  spans; chunk IDs chỉ được phân giải theo candidate chunking lúc evaluation;
- report giữ rõ exact full schema, alternative evidence groups, case types,
  validation, quotas/split, thresholds và judge rubric vẫn chưa chốt;
- self-review không tự approve R4 và `CURRENT_HANDOFF.md` trả đúng Reviewer với
  `handoff_kind: final_review`.

Reviewer đã đọc trực tiếp các vùng sửa, tìm các field và câu hỏi cũ trên toàn
report, rồi đối chiếu mục 5 của canonical Foods V3 design và record thật đầu
tiên của `golden_v3.jsonl`. Không còn blocker, major hoặc minor trong correction
scope. R1–R3 giữ trạng thái đóng; R4 được đóng.

Không chạy code, model, notebook, tests, API, Qdrant hoặc benchmark. HEAD vẫn là
`ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`; tracked `git diff --check` sạch và
file report untracked được Reviewer đọc trực tiếp.

## 12. Technical verdict và Approval Closure Contract

Technical verdict: `ready_for_user_confirmation`.

Khảo sát reference Golden/evaluation đạt Review Contract trong phạm vi đọc và
tổng hợp. Kết quả đủ dùng làm evidence cho thiết kế tiếp theo, với các giới hạn
đã ghi trong report: không chứng minh chất lượng toàn bộ 150 records, không phải
benchmark của Huế, không chốt full Golden schema, size, split, thresholds hoặc
exact judge rubric/prompt, và không cấp quyền tạo Golden hay triển khai evaluator.

User confirmation cần thiết: xác nhận chấp nhận khảo sát reference với các
evidence và giới hạn trên. Xác nhận này chỉ đóng khảo sát; không approve written
spec hoặc implementation plan.

Sau khi User xác nhận, Reviewer được cập nhật cơ học:

1. đổi review decision thành `approved` và ghi ngày User confirmation;
2. đổi user report và reference survey status thành `completed`;
3. cập nhật `CURRENT_HANDOFF.md`, context và project status sang completed hoặc
   bước thiết kế kế tiếp theo yêu cầu của User;
4. tiếp tục brainstorming Golden/evidence/evaluation từ các quyết định C, một
   file canonical đích và P7;
5. không commit hoặc push vì phiên này không có quyền Git ghi.

User không cần chạy lại kỹ thuật để xác nhận.

## 13. User confirmation — 2026-09-10

User đã trả lời “xac nhận”. Theo Approval Closure Contract tại §12, khảo sát
reference Golden/evaluation được chuyển thành `approved/completed`.

Approval này chỉ đóng khảo sát và chấp nhận report như evidence thiết kế trong
các giới hạn đã nêu. Written spec và implementation plan vẫn chưa approved;
không phát sinh quyền tạo Golden, chạy evaluator, sửa runtime/corpus/index hoặc
thực hiện Git write.
