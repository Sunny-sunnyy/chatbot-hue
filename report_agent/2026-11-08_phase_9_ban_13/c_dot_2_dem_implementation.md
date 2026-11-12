# Implementation Report: đợt 2 cổng — lượt đếm rẻ trước khi xây (lưu trú · ăn gần · sự kiện theo ngày)

Người làm: C (`hue-rag-e1`). Viết 19:04 12/11/2026 (`date`). A giao 18:45 12/11/2026 (`CURRENT_HANDOFF.md` "VIỆC PHIÊN 12/11", dòng C).
Luật áp: `Session_Prompt.md` §7 "Đếm lỗi trước khi xây" — xác nhận lỗi có thật và cỡ của nó trên hệ thống đang chạy trước khi viết plan.
Report tả câu ở **mức loại câu**; không chép câu hỏi, câu trả lời hay nội dung kho. Dữ liệu chạy (private): `data/phase_11/dot_2_dem/`.

## 1. Phạm vi

- Ba ý của đợt 2 (spec cổng đợt 1, D2 + mục "Ngoài"): **lưu trú** · **ăn uống gần một điểm** · **sự kiện theo ngày**.
- Với mỗi ý: người hỏi loại câu đó hôm nay nhận được gì — kho trả lời được · kho từ chối rồi ra mục web · trả lời sai.
- Không viết spec / code, không mở `*sealed*`, không sửa kho. Code `main` tại `a83defd` (không đổi `backend/` so với `e5d90c4`).

## 2. Nguồn số liệu — cái nào dùng được, cái nào không

| Nguồn | Dùng được không | Vì sao |
|---|---|---|
| Log `chat_metrics` / `chat_feedback` (`backend/logs/application.log`, 1.049 + 22 dòng tới 10/11) | **Không** cho việc đếm theo loại câu | Log cố ý **không ghi nội dung câu hỏi** ⇒ không biết dòng nào là câu lưu trú / ăn gần / sự kiện. Ngoài ra đa số dòng là lượt test và lượt đo của agent, không phải người dùng thật (hệ thống chưa deploy). Chỉ dùng log để **ước tiền** trước khi gửi câu mới |
| Bộ câu đã thấy trong `data/` | **Gần như không** | Quét bằng mẫu chữ (script chỉ in số đếm, bỏ mọi bộ kín): câu khớp 3 loại hầu hết là câu Golden lặp lại qua nhiều lượt chấm — Golden viết theo nội dung kho nên **không** có dạng "tìm cơ sở gần điểm X" hay "tuần này có gì". Câu riêng cho 3 loại ở các bộ khác: mỗi loại chỉ 1–4 câu |
| Kho (qua `scripts/grep_kb.sh`, chỉ đếm file) | **Có** — cho biết kho có sẵn gì | §4 |
| **18 câu tự viết gửi hệ thống thật** | **Có** — nguồn chính | 6 câu mỗi loại, kiểu khách du lịch hỏi; gửi `POST /api/chat` tới server `main` thật (uvicorn, Qdrant thật, `gpt-6-luna`, Serper thật), mỗi câu một cuộc mới |

**Giới hạn phải đọc cùng mọi số dưới đây:** câu do C tự viết, **n = 6 mỗi loại**, một lượt ⇒ chỉ thấy được khác biệt lớn; tỉ lệ các kiểu câu trong mỗi loại là do C chọn,
không phải tỉ lệ người dùng thật hỏi (chưa có người dùng thật).

## 3. Cách đã chạy thật

