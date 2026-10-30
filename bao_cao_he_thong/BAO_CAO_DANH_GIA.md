# Báo cáo cho bạn: Đánh giá — thước đo chất lượng và điểm mốc (Phase 7B, 8.1, 8.2, đợt sửa kho 1–2)

**Cập nhật lần cuối: 14:32 30/10/2026 — bản 5: nhãn "đoạn đúng" bản 5 (sau đợt 2 sửa kho) là mặc định; Golden sửa 2 đáp án (md5 `6331e88fb171`); thước
"trước ↔ sau" đợt 2 (thêm bộ 32 câu an toàn bắt buộc, luật "chạm theo file") và kết quả: không làm hỏng, 0 câu nói sai điều kiện mới; thước "lỗi nặng" đã có.**
Trước đó 12:14 28/10/2026 — bản 4 (nhãn bản 4, đợt 1, câu kín). Người viết: A (bản 1, 24/10), C (bản 2, 25/10; bản 3, 27/10), B (bản 4, 28/10; bản 5, 30/10) ·
Review: B (bản 2), A (bản 3–5). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chấm chatbot tự động, lặp lại được: mọi thay đổi so với một **điểm mốc** trên cùng bộ câu, theo luật ghi **trước** khi chạy,
  rồi mới quyết giữ hay bỏ.
- **Đang chạy cách nào:**
  - Bộ chấm đi đúng đường API thật (tìm đoạn → đóng gói đoạn → `gpt-6-luna` trả lời → kiểm trích dẫn).
  - Chấm câu trả lời: Claude chấm 3 điểm 1–5 (Đúng / Đủ / Trúng ý), chấm **mù** — mốc và biến thể trộn chung một lượt, người chấm không biết câu nào của bên nào.
  - So hai cấu hình **theo cặp từng câu** (bootstrap 10.000 lần, CI 95 %, thắng / hòa / thua); nhóm **thử** 120 câu để chọn, nhóm **kiểm** 56 câu để xác nhận;
    **36 câu kín** là phép kiểm cuối (đã dùng 28/10).
  - Tầng tìm: đo "đoạn có đáp án có lọt vào phần đưa model không" bằng **nhãn đoạn đúng** — đang dùng **bản 5** (từ 30/10, sau đợt 2 sửa kho); mọi số đoạn đúng
    phải ghi kèm bản nhãn (§2).
  - Câu người dùng thấy lỗi trích dẫn (500) tính **điểm 1** khi so (đã dùng ở câu kín và hai đợt sửa kho).
  - **Thước "lỗi nặng"** (từ 28/10, bạn nhận 29/10): người chấm Claude tách từng ý của câu trả lời, so với chính ngữ cảnh model đọc ⇒ đếm **bịa thêm** (ý không có /
    trái ngữ cảnh) và **sai điều kiện** (sai ở giờ, vé, quy định, cảnh báo). Có **bộ 32 câu an toàn** tự viết (giờ, vé, miễn giảm, giấy tờ, cảnh báo sông nước…) là
    phép kiểm **bắt buộc** cho mọi thay đổi; 15 câu đối chứng chèn sai / chép đúng để kiểm người chấm mỗi lượt.
- **Thước "đạt" (bạn chốt 28/10):**
  - **Thứ tự lỗi** nặng → nhẹ: sai cảnh báo an toàn / điều kiện vào khu vực > nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm. Bộ chấm điểm
    bắt "trả lời câu ngoài kho", "thiếu ý", "từ chối nhầm", "nói ngược đáp án mẫu"; thước lỗi nặng bắt "bịa thêm" và "sai điều kiện". **Sàn bộ an toàn** (theo nhiễu
    đo 29/10): câu sai điều kiện **mới** ≤ 2, mỗi câu mới sinh lại 3 lần; **đảo cảnh báo = 0**.
  - **Tốc độ / tiền** cả câu: trung vị ≤ 3 s, câu chậm (p95) ≤ 5 s, ≤ 0,0005 USD / câu.
