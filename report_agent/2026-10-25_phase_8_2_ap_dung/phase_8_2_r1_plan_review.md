# Review: Phase 8.2 §10 R1 — plan "mức suy luận `none` cho lượt sinh"

Decision: **changes_requested** (0 blocker / 1 major / 3 minor) — tiêu chí đúng spec, số mốc khớp; một giả định về citation sai, làm lệch dự đoán sàn
Người kiểm: B (Claude Opus 5.5, `hue-rag-31`) · Việc: B55 (A giao 27/10)
Date: 2026-10-27 09:04 +0700 (`date`)
Canonical guide: spec 8.2 §10.2–§10.4 (sha `cd910c4c4169`, tính từ file); `skills/run-experiment/SKILL.md` §1, §3, §4
Plan được review: `phase_8_2_r1_plan.md` sha **`0a702b4ac1e4`** (tính từ file lúc bắt đầu và lúc ghi review — không đổi)

## 1. Phạm vi đã review

Chỉ dựa trên mục "Căn cứ để review" của plan (WORKFLOW §9.1). Không đọc STATUS_C hay tin của C.
- Đọc hết plan. Đọc spec §10.2–§10.4, `phase_8_1_g2_implementation.md` §4.5, `de_xuat_khau_tra_loi_C.md` §1.4, §3 dòng R1, §4,
  `phan_loai_loi_C.md` §3 (và §5, xem m-1), skill `run-experiment`.
- Tự tính lại số của plan bằng script riêng (`/tmp/b55/`, chỉ đọc, 0 USD), không chạy `c46_*.py` của C. Dữ liệu dùng: `data/phase_8_2/b1/`
  (`b1_{dev,test}.jsonl`, `judge/`), `data/phase_8_1/g2/` (`g20_baseline`, `g24_none`, `g2_context10`, `t_context10`). Không đọc câu test theo
  từng câu, không mở câu kín.

## 2. Findings

