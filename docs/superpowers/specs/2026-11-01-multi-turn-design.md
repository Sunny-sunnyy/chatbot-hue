# Hội thoại nhiều lượt — tài liệu thiết kế (NHÁP — **DỜI SANG PHASE 9**, không làm ở Phase 1–8)

> **11:20 01/11/2026 (User):** lịch sử cuộc trò chuyện / hỏi tiếp được nghiên cứu ở phần **trợ lý / agent (Phase 9)**, không làm ở các Phase này. File này giữ làm **tư liệu đầu vào** cho nghiên cứu Phase 9 (chưa review, các `TBD` không điền; Q1 User nghiêng "trình duyệt giữ lịch sử" — chỉ là ý ban đầu). Không dùng làm căn cứ code.

Người viết: C · Ngày: 01/11/2026 (viết 11:08 01/11/2026, `date`) · Trạng thái: **bản 1 — nháp C102**. Còn `TBD` ở §2, §6 (chờ "Câu hỏi cho User" §11). Sau khi User chọn: A điền `TBD`, một session khác C review, User duyệt sha.
Gốc: nháp phương án C91 (private `data/tinh_nang_moi_2026-10-27/c91_phuong_an_nhieu_luot.md`, sha `1c0313aafd25`, PA1 = C nghiêng; chưa ai review, User chưa chọn). Spec streaming đã duyệt
`docs/superpowers/specs/2026-10-31-streaming-design.md` bản 5 `00fb57ee01b2` (commit `74a6082`). Code tham chiếu: nhánh `s1-loi-chung` commit **`9c83003`** (lõi chung sau S1 streaming). File tracked này **không chép nội dung kho,
câu Golden hay câu kín**; câu ví dụ là câu tự viết. Số liệu của dự án khác của User chỉ nằm ở file private (C91 §0 dẫn), ở đây chỉ nói "một dự án khác của User".

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `data/tinh_nang_moi_2026-10-27/c91_phuong_an_nhieu_luot.md` (`1c0313aafd25`) | §0–§5 | spec giữ đủ phương án, điểm khó, cách đo; không tự chọn thay User |
| code nhánh `s1-loi-chung` `9c83003` (`git show 9c83003:<file>`) | `backend/llm/grounded_answer.py`, `backend/api/routes/chat.py`, `backend/retrieval/full_corpus_context.py`, `backend/llm/{full_corpus_prompt.py, citations.py}`, `backend/evaluation/full_corpus_eval.py:321-361`, `frontend/app.js` | mọi `file:dòng` khớp code; thiết kế không làm đổi câu đủ ý (T1, prompt) |
| `docs/superpowers/specs/2026-10-31-streaming-design.md` (`00fb57ee01b2`) | §3, §4.1, §4.4, §4.6, §4.8 | nhiều lượt khớp route stream + lõi chung + log đã duyệt |
| `session_prompt/Project_Status.md` | §1 "Mục tiêu sản phẩm", §5 dòng 2026-10-28 09:59 | sàn tốc độ / tiền / thứ tự lỗi đúng quyết định User |

## 1. Mục tiêu

Hôm nay mỗi lần hỏi là độc lập: API chỉ nhận `query` (`backend/api/routes/chat.py:32-34`), tìm bằng đúng câu đó (`backend/llm/grounded_answer.py:50`), docstring "Single-turn" (`chat.py:1`); giao diện
xóa câu trả lời cũ trước mỗi lần hỏi (`frontend/app.js:83-84`). Người dùng thật hay hỏi tiếp bằng câu thiếu chủ thể ("còn giá vé ở đó?", "món này ăn ở đâu?") ⇒ hệ thống tìm bằng câu thiếu
chủ thể ⇒ từ chối nhầm hoặc trả lời về chỗ khác [giả thuyết — chưa đo trên hue_rag]. Mục tiêu: **câu hỏi tiếp được hiểu theo lượt trước**, mà câu hỏi đủ ý vẫn đi đúng đường hôm nay, server không phải giữ
dữ liệu người dùng (nếu User chọn D1 = trình duyệt), và mọi sàn chất lượng / tốc độ / tiền hiện hành giữ nguyên.