- **Số mốc chính:**
  - 7B (24/10, 176 câu, 5 đoạn): Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45; từ chối nhầm 22 / 158.
  - Chatbot hiện tại (10 đoạn, kho sửa hai đợt, 176 câu, 30/10): từ chối nhầm **12 / 158**; 0 câu ngoài kho bị trả lời; 0 lỗi trích dẫn; ~0,0002 USD / câu;
    trung vị 2,19 s / câu chậm 4,90 s (đo trong công cụ, chưa tính đường mạng tới web).
  - Bộ 32 câu an toàn (30/10): 0 câu ngoài kho bị trả lời; **0 câu sai điều kiện**, 0 câu bịa thêm (lượt 28/10 có 2 câu sai điều kiện — đều "lúc có lúc không").
  - **Câu kín (28/10)**, chatbot cuối 8.2 so với đầu 8.2 trên 33 câu trong kho: **Đủ +0,82**, **Đúng +0,70**, 0 câu tụt.
  - Nhiễu "hai lượt cùng cấu hình" (A/A) ở 10 đoạn, 176 câu: điểm Đủ tụt 1 câu, Đúng tụt 2 câu — nhiễu nền cho các luật "không làm hỏng".
  - Đoạn đúng lọt vào 10 đoạn của chatbot: nhóm thử 40 câu có nhãn **24 / 40** (bản 4, kho đợt 1; bản 1: 22); cả 55 câu có nhãn, **bản 5** trên kho đợt 2:
    **33 / 55** câu đủ mọi ý, tỉ lệ ý có trong ngữ cảnh **0,77** — trước ↔ sau đợt 2 **không câu nào mất** đoạn đúng.
- **Thay đổi thước đo 30/10:** nhãn đoạn đúng **bản 5** (173 / 174 trích dẫn tìm lại nguyên văn trong kho đợt 2; 1 trích dẫn đổi chữ, bạn duyệt); **Golden sửa 2 đáp
  án mẫu** theo bạn chọn (md5 `0f7dbf41b422` ⇒ `6331e88fb171`); thước "trước ↔ sau" đợt 2 thêm **bộ 32 câu an toàn** và luật **"chạm theo file"** (khi xóa một
  dòng làm mã đoạn dồn số) (§4). 28/10: nhãn bản 4, sàn "nói chắc sai", tách câu chạm phần sửa.
- **Giới hạn chính:**
  - **chưa có mốc người** — B0 (bạn đọc 20 cặp câu trả lời mù) dời làm sau (trước buổi bảo vệ); mọi kết luận dựa điểm Claude là tạm;
  - chỉ 40 câu thử / 15 câu kiểm có nhãn đoạn đúng ⇒ nhiều kết quả tầng tìm chỉ "chưa rõ";
  - nhóm kiểm 56 câu và 36 câu kín **đều đã dùng** ⇒ phép kiểm sau cần bộ câu mới;
  - đáp án mẫu không nhạy với sửa kho kiểu "thêm tên mới / bỏ chi tiết không chắc" ⇒ hai đợt sửa kho không làm điểm tăng dù kho đúng hơn;
  - thước lỗi nặng và bộ an toàn do agent viết + người chấm Claude, chưa có người đọc; bộ an toàn chỉ 28 câu trong kho ⇒ cận trên tỉ lệ sai điều kiện ~12 %.
- **Chi phí:** 7B + thử nhanh ~0,087 USD; 8.1 ~0,165 USD; 8.2 ≈ 0,227 / 0,5 USD; sửa kho đợt 1 ≈ 0,073 / 0,15 USD, đợt 2 ≈ 0,047 / 0,10 USD. Chấm bằng Claude dùng
  quota Claude Code (không USD).
- **Bạn cần quyết gì:** B0 khi tiện (~30–45 phút, trước buổi bảo vệ) — mốc người đầu tiên; nếu bạn ngược người chấm Claude ở nhiều cặp ⇒ A trình bạn giữ 10 đoạn hay
  quay về 5.

## 2. Hoạt động thế nào (bản đang chạy)

```text
Mốc / biến thể:  176 câu Golden → đường API thật (tìm → đóng gói N đoạn → gpt-6-luna → kiểm trích dẫn)
                 → tầng tìm: keyword @10 (miễn phí) + đoạn đúng theo tầng: pool → top-10 → N đoạn đưa model (nhãn bản 5)
                 → câu trả lời mốc + biến thể trộn MÙ → Claude chấm Đúng / Đủ / Trúng ý (1–5)
                 → so theo cặp từng câu: chênh, CI 95 %, thắng / hòa / thua; nhiều biến thể ⇒ Holm
                 → luật ghi trước: sàn · mức tụt cho phép · 1–2 chỉ số quyết
```