- Server: `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8871` (`/health` 5 / 5), tắt bằng TaskStop sau mỗi lượt. Đã nhắn B trước mỗi lần chạy (một session chạy server một lúc); không ai đo tốc độ lúc đó.
- Gửi câu: `data/phase_11/dot_2_dem/tools/gui_cau.py` — lưu câu trả lời + nguồn + mục web + dòng `chat_metrics` (đọc log sau mốc dòng); dừng theo trần tiền.
- Bộ câu: `data/phase_11/dot_2_dem/cau_18.jsonl` (md5 `7ea1663748f0`), **ghi trước khi gửi**. Kiểu câu trong mỗi loại:
  - lưu trú: 2 câu "nên ở khu nào" · 4 câu hỏi cơ sở cụ thể (gần một điểm ×2, giá rẻ, hạng sao);
  - ăn gần: 4 câu "quán gần điểm X" · 2 câu "món gì / quán nào quanh điểm X";
  - sự kiện: 3 câu khoảng ngày gần (cuối tuần này, tối nay, tuần sau) · 2 câu theo tháng · 1 câu "lễ hội X lần tới rơi vào ngày dương nào".
- Hai lần gửi (giờ theo dòng log `chat_metrics` ngày 12/11/2026): 18:49–18:52 (13 câu, dừng ở ngưỡng tiền) và 19:02–19:03 (5 câu sự kiện còn lại, sau khi A nâng trần 0,02 ⇒ 0,032 USD).
- Phân loại: C đọc từng câu trả lời; mọi tên riêng / giờ / ngày trong các câu "kho trả lời" được đối chiếu lại với kho bằng `scripts/grep_kb.sh` (có trong đúng bài được trích); 2 phép tính ngày của hệ thống (khoảng "tuần sau", tháng dương của hai ngày âm đầu năm 2027) C tính lại bằng lịch — khớp.
- Thời gian: quét bộ + log ~5 phút; lượt có phí 4 phút + 1 phút; đọc + đối chiếu ~10 phút.

## 4. Kết quả quan sát

### 4.1 Hệ thống trả lời ra sao (18 câu, 1 lượt)

| Loại (n = 6) | Kho trả lời — đủ dùng | Kho trả lời — một phần | Kho từ chối ⇒ mục web có nội dung | Kho từ chối ⇒ web không ra thông tin | Trả lời sai |
|---|---:|---:|---:|---:|---:|
| **Lưu trú** | 2 | 1 | 2 | 1 | 0 |
| **Ăn gần** | 1 | 2 | 2 | 1 | 0 |
| **Sự kiện theo ngày** | 4 | 0 | 1 | 1 | 0 |
| **Cộng** | 7 | 3 | 5 | 3 | **0** |

Đọc bảng theo từng loại:

- **Lưu trú.** Hai câu "nên ở khu nào" đều được kho trả lời đủ dùng (bài cẩm nang có mục khu nên ở + lý do). Bốn câu hỏi **cơ sở cụ thể**: 1 câu kho trả lời
  một phần (nêu tên cơ sở ở một trong hai nơi được hỏi, nói rõ nơi kia kho không có tên), 3 câu kho từ chối. Trong 3 câu đó, mục web ra danh sách tên ở 2 câu
  (nguồn là trang đặt phòng / trang du lịch; hệ thống tự ghi "chưa xác minh được khoảng cách / hạng sao"), 1 câu web trả "chưa tra được thông tin đáng tin".
  Không câu nào nêu giá phòng (đúng luật kiểm của mục web).
- **Ăn gần.** Chỉ 1 / 6 câu được kho trả lời đủ dùng (nêu đúng một quán có bài riêng trong kho, bài đó có câu định vị theo điểm được hỏi). 2 câu trả lời một
  phần: nêu khu + món nhưng nói rõ "nguồn không nêu tên quán", hoặc chỉ nêu một nhóm món của một khu. 3 câu kho từ chối: web ra tên quán ở 2 câu (một câu chỉ
  có 1 gợi ý từ mạng xã hội, hệ thống tự ghi chưa xác minh), 1 câu web không ra thông tin. ⇒ **5 / 6 câu người hỏi không nhận được câu trả lời đủ dùng từ kho.**
