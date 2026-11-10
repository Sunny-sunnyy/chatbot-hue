# Project Status

Last updated: `22:34 09/11/2026` (A, kết phiên 09/11: định tuyến phương án B; công cụ ngày + âm lịch bật; T2 / T3 / T4 + G đóng hồ sơ; 4 chốt deploy; trần Phase 9 4,0). Trước: `12:25 08/11/2026`.

Chỉ ghi hiện trạng (quy tắc: Governance v2 §6). Lịch sử và lý do các quyết
định cũ: `PROJECT_HISTORY.md`. Việc đang làm của từng session: `CURRENT_HANDOFF.md`.

## 1. Tổng quan

`hue_rag` là chatbot RAG về văn hóa và du lịch Huế, trả lời từ kho tri thức
curated `knowledge-base-hue/` (5 domain: `foods`, `heritages`, `festivals`,
`performing_arts`, `travel`). Ưu tiên code/data flow dễ hiểu, độ phức tạp tương
xứng nhu cầu và bằng chứng từ dữ liệu, Qdrant, model, API thật.

```text
curated Markdown (204 file, sửa kho đợt 1 28/10 + đợt 2 30/10 + giờ mở cửa 05/11) -> chunker (8.435 chunk) -> e5-small dense + BM25 sparse
-> Qdrant -> query NFC -> retrieval dense_bm25_rrf (top-10 whole chunk vào context) -> gpt-6-luna -> API/UI có citation (stream SSE từ 01/11, `a80e12d`)
```

Làm việc theo mô hình A/B/C (Governance v2, User duyệt 2026-10-24): A điều phối
và làm việc với User; B, C (và E từ 05/11) thực thi; review chéo; mọi session Claude Opus 5.5.

### Mục tiêu sản phẩm (thước "đo theo mục tiêu cuối" — `Session_Prompt.md` §7)

**Đã chốt (từ quyết định cũ):** trả lời **closed-world** từ kho, có citation `[n]` tới nguồn; câu ngoài kho ⇒ từ chối đúng câu chuẩn
(sàn: 0 câu ngoài kho bị trả lời); không bịa; người dùng gõ **có dấu** (câu không dấu ngoài phạm vi, User 25/10); câu đánh giá phải là câu
**người dùng thật hỏi** — số chính bỏ câu không tự nhiên (User 24/10 21:40). Thứ tự: chất lượng cần thiết trước, rồi tốc độ / tiền (User 26/10).
Đang chạy trên máy User (CPU), có thể deploy AWS sau (chưa chắc).

**User trả lời (08:47 27/10/2026):** đây là **đồ án tốt nghiệp** đem đi trình bày, xem như **sản phẩm kinh doanh thật**; người dùng = User, **du khách,
người dân**. Lỗi tệ nhất: User hỏi ý A (A đề xuất thứ tự, chờ User chốt). Yêu cầu phi chức năng (chờ tối đa, tiền / câu, chạy ở đâu): User chưa
rõ ⇒ **so sánh, đánh giá, nhận xét; chỗ nào tối ưu được thì tối ưu** — A tạm theo dõi p95 ≤ 5 s, mỗi biến thể báo USD / câu + latency p50 / p95. **User chốt 28/10:** p50 ≤ 3 s, p95 ≤ 5 s cả câu (**31/10 D2:** khi streaming chạy, sàn này áp cho "tới chữ trả lời đầu tiên trên trình duyệt"; tới lúc đó vẫn áp cả câu); ≤ 0,0005 USD / câu; thứ tự lỗi: sai cảnh báo an toàn > nói chắc sai > ngoài kho > thiếu ý > từ chối nhầm (§5).
Thước tạm giữ: Completeness / Accuracy (judge Claude) trên câu tự nhiên + năng lực, sàn closed-world ở trên; B0 (người đọc cặp mù) là mốc người đầu tiên.

## 2. Phase hiện tại

