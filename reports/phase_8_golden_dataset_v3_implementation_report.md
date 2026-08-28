# Implementation Report: Phase 8 Golden Dataset V3 (Gate 0 - Correction Round 2)

Implementer: Implementer
Date: 2026-08-28 +07
Canonical guide: `guides/phase_8_benchmark_model_selection.md`
Canonical design: `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md`
Implementation plan: `docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md`
Reviewer report: `reports/phase_8_golden_dataset_v3_codex_review.md`

## 1. Phạm vi & Xử lý toàn diện các Reviewer Findings

Trong Correction Round 2, Implementer đã thực hiện các điều chỉnh phẫu thuật (surgical corrections) nhằm giải quyết dứt điểm toàn bộ các blocker từ Reviewer:

1. **Major 1 — Khôi phục Intent Food tour nửa ngày:**
   - Đã khôi phục câu hỏi food tour nửa ngày buổi sáng tại `foods-v3-0044` với keywords được User chốt: `["bún bò", "cà phê", "buổi sáng"]`.
   - Để duy trì kích thước tối ưu **45 câu**, loại bỏ câu hỏi địa chỉ đơn lẻ yếu nhất (Bánh canh O Hoa `0003` cũ), giúp tập dataset nâng số câu `guide_planning` lên 2 cases (nửa ngày và 1 ngày) và giảm thêm 1 câu template địa chỉ lặp.

2. **Major 2 — Khắc phục triệt để mismatch Question / Answer / Evidence:**
   - `foods-v3-0011` (Cơm Âm Phủ): Loại bỏ cụm từ quảng bá thừa "tạo nên hương vị đặc sắc", giữ đúng mô tả món cơm sử dụng gạo An Cựu và 7 món ăn kèm.
   - `foods-v3-0012` (Bánh canh cá lóc Hải Triều): Tách biệt phần nước dùng; answer chỉ tập trung vào nước dùng ninh từ xương cá lóc và xương heo tạo vị ngọt tự nhiên và sắc đỏ nhẹ từ dầu điều.
   - `foods-v3-0017` (Quán chay Thanh Liễu): Bỏ "số 50 Nguyễn Công Trứ", trả lời chuẩn xác khu vực Phố Tây Huế và các món thuần chay theo đúng 2 section `Tóm tắt` và `Món ăn / trải nghiệm`.
   - `foods-v3-0018` (DeChill): Sửa answer bám sát đúng section Markdown là không gian nhiều cây xanh và tầm nhìn thoáng đãng ra khúc uốn sông Hương tại Đồi Vọng Cảnh (bỏ claim ngắm đồi thông).
   - `foods-v3-0019` (The TIME Coffee): Giữ đúng chi tiết địa điểm nguyên văn trong corpus là "gần ngã tư gầm cầu Phú Xuân".
   - `foods-v3-0039` & `foods-v3-0040` (Spanning Cơm hến & Bún bò): Loại bỏ presupposition "nổi tiếng", dùng cách hỏi và trả lời trung tính ("một số quán cơm hến", "một số quán bún bò").

3. **Major 3 — Thu hẹp và chính xác hóa Evidence H2 Mappings:**
   - Đã thu hẹp triệt để các section thừa/không bảo vệ answer trực tiếp:
     - `0001` (Chè Mợ Tôn Đích): chỉ giữ `Thông tin` (chứa địa chỉ và vị trí).
     - `0003` (Bánh ép 1992): chỉ giữ `Thông tin` (chứa 2 cơ sở).
     - `0008` (Cơm Âm Phủ đĩa cơm): giữ `Thông tin` (quán số 51) và `Món ăn / trải nghiệm` (món ăn kèm).
     - `0009` (Cơm niêu Chạn): chỉ giữ `Món ăn / trải nghiệm`.
     - `0010` (Tịnh Tâm Đinh Vũ view): chỉ giữ `Tóm tắt` và `Thông tin`.
     - `0011` (Cơm Âm Phủ tên gọi & gạo): chỉ giữ `Thông tin` và `Món ăn / trải nghiệm`.
     - `0012` (Bánh canh cá lóc Hải Triều): chỉ giữ `Món ăn / trải nghiệm`.
     - `0013` (Bánh mì Đông Ba nhân): chỉ giữ `Món ăn / trải nghiệm`.
     - `0014` (Donald Trung buffet rau): chỉ giữ `Món ăn / trải nghiệm`.
     - `0017` (Thanh Liễu món chay): giữ `Tóm tắt` và `Món ăn / trải nghiệm`.
     - `0021` (Cà phê muối gốc): chỉ giữ `Tóm tắt` (đã đủ năm 2010 và 2 địa chỉ).
     - `0029` (Bánh nậm vs Bánh ép làm chín): giữ `banh nam.md :: Thành phần và đặc điểm` và `banh ep.md :: Tóm tắt`.
     - `0031` (Cơm hến vs Bún bò Huế): giữ `com hen.md :: Thành phần và đặc điểm` và `bun bo hue.md :: Thành phần và đặc điểm`.
     - `0033` (Mè xửng khối lượng & giá): chỉ giữ `Mua làm quà`.
     - `0035` (Bánh canh Nam Phổ màu đỏ gạch & bột sánh): chỉ giữ `Thành phần và đặc điểm`.
     - `0036` (Bánh nậm nhân): chỉ giữ `Thành phần và đặc điểm`.
     - `0038` (Chè bột lọc heo quay chế biến): chỉ giữ `Thành phần và đặc điểm` và `Cách làm tóm tắt`.

