# Project Status

Last updated: `13:26 28/10/2026` (A, **kết phiên 28/10**: 8.2 đóng; đợt sửa kho đợt 1 đóng; phiên sau: đợt 2 ⇒ 8B ⇒ streaming). Trước: `09:40 28/10/2026` (A, **phiên 28/10**: User chọn PA3 — B0 không chặn (spec 8.2 §11); **merge B1 `510e1a8`: chatbot context 10 + NFC**, C71 review ready; B78 / C70 plan chờ review). Trước: `15:43 27/10/2026` (A, **phiên 27/10 chiều, kết phiên**: phần tồn Phase cũ — B1 rebase sẵn `c3d5607`; plan B3 duyệt `27e75be5ed44`; gold v3 mặc định; `dense_ms` làm tròn; đợt sửa kho soạn xong, spec duyệt `937cf8969810`; Qwen3-8B ⇒ thí nghiệm sau sửa kho; vòng cải tiến 8). Trước: `13:30 27/10/2026` (A, **kết phiên 27/10**: đợt cải tiến đóng; API ghi `chat_metrics` mỗi câu (merge `5100b90`); nhãn đoạn đúng v2 (merge `a819789`); bước tiếp B0)

Chỉ ghi hiện trạng (quy tắc: Governance v2 §6). Lịch sử và lý do các quyết
định cũ: `PROJECT_HISTORY.md`. Việc đang làm của từng session: `CURRENT_HANDOFF.md`.

## 1. Tổng quan

`hue_rag` là chatbot RAG về văn hóa và du lịch Huế, trả lời từ kho tri thức
curated `knowledge-base-hue/` (5 domain: `foods`, `heritages`, `festivals`,
`performing_arts`, `travel`). Ưu tiên code/data flow dễ hiểu, độ phức tạp tương
xứng nhu cầu và bằng chứng từ dữ liệu, Qdrant, model, API thật.

```text
curated Markdown (204 file, từ 28/10 sửa kho) -> chunker (8.426 chunk) -> e5-small dense + BM25 sparse
-> Qdrant -> query NFC -> retrieval dense_bm25_rrf (top-10 whole chunk vào context) -> gpt-6-luna -> API/UI có citation
```

Làm việc theo mô hình A/B/C (Governance v2, User duyệt 2026-10-24): A điều phối
và làm việc với User; B, C thực thi; review chéo; cả ba Claude Opus 5.5.

### Mục tiêu sản phẩm (thước "đo theo mục tiêu cuối" — `Session_Prompt.md` §7)

**Đã chốt (từ quyết định cũ):** trả lời **closed-world** từ kho, có citation `[n]` tới nguồn; câu ngoài kho ⇒ từ chối đúng câu chuẩn
(sàn: 0 câu ngoài kho bị trả lời); không bịa; người dùng gõ **có dấu** (câu không dấu ngoài phạm vi, User 25/10); câu đánh giá phải là câu
**người dùng thật hỏi** — số chính bỏ câu không tự nhiên (User 24/10 21:40). Thứ tự: chất lượng cần thiết trước, rồi tốc độ / tiền (User 26/10).
Đang chạy trên máy User (CPU), có thể deploy AWS sau (chưa chắc).

**User trả lời (08:47 27/10/2026):** đây là **đồ án tốt nghiệp** đem đi trình bày, xem như **sản phẩm kinh doanh thật**; người dùng = User, **du khách,
người dân**. Lỗi tệ nhất: User hỏi ý A (A đề xuất thứ tự, chờ User chốt). Yêu cầu phi chức năng (chờ tối đa, tiền / câu, chạy ở đâu): User chưa
rõ ⇒ **so sánh, đánh giá, nhận xét; chỗ nào tối ưu được thì tối ưu** — A tạm theo dõi p95 ≤ 5 s, mỗi biến thể báo USD / câu + latency p50 / p95. **User chốt 28/10:** p50 ≤ 3 s, p95 ≤ 5 s cả câu; ≤ 0,0005 USD / câu; thứ tự lỗi: sai cảnh báo an toàn > nói chắc sai > ngoài kho > thiếu ý > từ chối nhầm (§5).
Thước tạm giữ: Completeness / Accuracy (judge Claude) trên câu tự nhiên + năng lực, sàn closed-world ở trên; B0 (người đọc cặp mù) là mốc người đầu tiên.

## 2. Phase hiện tại

**Bây giờ (kết phiên 28/10, 13:26):** Phase 8.2 **đóng**; **đợt sửa kho đợt 1 đóng** (User; giữ sao lưu): 204 file / 8.426 đoạn, "trước ↔ sau" không làm hỏng.
Phiên sau (thứ tự): **áp đợt 2 sửa kho** (soạn sẵn `dot2.jsonl` `9b5105b35e8b`, 104 edit / 33 file) ⇒ **thí nghiệm Qwen3-8B** (plan `52555da95828`; chạy cần User duyệt gửi kho ra
OpenRouter + collection thử) ⇒ **spec streaming** (chờ kết quả ChatGPT; đo: chữ hiện sớm hơn ~1,9 s) ⇒ hội thoại nhiều lượt. Thước "lỗi nặng" (bịa thêm / sai điều kiện an toàn) đã
có (`report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_*`). Chi tiết: `CURRENT_HANDOFF.md`. Đoạn dưới là lịch sử 8.1 + rà code (đã xong), rồi 8.2.

**Phase 8.1 — rà quyết định Phase 0–7 bằng thí nghiệm: User-closed 15:27 25/10/2026** (spec
`docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` bản 4 + sửa đổi 25/10; đợt
`report_agent/2026-10-24_phase_8_1_ra_soat/` — `TONG_HOP.md`, kết luận `phase_8_1_g5_synthesis.md`, bảng
`phase_8_1_g5_decision_table_draft.md`, theo loại câu `phase_8_1_g5_by_category.md`). **Chatbot không đổi.**

