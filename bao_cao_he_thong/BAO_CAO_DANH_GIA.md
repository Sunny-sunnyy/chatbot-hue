# Báo cáo cho bạn: Đánh giá — thước đo chất lượng và điểm mốc (Phase 7B, 8.1, 8.2, đợt sửa kho 1–2)

**Cập nhật lần cuối: 17:12 31/10/2026 — bản 6: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này. Người viết: sub-agent của A (bản 6) · Review: agent con ngữ cảnh mới (31/10). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (đúng hiện trạng 31/10/2026)

- **Khâu này làm gì:** chấm chatbot tự động, lặp lại được: mọi thay đổi so với một **điểm mốc** trên cùng bộ câu, theo luật ghi **trước** khi chạy,
  rồi mới quyết giữ hay bỏ.
- **Thước đang dùng:**
  - **Golden 176 câu** (md5 `6331e88fb171` từ 30/10), chia **120 câu thử** (để chọn) / **56 câu kiểm** (để xác nhận). Số chính bỏ 29 câu người thật ít hỏi.
  - Bộ chấm đi đúng đường của API (tìm đoạn → đóng gói đoạn → `gpt-6-luna` trả lời → kiểm trích dẫn).
  - Chấm câu trả lời: Claude chấm 3 điểm 1–5 (Đúng / Đủ / Trúng ý), **mù** — mốc và biến thể trộn chung một lượt, người chấm không biết câu nào của bên nào.
  - So hai cấu hình **theo cặp từng câu** (bootstrap 10.000 lần — rút lại ngẫu nhiên các câu để ước khoảng tin cậy 95 %; đếm thắng / hòa / thua; nhiều biến thể cùng lúc ⇒ hiệu
    chỉnh Holm để không nhận nhầm một biến thể chỉ "thắng may").
  - Tầng tìm: **nhãn đoạn đúng bản 5** (từ 30/10, khớp kho sau đợt 2 sửa kho) cho 55 câu khó — đo "đoạn có đáp án có lọt vào phần đưa model không";
    mọi số đoạn đúng phải ghi kèm bản nhãn.
  - Câu người dùng nhận lỗi trích dẫn (500) tính **điểm 1** khi so.
  - **Thước lỗi nặng:** người chấm Claude tách từng ý của câu trả lời, so với chính ngữ cảnh model đọc ⇒ đếm **bịa thêm** và **sai điều kiện** (giờ, vé,
    quy định, cảnh báo). **Bộ 32 câu an toàn** tự viết (giờ, vé, miễn giảm, giấy tờ, cảnh báo sông nước…; 28 trong kho, 4 ngoài kho) là phép kiểm **bắt buộc** cho
    mọi thay đổi, kèm 15 câu đối chứng (chèn sai / chép đúng) để kiểm người chấm mỗi lượt.
  - **Bộ 15 câu theo ngày tương đối** ("tối nay", "tháng sau"…, 30/10) — mốc cho việc Phase 9.
- **Thước "đạt" (bạn chốt 28/10):**
  - **Thứ tự lỗi** nặng → nhẹ: sai cảnh báo an toàn / điều kiện vào khu vực > nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.
  - **Sàn bộ an toàn** (theo nhiễu đo 29/10): câu sai điều kiện **mới** ≤ 2, mỗi câu mới sinh lại 3 lần; **đảo cảnh báo = 0**; 0 câu ngoài kho bị trả lời.
  - **Tốc độ / tiền:** trung vị ≤ 3 s, p95 ≤ 5 s, ≤ 0,0005 USD / câu. Hôm nay đo cho **cả câu**; khi streaming chạy, sàn thời gian đo tới **chữ trả lời đầu tiên
    hiện trên trình duyệt** (bạn chốt 31/10).
