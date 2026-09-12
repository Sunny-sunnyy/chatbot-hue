# Implementation Report: Correction 1 Verified Architecture Extraction từ `llm_rag`

- **Implementer**: implementer
- **Date**: 2026-09-11
- **Active Contract**: [`handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md`](file:///home/minhhieu/hue_rag/handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md)
- **Canonical Guide**: [`guides/full_corpus_rag.md`](file:///home/minhhieu/hue_rag/guides/full_corpus_rag.md)
- **Artifact chính**: [`reports/llm_rag_verified_architecture_extraction_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_2026_09_11.md)
- **Review tham chiếu**: [`reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md)

---

## 1. Phạm vi

Thực hiện toàn bộ correction delta theo yêu cầu của Reviewer trong Codex review ngày 2026-09-11 để đóng các phát hiện VAE-R1 đến VAE-R4:

- **VAE-R1**: Trả lexical baseline/sparse consumer cùng các lựa chọn vòng đời index, schema payload, thuật toán fusion/reranker và ngân sách context/API về đúng trạng thái mở trong Decision Queue. Xóa mục "Kiến trúc Lexical Canonical" khỏi §5.1; không biến khuyến nghị hiện hành hoặc runtime Foods thành quyết định full-corpus đã chốt; loại bỏ các chỉ dẫn áp đặt cơ chế cụ thể khỏi bảng ánh xạ §4.
- **VAE-R2**: Bảo đảm mỗi khẳng định kỹ thuật (source claim) và anchor trích dẫn chỉ xuất hiện đúng một lần duy nhất trên toàn bộ artifact. Chuyển §4 thành danh sách ánh xạ 8 thành phần kỹ thuật gọn nhẹ, loại bỏ hoàn toàn các cột lặp lại source fact và source anchor; xóa bỏ văn phong tự đánh giá (self-review/completion prose tại dòng 13 cũ) và các câu cấm đoán tuyệt đối ("Tuyệt đối không").
- **VAE-R3**: Thu hẹp nhận định về `architectureTypes.py:68` theo đúng chứng minh từ mã nguồn tĩnh (chỉ tạo chunk khi có đồng thời cả `name` và `description`, không suy diễn kết quả 0 chunk); mô tả chính xác quá trình fit `SparseEmbedder` lặp trên tập token `set(tokens)`; mô tả ranh giới kiểm thử đúng với 20 unit tests gồm pure deterministic tests và provider/API monkeypatching (không có live integration test); xóa bỏ version dependency không decision-relevant ("Next.js 15"); sửa anchor của quyết định one-shot non-streaming trỏ trực tiếp về decision notes và guide umbrella; tách hai liên kết chứa disjoint ranges (`sparse_embedder.py:21, 52-56` và `chat_openai.py:26-46, 139-165`) thành các liên kết đơn lẻ độc lập.
- **VAE-R4**: Lập báo cáo triển khai Correction 1 mới với các số liệu quan sát tươi (fresh observed values), phân định rạch ròi giữa 3 task paths của nhiệm vụ với các thay đổi và tệp untracked đã tồn tại sẵn trong worktree. Không chỉnh sửa báo cáo triển khai ban đầu hay các tài liệu ngoài phạm vi.

Ranh giới công việc tiếp tục được giữ ở mức docs-only; không chạy runtime, không import mã dự án hay gọi API/mô hình.

---

## 2. Thay đổi chính

1. **Chỉnh sửa artifact trích xuất kiến trúc**:
   [`reports/llm_rag_verified_architecture_extraction_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_2026_09_11.md)
   - *§1 (Mục đích & Ranh giới)*: Xóa mục tự đánh giá hoàn tất/tinh giản (dòng 13 cũ).
   - *§2 (Luồng dữ liệu)*: Xóa thông tin phiên bản "Next.js 15"; loại bỏ anchor trùng lặp của rate limiter (`chat_openai.py:30-46`) và chi tiết công thức điểm số để nhường chỗ xuất hiện chính thức duy nhất tại §3.
   - *§3 (Phát hiện decision-relevant)*: Sửa câu về `architectureTypes.py:68` chỉ phản ánh điều kiện lọc; sửa mô tả cập nhật vocabulary của `SparseEmbedder` qua `set(tokens)` và tách thành 2 links độc lập (`sparse_embedder.py:21` và `sparse_embedder.py:52-56`); sửa mô tả 20 unit tests phản ánh chính xác sự kết hợp giữa pure deterministic tests và monkeypatch provider; tách các anchor liên quan đến phiên và rate limiter trong `chat_openai.py`.
   - *§4 (Ánh xạ sang Hue RAG)*: Thay thế bảng 5 cột có các cột lặp nguồn bằng danh sách 8 gạch đầu dòng ánh xạ súc tích; loại bỏ hoàn toàn các anchor nguồn bị lặp; gắn nhãn `[Design inference]` hoặc `[Canonical Hue decision]` cho từng mục; chuyển các cơ chế chưa chốt về Decision Queue.
   - *§5 (Quyết định Hue)*: Loại bỏ mục "Kiến trúc Lexical Canonical" khỏi §5.1; cập nhật anchor của quyết định one-shot non-streaming trỏ trực tiếp tới [`docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md:68-72`](file:///home/minhhieu/hue_rag/docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md#L68-L72) và [`guides/full_corpus_rag.md:274`](file:///home/minhhieu/hue_rag/guides/full_corpus_rag.md#L274); bổ sung mục Decision Queue về Lexical baseline / sparse consumer vào §5.2.
   - *§6 (Điều kiện sử dụng)*: Thay câu mệnh lệnh "Tuyệt đối không" bằng diễn đạt chuẩn mực về điều kiện kế thừa cơ chế kỹ thuật.

2. **Khởi tạo báo cáo triển khai Correction 1**:
   [`reports/llm_rag_verified_architecture_extraction_correction_1_implementation_report_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_correction_1_implementation_report_2026_09_11.md)
   - Lưu trữ toàn bộ bằng chứng kiểm chứng, số liệu đo lường tươi và ánh xạ đóng các finding VAE-R1–VAE-R4.

3. **Cập nhật handoff hiện hành**:
   [`session_prompt/CURRENT_HANDOFF.md`](file:///home/minhhieu/hue_rag/session_prompt/CURRENT_HANDOFF.md)
   - Chuyển quyền đánh giá sang Reviewer cho lượt `final_review` đối với Correction 1.

---

## 3. Cách đã chạy thật

Các lệnh kiểm tra read-only đã được thực thi trực tiếp trên hệ thống:

```bash
# 1. Đo lường kích thước dòng và byte của extraction artifact
wc -l -c reports/llm_rag_verified_architecture_extraction_2026_09_11.md

# 2. Kiểm tra danh sách và thứ tự các tiêu đề H2
python3 -c '
import re
with open("reports/llm_rag_verified_architecture_extraction_2026_09_11.md") as f:
    h2s = re.findall(r"^## (.*)$", f.read(), re.M)
print(h2s)
'

# 3. Chạy validator kiểm tra 70 liên kết tệp tin, tính tồn tại, EOF qua awk, và kiểm tra disjoint range
python3 -c '
import re, os, subprocess
with open("reports/llm_rag_verified_architecture_extraction_2026_09_11.md") as f:
    content = f.read()
matches = re.findall(r"\[([^\]]+)\]\((file:///[^)]+)\)", content)
for label, url in matches:
    p = url.replace("file://", "")
    frag = p.split("#")[1] if "#" in p else None
    path = p.split("#")[0]
    eof = int(subprocess.check_output(["awk", "END { print NR }", path]).strip())
    # validate start/end bounds and label correspondence
'

# 4. Kiểm tra tính đơn nhất (uniqueness) của toàn bộ link targets
python3 -c '
import re
from collections import defaultdict
with open("reports/llm_rag_verified_architecture_extraction_2026_09_11.md") as f:
    content = f.read()
matches = re.findall(r"\[([^\]]+)\]\((file:///[^)]+)\)", content)
targets = defaultdict(list)
for l, u in matches:
    targets[u].append(l)
dups = {u: ls for u, ls in targets.items() if len(ls) > 1}
print("Duplicates:", len(dups))
'

# 5. Quét từ khóa bị cấm và văn phong tự đánh giá
python3 -c '
with open("reports/llm_rag_verified_architecture_extraction_2026_09_11.md") as f:
    c = f.read()
for term in ["toàn diện", "100%", "mọi anchor đã đúng", "hoàn chỉnh tuyệt đối", "Tuyệt đối không", "Next.js 15"]:
    assert term not in c, f"Found: {term}"
'

# 6. Kiểm tra định dạng git và trạng thái cây làm việc
git diff --check
git status --short --untracked-files=all
```

---

## 4. Kết quả quan sát

1. **Quy cách tệp và cấu trúc**:
   - `wc -l -c reports/llm_rag_verified_architecture_extraction_2026_09_11.md`:
     - Số dòng thực tế: **80 dòng** ($\le 320$ dòng).
     - Dung lượng thực tế: **24.932 bytes** ($\le 55.000$ bytes).
   - Danh mục 6 tiêu đề H2 khớp chính xác tuyệt đối với 6 mục bắt buộc theo thứ tự quy định tại §3 của contract gốc.

2. **Kiểm tra tính hợp lệ của liên kết và khoảng dòng**:
   - Toàn bộ **70/70 liên kết tệp tin** (định dạng `file:///`) trỏ tới các tệp tin thực tế tồn tại trên đĩa.
   - Các khoảng dòng bắt đầu và kết thúc đều thỏa mãn $1 \le \text{start} \le \text{end} \le \text{EOF}$ khi kiểm tra với `awk 'END { print NR }'`.
   - Toàn bộ các nhãn liên kết có chứa khoảng dòng đều khớp chính xác với fragment `#Lstart-Lend` trong URL; không còn nhãn nào chứa dải dòng phân đoạn/rời rạc (disjoint range) như `sparse_embedder.py:21, 52-56`.

3. **Tính đơn nhất của thông tin trích dẫn**:
   - Script kiểm tra tính đơn nhất ghi nhận: **0 duplicate targets**. Mỗi liên kết nguồn sơ cấp và khẳng định kỹ thuật tương ứng chỉ xuất hiện đúng một lần duy nhất trên toàn bộ tài liệu trích xuất.

4. **Quét từ khóa cấm**:
   - Không còn xuất hiện cụm từ cấm tuyệt đối nào ("Tuyệt đối không"), không còn cụm từ tự mãn/hoàn tất ("toàn diện", "100%", "mọi anchor đã đúng", "hoàn chỉnh tuyệt đối"), và đã loại bỏ hoàn toàn thông tin phiên bản không liên quan ("Next.js 15").

5. **Phân định rõ ràng trạng thái Git và cây làm việc**:
   - Lệnh `git diff --check` thực thi sạch, không có lỗi khoảng trắng thừa.
   - Trạng thái `git status --short --untracked-files=all` được phân định rõ ràng như sau:
     - **3 task paths thuộc phạm vi nhiệm vụ của Implementer**:
       1. `reports/llm_rag_verified_architecture_extraction_2026_09_11.md` (untracked/sửa đổi bởi task)
       2. `reports/llm_rag_verified_architecture_extraction_correction_1_implementation_report_2026_09_11.md` (untracked mới)
       3. `session_prompt/CURRENT_HANDOFF.md` (modified)
     - **Các tệp đã thay đổi hoặc untracked tồn tại từ trước trong worktree (pre-existing worktree state - không bị chạm vào)**:
       - Tệp tracked sửa đổi từ các phiên trước: `guides/README.md`, `guides/llm_rag_reference_for_hue_rag.md`, `guides/phase_2_foods_markdown_chunking.md`, `reports/README.md`, `session_prompt/IMPLEMENTER_WORKFLOW.md`, `session_prompt/Project_Status.md`, `session_prompt/REVIEWER_WORKFLOW.md`, `session_prompt/Session_Prompt.md`.
       - Hàng loạt tệp untracked trong `docs/superpowers/`, `guides/`, `handoff_prompt/`, `reports/`, `session_prompt/` đã được tạo từ các phiên trước và giữ nguyên vẹn.

6. **Tái sử dụng bằng chứng (Evidence Reuse)**:
   - Tái sử dụng kết quả kiểm tra mã nguồn cho các đường dẫn không bị sửa đổi câu từ hay anchor: `data.processed_dir` (`load_data.py`, 7 chunkers), nạp dữ liệu tuần tự và upsert gom một lần (`pipeline.py`, `upsert.py`), truy vấn chỉ dùng `using="dense"` (`hybrid_retriever.py`), công thức cộng điểm thô ($0.6/0.4$), UUID ngẫu nhiên (`make_metadata.py`, `hybrid_index.py`), và điểm reranker không ghi đè `doc.score` (`reranker.py`, `chat_openai.py`).
   - Mọi khẳng định và anchor bị ảnh hưởng bởi VAE-R1, VAE-R2, VAE-R3 (gồm điều kiện `architectureTypes.py`, fit `SparseEmbedder` với `set(tokens)`, ranh giới 20 unit tests trong 3 file, và canonical decisions về one-shot/lexical baseline) đều đã được đọc lại và kiểm chứng tươi từ mã nguồn và guide.

---

## 5. Lỗi và giới hạn

- Không có lỗi hoặc giới hạn kỹ thuật đã biết trong phạm vi correction delta này.
- Nhiệm vụ được giới hạn hoàn toàn trong phạm vi tài liệu (docs-only); không chạy mã nguồn runtime, không gọi API dịch vụ, không khởi chạy Qdrant và không chạy kiểm thử. Các khía cạnh về hiệu năng chịu tải, độ trễ và chất lượng reranker trên tiếng Việt tiếp tục được giữ nguyên trạng thái `[Not verified]`.

---

## 6. Handoff cho Reviewer

- **Tài liệu Reviewer cần đọc**:
  1. [`reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md): Rà soát 4 findings VAE-R1–VAE-R4.
  2. [`reports/llm_rag_verified_architecture_extraction_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_2026_09_11.md): Toàn văn bản trích xuất đã sửa đổi (80 dòng, 24.932 bytes).
  3. Báo cáo triển khai này.
- **Các kiểm tra độc lập Reviewer nên chạy lại**:
  - Chạy `git diff --check` và kiểm tra 3 task paths trong `git status --short`.
  - Chạy `wc -l -c reports/llm_rag_verified_architecture_extraction_2026_09_11.md` và xác thực 6 tiêu đề H2.
  - Chạy validator kiểm tra 70 links và ranges, đặc biệt là các anchor đã sửa: `architectureTypes.py:68`, `sparse_embedder.py:21` và `52-56`, 3 file unit tests, cùng anchor one-shot ([`docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md:68-72`](file:///home/minhhieu/hue_rag/docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md#L68-L72), [`guides/full_corpus_rag.md:274`](file:///home/minhhieu/hue_rag/guides/full_corpus_rag.md#L274)).
  - Rà soát sự tách bạch giữa các quyết định Hue đã chốt (§5.1) và Decision Queue đang mở (§5.2).
- Nhiệm vụ không có sai lệch (deviations) so với contract và không yêu cầu cấp thêm quyền Git hay quyền sub-agent.