**Năm dòng khám phá** (skill `propose-options` §4b):
1. **Vấn đề + đo bằng gì:** câu hỏi tiếp thiếu chủ thể bị từ chối / trả lời lệch; đo bằng Completeness / Accuracy (judge Claude) của **lượt 2** trên bộ cặp câu tự viết (§5 M0), so với mốc "lượt 2 gửi như câu độc lập".
2. **Ba ô:** đo được — có (judge + bộ cặp, cùng cách đo 8.1 / 8.2); dữ liệu — **chưa có** câu hỏi tiếp thật (không lưu câu người dùng, `chat.py:24-25`) ⇒ bộ cặp tự viết, có phần giữ kín; giá trị — **làm khác đi** (hỏi tiếp được), không rẻ / nhanh hơn.
3. **Mốc đơn giản nhất:** hệ thống hôm nay (một lượt). Phương án "không làm gì" và "chỉ đổi giao diện" (PA0) cũng là mốc so (§11 Q1).
4. **Tiêu chí bằng số:** §6 (một phần `TBD` — User chọn sàn ở §11 Q3).
5. **Phương án B nếu dưới ngưỡng:** PA0 (gợi ý hỏi đủ tên trên giao diện, không đổi server); hoặc xem lại D2 (viết lại câu bằng model) nếu luật chữ sót phần lớn câu hỏi tiếp.

**Thử nhỏ trước khi viết (0 USD, chạy giữa 11:03 và 11:08 01/11/2026, chỉ in số đếm):** luật chữ mốc của C91 (câu mở đầu bằng "còn", hoặc ≤ 6 từ, hoặc có "đó / này / kia / ấy" và ≤ 25 từ) chạy trên câu **độc lập**
đang có: Golden 176 câu ⇒ **0** câu bị nhận nhầm là câu hỏi tiếp; bộ an toàn 32 câu ⇒ **2** (cả hai vì nhánh "đại từ + ≤ 25 từ"). Tổng **2 / 208** — vừa bằng mức C91 đề xuất (≤ 2 / 208). Trung vị độ dài: 14 từ
(Golden), 16 từ (bộ an toàn). Chưa đo: luật **bắt được** bao nhiêu câu hỏi tiếp thật (cần bộ cặp M0). Script tạm `/tmp/c102/dem_luat_chu.py` (đã xóa sau khi chạy; không ghi nội dung câu).

## 2. Quyết định

| Ngày / giờ (A ghi nhận) | Quyết định | Ai |
|---|---|---|
| 30/10/2026 14:39 | Thứ tự: streaming ⇒ hội thoại nhiều lượt ⇒ đóng gói Phase 1–8 ⇒ Phase 9 | User (`Project_Status.md` §5) |
| 30/10/2026 | Nhiều lượt làm **sau** streaming vì cùng sửa `chat.py` + `app.js` (dòng trên; nháp streaming v2 C77 "D0" — handoff gọi "spec streaming §2 D0", spec streaming không có dòng D0 riêng; spec streaming §3 ghi nhiều lượt là "Ngoài") | User / A |
| `TBD` | **D1 — lịch sử giữ ở đâu** (§11 Q1) | User |
| `TBD` | **D2 — nhận câu hỏi tiếp bằng gì** (§11 Q2) | User |
| `TBD` | **D7 — sàn + bộ đo** (§11 Q3) | User |
| `TBD` | **D8 — giao diện hiện lịch sử thế nào** (§11 Q4) | User |
| (đề xuất, chờ D1–D2) | **D3 — tìm bằng câu hiện tại hay ghép câu trước:** chọn **bằng đo** (PA1 ↔ PA2, §5 M2) theo luật ghi trước §6 — không chọn trước | A theo luật, báo User |
| (đề xuất, chờ D1–D2) | **D5 — đưa câu hỏi trước vào tin nhắn cho model (chỉ nhánh hỏi tiếp):** đo cùng lượt M2 (có / không) — đổi prompt chỉ ở nhánh hỏi tiếp | A theo luật, báo User |
| (đề xuất, A tự quyết — kỹ thuật) | D4: mang **≤ 3 đoạn đã được trích** của **một** lượt trước; D6: chỉ lượt **thành công có trích dẫn** được làm lượt trước (không: từ chối, lỗi, citation hỏng, stream rút / xóa / ngắt) | A |

Yêu cầu phi chức năng giữ nguyên (User 28/10, 01/11): tới chữ trả lời đầu tiên p50 ≤ 3 s / p95 ≤ 5 s (spec streaming C1); ≤ 0,0005 USD / câu; thứ tự lỗi: sai cảnh báo an toàn / điều kiện vào khu vực
> nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.

## 3. Phạm vi

**Trong** (theo PA1 — sẽ sửa lại nếu User chọn D1 / D2 khác):
- request hai route (`POST /api/chat`, `POST /api/chat/stream` của spec streaming) nhận thêm trường tùy chọn `previous`; phản hồi thêm mã đoạn cho mỗi nguồn;
- hàm thuần nhận câu hỏi tiếp; lấy lại đoạn lượt trước từ Qdrant (chỉ đọc) theo mã;
- builder ngữ cảnh nhận "đoạn mang sang" ngoài trần 10; prompt nhận "câu hỏi trước" (chỉ nhánh hỏi tiếp) — **một chỗ dựng** để đếm token đúng chuỗi gửi đi;
- lõi chung `answer_query` nhận thêm tham số tùy chọn (mặc định = hành vi hôm nay); bộ đánh giá thêm đường chạy **cặp** câu (không đổi `answer_case`);
- log `chat_metrics` thêm 2 trường số; giao diện giữ lượt trước + nút "Cuộc trò chuyện mới" + nhãn "đang hỏi tiếp về …".