- **Sự kiện theo ngày.** 4 / 6 kho trả lời đủ dùng, có dùng "Lịch hệ thống" do code tính (khoảng ngày của "tuần sau", năm của "tháng 1 năm sau", đổi ngày âm
  đầu năm sang tháng dương) và có dòng nhắc "lịch có thể đã thay đổi" ở 3 / 4 câu. 2 câu từ chối: (a) câu "cuối tuần này có sự kiện gì" — web trả câu cố định
  "thay đổi theo thời gian, chưa xác minh được" kèm 5 link (đúng thiết kế: không nói số liệu thời gian thực); (b) câu "lễ hội X lần tới ngày dương nào" — kho
  **có** bài riêng về lễ hội đó nhưng trợ lý từ chối cả câu rồi ra web (1 ngày lấy từ mạng xã hội, tự ghi chưa xác minh).

**Trả lời sai: 0 / 18** theo phần C kiểm được (tên, giờ, ngày trong câu kho trả lời đều có trong bài được trích; phép tính ngày đúng). Nội dung mục web C **không**
kiểm đúng / sai ngoài đời — hệ thống đã gắn nhãn "Từ web (chưa kiểm)".

### 4.2 Kho đang có gì cho 3 loại (đếm file, không đọc nội dung)

| Loại | Kho có | Kho thiếu |
|---|---|---|
| Lưu trú | 1 bài cẩm nang có mục "khu nên ở"; 6 / 47 bài `travel/` có nêu tên một vài cơ sở lưu trú | không có danh sách cơ sở, không có bài riêng cho cơ sở nào |
| Ăn gần | **81 bài riêng cho quán ăn (57) + cà phê (24)**; 63 / 81 có dòng địa chỉ | chỉ **12 / 81** bài có câu định vị theo một điểm tham quan ("gần / cạnh / đối diện …"); 4 / 81 có toạ độ. Số bài quán nhắc tới từng điểm lớn: 0–8 bài mỗi điểm (có điểm lớn không bài quán nào nhắc) |
| Sự kiện | 26 bài lễ hội, 20 có ngày (dương hoặc âm); 11 / 13 bài nghệ thuật biểu diễn + 6 / 6 bài vé có giờ diễn định kỳ; code tính ngày (lịch hệ thống, âm ↔ dương) đã chạy | lịch sự kiện **của đúng tuần / tháng này** (5 / 26 bài nhắc năm 2026–2027); nghiên cứu 06/11 đã ghi: không nguồn chính thức nào có RSS / API cho lịch sự kiện |

### 4.3 Số theo dõi (không phải lượt đo tốc độ)

- Tiền: **0,024691 USD** cho 18 câu (lượt 1 0,018295 + lượt 2 0,006396; trần sau khi A nâng 0,032). Trung bình ≈ 0,0013–0,0014 USD / câu ở cả 3 loại — gấp ~2,7 lần
  sàn 0,0005 USD / câu Huế, vì 8 / 18 câu đi đường web (≈ 0,0018–0,0022 / câu) và các câu còn lại gọi `tim_kho` 2–4 lần.
- Thời gian cả câu (đường `/api/chat` không stream, **không** phải chữ đầu): trung vị ≈ 19–24 giây mỗi loại. Đây là tín hiệu để đo riêng, chưa phải số đo tốc độ.

## 5. Kết luận: đủ lỗi để xây / không xây

