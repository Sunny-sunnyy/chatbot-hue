# C48 — Lỗi "nói chắc sai" về con số trong chatbot hiện tại (đo hiện trạng, B1 dev)

Người làm: C (Claude Opus 5.5, `hue-rag-5b`) · 2026-10-27 09:09 +0700 (`date`) · Việc: C48 (A giao). **0 USD**, không gọi API: đọc câu trả lời đã
ghi của mốc B1 (context 10, `data/phase_8_2/b1/b1_dev.jsonl`). Chỉ nhóm dev 120; không đọc test từng câu, không mở câu kín. File không chép câu
hỏi, câu trả lời hay nội dung kho — chỉ `case_index` và số đếm.

## Cho bạn (3 dòng)

- Trong 99 câu dev chatbot trả lời (68 câu có con số: giá, giờ, năm, khoảng cách), **không tìm thấy câu nào nói sai một con số** so với đoạn nó trích.
- Máy bắt cờ 4 câu, nhưng đọc lại thì **cả 4 là phép tính đúng** (hiệu hai giá, hiệu hai giờ) — con số đó không có nguyên văn trong nguồn nên máy
  nghi. Đọc thêm 10 câu không bị cờ (chọn ngẫu nhiên): 10 / 10 đúng số, đúng đối tượng.
- Nghĩa là ở mốc hiện tại, "nói chắc sai về số" **hiếm** (0 câu thấy được trên 68). Giới hạn: chỉ đo số, chỉ dev; lỗi sai chữ (tên, sự kiện) chưa đo.

## 1. Cách đo

Script private `data/cai_tien_tung_khau_2026-10-26/c48/c48_numbers.py` (chạy từ `backend/` của working tree chính: `HF_HUB_OFFLINE=1 PYTHONPATH=. uv run
python ../data/cai_tien_tung_khau_2026-10-26/c48/c48_numbers.py`; kết quả theo câu `c48_b1_dev.jsonl`, tổng `c48_summary.json`; từ chối ghi đè).

- **Dùng lại R4** (`backend/experiments/phase_8_2/r4_numbers.py`, `2c7ecfd`): chuẩn hóa số (`95.000` = `95,000` = `95000`; `08:00` = `8:00`; khoảng
  `3–5` tách hai số), bỏ số có trong câu hỏi, dựng lại đúng 10 đoạn model đã thấy từ `top_chunk_ids` (kiểm số nguồn bằng nhau mọi câu và độ lệch
  token một hằng số: 30).
- **Chặt hơn R4 ở một chỗ:** R4 cho mỗi số dùng **mọi** nguồn câu trả lời trích. C48 cho mỗi **câu** (tách theo dòng rồi dấu kết câu) chỉ dùng nguồn
  chính câu đó trích. Câu không có `[n]` mượn citation của câu kế tiếp cùng dòng, không có thì câu trước cùng dòng (model hay đặt `[n]` cuối đoạn).
- Mỗi số không thấy trong nguồn của câu xếp một nhóm: **không có ở đoạn nào** (bịa / tự tính / viết khác dạng) · **có ở đoạn không được trích** (trích
  sai đoạn) · **có ở nguồn trích ở câu khác** (gán lệch câu) · **câu không có citation**.

## 2. Kết quả (script in, `c48_summary.json`)

| | Số câu |
|---|---:|
| dev | 120 |
| chatbot trả lời (không từ chối) | 99 |
| câu trả lời có ≥ 1 con số | 68 |
| **câu có ≥ 1 số không thấy trong đoạn câu đó trích** | **4** (30, 137, 155, 172) — 6 số |
| — số không có ở đoạn context nào | 1 câu / 1 số (30) |
| — số có ở đoạn không được trích | 3 câu / 5 số (137, 155, 172) |
| — số có ở nguồn trích ở câu khác | 0 |
| — số nằm trong câu không có citation | 0 |

Bốn câu bị cờ trùng đúng 4 câu R4 đã cờ trên cùng file (`phase_8_2_r4_implementation.md` §4). Đo theo câu không thêm cờ nào: chỉ **2 / 68** câu trả lời
có số mà một câu dùng ít nguồn hơn cả câu trả lời (model đặt `[n]` ở cuối dòng, gần như mỗi dòng một ý) ⇒ ở mốc này đo theo câu ≈ đo theo câu trả lời.

## 3. Đọc tay

Ghi chép private `data/cai_tien_tung_khau_2026-10-26/c48/doc_tay.md`.

- **6 / 6 số bị cờ là báo nhầm**, cùng một dạng: model **tự tính đúng** hiệu hai số có trong nguồn được trích (hiệu hai giá: 30, 172; hiệu hai mốc giờ:
  137; ba hiệu của hai khoảng giá: 155). Nhóm "có ở đoạn không được trích" của 137 / 155 / 172 cũng là nhầm: số kết quả phép tính **tình cờ** có ở một
  đoạn khác (một khoảng cách, một mức tiết kiệm combo) ⇒ với số tự tính, cách xếp nhóm của máy không đáng tin.
- **Mẫu không bị cờ** (seed 20261024, 10 / 64 câu có số: 1, 9, 25, 38, 44, 80, 101, 124, 128, 156): đọc từng số với đoạn được trích — **10 / 10 đúng số và
  đúng đối tượng** (không có dạng "số có trong nguồn nhưng gắn nhầm món / ngày / nơi").
- Báo nhầm 6 / 6 trên đủ các cờ (không chỉ ~10 mẫu như A dự tính: chỉ có 6 cờ).

## 4. Kết luận và giới hạn

- **Quan sát:** ở mốc B1 dev, lỗi "nói chắc sai về số" bắt được bằng máy = **0 / 68** câu có số; mẫu đọc tay không thấy lỗi gắn nhầm (0 / 10).
  *Suy ra* (không chứng minh): lỗi này hiếm ở mốc hiện tại — với 0 / 10 trong mẫu, cận trên thô (luật "3 / n") ≈ 30 % cho phần không bị cờ, nên mẫu chưa
  đủ để nói "gần 0". Trước đây (G2.1a, cùng context 10) R4 bắt 2 lỗi thật (51 năm ở đoạn không trích; 155 tính sai) — ở B1 cả hai câu đó trả lời đúng ⇒
  lỗi số **có xảy ra, nhưng dao động giữa các lượt**, nên một lượt không đủ để ước tỉ lệ.
- **Thước số chỉ là danh sách đọc lại** (như R4): mọi cờ ở mốc này là phép tính đúng; thước không bắt được số đúng có trong nguồn nhưng gắn nhầm đối
  tượng (chỉ đọc tay mới thấy).
- **Chưa đo:** sai về chữ (tên, sự kiện, quan hệ), nhóm test, câu kín, câu không tự nhiên tách riêng. Nhãn đọc tay do **một người** (C).
- **Gợi ý cho A (đề xuất):** nếu "nói chắc sai" là lỗi tệ nhất, cách đo hữu ích hơn là (1) chạy thước này trên **mọi** lượt mới (R1, K3) để thấy lỗi
  dao động như 51 / 155; (2) đọc tay theo mẫu có seed cả câu trả lời **không có số** (sai chữ) — việc riêng, chưa làm.