**Ngoài:** server lưu lịch sử / tài khoản / đồng bộ nhiều thiết bị (trừ khi User chọn D1 khác); viết lại câu bằng model (trừ khi User chọn D2 khác); mang **nhiều** lượt trước; mang cả
câu trả lời trước vào prompt; giao diện mới (React…, sau Phase 8); lưu câu hỏi người dùng để đo; công cụ ngày cho câu "tối nay / tuần này" (Phase 9).

## 4. Thiết kế (theo PA1; phần phụ thuộc lựa chọn của User ghi rõ)

### 4.1 Luồng

```text
trình duyệt giữ lượt trước THÀNH CÔNG gần nhất: {query, source_refs[≤ 3]}   (D6: lượt từ chối / lỗi / rút / xóa / ngắt không ghi đè)
POST /api/chat(/stream) {query, previous?: {query, source_refs}}
  ├─ không có previous, hoặc is_followup(query) = false  ⇒ đường y hệt hôm nay (tìm, ngữ cảnh, prompt giống từng byte)
  └─ is_followup(query) = true
       ├─ tìm: bằng query (PA1)  |  bằng previous.query + " " + query (PA2)      — D3, chọn bằng đo
       ├─ lấy lại ≤ 3 đoạn theo source_refs từ Qdrant (đọc); mã lạ / không còn ⇒ bỏ, không lỗi
       ├─ ngữ cảnh: 10 đoạn mới + đoạn mang sang (bỏ đoạn đã có trong 10) đánh số tiếp [Nguồn 11]…; vượt ngân sách ⇒ bỏ đoạn mang sang
       ├─ prompt: thêm dòng "Câu hỏi trước (chỉ để hiểu ngữ cảnh): …" (D5, đo có / không)
       └─ sinh + kiểm citation: luật hôm nay, trên nguồn của CHÍNH lượt này
```

Server **không giữ gì** giữa hai lần gọi (PA1): `previous` đến cùng request, dùng xong bỏ; log không ghi chữ (§4.8).

### 4.2 Hợp đồng request / response

- `ChatRequest` hôm nay: `query` 1–500 ký tự, `extra="forbid"`, `str_strip_whitespace` (`chat.py:32-34`). Thêm `previous: PreviousTurn | None = None`, với `PreviousTurn{query: str (1–500),
  source_refs: list[str] (0–3)}`, cũng `extra="forbid"`. Thân sai ⇒ 422 của FastAPI trước handler như hôm nay (spec streaming §4.6: không có dòng log).
- `SourceResponse` hôm nay: `id, title, heading_path, excerpts` (`chat.py:37-41`) — không có mã đoạn. Thêm `ref: str`.
  - **A tự quyết (đề xuất C): `ref` = point id UUID** (`point_id_for_chunk_id`, `backend/core/schema.py:53-55`), **không** phải `chunk_id`: `chunk_id` có dạng `<đường dẫn file kho>#<số>`
    (`schema.py:78-80` `validate_chunk_id`; `RetrievedDocument.id` = `chunk_id`, `backend/retrieval/full_corpus.py:296`) ⇒ lộ tên file kho qua API; UUID lấy thẳng được bằng Qdrant mà không lộ đường dẫn.
- `PackedSource` hôm nay không mang mã đoạn (`backend/retrieval/full_corpus_context.py:9-14`), và builder **bỏ qua** tài liệu không có `evidence_parts` (`:60-61`, `:90-92`) ⇒ số `[n]` không suy ngược
  được từ vị trí trong `documents` ⇒ `PackedSource` thêm trường `ref` (điền lúc build) để route trả về đúng mã của nguồn được trích.
- Phản hồi JSON và sự kiện `sources` của route stream (spec streaming §4.4) đều dùng cùng `SourceResponse` ⇒ thêm `ref` một chỗ.

### 4.3 Nhận câu hỏi tiếp — `is_followup(query) -> bool` (hàm thuần, D2 = luật chữ)

- Mốc: luật C91 (§1 "thử nhỏ"). Chuẩn hóa NFC trước (như `normalize_query`, `full_corpus.py:97`). Ngưỡng **chỉnh trên phần "đã thấy" của bộ cặp M0**, khóa trước khi đo phần kín.
- Chỉ gọi khi request có `previous` — câu đầu phiên luôn đi đường hôm nay.
- Bắt nhầm (câu đủ ý bị nhận là hỏi tiếp) chỉ **thêm** đoạn lượt trước vào cuối ngữ cảnh — không bỏ đoạn mới nào ⇒ hại chính là đổi ngữ cảnh / prompt của câu đó ⇒ đếm bằng sàn ở §6 C2.
- Hạn chế đã biết: câu lược chủ thể không có chữ báo hiệu sẽ bị sót (một dự án khác của User báo sót phần lớn loại này — số ở file private C91 §0).
- D2 khác (viết lại câu bằng model): thêm một lần gọi model / câu hỏi tiếp, ước +~1,8 s (C91 §2 PA3, số của dự án khác) ⇒ ăn vào sàn chữ đầu tiên 3 / 5 s; khi đó §4.3–§4.5 viết lại.