- **Chỉ context 10 thắng** (Completeness dev +0,26 [+0,08; +0,48], test +0,27 [+0,02; +0,59]; lợi ở câu nhiều nguồn / so
  sánh). Giữ: chunker (12 biến thể), cách trộn + pool 30, BM25 âm tiết (k1 1,5 / b 0,75), không rerank, prompt, reasoning
  mặc định, validator. Tín hiệu: pool rộng, rerank luna (MRR +0,17), H8 (phạm sàn), NFC.
- Thước đo: so theo cặp + Holm; 120 dev / 56 test (`split.json`); đoạn đúng 55 câu; độ tự nhiên 82 / 65 / 29; Golden sửa
  10 đáp án (md5 `0f7dbf41b422`); **câu kín 36 câu khóa** (`knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl`,
  mở ở mốc cuối 8.2 do User quyết); **G0.6 manifest** `data/phase_8_1/baseline/g0_6_manifest.json` (`9ea480d0d083`).
- Giới hạn: bộ thử nhỏ; judge Claude, **chưa có mốc người**; câu không dấu **ngoài phạm vi** (User 25/10). User 15:44 25/10: sẽ đọc và nhận xét, **không chấm điểm** tay.
- Tiền 8.1: 0,1653 USD.

Đã xong (25–26/10): **sửa code sau rà soát Phase 0–7** (User duyệt 5 gói 19:4x 25/10; `bao_cao_he_thong/DE_XUAT_SUA_CODE.md`; đợt
`report_agent/2026-10-25_ra_soat_code/` — `TONG_HOP.md`). Đã vào `main` + cổng ổn định: **1a** `9e6d371` (validator nhận `[Nguồn n]`),
**4** `1b9c126` (guide / notebook), **3** `47a4e32` (công cụ so cặp, một chỗ dựng tin nhắn), **1b** `1e4acd0` (import trần, mọi lệnh từ
`backend/`, API 409 / 503 đúng), **đợt 3** = gói 2 + 5 + B-12 (merge `421c302` 26/10: đoạn vượt token luôn dừng build; test identity so nội dung +
sparse bytes; gỡ Rep B, smoke Phase 5, nhánh `minilm`, converter; nội dung kho ra khỏi file tracked; code backend 8.345 → 6.218 dòng; B review
ready; 8 file `reports/artifacts/` chứa nguyên văn kho ⇒ `data/reports_artifacts_private_2026-10-26/`, User 26/10). **Sửa code: xong 5 gói.** **Phase 8.2 chạy lại tối 26/10** (spec
`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`: bản gốc `dabae90b2b60` + **§10 "Sửa đổi 26/10"**, bản A duyệt `cd910c4c4169`).
B1 (context 10 + NFC) rebase lên `main` mới ⇒ nhánh `p82-b1` `811d25d` (27/10 chiều rebase lại ⇒ `c3d5607`), T1 giống byte, review ready — **merge 28/10 `510e1a8`** (PA3, không chờ B0). **Bước 2 =
đợt cải tiến từng khâu** (User 21:1x: phạm vi B — khâu trả lời + khâu tìm, không ghi Qdrant; luật (a) / (i); A tự chọn trong luật): phân loại lỗi
(C36 / B42: 80 % điểm mất đi kèm thiếu bằng chứng; chỗ nghẽn là xếp hạng); **K1** pool 100 kém hơn (nhánh `p82-k1`); **R2** trả lời một phần kém hơn
(phạm sàn OOS, 0,0027 USD; gác; `p82-r2`); **R3** NOT RUN (6 câu); **R4** thước số (chỉ danh sách đọc lại, `2c7ecfd`); K2, E2 NOT RUN; **27/10:** K3, R1, K3b-n kém hơn;
**K3b-m** (luna chọn 10 / 30) tầng tìm tốt hơn (tạm) (22 → 31 / 40 theo nhãn v1; v2: 24 → 33) nhưng khâu trả lời kém hơn theo luật (5 câu tụt > 4; e2e p50 6,5 / p95 9,1 s khi gọi đồng thời 4, 3,8× tiền) ⇒ **User 27/10 chọn chốt đợt**
(đợt đóng). Tiền 8.2: ≈ 0,212 / 0,5 USD. Bước tiếp: xem dòng "Bây giờ" đầu mục này. Tổng hợp:
`report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.

## 3. Bảng Phase

| Phase | Status | Kết quả / ranh giới |
|---:|---|---|
| 0–1 | `approved` | MVP foundation, simplicity governance, backend foundation |
| 2 | `approved` | Foods chunking; full-corpus chunker/locator (205 file) |
| 3 | `approved` | Embedding/sparse preflight (lịch sử; module preflight đã xóa ở 7A2) |
| 4 | `approved` | Qdrant ingestion 4 collection legacy (xóa ở 7A2 Gate 3) |
| 5 | `approved` | Retrieval profiles/reranking |
| 6 | `approved` | Generation/API/UI trên `gpt-6-luna`, live 4/5; giới hạn F1 (đa nguồn), F2 (bảng giá ngoài top-30) |
| 7 | `approved` | Evaluation baseline Foods (lịch sử) |
| 7A | `approved` | Golden full-corpus 176 case + smoke 10 (private) |
| 7A2 | `approved` | User-closed 2026-10-24; giới hạn: index 8B hoãn sang Phase 8 |
| 7B | `approved` | User-closed 2026-10-24: evaluator + baseline 176 (Claude judge); giới hạn: chưa có mốc người |
| 8.1 | `approved` | User-closed 15:27 25/10: chỉ context 10 thắng (đề xuất 8.2); còn lại giữ; G0.6 khóa; không đổi chatbot (`report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`) |
| 8.2 | `approved` | **User-closed 10:23 28/10/2026**: context 10 + NFC vào chatbot (`510e1a8`); B3 câu kín (S36, 33 câu trong kho): Completeness +0,818 [+0,394; +1,333], Accuracy +0,697, 0 câu tụt; ngoài kho 0 / 3 bị trả lời; Bước 2 đợt cải tiến: không biến thể nào vào; B0 dời (spec §11, mốc người làm sau). ≈ 0,227 / 0,5 USD. `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` |
| 9 | `not_ready` | Agentic RAG / Hybrid Recommender — roadmap, chưa có scope |

## 4. Runtime và dữ liệu đang chạy

**Full-corpus runtime (API `backend/api/app.py`):**

- candidate `e5-small-384` (`intfloat/multilingual-e5-small`, local CPU, 384 chiều);
- collection `hue_full_corpus_7a2_e5_small_384`, 8.426 point (build lại 28/10, đợt sửa kho; build record `574b5d02088b`), payload 7 field
  (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`,
  `chunk_id`, `domain`), dense + sparse;