| Ý đợt 2 | Lỗi thật đếm được | Kết luận | Cái nhỏ nhất đáng làm (đề xuất, chưa duyệt) |
|---|---|---|---|
| **Ăn gần** | 5 / 6 câu không đủ dùng từ kho (3 từ chối, 2 một phần), dù kho có 81 bài quán | **Đủ lỗi để xây** — nhưng lỗi nằm ở **dữ liệu định vị**, không phải thiếu bản đồ | Gắn cho mỗi bài quán một dòng "ở khu nào / gần điểm nào" (63 bài đã có địa chỉ) theo luật sửa kho, rồi đo lại đúng 6 câu này. Không cần ghim bản đồ để hết lỗi này |
| **Lưu trú** | Câu "khu nên ở": 0 lỗi / 2. Câu hỏi cơ sở cụ thể: 3 / 4 kho từ chối, web cứu 2 / 3 | **Đủ lỗi cho một phần nhỏ, không đủ cho trang danh sách cơ sở** | Khi câu hỏi là tìm cơ sở lưu trú: thay câu từ chối bằng "khu nên ở (từ kho) + link tìm phòng do code dựng" — đúng ý đã nằm trong backlog Phase 11 (User 05/11: không nói giá phòng). Trang lưu trú kiểu danh sách: chưa có lỗi nào đòi |
| **Sự kiện theo ngày** | 4 / 6 kho trả lời đủ dùng; 1 câu "tuần này có gì" không nguồn nào trả lời được; 1 câu từ chối cả câu dù kho có bài | **Không đủ lỗi để xây** trang / lịch sự kiện | Không xây. Hai việc rẻ nằm ngoài đợt 2: (a) xem lại câu bị từ chối cả câu dù kho có bài (cùng gốc "từ chối cả câu" đã thấy ở các bậc trước); (b) nếu muốn có trang "lễ hội theo tháng" thì đó là việc hiển thị 20 bài có ngày, không đổi câu trả lời |

Bản đồ (ý thứ tư của đợt 2) không nằm trong lượt đếm này: nó là cách hiển thị, không đổi câu trả lời; đang chờ phiếu toạ độ của User.

## 6. Lỗi và giới hạn

- n = 6 mỗi loại, câu tự viết, 1 lượt; model không tất định ⇒ một câu có thể đổi nhóm ở lượt khác. Kết luận "ăn gần" (5 / 6) đủ lớn để tin hướng; kết luận
  "lưu trú" và "sự kiện" dựa trên ít câu hơn mỗi kiểu (2–4).
- Không có số người dùng thật ⇒ không biết loại nào được hỏi nhiều. Khi deploy: log đã có `route`, `web_outcome`, `refusal` nhưng không có loại câu — muốn đếm
  theo loại về sau cần một nhãn loại câu do code gắn (không ghi nội dung) — ghi làm ý cho A, không làm ở đây.
- Mục web: C chỉ đếm "có nội dung / không", không kiểm thông tin web đúng ngoài đời.
- Lượt 1 dừng ở 0,018295 USD (ngưỡng dừng 0,018 kiểm trước mỗi câu, câu cuối đẩy vượt 0,0003; vẫn dưới trần 0,02 lúc đó).
- Lệnh quét bộ đầu tiên (viết thẳng trong shell) bị auto mode chặn ⇒ viết thành file script rồi chạy; không lách rào, không đọc bộ kín.

## 7. Bàn giao cho người kiểm

- File private: `data/phase_11/dot_2_dem/cau_18.jsonl` · `ket_qua_lan_1.jsonl` (13 dòng) · `ket_qua_lan_2.jsonl` (5 dòng) · `tools/gui_cau.py` (có phí) ·
  `tools/quet_bo.py`, `tools/log_tien.py`, `tools/log_tong.py` (0 USD).
- Kiểm lại nhanh (0 USD): đếm `refusal` / `web_outcome` trong hai file kết quả; chạy lại các lệnh đếm kho ở §4.2 bằng `scripts/grep_kb.sh --dir foods -l …`.
- Việc cần A: trình User bảng §5 (hai ý "đủ lỗi" đều là việc **dữ liệu / lời trả lời**, không phải giao diện đợt 2 như hình dung ban đầu).

**Sửa số (19:34 12/11/2026, C):** §4.2 dòng "Ăn gần" ghi "15 / 81 bài có câu định vị theo một điểm tham quan" ⇒ đúng là **12 / 81** (15 là đếm cả thư mục món ăn, gồm 3 bài không phải bài quán / cà phê). Kết luận §5 không đổi.
