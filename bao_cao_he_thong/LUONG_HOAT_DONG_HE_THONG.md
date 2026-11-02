# Luồng hoạt động hiện tại của chatbot Huế (hue_rag)

**Cập nhật lần cuối: 10:35 02/11/2026 — bản 19: giao diện web làm lại (React + Vite + Tailwind, merge `ed8e6e8`); API, tìm kiếm, model không đổi.** Trước: 14:33 01/11/2026 — bản 18: B0 xong, Phase 8 bạn đóng 14:29 01/11/2026.** Trước: 13:42 01/11/2026 — bản 17: lượt đo cuối xong (mọi sàn đạt). Trước: 12:50 01/11/2026 — bản 16: streaming vào chatbot (bước 8 mục 3, số tốc độ mới mục 5); công thức tiền giá đủ; việc kế tiếp = đo cuối.** Trước: 11:33 01/11/2026 — bản 15: mục 5 "Giới hạn đã biết" viết lại đầy đủ theo mức nặng (bảng giới hạn bản 4, 01/11); việc kế tiếp: streaming đang code, nhiều lượt dời Phase 9.** Bản 14: 17:10 31/10/2026.
Các bản trước: xem `git log` file này.

File này mô tả hệ thống **đang chạy**. Mỗi lần hành vi đổi (chia đoạn, chỉ mục, cách tìm, prompt, model), file này được cập nhật theo.
Những gì đã thử và bỏ nằm trong báo cáo từng khâu (`BAO_CAO_*.md` cùng thư mục). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

**Tóm tắt hôm nay (01/11):** kho 204 file / 8.424 đoạn; tìm bằng vector nghĩa e5-small + từ khoá BM25; đưa tối đa 10 đoạn vào ngữ cảnh; `gpt-6-luna`
trả lời có trích dẫn. **Mới 01/11: chữ hiện dần (streaming)** — trang web hiện câu trả lời ngay khi model viết; đo trên trình duyệt: chữ đầu tiên
trung vị **1,23 s**, câu chậm (p95) **2,61 s** ⇒ đạt sàn 3 / 5 s và cả mục tiêu 1,5 / 3 s. Lượt đo cuối Phase 1–8 xong (mọi sàn đạt), B0 xong; **Phase 8 bạn đóng 14:29 01/11/2026**. Việc kế tiếp: giao diện mới ⇒ Phase 9 (mục 5).

---

## 1. Toàn cảnh

```text
CHUẨN BỊ (chạy một lần khi kho đổi):
  204 file Markdown → chia đoạn (8.424 đoạn) → vector nghĩa e5-small + từ khoá BM25 → lưu Qdrant
HỎI ĐÁP (mỗi câu hỏi):
  giao diện web → API /api/chat → chuẩn hóa NFC câu hỏi → tìm 10 đoạn → đưa tối đa 10 đoạn làm ngữ cảnh → gpt-6-luna trả lời
  → kiểm trích dẫn [n] → trả câu trả lời + nguồn (trả một lần khi xong cả câu; chưa hiện chữ dần)
```

| Thành phần | Dùng gì | Code |
|---|---|---|
| Kho tri thức | 204 file Markdown tiếng Việt vào chỉ mục (đã sửa hai đợt: 28/10 và 30/10), 5 chủ đề: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch | `knowledge-base-hue/` (private) |
| Chia đoạn | Theo cấu trúc Markdown (tiêu đề, đoạn, bảng), không chồng lấn | `backend/ingestion/chunking/full_corpus_chunker.py` |
| Vector nghĩa | `intfloat/multilingual-e5-small`, 384 chiều, chạy trên máy (CPU), miễn phí | `backend/embedding/full_corpus.py` |
| Từ khoá | BM25 tự viết, tách theo âm tiết, từ điển 5.631 từ | `backend/scoring/bm25.py` |
| Cơ sở dữ liệu vector | Qdrant `127.0.0.1:6335`, chạy trong Docker Desktop (Windows); collection `hue_full_corpus_7a2_e5_small_384`, 8.424 điểm | `backend/vectorstore/`, `docker-compose.yml` |
| Tìm kiếm | `dense_bm25_rrf` (mục 3) | `backend/retrieval/full_corpus.py` |
| Trả lời | `gpt-6-luna` (OpenAI) | `backend/llm/generator_openai_full_corpus.py` |
| API + giao diện | FastAPI (`/api/chat`, `/api/chat/stream`, `/health`); trang web React + Vite + Tailwind (từ 02/11) — FastAPI phục vụ bản build tĩnh `frontend/dist/` (build một lần: `cd frontend && npm ci && npm run build`; thiếu bản build ⇒ API vẫn chạy, log cảnh báo) | `backend/api/`, `frontend/src/` |
| Cấu hình | `backend/config/settings.yaml` (`full_corpus_runtime`, `full_corpus_generation`) | |

