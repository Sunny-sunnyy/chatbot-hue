# User Report: Full-corpus RAG Wave 1

Date: 2026-09-12
Status: approved — User closure 2026-09-12

## 1. User nhận được gì

Wave 1 đã tạo pipeline offline cho toàn curated corpus: deterministic discovery,
LF normalization/hash, Markdown parser với source spans, semantic chunking,
condition attachment, deterministic IDs/UUID5 và Representation A preview. Wave
này chưa tạo embedding hoặc ghi Qdrant.

## 2. Hệ thống hiện hoạt động thế nào

Canonical preview phát hiện 205 source files và tạo 8460 chunks. Mọi reported
representation vừa ba tokenizer limits; condition rules được exact-one-match;
artifact báo `PASS`, zero blocking errors và zero oversized groups. Evidence parts
dùng Unicode offsets `[start,end)` trên source LF.

## 3. Reviewer đã quan sát gì

Reviewer đã đọc toàn bộ source/config/test/report/artifact bắt buộc qua các vòng
review, đối chiếu Correction 3 direct assertions và xác nhận không còn
Blocker/Major. Correction 3 chứng minh bằng test source rằng hai lần full chunking
được deep-compare, point IDs là deterministic UUID5, preview outputs được so bytes
và các quan hệ Mệ Kéo/Gia Lạc được kiểm trong exact chunks.

Reviewer không tự chạy tests hoặc preview. Implementer báo fresh offline result
`39 passed, 1 warning`, preview exit 0 và canonical/repeated artifact `cmp` exit 0;
các claim này đã được đối chiếu với source và artifact hiện hành.

## 4. Cách User có thể chạy lại

User không bắt buộc chạy lại để xác nhận closure. Exact offline commands nằm trong
`reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`
và Correction 3 Contract; chúng không gọi model inference hoặc Qdrant.

## 5. Giới hạn và bước tiếp theo

Wave 1 không chứng minh embedding, live Qdrant ingestion, retrieval, generation,
API/frontend, Golden hoặc benchmark. Wave 2.1 vẫn đóng.

User đã xác nhận exact Approval Closure Contract ngày 2026-09-12. Session tiếp
theo thuộc Reviewer/`next_design`: bắt đầu design gate Phase 3/Wave 2.1 bằng
brainstorming từng quyết định còn mở, cập nhật detailed Phase 3 guide và soạn
exact addendum/plan/Review Contract để User duyệt. Chưa giao Implementer hoặc
chạy live action.
