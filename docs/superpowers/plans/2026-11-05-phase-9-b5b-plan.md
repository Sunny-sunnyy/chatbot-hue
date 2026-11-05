# Plan B5b — thời tiết Huế (`thoi_tiet`) + phương án ngày mưa trong lịch

Người viết: C · **bản 2** 13:34 05/11/2026 (`date`, review E vòng 1 `c836a12438de`) · bản 1 13:26 05/11/2026 (`date`, việc **C194**, A giao). Nền: `main` sau B5 (cờ `lich_trinh` bật khi User chấm Q3 đạt) + #6 (`5a8aa5e`). Nhánh `p9-b5b`.
File tracked, repo public: không chép kho / Golden / câu bộ đo; câu ví dụ tự viết.

**Lệch đề bài ↔ tài liệu (báo A):** spec Phase 9 **không có mục "§5 B5b"** (§5 chỉ có B0–B7). B5b được định nghĩa ở plan B5 §2c (b) + D9 (User chọn 03/11) và spec §11.1 / §11.4 / §11.5 (giữ bậc; lịch 01–07/12; luật cắt 07/12; tiền ≈ 0,05). Plan này lấy các chỗ đó làm căn cứ.

## Căn cứ để review (`WORKFLOW.md` §9.1 — file + hàm, không số dòng)