- **Luật ghi trước (ba lớp):** sàn không được vi phạm (0 câu ngoài kho bị trả lời; 0 lỗi kỹ thuật) · mức tụt cho phép (ví dụ điểm Đủ / Đúng trung bình
  ≥ −0,1 **và** số câu tụt ≤ nhiễu A/A + 3) · chỉ số quyết phải tốt lên vượt nhiễu. Nhóm kiểm nhỏ ⇒ xác nhận ở nhóm kiểm = **"không làm hỏng"** (User 27/10).
- **Nhãn đoạn đúng — năm bản, mỗi số ghi kèm bản:**

  | Bản | Khi nào | Khác bản trước | Dùng cho |
  |---|---|---|---|
  | 1 (`gold_draft`) | 8.1 G0.3, 25/10 | 55 câu khó (40 thử / 15 kiểm), một chỗ cho mỗi ý | mọi số đoạn đúng **trước 27/10** |
  | 2 | 27/10 sáng (User duyệt 13:05) | +3 chỗ kho nói lại cùng ý (2 câu thử) **và** luật trúng dòng tiêu đề | số 27/10 sáng |
  | 3 | 27/10 chiều (mặc định từ `fa192f8` tới 28/10) | +2 câu nhóm kiểm: một câu thêm một chỗ nói lại; một câu so sánh gắn đúng trích dẫn nói thẳng ý so sánh | số trên **kho trước sửa** |
  | 4 | 28/10 (mặc định từ `e08a126` tới 30/10; bạn duyệt 2 trích dẫn) | cùng ý như bản 3, vị trí tìm lại trong **kho đợt 1**: 172 / 174 trích dẫn giữ nguyên chữ (42 chỉ dời vị trí); 2 trích dẫn của 1 câu đổi chữ theo chỗ sửa | số trên **kho đợt 1** |
  | 5 | 30/10 (mặc định; bạn duyệt 1 trích dẫn) | cùng ý như bản 4, vị trí tìm lại trong **kho đợt 2**: 173 / 174 trích dẫn giữ nguyên chữ (38 chỉ dời vị trí); 1 trích dẫn đổi chữ theo đúng chỗ sửa | **mặc định hiện nay** |

  Bản 1–4 giữ nguyên để tái lập số cũ (bản 3, 4 ghi vị trí theo kho trước đợt 1 / đợt 2). So số mới với số cũ thì chạy lại mốc bằng cùng bản nhãn.
- **Luật trúng dòng tiêu đề (từ bản 2):** nhãn đánh dấu một đoạn văn trong file kho; một đoạn tìm được "trúng" nhãn khi phần thân đoạn giao vị trí nhãn,
  **hoặc** khi nhãn là một dòng tiêu đề Markdown nằm trong đường tiêu đề của đoạn (model thấy tiêu đề đó trong ngữ cảnh). Trước bản 2, câu có ý nằm ở tiêu đề
  mục bị đếm "thiếu" dù model đã thấy và trả lời đúng.
