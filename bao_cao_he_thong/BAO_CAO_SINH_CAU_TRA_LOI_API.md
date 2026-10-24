# Báo cáo cho bạn: Sinh câu trả lời, API và giao diện (Phase 6)

**Cập nhật lần cuối: 19:32 24/10/2026 — bản 3: đính chính §5 — "Representation B" đã được gọi thử thật
1 lần ở Phase 6, chỉ chưa có chỉ mục (bản 2 ghi "chưa từng dùng").**
Người viết: C · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chatbot Huế **trả lời câu hỏi trên toàn bộ kho dữ liệu** (món ăn, di tích, lễ
  hội, nghệ thuật, du lịch) qua một API và một trang web đơn giản. Mỗi câu trả lời có trích dẫn `[1]`,
  `[2]`… trỏ tới đoạn nguồn thật; không tìm thấy thông tin thì nói không đủ thông tin, không bịa.
- **Đang chạy cách nào:** lấy tối đa 5 đoạn nguyên vẹn từ bước tìm kiếm → `gpt-6-luna` (OpenAI) viết
  câu trả lời chỉ từ 5 đoạn đó → backend kiểm từng `[n]`. Trạng thái: đã đóng 23/10/2026, đạt kèm hai
  giới hạn (bảng giá, tổng hợp nhiều nguồn).
- **Đo được (Phase 7B, 176 câu):** Đúng / Đủ / Trúng ý **4,43 / 4,28 / 4,45** (thang 1–5); khi đã trả
  lời thì gần tối đa (~4,9). Từ chối đúng 18/18 câu ngoài kho. Lỗi trích dẫn 4/176.
- **Giới hạn chính:** **từ chối nhầm 22/158** câu có trong kho — nguồn mất điểm lớn nhất; không tìm ra
  bảng giá; câu cần nhiều nguồn lúc đóng chỉ dùng 1 nguồn.
- **Chi phí:** sinh 176 câu ~0,024 USD (~600 đồng). Mỗi câu hỏi trên web có phí rất nhỏ.
- **Bạn cần quyết gì (Phase 8):** khi chỉ có bằng chứng cho một phần câu hỏi, bot **trả lời phần có
  căn cứ (nói rõ phần thiếu)** hay **từ chối cả câu** như hiện nay (xem §6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
trang web / POST /api/chat {"query": "..."}
 → tìm 10 đoạn (Phase 5) → lấy tối đa 5 đoạn nguyên vẹn, vừa ngân sách token
 → gpt-6-luna viết câu trả lời, chỉ dùng 5 đoạn đó, đặt [n] sau mỗi ý
 → backend kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources} — hoặc lỗi có mã rõ ràng (vd. 500 nếu trích dẫn hỏng)
