# Review: báo cáo hệ thống của A — `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_DANH_GIA.md`

Decision: **changes_requested** (1 major, 6 minor; sửa nhỏ, không cần review lại cả file)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Đối tượng: `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md` (87 dòng), `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` (84 dòng)
Nguồn đối chiếu: `reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md`,
`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`, `reports/phase_8_probe_context_top10_2026_10_24.md`,
`reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1), code `backend/`.

## 1. Phạm vi đã review

B đọc toàn bộ cả hai file. Mỗi số liệu được đối chiếu với report 7B/B4/B5 (do B viết, đã được
C hoặc A kiểm) và với file private trong `data/evaluation/phase_7b/`. Mỗi mô tả hành vi được đối
chiếu với code hiện tại.

## 2. Findings

### Major

**M1 — `LUONG_HOAT_DONG_HE_THONG.md:73`: gán sai nguyên nhân của chunk vụn.**
- File ghi: "20% đoạn rất ngắn (≤48 token) **do** chunker vẫn giữ giới hạn 256 token của model
  HuyDang đã bỏ."
- Bằng chứng: report C1 tách thành hai quan sát riêng.
  - O1 + O2 (`reports/phase_8_candidate_hypotheses_2026_10_24.md:32-33`): chunk vụn đến từ quy tắc
    "mỗi khối Markdown là một chunk, không gộp khối cạnh nhau". 20,3% ≤48 token; 8.276/8.459 chunk
    chỉ có `body`.
  - O3 (`:34`): giới hạn HuyDang 256 chỉ làm **6 bảng** bị tách thêm.
- Giới hạn trên (max token) chỉ khiến khối dài bị cắt nhỏ, không tạo ra hàng nghìn chunk ngắn.
- Tác động: User đọc file này trước khi brainstorm Phase 8. Nếu tin câu trên, User có thể nghĩ
  "bỏ ràng buộc 256" (H1) sẽ hết chunk vụn, trong khi cái cần đổi là gộp khối (H2).
- Tiêu chí đóng: tách thành hai ý. (a) ~20% đoạn rất ngắn (≤48 token) vì mỗi khối Markdown là
  một đoạn, không gộp. (b) Chunker còn giữ giới hạn 256 token của HuyDang (model đã bỏ), làm 6
  bảng bị tách theo dòng.

### Minor

**m1 — `LUONG_HOAT_DONG_HE_THONG.md:52`: viết giả thuyết như sự thật.**
- File ghi "kể cả khi chỉ thiếu một phần (prompt 'tất cả hoặc không')".
- Prompt thật (`backend/llm/full_corpus_prompt.py:7-16`) chỉ nói "Nếu bằng chứng không đủ, trả đúng
  duy nhất câu sau". Prompt không nói gì về trường hợp thiếu một phần. "Tất cả hoặc không" là giả
  thuyết H8, rút từ hành vi quan sát được ở B4 (10/22 case có một phần bằng chứng mà vẫn từ chối).
- Tiêu chí đóng: ghi "quan sát: bot thường từ chối cả câu khi chỉ có một vế (giả thuyết H8, Phase 8 thử)".

**m2 — `LUONG_HOAT_DONG_HE_THONG.md:62`: "gần như toàn bộ điểm bị mất nằm ở đây" là nói quá.**
- Khoảng cách tới trần do 22 từ chối nhầm, tính từ số trong Gate 4 §4.4: Accuracy ~85%,
  Completeness ~65%, Relevance ~90%. Phần còn lại của Completeness đến từ câu đã trả lời nhưng thiếu ý.
- Tiêu chí đóng: "phần lớn điểm bị mất (65–90% tùy tiêu chí) nằm ở đây".

**m3 — `LUONG_HOAT_DONG_HE_THONG.md:65`: token ra mỗi câu.**
- File ghi "~70 token ra". Run 1 thật: 14.392 / 176 = **~82** output, 166.713 / 176 = **~947** input.
  Chi phí ~0,00014 USD là đúng (0,02387 / 176).
- Tiêu chí đóng: "~950 token vào, ~80 token ra".

**m4 — `BAO_CAO_DANH_GIA.md:47-51`: cột "Nguyên nhân" trình bày phân loại như nguyên nhân đã chứng minh.**
- B4 ghi rõ đây là phân loại theo keyword proxy, chưa chứng minh nguyên nhân
  (`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md` §4.3, "Giới hạn của cách đo").
- Tiêu chí đóng: đổi tiêu đề cột thành "Phân loại (theo keyword đáp án trong 5 đoạn)", và thêm một
  câu "dấu hiệu, chưa chứng minh nguyên nhân".

**m5 — `BAO_CAO_DANH_GIA.md:53`: "12/22 câu có đáp án nằm ở hạng 6–10" là nói quá số đo.**
- B4 đo được: 12/22 case có **nhiều keyword hơn** trong top-10 so với trong 5 đoạn ngữ cảnh. Phép đo
  tính trên mọi keyword, không chỉ keyword mang đáp án, và không đòi đủ đáp án.
- Tiêu chí đóng: "12/22 câu có thêm keyword liên quan ở hạng 6–10, bị cắt vì chỉ giữ 5 đoạn".

**m6 — `BAO_CAO_DANH_GIA.md`: còn thiếu so với yêu cầu "Việc chung" và spec §7.6.**
- (a) Bảng "Hôm nay còn đúng không" (`:69-75`) chưa dẫn file:dòng. Mục "Việc chung" trong
  `CURRENT_HANDOFF.md` yêu cầu phần này.
- (b) Baseline có 6 metric, nhưng file chỉ nêu 3 metric answer. Thiếu retrieval: MRR 0,72 / nDCG 0,75
  / Keyword Coverage 92,4% trên 158 câu.
- Tiêu chí đóng: thêm một dòng retrieval vào bảng §3. Thêm bằng chứng cho §6, ví dụ
  `backend/evaluation/full_corpus_eval.py` (lệnh `generate`/`summarize`),
  `backend/evaluation/full_corpus_judge_prompt.md`, `backend/config/settings.yaml:110-113`.

## 3. Cách người kiểm đã kiểm

Kiểm bằng đọc file và tính lại từ dữ liệu private. Không gọi paid, không sửa code.

- Số trong `BAO_CAO_DANH_GIA.md` §3 và `LUONG_HOAT_DONG_HE_THONG.md` §4: so với Gate 4 §4–6
  (B đã tính lại từ `run1_answers.jsonl` và `claude_run1.jsonl` trong B6).
- Đường chạy (mục 1–3 của `LUONG`): đọc `backend/api/app.py:182` (`app = create_app()`, nên lệnh
  `uvicorn api.app:app` ở `:83` đúng); `backend/retrieval/full_corpus.py:149-150`, `:608`
  (RRF k=60, limit 30), `:627` (`fused[:10]`); `backend/retrieval/full_corpus_context.py:88-110`
  (5 đoạn, đánh số); `backend/llm/citations.py:12-27` (luật lỗi citation); `backend/llm/full_corpus_prompt.py:3-16`;
  `frontend/` có `index.html`, `app.js`.
- Nguyên nhân chunk vụn: `reports/phase_8_candidate_hypotheses_2026_10_24.md:32-34`.

## 4. Kết quả quan sát — các điểm đúng

| Nội dung trong file | Kiểm | Kết quả |
|---|---|---|
| Điểm mốc 4,43 / 4,28 / 4,45; theo category | Gate 4 §4.1 | Đúng |
| 22/158 từ chối nhầm = đúng 22 câu 1/1/1; bỏ ra còn 4,92 / 4,75 / 4,95 | Gate 4 §4.3–4.4 | Đúng |
| Từ chối đúng 18/18; lỗi citation 4/176 | Gate 4 §4.2 | Đúng |
| Nhiễu cả đường ≤0,011; Claude chấm lại không lệch >1 | Gate 4 §5 | Đúng |
| Claude–luna trùng 89–96% | Gate 4 §5 (0,892 / 0,949 / 0,960) | Đúng |
| 8 / 10 / 4 (phân loại B4); thử 10 đoạn → 10/22 hết từ chối, 0,005 USD | B4 §4.3, B5 §4.2 | Đúng số (xem m4, m5 về cách diễn đạt) |
| Chi phí ~0,087 USD; quota Claude ~1,1M token; 121 câu 5/5/5 → 55 câu còn lại | Gate 4 §6, §4.3 | Đúng |
| Dense 30 ứng viên → BM25 chấm lại trong 30 → RRF k=60 → 10 đoạn → 5 đoạn ngữ cảnh (~900 token) | code (mục 3) | Đúng |
| Luật lỗi citation (không [n], [n] lạ, từ chối có [n]) → 500 | `citations.py:16-26`, `chat.py` | Đúng |
| BM25 tự viết tách theo âm tiết, vocabulary 5.660 | `backend/scoring/bm25.py` (`\w+`), build record | Đúng |
| Lệnh chạy thử `uvicorn api.app:app` | `backend/api/app.py:182` | Đúng |

## 5. Giới hạn

- Không khởi động API hay chạy lệnh ở mục 6 của `LUONG`. Lệnh chỉ được kiểm bằng đọc code.
- Tỉ giá 1 USD ≈ 25.000 đồng và "~2.200 đồng" không kiểm (không phải dữ liệu dự án).

## 6. Decision và bước tiếp theo

`changes_requested`: sửa M1 và các minor theo tiêu chí đóng ở trên. Đây đều là sửa câu chữ, không
cần chạy lại gì. B kiểm lại diff khi A báo sửa xong.
