# Review: Phase 9 B2 (nhánh `p9-b2`, B134)

## Vòng sớm `456df18` (C137 · 10:19 03/11/2026 `date`)

Người kiểm: C (Claude Opus 5.5) — viết bộ đo B2 (C133), không code B2. Đối chiếu plan B2 **bản 3 `efa27cb8207c`** (C135 vòng 3 ready). `risk-gated-agent-review`. 0 USD (B đang chạy pilot có phí, không đo latency ⇒ C chỉ chạy việc 0 USD, nhẹ).
Ca dò của C (private): `data/phase_9/c137_review/`.

### 1. Cổng tối thiểu

- `origin/p9-b2` = `456df18` (1 commit trên `main`), worktree B `/tmp/b_p9b2` ở `456df18`.
- 9 file, +712 / −73:
  - `llm/assistant.py`, `llm/generator_openai_full_corpus.py`, `llm/full_corpus_prompt.py`;
  - `retrieval/full_corpus.py` (`search_many`), `retrieval/full_corpus_context.py`;
  - `api/routes/chat.py` (`routing_ms`), `evaluation/full_corpus_eval.py` (`tang_tim`, `--lan-tim-dau`);
  - `config/settings.yaml` (`lan_tim_dau: v0`, `tim_them: false`), `tests/test_b2_tool_loop.py` (mới).
- Không file ngoài plan §3; `frontend/` không sửa (D7 dùng lại nhãn có sẵn).
- `git diff --check main...456df18` sạch.

### 2. Kiểm theo rủi ro

| Mục (plan bản 3) | Cách C kiểm | Kết quả |
|---|---|---|
| **Q7** gỡ được (`v0` + `tim_them` tắt = B1 giống byte) | `probe_q7.py` (`d1edaa151245`). Khác cách B: bắt thân **HTTP** ở `httpx.AsyncClient.send` (B bắt kwargs). Cờ **mặc định** `settings.yaml` (router + notice bật). 32 câu an toàn + 10 smoke qua `answer_case`, chạy trên `main` và trên nhánh | **42 / 42 câu giống byte**, mỗi câu 2 lần gọi (định tuyến + trả lời) ở cả hai bên (`q7_main.json` `d1ffe407c1b6` = `q7_branch.json` `2a49d65244b9` theo từng câu). Đạt |
| **Lệch D2** — bỏ "cắt 3 câu" của V3 | `probe_d2.py` (`7b7ac2c5d2f3`): `AgentOutputSchema(RouteSplitOutput)` của SDK 0.19.4 | schema strict có `maxItems: 3`. 3 câu ⇒ nhận; **4 câu ⇒ SDK chặn (`ModelBehaviorError`)**. `_run` đổi mọi lỗi thành `GenerationError` (`generator…:308-313`) ⇒ `_pick_route` đặt `router_failed` + `tro_ly_hue`. Lệch đúng **về kỹ thuật**; hệ quả ⇒ m-2 |
| Lỗi định tuyến V1 / V3 ⇒ tìm bằng câu gốc thật | `probe_d2.py`: generator giả (route_search ném `GenerationError` / trả câu toàn khoảng trắng / trả câu thường); dịch vụ tìm giả ghi câu được tìm; chạy `answer_turn` thật | lỗi ⇒ tìm **đúng câu gốc**, `route_error=router_failed`; câu toàn khoảng trắng ⇒ câu gốc + `cau_tim_rong=True`; câu thường ⇒ câu định tuyến viết. Đúng ở cả V1 lẫn V3. Harness `tang_tim` cùng luật (`full_corpus_eval.py` `run_search_layer`) |
| D3 câu tìm ↔ câu hỏi | Đọc `search_into_trace`: ngân sách đếm bằng `cau_hoi`; V0 truyền câu gốc cho cả hai | đúng; Q7 trên xác nhận V0 không đổi byte |
| D4 `search_many` | Đọc: 1 câu ⇒ `search`; nhiều câu ⇒ `reciprocal_rank_fusion(k=rrf_k, limit=candidate_pool)` (chữ ký khớp `full_corpus.py:105`); bỏ trùng theo id; tất định | đúng. Ghi nhận (không finding): `score` của đoạn sau trộn vẫn là điểm của lần tìm đầu thấy nó, không phải điểm RRF mới — hôm nay không chỗ nào dùng `score` sau bước này |
| D5 sổ nối số + ngân sách | Đọc `full_corpus_context.build`: `first_id`, `skip_ids`, `prior_context`, `instructions`. Hết ngân sách ở lần tìm thêm ⇒ ít / 0 đoạn (chỉ lần đầu `ContextBudgetError`). ≤ 10 đoạn mỗi lần | đúng plan D5 (m-4 C135) |
| D5 trần + m-6 C135 | `tool_for_turn`: `MODEL_SEARCH_LIMIT` 2, lần 3 trả `TOOL_LIMIT_TEXT`, không tìm. `_assistant_for` dựng công cụ + handler + `state` **mỗi lượt**; test `test_concurrent_turns_do_not_share_max_turns_flag` | đúng; m-6 đóng |
| V2 khi model không gọi `tim_kho` | `grep trace.packed`: mọi chỗ đọc đều kiểm None hoặc nằm sau `prepare_answer` (đường đã tìm trước) | không lỗi `None` |
| D10 token = tổng mọi lượt | Đọc `_generated_text`: cộng `usage` của mọi `raw_responses`; một lần gọi ⇒ đúng số cũ (Q7 xác nhận chuỗi không đổi; số token một lần gọi giữ nguyên) | đúng |
| T-3 ranh giới | `function_tool` chỉ ở generator; lõi đưa closure thường; `test_assistant_boundary.py` pass | đúng |
| test chạm | `pytest tests/test_b2_tool_loop.py tests/test_assistant.py tests/test_assistant_boundary.py tests/test_chat_stream.py` (không key) | **41 / 41 pass** |