```

- Khi khởi động, hệ thống so "dấu vân tay" dữ liệu với chỉ mục; dữ liệu đổi mà chưa build lại thì
  từ chối chạy.
- Câu hỏi 1–500 ký tự (sau khi bỏ khoảng trắng đầu/cuối).
- Ví dụ: hỏi về đồi Vọng Cảnh → câu trả lời có `[1]`; bấm `[1]` trên trang web sẽ cuộn tới thẻ nguồn
  ghi tiêu đề, mục và đoạn trích nguyên văn.
- Code: `backend/api/routes/chat.py` (API), `backend/retrieval/full_corpus_context.py` (chọn 5 đoạn),
  `backend/llm/full_corpus_prompt.py` (prompt), `backend/llm/generator_openai_full_corpus.py` (gọi
  model), `backend/llm/citations.py` (kiểm trích dẫn), `frontend/` (trang web).

Tự hỏi chatbot (không bắt buộc): bật Qdrant (`docker compose up -d`), chạy API từ `backend/`
(`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`), mở
`http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (có phí rất nhỏ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu có đủ bằng chứng trong 5 đoạn → trả lời kèm `[n]` | **Đã xử lý, đóng gói** | 4,43 / 4,28 / 4,45 trên 176 câu; khi đã trả lời ~4,9 |
| Câu ngoài kho → từ chối, không bịa | **Đã xử lý, đóng gói** | 18/18 từ chối đúng |
| Kiểm `[n]` trỏ đúng nguồn, lỗi thì trả mã rõ ràng | **Đã xử lý, đóng gói** | 4/176 câu người dùng thấy lỗi 500; `backend/llm/citations.py:12` |
| Trang web bấm `[n]` tới thẻ nguồn | **Đã xử lý, đóng gói** | `frontend/`; `backend/api/app.py:147–151` |
| Dữ liệu lệch chỉ mục → từ chối khởi động | **Đã xử lý** | `backend/retrieval/full_corpus.py:353,415` |
| Câu có một vế có bằng chứng, vế kia thiếu | **Xử lý một phần** | Prompt bắt từ chối cả câu (`full_corpus_prompt.py:14`); 10/22 câu từ chối nhầm thuộc loại này; chờ bạn quyết |
| Đoạn chứa đáp án nằm ngoài 5 đoạn ngữ cảnh | **Xử lý một phần** | 8/22 câu từ chối nhầm; thử 10 đoạn ở dòng dưới |
| Có đủ bằng chứng mà vẫn từ chối | **Xử lý một phần** | 4/22 câu từ chối nhầm |
| Đưa 10 đoạn ngữ cảnh thay vì 5 | **Đã thử, chưa áp dụng** | Thử nhanh: 10/22 câu hết từ chối, chưa chấm đúng/sai; Phase 8 đo đủ |
| Câu tổng hợp nhiều nguồn | **Xử lý một phần** | Lúc đóng đạt nhưng chỉ dùng 1 nguồn; chưa chứng minh tổng hợp |
| Câu hỏi giá vé + miễn giảm (bảng giá) | **Chưa thực hiện** | Không tìm ra bảng giá (xem `BAO_CAO_TIM_KIEM.md`) |
| Tách câu hỏi hai ý | **Chưa thực hiện** | Phase 8 thử |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 24/10/2026 — Đính chính về "Representation B" (bản 3)
Khi rà quyết định Phase 8.1: phần sinh ngữ cảnh B đã được gọi thử thật 1 lần ở Phase 6 (đạt); cái chưa
có là chỉ mục dựng từ B và phép đo tìm kiếm. Bản 2 ghi "chưa từng dùng" là nhầm. Không đổi số đo nào.

### 24/10/2026 — Đo đủ 176 câu (Phase 7B, cùng code Phase 6, chỉ mục 7A2)
Cách đo: chatbot thật trả lời, Claude chấm so với đáp án mẫu · kết quả: đo mốc (chưa đặt ngưỡng) —
Đúng/Đủ/Trúng ý 4,43 / 4,28 / 4,45; từ chối đúng 18/18; từ chối nhầm 22/158 (8 đoạn đáp án không vào
ngữ cảnh, 10 có một vế thiếu vế kia, 4 có đủ mà vẫn từ chối); lỗi trích dẫn 4/176 · tiền sinh 176 câu
~0,024 USD (~600 đồng).
Thử nhanh 10 đoạn ngữ cảnh trên 22 câu từ chối nhầm: 10/22 câu hết từ chối — **chưa chấm** đúng/sai,
chỉ là dấu hiệu; **chưa áp dụng**, chờ Phase 8.

### 23/10/2026 — Đóng Phase 6 trên `gpt-6-luna`
Cách đo: 5 câu thật · kết quả: **PARTIAL** — 4 đạt / 1 không đạt (câu "giá vé + miễn giảm": không tìm
ra bảng giá); câu tổng hợp nhiều nguồn đạt nhưng chỉ dùng 1 nguồn · giữ, đóng kèm hai giới hạn.

### Trước 23/10/2026 — Đổi model sinh nhiều lần (bản toàn kho)
Qwen 3.5-9B qua OpenRouter → `gpt-5.4-nano` → `gpt-6-luna` · hai model đầu **đã bỏ**, thay bằng
`gpt-6-luna` (quyết định 23/10).

### 08/2026 — Bản món ăn (`gpt-5.4-nano`)
Nay **đã bỏ** và hỏng thật: đường sinh câu trả lời bản món ăn gửi tham số `temperature` nên
`gpt-6-luna` trả lỗi 400; nằm trong danh sách dọn.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `54670a0`) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| API `POST /api/chat`, trả `{answer, sources}`, câu hỏi 1–500 ký tự | **còn dùng** | `backend/api/routes/chat.py:24–26,48` |
| Model sinh `gpt-6-luna` (OpenAI) | **còn dùng** | `backend/config/settings.yaml:117` |
| Tối đa 5 đoạn nguyên vẹn, ngân sách 16.384 token | **còn dùng**; Phase 8 sẽ thử 10 đoạn | `settings.yaml:123,126`; `backend/retrieval/full_corpus_context.py` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng**; Phase 8 xem xét cho trả lời phần có căn cứ (bạn quyết) | `backend/llm/full_corpus_prompt.py:14` |
| Backend kiểm trích dẫn, lỗi trả mã rõ ràng | **còn dùng** | `backend/llm/citations.py:12`; `backend/api/routes/chat.py` |
| Trang web tối giản, bấm `[n]` tới thẻ nguồn | **còn dùng** | `frontend/`; `backend/api/app.py:147–151` |
| Từ chối chạy khi dữ liệu lệch chỉ mục | **còn dùng** | `backend/retrieval/full_corpus.py:353,415` |
| Qdrant cổng 6335 | **còn dùng** | `settings.yaml` `vector_database.url` |
| Qwen 3.5-9B qua OpenRouter, `gpt-5.4-nano` | **đã thay** bởi `gpt-6-luna` (quyết định 23/10) | [R3] |
| Collection metadata v2 (8.460 đoạn) mà Phase 6 đóng trên đó | **đã thay** bởi chỉ mục 7A2 (8.459 đoạn) | `Project_Status.md` §4 |
| "Representation B" (LLM viết thêm ngữ cảnh cho đoạn) | **có code; đã gọi thử thật 1 lần ở Phase 6, chưa có chỉ mục, chưa đo** | `backend/llm/full_corpus_prompt.py:37`; `backend/llm/representation_b.py` |
| API/sinh câu trả lời bản món ăn | **đã bỏ, hỏng thật** (gửi `temperature` → lỗi 400); nằm trong danh sách dọn | `backend/llm/generator_openai.py:30,44` |

