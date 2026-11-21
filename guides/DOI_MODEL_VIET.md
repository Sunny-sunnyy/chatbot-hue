# Đổi model viết: qua Claude Sonnet 5.5 (Amazon Bedrock) ⇄ về gpt-6-luna (OpenAI)

Viết: 10:12 21/11/2026 (giờ `date`), phiên B. Người đọc: bất kỳ coding agent nào mở phiên sau và được bảo "chuyển về luna" hoặc "chuyển qua Sonnet".
Trang này đủ để làm việc đó mà không phải đọc lại lịch sử. Số đo trong trang lấy từ các lượt gọi thật ngày 21/11/2026; chỗ nào chưa kiểm ghi rõ **[chưa kiểm]**.

Từ dùng:
- **model viết** = model sinh mọi chữ của trợ lý (định tuyến, trả lời, trò chuyện, mục web, viết câu cho lịch, hiểu ý sửa lịch, nhận ảnh).
- **provider** = dòng công tắc trong cấu hình chọn nơi gọi model viết: `openai` (gpt-6-luna) hoặc `bedrock` (Claude Sonnet 5.5 trên Amazon Bedrock).
- **lớp dịch** = file `backend/llm/bedrock_model.py`, đổi qua lại giữa kiểu gọi của OpenAI Agents SDK (bộ khung chạy agent dự án đang dùng) và kiểu gọi gốc của Claude.
- **người chấm** = model chấm điểm câu trả lời trong bộ đo; LUÔN là luna, không đổi theo provider.
- **stream** = chữ chạy dần ra màn hình khi model đang viết; **stream giả** = model viết xong cả câu rồi mới phát chữ một lần.
- **mức suy luận** = model "nghĩ" nhiều hay ít trước khi viết (none / low / medium / high); nghĩ nhiều thì chậm và tốn token hơn.

## 1. Hiện có gì

Hai đường gọi model viết cùng nằm trong code; **một dòng cấu hình** chọn đường nào chạy. Đổi tạm sang Sonnet là quyết định của chủ dự án ngày 21/11/2026,
kèm yêu cầu: nói "chuyển về luna" là về được ngay.

| Thứ | Ở đâu | Ghi chú |
|---|---|---|
| Công tắc | `backend/config/settings.yaml`, mục `full_corpus_generation`, dòng `provider:` | `openai` hoặc `bedrock`. Xem giá trị đang ghi: `grep -n '^  provider:' backend/config/settings.yaml` |
| Đường luna | cùng mục đó: `model: gpt-6-luna`, `api_key_env: OPENAI_API_KEY` | Không bị sửa khi đổi qua Sonnet. Người chấm cũng đọc dòng `model` này. |
| Đường Sonnet | khối con `bedrock:` trong cùng mục: mã model, vùng, `max_tokens`, `reasoning_default`, `creds_file_env` | Chỉ được đọc khi `provider: bedrock`. |
| Lớp dịch | `backend/llm/bedrock_model.py` | Một lớp `BedrockClaudeModel`; không thêm gói nào vào dự án. |
| Chỗ chọn đường | `backend/llm/generator_openai_full_corpus.py`, hàm `from_environment` | Đọc `provider` từ dict cấu hình truyền vào; `bedrock` ⇒ dựng lớp dịch, còn lại ⇒ dựng model OpenAI như trước. |
| Kiểm cấu hình | `backend/core/settings_loader.py`, hàm `validate_phase6_settings` | Giá trị lạ ở `provider` hoặc khối `bedrock` thiếu trường ⇒ server không khởi động, lỗi nêu tên trường. |
| Bảng giá | `backend/llm/pricing.py`, `PRICES_PER_M` | Tiền mỗi lần gọi tính theo model THẬT của lần gọi đó. |
| Người chấm | `backend/evaluation/full_corpus_eval.py`, hàm `run_judge_luna` | Ép `provider: openai` cho riêng người chấm. |
| Test của lớp dịch | `backend/tests/test_bedrock_model.py` | 16 ca, không gọi mạng. |

