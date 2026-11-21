# Đổi tạm model viết sang Claude Sonnet 5.5 trên Amazon Bedrock — phần code (nhánh `p9-b-bedrock-sonnet`)

Viết: 09:55 21/11/2026, sửa 09:56 21/11/2026 sau phần bổ sung thiết kế (giờ `date`), phiên B. Giao việc: `session_prompt/VIEC_DANG_MO.md` khối 0a (bản giao việc đủ ở thư mục riêng tư ghi tại đó).
Trạng thái (10:07 21/11/2026, giờ `date`): **code + test xong; lượt thật qua giao diện ĐÃ chạy (mục 3b); phiên C review vòng 1 trả một điểm lớn + hai điểm nhỏ — đã sửa (mục 5), chờ C xác nhận.**

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
| [máy kiểm] Test lớp dịch — phản hồi Claude DỰNG SẴN, vòng chạy SDK thật | `R pytest tests/test_bedrock_model.py -q` | 16 đạt (10 ca đầu + 6 ca thêm sau review). Đã thấy đỏ một lần: bỏ phép cộng phần đệm vào token vào ⇒ 3 ca hỏng. |
| [máy kiểm] Đường OpenAI không đổi — test cũ chạm đường đổi, từng file | `R pytest tests/<file>.py -q` với `test_openai_full_corpus_generator` · `test_phase6_settings` · `test_full_corpus_eval` · `test_input_cache_tokens` · `test_b2_tool_loop` | 9 · 5 · 21 · 3 · 11 đạt |
| [máy kiểm] LƯỢT THẬT qua code sản phẩm, provider bedrock (không qua server): 4 câu × (không stream + đường stream của `/api/chat/stream`) + 1 lần hiểu ý sửa lịch | script riêng tư `b_goi_that.py` (thư mục lượt thử Bedrock trong `data/`) | 9 / 9 không lỗi. Câu giá vé: trả lời có nguồn, 0 lỗi citation, 4,8 s (không stream) / 5,6 s (stream). Câu chào: tuyến trò chuyện 2,2–2,5 s. Câu ngoài Huế: từ chối cố định 0,65 s. Câu so sánh hai lăng: 7,9–9,4 s. Hiểu ý sửa lịch (khuôn có `maxItems`): ra đúng một hành động dời buổi, 1,3 s. |
| [máy kiểm] VÒNG CÔNG CỤ thật trên Bedrock (model xin `tim_kho` ⇒ nhận kết quả ⇒ viết), cả hai đường | script riêng tư `b_vong_cong_cu.py` | 2 / 2 đạt: 2 lần gọi model mỗi lượt, 2,1–2,7 s; đường stream phát đúng: công cụ được gọi ⇒ kết quả ⇒ một mảnh chữ ⇒ xong. |
| [máy kiểm] Bốn generator bốn mức suy luận (`none`, `low`, `medium`, `high`) trong MỘT tiến trình, `max_tokens` 128000: mỗi mức một lượt có công cụ + một lần định tuyến | script riêng tư `b_muc_suy_luan.py` | 4 / 4 mức chạy, 0 lỗi; 2,7–8,0 s mỗi lượt (mức `none` lượt này gọi công cụ hai lần). Câu thử dễ ⇒ 0 token suy luận ở cả bốn mức — KHÔNG phải số so sánh các mức. |
| [chưa kiểm] Cả bộ test | để mốc (theo cách làm 20/11) | không chạy |

Tiền thật các lượt trên (giá ghi sổ, chưa đối chiếu hoá đơn): ≈ 0,16 USD Bedrock. So để biết cỡ: một câu trả lời có nguồn ≈ 0,018 USD trên Sonnet 5.5, cùng loại câu trên luna ≈ 0,0007 USD (≈ 25 lần).

## 3b. Lượt thật qua giao diện (viết 10:07 21/11/2026) — server tạm trong worktree, provider bedrock, mức suy luận mặc định `low`, trình duyệt tự động

