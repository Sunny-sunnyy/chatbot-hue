# Implementation Report: Phase 8.2 §10 R4 — thước "số trong câu trả lời có trong đoạn được trích"

Người làm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 21:46 +0700 (`date`)
Việc: C39 (`CURRENT_HANDOFF.md` mục "Việc giao phiên tối 26/10"). Căn cứ: spec 8.2 §10.3 dòng R4 (bản duyệt `09e8f3932ede`), C37 §3.
**0 USD**: không gọi API, chỉ đọc câu trả lời đã lưu. **Không commit**; người kiểm: B.

## 1. Phạm vi

R4 là **thước theo dõi, không chặn**. Với mỗi câu trả lời đã lưu, nó liệt kê các con số không có trong câu hỏi và không có trong nguồn được
trích. Thước dùng làm chỉ số theo dõi `unsupported claim` cho R1–R3 (spec §10.5). Thước không đổi chatbot, không đổi validator production.

## 2. Thay đổi

| File | Mục đích |
|---|---|
| `backend/experiments/phase_8_2/r4_numbers.py` (mới) | Gồm: hàm thuần `normalize_number` / `number_tokens` / `unsupported_numbers`; `check_file` dựng lại đúng context model đã thấy; lệnh chạy trên file JSONL đã lưu |
| `backend/experiments/phase_8_2/__init__.py` (mới, rỗng) | Gói `experiments.phase_8_2`. Nhánh `p82-b1` cũng thêm đúng file rỗng này, nên khi merge sẽ không xung đột (add / add cùng nội dung) |
| `backend/tests/test_r4_numbers.py` (mới) | 6 test logic thuần, chuỗi tự viết (không lấy từ kho) |

**Luồng:**
1. Đầu vào: câu trả lời đã lưu (`answer`, `top_chunk_ids`, `context_sources`, `input_tokens`).
2. Chunker production (`chunk_full_corpus`) cho ra `RetrievedDocument` (`build_retrieved_document`).
3. **Context builder production** (`build_context_builder(settings, max_documents=10)`) cho ra `PackedSource` 1..10.
4. Lấy các nguồn mà câu trả lời trích (`CITATION_PATTERN` của `llm/citations.py`, bắt cả `[n]` lẫn `[Nguồn n]`).
5. So số. Kết quả ghi `data/phase_8_2/r4/<tên file>.jsonl`, private; file đã có thì **từ chối ghi đè** (như `b1.py` / `k1.py`; B47 review).

Thước dùng lại code production ở mọi khâu, không dựng đường đi thứ hai.

**Quy tắc số** (C37 §3):
- token là chuỗi chữ số, có thể có `.` `,` `:` ở giữa;
- dấu gạch / "–" tách khoảng số thành từng số, nên "3–5" khớp được "3 đến 5";
- bỏ dấu ngăn nghìn ("95.000" = "95,000" = "95000"); "2,5" thành "2.5"; "08:00" thành "8:00";
- bỏ nhãn citation;
- số có trong câu hỏi thì không tính;
- câu từ chối, câu lỗi, câu không trích nguồn thì không kiểm.

**Kiểm "context dựng lại = context model đã thấy":** số nguồn phải bằng `context_sources`. Thêm vào đó, `input_tokens` đã lưu (số provider
đếm) trừ số của builder phải là **một hằng số cho mọi câu** trong file. Khác thì dừng. Lần chạy đầu so bằng nhau tuyệt đối và dừng ở câu đầu:
lệch đều +30 token (khung tin nhắn phía provider). C đổi phép kiểm sang "một độ lệch chung" và ghi lý do trong comment.

## 3. Cách đã chạy thật

Từ `backend/`:

```bash
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_r4_numbers.py -q
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.r4_numbers ../data/phase_8_1/g2/g2_context10.jsonl
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.r4_numbers ../data/phase_8_2/b1/b1_dev.jsonl \
    ../data/phase_8_2/b1/b1_test.jsonl ../data/phase_8_1/g2/t_context10.jsonl
```

Mỗi lượt khoảng 30–45 s (chia đoạn toàn kho). Mọi file qua phép kiểm context: 10 / 10 nguồn, một độ lệch token chung.

## 4. Kết quả quan sát

**Kiểm thước** trên 5 ca C36 đã biết (G2.1a dev). Tiêu chí ghi trước ở handoff dòng C39: bắt 2 / 2, báo nhầm ≤ 1 / 3.

| Ca (C36) | Loại đã biết | R4 | |
|---|---|---|---|
| 155 | lỗi thật: phép tính chênh lệch sai | bị cờ (2 số) | ✓ bắt |
| 51 | lỗi thật: năm nằm ở đoạn không trích | bị cờ (1 số) | ✓ bắt |
| 30 | báo nhầm: số tự tính đúng | bị cờ | ✗ báo nhầm |
| 93 | báo nhầm: "3–5" / "3 đến 5" | không cờ | ✓ (tách khoảng số) |
| 143 | báo nhầm: số lấy từ câu hỏi | không cờ | ✓ (bỏ số trong câu hỏi) |

