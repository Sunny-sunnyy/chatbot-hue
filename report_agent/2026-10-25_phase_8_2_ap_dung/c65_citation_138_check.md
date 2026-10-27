# C65 — câu 138 (B1 test) bị ghi lỗi citation dù có trích nguồn: validator nào, validator hiện tại có lỗi không

Người làm: C (Claude Opus 5.5, `hue-rag-86`) · 14:33 27/10/2026 (`date`) · Việc: A giao C65 (14:3x 27/10). **0 USD**, chỉ đọc, không gọi API. Không chép câu hỏi / câu trả lời /
nội dung kho — chỉ `case_index`, loại câu, số đếm. Bằng chứng private: `data/phase_8_2/b1/c65/` (`check.py`, `result.json`).

## Cho bạn (3 dòng)

- Lượt đo B1 (25/10 chiều) chạy **trước** khi sửa bộ kiểm trích nguồn: bộ kiểm lúc đó chỉ nhận `[n]`, nên câu trả lời viết `[Nguồn n]` bị đếm là "không có trích nguồn".
- Đưa đúng các câu trả lời đã lưu qua bộ kiểm **hiện tại** trên `main`: cả **12 / 176** câu bị ghi lỗi (6 dev, 6 test, có câu 138) đều **qua**; không câu nào đổi chiều
  ngược lại. Tức chatbot hôm nay (và nhánh B1) **không** trả 500 cho các câu đó.
- Hệ quả: số "lỗi citation B1 12 câu" trong report B1 là theo bộ kiểm cũ; ở mốc cuối B3, nhánh đầu (`f26485b`, bộ kiểm cũ) sẽ có phần lỗi kiểu này mà nhánh cuối không có.

## 1. (a) Lượt B1 chạy với bộ kiểm nào

- `data/phase_8_2/b1/b1_{pilot,rest,test_pilot,test_rest}.meta.json`: chạy **16:35:24 – 16:38:12 25/10/2026**; meta không ghi commit.
- `9e6d371` (bộ kiểm v2, nhận cả `[Nguồn n]` và đổi về `[n]` trước khi kiểm): **19:58:17 25/10/2026** — sau lượt B1 ~3 giờ.
- Commit gần nhất trên `main` trước lượt chạy: `f26485b` (15:49), `5e6936b` (16:22); `f4353e2` (16:41, sau lượt chạy, chỉ tài liệu): `llm/citations.py` đều có
  `CITATION_PATTERN = re.compile(r"\[(\d+)\]")` (chỉ `[n]`). Nhánh B1 khi đó chỉ sửa tìm kiếm / context (`e1e16b3` = các file B1, không chạm `citations.py`).
- Kiểm tái lập: chạy lại hàm kiểm **bản cũ** (`git show f4353e2:backend/llm/citations.py`) trên câu trả lời đã lưu ⇒ khớp `citation_error` đã lưu **120 / 120 dev, 56 / 56
  test**. ⇒ **Đã chứng minh:** lượt B1 dùng bộ kiểm v1.

## 2. (b) Bộ kiểm hiện tại trên `main` với đúng chuỗi trả lời đã lưu

Cách: `normalize_citations` rồi `select_cited_sources` (đúng thứ tự `backend/api/routes/chat.py:176-178`), nguồn đóng gói = id 1..`context_sources` của dòng đó (hàm chỉ đọc
`.id`). Logic thuần, không gọi model / Qdrant.

| Tập | n | cũ ok → mới ok | cũ lỗi → mới ok | cũ ok → mới lỗi | cũ lỗi → mới lỗi |
|---|---:|---:|---:|---:|---:|
| B1 dev | 120 | 114 | **6** | 0 | 0 |
| B1 test | 56 | 50 | **6** (gồm 138) | 0 | 0 |

- Cả 12 câu: lỗi cũ là "Grounded answer has no citation", câu trả lời đều viết dạng `[Nguồn n]`, số trong ngoặc đều nằm trong số nguồn đóng gói.
- Loại câu của 12 câu: dev — so sánh 1, sự kiện trực tiếp 3, có điều kiện 1, nhiều nguồn 1; test — so sánh 2, nhiều nguồn 2, có điều kiện 1, sự kiện trực tiếp 1.
- **Production hôm nay:** `main` có `9e6d371` từ 25/10 tối, nhánh `p82-b1` `c3d5607` cũng có (gốc `576f84e`) ⇒ 12 câu này **không** ra 500.

## 3. Ảnh hưởng (suy ra — chưa kiểm phần ngoài B1)

- Report B1 (`phase_8_2_b1_implementation.md` trên `p82-b1`, dòng 79) ghi "Lỗi citation (validator production): B1 12 câu, G2.1a 8 câu" — "production" là của lúc chạy (v1).
  Với bộ kiểm hiện tại B1 = **0 / 176**. G2.1a (8.1) C **chưa** đếm lại.
- **B3 (mốc cuối, plan `27e75be5ed44`):** nhánh đầu `f26485b` dùng bộ kiểm v1 ⇒ nếu model vẫn viết `[Nguồn n]` với tỉ lệ cỡ 12 / 176 (≈ 7 %), trên ~30 câu trong phạm vi
  nhánh đầu có thể có ~2 câu 500 kiểu này. Theo luật M-1 của plan (câu 500 = Completeness / Accuracy 1 ở cả hai nhánh) phần đó **cộng cho nhánh cuối**, và đến từ bộ kiểm
  v2 (đã có trong chatbot từ 25/10), không từ context 10 + NFC. Plan §1 đã ghi "cuối − đầu đo gộp ba thay đổi"; C khuyên report B3 tách riêng số câu 500 kiểu này mỗi nhánh.
- Các thí nghiệm 8.2 dùng câu trả lời B1 làm mốc (K3b-m khâu trả lời, R1…) — nếu so `citation_error` đã lưu của mốc với lượt mới (chạy sau 25/10 tối, bộ kiểm v2) thì mốc bị
  tính thừa tới 12 lỗi. C **chưa kiểm** các report đó đếm lại bằng v2 hay dùng số lưu.