14 lượt, 14 thành công, 0 lỗi trang. Lời gọi model dài nhất 11,6 giây; không lượt nào tới 35 giây (hạn giờ mỗi lượt là 45 giây). Tiền thật 0,30 USD.
Phiên E đã tự đếm lại từ log và ra cùng các con số thời gian. Hồ sơ riêng tư (chữ từng lượt + 13 ảnh chụp màn hình): thư mục `ket_qua/b_giao_dien/` của lượt thử Bedrock trong `data/`.

| Người dùng làm gì | Thấy gì | Thời gian |
|---|---|---|
| Hỏi thường (giá vé Đại Nội) | câu trả lời có 3 nguồn + dòng "có thể đã thay đổi" | 3,7 s |
| Hỏi tiếp ("thế còn lăng Minh Mạng?") | hiểu đúng ý nối câu trước; model tự tìm kho thêm 2 lần rồi mới viết | 5,7 s (4 lần gọi model) |
| Xin danh sách (quán bún bò) | danh sách + dòng "có thể chưa đủ" | 5,0 s |
| Câu so sánh hai chùa | trả lời từ kho 2 nguồn + mục "Từ web" | 11,5 s |
| Lên lịch bằng biểu mẫu (3 ngày · cân bằng · di tích), hai lần | thẻ lịch đủ 3 ngày, câu mô tả từng điểm, quán ăn gần | 9,3 s và 9,1 s |
| Sửa lịch — lệnh làm được ("dời Đại Nội sang sáng ngày 3") | "Đã dời…", lịch đổi đúng | 1,6 s |
| Sửa lịch — hai lệnh code từ chối | nói lý do, gợi ý chỗ dời được | 2,7–2,9 s |
| Hỏi về lịch đang có ("ngày 1 đi hết mấy tiếng?") | trả lời theo lịch; lần gọi này có 483 token suy luận | 11,6 s |
| Hỏi bằng ảnh (ảnh chùa Thiên Mụ) | nhận đúng tên ⇒ tự hỏi ⇒ câu giới thiệu có nguồn | nhận tên 1,2–1,7 s; cả lượt 11,3 s |

Khác với luna mà người dùng thấy: chữ hiện MỘT lần sau khi model viết xong — mọi lượt trên là chờ 4–12 giây rồi thấy cả câu.
Chưa thử qua giao diện: lịch 1 ngày / kiểu gấp / nhiều sở thích · ảnh ra 2–3 tên · câu bão lũ · màn hẹp · hai người hỏi cùng lúc · khoá hết hạn giữa chừng.

## 4. Giới hạn đã biết của nhánh

- Chữ hiện MỘT lần sau khi model viết xong (stream giả), không chạy dần như luna.
- Token suy luận: ở lượt giao diện đã có hai lần gọi ra số khác 0 (122 và 483) ⇒ trường này đọc đúng; token ra đã gồm phần suy luận nên tiền không đổi.
- Hạn giờ 45 giây mỗi lượt giữ nguyên; lượt lên lịch dài trên Sonnet chưa đo ở nhánh này (phiên đo sẽ đọc thời gian từng lần gọi).
- Tổng tiền phần sinh trong bảng tổng hợp của bộ đo (`generation_usage`) tính theo provider trong `settings.yaml` lúc tổng hợp; tiền từng dòng (`usd`, `llm_calls`) luôn đúng theo model của lần gọi.

## 5. Review vòng 1 của phiên C trên `a463292` và cách sửa (10:07 21/11/2026)

Phiên C đã kiểm đạt: đường OpenAI giống từng byte (10 loại lời gọi chụp ở main và ở nhánh ra cùng một mã băm) · không có khoá / đường dẫn khoá / mã tài khoản trong diff · dịch lịch sử và vòng công cụ (6 ca biên + 2 lời gọi thật) · số token ⇒ tiền khớp số tính tay.