### 4.4 Lấy lại đoạn lượt trước

- Retrieval service đã giữ client Qdrant (`full_corpus.py:414`) và tên collection (`:437`); thêm một hàm đọc `client.retrieve(collection, ids=source_refs, with_payload=[7 trường])` (API có trong bản
  `qdrant-client` đã cài, `.venv/…/qdrant_client/qdrant_client.py:1078`) ⇒ `validate_point_payload` (`full_corpus.py:181`) ⇒ `build_retrieved_document` (`:290-306`). Không ghi Qdrant.
- **Ranh giới tin cậy:** server **không** nhận chữ nguồn từ trình duyệt — chỉ nhận mã, tự đọc đoạn từ kho ⇒ người sửa request tay cũng chỉ chọn được đoạn **có thật trong kho** (closed-world giữ).
  Mã không tồn tại / payload sai ⇒ bỏ mang nguồn cho request đó (`n_carried_sources = 0`), **không** 422 / 503.
- **Sau khi build lại index** (sửa kho), `chunk_id` có thể **dồn số** (đợt 2 sửa kho: 2 file — bảng giới hạn dòng 10, private `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md`) ⇒ mã cũ trỏ sang đoạn khác cùng
  file. Hệ quả: mang sang một đoạn **có thật** nhưng có thể không liên quan (thêm bằng chứng thừa, không bịa). A tự quyết giữ hay thêm dấu phiên bản index vào `ref` — C đề xuất **giữ đơn giản** (sửa kho hiếm,
  phải khởi động lại server; trình duyệt tải lại trang là mất lịch sử), ghi giới hạn.

### 4.5 Ngữ cảnh, đánh số, ngân sách

- Builder hôm nay: dừng ở `max_documents` (`full_corpus_context.py:88`; `settings.yaml:56` = 10), đánh số `len(sources) + 1` (`:90`), nhãn `[Nguồn n]` (`:75`), kiểm ngân sách
  `candidate_tokens + reserved + margin ≤ context_limit` (`:93-95`; 16.384 / 2.048 / 512, `settings.yaml:53-55`).
- Thêm tham số `carried: Sequence[RetrievedDocument] = ()` cho `build`: sau vòng 10 đoạn mới, thêm từng đoạn mang sang **không trùng** `chunk_id` với đoạn đã có, số tiếp theo (thường `[Nguồn 11]`…`[13]`;
  ít hơn 10 đoạn mới thì số liền sau đoạn cuối), **cùng** phép kiểm ngân sách; không vừa ⇒ dừng thêm (không lỗi — khác đoạn hạng 1, `:96-98`). `carried=()` ⇒ vòng lặp hôm nay, **chuỗi ngữ cảnh giống từng byte**.
- Đoạn mang sang luôn ở **cuối** ngữ cảnh (sau 10 đoạn tìm mới) — ưu tiên bằng chứng của câu hiện tại.
- Prompt: `build_answer_input(query, context)` là **một chỗ dựng** tin nhắn user, dùng cho cả đếm token (`full_corpus_context.py:40-47` qua `build_answer_messages`) và gửi model
  (`generator_openai_full_corpus.py:225-228`) (`full_corpus_prompt.py:18-27`, C-03). D5 = có ⇒ thêm tham số `previous_query: str | None = None` vào `build_answer_input` / `build_answer_messages`,
  builder và `generate_answer` truyền cùng giá trị ⇒ token đếm vẫn đúng chuỗi gửi đi; `None` ⇒ chuỗi giống từng byte hôm nay. Dòng thêm đặt **trước** "Câu hỏi:" và ghi rõ "chỉ để hiểu ngữ cảnh";
  lời dặn hệ thống (`full_corpus_prompt.py:7-16`) đã coi câu hỏi là dữ liệu không đáng tin ⇒ không đổi lời dặn hệ thống.

### 4.6 Citation

- Không đổi luật: `select_cited_sources` nhận mọi `n` có trong `sources` của **chính lượt đó** (`backend/llm/citations.py:30-34`) ⇒ `[11]`–`[13]` hợp lệ khi đoạn mang sang có trong ngữ cảnh.
- Giao diện ánh xạ `[n]` ⇒ thẻ nguồn của **lượt đang hiện** (`app.js:39-69`, `#source-n`); lượt trước bị thay (D8 = chỉ hiện lượt mới) hoặc có khung riêng (D8 khác) ⇒ id thẻ phải theo lượt để không trùng.

