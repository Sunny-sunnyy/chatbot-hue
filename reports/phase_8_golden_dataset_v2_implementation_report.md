# Implementation Report: Phase 8 Golden Dataset V2 (Consolidated Correction Round 3)

> **Historical implementation evidence:** V2 đã được thay thế làm Gate 0 hiện
> hành bởi approved Golden Dataset V3 design/plan ngày 2026-08-27.

Implementer: AI Assistant (Implementer Role)
Date: `2026-08-27 +07`
Canonical guide: `guides/phase_8_benchmark_model_selection.md`
Canonical design: `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`
Implementation plan: `docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md`
Language Quality Audit: `reports/phase_8_golden_dataset_v2_language_quality_audit.md`
Codex Review: `reports/phase_8_golden_dataset_v2_codex_review.md`

---

## 1. Tuyên bố Không Fake Dữ liệu (No-Fake Statement)

Toàn bộ 100 cases trong `knowledge-base-hue/foods/evaluation/golden_v2.jsonl` và 20 cases trong `knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl` được xây dựng và xác thực 100% dựa trên closed-world corpus thực tế (`knowledge-base-hue/foods/`).
- Tuyệt đối **không** sử dụng synthetic/mock/stub data hay benchmark-centric phrasing dưới bất kỳ hình thức nào.
- Toàn bộ câu hỏi được chuẩn hóa theo ngữ văn tiếng Việt tự nhiên, phản ánh đúng câu hỏi của du khách thật về ẩm thực Huế.
- Toàn bộ keywords (2–4 từ khóa ngữ nghĩa trên mỗi case) và reference answers đều là substring xuất hiện thực tế và được grounding chính xác trong các H2 sections tương ứng của Markdown corpus.

---

## 2. Chi tiết Triển khai Consolidated Correction Round 3

Thực hiện chỉnh sửa đồng bộ toàn bộ 100 cases dựa trên Language Quality Audit và Codex Review Round 3:

### A. Sửa 21 Mandatory Finding Cases
1. **`foods-0008`**: Đổi câu hỏi tự nhiên "Quán Cơm Hến 17 Hàn Mặc Tử thuộc phường nào của thành phố Huế?" (không để lộ đáp án "phường Vỹ Dạ" trong câu hỏi).
2. **`foods-0023`**: Làm rõ câu hỏi hỏi giá của một tô bánh canh Nam Phổ tại Quán Thúy ("Giá một tô bánh canh Nam Phổ tại Quán Thúy theo thực đơn tham khảo là bao nhiêu?").
3. **`foods-0028`**: Sửa chính xác tên quán là `Nhà hàng cơm niêu Chạn` (không viết nhầm thành "Chân").
4. **`foods-0039`**: Viết câu hỏi tự nhiên "Thịt ba chỉ làm nhân bánh ép tại quán Gia Di được tẩm ướp như thế nào?".
5. **`foods-0040`**: Viết câu hỏi tự nhiên "Ổ bánh mì tại tiệm Bánh mì Đông Ba thường gồm những loại nhân nào?".
6. **`foods-0044`**: Câu hỏi tự nhiên "Chi nhánh KOI Thé nằm ở đâu trong AEON MALL Huế?", keywords gồm tên thương hiệu và vị trí gian hàng (`KOI Thé`, `Lô số T133, tầng 1`, `AEON MALL Huế`).
7. **`foods-0053`**: Bỏ ghép đôi cơ học, đặt câu hỏi quan hệ tự nhiên "Quán Cà Phê Muối gốc ra đời năm nào và có những cơ sở nào ở Huế?".
8. **`foods-0054`**: Đặt câu hỏi tự nhiên "Giao Cafe nằm ở đâu và có phong cách không gian như thế nào?".
9. **`foods-0059`**: Bỏ viết tắt "CNN", câu hỏi tự nhiên "Quán Cà Phê Muối gốc ở Huế ra đời từ khi nào và có không gian trải nghiệm ra sao?", bổ sung evidence `foods/cafes/quan ca phe muoi.md :: Món ăn / trải nghiệm`.
10. **`foods-0062`**: Đặt câu hỏi xuất xứ tự nhiên "Món bánh ép Huế có nguồn gốc xuất xứ từ vùng nào?", bổ sung evidence `foods/restaurants/banh ep gia di.md :: Món ăn / trải nghiệm`.
11. **`foods-0063`**: Không tuyệt đối hóa bột gạo tẻ cho mọi loại bánh nậm; chuyển sang hỏi loại lá gói truyền thống ("Bánh nậm Huế được gói bằng những loại lá gì theo cách làm truyền thống?").
12. **`foods-0072`**: Đổi câu hỏi bao quát tự nhiên "Kể tên các món ăn đặc sản truyền thống xứ Huế làm từ các loại bột như bột gạo, bột lọc và bột năng?".
13. **`foods-0073`**: Đổi câu hỏi tự nhiên "Những món ăn đặc sản nào của Huế sử dụng mắm ruốc làm gia vị tạo hương vị đặc trưng?".
14. **`foods-0075`**: Đổi câu hỏi tự nhiên "Đĩa Cơm âm phủ truyền thống được trình bày như thế nào và gồm những thành phần gì?".
15. **`foods-0080`**: Tinh gọn thành single intent "Chè bột lọc heo quay được làm từ những nguyên liệu chính nào và quy trình chế biến ra sao?".
16. **`foods-0083`**: Đổi câu hỏi tự nhiên "Những quán cà phê nào tại Huế được gợi ý cho khách muốn tìm không gian mở cửa khuya đến 24:00?".
17. **`foods-0084`**: Tách bạch single-intent "Lần đầu đến Huế nên thử những món ăn tiêu biểu nào?".
18. **`foods-0087`**: Đổi câu hỏi tự nhiên "Đi Huế cùng nhóm bạn thì nên ghé đâu để thưởng thức món địa phương, ăn vặt và món ngọt?", thay 4 địa chỉ bằng các tên quán/món thực tế.
19. **`foods-0090`**: Thay thế bằng case `food_knowledge` chuẩn từ `food-guides.md [Lần đầu đến Huế nên thử gì?]`: hỏi đặc điểm chung của nhóm bánh Huế ("Nhóm bánh bèo, bánh nậm, bánh bột lọc ở Huế có điểm chung gì trong cách chế biến và thưởng thức?").
20. **`foods-0098`**: Tinh gọn thành câu hỏi lịch trình nửa ngày buổi sáng tự nhiên, loại bỏ các mốc giờ tự bịa (`7:00 – 8:00`, `8:30 – 10:00`), thay 4 địa chỉ bằng tên quán cụ thể.
21. **`foods-0100`**: Đổi câu hỏi tự nhiên "Gợi ý lịch trình food tour 2 ngày tại Huế để trải nghiệm các món ăn đặc trưng?", keywords dùng tên các chặng/quán đại diện thay cho chuỗi 4 địa chỉ.

### B. Polish 18 Cases
Đã chuẩn hóa ngôn từ tự nhiên, loại bỏ các tiền tố/hậu tố văn phong máy móc ("theo cẩm nang", "theo tài liệu", "tổng quan các") trên toàn bộ 18 cases: `foods-0027`, `foods-0036`, `foods-0037`, `foods-0042`, `foods-0055`, `foods-0056`, `foods-0065`, `foods-0067`, `foods-0079`, `foods-0081`, `foods-0082`, `foods-0085`, `foods-0086`, `foods-0088`, `foods-0089`, `foods-0092`, `foods-0095`, `foods-0097`.

