# Implementation Report: Phase 7A2 Gate 3 — Xóa 13 collection cũ + build record cũ

Người làm: B (Claude Opus 5.5, terminal `hue-rag-c0`)
Date: 2026-10-24
Canonical inputs:

```text
docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md §6 (bản sửa 2026-10-24)
docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md Task 9
session_prompt/CURRENT_HANDOFF.md, mục "Việc của B" (base b781af8)
```

## 1. Phạm vi

Làm plan Task 9, có điều chỉnh vì 8B hoãn sang Phase 8: xóa đúng 13 collection
trong spec §6.1, xóa 8 build record cũ và `phase_3_sparse_state.json`, rồi kiểm
trạng thái sau và health runtime. Không đổi code. Không tạo hay sửa collection.
Không động vào `knowledge-base-hue/`. Không gọi paid. Không commit.

Trước khi xóa, B xin User xác nhận một dòng trong terminal B; User đồng ý.

## 2. Thay đổi chính

| Đối tượng | Thay đổi |
|---|---|
| Qdrant `127.0.0.1:6335` | Xóa 13 collection: 8 `hue_full_corpus_a_*` (4 legacy + 4 metadata v2), 3 `hue_foods_08a_*`, 2 `hue_rag_phase8_08b_tfidf_v1_unicode_word_*` |
| `data/full_corpus_builds/` (private) | Xóa 8 `hue_full_corpus_a_*.json` và `phase_3_sparse_state.json` |
| Repo | Chỉ thêm report này; cập nhật hàng/mục B trong `CURRENT_HANDOFF.md` và `sessions/STATUS_B.md` |

## 3. Cách đã chạy thật

```bash
# Bước 1: trạng thái trước (GET /collections và /collections/<name>, ls thư mục build)
# Bước 2: plan Task 9 Step 2, từng tên một
for name in <13 tên spec §6.1>; do curl -s -X DELETE "http://127.0.0.1:6335/collections/$name"; echo " $name"; done
# Bước 3: rm 9 file. User chạy bằng `!` trong terminal B, vì auto-mode permission của B chặn `rm`
cd data/full_corpus_builds && rm -v hue_full_corpus_a_*.json(8 tên cụ thể) phase_3_sparse_state.json
# Bước 4: health
cd backend && uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8018
curl -s http://127.0.0.1:8018/health
# Server dừng bằng `kill 321261 321255`. User chạy bằng `!`, vì permission của B chặn `kill`
# Health lần 2, sau khi xóa file: in-process (create_app + lifespan + ASGITransport GET /health)
```

## 4. Kết quả quan sát

### 4.1 Trạng thái trước

16 collection, khớp đúng danh sách kỳ vọng của handoff (`matches_expected True`):

| Collection | Point | Status | Xử lý |
|---|---:|---|---|
| `hue_full_corpus_a_{e5_small_384,e5_base_768,huydang_dek21_768,qwen3_06b_1024}` và 4 bản `_metadata_v2` | 8.460 mỗi collection | green | xóa |
| `hue_foods_08a_{e5_small_384,e5_base_768,huydang_dek21_768}` | 572 mỗi collection | green | xóa |
| `hue_rag_phase8_08b_tfidf_v1_unicode_word_{49c5d03359f9,5297c8604335}` | 572 mỗi collection | green | xóa |
| `hue_foods_e5_small_384` | 572 | green | giữ |
| `hue_foods_e5_small_384_dense` | 572 | green | giữ |
| `hue_full_corpus_7a2_e5_small_384` | 8.459 | green | giữ |

`data/full_corpus_builds/`: 11 file, gồm 8 `hue_full_corpus_a_*.json`,
`phase_3_sparse_state.json`, `hue_full_corpus_7a2_e5_small_384.json` và
`full_corpus_sparse_state.json`.

### 4.2 Xóa

- 13 lệnh `DELETE` đều trả `{"result":true,"status":"ok"}`, thời gian 0,007–0,066 s.
- `rm -v` báo `removed` cho đủ 9 file (User chạy trong terminal B).

### 4.3 Trạng thái sau (acceptance spec §6.3)

| Kiểm | Kết quả |
|---|---|
| Qdrant còn đúng 3 collection | **Đạt**: `hue_foods_e5_small_384` 572, `hue_foods_e5_small_384_dense` 572, `hue_full_corpus_7a2_e5_small_384` 8.459, đều green. Point count không đổi so với trước |
| `data/full_corpus_builds/` còn đúng 2 file | **Đạt**: `full_corpus_sparse_state.json`, `hue_full_corpus_7a2_e5_small_384.json` |
| Health runtime | **Đạt**: uvicorn port 8018, sau khi xóa collection và trước khi xóa file, trả HTTP 200 `{"status":"ok","components":{"app":"alive","qdrant":"ready","retrieval":"ready","tokenizer":"ready","generator":"ready"}}`. Chạy lại in-process sau khi xóa file: cùng HTTP 200 và cùng 5 component ready |
| Server đã dừng | Port 8018 free, không còn tiến trình |

## 5. Lỗi và giới hạn

- Auto-mode permission của B chặn lệnh `rm` 9 file và lệnh `kill` server. B không
  tìm cách lách; User chạy hai lệnh bằng `!` trong terminal B.
- Lần health thứ hai chạy in-process (ASGI), không qua uvicorn, để không phải
  dừng server thêm lần nữa. Đường code giống hệt: `create_app`, lifespan,
  `GET /health`.
- `kill $!` lần đầu chỉ dừng tiến trình `uv`, server con vẫn chạy. Đã ghi thành
  bẫy trong `STATUS_B.md`.
- Không xóa backup Gate 1 (`knowledge-base-hue/meta/backup_7a2_2026_10_23/`). Theo
  spec, backup chỉ xóa khi User đóng Phase.
- Notebook 06 và 08a còn tham chiếu collection vừa xóa (giới hạn đã ghi ở Gate 2,
  thuộc đợt dọn sau Phase 7).

## 6. Bàn giao cho người kiểm

- Đọc: report này và mục "Việc của B" trong `CURRENT_HANDOFF.md`.
- Chạy lại (chỉ đọc): `GET http://127.0.0.1:6335/collections` phải còn đúng 3 tên
  ở mục 4.3; `ls data/full_corpus_builds/` phải còn 2 file; health runtime.
- Evidence private ở `/tmp/phase7a2_gate2/`: `g3_before.txt`, `g3_delete.txt`,
  `g3_after.txt`, `g3_after_files.txt`, `g3_health.json`.
- Git: B không commit.
