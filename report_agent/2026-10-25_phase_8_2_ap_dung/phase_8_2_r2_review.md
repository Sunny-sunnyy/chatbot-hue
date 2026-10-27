# Review: Phase 8.2 §10 R2 — trả lời phần có căn cứ (chữ E1b), dừng ở bước 1

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor) — kết luận "kém hơn (phạm sàn)" đúng theo tiêu chí ghi trước
Người kiểm: B (Claude Opus 5.5, `hue-rag-31`) · Việc: B53 (A giao 27/10)
Date: 2026-10-27 08:51 +0700 (`date`)
Canonical guide: plan `phase_8_2_r2_plan.md` sha `b70ea775efb2` (tính từ file trên `main` và từ `git show 08419c0:` — cả hai `b70ea775efb2`); spec 8.2 §10.2–§10.4
Implementation report: `git show origin/p82-r2:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_implementation.md` (C, 22:13 26/10)

## 1. Phạm vi đã review

- Git: `origin/p82-r2` = `p82-r2` = `aec9ab8`; `811d25d..aec9ab8` có đúng 2 commit (`0cbad2d` harness, `aec9ab8` report), đúng 2 file mới:
  `backend/experiments/phase_8_2/r2.py` (+268) và report (+93). **Không đụng production**, không file nào khác. `git diff --check`: sạch.
- Thứ tự thời gian: A duyệt plan `08419c0` 22:08:50 → commit harness 22:11:31 → lượt có phí 22:12:04–22:12:21 (`.meta.json`) ⇒ chạy **sau** khi duyệt.
- Đọc hết `r2.py`, plan R2 (full-read), report R2; dữ liệu `data/phase_8_2/r2/` (2 file: `r2_oos_dev.jsonl`, `.meta.json`); mốc
  `data/phase_8_2/b1/b1_dev.jsonl`; P1 8.1 `data/phase_8_1/g2/g2_p1_partial.jsonl` (chỉ câu OOS dev).
- Không đọc câu test, không mở câu kín. Chỉ đọc câu trả lời của câu dev 160 (cần để kiểm mô tả dạng lỗi); review không chép nội dung câu.

## 2. Findings

Không có blocker / major.

