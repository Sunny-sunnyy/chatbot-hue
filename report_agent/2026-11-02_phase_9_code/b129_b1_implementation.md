# Implementation Report: Phase 9 B1 — định tuyến + trò chuyện + ngoài phạm vi + khẩn cấp + ngày + H4c (**xong — chờ C review delta `7e190d7..dcd1519`**)

Người làm: B (Claude Opus 5.5, `hue-rag-e7`; phiên 03/11 `hue-rag-52`) · việc **B129** + **B131** (hoàn tất) · bắt đầu 19:55 02/11/2026, bản này 08:59 03/11/2026 (`date`).
Plan: `docs/superpowers/plans/2026-11-02-phase-9-b1-plan.md` bản 2 sha `0c9e137b56af` (A duyệt; C129 vòng 2 ready).
Nhánh **`p9-b1`** (từ `main` `a406bea`), commit code **`d7a4382`** + vòng chỉnh định tuyến **`7e190d7`** + **B131 `dcd1519`** (m-1, 2 cờ bật), đã push; worktree `/tmp/b_p9b1`. **Chưa merge. Mặc định: `router` + `may_have_changed_notice` BẬT, `emergency_rule` + `today_line` TẮT.**
Report tracked, repo public: không chép câu bộ đo / Golden / kho; chỉ số đếm + mã câu bộ tuyến (`t…`, `l…`) + `case_index`. Dữ liệu chạy: `data/phase_9/b1/` (private).
**B không mở `*sealed*`.**

## 1. Phạm vi — đã làm / chưa làm

| Phần | Code | Đo phần đã thấy | Phần kín (C) |
|---|---|---|---|
| D1 / D2 luật khẩn cấp (P3) | xong | **xong** (0 USD) | **C131: (a) KHÔNG ĐẠT ⇒ cờ `emergency_rule` tắt**; (b) âm |
| D3 định tuyến + D4 trò chuyện + D5 ngoài phạm vi (P1) | xong | **xong** (vòng chỉnh 1) + sàn 2 judge | **C131: đạt** |
| D7 ngày hôm nay (P2) | xong | **xong — KHÔNG ĐẠT ⇒ cờ `today_line` tắt** | không chạy (phần đã thấy đã âm) |
| D8 H4c (P4) | xong + test 3 ca | theo dõi ở P5: dòng H4c 66 / 176 Golden, 24 / 32 an toàn | — |
| P5 hồi quy 208 | — | Golden **chấm xong** (sàn đạt; Đủ vượt 1 câu tụt — nhiễu, xem §4); S-AT **dùng lại 01/11** (B131: 32 / 32 giống byte) | — |
| P6 4 cờ tắt ⇒ giống B0 | — | **PASS** | — |
| P7 log + cổng ổn định | xong (test) | **cổng xong** (4 cờ bật, uvicorn + Playwright); **cổng cuối B131** (mặc định mới) + ca ngắt thật + chữ đầu 10 câu | — |
| sàn 2 (judge lời trò chuyện) | — | **xong** | **C131: 0 / 5 lọt** |

## 2. Thay đổi chính (`git diff a406bea..d7a4382`, 16 file, +640 / −177)