| File | Mục / hàm | Để kiểm gì |
|---|---|---|
| file này | toàn bộ | đủ ý A giao (nguồn, code gọi API, bão lũ, ý #10, không sự kiện theo ngày); tiêu chí ghi trước |
| plan B5 bản 7 `b572443dc9cd` | §2c, D9, D4b, D8, D12 | B5b đúng phương án (b) User chọn; dùng lại khối ghi chú + kiểm cuối |
| spec Phase 9 bản 12 `77250689e605` | §7 (bộ ba, đường ra), §11.1, §11.4, §11.5 | đường ra mới được rà; lịch / tiền |
| `data/phase_9/thoi_tiet/nghien_cuu.md` `b156a0667ee2` (C139) | §1 bảng, §3 đề xuất | Open-Meteo: không khoá, hạn mức, xác suất mưa theo giờ / ngày, ghi công CC BY 4.0; NCHMF không có API ⇒ chỉ là link chính thức |
| `CURRENT_HANDOFF.md` | ý #10 | cột trong nhà / nhiều bậc thang |
| `backend/llm/lich_trinh.py` | `khoi_ghi_chu`, `kiem_cuoi`, `tim_so_tien` (so_tien.py) | chỗ thêm dòng ngày mưa + kiểm số thời tiết |
| `backend/llm/assistant.py` | `_lich_extra`, `lich_trinh_for_turn`, `ROUTE_INPUTS` | chỗ đưa công cụ có điều kiện |

## 1. Mục tiêu và phạm vi

- **Vấn đề:** câu "mai Huế có mưa không", "cuối tuần này trời Huế thế nào" hôm nay chỉ trả được ý khí hậu chung trong kho (mùa mưa…), không có dự báo. Lịch B5 không nói mưa nắng (D9). LLM tự dự báo là bịa số.
- **Trong phạm vi:**
  - (1) câu hỏi thời tiết Huế trong 7 ngày tới ⇒ **code** gọi Open-Meteo, dựng câu số liệu cố định + nguồn + giờ cập nhật;
  - (2) lịch B5 có ngày đi trong 7 ngày ⇒ khối ghi chú thêm dòng dự báo từng ngày + **phương án ngày mưa** từ bảng v4;
  - (3) ý #10: bảng điểm v4 thêm cột trong nhà / ngoài trời + nhiều bậc thang (chỉ khi kho ghi; không ghi ⇒ để trống).
- **Ngoài phạm vi:** sự kiện theo ngày (Phase 11); cảnh báo bão / lũ tự động (NCHMF không có API — C139); dự báo > 7 ngày; nơi khác ngoài Huế.

## 2. Quyết định thiết kế

| Mã | Quyết định | Vì sao |
|---|---|---|
| **D1** | **Nguồn: Open-Meteo** (forecast API, không khoá). User 05/11 bỏ điều kiện giấy phép / phi thương mại; **vẫn ghi công** "Dữ liệu thời tiết: Open-Meteo.com (CC BY 4.0)" ở mọi câu có số. Không dùng `alerts` của nguồn quốc tế | C139 §3; một nguồn, không khoá ⇒ không thêm secret |
| **D2** | **Toạ độ Huế cố định trong code** (một điểm trung tâm thành phố) + `timezone=Asia/Ho_Chi_Minh` (để "ngày" của API khớp giờ Việt Nam — probe bước 3 kiểm); URL do code dựng, chỉ đổi **khoảng ngày**. Model **không** đưa gì vào URL | tham số model không vào URL (khung FDE §3) |
| **D3** | **Công cụ `thoi_tiet(tu_ngay, den_ngay)`**: tham số = số ngày tính từ hôm nay, enum 0–6. Code tính ngày từ `today_line` (giờ Việt Nam); hỏi > 6 ngày ⇒ model gửi giá trị lớn nhất; code thêm câu cố định "Mình chỉ có dự báo 7 ngày tới" (dò "tuần sau / tháng sau / dd/mm" ngoài khoảng) | model chỉ hiểu "mai / cuối tuần" ⇒ số; ngày cụ thể do code |
| **D4** | **Chỉ đưa công cụ khi code thấy từ khoá thời tiết** trong tin nhắn cuối **hoặc câu hỏi liền trước** trong lịch sử của cuộc (`trace.history`, đã có từ B3 — câu hỏi tiếp "còn chủ nhật?") (thời tiết, mưa, nắng, nhiệt độ, bão, lũ, trời, nóng, lạnh, độ ẩm, gió — so cả từ, không chuỗi con). Không khớp ⇒ danh sách công cụ như hôm nay | lượt khác (không từ khoá ở cả hai câu) **không đổi chuỗi gửi** ⇒ Q1m giống byte. Bỏ sót từ khoá ⇒ không công cụ, nhưng D8 vẫn chạy (không lọt số bịa). Đếm 05/11: Golden khớp **1 / 176**, an toàn **4 / 32** ⇒ hồi quy chỉ 5 câu |
| **D5** | **Code dựng câu số liệu** (khuôn cố định tiếng Việt): mỗi ngày "Thứ X dd/mm: a–b °C, khả năng mưa c %, lượng mưa d mm" + dòng nguồn + "cập nhật hh:mm dd/mm" (giờ API trả). Câu có buổi ("chiều nay", "sáng mai", "tối…") ⇒ thêm câu cố định "Đây là dự báo theo cả ngày, không riêng buổi bạn hỏi." (Open-Meteo có số theo giờ, nhưng bậc này chỉ dùng số ngày). Model chỉ viết lời quanh khối đó, **không thêm số** | khung FDE §2: số liệu ⇒ code |
| **D6** | **Bão / lũ:** câu có "bão / lũ / ngập" — hoặc "cảnh báo" **cùng** một từ thời tiết của D4 ("cảnh báo bậc thang", "cảnh báo đường trơn" thì **không**) ⇒ code luôn nối câu cố định trỏ **NCHMF** (link trang chính thức do code dựng) + **112**; nguy hiểm ngay ⇒ đường khẩn cấp hiện có (định tuyến B1) giữ nguyên | không tự cảnh báo; theo đường an toàn đã đo |
| **D7** | **Phục hồi:** gọi API timeout 3 s, **không thử lại**; lỗi / hết giờ / JSON sai schema / số ngoài miền hợp lệ (nhiệt −10…50, xác suất 0…100) ⇒ kết quả công cụ "chưa lấy được dự báo" + câu cố định trỏ NCHMF; không bao giờ đưa số khi lỗi. **Cache RAM 30 phút** cho cùng khoảng ngày | lỗi hạ tầng ≠ kết quả rỗng (khung FDE §3); hạn mức 10.000 / ngày ≫ nhu cầu |
| **D8** | **Kiểm cuối số thời tiết — chạy ở MỌI câu tuyến `tro_ly_hue` khi cờ bật** (có công cụ hay không — review E M-1): mọi số **dạng thời tiết** trong chữ model ∈ **{số code đưa} ∪ {số có trong các đoạn kho được trích ở lượt đó}** (như sàn tiền B5c spec §11.2 (1)). Dạng thời tiết: `°C`, `°`, `độ`, `độ C`, `%`, `phần trăm` (cạnh "mưa / ẩm"), `mm`, `mi-li-mét`, `li`; khoảng "24–30", "từ 24 đến 30"; số thập phân dấu phẩy. Code **làm tròn trước** khi dựng câu D5 (nhiệt độ nguyên, xác suất nguyên, mưa 1 chữ số thập phân) ⇒ tập cho phép gồm đúng chuỗi số code in. Có số từ công cụ mà thiếu dòng nguồn + giờ cập nhật ⇒ rút lại như citation hỏng | "0 số thời tiết không có nguồn" (plan B5 §2c); câu khí hậu trả từ kho (17 file kho có số kèm °C — E đếm) **không** bị rút nhầm vì số kho được trích nằm trong tập |
| **D9** | **Lịch có ngày đi** (code dò "mai", "ngày kia", "thứ X", "cuối tuần này", "dd/mm" trong 7 ngày — cùng chỗ `do_so.py`): `lich_trinh` gọi cùng hàm của D5 cho các ngày của lịch ⇒ khối ghi chú D4b thêm dòng dự báo từng ngày. Ngày có khả năng mưa ≥ 60 % ⇒ thêm "Nếu mưa: có thể thay <điểm ngoài trời> bằng <điểm trong nhà cùng cụm>" (từ bảng v4). Không dò được ngày ⇒ lịch như B5 (không nói thời tiết). **API lỗi** ⇒ lịch như B5 + câu cố định "chưa lấy được dự báo", 0 số (lịch không bao giờ hỏng vì thời tiết) | ý #10; khung lịch B5 **không đổi** (chỉ thêm dòng ghi chú) ⇒ tất định giữ |
| **D10** | **Bảng điểm v4** = v3 + `trong_nha` ∈ {`trong_nha`, `ngoai_troi`, `ca_hai`, null} + `bac_thang` ∈ {`nhieu`, null} + `*_can_cu` (đường kho + chữ ngắn). C soạn bằng `scripts/grep_kb.sh`; **kho không ghi ⇒ null, không suy**; User duyệt v4. `bac_thang: nhieu` + người đi cùng là người lớn tuổi ⇒ ghi chú "X có nhiều bậc thang (theo kho)" | ý #10; không khẳng định điều kho không ghi |
| **D11** | **Cờ `thoi_tiet: false`**. Log: có gọi API, ms, lỗi (mã), số ngày; không chữ người dùng | như các bậc trước |

## 3. Thay đổi theo file (dự kiến)

`backend/llm/thoi_tiet.py` (mới: gọi API **async** — `httpx.AsyncClient` hoặc `asyncio.to_thread`, không chặn vòng sự kiện của luồng SSE khác — cache, schema, dựng câu D5, kiểm D8) · `tests/test_assistant_boundary.py` (thêm `"llm.thoi_tiet"` vào `ALLOWED` với gói mạng nó dùng + 1 dòng lý do: module duy nhất gọi Open-Meteo) · `assistant.py` (công cụ có điều kiện D4, nối `_finish_generated`) · `generator_openai_full_corpus.py` (công cụ) · `full_corpus_prompt.py` (`THOI_TIET_MO_TA`) · `lich_trinh.py` + `do_so.py` (dò ngày, dòng ghi chú D9, D10) · `settings.yaml` (`thoi_tiet: false`, toạ độ, timeout) · `data/phase_9/lich_trinh/diem_v4.json` (private, User duyệt) · test `test_b5b_thoi_tiet.py`: **không gọi mạng** — phản hồi API ghi sẵn (fixture); ca lỗi / hết giờ / schema sai / số ngoài miền; ca model thêm số ⇒ bị bắt; ca từ khoá (khớp / không khớp, "trời ơi" ⇒ ghi là giới hạn; câu liền trước có từ khoá ⇒ đưa công cụ); **mỗi dạng số của D8 một ca** (°C, độ, %, phần trăm, mm, li, khoảng, thập phân); ca model tự viết số ở lượt **không có công cụ** ⇒ bị bắt; ca câu khí hậu trích kho có số ⇒ **không** bị rút; ca "cảnh báo bậc thang" ⇒ không nối NCHMF; ca API lỗi ở lịch có ngày ⇒ lịch B5 + câu cố định.

## 4. Tiêu chí ghi trước

| Mã | Loại | Tiêu chí | Đo bằng |
|---|---|---|---|
| **Q1** | sàn | cờ tắt ⇒ chuỗi gửi giống byte `main` (228 / 228) | `capture_all.py` |
| **Q1m** | sàn | cờ bật ⇒ mọi lượt **không có từ khoá** (ở cả tin nhắn cuối lẫn câu liền trước) giống byte cờ tắt; lượt có từ khoá chỉ khác một mục công cụ | `capture_q1m.py` (bỏ mục `thoi_tiet`) |
| **Q2** | sàn code, mọi câu, **2 lần chạy** | 0 số thời tiết ngoài tập code đưa · 100 % câu có số mang dòng nguồn + giờ cập nhật · câu bão / lũ có NCHMF + 112 · câu > 7 ngày có câu cố định, 0 số · khi API lỗi (fixture ở harness) ⇒ 0 số + câu cố định · lịch có ngày ⇒ dòng dự báo đúng ngày, khung lịch giống B5 · **câu không từ khoá / câu hỏi tiếp** (§5): 0 số thời tiết ngoài tập · câu khí hậu kho: 0 lần bị rút nhầm | harness đọc kết quả công cụ + chữ (tất định theo bản ghi API của lần chạy) |
| **Q3** | quyết | gọi `thoi_tiet` ở câu dự báo **≥ 9 / 10 mỗi lần** (2 lần); 0 lần gọi ở câu khí hậu chung (kho trả lời) | harness |
| **Q4** | sàn hồi quy | 5 câu có từ khoá (Golden 1 + an toàn 4), cờ tắt ↔ bật, 2 lần: Golden F1–F4 sạch; an toàn: 0 sai điều kiện / thiếu cảnh báo mới (judge 2 sub-agent mù) | `generate` + `sinh_an_toan.py --qids` |
| **Q8** | cổng | server thật: 1 câu dự báo + 1 lịch có "mai" + 1 câu thường; hiện ghi công Open-Meteo; log không chữ; CSP 0 (trình duyệt không gọi API ngoài) | như B5 Q8 |

**Kết quả âm:** Q2 phạm sau 2 vòng chỉnh hoặc Q3 dưới ngưỡng ⇒ cờ tắt; B5 giữ nguyên.

## 5. Bộ đo — C viết · **bộ kín: KHÔNG** (quyết ngay ở plan, luật 05/11 (2))

- **Lý do không có bộ kín:** sàn chính là code tất định (số ⊂ số code đưa, có nguồn). Phần model chỉ là chọn gọi công cụ, đo bằng bộ đã thấy chạy 2 lần (như ảnh Phase 10).
- **Đã thấy 16 câu:**
  - 10 câu dự báo: mai · ngày kia · cuối tuần · 7 ngày tới · "chiều nay có mưa không" · cách viết khác · không dấu;
  - 2 câu > 7 ngày;
  - 2 câu bão / lũ;
  - 2 câu khí hậu chung ("Huế mùa nào hay mưa") ⇒ kho trả lời, không gọi công cụ.
- **Thêm 4 lịch:** 2 có ngày trong 7 ngày (1 câu có người lớn tuổi + điểm nhiều bậc), 2 không có ngày.
- **Thêm 4 câu cho M-1 / m-2 (bản 2):** 2 câu thời tiết viết lạ **không có từ khoá** ("mai đi Huế có cần mang ô không?", "thứ bảy ra biển Thuận An được không?") ⇒ sàn: 0 số ngoài tập (gọi công cụ hay không chỉ theo dõi); 1 chuỗi "thời tiết mai?" ⇒ "còn chủ nhật?" (câu liền trước có từ khoá ⇒ có công cụ); 1 câu an toàn có "cảnh báo" không phải thời tiết ⇒ không nối NCHMF. Bộ đã thấy ⇒ **24 câu**.
- **Cỡ mẫu:** "≥ 9 / 10" chỉ thấy khác biệt lớn. Số dự báo đổi theo giờ chạy ⇒ sàn tính trên **bản ghi API của chính lần chạy** (harness lưu, private).

## 6. Bước làm

1. C soạn bảng v4 (cột D10 + căn cứ) ⇒ **User duyệt**; C viết bộ đo. 0 USD.
2. B code + test (fixture, không mạng) ⇒ Q1, Q1m. 0 USD.
3. Probe 1 lần gọi Open-Meteo thật (0 USD) ⇒ kiểm schema + giờ cập nhật.
4. Đã thấy × 2 ⇒ chỉnh ≤ 2 vòng ⇒ khoá ⇒ Q4 ⇒ Q8 ⇒ review cả nhánh (≤ 2 vòng) ⇒ A merge.
- W31: không chạy cùng lượt đo tốc độ.

## 7. Tiền

- Đã thấy 24 câu × 2 lần × ≈ 0,0008: ≈ **0,038** (vòng chỉnh 2 chỉ chạy câu hỏng: ≈ 0,01).
- Q4 5 câu × 2 bên × 2 lần: ≈ 0,008.
- Q8 + probe: ≈ 0,003. Open-Meteo 0 USD.
- **Cộng ≈ 0,05–0,06.** Trần **0,07**, dừng **0,065** (bản 2: +4 câu). Spec §11.5 ước 0,05.

## 8. Điều kiện dừng (báo A)

- Q1 / Q1m khác byte.
- Chạm 0,065 USD.
- Probe Open-Meteo trả schema khác tài liệu, hoặc điều khoản đổi.
- Bảng v4 User chưa duyệt.
- Kiểm cuối D8 rút lại > 2 / 24 ở đã thấy (rào quá chặt ⇒ xem lại trước khi chạy tiếp).
- B5 Q3 âm (D9 dựa trên lịch B5).

## 9. Rà agent design / security (phần chạm B5b)

| Mục khung | Hiện trạng (file + hàm) | B5b | Khớp / lệch | Đề xuất |
|---|---|---|---|---|
| §1 có cần agent | `assistant.py` trợ lý + công cụ | câu dự báo gần luồng cố định; model chỉ hiểu "mai / cuối tuần" ⇒ số ngày; còn lại code | khớp | — |
| §2 số liệu ⇒ code | `so_tien.py` `tim_so_tien` (kiểu kiểm số của B5c); `lich_trinh.py` `kiem_cuoi` | số, nguồn, giờ cập nhật, câu bão lũ, câu > 7 ngày, câu "theo cả ngày" do code (D5, D6); D8 mọi câu `tro_ly_hue` | khớp sau bản 2 | dùng chung bộ dò số với B5c |
| §3 tham số vào URL | — | model chỉ gửi enum 0–6; toạ độ + múi giờ + URL do code (D2, D3) | khớp | — |
| §3 lỗi hạ tầng ≠ rỗng | — | lỗi API ⇒ câu cố định, không trả lời như "không mưa"; lịch có ngày ⇒ lịch B5 + câu cố định (D7, D9) | khớp | — |
| §4 trần + phục hồi | `ASSISTANT_MAX_TURNS` 4 | 1 lần gọi / lượt, timeout 3 s, không thử lại, cache 30 phút, gọi async | khớp | — |
| §5 trí nhớ / lời dặn | `assistant.py` `ROUTE_INPUTS` gồm `history` (cổng D4 xét câu liền trước — đã có) | không trí nhớ mới; không thêm lời dặn hệ thống | khớp | — |
| security: **đường ra mới** | `tests/test_assistant_boundary.py` `ALLOWED` (2 module được gọi mạng) | Open-Meteo: yêu cầu chỉ có toạ độ cố định + khoảng ngày ⇒ **không chữ người dùng ra ngoài**; phản hồi qua schema chặt, chỉ lấy số, **không đưa chữ của API vào model** | khớp | thêm `llm.thoi_tiet` vào `ALLOWED` có lý do; ghi spec §7 lúc merge |
| security: trước deploy | spec §7 "Trước khi deploy" | đọc lại điều khoản Open-Meteo khi lên AWS; IP AWS dùng chung hạn mức | đầu vào Phase 12 | — |

## 10. Rủi ro

- **Dò từ khoá** bỏ sót câu hỏi thời tiết không có từ khoá ⇒ không có công cụ ⇒ trả từ kho / từ chối, **nhưng D8 vẫn chặn số bịa** (bản 2). Thêm từ vào D4 chỉ qua vòng chỉnh có đo.
- **Độ chính xác:** lưới ~27 km, mưa miền Trung khó dự báo (C139 §2) ⇒ luôn có câu "dự báo có thể đổi".
- **Bảng v4:** kho có thể ít ghi trong nhà / bậc thang ⇒ nhiều ô null ⇒ ít phương án ngày mưa. Chấp nhận (không suy).

## Chỗ đổi bản 2 (13:34 05/11/2026)

Theo review E vòng 1 (`…b5b-plan_review.md` `c836a12438de`):
- **M-1:** D8 chạy ở **mọi** câu `tro_ly_hue` khi cờ bật; tập số cho phép = số code đưa ∪ số trong đoạn kho được trích (như B5c); thêm 2 câu không từ khoá + ca câu khí hậu kho (§5, Q2).
- **m-1:** danh sách dạng số + làm tròn trước khi dựng tập.
- **m-2:** cổng xét cả câu hỏi liền trước.
- **m-3:** "cảnh báo" chỉ tính khi đi cùng từ thời tiết.
- **m-4:** gọi async + thêm `llm.thoi_tiet` vào `ALLOWED` của test rào.
- **m-5:** câu "dự báo theo cả ngày"; `timezone=Asia/Ho_Chi_Minh`; đường lỗi API ở lịch.
- **m-6:** §9 thêm cột hiện trạng / đề xuất.
- Bộ đã thấy 20 ⇒ 24 câu; tiền ≈ 0,05–0,06, trần 0,07 / dừng 0,065. Không đổi: D1, D3, D7, D10, D11, Q1, Q3, Q4, Q8, bộ kín không.
