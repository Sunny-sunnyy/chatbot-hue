# STATUS B — cập nhật 2026-10-24 21:08 +0700

Terminal: `hue-rag-b0` (A = `hue-rag-47`, C = `hue-rag-a3`) · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm — B11 (G0.5 Phase 8.1): XONG 21:07, chờ C review
- Report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_5_params_implementation.md`.
- Sửa (chưa commit): `backend/llm/generator_openai_full_corpus.py`, `backend/retrieval/full_corpus.py`,
  `backend/ingestion/full_corpus_pipeline.py` (+97/−26). Gate: retrieval byte `cefb2d1a` PASS (evaluator HEAD,
  tách khỏi C16), pytest 15 file 195 passed, `/health` 200. 0 USD.
- Quan sát: mốc `native_hybrid_rrf` 7B không tái lập (6/158 câu), code HEAD cũng vậy ⇒ không do B11; báo A trước G1.
- Đã review skill "Ranh giới theo khâu pipeline" + `run-experiment` (report §7).

## Vừa xong — B10 (A giao 19:55): A review đạt, commit+push `74270ab` (docs, free)
- File đã sửa (chỉ 4 file này): `bao_cao_he_thong/BAO_CAO_{NEN_TANG,CHIA_DOAN,EMBEDDING_TU_KHOA,LUU_TRU_QDRANT}.md` → bản 2.
- Theo `TEMPLATE_USER_REPORT.md`: dòng "Cập nhật lần cuối … bản 2", Tóm tắt, checklist 5 mức, lịch sử mới ở trên,
  §5 kiểm với commit `1832201`, mã nội bộ + "Lệch" bản 1 (kèm trạng thái đã sửa ở B9 / còn) xuống Phụ lục.
- Số đo cũ giữ nguyên; thêm một mục lịch sử 24/10 "gỡ code bản món ăn (B9)"; dòng trỏ file đã xóa ghi "đã gỡ ở B9".
- Kiểm: mọi `file:dòng` trỏ file còn tồn tại đều trong độ dài file (script), đường dẫn thiếu chỉ là file đã gỡ có chủ đích; `git diff --check` sạch.
- Không sửa `bao_cao_he_thong/README.md` (cột "cập nhật" của 4 dòng B là việc của A).

## Vừa xong — B9 dọn sau Phase 7: commit `1832201`, User đóng 20:01 (C9 ready_for_user_confirmation)
- Report: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` (§0 tóm tắt, §4b phiên 2).
- Phiên 2 (18:51–19:45): pytest 15 file 191 passed / 0 lỗi; retrieval giống từng byte mốc (sha `cefb2d1a`);
  `/health` in-process 200 + 1 retrieval; golden check 176/10 exit 0; smoke 10 0 lỗi kỹ thuật (0,0013334 USD).
- Đã xóa 5 file `data/full_corpus_metadata_v2_*.json` (B) và 2 collection Foods (User chạy `!` vì auto-mode
  chặn B). Qdrant còn đúng `hue_full_corpus_7a2_e5_small_384` 8.459 point; `/health` chạy lại vẫn 200.
- Quan sát: smoke case 81 lỗi citation (thiếu `[n]`), 7B không có; context giống hệt — giả thuyết dao động
  model, A đưa vào bảng rà 8.1.
- A trả lời: `backend/test.ipynb`, `backend/scripts/` giữ; phát hiện B8 xếp Phase 8.1.

## File đang đổi, chưa commit (của B)
- Không có (B9 trong `1832201`, B10 trong `74270ab`). Log phiên 2 của B9 ở `/tmp/phase7_cleanup/` (có thể mất).

## Tiếp theo
- Chờ C review B11. Có thể review C16 nếu A giao.

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
