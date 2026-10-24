# Phase 7A2 survey: OpenRouter `qwen/qwen3-embedding-8b`

Implementer: Claude Opus 5.5
Date: 2026-10-23
Handoff: `session_prompt/CURRENT_HANDOFF.md` (next_design, base `8b7b76d`)
Loại: khảo sát hỗ trợ thiết kế; không sửa runtime, không ghi Qdrant, không sửa
corpus, không commit.

## 1. Phạm vi

Lấy số liệu thật để Reviewer viết spec Phase 7A2. Mỗi câu hỏi 1–6 của handoff
được trả lời ở mục 4. Đã dùng **8/10** embedding call (1 lỗi 429, 7 thành công)
và 2 GET metadata miễn phí. Data egress: đúng **64 chunk** duy nhất. Call 128
input chỉ là 64 chunk đó gửi lặp hai lần, không có chunk mới. Mọi call đều gửi
`provider.data_collection: "deny"`.

## 2. Thay đổi chính

- Tạo report này.
- Script tạm `/tmp/phase7a2_survey/survey.py` (ngoài repo, không commit) và số
  liệu tổng hợp `/tmp/phase7a2_survey/results.json`. Không lưu vector hay raw
  payload.
- Không đụng `backend/`, Qdrant, `knowledge-base-hue/`.

## 3. Cách đã chạy thật

```bash
# GET metadata miễn phí
GET https://openrouter.ai/api/v1/models/qwen/qwen3-embedding-8b/endpoints
GET https://openrouter.ai/api/v1/embeddings/models
# Embedding calls (POST /api/v1/embeddings, httpx, timeout 180 s, không retry)
PYTHONPATH=. uv run --env-file .env python /tmp/phase7a2_survey/survey.py
```

Script được chạy hai lần. Lần 1 dừng ở call 1 (429, xem mục 4.6). Lần 2 sửa
provider pin chính sang Nebius và chạy call 2–8. Bộ đếm call được nối tiếp từ
lần 1 nên tổng không vượt 10.

Input lấy từ chunker hiện hành: `chunk_full_corpus(load_settings())` cho ra
8.460 chunk, không có chunking error. Text gửi đi là `search_text`, tức
Representation A, đúng contract document `qwen3` trong
`backend/embedding/full_corpus.py`: document giữ nguyên, không instruction.

Cách chọn mẫu: chunk sort theo `chunk_id` trong từng domain, rồi lấy cách đều
theo quota.

| Domain | Chunk trong corpus | Mẫu |
|---|---:|---:|
| festivals | 1.130 | 13 |
| foods | 1.670 | 13 |
| heritages | 1.614 | 13 |
| performing_arts | 724 | 13 |
| travel | 3.322 | 12 (10 places, 1 services, 1 tickets) |

64 chunk thuộc 64 file khác nhau. Độ dài từ 55 đến 638 ký tự, tổng 18.601 ký
tự. Danh sách `chunk_id` (source path + ordinal) nằm ở Phụ lục.

## 4. Kết quả quan sát

### Bảng call

| # | Mục đích | Provider request | HTTP | Provider phục vụ | Input | Vector × dim | `index` đúng thứ tự | prompt_tokens | cost (USD) | Latency |
|---:|---|---|---:|---|---:|---|---|---:|---:|---:|
| 1 | batch 64 | `order:[deepinfra]` | **429** | — | 64 | — | — | — | — | 1,49 s |
| 2 | batch 64 lần 1 | `order:[nebius]` | 200 | Nebius | 64 | 64 × 4096 | có | 5.905 | 5,905e-5 | 9,01 s |
| 3 | batch 64 lần 2 | `order:[nebius]` | 200 | Nebius | 64 | 64 × 4096 | có | 5.905 | 5,905e-5 | 6,46 s |
| 4 | query Instruct | `order:[nebius]` | 200 | Nebius | 1 | 1 × 4096 | có | 53 | 5,3e-7 | 10,54 s |
| 5 | `dimensions: 1024` | `order:[nebius]` | 200 | Nebius | 4 | 4 × **1024** | có | 419 | 4,19e-6 | 2,16 s |
| 6 | 128 input (64 × 2) | `order:[nebius]` | 200 | Nebius | 128 | 128 × 4096 | có | 11.810 | 1,181e-4 | 18,05 s |
| 7 | không pin order | chỉ `data_collection` | 200 | **Nebius** | 4 | 4 × 4096 | có | 419 | 4,19e-6 | 9,36 s |
| 8 | so chéo provider | `order:[siliconflow]` | 200 | SiliconFlow | 64 | 64 × 4096 | có | 5.905 | 2,362e-4 | 6,10 s |

