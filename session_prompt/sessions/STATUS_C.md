# STATUS C — cập nhật 2026-10-24

Terminal: `hue-rag-d9` · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- Chờ A review C2; sau đó chờ 7B Gate 3 (Claude judge, spec 7B §4.3).


## Đang khai báo sửa
- không

## Vừa xong
- C2: `reports/phase_7_cleanup_inventory_2026_10_24.md` (chỉ đọc; đồ thị import AST `/tmp/c_probe/imports.py`; gồm input B1).
- C1 A đóng, commit `1027ec3`.
- Report giả thuyết Phase 8: 14 giả thuyết (H1–H14), 11 quan sát đo được (O1–O11),
  thứ tự đề xuất. Probe chỉ đọc bằng `uv run` (script `/tmp/c_probe/`, không commit);
  không sửa code/dữ liệu/Qdrant, không gọi paid.
- Yêu cầu nghiên cứu ChatGPT (9 câu, đòi URL) — chờ User gửi.

## Đã học / bẫy gặp
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
