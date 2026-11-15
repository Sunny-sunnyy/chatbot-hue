# Implementation Report: đo bù ghi kho 4 / 5 / 6 (65 câu có top 10 đổi)

Người làm: B (Claude Code, Opus 5.5, terminal `hue-rag-b2`)
Date: 09:41 15/11/2026
Việc: `CURRENT_HANDOFF.md` mục "Việc đầu phiên sau" số 0 (A giao 15/11, quyền phiên "như tối 14/11").

## 1. Phạm vi

Ba lần ghi kho tối 14/11 (4, 5, 6) chỉ chạy lại câu Golden có **đoạn bài mới** trong top 10 (3 + 3 + 2 câu). Luật "đo đúng chỗ đổi"
(User 15:03 14/11) tính câu chạm là **mọi câu có top 10 đổi** ⇒ bỏ sót. Đo bù: Golden ×1 trên **65 / 158 câu** có top 10 T1 kho 6
(`aa34d4215f15`) khác top 10 lượt đủ 176 câu sau ghi kho 2. Trong 65 câu không có câu ngoài kho nào. An toàn 32 và 18 câu ngoài kho đã chạy trên đúng kho 6 nên không chạy lại.

Tiêu chí (ghi trước, theo TIEU_CHI kho 4–6 + tin A): 0 lỗi kỹ thuật · từ chối nhầm ≤ mốc + 1 · 0 lỗi trích dẫn mới · câu có chữ trả lời
khác mốc ⇒ agent con chấm mù cùng ý / khác ý; khác ý mà bản sau kém ⇒ báo A.

## 2. Thay đổi chính

Không đổi code, kho hay chỉ mục. Hai script mới trong `data/sua_kho_2026-11-14_do_bu/tools/` (private):
- `do_bu.sh` — đọc 65 câu từ `data/sua_kho_2026-11-14_ghi_kho_6/bu_doi.json`, dừng nếu ≠ 65 câu hoặc đích đã có (không ghi đè), `DRY=1` dừng trước lượt có phí.
- `so.py` — so với mốc `data/sua_kho_2026-11-14_ghi_kho_2/sau/golden.jsonl`, đếm sàn, dựng file chấm mù (thứ tự X / Y xáo, khoá riêng).

## 3. Cách đã chạy thật

```bash
DRY=1 bash data/sua_kho_2026-11-14_do_bu/tools/do_bu.sh   # 0 USD: 65 câu, đích mới
bash data/sua_kho_2026-11-14_do_bu/tools/do_bu.sh         # có phí; HEAD 6c7c01b, cờ theo settings.yaml (như mốc)
python3 -I data/sua_kho_2026-11-14_do_bu/tools/so.py
```
Agent con (ngữ cảnh mới) chấm 57 cặp từ `cham/cap_mu.jsonl`, không mở `cham/khoa.json`; kết quả `cham/ket_qua.jsonl`.

## 4. Kết quả quan sát — ĐẠT

| | Mốc (sau ghi kho 2) | Sau (kho 6) | Sàn |
|---|---|---|---|
| Lỗi kỹ thuật | 0 | 0 | 0 — đạt |
| Từ chối | 2 | 1 | ≤ 3 — đạt (0 từ chối mới; 1 câu hết từ chối) |
| Lỗi trích dẫn | 0 | 0 | 0 mới — đạt |

- Chữ trả lời giống hệt mốc 8 / 65; khác 57 ⇒ chấm mù: **56 cùng ý, 1 khác ý**. Câu khác ý duy nhất (loại hỏi một con số cụ thể):
  mốc từ chối, bản sau trả lời đúng như đáp án mẫu ⇒ **tốt lên**. Một cặp sát ranh giới (loại hỏi có / không) agent con xếp cùng ý;
  mở khoá thì bên nói rõ hơn là bản sau.
- Nhiều cặp "cùng ý" là cả hai bản cùng thiếu một ý của đáp án mẫu (4 cặp) — thiếu có từ trước, không do kho mới.
- **Kết luận:** ba lần ghi kho tối 14/11 không làm câu Golden nào tụt trên **mọi câu có top 10 đổi** (trước đây chỉ khẳng định được cho 8 câu có đoạn bài mới).
- Thời gian: lượt có phí 09:39:08 → 09:40:41 (1 phút 33 giây); chấm mù ~27 giây; 0 server.
- Tiền (từ file kết quả, cộng `usd` mỗi câu, gồm định tuyến): **≈ 0,029 USD** (phần sinh trả lời trong log: 0,0225). Agent con: quota Claude.
- Đường dẫn: `data/sua_kho_2026-11-14_do_bu/` (`sau/golden.jsonl`, `tom_tat.json`, `cham/`).

## 5. Lỗi và giới hạn

- Mốc là lượt sau ghi kho 2 ⇒ khác biệt gồm cả tác động ghi kho 3 và các merge 14/11 chạm mục web (luật số / năm); đo một lần ×1 nên
  khác chữ phần lớn là nhiễu sinh của model.
- Chấm cùng ý / khác ý do một agent con; chỉ 1 cặp khác ý, B đã tra khoá.

## 6. Đề xuất sửa mẫu TIEU_CHI ghi kho

`tools/cau_cham.py` (gói ghi kho): `cham = doi` — câu chạm = **mọi câu có top 10 T1 đổi** (kể cả chỉ đổi thứ tự), không chỉ câu có
đoạn bài mới; dòng "Câu chạm" của `TIEU_CHI.md` sửa theo. Mốc T1 so sánh = T1 của lượt có câu trả lời gần nhất, để những lần ghi chưa đo không cộng dồn bị sót.
