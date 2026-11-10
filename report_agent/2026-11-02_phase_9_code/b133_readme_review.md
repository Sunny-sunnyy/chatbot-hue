# Review: `README.md` gốc repo (A viết, chưa commit) — B133

Người kiểm: B (Claude Opus 5.5, `hue-rag-52`) · 09:26 03/11/2026 (`date`) · skill `risk-gated-agent-review`. Bản được kiểm: `README.md` 171 dòng, sha256 (12) **`5dd1c8a3abbd`** (B tính từ file).
0 USD: chỉ đọc code / report, probe nhẹ (`--help`, `--dry-run`, hook quét). Không build index, không ghi Qdrant, không sửa README. Nhãn: [Chạy] = đã chạy lệnh · [Code] = đọc code, chưa chạy.

**Kết luận: `changes_requested`** — 0 blocker · 3 major · 7 minor. Không lộ thông tin private.

## 1. Đã kiểm, đúng

- **Phiên bản [Chạy]:** Python 3.13 (`pyproject.toml` `>=3.13`, `.venv` 3.13.15); React 19.3.1, Vite 8.3.4, Tailwind 4.3.3 (`frontend/package.json` + `node_modules`); Node v24.19.0 trên máy (không có `engines`).
- **Qdrant:** `docker-compose.yml` service `qdrant`, `127.0.0.1:6335→6333`, `6336→6334`; `settings.yaml` `url: http://localhost:6335`.
- **Endpoint:** `/api/chat`, `/api/chat/stream`, `/health` (cổng ổn định B131 hôm nay). Thư mục §"Cấu trúc thư mục": cả 21 đường dẫn đều có.
- **Tìm kiếm [Code]:** `dense_bm25_rrf` = dense pool 30 ⇒ BM25 chấm lại 30 đoạn đó ⇒ RRF `rrf_k` 60 ⇒ 10 đoạn ngữ cảnh (`retrieval/full_corpus.py:402`, `:482-500`).
- **Tính năng [Code]:** câu từ chối đúng chữ `INSUFFICIENT_ANSWER`; khẩn cấp 113 / 114 / 115 / 112 (`llm/emergency.py:13`); H4c cho `travel/tickets/`, `travel/places/`, `festivals/` (`assistant.py:40`); số trích dẫn bấm được (`App.jsx:115-130` `data-cite` ⇒ focus nguồn); log không ghi chữ câu hỏi (mọi `logger.*` trong `api/`, `llm/`, `retrieval/` chỉ ghi chuỗi cố định / tên lớp lỗi).
- **Lệnh [Chạy]:** `uv sync --locked --dry-run` ⇒ "Would make no changes"; `python -m ingestion.full_corpus_pipeline build --help` ⇒ đúng `--candidate {e5-small-384,qwen3-embedding-8b-4096}`; `npm ci && npm run build` và `uvicorn api.app:app --port …` đã chạy thật sáng nay (B131).
- **Số đúng nguồn:** 12 / 158 từ chối nhầm; +0,82 / +0,70 trên 33 câu kín (28/10); ≈ 0,00025 USD / câu (01/11); chữ đầu 3,05 / 5,64 s (03/11, B131).
- **Lộ thông tin [Chạy]:** `grep -ciE 'm[e]kong'` = 0; `.githooks/overlap_scan.py README.md` ⇒ "0 trùng" (không câu nào trùng ≥ 40 ký tự với Golden / kho / câu kín). Không có đường dẫn private ngoài tên thư mục; không chép câu Golden.

## 2. Finding