## 2. Chuẩn bị kho (khi corpus đổi)

1. Đọc 204 file Markdown (3 file danh mục biên soạn bị loại — `settings.yaml:18-21`), mỗi file chia theo cấu trúc: mỗi đoạn văn / mục
   danh sách / bảng là một đoạn; bảng quá dài thì mỗi dòng một đoạn kèm hàng tiêu đề. Đoạn mang theo tên file và đường tiêu đề
   (ví dụ "Bún bò Huế > Quán nổi tiếng") để tìm dễ hơn.
2. Mỗi đoạn được tạo **vector nghĩa** (e5-small) và **vector từ khoá** (BM25), lưu cùng một điểm trong Qdrant kèm 7 trường: chữ để tìm,
   nguồn, tiêu đề, đường tiêu đề, phần trích dẫn, mã đoạn, chủ đề.
3. Đoạn nào vượt giới hạn token, hay quy tắc điều kiện không khớp đúng một chỗ ⇒ **dựng kho dừng**. Từ điển BM25 dùng chung chỉ được ghi
   **sau** khi kiểm chỉ mục đích hợp lệ. Quy trình dựng lại: `guides/full_corpus_rag.md` mục "Build lại index khi corpus đổi".
4. Một **phiếu build** ghi dấu (hash) của từng file corpus. Khi khởi động, API so dấu với kho hiện tại; kho đã sửa mà chưa build lại thì
   **API từ chối chạy** (để không trả lời bằng dữ liệu cũ).

## 3. Khi người dùng hỏi

0. **Chuẩn hóa câu hỏi:** câu hỏi rỗng bị từ chối; câu còn lại đổi về dạng Unicode **NFC** (kho và chỉ mục đều ở dạng NFC; câu gõ dạng
   NFD — dấu tách rời, có ở một số máy — trước đây làm tìm kiếm tụt). Câu đã ở NFC giữ nguyên từng byte
   (`backend/retrieval/full_corpus.py:97` `normalize_query`).
1. **Tìm 30 ứng viên** bằng vector nghĩa (câu hỏi được thêm tiền tố `query:` theo hướng dẫn của e5).
2. **Chấm lại bằng BM25** trong chính 30 ứng viên đó, rồi **gộp hai bảng xếp hạng bằng RRF** (k = 60) → giữ 10 đoạn đầu
   (`backend/retrieval/full_corpus.py:483-602`). Lưu ý: BM25 chỉ chấm lại đoạn mà vector nghĩa đã tìm thấy, không tìm thêm đoạn mới.
3. **Không xếp lại bằng reranker** (`settings.yaml:44` `reranker: none`) — các cách xếp lại đã thử đều chưa đáng đưa vào (mục 4).
4. **Đóng gói ngữ cảnh:** lấy tối đa **10 đoạn đầu**, nguyên vẹn, đánh số [1]…[10], trong ngân sách 16.384 token
   (`settings.yaml:53`, `:56` `max_context_documents: 10`). Trung bình ~1.655 token vào mỗi câu (176 câu Golden, đo ở bản 10 đoạn).
5. **gpt-6-luna trả lời** chỉ từ các đoạn đó, tiếng Việt, đặt [n] sau mỗi ý. **Nếu thiếu bằng chứng** thì trả đúng câu: "Tôi không tìm thấy
   đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." (`backend/llm/full_corpus_prompt.py:4`). Câu hỏi ghép nhiều vế mà kho chỉ có
   một vế thường bị từ chối cả câu (mục 5).
