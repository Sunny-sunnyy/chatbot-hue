# STATUS B — cập nhật 2026-10-24 19:45 +0700

Terminal: `hue-rag-b0` (A = `hue-rag-47`, C = `hue-rag-a3`) · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm — B9 dọn sau Phase 7: XONG, chờ C review (C9), A commit
- Report: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` (§0 tóm tắt, §4b phiên 2).
- Phiên 2 (18:51–19:45): pytest 15 file 191 passed / 0 lỗi; retrieval giống từng byte mốc (sha `cefb2d1a`);
  `/health` in-process 200 + 1 retrieval; golden check 176/10 exit 0; smoke 10 0 lỗi kỹ thuật (0,0013334 USD).
- Đã xóa 5 file `data/full_corpus_metadata_v2_*.json` (B) và 2 collection Foods (User chạy `!` vì auto-mode
  chặn B). Qdrant còn đúng `hue_full_corpus_7a2_e5_small_384` 8.459 point; `/health` chạy lại vẫn 200.
- Quan sát: smoke case 81 lỗi citation (thiếu `[n]`), 7B không có; context giống hệt — giả thuyết dao động
  model, A đưa vào bảng rà 8.1.
- A trả lời: `backend/test.ipynb`, `backend/scripts/` giữ; phát hiện B8 xếp Phase 8.1.

## File đang đổi, chưa commit (của B)
- Xóa: xem report §2 (`git status --short | grep '^ D'`).
- Sửa: `backend/config/settings.yaml`, `backend/core/settings_loader.py`,
  `backend/vectorstore/{qdrant,points,upsert}.py`, `backend/scoring/bm25.py`,
  `backend/tests/{conftest,test_bm25,test_full_corpus_chunker,test_full_corpus_qdrant_ingestion}.py`,
  `notebooks/{03,04,06}_*.ipynb`.
- Mới: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`.
- Log phiên 2: `/tmp/phase7_cleanup/` (`pytest_after2.txt`, `retrieval_after.jsonl`, `smoke_generate.jsonl`, `health_check.py`); log phiên 1 đã mất. Mốc cũ (phiên 1): (`retrieval_baseline.jsonl`, `pytest_before.txt`,
  `pytest_after.txt`, `collections_before.json`). `/tmp` có thể mất; bản gốc mốc retrieval là
  `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl` (sha `cefb2d1a…`).

## Tiếp theo
- C9 review: ready_for_user_confirmation, 0 blocker/major; B đã sửa minor m1 (report §4b). Chờ A commit.
- A (19:50): không có việc mới cho B tới khi User duyệt spec Phase 8.1; B nghỉ, không mở việc khác.

## Tiền paid hôm nay (B)
- B9 phiên 2: 0,0013334 USD (smoke 10).
- ~0,087 USD: 7B 0,0820 (smoke 0,0028 + Gate 2 0,0792) + probe B5 0,0050. B1 có 1 request trả 400, ~0 USD. B9 phiên 1: 0.

## Vừa xong hôm nay (đã commit bởi A)
- B1 health audit, B2–B4/B6/B7 Phase 7B (evaluator, Run 1/2, chẩn đoán từ chối nhầm, baseline);
  B5 probe context 10; B8 báo cáo khâu Phase 0–4 (`bao_cao_he_thong/BAO_CAO_{NEN_TANG,CHIA_DOAN,EMBEDDING_TU_KHOA,LUU_TRU_QDRANT}.md`);
  review A1 (đóng).

## Đã học / bẫy gặp
- Qdrant có thể tắt giữa phiên. Pytest vẫn chạy và lỗi môi trường trông như lỗi code: đọc dòng `E` trước khi kết luận.
- pytest: rootdir là gốc repo, node id là `backend/tests/…`; không dựa vào `--deselect`, chỉ liệt kê file test.
- Lệnh paid mới: chạy thử trước không có `--env-file` để thấy nó định gọi gì (đã cứu bug `select_cases([])`).
- Chạy notebook trên bản tạm: `nbclient` với `resources={"metadata": {"path": "<repo>/notebooks"}}`.
- Dùng `rm` thường, không `git rm`. `pkill -f` có thể kill chính shell; `kill $!` sau `uv run … &` không dừng server con. Kiểm health in-process bằng `create_app` + `httpx.ASGITransport`.
- Auto-mode có thể chặn `rm`/`kill`/xóa Qdrant: dừng, nhờ User chạy bằng `!` trong terminal B.
- User 2026-10-24: báo cáo trực tiếp với A; việc A giao = User giao.

## Câu hỏi / thắc mắc cho A
- Ai bật lại Qdrant cho phiên sau, và chạy bằng cách nào (B không thấy docker; không biết lệnh khởi động)?
- `backend/test.ipynb` và `backend/scripts/` (convert huegov raw→md) không nằm trong C2. Giữ hay dọn?
- Phát hiện ở B8 chưa có chủ: 3 cặp chunk chồng (blockquote trong list item), test còn mock/monkeypatch,
  entrypoint dùng `logging.basicConfig`, nhánh CUDA Qwen-0.6B còn sót trong `embedding/full_corpus.py`. Xếp vào Phase 8 hay dọn riêng?