| File | Thay đổi |
|---|---|
| `backend/llm/emergency.py` (mới) | `is_emergency` (mẫu "đang gặp nguy", không từ đơn dễ trùng) + `EMERGENCY_ANSWER` = Bản 1 nguyên văn |
| `backend/llm/assistant.py` | `AssistantFlags` (4 cờ), `answer_turn` / `answer_turn_stream` (luật ⇒ định tuyến ⇒ rẽ tuyến); câu cố định (`fixed_outcome`); `set_notice` (H4c); vòng đọc stream + huỷ / đọc nốt **dời vào lõi** (D6); mọi lần gọi đã xong ghi ở `finally` cả đường không stream (C128 m-1); `llm_calls` mỗi mục có `route` của lần gọi |
| `backend/llm/full_corpus_prompt.py` | `build_answer_input(…, today)`; `today_line()` (giờ VN, `zoneinfo`); `ROUTER_INSTRUCTIONS`, `CHAT_INSTRUCTIONS`, `OUT_OF_SCOPE_ANSWER`, `REFUSAL_ANSWERS`, `MAY_HAVE_CHANGED_NOTICE` |
| `backend/llm/generator_openai_full_corpus.py` | agent `hue_router` (`RouteOutput` strict, `max_tokens` 512) + `hue_chat`; `route`, `generate_chat`, `start_chat_stream`; `CallLog` do nơi gọi đưa vào |
| `backend/retrieval/full_corpus_context.py` | `PackedSource.source` (không vào chữ ngữ cảnh); `build(…, today)` đếm token cùng chuỗi gửi |
| `backend/api/routes/chat.py` | `/api/chat` qua `answer_turn`; stream: chỉ kiểm "chưa sẵn sàng" trước luồng (thêm generator), còn lại trong luồng; `StreamEvents.fixed`, sự kiện `notice`, `failure` mang mã + câu cũ cho lỗi tìm / ngữ cảnh; `ChatResponse.notice`; trường log `route_error`, `emergency_by`, `today` |
| `backend/evaluation/full_corpus_eval.py` | `answer_case` qua `answer_turn`; `is_refusal` nhận 2 câu; `generate --flags …`; dòng thêm `route_error`, `emergency_by`, `notice`, `today` |
| `backend/config/settings.yaml` | khối `assistant:` 4 cờ + `router_timeout_seconds: 10`; B131: `router`, `may_have_changed_notice` = `true` |
| `backend/api/app.py` | `app.state.assistant_flags` |
| `frontend/src/App.jsx`, `stream.js` | nhãn `routing` ("Đang hiểu câu hỏi…"); trạng thái lạ không còn bị gán "đã tìm" (`App.jsx:61` cũ); dòng `notice` dưới câu trả lời |
| tests | mới `test_emergency.py` (3); `test_assistant.py` +9 (rẽ tuyến với generator thay thế — logic, không phải bằng chứng model); `test_chat_stream.py` (câu cố định, lỗi tìm giữa luồng giữ câu 503 cũ, sự kiện `notice`); 2 fake cập nhật chữ ký |

**Chữ cho người dùng (A chọn / sửa lúc review):** `OUT_OF_SCOPE_ANSWER` "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" · `MAY_HAVE_CHANGED_NOTICE`
(như spec bản 5 §5.3) · nhãn `routing` "Đang hiểu câu hỏi…".

**Đổi hành vi ngoài cờ (ghi rõ):** (1) lỗi tìm kho / ngữ cảnh ở route stream thành sự kiện `error` trong luồng (D6, A chọn M-3 (b)); (2) route stream kiểm generator chưa sẵn sàng **trước** luồng ⇒
JSON 502 cả khi ngữ cảnh rỗng (trước B1: ngữ cảnh rỗng + generator chưa sẵn sàng ⇒ câu từ chối 200 — ca chỉ xảy ra khi thiếu key).

## 3. Cách đã chạy thật

Từ `/tmp/b_p9b1/backend`, `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`.
1. **P3 đã thấy** (0 USD): `PYTHONPATH=$PWD … python ../data/phase_9/b1/tools/emergency_check.py` — 14 câu phải bắt (10 C122 + 4 `khan_cap` bộ tuyến đã thấy); 249 câu không được bắt (36 câu khác của bộ tuyến đã thấy + 5 ca lái + Golden 176 + an toàn 32).
2. **Test** không key: `pytest tests/test_assistant.py tests/test_assistant_boundary.py tests/test_chat_stream.py tests/test_api_chat.py tests/test_openai_full_corpus_generator.py tests/test_emergency.py tests/test_r4_numbers.py tests/test_static_ui.py -q` (sau `cd frontend && npm ci && npm run build`).
3. **P6** (0 USD, không mạng): `capture_model_request.py` của B0 với `settings.yaml` (4 cờ tắt) ⇒ `data/phase_9/b1/req_flags_off_*`, so `data/phase_9/b0/req_head_1_*` (mốc B0).
4. **Pilot P1** (có phí): `--env-file …/.env python ../data/phase_9/b1/tools/p1_route.py data/phase_9/b1/pilot_route10.jsonl --set tuyen --limit 10`.
5. **P1 đã thấy**: `p1_route.py data/phase_9/b1/p1_da_thay_r1.jsonl` (mặc định 4 bộ: tuyến 40, lái 5, Golden 176 theo nhãn `golden_oos_nhan.jsonl`, an toàn 32).