### 4.7 Lõi chung và bộ đánh giá

- `answer_query(query, retrieval_service, context_builder, generator, trace, recorder=None)` (`grounded_answer.py:43`) thêm tham số `followup: FollowupInput | None = None` (câu trước + đoạn đã
  lấy). `None` ⇒ đúng các bước hôm nay (`:50`, `:57`, `:73`, `:83`) ⇒ `answer_case` (`full_corpus_eval.py:340`) không đổi ⇒ **T1 giống byte** `4d5bbe9e0edc` và Golden đi đường cũ.
- Nhận câu hỏi tiếp + lấy đoạn chạy **trước** `answer_query` (ở route / harness cặp), để lõi không phụ thuộc request HTTP; route stream (spec streaming S2) dùng cùng hàm.
- `AnswerTrace` (`grounded_answer.py:25-40`) thêm `followup: bool`, `n_carried: int` để route ghi log, harness ghi dòng kết quả.
- Bộ đánh giá: hàm mới chạy **cặp** (lượt 1 qua `answer_query`, lấy nguồn được trích ⇒ lượt 2 có / không `followup`); dòng kết quả ghi như `answer_case` + `followup`, `n_carried`. Dữ liệu cặp private ở `data/`.
- Khác biệt route ↔ `answer_case` của spec streaming §4.8 giữ nguyên (không chuẩn hóa `[Nguồn n]` ở bộ đánh giá, giữ chữ khi citation hỏng…).

### 4.8 Log `chat_metrics`

- Giữ chính sách: không ghi câu hỏi, câu trả lời, nguồn, mã đoạn, id (`chat.py:24-25`) ⇒ **không** ghi `previous.query` hay `source_refs`.
- `METRIC_FIELDS` (`chat.py:26-29`) thêm `followup` (bool; `None` khi request không có `previous`) và `n_carried_sources` (int). Test khóa tập trường (`backend/tests/test_api_chat.py:88`) sửa có chủ đích.

### 4.9 Giao diện (`frontend/app.js`, JS thuần, sửa tối thiểu)

- Sau lượt **thành công có trích dẫn** (JSON 200 không phải câu từ chối; stream: `done{success}` có `sources`) ⇒ lưu `{query, source_refs: ref của ≤ 3 nguồn được trích đầu tiên}` trong biến JS (mất khi tải lại
  trang — chấp nhận, không `localStorage` ở bản này). Lượt từ chối / lỗi / rút / xóa / ngắt ⇒ **giữ** lượt trước cũ (D6).
- Gửi `previous` trong mọi request khi đang có lượt trước. Nút "Cuộc trò chuyện mới" xóa lượt trước.
- Khi phản hồi cho biết là câu hỏi tiếp (thêm trường `followup` trong phản hồi / sự kiện `status`) ⇒ nhãn nhỏ "Đang hỏi tiếp về: <tiêu đề nguồn lượt trước>" để người dùng biết hệ thống hiểu câu là nối tiếp
  (giúp sửa khi luật bắt nhầm) — **TBD theo D8**.
- Hiện lịch sử: **TBD theo D8** (chỉ lượt mới như hôm nay `app.js:83-84` / khung hội thoại cuộn).

## 5. Bước làm (mỗi bước review chéo trước bước sau; bắt đầu **sau** khi streaming S1–S4 đóng)

| Bước | Làm | Kiểm trước khi qua bước sau |
|---|---|---|
| M0 | **Bộ đo** (chỉ dữ liệu, có thể làm song song streaming): ~40 cặp câu tự viết, lượt 1 có đáp án trong kho (dạng câu Golden), 5 loại (a) hỏi lại ý đã có trong nguồn lượt 1 · (b) hỏi ý mới cùng chủ thể · (c) hỏi tiếp **ngoài kho** · (d) hỏi tiếp về **điều kiện / cảnh báo** · (e) đổi chủ đề bằng câu ngắn; chia **đã thấy / kín** (theo §11 Q3); tiêu chí §6 ghi trước; mốc + A/A lượt 2 gửi như câu độc lập | session khác review bộ cặp + tiêu chí (W32: ca dò khác cách); User duyệt mẫu theo Q3; sha bộ cặp ghi vào report |
| M1 | Lõi: `is_followup`, đọc đoạn theo `ref`, builder `carried`, prompt `previous_query`, `answer_query(followup=…)`, harness cặp (chưa đổi API) | **T1 giống byte**; chuỗi prompt của câu không có `followup` giống byte (test logic); bắt nhầm trên 176 + 32 câu (§6 C2); test file chạm |
| M2 | Đo trên phần "đã thấy": mốc ↔ PA1 ↔ PA2, D5 có / không (tổ hợp đo **ghi trước**, mỗi nhánh một lượt, judge cùng lượt mù); chọn D3 / D5 theo luật §6; **xác nhận** cấu hình chọn trên phần kín | report + review; vượt trần tiền ⇒ dừng |
| M3 | API cả hai route + log + `ref` trong `SourceResponse` | cổng ổn định cả hai route (spec streaming C4) + 1 cặp hỏi tiếp + 1 request `ref` lạ (200, `n_carried_sources = 0`); grep câu hỏi trong log = 0 |
| M4 | Giao diện + đo tốc độ câu hỏi tiếp trên trình duyệt | Playwright: cặp hỏi tiếp hiện nhãn, nút "Cuộc trò chuyện mới", lượt lỗi không ghi đè lượt trước; §6 C6; ghi báo cáo + 5 chỗ (`WORKFLOW.md` §6) |