- build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`
  (schema `full_corpus_build:v3`) là nguồn sự thật duy nhất "index khớp corpus";
  runtime từ chối khởi động nếu hash file corpus khác record;
- sparse state chung `data/full_corpus_builds/full_corpus_sparse_state.json`
  (vocabulary 5.631; sparse state `1bae9e0f3c49`); mốc tìm T1 (158 câu) **`23c58c47635d`** từ 28/10 (trước `cefb2d1ad609`);
- query chuẩn hóa NFC trước khi tìm (`backend/retrieval/full_corpus.py` `normalize_query`, từ 28/10 `510e1a8`);
- retrieval `dense_bm25_rrf`, reranker `none`, context tối đa **10** whole chunk (`settings.yaml` `max_context_documents: 10`, từ 28/10 `510e1a8`; trước 5);
  chọn bằng judge Claude 8.1, **chưa có mốc người** (B0 dời, spec 8.2 §11);
- **log số đo** (từ 27/10, `5100b90`; `dense_ms` làm tròn 1 chữ số từ `dfbcca5`): mỗi lần gọi `/api/chat` ghi một dòng `chat_metrics` (logger `chat`, `backend/logs/application.log`, gitignore):
  outcome, mã HTTP, từ chối, model, token vào / ra / suy luận, số nguồn, ms tìm / dense / ngữ cảnh / sinh / citation / tổng — không ghi nội dung, không ghi USD;
  latency thật 27/10 (B65, context 5): p50 3,3 s / p95 5,7 s tuần tự; context 10 (bộ "trước" B78, 176 câu, đo trong harness — chưa tính HTTP): p50 2,2 s / p95 4,9 s; lượt "sau" p95 9,8 s **không đại diện** (phía mạng / provider);
- generation `gpt-6-luna` (OpenAI); config `backend/config/settings.yaml`
  (`full_corpus_runtime`, `full_corpus_generation`).

**Candidate dense trong code** (`backend/embedding/full_corpus.py`):
`e5-small-384` (local) và `qwen3-embedding-8b-4096` (OpenRouter
`qwen/qwen3-embedding-8b`, pin Nebius, `data_collection: deny`, batch 64) —
8B chưa có index.

**Qdrant** `127.0.0.1:6335` (gRPC 6336; port đổi để chạy song song
một dự án khác của User). Còn đúng **1 collection** `hue_full_corpus_7a2_e5_small_384` (8.426
point). Hai collection Foods đã xóa ở B9 (24/10, User chạy); code/test/notebook Foods cũ đã gỡ
(`1832201`).

**Corpus:** 204 file → 8.426 chunk (28/10: đợt sửa kho 123 sửa / 65 file, loại file danh mục `performing_arts`; chunker giữ nguyên từ Phase 2: chia theo cấu
trúc Markdown, không overlap có chủ đích (thực tế 3 cặp chunk lặp body: blockquote lồng trong list
item, `markdown_blocks.py:233-250`, B8 2026-10-24), mỗi chunk vừa cả 3 tokenizer e5-small 512 / e5-base
512 / huydang 256; trung vị 85 token e5). `knowledge-base-hue/` không có Git
(`.gitignore`); backup Gate 1 đã xóa khi đóng Phase 7A2.

**Golden:** `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (176 case),
`golden_full_corpus_smoke.jsonl` (10, deep-equal); schema 4 field `question`,
`keywords`, `reference_answer`, `category`; private. Foods Golden V3 (45 + 10)
là lịch sử.

## 5. Quyết định đang hiệu lực