**Không bị đụng khi đổi provider:** kho, chỉ mục Qdrant, cách tìm (10 đoạn), mọi lời dặn (prompt), mọi cờ ở mục `assistant:`, công cụ của trợ lý, bộ kiểm trích nguồn,
giao diện, bộ đếm token dựng ngữ cảnh, người chấm. Chín loại lời gọi model dùng chung MỘT đối tượng model nên đổi là đổi cả chín, không đổi lẻ được.

**Đường luna giống từng byte so với trước khi có lớp dịch** — một phiên khác đã chụp 10 loại lời gọi gửi OpenAI ở bản trước và bản sau, ra cùng một mã băm [người thứ hai kiểm].

## 2. ĐỔI VỀ luna

1. Sửa dòng công tắc thành `provider: openai` (chỉ chữ `openai` / `bedrock` trên dòng đó; không sửa gì khác):
   ```bash
   cd /home/minhhieu/hue_rag
   grep -n '^  provider:' backend/config/settings.yaml      # phải ra đúng MỘT dòng
   # sửa chữ bedrock thành openai trên dòng đó bằng trình soạn thảo, rồi xem lại:
   grep -n '^  provider:' backend/config/settings.yaml      # ⇒ "  provider: openai   # …"
   ```
2. Chạy ba file test chạm công tắc, MỖI file hai lần (có và không nạp `.env`), từ `backend/`:
   ```bash
   cd /home/minhhieu/hue_rag/backend
   for f in test_bedrock_model test_phase6_settings test_openai_full_corpus_generator; do
     uv run --env-file /home/minhhieu/hue_rag/.env pytest tests/$f.py -q | tail -1     # CÓ khoá
     uv run pytest tests/$f.py -q | tail -1                                            # KHÔNG khoá
   done
   ```
   Kết quả phải ra [máy kiểm 21/11/2026, cả khi dòng công tắc là `openai` lẫn `bedrock`]:

   | File | CÓ nạp `.env` | KHÔNG nạp `.env` |
   |---|---|---|
   | `test_bedrock_model` | 16 đạt | 16 đạt |
   | `test_phase6_settings` | 5 đạt | 4 đạt, **1 hỏng**: `test_openai_api_key_exists_without_leaking` |
   | `test_openai_full_corpus_generator` | 9 đạt | 7 đạt, **2 lỗi**: `test_real_environment_builds_openai_generator`, `test_empty_or_blank_input_rejected_before_network` |

   Ba ca đỏ ở cột phải là **đúng thiết kế**: chúng kiểm rằng máy có khoá OpenAI, không có khoá thì phải đỏ. Bất kỳ ca nào KHÁC đỏ ⇒ dừng, đọc lỗi.
   Bảng này đúng với `provider: bedrock` chỉ khi bản sửa test `p9-b-test-theo-provider` đã ở main (kiểm: `grep -c 'def openai_settings' backend/tests/test_openai_full_corpus_generator.py` ra 1).
   Chưa có bản sửa đó mà công tắc là `bedrock` ⇒ thêm 4 ca đỏ GIẢ (1 ở `test_bedrock_model`, 3 ở `test_openai_full_corpus_generator`): các ca ấy mong model OpenAI từ cấu hình thật.
3. Khởi động lại server (cấu hình chỉ được đọc lúc khởi động) theo `guides/RUNBOOK_BAN_GIAO.md` mục 2. Không cần biến môi trường nào của Bedrock.
4. Một lượt thật để chắc model đang chạy đúng là luna:
   ```bash
   curl -s http://127.0.0.1:8010/health                       # ⇒ "generator":"ready"
   curl -s -X POST http://127.0.0.1:8010/api/chat -H 'Content-Type: application/json' \
        -d '{"query":"Giá vé tham quan Đại Nội Huế là bao nhiêu?"}' | head -c 300
   grep chat_metrics backend/logs/application.log | tail -1 | grep -o '"model": "[^"]*"'
   ```
   Dòng cuối phải in `"model": "gpt-6-luna"`. (Trường `model` trong dòng log này đã thấy thật ở lượt chạy Sonnet 21/11; lệnh `curl` tới `/api/chat` ở trên
   **[chưa chạy lại]** trong ngày viết trang.)
5. Ghi một dòng vào `session_prompt/HIEN_TRANG.md` mục 1 (model viết đang là gì) và `bai_hoc/` nếu người dùng thấy khác.