## 4. Kết quả quan sát

| Mã | Kết quả | Bằng chứng |
|---|---|---|
| P3 (b) đã thấy | **14 / 14** bắt. Mẫu chỉnh 3 lần trên phần đã thấy / câu tự viết: "đuối nước" một mình bắt nhầm 1 câu an toàn loại sông nước ⇒ thành "vừa / đang / mới (bị) đuối nước"; "tai nạn giao thông" ⇒ "vừa / bị / gặp / đang tai nạn" (câu tự viết hỏi chung) | `emergency_check.py` |
| P3 (a) đã thấy | **0 / 249** chặn nhầm | như trên |
| test | không key, 8 file: **57 pass / 3 error** (55 trước build + 2 test `test_static_ui.py` đạt sau build; 3 error = 3 test cần key, như mốc) | lệnh §3.2 |
| T-3 / T-4 (B0) | giữ xanh (không thêm module mạng; `llm.assistant` import `anyio`, không client mạng) | `test_assistant_boundary.py` |
| **P6** | **PASS** — 4 cờ tắt: `answer_case` 176 / 176 + 2 route 20 / 20 sha = mốc B0; so chéo thường ↔ stream 10 / 10 | `req_flags_off_*` |
| pilot P1 | 10 / 10 đúng; **0,000674 USD / 10 câu** (≈ 0,000067 / câu, khớp ước 0,00007); ms mỗi lần định tuyến **1.583–3.498** (model có bước suy luận: `kind` = `reasoning, message`) — chỉ theo dõi | `pilot_route10.jsonl` |
| P1 đã thấy r1 | tuyến 40 / 40, lái 5 / 5, an toàn 32 / 32, Golden 175 / 176; **sàn 1 phạm 1**: Golden câu 166 (loại câu hỏi giá vé phương tiện tham quan, **không nhắc chữ "Huế"**, `nhan` `tro_ly_hue`) ⇒ `ngoai_pham_vi`; 0,018513 USD | `p1_da_thay_r1.jsonl` |
| **vòng chỉnh 1** (plan §7: ≤ 3 vòng trên phần đã thấy) | `ROUTER_INSTRUCTIONS` thêm: câu vé / giờ / giá / địa điểm / phương tiện / món / lễ hội **không nêu nơi khác** ⇒ coi là hỏi về Huế; chỉ `ngoai_pham_vi` khi nói rõ nơi khác hoặc không liên quan văn hoá, du lịch (`7e190d7`) | — |
| **P1 đã thấy r2** | **253 / 253 đúng tuyến** (tuyến 40 / 40 = 100 % ≥ 90 %; lái 5 / 5; Golden 176 / 176 gồm 7 câu `out_of_scope` về Huế ⇒ `tro_ly_hue`, 11 ⇒ `ngoai_pham_vi`; an toàn 32 / 32); **sàn 1: 0**; lỗi định tuyến 0; định tuyến p50 **1,70 s** / p95 **2,74 s**; 0,020796 USD | `p1_da_thay_r2.jsonl` |
| **sàn 2 đã thấy** | 8 câu đi `tro_chuyen` (đúng 8 câu nhãn trò chuyện) ⇒ 2 judge sub-agent độc lập, lô mù 10 mục xáo seed (8 thật + 2 phiếu kiểm biết trước): cả 2 judge đúng 2 / 2 phiếu kiểm; **0 / 8 lọt thông tin Huế cụ thể** ("một trong hai"); 0 bất đồng | `san2_input.jsonl`, `san2_key.json`, `san2_judge_{1,2}.json` |
| **P7 cổng ổn định** (4 cờ bật trên bản sửa tạm `settings.yaml`, trả lại sau) | `/` 200, `/health` 5 / 5; 4 câu tự viết × `/api/chat` + `/api/chat/stream`: `tro_ly_hue` có nguồn + `notice` (stream: `routing ⇒ searched ⇒ generating … sources ⇒ notice ⇒ done`); `tro_chuyen` 0 nguồn (`routing ⇒ generating`); `ngoai_pham_vi` câu cố định, `refusal` true (`routing`, 1 `delta`); khẩn cấp luật bắt: **0 lần gọi model, 0 USD**, không có `routing`, 1 `delta`. `chat_metrics` mới = 8 = số câu; mỗi `llm_calls` có `route` của lần gọi; `today` = ngày chạy; grep câu hỏi trong log = 0. Chữ đầu stream (theo dõi): `tro_ly_hue` 4,86 s, `tro_chuyen` 2,91 s, `ngoai_pham_vi` 1,26 s, khẩn cấp 0,2 ms. Playwright: thấy "Đang hiểu câu hỏi…" ⇒ "Đang viết câu trả lời…" ⇒ dòng H4c (ảnh `gate/ui/`). 0,001323 USD | `gate/` |