### C. Rà soát 100/100 Semantic Keywords
- Chuẩn hóa toàn bộ 100 cases chỉ chứa **2–4 keywords** thực sự quan trọng.
- Ưu tiên tên thực thể, tên món ăn, đặc trưng cốt lõi (ví dụ: `foods-0006` có `Bánh ép Gia Di`, `foods-0041` có `DeChill`, `foods-0091`–`foods-0100` dùng tên quán/chặng lịch trình).
- Loại bỏ hoàn toàn việc dùng 4 chuỗi địa chỉ làm proxy keywords cho các câu hỏi holistic/planning.
- Giữ nguyên các brand names chính thức (`AEON MALL`, `KOI Thé`, `ANH KAFE`) và đơn vị đo lường chuẩn (`VNĐ`, `g`, `ml`), đồng thời xóa bỏ các từ viết tắt mô tả không cần thiết như `CNN`, `TTTM`, `TP`.

### D. Kiểm tra Hoàn thiện Alternative Evidence
- `foods-0052`: Bổ sung `foods/food-guides.md :: Theo ngân sách`.
- `foods-0062`: Bổ sung `foods/restaurants/banh ep gia di.md :: Món ăn / trải nghiệm`.
- `foods-0090`: Tái lập evidence chuẩn xác từ `foods/food-guides.md :: Lần đầu đến Huế nên thử gì?`.
- Kiểm tra toàn diện toàn bộ 100 cases: 100% keywords đều là substring xuất hiện thực tế trong reference answer và các section declared evidence.

---

## 3. Nghiên cứu Thực tế / Internet Research

Trong quá trình chuẩn hóa câu hỏi tự nhiên và kiểm tra tính xác thực của thực thể, Implementer đã tiến hành tra cứu thực tế trên các nguồn tư liệu du lịch & ẩm thực Huế uy tín:

1. **Nhà hàng cơm niêu Chạn**:
   - *Truy vấn & Nguồn*: Tra cứu thông tin quán Chạn Huế trên Cổng thông tin Khám phá Huế (`khamphahue.com.vn`), `Mia.vn` và bài viết trải nghiệm ẩm thực Huế (tháng 8/2026).
   - *Kết quả*: Xác nhận tên thương hiệu chuẩn là "Nhà hàng cơm niêu Chạn" (chữ "Chạn" mang ý nghĩa chiếc chạn bếp xưa) tại 01 và 19 Nguyễn Thái Học, phục vụ các món ăn cơm nhà Huế truyền thống. Corpus và câu hỏi hoàn toàn khớp thực tế.
2. **KOI Thé tại AEON MALL Huế**:
   - *Truy vấn & Nguồn*: Tra cứu sơ đồ gian hàng AEON MALL Huế trên website chính thức (`hue.aeonmall-vietnam.com`) và hệ thống ShopeeFood / Foody (tháng 8/2026).
   - *Kết quả*: Gian hàng KOI Thé nằm tại Lô số T133, Tầng 1 TTTM AEON MALL Huế, số 8 Võ Nguyên Giáp. Khớp 100% với dữ liệu corpus và câu hỏi chuẩn hóa.
3. **DeChill Coffee & Glamping**:
   - *Truy vấn & Nguồn*: Tra cứu thông tin quán DeChill trên `thanhphohue.net` và các kênh du lịch Đồi Vọng Cảnh Huế (tháng 8/2026).
   - *Kết quả*: Quán tọa lạc tại số 102 Đường Huyền Trân Công Chúa, Phường Thủy Xuân, khu vực Đồi Vọng Cảnh.
4. **Quán Cà Phê Muối gốc**:
   - *Truy vấn & Nguồn*: Tra cứu lịch sử quán cà phê muối Huế trên Báo Tuổi Trẻ (`tuoitre.vn`) và Cổng thông tin Thừa Thiên Huế (tháng 8/2026).
   - *Kết quả*: Quán được sáng lập năm 2010 tại số 10 Nguyễn Lương Bằng và mở rộng cơ sở 2 tại 142 Đặng Thái Thân. Không gian giữ nét cổ điển, sân vườn thoáng đãng.
5. **Bún bò Huế - Di sản Văn hóa**:
   - *Truy vấn & Nguồn*: Tra cứu quyết định công nhận của Bộ Văn hóa, Thể thao và Du lịch (tháng 8/2026).
   - *Kết quả*: Tri thức dân gian về Bún bò Huế đã được ghi danh là Di sản văn hóa phi vật thể quốc gia.