| Ngày | Quyết định | Nguồn |
|---|---|---|
| 2026-10-28 13:26 | **Kết phiên 28/10:** User **đóng đợt sửa kho đợt 1, giữ sao lưu**; **đợt 2 áp phần sẵn sàng ở phiên sau** (việc đầu tiên); **Qwen3-8B chạy phiên sau**; cho thử W30 (hook cảnh báo giờ ước), W31 (đang đo latency ⇒ cấm việc nặng song song), I6 | User |
| 2026-10-28 10:23 | **User đóng Phase 8.2** (TONG_HOP; giới hạn chưa có mốc người, tốc độ chưa đạt) | User |
| 2026-10-28 09:59 | **Yêu cầu phi chức năng chốt** (nghiên cứu ChatGPT 28/10, A kiểm 7 nguồn): cả câu (chưa stream) **p50 ≤ 3 s, p95 ≤ 5 s** (p99 ≤ 10 s theo dõi), USD / câu TB **≤ 0,0005**; có streaming ⇒ đề xuất đổi thước sang "chữ đầu tiên". **Thứ tự lỗi** thêm mức trên cùng: **sai cảnh báo an toàn / điều kiện vào khu vực** > nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm. **B3 chạy ngay** (mở câu kín cho người chạy B) | User |
| 2026-10-28 09:2x | **PA3: B0 không chặn B1 / đóng 8.2** (spec 8.2 §11, `5255f3274707`): merge B1 (context 10 + NFC) theo judge Claude, B0 làm sau (trước bảo vệ), luật dừng kích hoạt ⇒ A trình giữ 10 / về 5. **Thứ tự lỗi đồng ý:** nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm. Quyền phiên 28/10: ≤ 1 USD, A tự điều phối, B / C push nhánh riêng | User |
| 2026-10-27 15:3x | **Spec đợt sửa kho DUYỆT** sha `937cf8969810` (C68 3 vòng ready; chạy sau đóng 8.2; trần 0,15 USD). Vòng cải tiến 8: W27–W29 cho thử. User nhắc lại: "cứ thoải mái thử nghiệm, so sánh, đánh giá, nhận xét, ghi lại báo cáo, rồi chọn phương án phù hợp với dự án" (giữ nguyên tắc 24/10 20:49; quyền / tiền / dữ liệu vẫn theo luật) | User |
| 2026-10-27 15:0x–15:2x | **Đợt sửa kho** (sau đóng 8.2): Q1 41 mục + tên đơn vị sót + loại file danh mục `performing_arts` + 16 câu User; Q2 tra ngoài qua ChatGPT chỉ câu ngắn; Q3 build lại tại chỗ; Q4 **Qwen3-8B = thí nghiệm sau sửa kho** (chưa từng đo); Q5 quét + sửa Golden lệch kho trước khi đo lại | User; spec sửa kho §4 |
| 2026-10-27 15:01 | **Gold v3** (v2 + 2 câu test sửa nhãn, C64 / B74 / B75 / C) là nhãn mặc định (`fa192f8`); v2, v1 giữ — **thay bởi gold v4 từ 28/10** (`e08a126`, User duyệt 2 trích dẫn) | User |
| 2026-10-27 14:15 | "Xong phần tồn càng sớm càng tốt, xong phần tồn mới yên tâm đi tiếp các phase tiếp theo" | User |
| 2026-10-27 13:46–14:04 | Quyền phiên như 27/10 sáng; PA3 (chuẩn bị B1 + dọn nợ + **bàn** tính năng mới trước khi đóng 8.2, lệch WORKFLOW §9.4); tính năng ưu tiên: streaming, hội thoại nhiều lượt; gợi ý / lịch trình ⇒ Phase 9; deploy khi ổn định; bảo vệ ~tháng 1/2027 | User |
| 2026-10-27 13:05 | User duyệt: `/api/chat` ghi `chat_metrics` mỗi câu (merge `5100b90`); nhãn đoạn đúng v2 + đếm dòng tiêu đề (merge `a819789`, `gold_draft` giữ); W24–W26 | User; `TONG_HOP.md` §7 |
| 2026-10-27 11:0x | **Chốt đợt cải tiến từng khâu** (User chọn (1)): chatbot không đổi; K3b-m gác làm hồ sơ; bước tiếp B0 ⇒ B1 ⇒ đóng 8.2 ⇒ tính năng mới | User; `TONG_HOP.md` |
| 2026-10-27 10:2x | Lượt answer K3b-m: câu 120 về "theo dõi" (sàn A đặt trên tiền đề nhãn chưa kiểm), chạy lại từ đầu, không sửa nhãn lúc đó | User |
| 2026-10-27 08:47 | **Mục tiêu sản phẩm:** đồ án tốt nghiệp, xem như sản phẩm kinh doanh thật; người dùng = User, du khách, người dân; yêu cầu phi chức năng chưa có số ⇒ so sánh, tối ưu chỗ được. Q2 spec §10.6: test = "không làm hỏng" | User |
| 2026-10-26 21:31 | **Nguyên tắc: "ưu tiên đạt chất lượng cần thiết trước, sau đó mới tối ưu hiệu suất"** — biến thể nâng chất lượng chạy / chọn trước biến thể tối ưu tiền / tốc độ | User; spec 8.2 §10.3 |
| 2026-10-26 21:1x–21:31 | **Đợt cải tiến = spec 8.2 §10** (phạm vi B: khâu trả lời + thí nghiệm khâu tìm, không ghi Qdrant). Luật nhận: (a) chất lượng giữ (Completeness TB ≥ −0,1, câu tụt ≤ A/A + 3) + rẻ / nhanh hơn rõ; (i) chất lượng tăng vượt nhiễu + latency ≤ +50 ms + không thêm lần gọi API, USD / câu ≤ +20 %; tốn hơn ⇒ trình User. A tự đề xuất / thử / chọn trong luật. Hook quét cả câu kín | User; spec 8.2 §10 |
| 2026-10-25 19:4x | **Sửa code theo rà soát: đồng ý 5 gói** (`bao_cao_he_thong/DE_XUAT_SUA_CODE.md`); gỡ code không dùng nếu không ảnh hưởng hệ thống; guide 0–4 thêm dòng lịch sử; nội dung kho + đường dẫn dự án khác ra khỏi file tracked từ giờ, không xóa lịch sử git. Sửa trên `main`; B1 chờ B0 như spec 8.2 | User; `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md` |
| 2026-10-25 16:5x | **Dừng 8.2, rà code Phase 0–7 trước** khi đi tiếp (User hỏi về code: file / folder / guide, không phải dữ liệu kho). B1 cất nhánh `p82-b1` | User; `report_agent/2026-10-25_ra_soat_code/` |
| 2026-10-25 16:21 | **Spec 8.2 approved** (sha `dabae90b2b60`): hai bước không build lại index; mốc người đọc cặp mù; E1 → E2 → E3a / E3b; A tự đưa vào chatbot khi qua luật + review (E1, E3b chờ User); trần 0,5 USD | User; spec 8.2 |
| 2026-10-25 15:27 | **User đóng Phase 8.1**; G0.6 khóa 15:22 (câu kín 36 × 4, manifest `9ea480d0d083`) | User; `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md` |
| 2026-10-25 15:15 | **Câu hỏi không dấu: ngoài phạm vi** — thiết kế giả định người dùng gõ có dấu; bỏ nghiên cứu ChatGPT về không dấu (prompt B21 không gửi). Mẫu câu kín bản 5: User duyệt | User |
| 2026-10-25 (chiều) | Thư viện nhỏ, phổ biến cần cho việc đã duyệt: A tự duyệt, báo User sau ("mấy việc đơn giản này thì bạn tự thêm"); thêm `sentencepiece` để nạp M2 | User; `Session_Prompt.md` §4 |
| 2026-10-25 (chiều) | Câu kín 8.1: **thêm dấu cho mọi câu** (thay "không dấu" của spec G0.4); 9 câu độ tự nhiên bất đồng: giữ cả 9 (natural) | User 11:33, 11:40 |
| 2026-10-25 (chiều) | 8.1 G4: duyệt G4-A (xếp lại top-10) **và G4-B** (rerank pool 100 → top-10; sửa spec §5 G4). GPU yếu ⇒ mỗi lượt GPU chỉ 20–30 câu, kiểm model thật trên GPU trước khi chạy (không chạy nhầm CPU) | User; spec 8.1 §5 G4 "Sửa đổi 25/10" |
| 2026-10-25 | Cải tiến cách làm (không đổi chatbot): vòng tự cải tiến có người duyệt (`improve-workflow` + `SO_CAI_TIEN_CACH_LAM.md`); `run-experiment` có sàn / mức tụt / chỉ số quyết, cỡ mẫu trước, nhiễu A/A, kiểm người chấm; Session D học cùng User; `AGENTS.md` bản chính cho mọi agent; hook git chặn commit dữ liệu private. **Cách làm phải dùng được gần như nhau cho Codex/AGY**: luật ở Markdown trong repo + rào ở tầng git, không chỉ ở memory / settings của Claude | User; `report_agent/2026-10-25_cai_tien_cach_lam/` |
| 2026-10-24 | User ủy quyền A: tự điều phối B/C, tự kiểm tra, đề xuất, thử nghiệm, tối ưu và phát triển các Phase trước; commit/push theo mốc; ghi report; hệ thống phải chạy ổn định; dùng skill khi code | User (trước khi nghỉ) |
| 2026-10-24 | Giá `gpt-6-luna`: 0,1 USD/1M input, 0,5 USD/1M output. Ngân sách session ≤1 USD (tối đa 1,5 USD), không cần dùng hết | User |
| 2026-10-24 | Phase 7B: judge chính là Claude (session Claude Code), `gpt-6-luna` chỉ sinh + judge phụ; User chấm ~20 case; đo nhiễu (thay judge `gpt-6-luna` cũ) | `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` |
| 2026-10-24 | Mô hình A/B/C, review chéo, quy trình theo rủi ro, một tài liệu thiết kế/Phase, STATUS riêng mỗi session; duyệt cho A = duyệt cho B/C | `docs/superpowers/specs/2026-10-24-governance-v2-design.md` |
| 2026-10-24 | Index 8B hoãn sang Phase 8; khi build lại thiết kế cách gọi chịu 504/429 (batch, thử lại) | `reports/phase_7a2_gate_2_review_2026_10_24.md` §6 |
| 2026-10-24 | OpenRouter 8B pin Nebius (`order:[nebius]`, `allow_fallbacks:false`) | spec 7A2 §5.2 |
| 2026-10-24 | Giữ 2 collection Foods qua Phase 7; sau Phase 7 A đề xuất xóa mọi collection không dùng (kèm gỡ code/test/notebook Foods cũ) | User |
| 2026-10-24 | Cách làm việc học từ MekongAI: báo cáo cho User chỉ ở `bao_cao_he_thong/` (README mục lục, `LUONG_HOAT_DONG_HE_THONG`, `BAO_CAO_<khâu>` sống + thang 5 mức, `nhat_ky/`); report agent theo đợt `report_agent/<YYYY-MM-DD>_<chủ_đề>/` + `TONG_HOP.md`; giờ bằng `date`; stage từng file + `git diff --cached --stat`; A thử trong worktree; quyền đặc biệt hết hạn cuối phiên | `WORKFLOW.md` §6, §8, §9; `report_agent/2026-10-24_to_chuc_bao_cao/MO_TA_CACH_LAM_VIEC_MEKONGAI.md` |
| 2026-10-24 | Chunker giữ nguyên tới khi có baseline 7B | User |
| 2026-10-24 | Code/test/script luôn chạy bằng `uv` trong `.venv` của dự án | `Session_Prompt.md` §10 |
| 2026-10-24 | Kênh liên lạc: Claude Code ↔ Claude Code `trực tiếp` (SendMessage); có Codex/AGY thì `qua User` (khối "Tin cho <X>") | `WORKFLOW.md` §7 |
| 2026-09 (giữ) | Phase tuần tự `7A2 → 7B → 8 → 9`; trước Phase mới: Phase trước review + User đóng, cập nhật guide bằng bằng chứng, rồi một tài liệu thiết kế User duyệt | `WORKFLOW.md` §9.4 |
| 2026-10-24 (tối) | Phase 8 tách **8.1** (Claude rà mọi quyết định Phase 0–7 do AGY/Codex làm; thí nghiệm, phương án cũ làm baseline; không đổi chatbot) → **8.2** (cải tiến). 8.1 rà toàn bộ gồm Golden/evaluator; model/thư viện mới liệt kê trong spec để User duyệt từng cái; paid nhỏ trong trần 1 USD/phiên; index 8B để 8.2. Bộ chấm: chia 176 thành 120 thử / 56 kiểm, thêm 30–40 câu mới kiểu người dùng thật giữ kín tới cuối 8.2 | User |
| 2026-10-24 (tối) | Đoạn đúng cho câu khó: agent gắn, agent khác kiểm chéo, User duyệt ~10 câu; điểm câu trả lời chưa có mốc người | User |
| 2026-10-24 (tối) | **Giữ `gpt-6-luna`**, không so model sinh ở Phase 8; tối ưu sang model nhỏ để sau khi hệ thống ổn. **Thay** amendment `2026-10-01-phase-6-openai-baseline-amendment.md` §5 và amendment 10-23 R6 ("Qwen là benchmark bắt buộc ở Phase 8") | User |
| 2026-10-24 (tối) | Dense ở Phase 8 chỉ e5-small + Qwen3-Embedding-8B (giữ spec 7A2 §2; 8B ở 8.2). Rerank thử trên GPU GTX 1650 4 GB fp32 trong `.venv` (torch cu130 sẵn có); chatbot hiện chạy máy User, có thể deploy AWS sau (chưa chắc) ⇒ đo cả latency CPU | User |
| 2026-10-24 21:58 | Số chính 8.1 = **bỏ câu không tự nhiên** (tự nhiên + đo năng lực; 2 agent gắn độc lập, kappa 0,765, 29 câu loại, 9 câu bất đồng chờ User); "chỉ tự nhiên" là số phụ. Nhãn: `data/phase_8_1/golden_realism_final.jsonl` (private) | User |
| 2026-10-24 21:40 | Câu hỏi đánh giá phải **tự nhiên** (người dùng thật hỏi). Golden giữ nguyên nhưng gắn nhãn natural / capability_only / unnatural; số chính = phần natural; câu kín không tự nhiên thì thay. Skill tự cải thiện + ý từ khóa AI FDE tạm gác tới khi User gửi báo cáo | User |
| 2026-10-24 20:49 | **Nguyên tắc thường trực:** được thực nghiệm, so sánh, thử — không chỉ Phase 8.1, cả khi quay lại các Phase trước; luôn thử + đánh giá + so với baseline trước khi chọn, không chọn một giải pháp rồi làm luôn. Vẫn theo quyền/tiền/ranh giới dữ liệu hiện hành | User |
| 2026-10-24 20:49 | **Spec 8.1 approved** (`docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` bản 4) + M1 `bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker` | User |
| 2026-10-24 (tối) | 8.1 G4 thêm rerank listwise bằng `gpt-6-luna` (kiểu `rag_old_0`) so cùng rerank GPU; chi tiết dự án khác của User giữ private (`data/phase_8_1/external_lessons_private.md`), không đưa lên repo công khai | User |
| 2026-10-24 (tối) | B9 đóng; thư viện không dùng giữ nguyên, chỉ gỡ khi xung đột; nghiên cứu ngoài qua ChatGPT trước với prompt deep research đầy đủ | User |
| 2026-10-24 | Phase 8 = đợt ổn định: chunk size/gộp chunk vụn, reranker đa ngôn ngữ, truy xuất bảng giá (F2), tổng hợp đa nguồn (F1), BM25 tiếng Việt (tách từ/bigram), rà lại lựa chọn các Phase trước | User |
| 2026-10-23 | Dense full-corpus chỉ e5-small + qwen3-embedding-8b; build thẳng metadata v2; build record là nguồn sự thật; runtime mặc định e5-small, cutover 8B chờ bằng chứng 7B/8 | spec 7A2 §2 |
| 2026-10-23 | Mọi model OpenAI (generation, evaluation answer/judge) là `gpt-6-luna` | `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md` |
| 2026-10-23 | Golden 176 + smoke 10; retrieval K=10; 3 metric answer thang 1–5; macro-average theo case; lỗi kỹ thuật làm run incomplete; chưa đặt ngưỡng trước baseline | `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` |
| 2026-09-29 | Payload metadata v2 đúng 7 field; `domain` = thành phần đầu của path; không payload index/filter | `docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md` |
| 2026-09-11 | Full-corpus umbrella: chia theo cấu trúc, evidence slice từ source, citation đọc `evidence_parts`, context whole-chunk top-5 | `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` |
| 2026-09-08 | Taxonomy `knowledge-base-hue/travel/{places,services,tickets}`; inventory bị loại khỏi discovery | `PROJECT_HISTORY.md` |
| — | User ưu tiên mặc định đơn giản, nhưng mặc định phải được kiểm bằng bằng chứng thật | User |