| **P2 đã thấy** (cờ `today_line` bật ↔ tắt, các cờ khác tắt, 2 lượt, cùng ngày 02/11/2026) | 18 câu (15 cũ + 3 mới đã thấy) × 2 lượt × 2 bên. **Chỉ số quyết** — từ chối nhầm, trung bình theo câu trên 11 câu quyết có trong kho (R11 là câu ngoài kho): **tắt 5,0** (khớp mốc lượt đo cuối 01/11: 5 / 12) ⇒ **bật 4,5** — giảm 0,5 < 3 ⇒ **không đạt**. Câu ngoài kho R11 từ chối đúng 4 / 4; 0 lỗi, 0 lỗi trích dẫn; số đoạn ngữ cảnh không đổi ở câu nào (m-4). 0,020605 USD | `p2_da_thay.jsonl` |
| P2 vòng chỉnh 1 (chỉ trên phần đã thấy) | dòng ngày thêm câu "câu có hôm nay / tối nay / ngày mai… thì tính theo ngày này và đối chiếu lịch trong bằng chứng"; chỉ bên bật (mốc tắt cùng ngày đã có): **vẫn 4,5** ⇒ không đạt; code **trả về bản khoá** (không commit vòng này). 0,010853 USD | `p2_da_thay_v2_bat.jsonl` |
| P2 kết luận | Kết quả âm, giống phát hiện C93 (30/10): các câu bị từ chối phần lớn là lỗi tầng tìm (câu không có lịch trong ngữ cảnh) hoặc model không dám kết luận cho thời điểm hỏi, **không** do thiếu ngày ⇒ theo plan §4 P2 "không đạt ⇒ tắt `today_line`". Sàn L1 / L2 (judge) **NOT RUN**: cờ tắt nên không vào chatbot; thước C93 viết cho chatbot không biết ngày ("nêu hôm nay thứ…" ⇒ L1) phải sửa trước khi dùng cho bên được báo ngày — ghi cho lần thử sau | — |