### M-1 (major) — Bước 4 "lần đầu cần mạng để tải model e5": sai — build và API **không bao giờ tự tải model**
- **Vị trí:** README dòng 121 (+ dòng 130 `HF_HUB_OFFLINE=1`).
- **Bằng chứng [Code]:** dense e5 nạp bằng `resolve_snapshot(spec, allow_download=False)` (`embedding/full_corpus.py:379`, `snapshot_download(local_files_only=True)` ở `:117-121`), đúng revision `614241f622f5…` (`:45`). Chia đoạn nạp **3 tokenizer** `AutoTokenizer.from_pretrained(..., local_files_only=True)` (`ingestion/preview.py:53`, gọi từ `full_corpus_chunker.py:293`): `intfloat/multilingual-e5-small`, `intfloat/multilingual-e5-base`, `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (`settings.yaml` `embedding_models`).
- **Tác động:** người clone làm đúng README ⇒ build dừng vì thiếu model trong cache; không có câu nào nói phải tải trước 3 model.
- **Sửa thành:** thêm bước tải trước, vd `uv run python -c "from huggingface_hub import snapshot_download as d; d('intfloat/multilingual-e5-small', revision='614241f622f53c4eeff9890bdc4f31cfecc418b3'); d('intfloat/multilingual-e5-base'); d('CODE4LIFEOFFICIAL/huydang-dek21-embedding')"`
  (B **chưa chạy** lệnh này — tải ~2 GB; A chạy thử hoặc ghi "[chưa thử trên máy sạch]"). Bỏ chữ "lần đầu cần mạng…".

### M-2 (major) — Bước 4 thiếu file private bắt buộc khi build: `knowledge-base-hue/meta/full_corpus_conditions.json`
- **Vị trí:** README §"Dữ liệu" dòng 105-107 + bước 4.
- **Bằng chứng [Code]:** `ingestion/full_corpus_pipeline.py:97` gọi `load_settings()` (mặc định `validate_private_paths=True`) ⇒ `core/settings_loader.py:112-114` raise "conditions file does not exist" khi thiếu `conditions_file` (`settings.yaml` `../knowledge-base-hue/meta/full_corpus_conditions.json`). API thì không (`app.py:55` `validate_private_paths=False`).
- **Tác động:** câu "chỉ cần kho Markdown riêng (cấu trúc `<foods|…>/…`)" chưa đủ để build.
- **Sửa thành:** ghi thêm "và file điều kiện `knowledge-base-hue/meta/full_corpus_conditions.json`" (nói nó là gì ở mức chung, không chép nội dung), hoặc ghi rõ "build chỉ chạy được khi có kho private của dự án". Nên trỏ thêm `guides/full_corpus_rag.md` mục "Build lại index" (bẫy sparse state chỉ ghi một lần — `Project_Status.md` §8).

### M-3 (major) — Bảng "Kết quả đo": 2 dòng sai / lệch ngày so với nguồn mới nhất
1. **"Sai điều kiện / cảnh báo trên bộ an toàn 32 câu: 0 — 30/10/2026"** — lượt đo cuối **01/11** (số đang chạy): **0 đảo cảnh báo**, nhưng **2 câu sai điều kiện mới** (cả hai "nói sai về nguồn"; đúng ngưỡng ≤ 2; bản cũ sinh lại cũng sai 1 / 3 mỗi bên) — `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md:34-35`. Số 0 của 30/10 là lượt sửa kho, đã cũ.
   **Sửa thành:** "0 đảo cảnh báo; 2 câu sai điều kiện mới (đúng ngưỡng ≤ 2, bản trước cũng sai y vậy) — 01/11/2026". Ghi số xấu hơn ở README public là đúng luật "báo cáo đúng, không chọn số đẹp".
2. **"Lỗi trích dẫn 0 / 489 lần sinh — 01/11/2026"** — số 489 là phép đếm **C89** trong đợt phần tồn (`report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md:142`), `94_DE_XUAT_SUA_CODE.md:15` ghi "số 30/10". Không có nguồn nào đếm 489 ngày 01/11. Lượt đo cuối 01/11 ghi "0 lỗi trích dẫn" trên Golden 176 (`10_BAO_CAO_DANH_GIA.md:29`); hồi quy B1 02/11 cũng 0 / 208 (`b129_b1_implementation.md` P5).
   **Sửa thành (chọn một):** "0 / 489 lần sinh — đếm 30/10 trên mọi lượt đã lưu (cấu hình 10 đoạn)" **hoặc** "0 trên Golden 176 + 32 an toàn — 01/11 và 02/11/2026".

### m-1 — "Câu ngoài kho bị trả lời 0 — 30/10": ngày cũ
Lượt đo cuối 01/11: 0 Golden, 0 / 4 an toàn, 0 / 6 bộ kín 40 câu (`10_BAO_CAO_DANH_GIA.md:29, :34, :36`); B1 02/11: 18 / 18 câu `out_of_scope` từ chối. ⇒ ghi "01/11/2026 (và hồi quy B1 02/11)". Tương tự 12 / 158: số này giữ nguyên ở 01/11 và 02/11 ⇒ ghi 01/11.

### m-2 — "So với bản đầu Phase 8 trên 33 câu kín"
Phép so là **đầu ↔ cuối Phase 8.2**: ngữ cảnh 5 ⇒ 10 đoạn + chuẩn hoá NFC (`Project_Status.md` §3 dòng 8.2), không phải "bản đầu Phase 8". **Sửa:** "Ngữ cảnh 5 ⇒ 10 đoạn (Phase 8.2), 33 câu kín: đủ ý +0,82, đúng +0,70, 0 câu tụt".

### m-3 — "Tiền mỗi câu ≈ 0,00025 (chưa tính lần phân loại, ≈ +0,000075)"
Lần phân loại đo thật ≈ **0,00008** / câu (B131 03/11: 3 câu chỉ định tuyến 0,0000788–0,0000825; P1 r2 B1: 0,020796 / 253 = 0,000082). Cả câu tuyến hỏi Huế sau B1 đo được 0,00029–0,00037 USD (5 câu, B131, `data/phase_9/b131/first_text_server.jsonl`). **Sửa:** "≈ +0,00008 USD (02–03/11)"; có thể thêm "cả câu ≈ 0,0003–0,0004 USD (5 câu, 03/11)".

### m-4 — Chữ đầu 3,05 / 5,64 s: thiếu ngữ cảnh
Đúng số (10 câu), nhưng (a) đo bằng script gọi API, không phải trình duyệt như mốc 01/11 (p50 1,23 / p95 2,61 s, 38 câu); (b) **vượt** mục tiêu p50 ≤ 3 / p95 ≤ 5 s. **Sửa:** thêm "(script gọi API; trước khi thêm bước phân loại 1,23 / 2,61 s trên trình duyệt; vượt mục tiêu 3 / 5 s — đang theo dõi)".

### m-5 — Câu dẫn bảng "Đo trên bộ Golden 176 câu…"
Bảng có dòng đo trên bộ khác (an toàn 32, 33 câu kín, 10 câu tự viết). **Sửa:** "Đo chủ yếu trên Golden 176 câu (private); dòng nào dùng bộ khác thì ghi trong dòng đó."

### m-6 — Sơ đồ: "chuẩn hoá Unicode NFC → model phân loại câu hỏi"
NFC làm **trong tầng tìm** (`retrieval/full_corpus.py:420` `normalize_query`), không trước định tuyến (định tuyến nhận câu gốc). **Sửa:** dời "chuẩn hoá NFC" vào nhánh "hỏi về Huế ⇒ (NFC) tìm 30 ứng viên…".
Thêm cho chính xác: "Backend kiểm mọi trích dẫn **trước khi trả**" (dòng 18) đúng cho `/api/chat`; ở đường stream chữ hiện trước, trích dẫn hỏng thì **rút lại** (`chat.py` `StreamEvents.finish`) ⇒ nên ghi "kiểm mọi trích dẫn; trích dẫn hỏng thì rút câu trả lời".

### m-7 — Nhỏ, tuỳ A
- Bước 6 "Qdrant tắt hoặc thiếu model ⇒ 503": đúng cho Qdrant / e5; thiếu khoá OpenAI thì generator không sẵn sàng ⇒ 502 (`chat.py` `_ready_generator`). Câu "Kho đã sửa mà chưa dựng lại ⇒ **API từ chối chạy** (409)" sai chữ: API **vẫn khởi động**, chỉ `/api/chat` trả **409** `corpus_reingest_required` (`app.py:85-91`). Sửa: "API vẫn chạy nhưng mọi câu hỏi trả 409".
- Bước 4 `--env-file ../.env`: không cần cho e5 (chỉ ứng viên `qwen3-…` gọi OpenRouter); để cũng không hại.
- Cấu trúc thư mục: `backend/` còn `core/`, `experiments/`, `reranking/`, `vectorstore/`, `scripts/` chưa liệt kê (README nói "không rerank" mà có `reranking/` — người đọc dễ thắc mắc; ghi "reranking/ — thử nghiệm Phase 8, không dùng ở runtime"). Ngoài README: `backend/test.ipynb` (tracked, 1 ô `print("hi")`) là file thừa — A xét gỡ.
- Repo public chưa có `LICENSE` — README không nói điều khoản dùng lại; hỏi User nếu muốn ghi.

## 3. Giới hạn của review

- Không chạy build index, không tải model, không chạy trên máy sạch ⇒ M-1 / M-2 là [Code] (đọc đường gọi), chưa tái hiện trên clone mới.
- Không mở nội dung kho / Golden; số đo chỉ đối chiếu với report / `bao_cao_he_thong/`, không tính lại từ dữ liệu.
