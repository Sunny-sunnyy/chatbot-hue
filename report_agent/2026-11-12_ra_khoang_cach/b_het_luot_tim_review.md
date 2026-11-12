# Review: "Hết lượt tìm thì dừng" — nhánh `p9-het-luot-tim` `ab66f5e` (cờ `assistant.het_luot_bo_cong_cu`, mặc định TẮT)

Decision: **ready_for_user_confirmation** — merge với cờ tắt: đạt (0 blocker, 0 major, 5 minor). **Bật cờ là quyết định của User**; khuyến nghị của E ở mục 6.
Người kiểm: E (Claude Code — Fable 5.2, `hue-rag-33`) · Date: 21:37 12/11/2026 (`date`) · mức nhẹ, một review cả nhánh
Plan: `docs/superpowers/plans/2026-11-12-het-luot-tim-plan.md` · Implementation report: `report_agent/2026-11-12_ra_khoang_cach/b_het_luot_tim_implementation.md` (B)

## 1. Phạm vi đã review
- `git diff main...origin/p9-het-luot-tim`: 4 file (+167 / −12) — `backend/config/settings.yaml` (+1), `backend/llm/assistant.py` (+9 / −2), `backend/llm/generator_openai_full_corpus.py` (+35 / −10), `backend/tests/test_het_luot_tim.py` (mới). Không file nào ngoài phạm vi plan.
- Đọc hết report + `data/het_luot_tim_2026-11-12/ghi_truoc.md`; tính lại từ dữ liệu thô (script riêng, chỉ in số); chạy 7 test mới trong worktree tạm của E (đã gỡ); đọc đường stream sau chỗ bắt lỗi; đối chiếu chữ thông báo lỗi và tham số `is_enabled` với mã thư viện đang cài. 0 USD.

## 2. Findings
Không có blocker / major. Code đúng plan (kể cả ca xấu plan đã lường: model vẫn xin công cụ đã ẩn ⇒ câu từ chối cố định).

**Minor:**
- **m-1 — ca "model vẫn xin `tim_kho` đã ẩn" mất đường tra web.** Ca này được gắn như chạm trần vòng (`fixed_outcome = "max_turns"`) ⇒ theo luật mở cổng hiện có, **cổng web không mở**; trong khi ở bản cờ tắt, cùng tình huống (xin lần 3 ⇒ nhận "hết lượt" ⇒ model từ chối) thì cổng web **mở**. Đúng chữ plan và **0 lần xảy ra trong ~170 lượt cờ bật đã đo** (mọi lượt `outcome` thường, 0 `max_turns`), nên không chặn. Nhưng hôm nay log không phân biệt được ca này với chạm trần vòng thật ⇒ đề nghị (việc nhỏ sau merge, không cần đo lại): ghi một dấu riêng trong `chat_metrics` để đếm; nếu về sau thấy xảy ra thật thì cho nó đi đường "từ chối thường" để cổng web mở.
- **m-2 — luật đọc A/A được viết 21:11, sau khi đã thấy sàn Golden phạm** (file cờ bật có trước), nhưng **trước** khi chạy lượt A/A. Chấp nhận được (luật không thể bị chỉnh theo kết quả A/A), ghi rõ trong report là "luật thêm sau khi thấy phạm".
- **m-3 — vế sàn "số đoạn mới tìm được không giảm" (107 ⇒ 89) cũng phạm theo chữ.** Cờ không thể làm giảm số đoạn tìm được (trần vẫn 2 lần; lần thứ ba trước đây cũng bị chặn, 0 đoạn) và A/A cờ tắt đã là 100 ⇒ đây là tiêu chí **không đo được bằng một lượt**; lần sau bỏ hoặc đổi thành "số lần tìm thật không giảm".
- **m-4 — số "trước" lấy từ lượt khác giờ** (lượt đếm của C, B7) và đo qua đường không stream ⇒ con số −6,7 s là thật về hướng (8 / 8 bớt lượt gọi) nhưng không phải số tốc độ người dùng thấy; chữ đầu chưa đo.
- **m-5 — lượt an toàn chính không ghi số lần tìm** (B đã tự nêu, đã sửa ở lượt sinh lại). Không cần làm lại.

## 3. Cách người kiểm chạy lại thật (0 USD)
- `cmp data/het_luot_tim_2026-11-12/q1/main.jsonl …/nhanh.jsonl` (228 dòng).
- `git worktree add --detach /tmp/e_hlt ab66f5e` ⇒ `HF_HUB_OFFLINE=1 uv run --project … python -m pytest tests/test_het_luot_tim.py -q`.
- Script tính lại: ghép `golden_sau.jsonl` / `golden_aa_tat.jsonl` với file Golden của B7 theo `case_index`; đếm số lần model tìm từ trường `tools`; ghép 8 câu cũ với hai file "trước" theo mã câu; đếm `outcome` mọi file cờ bật.
- `grep` mã thư viện: chữ lỗi "Tool … not found in agent …" ném `ModelBehaviorError`; tham số `is_enabled` của công cụ nhận hàm.

