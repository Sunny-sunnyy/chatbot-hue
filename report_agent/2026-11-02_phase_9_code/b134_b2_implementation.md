# Implementation Report: Phase 9 B2 — câu tìm kho (B2a V0 / V1 / V3 / V2) + vòng công cụ `tim_kho` (**xong — chờ C review cả nhánh `74c5d68..1f2a57c`**: B2a giữ V0 · B2b `tim_them` BẬT — User giữ)

Người làm: B (Claude Opus 5.5, `hue-rag-52`) · việc **B134** · bắt đầu ~09:41 03/11/2026, bản này 11:09 03/11/2026 (`date`).
Plan: `docs/superpowers/plans/2026-11-03-phase-9-b2-plan.md` bản 3 sha `efa27cb8207c` (A duyệt; review C135 vòng 3 `90ed2605c9a9`; commit `74c5d68`).
Nhánh **`p9-b2`** từ `main` `74c5d68` (code = `f01c032`), worktree `/tmp/b_p9b2`. Commit: `456df18` (code D1–D10 + test), `e0ca48c` (vòng chỉnh 2 + harness C137 m-1 / m-2), **`1f2a57c`** (mặc định `tim_them: true`). Đã push. **Chưa merge.**
Report tracked, repo public: không chép câu Golden / kho / câu tìm model viết; chỉ số đếm + `case_index` khi cần. Dữ liệu chạy: `data/phase_9/b2_chay/` (private).

## 1. Phạm vi — đã làm / chưa làm

| Phần plan | Trạng thái |
|---|---|
| D1 cờ `lan_tim_dau` + `tim_them` | xong (`v1` / `v3` không có `router` ⇒ lỗi cấu hình lúc dựng cờ) |
| D2 định tuyến viết câu tìm (V1 / V3) | xong — **Lệch D2** (§2) |
| D3 tìm bằng câu tìm, đếm ngân sách bằng câu hỏi thật | xong + test |
| D4 `search_many` (V3) | xong + test (1 câu = `search`; trộn tất định) |
| D5 vòng công cụ (`max_turns` 4, lần 3 "đã hết lượt", hết trần ⇒ câu từ chối cố định, sổ nối số, một ngân sách) | xong + test logic (client giả của SDK); **chưa chạy với model thật ở đường trả lời** |
| D6 harness V2 tới lần gọi công cụ đầu | xong, chạy thật (pilot + 2 vòng dev) |
| D7 thẻ công cụ | lõi phát lại `searching` / `searched` mỗi lần `tim_kho`; **giao diện không sửa** (nhãn có sẵn `App.jsx:6, :8`) — Playwright ở cổng cuối |
| D8 chỉnh trên dev, khoá | xong 2 vòng, **khoá `e0ca48c`** (§5) |
| D9 `routing_ms`; D10 token = tổng mọi lần gọi | xong |
| Q1, Q7 | **PASS** |
| Q2 lượt đo cuối tầng tìm | **xong — không biến nào qua cổng sàng ⇒ Q4 giữ V0** (§4) |
| Q8 (B2b `tim_them`) | **xong — đạt quyết + sàn S-G / F1–F4; S-AT 1 ca P0_sai mới thật (≤ 2 cả Phase) ⇒ báo A** (§4b) |
| Q9 cổng ổn định | **xong — đạt** (§4c) |
| bước 0 câu hai ý | C138 (C) |

## 2. Thay đổi chính (`git diff 74c5d68..e0ca48c`)

