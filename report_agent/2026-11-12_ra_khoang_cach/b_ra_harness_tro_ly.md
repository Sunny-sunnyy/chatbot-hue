# Rà harness trợ lý (định tuyến, vòng công cụ, phục hồi, nhớ, song song) — B · **XONG 09:50 14/11/2026** (bắt đầu 13/11, dừng vì kết phiên, làm nốt 14/11)

A giao 13/11 (hướng thường trực User: nghiên cứu khả năng / harness của trợ lý). Chỉ đọc, **0 USD**. Theo skill `skills/agent-design-review/SKILL.md`.
Đã đọc trước để không đề xuất trùng: `e_khoang_cach_agentic.md`, `c_ra_loi_dan.md`, `c_phan_chua_on.md` (mục 3b–3e).

## 1. Đã làm: đếm log thật (0 USD) — `data/ra_harness_2026-11-13/dem_log.py` ⇒ `dem_log.txt`

**Thước:** chỉ dòng `chat_metrics` của `backend/logs/application.log` (main) có **gọi model thật** (`model = gpt-6-luna`). Log trộn dòng pytest mô phỏng lỗi
(`internal_error`, `generation_failed`, `retrieval_unavailable`… không tách sạch được bằng trường nào) ⇒ **mọi con số lỗi / outcome lỗi của log không dùng làm bằng chứng**.
Còn **354 lượt** (27/10 – 13/11), **gần như toàn bộ là lượt đo của agent** (B7, thí nghiệm, Playwright), không phải người dùng thật ⇒ chỉ là **dấu hiệu**, không phải phân bố thật.

