# Báo cáo cho bạn: Đánh giá — thước đo chất lượng và điểm mốc (Phase 7B, 8.1, 8.2, đợt sửa kho)

**Cập nhật lần cuối: 16:47 27/10/2026 — bản 3: nhãn "đoạn đúng" bản 2 và bản 3 (27/10), luật trúng dòng tiêu đề, thước đo đợt cải tiến 8.2 và
mốc cuối trên câu kín (plan đã duyệt), phát hiện bộ kiểm trích dẫn cũ trong lượt đo context 10, thước đo cho đợt sửa kho (spec đã duyệt).
Bản 2 (25/10) giữ nguyên ở §4.**
Người viết: A (bản 1, 24/10), C (bản 2, 25/10; bản 3, 27/10) · Review: B (bản 2), A (bản 3). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chấm chatbot tự động, lặp lại được: mọi thay đổi so với một **điểm mốc** trên cùng bộ câu, theo luật ghi **trước** khi chạy,
  rồi mới quyết giữ hay bỏ.
- **Đang chạy cách nào:**
  - Bộ chấm đi đúng đường API thật (tìm đoạn → đóng gói đoạn → `gpt-6-luna` trả lời → kiểm trích dẫn).
  - Chấm câu trả lời: Claude chấm 3 điểm 1–5 (Đúng / Đủ / Trúng ý), chấm **mù** — mốc và biến thể trộn chung một lượt, người chấm không biết câu nào của bên nào.
  - So hai cấu hình **theo cặp từng câu** (bootstrap 10.000 lần, CI 95 %, thắng / hòa / thua); nhóm **thử** 120 câu để chọn, nhóm **kiểm** 56 câu để xác nhận.
  - Tầng tìm: đo "đoạn có đáp án có lọt vào phần đưa model không" bằng **nhãn đoạn đúng** — đang dùng **bản 3** (từ 27/10 chiều); mọi số đoạn đúng phải
    ghi kèm bản nhãn (§2).
- **Số mốc chính:**
  - 7B (24/10, 176 câu, 5 đoạn): Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45; từ chối nhầm 22 / 158.
  - 8.1 (25/10): **10 đoạn thay 5** làm câu trả lời đủ hơn (Đủ +0,26 nhóm thử, +0,27 nhóm kiểm) — chưa vào chatbot (chờ B0, §6).
  - Nhiễu "hai lượt cùng cấu hình" (A/A) ở 10 đoạn, 176 câu: điểm Đủ tụt 1 câu, Đúng tụt 2 câu — đây là nhiễu nền dùng cho các luật "không làm hỏng".
  - Đoạn đúng lọt vào 10 đoạn của chatbot 10 đoạn (nhóm thử 40 câu có nhãn): **24 / 40** theo nhãn bản 2 và bản 3 (bản 1: 22).
- **Thay đổi thước đo 27/10:**
  - Nhãn đoạn đúng **bản 2** (sáng) rồi **bản 3** (chiều): thêm chỗ kho nói lại cùng một ý, và đếm cả **dòng tiêu đề mục** mà model thấy (§2, §4).
  - Phát hiện: lượt đo context 10 (25/10) chấm trích dẫn bằng **bộ kiểm cũ** chỉ nhận `[n]` — 12 / 176 câu bị ghi "lỗi trích dẫn" mà bộ kiểm hiện tại cho qua (§4).
- **Giới hạn chính:**
  - **chưa có mốc người** — B0 (bạn đọc 20 cặp câu trả lời mù) **chưa làm**; mọi kết luận dựa điểm Claude là tạm;
  - chỉ 40 câu thử / 15 câu kiểm có nhãn đoạn đúng ⇒ nhiều kết quả tầng tìm chỉ "chưa rõ";
  - nhóm kiểm 56 câu đã bị nhìn ở 8.1 ⇒ phép kiểm cuối là **36 câu kín** (khóa, chưa ai chạy);
  - sửa kho sẽ làm lệch nhãn đoạn đúng (nhãn ghi vị trí ký tự) ⇒ phải dựng bản 4 sau khi build lại (§6).