- **Một ý được tính "có trong ngữ cảnh"** khi **một** trích dẫn bất kỳ của ý đó trúng; câu "đủ đoạn đúng" khi **mọi** ý đều có (test ghim luật này).
- Code:
  - bộ chấm `backend/evaluation/full_corpus_eval.py` (`answer_case` :322, `is_refusal` :162, so theo cặp `paired_stats` :634, `bootstrap_mean_diff` :590, 10.000 vòng :55);
  - prompt chấm `backend/evaluation/full_corpus_judge_prompt.md`;
  - nhãn: `backend/experiments/phase_8_1/g1_retrieval.py` (`GOLD_PATH` :48 = bản 5, `quote_is_chunk_heading` :76, `chunk_hits_quote` :82, `gold_coverage` :93);
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
| Đoạn đúng (vị trí trong file) cho câu khó | **Xử lý một phần** | 55 / 176 câu (40 thử / 15 kiểm); **bản 5** mặc định (30/10, sau đợt 2 sửa kho); câu khác chỉ có keyword |
| Đếm ý nằm ở dòng tiêu đề mục | **Đã xử lý, đóng gói** | từ bản 2; `g1_retrieval.py:76-90` + test |
| Nhãn độ tự nhiên (bỏ câu người thật ít hỏi) | **Đã xử lý** | 82 / 65 / 29; số chính bỏ 29 câu |
| Bộ câu kín cho chấm cuối 8.2 | **Đã xử lý, đóng gói** (chạy 28/10) | 36 câu; chatbot cuối 8.2 tốt hơn, không làm hỏng (§4 28/10); **đã dùng** ⇒ lần kiểm cuối sau cần bộ mới |
| Mốc người (bạn đọc cặp mù) | **Chưa thực hiện** (dời — làm trước buổi bảo vệ) | B0 — 20 cặp đã chuẩn bị (`data/phase_8_2/b0/`); không còn chặn việc nào (bạn chọn 28/10) |
| Điểm trên câu người dùng thật sự nhận (câu lỗi trích dẫn tính là hỏng) | **Đã xử lý** (dùng ở câu kín và hai đợt sửa kho, 28/10, 30/10) | câu 500 = điểm 1 ở cả hai bên; chưa vào bộ chấm chung `full_corpus_eval` |
| Kiểm số trong câu có trích dẫn phải có trong nguồn | **Đã thử, chưa áp dụng** | 27/10 đo lượt 10 đoạn: 68 câu có số, 0 lỗi thấy được (4 câu bị cờ đều là phép tính đúng; mẫu 10 / 10 đúng) ⇒ chưa cần kiểm bằng code |
| Thước đo sau khi sửa kho (trước ↔ sau) | **Đã xử lý, đóng gói** (28/10 nhãn bản 4; 30/10 nhãn bản 5) | sàn ngoài kho / lỗi / 500 mới / **nói chắc sai mới** + mức tụt + câu chạm báo riêng; 30/10 thêm **bộ 32 câu an toàn** + luật "chạm theo file"; cả hai đợt **không làm hỏng** (§4) |
| "Bịa thêm" và "sai điều kiện / cảnh báo" (hai lỗi nặng nhất bạn chốt) | **Đã xử lý** (thước lỗi nặng 28/10, bạn nhận 29/10; dùng ở đợt 2) | người chấm Claude tách ý, so với ngữ cảnh model đọc; Golden 28/10: bịa thêm 1 / 145, sai điều kiện 0 / 65; bộ an toàn 30/10: 0 / 28 sai điều kiện, 0 bịa; nhiễu hai lượt 29/10: 2 câu dao động ⇒ sàn "mới ≤ 2 + sinh lại 3 lần"; chưa có người đọc |
| Bộ câu an toàn (giờ, vé, miễn giảm, giấy tờ, cảnh báo) | **Đã xử lý** (bắt buộc từ 29/10) | 32 câu (28 trong kho, 4 ngoài kho), agent viết; 15 câu đối chứng kiểm người chấm mỗi lượt (đợt 2: cả 2 người chấm bắt 10 / 10 câu chèn sai) |
| Tốc độ / tiền theo yêu cầu bạn chốt | **Xử lý một phần** | đo tuần tự 176 câu (10 đoạn): trung vị 2,2 s, câu chậm 4,9 s (lại 2,19 / 4,90 s ngày 30/10), ~0,0002 USD / câu ⇒ đạt; câu trả lời dài (bộ tự viết) trung vị 4,6 s ⇒ chưa đạt; đo trong script, chưa qua web; tiền ước theo giá phẳng, có thể thiếu ~20 % nếu bị tính giá ghi đệm (chờ bạn xem billing) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 30/10/2026 — thước "trước ↔ sau" đợt 2 sửa kho: kết quả không làm hỏng

Plan `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` (bản 3 + §10, A duyệt `2adef0d4e5fc` sau 3 vòng review C):
- **Hai bên:** bộ "trước" = bộ "sau" đợt 1 (dùng lại sau 4 kiểm "còn hiệu lực"; không tốn tiền); bộ "sau" chạy mới trên kho đợt 2; Golden đã sửa 2 đáp án (bạn chọn),
  chấm cả hai bên bằng đáp án mới trong **một lượt mù** (300 câu trả lời khác nhau, 7 người chấm Claude).
- **Mới trong thước:** **bộ 32 câu an toàn** (trước = lượt 28/10; sau = lượt mới; cộng 6 câu sinh lại mốc cho 2 câu từng dao động và 15 câu đối chứng; 2 người chấm ×
  6 lô, mỗi bản của cùng câu ở một lô khác) và luật **"chạm theo file"**: hai dòng bị xóa làm mã đoạn ở 2 file dồn số ⇒ mọi câu dùng đoạn của 2 file đó tính là
  "chạm" (A đồng ý trước khi có số), câu chỉ chạm theo luật này được C đọc tay.