Call 1–6 và 8 cùng gửi `allow_fallbacks: false`. Mọi call gửi
`data_collection: "deny"` và `encoding_format: "float"`. Tổng cost OpenRouter
báo trong `usage.cost` của các call thành công là **4,81e-4 USD**.

### 4.1 Provider và pin

- Endpoint listing có 3 provider:

  | Provider | Tag | Quantization | context_length | Giá prompt/token | p50 30 phút |
  |---|---|---|---:|---:|---:|
  | Nebius | `nebius` | unknown | 40.960 | 1e-8 | 1.454,5 ms |
  | DeepInfra | `deepinfra/us` | unknown | 32.768 | 1e-8 | 922 ms |
  | SiliconFlow | `siliconflow/fp8` | fp8 | 32.768 | 4e-8 | 1.521,5 ms |

  Cả ba có `supported_parameters: []`. Listing không ghi data policy theo
  provider.
- Pin bằng `order: [<slug>]` + `allow_fallbacks: false` +
  `data_collection: "deny"` được chấp nhận với cả `nebius` và `siliconflow`.
  Cả hai trả 200 và đúng provider đã pin. Với `deepinfra`, request được định
  tuyến tới DeepInfra nhưng provider trả lỗi 429 (mục 4.6). Request không bị
  âm thầm chuyển sang provider khác.
- Response body có field top-level `provider` ghi provider đã phục vụ (`Nebius`
  / `SiliconFlow`). Các field top-level là `data, id, model, object, provider,
  usage`. `model` trả `Qwen/Qwen3-Embedding-8B`. Trong header không có
  `x-*`/`openrouter*` nào ngoài `x-content-type-options`, nên provider chỉ đọc
  được từ body.
- Không pin order, chỉ gửi `data_collection: "deny"` (call 7): OpenRouter chọn
  Nebius, nhưng chỉ quan sát được một lần.

### 4.2 Số chiều và `dimensions`

- Số chiều gốc là **4096**. Mọi vector có L2 norm = 1,0 (min = max = 1,000000),
  tức provider đã normalize sẵn.
- `dimensions: 1024` được chấp nhận và có tác dụng: trả 4 vector 1024 chiều,
  norm 1,0. Cosine giữa các vector đó và 1024 chiều đầu của vector 4096 tương
  ứng ở call 2 (sau khi renormalize): min = mean = max = **1,00000000** (làm
  tròn 8 chữ số). Kết quả khớp với cắt prefix rồi renormalize (MRL). Chỉ thử
  trên Nebius, với một giá trị là 1024.

### 4.3 Batch 64 / 128

- Batch 64: đủ 64 vector, `index` 0..63 đúng thứ tự, 5.905 prompt tokens (trung
  bình ≈ 92 token/chunk). Latency 9,01 s, 6,46 s (Nebius) và 6,10 s
  (SiliconFlow).
- Batch 128: đủ 128 vector, `index` đúng thứ tự, 11.810 tokens (đúng 2 ×
  5.905), 18,05 s. **Chưa chạm giới hạn mỗi request**. Không thử lớn hơn 128 vì
  giới hạn egress 64 chunk và để dư call.

### 4.4 Độ ổn định (gửi lại đúng batch)