| Điểm | Nội dung | Sửa |
|---|---|---|
| Lớn | Trên đường stream, lỗi của Bedrock (403, 429, hết giờ, rớt mạng) đi tới nơi đọc dưới dạng lỗi lạ ⇒ lịch mất đường "câu dự phòng, lịch vẫn hiện", ô chat báo "lỗi hệ thống" thay cho "không tạo được câu trả lời" | `BedrockError` nay là một `GenerationError`; lỗi mạng / hết giờ / không đọc được file khoá đều được đổi thành lỗi này ngay trong lớp dịch. Test mới 5 ca trên đường stream: ĐỎ trên code cũ, xanh sau sửa. |
| Nhỏ 1 | Che mã tài khoản SAU khi cắt 300 ký tự ⇒ mã vắt qua mốc cắt còn sót một phần | Che trước rồi cắt. Ca test mới còn bắt thêm một lỗi của chính mẫu che (mã đứng liền sau chữ cái không được nhận) — đã sửa mẫu. |
| Nhỏ 2 | Lời lỗi chung vẫn ghi chữ "OpenAI generation…" khi chạy Bedrock | Không sửa (chỉ là chữ trong log; đổi sẽ chạm đường OpenAI). |

## 6. Lượt đo nhỏ lịch · sửa lịch · ảnh trên bốn nhánh, và nhánh `p9-b-sua-lich-high` (11:04 21/11/2026, giờ `date`)

Câu hỏi của chủ dự án: với lên lịch, sửa lịch và ảnh, Sonnet ở low / medium / high khác nhau gì, và so với luna. 156 lời gọi thật qua code sản phẩm (không server), 0 lỗi,
0 lời gọi bị cắt vì trần token, lời gọi dài nhất 11,7 giây. Mẫu và kết quả mong đợi ghi trước khi chạy (đầu script riêng tư `b_do_lich_sua_anh.py`). Cỡ mẫu nhỏ: đọc là "ngang nhau" trừ chỗ lặp lại qua ba lượt.

| Phần (cỡ mẫu mỗi nhánh) | luna | Sonnet low | Sonnet medium | Sonnet high |
|---|---|---|---|---|
| Sửa lịch, lệnh rõ ràng: đúng ý (18 lần) | 17 | 18 | 18 | 18 |
| Sửa lịch, lệnh phủ định "đừng bỏ…" (3 lần) | 3 | 3 | 3 | 3 |
| Sửa lịch, lệnh mơ hồ: không tự chọn điểm (3 lần) | 3 | 0 | 0 | 2 |
| Sửa lịch, lệnh bị luật chặn: model vẫn trả đúng hành động (3 lần) | 3 | 2 | 0 | 3 |
| Sửa lịch, thời gian giữa – lâu nhất | 2,1 – 5,5 s | 1,3 – 4,0 s | 1,4 – 3,1 s | 2,1 – 6,8 s |
| Lên lịch 4 kiểu: câu model qua bộ kiểm của code (27 mục, một lần) | 27 | 27 | 27 | 27 |
| Lên lịch, thời gian giữa – lâu nhất | 3,7 – 4,4 s | 5,5 – 8,3 s | 5,2 – 8,3 s | 6,0 – 11,7 s |
| Ảnh trong danh sách: tên đúng trong ≤ 3 tên (6 ảnh, một lần) | 6 | 6 | 6 | 6 |
| Ảnh ngoài danh sách: không ép tên Huế (2 ảnh) | 1 | 2 | 2 | 2 |
| Ảnh, thời gian giữa – lâu nhất | 3,1 – 7,8 s | 1,6 – 3,5 s | 1,4 – 1,8 s | 1,5 – 2,3 s |

Đối chiếu sự thật 17 câu mô tả điểm (5 mục) với đúng đoạn nguồn của lời gọi: luna 7 chi tiết, Sonnet low 13, medium 9, high 14 — tất cả có trong đoạn nguồn, 0 chi tiết bịa;
một lỗi GỘP Ý của Sonnet (tháp Phước Duyên bị xếp chung vào "Bảo vật quốc gia" — nguồn chỉ ghi chuông và bia): sai hẳn ở một câu của lượt giao diện, nói lỏng ở low và high, đúng ở medium.

