# Đổi tạm model viết sang Claude Sonnet 5.5 trên Amazon Bedrock — phần code (nhánh `p9-b-bedrock-sonnet`)

Viết: 09:55 21/11/2026, sửa 09:56 21/11/2026 sau phần bổ sung thiết kế (giờ `date`), phiên B. Giao việc: `session_prompt/VIEC_DANG_MO.md` khối 0a (bản giao việc đủ ở thư mục riêng tư ghi tại đó).
Trạng thái: **code + test xong, chờ review của phiên C; CHƯA có lượt thật qua giao diện** (cần bật server — xin lượt máy qua phiên điều phối).

Từ dùng: *lớp dịch* = file mới đổi qua lại giữa kiểu gọi của OpenAI Agents SDK và kiểu gọi gốc của Claude · *provider* = dòng công tắc chọn nơi gọi model viết ·
*stream giả* = gọi trọn câu trả lời rồi mới phát chữ một lần (bộ khoá đang dùng không có quyền stream thật) · *người chấm* = model chấm điểm câu trả lời trong bộ đo.

## 1. Đổi gì

| File | Đổi gì |
|---|---|
| `backend/llm/bedrock_model.py` (MỚI) | Lớp `BedrockClaudeModel` (một `Model` của Agents SDK) gọi `/invoke` của Bedrock, tự ký yêu cầu bằng thư viện chuẩn, không thêm gói. Dịch vào: lời dặn, lịch sử, vòng công cụ, ảnh, khuôn đầu ra, công cụ, mức suy luận. Dịch ra: chữ, lời gọi công cụ, số token. Stream giả. |
| `backend/config/settings.yaml` | Dòng `full_corpus_generation.provider` thành công tắc `openai` ↔ `bedrock` (**mặc định trong repo vẫn `openai`**) + khối `bedrock`: mã model, vùng, `max_tokens: 128000` (trường bắt buộc của kiểu gọi Claude ⇒ để mức tối đa của model = coi như không trần), `reasoning_default: low` (mức suy luận `none | low | medium | high` cho lời gọi không tự đặt mức; tạm `low`, phiên điều phối chọn lại sau lượt đo), TÊN biến môi trường trỏ tới file khoá. |
| `backend/core/settings_loader.py` | Nhận `bedrock` ngoài `openai`; khi là `bedrock` thì kiểm khối `bedrock`. Các dòng khoá model luna giữ nguyên. |
| `backend/llm/generator_openai_full_corpus.py` | `from_environment` dựng lớp dịch khi provider là `bedrock`; chín agent dùng chung đối tượng model như cũ. Tiền mỗi lần gọi tính theo model THẬT của lần gọi đó. Lỗi của Bedrock thành `GenerationError` có lời rõ. |
| `backend/llm/pricing.py` | Thêm bảng giá Sonnet 5.5; `cost_usd(..., provider="openai")` — không truyền thì đúng giá luna như trước. |
| `backend/llm/assistant.py` | Một dòng: tiền cận dưới của lần gọi bị huỷ tính theo provider của generator. |
| `backend/evaluation/full_corpus_eval.py` | Người chấm LUÔN là model OpenAI ghi ở `model` (luna), kể cả khi provider là `bedrock`; tổng tiền phần sinh tính theo provider đang cấu hình. |
| `backend/tests/test_bedrock_model.py` (MỚI, 10 ca) · `tests/test_phase6_settings.py` | Test lớp dịch; test cấu hình thôi khoá giá trị `provider` (để đổi một dòng không làm đỏ test), các dòng khác vẫn khoá. |

Đổi qua: sửa `provider: openai` thành `provider: bedrock` + đặt biến môi trường `HUE_BEDROCK_CREDS_FILE` trỏ tới file khoá tạm lúc bật server. Đổi về: sửa lại `openai`.

## 2. Lệch so với thiết kế được giao (đã chọn, lý do)

1. Tiền không chọn theo một hằng toàn cục mà theo từng lần gọi (đọc từ đối tượng model của agent): phiên đo cần hai generator khác provider sống cùng một tiến trình.
2. Hàm gỡ từ khoá ràng buộc trong khuôn không gỡ nhầm một TRƯỜNG có tên trùng từ khoá (bản ở script thử gỡ theo tên bất kể vị trí).
3. Lượt model xin công cụ thì đường stream giả KHÔNG phát chữ (nơi đọc ghép mọi mảnh chữ của cả lượt thành một chuỗi JSON câu trả lời).
4. Lời lỗi 403 không mang thân phản hồi của AWS (thân đó có mã tài khoản / tên vai); lời lỗi mã khác được che các chuỗi dạng đó trước khi ghi.
5. (Bổ sung của phiên điều phối 09:53, theo lời chủ dự án) Luôn gửi `max_tokens` của cấu hình, agent không hạ được; mức suy luận luôn gửi rõ — `none` ⇒ `thinking: between_tools`, ba mức còn lại ⇒ `thinking: adaptive` + mức; agent tự đặt mức (nhóm lịch: low) giữ mức của nó. Cả hai khoá đọc từ dict `settings` lúc dựng generator ⇒ nhiều generator khác mức sống cùng một tiến trình.
6. Chưa bật đệm lời dặn (prompt caching) cho Claude — thiết kế không yêu cầu; số token đệm sẽ là 0. Muốn giảm tiền thì là một việc riêng.