- **Chi phí:** 7B + thử nhanh ~0,087 USD; 8.1 ~0,165 USD; 8.2 tới nay ≈ 0,213 / 0,5 USD. Chấm bằng Claude dùng quota Claude Code (không USD).
- **Bạn cần quyết gì:**
  1. **B0** khi tiện (~30–45 phút) — chặn việc đưa 10 đoạn vào chatbot và mốc cuối 8.2.
  2. Khi 8.2 xong: quyết **mở câu kín** để chạy mốc cuối (B3).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Mốc / biến thể:  176 câu Golden → đường API thật (tìm → đóng gói N đoạn → gpt-6-luna → kiểm trích dẫn)
                 → tầng tìm: keyword @10 (miễn phí) + đoạn đúng theo tầng: pool → top-10 → N đoạn đưa model (nhãn bản 3)
                 → câu trả lời mốc + biến thể trộn MÙ → Claude chấm Đúng / Đủ / Trúng ý (1–5)
                 → so theo cặp từng câu: chênh, CI 95 %, thắng / hòa / thua; nhiều biến thể ⇒ Holm
                 → luật ghi trước: sàn · mức tụt cho phép · 1–2 chỉ số quyết
```

- **Luật ghi trước (ba lớp):** sàn không được vi phạm (0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật) · mức tụt cho phép (ví dụ điểm Đủ / Đúng trung bình
  ≥ −0,1 **và** số câu tụt ≤ nhiễu A/A + 3) · chỉ số quyết phải tốt lên vượt nhiễu. Nhóm kiểm nhỏ ⇒ xác nhận ở nhóm kiểm = **"không làm hỏng"** (User 27/10).
- **Nhãn đoạn đúng — ba bản, mỗi số ghi kèm bản:**

  | Bản | Khi nào | Khác bản trước | Dùng cho |
  |---|---|---|---|
  | 1 (`gold_draft`) | 8.1 G0.3, 25/10 | 55 câu khó (40 thử / 15 kiểm), một chỗ cho mỗi ý | mọi số đoạn đúng **trước 27/10** |
  | 2 | 27/10 sáng (User duyệt 13:05) | +3 chỗ kho nói lại cùng ý (2 câu thử) **và** luật trúng dòng tiêu đề | số 27/10 sáng |
  | 3 | 27/10 chiều (mặc định từ commit `fa192f8`) | +2 câu nhóm kiểm: một câu thêm một chỗ nói lại; một câu so sánh gắn đúng trích dẫn nói thẳng ý so sánh | **mặc định hiện nay** |

  Bản 1, 2 giữ nguyên để tái lập số cũ. So số mới với số cũ thì chạy lại mốc bằng cùng bản nhãn.
- **Luật trúng dòng tiêu đề (từ bản 2):** nhãn đánh dấu một đoạn văn trong file kho; một đoạn tìm được "trúng" nhãn khi phần thân đoạn giao vị trí nhãn,
  **hoặc** khi nhãn là một dòng tiêu đề Markdown nằm trong đường tiêu đề của đoạn (model thấy tiêu đề đó trong ngữ cảnh). Trước bản 2, câu có ý nằm ở tiêu đề
  mục bị đếm "thiếu" dù model đã thấy và trả lời đúng.
- **Một ý được tính "có trong ngữ cảnh"** khi **một** trích dẫn bất kỳ của ý đó trúng; câu "đủ đoạn đúng" khi **mọi** ý đều có (test ghim luật này).
- Code:
  - bộ chấm `backend/evaluation/full_corpus_eval.py` (`answer_case` :322, `is_refusal` :162, so theo cặp `paired_stats` :634, `bootstrap_mean_diff` :590, 10.000 vòng :55);
  - prompt chấm `backend/evaluation/full_corpus_judge_prompt.md`;
  - nhãn: `backend/experiments/phase_8_1/g1_retrieval.py` (`GOLD_PATH` :47 = bản 3, `quote_is_chunk_heading` :76, `chunk_hits_quote` :82, `gold_coverage` :93);
    test `backend/tests/test_gold_coverage.py`;
  - harness thí nghiệm `backend/experiments/phase_8_1/`, `phase_8_2/` (một số chỉ trên nhánh hồ sơ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Chấm tìm đoạn bằng keyword (MRR, nDCG, Keyword Coverage @10) | **Đã xử lý, đóng gói** | mốc 7B; `full_corpus_eval.py` |
| Chấm câu trả lời bằng Claude (Đúng / Đủ / Trúng ý), mù, cùng lượt | **Đã xử lý, đóng gói** | nhiễu riêng người chấm: Đủ đổi 2 / 88 câu |
| Từ chối đúng / từ chối nhầm, lỗi trích dẫn | **Đã xử lý, đóng gói** | lượt context 10 ngày 25/10 đếm trích dẫn bằng bộ kiểm cũ (12 / 176 lỗi giả) — §4 27/10 |
| So theo cặp + CI + Holm; đối chứng âm / dương | **Đã xử lý, đóng gói** | `paired_stats` (`full_corpus_eval.py:634`) |
| Nhóm thử 120 / nhóm kiểm 56 | **Đã xử lý, đóng gói** | `split.json` seed cố định |
| Nhiễu A/A ở 10 đoạn | **Đã xử lý** | 176 câu: Đủ tụt 1, Đúng tụt 2 (thắng / hòa / thua 4/171/1 và 3/171/2) |
| Đoạn đúng (vị trí trong file) cho câu khó | **Xử lý một phần** | 55 / 176 câu (40 thử / 15 kiểm); **bản 3** mặc định; câu khác chỉ có keyword |
| Đếm ý nằm ở dòng tiêu đề mục | **Đã xử lý, đóng gói** | từ bản 2; `g1_retrieval.py:76-90` + test |
| Nhãn độ tự nhiên (bỏ câu người thật ít hỏi) | **Đã xử lý** | 82 / 65 / 29; số chính bỏ 29 câu |
| Bộ câu kín cho chấm cuối 8.2 | **Đã xử lý** (khóa, chưa chạy) | 36 câu khóa 25/10 15:22; plan chạy đã duyệt (§4 27/10) |
| Mốc người (bạn đọc cặp mù) | **Chưa thực hiện** | B0 — 20 cặp đã chuẩn bị (`data/phase_8_2/b0/`), bạn chưa đọc |
| Điểm trên câu người dùng thật sự nhận (câu lỗi trích dẫn tính là hỏng) | **Xử lý một phần** | luật này **có** trong plan câu kín (câu 500 = điểm 1) và spec sửa kho; chưa vào bộ chấm chung |
| Kiểm số trong câu có trích dẫn phải có trong nguồn | **Đã thử, chưa áp dụng** | 27/10 đo lượt 10 đoạn: 68 câu có số, 0 lỗi thấy được (4 câu bị cờ đều là phép tính đúng; mẫu 10 / 10 đúng) ⇒ chưa cần kiểm bằng code |
| Thước đo sau khi sửa kho (trước ↔ sau, nhãn bản 4) | **Chưa thực hiện** | spec đã duyệt (§4 27/10, §6); chạy sau khi đóng 8.2 |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 27/10/2026 chiều — thước đo cho đợt sửa kho (spec đã duyệt, chưa chạy)

Spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (bạn duyệt sha `937cf8969810`, 15:39 27/10), sau 3 vòng review:
- **Bộ "trước"**: chạy 176 câu trên chatbot cuối 8.2 với kho + chỉ mục hiện tại **trước khi đụng kho** (bước 0) — vì chỉ mục được thay tại chỗ, sau đó không
  còn bản cũ để sinh lại. Plan đo ghi tiêu chí trước và được review trước bước này.
- **Bộ "sau"**: 176 câu trên chỉ mục mới (bước 9). Hai bộ chấm **cùng một lượt mù**, **cùng bản Golden đã sửa** (bạn duyệt từng câu sửa, bước 8); câu chạm ý
  đã sửa trong kho báo riêng.
- **Tiêu chí "không làm hỏng"** (§6): sàn 0 câu ngoài kho bị trả lời, 0 lỗi kỹ thuật / 500 mới; điểm Đủ / Đúng trung bình ≥ −0,1; số câu tụt ≤ A/A + 3 với
  **A/A = 2** (nhiễu hai lượt 10 đoạn trên 176 câu: Đủ 1, Đúng 2 — lấy số lớn); mỗi câu tụt có giải thích.
- **Nhãn đoạn đúng bản 4** dựng **sau khi build** (bước 7): sửa kho làm lệch vị trí — đếm trên các chỗ sửa đợt 1: 24 câu có nhãn trong file bị sửa, 66 trích
  dẫn lệch vị trí, 3 trích dẫn bị chính chỗ sửa chồng lên (cần đề xuất mới, bạn duyệt). Số đoạn đúng chỉ tính lại sau bước này; bản 3 giữ để tái lập số cũ.
- **Mốc tìm mới (T1)**: ghi mã mới sau build, thay chỗ đang trỏ mốc cũ `cefb2d1ad609` (bước 6).
- Tiền ước 2 lượt × 176 câu ≈ 0,074 USD; trần đợt 0,15 USD.

### 27/10/2026 chiều — lượt đo 10 đoạn (25/10) chấm trích dẫn bằng bộ kiểm cũ

- **Quan sát:** lượt sinh câu trả lời 10 đoạn chạy 16:35–16:38 ngày 25/10, **trước** khi bộ kiểm trích dẫn được sửa (19:58 cùng ngày) để nhận cả `[Nguồn n]`.
  Chạy lại hàm kiểm cũ trên câu trả lời đã lưu: khớp mọi ghi chép lỗi (176 / 176) ⇒ **đã chứng minh** lượt đó dùng bộ kiểm cũ.
- **Với bộ kiểm hiện tại:** cả **12 / 176** câu bị ghi "lỗi trích dẫn" (6 thử, 6 kiểm; đều viết `[Nguồn n]`) đều qua; 0 câu đổi chiều ngược ⇒ chatbot hôm nay
  không báo lỗi các câu đó.
- **Hệ quả:** con số "lỗi trích dẫn 12 câu" của lượt đó là theo bộ kiểm cũ. Các thí nghiệm đợt cải tiến so "lỗi trích dẫn" với mốc này bị lệch có lợi cho biến
  thể — kết luận "kém hơn" của chúng không đảo (A suy ra). Lượt 10 đoạn của 8.1 (8 câu) chưa đếm lại. Mốc cuối câu kín sẽ **tách riêng** số câu lỗi kiểu này
  mỗi bên. 0 USD. Report: `report_agent/2026-10-25_phase_8_2_ap_dung/c65_citation_138_check.md`.

### 27/10/2026 chiều — mốc cuối 8.2 trên câu kín (plan duyệt, chưa chạy)

Plan `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md` (A duyệt sha `27e75be5ed44` sau 2 vòng review):
- So **chatbot đầu 8.2** (5 đoạn, chưa chuẩn hóa dấu, bộ kiểm trích dẫn cũ) với **chatbot cuối 8.2** (dự kiến 10 đoạn + chuẩn hóa dấu + bộ kiểm mới) trên 36 câu kín —
  phép kiểm tổng, không tách phần của từng thay đổi.
- **Giữ mù:** người điều phối (A) không đọc câu kín; **người chạy: B** (chỉ chạy script in số đếm); người chấm là sub-agent Claude mới; report chỉ có số dòng,
  số đếm theo loại câu. Tập quyết **33 câu** (bỏ 3 câu A từng thấy do bạn trích; B khớp số dòng — không khớp đủ thì chỉ báo 36 câu).
- **Luật câu lỗi trích dẫn (500):** người dùng không thấy câu trả lời ⇒ câu đó tính **điểm 1** ở cả hai bên, gộp vào trung bình và số câu tụt; số câu 500 báo riêng.
- Sàn: 0 câu ngoài kho bị trả lời ở chatbot cuối; 0 lỗi kỹ thuật sau một lần chạy lại đúng câu đó. Mức tụt: Đủ / Đúng trung bình ≥ −0,1 và ≤ A/A + 3 câu tụt;
  từ chối nhầm ≤ +1 câu. "Tốt hơn" chỉ báo, không quyết (tập kiểm nhỏ).
- Chạy khi bạn quyết mở câu kín (sau B0 + merge 10 đoạn). Ước ≈ 0,012 USD, trần 0,03 USD.

### 27/10/2026 — nhãn đoạn đúng bản 2 (sáng) và bản 3 (chiều)

| | Bản 1 → 2 | Bản 2 → 3 |
|---|---|---|
| Vì sao | nhãn đánh dấu **một** chỗ cho mỗi ý, kho thường nói lại ở chỗ khác; một câu có ý nằm ở **dòng tiêu đề mục** bị đếm thiếu | 3 câu nhóm kiểm còn chưa ai đọc |
| Đổi | +3 chỗ nói lại (2 câu thử) + luật trúng dòng tiêu đề | 1 câu nhiều nguồn +1 chỗ nói lại; 1 câu so sánh gắn đúng trích dẫn nói thẳng ý so sánh; 1 câu giữ (thật sự thiếu) |
| Cách làm | C đề xuất (đọc tay, cắt nguyên văn) ⇒ B dựng + kiểm ⇒ C review ⇒ bạn duyệt | C đề xuất ⇒ B kiểm, B dựng ⇒ C review ⇒ bạn đồng ý |
| Đoạn đúng trong 10 đoạn — chatbot 10 đoạn, nhóm thử (40) | 22 → **24** | 24 → **24** |
| — biến thể "luna chọn 10 / 30 đoạn", nhóm thử | 31 → **33** | 33 → **33** |
| — chatbot 10 đoạn, nhóm kiểm (15) | — | 7 → **9** |
| — "luna chọn 10 / 30", nhóm kiểm | — | 10 → **11** |
| Kết luận đã đóng có đổi không | không (biến thể vẫn thắng 9, thua 0 ở tầng tìm; vẫn gác vì khâu trả lời kém hơn) | không |

Tiền 0 USD. Review: `report_agent/2026-10-26_cai_tien_tung_khau/gold_v2_review.md`, `gold_v3_review.md`.

### 26–27/10/2026 — đợt cải tiến từng khâu (8.2 Bước 2): thước đo đã dùng

- Mốc duy nhất: chatbot 10 đoạn + chuẩn hóa dấu (nhánh B1); mọi biến thể so với mốc này, cùng lượt mù.
- Luật nhận: (a) rẻ / nhanh hơn rõ mà chất lượng giữ (TB ≥ −0,1, câu tụt ≤ A/A + 3); (i) chất lượng tăng vượt nhiễu, tốc độ / tiền không tệ hơn (không thêm lần gọi API,
  USD / câu ≤ +20 %). "Tốc độ" khâu sinh đo bằng **số token ra / câu** (thời gian một lần gọi dao động quá mạnh để phân giải ±50 ms).
- Kết quả: 5 biến thể **kém hơn** theo luật; biến thể "luna chọn 10 / 30 đoạn" tốt hơn ở tầng tìm (tạm) nhưng khâu trả lời kém hơn theo luật (5 câu tụt > 4), chậm
  ≈ 4,6–5 s, ≈ 3,8 × tiền ⇒ gác. Bạn chốt đợt 27/10 sáng. Chi tiết: `bao_cao_he_thong/` các báo cáo khâu tìm / sinh; `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.