| **P5 sinh** (`router` + `may_have_changed_notice` + `emergency_rule` bật — luật khớp 0 / 208 ⇒ = cấu hình {router, notice}; `today_line` tắt) | Golden 176: 0 lỗi kỹ thuật, 0 lỗi trích dẫn; tuyến 165 `tro_ly_hue` / 11 `ngoai_pham_vi` (đúng 11 câu nhãn ngoài chủ đề Huế); **S-OOS: 18 / 18 câu `out_of_scope` từ chối** (0 câu ngoài kho bị trả lời); từ chối nhầm **12 / 158** (= mốc 12 / 158; giới hạn ≤ mốc + 1); dòng H4c ở 66 / 176. An toàn 32: 0 lỗi, tuyến 32 `tro_ly_hue`, 4 câu từ chối, H4c 24 / 32. 0,054714 + 0,012245 USD | `p5_golden_r1.jsonl`, `p5_an_toan_r1.jsonl` |
| **P5 judge Golden (B130, 20:44 02/11/2026)** | Thủ tục lượt đo cuối 01/11 (`do_cuoi.py`, `DO_CUOI_DIR=data/phase_9/b1/p5_judge`): bên "trước" = câu trả lời mốc RAG 1–8 01/11, bên "sau" = B1; 311 câu khác chữ, 13 lô, mỗi lô một sub-agent Claude mới (prompt `full_corpus_judge_prompt.md`), **311 / 311 điểm, 0 lỗi điểm**; ứng viên F2 = 0 ⇒ không chấm lại; `analyze` một lần. **Sàn F1–F4 đạt** (0 câu ngoài kho bị trả lời, 0 lỗi kỹ thuật, 0 lỗi trích dẫn mới, 0 "nói chắc sai" mới). **Đúng**: 2 câu tụt ≤ 5, TB −0,008 [−0,031; +0,016] ⇒ đạt. **Đủ**: TB −0,023 [−0,070; +0,023] (≥ −0,1 đạt) nhưng **6 câu tụt > 5 (N_AA 2 + 3) ⇒ vượt 1**. Từ chối nhầm 12 = 12 ⇒ đạt. TB 129 câu chính: Đúng 4,721 ⇒ 4,713, Đủ 4,581 ⇒ 4,558 | `p5_judge/golden/analyze.json` |
| P5 — vì sao 6 câu tụt (đã kiểm, 0 USD) | Với `router` + `may_have_changed_notice`, lần gọi **trả lời** của tuyến `tro_ly_hue` gửi model **giống byte B0 ở 176 / 176 câu** (bắt thân yêu cầu như T-2 B0, chuẩn hoá cùng bảng; lần định tuyến là yêu cầu riêng đứng trước). 11 câu đi `ngoai_pham_vi` đều là câu `out_of_scope`, nằm ngoài 129 câu chính ⇒ 6 câu tụt Đủ là **nhiễu sinh lại cùng đầu vào**, không do cờ [Suy ra từ giống byte; A/A của B1 chưa sinh]. Spec §4: "chuỗi gửi model không đổi ⇒ dùng lại số của bậc trước" ⇒ đề xuất A: coi P5 Golden đạt theo luật đó, hoặc sinh A/A B1 (≈ 0,055 USD) để tách nhiễu theo thủ tục 01/11 | — |
| **P5 — A quyết (a) (20:46 02/11/2026)** | Theo spec §4 dòng "chuỗi gửi model không đổi ⇒ dùng lại số của bậc trước": **6 > 5 theo ngưỡng câu tụt Đủ, nhưng đầu vào lần gọi trả lời giống byte B0 176 / 176 ⇒ áp luật dùng lại; P5 Golden ĐẠT theo §4.** Không sinh A/A B1 | — |
| P5 S-AT (bộ an toàn 32) | **NOT RUN** (judge thước lỗi nặng + cổng câu chèn sai). A quyết: **phiên sau, trước merge**, B kiểm 0 USD lần gọi trả lời của 32 câu an toàn giống byte B0 (cùng cách bắt) ⇒ giống: dùng lại S-AT 01/11; khác: báo A | — |

