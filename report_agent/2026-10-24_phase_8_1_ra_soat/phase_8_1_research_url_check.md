# Phase 8.1 — Kiểm nguồn của kết quả nghiên cứu ChatGPT bằng WebFetch (C14)

Ngày: 24/10/2026, 20:01–20:05 (giờ lấy bằng `date`) · Người làm: C · Loại: kiểm nguồn, chỉ đọc,
miễn phí · Việc: `session_prompt/CURRENT_HANDOFF.md` "### C14" · Review: A.

Đầu vào (private, đọc hết, không chép nội dung):
`gửi chatgpt/2026-10-24/kết quả nghiên cứu/phase_8_1_decision_audit_2026_10_24.md`. Gọi đúng mã nguồn
S01–S29 như mục V của file đó. Mỗi trích dẫn dưới đây là câu ngắn trên trang gốc (WebFetch, 24/10/2026).

## 1. Tóm tắt

- **Đã kiểm 22/29 nguồn:** cả 16 nguồn bắt buộc (S01, S02, S04, S10–S14, S16, S17, S20–S22, S24–S26),
  thêm S03, S06, S09, S18, S19, S27. Cả 22 nguồn đều tồn tại. URL S18 chuyển hướng sang trang khác,
  nội dung vẫn đúng.
- **Khớp:** 16 nguồn. **Khớp một phần / lệch:** 5 (S02, S12, S13, S22 phần reranker, S24; mục 3).
  **Không kiểm được trọn:** 1 (S27).
  Chưa có chỗ nào cho thấy ChatGPT bịa nguồn.
- **Qdrant đang chạy `1.18.3`** (`curl :6335/`). Mọi mốc phiên bản trong S10 đều có sẵn: Query API
  v1.10, DBSF v1.11, RRF k cấu hình được từ v1.16, RRF có trọng số từ v1.17.
- **Phát hiện có ích cho spec 8.1:**
  1. Công thức IDF của Qdrant `modifier: idf` **giống hệt** công thức IDF đang dùng trong
     `backend/scoring/bm25.py:66-70` (cùng `ln((N − n + 0.5)/(n + 0.5) + 1)`). Đây là câu hỏi nghiên
     cứu phụ ghi lại khi rà C11 (ghi chú vùng 3–5).
  2. Giá $0,08/$0,13 của `qwen/qwen3.5-9b` là của provider rẻ nhất, chạy **fp4**. Provider bf16 rẻ nhất
     là $0,10/$0,15.
  3. `gpt-6-luna` mặc định `reasoning.effort = medium`; context window 1.050.000 token, output tối đa
     128.000.

## 2. Bảng nguồn