6. **Kiểm trích dẫn:** model đôi khi viết `[Nguồn n]` thay vì `[n]` — hai dạng cùng nghĩa: backend đổi hết về `[n]` (để trang web gắn
   link) rồi mới kiểm (`backend/llm/citations.py`). Mọi [n] phải trỏ tới đoạn có thật; câu trả lời có nội dung mà không có [n], hay từ chối
   mà vẫn có [n] → API báo lỗi 500 thay vì trả câu trả lời không kiểm được.
7. **Ghi số đo:** mỗi lần gọi `/api/chat` — kể cả lỗi 409 / 503 / 500 — ghi đúng **một dòng** `chat_metrics` vào log `chat` (màn hình +
   `backend/logs/application.log`, không commit; `backend/api/routes/chat.py:24-83`): kết quả, mã HTTP, có từ chối không, model, token vào /
   ra / suy luận, số nguồn đưa vào / được trích, thời gian tìm / dựng ngữ cảnh / sinh / kiểm trích dẫn / tổng (ms). **Không** ghi câu hỏi,
   câu trả lời, nguồn, tiền (tiền tính sau từ token theo bảng giá). Thêm < 1 ms mỗi câu. Từ 01/11 ghi thêm token **ghi đệm / đọc đệm** (để tính đúng giá),
   và ở đường stream: thời gian tới sự kiện / chữ đầu tiên, có ngắt giữa chừng không.
8. **Chữ hiện dần (từ 01/11, `POST /api/chat/stream`, trang web dùng đường này):** bước 0–5 như trên; lỗi trước khi model viết vẫn trả JSON như `/api/chat`.
   Khi model viết, server gửi từng mảnh chữ (sự kiện `status` → `delta` … → `sources` → `done`); **bước 6 (kiểm trích dẫn) chạy lúc cuối** — qua thì mới gửi
   nguồn và bật link [n]; **hỏng thì trang web rút lại chữ đã hiện**, lỗi / đứt giữa chừng thì **xoá hết** — cả hai hiện lời báo + nút "Thử lại" (bạn chọn 31/10).
   Người dùng rời trang ⇒ server dừng model, vẫn ghi một dòng log. Trang web chỉ hiện các thẻ Markdown thường (danh sách cho phép) và có chính sách bảo mật
   trang (CSP) — không tự tải ảnh / tài nguyên từ máy khác. `/api/chat` (một lần, JSON) vẫn giữ; API và bộ đánh giá dùng **chung một lõi**
   (`backend/llm/grounded_answer.py`) nên đo và chạy đi đúng một đường.

## 4. Chất lượng, tốc độ, tiền đo được

**Bản đang chạy (10 đoạn ngữ cảnh + NFC):**

| Đo gì | Kết quả | Nguồn |
|---|---|---|
| So với bản cũ (5 đoạn) trên 33 câu kín trong kho — câu viết mới, giữ kín tới cuối Phase 8 | điểm Đủ ý **+0,82** [+0,39; +1,33], điểm Đúng **+0,70**, **0 câu tụt**; câu ngoài kho bị trả lời **0 / 3** | `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` |
| Lượt đo mới nhất trên 176 câu Golden (30/10, sau sửa kho đợt 2) | không làm hỏng so với trước đợt 2 (trên 129 câu số chính: 4 câu tốt hơn / 3 kém hơn / 122 như cũ); từ chối nhầm 13 ⇒ 12 câu; 0 lỗi kỹ thuật, 0 lỗi trích dẫn mới; bộ an toàn 32 câu: 0 câu ngoài kho bị trả lời, 0 câu nói sai điều kiện mới | `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` |
| Thời gian chờ (176 câu, hỏi lần lượt, đo trong công cụ đo — **chưa** tính đường mạng tới trang web) | trung vị **2,19 s**, câu chậm (p95) **4,90 s** — trong trần bạn chốt 3 / 5 s; câu trả lời dài (bộ tự viết) trung vị 4,6 s ⇒ chưa đạt | như trên; `BAO_CAO_DANH_GIA.md` |
| Tiền một câu | ~0,00021 USD (~5 đồng) tính theo giá phẳng 0,10 USD / 1M token vào, 0,50 USD / 1M token ra; nhà cung cấp còn tính phần "ghi đệm" 0,125 USD / 1M nên số thật cao hơn ~20 % (≈ 0,00025 USD / câu), vẫn dưới trần 0,0005. Sửa công thức tính tiền: việc đóng gói Phase 1–8 | `session_prompt/Project_Status.md` §5 (30/10) |