Ước công [Ước]: M0 ~0,5 ngày; M1–M4 2–3 ngày code + test + review (C91 §2). Mỗi bước: khai báo file trong `STATUS_<X>.md`, nhánh riêng, skill `practical-project-coding` + `run-experiment` (M0, M2).
Trước khi merge M1–M4: review **cả nhánh** bằng một sub-agent ngữ cảnh mới (như spec streaming, handoff mục "Khi code" a1); M1 đổi hàm dùng chung ⇒ `git grep` mọi nơi gọi trước khi sửa.

## 6. Tiêu chí nghiệm thu (bằng số — `TBD` chờ §11 Q3; số dưới là **đề xuất của C**)

| # | Tiêu chí | Ngưỡng | Cách đo |
|---|---|---|---|
| C1 | Câu đủ ý không đổi | T1 giống byte `4d5bbe9e0edc`; chuỗi prompt + ngữ cảnh câu không có `followup` giống byte | harness T1; test logic so chuỗi |
| C2 | Bắt nhầm câu đủ ý | `TBD` — đề xuất **≤ 2 / 208** (176 Golden + 32 bộ an toàn; hôm nay luật mốc = 2 / 208); mọi câu bắt nhầm đo ở cả hai nhánh, **0 câu tụt** Completeness / 0 P0_sai mới | chạy `is_followup` trên câu thật (0 USD; private, chỉ in số đếm); câu bị bắt: sinh 2 nhánh, judge |
| C3 | Lợi ở câu hỏi tiếp (chỉ số quyết) | `TBD` — đề xuất: lượt 2 loại (a) + (b): Completeness TB theo cặp (PA ↔ mốc) **CI 95 % > 0** (bootstrap) **và** số câu tụt ≤ A/A + 3 | judge Claude cùng lượt mù; mốc = lượt 2 gửi như câu độc lập |
| C4 | Câu hỏi tiếp ngoài kho (c) | **0** câu bị trả lời (sàn hiện hành "0 câu ngoài kho bị trả lời") | judge + đọc tay mọi câu (c) |
| C5 | Câu hỏi tiếp điều kiện / cảnh báo (d) | **0** đảo cảnh báo; P0_sai mới ≤ 2 (hai chiều, như bộ an toàn) | thước lỗi nặng (judge tách ý) |
| C6 | Tốc độ câu hỏi tiếp | tới chữ đầu tiên vẫn đạt sàn p50 ≤ 3 s / p95 ≤ 5 s (spec streaming C1); thêm so với câu độc lập: `search_ms + context_ms` p50 tăng ≤ **+100 ms** (không thêm lần gọi model) | log `chat_metrics` lượt M2 + Playwright M4 |
| C7 | Tiền | ≤ 0,0005 USD / câu hỏi tiếp (token vào thêm ~3 đoạn) | token từ log, giá User 30/10 |
| C8 | Server không giữ dữ liệu người dùng (D1 = trình duyệt) | không biến / bộ nhớ nào giữ `previous` sau khi request xong; log không có chữ câu trước | đọc diff + grep log |
| C9 | Đổi chủ đề (e) | số câu tụt Completeness so mốc ≤ 1 | như C3 |

**C3, C4 hoặc C5 trượt trên phần kín** ⇒ dừng trước khi vào chatbot (không đo lại để "qua"); A trình User: PA0 / giữ một lượt / đổi D2.
Cỡ mẫu ~40 cặp ⇒ (a) + (b) ~20 câu: chỉ phát hiện được lợi lớn; "chưa rõ" là kết quả dễ xảy ra (`run-experiment`: ghi trước, kết quả âm giữ).

## 7. Cách kiểm