## 6. Ranh giới an toàn

- Qdrant: chỉ đọc, trừ đích chính xác được ghi trong việc của session.
- `knowledge-base-hue/`, `data/`, Qdrant storage, Golden, trace chi tiết và
  `gửi chatgpt/` là private: không commit, không chép nội dung vào report tracked.
- Sửa corpus: backup vào `knowledge-base-hue/meta/` trước, review bằng diff.
- Data egress: chỉ gửi chunk/query tới OpenRouter cho `qwen/qwen3-embedding-8b`
  trong việc đã duyệt; mọi request `data_collection: deny`.
- Không đọc/in/log `.env` hay secret; dùng `uv run --env-file .env`.
- Provider/model/dataset mới, paid run ngoài giới hạn đã ghi, deploy, xóa dữ
  liệu: cần User duyệt qua A.
- Git: A được commit/push (User 2026-10-24); B/C không commit trừ khi việc ghi rõ.

## 7. Bản đồ tài liệu đang dùng

```text
AGENTS.md                              lối vào cho mọi agent (CLAUDE.md chỉ nhập file này)
session_prompt/START_SESSION.md        mở mọi session
session_prompt/Session_Prompt.md       luật chung
session_prompt/WORKFLOW.md             cách làm, việc thêm của A
session_prompt/CURRENT_HANDOFF.md      việc đang mở của A/B/C
session_prompt/sessions/STATUS_*.md    ngữ cảnh riêng từng session
session_prompt/PROJECT_HISTORY.md      lịch sử (reference-only)
session_prompt/TEMPLATE_*.md           mẫu report
session_prompt/SO_CAI_TIEN_CACH_LAM.md sổ cải tiến cách làm (skill improve-workflow)
skills/{practical-project-coding,risk-gated-agent-review,propose-options,run-experiment,improve-workflow}/SKILL.md
.githooks/pre-commit, .claude/settings.json   rào bằng máy (hook git mọi agent; Claude Code cấm đọc .env)
scripts/grep_kb.sh                     tìm trong nội dung kho, luôn loại evaluation/ meta/ *sealed* (W27)
guides/full_corpus_rag.md              guide umbrella full-corpus
docs/superpowers/specs/, docs/superpowers/plans/   thiết kế từng Phase
report_agent/<YYYY-MM-DD>_<chủ_đề>/   report + review từ 2026-10-24 (README trong report_agent/)
bao_cao_he_thong/                      báo cáo cho User: luồng hệ thống, BAO_CAO_<khâu>, nhat_ky/
reports/                               report cũ tới 2026-10-24 — lịch sử, chỉ đọc
gửi chatgpt/<YYYY-MM-DD>/              yêu cầu + kết quả nghiên cứu ChatGPT (private)
handoff_prompt/README.md               contract lịch sử (reference-only)
```