- Phát hiện về thước: 80 % điểm mất đi kèm thiếu bằng chứng trong ngữ cảnh (chỗ nghẽn là xếp hạng); nhãn một chỗ / ý làm đếm thiếu (dẫn tới bản 2).

### 25/10/2026 — Phase 8.1: làm thước đo chặt hơn (G0)

Tiêu chí ghi trước (spec 8.1): so theo cặp phải ra "không khác" khi so hai lượt như nhau, và "kém hơn" khi cố tình làm hỏng.

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Chia 120 thử / 56 kiểm theo loại câu | một dữ kiện 24, nhiều nguồn 9, điều kiện 9, so sánh 8, ngoài kho 6 ở nhóm kiểm | chọn phương án trên nhóm thử, chỉ xác nhận trên nhóm kiểm ⇒ tránh "tự chấm bài mình chọn" |
| Đối chứng âm (hai lượt 7B như nhau) | mọi chỉ số "không khác", ở cả tổng, từng loại câu và cả hai nhóm · **PASS** | thước không báo khác giả |
| Đối chứng dương (cố tình xáo top-10) | MRR, nDCG "kém hơn" rõ ở cả ba nhóm · **PASS** | thước bắt được thay đổi thật |
| Đoạn đúng cho 55 câu khó | agent gắn, agent khác kiểm (55/55 đúng nguồn), bạn xem mẫu · **PASS** | đo "đoạn có đáp án có lọt vào phần đưa model không", không chỉ đếm keyword |
| Nhãn độ tự nhiên 176 câu | 2 agent gắn độc lập, đồng ý cao (kappa 0,765); 9 câu bất đồng bạn giữ ⇒ 82 / 65 / 29 | số chính chỉ tính câu người dùng thật có thể hỏi |
| Nhiễu riêng của người chấm (G2) | cùng câu trả lời chấm 2 lần: "Đủ" đổi 2/88 câu, chênh TB 0,000; "Đúng" 1/88; "Trúng ý" 3/88 | nhiễu nhỏ; vẫn chấm mốc và biến thể trong **cùng một lượt mù** |
| Nhiễu "sinh lại + chấm lại" (G2.0 so 7B Run 1) | 10/83 câu đổi điểm "Đủ", chênh TB +0,048 | đây là lý do mỗi biến thể có mốc chạy lại cùng lúc |
| Câu kín | 36 câu: soạn mới, đủ dấu (25/10), 36/36 tự nhiên, sửa đáp án theo nguyên tắc bạn duyệt 12:20; chưa khóa | dùng cho chấm cuối 8.2; C không đọc nội dung, A chỉ thấy 3 câu do bạn trích khi hỏi (không đề xuất biến thể nhắm vào chúng) |

