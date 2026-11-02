# C126 — ước lợi của thí nghiệm `prompt_cache_key` / đệm prompt (trước khi A quyết)

Người làm: C (Claude Opus 5.5, `hue-rag-cc`) · 19:13 02/11/2026 (`date`) · 0 USD · chỉ đọc + phân tích, không sửa code.
Nguồn của việc: review plan B0 C124 phát hiện SDK 0.19.4 gán `prompt_cache_key = agents-sdk:run:<ngẫu nhiên>` mỗi lần chạy; A ghi giả thuyết "đây là lý do `cached_tokens` = 0".

## Kết luận ngắn

- **Giả thuyết "khoá đổi mỗi lần ⇒ không đọc được đệm" gần như không đúng là nguyên nhân chính.** Dù có khoá cố định, các câu khác nhau cũng **không thể** dùng chung đệm.
  - Phần đầu giống nhau giữa các câu (lời dặn hệ thống) chỉ ≈ 148 token, dưới ngưỡng 1.024 token của OpenAI.
  - Tin nhắn người dùng bắt đầu bằng **câu hỏi** (`full_corpus_prompt.py:20`), nên phần chung chấm dứt ngay sau lời dặn.
  - ⇒ Đặt khoá cố định: lợi cho câu khác nhau **≈ 0**. Chỉ câu **giống hệt** lặp lại trong 30 phút mới có thể đọc đệm, và cả điều đó cũng chưa chắc.
- **Lợi thật duy nhất đo được: bỏ "phí ghi đệm".** Hôm nay ≈ 95 % token vào bị tính giá ghi đệm 0,125 thay vì giá thường 0,10 USD / 1M.
  - Tắt ghi đệm ⇒ **0,0003073 ⇒ 0,0002664 USD / câu (−0,000041 USD, −13,3 %)**, tức ≈ 0,04 USD / 1.000 câu.
  - Theo thiết kế của OpenAI, đệm chỉ đổi giá, không đổi chữ trả lời; nên rủi ro chất lượng **≈ 0 (chưa đo)**.
- Trần lý thuyết là −61 %, nếu mọi token ghi đệm thành đọc đệm. Mức này **không đạt được** với cấu trúc prompt hiện tại (lý do ở trên).

## 1. Hiện trạng từ log (chỉ dòng `chat_metrics`, không có chữ người dùng)

Script: `data/phase_9/c126_cache/phan_tich_log.py`; kết quả: `phan_tich_log.json` (private).
Có 110 dòng `chat_metrics`. Trong đó **44 dòng** có token và có trường đệm (sau 30/10); 17 / 44 là câu từ chối (vẫn gọi model).
Giá dùng để tính là giá `gpt-6-luna` (User 30/10): vào 0,10 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 · ra 0,50 USD / 1M.

| Chỉ số (mỗi lần gọi) | p50 | p95 | max | TB |
|---|---:|---:|---:|---:|
| token vào | 1.671 | 2.373 | 2.940 | 1.680,8 |
| token ghi đệm | 1.668 | 2.370 | 2.937 | 1.635,7 |
| token đọc đệm | 0 | 0 | 0 | 0 (0 / 44 dòng > 0) |
| token ra | 159 | 531 | 666 | 196,7 |

- Ghi đệm chiếm trung bình **95,3 %** token vào. Đọc đệm = 0 ở mọi dòng.
- USD / câu hiện tại: TB **0,0003073**, p50 0,000304, p95 0,000438. Phần token vào chiếm 68 % tiền.
- **Phần đắt thêm do ghi đệm** (0,125 so với 0,10) = **13,3 %** tiền mỗi câu.
- Giới hạn: 44 dòng là một mẫu nhỏ và trộn nhiều lượt thử (cổng ổn định, bước 0 khẩn cấp…). Các lượt đo lớn hơn (bộ đánh giá) không ghi vào `chat_metrics`. Dù vậy, tỉ lệ ghi đệm ≈ toàn bộ khớp với B95 (30/10).

