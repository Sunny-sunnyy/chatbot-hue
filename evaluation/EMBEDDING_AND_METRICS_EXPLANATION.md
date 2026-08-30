# Hướng dẫn & Giải thích Kỹ thuật: Mô hình Embedding, Sparse Retrieval, Fusion và Các Độ đo Đánh giá (Hue Foods RAG)

> **Tài liệu kỹ thuật tham chiếu nội bộ** cho nhóm phát triển và nghiên cứu dự án **Hue Foods RAG**.
> **Cập nhật:** `2026-08-30` (Bổ sung toàn diện Phase 8 — Notebook 08a Dense & Notebook 08b Sparse/Fusion Benchmark).

---

## Mục lục

1. [Tổng quan về Retrieval & Kiến trúc Đa tầng trong RAG](#1-tổng-quan-về-retrieval--kiến-trúc-đa-tầng-trong-rag)
2. [Các Mô hình Dense Embedding (Ngữ nghĩa)](#2-các-mô-hình-dense-embedding-ngữ-nghĩa)
   - [2.1. `intfloat/multilingual-e5-small` (384D) — Control Baseline](#21-intfloatmultilingual-e5-small-384d--control-baseline)
   - [2.2. `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (768D) — Candidate 1](#22-code4lifeofficialhuydang-dek21-embedding-768d--candidate-1)
   - [2.3. `intfloat/multilingual-e5-base` (768D) — Candidate 2](#23-intfloatmultilingual-e5-base-768d--candidate-2)
   - [2.4. Phân tích các mô hình Dense đã loại bỏ](#24-phân-tích-các-mô-hình-dense-đã-loại-bỏ)
3. [Các Thuật toán Sparse Retrieval (Từ khóa & Tần suất)](#3-các-thuật-toán-sparse-retrieval-từ-khóa--tần-suất)
   - [3.1. Thuật toán BM25 (Best Matching 25) & Hiệu chỉnh Siêu tham số](#31-thuật-toán-bm25-best-matching-25--hiệu-chỉnh-siêu-tham-số)
   - [3.2. TF-IDF Sparse Representation & Qdrant Sparse Vectors](#32-tf-idf-sparse-representation--qdrant-sparse-vectors)
   - [3.3. So sánh Bộ tách từ (Tokenizers): Unicode Word vs Underthesea Word](#33-so-sánh-bộ-tách-từ-tokenizers-unicode-word-vs-underthesea-word)
4. [Các Chiến lược Hợp nhất Đa luồng (Hybrid Fusion Strategies)](#4-các-chiến-lược-hợp-nhất-đa-luồng-hybrid-fusion-strategies)
   - [4.1. Reciprocal Rank Fusion (RRF)](#41-reciprocal-rank-fusion-rrf)
   - [4.2. Min-Max Score Normalization Weighted Sum (Score Fusion)](#42-min-max-score-normalization-weighted-sum-score-fusion)
   - [4.3. Dense-to-BM25 Rescoring (Chấm lại điểm 2 chặng)](#43-dense-to-bm25-rescoring-chấm-lại-điểm-2-chặng)
5. [Nguyên lý Tiền xử lý & Hợp đồng Input (Input Contracts)](#5-nguyên-lý-tiền-xử-lý--hợp-đồng-input-input-contracts)
   - [5.1. Tiền tố Bất đối xứng (Asymmetric Query/Passage Prefix)](#51-tiền-tố-bất-đối-xứng-asymmetric-querypassage-prefix)
   - [5.2. Tách từ tiếng Việt chuyên biệt (PyVi ViTokenizer)](#52-tách-từ-tiếng-việt-chuyên-biệt-pyvi-vitokenizer)
   - [5.3. Giới hạn độ dài chuỗi (Max Sequence Length) & Hiện tượng Cắt ngắn (Truncation)](#53-giới-hạn-độ-dài-chuỗi-max-sequence-length--hiện-tượng-cắt-ngắn-truncation)
   - [5.4. Chuẩn hóa Vector L2 & Dot Product Similarity](#54-chuẩn-hóa-vector-l2--dot-product-similarity)
6. [Các Độ đo Đánh giá Chất lượng Truy xuất (Retrieval Metrics)](#6-các-độ-đo-đánh-giá-chất-lượng-truy-xuất-retrieval-metrics)
   - [6.1. Đơn vị Tính điểm Relevance: Cặp `(source, section)` & Bão hòa Bằng chứng](#61-đơn-vị-tính-điểm-relevance-cặp-source-section--bão-hòa-bằng-chứng)
   - [6.2. Recall@K (Recall@5 & Recall@30)](#62-recallk-recall5--recall30)
   - [6.3. Candidate Union Recall (Độ phủ Tập ứng viên Gộp)](#63-candidate-union-recall-độ-phủ-tập-ứng-viên-gộp)
   - [6.4. MRR@K (Mean Reciprocal Rank @ K)](#64-mrrk-mean-reciprocal-rank--k)
   - [6.5. nDCG@K (Normalized Discounted Cumulative Gain @ K)](#65-ndcgk-normalized-discounted-cumulative-gain--k)
   - [6.6. Hit Rate / Hit Case Count](#66-hit-rate--hit-case-count)
7. [Đo lường Hiệu năng: Phân tích Độ trễ (p50, p95, p99) & Bộ nhớ](#7-đo-lường-hiệu-năng-phân-tích-độ-trễ-p50-p95-p99--bộ-nhớ)
   - [7.1. Phân vị Độ trễ (Latency Percentiles: p50, p95, p99) là gì?](#71-phân-vị-độ-trễ-latency-percentiles-p50-p95-p99-là-gì)
   - [7.2. Tại sao p95 và p99 là Thước đo Vàng trong RAG & Hệ thống Phân tán?](#72-tại-sao-p95-và-p99-là-thước-đo-vàng-trong-rag--hệ-thống-phân-tán)
   - [7.3. Quy trình đo lường 3 Repetitions & Loại bỏ Warm-up](#73-quy-trình-đo-lường-3-repetitions--loại-bỏ-warm-up)
8. [Phương pháp Kiểm định Thống kê & Guardrails](#8-phương-pháp-kiểm-định-thống-kê--guardrails)
   - [8.1. Category Guardrails (9 Danh mục câu hỏi V3)](#81-category-guardrails-9-danh-mục-câu-hỏi-v3)
   - [8.2. Paired Bootstrap 95% Confidence Interval (CI)](#82-paired-bootstrap-95-confidence-interval-ci)
   - [8.3. Tiêu chuẩn Khoa học Fail-Closed](#83-tiêu-chuẩn-khoa-học-fail-closed)
9. [Bảng Tổng hợp Toàn diện Benchmark 08a & 08b](#9-bảng-tổng-hợp-toàn-diện-benchmark-08a--08b)
10. [Khuyến nghị Kiến trúc cho Production & Bước đi Tiếp theo (Phase 8c)](#10-khuyến-nghị-kiến-trúc-cho-production--bước-đi-tiếp-theo-phase-8c)

---

### 1. Tổng quan về Retrieval & Kiến trúc Đa tầng trong RAG

Trong kiến trúc **Retrieval-Augmented Generation (RAG)** hiện đại, chất lượng câu trả lời của mô hình ngôn ngữ lớn (LLM) phụ thuộc trực tiếp vào tính chính xác và đầy đủ của ngữ cảnh được truy xuất.

Hệ thống RAG nâng cao không chỉ dựa vào một phương pháp tìm kiếm đơn lẻ mà kết hợp **đa tầng truy xuất (Multi-stage Retrieval)**:

```
                      [ Câu hỏi của người dùng ]
                                  │
            ┌─────────────────────┴─────────────────────┐
            ▼                                           ▼
  ┌───────────────────┐                       ┌───────────────────┐
  │  Dense Retrieval  │                       │ Sparse Retrieval  │
  │ (Semantic Vector) │                       │  (BM25 / TF-IDF)  │
  └─────────┬─────────┘                       └─────────┬─────────┘
            │ (Top-30 Candidates)                       │ (Top-30 Candidates)
            └─────────────────────┬─────────────────────┘
                                  ▼
                    ┌───────────────────────────┐
                    │  Hybrid Fusion (RRF/Sum)  │ -> Tạo Candidate Pool (Union)
                    └─────────────┬─────────────┘
                                  │ (Top-10 -> Top-5)
                                  ▼
                    ┌───────────────────────────┐
                    │ Cross-Encoder Reranker    │ (Phase 8c)
                    └─────────────┬─────────────┘
                                  │ (Top-5 Reranked Context)
                                  ▼
                    ┌───────────────────────────┐
                    │    LLM Generator (Hue)    │ -> Câu trả lời chính xác
                    └───────────────────────────┘
```

1. **Dense Retrieval (Ngữ nghĩa):** Sử dụng các mạng nơ-ron Transformer để nắm bắt ngữ nghĩa trừu tượng, đồng nghĩa, ngữ cảnh câu hỏi dù từ ngữ không trùng lặp (ví dụ: *"quán ăn ngon cố đô"* $\leftrightarrow$ *"địa chỉ ẩm thực nức tiếng ở Huế"*).
2. **Sparse Retrieval (Từ khóa):** Dựa trên tần suất từ và nghịch đảo tần suất văn bản (BM25, TF-IDF) để nắm bắt chính xác các danh từ riêng, tên quán, địa chỉ, số liệu (ví dụ: *"bánh ép Cây Dừa"*, *"04 Phan Bội Châu"*, *"chè hẻm"*).
3. **Fusion (Hợp nhất):** Kết hợp các danh sách ứng viên từ Dense và Sparse để tạo ra tập ngữ cảnh vừa giàu ngữ nghĩa vừa chuẩn xác từ khóa.

---

## 2. Các Mô hình Dense Embedding (Ngữ nghĩa)

Hệ thống đã đánh giá thực nghiệm **3 cấu hình dense embedding canonical** trên CPU FP32 với 572 chunks dữ liệu thật:

---

### 2.1. `intfloat/multilingual-e5-small` (384D) — Control Baseline

- **Đơn vị phát triển:** Microsoft Research.
- **Kiến trúc:** XLM-RoBERTa backbone, 12 layers, hidden dimension $d = 384$, ~118M tham số.
- **Pooling & Tiền tố:** Attention-mask mean pooling; yêu cầu tiền tố bất đối xứng `passage: ` cho tài liệu và `query: ` cho câu hỏi.
- **Max Sequence Length:** 512 tokens (bao phủ 100% tài liệu mà không bị cắt ngắn).
- **Cách thức hoạt động:** Được huấn luyện đối chiếu (contrastive learning) trên tập dữ liệu đa ngôn ngữ CCPairs (>1 tỉ cặp câu), tối ưu hóa việc phân biệt giữa câu hỏi ngắn và văn bản dài.
- **Hiệu năng trên dữ liệu Huế (08a):**
  - **nDCG@5:** `0.7425` | **MRR@5:** `0.7748` | **Recall@5:** `0.8185` | **Hits:** `41/45` (91.1%).
  - **Độ trễ p50:** `24.2 ms` | **Độ trễ p95:** `30.8 ms`.
  - **RAM Peak:** ~1.54 GB RSS.
- **Đánh giá:** **Xuất sắc toàn diện về tốc độ và tài nguyên**. Là mốc đối chứng (Control) chuẩn mực cho hệ thống.

---

### 2.2. `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (768D) — Candidate 1

- **Tác giả:** Đặng Quang Huy (HCMUTE).
- **Kiến trúc:** **PhoBERT-base** (RoBERTa chuyên biệt cho tiếng Việt), 12 layers, hidden dimension $d = 768$, ~135M tham số.
- **Pooling & Tiền xử lý:** Mean pooling; bắt buộc phân đoạn từ vựng tiếng Việt bằng `pyvi.ViTokenizer.tokenize()`; không dùng tiền tố.
- **Max Sequence Length:** 256 tokens.
- **Dữ liệu huấn luyện:** Fine-tune trên ~100.000 cặp câu hỏi/văn bản tiếng Việt bằng hàm mất mát Matryoshka Loss kết hợp Multiple Negatives Ranking (MNRL).
- **Hiệu năng trên dữ liệu Huế (08a & 08b):**
  - **Độc lập (08a):** Recall@5 = `0.8370`, nDCG@5 = `0.7164`.
  - **Khi kết hợp BM25 (08b):** **Recall@5 = `0.9111`** (tăng vọt +7.41%), **nDCG@5 = `0.7655`** (vô địch về chất lượng).
  - **Độ trễ p95:** `62.9 ms` (độc lập), `65.4 ms` (hybrid).
- **Đánh giá:** **Biểu diễn ngữ nghĩa tiếng Việt cực kỳ xuất sắc**. Khi kết hợp cùng BM25, mô hình giải quyết được toàn bộ điểm mù từ khóa và trở thành cấu hình retrieval mạnh nhất toàn hệ thống.

---

### 2.3. `intfloat/multilingual-e5-base` (768D) — Candidate 2

- **Đơn vị phát triển:** Microsoft Research.
- **Kiến trúc:** XLM-RoBERTa-base, 12 layers, hidden dimension $d = 768$, ~278M tham số.
- **Pooling & Tiền tố:** Attention-mask mean pooling; tiền tố `passage: ` và `query: `.
- **Max Sequence Length:** 512 tokens.
- **Hiệu năng trên dữ liệu Huế:**
  - **Độc lập:** Recall@5 = `0.8407`, nDCG@5 = `0.7061`, Hits = `42/45` (93.3%).
  - **Khi kết hợp BM25 (Rescore):** Recall@5 = `0.8963`, nDCG@5 = `0.7659`.
  - **Độ trễ p95:** `61.5 ms` (độc lập), `73.7 ms` (rescore).
- **Đánh giá:** Độ phủ Recall ban đầu cao, nhưng số lượng tham số lớn (~278M) khiến chi phí tính toán cao hơn E5-small mà nDCG độc lập không vượt trội.

---

### 2.4. Phân tích các mô hình Dense đã loại bỏ

| Mô hình | Lý do loại bỏ khỏi phạm vi Local Execution |
| :--- | :--- |
| **`paraphrase-multilingual-MiniLM-L12-v2` (384D)** | • **Tử huyệt max length 128:** Bị cắt ngắn 83/572 chunks (14.5%), gây mất mát nghiêm trọng phần đuôi văn bản.<br>• **Chất lượng tụt sâu:** nDCG@5 chỉ đạt `0.4709` ($\Delta = -0.2716$), trượt 7/9 guardrails.<br>• Không nhẹ hơn và không nhanh hơn E5-small. |
| **`Qwen/Qwen3-Embedding-0.6B` (384D / 1024D)** | • **Độ trễ CPU quá lớn:** 572 chunks mất 765 giây (~12.7 phút), query p50 mất **781.8 ms** (chậm gấp 36 lần E5-small).<br>• Chất lượng nDCG@5 chỉ đạt `0.6175` ($\Delta = -0.1251$). |
| **`BAAI/bge-m3` & `E5-large` (1024D)** | • Kích thước lớn (>560M params) gây quá tải CPU và RAM cục bộ; chuyển hướng đánh giá qua Remote API. |

---

## 3. Các Thuật toán Sparse Retrieval (Từ khóa & Tần suất)

---

### 3.1. Thuật toán BM25 (Best Matching 25) & Hiệu chỉnh Siêu tham số

**BM25** là thuật toán xếp hạng dựa trên xác suất (Probabilistic Relevance Framework), cải tiến từ TF-IDF cổ điển bằng cách bổ sung cơ chế **bão hòa tần suất từ (Term Frequency Saturation)** và **chuẩn hóa độ dài văn bản (Document Length Penalization)**.

#### Công thức toán học BM25:

$$\text{BM25}(D, Q) = \sum_{i=1}^{|Q|} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

Trong đó:
- $f(q_i, D)$: Tần suất xuất hiện của từ $q_i$ trong tài liệu $D$.
- $|D|$: Độ dài (số lượng từ) của tài liệu $D$.
- $\text{avgdl}$: Độ dài trung bình của tất cả tài liệu trong toàn bộ kho dữ liệu.
- $\text{IDF}(q_i) = \ln \left( \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1 \right)$: Nghịch đảo tần suất văn bản ($N$ là tổng số chunks, $n(q_i)$ là số chunks chứa từ $q_i$).

#### Ý nghĩa 2 Siêu tham số $(k_1, b)$:
1. **$k_1$ (Tốc độ bão hòa TF):** Điều khiển mức độ ảnh hưởng của tần suất từ. Khi một từ xuất hiện nhiều lần, điểm số sẽ tiệm cận mức bão hòa $(k_1 + 1)$. $k_1$ nhỏ $\rightarrow$ bão hòa nhanh; $k_1$ lớn $\rightarrow$ cho phép tần suất từ đóng góp nhiều điểm hơn.
2. **$b$ (Hệ số phạt độ dài):** $b \in [0.0, 1.0]$. Khi $b = 1.0$, hệ thống phạt tối đa các đoạn văn bản dài (để tránh việc văn bản dài có lợi thế ngẫu nhiên vì chứa nhiều từ); khi $b = 0.0$, độ dài văn bản bị bỏ qua hoàn toàn.

#### Kết quả Calibration trên 572 chunks ẩm thực Huế:
- Bộ tham số **Baseline ($k_1=1.5, b=0.75$)** đạt Recall@30 = `0.9519`, nDCG@5 = `0.6478`, vượt qua 100% category guardrails và được chọn làm tiêu chuẩn.

---

### 3.2. TF-IDF Sparse Representation & Qdrant Sparse Vectors

Bên cạnh BM25 in-memory, hệ thống xây dựng mô hình biểu diễn vector thưa (**Sparse Vector**) lưu trữ trực tiếp trên Qdrant:
- **Từ điển (Vocabulary):** 2,093 từ vựng duy nhất được sắp xếp cố định (`vocabulary_fingerprint: b75949...`).
- **Công thức Log-TF:**
  $$\text{TF}(t, d) = \begin{cases} 1 + \ln(\text{count}(t, d)), & \text{nếu } \text{count}(t, d) > 0 \\ 0, & \text{ngược lại} \end{cases}$$
- **Công thức Smoothed-IDF:**
  $$\text{IDF}(t) = \ln\left(\frac{N + 1}{\text{df}(t) + 1}\right) + 1$$
- **Chuẩn hóa $L_2$:**
  $$\mathbf{s} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2}, \quad \|\mathbf{s}\|_2 = 1.0$$

Vector thưa được lưu dưới dạng danh sách cặp `(indices, values)` giúp Qdrant thực hiện tìm kiếm inverted index cực nhanh với dot product.

---

### 3.3. So sánh Bộ tách từ (Tokenizers): Unicode Word vs Underthesea Word

| Tiêu chí | `unicode_word` (Regex `\w+`) | `underthesea_word` (Compound Tokenizer) |
|---|:---:|:---:|
| **Nguyên lý** | Tách từ đơn thuần theo ranh giới ký tự Unicode và dấu cách. | Phân đoạn từ ghép tiếng Việt (ví dụ: *"bún_bò"*, *"bánh_khoái"*). |
| **Recall@30** | `0.9519` (44/45 hits) | `0.9556` (44/45 hits) |
| **nDCG@5** | **`0.6478`** | `0.6416` |
| **Độ trễ p95** | **`5.3 ms`** (Cực nhanh) | `14.8 ms` (Chậm hơn gần $3\times$) |
| **Phụ thuộc** | 0 thư viện ngoài (Chuẩn Python) | Cần nạp model ML tách từ phức tạp |
| **Quyết định** | ✅ **CHỌN** (Nguyên tắc Simplicity First) | ❌ Không chọn do chi phí không tương xứng |

---

## 4. Các Chiến lược Hợp nhất Đa luồng (Hybrid Fusion Strategies)

Khi truy xuất đồng thời từ cả kênh Dense ($K=30$) và kênh Sparse ($K=30$), hệ thống cần thuật toán hợp nhất để sắp xếp lại danh sách kết quả tối ưu:

---

### 4.1. Reciprocal Rank Fusion (RRF)

**RRF** là thuật toán hợp nhất dựa trên **thứ hạng (Rank-based Fusion)**, không phụ thuộc vào thang điểm số (score scale) của từng hệ thống tìm kiếm:

$$\text{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Trong đó:
- $M = \{\text{Dense}, \text{Sparse}\}$: Tập hợp các bộ truy xuất.
- $r_m(d) \in \{1, 2, \dots, K\}$: Thứ hạng của tài liệu $d$ trong danh sách của bộ truy xuất $m$. (Nếu tài liệu không xuất hiện, $r_m(d) = \infty \rightarrow \frac{1}{k + \infty} = 0$).
- $k = 60$: Hằng số làm mượt chuẩn (Smoothing constant).

- **Ưu điểm:** Cực kỳ ổn định, không cần chuẩn hóa điểm số, không sợ điểm số của một mô hình lấn át mô hình kia.
- **Nhược điểm:** Bỏ qua độ lớn khoảng cách cosine thực tế giữa câu hỏi và tài liệu.

---

### 4.2. Min-Max Score Normalization Weighted Sum (Score Fusion)

Phương pháp hợp nhất dựa trên **điểm số có trọng số (Score-based Fusion)**:

**Bước 1: Chuẩn hóa Min-Max điểm số của từng kênh về đoạn $[0.0, 1.0]$:**
$$S_{\text{norm}, m}(d) = \frac{S_m(d) - \min_{d'} S_m(d')}{\max_{d'} S_m(d') - \min_{d'} S_m(d') + \epsilon}$$

**Bước 2: Tính tổng điểm có trọng số:**
$$\text{Final\_Score}(d) = w_{\text{dense}} \cdot S_{\text{norm, dense}}(d) + w_{\text{sparse}} \cdot S_{\text{norm, sparse}}(d)$$

Trong đó hệ thống sử dụng cấu hình chuẩn:
- $w_{\text{dense}} = 0.6$ ($60\%$ trọng số Ngữ nghĩa)
- $w_{\text{sparse}} = 0.4$ ($40\%$ trọng số Từ khóa)

- **Kết quả thực nghiệm:** Đạt nDCG@5 = **`0.7655`**, **vượt trội hơn RRF (`0.7567`)** vì phản ánh chính xác độ tin cậy của khoảng cách cosine trên dữ liệu tiếng Việt.

---

### 4.3. Dense-to-BM25 Rescoring (Chấm lại điểm 2 chặng)

Quy trình 2 chặng:
1. **Chặng 1 (Candidate Generation):** Dùng Dense Embedding quét nhanh toàn bộ kho dữ liệu để lấy ra $K_1 = 30$ chunks tiềm năng nhất.
2. **Chặng 2 (Lexical Rescoring):** Dùng BM25 tính điểm lại trên 30 chunks này và sắp xếp lại để chọn ra Top $K_2 = 5$ chunks đưa vào LLM.

- **Ưu điểm:** Tốc độ cực nhanh (chỉ tính BM25 trên 30 chunks), bộ nhớ RAM thấp.
- **Hiệu năng:** `dense-bm25-rescore__e5-small-384` đạt Recall@5 = `0.8630`, nDCG@5 = `0.7545`, p95 chỉ **32.2 ms**.

---

## 5. Nguyên lý Tiền xử lý & Hợp đồng Input (Input Contracts)

```
                 ┌────────────────────────────────────────────────────────┐
                 │                INPUT TEXT BAN ĐẦU                      │
                 └──────────────────────────┬─────────────────────────────┘
                                            │
            ┌───────────────────────────────┼────────────────────────────────┐
            ▼                               ▼                                ▼
   [ Họ mô hình E5 ]                [ Mô hình Huydang ]             [ BM25 / TF-IDF ]
┌───────────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐
│ passage: {văn bản}    │        │ ViTokenizer.tokenize()│        │ unicode_word_tokenize │
│ query: {câu hỏi}      │        │ "Bún_bò Huế..."       │        │ (lowercase NFC words) │
└──────────┬────────────┘        └──────────┬────────────┘        └──────────┬────────────┘
           ▼                                ▼                                ▼
┌───────────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐
│ Max Length: 512       │        │ Max Length: 256       │        │ Max Length: Không hạn chế
└──────────┬────────────┘        └──────────┬────────────┘        └──────────┬────────────┘
           ▼                                ▼                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│              MEAN POOLING -> L2 NORMALIZATION (||v|| = 1.0) -> QDRANT / MEMORY          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1. Tiền tố Bất đối xứng (Asymmetric Query/Passage Prefix)
Họ mô hình E5 bắt buộc:
- Thêm tiền tố `"passage: "` cho văn bản nạp vào DB.
- Thêm tiền tố `"query: "` cho câu hỏi tìm kiếm.

### 5.2. Tách từ tiếng Việt chuyên biệt (PyVi ViTokenizer)
PhoBERT backbone của Huydang DEk21 bắt buộc chạy qua `pyvi.ViTokenizer.tokenize()` để tạo các từ ghép nối bằng dấu gạch dưới (`"Bún_bò"`, `"cố_đô"`).

### 5.3. Giới hạn độ dài chuỗi (Max Sequence Length) & Hiện tượng Cắt ngắn (Truncation)
- E5-small / E5-base ($512$ tokens): $0/572$ chunks bị cắt ngắn.
- Huydang DEk21 ($256$ tokens): $1/572$ chunks bị cắt ngắn nhẹ.

### 5.4. Chuẩn hóa Vector L2 & Dot Product Similarity
Mọi vector đầu ra $\mathbf{v}$ đều được chuẩn hóa $\|\mathbf{v}\|_2 = 1.0$, đưa phép tính Cosine Similarity thành Dot Product trực tiếp:
$$\text{CosineSimilarity}(\mathbf{q}, \mathbf{d}) = \mathbf{q} \cdot \mathbf{d} = \sum_{i=1}^d q_i \cdot d_i$$

---

## 6. Các Độ đo Đánh giá Chất lượng Truy xuất (Retrieval Metrics)

---

### 6.1. Đơn vị Tính điểm Relevance: Cặp `(source, section)` & Bão hòa Bằng chứng

Ground Truth trong Golden Dataset V3 được định nghĩa theo:
$$\text{Evidence Unit} = (\text{source\_file}, \text{section\_h2})$$

> **Quy tắc Bão hòa Bằng chứng (De-duplication Credit):**
> Mỗi cặp `(source, section)` chỉ nhận điểm thưởng $\text{gain} = 1$ **duy nhất ở lần xuất hiện đầu tiên** trong Top $K$. Các chunk tiếp theo cùng section trong Top $K$ sẽ nhận $\text{gain} = 0$.

---

### 6.2. Recall@K (Recall@5 & Recall@30)

Tỷ lệ giữa số lượng bằng chứng liên quan tìm thấy trong Top $K$ so với tổng số lượng bằng chứng được khai báo:

$$\text{Recall@K} = \frac{|\text{Declared Evidence} \cap \text{Retrieved Evidence Top K}|}{|\text{Declared Evidence}|}$$

- **Recall@5:** Đo lường độ bao phủ thông tin trong ngữ cảnh hẹp chuyển trực tiếp cho LLM.
- **Recall@30:** Đo lường độ bao phủ thông tin ở tầng tạo ứng viên (Candidate Generation).

---

### 6.3. Candidate Union Recall (Độ phủ Tập ứng viên Gộp)

Độ phủ bằng chứng khi gộp chung $K=30$ ứng viên từ Dense và $K=30$ ứng viên từ Sparse:

$$\text{Candidate Union Recall} = \frac{|\text{Declared Evidence} \cap (\text{Dense}_{Top30} \cup \text{Sparse}_{Top30})|}{|\text{Declared Evidence}|}$$

- **Kết quả:** `hybrid-bm25-weighted__huydang-dek21` đạt **`0.9852` (98.52%)**, chứng minh tập ứng viên gộp hầu như không bỏ sót bất kỳ thông tin nào của 45 câu hỏi.

---

### 6.4. MRR@K (Mean Reciprocal Rank @ K)

Nghịch đảo vị trí xếp hạng của tài liệu liên quan hợp lệ **đầu tiên** xuất hiện trong danh sách kết quả:

$$\text{MRR@K} = \frac{1}{N} \sum_{i=1}^N \frac{1}{\text{rank}_{\text{first}, i}}$$

---

### 6.5. nDCG@K (Normalized Discounted Cumulative Gain @ K)

Thước đo chuẩn mực đánh giá toàn diện cả số lượng lẫn vị trí thứ hạng của tất cả các tài liệu liên quan:

$$\text{DCG@K} = \sum_{r=1}^K \frac{\text{gain}_r}{\log_2(r + 1)}, \quad \text{nDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$

---

### 6.6. Hit Rate / Hit Case Count

Tỷ lệ câu hỏi tìm thấy **ít nhất một** tài liệu liên quan trong Top $K$ ($\text{Recall@K} > 0$).

---

## 7. Đo lường Hiệu năng: Phân tích Độ trễ (p50, p95, p99) & Bộ nhớ

---

### 7.1. Phân vị Độ trễ (Latency Percentiles: p50, p95, p99) là gì?

Khi đo lường thời gian đáp ứng của hệ thống phần mềm, việc sử dụng **giá trị trung bình (Mean / Average)** thường tạo ra **ảo tưởng về hiệu năng** do các trường hợp chạy nhanh che giấu các trường hợp bị nghẽn nghiêm trọng.

Do đó, kỹ thuật phần mềm chuẩn mực sử dụng **Phân vị (Percentiles)**:

```
Tất cả các lượt truy vấn được sắp xếp theo thời gian tăng dần:
[ 12ms, 15ms, 18ms, ..., 25ms, ..., 65ms, ..., 120ms, 450ms ]
                         ▲          ▲           ▲
                        p50        p95         p99
                    (Median)   (95% nhanh hơn) (99% nhanh hơn)
```

1. **p50 (Median - Phân vị thứ 50):**
   $50\%$ số lượt truy vấn hoàn thành nhanh hơn giá trị này. Đại diện cho **trải nghiệm người dùng thông thường** trong điều kiện lý tưởng.
2. **p95 (95th Percentile - Phân vị thứ 95):**
   $95\%$ số lượt truy vấn có thời gian xử lý nhanh hơn mức này (chỉ $5\%$ chậm hơn). Đại diện cho **trải nghiệm trong trường hợp tải nặng, câu hỏi dài hoặc tài nguyên máy chủ bận rộn**.
3. **p99 (99th Percentile - Phân vị thứ 99):**
   $99\%$ số lượt truy vấn có thời gian xử lý nhanh hơn mức này. Đại diện cho **trường hợp xấu nhất (Worst-case Scenario)**.

---

### 7.2. Tại sao p95 và p99 là Thước đo Vàng trong RAG & Hệ thống Phân tán?

Trong kiến trúc RAG, một truy vấn của người dùng phải trải qua chuỗi xử lý nối tiếp:
$$\text{Total Latency} = \text{Embed Query} + \text{Vector Search} + \text{Sparse Search} + \text{Fusion} + \text{Rerank} + \text{LLM Generation}$$

Nếu một thành phần trong chuỗi bị chậm ở $5\%$ số request (p95 cao), thì khi ghép nhiều thành phần lại với nhau, xác suất người dùng gặp phải phản hồi chậm trễ sẽ tăng lên gấp nhiều lần (**Hiệu ứng Tail Latency Amplification**).

**Các nguyên nhân chính gây ra đuôi độ trễ cao (High Tail Latency / p95) trong RAG:**
- **Câu hỏi dài và phức tạp:** Cần nhiều phép toán ma trận hơn trong Transformer.
- **Bộ nhớ đệm (Cache Miss):** Chưa kịp nạp vector hoặc index vào L3 Cache / RAM.
- **Tranh chấp tài nguyên CPU / Garbage Collection:** PyTorch hoặc Python runtime thực hiện thu dọn bộ nhớ trong lúc đang tính toán.

> 🎯 **Quy chuẩn SLA trong Hue RAG:**
> Hệ thống đặt ngưỡng bảo vệ: $\text{p95 Latency} \le 2.0 \times \text{Control Baseline}$.
> Cấu hình `hybrid-bm25-weighted__huydang-dek21` đạt **p95 = 65.4 ms**, hoàn toàn nằm trong vùng an toàn và đảm bảo trải nghiệm người dùng mượt mà tức thì.

---

### 7.3. Quy trình đo lường 3 Repetitions & Loại bỏ Warm-up

Để loại bỏ hoàn toàn sai số ngẫu nhiên:
1. **Cold Load:** Đo thời gian nạp mô hình từ đĩa cứng vào bộ nhớ.
2. **Discarded Warm-up:** Thực thi 1 câu hỏi mẫu (`foods-v3-0001`) để làm nóng bộ đệm PyTorch/CPU; kết quả này bị loại bỏ khỏi thống kê.
3. **3 Lần Chạy Độc lập (3 Repetitions):** Thực thi toàn bộ 45 câu hỏi $\times$ 3 vòng (900 lượt query), đo lường chi tiết p50, p95 và kiểm tra tính bất biến thứ hạng (`ranking_stable: True`).

---

## 8. Phương pháp Kiểm định Thống kê & Guardrails

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
                                      │
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │ LỚP 2: PAIRED BOOTSTRAP 10.000 LẦN (95% CI)     │
             │ • Tính khoảng tin cậy của delta Recall & nDCG   │
             │ • Yêu cầu: Lower Bound CI > 0                   │
             └────────────────────────┬────────────────────────┘
                                      │
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │ LỚP 3: NGUYÊN TẮC FAIL-CLOSED KHOA HỌC          │
             │ • Không tự ý bypass ngưỡng bảo vệ               │
             │ • Giữ minh bạch báo cáo thực tế                 │
             └─────────────────────────────────────────────────┘
```

### 8.1. Category Guardrails (9 Danh mục câu hỏi V3)
- **Nhóm lớn ($n \ge 6$):** `relationship` ($n=14$), `direct_fact` ($n=7$), `food_knowledge` ($n=7$), `comparative` ($n=6$). Yêu cầu không giảm số lượng Hit, $\Delta \text{nDCG@5} \ge -0.02$.
- **Nhóm nhỏ ($n \le 3$):** `holistic` ($n=3$), `spanning` ($n=3$), `guide_planning` ($n=2$), `numerical` ($n=2$), `temporal` ($n=1$). Tuyệt đối không được làm mất Hit ở bất kỳ case nào mà Control đã làm được.

### 8.2. Paired Bootstrap 95% Confidence Interval (CI)
Lấy mẫu lại có hoàn lại 10.000 lần ($N=45$, `seed=42`) để tính khoảng tin cậy của mức tăng trưởng $\Delta \text{Recall@5}$ và $\Delta \text{nDCG@5}$.

### 8.3. Tiêu chuẩn Khoa học Fail-Closed
Nếu một ứng viên có Recall tổng thể rất cao nhưng giảm nhẹ ở một danh mục bảo vệ (như `relationship` giảm $-0.0279$ vượt ngưỡng $-0.02$), hệ thống tự động trả về `finalist = None` (fail-closed) để kiến trúc sư đánh giá và ra quyết định, tuyệt đối không tự ý làm sai lệch kết quả.

---

## 9. Bảng Tổng hợp Toàn diện Benchmark 08a & 08b

Bảng đối chiếu toàn bộ các cấu hình tiêu biểu qua 2 giai đoạn benchmark (CPU FP32, 572 chunks, 45 câu hỏi Golden V3):

| Nhóm | Cấu hình Retrieval | Recall@5 | $\Delta$ Recall@5 | nDCG@5 | $\Delta$ nDCG@5 | MRR@5 | Độ trễ p50 | Độ trễ p95 | RAM (RSS) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Dense** | `dense__e5-small-384` (Control 08a) | 0.8185 | *Baseline* | 0.7425 | *Baseline* | 0.7088 | 24.2 ms | 30.8 ms | **1.54 GB** |
| **Dense** | `dense__huydang-dek21-768` (08a) | 0.8370 | +0.0185 | 0.7164 | -0.0261 | 0.6698 | 53.8 ms | 62.9 ms | 2.06 GB |
| **Dense** | `dense__e5-base-768` (08a) | 0.8407 | +0.0222 | 0.7061 | -0.0364 | 0.6559 | 112.3 ms | 122.8 ms | 2.15 GB |
| **Sparse**| `bm25-only` (Lexical Baseline) | 0.7889 | -0.0296 | 0.6478 | -0.0947 | 0.5960 | **4.5 ms** | **6.3 ms** | **~0.15 GB** |
| **Sparse**| `tfidf-only` (Qdrant Sparse) | 0.7667 | -0.0518 | 0.6150 | -0.1275 | 0.5599 | 4.2 ms | 5.1 ms | ~0.20 GB |
| **Rescore**| `dense-bm25-rescore__e5-small-384` | 0.8630 | +0.0444 | 0.7545 | +0.0120 | 0.7073 | **26.8 ms** | **32.2 ms** | **1.55 GB** |
| **Rescore**| `dense-bm25-rescore__e5-base-768` | 0.8963 | +0.0556 | 0.7659 | +0.0598 | 0.7147 | 64.2 ms | 73.7 ms | 2.16 GB |
| **Hybrid** | **`hybrid-bm25-weighted__huydang-dek21`** | **0.9111** | **+0.0741** | **0.7655** | **+0.0491** | **0.7076** | **55.6 ms** | **65.4 ms** | 2.08 GB |
| **Hybrid** | `hybrid-bm25-weighted__e5-base-768` | 0.8889 | +0.0481 | 0.7560 | +0.0499 | 0.7064 | 56.4 ms | 66.3 ms | 2.16 GB |
| **Hybrid** | `hybrid-bm25-rrf__huydang-dek21` | 0.8778 | +0.0407 | 0.7567 | +0.0403 | 0.7107 | 54.8 ms | 63.0 ms | 2.08 GB |
| **Hybrid** | `hybrid-tfidf-weighted__huydang-dek21` | **0.9111** | **+0.0741** | 0.7424 | +0.0260 | 0.6778 | 53.2 ms | 62.4 ms | 2.07 GB |

---

## 10. Khuyến nghị Kiến trúc cho Production & Bước đi Tiếp theo (Phase 8c)

### 🏆 1. Cấu hình Khuyến nghị Số 1 (Top Quality Pipeline — Chất lượng Cao nhất)
- **Pipeline:** `Dense Huydang DEk21 768D` + `BM25 FullCorpus` $\rightarrow$ `Min-Max Weighted Sum (0.6/0.4)`.
- **Chỉ số:** Recall@5 = **`91.11%`**, nDCG@5 = **`0.7655`**, Candidate Union Recall (Top-30) = **`98.52%`**, độ trễ p95 = **`65.4 ms`**.
- **Ứng dụng:** Triển khai làm tầng Candidate Generation chính thức cho hệ thống Chatbot RAG Ẩm thực Huế.

### ⚡ 2. Cấu hình Khuyến nghị Số 2 (Top Speed & Resource Pipeline — Siêu nhẹ & Siêu nhanh)
- **Pipeline:** `Dense E5-small 384D` $\rightarrow$ `BM25 Rescoring trên Top-30`.
- **Chỉ số:** Recall@5 = **`86.30%`**, nDCG@5 = **`0.7545`**, độ trễ p95 chỉ **`32.2 ms`**, tiết kiệm 50% RAM.
- **Ứng dụng:** Triển khai trên môi trường Edge / Server tài nguyên hạn chế.

### 🚀 3. Bước đi tiếp theo cho Phase 8c (Cross-Encoder Reranker Benchmark)
Với tập ứng viên Top-30 có độ phủ lên tới **`98.52%`**, hệ thống đã có đầu vào hoàn hảo để tiến hành **Phase 8c (Notebook 08c)**:
- Thử nghiệm các mô hình **Cross-Encoder Reranker** (như BGE-Reranker, Viet-Reranker, Cohere) để chấm lại điểm sâu sắc giữa cặp `(Câu hỏi, Đoạn văn bản)`.
- Kỳ vọng đưa Recall@5 và nDCG@5 vượt ngưỡng **`95%`** trước khi tổng hợp câu trả lời qua LLM.
