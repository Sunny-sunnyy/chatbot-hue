# Gói 3c (phần miễn phí) — tính lại "lỗi citation" theo định nghĩa mới cho mọi lượt đã sinh

Người làm: C (Claude Opus 5.5, terminal `hue-rag-7f`) · 2026-10-25 20:45 (`date`) · A giao 20:4x · nền `main` `83e1aa9` · **0 USD**, chỉ đọc + ghi
`data/` (private). Không sinh mới, không mở câu kín, **không kết luận lại quyết định** (xác nhận trên test cần sinh mới — paid, User duyệt).

## 1. Định nghĩa và cách tính

- **v1** = giá trị `citation_error` lưu lúc sinh (validator cũ: chỉ nhận `[n]`). **v2** = `llm/citations.py` sau `9e6d371` (gói 1a: nhận `[n]` và
  `[Nguồn n]`, hoa / thường, khoảng trắng), sha256 `9e99744d21be…`; script tự kiểm `citations.py` không khác HEAD.
- v2 tính lại trên câu trả lời đã lưu, với số nguồn context đã lưu (`context_sources`) — đúng cách harness G2 (`g2_generate.citation_error`) và
  evaluator dựng nguồn; câu từ chối không tính; câu lỗi kỹ thuật bỏ. Khâu sau bước sinh, tất định ⇒ được phát lại (`run-experiment` §3.5).
- So theo cặp: `evaluation.full_corpus_eval.paired_compare` (đã commit, không đổi), chỉ số `citation_error` (`LOWER_IS_BETTER`), category lấy từ
  file câu trả lời 7B (không đọc Golden). Luật 8.1 đối chiếu: plan `phase_8_1_g2_g4_plan.md` (sha `a4adfc8eedd9`) §2.1 — "lỗi citation: tổng của
  biến thể − G2.0 **≤ +2 câu** trên 120 dev (nhiễu 7B 4 → 6); > +2 = vi phạm; báo cả số câu lỗi **mới** và **hết**".

## 2. File dẫn xuất (mới, private)

`data/ra_soat_code_2026-10-25/citation_v2/`: 14 file `<lượt>.jsonl` (`case_index`, `category`, `refusal`, `error`, `citation_error_v1`,
`citation_error` = v2) + 14 `<lượt>.meta.json` (đường nguồn, **sha256 nguồn**, commit, sha `citations.py`, định nghĩa) + `summary.json`
(sha `a1990d07788b`). Lượt: 7B Run 1 / 2; G2.0, G2.1a, G2.1b, P1, P2, G2.4 none / low / high (dev 120); `t_baseline`, `t_context10` (test 56); B1
dev / test. Script: `data/ra_soat_code_2026-10-25/tools/citation_v2/citation_v2.py` (chạy từ `backend/`). **Không ghi đè** file nào trong
`data/phase_8_1/`, `data/evaluation/`, `data/phase_8_2/`; manifest G0.6 vẫn sha `9ea480d0d083`.

## 3. Bảng trước / sau (theo cặp với mốc, dạng report G2)

"a → b (mới / hết)": tổng lỗi mốc → biến thể; *mới* = lỗi ở biến thể, không lỗi ở mốc; *hết* = ngược lại. CI 95 % là chênh tỉ lệ (biến thể − mốc).

| Cặp (mốc → biến thể) | n | v1 (lưu lúc sinh) | **v2 (định nghĩa mới)** | v2 theo cặp: CI 95 %, kết luận |
|---|---:|---|---|---|
| **A/A 7B** Run 1 → Run 2 (nhiễu) | 176 | 4 → 6 (4 / 2) | **0 → 2** (2 / 0) | [0; +0,028], không khác |
| G2.1a context 10 (dev) | 120 | 4 → 4 (2 / 2) | **0 → 0** | [0; 0], không khác |
| G2.1a context 10 (test) | 56 | 4 → 4 (3 / 3) | **0 → 0** | [0; 0], không khác |
| G2.1b thứ tự theo tài liệu (dev) | 120 | 4 → 6 (6 / 4) | **0 → 2** (2 / 0) | [0; +0,042], không khác |
| G2.2 P1 trả lời một phần (dev) | 120 | 4 → 3 (2 / 3) | **0 → 2** (2 / 0) | [0; +0,042], không khác |
| G2.2 P2 hai luật spec (dev) | 120 | 4 → 1 (1 / 4) | **0 → 1** (1 / 0) | [0; +0,025], không khác |
| G2.4 reasoning `none` (dev) | 120 | 4 → 8 (7 / 3) | **0 → 2** (2 / 0) | [0; +0,042], không khác |
| G2.4 reasoning `low` (dev) | 120 | 4 → 9 (8 / 3) | **0 → 4** (4 / 0) | [+0,008; +0,067], **kém hơn** |
| G2.4 reasoning `high` (dev) | 120 | 4 → 4 (2 / 2) | **0 → 1** (1 / 0) | [0; +0,025], không khác |
| B1 ↔ G2.1a — A/A context 10 (dev) | 120 | 4 → 6 (4 / 2) | **0 → 0** | [0; 0], không khác |
| B1 ↔ G2.1a — A/A context 10 (test) | 56 | 4 → 6 (6 / 4) | **0 → 0** | [0; 0], không khác |

