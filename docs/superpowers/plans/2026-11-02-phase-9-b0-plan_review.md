# Review: Phase 9 B0 — plan nền (`2026-11-02-phase-9-b0-plan.md`)

Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-cc`) · việc **C124** · 19:03 02/11/2026 (`date`).
Bản được review: **bản 1 sha `592a519bdd91`** (C tính lại từ file — khớp). Skill `risk-gated-agent-review`.
Chỉ dựa "Căn cứ để review" của plan (plan; spec bản 9 §3, §4 S-T1, §5 B0, §7, §8; handoff "Kế hoạch chi tiết tuần" + "Câu B hỏi A"; code `main` `a17a596`). Không đọc `STATUS_B` / tin nhắn của B.
Ngoài căn cứ C chỉ chạy dò 0 USD trên code `main` và mã nguồn SDK đã cài (`.venv`, openai-agents 0.19.4); không gọi mạng, không nạp `.env`.

## 1. Phạm vi đã review

- Mục tiêu / phạm vi (§1) đối chiếu spec §5 B0 và câu A trả lời B (B0 giữ đường RAG 1–8, mỗi nhà cung cấp một module, so chuỗi gửi model + T1 giống byte, không hai lõi). **Khớp.**
- 7 quyết định D1–D7: lý do, phương án khác, khi nào sai. Đánh giá độ đơn giản: D2 (chưa `function_tool`), D4 (sổ nguồn tối thiểu), D6 (không dời vòng stream) đều theo "ai dùng" (W48). **Không thấy phần phòng xa.**
- Tiêu chí ghi trước T-1…T-9: đo được không, có chạy 0 USD trước bước có phí không (§5 dòng "Thứ tự đảm bảo"). Tiền ước 0,003 / trần 0,01 USD khớp spec §8.
- `file:dòng` trong plan, đối chiếu với `main`: `chat.py:13, 17, 30, 118, 246, 332-392`; `full_corpus_eval.py:32, 47-50, 52 (CONCURRENCY = 4), 169-173, 301-325, 351`;
  `generator_openai_full_corpus.py:98-104, 179-270`; `test_api_chat.py:88, 144`; `test_chat_stream.py:16`; cờ CLI `retrieval --out`, `generate --golden smoke --cases … --out` (`full_corpus_eval.py:818-829`).
  **Tất cả khớp.** Có một chỗ thiếu ở m-3.

## 2. Findings

### M-1 (major) — T-2 không đo được như đang ghi: chuỗi gửi model **không ổn định ngay trên HEAD**

- **Vị trí:** plan §4 dòng T-2 (`json.dumps(kwargs, sort_keys=True)`, sha từng câu; "thân `/api/chat` = thân stream sau khi bỏ khoá `stream`"); §8 dòng 2.
- **Yêu cầu bị ảnh hưởng:** spec §5 B0 "`answer_case` qua lõi chung ra đúng câu trả lời đường RAG 1–8". Theo câu A trả lời và rủi ro C ghi trước, yêu cầu này đo bằng **chuỗi gửi model giống byte**. T-2 là tiêu chí chính của B0.
- **Bằng chứng** (`data/phase_9/c124_review/t2.py` sha `41d7d7bf030d`, 0 USD): thay `AsyncResponses.create` bằng hàm ghi kwargs rồi ném lỗi, đúng cách plan định làm; gọi `generate_answer` 2 lần, rồi `start_answer_stream` + đọc hết 2 lần, cùng câu, cùng ngữ cảnh:
  1. `json.dumps(kwargs, sort_keys=True)` **ném `TypeError: Object of type Omit is not JSON serializable`**. Có 14 / 26 khoá là `openai.Omit` ở đường thường và 13 / 26 ở đường stream. Nếu dùng `default=repr` thì chuỗi chứa địa chỉ bộ nhớ `0x…`, nên sha đổi theo tiến trình.
  2. **`prompt_cache_key` = `agents-sdk:run:<32 hex ngẫu nhiên>` sinh mới ở mỗi lần `Runner.run`** (`agents/run_internal/prompt_cache_key.py:124-129`). Đo được 4 lần ⇒ 4 sha khác nhau dù đầu vào giống hệt. Vì vậy T-2 (a) / (b) **không bao giờ đạt**, kể cả HEAD so với chính HEAD, và sẽ luôn chạm điều kiện dừng §8 dòng 2.
  3. Thường so với stream còn khác ở `extra_headers`: stream thêm `X-Stainless-Raw-Response: stream`, cùng với `stream` và `prompt_cache_key`. Nên câu "bỏ khoá `stream` là bằng nhau" sai.
  - Phần còn lại (`instructions`, `input`, `model`, `text`, `include`, `tools`, `max_output_tokens`, `store`…) giống nhau giữa các lần.
- **Tác động:** tiêu chí ghi trước không thoả được. B sẽ dừng ở bước 2, hoặc phải tự chế cách chuẩn hoá lúc chạy, tức là sửa tiêu chí sau khi đã thấy kết quả.
- **Tiêu chí đóng:** plan ghi **trước** cách chuẩn hoá trước khi băm, gồm danh sách khoá loại hoặc thay và lý do từng khoá. Ví dụ:
  - `Omit` ⇒ chuỗi cố định;
  - `prompt_cache_key` ⇒ chỉ kiểm có dạng `agents-sdk:run:*`;
  - so thường với stream sau khi bỏ `stream` + `X-Stainless-Raw-Response`.
  Giữ dòng §8 "HEAD hai lần phải cùng sha". Chạy thử 2 câu (bước 2) cho thấy HEAD hai lần cùng sha theo cách chuẩn hoá đó.

### m-1 (minor) — T-3 dựng cây từ `sys.modules` sau `import api.app` ⇒ bỏ sót module nạp lười

- **Vị trí:** plan §4 T-3 ("tiến trình con `import api.app` ⇒ lấy module dự án trong `sys.modules`").
- **Bằng chứng** (`data/phase_9/c124_review/d3.py` sha `b7baec658959`): C dựng cây theo cách khác, bằng AST tĩnh từ `api.app`, có tính cả `import` nằm trong hàm. Cây này có thêm đúng **1** module so với `sys.modules` (35 module dự án): `ingestion.preview`, được nạp lười ở `ingestion/chunking/full_corpus_chunker.py:293`. Module này **không** import thư viện mạng. `importlib` / `__import__` chỉ xuất hiện trong `tests/`.
- **Trả lời câu A (D3):** **hôm nay 0 module gọi mạng nằm ngoài cây.** Chỉ 3 module dự án import thư viện mạng:
  - `llm.generator_openai_full_corpus`: `agents`, `openai`;
  - `api.routes.chat`: chỉ lớp lỗi ở `:13`, `:17`;
  - `embedding.full_corpus`: `httpx`; xem thêm m-2.
  Cả 3 đều nằm trong danh sách D3.
- **Tác động:** sau này một client mạng được import trong hàm sẽ lọt khỏi T-3.
- **Tiêu chí đóng:** T-3 dựng cây bằng AST, có tính import trong hàm; hoặc plan ghi rõ giới hạn này.

### m-2 (minor) — danh sách thư viện mạng của T-3 thiếu `huggingface_hub`

- **Vị trí:** plan §2 D3 + §4 T-3 (danh sách `openai, agents, httpx, requests, aiohttp, urllib.request, http.client, socket, websockets`).
- **Bằng chứng:** `embedding/full_corpus.py:12` có `from huggingface_hub import snapshot_download` (dùng ở `:117`). Hàm này gọi HF Hub khi không bật `HF_HUB_OFFLINE`, mà runtime không mặc định bật (`Session_Prompt.md` §10). Lời gọi này chỉ tải model, không mang chữ người dùng, nên **không** phải lỗ rò dữ liệu.
- **Tiêu chí đóng:** thêm `huggingface_hub` vào danh sách quét, cho `embedding.full_corpus` được phép (lý do: tải model). Hoặc ghi rõ T-3 chỉ xét client có thể mang chữ người dùng, còn thư viện gọi mạng gián tiếp (`transformers`, `sentence_transformers`, `qdrant_client` tới `127.0.0.1`) nằm ngoài test.

### m-3 (minor) — D1 / §3 thiếu một nơi nhắc `llm.grounded_answer`

- **Bằng chứng:** `git grep -n grounded_answer -- backend` ra cả `tests/test_api_chat.py:169, 178, 180`. Đây là phép dò danh tính lớp lỗi (`GeneratorNotReadyError`, `CitationIntegrityError`). Bảng §3 chỉ ghi `test_api_chat.py` đổi phần trường log. T-7 vẫn bắt được, nên đây chỉ là chỗ thiếu trong mô tả.
- **Tiêu chí đóng:** thêm vào dòng `test_api_chat.py` của §3: đổi 3 chỗ `llm.grounded_answer` ⇒ `llm.assistant`.

### m-4 (minor) — T-1 sửa hàm đo dùng chung `run_retrieval_eval`

- **Vị trí:** §4 T-1 ("`run_retrieval_eval` … đổi sang lấy `documents` qua `tim_kho`; thêm dựng `context_builder`").
- **Bằng chứng:** `full_corpus_eval.py:301-325` hiện là hàm đồng bộ, có `treatment` và `shuffle_seed` (đối chứng dương 8.1 G0.2). `tim_kho` là `async`, cần `context_builder` (tokenizer).
- **Tác động:** đổi công cụ đo cùng lúc với thứ được đo. Nếu không giữ `treatment` / `shuffle_seed` thì lệnh cũ của các thí nghiệm đổi nghĩa.
- **Tiêu chí đóng:** plan nói rõ một trong hai cách. (a) Hàm vẫn nhận `treatment` / `shuffle_seed` như cũ, có lý do vì sao muốn bộ đo đi qua `tim_kho` từ nay (để mỗi bậc sau tự kiểm S-T1). (b) Hoặc dùng một script đo riêng ở `data/phase_9/b0/tools/`, để hàm cũ nguyên.

### Giờ ước trong plan (A dặn ghi minor) — **không còn trong bản này**

- Hook từng báo giờ dạng ước khi B ghi file. Trên bản `592a519bdd91`, chỉ có 2 dòng chứa giờ, đều ghi `(date)`: dòng 3 "viết 18:37 02/11/2026" và dòng 5 "B kiểm `sha256sum` 18:28 02/11/2026". Lệnh `grep -nE "[0-9]{2}:[0-9]x"` ra 0 dòng. ⇒ **Không có finding.** Cảnh báo của hook là lúc ghi bản nháp trước đó.

### D6 (A hỏi) — vòng stream ở lại `chat.py`: **không lệch spec ở B0**, không phải finding

- Spec §3 ghi "LÕI CHUNG `assistant.py` — route stream, `/api/chat` và `answer_case` cùng gọi". Hôm nay route stream đã gọi lõi chung cho phần trước model (`prepare_answer`, `chat.py:246`) và cho bước kiểm citation (`check_citations`, `chat.py:377`). Chỉ vòng đọc sự kiện của model nằm ở route (`chat.py:330-392`). Sau B0, chỗ này giữ nguyên, đúng như spec nói về lõi chung.
- Mục "Streaming" của spec §3 (thẻ trạng thái "đang hiểu câu hỏi…", lượt gọi công cụ không có chữ) thuộc B1 trở đi.
- **Nhắc cho plan B1** (không chặn B0): khi có hai lần `Runner` (định tuyến + trợ lý), plan B1 phải quyết vòng đọc sự kiện ở đâu và ai phát sự kiện trạng thái. Plan B0 D5 dòng "Sai khi" đã ghi phần `CallLog` nối danh sách.

### Ngoài phạm vi B0 (báo A, không đưa vào sửa)

- **Giả thuyết về tiền:** `prompt_cache_key` sinh mới mỗi lần `Runner.run`, kèm chú thích trong SDK: "reuse the key only inside this run". Đây có thể là lý do `cached_tokens` = 0 ở mọi câu (B95 30/10; giá đọc đệm 0,01 so với giá thường 0,10 USD / 1M). **Chưa chứng minh**: ngưỡng độ dài đệm của OpenAI và cách provider dùng khoá chưa kiểm.
- Thử chỗ này là đổi chuỗi gửi model, nên là thí nghiệm riêng (`run-experiment`), **không** làm ở B0.

## 3. Cách người kiểm chạy lại thật

```bash
cd backend && HF_HUB_OFFLINE=1 uv run python ../data/phase_9/c124_review/d3.py                                   # cây import động ↔ tĩnh + import mạng
cd backend && env -u OPENAI_API_KEY HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/phase_9/c124_review/t2.py   # bắt kwargs, không mạng
git grep -n grounded_answer -- backend
```

## 4. Kết quả quan sát

- d3: 35 module dự án sau `import api.app`; cây tĩnh có thêm `ingestion.preview`. Import mạng chỉ ở 3 module nêu ở m-1.
- t2: 4 lần bắt cho 4 sha khác nhau. Khoá khác nhau: `prompt_cache_key` (mọi lần), `stream` + `extra_headers` (thường so với stream). Có 14 giá trị `Omit` (thường) và 13 (stream). Mọi lần gọi đều dừng ở hàm giả (`Stop`), 0 request ra mạng.
- Probe dùng câu và ngữ cảnh tự viết, không dùng kho hay Golden. 0 USD.

## 5. Giới hạn hoặc phần chưa chạy

- C chưa chạy thử cách chuẩn hoá đề xuất ở M-1 trên `answer_case` hay `TestClient`. Probe chỉ dùng generator trực tiếp. Phần này là việc của B ở bước 2 của plan.
- Không review code, vì chưa có code. Không chạy T-1 / T-8.

## 6. Decision và bước tiếp theo

**`changes_requested`**: 1 major (M-1), 4 minor (m-1…m-4).

- B sửa M-1 trong một lượt: thêm cách chuẩn hoá vào §4 T-2, báo sha mới. Minor sửa cùng đợt, nếu không sửa thì phản biện. Theo luật làm vừa sức, **không mở vòng review mới cho minor**.
- C chỉ kiểm lại phần sửa của M-1 (và m-1…m-4 nếu B sửa). Ngoài ra không review lại cả plan.
- Sau đó A duyệt sha (tính từ file).

## Vòng 2 — kiểm phần sửa (bản 2 sha `c126e7432c82`, C tính lại từ file — khớp; 19:10 02/11/2026 `date`)

Phạm vi: chỉ bảng "Chỗ đổi bản 2" cuối plan, đối với M-1 và m-1…m-4 (A dặn). Không mở finding mới.

| Finding | Sửa ở (plan bản 2) | C kiểm thế nào | Kết luận |
|---|---|---|---|
| **M-1** T-2 không ổn định | §4 T-2 (HEAD chạy 2 lần trước; (c) so chéo) + bảng "T-2 — chuẩn hoá trước khi băm"; §5 bước 2; §8 dòng 2 | Viết lại đúng bảng chuẩn hoá (`Omit` / `NotGiven` ⇒ `"<omit>"` đệ quy; `prompt_cache_key` kiểm `^agents-sdk:run:[0-9a-f]{32}$` rồi thay `"<run-key>"`; so chéo bỏ `stream` + `X-Stainless-Raw-Response`). Chạy trên **2 tiến trình riêng**, mỗi tiến trình 2 lần thường + 2 lần stream (`data/phase_9/c124_review/norm_v2.py` `00c23079fe53`, 0 USD, không mạng) ⇒ cùng đường: thường `3903d5688f73` ×4, stream `c168ecbe6f11` ×4; so chéo: `75f84d95702b` ×8. Khẳng định của B `run_grouping.py:34` `uuid4().hex` ⇒ 32 hex: đúng. Luật "khoá đổi ngoài bảng ⇒ dừng, không thêm vào bảng sau khi thấy kết quả" đặt đúng chỗ | **đóng** |
| m-1 T-3 `sys.modules` | §4 T-3: cây tĩnh AST, gồm import trong hàm; ghi giới hạn `importlib` / `__import__` (chỉ ở `tests/`) | đối chiếu với probe vòng 1 (`d3.py`): cùng cách, cùng ví dụ `ingestion.preview` | **đóng** |
| m-2 thiếu `huggingface_hub` | §2 D3 (cho phép ở `embedding/full_corpus.py:12, :117`, lý do) + dòng thư viện gián tiếp ngoài test; §4 T-3 danh sách quét | dòng `:12` / `:117` khớp `main` | **đóng** |
| m-3 `test_api_chat.py` | §3 dòng test: 3 chỗ `:169, 178, 180` | khớp `git grep` vòng 1 | **đóng** |
| m-4 T-1 sửa hàm đo dùng chung | §3 + §4 T-1: `run_retrieval_eval` **không sửa**; (b) script riêng `t1_qua_tim_kho.py`, cùng khuôn dòng, `cmp` với (a) | đúng cách (b) của tiêu chí đóng | **đóng** |

Phần sửa không sinh lỗi mới. Có một ghi chú, không phải finding: T-1 (b) dựng `retrieval_service` theo **runtime** (`tim_kho` qua `deps`), còn (a) dựng theo `build_retrieval(load_settings(…), "dense_bm25_rrf")`. Nếu hai cách dựng khác profile thì (b) sẽ khác sha. Khi đó plan đã có điều kiện dừng §8 dòng 1, nên không phải sửa trước.

**Kết luận vòng 2: `ready_for_user_confirmation`** (bản `c126e7432c82`). A duyệt sha (tính từ file).
