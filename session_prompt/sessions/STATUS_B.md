# STATUS B — cập nhật 2026-10-24 17:12 +0700

Terminal: `hue-rag-64` · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm — B9 dọn sau Phase 7: DỞ, dừng ở điểm an toàn
- Report: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` (§6: các bước còn lại).
- Đã xong (working tree, **chưa commit**): xóa 42 file Foods (code/test/notebook 02,05,07,08a/b/c,
  CSV, `requirements.txt`) và thư mục `backend/ingestion/helpers/`. Đã sửa settings, loader,
  vectorstore, bm25, conftest, 3 test, notebook 03/04/06.
- Kiểm đạt: import toàn backend, grep sạch, notebook 04 và 03 Run All trên bản tạm.
- **Dừng vì Qdrant tắt** (17:10, `curl :6335` exit 7, không phải do B). Lượt pytest sau dọn:
  176 passed, 15 lỗi, tất cả do `Connection refused`/health degraded. **NOT RUN**: so byte retrieval,
  `/health`, golden check, smoke 10 paid.
- **Chưa xóa** 2 collection Foods và 5 file `data/full_corpus_metadata_v2_*.json`.

## File đang đổi, chưa commit (của B)
- Xóa: xem report §2 (`git status --short | grep '^ D'`).
- Sửa: `backend/config/settings.yaml`, `backend/core/settings_loader.py`,
  `backend/vectorstore/{qdrant,points,upsert}.py`, `backend/scoring/bm25.py`,
  `backend/tests/{conftest,test_bm25,test_full_corpus_chunker,test_full_corpus_qdrant_ingestion}.py`,
  `notebooks/{03,04,06}_*.ipynb`.
- Mới: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`.
- Mốc so sánh: `/tmp/phase7_cleanup/` (`retrieval_baseline.jsonl`, `pytest_before.txt`,
  `pytest_after.txt`, `collections_before.json`). `/tmp` có thể mất; bản gốc mốc retrieval là
  `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl` (sha `cefb2d1a…`).

## Phiên sau làm tiếp (theo thứ tự)
1. Bật Qdrant; `GET /collections` phải còn đúng 3 collection (Foods 572/572, full-corpus 8.459).
2. Pytest lại 15 file (lệnh ở report §4); kỳ vọng 0 lỗi.
3. So byte retrieval; `/health` + 1 retrieval; `golden_full_corpus check`; smoke 10 (≤0,005 USD).
4. Đạt hết thì xóa 2 collection Foods + 5 file metadata_v2 (liệt kê trước/sau), cập nhật report, nhắn A, rồi C review.

## Tiền paid hôm nay (B)
- ~0,087 USD: 7B 0,0820 (smoke 0,0028 + Gate 2 0,0792) + probe B5 0,0050. B1 có 1 request trả 400, ~0 USD. B9: 0.

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