## 2. Phần đầu giống nhau giữa các câu

- **Lời dặn hệ thống** `ANSWER_SYSTEM_INSTRUCTIONS`: 545 ký tự ≈ **148 token**.
  - Cách ước: đếm bằng `tiktoken` `o200k_base`. Bộ tách token của `gpt-6-luna` không công khai, nên đây chỉ là ước. Cùng bậc độ lớn là đủ, vì còn xa ngưỡng.
  - Kiểm chéo bằng log: câu ngắn nhất có **841** token vào (lời dặn + câu hỏi + ít nhất 1 đoạn kho), cũng dưới 1.024.
- **Thứ tự trong tin nhắn người dùng:** `Câu hỏi:\n{câu hỏi}\n\nNgữ cảnh truy xuất:\n{10 đoạn}` (`backend/llm/full_corpus_prompt.py:20`). Câu hỏi đứng trước nên phần chung dừng ngay sau lời dặn. Ngữ cảnh cũng đổi theo câu.
- **Ngưỡng OpenAI** (trang chính thức, mục 3): GPT-5.6 trở đi cần **≥ 1.024 token đầu vào nhìn thấy được** cho phần đầu được đệm. Khi không đặt mốc, OpenAI tự đặt mốc ở **cuối tin nhắn người dùng mới nhất**. Lần tra cũng xét tối đa 20 mốc cuối tin nhắn trước đó và cuối khối developer đầu tiên.
  - ⇒ Với một tin nhắn hệ thống ngắn + một tin nhắn người dùng, mốc duy nhất là **cuối cả prompt**. Mỗi câu ghi đệm gần hết phần vào (khớp 95 %), và chỉ prompt **giống hệt từng chữ** mới đọc lại được.

## 3. Tài liệu công khai (Codex tra + C tự WebFetch kiểm)

- Codex: `data/tra_cuu_cli/2026-11-02_c126-prompt-cache/` (90 s, 9 lượt tìm, **2 trang thật sự mở** — chỉ là mã SDK trên GitHub, không phải trang tài liệu). Phần trích từ trang tài liệu OpenAI trong kết quả là **tự khai** ⇒ C WebFetch kiểm lại.
- C **WebFetch** `https://developers.openai.com/api/docs/guides/prompt-caching` (2 lần, 02/11/2026; trang không ghi ngày cập nhật). Khớp với kết quả Codex:
  - ngưỡng: "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later";
  - `prompt_cache_key` ở GPT-5.6+: "the key is not needed to optimize caching". Khoá dùng để "maintain separate cache accounting" và "help prevent cache-hit probing across users". Như vậy khoá khác nhau **có vẻ** tách đệm, nhưng trang **không hứa** chặt chẽ;
  - giá ghi: "1.25× the standard, uncached input-token rate for the default 30-minute lifetime"; 12 giờ = 2,5×; "These are total write rates, not surcharges"; đọc 0,1×. Khớp đúng giá User đưa: 0,125 / 0,10 = 1,25 và 0,01 / 0,10 = 0,1. ⇒ `gpt-6-luna` nằm trong nhóm GPT-5.6+ (suy ra từ giá; trang có ví dụ `gpt-6.1-sol` trong nhóm này);
  - tắt ghi: `prompt_cache_options.mode = "explicit"` mà không đặt mốc nào ⇒ "the request does not use prompt caching or create cache writes";
  - đọc đệm cần "the entire rendered prefix to match", cùng tổ chức, entry còn hạn.
- **SDK 0.19.4** (C đọc mã đã cài trong `.venv`, cùng tag Codex mở):
  - `ModelSettings.prompt_cache_options` có sẵn (`agents/model_settings.py:197`), được chuyển vào `responses.create` (`agents/models/openai_responses.py:891`);
  - khoá tự sinh bị bỏ qua khi `ModelSettings.extra_args` đã có `prompt_cache_key` (`agents/run_internal/prompt_cache_key.py:102`).