**Bây giờ (22:34 09/11/2026, kết phiên 09/11):** `main` = như 08/11 + **định tuyến phương án B** (`3b52017`: 4 tuyến, tuyến khẩn cấp ⇒ trợ lý Huế, bỏ câu soạn sẵn) + **công cụ ngày + âm lịch BẬT** (`7eb1f12`) + **4 chốt deploy** theo biến môi trường (`ccc9f4f`). Đóng hồ sơ (đo âm): G cổng 2 nhóm, T2 tra web thành công cụ, T3 bảng vé + giờ, T4 lịch trình câu gõ. Tốc độ chung (S5 09/11): câu Huế chữ đầu p50 2,16 / p95 4,32 s, 0,00047 USD; xã giao p95 7,73 s ✗; câu ngày p50 5,19 s, 0,00063 USD ✗ (User: giữ bật, tối ưu sau). Phase 9 ≈ 3,6 / 4,0. Mốc đóng tính năng: User chưa chốt. **Dòng 08/11:** (12:25 08/11/2026, kết phiên 08/11): như dòng 07/11 dưới + 08/11: 7 ảnh cổng, **hỏi bằng ảnh bật**, bản đồ lịch trình (cờ tắt), 14 việc nhỏ giao diện / kiểm số web / `turn_id`; **spec bản 13** `5557f0fd7650` (cổng 2 nhóm, bỏ khẩn cấp, 4 công cụ) — G đạt bộ đã thấy (chờ kín + S5), T1 đạt (chờ review vòng 2 + S5), T3 trượt Q3 (chờ User); trần Phase 9 3,5 (đã dùng ≈ 3,0). Chưa deploy (User: sau khi đủ tính năng + đóng gói). Việc tiếp: `CURRENT_HANDOFF.md` "PHIÊN SAU ĐỌC TRƯỚC". **Dòng 07/11:** (15:44 07/11/2026, giữa phiên 07/11): `main` = RAG 1–8 + trợ lý Phase 9 (định tuyến 4 tuyến, tìm thêm ≤ 2, nhớ câu hỏi 3 lượt, câu dặn hẹp, 👍 / 👎, khẩn cấp PA1, #6 song song bật, tra web B6 bật) **+ giao diện cổng du lịch đợt 1** (bản mẫu Sông Hương; trang chủ, Khám phá 204 bài, Trợ lý Huế nổi mọi trang, Giới thiệu, dòng "Nguồn" thay số [n]; 4 API chỉ đọc) **+ thời tiết bật + biểu mẫu "Lên kế hoạch" bật** (code xếp bằng giá trị nút; lượt biểu mẫu = luật lịch trong lời dặn hệ thống + suy luận "low" — V5; S3 bộ quyết 24 / 24, chữ đầu p95 4,22 s trên `main`). Cờ tắt: lịch trình câu tự do, `hoi_lai`, ảnh. Chờ User: 7 ảnh (lấy lại từ vi.wikipedia, chỉ file Commons), lộ trình (deploy thử sớm — nhánh `p12-deploy-nhap` + nháp Docker chạy được cục bộ), giọng nói giữ / cắt, phiếu thời lượng v7. Tiền Phase 9 ≈ 2,02 / 2,5; Phase 10 ≈ 0,098 / 0,15. Việc tiếp: `CURRENT_HANDOFF.md` "PHIÊN SAU ĐỌC TRƯỚC".

Diễn biến các phiên trước: `session_prompt/archive/PROJECT_STATUS_LICH_SU_2026-11-05.md`, `PROJECT_HISTORY.md`.

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

Đã xong (25–26/10): **sửa code sau rà soát Phase 0–7** (User duyệt 5 gói 19:4x 25/10; `bao_cao_he_thong/94_DE_XUAT_SUA_CODE.md`; đợt
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
| 8 (đóng gói 1–8) | `approved` | **User-closed 14:29 01/11/2026**: streaming (`a80e12d`); lượt đo cuối mọi sàn đạt (`report_agent/2026-10-31_streaming_spec/do_cuoi_implementation.md`); báo cáo so sánh phương án; B0 mốc người tham khảo ⇒ giữ 10 đoạn. Giới hạn: judge Claude, B0 không chọn bên theo cặp + kho cũ; câu nhiều nguồn Đủ 3,50 ⇒ Phase 9; nhiều lượt ⇒ Phase 9; chữ đầu đo một lần (`report_agent/2026-10-31_streaming_spec/TONG_HOP.md`) |
| 9 | `in_progress` | **09/11:** định tuyến phương án B + công cụ ngày bật + 4 chốt deploy vào `main`; G / T2 / T3 / T4 đóng hồ sơ (tag `hoso/p9-*`); trần **4,0** (≈ 3,6). **08/11:** spec bản 13 `5557f0fd7650` duyệt (cổng 2 nhóm + T1–T4); hỏi bằng ảnh bật; bản đồ cờ tắt; 14 việc nhỏ; trần **3,5** (≈ 3,0). **07/11:** giao diện cổng đợt 1 + thời tiết + biểu mẫu "Lên kế hoạch" (V5) vào `main` và bật; lịch trình câu tự do + sửa lịch hoãn (tự soi đề xuất đóng tới sau bảo vệ — chờ User); B4b cờ tắt; còn ảnh cổng, B7 đóng gói. Spec Phase 9 **bản 13 `5557f0fd7650`** (User duyệt 11:01 08/11/2026: cổng 2 nhóm, bỏ khẩn cấp, 4 công cụ; trần 3,5); bản 12 `77250689e605`; spec cổng đợt 1 `ff3c317ec88b`. Trần **2,5** (đã dùng ≈ 2,02). |

## 4. Runtime và dữ liệu đang chạy

**Full-corpus runtime (API `backend/api/app.py`):**

- candidate `e5-small-384` (`intfloat/multilingual-e5-small`, local CPU, 384 chiều);
- collection `hue_full_corpus_7a2_e5_small_384`, 8.435 point (build lại 05/11 tối, đợt giờ mở cửa 11 file; build record `9921888f2030`; 30/10 `51fb1ec63cbc`; trước 28/10 `574b5d02088b`), payload 7 field
  (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`,
  `chunk_id`, `domain`), dense + sparse;
- build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`
  (schema `full_corpus_build:v3`) là nguồn sự thật duy nhất "index khớp corpus";
  runtime từ chối khởi động nếu hash file corpus khác record;
- sparse state chung `data/full_corpus_builds/full_corpus_sparse_state.json`
  (vocabulary 5.631; sparse state `4a8311a2dfef` từ 05/11 tối, 30/10 `c8134c49a648`, trước `1bae9e0f3c49`); mốc tìm T1 (158 câu) **`64656a87c109`** từ 05/11 tối (30/10 `4d5bbe9e0edc`, 28/10 `23c58c47635d`, trước nữa `cefb2d1ad609`);
- query chuẩn hóa NFC trước khi tìm (`backend/retrieval/full_corpus.py` `normalize_query`, từ 28/10 `510e1a8`);
- retrieval `dense_bm25_rrf`, reranker `none`, context tối đa **10** whole chunk (`settings.yaml` `max_context_documents: 10`, từ 28/10 `510e1a8`; trước 5);
  chọn bằng judge Claude 8.1; **B0 01/11** (mốc người tham khảo): User giữ 10 — 3 cặp bản 5 đoạn từ chối nhầm, còn lại như nhau;
- **log số đo** (từ 27/10, `5100b90`; `dense_ms` làm tròn 1 chữ số từ `dfbcca5`): mỗi lần gọi `/api/chat` ghi một dòng `chat_metrics` (logger `chat`, `backend/logs/application.log`, gitignore):
  outcome, mã HTTP, từ chối, model, token vào / ra / suy luận, số nguồn, ms tìm / dense / ngữ cảnh / sinh / citation / tổng — không ghi nội dung; **từ Phase 9 B0 (merge `1c10111`) thêm** `route`, `usd`, `n_llm_calls`, `llm_calls` (mỗi lần gọi: loại, ms, USD, token), `tools`;
  latency thật 27/10 (B65, context 5): p50 3,3 s / p95 5,7 s tuần tự; context 10 (bộ "trước" B78, 176 câu, đo trong harness — chưa tính HTTP): p50 2,2 s / p95 4,9 s; lượt "sau" p95 9,8 s **không đại diện** (phía mạng / provider);
- **streaming (01/11, merge `a80e12d`):** `POST /api/chat/stream` (SSE) + giao diện chữ hiện dần; `/api/chat` giữ; lõi chung `backend/llm/assistant.py` (tên cũ `grounded_answer.py` tới B0; có công cụ `tim_kho` + sổ nguồn từ Phase 9 B0, merge `1c10111`); tới chữ đầu trên trình duyệt p50 1,23 / p95 2,61 s (38 câu, S4); `cost_usd` giá đủ + log token đệm;
- **giao diện web (02/11, merge `ed8e6e8`):** React 19 + Vite 8 + Tailwind 4 (`frontend/src/`), FastAPI phục vụ bản build `frontend/dist/` (không commit — `cd frontend && npm ci && npm run build`); CSP giữ nguyên; 0 gói Radix / shadcn; `.npmrc` `ignore-scripts` + `before=2026-10-19`;
- **hỏi lại do code + thẻ nút (B4b `b019aab` → B5 `d66f6a3`, 05/11):** `ChatRequest.truong` (nút) + sự kiện SSE `clarify` + thẻ giao diện; phần công cụ `hoi_lai` cho model **đã gỡ** ở B5 (C183 m-2); B5 dùng thẻ khi `lich_trinh` thiếu số ngày (**code** quyết hỏi); API nhận `truong` cả khi cờ tắt (giao diện không gửi);
- **lịch trình (B5, merge `d66f6a3` 05/11) — cờ `lich_trinh: false`:** `backend/llm/lich_trinh.py` (xếp theo buổi từ bảng `data/phase_9/lich_trinh/diem_v3.json`, khung + kiểm khung + kiểm cuối D8 + khối ghi chú do code nối + link Google Maps), `do_so.py` (dò số ngày), `so_tien.py`; giao diện bước tiến độ chỉ từ sự kiện thật + nút Sửa; cờ tắt ⇒ chuỗi gửi model giống byte bản trước (228 / 228);
- **thời tiết B5b (merge `db77f32` 06/11 tối) — cờ `thoi_tiet: true` từ 07/11 (`0dab4e5`, User Q-U4):** `backend/llm/thoi_tiet.py` (Open-Meteo, cache 30 phút, số do code dựng, ngoài 7 ngày ⇒ câu cố định, bão / lũ ⇒ NCHMF + 112); **B171 (merge `dbb4004`)** sửa lịch trình: sáng ưu tiên điểm hợp sở thích, dòng "Buổi tối: để trống — <lý do>" + kiểm cuối bắt nói ngược, model từ chối ⇒ code dựng lời lịch tối thiểu từ khung (cờ `lich_trinh` vẫn tắt);
- **giao diện cổng du lịch đợt 1 (merge `dbfc925` 07/11) + biểu mẫu "Lên kế hoạch" (V5 `312ad9f`, cờ `lich_trinh_bieu_mau: true` `a884de4`):** điều hướng hash, 0 gói router, CSP không đổi; `backend/api/routes/cong.py` 4 API chỉ đọc (`/api/kham_pha` 204 bài theo build record, `/api/kham_pha/bai?id=` chỉ id nguyên văn trong `corpus.sources`, `/api/thoi_tiet`, `/api/tinh_nang`); `SourceResponse.bai_id`; `ChatRequest.bieu_mau` ⇒ không định tuyến, code gọi `lich_trinh` với giá trị nút, `generator.bieu_mau_agent` (lời dặn trả lời + `LICH_TRINH_LUAT`, suy luận "low"), không công cụ; `_lay_nguon_lich` chọn đoạn cùng file có bằng chứng dài nhất (`0cb0b0a`); bundle 106 KB gzip;
- **trả lời song song định tuyến (#6, merge `92705ce`, BẬT `5a8aa5e` 05/11):** `song_song_tra_loi: true` — đường stream chạy phần `tro_ly_hue` cùng lúc định tuyến; tuyến khác ⇒ bỏ phần đã chạy; chữ đầu câu về Huế −1,37 s (đo 04/11); câu không về Huế +~0,00023 USD;
- **tra web sau câu từ chối (Phase 9 B6, merge `7ff8e5a` 05/11 tối) — cờ `tra_web: true` (BẬT 21:15 05/11/2026, User duyệt):** `backend/llm/tra_web.py` (Serper một lần, hạn 5 s; sổ link; mục "Từ web (chưa kiểm)" tách khỏi câu kho; kiểm bằng code: [w n] ∈ sổ, link / HTML thô bị chặn, tiền ⊂ đoạn trích, lưu trú 0 tiền, thời gian thực 0 chữ số, thiên tai ⇒ câu cố định NCHMF / 112); giao diện bộ lọc riêng không tạo link từ chữ model; câu kho trả lời được ⇒ không tra; câu hỏi (đã chuẩn hoá) gửi Serper = đường ra mới (spec Phase 9 §7, User chấp nhận);
- **hỏi bằng ảnh — Phase 10 P1 v1 (merge `2ca9937` 05/11 tối) — cờ `anh.bat: true` từ 08/11 (`cf57309`, User bật; sửa dòng cũ 10/11):** `backend/llm/nhan_anh.py` (luna gợi ≤ 3 tên trong danh sách 42 mục do code dựng / `khong_nhan_ra`), `backend/api/routes/anh.py` (rào cỡ / kiểu / Origin, đọc luồng có bộ đếm, log `anh_metrics` không nội dung), giao diện `HoiBangAnh.jsx` (gợi ý "có thể sai" + nút xác nhận; trả lời chỉ sau khi bấm); cờ tắt ⇒ route 404, chuỗi gửi model giống byte (228 / 228). P1 âm theo thước gốc ⇒ User giữ dạng gợi ý có xác nhận; P2 SigLIP 2 đang đo;
- **định tuyến phương án B (09/11, merge `3b52017`):** tuyến `khan_cap` của định tuyến ⇒ đi trợ lý Huế (log `emergency_by="router"`); câu soạn sẵn + luật từ khoá khẩn cấp + `emergency.py` gỡ; lời dặn định tuyến / trả lời giống byte bản trước; giới hạn User nhận: câu ngoài phạm vi bị xếp khẩn cấp (vd y tế) ⇒ trợ lý từ chối ⇒ cổng web mở;
- **công cụ ngày + âm lịch T1 (merge `e401c71` + `99ea59a`, BẬT `7eb1f12` 09/11):** `backend/llm/ngay_lich.py` (`lunar-vn`; code tính hôm nay / đổi dương ↔ âm; không nêu năm hoặc "năm nay" với ngày âm ⇒ code nêu lần đã qua + lần sắp tới); chỉ đưa công cụ khi code dò thấy từ chỉ ngày; câu ngày p50 chữ đầu 5,19 s (n = 5, vượt sàn — tối ưu sau);
- **4 chốt deploy (merge `ccc9f4f` 09/11):** `backend/api/gioi_han.py` (`HUE_LUOT_MOI_NGAY` lượt / IP / ngày, RAM, 429), `HUE_COOKIE_SECURE`, `HUE_TAT_DOCS`, log `RotatingFileHandler` 10 MB × 3; không đặt ⇒ như cũ;
- **định tuyến khẩn cấp (B143, merge `e3cdb96` 03/11 tối — câu soạn sẵn đã gỡ 09/11):** `khan_cap` thêm loại vừa bị cướp / giật / trộm / hành hung cần báo công an (`ROUTER_INSTRUCTIONS` `164bd4a254e9`); **04/11 (B154, merge `4e3cb4e`):** câu soạn sẵn đổi dòng mở PA1 — thêm "hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng)";
- **thử tốc độ #1 (04/11, âm):** mức suy luận "none" cho định tuyến phạm sàn S1 (2 câu an toàn ⇒ `ngoai_pham_vi`) ⇒ cờ `router_reasoning_effort` không vào `main`; tag `hoso/p9-toc-do-1` (`c156_toc_do_dinh_tuyen.md`);
- **định tuyến (Phase 9 B1, merge `f01c032` 03/11):** `assistant.py` `_pick_route` — một lần gọi `gpt-6-luna` (~580 token vào / ~35 ra, ~1,5 s) chọn `tro_chuyen` / `tro_ly_hue` / `ngoai_pham_vi` / `khan_cap`; lỗi / > 10 s ⇒ `tro_ly_hue`; cờ `settings.yaml` `assistant:` (bật `router`, `may_have_changed_notice`; tắt `emergency_rule`, `today_line`); `evaluation generate` không `--flags` theo `settings.yaml` ⇒ đo RAG 1–8 thuần truyền `--flags` rỗng;
- **đánh giá người dùng (B142, merge `6817897` 03/11 tối):** `POST /api/feedback` ⇒ log `chat_feedback` (turn_id ngẫu nhiên, tuyến, kết quả, số nguồn, đánh giá; không nội dung); nút gợi ý dưới câu ngoài phạm vi;
- **nhớ hội thoại + giao diện nhiều lượt (Phase 9 B3, merge `a3dabba` 03/11 tối):** `backend/api/conversations.py` (RAM, 3 lượt, cookie 30 phút) — **bật từ B3b** (`9e2ecd9`): `nho_hoi_thoai: true`, `nho_cau_tra_loi: false` (chỉ nhớ câu hỏi); câu dặn hẹp D6 trong `ANSWER_SYSTEM_INSTRUCTIONS` chạy mọi câu; giao diện Bản 1 (số nguồn hiển thị 1..k, "Cuộc trò chuyện mới");
- **tìm thêm (Phase 9 B2, merge `00d670e` 03/11):** `tim_them` bật — tuyến `tro_ly_hue` tìm đầu bằng câu gốc (`lan_tim_dau: v0`) rồi model gọi `tim_kho` thêm ≤ 2 lần, `max_turns` 4; token `chat_metrics` = tổng mọi lượt; ≈ 0,00031 USD / câu;
- generation `gpt-6-luna` (OpenAI); config `backend/config/settings.yaml`
  (`full_corpus_runtime`, `full_corpus_generation`).

**Candidate dense trong code** (`backend/embedding/full_corpus.py`):
`e5-small-384` (local) và `qwen3-embedding-8b-4096` (OpenRouter
`qwen/qwen3-embedding-8b`, pin Nebius, `data_collection: deny`, batch 64) —
8B đã thử 30/10: kém hơn, không chọn, index thử đã xoá.

**Qdrant** `127.0.0.1:6335` (gRPC 6336; port đổi để chạy song song
một dự án khác của User). Collection chatbot `hue_full_corpus_7a2_e5_small_384` (8.435
point) + collection thử ảnh `hue_anh_siglip2` (172 điểm, chờ User quyết xoá). Hai collection Foods đã xóa ở B9 (24/10, User chạy); code/test/notebook Foods cũ đã gỡ
(`1832201`).

**Corpus:** 204 file → 8.435 chunk (05/11 tối: giờ mở cửa 11 file; 28/10: đợt sửa kho 123 sửa / 65 file, loại file danh mục `performing_arts`; 30/10 đợt 2: 123 sửa / 40 file, 2 dòng xoá ⇒ −2 đoạn, chunk_id `file#số` dồn ở 2 file; chunker giữ nguyên từ Phase 2: chia theo cấu
trúc Markdown, không overlap có chủ đích (thực tế 3 cặp chunk lặp body: blockquote lồng trong list
item, `markdown_blocks.py:233-250`, B8 2026-10-24), mỗi chunk vừa cả 3 tokenizer e5-small 512 / e5-base
512 / huydang 256; trung vị 85 token e5). `knowledge-base-hue/` không có Git
(`.gitignore`); backup Gate 1 đã xóa khi đóng Phase 7A2.

**Golden:** `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (176 case),
`golden_full_corpus_smoke.jsonl` (10, deep-equal); schema 4 field `question`,
`keywords`, `reference_answer`, `category`; private; md5 **`6331e88fb171`** từ 30/10 (đợt 2: User sửa đáp án mẫu câu 5, 127; trước `0f7dbf41b422`). Foods Golden V3 (45 + 10)
là lịch sử.

## 5. Quyết định đang hiệu lực

| Ngày | Quyết định | Nguồn |
|---|---|---|
| 2026-11-09 (A ghi nhận 20:13–22:34 09/11/2026) | Quyền như 08/11; **trần Phase 9 4,0**; tiền API thoải mái nhưng ưu tiên tốc độ; **vòng tự soi bắt buộc mỗi phiên** + bỏ test không bảo vệ sàn + "cắt giảm nhưng vẫn đảm bảo chất lượng"; bỏ "rảnh phải giao việc" (giữ 4 session); mọi phương án tự trả lời "đã thấy thật chưa · không làm mất gì"; khẩn cấp sau G giữ như 08/11; G S2b + S09 nhận giới hạn; T3 (a) rồi đóng hồ sơ; bật `ngay_lich`; câu ngày chậm ⇒ giữ bật, tối ưu sau; mốc đóng tính năng chưa chốt; User học dự án sau khi xây xong | User |
| 2026-11-05 tối (A ghi nhận 19:19–20:27 05/11/2026) | Quyền phiên như sáng; **trần Phase 9 nâng 2,5 USD**; giữ sửa kho giờ mở cửa (1 câu Golden phạm sàn lượt 1, chạy lại đạt); **luật S-AT mới** (chênh đúng 1 ⇒ sinh thêm 3 + 3, âm khi tổng chênh ≥ 2 / 6); **cache câu trả lời giữa các cuộc trò chuyện ⇒ backlog Phase 12** (đo tỉ lệ lặp trước; không cache theo nghĩa) | User |
| 2026-11-05 (A ghi nhận 08:53–09:43 05/11/2026) | Quyền phiên như 04/11; tiền Phase 9: hết thì xin thêm; **B4 tách — giữ hỏi lại lịch trình** (Cách A chi phí âm); duyệt bậc 1 đề xuất mở rộng (`bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md`) — ý khác là backlog, làm dần; **chia Phase 10 (giọng nói + ảnh, song song Phase 9) · 11 (trải nghiệm Huế) · 12 (vận hành, deploy)**; mở phiên E; giọng nói: nghiên cứu open-source / VN trước, không gọi API ngay; **vẫn áp nền tảng AI FDE**; **đóng code khi User nói (dự kiến 25–30/12, không còn 20/12), đóng = đã chạy trên AWS**; lưu trú ⇒ backlog Phase 11 (khu nên ở + link tìm phòng do code dựng + web B6, không nói giá phòng); **quyền dữ liệu (09:56 05/11/2026): dữ liệu công khai dùng thoải mái — mục đích học tập / phát triển, không thương mại** (thước chất lượng vẫn như sản phẩm thật; thêm vào kho vẫn theo luật sửa kho) | User |
| 2026-11-04 (A ghi nhận 19:35–21:07 04/11/2026) | Quyền phiên như 03/11 + "tiếp tục điều phối, phát triển, triển khai, tự nghiên cứu, so sánh, đánh giá, viết báo cáo"; vòng cải tiến 17 duyệt (W52, W54, I10); **câu khẩn cấp PA1** (merge `4e3cb4e`); B4 vòng sửa 2 (thêm câu "không nhân giá theo số người / ngày"); bảng điểm B5 v2 duyệt (cột buổi; phố đêm chỉ tối; Bao Vinh sáng + chiều; giữ lưu ý); **thêm bậc "sửa lịch nhiều lượt" sau B5** + cột `ten_khac` (nghiên cứu repo + TRIPO vòng 3, `92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000) | User |
| 2026-11-03 (A ghi nhận 10:52 03/11/2026) | **Công cụ dự báo thời tiết Huế** (User đề xuất): tra cứu API + điều khoản trước (0 USD), **quyết lúc viết plan B5**; code gọi API, model không tự dự báo, ghi nguồn + giờ. Quyền phiên như 02/11 + A tự commit / push cả phiên (User). Tốc độ B1: PA1 mặc định (merge, tối ưu sau B2). README không nhắc quy trình agent / lộ trình (User) | User |
| 2026-11-02 (A ghi nhận 11:21–14:48 02/11/2026) | **Phase 9 = trợ lý agent có công cụ** (User: "lên trợ lý mà không khác RAG mức 1 thì cần gì trợ lý"); giữ OpenAI Agents SDK 0.19.4 + mẫu khoá AI FDE (không người duyệt lúc chạy — không hành động ghi ra ngoài); agent định tuyến đầu ra có cấu trúc (ý User); câu tìm kho = thí nghiệm nhiều phương án; nhớ hỏi + đáp bắt buộc (P1: chỉ trong cuộc trò chuyện); code giữ ngày / web / lần tìm đầu (thí nghiệm); P2 model viết mục "Từ web"; P3 không giới hạn tên miền; P4 trần Phase 2,0 USD; P5 dùng Serper luôn (User chấp nhận rủi ro điều khoản); **chất lượng trước — tiền / tốc độ chỉ theo dõi, log USD mỗi lần gọi**; bỏ bộ web xấu cố định (User: over-engineer); khi ổn định nghiên cứu thêm công cụ mới. **Spec bản 9 duyệt `169c2dd5f86a`** | User; spec Phase 9 §2, §10 |
| 2026-11-02 (A ghi nhận 09:48–10:36 02/11/2026) | Quyền phiên như 01/11; gói npm giao diện (lõi + shadcn có điều kiện ⇒ dùng 0 Radix sau dò CSP); **giao diện mới vào `main` `ed8e6e8`** (review C119 đạt) | User; `report_agent/2026-11-02_giao_dien_moi_code/` |
| 2026-11-01 (A ghi nhận 16:01 01/11/2026) | **Tên đề tài đã chốt với giảng viên:** "Xây dựng ứng dụng hỗ trợ trải nghiệm văn hóa và du lịch Huế dựa trên Retrieval-Augmented Generation" (*Developing a Retrieval-Augmented Generation-Based Application for Cultural and Tourism Experiences in Hue*). **Brainstorm Phase 9 câu B1 = (b):** "trợ lý di sản Huế đáng tin" (câu nhiều nguồn, hỏi lại, nhớ ngắn, thông tin theo ngày + chặn câu an toàn) **+ lịch trình gợi ý có điều kiện mức nhỏ** (thứ tự điểm có nguồn; không giá / giờ chính xác; không đặt chỗ). Căn cứ: nghiên cứu sơ bộ + thử Huế TRIPO (B119). **Bảo vệ: khoảng 04–10/01/2027** (lịch trường, chưa có ngày cụ thể — User 16:08 01/11/2026) ⇒ A tạm đặt **đóng code ~20/12/2026** (~7 tuần) | User |
| 2026-11-01 (A ghi nhận 14:23–14:29 01/11/2026) | **B0 xong, giữ context 10** (luật dừng "chưa rõ" ⇒ User chọn (a)); **User đóng Phase 8**. Nhận xét User: câu dự trù chi phí nên để trợ lý hỏi lại (Phase 9); `[n]` chen trong câu khó đọc — A đề xuất giữ ở tầng máy, đổi cách hiển thị ở giao diện mới (chờ User). Quyền phiên chiều như sáng 01/11 | User; `data/phase_8_2/b0/ket_qua_b0_2026-11-01.md` |
| 2026-11-01 (A ghi nhận 12:02 01/11/2026) | **Câu nhiều nguồn để Phase 9** (Q3a: chỉ loại này còn lỗi lớn — 18 câu Đủ 3,50 ↔ 4,92, 8 câu yếu đều thiếu bằng chứng ở tầng tìm); không mở thí nghiệm ở Phase 8. Plan đo cuối duyệt `ae8d42d520d4` (bộ kín agent 40 câu, A/A cùng ngày, trần 0,20 USD) | User; `q3a_theo_loai_cau_implementation.md` |
| 2026-11-01 (A ghi nhận 11:20 01/11/2026) | **Hội thoại nhiều lượt / nhớ lịch sử dời sang Phase 9** (phần trợ lý / agent) — không làm ở Phase 1–8; nháp spec C102 giữ làm tư liệu | User |
| 2026-11-01 (A ghi nhận 10:20–11:04 01/11/2026, theo các dòng `date` trong `CURRENT_HANDOFF.md` / `STATUS_A.md`) | Quyền phiên như 31/10 (≤ 1 USD); **Q1 streaming:** sàn tới chữ đầu giữ p50 ≤ 3 / p95 ≤ 5 s + mục tiêu báo cáo 1,5 / 3 s (không chặn); **duyệt spec streaming `00fb57ee01b2`** (commit `74a6082`); B0 làm hôm nay; Golden câu 127 (lệch kho chỉ ở hoa / thường, chấm không sai) **giữ nguyên**; "tiếp tục điều phối, phát triển, cải thiện, tối ưu, so sánh đánh giá, viết báo cáo", đóng phiên ~16:20, không làm nhanh bỏ sót | User |
| 2026-10-31 (A ghi nhận 17:32 31/10/2026) | **Đóng gói Phase 1–8:** một báo cáo tổng "so sánh phương án + nhìn lại Phase 1–8" (hai phần: theo khâu + theo Phase, chỉ mục chéo; đầy đủ, có số đo, nhãn độ tin; người đọc = User + Claude + ChatGPT); trước đó **đo cuối + thử có giới hạn** (lượt đo cuối cùng một commit + bộ kín mới + B0; thử thêm chỉ cho 2–3 lỗi đã biết). Báo cáo `bao_cao_he_thong/` luôn đúng thông tin mới nhất, xoá phần không còn đúng (`WORKFLOW.md` §6) | User; `CURRENT_HANDOFF.md` mục 4 |
| 2026-10-31 (A ghi nhận 16:48 31/10/2026) | **Phase 9 mở bằng nghiên cứu rộng** (đề tài, dự án, paper, ứng dụng thực tế; cách đã làm ở một dự án khác của User: nghiên cứu ⇒ thử nghiệm trước), không chỉ gợi ý lịch trình; ứng viên cũ (agentic RAG, gợi ý / lịch trình — 27/10) giữ làm ứng viên. Phase 1–8 = RAG mức 1 | User |
| 2026-10-31 15:51–16:43 | **Phiên chiều 31/10 chỉ làm AI FDE** (chưa làm tiếp dự án). Áp khung_fde (khung cá nhân của User): W37 hook giờ ước, W38 xét mọi mục đang thử, W39 `teach-and-quiz` cho D, W40 phần nhỏ từ skill mẫu, W41 chép sẵn `agent-design-review` + `agent-security-review` cho Phase 9; vòng cải tiến 12 (40 ⇒ 7 mục đang thử). **Nhìn lại Phase 1–8 theo khung khoá** làm ở bước đóng gói (sau streaming + nhiều lượt). A được commit + push phiên này | User; `SO_CAI_TIEN_CACH_LAM.md` W37–W41 |
| 2026-10-31 11:26–11:48 | **Streaming:** D1 = **PA1** (chữ hiện ngay khi model viết + tiến độ thật; kiểm citation cuối như hôm nay); D2 = **(a)** sàn p50 ≤ 3 s / p95 ≤ 5 s đổi sang "tới chữ trả lời đầu tiên hiện trên trình duyệt" (Playwright), tới đủ câu chỉ theo dõi; D3 = bộ kiểm cuối hỏng ⇒ **rút lại**, lỗi / đứt giữa chừng ⇒ **xóa hết** (lời báo + "Thử lại"). Phạm vi: API + sửa tối thiểu `frontend/`; **giao diện mới bàn sau Phase 8** gộp AI FDE (10:23) | User; spec `2026-10-31-streaming-design.md` §2 |
| 2026-10-31 11:21–11:44 | **Tra web bằng Codex CLI** (`scripts/tra_web_codex.sh`, thêm ngày hôm nay + đòi thông tin mới nhất): câu tra nhanh mọi session tự chạy; nghiên cứu lớn: Codex **và** ChatGPT web (thử 31/10: Codex ngang ChatGPT 2 / 3 bài). **Không bao giờ gọi `agy` từ agent** (điều khoản Google; `.claude/settings.json` chặn; User tự dùng được). A tự chạy commit / push sau khi hỏi; chỉ đưa `!` khi bị chặn | User; `report_agent/2026-10-31_tra_web_codex/TONG_HOP.md` |
| 2026-10-30 16:12 | **Qwen3-8B kém hơn ⇒ giữ e5-small** (sàn 0 câu mất đoạn đúng vỡ 3 / 40 dev + 3 test; vector câu hỏi 2,2 s qua mạng); collection thử xoá; User: không giữ bộ đệm, chỉ ghi kết quả; code giữ bằng tag `hoso/b92-qwen3-harness`, không merge | User; `qwen3_8b_implementation.md` |
| 2026-10-30 15:07 | **Giá `gpt-6-luna` đủ (User dán bảng giá, ngữ cảnh < 272k token):** vào 0,10 · ra 0,50 · đọc đệm 0,01 · **ghi đệm 30 phút 0,125** · ghi đệm 12 giờ 0,25 USD / 1M. B95: mỗi câu `cache_write_tokens` ≈ toàn bộ phần vào, `cached_tokens` = 0 ⇒ `cost_usd` (giá phẳng 0,10) **ghi thiếu ≈ 20 % / câu** (~0,00021 ⇒ ~0,00025, vẫn dưới trần 0,0005); mọi số USD cũ đếm theo giá phẳng. Sửa công thức + log `cache_write_tokens`: việc đóng gói | User; B95 |
| 2026-10-30 14:39 | **User đóng đợt 2 sửa kho, giữ sao lưu cả hai đợt** (không làm hỏng: Golden 176 + bộ an toàn 32, 0 sai điều kiện mới, ≈ 0,047 USD); gold v5 + Golden câu 5 / 127 (User duyệt 13:39–13:43); thứ tự sau đợt 2: **đo "ngày hôm nay" trước Qwen3-8B**; giữ thứ tự cũ (PA2) ⇒ streaming ⇒ nhiều lượt ⇒ đóng gói Phase 1–8 ⇒ Phase 9; bối cảnh đồ án 5 ý đúng; quyền phiên như 29/10 | User |
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
| 2026-10-25 19:4x | **Sửa code theo rà soát: đồng ý 5 gói** (`bao_cao_he_thong/94_DE_XUAT_SUA_CODE.md`); gỡ code không dùng nếu không ảnh hưởng hệ thống; guide 0–4 thêm dòng lịch sử; nội dung kho + đường dẫn dự án khác ra khỏi file tracked từ giờ, không xóa lịch sử git. Sửa trên `main`; B1 chờ B0 như spec 8.2 | User; `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md` |
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
| 2026-10-24 | Cách làm việc học từ một dự án khác của User: báo cáo cho User chỉ ở `bao_cao_he_thong/` (README mục lục, `01_LUONG_HOAT_DONG_HE_THONG`, `BAO_CAO_<khâu>` sống + thang 5 mức, `nhat_ky/`); report agent theo đợt `report_agent/<YYYY-MM-DD>_<chủ_đề>/` + `TONG_HOP.md`; giờ bằng `date`; stage từng file + `git diff --cached --stat`; A thử trong worktree; quyền đặc biệt hết hạn cuối phiên | `WORKFLOW.md` §6, §8, §9; tài liệu cách làm của dự án khác (`report_agent/2026-10-24_to_chuc_bao_cao/`) |
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
- Data egress: runtime gửi câu hỏi + ngữ cảnh (tối đa 10 đoạn kho) tới OpenAI (`gpt-6-luna`) mỗi lần sinh câu trả lời; chunk/query tới OpenRouter
  chỉ cho `qwen/qwen3-embedding-8b` trong việc đã duyệt, mọi request `data_collection: deny`; **từ 21:15 05/11/2026:** câu hỏi về Huế mà kho từ chối ⇒ gửi Serper (tra web B6) + đoạn trích web gửi OpenAI; **cờ `anh.bat` bật từ 08/11** (Phase 10): ảnh người dùng (thu nhỏ) gửi OpenAI `gpt-6-luna` kèm dòng báo trên giao diện (User duyệt spec Phase 10 10:28 05/11/2026) (sửa 30/10: dòng cũ thiếu OpenAI — sub-agent đối chiếu khoá FDE tuần 3).
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
skills/{practical-project-coding,risk-gated-agent-review,propose-options,run-experiment,improve-workflow,teach-and-quiz,agent-design-review,agent-security-review}/SKILL.md
                                       (3 skill cuối theo khung_fde — khung cá nhân của User, private, ngoài repo; 2 skill agent dùng từ Phase 9)
.githooks/pre-commit, pre-push, .claude/settings.json   rào bằng máy (hook git mọi agent — pre-push 01/11 kiểm lại private / secret / tên dự án khác trên mọi commit sắp đẩy; Claude Code cấm đọc .env, cấm `agy`)
.claude/hooks/                         hook Claude Code cảnh báo giờ ước lúc ghi (W37; `bash .claude/hooks/thu_hook.sh` ⇒ ĐÚNG n / n)
scripts/grep_kb.sh                     tìm trong nội dung kho, luôn loại evaluation/ meta/ *sealed* (W27)
scripts/tra_web_codex.sh               tra web bằng Codex CLI (chỉ thông tin công khai; kết quả data/tra_cuu_cli/) — §9
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
  khóa sha `bab707b9ab22`) ⇒ không chạy lại; kiểm nhãn v2 bằng `data/phase_8_1/tools/build_gold_v2.py` (chỉ đọc). Nhãn dùng cho đo: **`gold_v5.jsonl` từ 30/10** (`33d16fd6b8f4`, kho sau đợt 2, User duyệt 1 trích dẫn; `GOLD_PATH` trỏ v5 từ `bfb0b41`); trước đó `gold_v4.jsonl` từ 28/10 (`927bae1bf201`, kho sau sửa đợt 1; trước đó `gold_v3.jsonl` từ 27/10 chiều (`3b1117cf59e9`, B75; trước đó `gold_v2.jsonl` B69) — `GOLD_PATH`
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
- **Codex CLI (31/10):** `--search` phải đứng **trước** `exec`; model mặc định trong `~/.codex/config.toml` (`gpt-6.1-sol`) không dùng được với tài khoản ChatGPT ⇒ `-m gpt-6-luna`;
  `-s read-only` **không** chặn đọc file ngoài thư mục làm việc ⇒ **từ 01/11 script bỏ `-s`**, tắt `shell_tool` / `view_image`, dùng permission profile chỉ đọc thư mục làm việc, `--ignore-user-config`; còn `command_execution` ⇒ lỗi (thử thật 01/11: tìm web chạy, 0 lệnh shell, "không có công cụ đọc file"). Vẫn chỉ gửi thông tin công khai. `url_da_mo.txt` thường ít hơn nhiều so với URL trong báo cáo (31/10: 1 / 15) ⇒ URL còn lại là tự khai, kiểm kỹ.
- **Qdrant chạy bằng Docker Desktop (Windows):** WSL không có lệnh `docker` khi Docker Desktop tắt (31/10 mở phiên) ⇒ User bật rồi `docker compose up -d qdrant`.
- `rm` / `cp` với đường dẫn ghép từ biến (`$X/*`) bị tầng an toàn Claude Code chặn ⇒ `"${X:?}"/…` hoặc đường dẫn tuyệt đối (31/10, A + B).
- **Giao diện cần bản build (02/11):** `frontend/dist/` không commit ⇒ clone / worktree mới hoặc sau khi sửa `frontend/src/`: `cd frontend && npm ci && npm run build`; thiếu ⇒ `/` 404 và `tests/test_static_ui.py` báo lệnh cần chạy. Kiểm CSP chỉ trên bản build do FastAPI phục vụ (không dùng `vite dev`).
- **`pgrep -f` / `pkill -f` khớp chính lệnh đang chạy** (02/11: A tự tắt shell khi `pkill -f "port 8831"`; B chờ ~2 giờ vì vòng chờ `pgrep -f` luôn thấy chính nó) ⇒ chờ tiến trình nền bằng thông báo của công cụ (`run_in_background`), hoặc mẫu không khớp chính nó (`pgrep -f "[u]vicorn …"`); tắt server tạm bằng TaskStop / PID đã ghi.
- **WebSearch không dùng được** dù có trong danh sách công cụ hoãn của Claude Code: 31/10 A thử ⇒ `API Error: 400 tool type 'web_search_20250305' is not supported for this model` (Bedrock) ⇒ tra web bằng `scripts/tra_web_codex.sh`.
- **Kiểm dòng log trong test / ca dò** (03/11 tối, S89, I10): đọc `backend/logs/application.log` sau mốc dòng (`wc -l` trước), không gắn handler riêng vào logger — app dựng handler riêng nên handler gắn thêm có thể không thấy dòng log.