**Câu bất biến:** "Câu tìm của mọi lượt không bao giờ là chuỗi rỗng, và định tuyến lỗi thì luôn tìm bằng câu gốc." **Đúng** ở 6 / 6 ca dò (3 tình huống × V1 / V3).

### 3. Findings (vòng sớm)

**0 blocker · 0 major · 2 minor.**

#### m-1 (minor) — harness `tang_tim`: một câu lỗi làm hỏng cả lượt có phí

- **Vị trí:** `evaluation/full_corpus_eval.py` `run_search_layer`: `asyncio.gather(*(one(case) …))` không `return_exceptions`, và `one()` không bắt lỗi.
- **Hệ quả:** ở V2, `first_tool_search` ném `GenerationError` khi hết giờ hoặc lỗi API. Lỗi tìm trong công cụ (`RetrievalDependencyError`) cũng ném thẳng. Chỉ một câu lỗi là cả lượt 61 / 43 câu dừng, không ghi dòng nào ra file, mà tiền các câu đã chạy vẫn mất.
- **Tác động:** nhỏ (một lượt ≈ 0,01 USD), nhưng lặp ở pilot / chỉnh / Q2.
- **Đóng:** bắt lỗi từng câu, ghi `error` vào dòng chi tiết. Lượt có câu lỗi thì chạy lại riêng câu đó, rồi mới đưa vào `cham` (`cham` cần đủ câu). Hoặc ghi rõ cách làm này trong report.

#### m-2 (minor) — lệch D2: V3 trả > 3 câu ⇒ mất luôn **tuyến**, không chỉ câu thứ 4

- **Vị trí:** `generator…` `route_search` (docstring), `assistant._pick_route`.
- Plan bản 3 D2 ghi "code lấy 3 câu đầu". Như vậy vẫn giữ được tuyến mà định tuyến đã chọn. Bản code dựa vào SDK chặn ⇒ cả đầu ra định tuyến bị bỏ ⇒ `router_failed` ⇒ `tro_ly_hue`, **kể cả câu khẩn cấp / ngoài phạm vi**. Đây cùng loại với "định tuyến lỗi ⇒ đường cũ" mà B1 D3 đã chấp nhận, nhưng là một đường gây lỗi mới.
- Chỉ xảy ra khi API thật **không** ép `maxItems` mà model vẫn viết ≥ 4 câu. Pilot cho biết điều đó.
- **Đóng:**
  - ghi "Lệch D2" vào report kèm lý do + bằng chứng (`probe_d2.py`, hoặc test của B);
  - ở pilot / Q3 / Q5 của V3, báo số `route_error` và số lỗi do > 3 câu;
  - nếu > 0 thì quay về cắt 3 câu: đọc đầu ra không strict, hoặc bỏ `max_length` rồi cắt trong code.

### 4. Giới hạn

- Chưa chạy đường thật nào có model (pilot của B đang chạy; vòng sớm 0 USD). V2 / B2b, vòng công cụ trên model thật, chênh ngân sách so `usage` thật (m-7 C135), stream nhiều lượt + thẻ công cụ trên trình duyệt ⇒ review cuối.
- Không chạy lại Q1 (T1 158 câu, B báo đạt). Q7 C kiểm độc lập trên 42 câu, không phải 228.
- Lời dặn V1 / V3 / công cụ chỉ đọc, chưa đánh giá chất lượng (đo ở Q2 / Q6).

### 5. Kết luận vòng sớm

**Không có finding chặn** ở `456df18`. Lệch D2 đúng kỹ thuật (SDK chặn > 3 câu; lỗi ⇒ câu gốc). m-1, m-2 sửa hoặc ghi lại trước lượt đo cuối Q2. Review cuối chỉ xem `456df18..<cuối>` + bằng chứng có phí.
