# Vì sao mục web hay rơi về câu cố định — đếm + nguyên nhân · B · 16:13 15/11/2026

A giao: ca gốc của User (hỏi tiếp giờ mở cửa) sau bản sửa `p9-web-noi-tiep` hết lạc đề nhưng 2 / 2 lần ra câu "chưa tra được thông tin đáng tin" (mã `so_ngoai_trich`); lượt đo đó 5 / 13 mục web là câu cố định.
**Chỉ đếm, chưa sửa gì.** Dữ liệu + công cụ (private): `data/web_kiem_so_2026-11-15/` (`tools/phan_loai.py`, `tools/lay_mau.py`, `cau_gio.json`, `mau_gio.jsonl`).

## Đã tra quyết định cũ (không đo lại)

- 14/11 tối: năm (19xx / 20xx) người dùng gõ được miễn — cứu 11 / 21 mục; giờ / ngày / số nhà người dùng gõ **cố ý không miễn** (review C).
- 14/11: tiền so theo giá trị (43 ⇒ 51 / 76).
- 15/11 sáng: bỏ số 0 đầu ("8/11" ↔ "08/11") — đếm cứu 0 / 76 ⇒ BỎ (`b_web_so_0_implementation.md`).

## Nguồn đếm

| Nguồn | Có chữ model viết + đoạn trích? | Số mục |
|---|---|---|
| (1) 76 mục web đã lưu 14/11 (38 câu × 2 bản), chấm lại bằng bộ kiểm HIỆN TẠI, có truyền câu hỏi | có | 76 |
| (2) Mẫu mới chiều nay: câu "giờ mở cửa / giờ lễ / giờ làm việc" kho thiếu — 7 câu một lượt + 1 cặp hỏi tiếp (đúng ca của User), cờ bật trên nhánh, tra web thật; bọc bộ kiểm để **ghi** chữ model + đoạn trích rồi gọi tiếp hàm thật | có | 9 |
| (3) 13 mục của lượt đo `quyet_r1` (5 câu cố định) | **không** — harness lượt đó chỉ lưu kết quả sau kiểm; log `chat_metrics` chỉ có mã | 13 |
| Log `chat_metrics` cũ | không có chữ (đúng thiết kế) ⇒ không phân loại (a)–(d) được | — |

## Kết quả

**(2) Mẫu giờ mở cửa: 9 / 9 mục QUA bộ kiểm, 0 câu cố định.** Ca của User lần này ra đúng nơi kèm giờ (và nói rõ các nguồn không thống nhất). 6 / 9 mục có nêu giờ cụ thể; 2 / 9 nói "chưa xác minh được" bằng chữ model (đạt kiểm); 1 / 9 là lượt đầu của cặp hỏi tiếp, không hỏi về giờ.
Model viết giờ theo đúng dạng đoạn trích hoặc dạng bộ kiểm đã coi là một ("8h00" ↔ "8:00", "08:00"); **0 lần bị chặn vì khác cách viết giờ**.

**(1) 76 mục cũ theo luật hiện tại: 62 đạt · 4 "chưa xác minh" (luật thời gian thực) · 10 câu cố định (13 %)**, chia theo lý do:

| Loại | Số mục (số câu hỏi khác nhau) | Là gì |
|---|---|---|
| (a) số không có trong đoạn trích, model tự đưa vào (bịa / suy) | **0** | — |
| (b) giờ CÓ trong đoạn trích nhưng khác cách viết (7h ↔ 7:00 ↔ 7 giờ) | **0** | — |
| (c) số model tự tính (cộng trừ, đổi đơn vị) | **0** | — |
| (d1) ngày / tháng **người dùng gõ** được model nhắc lại trong câu "chưa xác minh được …" | 4 (1 câu, 4 lần viết) | chặn theo thiết kế (quyết định 14/11: không miễn ngày người dùng gõ) |
| (d2) bộ tách chuỗi số ghép nhầm hai số cách nhau một dấu cách (kiểu "thứ … 9 giờ") | 1 (1 câu) | chặn nhầm do cách tách |
| (d3) số tiền viết rời chữ "đồng" ở cuối một liệt kê ⇒ bị coi là chuỗi số thường | 1 (1 câu) | chặn nhầm do ranh giới luật tiền ↔ luật số |
| luật tiền `tien_ngoai_trich` | 3 | ngoài phạm vi việc này (đã có bậc riêng 14/11) |
| `doan_khong_ma` (một đoạn văn thiếu mã nguồn) | 1 | lỗi trình bày của model |

**(3) Lượt đo trước (13 mục, 5 câu cố định: 3 `so_ngoai_trich`, 1 tiền + số, 1 luật thời gian thực): KHÔNG phân loại được** — không có chữ model viết. Chỉ biết: cùng ca của User, lượt đó 2 / 2 bị chặn, lượt lấy mẫu sau 1 / 1 qua ⇒ **kết quả dao động theo lượt** (đoạn trích Serper và chữ model đổi giữa các lần), chưa biết tỉ lệ thật.

## Kết luận

- **Giả thuyết "chặn nhầm vì cách viết giờ" không có bằng chứng: 0 / 85 mục có chữ.** Không đáng xây chuẩn hoá cách viết giờ lúc này (luật "đếm trước khi xây": không đủ lỗi).
- Số bịa lọt qua không đo ở đây; trong 10 mục bị chặn đọc được, **0 mục là số bịa** — bộ kiểm đang chặn chủ yếu vì cách tách / ngày người dùng gõ, không phải vì bắt được số sai.
- Tỉ lệ câu cố định do luật số: 6 / 76 (8 %) trên bộ cũ; 0 / 9 trên mẫu giờ; 3–4 / 13 trên lượt đo trước (không rõ lý do).

## Đề xuất (A / User chọn)

1. **Không xây gì cho "giờ mở cửa"** — ca của User đã ra được câu trả lời ở lượt lấy mẫu; lỗi lạc đề đã sửa ở nhánh `p9-web-noi-tiep`.
2. **Lưu chữ bị chặn để lần sau đếm được** (rẻ, không đổi hành vi): harness đo web luôn ghi chữ model + đoạn trích trước kiểm vào `data/` (như `lay_mau.py`). Không đưa chữ vào log server.
3. Nếu muốn biết vì sao 4 mục lượt trước bị chặn: chạy lại đúng 4 cặp đó × 2 lượt có ghi chữ (≈ 16 lượt, ≈ 0,04 USD) — B **chưa chạy** vì vượt mức A cho (≤ 10 lượt).
4. Ứng viên sửa nhỏ nếu sau này đủ lỗi (mỗi cái một bậc, giữ sàn "0 số ngoài đoạn trích lọt ra" bằng test ca bịa hiện có + đếm lại 85 mục): (d2) không ghép hai số qua dấu cách khi số sau đứng trước chữ chỉ giờ; (d3) số đứng trong liệt kê tiền tính theo luật tiền. Hiện mỗi loại mới 1 câu ⇒ chưa đủ để làm.

Tiền: mẫu giờ 9 lượt **0,0159 USD** (log lọc `git_sha 2b0be16`; mức A cho 0,03). Phân loại: 0 USD.