**M-1 (major) — G8 / C37 "lý do loại đã hết với validator v2" là sai: 2 lỗi v2 của `none` ở 8.1 đều là dạng phạm sàn của chính plan.**
- Vị trí: plan §1 bảng giả định dòng G8; YAML dòng "lỗi citation v2 … tăng ≤ 2 câu"; dẫn từ `de_xuat_khau_tra_loi_C.md` §3 dòng R1 ("0 → 2, nằm
  trong nhiễu, nên lý do loại đã hết").
- Bằng chứng (B tính lại: `g2_generate.citation_error(answer, context_sources, single_source_policy=False)` trên `g24_none.jsonl`): đúng **2** câu
  lỗi là dev **172** và **173**. Cả hai báo **`Grounded answer has no citation`**. Mốc `g20_baseline`: 0 lỗi.
- Đây chính là dòng sàn của plan: "câu không citation mà không phải câu từ chối chuẩn (API 500) = 0". Production trả 500 ở đúng chỗ này
  (`full_corpus_eval.answer_case`). Vậy ở context 5, `none` **đã phạm sàn** (2 / 120). Mức tụt "+2 citation v2" không bao giờ phát huy cho dạng
  này, vì sàn đã chặn trước.
- Tác động: plan §2 "Ghi trước" chỉ báo rủi ro vỡ sàn ở 120 / 168, không báo rủi ro vỡ sàn API 500. Đó lại là rủi ro có bằng chứng mạnh nhất
  (2 / 120 ở 8.1). Bước 1–2 (pilot 23 câu) không có 172 / 173, nên lỗi này chỉ lộ ra sau lượt dev 120 câu. Kết quả có thể là "kém hơn" mà plan
  không dự báo, và A / User đánh giá giá trị của việc chạy R1 dựa trên giả định sai.
- Tiêu chí đóng:
  - (1) Sửa G8: "validator v2: 0 → 2, **cả 2 là 'no citation' (172, 173) ⇒ API 500 = phạm sàn ở context 5**".
  - (2) Thêm vào "Ghi trước": "sàn API 500 có thể vỡ; 8.1: 2 / 120".
  - (3) Đề xuất, không bắt buộc: đưa 172, 173 vào bước 2 (pilot) để dừng sớm, thêm ≈ 0,0004 USD.
  - (4) Ghi rõ mức tụt "+2" chỉ đếm lỗi v2 **khác** "no citation" (ví dụ số `[n]` ngoài khoảng), để hai dòng không chồng nhau.

**m-1 (minor) — "Căn cứ để review" mục 3 trỏ sai chỗ cho 9 câu under-answer.**
- `phan_loai_loi_C.md` §3 là bảng "10 câu bị cờ" (có 120 / 168). Danh sách 9 câu U nằm ở **§5** (dòng 102).
- Tiêu chí đóng: sửa thành "§3 (120 / 168) và §5 (9 câu U)".

**m-2 (minor) — danh sách theo dõi 9 câu U lấy ở G2.1a, chưa đếm lại trên mốc B1 (W23 / `run-experiment` §1.6).**
- Bằng chứng (điểm judge cùng lượt mù `data/phase_8_2/b1/judge/`): ở B1 chỉ **6 / 9** câu còn Completeness 4 (38, 51, 65, 66, 141, 173). Ba câu
  **28, 41, 93** đã đạt 5 ở B1 (93: 4 ở G2.1a, 5 ở B1), nên không thể "tăng".
- Tác động: chỉ là chỉ số theo dõi, không đổi luật.
- Tiêu chí đóng: ghi "6 / 9 còn điểm 4 ở B1". Nếu muốn, tách thành "có thể tăng: 6; chỉ có thể tụt: 3".

**m-3 (minor) — dòng "từ chối nhầm" ghi hàm và ngưỡng không cùng loại.**
- `fn: paired_stats(b1, r1, 'false_refusal')` trả chênh TB / CI, còn `max` là "số câu từ chối **mới** ≤ 1" (một số đếm).
- Tiêu chí đóng: ghi rõ cách đếm, ví dụ "đếm câu dev chính có `refusal` B1 = false và R1 = true". `paired_stats` để theo dõi. 120 / 168 đã là
  sàn riêng, không tính ở đây.

## 3. Cách người kiểm chạy lại thật (0 USD)

`/tmp/b55/r1_check.py`, `/tmp/b55/cite_kind.py`, chạy từ `/tmp/b_k3/backend` (code `811d25d`):
`PYTHONPATH=. HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python /tmp/b55/<file>`. Hàm production / harness dùng: `cost_usd`,
`bootstrap_mean_diff` (seed 20261024), `keep_realism`, `g2_generate.citation_error`.

## 4. Kết quả quan sát

| Mục plan | Plan | B tính lại | |
|---|---|---|---|
| G1 `none` không đổi đầu vào (8.1) | 120 / 120 | `input_tokens` = 120 / 120, `top_chunk_ids` = 120 / 120 | ✓ |
| G2 mốc B1 dev 120 | TB ra 76,96; vào 1.658; 0,000204316 USD / câu; ra = 18,8 % USD | 76,96; 1.658,4; 0,00020432; 18,8 % | ✓ |
| G3 ngưỡng USD 0,95× | bớt ≥ 20,4 token ⇒ ≤ 56,5 (0,735×); ước 0,94× | 20,4 ⇒ 56,5 (0,735×); token ra × 0,689 ⇒ USD **0,941×**; giảm USD tối đa (ra = 0) **18,8 %** | ✓ |
| G4 ngưỡng token 0,9× | ≤ 69,3 | 0,9 × 76,96 = 69,3; ctx 5 `none` / mốc = 54,3 / 78,8 = **0,690×** | ✓ |
| G5 nhiễu A/A B1 ↔ G2.1a dev 120 | USD ±1,24 %; token ra ±6,6 % | USD SD 1,41e-5 ⇒ **±1,24 %** (bootstrap [−1,20; +1,26] %); token ra SD 28,25 ⇒ **±6,57 %** ([−6,35; +6,68] %) | ✓ |
| G6 mốc từ chối dev chính | 7 câu (48, 67, 68, 113, 120, 167, 168); 120, 168 từ chối | đúng 7 câu đó; 120, 168 `refusal` true; OOS bị trả lời ở B1: 0 | ✓ |
| G8 citation v2 mốc | 0 | B1 dev + test: 0 lỗi | ✓ |
| G8 8.1 `none` v2 0 → 2 | "nằm trong nhiễu" | 2 câu = **172, 173, cả hai "no citation"** | ✗ **M-1** |
| A/A judge dev chính | C 1/86/1, A 1/86/1, từ chối đổi 0 | C 1/86/1, A 1/86/1, đổi 0 | ✓ |
| A/A judge test chính | C 3/38/0, A 2/38/1, từ chối đổi 0 | C 3/38/0, A 2/38/1, đổi 0 | ✓ |
| Ngưỡng mức tụt | dev 4 / 4; test 6 / 5 | max(thắng, thua) + 3: dev C 4, A 4; test C 6, A 5 | ✓ |
| A/A test token ra | 113,4 / 84,1 | 113,4 / 84,1 (n 56) | ✓ |
| 9 câu U | 9 | 6 / 9 còn điểm 4 ở B1 | m-2 |

### Trả lời hai câu A hỏi

**(1) Mức tụt C thêm chặt hơn spec (Accuracy ≤ 4, từ chối nhầm ≤ +1, citation v2 ≤ +2) — hợp lý, nên giữ, sửa nhỏ một dòng.**
- **Accuracy ≤ A/A + 3** (dev 4 / test 5): cùng mức luật (i) đang dùng. Bớt suy luận có thể làm model nói sai, và "nói chắc sai" là lỗi tệ nhất A
  đề xuất 27/10. Với A/A 1 / 86 / 1, mức này vẫn cho 4 câu tụt, nên không khắt quá. Ở 8.1, `none` làm Accuracy **tăng** (+0,227), nên khả năng
  cao là không chạm ngưỡng.
- **Từ chối nhầm ≤ +1:** rủi ro thấp, vì 8.1 cho thấy `none` từ chối ít hơn (13 → 4, 0 câu từ chối mới). Giữ để bắt chiều ngược lại. Cần sửa
  cách đếm (m-3).
- **Citation v2 ≤ +2:** đúng hướng, nhưng như M-1, dạng lỗi `none` hay gặp nhất là "no citation", và dạng đó đã là sàn (0). Sau M-1, dòng này
  chỉ còn đếm lỗi dạng khác. Giữ được.
- Một điều spec không đòi nhưng nên ghi: luật (a) cho R1 "tốt hơn" khi rẻ hơn ~6 % (≈ 0,000012 USD / câu). Mức lợi này rất nhỏ so với mọi rủi ro
  chất lượng, nên các mức tụt chặt là tương xứng.

**(2) Ngưỡng USD 0,95× so nhiễu A/A ±1,24 % — ngưỡng tự nó phân giải được, nhưng dự đoán R1 nằm sát ngưỡng trong vùng nhiễu.**
- Ngưỡng cách mốc 5 %, gấp ~4 lần nửa độ rộng nhiễu. Một mức giảm thật 5 % vẫn phân biệt được với nhiễu.
- Nhưng dự đoán là **0,941×**, chỉ cách ngưỡng 0,9 điểm %, nhỏ hơn nhiễu ±1,24 %. Vì vậy nhánh USD qua hay trượt gần như do may.
- Luật là **USD ≤ 0,95 HOẶC `output_tokens` ≤ 0,9**. Nhánh token ra: dự đoán 0,69×, cách ngưỡng ~21 điểm %, khoảng 3 lần nhiễu ±6,6 %. "Mặt còn
  lại ≤ 1,00": token vào không đổi (G1), nên khi token ra giảm thì USD chắc chắn ≤ 1,00.
- ⇒ Trên thực tế, **chỉ số quyết là `output_tokens`**. Ngưỡng USD không gây quyết định nhầm; nó chỉ ít khi quyết. Không cần đổi. Report R1 nên
  báo USD kèm CI, để User thấy mức tiết kiệm thật (tối đa có thể 18,8 %).

## 5. Giới hạn hoặc phần chưa chạy

- Chưa xem harness `r1.py` (chưa có trong gói review; plan §3 nói B review cùng report).
- Không tính lại cỡ mẫu Completeness (C37 §1.4) bằng bootstrap. B chỉ kiểm phép tính chênh TB của 4 câu tụt 1 / 2 điểm (−0,045 / −0,091) bằng tay.
- M-1 dựa trên context 5 (8.1). Ở context 10 tỉ lệ có thể khác, nhưng đó chính là điều phải ghi trước.

## 6. Decision và bước tiếp theo

- **changes_requested:** C sửa M-1 (G8 + "Ghi trước"; nên thêm 172 / 173 vào pilot), m-1, m-2, m-3, rồi báo sha mới. B kiểm lại phần sửa.
- Tiêu chí còn lại (sàn, chỉ số quyết, mức tụt, tiền ≤ 0,05 USD, dừng, trình User khi đưa vào chatbot §5) đúng spec §10.2–§10.4 và đủ để A
  duyệt sau khi sửa.