## 8. Bẫy kỹ thuật đã biết

- Chunker và e5 cần tokenizer trong HF cache; chạy với `HF_HUB_OFFLINE=1`. Cảnh
  báo "Token indices sequence length…" là bình thường.
- Sửa corpus làm runtime từ chối khởi động (freshness) cho tới khi build lại index.
- `full_corpus_sparse_state.json` chỉ ghi một lần: corpus đổi thì phải xóa file cũ
  trước khi build lại, nếu không build raise. Từ 26/10 (C-21) build chỉ ghi sparse state **sau** khi kiểm đích — đích hỏng không để lại file mồ côi.
  Quy trình: `guides/full_corpus_rag.md` mục "Build lại index".
- **Mọi lệnh chạy từ `backend/`, import trần** (`core.…`, `retrieval.…`; không `backend.…`) từ `1e4acd0` (rà code 1b, 25/10): API, pytest,
  build (`python -m ingestion.full_corpus_pipeline build …`), evaluator, harness. Lệnh cũ từ gốc repo báo `ModuleNotFoundError: core`.
  Đặt tên module mới không trùng gói đã cài (`find_spec`). API: index lệch ⇒ 409; Qdrant / model không nạp ⇒ 503.
- Pytest chạy từ `backend/`: `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/<file> -q` (không nạp key). Chỉ thêm
  `--env-file ../.env` khi việc ghi rõ cần test có key OpenAI: `test_api_chat.py`, `test_openai_full_corpus_generator.py`,
  `test_phase6_live_smoke.py` (rà code 25/10, C-17 / C-18: không có key thì 3 test miễn phí cũng fail vì `require_openai_key`).
  Thêm: `test_phase6_settings.py::test_openai_api_key_exists_without_leaking` cũng đòi key (fail khi không key — B63 27/10, giống trên `main`).