Người chấm: Claude (chấm theo đáp án mẫu). Mốc người: B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp).

**Mốc cũ để so (Phase 7B, bản 5 đoạn, 176 câu Golden):** Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45 (tốt ở câu một dữ kiện 4,87, kém ở câu
ghép nhiều nguồn 3,28 và so sánh 3,68); từ chối đúng 18 / 18 câu ngoài kho; từ chối nhầm 22 / 158 câu kho có đáp án; đoạn chứa đáp án lọt
top-10 92,4 % (đo theo từ khoá); ~0,00014 USD / câu; thời gian chờ trung vị 3,3 s / p95 5,7 s (27/10). Bản 10 đoạn được chọn ở Phase 8.1
vì điểm Đủ ý tăng +0,26 [+0,08; +0,48] trên bộ thử, +0,27 [+0,02; +0,59] trên bộ kiểm, lợi chủ yếu ở câu nhiều nguồn / so sánh.

**Đã thử, không đưa vào chatbot** (chi tiết ở báo cáo khâu):

- Xếp lại kết quả (reranker): MiniLM tiếng Anh (bản món ăn) kém hơn; 2 model đa ngôn ngữ + `gpt-6-luna` (Phase 8.1) chưa qua luật; để
  `gpt-6-luna` chọn 10 / 30 đoạn (27/10) tìm tốt hơn nhưng câu trả lời kém hơn, chậm (p95 9,1 s khi 4 câu gọi cùng lúc), tốn 3,8× ⇒ bỏ (`BAO_CAO_TIM_KIEM.md`).
- Lấy 100 ứng viên thay 30; cho trả lời một phần khi kho chỉ có một vế (vi phạm sàn câu ngoài kho) ⇒ kém hơn, bỏ
  (`report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`).
- Model vector lớn Qwen3-Embedding-8B (30/10): 3 / 40 câu thử mất đoạn đúng (luật: 0 câu), bước biến câu hỏi thành vector chậm từ
  0,02 s lên ~2,2 s; tiền 0,0089 USD; chỉ mục thử đã xoá ⇒ giữ e5-small (`BAO_CAO_EMBEDDING_TU_KHOA.md`).

## 5. Giới hạn đã biết và việc kế tiếp

Xếp theo **mức nặng bạn chốt 28/10**: **M1** sai cảnh báo an toàn / điều kiện vào khu vực > **M2** nói chắc sai / bịa > **M3** trả lời câu ngoài kho > **M4** thiếu ý > **M5** từ chối nhầm.
Ngoài thang đó: **tốc độ / tiền** (yêu cầu bạn chốt: p50 ≤ 3 s, p95 ≤ 5 s, ≤ 0,0005 USD / câu), **thước đo** (giới hạn của bằng chứng — không phải lỗi người dùng thấy, nhưng làm kết luận yếu đi),
**vận hành** (chạy / bảo trì).

**Chất lượng câu trả lời (người dùng thấy)**

- **M1 — có thể nói sai điều kiện / cảnh báo** (vé, giờ, quy định vào khu vực): bộ 32 câu an toàn hiện **0** câu sai mới, 0 câu đảo cảnh báo (30/10); trước đó 2 câu từng nói sai *về nguồn*
  ("nguồn không nêu…") rồi lần sinh lại không sai ⇒ "lúc có lúc không". Bộ này do AI viết, chỉ 28 câu trong kho ⇒ "0 lỗi" chỉ nói được tỉ lệ sai dưới ~12 %.