## 4. Các cách làm (chưa làm — mỗi cách là đổi chuỗi gửi model ⇒ thí nghiệm riêng sau B0, `run-experiment`)

| Cách | Đổi gì | Lợi ước (USD / câu) | Rủi ro chất lượng | Khi nào sai |
|---|---|---|---|---|
| **A. Tắt ghi đệm** | `ModelSettings(prompt_cache_options={"mode": "explicit"})`, không đặt mốc nào | **−0,000041 (−13,3 %)**: token ghi đệm tính giá thường | ≈ 0, vì đệm không đổi chữ trả lời (theo thiết kế; chưa đo) | OpenAI đổi giá / chính sách đệm; hoặc sau này có nhiều câu lặp giống hệt (mất phần đọc đệm, hôm nay = 0) |
| **B. Khoá cố định** | `ModelSettings(extra_args={"prompt_cache_key": "<cố định>"})` | câu khác nhau: **≈ 0** (phần chung < 1.024 token). Câu giống hệt trong 30 phút: có thể đọc đệm (−90 % phần vào của câu đó), nhưng chưa chắc vì trang không hứa | ≈ 0 | — |
| **C. Không làm gì** | — | 0 | 0 | — |

Hai cách khác C đã xét và **không** khuyên:
- Đưa ngữ cảnh lên trước câu hỏi, hoặc kéo dài lời dặn cho đủ 1.024 token: ngữ cảnh vẫn đổi theo câu, nên lợi ≈ 0. Kéo dài lời dặn lại tốn thêm token và đổi hành vi.
- Đệm 12 giờ: giá ghi 2,5×, đắt hơn nữa.

**Ghi cho bậc sau (không phải việc hôm nay):**
- **B3 (nhớ hội thoại):** lượt sau của **cùng một cuộc trò chuyện** có phần đầu giống lượt trước (lời dặn + lịch sử). Khi lịch sử dài ≥ 1.024 token, đệm mới thật sự có ích.
  - Lúc đó khoá **mỗi lần chạy một khoá** có thể chặn việc đọc lại giữa các lượt.
  - SDK có sẵn khoá theo phiên / nhóm (`_hashed_key`, `prompt_cache_key.py:118-130`), nên plan B3 nên xét luôn.
- **B1** thêm lần gọi định tuyến (prompt ngắn, cũng < 1.024) ⇒ cách A áp dụng như nhau.

## 5. Ý kiến cho A quyết

- Lợi lớn nhất có thể đo được là **13,3 % tiền mỗi câu (≈ 0,00004 USD)**. Hôm nay đã dưới sàn 0,0005 USD / câu, và User chốt "chất lượng trước, tiền chỉ theo dõi".
- ⇒ **Khuyên: không mở thí nghiệm riêng bây giờ.** Ghi cách A thành một dòng "tối ưu tiền sau khi Phase 9 ổn" (tức một lần đổi `ModelSettings` + đo lại tiền trên vài câu). Khoá đệm thì xét lại ở plan B3.
- Nếu A vẫn muốn làm cách A: chỉ đổi tiền, không đổi chữ. Cách đo đủ gọn là ~10 câu × 2 lượt so tiền / token trong log, cùng đối chiếu chữ trả lời không lệch hơn A/A thường (≈ 0,006 USD).

## 6. Giới hạn

- Token lời dặn đếm bằng `o200k_base`, không phải bộ tách token của `gpt-6-luna` (không công khai).
- Mẫu log 44 dòng.
- "Khoá khác nhau thì tách đệm" ở GPT-5.6+ chỉ là ngụ ý của trang, chưa thử.
- "Đệm không đổi chữ trả lời" chưa đo trên hệ thống này.
- `gpt-6-luna` thuộc nhóm GPT-5.6+: suy ra từ bảng giá khớp hệ số, chưa có câu trực tiếp trên trang.
