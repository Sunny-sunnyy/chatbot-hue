# Implementation Report: rà code — gói 4 (tài liệu: guide + notebook) — B26

Người làm: B (Claude Opus 5.5, terminal `hue-rag-c3`) · việc B26
Date: 2026-10-25 20:04 +0700 (`date`) · nền `main` `5d3376f` · chưa commit (A commit sau review) · **0 USD**
Canonical: `bao_cao_he_thong/DE_XUAT_SUA_CODE.md` gói 4 (User duyệt 19:4x: thêm dòng lịch sử cho guide 0–4; đường dẫn dự án khác ra khỏi
file tracked, không xóa lịch sử git); mục B26 trong `session_prompt/CURRENT_HANDOFF.md`; finding B-16, B-18, B-19, B-21 (`ra_soat_code_B.md`),
C-12, C-13, C-14 (`ra_soat_code_C.md`), R2 (`kiem_cheo_C.md`). Review: C.

## 1. Phạm vi

- **Làm:** banner lịch sử guide 0–4 + viết lại `guides/README.md` (B-16); mục "Hiện hành" guide 7 / 8 (C-12); dòng lệch C-13 (guide 5, 6, 9,
  `llm_rag_reference_for_hue_rag.md`, `full_corpus_rag.md`); C-14 (notebook 06); B-21 (notebook 03, 04); mục "Build lại index khi corpus đổi"
  trong `full_corpus_rag.md` gồm giới hạn huydang 256 (B-18 + R2); thay 48 đường dẫn tuyệt đối tới repo khác (B-19).
- **Không làm (theo mục việc):** lệnh chạy API / build / pytest (B-17 — để sau gói 1b vì phụ thuộc quy ước import). Hai chỗ có lệnh do chính
  việc này viết / chạm đều để nguyên dạng hiện chạy được và ghi "có thể đổi sau 1b" (xem §5). Không sửa code. Không đụng 4 file của C35.
- **File (16):** `guides/README.md`, `full_corpus_rag.md`, `llm_rag_reference_for_hue_rag.md`, 10 guide `phase_0`…`phase_9`, `notebooks/03_embedding_models.ipynb`, `04_qdrant_ingestion.ipynb`, `06_generation_and_api.ipynb`. Private (không commit):
  `data/ra_soat_code/b19_duong_dan_ngoai.md`, `data/ra_soat_code/tools/{deadrefs,edit_notebooks}.py`, `data/ra_soat_code/b26_deadrefs_{before,after}.txt`.

## 2. Thay đổi chính

- **Guide 0–4 (B-16):** khối `> **Guide lịch sử** …` ngay dưới tiêu đề: tả hệ thống Foods / gate 08–10/2026, nhiều file / collection / lệnh đã
  gỡ; trỏ `full_corpus_rag.md` + `Project_Status.md` §4 / §8; mỗi guide ghi file code đang chạy của khâu đó. Nội dung cũ giữ nguyên.
- **`guides/README.md`:** viết lại thành mục lục ngắn (276 ⇒ ~50 dòng): đọc gì trước (Project_Status, CURRENT_HANDOFF, Session_Prompt / WORKFLOW,
  `full_corpus_rag.md`, `bao_cao_he_thong/`, `report_agent/`), bảng 13 guide với trạng thái Phase và loại guide (lịch sử / có mục Hiện hành),
  notebook còn 3 + luật §11, ai sửa guide. Bỏ phần vai "Implementer / Codex Reviewer", vòng đời cũ, quy ước `reports/` (đã thay bằng
  `session_prompt/` và `WORKFLOW.md` §6). Bản cũ còn trong lịch sử Git.
- **Guide 7 / 8 (C-12):** banner "Guide lịch sử **trừ mục Hiện hành ngay dưới**" + `## Hiện hành` (guide 7: Golden 7A, evaluator 7B, judge Claude,
  thước đo 8.1, định nghĩa lỗi citation đổi từ gói 1a; guide 8: 8.1 đóng / kết luận, 8.2 tạm dừng, giữ `gpt-6-luna`, dense e5 + 8B chưa có index)
  + heading `## Lịch sử (Foods và thiết kế trước 2026-10-23)`; banner cũ "chưa active" gắn "(Lịch sử)"; guide 7 "nguồn canonical" và
  `temperature=0` gắn nhãn lịch sử; guide 8 `not_ready` gắn nhãn lịch sử.