Về luna KHÔNG cần: sửa code, xoá khối `bedrock:`, xoá file lớp dịch, dựng lại chỉ mục, dựng lại giao diện.

## 3. ĐỔI QUA Sonnet 5.5

1. Sửa dòng công tắc thành `provider: bedrock` (như bước 1 mục 2).
2. Chọn mức suy luận mặc định ở `full_corpus_generation.bedrock.reasoning_default`: `none`, `low`, `medium` hoặc `high`. Mức này áp cho lời gọi KHÔNG tự đặt mức
   (định tuyến, trả lời, trò chuyện, mục web, nhận ảnh). Nhóm lịch KHÔNG theo khoá này (sửa 11:04 21/11/2026):
   - viết câu cho lịch và lượt biểu mẫu: tự đặt `low` trong code, giữ `low` — đo 21/11 (4 kiểu lịch, mỗi mức một lần): ba mức cho cùng kết quả, Sonnet không dùng token suy luận nào cho việc này;
   - hiểu ý sửa lịch (hai agent): theo khoá RIÊNG `full_corpus_generation.bedrock.reasoning_sua_lich`, đang để `high` — đo 21/11 trên 9 lệnh × 3 lượt: lệnh rõ ràng bốn nhánh
     ngang nhau (17–18 / 18); hai lệnh khó (mơ hồ · bị luật xếp lịch chặn) đúng 5 / 6 ở high, 2 / 6 ở low, 0 / 6 ở medium (luna 6 / 6). Đường luna không đọc khoá này (vẫn `low`).
   Giá trị `reasoning_default` đang ghi trong repo là giá trị TẠM; giá trị chốt chọn theo mục 7.
3. Đặt biến môi trường `HUE_BEDROCK_CREDS_FILE` trỏ tới file khoá tạm của Bedrock **lúc bật server** (đặt trước lệnh `uv run`, như `HF_HUB_OFFLINE=1`).
   Trang này và repo chỉ ghi TÊN biến; đường dẫn file khoá hỏi chủ dự án hoặc xem bản giao việc riêng tư ghi ở `session_prompt/VIEC_DANG_MO.md`. File khoá là JSON có
   `accessKeyId`, `secretAccessKey`, `sessionToken`; code đọc lại file ở MỖI lời gọi nên khoá được làm mới bên ngoài thì không phải khởi động lại. Không in, không chép, không commit file này.
   Thiếu biến ⇒ `from_environment` báo lỗi nêu tên biến [máy kiểm bằng test]; server khi đó khởi động với generator không sẵn sàng, `/health` không báo `generator` là `ready` [đọc code, chưa chạy]. Đường Sonnet không cần khoá OpenAI để trả lời (bộ đo vẫn cần, cho người chấm).
4. Chạy ba file test như bước 2 mục 2 — kết quả phải đúng bảng ở đó (bảng đã đo với cả hai giá trị của công tắc).
5. Khởi động lại server, rồi một lượt thật như bước 4 mục 2; dòng cuối phải in `"model": "global.anthropic.claude-sonnet-5-5"`.
6. Ghi `HIEN_TRANG.md` mục 1.

Lưu ý khi chạy test dựng cả app với `provider: bedrock` **[chưa kiểm]**: khoảng 15 file test bật cả app. Không đặt `HUE_BEDROCK_CREDS_FILE` thì generator của app không
sẵn sàng (giống thiếu khoá OpenAI hôm nay); file nào gọi model thật (ví dụ `test_api_chat` khi nạp khoá) sẽ gọi Sonnet thay cho luna, tốn tiền Bedrock. Nhóm này chưa
được chạy với `bedrock` — chạy ở lượt "cả bộ test" của mốc, trên đúng cấu hình sẽ dùng.

Lỗi hay gặp:

| Thấy gì | Nghĩa là | Làm gì |
|---|---|---|
| Lời lỗi có chữ "khoá Bedrock" (HTTP 403) | khoá tạm hết hạn hoặc không có quyền | báo chủ dự án làm mới file khoá; không sửa code |
| "Không đọc được file khoá Bedrock" | biến trỏ sai chỗ, file thiếu trường, file hỏng | kiểm biến môi trường; lời lỗi cố ý chỉ nêu tên loại lỗi, không nêu đường dẫn |
| "Bedrock HTTP 400 …" | Bedrock từ chối thân yêu cầu | xem bảng mục 4 — gần như luôn là một trường Claude không nhận |
| "Bedrock request failed: ReadTimeout" | lời gọi quá `timeout_seconds` (45 giây) | xem mức suy luận; lời gọi dài nhất đã thấy là 11,6 giây ở mức `low` |

Mọi lỗi trên đều được xếp vào nhóm "không tạo được câu trả lời" ở cả đường thường lẫn đường stream; lịch trình vẫn hiện bằng câu dự phòng khi lần viết câu hỏng.

## 4. luna gửi gì ⇄ Claude cần gì (đã đo thật 21/11/2026)

Nơi gọi: `POST https://bedrock-runtime.<vùng>.amazonaws.com/model/<mã model>/invoke`, thân kiểu Anthropic Messages kèm `"anthropic_version": "bedrock-2023-05-31"`,
không có trường `model` trong thân. Yêu cầu được ký AWS SigV4 (tên dịch vụ `bedrock`) bằng `hmac` + `hashlib` của thư viện chuẩn.

| Việc | Đường luna (OpenAI Responses) | Claude trên Bedrock | Lớp dịch làm gì |
|---|---|---|---|
| Đổi nơi gọi bằng `base_url` | — | cổng kiểu OpenAI của Bedrock trả **404** cho model này | vì vậy phải có lớp dịch, không đổi `base_url` suông được |
| Trần token đầu ra | không gửi (chủ dự án: không đặt trần) | `max_tokens` là trường **bắt buộc** | luôn gửi `128000` (mức tối đa của model, đã đo 200) lấy từ cấu hình; `max_tokens` của agent bị bỏ qua, không hạ được |
| Mức suy luận | chỉ nhóm lịch gửi `reasoning.effort: low`; lời gọi khác không gửi (đường Sonnet: hiểu ý sửa lịch gửi `reasoning_sua_lich`) | không gửi gì thì model tự suy luận cỡ "high" (687 token suy luận ở một câu thử) | luôn gửi rõ: `low / medium / high` ⇒ `"thinking": {"type": "adaptive"}` + `output_config.effort`; `none` ⇒ `"thinking": {"type": "between_tools"}`, không gửi effort |
| Tắt hẳn suy luận | — | `effort: "none"` / `"minimal"` ⇒ 400; `thinking: disabled` ⇒ 400 | dùng `between_tools` (đo: 0 token suy luận 6 / 6 lần, kể cả lượt có công cụ) |
| Khuôn đầu ra (JSON) | `text.format` json_schema strict | `output_config.format` json_schema; khuôn có `maxItems`, `minimum`, `maximum` ⇒ **400** | gỡ các từ khoá ràng buộc (`maxItems`, `minItems`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `minLength`, `maxLength`, `pattern`, `default`) khỏi khuôn GỬI ĐI; pydantic phía mình vẫn kiểm đủ ràng buộc khi nhận về. Tên trường trùng từ khoá không bị gỡ. |
| Công cụ | `tools` kiểu function | `tools` với `name`, `description`, `input_schema`, `strict` | dịch thẳng; khuôn tham số cũng được gỡ ràng buộc |
| Ép gọi công cụ | `tool_choice` tuỳ ý | chỉ nhận `auto` / `none`; ép một công cụ ⇒ 400 | không ép. `parallel_tool_calls=False` ⇒ `{"type": "auto", "disable_parallel_tool_use": true}` |
| Lịch sử + vòng công cụ | các mục `function_call`, `function_call_output` rời | `tool_use` nằm trong tin assistant, `tool_result` ở tin user ngay sau | gộp các mục liền nhau cùng vai vào một tin; `call_id` = `id` của `tool_use` |
| Khối suy luận giữa các vòng công cụ | SDK tự giữ | **bỏ** khối suy luận ở lượt kế vẫn 200 (4 / 4 cách thử) | bỏ luôn, không cất chữ ký |
| Ảnh | `input_image` dạng data URL | khối `image` với `source.type: base64` | tách kiểu ảnh + dữ liệu từ data URL |
| Stream | stream thật, chữ chạy dần | `invoke-with-response-stream` ⇒ **403**: bộ khoá đang dùng không có quyền | stream giả: gọi trọn, phát MỘT mảnh chữ rồi sự kiện kết thúc; lượt model xin công cụ không phát chữ |
| Nhiệt độ / top_p | không gửi | không gửi | không gửi |
| `store`, `prompt_cache_key`, `include_usage` | có | không có nghĩa | bỏ qua |
| Đệm lời dặn (prompt caching) | OpenAI tự đệm | phải tự đánh dấu chỗ đệm | **chưa bật** ⇒ token đệm luôn 0, mỗi lời gọi trả giá đủ |
| Đếm token vào | `input_tokens` đã GỒM phần đọc / ghi đệm | `input_tokens` KHÔNG gồm phần đệm (`cache_read_input_tokens`, `cache_creation_input_tokens` đứng riêng) | cộng ba phần lại để cùng nghĩa với OpenAI; `cost_usd` trừ phần đệm ra khi tính |
| Token suy luận | `output_tokens_details.reasoning_tokens` | `output_tokens_details.thinking_tokens`; `output_tokens` đã gồm phần này | chép sang `reasoning_tokens` (đã thấy số khác 0: 122 và 483) |
| Giá ghi sổ, USD / triệu token | vào 0,10 · đọc đệm 0,01 · ghi đệm 0,125 · ra 0,50 | vào 2,00 · đọc đệm 0,10 · ghi đệm 2,50 · ra 10,00 (**chưa đối chiếu hoá đơn**) | `PRICES_PER_M` trong `llm/pricing.py` |