Tiền: 0 USD; chấm dùng quota Claude.

**Phát hiện làm đổi chẩn đoán cũ:** chẩn đoán 7B (dựa trên keyword) ghi "4/22 câu có đủ bằng chứng mà vẫn từ chối". Đo bằng
đoạn đúng ở 8.1 cho thấy **22/22 câu từ chối nhầm đều thiếu dữ kiện trong 5 đoạn đưa model**. Nguyên nhân chính là khâu tìm
và xếp đoạn, không phải model "từ chối vô cớ".

### 24/10/2026 — Phase 7B: bộ chấm và điểm mốc 176 câu (bản 1, A)

Bộ chấm tự động + điểm mốc của hệ thống hiện tại trên 176 câu Golden; mỗi cải tiến Phase 8 so với mốc này. Người chấm chính
là Claude (bạn chọn, để tiết kiệm), `gpt-6-luna` chấm phụ để so. Câu trả lời vẫn do `gpt-6-luna` sinh.

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Điểm mốc (Đúng / Đủ / Trúng ý) | **4,43 / 4,28 / 4,45** | Khá tốt tổng thể |
| Câu một dữ kiện (75 câu) | 4,87 / 4,84 / 4,89 | Gần hoàn hảo |
| Câu có điều kiện (29) | 4,72 / 4,41 / 4,76 | Tốt |
| Câu so sánh (25) | 3,68 / 3,44 / 3,60 | Yếu |
| Câu ghép nhiều nguồn (29) | **3,28 / 3,00 / 3,41** | Yếu nhất |
| Câu ngoài kho (18) | 5 / 5 / 5 — từ chối đúng 18/18 | Không bịa |
| Tìm đoạn (158 câu, keyword proxy @10) | MRR 0,72 · nDCG 0,755 · Keyword Coverage 92,4% | Đoạn chứa keyword đáp án thường lọt top-10; yếu ở câu so sánh (MRR 0,53) và nhiều nguồn (0,54) |
| **Từ chối nhầm** | **22 / 158 câu** | Đây là toàn bộ 22 câu bị 1/1/1; bỏ chúng ra điểm còn 4,92 / 4,75 / 4,95 |
| Lỗi trích dẫn (người dùng thấy lỗi) | 4 / 176 | Hiếm |
| Chạy lại toàn bộ lần 2 | chênh trung bình ≤ 0,011 điểm | Thước đo rất ổn định |
| Claude chấm lại 30 câu | không câu nào lệch quá 1 điểm | Người chấm ổn định |
| Claude so với gpt-6-luna | trùng 89–96% số câu | Hai người chấm khác hãng đồng ý cao |

