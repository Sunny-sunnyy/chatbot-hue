# Review: Rà code C34 — kiểm chéo top 5 của C (C-09, C-02, C-01, C-12, C-19)

Decision: **ready_for_user_confirmation** (cả 5 finding đúng về chất; 0 blocker / 0 major với phần rà của C; 4 minor bổ sung để A gộp vào
TONG_HOP — không cần C sửa lại report trước khi trình User)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-c3`)
Date: 2026-10-25 18:49 +0700 (`date`) · `main` `c272644` (code giống `1e8cf8f`; chỉ thêm commit docs) · chỉ đọc · **0 USD**
Canonical guide: `CURRENT_HANDOFF.md` mục "Rà code các Phase trước" (tiêu chí, khuôn finding)
Implementation report: `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md` (bản C chốt top 10, đã commit ở `c272644`)

Căn cứ duy nhất: `ra_soat_code_C.md` + code + file kết quả có sẵn trong `data/`. Không đọc `STATUS_C.md`, không chạy script của C
(`data/ra_soat_code_2026-10-25/tools/*`); mọi số dưới đây từ script riêng của B ở `/tmp/b25x/`. **Xung đột lợi ích phải khai:** nhận định
"lỗi citation là model quên `[n]`" mà C-09 bác nằm trong report 8.1 G2 do **chính B viết** (`phase_8_1_g2_implementation.md:100, 132, 156`);
B đồng ý với C bằng số đo dưới, không bênh report cũ.

## 1. Phạm vi đã review

| Mục C | Đã đọc | Đã chạy (script B) |
|---|---|---|
| C-09 | `retrieval/full_corpus_context.py:78-86`, `llm/full_corpus_prompt.py:12`, `llm/citations.py` (toàn bộ), `api/routes/chat.py:120-157`, `frontend/app.js:39-60`, `evaluation/full_corpus_eval.py:345-367, 578-592`; report 8.1 G2 + G2 review + bảng G5 (dòng 3c, 6.6, 7) | `c09_recount.py` (11 lượt), `c09_shapes.py` (14 file) |
| C-02 | `experiments/phase_8_1/g2_generate.py:243-270`, `evaluation/full_corpus_eval.py:600-648`; plan E1 dòng 93-112; `p82-b1:backend/experiments/phase_8_2/b1.py` (nơi chép `paired`) | `c02_check.py` (input nhỏ) |
| C-01 (chỉ điểm mới a, b, c) | `api/app.py:1-100`, `api/routes/chat.py:60-82`, `retrieval/full_corpus.py:760-840` + danh sách mọi `raise` lớp lỗi; `ingestion/full_corpus_pipeline.py:10-50`; `session_prompt/chạy_môi_trường.md:6` | `c01_stale.py`, `c01_stale2.py` (không `.env`, không key) |
| C-12 | `guides/phase_7_…md:3-8, 19, 206`, `guides/phase_8_…md:12`, `full_corpus_rag.md:93`, `backend/evaluation/` | `grep` |
| C-19 | `retrieval/full_corpus_smoke.py:80-90, 264-271`, `llm/phase6_live_smoke.py:226-229, 493-494`; ngày file trace trong `data/` | `--help` từ `backend/` và từ gốc |

## 2. Findings

Kết luận từng mục (đúng / sai / một phần; mức; phương án sửa):

| Mục | Kết luận | Mức C ghi | B thấy mức | Phương án sửa |
|---|---|---|---|---|
| C-09 | **đúng** (số khớp 11 / 11 lượt) | cao | **hợp lý** | (1) đủ và an toàn trên dữ liệu có sẵn; thiếu 2 ý nhỏ (R-02, R-03) |
| C-02 | **đúng** | vừa | hợp lý | "thêm `sign`" một mình **chưa đủ** — `verdict` cũng ngược (R-04) |
| C-01 (a) | **đúng** — tái tạo được | (vừa) | hợp lý | — |
| C-01 (b) | **đúng** — đọc code xác nhận | — | — | bọc lỗi nạp model bằng `RetrievalDependencyError` là đúng chỗ; MiniLM (`:827-834`) cùng kiểu |
| C-01 (c) | **đúng** | — | — | trùng phương án B-01 (a/b/c) — một quyết định chung |
| C-12 | **đúng** | vừa | hợp lý | cùng loại B-16 ⇒ nên một lần sửa tài liệu chung (R-05) |
| C-19 | **đúng** | thấp | hợp lý | thêm một điểm đơn giản hóa C chưa nêu (R-06) |

### R-01 (minor) — C-09: "8 / 176 câu (4,5 %)" là một lượt; lượt cùng cấu hình khác cho 4 / 176
- Vị trí: `ra_soat_code_C.md` C-09 "Ở cấu hình đang chạy, 8 / 176 câu (4,5 %)…".
- Bằng chứng (`c09_recount.py`): 7B Run 1 (cấu hình đang chạy) 4 / 176 lỗi, cả 4 chỉ có `[Nguồn n]`; G2.0 (= chatbot hiện tại, lượt khác)
  4 dev + 4 test = 8 / 176, cả 8 chỉ có `[Nguồn n]`. Hai lượt cùng cấu hình ⇒ tỉ lệ người dùng gặp 500 khoảng **2–4,5 %**, không phải một số.
- Tiêu chí đóng: TONG_HOP ghi "4–8 / 176 câu ở hai lượt cùng cấu hình (≈ 2–4,5 %)".

### R-02 (minor) — C-09: mốc đã khóa không được ghi đè khi tính lại; định nghĩa mới phải chốt trước khi mở câu kín
- C-09 "Rủi ro khi sửa" nói mốc 7B / 8.1 / G0.6 phải tính lại. Thiếu: (a) `citation_error` là field **ghi sẵn** trong JSONL lúc sinh
  (`full_corpus_eval.py:361-364`), các file G0.6 bị khóa bằng hash (`data/phase_8_1/baseline/g0_6_manifest.json`) ⇒ tính lại phải ra **file
  dẫn xuất mới** (hoặc bảng trong report), không sửa file đã khóa; (b) câu kín 8.2 sẽ được chấm bằng chỉ số này ⇒ định nghĩa mới phải ghi
  vào spec / plan **trước** mốc mở câu kín, nếu không là đổi thước đo sau khi thấy kết quả.
- Thêm (quan sát): evaluator **giữ** text câu lỗi citation để judge chấm (`:362-364` "API trả 500 ở đây; vẫn giữ text để chấm") ⇒ Completeness /
  Accuracy 7B / 8.1 không đổi khi sửa C-09 (C nói đúng ở M2) — nhưng cũng nghĩa là điểm judge đang chấm cả câu mà người dùng thật **không thấy**
  (nhận 500). Chỉ cần ghi là giới hạn của mốc.
- Tiêu chí đóng: phương án (1) trong TONG_HOP ghi hai ràng buộc (a), (b).

### R-03 (minor) — C-09: kiểm an toàn của phương án (1) đã chạy được ngay, kết quả sạch
- C đề xuất đo 3 sàn khi sửa ("câu đang hợp lệ thành lỗi", "đổi tập nguồn", "id lạ"). B đã tính trên 11 lượt (`c09_recount.py`, thay
  `[Nguồn n]` → `[n]` rồi gọi **đúng** `select_cited_sources` production): **ok→err = 0**, **tập nguồn đổi ở câu đang hợp lệ = 0**, không câu nào trộn
  hai dạng, không id lạ; lỗi còn lại chỉ là "Grounded answer has no citation" (7B Run 2: 2; G2.4 none 2 / low 4 / high 1). `c09_shapes.py`: 14 file,
  **0** cụm ngoặc vuông có số nằm ngoài hai dạng `[n]` / `[Nguồn n]` (không có `[1, 2]`, `[Nguồn 1-2]`…), 0 câu NFD.
- Ý nghĩa: sàn của M1 đạt trên dữ liệu hiện có; khi sửa chỉ cần chạy lại như test + một câu `/api/chat` thật (như C ghi).
- Thêm cho UI: `frontend/app.js:44` chỉ tách `\[\d+\]` ⇒ phương án (1) **phải** đổi text về `[n]` trước khi trả (C đã ghi) — nếu chỉ nới regex
  validator mà không đổi text, UI hiện `[Nguồn 2]` là chữ thường không link. Route không stream (`chat.py:135-157` trả một lần) ⇒ đổi text trước
  `ChatResponse` là đủ, không có phần đã gửi dở.
- Plan E1 (`phase_8_2_e1_plan.md:103`) có chỉ số `uncited_non_refusal` "không có `[n]` (API trả 500)" ⇒ E1 phụ thuộc **cả** C-02 (dòng 95) **và**
  định nghĩa C-09 (dòng 103). Tiêu chí đóng: ghi vào TONG_HOP mục "plan E1 phải sửa".

### R-04 (minor) — C-02: phương án "thêm `sign` như evaluator" phải sửa cả `verdict`
- Bằng chứng (`c02_check.py`, 30 câu, mốc từ chối nhầm 6, biến thể 1 — biến thể rõ ràng tốt hơn): `g2 paired('refusal')` ⇒ `wins 0, losses 5,
  verdict worse`; `paired_compare` ⇒ `false_refusal: wins 5, losses 0, verdict better`. `verdict()` (`full_corpus_eval.py:604-611`) chỉ đảo chiều
  cho tên trong `LOWER_IS_BETTER = {false_refusal, citation_error}` — tên `"refusal"` không có ⇒ `verdict` cũng ngược, không chỉ thắng / thua.
- Ảnh hưởng 8.1: `grep -rln refusal_in_scope report_agent/` chỉ ra plan E1 và report C ⇒ report 8.1 không trích verdict / thắng-thua của chỉ số
  này (khớp *suy ra* của C). `p82-b1:…/phase_8_2/b1.py:119-137` có bản `paired` riêng nhưng chỉ gọi cho `ANSWER_METRICS` (điểm judge, càng cao càng
  tốt) ⇒ report B1 không bị.
- Tiêu chí đóng: phương án trong TONG_HOP là "dùng `paired_compare` (`false_refusal`)" — hoặc nếu giữ `paired`, đổi tên chỉ số thành `false_refusal`
  để cả `sign` lẫn `verdict` đúng; kiểm bằng input nhỏ trên ⇒ hai hàm cùng kết quả.

### R-05 (minor) — C-01 / C-12 / B-01 / B-16: gộp quyết định
- C-01 (c) đúng: `ingestion/full_corpus_pipeline.py` có 9 dòng `from backend.…`, không nhánh dự phòng ⇒ từ `backend/` import lỗi
  (`ModuleNotFoundError: No module named 'backend'`, B chạy); API chạy từ `backend/` (`chạy_môi_trường.md:6` `uv run uvicorn api.app:app`). Đây là
  cùng quyết định với B-01 (phương án a/b/c) ⇒ TONG_HOP nên trình **một** câu hỏi "chọn một quy ước import cho build, API, test, harness".
- C-01 (b) đúng và là điều kiện của mọi phương án B-01: `retrieval/full_corpus.py:816-823` bọc lỗi nạp / warm-up e5 thành `ComponentNotReadyError`,
  `:827-834` MiniLM cũng vậy ⇒ sửa import xong mà không đổi lớp ở hai chỗ này thì thiếu HF cache ⇒ 409 "cần lập chỉ mục lại". B kiểm thêm: Qdrant
  tắt lúc khởi động ⇒ `client.collection_exists` (`:800`) ném lỗi kết nối không bọc ⇒ `except Exception` ⇒ 503 — **không** đổi khi sửa C-01 (đúng).
- C-12 đúng (banner `phase_7:3-8` "chưa active" + `:19` "nguồn canonical"; `:206` `temperature=0` trái `full_corpus_rag.md:93`; `grep -c
  full_corpus_eval` = 0; guide 8 `not_ready`, 0 lần nhắc 8.1 / 8.2 / `gpt-6-luna`; 43 dòng `not_ready|canonical|gpt-5.4|MiniLM` ở hai guide). Cùng
  loại B-16 (guide 0–4) ⇒ một bộ phương án (banner lịch sử / viết lại phần hiện hành / chuyển `guides/history/`) cho cả 0–8.
- Tiêu chí đóng: TONG_HOP gộp hai cặp này.

### R-06 (minor) — C-19: điểm đơn giản hóa chưa nêu
- `phase6_live_smoke.py:226-229, 494` cờ `--confirm-paid` là "consent gate cho API đã duyệt" — `Session_Prompt.md` §7 liệt kê là cơ chế **đã loại**.
  Nếu chọn (A) giữ runner, bỏ cờ này cùng lúc. Các điểm khác của C-19 B kiểm lại khớp: `--help` từ `backend/` ⇒ `ModuleNotFoundError: No module
  named 'backend'`, từ gốc chạy được; mặc định `ALL_RERANKERS = ("none", "minilm")` (`:86`), `reranker="minilm"` chỉ ở `:268` (ngoài `retrieval/`);
  trace Phase 5 ngày 2026-09-13, live smoke 7A2 2026-10-24.
- Ghi thêm cho A: runner live này là chỗ duy nhất đi qua route HTTP ⇒ nó **sẽ** thấy cả C-01 lẫn C-09 (500) — lý do để giữ (A) nếu User muốn có một
  bước kiểm API thật trong 8.2.

## 3. Cách người kiểm chạy lại thật

Mọi lệnh: `uv run` trong `.venv` dự án, `HF_HUB_OFFLINE=1`, **không** `--env-file` (không key ⇒ không thể gọi API trả phí); không ghi file dùng chung,
không ghi Qdrant (chỉ đọc qua runtime thật), không gọi `/api/chat`.
- `cd backend && uv run python -I /tmp/b25x/c09_recount.py` — validator production trên câu trả lời đã sinh: 7B run1/run2, 8.1 G2.0 dev/test,
  G2.1a dev/test, 8.2 B1 dev/test, G2.4 none/low/high.
- `cd . && uv run python -I /tmp/b25x/c09_shapes.py` — 14 file JSONL.
- `cd backend && uv run python -I /tmp/b25x/c02_check.py` — input nhỏ dựng tay.
- `cd backend && uv run python -I /tmp/b25x/c01_stale.py` — `create_app` thật, settings thật, chỉ trong bộ nhớ `exclude_parts += ["foods"]`, lifespan qua
  `TestClient`, đọc `app.state` lúc khởi động; `c01_stale2.py` — gọi thẳng `build_full_corpus_retrieval_service` với cùng settings, in lớp lỗi.
- `cd backend && uv run python -m retrieval.full_corpus_smoke --help`; `cd . && uv run python -m backend.retrieval.full_corpus_smoke --help`.

## 4. Kết quả quan sát

- C-09 (`c09_recount.py`, mỗi dòng: lỗi hiện tại / chỉ `[Nguồn n]` / lỗi nếu nhận cả hai dạng): 7B Run 1 4 / 4 / **0**; 7B Run 2 6 / 4 / 2; G2.0 dev
  4 / 4 / 0, test 4 / 4 / 0; G2.1a dev 4 / 4 / 0, test 4 / 4 / 0; B1 dev 6 / 6 / 0, test 6 / 6 / 0; G2.4 none 8 / 6 / 2, low 9 / 5 / 4, high 4 / 3 / 1.
  Field `citation_error` ghi sẵn khớp số tính lại ở mọi lượt. **Khớp bảng của C ở cả 11 dòng** (dòng G2.1b không tính lại — R-03 đủ cho phương án).
- C-02: như R-04.
- C-01 (a): `đúng kho: retrieval_ready=True`; `kho thiếu domain foods: retrieval_ready=False status=503 code=retrieval_unavailable`; lớp ném ra
  `backend.core.schema.ComponentNotReadyError` "Full-corpus source state is stale", `is core.schema.ComponentNotReadyError` = False; module nạp đôi:
  `backend.core`, `backend.core.schema`, `backend.core.settings_loader`. *Về cách dựng:* đây là đường code thật với đầu vào khác (settings trong bộ
  nhớ), không mock, không đổi kho / Qdrant / môi trường dùng chung ⇒ B coi là hợp lệ với `Session_Prompt.md` §8; A xác nhận nếu muốn chặt hơn.
- C-12, C-19: như R-05, R-06.

## 5. Giới hạn hoặc phần chưa chạy

- C-09: không gọi `/api/chat` thật (paid) — tác động 500 suy từ code route + validator production, không quan sát qua HTTP. Không tính lại G2.1b / P1 / P2.
- C-01: trường hợp "Qdrant lỗi khi đang hỏi ⇒ 500" vẫn chỉ suy ra từ code (cả C lẫn B); không tắt Qdrant.
- C-01 (b): xác nhận bằng đọc code, không dựng lỗi thiếu HF cache.
- Chỉ kiểm 5 mục được giao; C-03 → C-20 còn lại không kiểm.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** — 5 / 5 finding đúng, mức hợp lý; 6 ý minor (R-01 → R-06) là bổ sung cho TONG_HOP, không cần vòng sửa riêng của C.
A gộp vào `TONG_HOP.md` rồi trình User chọn sửa gì. Gợi ý gộp câu hỏi cho User: (1) quy ước import (B-01 + C-01 c, kèm điều kiện C-01 b);
(2) C-09 phương án (1) + ràng buộc R-02; (3) tài liệu guide 0–8 một bộ phương án (B-16 + C-12); (4) harness 8.2 dùng `paired_compare` trước khi sửa
plan E1 (C-02 + R-03 dòng 103).

**Tự sửa của B (không thuộc C):** khi đọc `retrieval/full_corpus.py:815-823` B thấy runtime **đã làm nóng** e5 bằng một câu lúc khởi động ⇒ finding
**B-08** của B ("câu đầu chậm thêm ~1 s") **sai** (script đo của B nạp model không qua đường khởi động). B rút B-08 trong `ra_soat_code_B.md`.