- **Kết quả Golden:** 0 câu ngoài kho bị trả lời · 0 lỗi · 0 lỗi trích dẫn mới · 0 "nói chắc sai" mới · Đủ +0,008 (4 tăng / 3 tụt trên 129 câu chính), Đúng 0,000 (1 / 1)
  · tập không chạm 4 / 2 · từ chối nhầm 13 → 12 ⇒ **không làm hỏng**. C đọc tay 8 câu: 0 lỗi nội dung kho; 1 câu thiếu ý vì một đoạn nhắc thời tiết bị đẩy khỏi
  10 đoạn đầu khi thứ hạng đổi (theo dõi). Đoạn đúng trong ngữ cảnh 0,7615 ⇒ 0,7615, không câu nào mất.
- **Kết quả bộ an toàn:** cả hai người chấm qua phép kiểm (bắt 10 / 10 câu chèn sai, gồm 5 / 5 đảo cảnh báo; báo nhầm 0 / 5 và 1 / 5) · 0 / 4 câu ngoài kho bị trả lời ·
  **0 câu sai điều kiện mới**, 0 đảo cảnh báo · 2 câu sai ở lượt 28/10 nay không sai; sinh lại 3 lần trên kho cũ cũng 0 / 3 ⇒ "lúc có lúc không" · 0 bịa thêm mới ·
  "thiếu điều kiện" đổi 5 câu (1 mới, 4 mất), hơi trên mức dao động 3 câu ⇒ theo dõi.
- **Tốc độ / tiền:** trung vị 2,19 s, câu chậm 4,90 s; ~0,00021 USD / câu. Tiền đợt 2 ≈ 0,047 USD. Report: `sua_kho_dot2_implementation.md` (+ review C).

### 28/10/2026 — thước "trước ↔ sau" của đợt sửa kho: kết quả không làm hỏng

Plan `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_do_truoc_sau_plan.md` (A duyệt sha `41485782b39e` sau review C):
- **Hai bên:** chatbot đang chạy (10 đoạn) trên kho **trước** và **sau** khi sửa, cùng 176 câu Golden, đo tuần tự; hai bộ câu trả lời trộn chung **một lượt chấm mù**
  (303 câu trả lời khác nhau, 7 người chấm Claude); Golden không đổi (bạn duyệt "0 câu cần sửa").
- **Mới trong thước:** sàn **"nói chắc sai" mới** (người dùng thấy câu trả lời mà điểm Đúng ≤ 3 — nhiễu A/A 0 / 0); **câu chạm phần sửa** tách bằng máy (đoạn ngữ cảnh
  giao chỗ sửa / file bị bỏ: 43 / 176 câu); trung bình kiểm cả trên **tập không chạm** để câu chạm không làm số đẹp giả; mỗi câu tụt có nhãn giải thích.
- **Kết quả:** 0 câu ngoài kho bị trả lời · 0 lỗi · 0 lỗi trích dẫn mới · 0 "nói chắc sai" mới · Đủ −0,008 (4 tụt / 4 tăng trên 129 câu chính), Đúng 0,000 (1 / 1) ·
  tập không chạm: 0,000 / +0,010 · từ chối nhầm 12 → 13 (đúng mức cho phép) ⇒ **không làm hỏng**. Câu tụt: 3 câu "nhiễu" (ngữ cảnh hai bên giống hệt), 2 câu chạm
  phần sửa. Câu chạm (31 câu chính): không tốt hơn (đáp án mẫu không đổi). C kiểm lại ra giống hệt.
- **Tốc độ / tiền:** ~0,0002 USD / câu; câu chậm lượt "sau" 9,8 s (trước 4,9 s) — chậm ở phía mạng / nhà cung cấp trong vài phút cuối lượt (không tách được hai bên),
  phần trên máy không đổi ⇒ số câu chậm của lượt này **không đại diện**.
- Tiền 2 lượt ≈ 0,073 USD. Report: `sua_kho_do_truoc_sau_plan.md`, `sua_kho_b9_implementation.md` (+ review).

### 28/10/2026 — mốc cuối 8.2 trên câu kín (đã chạy)