4. **Minor 1 — Nhật ký Web Research thực tế:**
   - Tra cứu trực tiếp:
     - URL 1: `https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/an-sang-hue.html` (Món ăn sáng phổ biến)
     - URL 2: `https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/an-trua-o-hue.html` (Món ăn trưa và cơm Huế)
     - URL 3: `https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/an-dem-hue.html` (Ăn đêm, bánh mì, chè Huế)
     - URL 4: `https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/chi-phi-di-hue.html` (Cân đối chi phí ẩm thực)
     - Web Search Query: `"cẩm nang ăn uống ở Huế kinh nghiệm du lịch Huế ăn gì"` (tổng hợp cấu trúc nhu cầu du khách từ Khám Phá Huế, Vietnam Tourism và iVIVU).

## 2. Toàn bộ 45 câu hỏi Final Golden Dataset V3

1. `foods-v3-0001`: Quán Chè Mợ Tôn Đích nằm ở địa chỉ nào tại Huế? *(direct_fact)*
2. `foods-v3-0002`: Bánh mì Trường Tiền O Tho có cơ sở chính ở đâu tại Huế? *(direct_fact)*
3. `foods-v3-0003`: Bánh ép 1992 có các cơ sở nằm ở những địa chỉ nào tại Huế? *(direct_fact)*
4. `foods-v3-0004`: Bánh canh cá lóc Hải Triều và Bánh canh cá lóc Thủy Dương có điểm chung gì về các loại topping gọi thêm? *(comparative)*
5. `foods-v3-0005`: Không gian và phong cách của An Nhien Garden Vegetarian khác gì so với Quán chay Thanh Liễu? *(comparative)*
6. `foods-v3-0006`: Quán Huyền Anh tại khu vực Kim Long phục vụ những món ăn nào? *(relationship)*
7. `foods-v3-0007`: Món chè đặc sản độc đáo nào làm nên tên tuổi của quán Chè Mợ Tôn Đích? *(relationship)*
8. `foods-v3-0008`: Đĩa Cơm Âm Phủ tại quán 51 Nguyễn Thái Học gồm những món ăn kèm nào? *(relationship)*
9. `foods-v3-0009`: Nhà hàng cơm niêu Chạn phục vụ các món ăn truyền thống nào của bữa cơm Huế? *(relationship)*
10. `foods-v3-0010`: Ẩm thực chay Tịnh Tâm Đinh Vũ có vị trí và hướng nhìn như thế nào? *(relationship)*
11. `foods-v3-0011`: Quán Cơm Âm Phủ tại 51 Nguyễn Thái Học có nguồn gốc tên gọi như thế nào và phục vụ món cơm đặc trưng ra sao? *(holistic)*
12. `foods-v3-0012`: Nước dùng của bánh canh cá lóc Hải Triều được ninh nấu từ những nguyên liệu gì để tạo hương vị đặc trưng? *(food_knowledge)*
13. `foods-v3-0013`: Ổ bánh mì tại tiệm Bánh mì Đông Ba thường gồm những loại nhân nào? *(food_knowledge)*
14. `foods-v3-0014`: Quán Bánh cuốn thịt heo Donald Trung có điểm nhấn đặc biệt gì về phần rau ăn kèm? *(relationship)*
15. `foods-v3-0015`: Quán Bánh ép Gia Di có nguồn gốc từ đâu và không gian quán như thế nào? *(relationship)*
16. `foods-v3-0016`: Nhà hàng chay Sala phục vụ theo mô hình gì và không gian quán có đặc trưng nào? *(relationship)*
17. `foods-v3-0017`: Quán chay Thanh Liễu nằm ở khu vực nào và phục vụ những món chay tiêu biểu nào? *(relationship)*
18. `foods-v3-0018`: Quán cà phê DeChill nằm ở đâu và có tầm nhìn ngắm cảnh như thế nào? *(relationship)*
19. `foods-v3-0019`: The TIME Coffee & Bakery tọa lạc ở đâu và có vị trí ngắm cảnh như thế nào? *(direct_fact)*
20. `foods-v3-0020`: Phong cách thiết kế không gian của Hanok Cafe Huế và Củi Coffee khác nhau như thế nào? *(comparative)*
21. `foods-v3-0021`: Quán Cà Phê Muối gốc ra đời năm nào và có những cơ sở nào ở Huế? *(relationship)*
22. `foods-v3-0022`: Giao Cafe nằm ở đâu và có phong cách không gian như thế nào? *(relationship)*
23. `foods-v3-0023`: Trốn Studio tại Huế nằm ở đâu và hoạt động theo mô hình như thế nào vào ban ngày và ban đêm? *(relationship)*
24. `foods-v3-0024`: Hương vị và cách pha chế món cà phê muối tại quán Cà Phê Muối gốc có đặc trưng gì? *(food_knowledge)*
25. `foods-v3-0025`: Bánh canh Nam Phổ có nguồn gốc từ làng nào ở Huế? *(direct_fact)*
26. `foods-v3-0026`: Món bánh ép Huế có nguồn gốc xuất xứ từ vùng nào? *(direct_fact)*
27. `foods-v3-0027`: Bánh nậm Huế được gói bằng những loại lá gì theo cách làm truyền thống? *(direct_fact)*
28. `foods-v3-0028`: Người Huế thường thưởng thức bánh canh Nam Phổ vào thời điểm nào trong ngày? *(temporal)*
29. `foods-v3-0029`: Bánh nậm và Bánh ép khác nhau như thế nào về phương pháp làm chín bánh? *(comparative)*
30. `foods-v3-0030`: Bánh ép dẻo ăn tại chỗ và bánh ép khô mua làm quà khác nhau như thế nào? *(comparative)*
31. `foods-v3-0031`: Cơm hến và bún bò Huế khác nhau thế nào về thành phần chính và cách dùng phần nước? *(comparative)*
32. `foods-v3-0032`: Tỷ lệ pha bột gạo và bột lọc truyền thống để làm sợi bánh canh Nam Phổ là bao nhiêu? *(numerical)*
33. `foods-v3-0033`: Mè xửng mua làm quà thường được đóng gói theo các khối lượng nào và mức giá tham khảo dao động trong khoảng bao nhiêu? *(numerical)*
34. `foods-v3-0034`: Món chè heo quay xứ Huế có sự kết hợp hương vị độc đáo như thế nào? *(relationship)*
35. `foods-v3-0035`: Trong món bánh canh Nam Phổ, thành phần nào tạo nên màu đỏ gạch tự nhiên và nước dùng được nấu như thế nào để đạt độ sánh? *(food_knowledge)*
36. `foods-v3-0036`: Nhân bánh nậm truyền thống của Huế gồm những nguyên liệu gì và được xào như thế nào? *(food_knowledge)*
37. `foods-v3-0037`: Tri thức dân gian về bún bò Huế được ghi danh là di sản gì? *(food_knowledge)*
38. `foods-v3-0038`: Chè bột lọc heo quay được làm từ những nguyên liệu chính nào và quy trình chế biến ra sao? *(food_knowledge)*
39. `foods-v3-0039`: Ở Huế có những quán cơm hến nào và địa chỉ của từng quán ở đâu? *(spanning)*
40. `foods-v3-0040`: Ở Huế có những quán bún bò nào và địa chỉ tương ứng của từng quán ở đâu? *(spanning)*
41. `foods-v3-0041`: Ở Huế có những thương hiệu mè xửng truyền thống nào có cửa hàng để mua làm quà? *(spanning)*
42. `foods-v3-0042`: Lần đầu đến Huế nên thử những món ăn tiêu biểu nào? *(holistic)*
43. `foods-v3-0043`: Ở Huế có những quán và nhà hàng chay nào? *(holistic)*
44. `foods-v3-0044`: Nếu chỉ có nửa ngày buổi sáng ở Huế, tôi nên ăn bún bò và uống cà phê ở đâu? *(guide_planning)*
45. `foods-v3-0045`: Gợi ý lịch trình ăn uống một ngày ở Huế từ sáng đến tối? *(guide_planning)*