## 3. Bằng chứng

| Kiểm | Lệnh (từ `backend/` của worktree; `R` = `uv run --no-sync --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env`) | Kết quả |
|---|---|---|
| [máy kiểm] Test lớp dịch — phản hồi Claude DỰNG SẴN, vòng chạy SDK thật | `R pytest tests/test_bedrock_model.py -q` | 10 đạt. Đã thấy đỏ một lần: bỏ phép cộng phần đệm vào token vào ⇒ 3 ca hỏng. |
| [máy kiểm] Đường OpenAI không đổi — test cũ chạm đường đổi, từng file | `R pytest tests/<file>.py -q` với `test_openai_full_corpus_generator` · `test_phase6_settings` · `test_full_corpus_eval` · `test_input_cache_tokens` · `test_b2_tool_loop` | 9 · 5 · 21 · 3 · 11 đạt |
| [máy kiểm] LƯỢT THẬT qua code sản phẩm, provider bedrock (không qua server): 4 câu × (không stream + đường stream của `/api/chat/stream`) + 1 lần hiểu ý sửa lịch | script riêng tư `b_goi_that.py` (thư mục lượt thử Bedrock trong `data/`) | 9 / 9 không lỗi. Câu giá vé: trả lời có nguồn, 0 lỗi citation, 4,8 s (không stream) / 5,6 s (stream). Câu chào: tuyến trò chuyện 2,2–2,5 s. Câu ngoài Huế: từ chối cố định 0,65 s. Câu so sánh hai lăng: 7,9–9,4 s. Hiểu ý sửa lịch (khuôn có `maxItems`): ra đúng một hành động dời buổi, 1,3 s. |
| [máy kiểm] VÒNG CÔNG CỤ thật trên Bedrock (model xin `tim_kho` ⇒ nhận kết quả ⇒ viết), cả hai đường | script riêng tư `b_vong_cong_cu.py` | 2 / 2 đạt: 2 lần gọi model mỗi lượt, 2,1–2,7 s; đường stream phát đúng: công cụ được gọi ⇒ kết quả ⇒ một mảnh chữ ⇒ xong. |
| [máy kiểm] Bốn generator bốn mức suy luận (`none`, `low`, `medium`, `high`) trong MỘT tiến trình, `max_tokens` 128000: mỗi mức một lượt có công cụ + một lần định tuyến | script riêng tư `b_muc_suy_luan.py` | 4 / 4 mức chạy, 0 lỗi; 2,7–8,0 s mỗi lượt (mức `none` lượt này gọi công cụ hai lần). Câu thử dễ ⇒ 0 token suy luận ở cả bốn mức — KHÔNG phải số so sánh các mức. |
| [chưa kiểm] Lượt thật qua GIAO DIỆN (hỏi thường có công cụ, hỏi tiếp, lên lịch, sửa lịch, ảnh) | cần server | chưa chạy |
| [chưa kiểm] Cả bộ test | để mốc (theo cách làm 20/11) | không chạy |

Tiền thật các lượt trên (giá ghi sổ, chưa đối chiếu hoá đơn): ≈ 0,16 USD Bedrock. So để biết cỡ: một câu trả lời có nguồn ≈ 0,018 USD trên Sonnet 5.5, cùng loại câu trên luna ≈ 0,0007 USD (≈ 25 lần).

## 4. Giới hạn đã biết của nhánh

- Chữ hiện MỘT lần sau khi model viết xong (stream giả), không chạy dần như luna.
- Token suy luận ghi 0 ở mọi lần gọi B đã chạy (câu thử dễ, model không suy luận). Tên trường đọc (`output_tokens_details.thinking_tokens`) khớp sổ lượt thử của phiên điều phối; chưa có lần gọi nào QUA lớp dịch ra số khác 0. Không ảnh hưởng tiền: token ra đã gồm phần suy luận.
- Hạn giờ 45 giây mỗi lượt giữ nguyên; lượt lên lịch dài trên Sonnet chưa đo ở nhánh này (phiên đo sẽ đọc thời gian từng lần gọi).
- Tổng tiền phần sinh trong bảng tổng hợp của bộ đo (`generation_usage`) tính theo provider trong `settings.yaml` lúc tổng hợp; tiền từng dòng (`usd`, `llm_calls`) luôn đúng theo model của lần gọi.
