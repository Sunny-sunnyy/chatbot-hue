# STATUS C — cập nhật 2026-10-24

Terminal: `hue-rag-d9` · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- C7 (A giao sau khi User đóng 7B, commit `62c757d`): cập nhật cột "Cách làm phổ biến" + nguồn trong
  `reports/phase_8_candidate_hypotheses_2026_10_24.md`. Sau đó C8 user report Phase 5, 6, 7/7A, 7A2.
- Report mới vào `report_agent/<YYYY-MM-DD>_<chủ_đề>/`; `reports/` là lịch sử. ChatGPT: `gửi chatgpt/<ngày>/…`.

## Đang khai báo sửa
- `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C7, sửa tại chỗ)
- `report_agent/user_reports/phase_05_truy_xuat.md`, `phase_06_sinh_cau_tra_loi_api.md`, `phase_07_golden.md`,
  `phase_07a2_sua_corpus_index.md` (C8, mới); file này

## Vừa xong
- C7 xong (chờ A review): report giả thuyết Phase 8 có cột nguồn [R1]–[R11] + §8 (WebFetch 5 URL: khớp, lệch nhỏ
  bge-reranker max len 8K vs card 512; thứ tự mới: đo pool/gold → context10+partial → bảng/bigram/tách câu → chunk → rerank → paid).
- C5 A nhận, commit `c1f4f20`: `reports/phase_7b_review_2026_10_24.md` (ready_for_user_confirmation có điều kiện; m1–m3 → B7).
- C3 A đóng, commit `1994ea5`.
- C3: 3 file điểm Claude (`claude_run1`, `claude_run1_rerun30`, `claude_run2` trong `data/evaluation/phase_7b/`),
  39 sub-agent / 39 lô, 0 lỗi, `score_errors` rỗng; ~8 phút. Report
  `reports/phase_7b_gate_3_claude_judge_implementation_2026_10_24.md`. Script `/tmp/c_judge/` (ngoài repo).
- C2 A đóng, commit `dba4881`: `reports/phase_7_cleanup_inventory_2026_10_24.md` (chỉ đọc; đồ thị import AST `/tmp/c_probe/imports.py`; gồm input B1).
- C1 A đóng, commit `1027ec3`.
- Report giả thuyết Phase 8: 14 giả thuyết (H1–H14), 11 quan sát đo được (O1–O11),
  thứ tự đề xuất. Probe chỉ đọc bằng `uv run` (script `/tmp/c_probe/`, không commit);
  không sửa code/dữ liệu/Qdrant, không gọi paid.
- Yêu cầu nghiên cứu ChatGPT (9 câu, đòi URL) — chờ User gửi.

## Đã học / bẫy gặp
- Kiểm tuân thủ sub-agent: grep transcript `tasks/*.output` chỉ lấy tool name + `file_path` (không đọc nội dung).
- `knowledge-base-hue/foods/evaluation/` vừa có Golden Foods cũ vừa có file authoring 7A đang dùng — không xóa cả thư mục.
- `load_settings` bắt buộc `active_profile` ∈ `profiles` (Foods); `vector_database.url/timeout` vẫn được full-corpus dùng.
- Grep với brace-expansion `--exclude-dir={…}` có tên tiếng Việt bị safety check chặn; dùng nhiều `--exclude-dir=` riêng.
- Lần mở này A = `hue-rag-77`, B = `hue-rag-64`.
- Lấy thông tin ngoài: file yêu cầu (kèm URL) trong `gửi chatgpt/tìm thông tin/` → báo A
  → đọc `gửi chatgpt/kết quả nghiên cứu/` + WebFetch đối chiếu.
- User 2026-10-24 (terminal C): A giao việc = User giao; báo cáo trực tiếp với A.
- Script probe import `backend.*` phải chạy từ repo root (`sys.path` = repo root), không
  phải `backend/` — `full_corpus_pipeline.py` import tuyệt đối `backend.core`.
- Golden thực tế có 5 category (`direct_fact` 75, `multi_source` 29, `conditional` 29,
  `comparative` 25, `out_of_scope` 18) theo spec 7A — guide còn mô tả 7 nhãn cũ (lịch sử).

## Việc dở / câu hỏi cho A
- Khi có kết quả nghiên cứu: cập nhật cột "Cách làm phổ biến" của report bằng nguồn.
- Câu hỏi trong report §5 (spec lệch về câu trả lời một phần; hạ ưu tiên F1).