**Đổi ở nhánh `p9-b-sua-lich-high`:** đường Bedrock, hai agent hiểu ý sửa lịch gửi mức suy luận của khoá mới `bedrock.reasoning_sua_lich` (`high`); viết câu lịch và lượt biểu mẫu giữ `low`;
đường OpenAI không đổi (tham số mới của generator mặc định bằng mức cũ). Lượt thật trên cấu hình của nhánh [máy kiểm]: lệnh bị luật chặn đúng 3 / 3; lệnh dễ đúng 1 / 1.

**Giới hạn ghi lại, CHƯA sửa:** lệnh sửa lịch mơ hồ — Sonnet high vẫn tự bỏ một điểm người dùng không nêu 3 / 6 lần (1 / 3 ở lượt đo + 2 / 3 ở lượt thật của nhánh); low và medium 3 / 3.
Sửa việc này cần đổi lời dặn và đo lại — không làm ở nhánh này. Lỗi gộp ý trong câu mô tả điểm của thẻ lịch (1 mục / 5 đã đối chiếu, 0 chi tiết bịa hẳn, bộ kiểm của code không bắt) cũng chưa sửa: phiên điều phối chốt GHI GIỚI HẠN sau khi một phiên khác đọc tay 36 câu trả lời ở ô hỏi đáp và thấy 0 / 36 lần lặp lại.

## 7. Nhánh `p9-b-loi-dan-sonnet` (11:26 21/11/2026, giờ `date`): sửa lỗi gọi lặp công cụ + bốn đoạn dặn riêng cho Sonnet

### 7.1 Lỗi gọi lặp công cụ — nguyên nhân gốc và bản sửa

Phiên đo thấy: câu cần công cụ thời tiết / ngày, Sonnet gọi lặp công cụ tới hết vòng rồi trả câu từ chối — 4 câu × 3 lượt chạm trần vòng 9 / 12 ở low, 8 / 12 medium, 1 / 12 high, luna 0.
Tái hiện một câu trên bản chính, in nguyên thân gửi Bedrock từng vòng: kết quả công cụ tới model ĐÚNG và đủ ⇒ không phải lỗi dịch. Phát lại đúng thân của vòng "đã có dự báo, phải viết", mỗi lần đổi MỘT thứ:

| Đổi gì | Model viết | Model gọi công cụ tiếp |
|---|---|---|
| không đổi (low) · medium · high · không suy luận | 0 / 8 mỗi mức | 8 / 8 mỗi mức |
| thêm câu "đã có dự báo, hãy viết" vào kết quả công cụ | 1 / 8 | 7 / 8 |
| thêm "mỗi lượt gọi một lần" vào mô tả công cụ | 0 / 8 | 8 / 8 |
| ẩn công cụ thời tiết | 0 / 8 | 8 / 8 (quay sang công cụ tìm kho) |
| công cụ không strict · bỏ `tool_choice` | 0 / 12 | 12 / 12 |
| **bỏ khuôn JSON ép đầu ra, giữ mọi thứ khác** | **14 / 14** | 0 |

Nguyên nhân: khuôn JSON ép đầu ra (`output_config.format`) gửi cùng công cụ. Bản sửa (chỉ trong `backend/llm/bedrock_model.py`): lời gọi vừa có công cụ vừa có khuôn thì không gửi khuôn, thêm công cụ nội bộ
`tra_loi` mang đúng khuôn của agent; model gọi nó ⇒ lớp dịch đổi thành tin trả lời JSON. Quy tắc: `tra_loi` cùng công cụ thật ⇒ chạy công cụ thật, bỏ `tra_loi`; gọi hai lần ⇒ lấy lần đầu;
model viết chữ thường ⇒ bọc vào khuôn nếu khuôn chỉ có một trường chuỗi, khuôn khác ⇒ lỗi nhóm model. SDK, sổ vết, số vòng, stream giả không thấy khác.