Vì sao từ chối nhầm (chẩn đoán 22 câu, không tốn tiền; dấu hiệu, chưa chứng minh nguyên nhân). **Đã được 8.1 thay**, xem
mục 25/10 và §5:

| Phân loại (theo keyword đáp án trong 5 đoạn ngữ cảnh) | Số câu |
|---|---:|
| Đoạn chứa đáp án không nằm trong 5 đoạn ngữ cảnh | 8 |
| Có một vế, thiếu vế kia → bot từ chối cả câu | 10 |
| Có đủ bằng chứng mà vẫn từ chối | 4 |

12/22 câu có thêm keyword liên quan ở hạng 6–10, bị cắt vì chỉ giữ 5 đoạn. Thử nhanh với 10 đoạn (0,005 USD): 10/22 câu hết
từ chối (chưa chấm điểm, chỉ là dấu hiệu). 8.1 đã đo đầy đủ: 10 đoạn **tốt hơn**, đã xác nhận trên bộ kiểm.

Giới hạn ghi ở bản 1, nay vẫn đúng:
- chưa có người chấm tay (bạn quyết bỏ);
- 121/176 câu đã đạt tối đa, nên cải tiến chủ yếu lộ ở 55 câu còn lại;
- Golden do LLM viết, người duyệt;
- chỉ số truy xuất dựa trên keyword nên chỉ là "proxy".