- Pytest lấy **gốc repo** làm rootdir: node id là `backend/tests/<file>::<test>`; `--deselect tests/…` không khớp và không bỏ được test (B1 2026-10-24: lỡ chạy 1 paid call trả 400 + một collection tạm tự xóa). Bỏ test ghi/paid bằng cách liệt kê file cần chạy, không dựa vào `--deselect`. Danh sách test ghi Qdrant / paid cũ (4 file) đã gỡ ở B9; hiện không test nào ghi Qdrant (rà code 25/10, B25 / C34).
- `test_phase6_live_smoke.py` còn mock/monkeypatch — rà ở Phase 8.1 (B8). Code/test Foods cũ đã gỡ ở B9
  (`1832201`). Mốc pytest sau đợt 3 (26/10, không key, 15 file trừ `test_startup_model_missing.py`): **197 passed / 1 failed / 4 error** — phần
  failed / error đúng là test cần `OPENAI_API_KEY` (C-17); `test_startup_model_missing.py` User chạy `!` (auto mode chặn `HF_HOME` rỗng): 1 passed.
- Test mẫu chunker đọc chuỗi kỳ vọng từ `knowledge-base-hue/meta/chunker_acceptance_samples.json` (private, B-12): clone không có kho ⇒ 7 test đó báo
  `FileNotFoundError` có tên file (đúng thiết kế).
- OpenRouter 8B: không pin thì trộn provider (vector lệch, cos ~0,996); pin Nebius
  thì 10–30 s/batch và đã gặp 504; DeepInfra từng trả 429.
- Notebook còn lại: 03, 04, 06 (02, 05, 07, 08a–c đã xóa ở B9); 03/04 Run All đạt trên bản tạm.
- Permission tự động của từng session có thể chặn `rm`/`pkill`: session đó dừng và
  nhờ User chạy bằng `!` trong terminal của nó; session khác không chạy hộ.
- Model "đã có trong HF cache" có thể chỉ là thư mục `refs` rỗng: kiểm `du -sh` / file `.safetensors` trước khi lập kế
  hoạch offline (8.1 G4: M1 / M2 phải tải 2,2 GB mỗi cái; M2 cần `sentencepiece`).
