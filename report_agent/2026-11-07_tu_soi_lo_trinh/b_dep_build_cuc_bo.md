# B-dep — thử build + chạy cục bộ bản deploy (13:03 07/11/2026, `date`)

Người làm: B. Việc A giao, chưa đụng AWS. Tiền: **0,00107 USD** (2 câu cổng). Nhãn: **[Chạy]** = chạy thật · **[Suy]** = suy luận.
Chạy sau khi E xong ca dò, trước X1c của C — không chồng việc nặng. Qdrant chatbot (6335) không bị đụng.

## 1. Đã làm

- **M2 — nhánh `p12-deploy-nhap` `50e4ebf`** (từ `main` `0324548`, đã push, chưa merge):
  - `core/settings_loader.py` thêm `apply_env_overrides`: `HUE_QDRANT_URL` ⇒ `vector_database.url`; `HUE_TRA_WEB=true|false` ⇒ `assistant.tra_web`; giá trị lạ ⇒ báo lỗi.
  - Test `tests/test_settings_env.py`: không đặt biến ⇒ settings y hệt file. [Chạy] đạt; test hỏng duy nhất trong cùng lượt là test cần khoá OpenAI, như `main`.
- **Bản nháp `data/phase_12/deploy_nhap/` (B nhận từ E):**
  - M1: `COPY` riêng `diem_v3.json`.
  - `Dockerfile.dockerignore` mới cạnh Dockerfile: mặc định loại hết, chỉ mở thứ ảnh cần.
  - Stage `code`: thay được bằng `--build-context code=<backend nhánh>`.
  - Bước xoá `trees/` (lỗi mới ở mục 2).
  - M2: compose bỏ `network_mode`, app gọi `http://qdrant:6333`, đặt `HUE_TRA_WEB: "false"`.
  - M3: healthcheck Qdrant bằng bash + `depends_on: service_healthy`.
  - Log app mount ra ngoài.
  - Caddy đọc `{$HUE_SITE}`; không nén `/api/chat/stream`.

## 2. Chạy thật từng bước [Chạy]

| Bước | Kết quả |
|---|---|
| `docker build` từ working tree chính, `--build-context code=/tmp/b_dep/backend`, `timeout 1800` | **209 s** lần 1 (xuất ảnh 144 s là bước lâu nhất); 40 s lần 2 (dùng cache) |
| Cỡ ảnh | **1,44 GB** nén (cỡ `docker save` / chuyển máy). `docker images` báo 6,13 GB — số đếm của Docker Desktop [Suy: tính cả bản giải nén]. Bên trong: `.venv` 1,9 GB (torch 711 MB, polars 206 MB, pyarrow 152 MB, gradio 77 MB) + model 471 MB + kho 6,7 MB |
| torch | `2.13.0+cpu`, `torch.version.cuda` = None ⇒ cách lọc gói CUDA + `--torch-backend cpu` chạy đúng |
| Dữ liệu private trong ảnh | **SAI — đã rút lại:** B ghi "0 file `evaluation/`" vì lệnh kiểm `find … \| head -3` chỉ in 3 dòng đầu (đều của thư viện). E review (`e_review_b_dep.md` M-1) đếm đủ: ảnh có **16 file trong các thư mục `evaluation/` lồng trong từng lĩnh vực** (Golden authoring…) + **148 file `meta/`** (gồm sao lưu Golden). Lý do: `.dockerignore` `knowledge-base-hue/evaluation` chỉ khớp thư mục ở gốc kho. Ảnh chỉ ở máy User, chưa chuyển đi đâu. Sửa + đếm lại: mục 4 |
| **Lỗi 1 — `/health`: retrieval `not_ready`** | Gốc: `IncompleteSnapshotError` của `huggingface_hub` 1.26. Thư viện lưu danh sách file repo (`trees/<rev>.json`); chỉ tải một phần ⇒ runtime (`snapshot_download(local_files_only=True)`) báo thiếu 30 file ⇒ 503. **Sửa:** xoá `trees/` sau khi tải (có danh sách thì kiểm, không có thì bỏ qua — đọc code thư viện). Thử trong container trước: tìm ra 10 đoạn. Rồi build lại |
| `compose up` (`-p hue_deploy_thu`, Caddy 8880) | Qdrant healthy ⇒ app khởi động sau; `/health` **5 / 5** sau ~23 s |
| Qua Caddy | `/` 200 + CSP còn nguyên. Câu trong kho (stream): success, có `sources`. Câu ngoài kho: câu từ chối chuẩn. 2 dòng `chat_metrics`, 0 chữ câu hỏi trong log |
| SSE qua Caddy | 236 sự kiện `delta` rải từ giây 9,6 tới 11,4 ⇒ **chữ hiện dần**, không bị gom; không có `content-encoding` trên luồng. File JS được gzip |
| RAM (`docker stats`) | app **966 MiB** · Qdrant 320 MiB · Caddy 13 MiB. RSS 1,49 GB E đo trên máy chủ — khác cách đếm |
| Dọn | `compose down -v`: 0 container còn lại; xoá `/tmp/b_dep_run` (bản chép Qdrant + log). **Giữ ảnh** `hue-rag-app:nhap` |