| File | Thay đổi |
|---|---|
| `backend/llm/assistant.py` | `AssistantFlags.lan_tim_dau`, `tim_them`, `uses_tools`; `search_into_trace` (1 / nhiều câu tìm, đếm bằng `cau_hoi`, đánh số tiếp, bỏ đoạn trùng, ngân sách chung, thời gian cộng dồn); `tim_kho(…, cau_hoi=None)` (T-4 giữ chỉ `cau_tim`); `tool_for_turn` (closure công cụ của một lượt: trần `MODEL_SEARCH_LIMIT` 2, lần 3 trả `TOOL_LIMIT_TEXT`, lỗi tìm ⇒ `trace.tool_error`); `_before_model` / `_finish_generated`; `answer_query` / `answer_turn_stream` rẽ sinh một lần ↔ trợ lý có công cụ; chạm trần ⇒ `fixed_outcome="max_turns"` + một `delta` |
| `backend/llm/generator_openai_full_corpus.py` | `RouteSearchOutput` / `RouteSplitOutput` + agent định tuyến V1 / V3 (clone agent B1, lời dặn thêm một đoạn); `route_search`; agent `hue_assistant` (`parallel_tool_calls=False`); `_assistant_for` bọc `function_tool(failure_error_function=None)` từ closure lõi + handler `max_turns` + cờ **dựng mỗi lượt** (m-6); `generate_with_tools`, `start_tools_stream`, `first_tool_search`; `_run(max_turns, error_handlers)`; `GeneratedText.hit_max_turns`; `_generated_text` cộng token mọi `raw_responses` (D10) |
| `backend/llm/full_corpus_prompt.py` | `ROUTER_SEARCH_V1`, `ROUTER_SEARCH_V3`, `ASSISTANT_TOOL_NOTE`, `TOOL_LIMIT_TEXT`, `TOOL_NO_NEW_TEXT`, `build_assistant_input` |
| `backend/retrieval/full_corpus.py` | `search_many` (RRF lần hai, `rrf_k` 60, pool 30) |
| `backend/retrieval/full_corpus_context.py` | `build(…, first_id, prior_context, skip_ids, instructions)`; `PackedContext.document_ids`; `_token_count(…, instructions)`. Mặc định = B1 |
| `backend/api/routes/chat.py` | trường `routing_ms` (D9) |
| `backend/evaluation/full_corpus_eval.py` | `generate --lan-tim-dau`; lệnh `tang_tim <bien> --cases-file --out` (hợp đồng C133 + file chi tiết private; lỗi từng câu ⇒ `<out>.loi.json`); dòng thêm `routing_ms`, `fixed_outcome`, `cau_tim_rong` |
| `backend/config/settings.yaml` | `lan_tim_dau: v0`, `tim_them: false` |
| `backend/tests/test_b2_tool_loop.py` (mới) | 10 test logic: sổ nối số + trích nguồn lần 2 + token tổng; lần 3 "hết lượt" không tìm; hết `max_turns` ⇒ câu cố định + 1 `delta` stream + thẻ công cụ; **2 lượt đồng thời không lẫn cờ (m-6)**; lỗi Qdrant trong công cụ ra đúng lỗi gốc; ngân sách đường trợ lý; `search_many`; D3; `build` nối số; cờ |

**Lệch D2 (ghi theo review C137, A quyết):** plan ghi "V3 > 3 câu ⇒ code lấy 3 câu đầu". Thực tế SDK kiểm đầu ra theo schema (`maxItems` 3) và ném `ModelBehaviorError` **trước** khi tới code ⇒ lần định tuyến lỗi ⇒ `tro_ly_hue` bằng câu gốc — **mất cả tuyến** (kể cả câu khẩn cấp / ngoài phạm vi). Đoạn cắt 3 câu không bao giờ chạy nên đã bỏ.
A coi là rủi ro an toàn ⇒ harness đếm `qua_3_cau` (probe 0 USD: client giả trả 4 câu ⇒ đếm bắt đúng); **> 0 ở pilot / Q3 / Q5 ⇒ quay về cắt 3 câu trong code** (giữ tuyến). Tới giờ: **0** (pilot 10 + dev 43 × 2 vòng; API thật nhận `maxItems`).

## 3. Cách đã chạy thật

Từ `/tmp/b_p9b2/backend`, `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`; có phí thêm `--env-file /home/minhhieu/hue_rag/.env`.
1. **Q7 mốc** trên HEAD `74c5d68` **trước khi sửa**: `data/phase_9/b2_chay/tools/capture_all.py` (bắt mọi thân yêu cầu — định tuyến + trả lời; dùng lại chuẩn hoá `capture_model_request.py` B0) ⇒ `q7/head_74c5d68.jsonl`.
2. Test: 9 file chạm có key (§4). Test mới: `env -u OPENAI_API_KEY OPENAI_API_KEY=test-only … pytest tests/test_b2_tool_loop.py`.
3. **Q1:** `python ../data/phase_9/b0/tools/t1_qua_tim_kho.py <out>` (sha) + `python -m evaluation.full_corpus_eval tang_tim v0 --cases-file data/phase_9/b2_chay/cases_61.json --out …` so `data/phase_9/b2/ket_qua/v0.jsonl`.
4. **Chạy thử 0 USD** lệnh có phí (W36 4b): `tang_tim v1 / v3 / v2` khoá giả, 3 câu.
5. **Pilot** (có phí): `tang_tim v1|v3|v2 --cases-file pilot/cases10.json` (10 câu dev đầu).
6. **Vòng chỉnh** (có phí): `tang_tim … --cases-file cases_dev43.json` ⇒ `do_tang_tim.py cham --nhom dev` (`45e35e800500`, không in số test) + `tools/chan_doan_dev.py` (từng câu **dev**).