**Đường thật** (server thật, Qdrant chỉ đọc, model thật): cổng ổn định cả hai route có / không `previous`; `ref` lạ / sai định dạng ⇒ 200 + `n_carried_sources = 0`; một cặp hỏi tiếp trên trình duyệt
(Playwright); đo M2 bằng harness cặp (không qua HTTP) + latency qua log.
**Logic thuần** (input nhỏ tự viết, không chép Golden vào test — file tracked): `is_followup` (câu có / không chữ báo hiệu, NFC / NFD); builder `carried` (trùng, vượt ngân sách, ít hơn 10 đoạn mới, `carried=()` giống byte);
`build_answer_input(previous_query=None)` giống byte; schema `previous` (thừa trường ⇒ 422, > 3 `ref` ⇒ 422).
**Ghi giới hạn:** không có câu hỏi tiếp thật của du khách (bộ tự viết); chỉ một lượt trước; tải lại trang mất lịch sử.

## 8. Quyền và tiền

- Code trên nhánh riêng theo việc; B / C push nhánh khi việc ghi rõ; A commit / push `main`. Không thêm thư viện (Qdrant `retrieve` có sẵn).
- API trả phí (`gpt-6-luna`) [Ước, 0,00025 USD / câu]: M0 mốc + A/A ~80 lần ≈ 0,02; M2 ~40 cặp × (lượt 1 + 4 nhánh lượt 2) ≈ 200 lần ≈ 0,05; xác nhận phần kín + cổng ≈ 0,01 ⇒ **trần cả việc 0,1 USD**
  (`TBD` theo số nhánh User / A chốt). Lượt nào vượt ước > 50 % ⇒ dừng, báo A. Judge: quota Claude. Ghi usage token + tiền mỗi lượt.
- Không ghi Qdrant; không đổi kho / Golden; bộ cặp private (`data/`).

## 9. Rủi ro

| Rủi ro | Cách giảm |
|---|---|
| Câu đủ ý đổi hành vi (bắt nhầm, hoặc code nhánh mới rò vào đường cũ) | C1 (T1 + chuỗi prompt giống byte), C2 đếm bắt nhầm; tham số mặc định = hành vi cũ |
| Câu hỏi tiếp **ngoài kho** được trả lời bằng nguồn lượt trước (M3 / M2) | loại (c) trong bộ đo, sàn C4 = 0; lời dặn "bằng chứng không đủ ⇒ câu chuẩn" giữ nguyên |
| Đổi chủ đề bằng câu ngắn ⇒ nguồn cũ lạc đề kéo câu trả lời | loại (e), C9; đoạn mang sang ở cuối ngữ cảnh |
| Người dùng sửa request tay để chèn chữ | server chỉ nhận mã đoạn, tự đọc từ kho (§4.4); câu trước là dữ liệu (lời dặn hệ thống hiện có) |
| Mã đoạn cũ sau build lại index | đoạn có thật nhưng có thể lạc đề — giới hạn (§4.4) |
| Ngân sách token | đoạn mang sang thêm sau cùng, không vừa thì bỏ (§4.5); hôm nay TB ~1.657 token vào (C91 §0) ⇒ còn rộng |
| Sửa cùng file với streaming | bắt đầu sau khi streaming đóng (§2); M0 chỉ dữ liệu |

## 10. Giới hạn

- Bộ đo tự viết, ~40 cặp ⇒ chưa đại diện câu hỏi tiếp thật; kết luận nhiều khả năng "chưa rõ" ở loại (b).
- Chỉ nhớ **một** lượt trước, ≤ 3 đoạn đã trích; không nhớ câu trả lời trước (model không thấy mình đã nói gì).
- Luật chữ sót câu lược chủ thể không có chữ báo hiệu.
- Lịch sử mất khi tải lại trang / đổi thiết bị (D1 = trình duyệt).
- Mã đoạn không bền qua lần build lại index (§4.4).
- Không có công cụ ngày ⇒ "tối nay / tuần này" vẫn như hôm nay (Phase 9).

## 11. Câu hỏi cho User (A hỏi mỗi lần một câu, theo thứ tự)

**Q1 — Lịch sử cuộc hỏi giữ ở đâu? (D1)**
- **PA1 — trình duyệt giữ, server không lưu (C khuyên).** Là gì: trang web nhớ câu trước + mã ≤ 3 đoạn đã trích, gửi kèm câu sau; server dùng xong là bỏ. Đổi gì: API thêm một trường tùy chọn; log
  vẫn không có chữ. Tốn: 0 lần gọi model thêm; +~vài chục ms đọc 3 đoạn [Ước]. Khi nào sai: muốn xem lại lịch sử sau khi tải trang / trên máy khác; muốn đo câu hỏi thật của người dùng (vẫn không có dữ liệu).
- **PA0 — giữ một lượt, chỉ đổi giao diện:** gợi ý "hãy hỏi đủ tên nơi / món" khi câu ngắn; nút "hỏi tiếp về nguồn này" chèn tên nguồn vào ô hỏi. Tốn < 1 ngày, 0 rủi ro chất lượng. Khi nào sai: người dùng vẫn gõ
  "còn giá vé ở đó?" ⇒ như hôm nay; đồ án kém giống sản phẩm thật.
