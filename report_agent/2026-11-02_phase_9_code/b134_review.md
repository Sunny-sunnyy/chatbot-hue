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

## Vòng cuối `456df18..1f2a57c` + bằng chứng có phí (C141 · 11:36 03/11/2026 `date`)

Đầu vào: `origin/p9-b2` = `1f2a57c` (= worktree `/tmp/b_p9b2`, chỉ có `data`, `knowledge-base-hue` symlink untracked); cả nhánh `74c5d68..1f2a57c` (3 commit, 10 file, `git diff --check` sạch); phần mới sau vòng sớm: `e0ca48c` (vòng chỉnh 2 + harness m-1 / m-2) + `1f2a57c` (mặc định `tim_them: true` — User giữ).
Report người làm `b134_b2_implementation.md` `29670b185bd4`. Ca dò (private): `data/phase_9/c141_review/`. Tiền C: **0 USD** (chỉ bắt yêu cầu không gửi + đọc dữ liệu đã chạy).

### 1. Phần code mới (`456df18..1f2a57c`, 5 file +40 / −15)

- `settings.yaml`: `tim_them: true` (chú thích ghi số Q8 + "User giữ 03/11").
- `full_corpus_eval.py` `run_search_layer`: bắt lỗi từng câu ⇒ `error` trong dòng chi tiết, câu lỗi không vào file lượt + `<out>.loi.json` ⇒ **m-1 vòng sớm đóng**; đếm `qua_3_cau` từ lỗi gốc ⇒ **m-2 vòng sớm đóng** (B báo 0 ở pilot / dev / Q2 ⇒ API thật ép `maxItems`). Ghi nhận (không finding): `qua_3_cau` nhận diện bằng chữ trong `repr` lỗi pydantic ("at most 3 items" / "too_long") — đổi bản pydantic có thể đếm hụt; đây là bộ đếm theo dõi, không phải rào.
- `assistant.py`: `trace.model_queries` (câu tìm model viết) chỉ ở RAM / file private của harness — `chat.py` không chép trường này vào log (đã đọc `_copy_trace_metrics`).
- `full_corpus_prompt.py`: lời dặn V3 + `ASSISTANT_TOOL_NOTE` vòng 2 — khớp dòng "Khoá `e0ca48c`" (§5 report) **trước** lượt đo cuối Q2 / Q8.
- `test_api_chat.py`: generator giả thêm đường công cụ (vì mặc định bật).

### 2. Kiểm theo rủi ro (5 điểm A dặn)

| Điểm | Cách C kiểm (khác cách B) | Kết quả |
|---|---|---|
| **(a) Q7** — `tim_them` tắt = B1 giống byte | `probe_q7b.py` (`f04a303bfb0d`): bắt thân **HTTP** (httpx) mọi lần gọi OpenAI, 32 an toàn + 10 smoke qua `answer_case`, cờ mặc định **ép** `tim_them=False` ⇒ so `q7_main.json` C137 (code `main` không đổi từ `f01c032`). Đối chứng: cùng câu với `tim_them=True` | tắt: **42 / 42 giống byte `main`** (2 lần gọi / câu); bật: **0 / 42** giống ⇒ phép so phân biệt được hai đường. **Đạt** |
| **(b) Q8** — N_AA từ A/A của chính B2b; số quyết | Tính lại **độc lập** (không dùng `dc.scored` / `q8_quyet.py`): ghép `judge/scores_*.jsonl` qua `judge/map.json` (436 mục), số chính = trong kho, không `unnatural`, đủ điểm 3 bên ⇒ 129; `paired_stats` của dự án | **khớp B đến chữ số cuối:** N_AA Đủ **5** (ngược 4) / Đúng **5** (ngược 3) ⇒ ngưỡng **8**; tụt V0 ⇒ B2b lượt 1: Đủ **5**, Đúng **2**; TB Đủ +0,2171 [+0,062; +0,388], Đúng +0,2248 [+0,078; +0,395]; **quyết 18 câu nhiều nguồn +1,1667 [+0,444; +2,000]**, 6 / 12 / 0; test 4 câu chênh 0. N_AA đúng plan bản 3 M-4 (A/A lượt 1 ↔ lượt 2 cùng cấu hình B2b, không dùng 6 / 2 của P5). **Thêm (độ vững):** dùng **lượt 2** thay lượt 1 vẫn qua quyết: +0,944 [+0,222; +1,778] > 0. **Đạt** |
| **(c) S-AT** | `diff an_toan_cuoi.py an_toan_b2.py`; đọc `compare_main.json`, `compare_regen.json` | khác **đúng 1 dòng**: mốc = lượt đo cuối 01/11 (RAG 1–8) — đúng mốc spec §4. P0_sai mốc {S11, S12} ↔ B2b {S11, S20} ⇒ ca mới S20 ⇒ sinh lại 3 lần hai bên: **B2b 2 / 3, mốc 0 / 3** ⇒ "mới thật" đúng luật (≥ 2 / 3 và ≤ 1 / 3); dùng 1 / 2 suất cả Phase; 0 câu ngoài kho bị trả lời; "trái nguồn" 1 ⇒ 0. Ghi nhận: hai judge bên B2b **kappa 0** (lệch ở 2 câu, gộp theo luật "một trong hai judge" như B89) ⇒ S20 là cách đọc **bảo thủ**, không phải sai thủ tục. **Đạt** |
| **(d) Q9** — ngắt giữa vòng công cụ, một dòng log, 0 câu hỏi trong log | Đọc log worktree trong khoảng `log_mark.txt` (dòng 386–400); grep chữ 5 câu cổng (`q9/cau_cong.json`) + 10 câu đo chữ đầu (`data/phase_9/b131/questions.jsonl`) | 13 dòng `chat_metrics` + 2 `chat_stream_drain`. Ngắt (1) giữa lượt trợ lý đầu: `client_disconnected`, drain `finished` 0,7 ms, `llm_calls` = [định tuyến]; ngắt (2) giữa chữ: `client_disconnected`, drain 1,3 ms, `llm_calls` = định tuyến + 2 lượt trợ lý, `tools` = 1 lần code + 2 lần model (`n_new` 6, 8) — **mỗi lượt đúng một dòng `chat_metrics`**. Câu hỏi lọt log **0 / 15**, "Received question" 0. **Đạt** |
| **(e) 3 quan sát của B** | đếm trên dữ liệu Q8 thật + ảnh Playwright `q9/ui/` + luồng sự kiện `q9/cong_json_stream.json` | xem m-3…m-5 dưới — **không cái nào chặn merge** |
| test chạm (không key) | `pytest test_b2_tool_loop test_assistant test_assistant_boundary test_chat_stream` trên `1f2a57c` | **41 / 41** (B: có key 9 file 70 / 70) |