- **M1 — kho có dữ kiện theo thời điểm** (giá, giờ mở cửa, lịch, tên đơn vị hành chính) có thể đã cũ; hai đợt sửa kho đã sửa 246 chỗ và **không làm hỏng** chatbot, nhưng vẫn còn mục chờ tra ngoài /
  chờ người địa phương.
- **M1 / M5 — model không biết hôm nay là ngày nào:** câu "tối nay còn mở không?", "tuần sau có…?" — đo 30/10: **0** câu đoán ngày rồi nói sai, nhưng 6 / 14 câu bị **từ chối nhầm** dù ngữ cảnh có lịch ⇒
  để **Phase 9** (công cụ ngày cho trợ lý).
- **M2 — đôi khi thêm chi tiết không có trong nguồn** (thường là nhận xét chung ở câu nhiều nguồn): 1 / 145 câu (Claude chấm, chưa có người đọc). **Bộ kiểm trích dẫn chỉ kiểm định dạng** (`[n]` có, số nguồn
  có thật), không kiểm câu chữ có đúng với nguồn được trích ⇒ "có trích dẫn" nghĩa là *có nguồn*, chưa phải *đã kiểm nghĩa*.
- **M3 — câu ngoài kho:** 0 câu bị trả lời trên mọi bộ đã đo (25 câu ngoài kho) — mẫu nhỏ, cận trên ~12 %.
- **M4 / M5 — câu so sánh / cần nhiều nguồn** điểm thấp hơn rõ, hay bị từ chối cả câu khi chỉ tìm được một vế; đưa 10 đoạn (28/10) đã cải thiện chủ yếu ở loại này, số theo loại câu trên kho hiện tại
  **chưa đo lại**.
- **M5 — từ chối câu mà kho có đáp án:** **12 / 158** câu (30/10) — lỗi lớn nhất về số; nguyên nhân chính là **xếp hạng**: đoạn chứa đáp án có trong 30 ứng viên nhưng bị xếp ngoài 10 đoạn đưa model
  (9 / 40 câu thử). Các cách đã thử (lấy 100 ứng viên, xếp lại bằng model, model vector lớn Qwen3-8B, cho trả lời một phần) đều **không qua luật** ⇒ giữ cách hiện tại.
- **M4 / M5 — dòng bảng giá dài** bị tách thành đoạn một dòng ⇒ khó tìm đúng dòng giá; chưa có số riêng ở cấu hình hiện tại.
- **M4 — ~20 % đoạn rất ngắn** (mỗi khối Markdown là một đoạn; đếm trên kho cũ): đã thử 12 cách chia khác, không cách nào tốt hơn ⇒ giữ.
- **Câu gõ không dấu:** ngoài phạm vi (bạn quyết 25/10 — người dùng gõ có dấu); đo được: tìm kiếm gần như hỏng (13 ⇒ 1 / 32 câu đủ đoạn đúng).

**Tốc độ, tiền, tính năng**

- **Tốc độ (từ 01/11 đo "tới chữ trả lời đầu tiên trên trình duyệt", streaming):** 38 câu có trả lời: trung vị **1,23 s** / p95 **2,61 s** / chậm nhất 4,74 s ⇒ **đạt** sàn 3 / 5 s và mục tiêu
  1,5 / 3 s; câu từ chối (21 câu) 1,48 / 2,93 s ⇒ đạt; tới đủ câu 1,73 / 3,81 s. Lợi "thấy chữ sớm hơn chờ đủ câu" chỉ ~**0,44 s** (câu thử ngắn, hôm đó model gần như không suy luận trước) —
  bạn chọn giữ cách hiện chữ dần (01/11). Một lần đo, 38 câu ⇒ p95 gần như là câu chậm thứ hai. Trước streaming (cả câu, qua API, 27/10): p50 3,07 / p95 6,04 s — chưa đạt.