- **`full_corpus_rag.md` (C-13, B-18, R2):** dòng Status 2026-10-25 + trỏ mục build lại; CLI evaluator thêm `split` (đối chiếu `--help`: 11 lệnh);
  một câu "câu lỗi citation (API trả 500) vẫn được chấm, đếm riêng `citation_error`"; **mục mới "Build lại index khi corpus đổi"** — hành vi code
  (CLI chỉ `--candidate`, tên collection cố định, không ghi đè collection / build record / sparse state), 7 bước (sao lưu kho; chia đoạn thử +
  đếm token — chunker chưa chặn đoạn vượt (B-11) và giới hạn sát nhất là huydang 256 (255 hôm nay); snapshot đích cũ; chọn *tại chỗ* hay *đích mới
  rồi cutover* (cutover cần sửa hằng tên — B-06); build; kiểm; dọn có duyệt); heading `### Lịch sử (trước 7A2)` cho các đoạn cũ trong mục
  "Trạng thái hiện hành"; câu "payload năm field hiện hành" ⇒ "lúc đó"; #6a thêm nhãn hiện hành (từ chối tất-cả-hoặc-không, G5 dòng 2b);
  "Tài liệu hiện hành" thêm spec 7A2 / luna / 7A / 7B / 8.1 / 8.2 + build record, phần cũ dưới nhãn "Lịch sử (trước 10/2026)"; "đang active"
  của handoff 2026-10-01 ⇒ "lúc đó active"; bỏ tên collection Foods đã xóa khỏi bullet 7A2.
- **Guide 5 / 6 / 9 / `llm_rag_reference` (C-13):** guide 5 — ghi chú runtime hiện tại đầu "Full-corpus target hiện hành", "Reranker hiện hành
  MiniLM" ⇒ "tùy chọn trong code; runtime `none`", "Bước tiếp theo" gắn lịch sử; guide 6 — banner "handoff active" gắn "(Lịch sử)",
  `gpt-5.4-nano` ⇒ `gpt-6-luna` trong khối hiện hành, **bảng 7 mã lỗi** + dạng `/health` (đối chiếu `api/routes/chat.py`, `api/app.py`,
  `api/health.py`; ghi giới hạn B-01 / C-01), "Phase 8 vẫn đóng" gắn lịch sử; guide 9 — khối "Hiện hành" model (luna, judge Claude, không so model
  sinh ở Phase 8), lifecycle 2026-10-01 gắn lịch sử; `llm_rag_reference` — một dòng đầu "câu về trạng thái Hue là snapshot 08–09/2026",
  extraction "in progress" ⇒ "User-closed 2026-09-11", prefix `hue_rag_live_test_` và 3 profile gắn lịch sử.
- **B-19:** 48 lần `/home/minhhieu/llm_rag` trong 7 guide ⇒ `<repo tham khảo>` (giữ phần đường dẫn tương đối trong repo đó); đầu
  `llm_rag_reference` giải nghĩa `<repo tham khảo>`; danh sách gốc (file:dòng) lưu `data/ra_soat_code/b19_duong_dan_ngoai.md`.
- **Notebook 03 (B-21):** bỏ 2 import thừa (`json`, `QWEN_QUERY_TASK`); sửa câu sai "E5-base, HuyDang … đã bỏ khỏi code" ⇒ "không còn là dense
  candidate nhưng vẫn là tokenizer chunker kiểm giới hạn"; ô "Trạng thái hiện hành" trỏ mục build lại.
- **Notebook 04 (B-21):** cell code 5 việc ⇒ 3 cell code, mỗi cell có Markdown ngắn trước: (1) chia lại corpus + so build record (in kết quả,
  không `raise` — không đóng vai validator), (2) `verify_full_corpus_collection` (bỏ lời gọi `validate_full_corpus_collection_info` thừa vì
  hàm sau đã gọi, `upsert.py:86`; timeout dùng `QDRANT_TIMEOUT` thay `30`), (3) in hình dạng payload 2 point; intro sửa cho đúng (notebook chia lại
  corpus, cần 3 tokenizer, ~20 s); heading đặt sai chỗ được thay. Luật chọn mẫu vẫn chép trong notebook (đưa thành hàm pipeline là sửa code —
  đợt 3).
- **Notebook 06 (C-14):** tìm gốc repo theo `backend/config/settings.yaml` thay vì tên thư mục `hue_rag` (clone tên `chatbot-hue` chạy tới `/`);
  bỏ câu "ô gọi `/api/chat` tốn phí" (không có ô đó) ⇒ "notebook không gọi `/api/chat` thật"; Representation B ghi đúng "có trong code, runtime
  không dùng — chỉ runner smoke Phase 6 gọi" (`grep generate_search_context`: chỉ `llm/phase6_live_smoke.py:351`).

## 3. Cách đã chạy thật