| Kiểm sau sửa [máy kiểm] | Kết quả |
|---|---|
| Phát lại cùng thân yêu cầu, có bản sửa | nộp câu trả lời 8 / 8 ở low, 8 / 8 ở high (trước: 0 / 8) |
| 8 câu dạng công cụ (4 câu của phiên đo + 4 tự đặt) × 3 lượt ở high, qua `answer_turn` | chạm trần vòng 0 / 24 · lỗi 0 · lỗi trích nguồn 0 · nhiều nhất 4 lời gọi / lượt · lâu nhất 12,4 s |
| cùng 8 câu × 2 lượt ở low | chạm trần vòng 0 / 16 · lỗi 0 |
| 4 câu thường mỗi mức (có nguồn · hỏi rộng · kho không có · ngoài phạm vi) | câu có nguồn trả lời đúng khuôn, 0 lỗi trích nguồn; hai câu phải từ chối ra ĐÚNG câu từ chối cố định |
| Cách model nộp câu trả lời ở lời gọi có `tra_loi` | high: 14 lần qua `tra_loi`, 13 lần viết chữ thường (đường bọc); low: 19 qua `tra_loi`, 0 chữ thường |

Đọc dòng cuối: ở high gần một nửa số câu trả lời đi qua đường bọc chữ thường — đường đó là đường chính, không phải ca hiếm; nó chỉ an toàn vì khuôn của trợ lý có đúng một trường chuỗi.
Quan sát kèm, không sửa: câu "ngày mai nắng hay mưa, có nên ra biển…" Sonnet chọn loại `bao_lu` 3 / 3 lần ⇒ theo thiết kế câu bão / lũ, model không nêu số, phần dự báo do code nối dưới câu trả lời.

### 7.2 Bốn đoạn dặn chỉ nối khi chạy Sonnet (lời dặn gửi luna không đổi — test so đúng từng hằng cũ)

| Đoạn | Đo lại (cùng mẫu, mong đợi ghi trước) |
|---|---|
| Hiểu ý sửa lịch (ở high) | Sửa 11:36 sau review: bản đầu của đoạn dặn lấy NGUYÊN VĂN câu đo số 8 làm ví dụ ⇒ số của câu đó không tính. Đã đổi sang tả theo loại câu và đo lại: 8 lệnh còn lại × 3 lượt đúng ý 24 / 24 (trước đoạn dặn, ở high: 20 / 24… cộng câu 8 là 23 / 27); câu 8 (nay không còn trong lời dặn) 3 / 3; ba câu mơ hồ do phiên review đặt × 3 lượt 9 / 9 — đều đổi kiểu đi sang "nhẹ nhàng", 0 lần tự bỏ điểm (trước: 3 / 6 tự bỏ). Lệnh bị luật chặn 3 / 3. Lâu nhất 7,1 s ở một câu mơ hồ (hạn của lời gọi này là 10 s). |
| Viết câu thẻ lịch (nới một đến hai câu ~50 từ + giữ đúng vật) | Sửa 11:36 — số của người viết lúc đầu ("đúng 11 / 12") quá rộng; phiên review đọc lại 12 lượt mục Chùa Thiên Mụ: ĐÚNG RÕ 7 · LỎNG 4 (kể ba vật rồi "hai Bảo vật quốc gia", không nói hai vật nào) · SAI 1 ("đều là Bảo vật quốc gia"). Mốc bản 30 từ không đoạn dặn, cùng model, 10 lượt (4 lượt sáng + 6 lượt đo thêm): đúng rõ 2 · lỏng 4 · sai 1 · không nhắc danh hiệu 3. **Đọc thẳng: tỉ lệ sai và lỏng KHÔNG giảm thấy được (sai 1 / 10 ↔ 1 / 12; lỏng 4 / 10 ↔ 4 / 12); cái được là nhiều lượt viết đúng rõ hơn (2 / 10 ↔ 7 / 12) và câu đầy đủ hơn.** Thử 40 từ: sai 2 / 6. Câu dự phòng do nhắc tên điểm khác: bản 30 từ 3 / 51 mục, bản 50 từ 4 / 102 mục ⇒ ngang nhau (dòng "0 / 27" viết trước đó là mẫu quá nhỏ). Giá phải trả của bản 50 từ: PowerPoint cắt "…" 13 / 51 mục (bản 30 từ 0 / 27). Việc giữ bản 50 từ là lựa chọn về độ đầy đủ của câu, không phải bản sửa đã chứng minh được của lỗi ghép sai ý. |
| Định tuyến | 14 câu tự đặt × 2, hai bên cùng buổi: nơi rìa Huế low 14 / 16 ⇒ 16 / 16, high 16 / 16 ⇒ 16 / 16; nơi tỉnh khác vẫn từ chối 8 / 8 cả hai bên. Câu tự đặt chưa tái hiện được lỗi ở high ⇒ phép thử chính là bộ mù của phiên đo. |
| Trả lời | Chưa đo điểm "Trọng tâm" (phiên đo chạy lại 85 câu). Đã thấy: 44 lượt qua `answer_turn` có đoạn dặn này, 0 lỗi, câu từ chối cố định vẫn đúng chữ. |

