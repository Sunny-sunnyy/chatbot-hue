# Implementation Report: Phase 8.2 B0 — chuẩn bị file đọc cặp mù

Người làm: A (Claude Opus 5.5, terminal `hue-rag-00`)
Date: 2026-10-25 16:24 (`date`); vòng 2 16:3x sau review B24 (`phase_8_2_b0_prep_review.md` F1–F3)
Canonical guide: spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` (sha `dabae90b2b60`) §3.3, §3.4, §5 B0

## 1. Phạm vi

Chỉ phần **chuẩn bị** B0: chọn mẫu, xếp X / Y, giữ mù hình thức, kiểm mù bằng code. Chưa đưa User; chưa tóm nhãn; chưa áp
luật dừng (cần nhận xét của User). 0 USD, không gọi API, không đổi code / chatbot.

## 2. Thay đổi chính (toàn bộ private, không commit)

- `data/phase_8_2/b0/tools/make_pairs.py` (sha `b8ecd4177d0d`, vòng 2) — script tạo file.
- `data/phase_8_2/b0/doc_cap_mu.md` (sha `37b66efb3499`, vòng 2) — file đưa User: 20 câu, mỗi câu câu hỏi + X + Y + nguồn được trích +
  chỗ trống "Nhận xét" / "Bên hơn (không bắt buộc)".
- `data/phase_8_2/b0/khoa.json` (sha `5b9240842b7b`) — khóa: câu → `case_index`, dev / test, bên nào context 10, tầng, chênh
  Completeness. **Chỉ A giữ; không đưa User, không đưa sub-agent tóm nhãn.**
- `data/phase_8_2/b0/mau.json` — seed, quota, cỡ từng tầng.

## 3. Cách đã chạy thật

```bash
uv run python -I data/phase_8_2/b0/tools/make_pairs.py
```

Đầu vào: câu trả lời thật G2 8.1 (`data/phase_8_1/g2/g20_baseline.jsonl`, `g2_context10.jsonl`, `t_baseline.jsonl`,
`t_context10.jsonl`); điểm judge cùng lượt mù (`data/phase_8_1/g2/judge/`, `judge_test/`, ánh xạ qua `map.json`); Golden
chính thức (câu hỏi, loại); nhãn độ tự nhiên `data/phase_8_1/golden_realism_final.jsonl`.

## 4. Kết quả quan sát

- **Lọc:** bỏ câu `out_of_scope`, câu `unnatural`, cặp cả hai từ chối, cặp chữ giống hệt. Cỡ tầng (chênh Completeness
  context 10 − context 5): 10 hơn **15**, hòa **93**, 10 kém **3**.
- **Mẫu (seed `20261025`):** 10 hơn 10, hòa 7, 10 kém 3 = **20 câu**; dev 12 / test 8. Tầng "10 kém" chỉ có 3 câu ⇒ bù 1 câu từ
  tầng hòa (spec §3.3 "còn lại hòa hoặc 10 kém"). ⇒ tối đa **13 cặp judge khác nhau** cho luật "≥ 5 cặp quyết" (§3.4).
- **Kiểm mù (in bởi script):** 40 câu trả lời; số citation lớn nhất trong file `[3]`; số nguồn hiện nhiều nhất 3; **0** câu trả lời có
  số citation > số nguồn hiện kèm; context 10 nằm ở X **12 / 20** câu.
- **Vòng 2 (B24 F1):** model viết cả `[n]` (441 lần trong 4 file G2) lẫn `[Nguồn n]` (24 lần) — vòng 1 chỉ bắt `[n]` ⇒ câu 17 lộ
  `[Nguồn 8]`, câu 8 không đánh số lại. Sửa: bắt cả hai dạng (không phân biệt hoa thường, sau NFC), xuất `[k]`; kiểm mù thêm quét
  **mọi ngoặc vuông có số** và chữ "nguồn <số>" trong câu trả lời ⇒ **0**. Mẫu và khóa không đổi (`khoa.json` sha `5b9240842b7b` như vòng 1).

## 5. Lỗi và giới hạn

- **Lệch nhỏ spec §3.3:** xếp X / Y bằng script (seed `20261025`, `random.Random`) thay vì "một sub-agent không thấy điểm judge".
  Lý do: tái lập được; A vẫn chỉ giữ khóa như spec; sub-agent không thêm độ mù vì A chọn mẫu theo điểm judge trong cả hai cách.
  Người kiểm xét lệch này.
- Tên nguồn hiện lấy từ tên file của `top_chunk_ids[n−1]` — giả định thứ tự đóng gói = thứ tự `top_chunk_ids` (context builder chỉ
  bỏ đoạn không có `evidence_parts`, `backend/retrieval/full_corpus_context.py:97-99`); chưa kiểm bằng payload Qdrant.
- Độ dài câu trả lời khác nhau giữa hai bản là khác biệt thật về chất lượng, không che.
- Bộ test 56 câu đã bị nhìn ở 8.1 (giới hạn chung); câu kín không dùng.
- (B24 F3) Mẫu chỉ có **1 câu nhiều nguồn**, trong khi lợi của context 10 ở 8.1 tập trung ở câu nhiều nguồn / so sánh ⇒ mốc người
  kiểm judge chủ yếu trên câu trực tiếp; ghi khi trình User.
- B đã thấy khóa (người kiểm) ⇒ B không làm người tóm nhãn; người tóm nhãn là sub-agent mới (spec §3.4).

## 6. Bàn giao cho người kiểm

Người kiểm (B hoặc C) chạy lại script, so sha `doc_cap_mu.md`; kiểm bằng code: (1) không câu kín (so `case_index` khóa với
Golden, không đụng file `*sealed*`); (2) mù hình thức — 0 citation > nguồn hiện, không chuỗi nào lộ bản (ví dụ "10 nguồn",
`[6]`–`[10]`, tên biến thể); (3) tầng / quota khớp `mau.json` và điểm judge gốc; (4) lệch spec §5 có chấp nhận được. Người kiểm
**không** gửi nội dung file ra ngoài; report review không chép câu hỏi / câu trả lời.