Tiền: toàn bộ 7B + thử nhanh **~0,087 USD (~2.200 đồng)**. Claude chấm dùng quota Claude Code (~1,1M token).

## 5. Hôm nay còn đúng không

Kiểm ngày 27/10/2026 với `main` và các report 8.2 / đợt sửa kho.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Bộ chấm `full_corpus_eval.py` (`generate`, `compare`, `summarize`) | **còn dùng**; so theo cặp `paired_stats` | `backend/evaluation/full_corpus_eval.py:634` |
| Prompt chấm cố định | **còn dùng** (không chấm trích dẫn) | `backend/evaluation/full_corpus_judge_prompt.md` |
| Người chấm Claude, mù, cùng lượt | **còn dùng** | spec 8.2 §7; plan B3 §4 |
| Mốc chatbot (5 đoạn, `e5-small-384`, `dense_bm25_rrf`, không rerank) | **còn đúng** cho chatbot đang chạy; 10 đoạn ở nhánh B1, chờ B0 | `backend/config/settings.yaml`; `CURRENT_HANDOFF.md` |
| Mốc tìm T1 `cefb2d1ad609` | **còn dùng** tới đợt sửa kho (đổi sau build) | spec sửa kho §5 bước 6 |
| Nhãn đoạn đúng | **bản 3 mặc định** (`fa192f8`); bản 1, 2 chỉ để tái lập số cũ; **bản 4 sau sửa kho** | `g1_retrieval.py:47` |
| Số "lỗi trích dẫn" của lượt 10 đoạn 25/10 | **đã thay**: theo bộ kiểm hiện tại 0 / 12 câu đó lỗi | `c65_citation_138_check.md` |
| Điểm 7B Run 1 làm mốc | **lịch sử**; 10 câu Golden sửa đáp án 25/10 không so trực tiếp | `phase_8_1_golden_fix_review.md` |
| Chẩn đoán từ chối nhầm theo keyword | **đã thay** (8.1): 22 / 22 thiếu dữ kiện trong ngữ cảnh | report G1 8.1 §4 |
| "Chấm tay khoảng 20 câu" (bản 2 §6) | **đã thay** bởi B0: bạn đọc và nhận xét 20 cặp mù, không chấm điểm (bạn chọn 25/10) | spec 8.2 §3 mục 3–4 |