| ID | Tồn tại | Khẳng định trong kết quả nghiên cứu | Trang gốc nói (trích ngắn) | Kết luận |
|---|---|---|---|---|
| S01 | có (arXiv 2401.05856, 11/01/2024) | 7 failure point, rút từ 3 case study | "present 7 failure points to consider when designing a RAG system"; 3 case study (research, education, biomedical) | **khớp** |
| S02 | có (arXiv 2408.08067, v1 15/08/2024) | Chẩn đoán retrieval + generation **ở mức claim**; đánh giá 8 hệ thống; tương quan với người | "significantly better correlations with human judgments"; 8 hệ thống. Abstract **không** dùng chữ "claim" | **khớp một phần**: mức claim chưa thấy trong abstract, chưa đọc full paper |
| S03 | có (NeurIPS 2024) | RAGChecker ở NeurIPS 2024 | Trang proceedings NeurIPS 37, **Datasets and Benchmarks Track**, DOI 10.52202/079017-0692 | **khớp** (bổ sung: track D&B) |
| S04 | có (NAACL 2024 long, 06/2024) | ARES: dữ liệu tổng hợp huấn luyện judge nhẹ + vài trăm nhãn người qua PPI; không phải zero-human | "finetunes lightweight LM judges"; "using only a few hundred human annotations" | **khớp** |
| S06 | có | Faithfulness = claim được hỗ trợ / tổng claim | "Number of claims in the response supported by the retrieved context" / "Total number of claims" | **khớp** |
| S09 | có | NFC khuyến nghị cho văn bản thường; NFKC làm mất phân biệt | "NFC is the best form for general text"; NFKC/NFKD "do lose information" | **khớp** |
| S10 | có | RRF mặc định `k=2`; k cấu hình từ v1.16; RRF trọng số v1.17; DBSF v1.11; Query API v1.10 | "$k$ is a constant (set to 2 by default)"; "Available as of v1.16.0" / "v1.17.0" / "v1.11.0" / "v1.10.0" | **khớp**. Qdrant đang chạy 1.18.3 ≥ mọi mốc |
| S11 | có | `exact=true` quét toàn bộ; sparse luôn exact | "full scan to retrieve exact results"; sparse "Always exact in Qdrant" | **khớp**. Trang **không** ghi `hnsw_ef` mặc định |
| S12 | có (phần sparse ở offset >100k ký tự) | IDF tính theo shard; **không bật khi sparse đã nhân IDF** | "IDF statistics are calculated per shard"; công thức `ln((N − n + 0.5)/(n + 0.5) + 1)`. **Không có** câu cảnh báo "đã nhân IDF thì không bật" | **lệch một phần**: lời cảnh báo là suy luận của ChatGPT (đúng về logic, trùng lý do của spec Phase 4 §5), không phải câu trong tài liệu |
| S13 | có | Như S12 | "IDF statistics are computed over all data in the shard being queried"; không có cảnh báo | **lệch một phần** (như S12) |
| S14 | có | DBSF so với RRF mặc định trên 5 dataset: +0,0161 / +0,0184 / +0,0383 / −0,0045 / +0,0148; hai hiệu không rõ theo CI | nDCG@10: CodeSearchNet +0,0161, DBPedia-entity +0,0184, WANDS +0,0383, ArguAna −0,0045, SciFact +0,0148. 3 dataset "95% interval excludes zero"; SciFact/ArguAna "inconclusive" | **khớp**. Bổ sung điều kiện đo: dense `all-MiniLM-L6-v2`, BM25 core, **200 candidate/prefetch**, RRF `k=2`; tác giả gọi là "directional" |
| S16 | có (TACL vol. 12, 2024) | Có hiệu ứng vị trí ("lost in the middle") | Kém hơn khi thông tin nằm "in the middle of long contexts" | **khớp** |
| S17 | có (Google Research 2025, arXiv 2511.05850, Max McKinnon) | Gemini 2.5 Flash tìm fact đơn giản tốt bất kể vị trí | "great accuracy regardless of document position"; LITM "not present for simple factoid Q&A" | **khớp** (chỉ câu factoid) |
| S18 | có — URL chuyển hướng tới "Prompting best practices" | Bọc tài liệu bằng `<document>`/`<source>`/`<document_content>` | "wrap each document in `<document>` tags with `<document_content>` and `<source>`" (mục Long context prompting) | **khớp** (URL đổi; nên trích URL mới khi dùng) |
| S19 | có (23/09/2023) | Lỗi khi LLM tự sinh câu eval: trả lời được không cần context, mơ hồ "this document", lộ đáp án, quá dễ | "answer off the top of its head without reference to any document"; "reference 'this document'…"; "contain the answer" | **khớp** (bối cảnh: câu trắc nghiệm cho bài test long-context) |
| S20 | có (thread 08/04/2024, trả lời của BAAI) | Kiến trúc tối đa 8192, fine-tune với `max_length=1024`, khuyên 1024 | "fine-tune this model with a max length of 1024, so we recommend to set max_length=1024" | **khớp** |
| S21 | có (21/03/2024, trả lời của BAAI) | Như S20 | "Recommend to set max_length=1024 (we fine-tune the model with max_length=1024)" | **khớp** |
| S22 | có | 0.6B tối đa 1024 chiều; 4B 2560; 8B 4096; khuyên instruction tiếng Anh; instruction +1–5% | "Up to 1024, supports user-defined output dimensions ranging from 32 to 1024"; 4B "2560", 8B "4096"; "write their instructions in English"; "improvement of 1% to 5%" | **khớp**. Bổ sung: context 32K; tài liệu không cần instruction. **Lệch nguồn:** khẳng định "Qwen3-**Reranker**-0.6B context 32K" (§18) lại dẫn card **Embedding**, chưa kiểm card reranker |
| S24 | có (model `qwen/qwen3.5-9b`, tạo 10/03/2026) | Giá $0,08/M vào, $0,13/M ra; context 262.144; có structured output; nhiều provider | API công khai OpenRouter (`/api/v1/models`, `/endpoints`): context 262.144; giá cấp model $0,17/$0,25. Theo provider: Darkbloom $0,08/$0,13 (**fp4**), SiliconFlow $0,10/$0,15 (fp8), DeepInfra $0,10/$0,15 (bf16), Parasail $0,10/$0,25 (bf16), Together $0,17/$0,25. Cả 5 có `structured_outputs`; **không thấy** Venice | **lệch một phần**: $0,08/$0,13 là provider rẻ nhất chạy fp4 (lượng tử mạnh). Muốn so công bằng nên pin provider bf16 (DeepInfra $0,10/$0,15). Giá đổi theo thời gian |
| S25 | có | Giá $0,10/$0,50; `reasoning.effort` none/low/medium(mặc định)/high/xhigh/max | "Input \| $0.1 \| 1M tokens"; "Output \| $0.5"; "`reasoning.effort` supports `none`, `low`, `medium` (default), `high`, `xhigh`, and `max`" | **khớp**. Bổ sung: context 1.050.000 (input tối đa 922.000), output tối đa 128.000; prompt > 272K token tính giá ×2. Trang không nói gì về `temperature` |
| S26 | có | Mặc định effort phụ thuộc model | "Defaults are also model-dependent"; "GPT-6 Luna also default to `medium`" | **khớp**. Ghi chú: trang không ghi ID `gpt-6-luna` (chỉ thấy `gpt-5.6-luna`) |
| S27 | có | Structured Outputs bảo đảm **shape** theo schema, không bảo đảm citation/dữ kiện đúng | "ensures the model will always generate responses that adhere to your supplied JSON Schema". Phần đọc được (100k/136k ký tự) **không có** câu nói rõ "không bảo đảm đúng dữ kiện" | **không kiểm được trọn**: nửa đầu khớp; nửa sau là suy luận hợp lý, chưa thấy câu nguồn |

