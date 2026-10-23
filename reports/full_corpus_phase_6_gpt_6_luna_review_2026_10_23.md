# Review: Phase 6 gpt-6-luna + Qdrant port amendment

Decision: PASS WITH LIMITATIONS — User chọn Option A và xác nhận closure ngày 2026-10-23
(trước đó: changes_requested → User decision vì correction ceiling, xem §6)
Reviewer: Claude Opus 5.5 (session `hue-rag-66`)
Date: 2026-10-23 (+07)
Canonical guide: `guides/phase_6_generation_api.md`
Amendment: `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`
Implementation report: `reports/full_corpus_phase_6_gpt_6_luna_implementation_2026_10_23.md`

## 1. Phạm vi đã review

- Handoff `final_review` từ Implementer `hue-rag-08`; base `151bc53`, head worktree.
- Exact diff 12 file thuộc amendment §4, cùng report mới và các tài liệu Reviewer
  sở hữu. Không có changed/untracked path ngoài scope. File
  `báo cáo nghiên cứu github.txt` có từ trước, không thuộc task.
- Full implementation report; private artifact `data/full_corpus_phase_6_live_smoke.json`.
- Acceptance gốc: spec 2026-09-14 §live validation (5 calls: Representation B,
  direct fact một citation, synthesis "cần nhiều citations", conditional/
  conflicting evidence, out-of-scope fallback). Model contract theo amendment.
- Retrieval probe chỉ đọc cho hai case có vấn đề, dùng đúng production cell
  `e5-small-384` / `dense_bm25_rrf` / reranker `none`.

## 2. Findings

Không có blocker. Không phát hiện over-engineering trong delta: thay đổi chỉ
gồm giá trị model/URL và các guard tương ứng.

### F1 — major: tiêu chí PASS của `multi_source_synthesis` yếu hơn spec

- Vị trí: `backend/llm/phase6_live_smoke.py` (logic chấm PASS của case
  synthesis) và case 3 trong `data/full_corpus_phase_6_live_cases.json`.
- Requirement: spec 2026-09-14 yêu cầu "một synthesis answer cần nhiều citations".
- Evidence: call 3 PASS dù chỉ cite một source [3]. Retrieval probe cho thấy
  top RRF gần như toàn chunk của **một** tài liệu (`Quần thể Di tích Cố đô Huế`),
  nên câu hỏi hiện tại trả lời được trọn vẹn từ một nguồn.
- Tác động: acceptance item 3 chưa được quan sát. Runner báo PASS cho một hành
  vi không được chứng minh. Lỗi này có từ implementation 2026-10-01, không do delta
  hôm nay gây ra; các review trước đã bỏ sót. Lần này là lần đầu artifact lưu
  `packed_evidence` đủ để thấy rõ.
- Tiêu chí đóng: case synthesis thực sự cần ≥2 tài liệu, và runner chỉ PASS khi
  có ≥2 source khác nhau được cite và hợp lệ; hoặc User chấp nhận đây là
  limitation (option A).

### F2 — major: `conditional_evidence` FAIL do retrieval, không do model