- **Số của chatbot đang chạy** (10 đoạn, kho sửa hai đợt, 30/10):
  - Golden 176: từ chối nhầm **12 / 158**; 0 câu ngoài kho bị trả lời; 0 lỗi trích dẫn; trung vị **2,19 s** / p95 **4,90 s** (đo trong công cụ, chưa tính mạng tới web);
    **≈ 0,00025 USD / câu** theo giá đủ (công cụ ghi ~0,00021 — thiếu ≈ 20 %, mục 3).
  - Bộ 32 câu an toàn: **0** câu sai điều kiện, 0 bịa thêm, 0 / 4 câu ngoài kho bị trả lời.
  - Đoạn đúng: nhóm thử **24 / 40** câu có đủ mọi đoạn đúng trong ngữ cảnh; cả 55 câu **33 / 55**, tỉ lệ ý có trong ngữ cảnh **0,76** (nhãn bản 5).
  - **Câu kín (28/10):** chatbot cuối 8.2 so với đầu 8.2 trên 33 câu trong kho: **Đủ +0,82**, **Đúng +0,70**, 0 câu tụt.
  - Nhiễu "hai lượt cùng cấu hình" (A/A) ở 10 đoạn, 176 câu: Đủ tụt 1 câu, Đúng tụt 2 câu — nhiễu nền cho luật "không làm hỏng".
  - Điểm Đúng / Đủ / Trúng ý trung bình tuyệt đối chỉ có ở mốc 7B (5 đoạn, 24/10): **4,43 / 4,28 / 4,45**; các lượt sau báo chênh theo cặp.
- **Giới hạn chính:**
  - **1 câu Golden** còn keyword không khớp kho sau 2 đợt sửa kho (phát hiện 31/10, chờ bạn duyệt) ⇒ điểm keyword của câu đó lệch tới khi sửa;
  - **chưa có mốc người** — bạn đọc 20 cặp câu trả lời mù để sau (trước buổi bảo vệ); mọi kết luận dựa điểm Claude là tạm;
  - chỉ 40 câu thử / 15 câu kiểm có nhãn đoạn đúng ⇒ nhiều kết quả tầng tìm chỉ "chưa rõ";
  - nhóm kiểm 56 câu và 36 câu kín **đều đã dùng** ⇒ phép kiểm cuối sau cần bộ câu mới chưa ai nhìn;
  - đáp án mẫu không nhạy với sửa kho kiểu "thêm tên mới / bỏ chi tiết không chắc" ⇒ hai đợt sửa kho không làm điểm tăng dù kho đúng hơn;
  - thước lỗi nặng và bộ an toàn do agent viết + Claude chấm, chưa có người đọc; bộ an toàn chỉ 28 câu trong kho ⇒ 0 lỗi vẫn chỉ nói được tỉ lệ sai điều kiện dưới ~12 %.
- **Chi phí đã tiêu cho đánh giá** (theo giá phẳng, thực tế cao hơn ≈ 20 %): 7B ~0,087 USD; 8.1 ~0,165; 8.2 ≈ 0,227 / trần 0,5; sửa kho đợt 1 ≈ 0,073, đợt 2 ≈ 0,047.
  Chấm bằng Claude dùng quota Claude Code (không USD).
- **Bạn cần quyết:** không có việc gấp. Khi tiện: đọc cặp mù (~30–45 phút) làm mốc người đầu tiên.

## 2. Hoạt động thế nào (bản đang chạy)

```text
Mốc / biến thể:  176 câu Golden → đường của API (tìm → đóng gói N đoạn → gpt-6-luna → kiểm trích dẫn)
                 → tầng tìm: từ khóa @10 (miễn phí) + đoạn đúng theo tầng: kho ứng viên → top-10 → N đoạn đưa model (nhãn bản 5)
                 → câu trả lời mốc + biến thể trộn MÙ → Claude chấm Đúng / Đủ / Trúng ý (1–5)
                 → so theo cặp từng câu: chênh, CI 95 %, thắng / hòa / thua; nhiều biến thể ⇒ Holm
                 → bắt buộc: bộ 32 câu an toàn qua thước lỗi nặng
                 → luật ghi trước: sàn · mức tụt cho phép · 1–2 chỉ số quyết
```