- **Tiền:** ≈ **0,00025 USD / câu** theo giá đủ (lượt đo 01/11: TB 0,000247, lớn nhất 0,000339) ⇒ đạt trần 0,0005; công cụ đo **đã tính theo giá đủ** từ 01/11 (trước đó ghi thiếu ≈ 20 %).
- **Một lượt hỏi–đáp**, chưa nhớ câu trước ⇒ hội thoại nhiều lượt **dời sang Phase 9** (bạn quyết 11:20 01/11/2026).
- **Một nhà cung cấp sinh** (`gpt-6-luna`), không dự phòng: lỗi hoặc quá 45 s ⇒ báo lỗi, không tự đổi model.
- **Chưa đưa ra ngoài:** chạy máy cá nhân; API chưa giới hạn số lượt hỏi, chưa đăng nhập, chưa đặt hạn mức tiền phía nhà cung cấp ⇒ là điều kiện trước khi deploy.

**Streaming (chạy từ 01/11)**

- Trong vài giây người dùng thấy chữ **chưa qua bộ kiểm**; nếu bộ kiểm cuối hỏng thì chữ bị rút lại, lỗi giữa chừng thì xoá hết + nút "Thử lại" (bạn chọn 31/10). Lỗi kiểm cuối hôm nay 0 / 489 lần ⇒ hiếm;
  sẽ xem lại nếu > 1 % câu / tuần bị rút / xoá. Ca giao diện "rút lại" và "luồng đứt" chưa kiểm được bằng đường thật (chỉ phát lại luồng). Giao diện **làm lại 02/11** (merge `ed8e6e8`)
  giữ đủ 17 yêu cầu đó + nguồn hiện bằng số nhỏ bấm được + nhãn "Trợ lý AI… có thể sai"; lỗi mạng / server lạ báo bằng tiếng Việt (`report_agent/2026-11-02_giao_dien_moi_code/`).

**Thước đo (giới hạn của bằng chứng)**

- **Mốc người chỉ tham khảo:** mọi điểm chất lượng do Claude chấm (khớp `gpt-6-luna` 89–96 %). B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp).
- **Không còn bộ câu chưa ai thấy:** nhóm kiểm 56 câu và 36 câu kín đã dùng ⇒ số hiện tại có thể lạc quan hơn câu thật; **bộ kín mới** 40 câu cũng đã dùng ở lượt đo cuối 01/11 ⇒ lần kiểm sau cần bộ mới nữa.
- **Bộ đo nhỏ:** chỉ 55 / 176 câu có nhãn "đoạn đúng" ⇒ nhiều thí nghiệm ra "chưa rõ" — nghĩa là *chưa chứng minh được*, không phải *đã chứng minh bằng nhau*.
- **Gần như chưa có so sánh nào đo lại trên kho hiện tại:** phần lớn kết luận "giữ" của Phase 8 đo trên kho / cấu hình cũ. **Model sinh chưa từng được so có chấm điểm** (giữ `gpt-6-luna` theo quyết định
  của bạn 24/10).
- Không lưu câu hỏi người dùng ⇒ mọi số đo trên câu tự viết / Golden, chưa có câu hỏi thật.
- Lệnh kiểm Golden báo **1 lỗi đã biết** (1 câu khác kho chỉ ở chữ hoa / thường — không làm sai điểm; bạn chọn giữ nguyên 01/11).

**Vận hành**

- Log một file, không xoay vòng; log dùng chung cho test và server. Bộ test không có key OpenAI vẫn báo vài lỗi "bình thường" ⇒ chưa có một lệnh kiểm sạch. Kho không có Git (sửa bằng sao lưu tay + so
  khác). Mã đoạn dạng `<file>#<số>` dồn số khi thêm / xoá đoạn giữa file. Bộ chia đoạn còn giới hạn 256 token của một model đã bỏ.

Chi tiết từng dòng (số đo, nguồn, hướng xử lý) và mọi phương án đã thử: báo cáo khâu (`BAO_CAO_*.md`) và [`BAO_CAO_SO_SANH_PHUONG_AN.md`](BAO_CAO_SO_SANH_PHUONG_AN.md).