Chưa làm: lượt thật qua giao diện sau các thay đổi này; thẻ lịch câu dài trên màn 390 px và bản in; cả bộ test. Tiền Bedrock phần này ≈ 3 USD.

## 8. Nhánh `p9-b-sua-rong-m03` (11:54 21/11/2026, giờ `date`): lỗi "nội dung rỗng" ở vòng đã hết lượt tìm + gỡ đoạn dặn trả lời

**Lỗi phiên đo báo:** một câu của bộ chuỗi (hỏi độ cao một ngọn núi mà kho không ghi) ở Sonnet high ném lỗi "nội dung rỗng" 2 / 2 lượt, trước và sau bản 0 ⇒ người dùng thấy "Thử lại"; luna trả câu từ chối.
**Tái hiện + nguyên nhân gốc [máy kiểm]:** chạy câu đó 5 lần trên bản chính, in phản hồi thô: 2 / 5 lượt trả lời người dùng bằng đúng một chữ **"tim_kho"** (tên công cụ) với kết cục "thành công" — tệ hơn lỗi rỗng.
Cả hai là một bệnh: sau hai lần model tự tìm, công cụ tìm kho bị ẩn (cơ chế có từ 12/11) ⇒ vòng viết không còn công cụ ⇒ lớp dịch ép khuôn JSON; Claude vẫn muốn tìm tiếp, không gọi được công cụ nên viết rác vào khuôn.
Phát lại đúng thân của vòng đó:

| Thân gửi | Đúng câu từ chối | Rác vào khuôn (`placeholder`, `tim_kho`, rỗng, lời tự nhủ) | Tự nói bằng lời "chưa tìm thấy" |
|---|---|---|---|
| như bản chính (ép khuôn, không công cụ) — 22 lần | 8 | 14 | 0 |
| bản sửa (bỏ khuôn, chỉ còn công cụ nội bộ `tra_loi`) — 22 lần | 20 | 0 | 2 |
| bản sửa + thêm câu "không còn công cụ tìm" vào mô tả — 12 lần | 10 | 0 | 2 (không hơn ⇒ không dùng) |

**Sửa** (chỉ `backend/llm/bedrock_model.py`, hàm `build_body`): có khuôn VÀ (có công cụ HOẶC lượt đã có lời gọi công cụ) ⇒ không ép khuôn, đưa công cụ nội bộ. Test mới đỏ trên lớp dịch cũ.
**Lượt thật sau sửa:** câu đó 6 lần qua `answer_turn` ở high: 0 lỗi, 0 rác; 5 lần đúng câu từ chối cố định, 1 lần trả lời phần kho có (tên khác của ngọn núi, có trích nguồn) và nói rõ chưa thấy độ cao.
**Không làm lưới "rỗng ⇒ câu từ chối cố định":** lưới đó chỉ bắt được 1 trong 14 kết quả hỏng của phép phát lại (13 cái còn lại là chữ rác, không rỗng) và che mất dấu hiệu nếu bệnh quay lại; sau bản sửa chưa thấy lượt rỗng nào (0 / 22 + 0 / 6). Nếu lượt đo lại còn thấy rỗng thì thêm.

**Gỡ đoạn dặn riêng cho phần trả lời** (phiên điều phối giao theo số của phiên đo): 85 câu ở high, lời dặn mới ↔ cũ, hai người chấm — Đúng / Đủ ý không đổi; độ dài trung vị 236 ⇒ 258 ký tự; Trọng tâm 4,39 ⇒ 4,26.
Ba đoạn còn lại (câu lịch, sửa lịch, định tuyến) giữ.