## 6. Việc còn lại / cần quyết

- **Bạn:** B0 (đọc 20 cặp mù, ghi nhận xét) — sau đó A tóm nhãn, áp luật dừng (spec 8.2 §3 mục 4): bạn ngược chiều người chấm Claude ở nhiều cặp hơn ⇒ dừng, xem
  lại người chấm trước khi đưa 10 đoạn vào chatbot.
- **Bạn:** quyết mở câu kín (B3) khi 8.2 xong.
- **Sau 8.2:** đợt sửa kho chạy theo spec đã duyệt — bộ "trước" (bước 0) trước khi đụng kho; nhãn bản 4 + Golden sửa từng mục bạn duyệt.
- **Còn mở (A xử lý):** đếm lại "lỗi trích dẫn" lượt 10 đoạn của 8.1 bằng bộ kiểm hiện tại; mọi report mới ghi kèm bản nhãn khi nêu số đoạn đúng.
- **Đề xuất cũ còn giữ:** gắn thêm đoạn đúng cho câu thử để tăng cỡ mẫu (40 câu làm nhiều kết quả "chưa rõ").

## Phụ lục — hồ sơ kỹ thuật

- **7B:** spec `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`; report `reports/phase_7b_*`; guide `guides/full_corpus_rag.md` "Cập nhật Phase 7B".
- **8.1 G0** (`report_agent/2026-10-24_phase_8_1_ra_soat/`): G0.1–G0.2 `phase_8_1_g0_1_2_measure_implementation.md`; G0.3 đoạn đúng `phase_8_1_g0_3_gold_review.md`;
  G0.4 câu kín `phase_8_1_g0_4_sealed_review.md`; nhiễu người chấm `phase_8_1_g2_implementation.md` §4.5; theo loại câu `phase_8_1_g5_by_category.md`.