- Requirement: spec yêu cầu một conditional/conflicting-evidence answer.
- Root cause đã chứng minh (probe chỉ đọc, không tốn phí):
  - Câu hỏi gộp hai ý: giá vé Đại Nội và chính sách miễn giảm.
  - Chunk bảng giá vé lẻ (`Vé tham quan Quần thể Di tích Cố đô Huế.md#9`) và
    các chunk tư vấn có giá Đại Nội (#77, #78) **không có trong top-30** của
    dense, BM25 lẫn RRF. Lỗi xảy ra ở bước tìm kiếm, không phải do bước đóng gói
    context (top-5) cắt mất.
  - 5 source được đóng gói chỉ nói về miễn/giảm. Prompt quy định "nếu bằng chứng
    không đủ, trả đúng duy nhất câu fallback", đúng như spec 2026-09-14. Model
    tuân thủ spec.
- Tác động: acceptance item 4 chưa được quan sát. Đây là một điểm yếu thật của
  retrieval (chunk dạng bảng không được tìm thấy cho câu hỏi gộp), thuộc phạm vi
  benchmark retrieval của Phase 8. Thay prompt hay retrieval cell là đổi contract
  đã duyệt, không phải focused fix.
- Tiêu chí đóng: xem các option ở §6.

### Minor (không chặn)

- M1: `finish_reason` luôn `null` vì Responses API không trả field `choices`.
  R2 (reasoning token ăn hết cap) chỉ suy ra từ usage. Có thể ghi
  `response.status`/`incomplete_details` khi Phase 7/8 cần.
- M2: Reviewer không tự start uvicorn `/health` lại. Dùng lại evidence G6 của
  Implementer, vì `app.py` không đổi và config đổi đã được suite cùng
  construction check bao phủ.

## 3. Cách Reviewer chạy lại thật

```bash
git diff --check                                   # exit 0
sha256sum -c <15-file fingerprint>                 # 15/15 OK (trước và sau run)
curl http://localhost:6335/collections             # 15 hue collections
curl http://localhost:6333/                        # Mekong HTTP 200
cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest \
  <9 focused files như report 2026-10-01 §4> -q   # 141 passed, 1 warning in 47.57s
# Read-only retrieval probe (script ngoài repo /tmp/hue_review/): production
# build_full_corpus_retrieval_service("e5-small-384","dense_bm25_rrf","none").search()
# cho case 3 và 4; Qdrant scroll chỉ đọc theo source để định vị chunk bảng giá.
```

Không gọi OpenAI, không mutate Qdrant, không commit.

## 4. Kết quả quan sát

| Kiểm tra | Kết quả | Nguồn |
|---|---|---|
| Diff scope / `git diff --check` | Đạt | fresh Reviewer |
| Fingerprint 15 file | Khớp | fresh Reviewer |
| Focused suite | 141 passed | fresh Reviewer |
| Metadata v2 verify 33.840 trước/sau | VERIFIED | Implementer (G3/P2); runner before/after 8460/8460 trong artifact |
| Artifact | 5 attempts, model `gpt-6-luna` ở cả 5 call, overrides null, 4 PASS / 1 FAIL | fresh Reviewer đọc artifact |
| direct_fact citation audit | Các claim [1], [2][3] đúng với excerpt (Reviewer spot-check); [5] theo audit của Implementer | fresh + reuse |
| out_of_scope | Trả đúng exact fallback, 0 sources | artifact |
| Mekong không bị ảnh hưởng | Container và port 6333 nguyên vẹn | fresh Reviewer |

Ý nghĩa: chuyển sang `gpt-6-luna` hoạt động end-to-end: API, citation integrity,
fallback, an toàn dữ liệu. Lỗi 502 cũ của `direct_fact` không tái diễn. Hai hành
vi "tổng hợp nhiều nguồn" và "giữ điều kiện" **chưa được chứng minh**.

## 5. Giới hạn hoặc phần chưa chạy

- R1 tokenizer `gpt-6-luna`: not verified (tiktoken không biết model).
- R4 `temperature` cho Foods evaluation: not live-verified.
- R5 judge cùng model generator: limitation đã ghi cho Phase 7B/8.
- Không cost accounting (SDK không cung cấp).

## 6. Decision và bước tiếp theo

Phase 6 đã có verdict `changes_requested` ở bốn review: initial, C1, C2, C3.
Theo `REVIEWER_WORKFLOW.md`, Reviewer **không mở correction thứ năm** mà trình
User lựa chọn ở mức thiết kế:

- **Option A (Reviewer khuyến nghị):** đóng Phase 6 với `PASS WITH LIMITATIONS`.
  F1/F2 được ghi là limitation có root cause rõ. Hai hành vi synthesis/conditional
  sẽ được đo đúng bằng Golden full-corpus ở Phase 7, với 150–200 case thay vì 1
  smoke call mỗi loại. Retrieval miss của bảng giá được đưa vào Phase 8 làm case
  cụ thể. Không tốn thêm call, không đổi contract.
- **Option B:** correction theo thiết kế mới. Viết lại case 3 thành câu hỏi bắt
  buộc ≥2 tài liệu. Viết lại case 4 thành câu hỏi chỉ về điều kiện miễn giảm.
  Thêm kiểm tra ≥2 distinct cited sources cho case synthesis trong runner. Probe
  retrieval chỉ đọc trước để chắc evidence có trong top-5. Sau đó dùng contingent
  invocation (5 calls). Rủi ro: chỉnh case sau khi đã thấy FAIL, nên phải ghi rõ
  case cũ FAIL do retrieval, và option này không sửa retrieval miss.
- Option C (không khuyến nghị trong Phase 6): đổi prompt cho phép trả lời một
  phần hoặc đổi retrieval cell. Cả hai là thay đổi contract cần thiết kế riêng.

**Approval Closure Contract (áp dụng nếu User chọn A):**

1. User xác nhận: "Tôi xác nhận Phase 6 (PASS WITH LIMITATIONS)".
2. Reviewer cập nhật: `Project_Status.md` (Phase 6 `approved`, limitation F1/F2,
   R1/R4/R5), `guides/phase_6_generation_api.md` (status/limitation), user report,
   `CURRENT_HANDOFF.md` → `State: completed`, chờ User giao Phase 7A.
3. Git: Reviewer `commit_and_push` (User cấp 2026-10-23) cho 12 file amendment,
   amendment doc, hai report, user report và các tài liệu trạng thái. Không
   commit `data/`, `knowledge-base-hue/`, `qdrant_storage/` hoặc
   `báo cáo nghiên cứu github.txt`.
4. Phase 7A vẫn đóng cho tới khi có brainstorming, spec và plan riêng.

**User decision 2026-10-23: Option A.** Phase 6 `approved` với limitation F1/F2.
Contingent paid authority không dùng và hết hiệu lực. User report:
`reports/user_reports/full_corpus_phase_6_gpt_6_luna_user_report_2026_10_23.md`.
