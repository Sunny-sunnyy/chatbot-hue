# Implementer — đo hai input Ca Huế đã sửa ranh giới

> Completed/user-approved. Đây là contract lịch sử, không quyền chạy lại.
> Closure: `reports/full_corpus_vn_qt_token_check_codex_review_2026_09_09.md`,
> mục 6. Trạng thái task mới chỉ nằm trong session_prompt/CURRENT_HANDOFF.md.

Trạng thái: contract khảo sát bổ sung phục vụ thiết kế, do Reviewer giao theo
yêu cầu user. Không phải correction khảo sát parser đã approved hoặc quyền
triển khai MVP trước spec/plan approval. Dùng khi CURRENT_HANDOFF trỏ tới đây.

## Đọc và quyền

Đọc theo thứ tự:
1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. Contract này; áp dụng `skills/risk-gated-agent-review/SKILL.md` và
   `skills/practical-project-coding/SKILL.md` theo workflow.
6. `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`, mục 19
   (snapshots/preprocessing), 25–26 (queries/evidence), 28–32 (trạng thái).
7. `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`, các
   mục schema/locator, packing/condition mapping và trạng thái mẫu.
8. `reports/full_corpus_parser_locator_codex_review_2026_09_09.md`, mục 9–10.

Inputs đọc chọn lọc, không audit lại toàn bộ artifacts:
- `reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json`:
  đúng hai composites VN/QT đã correction, có search_text và evidence_parts.
- `reports/artifacts/full_corpus_chunk_samples_2026_09_09.json` và script
  cùng tên `.py`: chỉ queries cuối và cách tokenize; không chạy script cũ
  vì nó ghi lại artifact khảo sát lịch sử.
- `knowledge-base-hue/travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`:
  chỉ vùng nguồn của các parts hai composites để đối chiếu.

Kiểm read-only git status/HEAD; HEAD dự kiến
`ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`. Worktree có thay đổi sẵn; bảo toàn.
Không .env, inference/model weights, API/Qdrant/benchmark, mạng/downloads,
cài dependencies, sửa runtime/backend/tests/corpus/index/settings, Git mutation
hoặc subagent. Chỉ dùng project uv/environment và tokenizer cache sẵn có.
Nếu thiếu cache/dependency hoặc cần quyền khác, báo blocker; không tự tải.

## Mục tiêu và cách thực hiện

Đo full-input tokens của đúng hai search_text đã sửa trong JSON parser để
Reviewer biết chúng vừa giới hạn ba embedding models hay chưa. Không chọn
chunking winner hoặc gọi kết quả này là quality evidence/full-corpus coverage.

1. Tìm hai composite bằng source và body span, không lấy mẫu tokenizer sai:
   VN `[10901,11141)`, QT `[11142,11317)`. Mỗi composite gồm lead + header +
   nguyên hàng + Không bao gồm. Độ dài search_text đã ghi nhận là 931/866 ký
   tự, chỉ dùng kiểm đúng input, không suy token counts từ ký tự.
2. Đối chiếu parts với source UTF-8 strict, CRLF/CR → LF, Unicode `[start,end)`;
   không Unicode-normalize hoặc sửa whitespace. Nếu JSON/source/boundary
   không khớp, dừng phần đo phụ thuộc và báo rõ; không tự sửa input.
3. Giữ nguyên search_text từ artifact, không thay format theo spec đang thảo
   luận. Ghi rõ phép đo áp dụng representation mẫu này, không tự là acceptance
   của một representation runtime khác. Không đổi labels/queries cho dễ vừa.
4. Tokenize riêng E5-small, E5-base, HuyDang bằng exact snapshots mục 19,
   `local_files_only=True`, `truncation=False`, gồm special tokens. E5 thêm
   `passage: `; HuyDang dùng PyVi trên search_text, không E5 prefix.
5. MiniLM tokenize cặp `(query, search_text)` với cả query_orig/query_long
   Ca Huế đã cố định ở context mục 26, không E5 prefix; không truncation.
6. Ghi version thực tế/tokenizer revisions và input limit lấy từ config có
   sẵn; kỳ vọng tham chiếu E5 512, HuyDang 256, MiniLM pair 512. Nếu khác
   snapshots/config đã ghi, báo khác biệt thay vì tự đổi model/cấu hình.

Được viết/chạy một script nhỏ mới để làm các bước trên; không production
chunker, không test suite/validator framework. Nếu có input vượt, ghi model,
count và phần vượt; chưa chia lại input hoặc mở thêm khảo sát. Chặn ingest
khi nhóm tối thiểu vẫn vượt là lựa chọn A đã chốt, nhưng hai input này chưa
được chứng minh là nhóm bất khả chia.

## Outputs và acceptance

Chỉ tạo ba artifacts mới:
- `reports/full_corpus_vn_qt_token_check_2026_09_09.md`
- `reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.json`
- `reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.py`

Report ngắn gồm exact command, actual environment/revisions, đối chiếu nguồn,
bảng hai hàng VN/QT với E5-small/E5-base/HuyDang/MiniLM orig/long, counts và
limits, kết luận vừa/vượt cho từng input, giới hạn và lỗi/blocker nếu có.
JSON giữ hai input/parts/queries cùng counts thực để tái lập. Không sửa reports/
JSON/scripts lịch sử, spec/plan/guides/status hoặc tự ghi approved.

Acceptance: đúng hai inputs; đủ counts không truncation cho các tokenizers
nêu trên; query/prefix/PyVi đúng; không phục hồi counts cũ của input sai;
không đổi nguyên văn hoặc vượt allowed paths. Nếu không chạy được thì ghi
not_measured/blocked đúng phần, không tạo expected output làm PASS.

Tự review script/output và git diff --check; nhớ lệnh đó không kiểm nội dung
untracked. Kết thúc bằng report ngắn cho user và prompt chuyển Reviewer đọc
report/JSON, không yêu cầu user tự tổng hợp. Được cập nhật CURRENT_HANDOFF
thành final_review cho Reviewer, giữ authority/risk, dẫn contract/report này
và ghi phần chưa đạt nếu có. Không sửa verdict/approval hoặc context thay Reviewer.

Review Contract: risk low, không đổi runtime; Reviewer kiểm đúng inputs,
preprocessing/revisions và bảng kết quả qua script/artifacts có mục tiêu.
Chỉ rerun khi có thiếu sót/mâu thuẫn ảnh hưởng kết luận, không mặc định lặp đo.
Sau review trả về written spec; không coi số đo là approval schema hoặc MVP.