⇒ **Bắt 2 / 2, báo nhầm 1 / 3 — ĐẠT** tiêu chí ghi trước. **Nhưng đây là đạt trên mẫu đã thấy:** chính 5 ca này đã dùng để chọn quy tắc
(tách khoảng số vì 93, bỏ số trong câu hỏi vì 143). Đạt ở đây không nói gì về độ chính xác ngoài mẫu (B47 m-1). Ngoài mẫu, xem bảng dưới.

**Chạy trên mốc** (chỉ số câu; test chỉ đếm):

| File | Câu | Bị cờ | `case_index` | Phân loại (chỉ dev) |
|---|---:|---:|---|---|
| G2.1a dev `g2_context10` | 120 | 4 | 30, 51, 155, 172 | thật 2 (51, 155); nhầm 2 (30, 172: số tự tính đúng) |
| B1 dev `b1_dev` | 120 | 4 | 30, 137, 155, 172 | **thật 0; nhầm 4** (30, 137, 155, 172: số tự tính **đúng**). Câu 155 ở B1 viết lại câu trả lời và tính đúng cả ba hiệu số, khác lượt G2.1a. Câu 51 ở B1 trích đúng đoạn có năm đó ⇒ không cờ, đúng |
| B1 test `b1_test` | 56 | 1 | 114 | không đọc (test). Câu 114 thuộc nhóm `unnatural`, nằm ngoài số chính |
| G2.1a test `t_context10` | 56 | 1 | 114 | không đọc (test) |

- Test: **6 passed**.
- **Ý nghĩa:**
  - Thước bắt đúng hai loại lỗi mà judge chỉ trừ 1 điểm hoặc không trừ: tính sai, trích lệch đoạn.
  - Báo nhầm dồn vào **một loại duy nhất**: số model tự tính đúng (hiệu hai giá, hiệu hai mốc giờ).
  - **Ngoài mẫu kiểm thước** (câu 172 của G2.1a + 4 câu cờ của B1 dev): **0 / 5 câu là lỗi thật**. Cả 5 đều là số tự tính đúng. Vì vậy thước chỉ
    là **danh sách để người đọc lại**, không dùng làm chỉ số tự động. Giá trị chính: lỗi thật đã biết (51, 155 ở G2.1a) đều bị bắt.
  - Số câu bị cờ thấp (≤ 4 / 120): đọc lại tay rẻ.
- **Không vá báo nhầm "số tự tính".** Cho phép "hiệu / tổng của hai số trong nguồn" thì câu 155 cũng lọt: khoảng sai 100.000–700.000 gồm
  đúng những hiệu của các số trong nguồn. Như vậy sẽ mất đúng lỗi mà thước sinh ra để bắt.

## 5. Lỗi và giới hạn

- **Chỉ xét con số.** Tên riêng, điều kiện, phủ định không kiểm (C37 §3, báo cáo ChatGPT C1). Một câu trả lời sai chủ thể nhưng đúng con số
  sẽ lọt.
- Số nhỏ một chữ số dễ "có trong nguồn" một cách tình cờ, nên thước dễ bỏ lọt ở loại số này. Số viết bằng chữ ("hai mươi nghìn") không bắt.
  Giờ kiểu "8h" không khớp "08:00".
- Kiểm thước chỉ trên 5 ca đã biết (một người gắn nhãn, C36; cũng là ca dùng để chọn quy tắc). Ngoài ra đọc thêm 4 câu dev (137, 172, và 30,
  155 ở B1). Chưa có mẫu lớn có nhãn người.
- Test chạy theo `rootdir` gốc repo như các test khác (`Project_Status.md` §8). Không cần key.

## 6. Người kiểm nên chạy lại

1. `pytest tests/test_r4_numbers.py` (≈ 9 s).
2. Lệnh `r4_numbers` trên `g2_context10.jsonl` ⇒ đúng `[30, 51, 155, 172]`. So bảng §4 với `data/phase_8_2/r4/*.jsonl`.
3. Đọc `r4_numbers.py:check_file`: phép kiểm context có đủ chặt không (một độ lệch token chung cho 120 câu).

Tiền: 0 USD. Không sub-agent.

## 7. Sửa sau review B47 (21:57 26/10/2026 +0700, `date`)

| Finding | Sửa |
|---|---|
| m-1 kiểm thước trên mẫu đã thấy | §4 ghi rõ "đạt trên mẫu đã thấy"; precision ngoài mẫu tính riêng: **0 / 5** |
| m-2 nhãn 137 / 172 | C đọc lại bằng máy + đọc chữ: số bị cờ **có** ở nguồn khác của context, nhưng là **số khác nghĩa trùng giá trị**. Ở 172 là khoản tiết kiệm vé gộp, ở 137 là "2 km". Số trong câu trả lời là hiệu tự tính **đúng** ⇒ nhãn **giữ** "số tự tính đúng", không phải trích lệch đoạn kiểu 51. Đọc thêm phát hiện **155 ở B1 tính đúng** ⇒ bảng §4 sửa B1 dev từ "thật 1" thành **thật 0 / nhầm 4** |
| B47: `main()` ghi đè `data/phase_8_2/r4/` | thêm từ chối ghi đè trước khi chia đoạn (kiểm: chạy lại trên `g2_context10.jsonl` ⇒ `output exists (không ghi đè)`); test vẫn **6 passed** |