**Tiền B1 tới giờ (từ log / dòng kết quả):** pilot 0,000674 + P1 r1 0,018513 + P1 r2 0,020796 + cổng 0,001323 + P2 0,020605 + P2 v2 0,010853 + P5 sinh 0,066959 ≈ **0,1398 USD**; C131 phần kín 0,002384 ⇒ **B1 cả hai ≈ 0,142 USD** (trần 0,25, dừng 0,21) (+ ≈ 0,0005 Playwright 1 câu, không đọc log riêng). Trần 0,25.

**Phần kín — C131** (C chạy trên `7e190d7`, 6 / 6 sha khoá khớp; số đếm từ `report_agent/2026-11-02_phase_9_code/c131_kin_b1.md`, B không đọc câu kín; 0,002384 USD):

| Phần | Kết quả kín | Theo luật ghi trước |
|---|---|---|
| P1 định tuyến | **20 / 20** đúng (≥ 16 / 20 ⇒ không ngược chiều); sàn 1 phạm **0**; `route_error` 0 / 28 | **đạt** |
| P1 lưới thứ hai | câu khẩn cấp kín luật sót ⇒ định tuyến chọn `khan_cap` **8 / 8** (+ 2 / 2 câu khẩn cấp trong bộ tuyến kín) ⇒ người dùng vẫn nhận Bản 1, nhưng câu **đã qua một lần gọi model** (định tuyến) | báo số |
| sàn 2 kín | **0 / 5** lọt (2 judge, phiếu kiểm 2 / 2, 0 bất đồng) | đạt |
| P3 (a) chặn nhầm | **2 / 8** câu thường kín bị luật chặn; 0 / 18 câu thường bộ tuyến kín | **không đạt ⇒ tắt `emergency_rule`** |
| P3 (b) độ phủ | luật bắt **0 / 8** (+ 0 / 2 bộ tuyến kín) — mẫu chữ khớp quá sát 14 câu đã thấy | kết quả âm; không sửa luật theo câu kín |

**Đọc kết quả (B, suy ra):** câu khẩn cấp hiện chỉ còn lưới định tuyến (10 / 10 câu kín ⇒ Bản 1). Sàn spec "0 câu khẩn cấp vào model" **không** đạt được bằng luật mẫu chữ ở B1; hướng
khác (vd định tuyến chạy trước, hoặc luật viết lại trên bộ câu lớn hơn rồi đo kín mới) là quyết định của A / User, không làm trong B1.

**P5 và luật khẩn cấp:** lượt sinh P5 chạy với `emergency_rule` bật trước khi có C131, nhưng luật khớp **0 / 208** câu hồi quy (P3 (a) đã thấy) ⇒ câu trả lời P5 giống như khi tắt luật — dùng được cho cấu hình {`router`, `may_have_changed_notice`} [Suy ra từ 0 / 208, tất định].

### 4b. B131 — hoàn tất (03/11, `git diff 7e190d7..dcd1519`, 4 file, +41 / −11)