## 6. Việc còn lại / cần quyết

- **Bạn quyết (Phase 8):** trả lời phần có căn cứ hay từ chối cả câu. Spec chung của dự án cho phép
  "trả phần có căn cứ", nhưng spec Phase 6 và prompt hiện tại bắt từ chối cả câu; code đúng theo spec
  Phase 6. Đây là nguồn chính của 10/22 câu từ chối nhầm.
- Lỗi bảng giá và tổng hợp nhiều nguồn vẫn còn (xem `BAO_CAO_TIM_KIEM.md` và `BAO_CAO_DANH_GIA.md`).
- Phase 8 sẽ thử: 10 đoạn ngữ cảnh, prompt cho trả lời phần có căn cứ, tách câu hỏi hai ý.

## Phụ lục — hồ sơ kỹ thuật

- Mã giới hạn: tổng hợp nhiều nguồn = **F1**; bảng giá = **F2**. Câu hỏi "trả lời một phần" = **H8**
  trong [R1].
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- [R3] đổi model: `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`.
- Chẩn đoán từ chối nhầm: `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`; thử 10 đoạn:
  `reports/phase_8_probe_context_top10_2026_10_24.md`.
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C12): đính chính theo `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` dòng 6.10 và §6 mục 13.
- **Lệch phát hiện (24/10):**
  - Spec umbrella `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` §1, Decision #6a
    cho phép "trả phần có căn cứ", nhưng spec Phase 6 (2026-09-14 §10) và prompt bắt từ chối cả câu.
    Code đúng theo spec Phase 6; đã báo A từ C1.
  - Guide `guides/full_corpus_rag.md` (Decision #6d, lịch sử) còn ghi "dùng `AsyncOpenAI` trực tiếp,
    không Agent/Runner"; code dùng OpenAI Agents SDK một lượt, không tool
    (`backend/llm/generator_openai_full_corpus.py`) — **đúng** theo amendment 2026-10-01 §SDK boundary
    (`docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md:29,59`). Không phải lỗi
    code; chỉ là đoạn guide lịch sử dễ gây hiểu nhầm.