- Đếm đường dẫn / tên chết + đường dẫn home tới repo khác: `uv run python -I data/ra_soat_code/tools/deadrefs.py [--src <thư mục>] [--list]`.
  **Quy tắc (ghi trước khi đếm "sau"):** đếm chuỗi giống file có đuôi (`.py .md .ipynb .json .jsonl .yaml .yml .txt .js .html .css .toml`) hoặc thư
  mục kết thúc `/` dưới các thư mục gốc repo / `backend`, tên file trong backtick, tên collection `hue_*` trong backtick; "chết" = không có trong
  working tree (kể cả `data/` private). Vùng đếm: file có banner `> **Guide lịch sử**` ⇒ chỉ banner + `## Hiện hành`; file khác ⇒ bỏ vùng có nhãn
  máy đọc được (`## …lịch sử/history…` tới `## …hiện hành…` kế tiếp; `### …lịch sử…` tới heading cấp ≤ 3). In cả số **toàn file** để không che.
  "Trước" = `git archive HEAD guides notebooks` (`5d3376f`) với **cùng** quy tắc.
- Notebook Run All trên bản tạm: `HF_HUB_OFFLINE=1 uv run jupyter nbconvert --to notebook --execute notebooks/<nb>.ipynb --output-dir /tmp/b26/run`
  (kernel `.venv/share/jupyter/kernels/python3`; **không** `--env-file` ⇒ không key, không thể gọi paid; Qdrant `:6335` chỉ đọc). File trong repo
  không bị ghi output.
- Đối chiếu từng khẳng định mới với code / CLI: `--help` của `evaluation.full_corpus_eval`; đọc `ingestion/full_corpus_pipeline.py` (CLI, tên
  collection, không ghi đè, sparse state), `ingestion/source_state.py:197-212` (record `FileExistsError`), `api/routes/chat.py`, `api/app.py`,
  `api/health.py`, `core/settings_loader.py:36-37`, `grep` Representation B / Qwen3-0.6B.
- `git diff --check -- guides notebooks`; quét dòng thêm mới theo mẫu của `.githooks/pre-commit` (tên dự án khác, secret) + `/home/<user>/`.

## 4. Kết quả quan sát

| Đếm (`deadrefs.py`, cùng quy tắc) | Trước (`5d3376f`) | Sau |
|---|---:|---:|
| Đường dẫn / tên chết **ngoài vùng lịch sử** — tổng | 34 | **1** |
| — phase_0 / 1 / 3 | 3 / 4 / 1 | 0 / 0 / 0 |
| — phase_7 / 8 | 12 / 11 | 0 / 0 |
| — `full_corpus_rag.md` | 2 | 0 |
| — phase_9 | 1 | 1 (`backend/agentic/` — thư mục **dự kiến** của roadmap, không phải tham chiếu chết) |
| Toàn file (gồm vùng lịch sử, không xóa) | 115 | 114 |
| Đường dẫn `/home/<user>/<repo khác>` trong `guides/` | 48 | **0** |

- Số "trước" của phase_2 / 4 / 5 / 6 là 0 ngay từ đầu theo quy tắc vùng vì các guide đó đã có heading chứa "history" / "lịch sử" (nhãn yếu mà
  B-16 nêu — heading rỗng, mục con cùng cấp); nay có banner rõ. Số của C ở mục việc (phase_1 4, phase_2 4, phase_3 10, phase_4 5) đếm theo cách
  khác (không trừ vùng lịch sử, chỉ đường dẫn) — không so trực tiếp; số toàn file của B ở bảng trên.
- **Notebook Run All (bản tạm) — 3 / 3 chạy hết, 0 lỗi:** 03 — 2 spec dense, prep doc / query, dot product thưa = BM25 `3.75641` (assert đạt);
  04 — `e5-small-384 | chunk: 8459 | khớp build record: True []`, 8B "chưa có build record, bỏ qua", `verify_full_corpus_collection` ⇒
  `{'point_count': 8459, 'payloads_verified': 8459, 'sample_vectors_verified': 5}`, payload 7 field; 06 — `Generation Model: gpt-6-luna`,
  `/health` 200 `degraded` (generator `not_ready` vì không key — đúng dự kiến), `ChatResponse` mẫu. File repo: mọi code cell `outputs == []`,
  `execution_count is None` (kiểm bằng script).
- `git diff --check`: sạch. Quét mẫu hook + `/home/<user>/`: 0 dòng thêm mới vi phạm.

## 5. Lỗi và giới hạn

- **Lệnh (B-17 để sau 1b):** mục build lại mới có lệnh `uv run python -m backend.ingestion.full_corpus_pipeline build --candidate e5-small-384`
  (chạy được hôm nay từ gốc repo, ghi "có thể đổi sau 1b"); notebook 03 ô cuối vẫn lệnh cũ thiếu `uv run` (không sửa — thuộc B-17).