- **Chạy:** chatbot đầu 8.2 (5 đoạn, bộ kiểm trích dẫn cũ) ↔ chatbot cuối 8.2 (10 đoạn + chuẩn hóa dấu + bộ kiểm mới) trên 36 câu kín; người chạy B chỉ in số đếm,
  người chấm Claude mới; chỉ khớp được 1 / 3 câu A từng thấy ⇒ báo trên **cả 36 câu** (không đoán thêm).
- **Kết quả (33 câu trong kho):** **Đủ +0,82** [+0,39; +1,33] (12 thắng / 0 thua), **Đúng +0,70** [+0,27; +1,21] (8 / 0) ⇒ **không làm hỏng + tốt hơn**; câu ngoài kho
  từ chối đúng 3 / 3; từ chối nhầm 4 → 2; câu lỗi trích dẫn 4 → 0 (cả 4 do bộ kiểm cũ). Bỏ riêng 4 câu đó vẫn Đủ +0,45 [+0,14; +0,83] ⇒ lợi không chỉ do bộ kiểm mới.
- **Giới hạn:** không câu kín nào gõ dạng dấu tách rời ⇒ phần chuẩn hóa dấu chưa được thử ở đây; người chấm Claude. Tiền ≈ 0,014 USD. Report:
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_implementation.md` (+ review C74).

### 27/10/2026 chiều — thước đo cho đợt sửa kho (spec đã duyệt, chưa chạy)

Spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (bạn duyệt sha `937cf8969810`, 15:39 27/10), sau 3 vòng review:
- **Bộ "trước"**: chạy 176 câu trên chatbot cuối 8.2 với kho + chỉ mục hiện tại **trước khi đụng kho** (bước 0) — vì chỉ mục được thay tại chỗ, sau đó không
  còn bản cũ để sinh lại. Plan đo ghi tiêu chí trước và được review trước bước này.
- **Bộ "sau"**: 176 câu trên chỉ mục mới (bước 9). Hai bộ chấm **cùng một lượt mù**, **cùng bản Golden đã sửa** (bạn duyệt từng câu sửa, bước 8); câu chạm ý
  đã sửa trong kho báo riêng.
- **Tiêu chí "không làm hỏng"** (§6): sàn 0 câu ngoài kho bị trả lời, 0 lỗi kỹ thuật / 500 mới; điểm Đủ / Đúng trung bình ≥ −0,1; số câu tụt ≤ A/A + 3 với
  **A/A = 2** (nhiễu hai lượt 10 đoạn trên 176 câu: Đủ 1, Đúng 2 — lấy số lớn); mỗi câu tụt có giải thích.
- **Nhãn đoạn đúng bản 4** dựng **sau khi build** (bước 7): sửa kho làm lệch vị trí — đếm trên các chỗ sửa đợt 1: 24 câu có nhãn trong file bị sửa, 66 trích
  dẫn lệch vị trí, 3 trích dẫn bị chính chỗ sửa chồng lên (cần đề xuất mới, bạn duyệt). *(28/10, C76: ba số này đặt tên chưa đúng — 24 = câu có trích dẫn dời / bị chồng, 66 = trích dẫn trong file sửa, 3 = cặp (chỗ sửa, trích
  dẫn); đếm lại khi dựng bản 4: 2 trích dẫn của 1 câu bị chồng.)* Số đoạn đúng chỉ tính lại sau bước này; bản 3 giữ để tái lập số cũ.
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

Kiểm ngày 28/10/2026 với `main` và các report 8.2 / đợt sửa kho; 3 dòng mốc / T1 / nhãn sửa 30/10/2026 (đợt 2).

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Bộ chấm `full_corpus_eval.py` (`generate`, `compare`, `summarize`) | **còn dùng**; so theo cặp `paired_stats` | `backend/evaluation/full_corpus_eval.py:634` |
| Prompt chấm cố định | **còn dùng** (không chấm trích dẫn) | `backend/evaluation/full_corpus_judge_prompt.md` |
| Người chấm Claude, mù, cùng lượt | **còn dùng** | spec 8.2 §7; plan B3 §4 |
| Mốc chatbot (5 đoạn, `e5-small-384`, `dense_bm25_rrf`, không rerank) | **đã thay** 28/10: **10 đoạn** + chuẩn hóa dấu câu hỏi (merge `510e1a8`), kho đã sửa (204 file / 8.426 đoạn); 30/10 kho đợt 2 (204 / **8.424**); mốc so sánh mới = bộ "sau" đợt 2 | `backend/config/settings.yaml:56`; `sua_kho_b9_implementation.md`, `sua_kho_dot2_implementation.md` |
| Mốc tìm T1 `cefb2d1ad609` | **đã thay** 28/10 bằng `23c58c47635d` (40 / 158 câu đổi top-10), rồi 30/10 bằng **`4d5bbe9e0edc`** (đợt 2; 25 / 158 câu đổi) | spec sửa kho §5 bước 6; `sua_kho_b1_6_implementation.md`, `sua_kho_dot2_implementation.md` |
| Nhãn đoạn đúng | **bản 5 mặc định** (30/10); bản 1–4 chỉ để tái lập số cũ | `backend/experiments/phase_8_1/g1_retrieval.py:48` |
| Golden md5 `0f7dbf41b422` | **đã thay** 30/10 bởi `6331e88fb171` (2 đáp án sửa theo bạn chọn sau đợt 2) | `BAO_CAO_BO_CAU_HOI_GOLDEN.md` bản 6 |
| Số "lỗi trích dẫn" của lượt 10 đoạn 25/10 | **đã thay**: theo bộ kiểm hiện tại 0 / 12 câu đó lỗi | `c65_citation_138_check.md` |
| Điểm 7B Run 1 làm mốc | **lịch sử**; 10 câu Golden sửa đáp án 25/10 không so trực tiếp | `phase_8_1_golden_fix_review.md` |
| Chẩn đoán từ chối nhầm theo keyword | **đã thay** (8.1): 22 / 22 thiếu dữ kiện trong ngữ cảnh | report G1 8.1 §4 |
| "Chấm tay khoảng 20 câu" (bản 2 §6) | **đã thay** bởi B0: bạn đọc và nhận xét 20 cặp mù, không chấm điểm (bạn chọn 25/10) | spec 8.2 §3 mục 3–4 |

## 6. Việc còn lại / cần quyết

- **Bạn:** B0 (đọc 20 cặp mù, ghi nhận xét) khi tiện, trước buổi bảo vệ — mốc người đầu tiên; luật dừng (spec 8.2 §11) kích hoạt ⇒ A trình giữ 10 đoạn / về 5 và xét lại
  các kết luận dựa người chấm Claude.
- **Hai lỗi nặng nhất bạn chốt:** đã có thước (lỗi nặng) + bộ 32 câu an toàn bắt buộc; còn thiếu **người đọc** (20 câu mẫu `data/loi_nang_2026-10-28/human_sample.md`
  khi bạn rảnh) và câu an toàn **người dùng thật** viết. Một lỗi ứng viên đang đo: chatbot không biết hôm nay là ngày nào (câu hỏi "tối nay", "tuần này").
- **Bộ câu mới:** nhóm kiểm và câu kín đã dùng ⇒ phép kiểm cuối của thay đổi lớn sau (ví dụ Qwen3-8B, streaming) cần câu mới chưa ai nhìn.
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
  Golden md5 **`6331e88fb171`** (30/10; trước `0f7dbf41b422`); nhãn bản 4 `gold_v4.jsonl` `927bae1bf201`, bản 5 `gold_v5.jsonl` `33d16fd6b8f4`; B0 `data/phase_8_2/b0/`.
- **Bản 5 (B, 30/10):** đợt 2 `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` (+ review C85), `sua_kho_dot2_implementation.md` (+ `sua_kho_dot2_b2_6_review.md`);
  thước lỗi nặng `do_loi_nang_implementation.md` (B89), nhiễu `do_loi_nang_aa_implementation.md` (C84) + review; bộ an toàn private `data/loi_nang_2026-10-28/an_toan/`.
- **Bản 4 (B86, 28/10):** câu kín `phase_8_2_b3_implementation.md` + `phase_8_2_b3_review.md`; đợt sửa kho `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_do_truoc_sau_plan.md`,
  `sua_kho_b7_8_implementation.md` (nhãn bản 4), `sua_kho_b9_implementation.md` (+ review C72, C76, C80); nhãn bản 4 `data/phase_8_1/gold/gold_v4.jsonl` `927bae1bf201`.
- Bản 1: A, 24/10/2026. Bản 2: C30, 25/10/2026. Bản 3: C69, 27/10/2026. Bản 4: B86, 28/10/2026. Bản 5: B (B97), 30/10/2026.
