# Review: Phase 8.2 §10 R1 — mức suy luận `none` cho lượt sinh, dừng ở pilot

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor) — kết luận "kém hơn (phạm sàn, câu 168)" đúng theo tiêu chí ghi trước
Người kiểm: B (Claude Opus 5.5, `hue-rag-31`) · Việc: B58 (A giao 27/10)
Date: 2026-10-27 09:30 +0700 (`date`)
Canonical guide: plan `phase_8_2_r1_plan.md` bản 2 sha `8e76e77e0448` (file trên `main` + `git show 78a5f05:` — cả hai `8e76e77e0448`); spec 8.2 §10.2
Implementation report: `git show origin/p82-r1:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_implementation.md` (C, 09:23)

## 1. Phạm vi đã review

- Git: `origin/p82-r1` = `63a472f`; `811d25d..63a472f` có đúng 2 commit (`d2646e6` harness, `63a472f` report), 2 file mới
  (`backend/experiments/phase_8_2/r1.py` +283, report +108). **Không đụng production.** `git diff --check`: sạch. Quét trùng: report 0, `r1.py` 0.
- Thời gian: A duyệt plan `78a5f05` lúc 09:18:40 → commit harness 09:20:37 → lượt có phí 09:20:58–09:21:59 (`.meta.json`). Chạy **sau** khi duyệt.
- Đọc hết report + `r1.py` (diff với `r2.py` mà plan nói là khung). Dữ liệu `data/phase_8_2/r1/` (2 file + meta), mốc `data/phase_8_2/b1/b1_dev.jsonl`.
- Đọc câu trả lời câu dev 168 và dựng lại context của câu đó bằng code mốc (chỉ trong terminal), để kiểm mô tả dạng lỗi. Review không chép nội dung.
  Không đọc câu test, không mở câu kín.

## 2. Findings

Không có blocker / major.

**m-1 (minor) — hàm theo dõi `uncited_sentences` (`r1.py`) không đếm được đúng dạng lỗi nó nhắm tới.**
- Vị trí: `r1.py` `uncited_sentences` tách câu bằng `re.split(r"(?<=[.!?])\s+", …)`, dùng trong `check()` → `refusal_to_answer`.
- Bằng chứng (B chạy hàm của C trên dữ liệu thật):
  - câu trả lời R1 câu 168 → **0**; câu trả lời R2 câu 160 → **0**, dù cả hai có một câu "nguồn không nêu…" không citation;
  - chuỗi tự viết `"Câu một.[1] Câu hai không trích."` → 0, còn `"Câu một [1]. Câu hai không trích."` → 1.
  - Nguyên nhân: model đặt `[n]` **sau** dấu chấm (`….[2] Nguồn …`), nên ký tự trước khoảng trắng là `]` và regex không tách câu.
- Tác động: không đổi kết luận. `check()` chưa chạy, vì R1 dừng ở bước 2, và đây chỉ là chỉ số theo dõi. Nhưng nếu hướng "kiểm bằng code sau
  sinh" (C51) dùng lại hàm này, nó sẽ bỏ sót đúng dạng lỗi của R2 / R1.
- Tiêu chí đóng: ghi giới hạn này trong report R1 §6 (hoặc hồ sơ đợt). Nếu dùng lại, tách câu cho phép `[n]` đứng giữa dấu kết câu và khoảng trắng,
  ví dụ `(?<=[.!?])(?:\[(?:Nguồn )?\d+\])*\s+`, rồi thử lại trên 168 / 160. Không cần commit thêm trên `p82-r1` nếu nhánh chỉ để làm hồ sơ.

## 3. Cách người kiểm chạy lại thật (0 USD)

Script chỉ đọc `/tmp/b58/` (xóa khi xong), chạy từ `/tmp/b_k3b/backend` (code = `811d25d` + harness K3, context 10):
- `r1_data.py`: tập câu, sàn, tiền, tính tất định. Dùng `full_corpus_eval.is_refusal` / `cost_usd`, `g2_generate.citation_error`.
- `r1_168.py`: dựng lại retrieval + context cho câu 168, so `top_chunk_ids` với dòng R1, kiểm số trong câu có `[n]` có nằm trong đoạn được trích.
- `uncited.py`: gọi `uncited_sentences` của `r1.py` (bản `63a472f`) trên câu 168 / R2 160 và hai chuỗi tự viết.

## 4. Kết quả quan sát

