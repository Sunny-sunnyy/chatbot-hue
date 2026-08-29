# Hướng dẫn & Giải thích Kỹ thuật: Mô hình Embedding và Các Độ đo Đánh giá (Hue Foods RAG)

> **Tài liệu tham chiếu nội bộ** cho nhóm phát triển và nghiên cứu dự án **Hue Foods RAG**.
> **Cập nhật:** `2026-08-29` (Phase 8 — Benchmark & Model Selection).

---

## Mục lục

1. [Tổng quan về Embedding trong Hệ thống RAG](#1-tổng-quan-về-embedding-trong-hệ-thống-rag)
2. [Các Mô hình Embedding Đang Dùng](#2-các-mô-hình-embedding-đang-dùng)
   - [2.1. `intfloat/multilingual-e5-small` (384D) — Control Baseline](#21-intfloatmultilingual-e5-small-384d--control-baseline)
   - [2.2. `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (768D)](#22-code4lifeofficialhuydang-dek21-embedding-768d--candidate-1)
   - [2.3. `intfloat/multilingual-e5-base` (768D)](#23-intfloatmultilingual-e5-base-768d--candidate-2)
   - [2.4. Phân tích các mô hình đã loại bỏ](#24-phân-tích-các-mô-hình-đã-loại-bỏ-minilm-l12-qwen3-embedding-bge-m3-e5-large)
3. [Nguyên lý Tiền xử lý & Hợp đồng Input (Input Contracts)](#3-nguyên-lý-tiền-xử-lý--hợp-đồng-input-input-contracts)
   - [3.1. Tiền tố Asymmetric Query/Passage (E5 Family)](#31-tiền-tố-asymmetric-querypassage-e5-family)
   - [3.2. Tách từ tiếng Việt chuyên biệt (PyVi ViTokenizer)](#32-tách-từ-tiếng-việt-chuyên-biệt-pyvi-vitokenizer)
   - [3.3. Giới hạn độ dài chuỗi (Max Sequence Length) & Hiện tượng Cắt ngắn (Truncation)](#33-giới-hạn-độ-dài-chuỗi-max-sequence-length--hiện-tượng-cắt-ngắn-truncation)
   - [3.4. Chuẩn hóa Vector $L_2$ & Khoảng cách Cosine](#34-chuẩn-hóa-vector-l_2--khoảng-cách-cosine)
4. [Các Độ đo Đánh giá Chất lượng Truy xuất (Retrieval Metrics)](#4-các-độ-do-đánh-giá-chất-lượng-truy-xuất-retrieval-metrics)
   - [4.1. Đơn vị Tính điểm Relevance: Cặp `(source, section)`](#41-đơn-vị-tính-điểm-relevance-cặp-source-section)
   - [4.2. Recall@K (Recall@5)](#42-recallk-recall5)
   - [4.3. MRR@K (Mean Reciprocal Rank @ 5)](#43-mrrk-mean-reciprocal-rank--5)
   - [4.4. nDCG@K (Normalized Discounted Cumulative Gain @ 5)](#44-ndcgk-normalized-discounted-cumulative-gain--5)
   - [4.5. Hit Rate / Hit Case Count](#45-hit-rate--hit-case-count)
5. [Phương pháp Kiểm định Thống kê & Guardrails](#5-phương-pháp-kiểm-định-thống-kê--guardrails)
   - [5.1. Category Guardrails (9 Danh mục câu hỏi V3)](#51-category-guardrails-9-danh-mục-câu-hỏi-v3)
   - [5.2. Paired Bootstrap 95% Confidence Interval (CI)](#52-paired-bootstrap-95-confidence-interval-ci)
   - [5.3. Tiêu chí Quyết định "Clear Quality Gain"](#53-tiêu-chí-quyết-định-clear-quality-gain)
6. [Đo lường Hiệu năng: Độ trễ (Latency) & Bộ nhớ (Memory RSS)](#6-đo-lường-hiệu-năng-độ-trễ-latency--bộ-nhớ-memory-rss)
7. [Bảng Tổng hợp So sánh & Khuyến nghị Lựa chọn](#7-bảng-tổng-hợp-so-sánh--khuyến-nghị-lựa-chọn)

---

## 1. Tổng quan về Embedding trong Hệ thống RAG

Trong kiến trúc **Retrieval-Augmented Generation (RAG)**, mô hình **Dense Embedding** đóng vai trò là "cây cầu ngữ nghĩa" (semantic bridge) chuyển đổi ngôn ngữ tự nhiên (văn bản) thành các vector số thực trong không gian đa chiều (dense vector space $\mathbb{R}^d$).

```
[Văn bản ẩm thực / Câu hỏi du lịch]
           │
           ▼
  ┌─────────────────┐
  │ Embedding Model │  (Mô hình biến đổi ngữ nghĩa thành vector)
  └─────────────────┘
           │
           ▼  Vector d-chiều: [0.042, -0.128, 0.891, ..., 0.015]
  ┌─────────────────┐
  │ Qdrant Database │  (Tìm kiếm láng giềng gần nhất bằng Cosine Similarity)
  └─────────────────┘
```

- **Mục tiêu cốt lõi:** Các đoạn văn bản có ý nghĩa tương đồng (dù dùng từ ngữ khác nhau, ví dụ: *"quán ăn ngon cố đô"* và *"địa chỉ ẩm thực nổi tiếng ở Huế"*) sẽ có các vector nằm gần nhau trong không gian vector (khoảng cách góc cos nhỏ, độ tương đồng $\approx 1.0$).
- **Thách thức với tiếng Việt ẩm thực Huế:**
  1. Các danh từ riêng, tên món ăn ghép: *Bún bò Huế, bánh bèo, bánh nậm, bánh lọc, chè bột lọc bọc heo quay*.
  2. Địa danh địa phương: *đường Nguyễn Du, cồn Hến, Vĩ Dạ, chợ Đông Ba*.
  3. Cấu trúc ngữ pháp và từ đồng nghĩa, từ địa phương.

---

## 2. Các Mô hình Embedding Đang Dùng

Hệ thống hiện đã chuẩn hóa và đánh giá thực nghiệm **3 cấu hình dense embedding canonical** trên CPU FP32 với 572 chunks dữ liệu thật:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        3 CẤU HÌNH ĐƯỢC ỦY QUYỀN                        │
├───────────────────────────────┬────────────────────────────────────────┤
│ 1. E5-small 384D (Control)    │ 2. Huydang DEk21 768D (Candidate 1)    │
│    intfloat/multilingual-e5-small │    huydang-dek21-embedding           │
├───────────────────────────────┴────────────────────────────────────────┤
│ 3. E5-base 768D (Candidate 2)                                          │
│    intfloat/multilingual-e5-base                                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 2.1. `intfloat/multilingual-e5-small` (384D) — Control Baseline

- **Đơn vị phát triển:** Microsoft Research.
- **Kiến trúc:** XLM-RoBERTa backbone, 12 layers, hidden dimension $d = 384$, ~118M tham số.
- **Pooling & Tiền tố:** Attention-mask mean pooling; yêu cầu tiền tố bất đối xứng `passage: ` cho tài liệu và `query: ` cho câu hỏi.
- **Max Sequence Length:** 512 tokens.
- **Cách thức hoạt động:** Được huấn luyện đối chiếu (contrastive learning) trên tập dữ liệu đa ngôn ngữ quy mô lớn CCPairs (hơn 1 tỉ cặp text đa ngữ), tối ưu hóa việc phân biệt giữa câu hỏi ngắn và đoạn văn bản dài.
- **Hiệu năng trên dữ liệu Huế:**
  - **nDCG@5:** `0.7425` | **MRR@5:** `0.7748` | **Recall@5:** `0.8185` | **Hits:** `41/45` (91.1%).
  - **Độ trễ Query (p50):** `24.23 ms` (Tổng latency truy xuất: `30.77 ms`).
  - **Mức chiếm dụng RAM:** ~1.54 GB RSS.
  - **Cắt ngắn văn bản:** 0 / 572 chunks bị truncate.
- **Đánh giá:** **Xuất sắc toàn diện**. Giữ vị trí số 1 về nDCG@5 và MRR@5, tốc độ nhanh nhất, tiêu tốn ít RAM nhất. Là mốc đối chứng (Control) vững chắc.

---

### 2.2. `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (768D) — Candidate 1

- **Tác giả:** Đặng Quang Huy (HCMUTE).
- **Kiến trúc:** **PhoBERT-base** (RoBERTa chuyên biệt cho tiếng Việt), 12 layers, hidden dimension $d = 768$, ~135M tham số.
- **Pooling & Tiền tiền xử lý:** Mean pooling; bắt buộc tách từ tiếng Việt bằng `pyvi.ViTokenizer.tokenize()`; không dùng tiền tố.
- **Max Sequence Length:** **256 tokens**.
- **Dữ liệu huấn luyện:** Fine-tune trên ~100.000 cặp câu hỏi/văn bản Pháp luật Việt Nam (Legal domain) bằng hàm mất mát Matryoshka Loss kết hợp Multiple Negatives Ranking (MNRL).
- **Hiệu năng trên dữ liệu Huế:**
  - **nDCG@5:** `0.7164` ($\Delta = -0.0262$) | **Recall@5:** `0.8370` | **Hits:** `40/45` (88.9%).
  - **Điểm sáng:** Đạt kết quả rất cao ở nhóm **`food_knowledge`** (nDCG = `0.8571`, vượt trội so với E5-small `0.7546`), **`holistic`** (`0.7606`) và **`guide_planning`** (`0.5655`).
  - **Hạn chế:** Bị lệch miền pháp lý sang du lịch ẩm thực và max_length=256 khiến mô hình trượt 3 guardrails (`comparative`, `relationship`, `spanning` chỉ bắt 1/3 hits).
  - **Độ trễ Query (p50):** `53.84 ms` (chậm hơn khoảng 2.2 lần E5-small).
- **Đánh giá:** **Ứng viên tiềm năng về biểu diễn ngữ nghĩa tiếng Việt**. Dù chưa vượt qua E5-small toàn diện, mô hình chứng minh backbone PhoBERT và bộ tách từ tiếng Việt mang lại biểu diễn từ ngữ ẩm thực cố đô rất sắc nét.

---

### 2.3. `intfloat/multilingual-e5-base` (768D) — Candidate 2

- **Đơn vị phát triển:** Microsoft Research.
- **Kiến trúc:** XLM-RoBERTa-base, 12 layers, hidden dimension $d = 768$, ~278M tham số (gấp hơn 2 lần bản small).
- **Pooling & Tiền tố:** Attention-mask mean pooling; tiền tố `passage: ` và `query: `.
- **Max Sequence Length:** 512 tokens.
- **Hiệu năng trên dữ liệu Huế:**
  - **nDCG@5:** `0.7061` ($\Delta = -0.0364$) | **Recall@5:** **`0.8407`** (cao nhất) | **Hits:** **`42/45`** (93.3%).
  - **Độ trễ Query (p50):** `112.33 ms` (chậm hơn khoảng 4.6 lần E5-small).
  - **RAM Peak:** ~2.15 GB RSS.
- **Đánh giá:** **Độ bao phủ rộng (Recall cao) nhưng thứ hạng chưa tối ưu**. E5-base tìm thấy được nhiều tài liệu liên quan hơn (42/45 hits), nhưng khả năng đưa đúng tài liệu quan trọng nhất lên vị trí Top 1-2 lại kém hơn E5-small, dẫn đến MRR@5 và nDCG@5 thấp hơn, trong khi độ trễ và dung lượng vector tăng gấp đôi.

---

### 2.4. Phân tích các mô hình đã loại bỏ (`MiniLM-L12`, `Qwen3-Embedding`, `BGE-M3`, `E5-Large`)

| Mô hình | Lý do loại bỏ khỏi phạm vi Local Execution |
| :--- | :--- |
| **`paraphrase-multilingual-MiniLM-L12-v2` (384D)** | • **Tử huyệt max length 128:** Bị cắt ngắn 83/572 chunks (14.5%), gây mất mát nghiêm trọng phần đuôi văn bản.<br>• **Chất lượng tụt sâu:** nDCG@5 chỉ đạt `0.4709` ($\Delta = -0.2716$), trượt 7/9 guardrails, mất sạch bằng chứng nhóm `guide_planning` (0/2 hits).<br>• **Không có ưu thế tài nguyên:** Không nhẹ hơn và không nhanh hơn E5-small. Đã xóa collection `hue_foods_08a_minilm_l12_384`. |
| **`Qwen/Qwen3-Embedding-0.6B` (384D / 1024D)** | • **Độ trễ CPU quá lớn:** 572 chunks mất 765 giây (~12.7 phút), query p50 mất **781.8 ms** (chậm gấp 36 lần E5-small).<br>• **Chất lượng suy giảm:** nDCG@5 chỉ đạt `0.6175` ($\Delta = -0.1251$), trượt 3/9 guardrails. |
| **`BAAI/bge-m3` (1024D dense)** | • Mô hình lớn (~570M params), tài nguyên CPU không đảm bảo SLA phản hồi thực tế.<br>• Được chuyển hướng sang đề xuất đánh giá qua Remote API (OpenRouter) trong tương lai. |
| **`intfloat/multilingual-e5-large` (1024D)** | • Kích thước lớn (~560M params, vector 1024D) gây quá tải CPU và bộ nhớ.<br>• Được lưu giữ để xem xét đánh giá qua OpenRouter API. |

---

## 3. Nguyên lý Tiền xử lý & Hợp đồng Input (Input Contracts)

Mỗi họ mô hình embedding hiện hành có một **Hợp đồng Input (Input Contract)**
bắt buộc riêng. Sơ đồ vẫn hiển thị MiniLM như historical evidence để giải thích
kết quả đã lưu; MiniLM không còn là executable setting.

```
                 ┌────────────────────────────────────────────────────────┐
                 │                INPUT TEXT BAN ĐẦU                      │
                 └──────────────────────────┬─────────────────────────────┘
                                            │
           ┌────────────────────────────────┼────────────────────────────────┐
           ▼                                ▼                                ▼
  [ Họ mô hình E5 ]                [ Mô hình Huydang ]       [ MiniLM — historical ]
┌───────────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐
│ passage: {văn bản}    │        │ ViTokenizer.tokenize()│        │ Nhận nguyên bản       │
│ query: {câu hỏi}      │        │ "Bún_bò Huế..."       │        │ (Raw text)            │
└──────────┬────────────┘        └──────────┬────────────┘        └──────────┬────────────┘
           ▼                                ▼                                ▼
┌───────────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐
│ Max Length: 512       │        │ Max Length: 256       │        │ Max Length: 128       │
└──────────┬────────────┘        └──────────┬────────────┘        └──────────┬────────────┘
           ▼                                ▼                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│              MEAN POOLING -> L2 NORMALIZATION (||v|| = 1.0) -> QDRANT                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Tiền tố Asymmetric Query/Passage (E5 Family)

Họ mô hình E5 được huấn luyện theo kiến trúc bất đối xứng (asymmetric embedding):
- **Tài liệu lưu trữ (Passage):** Bắt buộc thêm tiền tố `"passage: "` vào đầu chunk text:
  ```python
  prepared_text = f"passage: {chunk_text}"
  ```
- **Câu hỏi tìm kiếm (Query):** Bắt buộc thêm tiền tố `"query: "` vào đầu câu hỏi:
  ```python
  prepared_query = f"query: {user_question}"
  ```
*Ý nghĩa:* Tiền tố giúp mô hình phân biệt rõ đâu là nội dung chứa câu trả lời dài và đâu là câu hỏi ngắn, tạo ra sự liên kết ngữ nghĩa vượt trội giữa câu hỏi và câu trả lời.

---

### 3.2. Tách từ tiếng Việt chuyên biệt (PyVi ViTokenizer)

Kiến trúc **PhoBERT** (backbone của `huydang-dek21-embedding`) được tiền huấn luyện trên các âm tiết tiếng Việt đã được ghép từ (word-level tokens). Do đó, trước khi đưa qua Tokenizer của HuggingFace, văn bản bắt buộc phải qua bộ phân đoạn từ vựng `pyvi`:

```python
from pyvi import ViTokenizer

raw_text = "Bún bò Huế rất ngon và nổi tiếng ở cố đô Huế."
segmented_text = ViTokenizer.tokenize(raw_text)
# Kết quả: "Bún_bò Huế rất ngon và nổi_tiếng ở cố_đô Huế ."
```
*Ý nghĩa:* Giúp mô hình hiểu `"Bún_bò"` là một thực thể món ăn duy nhất thay vì hai từ đơn lẻ `"Bún"` và `"bò"`, tương tự với `"nổi_tiếng"`, `"cố_đô"`.

---

### 3.3. Giới hạn độ dài chuỗi (Max Sequence Length) & Hiện tượng Cắt ngắn (Truncation)

Mỗi mô hình có giới hạn tối đa số lượng token mà bộ Transformer có thể xử lý trong một lượt forward:
- **E5-small / E5-base:** $512$ tokens $\rightarrow$ Bao phủ trọn vẹn toàn bộ 572 chunks của kho tri thức ẩm thực Huế (0 chunk bị cắt).
- **Huydang DEk21:** $256$ tokens $\rightarrow$ Ghi nhận **1 chunk** bị cắt ngắn nhẹ.
- **MiniLM-L12:** $128$ tokens $\rightarrow$ Ghi nhận **83 chunks (14.5%)** bị cắt ngắn, gây mất mát dữ liệu nghiêm trọng.

---

### 3.4. Chuẩn hóa Vector $L_2$ & Khoảng cách Cosine

Sau khi qua lớp Pooling (Mean Pooling: tính trung bình cộng các vector token có trọng số theo attention mask), mọi vector đầu ra $\mathbf{v}$ đều được **chuẩn hóa $L_2$** về độ dài đơn vị:

$$\mathbf{u} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2} = \frac{\mathbf{v}}{\sqrt{\sum_{i=1}^d v_i^2}}$$

Khi $\|\mathbf{u}\|_2 = 1.0$, độ tương đồng Cosine giữa vector truy vấn $\mathbf{q}$ và vector tài liệu $\mathbf{d}$ trở thành tích vô hướng (Dot Product) trực tiếp:

$$\text{CosineSimilarity}(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\|_2 \|\mathbf{d}\|_2} = \mathbf{q} \cdot \mathbf{d} = \sum_{i=1}^d q_i \cdot d_i$$

*Ý nghĩa:* Giúp Qdrant tính toán độ tương đồng cực kỳ nhanh chóng bằng các phép toán SIMD/AVX trên CPU.

---

## 4. Các Độ đo Đánh giá Chất lượng Truy xuất (Retrieval Metrics)

### 4.1. Đơn vị Tính điểm Relevance: Cặp `(source, section)`

Trong Golden Dataset V3, Ground Truth liên quan không gán cứng theo `chunk_id` vật lý (vì các mô hình chunking có thể khác nhau), mà được định nghĩa chính xác theo **Cặp nguồn tài liệu và tiêu đề mục H2**:

$$\text{Evidence Unit} = (\text{source\_file}, \text{section\_h2})$$

*Ví dụ:* Cặp `("foods/restaurants/bun-bo-hue.md", "Giới thiệu và hương vị")`.

> **Quy tắc Bão hòa Bằng chứng (De-duplication Credit):**
> Mỗi cặp `(source, section)` chỉ nhận điểm thưởng $\text{gain} = 1$ **duy nhất ở lần xuất hiện đầu tiên** trong Top 5. Các chunk tiếp theo từ cùng một section trong Top 5 sẽ nhận $\text{gain} = 0$. Quy tắc này ngăn chặn việc hệ thống "ăn gian điểm" bằng cách trả về nhiều đoạn văn trùng lặp của cùng một mục.

---

### 4.2. Recall@K (Recall@5)

**Định nghĩa:** Tỷ lệ giữa số lượng bằng chứng liên quan tìm thấy trong Top $K$ so với tổng số lượng bằng chứng liên quan được khai báo trong câu hỏi.

$$\text{Recall@K} = \frac{|\text{Declared Evidence} \cap \text{Retrieved Evidence Top K}|}{|\text{Declared Evidence}|}$$

- **Phạm vi giá trị:** $[0.0, 1.0]$.
- **Ý nghĩa thực tế:** Đo lường **độ bao phủ** thông tin. $\text{Recall@5} = 1.0$ nghĩa là toàn bộ thông tin cần thiết để trả lời câu hỏi đã nằm trọn vẹn trong Top 5 kết quả tìm kiếm.

---

### 4.3. MRR@K (Mean Reciprocal Rank @ 5)

**Định nghĩa:** Nghịch đảo vị trí xếp hạng của tài liệu liên quan hợp lệ **đầu tiên** xuất hiện trong danh sách kết quả Top $K$.

$$\text{RR@K} = \begin{cases} \frac{1}{\text{rank}_{\text{first}}}, & \text{nếu tìm thấy tài liệu liên quan ở vị trí } \text{rank}_{\text{first}} \le K \\ 0, & \text{nếu không có tài liệu liên quan trong Top } K \end{cases}$$

$$\text{MRR@K} = \frac{1}{N} \sum_{i=1}^N \text{RR@K}_i$$

- **Phạm vi giá trị:** $[0.0, 1.0]$.
- **Ý nghĩa thực tế:** Đo lường **tốc độ người dùng tiếp cận câu trả lời**.
  - Nếu tài liệu đúng nằm ở Top 1 $\rightarrow \text{RR} = 1.0$.
  - Nếu tài liệu đúng nằm ở Top 2 $\rightarrow \text{RR} = 0.5$.
  - Nếu tài liệu đúng nằm ở Top 3 $\rightarrow \text{RR} = 0.333$.
  - Nếu nằm ngoài Top 5 $\rightarrow \text{RR} = 0.0$.

---

### 4.4. nDCG@K (Normalized Discounted Cumulative Gain @ 5)

**Định nghĩa:** Độ đo toàn diện đánh giá cả **chất lượng** lẫn **thứ tự vị trí** của tất cả các tài liệu liên quan trong danh sách kết quả, có áp dụng hàm chiết khấu logarit (vị trí càng thấp thì giá trị đóng góp càng giảm).

**Bước 1: Tính Discounted Cumulative Gain (DCG@K)**
$$\text{DCG@K} = \sum_{r=1}^K \frac{\text{gain}_r}{\log_2(r + 1)}$$
Trong đó $\text{gain}_r \in \{0, 1\}$ (với $1$ là chunk mang bằng chứng liên quan mới).

**Bước 2: Tính Ideal DCG (IDCG@K)**
Là giá trị DCG lý tưởng khi tất cả các tài liệu liên quan đều được xếp ở các vị trí đầu tiên ($r = 1, 2, \dots$):
$$\text{IDCG@K} = \sum_{r=1}^{\min(K, |\text{Declared Evidence}|)} \frac{1}{\log_2(r + 1)}$$

**Bước 3: Chuẩn hóa nDCG@K**
$$\text{nDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$

- **Phạm vi giá trị:** $[0.0, 1.0]$.
- **Ý nghĩa thực tế:** Là **thước đo vàng** (Gold Standard Metric) của bài toán IR và RAG. nDCG@5 cao chứng minh hệ thống không chỉ tìm thấy đúng thông tin mà còn đẩy các thông tin quan trọng nhất lên đầu danh sách cho LLM đọc.

---

### 4.5. Hit Rate / Hit Case Count

**Định nghĩa:** Tỷ lệ các câu hỏi mà hệ thống tìm được **ít nhất một** tài liệu liên quan trong Top $K$:

$$\text{Hit} = \begin{cases} 1, & \text{nếu } \text{Recall@K} > 0 \\ 0, & \text{nếu } \text{Recall@K} = 0 \end{cases}$$

- **Ý nghĩa thực tế:** Phản ánh tỷ lệ câu hỏi mà hệ thống "không bị mù thông tin". Trong 45 câu hỏi V3:
  - E5-base đạt `42/45` (93.3%).
  - E5-small đạt `41/45` (91.1%).
  - Huydang DEk21 đạt `40/45` (88.9%).
  - MiniLM-L12 đạt `34/45` (75.6%).

---

## 5. Phương pháp Kiểm định Thống kê & Guardrails

Để đảm bảo việc lựa chọn mô hình dựa trên bằng chứng khoa học vững chắc thay vì ngẫu nhiên, Phase 8 áp dụng hệ thống kiểm định 3 lớp:

```
                  ┌────────────────────────────────────────┐
                  │    KẾT QUẢ RETRIEVAL (45 CÂU HỎI)      │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │ LỚP 1: 9 CATEGORY GUARDRAILS (Bảo vệ danh mục)   │
             │ • Nhóm lớn (n >= 6): Cấm giảm hits, delta >= -0.02│
             │ • Nhóm nhỏ (n <= 3): Cấm mất hit từng case       │
             └────────────────────────┬────────────────────────┘
                                      │ (Phải ĐẠT toàn bộ)
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │ LỚP 2: PAIRED BOOTSTRAP 10.000 LẦN (95% CI)     │
             │ • Tính khoảng tin cậy của delta nDCG@5          │
             │ • Yêu cầu: Lower Bound CI > 0                   │
             └────────────────────────┬────────────────────────┘
                                      │
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │ LỚP 3: CLEAR QUALITY GAIN                       │
             │ • delta nDCG@5 >= +0.03                         │
             │ • Vượt mốc Control và Best Lighter Finalist     │
             └─────────────────────────────────────────────────┘
```

---

### 5.1. Category Guardrails (9 Danh mục câu hỏi V3)

Tất cả 9 danh mục câu hỏi trong Golden Dataset V3 đều được bảo vệ nghiêm ngặt:

| Danh mục ($n$) | Số lượng câu | Quy tắc Guardrail áp dụng |
| :--- | :---: | :--- |
| **`relationship`** | 14 | **Quy tắc Nhóm Lớn ($n \ge 6$):**<br>1. Số lượng case có Hit trong Top 5 không được giảm so với Control.<br>2. Nếu số Hit bằng nhau, $\Delta \text{nDCG@5}$ không được giảm quá `-0.02`. |
| **`direct_fact`** | 7 | |
| **`food_knowledge`**| 7 | |
| **`comparative`** | 6 | |
| **`holistic`** | 3 | **Quy tắc Nhóm Nhỏ ($n \le 3$):**<br>Áp dụng kiểm tra chính xác trên từng câu hỏi (Per-case guardrail). Bất kỳ câu hỏi nào mà Control đã tìm thấy bằng chứng trong Top 5 thì Candidate **tuyệt đối không được làm mất** toàn bộ bằng chứng khỏi Top 5. |
| **`spanning`** | 3 | |
| **`guide_planning`**| 2 | |
| **`numerical`** | 2 | |
| **`temporal`** | 1 | |

---

### 5.2. Paired Bootstrap 95% Confidence Interval (CI)

- **Tại sao cần Bootstrap?** Kích thước tập kiểm thử $N = 45$ câu là mẫu hữu hạn. Sự chênh lệch điểm trung bình giữa hai mô hình có thể do ngẫu nhiên.
- **Cách thực hiện:**
  1. Lấy $N = 45$ cặp điểm $(\text{score}_{\text{cand}, i}, \text{score}_{\text{ctrl}, i})$ tương ứng từng câu hỏi.
  2. Lấy mẫu ngẫu nhiên có hoàn lại (Resampling with replacement) 45 cặp này, lặp lại **10.000 lần** với `seed = 42`.
  3. Với mỗi lần lặp, tính $\Delta \text{nDCG@5} = \text{mean}(\text{cand}) - \text{mean}(\text{ctrl})$.
  4. Lấy phân vị $2.5\%$ (Lower Bound) và phân vị $97.5\%$ (Upper Bound).
- **Ý nghĩa:** Nếu khoảng tin cậy `[Lower, Upper]` nằm hoàn toàn ở phía dương ($\text{Lower} > 0$), ta có thể kết luận với độ tin cậy $95\%$ rằng mô hình mới thực sự vượt trội hơn mô hình cũ.

---

### 5.3. Tiêu chí Quyết định "Clear Quality Gain"

Một mô hình ứng viên (Candidate) chỉ được công nhận là **vượt trội thực sự** (Clear Gain) khi thỏa mãn đồng thời cả 5 điều kiện:
1. `status == "completed"` (hoàn tất đủ 3/3 lần chạy lặp).
2. Đạt toàn bộ **9/9 Category Guardrails**.
3. $\Delta \text{nDCG@5} \ge +0.03$ (tăng ít nhất 3% điểm chuẩn hóa).
4. Phân vị dưới của 95% CI: $\text{Lower Bound} > 0.0$.
5. Thắng mốc Control (`E5-small`) và thắng mốc Lighter Finalist tốt nhất trước đó.

---

## 6. Đo lường Hiệu năng: Độ trễ (Latency) & Bộ nhớ (Memory RSS)

### 6.1. Quy trình đo lường 3 Repetitions
1. **Cold Load Latency:** Đo thời gian nạp mô hình từ ổ đĩa vào RAM ở lần gọi đầu tiên.
2. **Discarded Warm-up:** Thực thi 1 câu hỏi mẫu (`foods-v3-0001`) để làm nóng các bộ đệm CPU/PyTorch và loại bỏ kết quả này khỏi thống kê.
3. **3 Full Repetitions:** Chạy 3 vòng độc lập toàn bộ 45 câu hỏi:
   - **Query Embedding Latency:** Thời gian chuyển đổi câu hỏi thành vector.
   - **Qdrant Search Latency:** Thời gian tìm kiếm vector tương đồng trong cơ sở dữ liệu.
   - **Ranking Stable:** Xác nhận thứ tự xếp hạng của cả 45 câu có giống hệt nhau $100\%$ giữa 3 lần chạy hay không.

### 6.2. Các chỉ số phân vị (p50, p95)
- **p50 (Median):** $50\%$ số lượt truy vấn có thời gian xử lý nhanh hơn mức này (đại diện cho trải nghiệm người dùng thông thường).
- **p95:** $95\%$ số lượt truy vấn có thời gian xử lý nhanh hơn mức này (đại diện cho trường hợp tải nặng / câu hỏi phức tạp).

---

## 7. Bảng Tổng hợp So sánh & Khuyến nghị Lựa chọn

### Bảng đối chiếu ba model hiện hành và MiniLM historical (CPU FP32, 45 câu hỏi Golden V3, 572 chunks):

| Tiêu chí | E5-small 384D (Control) | MiniLM-L12 384D | Huydang DEk21 768D | E5-base 768D |
| :--- | :---: | :---: | :---: | :---: |
| **Kích thước Vector ($d$)** | **384** | **384** | 768 | 768 |
| **Số tham số (Params)** | **~118M** | **~118M** | ~135M | ~278M |
| **Hits / 45 cases** | 41 / 45 (91.1%) | 34 / 45 (75.6%) | 40 / 45 (88.9%) | **42 / 45 (93.3%)** |
| **Recall@5** | 0.8185 | 0.5815 | 0.8370 | **0.8407** |
| **MRR@5** | **0.7748** | 0.5144 | 0.7211 | 0.6985 |
| **nDCG@5** | **0.7425** | 0.4709 | 0.7164 | 0.7061 |
| **$\Delta$ nDCG@5 (vs Control)** | *Baseline* | -0.2716 | -0.0262 | -0.0364 |
| **Category Guardrails** | **9 / 9 ĐẠT** | 2 / 9 (FAIL) | 6 / 9 (FAIL) | 7 / 9 (FAIL) |
| **Độ trễ Query p50** | **24.23 ms** | 23.42 ms | 53.84 ms | 112.33 ms |
| **Tổng độ trễ p50** | **30.77 ms** | 29.34 ms | 60.56 ms | 122.81 ms |
| **Doc Embed 572 chunks** | **18.87 s** | **15.77 s** | 42.91 s | 52.63 s |
| **Peak RAM (RSS)** | **1.54 GB** | 1.83 GB | 2.06 GB | 2.15 GB |
| **Số chunk bị cắt ngắn** | **0 / 572** | 83 / 572 | 1 / 572 | **0 / 572** |
| **Độ ổn định (3/3 reps)** | `True` (100%) | `True` (100%) | `True` (100%) | `True` (100%) |

---

### Khuyến nghị & Kết luận Kỹ thuật

1. **Lựa chọn tối ưu cho MVP hiện tại:**
   **`intfloat/multilingual-e5-small` (384D)** tiếp tục là **mô hình vượt trội nhất** cho hệ thống Hue Foods RAG:
   - Đạt nDCG@5 (`0.7425`) và MRR@5 (`0.7748`) cao nhất toàn bảng.
   - Tốc độ truy vấn nhanh nhất (p50 ~27 ms trên CPU).
   - Kích thước vector 384D nhỏ gọn, tiết kiệm RAM và dung lượng index Qdrant.
   - Không bị hiện tượng cắt ngắn văn bản (max length 512).

2. **Bài học kinh nghiệm từ các mô hình khác:**
   - **`Huydang DEk21`:** Rất có triển vọng cho bài toán hiểu sâu ẩm thực tiếng Việt (`food_knowledge` nDCG đạt `0.8571`). Tuy nhiên, cần được fine-tune mở rộng thêm miền du lịch và tăng max sequence length lên 512 trước khi có thể thay thế E5-small.
   - **`MiniLM-L12`:** Không phù hợp cho văn bản RAG có đoạn văn dài do giới hạn 128 tokens gây sụt giảm chất lượng nghiêm trọng.
   - **`E5-base`:** Không đem lại lợi ích tương xứng với chi phí tính toán (tốn gấp đôi RAM, chậm gấp đôi nhưng nDCG lại thấp hơn bản small).