*Đánh giá chung*: Mọi thông tin thực tế ngoài đời thực đều đồng nhất và củng cố vững chắc tính chính xác của closed-world corpus; không có xung đột dữ liệu hay sự kiện nào phải sửa đổi trong corpus gốc.

---

## 4. Thống kê Phân bổ Dataset & Coverage

### Phân loại theo Nguồn Gốc Sửa đổi (Case Transformation Totals)
- **Tổng số cases**: 100 cases.
- **Rewritten / Replaced cases (Round 3)**: 21 cases (`foods-0008`, `foods-0023`, `foods-0028`, `foods-0039`, `foods-0040`, `foods-0044`, `foods-0053`, `foods-0054`, `foods-0059`, `foods-0062`, `foods-0063`, `foods-0072`, `foods-0073`, `foods-0075`, `foods-0080`, `foods-0083`, `foods-0084`, `foods-0087`, `foods-0090`, `foods-0098`, `foods-0100`).
- **Polished cases (Round 3)**: 18 cases (`foods-0027`, `foods-0036`, `foods-0037`, `foods-0042`, `foods-0055`, `foods-0056`, `foods-0065`, `foods-0067`, `foods-0079`, `foods-0081`, `foods-0082`, `foods-0085`, `foods-0086`, `foods-0088`, `foods-0089`, `foods-0092`, `foods-0095`, `foods-0097`).
- **Keywords overhaul (Round 3)**: 100/100 cases đã được tinh chỉnh toàn diện theo chuẩn 2–4 semantic keywords.
- **Source conflicts / Reallocations**: `none` (ma trận primary authoring được bảo toàn nguyên vẹn 100%).

### Phân bổ Category Matrix (Full 100 cases)
- `direct_fact`: 18
- `temporal`: 10
- `comparative`: 10
- `numerical`: 8
- `relationship`: 12
- `spanning`: 12
- `holistic`: 8
- `food_knowledge`: 12
- `guide_planning`: 10
**Tổng cộng**: 100 cases (đáp ứng 100% `CATEGORY_QUOTAS`).

### Phân bổ 4 Source Families (Primary + Alternative Evidence)
- `restaurants`: 42 cases (chỉ tiêu >= 40)
- `guide`: 42 cases (chỉ tiêu >= 20)
- `local_specialties`: 30 cases (chỉ tiêu >= 20)
- `cafes`: 20 cases (chỉ tiêu >= 20)

### Phân bổ Smoke Subset (20 cases)
- `restaurants`: 8 cases (`foods-0001`, `foods-0004`, `foods-0011`, `foods-0017`, `foods-0021`, `foods-0025`, `foods-0036`, `foods-0038`)
- `cafes`: 4 cases (`foods-0041`, `foods-0048`, `foods-0053`, `foods-0057`)
- `local_specialties`: 4 cases (`foods-0065`, `foods-0069`, `foods-0072`, `foods-0078`)
- `guide`: 4 cases (`foods-0084`, `foods-0088`, `foods-0091`, `foods-0099`)
*Độ phủ danh mục*: Đầy đủ 9/9 categories (direct_fact: 3, temporal: 2, comparative: 2, numerical: 2, relationship: 2, spanning: 2, holistic: 2, food_knowledge: 3, guide_planning: 2 = 20 cases).

---

## 5. Kết quả Kiểm thử & Benchmark Thực tế

### 1. CLI Validation Entrypoint
```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-correction-r3-uv-cache uv run python -m evaluation.golden_dataset
```
Kết quả:
```json
{
  "full": {
    "cases": 100,
    "categories": {
      "direct_fact": 18,
      "temporal": 10,
      "comparative": 10,
      "numerical": 8,
      "relationship": 12,
      "spanning": 12,
      "holistic": 8,
      "food_knowledge": 12,
      "guide_planning": 10
    },
    "source_coverage": {
      "restaurants": 42,
      "local_specialties": 30,
      "guide": 42,
      "cafes": 20
    }
  },
  "smoke": {
    "cases": 20,
    "categories": 9,
    "source_families": 4
  }
}
```

