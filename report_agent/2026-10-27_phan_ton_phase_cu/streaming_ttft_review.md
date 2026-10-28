# Review: C73 — kết quả đo "thời gian tới chữ đầu tiên" (streaming)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 10:59 28/10/2026 (`date`) · Việc: A giao (review kết quả C73). 0 USD, chỉ đọc file đã lưu.
Đối chiếu: plan `streaming_ttft_plan.md` bản 2 (A duyệt `9683641b6c38`); code `c70-ttft` `1f70095` (B review ready); report `streaming_ttft_implementation.md`.

## 1. Kiểm lại (free, từ `/tmp/c_ttft/backend` ở `1f70095`)

| Kiểm | Kết quả | Khớp |
|---|---|---|
| `summarize(["main"])` chạy lại trong bộ nhớ (không ghi đè) so với `main.summary.json` | giống hệt (so JSON đã sắp khóa) | ✓ |
| `main.meta.json` | commit `1f70095…`, `questions_sha` `107620cb30f1`, 31 dòng, 0 lỗi, 0,008906 USD, không dừng, `cached_tokens` có ở 20 / 20 dòng S / D | ✓ |
| Tính lại **độc lập** `t_first_visible` (delta đầu có ≥ 1 ký tự sau tiền tố JSON, không dùng `timeline`) ⇒ `gain_visible` trung vị trên 7 câu S10 trong kho có trả lời | 1.921,3 ms | ✓ |
| Dòng "chờ đủ câu hôm nay" (script inline của C): `search_ms + context_ms + t_done`, N10, trong kho | n 8, p50 4.621,9 ms (p95 nội suy 7.649,2; lớn nhất 8.572,5) | ✓ |
| Tiền | pilot 0,001385 + lượt thật 0,008906 = 0,010291 USD (trần 0,03); vượt ước pilot +70 % ⇒ C dừng, A duyệt tiếp — đúng luật dừng plan §8 | ✓ |
| Dải diễn giải | `gain_visible` 1.921 [1.608; 4.310] ⇒ **clear**; `gain_cited` 1.014 [144; 3.041] ⇒ moderate (CI chứa cả 500 lẫn 1.500); `extension_rule_triggered` false (luật chỉ cho chỉ số quyết — đúng plan §5) | ✓ |

## 2. Finding

### m-1 — câu "hôm nay đợi đủ câu: không đạt cả hai" (so yêu cầu p50 ≤ 3 s / p95 ≤ 5 s) dựa trên 8 câu có câu trả lời dài; bộ lớn hơn cho kết quả khác

- **Vị trí:** report §3 "So với yêu cầu phi chức năng" và mục "Cho bạn" ý 2 (≈ 4,6 s / 7,6 s).
- **Bằng chứng:** 8 câu tự viết của C70 có câu trả lời dài (S10 trong kho: token ra trung vị 295, suy luận 89). Bộ "trước" B78 (`data/sua_kho_2026-10-27/eval_truoc/check_truoc.json`,
  cùng chatbot context 10, cùng kiểu đo tuần tự trong harness = tìm + context + sinh, không HTTP) trên **176 câu Golden**: token ra TB 79,6; `wall_ms` **p50 2.207,7 / p95 4.883,6
  ms** ⇒ **đạt** cả hai ngưỡng. Thời gian sinh ≈ 1,16 s + 11,5 ms × token ra (C58) ⇒ kết luận "đạt / không đạt" phụ thuộc chủ yếu vào độ dài câu trả lời của bộ câu.
- **Tác động:** User đọc "hôm nay không đạt" có thể hiểu là chatbot đang chạy trượt yêu cầu phi chức năng, trong khi trên bộ câu lớn nhất đã đo thì đạt (sát p95).
- **Đóng:** ghi cả hai số (8 câu C70 và 176 câu B78), nói rõ "đạt / không đạt tùy loại câu: câu mở, trả lời dài thì không đạt". Không đổi chỉ số quyết hay kết luận "clear".

## 3. Giới hạn

- Không chạy lại lệnh `run` (có phí). Không kiểm bộ câu (`questions.jsonl`).
- So B78 ↔ C70 là hai lượt khác giờ / khác bộ câu ⇒ chỉ để chỉ ra phụ thuộc vào bộ câu, không phải phép so.

## 4. Decision

`ready_for_user_confirmation`: kết quả tái lập được, đúng tiêu chí ghi trước; streaming kiểu C / D đạt dải "rõ" (≈ 1,9 s). m-1 sửa chữ trong report trước khi A trình User.
Worktree `/tmp/c_ttft`: B xong phần chạy lại ⇒ C gỡ được.