## 4. Kết quả quan sát

| Mã | Kết quả | Bằng chứng |
|---|---|---|
| **Q7** | **PASS** — `v0` + `tim_them` tắt: **228 / 228** dòng (Golden 176 + an toàn 32 qua `answer_case`, smoke 10 × `/api/chat` + `/api/chat/stream`; mỗi dòng 2 lần bắt = định tuyến + trả lời) **giống byte** HEAD; chạy 2 lần trên code `456df18`, `cmp` đều giống (sha `d5d44222b2df`). Sửa sau đó (`e0ca48c`: lời dặn V3, đoạn công cụ, harness) không nằm trên đường `v0` — **chạy lại ở cổng cuối**. C137 kiểm độc lập 42 / 42 | `data/phase_9/b2_chay/q7/` |
| **Q1** | **PASS** — T1 158 câu qua `tim_kho` sha **`4d5bbe9e0edc`**; `tang_tim v0` trùng V0 C133 **61 / 61** | `q1/` |
| test | có key, 9 file: **70 / 70** (mốc 1); sau vòng 2: 6 file chạm 59 / 59. Kiểm test không rỗng: gỡ dòng "ném lại lỗi gốc" ⇒ test lỗi công cụ **FAIL**, trả lại ⇒ PASS | — |
| ngân sách đường trợ lý (D5 (4), client giả + tokenizer) | builder **2.306** ↔ thân yêu cầu lượt viết **2.322** token ⇒ chênh **16** (< 512). Số token thật của API (m-7): đo ở pilot cả lượt (chưa chạy) | `/tmp/b134_budget_probe.py` |
| chạy thử 0 USD | v1 / v3: lỗi định tuyến ⇒ tìm bằng câu gốc, đủ dòng; v2: lỗi model ⇒ (sau m-1) ghi `loi` 3, `.loi.json`, không dừng cả lượt | `/tmp/b134_dry/` |
| **pilot** tầng tìm (10 câu dev) | V1 **0,000117** · V3 **0,000130** · V2 **0,000080** USD / câu (ước 0,0001 / 0,0001 / 0,0002); `route_error` 0, `qua_3_cau` 0 ⇒ **API nhận `maxItems`**; V3 tách 1–2 câu; V2 gọi `tim_kho` 10 / 10; ms lần gọi p50 2,35 / 2,22 / 1,93 s | `pilot/` |
| **vòng chỉnh 1** (43 dev; 9 câu có thể đổi; lời dặn viết trước khi đo) | V1: thêm 1 / 9, mất ý 0 · **V3: thêm 3 / 9, mất ý ở 1 câu** (so sánh, câu nhỏ hẹp hơn câu gốc) · V2: thêm 1, mất keyword 1, mất ý ở 2 câu. V0 dev: đủ keyword 19 / 28 | `dev_r1/cham_dev.json` |
| **vòng chỉnh 2** (chỉ lời dặn V3 + đoạn công cụ V2) | V3: câu so sánh giữ cả câu làm câu tìm đầu ⇒ **thêm 1 / 9, mất 0** · **V2: lần gọi đầu giữ đủ tên + ý ⇒ thêm 3 / 9, mất 0, mất keyword 0** (p Holm dev 0,16 — chỉ báo số). V1 không chỉnh | `dev_r2/cham_dev.json` |
| **Q2 lượt đo cuối** (khoá `e0ca48c`; 3 biến × 2 lượt × 61 câu; chấm `do_tang_tim.py cham --nhom tat_ca`, `45e35e800500`) | 0 lỗi, `route_error` 0, **`qua_3_cau` 0** (m-2). V0: đủ keyword 26 / 38, 0 / 12 câu có thể đổi. **V1:** thêm **0** / 12 (đủ keyword 26 · 26), mất đoạn đúng 0, `qua_cong_sang` **False**. **V3:** thêm **1** / 12 ở cả hai lượt (27 · 29), mất đoạn đúng **1 câu ở lượt 1**, test thêm − mất 0, **False**. **V2:** thêm **0** / 12 ở cả hai lượt (28 · 26 — câu tìm model viết dao động; +3 của vòng chỉnh 2 không lặp lại), mất 0, **False**. `xep_hang_qua_cong` **rỗng**. Holm dev (chỉ báo số): V1 1,0 · V3 0,26 · V2 0,51 | `q2/cham.json` `c3cc0df07677` |
| **Q4** | Không biến nào qua cổng ⇒ **giữ V0** (luật ghi trước); B2a xong, **kết quả âm**: viết lại / tách câu tìm (V1 / V3) và để trợ lý tự viết câu tìm đầu (V2) không đưa thêm đủ 3 / 12 câu đủ keyword ổn định qua 2 lượt. Q5 / Q6 không chạy (chỉ cho biến được chọn). **Bài học (A):** +3 của V2 ở vòng chỉnh 2 trên 9 câu dev là **dò theo nhiễu** (1 lượt, câu tìm model viết dao động) — không lặp lại ở lượt khoá 2 lượt | — |
| tiền B2 tới giờ | pilot tầng tìm 0,003274 · vòng 1 0,014498 · vòng 2 0,009581 · Q2 0,041858 · pilot B2b 0,005443 · Q8 Golden 2 lượt 0,136625 · Q8 an toàn (2 lần sinh, lần 2 có ngữ cảnh cho judge) 0,034245 · sinh lại S20 0,002261 ⇒ **0,2478 USD** + cổng Q9 0,007155 ⇒ **≈ 0,255 USD** (trần 0,45, dừng > 0,40) | `usd` từng dòng (cộng `llm_calls`) |