- **Phân bố Categories (45 cases):**
  - `relationship`: 14
  - `direct_fact`: 7
  - `food_knowledge`: 7
  - `comparative`: 6
  - `holistic`: 3
  - `spanning`: 3
  - `guide_planning`: 2
  - `numerical`: 2
  - `temporal`: 1
- **Phân bố Sources (45 cases):**
  - `restaurants`: 20
  - `local_specialties`: 14
  - `cafes`: 7
  - `guide`: 4

## 3. Bằng chứng thực thi Tests & Verification

| Lệnh thực thi | Exact Output / Outcome |
|---|---|
| `pytest tests/test_evaluation.py -k 'golden_v3 and not binary_relevance'` | **`5 passed, 13 deselected in 3.75s`** |
| `pytest tests/test_evaluation.py -k 'golden_v2_contract or golden_v2_smoke'` | **`2 passed, 16 deselected in 3.87s`** |
| `pytest tests/test_evaluation.py::test_golden_v3_binary_relevance_uses_real_retrieval_metadata` | **`1 passed, 2 warnings in 44.50s`**, cleanup **`ok`** |
| `curl -s http://localhost:6333/collections/hue_foods_e5_small_384` | **`points_count: 572`** (Active collection được bảo vệ 100% read-only) |
| `git diff --check` | **`PASS`** |

