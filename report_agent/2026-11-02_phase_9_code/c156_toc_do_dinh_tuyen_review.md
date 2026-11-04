# Review: Phase 9 — thí nghiệm tốc độ #1 (`none` cho lần định tuyến), report C156 + C165

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 0 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-2d`) · việc **B155** (A giao) · 20:37 04/11/2026 (`date`)
Report: `report_agent/2026-11-02_phase_9_code/c156_toc_do_dinh_tuyen.md` sha `39b06ea1935c` · plan bản 5 `da2ff2c8e56c` (A duyệt `7460b42`). 0 USD; không đọc STATUS / tin của C.

## 1. Phạm vi đã review

Report; plan bản 5 §2–§4 (luật ghi trước); 8 file thô `data/phase_9/toc_do/thi_nghiem_1/ban4/` (mốc / biến × r1 / r2 × 123 câu + tầng lịch sử 50 lượt). Không chạy lại API.

## 2. Findings

Không có finding. Kiểm từng khẳng định bằng **script tự viết** (đọc thẳng `route`, nhãn `nhan` / `tuyen`, `chap_nhan`, `router_sha`, `usd`, `llm_calls` — không dùng `cham_ban4.py` của C):

| Khẳng định | Tính lại (B) | Khớp |
|---|---|---|
| Mọi dòng chạy trên lời dặn `164bd4a254e9` | 8 / 8 file, mọi dòng `router_sha` = `164bd4a254e9` | ✓ |
| **S1 phạm:** biến r1 2 câu, r2 1 câu (một câu cả 2 lượt); mốc 0 / 0 | biến r1 {S12, S17}, r2 {S12}; mốc r1 / r2 rỗng; tầng lịch sử 0 cả bốn file | ✓ |
| K 0 (24 câu + 6 lượt khẩn cấp có lịch sử) | 0 ở cả 8 file | ✓ |
| R 123 câu: sai biến 2 / 1 ≤ ngưỡng 2 (= 0 + N_AA 1 + 1) | sai mốc 0 / 0; N_AA = 1 (một câu khác tuyến giữa hai lượt mốc, cả hai tuyến đều được chấp nhận); sai biến 2 / 1 | ✓ |
| Lỗi gọi định tuyến 0 | `route_error` 0 ở 8 file | ✓ |
| Tiền 0,057431 | mốc 0,010907 + 0,010803 · mốc lịch sử 0,004778 + 0,004831 · biến 0,009126 × 2 · biến lịch sử 0,003930 × 2 = **0,057431** | ✓ |
| Theo dõi ms p50 / p95 (123 câu) mốc 1,74 / 3,04 · 1,66 / 2,50 ↔ biến 1,50 / 2,54 · 1,31 / 2,04; lịch sử biến 1,16 / 1,75–1,90 | đúng từng số | ✓ |
| Hai câu đổi tuyến là câu mốc suy luận nhiều nhất (62–90 token) | S12 90 / 63, S17 78 / 62 token suy luận ở mốc (TB mốc 25–32, max 104) | ✓ (ghi đúng là giả thuyết) |

**Kết luận đúng luật:** plan bản 5 §3 "Kết quả âm (một sàn phạm…) ⇒ cờ `null`" và thứ tự §4 "(K / S1 / N đạt) ⇒ Golden ⇒ chữ đầu" ⇒ S1 phạm thì dừng trước Golden 176 và chữ đầu; report ghi **NOT RUN** đúng, không chỉnh lời dặn định tuyến, AT không dùng lại được (2 câu ra tuyến ngoài tập mốc) và không sinh lại vì đã âm — đúng. Đề xuất bước sau (tag hồ sơ; #6 / #4; `low` / `minimal` là thí nghiệm mới) nằm ngoài kết luận, ghi đúng nhãn đề xuất.

## 3. Cách người kiểm chạy lại thật

Chỉ đọc file thô bằng Python (0 USD); không gọi API, không đọc câu hỏi.

## 4. Kết quả quan sát

Như bảng §2 — mọi số của report khớp số tính lại.

## 5. Giới hạn hoặc phần chưa chạy

Không kiểm lại code cờ trên `p9-toc-do-1` `d190545` (đã được review ở plan; kết quả âm ⇒ không merge). Chữ đầu NOT RUN (đúng luật).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** — A trình User kết quả âm; nhánh `p9-toc-do-1` là hồ sơ (tag `hoso/` khi User duyệt xoá).