### 4b. B2b — Q8 (cờ `router` + `may_have_changed_notice` + `tim_them`, `lan_tim_dau: v0`)

| Bước | Kết quả | Bằng chứng |
|---|---|---|
| 0 USD | thân yêu cầu B2b: công cụ `tim_kho` một tham số `cau_tim` (strict), `parallel_tool_calls=False`, lời dặn có đoạn công cụ | `tools/pilot_b2b.py --capture` |
| **pilot cả lượt** (10 câu dev: 9 có thể đổi + 1 nhiều nguồn) | 0 lỗi, 0 lỗi trích dẫn, 0 chạm trần, 0 từ chối; model gọi `tim_kho` thêm ở 8 / 10 câu (2 câu × 2 lần). **m-7:** `usage.input_tokens` thật lượt viết − số builder đếm = **194–352** token (max ở câu 2 lần tìm; ngưỡng 512) ⇒ **đạt**. USD TB **0,000544** / câu (ước 0,0005, +9 %) | `pilot/b2b10.jsonl` |
| **sinh Q8** | Golden 176 × **2 lượt** (A/A đường có công cụ) + an toàn 32: 0 lỗi kỹ thuật, 0 lỗi trích dẫn, 0 `max_turns`; `tim_kho` do model gọi 62 / 54 lần / 176 câu | `q8/` |
| sàn sinh (`do_cuoi.py check`) | **F1 0** câu ngoài kho bị trả lời (cả 2 lượt) · F3 0 · F4 0 · **từ chối nhầm câu trong kho 12 (V0) ⇒ 4 / 6** | `q8_judge/golden/*/check_*.json` |
| chấm Golden (judge Claude, mù 3 bên: V0 = câu trả lời P5 B1, B2b lượt 1, B2b lượt 2) | 436 mục / 19 lô (sub-agent mới mỗi lô, Opus 5.5), 0 lỗi điểm; F2 ứng viên câu 19 ⇒ chấm lại ⇒ **F2 = []** | `q8_judge/golden/analyze.json` |
| **N_AA đường có công cụ** (lượt 1 ↔ lượt 2, 129 câu chính; review C135 vòng 2 M-4) | Đủ **5** câu tụt (chiều ngược 4) · Đúng **5** (ngược 3) ⇒ ngưỡng câu tụt **8** | `q8_judge/golden/q8_quyet.json` |
| **S-G** V0 ⇒ B2b lượt 1 | Đủ tụt **5** ≤ 8, TB **+0,217** [+0,062; +0,388] (12 thắng / 112 hoà / 5 thua) · Đúng tụt **2** ≤ 8, TB **+0,225** [+0,078; +0,395] ⇒ **đạt** | như trên |
| **QUYẾT** — Completeness 18 câu nhiều nguồn (bộ C133) | **+1,167, CI 95 % [+0,444; +2,000] > 0** — 6 thắng / 12 hoà / **0 thua** ⇒ **đạt**. Test (4 câu) chênh 0 ⇒ không ngược chiều. Theo dõi 20 câu so sánh: +0,35 [−0,15; +1,00] | như trên |
| **S-AT** (2 judge, cả hai **qua cổng** đối chứng: chèn sai 10 / 10, đảo cảnh báo 5 / 5, báo nhầm 0 / 5) | mốc = lượt đo cuối 01/11 (RAG 1–8). 0 câu ngoài kho bị trả lời; "trái nguồn" mốc 1 ↔ B2b **0**. P0_sai: mốc 2 câu ↔ B2b 2 câu, **1 ca mới** (loại câu cảnh báo, có trong kho) ⇒ sinh lại 3 lần hai bên: **B2b 2 / 3 sai, mốc 0 / 3** ⇒ **"mới thật"** (luật spec §4). Kiểu lỗi: thêm một ý **không có trong nguồn** (lời khuyên chung), **không** đảo cảnh báo; 1 / 3 lần sinh lại bị **định tuyến sang `khan_cap`** (câu soạn sẵn, 0 nguồn — định tuyến B1, không do B2b; lượt chính 32 / 32 `tro_ly_hue`). Sàn "P0_sai mới ≤ 2 **cả Phase**" ⇒ **đạt, dùng 1 / 2** ⇒ báo A | `q8_judge/an_toan/` (`tools/an_toan_b2.py` = `an_toan_cuoi.py` với mốc 01/11) |
| tiền / câu (theo dõi) | V0 0,000230 ↔ B2b 0,000313 TB (p95 0,000611) USD | `analyze.json` `watch_usd_wall` |