## 4. Kết quả quan sát (E tính lại ↔ report)
| Mục | Report | E | |
|---|---|---|---|
| Cờ tắt giống byte | 228 / 228 | `cmp` giống hệt, 228 dòng | khớp |
| 7 test mới | đạt | 7 passed (14 s) | khớp |
| 8 câu cũ theo cặp | 8 / 8 bớt ≥ 1 lượt; trung vị 22,85 ⇒ 16,15 s; 0,00199 ⇒ 0,00185 USD | 8 / 8; 22,87 ⇒ 16,13 s; 0,00199 ⇒ 0,00185. (2 / 8 câu chậm hơn hoặc đắt hơn riêng lẻ — nhiễu / đường web) | khớp |
| Golden 33 câu, cờ bật ↔ B7 | 3 câu trả lời ⇒ từ chối, 1 ngược; từ chối 12; đoạn mới 89 | 3 câu, 1 ngược; 12; 89; 0 lỗi | khớp |
| A/A cờ tắt ↔ B7 | 3 câu trả lời ⇒ từ chối, 0 ngược; từ chối 13; đoạn mới 100 | 3, 0, 13, 100 | khớp |
| 3 câu chuyển sang từ chối ở lượt cờ bật có chạm chỗ cờ không | không (1 lần tìm) | cả 3 câu: **1 lần model tìm** ⇒ không tới lượt gọi mà cờ đổi; trong 7 câu có 2 lần tìm: 0 câu trả lời ⇒ từ chối, 1 câu từ chối ⇒ trả lời | khớp |
| Bảng S-AT: số lần model tìm | S11 2 2 1 · 2 2 2; S15 0; S14 1 | đọc file: đúng từng ô | khớp (nhãn người chấm E không chấm lại) |
| Ca model xin công cụ đã ẩn trong lượt đo thật | — | 0 lần (`outcome`: 0 `max_turns` ở 8 + 8 + 10 + 44 + 64 + 9 + 33 lượt cờ bật) | thêm |
| Chữ lỗi thư viện | "Tool tim_kho not found" | mã đang cài ném `ModelBehaviorError(f"Tool {name} not found in agent {agent}")` | khớp |

**Bất biến E kiểm:** "cờ tắt ⇒ không tham số mới nào tới generator" — `_lich_extra` chỉ thêm `con_luot_fn` khi cờ bật; `_assistant_for` chỉ thêm `is_enabled` khi có hàm; Q1 giống byte xác nhận. **Ca dò khác cách của B:** đọc đường stream sau khi lỗi bị nuốt ⇒ `finish_answer_stream` ⇒ `_tools_result` (nhánh mới) ⇒ `_finish_generated` đặt `max_turns` ⇒ phát đúng một `delta` là câu từ chối rồi `return` — **trước** `_web_stream` ⇒ ra m-1. Đường song song (`answer_turn_stream_parallel`) gọi lại `answer_turn_stream` với cùng cờ ⇒ cùng hành vi.

## 5. Trả lời ba câu B hỏi
1. **A/A có đủ để coi sàn Golden không phạm do cờ không? — Đủ.** Lý do mạnh nhất không phải A/A mà là cơ chế: cả 3 câu đổi chiều chỉ có 1 lần tìm, tức chuỗi gửi model **giống byte** bản cờ tắt (test khoá) ⇒ cờ **không thể** là nguyên nhân; A/A (3 câu đổi chiều khi cờ tắt) cho thấy đó là mức dao động thường của 33 câu này. Report giữ chữ "PHẠM theo chữ tiêu chí gốc" là đúng; kết luận của E: **không có bằng chứng cờ làm hỏng Golden; có bằng chứng cơ chế là không**.
2. **"Bớt từ chối" ở 3 câu chạm chỗ cờ là lợi hay hại? — Lợi nhỏ, bằng chứng mỏng, có một cái giá.** Lợi: 3 câu được trả lời có trích dẫn, 2 người đọc 6 / 6 đủ căn cứ. Giá: (a) câu trước có mục web nay nhận câu kho chung chung hơn (câu lưu trú chỉ nêu khu + khoảng giá); (b) đây đúng là vùng dễ "nói chắc khi kho chỉ có bằng chứng gần" — lỗi User xếp nặng hơn từ chối nhầm — mà n = 3. Không đủ để gọi là hại; đủ để **theo dõi**.
3. **Cách bắt `ModelBehaviorError` — vừa.** Ba điều kiện cùng lúc (đúng loại lỗi · công cụ đang bị ẩn · tên `tim_kho` trong thông báo) không nuốt lỗi hành vi khác (test có ca đó). Điểm giòn duy nhất: dựa vào **chữ** thông báo của thư viện — nâng thư viện mà đổi chữ thì ca này thành lỗi 500; test hiện có sẽ báo, nên chấp nhận.

## 6. Decision và bước tiếp theo
- **Merge (cờ tắt): ready.** Cờ tắt giống byte; test đạt; phạm vi gọn.
- **Bật cờ — khuyến nghị của E cho A / User: bật được, kèm một phép theo dõi.** Căn cứ: mục tiêu đạt rõ (8 / 8 bớt lượt gọi, trung vị cả câu −6,7 s ở câu kho thiếu, tiền không tăng); S2 đạt; an toàn không âm theo luật ghi trước; Golden không phạm do cờ. Phép theo dõi (0 USD, ở lượt B7 cuối hoặc lượt đo kế): trong các câu kho thiếu, đếm câu **đổi từ "từ chối + web" sang "kho trả lời"** và đọc có căn cứ không; ≥ 1 câu bịa ⇒ tắt cờ. *Nếu chọn không bật:* giữ chậm ~6–7 s ở câu kho thiếu, không mất gì khác.
- Lưu ý thứ tự: nhánh Exa (`p9-tra-web-exa`) cũng sửa khối `assistant:` của `settings.yaml` ⇒ merge nhánh này trước, E rebase nhánh Exa.
- B sửa chữ report theo m-2, m-3 (không cần review lại). m-1 ghi vào nợ của A.
- Việc riêng B nêu đúng và E xác nhận từ bảng: **một câu an toàn dao động "đảo cảnh báo" 1 / 3 ngay ở bản cờ tắt** — không thuộc nhánh này, cần A đưa vào danh sách chỗ chưa ổn.
