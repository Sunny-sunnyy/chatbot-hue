# Codex Review: hai input Ca Huế VN/QT đã sửa ranh giới

Decision: approved
Reviewer: Codex
Date: 2026-09-09
Contract: `handoff_prompt/FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md`
Implementation report: `reports/full_corpus_vn_qt_token_check_2026_09_09.md`

## 1. Phạm vi đã review

Đọc toàn bộ script/JSON/report mới và final_review handoff; đối chiếu contract,
hai composites JSON parser, source slices, snapshots/preprocessing/queries
canonical đã đọc. HEAD ea87d3ed52851f6b6ab5c47b138540ebc8ff8340. Worktree có
thay đổi sẵn; ba artifacts mới là untracked, đã đọc toàn văn thay vì coi Git
diff là đầy đủ. Không audit các docs thay đổi sẵn hoặc chạy survey cũ.

## 2. Findings

Không có blocker/major trong phạm vi đo hai input.

Ghi chú không chặn: câu “nghiệm thu đạt 100%” trong implementation report chỉ
là tuyên bố Implementer, không phải approval Reviewer/user. Claim “45 từ” và
“margin an toàn” không dùng làm contract; evidence là exact query/input cùng
counts token. Không mở correction chỉ để biên tập các câu này.

Bản thảo spec của Reviewer từng mô tả nối mọi parts bằng một LF, trong khi
mẫu parser/đo có hai LF giữa lead–bảng và bảng–Không bao gồm. Đây là khác biệt
representation ở spec, không lỗi Implementer: contract yêu cầu giữ nguyên
search_text parser. Reviewer chỉnh mô tả spec cho bảng ghép theo mẫu; không
gắn counts này vào text khác. Không cần rerun tokenizer cho input không đổi.

## 3. Cách Reviewer kiểm thật

Read-only `git status --short`, `git rev-parse HEAD`, `git diff --name-only`,
`git ls-files --others --exclude-standard`, `git diff -- CURRENT_HANDOFF.md`
(dùng path session_prompt đầy đủ khi chạy), `git diff --check`; đọc script,
report và JSON. Dùng jq với `--slurpfile` JSON parser và `--rawfile` source:
so search_text/metadata/parts với parser, so cả tám parts với source LF.
Kiểm thêm ghép label + lead + hai LF + header + LF + row + hai LF + exclusions.
Không chạy Python, tokenizer, inference, API hoặc Qdrant.

## 4. Kết quả quan sát

Hai search_text, metadata và parts đều bằng artifact parser; cả tám parts
khớp source slices. Phép so bản ghép một LF trả false ở cả hai mẫu; bản ghép
đúng khoảng cách paragraph/table trả true ở cả hai. Script dùng tokenizers
đúng local snapshots, prefix/PyVi/pair, add_special_tokens và truncation=False.
Configured limits khớp model_max_length attributes được ghi trong JSON;
revisions và queries khớp contract. Report/JSON thống nhất bảng sau:

| Mẫu | E5-small | E5-base | HuyDang | MiniLM orig/long |
|---|---:|---:|---:|---:|
| VN, 931 ký tự | 290 | 290 | 224 | 411/453 |
| QT, 866 ký tự | 268 | 268 | 208 | 385/427 |
| Limit | 512 | 512 | 256 | 512/512 |

Counts là evidence thực thi Implementer, được Reviewer kiểm code/artifact,
không phải lần đo độc lập của Reviewer. Không có mâu thuẫn cần rerun.
Git diff --check đạt tracked diff; không thấy tracked runtime/corpus changes.

## 5. Giới hạn hoặc phần chưa chạy

Không rerun tokenizer/environment/config file reads; version/attributes thực
thi đến từ artifact. Không có Git base/snapshot toàn bộ untracked files trước
task để chứng minh chúng đều bất biến. Không tuyên bố worktree sạch hoặc
diff-check kiểm mọi untracked artifact. Khảo sát chỉ chứng minh độ dài hai
inputs và hai queries đã định, không quality RAG, mọi query hoặc toàn corpus.
Script khảo sát không phải validator production; không yêu cầu harden cho
các inputs/cấu hình giả định ngoài task. Spec/runtime chưa approved.

## 6. Decision và Approval Closure Contract

Technical verdict: ready_for_user_confirmation, không yêu cầu correction.
User report: `reports/user_reports/full_corpus_vn_qt_token_check_user_report_2026_09_09.md`.
User xác nhận chấp nhận khảo sát hai input với giới hạn nêu trên; không cần
tự chạy lại. Chưa coi việc user chuyển report hoặc chọn non-streaming là
xác nhận khảo sát. Reviewer vẫn được tiếp tục phần thiết kế độc lập.

Sau xác nhận, Reviewer đổi Decision thành approved, ghi confirmation trong
review này; đồng bộ context mục 33/Project_Status/prompt và chuyển handoff về
next_design cho Reviewer. Giữ counts mới làm evidence đúng hai inputs, không
đổi artifacts lịch sử hoặc runtime. Checks closure: status/links nhất quán,
git diff --check. Git/subagent authorization none. Written spec rồi plan vẫn
cần user duyệt riêng; không cần giao Implementer closure cơ học.

### User confirmation và closure

User trả lời “xac nhận” sau tóm tắt Reviewer và các giới hạn. Khảo sát hai
input VN/QT approved/completed. Reviewer đồng bộ trạng thái, giữ số đo và
giới hạn, chuyển handoff về next_design. Không chạy lại tokenizer hoặc sửa
artifacts Implementer. Approval không duyệt written spec/plan. Technical
verdict/contract phía trên giữ lịch sử trước xác nhận; không còn chờ xác nhận.