- **8.2:** spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` (bản A duyệt `cd910c4c4169`; §3 mục 3–4 B0, §10.2 luật nhận); A/A 10 đoạn
  `phase_8_2_b1_implementation.md` §4 (nhánh `p82-b1`); plan câu kín `phase_8_2_b3_plan.md` (`27e75be5ed44`) + review; C65 `c65_citation_138_check.md`
  (`report_agent/2026-10-25_phase_8_2_ap_dung/`); nhãn bản 2 / 3: `c56_de_xuat_sua_nhan.md`, `gold_v2_*`, `c64_de_xuat_nhan_test.md`, `gold_v3_*`
  (`report_agent/2026-10-26_cai_tien_tung_khau/`).
- **Đợt sửa kho:** spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (`937cf8969810`) + `..._design_review.md` (3 vòng).
- **File private:** `split.json` `e2b1788dfbbc`; nhãn bản 1 `gold_draft.jsonl` `bab707b9ab22`, bản 2 `gold_v2.jsonl` `2f5a347a71ff`, bản 3 `gold_v3.jsonl` `3b1117cf59e9`
  (`data/phase_8_1/gold/`); độ tự nhiên `golden_realism_final.jsonl` `0b65d1c138d2`; câu kín `sealed_official.jsonl` md5 `ddc59587b502` (manifest G0.6 `9ea480d0d083`);
  Golden md5 `0f7dbf41b422`; B0 `data/phase_8_2/b0/`.
- Bản 1: A, 24/10/2026. Bản 2: C30, 25/10/2026. Bản 3: C69, 27/10/2026.