### 3. Findings (vòng cuối)

**0 blocker · 0 major · 3 minor** (đều không chặn merge; để B3 / giao diện v2). m-1, m-2 vòng sớm: **đóng**.

- **m-3 — thứ tự trạng thái ở đường có công cụ** (quan sát 2 của B). `assistant.py:400` phát `generating` **trước** `start_tools_stream` ⇒ luồng thật `routing ⇒ searched ⇒ generating ⇒ searching ⇒ searched …` (`cong_json_stream.json`); giao diện hiện "Đang viết câu trả lời…" rồi lại "Đang tìm thông tin…". Xảy ra ở mọi câu model gọi công cụ thêm: Golden **45 / 176** lượt 1 (~26 %). Không sai dữ liệu, chỉ gây hiểu nhầm. **Đóng (B3 / giao diện v2):** ở đường công cụ chỉ phát `generating` khi có `output_text.delta` đầu (hoặc giao diện bỏ qua `generating` khi sau đó có `searching`) + test thứ tự sự kiện.
- **m-4 — model gọi `tim_kho` tới lần 3** (quan sát 1). Đếm trên Q8: Golden 4 / 176 (lượt 1), 1 / 176 (lượt 2); an toàn 2 / 32; **`max_turns` 0**. Lần 3 chỉ trả "đã hết lượt" (không tìm) ⇒ tốn thêm một lượt model. Hiếm, không ảnh hưởng chất lượng đã đo. **Đóng (B3 / B7):** theo dõi tỉ lệ; nếu tăng khi có lịch sử hội thoại thì chỉnh lời dặn công cụ.
- **m-5 — số trích dẫn lớn** (quan sát 3). Ảnh `q9/ui/notice.png`: câu có `[17]` `[4]`, khung nguồn hiện đúng hai mục số **4** và **17** ⇒ ánh xạ đúng (sổ nối số: lần tìm 2 bắt đầu từ `[11]`). Chỉ là chuyện dễ đọc. **Đóng (giao diện v2):** đánh số hiển thị lại theo thứ tự xuất hiện ở tầng giao diện, giữ số máy trong dữ liệu / log.

**Câu bất biến:** "Tắt `tim_them` (cùng `lan_tim_dau: v0`) thì mọi lần gọi model giống byte B1." **Đúng** (42 / 42; bật thì 0 / 42).

### 4. Giới hạn

- Không chạy lại lượt có phí nào; số Q2 / Q8 / S-AT là của B, C tính lại từ dữ liệu đã lưu (không sinh lại). Không đọc lại chữ câu trả lời / không chấm lại.
- Q7 C kiểm trên 42 câu (B 228); Playwright giao diện chỉ xem ảnh của B.
- Bài học B ghi (+3 của V2 ở vòng chỉnh 2 là dò theo nhiễu) — C đồng ý: lượt khoá 2 lượt không lặp lại.

### 5. Kết luận vòng cuối

**`ready_for_user_confirmation`** cho nhánh `p9-b2` `1f2a57c` (B2a giữ V0 — kết quả âm có hồ sơ; B2b `tim_them` bật — quyết + sàn đạt, S-AT dùng 1 / 2 suất, User đã giữ). m-3…m-5 chuyển B3 / giao diện v2.