**Theo luật ghi trước (Q8):** quyết đạt + sàn S-G / F1–F4 đạt + test không ngược ⇒ **giữ `tim_them`**; S-AT đạt sàn nhưng có 1 ca P0_sai mới thật ⇒ **A quyết** (giữ cờ / gỡ / sửa gì trước merge). Chưa đổi mặc định `settings.yaml` (vẫn `tim_them: false`).

**Quyết định (User qua A, 03/11/2026): GIỮ `tim_them`.** Lỗi S20 — trả lời câu cảnh báo có **thêm một lời khuyên chung không có trong nguồn** (P0_sai mới thật, **dùng 1 / 2 suất cả Phase**) — **chưa sửa ở B2**; sửa ở **B3**: plan B3 thêm một dòng lời dặn "chỉ nêu điều có trong nguồn, không thêm lời khuyên chung" và kiểm lại S20 trong lượt đo an toàn của B3.
**Theo dõi:** định tuyến (B1) đưa S20 sang `khan_cap` ở 1 / 3 lần sinh lại (câu soạn sẵn, 0 nguồn) — lời dặn định tuyến ghi "câu hỏi an toàn không gấp không phải khan_cap"; lượt chính 32 / 32 đúng tuyến.

### 4c. Q9 — cổng ổn định cuối (11:28 03/11/2026; mặc định mới: `router` + `may_have_changed_notice` + `tim_them`, `lan_tim_dau: v0`; uvicorn cổng 8871, `npm ci && npm run build`)

| Kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Q7 trên code cuối `e0ca48c` (`v0`, `tim_them` tắt) | **228 / 228 giống byte** HEAD `74c5d68` | `q7/nhanh_e0ca48c_v0.jsonl` |
| test chạm (có key, 9 file) | **70 / 70** sau khi bật `tim_them` (generator giả của `test_api_chat.py` thêm đường công cụ) | — |
| `/`, `/health` | 200; 5 / 5 lần, 5 thành phần ready | — |
| 5 câu tự viết × `/api/chat` + `/api/chat/stream` | `tro_ly_hue` (có nguồn + H4c), câu nhiều nguồn (vòng công cụ), `tro_chuyen` (0 nguồn), `ngoai_pham_vi` (`out_of_scope`), `khan_cap` (`emergency`, câu soạn sẵn). Stream có công cụ: `routing ⇒ searched ⇒ generating ⇒ searching ⇒ searched (… mỗi lần tim_kho) ⇒ delta ⇒ sources ⇒ notice ⇒ done` | `q9/cong_json_stream.json` |
| log | `chat_metrics` mới **10 = 10** câu; **grep câu hỏi trong log 0**; `routing_ms` có ở mọi dòng; `tools` ghi lần do model (`by`, `n_new`) cả lần "hết lượt" (`het_luot`); token = tổng mọi lần gọi (vd 11.306 token vào / 5 lần gọi) | log worktree |
| ngắt thật `curl -m` | (1) `-m 4`: ngắt **giữa vòng công cụ** (lượt trợ lý đầu) ⇒ `client_disconnected`, drain `finished` 0,7 ms, `llm_calls` = định tuyến; (2) `-m 11`: ngắt **giữa chữ** (385 `delta`) ⇒ `client_disconnected`, drain 1,3 ms, `llm_calls` 3 (định tuyến + 2 lượt gọi công cụ) + 2 lần `tim_kho`; `/health` 200 sau đó | log worktree |
| giao diện (Playwright, câu nhiều nguồn) | thấy "Đang hiểu câu hỏi…", "Đang viết câu trả lời…", **"Đã tìm thông tin…" của lượt `tim_kho`**, dòng H4c; câu trả lời trích **[17]** (lần tìm 2, đánh số nối) + [4], bảng nguồn mở được — **không sửa giao diện** (D7) | `q9/ui/*.png`, `q9/ui_tools.py` |
| **chữ đầu** — 10 câu B131 (cùng câu, httpx tuần tự) | **cả 10: p50 3,33 / p95 5,20 s** (B1 cùng câu: 3,05 / 5,64). `tro_ly_hue` 5 câu: p50 **3,50** / p95 **5,33** s (B1 3,57 / 6,57); model gọi `tim_kho` thêm ở 2 / 5 câu. `tro_chuyen` 3,78 / 4,03 · `ngoai_pham_vi` 2,18 / 2,66 · `khan_cap` 1,48 s (khác B1 chủ yếu do định tuyến dao động). Mẫu nhỏ — chỉ theo dõi | `q9/first_text_client.jsonl` |
| tiền cổng | 0,007155 USD (từ `chat_metrics`) | — |