| So sánh | cos min | cos mean | cos max |
|---|---:|---:|---:|
| Nebius batch 64 lần 1 vs lần 2 (call 2 vs 3) | 1,00000000 | 1,00000000 | 1,00000000 |
| Trong call 6: nửa sau vs nửa đầu (cùng text, cùng request) | 1,00000000 | 1,00000000 | 1,00000000 |
| Call 6 nửa đầu (batch 128) vs call 2 (batch 64) | 0,99988714 | 0,99992722 | 0,99995580 |
| Call 7 (batch 4, không pin) vs call 2 (4 chunk tương ứng) | 0,99990499 | 0,99991955 | 0,99993083 |
| SiliconFlow fp8 (call 8) vs Nebius (call 2) | 0,99985297 | 0,99990844 | 0,99993772 |

- Call 2 và call 3 có cosine 1,0 khi làm tròn 8 chữ số nhưng **không
  bit-identical** (`np.array_equal` = False).
- Cùng provider nhưng khác kích thước batch thì vector lệch nhẹ (cos ≥
  0,99988). Khác provider (Nebius vs SiliconFlow fp8) thì cos ≥ 0,99985.

### 4.5 Query có prefix Instruct

Định dạng `Instruct: {QWEN_QUERY_TASK}\nQuery: {query}`, với `QWEN_QUERY_TASK`
lấy từ `backend/embedding/full_corpus.py`. Query mẫu tự viết, không lấy từ
Golden. Kết quả: 200, 1 vector **4096** chiều (khớp document), 53 tokens. Cosine
query với 64 chunk mẫu nằm trong khoảng 0,106–0,570. Số này chỉ là sanity, không
phải đánh giá retrieval.

### 4.6 Lỗi thật

Call 1 (`order:[deepinfra]`, `allow_fallbacks:false`, 64 input) trả **HTTP
429**, sau 1,49 s. Message:
`HTTP 429: {"error":{"message":"Model busy, retry later","type":"invalid_request_error","param":null,"code":"engine_overloaded"}}`.
Không retry, không fallback tự động. Các call sau không gửi lại request nào tới
DeepInfra.

## 5. Lỗi và giới hạn

- **Sai lệch so với kế hoạch ban đầu của Implementer:** dự định pin DeepInfra
  (p50 thấp nhất). Sau 429, các phép đo chính (câu 2–5) được chạy trên Nebius.
  Handoff không chỉ định provider, nên đây không phải retry cùng request mà là
  chọn provider khác cho phần đo còn lại. Reviewer cần biết DeepInfra **chưa có
  một call thành công** trong khảo sát này.
- Giới hạn input mỗi request chưa xác định: 128 vẫn chạy được.
- `dimensions` chỉ thử một giá trị (1024), một provider (Nebius), 4 input.
- Routing khi không pin chỉ có 1 mẫu (Nebius), không chứng minh là ổn định.
- Ổn định chỉ đo trên Nebius. Ổn định của SiliconFlow chưa đo. Ổn định của
  DeepInfra chưa đo được.
- Latency là số đo đơn lẻ từ máy local, không phải phân phối.
- Không có dữ liệu thời gian chạy hay rate limit cho build 8.460 chunk. Ước
  lượng suy ra (không phải quan sát): ≈ 8.460 × 92 ≈ 780k token, ≈ 0,008 USD theo
  giá Nebius, ≈ 133 request batch 64.
- Data egress: 64 chunk thật đã gửi tới OpenRouter → DeepInfra (bị từ chối
  429), Nebius và SiliconFlow, đều kèm `data_collection: "deny"`. Survey không
  kiểm chứng được việc provider thực sự tuân thủ policy đó.

## 6. Handoff cho Reviewer

- Đọc `full-read` report này. Không có real path nào cần chạy lại cho survey.
- Các điểm có thể cần quyết định trong spec 7A2: provider pin cho build 8B
  (Nebius đã chạy được; DeepInfra bị 429), batch size, có dùng `dimensions` hay
  không, và cách xử lý việc vector phụ thuộc nhẹ vào batch/provider (cos ≥
  0,99985).
- Sub-agent: không dùng.

## Phụ lục: 64 `chunk_id` đã gửi