Tổng 14 lượt: v1 **69** → v2 **14** lỗi (khớp C35). Mọi lỗi v2 còn lại là "Grounded answer has no citation" (không có ngoặc số nào), **đều ở context 5
nguồn** (không câu nào context 1 nguồn) ⇒ kết luận G2.3 "chính sách một nguồn thì gán: 0 câu đổi" vẫn đúng theo v2.

**Nhiễu theo v2:** A/A 7B 0 → 2 (+2 / 176 ⇒ ≈ +1,4 / 120, như cũ — ngưỡng "≤ +2 câu" của 8.1 vẫn ứng với nhiễu); A/A context 10 (B1 ↔ G2.1a) **0 → 0**
ở cả dev và test (v1 ghi "nhiễu citation lớn 12 vs 8, chỉ 2 câu chung" — toàn bộ là định dạng).

## 4. Quyết định 8.1 có số citation đổi — đối chiếu luật đã ghi

| Quyết định (bảng G5) | Số v1 → v2 (tổng biến thể − mốc, dev 120) | Luật "≤ +2" | Kết luận 8.1 có còn đứng **về phần citation**? |
|---|---|---|---|
| **3c reasoning `none`** (G5 §1 dòng 3c: "kém hơn — lỗi citation 4 → 8 (> +2)") | +4 → **+2** | v1 **vi phạm** → v2 **không vi phạm** (đúng ngưỡng) | **Lý do loại biến mất.** Các guardrail khác của `none` theo report G2 đều đạt (0 câu OOS bị trả lời — G2 §4.5 `:136`; Accuracy +0,227 [+0,080; +0,398]; USD 0,91×) và Completeness +0,136 [+0,034; +0,261] p Holm 0,031 ⇒ theo `decision_rule` của plan, `none` sẽ là ứng viên "tốt hơn" trên dev **cần xác nhận trên test** — **chưa kết luận**: (a) định nghĩa đổi sau khi đã thấy số (lý do độc lập: lỗi đo C-09) ⇒ dev chỉ là tín hiệu; (b) +2 bằng đúng nhiễu A/A; (c) test cần lượt sinh mới (paid, User duyệt — ước ≈ 0,007 USD ở context 5, `ung_vien_cai_tien_C.md` mục 2) |
| 3c reasoning `low` ("kém hơn — 4 → 9") | +5 → **+4** | vi phạm cả hai | không đổi (vẫn vi phạm; Completeness cũng không khác) |
| 3c reasoning `high` ("không khác") | 0 → +1 | không vi phạm cả hai | không đổi |
| 6.3 thứ tự context ("giữ"; G2.1b "+2 đúng ngưỡng, 6 mới / 4 hết") | +2 → +2 (2 mới / 0 hết) | không vi phạm cả hai | không đổi (Completeness không khác); nhưng "xáo trộn lỗi theo câu" (6 mới / 4 hết) của v1 chủ yếu là định dạng |
| 3b prompt P2 ("không khác; lỗi citation 4 → 1 — tín hiệu phụ") | −3 → **+1** | không vi phạm | kết luận "giữ" không đổi; **tín hiệu phụ "P2 giảm lỗi citation" biến mất** (là định dạng) |
| 2b trả lời một phần P1 ("kém hơn" vì 2 câu OOS bị trả lời) | −1 → +2 | không vi phạm | không đổi (lý do loại là sàn OOS, không phải citation). Theo v2, 1 trong 2 lỗi của P1 là câu `out_of_scope` |
| 2a context 10 ("thay bằng 10 đoạn"; "citation 4 → 4") | 0 → 0 (dev và test) | không vi phạm | không đổi — guardrail còn rõ hơn |
| G5 §3 đề xuất #7 "Giảm lỗi citation ở bước sinh" (= E2 spec 8.2) | mốc G2.0 dev + test: 8 → **0**; B1: 12 → **0** | — | cơ sở đề xuất (lỗi "thiếu `[n]`" khi nhiều nguồn) phần lớn là định dạng; còn 0 lỗi ở mốc hiện tại và ở B1 ⇒ đầu vào cho luật bỏ sớm E2 (`ung_vien_cai_tien_C.md` mục 3) |
| 6.6 validator citation — G2.3 "một nguồn thì gán" ("giữ") | — | — | không đổi (lỗi v2 đều ở context 5 nguồn) |

Không quyết định nào khác của 8.1 dùng số citation.

## 5. Giới hạn

- v2 tính trên câu trả lời đã lưu; không biết model có viết khác nếu prompt / nhãn đã khớp từ đầu (đó là thí nghiệm, `ung_vien_cai_tien_C.md` mục 9).
- Test chỉ có 56 câu (41 trong kho); bảng test chỉ có cặp G2.1a và B1 (biến thể khác của 8.1 không chạy test).
- Đây là số dẫn xuất cho mốc mới; **số trong report 8.1 / G0.6 giữ nguyên** (bằng chứng tại thời điểm đó). Khi dùng, ghi rõ "citation v2".

## 6. Bàn giao

- A: dùng §3 / §4 khi viết tài liệu thiết kế đợt "tìm hướng tốt hơn" (ứng viên `none`, luật bỏ sớm E2); quyết có xin User lượt xác nhận test cho `none`.
- Không cần review chéo bắt buộc (chỉ đọc + ghi `data/`, A 20:4x); người kiểm muốn chạy lại: `cd backend && HF_HUB_OFFLINE=1 uv run python -I
  ../data/ra_soat_code_2026-10-25/tools/citation_v2/citation_v2.py` (ghi đè chính thư mục `citation_v2/`, kết quả tất định).