Xoá ảnh khi không cần: `! docker rmi hue-rag-app:nhap && docker builder prune -f`.

## 3. Còn rủi ro khi lên AWS

- **Chữ đầu tiên 9,5 s** (`first_text_ms`) ở câu đầu sau khởi động. Trên máy User cùng loại câu: p50 1,2 s. Chỉ 1 câu ⇒ chưa biết do khởi động lạnh, CPU Docker Desktop hay mạng [Suy]. ⇒ 10 câu đo trên máy thật như E §5.
- **Cookie `Secure`, tắt `/docs`, giới hạn lượt / ngày** (E §4 #1, #5, #6) chưa làm: bắt buộc trước khi gửi link công khai.
- Ảnh khá nặng vì `jupyter` / `gradio` / `pytest` / `polars` nằm trong deps chính. Chạy được; dọn sau (đụng `uv lock`).
- HTTPS + sslip.io chưa thử (cục bộ chỉ http).
- Chép `qdrant_storage` lên máy: chép khi Qdrant nguồn không ghi, hoặc dùng snapshot.

**Giải thích ngắn:** đã đóng được app thành ảnh Docker chạy Qdrant + app + Caddy trên máy User, trả lời được và chữ vẫn hiện dần qua Caddy. Lỗi duy nhất gặp là thư viện tải model báo thiếu file; đã sửa trong Dockerfile. Còn phải làm giới hạn lượt / cookie trước khi đưa link công khai.

## 4. Sửa M-1 (review E) + đếm lại trong ảnh [Chạy] (13:25 07/11/2026 `date`)

- **Sửa:** `Dockerfile.dockerignore` nay kiểu **danh sách chừa**, sinh bằng `data/phase_12/deploy_nhap/dung_dockerignore.py` từ build record. Chỉ chừa:
  - 204 bài trong `corpus.sources`;
  - `knowledge-base-hue/meta/full_corpus_conditions.json`;
  - 2 file `data/full_corpus_builds/`;
  - `data/phase_9/lich_trinh/diem_v3.json`;
  - `backend/`, `frontend/`, `pyproject.toml`, `uv.lock`.
  - Build record đổi ⇒ chạy lại script.
- Thêm 5 minor của E vào `compose.yml`: log `json-file` 10 MB × 3; ghi chú mở cổng 443 + `systemctl enable --now docker`; `image: ${HUE_IMAGE:-…}`. Chú thích cổng 6333 trong `settings_loader.py` ở `23454f3`.
- **Build lại** ảnh `hue-rag-app:nhap2` (lớp nặng dùng lại cache); 1,44 GB nén.
- **Đếm** — `docker run --rm --network none --entrypoint bash hue-rag-app:nhap2 -c 'find …'` (bỏ qua `/app/.venv`):

| Mục | Số |
|---|---|
| `.md` của kho | **204** |
| file kho mọi loại | 205 (204 + `meta/full_corpus_conditions.json`) |
| `*sealed*` · `*backup*` · `_source-dumps` | **0 · 0 · 0** |
| đường dẫn có "evaluation" / "golden" | 5 / 2 — **đều là mã** `backend/evaluation/` (gói đánh giá, đã ở repo công khai) + `tests/test_golden_full_corpus.py`; không file dữ liệu Golden nào |
| `backend/` trong ảnh so với `git ls-files backend` | 102 = 102, khớp |
| `data/` trong ảnh | đúng 3 file đã chừa |

- **Chạy:** `compose up` với `HUE_IMAGE=hue-rag-app:nhap2` ⇒ `/health` **5 / 5** sau ~23 s (kho khớp build record ⇒ đủ đúng 204 file). Đã `down -v` + xoá thư mục chạy thử.
  - `/api/tinh_nang` 404 vì nhánh `p12-deploy-nhap` tách từ `main` trước khi merge cổng đợt 1 — merge `main` vào nhánh trước khi lên máy.
- **Ảnh cũ** `hue-rag-app:nhap` (có 16 file `evaluation/` + 148 file `meta/`) còn trên máy User, chưa chuyển đi đâu. User xoá: `! docker image rm hue-rag-app:nhap` (giữ `nhap2`, hoặc xoá cả hai: `! docker image rm hue-rag-app:nhap hue-rag-app:nhap2 && docker builder prune -f`).

## 5. Sau review vòng 2 của E (ready)

- m-6: ảnh còn cache uv `/root/.cache` ~1,9 GB, trùng `.venv` (E đếm). Số "nội dung ~2,4 GB" ở §2 của B **bỏ sót** phần này; 1,44 GB nén cũng đã gồm nó.
- Sửa nháp: `uv pip install --no-cache`. **Chưa build lại** (A: build lúc lên máy) ⇒ đo lại cỡ ảnh khi đó.
- Nhánh `p12-deploy-nhap` = `4cfe681` (merge `main` `fb8d3d2`); `test_settings_env` + `test_cong_dot_1`: 26 đạt. Nhánh giữ riêng, chưa merge.