### 2. Focused V2 Structural Tests
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-golden-v2-correction-r3-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q --tb=short -k 'golden_v2 and not binary_relevance'
```
Kết quả: `2 passed, 10 deselected, 1 warning in 7.03s`.

### 3. Task 7 Real Integration Test trên Isolated Collection (20 smoke cases)
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-golden-v2-correction-r3-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py::test_golden_v2_binary_relevance_uses_real_retrieval_metadata -q --tb=short -s
```
Kết quả:
```text
.LIVE CLEANUP hue_rag_live_test_e5_small_384: ok
1 passed, 2 warnings in 41.66s
```

### 4. Live Smoke Retrieval Benchmark trên Qdrant Active Collection (`hue_foods_e5_small_384`)
Đo lường bằng script Python chạy trực tiếp với `dense_only` profile (E5-small-384, top_k=5) qua `RetrievalService`:
```bash
uv run --env-file ../.env python -c '
import json, math
from pathlib import Path
from evaluation.golden_dataset import load_golden, document_is_relevant, SMOKE_PATH
from evaluation.eval import build_services

smoke = load_golden(SMOKE_PATH)
services = build_services("dense_only")

hits_at_5 = 0
rank_1_count = 0
rr_sum = 0.0
ndcg_sum = 0.0
misses = []

for case in smoke:
    docs = services.retrieval.search(case.question)[:5]
    rel = [document_is_relevant(case, doc) for doc in docs]
    hit = any(rel)
    if hit:
        hits_at_5 += 1
        rank = rel.index(True) + 1
        if rank == 1:
            rank_1_count += 1
        rr_sum += 1.0 / rank
    else:
        misses.append((case.case_id, case.question))

    dcg = sum(1.0 / math.log2(r + 1) for r, is_rel in enumerate(rel, 1) if is_rel)
    total_rel = sum(rel)
    idcg = sum(1.0 / math.log2(r + 1) for r in range(1, min(5, total_rel) + 1)) if total_rel > 0 else 1.0
    ndcg = dcg / idcg if idcg > 0 else 0.0
    ndcg_sum += ndcg

print(f"Hit@5: {hits_at_5}/{len(smoke)} ({hits_at_5/len(smoke)*100:.2f}%)")
print(f"Rank-1 Count: {rank_1_count}/{len(smoke)} ({rank_1_count/len(smoke)*100:.2f}%)")
print(f"MRR@5: {rr_sum/len(smoke):.4f}")
print(f"Binary NDCG@5: {ndcg_sum/len(smoke):.4f}")
print(f"Misses: {misses}")
'
```
Kết quả thực tế đo được:
- **Hit@5**: **100.00%** (20/20)
- **Rank-1 Count**: **16/20** (80.00% câu hỏi trả về relevant chunk ngay tại Rank 1)
- **MRR@5**: **0.8833**
- **Binary NDCG@5**: **0.8863**
- **Misses**: `none` (`[]`)

---

## 6. An toàn Dữ liệu & Cleanliness Verification

- **Active Collection Safety**: `hue_foods_e5_small_384` duy trì chính xác 572 points trước và sau kiểm tra (0 mutations, read-only hoàn toàn).
- **Phase 7 Baselines Integrity**: `knowledge-base-hue/foods/evaluation/tests.jsonl` và `test2.jsonl` không có bất kỳ thay đổi nào (`git diff` trả về 0 diff).
- **Code Cleanliness**: `git diff --check` sạch 100%, không có trailing whitespace.
- **Trạng thái lịch sử**: Bản V2 này từng sẵn sàng cho Re-review Round 4, nhưng
  workflow đó đã bị hủy sau complexity reset ngày `2026-08-27 +07`. V3 hiện là
  Gate 0 canonical; không dùng report này để khởi động lại V2 correction/review.