| Kiểm | Report nói | B tính lại | |
|---|---|---|---|
| Plan đúng bản duyệt | `8e76e77e0448` | `8e76e77e0448` | ✓ |
| Đổi đúng một thứ | `reasoning_effort="none"` | diff `r1.py` ↔ `r2.py`: `generate` chỉ gọi `from_environment(settings, reasoning_effort="none")`, không đổi `answer_instructions`; phần còn lại là khung + đếm | ✓ |
| Bước 1 = 12 OOS dev | 12 / 12 từ chối | tập câu = đúng 12 OOS của `split.json` dev; 12 / 12 đúng nguyên chuỗi từ chối; `refusal` khớp `is_refusal` 12 / 12 | ✓ |
| Bước 2 = 12 câu pilot | 120, 168, 172 + 9 U | tập câu = đúng {120, 168, 172} ∪ 9 câu U (gồm 173) | ✓ |
| **Dừng đúng plan §3 bước 2** | 168 trả lời ⇒ dừng | 168: R1 `refusal` **false**, B1 **true** (sàn "120 / 168 vẫn từ chối"); 120 vẫn từ chối; thư mục `r1/` chỉ có 2 lượt, không có `dev_rest` / judge / test | ✓ |
| Sàn API 500 | 0 / 12 | `citation_error` = null ở 24 / 24 dòng; validator v2 tính lại: 0 lỗi; 172, 173 có `[n]` | ✓ |
| Lỗi kỹ thuật | 0 | 0 | ✓ |
| Tất định | 24 / 24 | `top_chunk_ids`, `context_sources`, `input_tokens` = B1 ở **24 / 24** | ✓ |
| **Tiền từ usage log** | 22.637 + 20.653 vào; 372 + 776 ra ⇒ 0,0049030 USD | tổng token theo dòng: 43.290 vào / 1.148 ra; `cost_usd` = **0,0049030**; mỗi lượt khớp `.meta.json` (0,0024497 / 0,0024533) và tổng `usd` theo dòng | ✓ |
| Golden không đổi | — | `golden_md5` `0f7dbf41b422…` ở cả hai meta | ✓ |
| Số theo dõi §4.3 | token ra 31,0 / 42,3 và 64,7 / 90,2; USD 0,000204 / 0,000210 và 0,000204 / 0,000217; p50 2.355 / 2.250 ms | 31,0 / 42,3; 64,7 / 90,2; 0,000204 / 0,000210; 0,000204 / 0,000217; p50 trong phạm vi 2.356 / 2.250 ms | ✓ |

**Dạng lỗi câu 168 — mô tả của C đúng** (B đọc trong terminal, dựng lại context bằng code mốc; `top_chunk_ids` dựng lại = dòng R1):
- Câu trả lời có **hai câu**. Bộ tách câu theo dấu kết câu của B ban đầu đếm 1, cũng vì `[n]` đứng sau dấu chấm (xem m-1).
  - Câu 1 có `[2]`. Mọi con số trong câu đều **có nguyên văn trong đoạn được trích [2]** (4 / 4 số), nên đây **không phải bịa**.
  - Câu 2 không citation, dạng "nguồn không nêu … nên chưa xác định được".
- Thông tin ở câu 1 **cùng chủ đề** (cùng tuyến, cùng dịch vụ) nhưng **không phải điều câu hỏi hỏi**. Kho không có điều được hỏi: C36 ghi 0 / 2 fact
  trong context, và sàn 120 / 168 dựa trên nhãn này.
- Validator production nhận câu này (có `[n]`), nên người dùng nhận câu trả lời vòng thay vì câu từ chối chuẩn.
- Đúng dạng "trích ý chung + nguồn không có" của R2 câu 160 và P1 8.1.

**Kết luận theo tiêu chí ghi trước:** sàn "120 / 168 vẫn từ chối" bị phạm ⇒ **kém hơn**, dừng đúng plan §3 bước 2. Report không kết luận gì về
Completeness, Accuracy hay chỉ số quyết USD / `output_tokens` (NOT RUN). Số §4.3 được ghi rõ là pilot chọn có chủ đích, chỉ để theo dõi.

**Độ đơn giản:** harness theo khung `r2.py` như plan §3, không sửa production, lệnh ghi đều từ chối ghi đè. Các lệnh judge / `analyze` chưa chạy là
phần plan yêu cầu. Không có cơ chế thừa.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại lượt có phí. Câu 168 trượt ở một lượt; không có A/A cho riêng câu này (report §6 đã ghi).
- `check`, `merge`, judge, `analyze` chưa bao giờ chạy với dữ liệu thật. B chỉ đọc code của chúng và thử riêng `uncited_sentences` (m-1).
- Nhãn "168 = từ chối đúng" dựa trên C36 (một người gắn). B chỉ kiểm rằng câu trả lời không nêu điều được hỏi.

## 6. Decision và bước tiếp theo

- **ready_for_user_confirmation.** R1 (`none`) **kém hơn — phạm sàn câu 168**. Số liệu, tiền và tính tất định khớp; chạy đúng plan bản 2 đã duyệt;
  không đổi chatbot. Nhánh `p82-r1` giữ làm hồ sơ, không merge.
- m-1 không chặn. Liên quan trực tiếp tới C51 (kiểm sau sinh): bộ tách câu phải xử lý `[n]` sau dấu chấm.
- Quan sát cho A (không phải finding): đây là lần thứ ba cùng một dạng lỗi chặn một biến thể khâu trả lời (P1 8.1, R2 câu 160, R1 câu 168). Cả
  ba đều là câu trong kho không có điều được hỏi, và model "trả lời vòng" bằng một ý cùng chủ đề có `[n]` + một câu "nguồn không nêu…". Cả ba là
  câu dev đã thấy, nên đây là một mẫu lỗi lặp, chưa phải tỉ lệ.