**m-1 (minor) — mục "Cho bạn" mô tả câu hỏi cụ thể hơn §4 của chính report.**
- Vị trí: report "Cho bạn" mục 3 nêu phương tiện cụ thể và kiểu điểm đi của câu hỏi; §4 cùng report cố ý viết chung ("giá vé một phương tiện đi
  tới Huế"). Nhánh `p82-r2` đã push lên repo **public**.
- Yêu cầu: `Session_Prompt.md` §5 — report tracked không chép câu hỏi Golden. Đây không phải chép nguyên văn (quét `.githooks/overlap_scan.py`:
  0 trùng), chỉ là mô tả chủ đề rõ hơn mức report tự đặt ở §4.
- Tác động: nhỏ (câu dev, không phải câu kín, không nguyên văn). Không đổi kết luận.
- Tiêu chí đóng: A quyết. Đề xuất: khi có commit tiếp trên `p82-r2`, viết mục 3 ở mức chung như §4; không cần sửa riêng nếu nhánh chỉ để làm hồ sơ.

**m-2 (minor) — report chưa ghi số liệu về câu 115, câu thứ hai P1 từng phạm sàn.**
- Bằng chứng (B tính bằng máy): P1 8.1 (context 5) trả lời **2** câu OOS dev: 115 và 160. Ở R2, câu 115 **từ chối đúng chuỗi**, chỉ câu 160 bị
  trả lời. Theo plan E1 §2 / G4, hai câu P1 phạm sàn có hai dạng: một câu không `[n]` và một câu có `[n]` ý chung. Câu 160 có `[n]` (cả P1 lẫn R2),
  nên 115 là câu thuộc dạng không `[n]`.
- Tác động: report §4 ghi "dạng thứ hai không xuất hiện ở 12 câu này". Câu đó đúng nhưng thiếu điểm chính: đúng câu từng mắc dạng đó nay không
  mắc nữa. Đây **chưa phải** bằng chứng E1b chặn được dạng đó: mốc B1 (prompt cũ, context 10) cũng từ chối 115, và R2 đổi cả context 5 → 10
  lẫn chữ so với P1. Điểm này có ích cho điều kiện mở lại hướng R2 (A 22:1x: kiểm trước trên các câu lỗi cũ).
- Tiêu chí đóng: thêm một dòng vào §4 hoặc §6: "115 (P1 phạm dạng không `[n]`): R2 từ chối; B1 cũng từ chối ⇒ chưa tách được tác dụng của E1b".

## 3. Cách người kiểm chạy lại thật (0 USD)

- `git worktree add --detach /tmp/b53_r2 origin/p82-r2`. Script chỉ đọc `/tmp/b53/check_r2.py` chạy từ `/tmp/b53_r2/backend`:
  `PYTHONPATH=. HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python /tmp/b53/check_r2.py`. Script import `r2.E1B_INSTRUCTIONS` /
  `E1B_RULE`, `g2_generate._REFUSAL_RULE`, `full_corpus_eval.is_refusal` / `cost_usd` ở commit `aec9ab8`, rồi đọc dữ liệu ở working tree chính.
- So câu 160 với P1 8.1 bằng `difflib.SequenceMatcher` (chỉ in tỉ lệ giống).
- `uv run python .githooks/overlap_scan.py` trên report + `r2.py` (bản ở `aec9ab8`).
- `sha256sum` plan R2, harness, jsonl. Không gọi `r2.py run` (có phí; kết luận đã chốt từ một câu, như report §7 đề nghị).

## 4. Kết quả quan sát

| Kiểm | Report nói | B tính lại | |
|---|---|---|---|
| Plan đúng bản duyệt | `b70ea775efb2` | file `main` + `08419c0`: `b70ea775efb2` | ✓ |
| Harness sha | `a8967cfe591a` | `a8967cfe591a` | ✓ |
| Chữ E1b = plan §1 | nguyên văn | so bằng máy: khối `text` plan §1 (gộp xuống dòng, thay `{INSUFFICIENT_ANSWER}`) **==** `E1B_RULE`; cũng nằm trong plan E1 | ✓ |
| Thay đúng một chỗ | `replace` + `assert` | `_REFUSAL_RULE` xuất hiện **1** lần trong `ANSWER_SYSTEM_INSTRUCTIONS` ⇒ thay đúng một câu | ✓ |
| sha prompt | `4acd169d706d` | `4acd169d706d` (= `.meta.json`) | ✓ |
| Tập câu bước 1 | 12 OOS dev | `split.json` dev ∩ `out_of_scope` = 12 = đúng 12 `case_index` trong jsonl | ✓ |
| Context mốc 10 | `settings.yaml` ở `811d25d` | `context_sources` = 10 ở 12 / 12; `top_chunk_ids`, `context_sources` = B1 ở 12 / 12 (chỉ prompt đổi) | ✓ |
| Sàn OOS | 11 / 12 từ chối; bị trả lời: 160 | `is_refusal` tính lại: bị trả lời **[160]**; cờ `refusal` khớp 12 / 12; 11 câu đúng nguyên chuỗi từ chối | ✓ **phạm sàn** |
| Câu 160: dạng lỗi | 1 câu chung có `[1]` + 1 câu "nguồn không có…"; `citation_error` null | đúng: 2 câu, câu đầu `[1]`, câu sau không `[n]`; `citation_error` null, `error` null ⇒ API sẽ trả câu này cho người dùng | ✓ |
| P1 8.1 cùng câu 160 | gần như cùng câu trả lời | P1 cũng trả lời 160, có `[n]`; tỉ lệ giống chữ P1 ↔ R2 **0,933** | ✓ |
| Mốc B1 cùng 12 câu | 12 / 12 từ chối | 12 / 12 | ✓ |
| Lỗi kỹ thuật | 0 | 0 | ✓ |
| Tiền | 23.561 vào / 660 ra = 0,0026861 USD | tổng token theo dòng 23.561 / 660; `cost_usd` = **0,0026861**; tổng `usd` theo dòng = 0,0026861; ≤ trần 0,06 | ✓ |
| Golden không đổi | — | `golden_md5` trong meta `0f7dbf41b422…` = md5 Golden đang hiệu lực | ✓ |
| Dừng đúng plan §3 bước 1 | NOT RUN bước 2–6 | thư mục `r2/` chỉ có 2 file của bước 1; không có `judge_*` | ✓ |
| Quét trùng public | — | report 0 trùng, `r2.py` 0 trùng | ✓ |

**Kết luận theo tiêu chí ghi trước (plan §2 sàn "OOS bị trả lời = 0"; §3 bước 1):** 1 / 12 ⇒ **kém hơn (phạm sàn)**, dừng đúng chỗ. Report
không chốt gì về Completeness hay từ chối nhầm (đúng, vì NOT RUN). Việc A gác hướng R2 khớp `run-experiment` §4 (đổi chữ = biến thể mới, tối đa
3 vòng).

**Độ đơn giản:** harness 268 dòng gồm các lệnh plan §3 cần (`run` / `merge` / `check` / judge / `analyze`), dùng lại hàm production và 8.1, không
sửa production, lệnh ghi đều từ chối ghi đè (`run-experiment` §3.8). Không có cơ chế thừa.

## 5. Giới hạn hoặc phần chưa chạy

- Các lệnh `merge`, `check`, `export-judge`, `check-judge`, `analyze` **chưa bao giờ chạy** (R2 dừng ở bước 1). B chỉ đọc code, chưa kiểm bằng
  dữ liệu thật. Ghi chú cho lần mở lại: `check()` chỉ đọc `r2_dev` / `r2_test` đã gộp nên không dùng được cho `r2_oos_dev`. Holm
  `holm_adjust([p, 1.0])[0]` = p × 2, khớp plan.
- Không chạy lại lượt có phí. Kết luận dựa trên một lượt LLM; câu 160 trượt cả ở P1 (context 5) lẫn R2 (context 10) nên khó là nhiễu, nhưng
  không có A/A riêng (report §6 đã ghi).
- Không kiểm 6 câu OOS test (NOT RUN theo plan).

## 6. Decision và bước tiếp theo

- **ready_for_user_confirmation.** R2 (E1b) **kém hơn — phạm sàn**, số liệu và tiền khớp, chạy đúng plan đã duyệt, không đổi chatbot.
- Việc trung bình (thí nghiệm không vào runtime) ⇒ A tự đóng và báo User. m-1 / m-2 không chặn: C sửa khi có commit tiếp trên `p82-r2`, hoặc
  A ghi vào hồ sơ đợt.
- Nhánh `p82-r2` giữ làm hồ sơ, **không merge**.