Độ trễ đo trực tiếp ở Bedrock (không qua sản phẩm): định tuyến có khuôn 0,8–0,9 giây; trả lời khoảng 6,8 nghìn token vào / 400 ra: 3,5–3,9 giây; lượt suy luận thật + đầu ra
khoảng 2.000 token: 15–20 giây; 0 lần bị giới hạn tần suất (429) trong 46 lời gọi.

## 5. Người dùng thấy gì khác khi chạy Sonnet

Đo ở một lượt thật qua giao diện ngày 21/11/2026: 14 lượt, 14 thành công, mức suy luận mặc định `low` [máy kiểm; một phiên khác đếm lại từ log ra cùng số].

| Loại lượt | Thời gian chờ |
|---|---|
| Hỏi thường có nguồn | 3,7 giây |
| Hỏi tiếp (model tự tìm kho thêm 2 lần) | 5,7 giây |
| Xin danh sách | 5,0 giây |
| Câu có thêm mục "Từ web" | 11,5 giây |
| Lên lịch 3 ngày bằng biểu mẫu | 9,1–9,3 giây |
| Sửa lịch (hiểu ý + code áp) | 1,6–2,9 giây |
| Hỏi về lịch đang có | 11,6 giây (lời gọi dài nhất của cả lượt đo) |
| Hỏi bằng ảnh | nhận tên 1,2–1,7 giây; cả lượt 11,3 giây |

- **Chữ hiện MỘT lần** sau khi model viết xong, không chạy dần như luna: người dùng chờ hết thời gian ở bảng rồi thấy cả câu.
- **Tiền mỗi câu:** một câu trả lời có nguồn khoảng 0,018 USD trên Sonnet, cùng loại câu trên luna khoảng 0,0007 USD (khoảng 25 lần). Lượt hỏi tiếp có model tự tìm thêm: 0,048 USD.
- Hạn giờ mỗi lượt vẫn là 45 giây; chưa lượt nào tới 35 giây.

Giới hạn đã đo của Sonnet ở nhóm lịch (21/11, chưa sửa — sửa cần đổi lời dặn và đo lại):
- Lệnh sửa lịch MƠ HỒ ("ngày 2 hơi nặng, làm nhẹ bớt"): Sonnet hay TỰ bỏ một điểm người dùng không nêu — low 3 / 3 lần, medium 3 / 3, high 3 / 6 (ba lần còn lại đổi kiểu đi sang "nhẹ nhàng");
  luna 3 / 3 giữ nguyên lịch và bảo người dùng nói cụ thể.