| Số | Giá trị | Ghi chú |
|---|---|---|
| Tuyến | `tro_ly_hue` 295 · `tro_chuyen` 4 · không ghi tuyến 55 (dòng trước khi có định tuyến, 27/10) | `ngoai_pham_vi` không gọi model trả lời ⇒ không có trong thước này |
| `tro_ly_hue`: cả câu p50 / p95 | 5,99 s / 20,8 s | gồm lượt lịch (biểu mẫu) + câu nhiều lần tìm |
| `tro_ly_hue`: chữ đầu p50 / p95 (stream, n = 189) | 3,22 s / 9,43 s | sàn User: chữ đầu p50 ≤ 3 s, p95 ≤ 5 s ⇒ **vượt** trên tập đo này (tập lệch về câu khó) |
| Lần gọi model / lượt `tro_ly_hue` | 1: 82 · 2: 101 · 3: 29 · 4: 31 · 5: 21 · 6: 31 | 6 lần ⇒ định tuyến + 4 lượt vòng công cụ + web |
| `tim_kho` / lượt `tro_ly_hue` | 0: 82 · 1: 111 · 2: 39 · 3: 26 · 4: 37 | 3–4 = lần tìm đầu của code + model tìm thêm tới trần |
| Chạm trần tìm / `max_turns` | 37 lượt | đúng ca cờ "hết lượt tìm thì dừng" (bật 13/11) nhắm tới |
| USD / lượt `tro_ly_hue` | TB 0,00079 · p95 0,0021 | sàn User ≤ 0,0005 / câu ⇒ **vượt** ở TB trên tập đo này |
| Từ chối (`tro_ly_hue`) | 58 / 295; cổng web có mục 27 / 58 | web không tin cậy 15 · chưa xác minh 13 · thiên tai 1 |
| Định tuyến | `routing_ms` p50 1,83 s / p95 3,82 s · `route_error` 0 · khẩn cấp do định tuyến 4 | |
| Song song định tuyến (#6) | phần trả lời chạy trước bị bỏ 3 / 192 lượt stream, 0,0005 USD tổng | rẻ |
| Nhớ hội thoại | 0 lượt lịch sử 272 · có lịch sử 27; `history_tokens` p95 36 | chỉ nhớ câu hỏi (cờ) |
| Công cụ (số lần) | `tim_kho` 415 · `lich_trinh` 82 · `tra_web` 57 · `lich_san` 40 · `ngay_lich` 19 · `thoi_tiet` 2 | |

## 2. Tách theo loại lượt (0 USD) — `data/ra_harness_2026-11-13/dem2.py`, `dem3.py` ⇒ `dem_2_3.txt`

Cùng thước mục 1 (chỉ dòng gọi model thật, đa số là lượt đo của agent ⇒ **dấu hiệu**, không phải phân bố người dùng). Loại lượt tách bằng `tools` + `web_outcome`
(log chưa có nhãn loại câu). Chỉ 37 dòng sau khi bật cờ "hết lượt tìm" (13/11) ⇒ số dưới **phần lớn là trước khi bật cờ**.

| Loại lượt (`tro_ly_hue`) | n | Chữ đầu p50 / p95 (s) | Cả câu p50 (s) | USD p50 | So sàn (chữ đầu p50 ≤ 3, p95 ≤ 5; ≤ 0,0005 USD) |
|---|---|---|---|---|---|
| Câu kho, 1 lần tìm (chỉ lần đầu của code) | 79 | 2,17 / 4,05 | 4,14 | 0,00043 | **đạt cả ba** |
| Câu kho, model tìm thêm 1 lần | 20 | 4,88 / 8,62 | 8,75 | 0,00073 | trượt |
| Câu kho, tìm ≥ 3 lần | 12 | 9,29 / 13,62 | 14,35 | 0,00091 | trượt |
| Lịch trình | 82 | 2,92 / 8,10 | 5,01 | 0,00039 | p50 + tiền đạt, p95 trượt |
| Câu ngày | 45 | 3,79 / 11,25 | 4,75 | 0,00056 | trượt nhẹ |
| Từ chối ⇒ tra web | 57 | 6,56 / 9,93 | 14,32 | **0,00195** | trượt (tiền gấp ~4 sàn) |

- **Mỗi lần model tìm thêm ≈ +4–5 s và +0,0003 USD.** Phần trượt sàn tốc độ / tiền trong log đến từ vòng tìm thêm và đường web, không từ lượt thường.
- **Đường web tốn 0,00195 USD / lượt** (trung vị): Serper 0,001 (≈ 51 %, cố định mỗi lần tra) · trợ lý 0,00065 (trung vị **4** lần tìm kho trước khi từ chối, tức là đi hết vòng) · lần gọi viết mục web 0,0002 (4,7 s) · định tuyến 0,0001.
- **Cache prompt:** lần gọi trợ lý đầu tiên của lượt **0 / 295** lần có cache, vì phần đầu cố định (lời dặn ≈ 1.231 ký tự + mô tả công cụ) ngắn hơn ngưỡng cache của OpenAI (1.024 token, theo hiểu biết, chưa kiểm tài liệu). Từ lần gọi thứ 2 trở đi trong cùng lượt: **223 / 223** lần có cache, chiếm 43,9 % token vào của trợ lý. Định tuyến (≈ 727 token) cũng 0 cache. Muốn có cache ở lần gọi đầu thì phải độn lời dặn ⇒ **không đề xuất**.

## 3. Bảng rà theo skill `agent-design-review`

| Mục | Hiện trạng | Khớp / lệch | Số / ghi chú |
|---|---|---|---|
| §1 Có cần agent | `_pick_route` (`llm/assistant.py:805`): 1 lần gọi chọn 4 tuyến; lịch trình, biểu mẫu, ngày, thời tiết, web đều do code quyết | khớp | định tuyến p50 1,83 s; đường stream chạy song song nên không nằm trên đường chờ chữ đầu (bỏ 3 / 192, tốn 0,0005 USD tổng) |
| §2 Code ↔ model | xếp lịch, kiểm khung, kiểm cuối, số thời tiết, ngày âm, kiểm citation, kiểm mục web đều ở code (`_finish_generated` :665, `cong_web` :847) | khớp | |
| §3 Tham số công cụ | `tim_kho` model chỉ điền `cau_tim`; top-k / collection / ngân sách do code (`tool_for_turn` :265) | khớp | |
| §3 Lỗi hạ tầng ≠ rỗng | lỗi tìm ⇒ `trace.tool_error` rồi ném ra (route trả câu lỗi), không đưa cho model; không có nguồn mới ⇒ `TOOL_NO_NEW_TEXT` | khớp | |
| §4 Trần lượt | `ASSISTANT_MAX_TURNS = 4` (+1 khi có công cụ ngày, `generator_openai_full_corpus.py:77–82`); `MODEL_SEARCH_LIMIT` đếm ở code; cờ hết lượt ẩn `tim_kho` (`:412`) | khớp | 37 lượt chạm trần trong log (đa số trước khi bật cờ) |
| §4 Thời hạn | `asyncio.wait_for(..., 45 s)` bọc **cả** `Runner.run` nhiều lượt (`:356`); stream: một deadline 45 s cho cả luồng (`assistant.py:985`); không có hạn cho từng lần gọi; `max_retries=0` | lệch nhẹ so với skill ("thời hạn mỗi lời gọi") | **0** lần hết giờ trong 354 dòng thật ⇒ chưa có lỗi quan sát ⇒ **không đề xuất** |
| §4 Hết trần ⇒ đường có thật | chạm trần / hết lượt ⇒ câu từ chối cố định `max_turns`; `web_gate_open` (`:836`) **không mở** cổng web ở outcome này ⇒ người dùng chỉ nhận câu từ chối | lệch (ngõ cụt) | log: 2 lượt tìm ≥ 3 lần mà vẫn từ chối; ít ⇒ theo dõi, chưa xây |
| §5 Agent con | không có; mỗi đường (định tuyến / trợ lý / biểu mẫu / web) là một lần gọi có lời dặn riêng | khớp | |
| §5 Trí nhớ | `api/conversations.py`: RAM, cookie, 3 lượt, 30 phút, 1.500 token, chỉ nhớ câu hỏi (cờ `nho_cau_tra_loi: false`) | khớp | 27 / 299 lượt có lịch sử; `history_tokens` p95 36 |
| §5 Lời dặn | do C rà (`c_ra_loi_dan_ban2.md`) | — | không lặp ở đây |

## 4. Đề xuất (xếp theo lợi / công; không đề xuất nào là xây ngay — luật "đếm lỗi trước khi xây")

1. **Không xây gì thêm cho harness lúc này.** Lượt thường (1 lần tìm) đạt cả ba sàn. Phần trượt rơi đúng vào vòng tìm thêm mà cờ "hết lượt tìm" (bật 13/11) đang nhắm tới, và đường web mà User đã nhận.
2. **Đếm lại sau ~1 tuần dùng cờ (0 USD, chạy lại `dem2.py`):** phân bố số lần tìm / lượt và chữ đầu của câu kho tìm ≥ 2 lần. Đây chính là việc theo dõi cờ đã có trong handoff, không phải việc mới. Nhãn loại câu (việc 6 của handoff) giúp tách sạch hơn cách tách bằng `tools` hiện giờ.
3. **Ngõ cụt khi chạm trần (§4):** đếm trong cùng lượt đếm ở mục 2 số lượt có outcome `max_turns` hoặc hết lượt mà kết thúc bằng câu từ chối. Từ ≥ 5 lượt trên dòng thật trở lên thì mới bàn cho cổng web mở ở outcome này (đổi một dòng `web_gate_open` + đo an toàn kèm). Hiện có 2 lượt ⇒ chưa.
4. **Đường web gấp ~4 sàn tiền:** một nửa là Serper (giá cố định; Exa đã thử 12/11 và giữ Serper). Phần trợ lý đi hết vòng tìm trước khi từ chối thì cờ hết lượt đã cắt một phần. Không đề xuất thêm; ghi lại là giới hạn đã biết.

Giới hạn: log là lượt đo của agent, lệch về câu khó; tách loại lượt bằng `tools` nên câu ngày có tìm thêm bị tính vào "câu ngày". Không con số nào ở đây là phân bố người dùng thật.
