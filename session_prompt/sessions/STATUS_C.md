# STATUS C — cập nhật 2026-10-24

Terminal: `hue-rag-d9` · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- Chờ A review việc "rà soát lựa chọn Phase 2–6 cho Phase 8 (chỉ đọc)"
  (`CURRENT_HANDOFF.md` → Việc của C).

## Đang khai báo sửa
- không (đã xong: `reports/phase_8_candidate_hypotheses_2026_10_24.md`,
  `gửi chatgpt/tìm thông tin/phase_8_retrieval_improvements_2026_10_24.md`)

## Vừa xong
- Report giả thuyết Phase 8: 14 giả thuyết (H1–H14), 11 quan sát đo được (O1–O11),
  thứ tự đề xuất. Probe chỉ đọc bằng `uv run` (script `/tmp/c_probe/`, không commit);
  không sửa code/dữ liệu/Qdrant, không gọi paid.
- Yêu cầu nghiên cứu ChatGPT (9 câu, đòi URL) — chờ User gửi.

## Đã học / bẫy gặp
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