- Guide 5 / 6 không có banner (mục việc chỉ giao dòng lệch C-13); phần Foods của chúng vẫn chứa 30 / 10 đường dẫn chết nằm dưới heading lịch sử
  sẵn có. Nếu muốn đồng bộ kiểu guide 7 / 8 thì là việc nhỏ tiếp theo (A quyết).
- Notebook 04 vẫn chép luật chọn mẫu của pipeline (cần một hàm trong `full_corpus_pipeline.py` — sửa code, đợt 3).
- Notebook 06 tìm gốc theo file: B chưa chạy thử trong một clone tên khác (logic đọc thẳng; Run All trong repo này đạt).
- Bảng mã lỗi guide 6 là hành vi thiết kế đối chiếu code; ba trường hợp lệch do B-01 / C-01 ghi ngay dưới bảng — khi gói 1b xong cần sửa lại câu đó.
- Mục "Build lại index" tả code tại `5d3376f`; chưa có lần build lại thật nào theo mục này (lần build lại tới cần ghi chỗ lệch).

## 6. Bàn giao cho người kiểm (C)

- Đọc trước: `git diff -- guides notebooks`; trọng tâm rủi ro: (1) mục "Build lại index khi corpus đổi" (`full_corpus_rag.md`) — từng câu về hành
  vi code; (2) mục "Hiện hành" guide 7 / 8 / 9 và bảng mã lỗi guide 6 — đúng với `Project_Status.md` / code; (3) notebook 04 (cell mới).
- Chạy lại (free): tự viết bộ đếm của C hoặc đọc `data/ra_soat_code/tools/deadrefs.py`; Run All 3 notebook trên bản tạm (không `--env-file`).
- Không có lệch đã duyệt ngoài mục việc.

## 7. Sửa sau review C (`sua_4_review.md`, 2026-10-25 20:2x)

- **m1 — đồng ý, đã sửa:** gạch "Không ghi đè" của mục build lại ghi đúng chỗ chặn: bước kiểm đích ngay đầu build (`inspect_full_corpus_target` /
  `require_fresh_full_corpus_target`, `vectorstore/qdrant.py:104-105`) dừng khi collection hoặc build record đã có, trước khi nạp model / ghi
  Qdrant; `FileExistsError` chỉ là lớp chặn cuối.
- **m2 — đồng ý, đã sửa:** bước 4(a) thêm "trước khi chạy build, kiểm đủ cả ba (collection, build record, sparse state) đã xóa" và lý do
  (`build_candidate` ghi sparse state ở `full_corpus_pipeline.py:170` trước bước kiểm đích `:183`; C-21 để gói build lại).
- **m3 — phản biện bằng bằng chứng, giữ "H1" và ghi rõ hơn:** `phase_8_1_g3_plan.md` khối YAML `G3.H1_tokenizer_e5_only` —
  `changed_variable: chunker chỉ kiểm giới hạn e5-small 512 (bỏ e5-base 512, HuyDang 256)`; bảng G5 dòng 9 "H1 (bỏ e5-base + HuyDang 256): 8.398
  đoạn (−61), 0/32/0". Dòng plan `:109-110` C trích nói H2 / H3 **cần** bỏ giới hạn HuyDang **nên dựng trên chunker H1** — tức H1 chính là bước bỏ.
  Câu mới: "8.1 G3 H1 đã thử bỏ ràng buộc này — chỉ kiểm e5-small 512, bỏ e5-base và huydang; H2 / H3 dựng trên chunker H1".
- **m4 — A chọn làm:** guide 5 / 6 thêm banner `> **Guide lịch sử** … trừ mục "Hiện hành" ngay dưới` như guide 7 / 8; đổi heading "Full-corpus
  target hiện hành" / "Full-corpus package hiện hành" thành `## Hiện hành` (giữ tên cũ ở dòng nghiêng ngay dưới); banner cũ của guide 5 ("là nguồn
  contract hiện hành", 09/2026) gắn "(Lịch sử)"; guide 6 dòng "Superseded by: Full-corpus target hiện hành" ⇒ "mục Hiện hành"; bảng README dòng
  Phase 5 / 6 ⇒ "mục Hiện hành + lịch sử".
- Đếm lại (`deadrefs.py`): ngoài vùng lịch sử vẫn **1** (`backend/agentic/` roadmap); guide 5 / 6 nay có banner, vùng đếm chỉ banner + `## Hiện
  hành` ⇒ 0 ở cả hai (theo quy tắc chặt của C cũng hết 21 tham chiếu vì chúng nằm ngoài mục Hiện hành). `git diff --check` sạch.