- Câu mô tả điểm trong lịch: Sonnet chép nhiều chi tiết hơn luna và không lấy gì ngoài đoạn nguồn (đối chiếu 17 câu: 0 chi tiết bịa), nhưng có thể GỘP ý làm đổi nghĩa — một câu đã viết
  tháp Phước Duyên, chuông và bia "đều là Bảo vật quốc gia" trong khi nguồn chỉ ghi chuông và bia. Bộ kiểm câu của code không bắt được loại lỗi này.

Chưa thử qua giao diện với Sonnet: lịch 1 ngày / kiểu gấp / nhiều sở thích · ảnh ra 2–3 tên · câu bão lũ · màn hẹp điện thoại · hai người hỏi cùng lúc ·
khoá hết hạn giữa một lượt · cả bộ test với `provider: bedrock`.

## 6. Muốn thêm một model / nhà cung cấp khác

- **Model khác của cùng nhà cung cấp:** Claude khác trên Bedrock ⇒ sửa `bedrock.model` (và `region` nếu cần) trong `settings.yaml`, thêm giá vào `PRICES_PER_M` nếu giá khác;
  model OpenAI khác ⇒ dòng `model` đang bị `settings_loader.py` khoá cứng là `gpt-6-luna` (người chấm đọc dòng này) — đổi là một quyết định có đo, không phải sửa cấu hình.
- **Nhà cung cấp mới:** bốn chỗ, theo đúng mẫu của Bedrock:
  1. Một file lớp `Model` của Agents SDK trong `backend/llm/` (hai hàm `get_response`, `stream_response`; thêm thuộc tính `provider = "<tên>"`). Đường stream chỉ BẮT BUỘC phát
     một sự kiện `response.completed` mang `Response` đủ `output` + `usage`; muốn có chữ trên giao diện thì phát thêm `response.output_text.delta` trước đó. Mọi lỗi của lớp
     phải là `GenerationError` (hoặc lớp con), không thì đường stream không nhận ra lỗi model.
  2. Một nhánh trong `OpenAIFullCorpusGenerator.from_environment` dựng lớp đó khi `provider` mang tên mới.
  3. Tên mới + khối cấu hình của nó trong `validate_phase6_settings` (`core/settings_loader.py`) và `settings.yaml`.
  4. Một dòng giá trong `PRICES_PER_M` (`llm/pricing.py`), khoá là đúng tên `provider`.
- Trước khi viết: đo thật năm thứ đã làm đổi thiết kế lần này — khuôn JSON có ràng buộc, ép `tool_choice`, quyền stream, cách tắt suy luận, cách đếm token đệm.
- Sau khi viết: file test riêng như `test_bedrock_model.py`, một lượt thật qua giao diện, rồi mới tới lượt đo chất lượng. Người chấm giữ nguyên luna để điểm so được với mốc cũ.

## 7. Chất lượng trả lời so với luna, và mức suy luận nên dùng

**Điền sau lượt đo** (phiên đo đang chạy: bộ câu mẫu 176 câu, bộ an toàn 32 câu, bộ bẫy và chuỗi hội thoại; người chấm luna; so bốn mức suy luận). Chưa có số nào — không suy ra
từ các lượt chạy thử ở mục 5, vì các lượt đó chỉ chứng minh đường chạy được.

| Cần điền | Giá trị |
|---|---|
| Sàn "0 câu ngoài kho được trả lời bằng kho" | — |
| Bộ an toàn 32 câu | — |
| Đúng / Đủ ý / Trọng tâm so với mốc luna (nhiễu giữa hai lượt giống nhau: 1 · 2 · 7) | — |
| Mức suy luận được chọn và lý do | — |
| Quyết định của chủ dự án (giữ Sonnet / về luna) + ngày | — |

## 8. Hồ sơ

- Report phần code (bảng bằng chứng, chỗ lệch thiết kế, vòng review): `report_agent/2026-11-21/b_bedrock_sonnet.md`.
- Việc đang mở và bước kế: `session_prompt/VIEC_DANG_MO.md` khối 0a.
- Script và log các lượt gọi thật: thư mục lượt thử Bedrock ngày 21/11/2026 trong `data/` (riêng tư, không vào git).