- Qdrant dense (HNSW) phụ thuộc `limit`: 30 đầu của `limit=100` ≠ `limit=30` ở 1/108 câu ⇒ tái lập runtime phải hỏi đúng
  `limit` như production. Sparse Qdrant tính float32 ⇒ phá hòa có thể khác float64 trong bộ nhớ (G4K).
- Model tự suy luận (luna listwise) ra ~270 token/câu, gấp ~3 ước ⇒ lượt có phí luôn pilot 10 câu, ước lại từ pilot.
- So điểm judge giữa biến thể: chấm baseline **cùng lượt mù** (nhiễu judge-only 2/88 câu).
- `gpt-6-luna` viết citation cả `[n]` lẫn `[Nguồn n]` (24 / 465 lần ở 8.1 G2; runtime nhận cả hai + đổi về `[n]` từ `9e6d371`, 25/10 — số
  "lỗi citation" trước commit này đếm theo định nghĩa cũ) ⇒ code xử lý / đếm / đánh số lại citation phải bắt
  cả hai dạng (25/10 B24: file đọc cặp mù lộ bên vì chỉ bắt `[n]`).
- Memory Claude dùng chung cho cả ba session (cùng thư mục dự án).
- **Worktree `/tmp/…` (26/10):** chạy Python trong worktree bằng `uv run --project /home/minhhieu/hue_rag …` (không thì `uv` tạo `.venv` lạ ở đó);
  symlink `data/`, `knowledge-base-hue/` hiện untracked ⇒ gỡ khi xong; worktree giữ nhánh `main` thì session khác không `git switch main` được ⇒
  gỡ (`git worktree remove`) trước khi người kia chuyển nhánh; `git push` từ worktree bị auto mode chặn ⇒ push từ working tree chung hoặc User `!`.
- `uv run --env-file ../.env …` chạy nền (`run_in_background`) có thể báo không thấy file ⇒ dùng **đường dẫn tuyệt đối** `--env-file /home/minhhieu/hue_rag/.env` (28/10, I6).
- `backend/logs/application.log` dùng chung cho **pytest và server** (`test_api_chat.py` cũng ghi `chat_metrics`) ⇒ đếm dòng `chat_metrics` mới: lấy mốc **ngay trước** khi gửi câu,
  không chạy pytest xen giữa; gỡ worktree xóa luôn log của nó ⇒ chép dòng cần giữ vào `data/` trước (27–28/10, I6).
- Auto mode chặn chạy notebook (`jupyter nbconvert --execute`) và test thiếu model (`HF_HOME` rỗng) ở một số session ⇒ User `!` ở terminal đó.
- Test khóa tập trường `chat_metrics` (`test_api_chat.py::test_real_first_chunk_budget_error_has_no_partial_answer`) dừng ở lỗi ngân sách context, **trước** generator ⇒
  trường mới thêm ở phần sinh / citation chỉ cổng ổn định (đọc dòng log thật) bắt được; test đi qua generator cần key (B70 m-1, đóng bằng ghi bẫy 27/10).
- `validate_gold.py` từ 27/10 (C62) dừng nếu `gold_draft.jsonl` đã có.
- `data/phase_8_1/tools/validate_gold.py` **không nhận đầu vào**: đọc `gold_batch_*` rồi **ghi đè** `data/phase_8_1/gold/gold_draft.jsonl` (file manifest G0.6
  khóa sha `bab707b9ab22`) ⇒ không chạy lại; kiểm nhãn v2 bằng `data/phase_8_1/tools/build_gold_v2.py` (chỉ đọc). Nhãn dùng cho đo: **`gold_v4.jsonl` từ 28/10** (`927bae1bf201`, kho sau sửa đợt 1; trước đó `gold_v3.jsonl` từ 27/10 chiều (`3b1117cf59e9`, B75; trước đó `gold_v2.jsonl` B69) — `GOLD_PATH`
  mặc định của `backend/experiments/phase_8_1/g1_retrieval.py`: v2 + luật tiêu đề mục từ 27/10 sáng, **v3 từ `fa192f8`**, **v4 từ `e08a126`**) ⇒ **mọi số `*_gold_*` trước 27/10 tính bằng v1**, ghi kèm bản nhãn; so với số cũ thì chạy lại
  mốc bằng cùng thước (B1 dev: v1 22 / v2 24).
- Auto mode chặn **cả khối** khi lệnh ghép có thao tác rủi ro (`push --delete`, `rm`, push nhánh từ worktree) ⇒ tách thao tác rủi ro ra lệnh
  riêng; commit report ngay ở working tree chung, push riêng (26/10 tối, A và C).
- Hook `.githooks/pre-commit` chỉ chạy khi `git config core.hooksPath` = `.githooks` (cấu hình cục bộ, không đi theo
  clone): bản clone mới phải bật một lần. Hook chặn dòng thêm mới có tên dự án khác, kể cả khi trích tên file tài liệu
  cũ — viết "tài liệu cách làm của dự án khác" thay vì tên file. Bỏ qua (`--no-verify`) chỉ khi User duyệt đúng commit đó.
  Từ 26/10 (W16) hook còn quét **dòng thêm mới** trùng ≥ 40 ký tự với Golden / kho (`.githooks/overlap_scan.py`, ~0,4 s; kho đọc từ working
  tree chính nên commit từ worktree `/tmp` không symlink vẫn quét; báo "quét LỖI" khi thiếu `uv`). Câu kín: từ 26/10 tối (User duyệt) quét `question` + `reference_answer` của `*sealed*.jsonl` (nhãn
  `sealed`; không quét `sources` và ghi chú `*sealed*.md` vì báo nhầm). `_source-dumps/` không quét.