- `festivals/festival-guides.md#0`
- `festivals/festival/Chợ quê ngày hội – Cầu ngói Thanh Toàn.md#8`
- `festivals/festival/Festival Nghề truyền thống Huế.md#38`
- `festivals/festival/Hội vật làng Thủ Lễ.md#9`
- `festivals/festival/Lễ Ban Sóc triều Nguyễn.md#62`
- `festivals/festival/Lễ hội Cầu ngư.md#12`
- `festivals/festival/Lễ hội Hương xưa làng cổ – Phước Tích.md#9`
- `festivals/festival/Lễ hội Thanh Trà Huế.md#10`
- `festivals/festival/Lễ hội Áo dài Huế.md#20`
- `festivals/festival/Lễ hội Đua ghe truyền thống Huế.md#17`
- `festivals/festival/Lễ hội Ẩm thực Huế.md#17`
- `festivals/festival/Lễ tế Nam Giao.md#32`
- `festivals/festival/Ngày hội Hoàng Mai Huế.md#29`
- `foods/cafes/anh kafe hue.md#0`
- `foods/cafes/cui coffee.md#21`
- `foods/cafes/giao cafe.md#50`
- `foods/cafes/koi the hue.md#7`
- `foods/cafes/momiji coffee tea.md#2`
- `foods/cafes/tan cafe.md#11`
- `foods/cafes/tron studio.md#37`
- `foods/local_specialties/banh ep.md#19`
- `foods/local_specialties/com hen.md#13`
- `foods/restaurants/banh ep 1992.md#1`
- `foods/restaurants/bun bo o nhon.md#2`
- `foods/restaurants/com tam okla.md#6`
- `foods/restaurants/nha hang chay sala.md#2`
- `heritages/heritage-guides.md#0`
- `heritages/heritage/Châu bản triều Nguyễn.md#10`
- `heritages/heritage/Cung An Định.md#22`
- `heritages/heritage/Hải Vân Quan.md#52`
- `heritages/heritage/Hổ Quyền.md#48`
- `heritages/heritage/Lăng Dục Đức.md#9`
- `heritages/heritage/Lăng Minh Mạng.md#36`
- `heritages/heritage/Lăng vua Hiệp Hòa.md#11`
- `heritages/heritage/Nghệ thuật Bài Chòi Trung Bộ.md#15`
- `heritages/heritage/Thơ văn trên kiến trúc cung đình Huế.md#12`
- `heritages/heritage/Trường Quốc Học Huế.md#2`
- `heritages/heritage/Đàn Nam Giao.md#12`
- `heritages/heritage/Đàn Xã Tắc.md#62`
- `performing_arts/arts/Ca Huế trên sông Hương.md#0`
- `performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md#20`
- `performing_arts/arts/Huế Symphony – Bản Giao hưởng Cố đô.md#38`
- `performing_arts/arts/Huế Wonderverse Music Fest.md#30`
- `performing_arts/arts/Huế by Light – The Live Show.md#38`
- `performing_arts/arts/Lễ hội đường phố Sắc màu văn hóa.md#51`
- `performing_arts/arts/Mega Booming – Huế.md#49`
- `performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md#48`
- `performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md#40`
- `performing_arts/arts/Đêm Hoàng cung – Dạ yến Hoàng cung.md#34`
- `performing_arts/arts/Đêm nhạc Trịnh Công Sơn tại Huế.md#20`
- `performing_arts/performing-arts-entities-inventory.md#10`
- `performing_arts/performing_arts_guides.md#31`
- `travel/places/Bãi biển Bình An.md#0`
- `travel/places/Bãi biển Lộc Bình.md#36`
- `travel/places/Chợ An Cựu.md#78`
- `travel/places/Hòn Vượn.md#44`
- `travel/places/Làng du lịch cộng đồng Thác A Nôr.md#69`
- `travel/places/Phá Tam Giang.md#67`
- `travel/places/Suối Mơ.md#68`
- `travel/places/Vườn quốc gia Bạch Mã.md#59`
- `travel/places/Đèo Hải Vân.md#69`
- `travel/places/Đầm Lập An.md#53`
- `travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md#27`
- `travel/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md#111`