- **Luật ghi trước (ba lớp):** sàn không được vi phạm (0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật; 0 "nói chắc sai" mới; sàn bộ an toàn) · mức tụt cho phép
  (điểm Đủ / Đúng trung bình ≥ −0,1 **và** số câu tụt ≤ nhiễu A/A + 3) · chỉ số quyết phải tốt lên vượt nhiễu. Nhóm kiểm nhỏ ⇒ xác nhận ở nhóm kiểm = **"không làm hỏng"**.
- **Thay đổi chạm kho** (sửa kho, dựng lại chỉ mục): đo "trước ↔ sau" trên cùng Golden, chấm hai bên trong một lượt mù; câu có đoạn ngữ cảnh chạm chỗ sửa
  tách báo riêng; trung bình kiểm cả trên tập không chạm để câu chạm không làm số đẹp giả; xoá dòng làm mã đoạn dồn số ⇒ mọi câu dùng đoạn của file đó tính là "chạm".
- **Nhãn đoạn đúng:** một ý "có trong ngữ cảnh" khi **một** trích dẫn bất kỳ của ý trúng đoạn (giao vị trí, hoặc nhãn là dòng tiêu đề nằm trong đường tiêu đề
  của đoạn); câu "đủ đoạn đúng" khi **mọi** ý đều có. Kho đổi ⇒ dựng lại vị trí nhãn (bản mới), bạn duyệt trích dẫn đổi chữ; bản cũ giữ để tái lập số cũ.