**Việc kế tiếp (thứ tự bạn chốt 30/10; 01/11: hội thoại nhiều lượt + câu nhiều nguồn dời sang Phase 9):**
1. ~~Hiện chữ dần (streaming)~~ — **xong, chạy từ 01/11** (merge `a80e12d`).
2. **Đóng gói Phase 1–8 — xong, Phase 8 bạn đóng 14:29 01/11/2026:** lượt đo cuối cùng một commit (Golden 176 + lượt lặp cùng ngày, bộ an toàn 32, câu theo ngày, 22 câu qua API, **bộ kín mới 40 câu**) — **xong 01/11, mọi sàn đạt** (`report_agent/2026-10-31_streaming_spec/do_cuoi_implementation.md`; bộ kín cho thấy số dev lạc quan: Đủ 4,18 ↔ 4,58); B0 xong 01/11 (bạn giữ 10 đoạn); báo cáo so sánh phương án (đã đăng 01/11, thêm phần mới khi xong); bảng giới hạn (mục này).
3. Giao diện mới (yêu cầu phải giữ ở mục 5). Từ nhận xét B0 (đề xuất A, chờ bạn): `[n]` chen trong câu khó đọc ⇒ đổi cách hiển thị nguồn.
4. Phase 9: mở bằng nghiên cứu rộng rồi mới thử nghiệm; gồm **hội thoại nhiều lượt / nhớ lịch sử** và **câu cần nhiều nguồn** (agent tách câu con). Từ nhận xét B0 (đề xuất A, chờ bạn): câu dự trù chi phí theo mức ⇒ để trợ lý hỏi lại người dùng.

## 6. Chạy thử

```bash
# 1) Bật Docker Desktop (Windows) — tắt thì WSL không có lệnh docker, chatbot không tìm được
cd /home/minhhieu/hue_rag && docker compose up -d qdrant     # Qdrant ở 127.0.0.1:6335
# 2) Chạy API
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000
# mở http://127.0.0.1:8000/
```

Lần đầu cần tokenizer / model e5 trong HF cache. **Mọi lệnh chạy từ `backend/`**: API, test, dựng kho
(`cd backend && uv run --env-file ../.env python -m ingestion.full_corpus_pipeline build --candidate e5-small-384` — chỉ khi kho đổi,
theo quy trình trong guide).

**Khi có lỗi, API báo gì:**

| Tình huống | Mã | Ý nghĩa cho người vận hành |
|---|---|---|
| Kho / phiếu build / từ điển BM25 không khớp chỉ mục (lúc khởi động) | 409 `corpus_reingest_required` | Cần dựng lại chỉ mục |
| Qdrant tắt (vd Docker Desktop chưa bật), hoặc model tìm kiếm không nạp được (thiếu HF cache) | 503 `retrieval_unavailable` | Lỗi tạm, sửa môi trường — **không** dựng lại chỉ mục |
| Model sinh lỗi | 502 `generation_unavailable` | Lỗi phía OpenAI |
| Câu trả lời không qua kiểm trích dẫn | 500 `citation_integrity_error` | Hiếm (lượt 30/10: 0 lỗi mới) |

Code: `backend/api/app.py:65-85` (409 / 503 lúc khởi động), `backend/api/routes/chat.py` (502 / 500 khi hỏi).

## Phụ lục — hồ sơ kỹ thuật

- Mã nội bộ: "B1" = việc đưa 10 đoạn + NFC vào chatbot (merge `510e1a8`, 28/10); "B3" = đo trên câu kín (33 câu trong kho); "H8" = giả thuyết
  "từ chối cả câu khi chỉ có một vế" (Phase 7B); "R2" = thử trả lời một phần; "K1" = 100 ứng viên; "K3b-m" = luna chọn 10 / 30; "F2" = lỗi
  bảng giá ngoài top-30 (Phase 6).
- Phiếu build `51fb1ec63cbc` (30/10), từ điển BM25 `c8134c49a648`; ghi `chat_metrics` từ `5100b90` (27/10); kiểm trích dẫn nhận `[Nguồn n]`
  từ `9e6d371` (25/10); API báo đúng mã lỗi từ `1e4acd0` (25/10).
- Spec streaming: `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 5 `00fb57ee01b2` (User duyệt 01/11); code vào `main` merge `a80e12d` (01/11); tổng hợp
  `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
