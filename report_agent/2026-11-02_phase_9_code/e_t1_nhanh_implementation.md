# Implementation Report: Phase 9 T1 nhanh — câu ngày nhanh hơn (lịch code tính sẵn)

Người làm: E (Claude Code, `hue-rag-e4`) · Date: 19:37 10/11/2026
- Plan: `docs/superpowers/plans/2026-11-10-phase-9-t1-nhanh-plan.md` bản 1 `935f9358e25d` — mức nhẹ, A duyệt. Việc: `CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11".
- Nhánh `p9-t1-nhanh`: `5d0559b` (thay đổi chính) + `b8a96d8` (sửa "năm nay / năm sau", A chọn (a) sau lượt đo). Worktree `/tmp/e_t1_nhanh`.
- **Kết quả:** tiêu chí 1, 2, 4, 5, 6 **đạt**. Tiêu chí 3: lượt chính **tụt 1 câu** (Y2) ⇒ dừng, A chọn sửa bằng code (a) ⇒ lượt lại: ****không tụt** (8 câu "năm nay / năm sau": L 1 = mốc 1, Y2 nay OK)**. Tiền ≈ 0,031 USD.

## 1. Phạm vi

Câu có từ chỉ ngày (cờ `ngay_lich` bật): code tính sẵn ngày, đưa vào ngữ cảnh **trước** lần gọi model đầu, thay vì model gọi `ngay_lich` rồi mới viết.
Không đổi định tuyến, lời dặn trả lời, model. Câu không có từ chỉ ngày: không đổi.

**Thu hẹp sau vòng tự soi 1 (A chốt, theo ý C):** D1 chỉ giữ các dạng có trong bộ đo — hôm nay / ngày mai · từng ngày "tuần này" (gồm "chủ nhật này",
"thứ X này", "cuối tuần") / "tuần sau, tuần tới" · "rằm tháng này / tới / sau" · Tết / mùng N Tết · "rằm / mùng / mồng N tháng X" · "ngày N tháng X âm",
"N/N âm" · năm có số trong câu. **Bỏ so với plan:** "ngày kia", "tháng này", ngày dương có năm (không câu nào trong bộ cần). **Thêm sau lượt đo (A chọn (a)):**
câu nói "năm nay" / "năm sau, năm tới, sang năm" ⇒ dòng ngày của đúng năm âm đó.

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `backend/llm/ngay_lich.py` | `lich_san(cau, ngu_canh, now)` ⇒ (dòng, số ngày âm): dò các dạng ở mục 1 trong câu hỏi (+ câu hỏi liền trước) và trong đoạn kho lần tìm đầu (dạng có "âm" theo sau, hoặc rằm / mùng / mồng … tháng …; "tháng 3 Âm lịch" chỉ có tháng ⇒ bỏ); tối đa 6 ngày âm; mỗi ngày âm ⇒ lần gần nhất + lần sắp tới (dùng lại `_hai_lan`, thêm tham số nhãn) |
| `backend/llm/assistant.py` | `_before_model`: cờ `ngay_lich` + có từ chỉ ngày + lượt chưa từ chối sẵn ⇒ `_nguon_lich_san` đăng **một nguồn** "Lịch hệ thống" (id kế tiếp, như nguồn `ngay_lich`) nối sau ngữ cảnh; log `tools` thêm `{"name": "lich_san", "ms", "n_dong", "n_am"}` (chỉ số). Một chỗ phủ `/api/chat`, stream, song song #6. Không chạm `answer_turn_stream_parallel` / `AssistantFlags` (B) |
| `backend/llm/full_corpus_prompt.py` | `NGAY_LICH_MO_TA`: "hôm nay, mai, tuần, ngày âm trong câu / tài liệu đã có trong nguồn Lịch hệ thống — chỉ gọi khi cần ngày chưa có ở đó" (công cụ giữ làm dự phòng) |
| `backend/tests/test_ngay_lich.py` | + 4 test (dạng câu trong bộ · dò kho cần dấu âm + trần 6 · "năm nay / sang năm" · lần gọi đầu đã có nguồn lịch, trích nguồn đó qua kiểm citation — lượt đầu / lượt có lịch sử / không từ chỉ ngày × stream / không stream); 1 test cũ đổi số nguồn lịch 2 ⇒ 3 |

## 3. Thời gian từng bước (`date`) và lệnh

| Giờ / thời lượng | Bước |
|---|---|
| 19:09 | worktree + nhánh; plan; A duyệt ~19:12 |
| 17 s / 18 s | `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_ngay_lich.py -q` ⇒ 80 passed (sau sửa (a): 82 passed) |
| 29 s + 29 s | Q1: `env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python …/data/phase_9/b2_chay/tools/capture_all.py <out>` ở `main` và worktree |
| 19:20:19–19:22:06 (1 phút 47) | mốc: server `main` `fa7642a` (= `624a17b` về code) cổng 8861, `chay_t1.py … file:data/phase_9/t1_nhanh/bo_19.jsonl moc 1` |
| 19:22:56–19:24:01 (1 phút 05) | nhánh: server worktree cổng 8862, cùng bộ; rồi an toàn × 2 + Golden 9 tới 19:24:52 |
| 3 phút 44 | `pytest tests -q` cả `backend/tests` (không khoá) trên `5d0559b` |
| ~19:33–19:35:45 | lượt lại sau sửa (a): 8 câu "năm nay / năm sau" + 4 an toàn × 1 (chạy cùng lúc pytest của session khác ⇒ **không dùng cho tốc độ**) |
| ~3 phút × 2 | chấm mù bằng sub-agent (0 USD API) |

Đọc số: `chat_metrics` theo `turn_id` (log `backend/logs/application.log` của `main` / worktree). Dữ liệu: `data/phase_9/t1_nhanh/` (private).

## 4. Kết quả

**Tiêu chí 1–2 (tốc độ, tiền) — đạt.** Số tốc độ lấy từ lượt chính (máy không chạy việc nặng khác — B tạm dừng theo tin "bắt đầu đo").

| Nhóm | Mốc (`main`, T1 đang bật) | Nhánh |
|---|---|---|
| 19 câu ngày — chữ đầu p50 / p95 / max | 5,60 / 10,14 / 11,25 s | **2,35 / 4,56** / 8,87 s |
| 19 câu ngày — USD / câu | 0,00049 | **0,00036** |
| Câu đi trợ lý Huế (mốc n = 10, nhánh n = 8) — p50 / max | 5,98 / 11,25 s | 2,34 / 8,87 s |
| … trừ X14 (câu ngoài kho, model tìm kho 4 lần rồi từ chối — không do ngày; mốc 10,1 s) — p50 / max · USD / câu | 5,87 / 11,25 s · 0,00065 | **2,27 / 4,43 s · 0,00047** |
| Tổng lần gọi model (19 câu) · lần model gọi `ngay_lich` | 52 · 10 câu | **31 · 0** |

- **Model không gọi `ngay_lich` lần nào** ở nhánh (cả lượt lại, cả an toàn, Golden) — dự phòng chưa dùng trong bộ này (A hỏi, ghi chú 2).
- **9 / 19 câu bị định tuyến xếp ngoài phạm vi ở cả hai bên** (câu lịch thuần không nhắc Huế — giới hạn đã nhận 09/11) ⇒ không tới phần đổi; tốc độ của chúng là
  đường định tuyến (1 lần gọi). Số "19 câu" vì vậy gồm cả nhóm này — dòng "câu đi trợ lý" là số sát phần đổi.

**Tiêu chí 3 (đúng ngày không tụt).** `kiem_l2.py` (code): 0 cờ ở mọi file (mốc, nhánh, an toàn × 3, Golden 9, lượt lại). Một người chấm mù (sub-agent, brief
`data/phase_9/t1_nhanh/cham/brief.md` viết trước khi đọc câu trả lời) chấm 9 cặp khác chữ; 10 câu chữ giống hệt hai bên (9 câu ngoài phạm vi + X14 từ chối chuẩn — đúng, câu ngoài kho) ⇒ cùng nhãn, code đếm.

Bảng lượt chính (chữ đầu từ `chat_metrics.first_text_ms`; nhãn: chấm mù, đã mở khoá `cham/khoa.json`):

| Mã | Loại câu | Dạng D1 bật (nhánh) | Tuyến mốc → nhánh | Lần gọi model mốc → nhánh | `ngay_lich` mốc → nhánh | Chữ đầu (s) mốc → nhánh | Nhãn mốc → nhánh |
|---|---|---|---|---|---|---|---|
| R11 | hôm nay âm lịch (ngoài kho) | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 3,09 → 3,43 | R → R |
| A3 | rằm tháng tới | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 2,01 → 2,50 | R → R |
| A4 | hôm nay âm lịch | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 2,37 → 2,16 | R → R |
| A5 | Tết năm sau, thứ mấy | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 5,92 → 2,12 | R → R |
| A10 | thứ X tuần sau, âm lịch | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 3,12 → 2,18 | R → R |
| X1 | Tết năm có số, thứ mấy | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 1,93 → 1,70 | R → R |
| X8 | ngày mai âm lịch | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 2,84 → 4,56 | R → R |
| X12 | chủ nhật này, âm lịch | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 4,10 → 3,82 | R → R |
| X3 | Tết năm nay | — (định tuyến ngoài phạm vi) | Huế → ngoài | 4 → 1 | 2 → 0 | 8,42 → 2,39 | OK → R |
| Y1 | rằm tháng Giêng năm nay | — (định tuyến ngoài phạm vi) | Huế → ngoài | 4 → 1 | 2 → 0 | 5,87 → 3,29 | OK → R |
| Y2 | lễ ngày âm (kho), năm nay | 9 dòng, 3 ngày âm | Huế → Huế | 4 → 2 | 2 → 0 | 5,68 → 2,34 | OK → L1 |
| Y3 | còn mấy ngày tới rằm tháng Giêng | — (định tuyến ngoài phạm vi) | ngoài → ngoài | 1 → 1 | 0 → 0 | 2,90 → 2,99 | R → R |
| Y4 | lễ làng ngày âm (kho), sang năm | 5 dòng, 1 ngày âm | Huế → Huế | 4 → 2 | 2 → 0 | 5,11 → 2,21 | OK → OK |
| X14 | sự kiện tối nay (ngoài kho) | 2 dòng, 0 ngày âm | Huế → Huế | 6 → 6 | 1 → 0 | 10,14 → 8,87 | R (từ chối chuẩn, đúng) → R |
| X2 | còn bao nhiêu ngày tới Tết | 11 dòng, 4 ngày âm | Huế → Huế | 4 → 2 | 2 → 0 | 7,40 → 2,35 | OK → OK |
| X5 | lễ ngày âm (kho), năm sau | 7 dòng, 2 ngày âm | Huế → Huế | 4 → 2 | 2 → 0 | 5,98 → 1,67 | OK → OK |
| X6 | lễ làng ngày âm (kho), năm tới | 5 dòng, 1 ngày âm | Huế → Huế | 5 → 2 | 2 → 0 | 8,57 → 2,27 | OK → OK |
| X9 | lễ hội (kho), năm nay còn bao lâu | 2 dòng, 0 ngày âm | Huế → Huế | 5 → 2 | 1 → 0 | 11,25 → 4,43 | L2 → L2 |
| X13 | giờ mở cửa hôm nay (kho) | 2 dòng, 0 ngày âm | Huế → Huế | 3 → 2 | 1 → 0 | 5,60 → 2,07 | OK → OK |

- **Lượt chính:** mốc L 1 (X9) · nhánh L 2 (X9 giống mốc + **Y2 L1 mới**) + 2 câu R (X3, Y1) ⇒ **tụt** ⇒ dừng, báo A.
  - **Y2** (lễ ngày âm có trong kho, hỏi "năm nay", lần năm nay đã qua): nguồn tính sẵn có đủ lần đã qua + lần sắp tới + dòng ghi chú, model vẫn chọn lần năm sau và gọi là "năm nay".
    Mốc: model gọi công cụ với năm hiện tại ⇒ chỉ một ngày ⇒ đúng. ⇒ A chọn (a): code ghi thẳng dòng "năm âm lịch nay / sau" khi câu nói "năm nay / năm sau…" (`b8a96d8`).
  - **X3, Y1** (R ở nhánh, OK ở mốc): **dao động định tuyến**, không do thay đổi — Q1 cho thấy chuỗi gửi định tuyến giống byte ở mọi ca, phần đổi nằm sau định
    tuyến; ở mốc 7 câu cùng loại cũng bị xếp ngoài phạm vi. Lượt lại: X3 đi trợ lý (trả lời đúng), Y1 lại ngoài phạm vi (A5 cũng vậy, như mốc).
  - **X9** (L2 ở cả hai bên): người chấm ghi là **ca ranh giới** — câu "năm nay" của lễ hội rơi vào tháng Chạp năm âm trước; hiểu theo năm dương thì cả hai OK. Không đổi so mốc.
- **Lượt lại (sau sửa (a), 8 câu "năm nay / năm sau"):** người chấm mới (sub-agent, chỉ thấy câu trả lời nhánh, không thấy lượt trước): **OK 5** (X3, Y2, Y4, X5, X6) · **R 2** (A5, Y1 — định tuyến xếp ngoài phạm vi; mốc A5 cũng R) · **L2 1** (X9, ca ranh giới như trên — mốc cùng nhãn) · L1 0 · L3 0; người chấm tự đổi lại mọi ngày / thứ câu OK nêu: đúng. Cùng 8 câu ở mốc: OK 6 · R 1 · L2 1 ⇒ **số câu L nhánh = mốc (1 = 1)**; chênh R là Y1 (dao động định tuyến). Sửa (a) chỉ thêm ≤ 2 dòng chữ vào nguồn lịch khi câu nói "năm nay / năm sau" (không thêm lần gọi model) ⇒ số tốc độ / tiền của lượt chính vẫn dùng được; lượt lại 2 lần gọi model / câu như lượt chính, 0 lần `ngay_lich`.

**Tiêu chí 4 (giống byte) — đạt.** Q1 `main` ↔ nhánh: **215 / 228 ca giống byte**; 13 ca khác = **đúng** các ca bộ dò ngày bật (Golden 25, 26, 85, 90, 92, 93,
96, 114, 137 + an toàn S01, S02, S03, S12); lần gọi định tuyến giống byte ở **mọi** ca. (`data/phase_9/t1_nhanh/q1_main.jsonl`, `q1_nhanh.jsonl`)

**Tiêu chí 5 (an toàn S1) — đạt.** 4 câu bộ dò bật × 2 lượt (lượt chính) + 1 lượt sau sửa (a): **12 / 12 OK** — 0 đảo cảnh báo · 0 sai điều kiện · 0 thiếu cảnh báo · 0 ngoài kho bị trả lời.
28 câu an toàn còn lại: chuỗi gửi model giống byte (tiêu chí 4) ⇒ không chạy.

**Tiêu chí 6 (Golden bộ dò bật) — đạt.** 9 câu chỉ chạy bên nhánh (tự soi 1), chấm so đáp án mẫu: **9 OK** (G26 sát "thiếu" — bỏ một ngày nghỉ không được hỏi).

**Test:** `test_ngay_lich.py` 82 passed. Cả `backend/tests` (không khoá, trên `5d0559b`): **850 passed, 4 failed, 4 error** — đúng các test cần khoá OpenAI
(`test_api_chat::test_health_is_cached…`, `test_openai_full_corpus_generator` × 2, `test_phase6_live_smoke`, `test_phase6_settings::test_openai_api_key…`) và cần bản build
giao diện mà worktree không có (`test_static_ui` × 2, `test_ban_do_lich::test_csp_adds_tile_host…` — chạy trên `main` có bản build: passed). Sửa (a) chỉ chạm `lich_san` ⇒ chạy lại file chạm (82 passed), không chạy lại cả bộ.

**Tiền thật (`chat_metrics.usd`):** mốc 0,009263 · nhánh 0,006859 · an toàn × 2 0,004354 · Golden 9 0,004587 · lượt lại 0,003420 + an toàn 0,002374 ⇒ **≈ 0,0309 USD** (trần 0,1). Chấm: 0 USD API.

## 5. Lỗi và giới hạn

- Dạng ngày không có trong bộ ("ngày kia", "tháng này / tháng tới", ngày dương có năm, ngày âm viết bằng chữ "mồng mười") ⇒ không tính sẵn, model gọi công cụ như trước (không đo ở đây).
- Câu hỏi chung chung có từ chỉ ngày (vd "hôm nay âm lịch") ⇒ đoạn kho của lần tìm đầu có thể chứa tới 6 ngày âm không liên quan ⇒ thêm ~10–13 dòng ngữ cảnh (đo 0 USD trên đoạn thật: R11 6, A4 5 ngày). Chưa thấy làm sai câu nào; các câu này hiện bị định tuyến chặn trước.
- Cải thiện tốc độ chỉ tới câu được định tuyến cho đi trợ lý; 9 / 19 câu ngày bị xếp ngoài phạm vi (giới hạn cũ, ngoài việc này).
- n nhỏ (8–10 câu đi trợ lý mỗi bên, 1 lượt); X14 (ngoài kho) vẫn chậm do model tìm kho nhiều lần — không thuộc việc này.

## 6. Bàn giao cho C (review cả nhánh — chỉ chỗ rủi ro)

1. Regex dò ngày âm trong đoạn kho (`ngay_lich.py` `_AM_TIEN_TO`, `_AM_HAU_TO`, `_AM_SO`, `_THANG` — "tháng năm nay" ≠ tháng Năm) — chạy lại trên vài câu thật (0 USD, Qdrant chỉ đọc):
   `cd /tmp/e_t1_nhanh/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -c "from core.settings_loader import load_settings; from evaluation.full_corpus_eval import build_context_builder, build_retrieval; from llm import ngay_lich as nl; s=load_settings(validate_private_paths=False); r=build_retrieval(s, s['full_corpus_runtime']['retrieval_treatment']); c=build_context_builder(s); q='<câu tự viết có từ chỉ ngày>'; p=c.build(q, r.search(q).documents); print('\n'.join(nl.lich_san(q, p.text)[0]))"`
2. Nguồn lịch không chen khi lượt đã từ chối sẵn (`_before_model`: `trace.fixed_outcome is None`) và câu không từ chỉ ngày giống byte (Q1 ở mục 4).
3. Bảng từng câu ở mục 4; kết quả `data/phase_9/t1_nhanh/` (`ngay_moc.jsonl`, `ngay_nhanh.jsonl`, `nam_nhanh_2.jsonl`, `an_toan_nhanh_{1,2,3}.jsonl`, `golden9_nhanh.jsonl`, `cham/`).

## Đoạn lời thường cho `bao_cao_he_thong/` (A dán khi đóng đợt)

**Câu hỏi về ngày trả lời nhanh hơn (10/11, chưa merge).** Trước đây, với câu như "Tết năm nay vào ngày nào", chatbot phải hỏi model, model xin công cụ lịch,
rồi mới viết — 2–4 lần gọi model, chữ đầu chờ ~5–6 giây. Nay **code tự tính sẵn** hôm nay, ngày mai, các ngày trong tuần được hỏi, và đổi sẵn các ngày âm có trong câu
hỏi hoặc trong tài liệu vừa tìm được (lần đã qua, lần sắp tới, và đúng năm "năm nay / năm sau" nếu câu nói vậy), rồi đưa cho model **ngay lần đầu**. Đo 19 câu ngày (1 lượt):
chữ đầu trung vị 5,6 ⇒ 2,35 giây, 95 % câu dưới 4,6 giây; tiền 0,00049 ⇒ 0,00036 USD / câu; số câu sai ngày không tăng; câu an toàn và câu không nói về ngày không đổi.
Lần đo đầu có 1 câu "năm nay" bị model gọi nhầm lần năm sau ⇒ đã sửa bằng code, đo lại đúng. Giới hạn: gần nửa câu chỉ hỏi lịch (không nhắc Huế) vẫn bị xếp ngoài phạm vi
như trước; dạng ngày ít gặp (ngày kia, tháng tới…) vẫn đi đường cũ (chậm hơn).
