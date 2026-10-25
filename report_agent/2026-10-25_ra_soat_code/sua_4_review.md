# Review: rà code — gói 4 (tài liệu: guide + notebook) — B26

Decision: **ready_for_user_confirmation** — tiêu chí đạt; không blocker / major. 4 điểm `minor` (m1–m4), nên sửa m1–m3 trước khi A commit
(sửa chữ, không cần vòng review riêng — C xem lại diff phần đó). Thêm 1 phát hiện **ngoài phạm vi** về code (o1) cho A xếp gói.
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-7f`)
Date: 2026-10-25 20:16 (`date`)
Canonical: mục B26 trong `session_prompt/CURRENT_HANDOFF.md`; `bao_cao_he_thong/DE_XUAT_SUA_CODE.md` gói 4
Implementation report: `report_agent/2026-10-25_ra_soat_code/sua_4_implementation.md` (B, 20:04)

## 1. Phạm vi đã review

- Git: `main` `63fec4f` + working tree; 16 file đổi đúng danh sách report (13 guide + notebook 03 / 04 / 06), `git diff --stat` 382+ / 423−. Các file
  khác đang đổi (`CURRENT_HANDOFF.md`, `STATUS_A/B`) không thuộc gói. Không đọc `STATUS_B`, không chạy script của B (`data/ra_soat_code/tools/*`).
- Đọc diff trọng tâm theo §6 của B: mục "Build lại index khi corpus đổi" (`full_corpus_rag.md:140-185`), "Hiện hành" guide 7 / 8 / 9, bảng mã lỗi
  guide 6 (`:55-71`), notebook 04 (cell mới), notebook 06 (tìm gốc repo); lướt banner guide 0–4, `README.md`, guide 5, `llm_rag_reference`.
- Code đối chiếu: `ingestion/full_corpus_pipeline.py:60-100, 137-270`, `vectorstore/qdrant.py:93-150`, `ingestion/source_state.py:197-213`,
  `api/routes/chat.py`, `api/app.py:150-180`, `api/health.py`; plan 8.1 G3 `phase_8_1_g3_plan.md:109-110`.

## 2. Findings

### m1 (minor) — "build record đã có ⇒ `FileExistsError`" mô tả chỗ chặn muộn, không phải chỗ chặn thật
- Vị trí: `guides/full_corpus_rag.md`, mục build lại, gạch "Không ghi đè".
- Bằng chứng: build record có sẵn bị chặn **ngay đầu** build — `inspect_full_corpus_target` ghi `build_record_exists` (`vectorstore/qdrant.py:112-132`),
  `classify_full_corpus_target` thêm blocker "final build record already exists" (`:104-105`), `require_fresh_full_corpus_target` raise
  `QdrantSchemaError` (`:138-139`) — trước khi nạp model / ghi gì vào Qdrant (`full_corpus_pipeline.py:183-187`). `FileExistsError`
  (`source_state.py:200-201`) chỉ là lớp chặn cuối khi ghi record.
- Tiêu chí đóng: câu ghi đúng "record đã có ⇒ build dừng ngay từ đầu (blocker của bước kiểm đích)".

### m2 (minor, an toàn thao tác) — thiếu cảnh báo: build ghi sparse state **trước** khi kiểm đích
- Vị trí: mục build lại, bước 4(a) / 5.
- Bằng chứng: `build_candidate` gọi `_write_or_check_sparse_state` (`full_corpus_pipeline.py:170`) trước `inspect_full_corpus_target` /
  `require_fresh_full_corpus_target` (`:183-187`). Nếu sparse state chung **đã xóa** mà collection hoặc build record **còn** (xóa thiếu), build ghi
  sparse state mới rồi mới dừng ⇒ file mới khác sha trong record cũ ⇒ runtime từ chối khởi động (`retrieval/full_corpus.py:785-788`). Theo đúng
  bước 4(a) (xóa đủ ba) thì không sao — rủi ro chỉ khi làm thiếu.
- Tiêu chí đóng: bước 4(a) / 5 thêm một câu "trước khi chạy build, kiểm cả ba (collection, build record, sparse state) đều đã xóa — build ghi
  sparse state trước khi kiểm collection". Sửa thứ tự trong code là o1, không thuộc gói tài liệu.

### m3 (minor) — "8.1 G3 H1 đã thử bỏ ràng buộc này" — thực ra là H2 / H3
- Vị trí: mục build lại, bước 2.
- Bằng chứng: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_plan.md:109-110` — "H3 và H2 **cần** bỏ giới hạn HuyDang 256 … dựng trên
  chunker H1"; H1 không bỏ giới hạn này.
- Tiêu chí đóng: đổi thành "8.1 G3 H2 / H3 đã thử bỏ ràng buộc này (dựng trên chunker H1)".

### m4 (minor, ghi nhận) — tiêu chí "0 ngoài vùng lịch sử" phụ thuộc quy tắc vùng; guide 5 / 6 vẫn là nhãn yếu
- Bằng chứng: script độc lập của C (`data/ra_soat_code_2026-10-25/tools/review_4/deadrefs_zone.py`, quy tắc **chặt hơn** của B: vùng lịch sử
  kết thúc ở heading cùng cấp kế tiếp) — sau sửa còn **21** tham chiếu chết ngoài vùng ở guide 5 (14, các mục `## Dependency đã đạt`,
  `## Files được phép tạo hoặc sửa`, `## Notebook bắt buộc`) và guide 6 (7, `## Files dự kiến`, `### Files trong scope`) — các mục cùng cấp
  sau heading lịch sử duy nhất (`phase_5…:69`, `phase_6…:81`). Theo quy tắc B ghi trước (lịch sử kéo tới `## …hiện hành…` kế tiếp) thì 0. B đã
  nêu đúng điểm này ở §5 của report. Các file khác: theo quy tắc của C cũng **0** (trừ báo nhầm `hue_rag` / `hue_rag_live_test_` là tên dự án /
  tiền tố, không phải collection).
- Đề xuất (A quyết, không chặn): banner `> **Guide lịch sử** …` cho guide 5 / 6 như guide 7 / 8 — việc nhỏ, làm cùng lúc này hoặc sau.

### o1 (ngoài phạm vi — code, cho A xếp gói) — `build_candidate` có tác dụng phụ trước khi kiểm điều kiện
- Như m2: ghi sparse state chung (`full_corpus_pipeline.py:170`) trước khi kiểm đích sạch (`:183-187`). Sửa nhỏ nhất: chuyển dòng 170 xuống sau
  `require_fresh_full_corpus_target`. Hợp với gói 2 / đợt 3 (cùng lần sửa chunker / build). Mã đề xuất: **C-21**.

## 3. Cách người kiểm chạy lại thật

- Đếm: `python3 -I /tmp/c36/deadrefs_zone.py before|after` (before = `git show HEAD:<guide>`; after = working tree; collection so với
  `GET :6335/collections`). Đường dẫn home: `grep -rhoP "/home/[^/\s\`]+/(?!hue_rag)[^/\s\`)]+" guides/` (sau) và `git grep … HEAD -- guides/` (trước).
- Notebook: `HF_HUB_OFFLINE=1 uv run jupyter nbconvert --to notebook --execute notebooks/<nb>.ipynb --output-dir /tmp/c36/run` cho 03 / 04 / 06,
  **không** `--env-file`; md5 3 file repo trước / sau. Notebook 06 chạy thêm trong cây tạm `/tmp/c36/clone/chatbot-hue/` (symlink `backend`,
  `knowledge-base-hue`, `data`, `frontend` tới repo; copy notebook) để kiểm tìm gốc khi thư mục không tên `hue_rag`.
- Quét dòng thêm mới (`git diff -U0 -- guides notebooks`) theo đúng mẫu `.githooks/pre-commit` (tên dự án khác, secret) + `/home/`; `git diff --check`.
- Đối chiếu code bằng Read / `grep` như ghi ở mục 1.

## 4. Kết quả quan sát

| Tiêu chí | Kết quả của C |
|---|---|
| Đường dẫn chết ngoài vùng lịch sử (B: 34 → 1) | quy tắc của C: guide 0–4, 7, 8, `full_corpus_rag`: **→ 0** (trước: phase_1 4, phase_2 4, phase_4 8, phase_7 2, phase_8 7, phase_0 / 3 / `full_corpus_rag` 1 mỗi file). Guide 5 / 6: 21 (m4). Số tổng không so với B vì quy tắc khác (B ghi rõ) |
| Đường dẫn `/home/<user>/<repo khác>` trong `guides/` | 48 → **0** (khớp B) |
| Notebook Run All (bản tạm, không key) | 03: 3 cell, 0 lỗi (2 spec dense, BM25 `3.75641` = tham chiếu); 04: 4 cell, 0 lỗi (8.459 đoạn, khớp build record True, `point_count` / `payloads_verified` 8.459, 5 vector mẫu, payload 7 field); 06: 3 cell, 0 lỗi (`/health` 200 `degraded`, generator `not_ready` vì không key — đúng). File repo: outputs rỗng, `execution_count` None, md5 không đổi |
| Notebook 06 trong thư mục tên `chatbot-hue` | 0 lỗi — tìm gốc theo `backend/config/settings.yaml` chạy đúng (B ghi chưa thử) |
| Mục build lại ↔ code | đúng: CLI chỉ `build --candidate` 2 lựa chọn (`:264-268`); tên collection cố định `_COLLECTION_BY_CANDIDATE` (`:66-72`), runtime dùng cùng bảng + `SPARSE_STATE_PATH` (`retrieval/full_corpus.py:49-50`); đích phải `absent` (`:186-187`); sparse state khác byte ⇒ "Existing sparse state differs" (`:140-143`); hash nguồn kiểm lại sau encode (`:197-199`); kiểm sau upsert số point / payload / vector mẫu đoạn đầu mỗi domain (`:171-175, 211-214`); `build_candidate(collection_name=, sparse_state_path=, record_path=)` (`:149-154`). Lệch nhỏ: m1, m2, m3 |
| Bảng 7 mã lỗi guide 6 ↔ code | đúng: 422 `invalid_request` (`chat.py:52` + handler `app.py:153-163`), 409 / 503 lúc khởi động qua `app.state.retrieval_error_*` (`app.py:70-90`) và lúc hỏi (`chat.py:72-89`), 502 `generation_unavailable` (`chat.py:113, 125`), 500 `context_budget_error` (`:96`), 500 `citation_integrity_error` (`:141`), 500 `internal_error` (`app.py:166-175`). Ghi chú giới hạn B-01 / C-01 dưới bảng đúng. `/health` đúng dạng (`health.py:15-24`; `qdrant` suy từ `retrieval_ready`) |
| "Hiện hành" guide 7 / 8 / 9 | khớp `Project_Status.md` §2–§5 và việc đã đóng (7A / 7B / 8.1, 8.2 tạm dừng, B1 ở `p82-b1`, giữ luna, dense e5 + 8B chưa index, định nghĩa lỗi citation đổi từ 1a) |
| Quét dòng thêm mới | 0 tên dự án khác, 0 secret, 0 `/home/`; `git diff --check` sạch |

## 5. Giới hạn hoặc phần chưa chạy

- Không đọc từng dòng phần banner / lịch sử của mọi guide (chỉ lướt guide 0–4, `README.md`, guide 5, `llm_rag_reference`); trọng tâm theo rủi ro
  B nêu. Không chạy lệnh build (ghi Qdrant). Quy tắc vùng của C và B khác nhau ⇒ số tổng không so trực tiếp (đã ghi ở m4).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** (việc rủi ro trung bình ⇒ A đóng, báo User). Trước khi A commit: B sửa **m1, m2, m3** (3 câu trong mục build lại
của `full_corpus_rag.md`); C xem lại đúng 3 câu đó. **m4**: A quyết có thêm banner guide 5 / 6 không. **o1 / C-21**: A xếp vào gói 2 / đợt 3.

## 7. Kiểm lại sau sửa (C, 2026-10-25 20:27)

**Đóng — ready_for_user_confirmation.** m1, m2 sửa đúng (`full_corpus_rag.md:150-152`, `:168-170`); m4 xong (guide 5 / 6 có banner + `## Hiện hành`;
script của C: ngoài vùng lịch sử còn 3 = báo nhầm `hue_rag` / `hue_rag_live_test_`, tức **0** tham chiếu chết thật); **m3: C sai, B đúng** — H1 của
G3 chính là bước bỏ e5-base + huydang (`phase_8_1_g3_plan.md` khối `G3.H1_tokenizer_e5_only`; C đọc nhầm `:109-110`); câu mới của B (`:164`) đúng.
`git diff --check` sạch.