## 4. Bảng kiểm tra chi tiết Retrieval cho 10 Smoke Cases (Per-Smoke Audit)

10 smoke cases trích xuất deep-equal từ full V3 và chạy trên retrieval pipeline:

| Row | Case ID | Question | Docs Trả về | Relevant Hits | Rank Hit Đầu | Top Returned Evidence `Source :: Section` |
|:---:|:---:|---|:---:|:---:|:---:|---|
| 01 | `foods-v3-0001` | Quán Chè Mợ Tôn Đích nằm ở địa chỉ nào tại Huế? | 10 | 2 | **Rank 1** | `foods/restaurants/che mo ton dich.md :: Thông tin` |
| 02 | `foods-v3-0003` | Bánh ép 1992 có các cơ sở nằm ở những địa chỉ nào tại Huế? | 10 | 1 | **Rank 1** | `foods/restaurants/banh ep 1992.md :: Thông tin` |
| 03 | `foods-v3-0006` | Quán Huyền Anh tại khu vực Kim Long phục vụ những món ăn nào? | 10 | 1 | **Rank 1** | `foods/restaurants/banh uot bun thit nuong huyen anh.md :: Tóm tắt` |
| 04 | `foods-v3-0009` | Nhà hàng cơm niêu Chạn phục vụ các món ăn truyền thống nào của bữa cơm Huế? | 10 | 3 | **Rank 2** | `foods/restaurants/nha hang com nieu chan.md :: Món ăn / trải nghiệm` |
| 05 | `foods-v3-0014` | Quán Bánh cuốn thịt heo Donald Trung có điểm nhấn đặc biệt gì về phần rau ăn kèm? | 10 | 2 | **Rank 2** | `foods/restaurants/banh cuon thit heo donald trung.md :: Món ăn / trải nghiệm` |
| 06 | `foods-v3-0018` | Quán cà phê DeChill nằm ở đâu và có tầm nhìn ngắm cảnh như thế nào? | 10 | 2 | **Rank 1** | `foods/cafes/dechill.md :: Tóm tắt` |
| 07 | `foods-v3-0021` | Quán Cà Phê Muối gốc ra đời năm nào và có những cơ sở nào ở Huế? | 10 | 1 | **Rank 1** | `foods/cafes/quan ca phe muoi.md :: Tóm tắt` |
| 08 | `foods-v3-0025` | Bánh canh Nam Phổ có nguồn gốc từ làng nào ở Huế? | 10 | 3 | **Rank 1** | `foods/local_specialties/banh canh nam pho.md :: Nguồn gốc và bối cảnh` |
| 09 | `foods-v3-0029` | Bánh nậm và Bánh ép khác nhau như thế nào về phương pháp làm chín bánh? | 10 | 2 | **Rank 2** | `foods/local_specialties/banh nam.md :: Thành phần và đặc điểm` |
| 10 | `foods-v3-0039` | Ở Huế có những quán cơm hến nào và địa chỉ của từng quán ở đâu? | 10 | 3 | **Rank 1** | `foods/restaurants/com hen ba cam.md :: Tóm tắt` |

- **Kết quả:** **10/10 câu smoke** đều đạt relevant hit trong Top 2 (7 câu đạt Rank 1, 3 câu đạt Rank 2), với đúng các section H2 hẹp đã được declared bảo vệ.

## 5. Bàn giao cho Reviewer

- **Dataset Full V3:** [`knowledge-base-hue/foods/evaluation/golden_v3.jsonl`](file:///home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation/golden_v3.jsonl)
- **Dataset Smoke V3:** [`knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl`](file:///home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl)
- **Review kết quả:** [`reports/phase_8_golden_dataset_v3_codex_review.md`](../reports/phase_8_golden_dataset_v3_codex_review.md)
- Prompt Reviewer V3 đã được retire sau khi User phê duyệt Gate 0; xem lịch sử
  Git nếu cần audit handoff vận hành cũ.