**Không kiểm** (NOT RUN, không thuộc danh sách bắt buộc): S05 (RAGAS available metrics), S07–S08
(DeepEval), S15 (Sentence Transformers efficiency), S23 (repo Qwen3-Embedding), S28 (Holm 1979), S29
(Efron 1979).

## 3. Lệch và ý nghĩa cho spec 8.1

1. **S12/S13 — cảnh báo về IDF modifier là suy luận.** Kết luận vẫn đúng: giá trị sparse hiện tại đã
   gồm IDF (`embedding/sparse.py:90`), bật thêm modifier sẽ nhân IDF hai lần. Có một điểm mới: công thức
   IDF Qdrant giống hệt `bm25.py:66-70`. Nếu muốn dùng native sparse với `modifier: idf`, chỉ cần lưu
   giá trị không nhân IDF. Lúc đó cần kiểm thêm: N và n của Qdrant đếm theo shard và theo "non-zero
   element", phải khớp với cách project đếm df.
2. **S24 — giá Qwen 3.5-9B phụ thuộc provider và độ lượng tử.**
   - Giá rẻ nhất ($0,08/$0,13) là fp4. Bf16 rẻ nhất: DeepInfra $0,10/$0,15.
   - Ước chi phí so model trên 176 câu: ~176 × 950 token vào, ~176 × 90 token ra → **~0,02 USD** ở giá
     bf16 (C tính từ số token Run 1).
   - Theo luật dự án (pin provider để tái lập, bài học 8B), spec nên pin một provider bf16.
3. **S22 — khẳng định về Qwen3-Reranker dẫn sai card.** Muốn dùng số 32K cho reranker thì phải kiểm card
   `Qwen/Qwen3-Reranker-0.6B` riêng.
4. **S02 — "claim-level" của RAGChecker chưa thấy trong abstract.** Có thể nằm trong phần phương pháp
   của paper. Chưa ảnh hưởng spec, vì metric claim-level dự án định dùng tự định nghĩa
   (`unsupported_claim_rate`, `required_fact_recall`).
5. **S14 — số DBSF đo trong điều kiện khác dự án:** dense MiniLM, 200 candidate/prefetch, RRF k=2. Chỉ
   dùng làm hướng, đúng như tài liệu tự gọi "directional".
6. **S25/S26 — mặc định effort là `medium`.** Mọi kết quả 7B đã đo ở effort `medium` (khóa
   `reasoning_effort` đang bị cấm ở `settings_loader.py`, nên dùng mặc định). Thí nghiệm effort (C11
   dòng 6.8) có baseline rõ: `medium`.
7. **S11/S12 — `hnsw_ef` mặc định vẫn chưa rõ.** `full_scan_threshold` mặc định 10000 KB ("1Kb = 1
   vector of size 256") dùng cho truy vấn có điều kiện lọc. Dự án không lọc, nên tài liệu không cho
   biết truy vấn hiện có quét đủ hay không. Thí nghiệm exact vs HNSW (C11 dòng 4.2) vẫn cần.

## 4. Cách kiểm và giới hạn

- WebFetch từng URL với câu hỏi "tồn tại? trích câu ngắn về khẳng định X".
  - Trang dài thì đọc thêm bằng `offset`. S12 đọc tới phần sparse IDF; S10, S11, S27 chỉ đọc 100k ký tự
    đầu, các mốc cần kiểm đều nằm trong phần đó (trừ S27).
- S24 dùng thêm API công khai của OpenRouter (GET, không key): `https://openrouter.ai/api/v1/models` và
  `…/models/qwen/qwen3.5-9b/endpoints`. Lý do: trang HTML trả bản tóm tắt không có giá.
- Phiên bản Qdrant: `curl -s http://127.0.0.1:6335/` → `"version":"1.18.3"`.
- **Giới hạn:**
  - WebFetch trả nội dung qua một model tóm tắt. Trích dẫn ở đây là câu model đó báo lại, chưa đối
    chiếu từng ký tự với HTML.
  - Giá và provider là số tại 24/10/2026, có thể đổi.
  - Chưa đọc full paper S02/S04.
- Không gọi API trả phí, không sửa code/dữ liệu, không chép nội dung file nghiên cứu private ngoài các
  khẳng định ngắn cần đối chiếu.