| Việc | Kết quả | Bằng chứng |
|---|---|---|
| (a) 32 câu an toàn — lần gọi trả lời giống byte B0 (0 USD, không mạng) | **32 / 32 giống**: bên {`router`, `may_have_changed_notice`} bắt 2 lần / câu (định tuyến + trả lời), bên 4 cờ tắt 1 lần; lần bắt cuối (trả lời) chuẩn hoá như T-2 B0 ⇒ cùng sha ở mọi câu. Lượt P5 thật: 32 / 32 câu đi `tro_ly_hue` ⇒ đúng đường được so. Dòng H4c là trường riêng (`notice`), không vào chữ trả lời ⇒ **dùng lại S-AT 01/11** theo spec §4 | `data/phase_9/b1/b131_at_bytes.jsonl`; script tạm `/tmp/b131_at_bytes.py` (dùng `capture_model_request.py` B0) |
| (b) C132 m-1 | `_answer_events` `finally`: lấy `total_ms` (như B0, chưa tính đọc nốt) ⇒ `await turn.aclose()` **trong vùng che** ⇒ (`finally` lồng) `_copy_trace_metrics` + dòng log. Trước dòng log chỉ còn một `await` và nó được che ⇒ ý spec streaming §4.5 (anyio không huỷ mất dòng log) giữ. Thứ tự dòng log đổi: `chat_stream_drain` giờ đứng **trước** `chat_metrics` của cùng lượt. Test mới `test_disconnect_while_route_sends_text_still_logs_calls_the_core_records_on_close`: **FAIL trên code cũ, PASS trên code sửa** [Chạy] | `backend/api/routes/chat.py`, `backend/tests/test_chat_stream.py` |
| (c) mặc định cờ | `router: true`, `may_have_changed_notice: true`; `emergency_rule`, `today_line` giữ `false` (chú thích lý do trong `settings.yaml`). `test_api_chat.py`: generator giả thêm `route()` trả `tro_ly_hue` (cờ bật ⇒ lõi hỏi tuyến trước) | `backend/config/settings.yaml` |
| test chạm | có key, 8 file (`test_assistant`, `_boundary`, `test_chat_stream`, `test_api_chat`, `test_openai_full_corpus_generator`, `test_emergency`, `test_phase6_settings`, `test_static_ui`): **60 / 60 pass**; `git diff --check` sạch | — |
| (d) cổng ổn định (uvicorn cổng 8861, `settings.yaml` mặc định mới, `npm ci && npm run build`) | `/` 200; `/health` 5 / 5 (5 thành phần ready); 1 câu trong kho `/api/chat` ⇒ 6 nguồn; 1 câu ngoài kho ⇒ câu ngoài phạm vi, 0 nguồn; `chat_metrics` mới **14 = 14 câu đã gửi**; grep câu hỏi trong log **0**; tắt bằng TaskStop | `data/phase_9/b131/` |
| (d) ngắt thật `curl -m` (C132 m-2) | lần 1 `-m 4.5`: cắt **trước** chữ đầu (3 `status`) ⇒ `client_disconnected`, `n_llm_calls` 1 (định tuyến), `chat_stream_drain` finished. Lần 2 `-m 7`: cắt **giữa chữ** (262 `delta`, không `done`) ⇒ `outcome: client_disconnected`, `chat_stream_drain` `finished: true` 0,5 ms, `llm_calls` = [định tuyến] (lần trả lời bị huỷ không có usage — đúng spec §4.5); `/health` 200 ngay sau ⇒ server không treo | log worktree |
| (d) **chữ đầu 10 câu tự viết** trên `/api/chat/stream` (theo dõi; máy khách httpx tuần tự — gửi ⇒ sự kiện `delta` đầu; số phía server lệch ≤ 2 ms) | **tất cả 10: p50 3,05 s / p95 5,64 s** (max 7,30 s). Theo tuyến: `tro_ly_hue` 5 câu p50 **3,57 s** / p95 **6,57 s**; `tro_chuyen` 2 câu p50 2,63 / p95 2,82 s; `ngoai_pham_vi` 2 câu p50 1,82 / p95 1,93 s; `khan_cap` (định tuyến bắt) 1 câu 1,63 s. Định tuyến p50 **1,56 s** (1 câu 5,96 s ⇒ chữ đầu 7,30 s). Mốc trước B1 (01/11, trình duyệt Playwright, 38 câu): p50 1,23 / p95 2,61 s ⇒ **sàn cũ p50 ≤ 3 / p95 ≤ 5 s tới chữ đầu không đạt ở 10 câu này** — Phase 9 chỉ theo dõi (PA1 User mặc định 03/11) | `data/phase_9/b131/questions.jsonl`, `first_text_client.jsonl`, `first_text_server.jsonl` |
| tiền B131 | cổng 14 câu **0,002906 USD** (10 câu đo 0,002228; từ `usd` trong `chat_metrics`); (a) 0 USD. Trần 0,02 | log |

Ghi thêm (quan sát, không sửa): `chat_metrics` không có trường `routing_ms` riêng — ms định tuyến nằm trong mục `llm_calls` có `route: router`.