- **PA3 — server lưu có hạn (RAM, ~30 phút):** cần cookie phiên, server **giữ câu hỏi người dùng** (đổi chính sách dữ liệu hiện hành `chat.py:24-25`); mất khi khởi động lại, deploy nhiều worker cần chỗ chung.
  Khi nào đáng: muốn mang **nhiều** lượt / đo câu thật.
- Chọn khác PA1 thì mất gì: PA0 mất khả năng hỏi tiếp thật; PA3 thêm việc + đổi chính sách dữ liệu.
- *Tự kiểm:* "Ở PA1, nếu tôi hỏi một câu về một di tích rồi hỏi 'còn giá vé ở đó?', hệ thống làm gì khác hôm nay, và vì sao server vẫn không phải lưu câu hỏi của tôi?"

**Q2 — Nhận ra "câu hỏi tiếp" bằng gì? (D2)**
- **Luật chữ (C khuyên):** hàm thuần nhìn chữ báo hiệu ("còn…", "đó / này / kia / ấy", câu rất ngắn). Tốn 0 ms / 0 USD; thử nhỏ: bắt nhầm 2 / 208 câu độc lập (§1). Khi nào sai: câu lược chủ thể không có chữ báo hiệu (bị sót).
- **Model viết lại câu thành câu đủ ý:** hiểu cả câu không chữ báo hiệu. Tốn +1 lần gọi / câu hỏi tiếp, ước +~1,8 s và rủi ro viết sai ⇒ tìm sai chắc chắn (dự án khác của User đã thử và bỏ). Có thể làm trượt sàn chữ đầu tiên 3 / 5 s.
- **Lượt nào cũng mang nguồn cũ (không nhận diện):** đơn giản nhất; câu đổi chủ đề luôn bị kéo bởi nguồn cũ ⇒ rủi ro thiếu ý / lạc đề cao hơn.
- *Tự kiểm:* "Nếu tôi hỏi 'Ăn gì ngon ở gần đây?' sau một câu về một lăng, luật chữ có coi đó là câu hỏi tiếp không, và nếu có thì hại gì?"

**Q3 — Sàn và bộ đo (D7).** Đề xuất của C ở §6 (C2 ≤ 2 / 208; C3 CI > 0 + tụt ≤ A/A + 3; C4 = 0; C5 = 0 đảo cảnh báo, P0_sai mới ≤ 2; C6 +100 ms; C9 tụt ≤ 1) + bộ ~40 cặp tự viết (agent viết, session
khác kiểm, **User đọc mẫu 10 cặp**), chia ~25 đã thấy / ~15 kín. Khác: (b) bộ lớn hơn (~80 cặp, tiền đo ~×2, "chưa rõ" ít hơn); (c) User tự viết một phần câu (giống câu thật hơn, tốn thời gian User).
- *Tự kiểm:* "Vì sao cần một phần cặp câu giữ kín tới cuối?"

**Q4 — Giao diện hiện lịch sử thế nào? (D8)**
- **Chỉ lượt mới + nhãn "Đang hỏi tiếp về: …" + nút "Cuộc trò chuyện mới" (C khuyên cho bản JS thuần):** sửa ít nhất; giao diện mới (sau Phase 8) làm khung hội thoại đầy đủ.
- **Khung hội thoại cuộn (các lượt xếp chồng):** giống chatbot thật hơn; sửa `app.js` / `index.html` nhiều hơn, id thẻ nguồn phải theo lượt (§4.6); có thể làm lại khi đổi giao diện.

**Để User tự nói lại** (`propose-options` §4c): vấn đề là câu hỏi tiếp thiếu chủ thể (chưa đo trên câu thật) → đã xem 4 hướng (PA0 / PA1 / PA2 / PA3), nghiêng PA1 vì không thêm lần gọi model, server không lưu, câu đủ ý không
đổi → làm M0 (bộ cặp) → M1 (lõi) → M2 (đo, chọn ghép câu khi tìm hay không) → M3 / M4; kiểm bằng T1 giống byte + sàn ngoài kho / cảnh báo → cần User chọn Q1–Q4.

**Không cần tra web** cho bản nháp này (không có khẳng định cần nguồn ngoài; số "+1,8 s / sót câu lược chủ thể" là của một dự án khác của User, private). Nếu A muốn mốc ngoài cho tỉ lệ câu hỏi tiếp trong
chatbot du lịch: câu cần tra (thông tin công khai) — "tỉ lệ câu hỏi nối tiếp / thiếu chủ thể trong hội thoại chatbot hỏi đáp du lịch, và cách nhận diện bằng luật so với viết lại câu bằng LLM (số đo công bố)".