- Code:
  - bộ chấm `backend/evaluation/full_corpus_eval.py` (lệnh `retrieval` / `generate` / `export-judge-input` / `compare` / `split` `:802–843`; `answer_case` :322,
    `is_refusal` :162, `cost_usd` :167, `bootstrap_mean_diff` :590, `paired_stats` :634, 10.000 vòng :55);
  - prompt chấm `backend/evaluation/full_corpus_judge_prompt.md`;
  - nhãn: `backend/experiments/phase_8_1/g1_retrieval.py` (`GOLD_PATH` :48 = bản 5, `quote_is_chunk_heading` :77, `chunk_hits_quote` :83, `gold_coverage` :94);
    test `backend/tests/test_gold_coverage.py`;
  - harness thí nghiệm `backend/experiments/phase_8_1/`, `phase_8_2/` (một số chỉ trên nhánh / tag hồ sơ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Chấm tìm đoạn bằng từ khóa (MRR, nDCG, Keyword Coverage @10) | **Đã xử lý, đóng gói** | mốc 7B; `full_corpus_eval.py` lệnh `retrieval` |
| Chấm câu trả lời bằng Claude (Đúng / Đủ / Trúng ý), mù, cùng lượt | **Đã xử lý, đóng gói** | nhiễu riêng người chấm: Đủ đổi 2 / 88 câu |
| Từ chối đúng / từ chối nhầm, lỗi trích dẫn | **Đã xử lý, đóng gói** | `is_refusal` `full_corpus_eval.py:162`; lỗi trích dẫn đếm theo bộ kiểm hiện tại (từ 25/10) |
| So theo cặp + CI + Holm; đối chứng âm / dương | **Đã xử lý, đóng gói** | `paired_stats` `full_corpus_eval.py:634`; đối chứng 8.1 đạt (mục 4) |
| Nhóm thử 120 / nhóm kiểm 56 | **Đã xử lý, đóng gói** | `split.json` seed cố định; nhóm kiểm **đã dùng** |
| Nhiễu A/A ở 10 đoạn | **Đã xử lý** | 176 câu: Đủ tụt 1, Đúng tụt 2 |
| Đoạn đúng cho câu khó | **Xử lý một phần** | 55 / 176 câu (40 thử / 15 kiểm); **bản 5**; câu khác chỉ có từ khóa; `g1_retrieval.py:77–94` + test |
| Nhãn độ tự nhiên (bỏ câu người thật ít hỏi) | **Đã xử lý** | 82 tự nhiên / 65 chỉ đo năng lực / 29 bỏ |
| Bộ câu kín cho chấm cuối 8.2 | **Đã xử lý, đóng gói** (chạy 28/10) | 36 câu; tốt hơn, không làm hỏng (mục 4); **đã dùng** ⇒ cần bộ mới trước bảo vệ |
| Mốc người (bạn đọc cặp mù) | **Chưa thực hiện** (dời — trước buổi bảo vệ) | 20 cặp đã chuẩn bị (`data/phase_8_2/b0/`); không chặn việc nào (bạn chọn 28/10) |
| Câu lỗi trích dẫn tính là hỏng (điểm 1) | **Đã xử lý** | dùng ở câu kín và hai đợt sửa kho; chưa vào bộ chấm chung `full_corpus_eval` |
| Thước "trước ↔ sau" khi sửa kho | **Đã xử lý, đóng gói** | sàn ngoài kho / lỗi / 500 mới / nói chắc sai mới + mức tụt + câu chạm báo riêng + bộ an toàn + luật "chạm theo file"; hai đợt **không làm hỏng** (mục 4) |
| "Bịa thêm" và "sai điều kiện / cảnh báo" | **Đã xử lý** (từ 28/10, bạn nhận 29/10) | Golden 28/10: bịa thêm 1 / 145, sai điều kiện 0 / 65; bộ an toàn 30/10: 0 / 28 sai điều kiện, 0 bịa; nhiễu hai lượt: 2 câu dao động ⇒ sàn "mới ≤ 2 + sinh lại 3 lần"; chưa có người đọc |
| Bộ câu an toàn | **Đã xử lý** (bắt buộc từ 29/10) | 32 câu, agent viết; đợt 2: cả 2 người chấm bắt 10 / 10 câu chèn sai |
| Kiểm số trong câu trả lời phải có trong nguồn | **Đã thử, chưa áp dụng** | 27/10: 68 câu có số, 0 lỗi thấy được ⇒ chưa cần kiểm bằng code; chỉ dùng chọn câu đọc lại |
| Câu hỏi theo ngày tương đối | **Đã xử lý** (đo, 30/10) | 15 câu: 0 câu đoán ngày rồi nói sai; 6 / 14 câu trong kho bị từ chối nhầm ⇒ Phase 9 |
| Tốc độ / tiền theo yêu cầu bạn chốt | **Xử lý một phần** | Golden 176 (tuần tự, trong công cụ): 2,19 / 4,90 s ⇒ đạt sát; câu trả lời dài (8 câu tự viết, 28/10) 4,6 / 7,6 s ⇒ chưa đạt; chưa đo qua trình duyệt. Tiền: giá đủ ≈ 0,00025 USD / câu ⇒ đạt; `cost_usd` (`full_corpus_eval.py:167`) tính giá phẳng ⇒ ghi thiếu ≈ 20 %, sửa ở đóng gói |
| Thời gian "tới chữ đầu tiên" trên trình duyệt (streaming) | **Chưa thực hiện** — đang thiết kế | spec streaming: đo bằng trình duyệt tự động trên 40 câu thử tự nhiên, câu từ chối báo riêng; chưa code |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (mới ở trên)

Mỗi mục: thước / phép đo gì · kết quả · giữ / bỏ · hồ sơ.

### 30/10/2026 — "trước ↔ sau" đợt 2 sửa kho: không làm hỏng
- Bộ "trước" = bộ "sau" của đợt 1 (dùng lại, không tốn tiền); bộ "sau" chạy mới; Golden sửa 2 đáp án mẫu (bạn chọn), chấm cả hai bên bằng đáp án mới trong một lượt mù.
  Thêm vào thước: **bộ 32 câu an toàn** và luật **"chạm theo file"**.
- Golden: 0 câu ngoài kho bị trả lời · 0 lỗi · 0 lỗi trích dẫn mới · 0 nói chắc sai mới · Đủ +0,008 (4 tăng / 3 tụt / 129 câu) · Đúng 0,000 · từ chối nhầm 13 → 12 · không
  câu nào mất đoạn đúng. Bộ an toàn: 0 câu sai điều kiện mới, 0 đảo cảnh báo; 2 câu sai ở lượt 28/10 nay không sai (sinh lại 3 lần cũng 0) ⇒ "lúc có lúc không".
  **Không làm hỏng ⇒ bạn đóng đợt.** ≈ 0,047 USD. `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md`.
- Cùng ngày: **nhãn đoạn đúng bản 5** (173 / 174 trích dẫn tìm lại nguyên văn; 1 đổi chữ, bạn duyệt) và **Golden md5 `6331e88fb171`**. Thí nghiệm Qwen3-8B (tầng tìm) dùng
  thước này: kém hơn ⇒ không tới bước kiểm cuối (`BAO_CAO_EMBEDDING_TU_KHOA.md`).
- **Câu hỏi theo ngày tương đối** (15 câu + 11 câu bộ an toàn, 0,0037 USD): 0 câu đoán ngày rồi nói sai (với cỡ mẫu này chỉ nói được tần suất dưới ~25 %); 6 / 14 câu
  bị từ chối nhầm ⇒ bạn quyết để Phase 9. `report_agent/2026-10-27_phan_ton_phase_cu/ngay_hien_tai_implementation.md`.

### 28/10/2026 — "trước ↔ sau" đợt 1 sửa kho: không làm hỏng
- Thước mới: sàn **"nói chắc sai" mới** (câu trả lời có điểm Đúng ≤ 3 mà người dùng thấy); **câu chạm phần sửa** tách bằng máy (43 / 176); kiểm cả tập không chạm;
  mức tụt dùng A/A = 2. Golden không đổi.
- Kết quả: 0 câu ngoài kho bị trả lời · 0 lỗi · 0 nói chắc sai mới · Đủ −0,008 (4 / 4) · Đúng 0,000 · từ chối nhầm 12 → 13 (đúng mức cho phép) ⇒ **không làm hỏng**.
  p95 lượt "sau" 9,8 s do phía mạng / nhà cung cấp ⇒ không đại diện. ≈ 0,073 USD. `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b9_implementation.md`.
- **Thước lỗi nặng** ra đời cùng ngày (bạn nhận 29/10). `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_implementation.md`, nhiễu `do_loi_nang_aa_implementation.md`.

### 28/10/2026 — mốc cuối 8.2 trên câu kín
- Chatbot đầu 8.2 (5 đoạn, bộ kiểm trích dẫn cũ) ↔ cuối 8.2 (10 đoạn + chuẩn hóa dấu + bộ kiểm mới) trên 36 câu kín; người chạy chỉ in số đếm, người chấm Claude mới.
- 33 câu trong kho: **Đủ +0,82** [+0,39; +1,33] (12 thắng / 0 thua), **Đúng +0,70** [+0,27; +1,21]; câu ngoài kho từ chối đúng 3 / 3; từ chối nhầm 4 → 2; bỏ riêng 4 câu
  lỗi trích dẫn kiểu cũ vẫn Đủ +0,45 ⇒ lợi không chỉ do bộ kiểm mới. **Tốt hơn, không làm hỏng ⇒ 8.2 đóng.** Câu kín nay đã dùng. ≈ 0,014 USD.
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_implementation.md`.

### 27/10/2026
- **Lượt 10 đoạn ngày 25/10 chấm trích dẫn bằng bộ kiểm cũ:** 12 / 176 câu ghi "lỗi" đều qua bộ kiểm hiện tại ⇒ số đó không dùng; kết luận các thí nghiệm so với mốc
  này không đảo. `report_agent/2026-10-25_phase_8_2_ap_dung/c65_citation_138_check.md`.
- **Nhãn đoạn đúng bản 2 và 3:** thêm chỗ kho nói lại cùng ý + luật trúng dòng tiêu đề (bản 2), sửa 2 câu nhóm kiểm (bản 3); chatbot 10 đoạn nhóm thử 22 → 24 / 40;
  không kết luận đã đóng nào đổi. `report_agent/2026-10-26_cai_tien_tung_khau/gold_v2_review.md`, `gold_v3_review.md`.

### 26–27/10/2026 — đợt cải tiến từng khâu (8.2): thước đã dùng
- Mốc duy nhất: chatbot 10 đoạn + chuẩn hóa dấu; luật nhận: (a) rẻ / nhanh hơn rõ mà chất lượng giữ; (i) chất lượng tăng vượt nhiễu, tiền / câu ≤ +20 %. "Tốc độ" khâu
  sinh đo bằng số token viết ra (thời gian một lần gọi dao động quá mạnh).
- Kết quả: không biến thể nào qua luật (chi tiết từng biến thể: `BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `BAO_CAO_TIM_KIEM.md`). Phát hiện: 80 % điểm mất đi kèm thiếu bằng
  chứng trong ngữ cảnh (chỗ nghẽn là xếp hạng). `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.

### 25/10/2026 — Phase 8.1: làm thước đo chặt hơn
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Chia 120 thử / 56 kiểm theo loại câu | nhóm kiểm có đủ các loại (một dữ kiện, nhiều nguồn, điều kiện, so sánh, ngoài kho) | chọn trên nhóm thử, xác nhận trên nhóm kiểm ⇒ tránh "tự chấm bài mình chọn" |
| Đối chứng âm (hai lượt như nhau) | mọi chỉ số "không khác" · **PASS** | thước không báo khác giả |
| Đối chứng dương (cố tình xáo top-10) | MRR, nDCG "kém hơn" rõ · **PASS** | thước bắt được thay đổi thật |
| Đoạn đúng cho 55 câu khó | agent gắn, agent khác kiểm (55 / 55 đúng nguồn), bạn xem mẫu · **PASS** | đo được đoạn có đáp án có lọt vào ngữ cảnh không |
| Nhãn độ tự nhiên 176 câu | 2 agent độc lập, kappa 0,765; 9 câu bất đồng bạn giữ ⇒ 82 / 65 / 29 | số chính chỉ tính câu người dùng thật có thể hỏi |
| Nhiễu riêng người chấm | chấm lại cùng câu trả lời: Đủ đổi 2 / 88, Đúng 1 / 88, Trúng ý 3 / 88 | vẫn chấm mốc và biến thể trong cùng một lượt mù |
| Nhiễu "sinh lại + chấm lại" | 10 / 83 câu đổi điểm Đủ | lý do mỗi biến thể có mốc chạy lại cùng lúc |

Phát hiện đổi chẩn đoán cũ: đo bằng đoạn đúng, **22 / 22 câu từ chối nhầm** của 7B đều thiếu dữ kiện trong 5 đoạn đưa model (chẩn đoán theo từ khóa trước đó ghi 4 / 22
câu "đủ mà vẫn từ chối" — sai). 0 USD. `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`.

### 24/10/2026 — Phase 7B: bộ chấm và điểm mốc 176 câu
Người chấm chính là Claude (bạn chọn, để tiết kiệm), `gpt-6-luna` chấm phụ để so. Mốc **5 đoạn** — nay là lịch sử, chatbot đã chuyển 10 đoạn.

| Nội dung | Kết quả |
|---|---|
| Đúng / Đủ / Trúng ý | **4,43 / 4,28 / 4,45** |
| Theo loại câu: một dữ kiện · có điều kiện · so sánh · nhiều nguồn | 4,87 / 4,84 / 4,89 · 4,72 / 4,41 / 4,76 · 3,68 / 3,44 / 3,60 · **3,28 / 3,00 / 3,41** |
| Câu ngoài kho | từ chối đúng 18 / 18 |
| Tìm đoạn (158 câu, từ khóa @10) | MRR 0,72 · nDCG 0,755 · Keyword Coverage 92,4 % |
| Từ chối nhầm | 22 / 158 |
| Độ ổn định | chạy lại lần 2 chênh ≤ 0,011 điểm; Claude chấm lại 30 câu không lệch quá 1 điểm; Claude ↔ `gpt-6-luna` trùng 89–96 % |

Giới hạn còn đúng: Golden do LLM viết, người duyệt; chỉ số tìm theo từ khóa chỉ là "proxy"; 121 / 176 câu đã đạt tối đa nên cải tiến lộ ở 55 câu còn lại.
~0,087 USD. `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`; `reports/phase_7b_*`.

## 5. Hôm nay còn đúng không

Kiểm với code `main` (`1985a81`) lúc 17:12 31/10/2026 và `session_prompt/Project_Status.md` §4, `CURRENT_HANDOFF.md`.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Bộ chấm `full_corpus_eval.py`, so theo cặp | **còn dùng** | `backend/evaluation/full_corpus_eval.py:634,802–843` |
| Prompt chấm cố định (không chấm trích dẫn) | **còn dùng** | `backend/evaluation/full_corpus_judge_prompt.md` |
| Người chấm Claude, mù, cùng lượt | **còn dùng** | spec 8.2 §7 |
| Mốc so sánh chatbot | **còn dùng**: 10 đoạn + chuẩn hóa dấu, kho 204 file / 8.424 đoạn, bộ "sau" đợt 2 (30/10) | `backend/config/settings.yaml:56`; `sua_kho_dot2_implementation.md` |
| Mốc kết quả tìm 158 câu | **còn dùng**: `4d5bbe9e0edc` (30/10) | `Project_Status.md` §4 |
| Nhãn đoạn đúng | **bản 5 mặc định** (30/10); bản 1–4 chỉ để tái lập số cũ | `backend/experiments/phase_8_1/g1_retrieval.py:48` |
| Golden | **còn dùng**: md5 `6331e88fb171` (30/10) | `BAO_CAO_BO_CAU_HOI_GOLDEN.md` |
| Bộ 32 câu an toàn, thước lỗi nặng | **còn dùng**, bắt buộc | `do_loi_nang_implementation.md`; `sua_kho_dot2_implementation.md` |
| `cost_usd` của công cụ đo | **ghi thiếu ≈ 20 %** — sửa ở đóng gói | `full_corpus_eval.py:167`; `Project_Status.md` §5 (30/10 15:07) |
| Điểm 7B làm mốc | **lịch sử** (5 đoạn; 10 đáp án Golden sửa 25/10, 2 đáp án sửa 30/10 ⇒ không so trực tiếp) | `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md` |
| Chẩn đoán từ chối nhầm theo từ khóa | **đã thay** (8.1): 22 / 22 thiếu dữ kiện trong ngữ cảnh | report G1 8.1 |
| "Chấm tay khoảng 20 câu" | **đã thay** bởi đọc cặp mù: bạn đọc và nhận xét 20 cặp, không chấm điểm (bạn chọn 25/10) | spec 8.2 §3 mục 3–4 |

## 6. Việc còn lại / cần quyết

- **Bạn, khi tiện (trước buổi bảo vệ):** đọc 20 cặp câu trả lời mù — mốc người đầu tiên; nếu bạn ngược người chấm Claude ở nhiều cặp ⇒ A trình giữ 10 đoạn / về 5 và xét lại
  các kết luận dựa người chấm Claude. Thêm: 20 câu mẫu lỗi nặng để bạn đọc (`data/loi_nang_2026-10-28/human_sample.md`).
- **Streaming (đang thiết kế):** thước mới "tới chữ trả lời đầu tiên trên trình duyệt" — sàn 3 / 5 s đã chốt; còn một câu về mục tiêu báo cáo kèm theo + bạn duyệt spec.
  `docs/superpowers/specs/2026-10-31-streaming-design.md`.
- **Đóng gói Phase 1–8:** sửa `cost_usd` theo giá đủ; **bộ câu kín mới** cho phép kiểm cuối (nhóm kiểm và câu kín đã dùng); câu an toàn do **người dùng thật** viết nếu có.
- **Còn mở (A xử lý):** đếm lại "lỗi trích dẫn" lượt 10 đoạn của 8.1 (8 câu) bằng bộ kiểm hiện tại; mọi report mới ghi kèm bản nhãn khi nêu số đoạn đúng.
- **Đề xuất còn giữ:** gắn thêm đoạn đúng cho câu thử để tăng cỡ mẫu (40 câu làm nhiều kết quả "chưa rõ").

## Phụ lục — hồ sơ kỹ thuật

- **Mã việc:** đọc cặp mù = **B0** (`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md`); câu kín = B3 (plan `phase_8_2_b3_plan.md` sha
  `27e75be5ed44`, review C74); A/A 10 đoạn `phase_8_2_b1_implementation.md` §4 (nhánh `p82-b1`); trích dẫn kiểu cũ = C65; nhãn bản 2 / 3 = C56 / C64 (B dựng,
  `report_agent/2026-10-26_cai_tien_tung_khau/`); đợt 1 = B78–B83 (báo cáo bản 4: B86; `sua_kho_do_truoc_sau_plan.md` sha `41485782b39e`, nhãn bản 4 `sua_kho_b7_8_implementation.md`, review C72,
  C76, C80); đợt 2 = B90–B93 (báo cáo bản 5: B97; plan `sua_kho_dot2_do_plan.md` sha `2adef0d4e5fc`, review C85, `sua_kho_dot2_b2_6_review.md`); thước lỗi nặng = B89, nhiễu = C84; ngày tương
  đối = C93 (plan B96); giá đủ = B95. Mã trong report đợt 1–2: F1–F4 = sàn, T1–T3 = mức tụt (khác "T1" mốc kết quả tìm 158 câu), W1–W9 = theo dõi.
- **Spec:** 7B `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`; 8.1 `2026-10-24-phase-8-1-decision-audit-design.md`; 8.2
  `2026-10-25-phase-8-2-apply-winners-design.md` (bản A duyệt `cd910c4c4169`; §3 mục 3–4 B0, §10.2 luật nhận, §11 luật dừng); sửa kho
  `2026-10-27-sua-kho-build-lai-index-design.md` (`937cf8969810`); streaming `2026-10-31-streaming-design.md` (bản 4 `cf1ae9ef6c2c`, §6 C1 thước chữ đầu tiên).
- **8.1 G0** (`report_agent/2026-10-24_phase_8_1_ra_soat/`): `phase_8_1_g0_1_2_measure_implementation.md`; đoạn đúng `phase_8_1_g0_3_gold_review.md`; câu kín
  `phase_8_1_g0_4_sealed_review.md`; nhiễu người chấm `phase_8_1_g2_implementation.md` §4.5; theo loại câu `phase_8_1_g5_by_category.md`.
- **File private (không commit):** `split.json` `e2b1788dfbbc`; nhãn `data/phase_8_1/gold/`: bản 1 `gold_draft.jsonl` `bab707b9ab22`, bản 2 `2f5a347a71ff`, bản 3
  `3b1117cf59e9`, bản 4 `927bae1bf201`, **bản 5 `gold_v5.jsonl` `33d16fd6b8f4`**; độ tự nhiên `golden_realism_final.jsonl` `0b65d1c138d2`; câu kín md5 `ddc59587b502`
  (manifest G0.6 `9ea480d0d083`); Golden md5 **`6331e88fb171`** (trước `0f7dbf41b422`); bộ an toàn `data/loi_nang_2026-10-28/an_toan/` (`questions.jsonl` `9fa81b0fcec4`);
  đọc cặp mù `data/phase_8_2/b0/`.
- Bản nhãn: bản 1 — mọi số đoạn đúng trước 27/10; bản 2 — 27/10 sáng; bản 3 — kho trước sửa (27/10 chiều–28/10); bản 4 — kho đợt 1 (28/10–30/10); bản 5 — kho đợt 2 (từ 30/10).