## 5. Lỗi, giới hạn, chưa chạy

- NOT RUN: A/A của B1 (P5 Golden + S-AT dùng lại theo spec §4 nhờ giống byte); sàn L1 / L2 của P2 (cờ đã tắt; thước C93 phải sửa cho bên được báo ngày).
- P3 luật khẩn cấp: kết quả âm ở phần kín ⇒ cờ tắt (A quyết); sàn spec "0 câu khẩn cấp vào model" **không đạt** nguyên văn — câu khẩn cấp qua 1 lần gọi định tuyến rồi nhận Bản 1 (model không viết lời khẩn cấp).
- **Chữ đầu chậm thêm** do lần định tuyến: 10 câu B131 p50 3,05 / p95 5,64 s (`tro_ly_hue` p50 3,57 / p95 6,57 s) — vượt sàn cũ; chỉ theo dõi (PA1); ứng viên tối ưu sau (plan §9). 10 câu là mẫu nhỏ; đo máy khách httpx, không phải trình duyệt.
- Đường ngắt giữa luồng sau khi dời vòng stream vào lõi: **đã chạy thật** B131 (2 ca `curl -m`, trước chữ + giữa chữ).
- Độ trễ định tuyến 1,6–3,5 s / câu (pilot) ⇒ chữ đầu dự kiến chậm thêm tương ứng — chỉ theo dõi (User 13:36).

## 6. Khoá (cho phần kín — plan §5 bước 6, review C129 m-2)

**Khoá 20:23 02/11/2026** — commit nhánh `p9-b1` **`7e190d7`** (đã push). sha256 (12):
- `ROUTER_INSTRUCTIONS` (chuỗi) `fb4e1aa7f8fe` · `CHAT_INSTRUCTIONS` (chuỗi) `df921574c362` · `backend/llm/emergency.py` `3342783354d0` · `backend/config/settings.yaml` `0f12087f4d5a`
- công cụ cho C: `data/phase_9/b1/tools/p1_route.py` `ba7d7bb6bbc6`, `emergency_check.py` `f05e25c4975a`.

**C chạy phần kín** (từ `/tmp/b_p9b1/backend` hoặc worktree riêng ở `7e190d7`; `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag`):
1. P3: `python ../data/phase_9/b1/tools/emergency_check.py --sealed /home/minhhieu/hue_rag/data/phase_9/bo_do_b1/khan_cap_sealed.jsonl <ra_luat_sot.jsonl>` (0 USD) ⇒ (a) chặn nhầm câu thường kín, (b) luật bắt / sót.
2. P1: `--env-file /home/minhhieu/hue_rag/.env python ../data/phase_9/b1/tools/p1_route.py <ra.jsonl> --set /home/minhhieu/hue_rag/data/phase_9/bo_do_b1/tuyen_sealed.jsonl <ra_luat_sot.jsonl>` (≈ 0,002 USD) ⇒ định tuyến đúng / 20, sàn 1, lưới thứ hai cho câu khẩn cấp luật sót; lời trò chuyện của câu kín ⇒ sàn 2 (judge như §4).
3. Gửi B / A **chỉ số đếm** + sha đã kiểm. P2 kín: chưa có harness (P2 NOT RUN).

## 7. Bàn giao / chạy tiếp

**B131 xong (03/11):** (1)–(5) của phiên trước làm xong — §4b. **Tiếp:** C review delta `7e190d7..dcd1519` (C134) ⇒ A merge ⇒ 5 chỗ báo cáo.

**Đề xuất cờ (A đồng ý, chưa merge):** bật `router`, `may_have_changed_notice`; tắt `emergency_rule`, `today_line` (code giữ sau cờ). Đã vào mặc định ở `dcd1519`.
Chữ cho người dùng (§2) A chọn. Worktree `/tmp/b_p9b1` giữ cho review (đã build `frontend/dist/`; gỡ sau merge: `unlink` `data`, `knowledge-base-hue` rồi `git worktree remove`).