**Quan sát (theo dõi, không sửa ở B2):** (1) câu đơn giản có lúc model gọi `tim_kho` tới 3 lần (lần 3 "hết lượt") ⇒ tốn thêm lượt / thời gian; (2) trạng thái `generating` hiện **trước** các lượt `searching` của vòng công cụ (nhãn "Đang viết câu trả lời…" rồi lại "Đã tìm thông tin…"); (3) số trích dẫn có thể lớn (vd [17]) dù bảng nguồn chỉ 2 mục — đúng logic sổ nối số, có thể khó hiểu với người dùng. Ứng viên cho plan B3 / B7.

## 5. Khoá (plan D8 — trước lượt đo cuối Q2)

**Khoá 10:25 03/11/2026** — commit nhánh `p9-b2` **`e0ca48c`** (đã push). sha256 (12) chuỗi lời dặn: `ROUTER_INSTRUCTIONS` `fb4e1aa7f8fe` (= B1) · `ROUTER_SEARCH_V1` `7e7f9eff2b62` (vòng 1) ·
`ROUTER_SEARCH_V3` `346fff4ece2a` (vòng 2) · `ASSISTANT_TOOL_NOTE` `4cba5621ee48` (vòng 2) · `TOOL_LIMIT_TEXT` `0f64fe52619c` · `ANSWER_SYSTEM_INSTRUCTIONS` `41f616a83451` (= B1); `backend/config/settings.yaml` `6d018cfd3fdc`.
Lý do không chạy vòng 3: V3 vòng 1 (+3) đã phạm sàn "0 mất đoạn đúng" trên dev; chỉnh tiếp trên 9 câu có thể đổi là dò theo bộ nhỏ (quá khớp). Kết quả test (18 câu) chưa đọc.

## 6. Lỗi, giới hạn, chưa chạy

- NOT RUN: Q5–Q6 (không biến nào qua Q2 — đúng luật). Bước 0 câu hai ý: C138. đường trả lời có công cụ với model thật (pilot cả lượt + m-7 token thật).
- Trước merge: Playwright thẻ công cụ (D7) chỉ khi vòng công cụ vào chatbot.
- **Ngân sách token (m-7, pilot B2b, A ghi):** bộ dựng ngữ cảnh đếm **thiếu 194–352 token** so với `usage.input_tokens` thật của lượt viết (phần định dạng mục `function_call` / `function_call_output` + công cụ) — còn dư ~160 so với `safety_margin` 512. **Mang sang plan B3:** lịch sử hội thoại vào lượt gửi ⇒ dễ vượt ⇒ B3 phải đếm đúng phần được gửi (lời dặn + lịch sử + kết quả công cụ) hoặc có test chặn khi chênh > margin. Không sửa ở B2.
- `tools` của `chat_metrics` có thêm `by`, `n_queries`, `n_new` cho lần tìm do model / nhiều câu / lần tìm thêm; lần tìm đầu một câu giữ đúng `{name, ms}` như B1.