## 9. Nhánh `p9-b-lich-su-tach-luot` (13:43 21/11/2026, giờ `date`): gốc của lỗi "hỏi lại tên giữa cuộc" ở Sonnet

**Người dùng thấy gì trước khi sửa:** đã hỏi một câu về Huế, lượt sau hỏi "bạn còn nhớ tôi tên gì không?" ⇒ Sonnet hoặc báo lỗi "Thử lại" (phiên đo gặp 2 / 2 lần
trên bộ chuỗi), hoặc trả lời LẠI câu hỏi của lượt trước rồi mới nói tên (lượt tôi chạy lại: 2 / 2 câu như vậy). luna không bị.

**Nguyên nhân gốc [máy kiểm — in đúng thân gửi Bedrock khi chạy đúng lệnh bộ chuỗi của phiên đo]:** lịch sử hội thoại chỉ nhớ CÂU HỎI (câu trả lời cũ không lưu)
⇒ đầu vào là nhiều tin của người dùng đứng liền nhau. OpenAI giữ chúng là các tin riêng. Lớp dịch sang Claude lại GỘP các tin cùng vai liền nhau thành một tin
(Claude không nhận hai tin cùng vai liền nhau), nên model nhận MỘT tin duy nhất chứa lời tự giới thiệu, câu hỏi về vé của lượt trước và câu hỏi lại tên viết
liền nhau. Lời dặn định tuyến "chỉ chọn tuyến cho tin nhắn cuối cùng" không còn nghĩa — model không thấy tin cuối bắt đầu ở đâu ⇒ câu hỏi về Huế của lượt trước
kéo lượt này sang trợ lý tra kho ⇒ trả lời đúng tên nhưng không có nguồn để trích ⇒ luật "câu có căn cứ phải có [n]" báo lỗi (luật đúng, không nới).

**Sửa** (chỉ `backend/llm/bedrock_model.py`, hàm `to_messages`; đường OpenAI không đổi một byte): giữa hai CÂU HỎI liền nhau chèn một tin của trợ lý ghi "(Câu trả
lời của lượt này không được lưu trong lịch sử.)" ⇒ mỗi lượt cũ là một tin riêng, tin cuối đúng là câu đang hỏi. Kết quả công cụ liền nhau vẫn gộp như cũ.
Test: một test cũ đổi mong đợi (đỏ khi tắt riêng phần chèn) + một test mới cho ranh giới (kết quả công cụ không bị chèn).

| Chạy đúng lệnh bộ chuỗi, hai chuỗi có câu hỏi lại tên, Sonnet high | Lượt hỏi lại tên đi tuyến | Câu trả lời |
|---|---|---|
| Bản chính `e75cf18` — 1 lần chạy (2 lượt hỏi lại tên) | tra kho 2 / 2 | 2 / 2 trả lời lại câu vé của lượt trước rồi mới nói tên |
| Bản sửa — 2 lần chạy (4 lượt hỏi lại tên) | trò chuyện 4 / 4 | 4 / 4 chỉ nói đúng tên ("Bạn tên là Quân", "Bà tên là Hạnh, 65 tuổi…"); 0 lỗi |

Các lượt khác của hai chuỗi (6 lượt trong 2 lần chạy): tuyến và nội dung như trước, câu về vé vẫn có trích nguồn.

**Chưa kiểm — cần phiên đo:** cả bộ chuỗi (25 chuỗi) và bộ thước trên bản sửa, vì MỌI lượt có lịch sử ở Sonnet giờ gửi thân khác trước (có thêm tin giữ chỗ) — kể cả
câu hỏi tiếp kiểu "thế còn lăng Minh Mạng?". Rủi ro tôi thấy được: model nhại lại dòng giữ chỗ trong câu trả lời (10 lượt thật ở trên: 0 lần). Lượt không có lịch sử:
thân gửi không đổi. Tiền phần này ≈ 0,25 USD.
