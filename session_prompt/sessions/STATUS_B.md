# STATUS B — cập nhật 2026-10-24

Terminal: `hue-rag-64` · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- Chờ A review B2 (Phase 7B Gate 1); sau đó Gate 2 (Run 1/2 + judge luna) nếu A giao.

## Đang khai báo sửa
- `backend/evaluation/full_corpus_eval.py` (mới)
- `backend/evaluation/full_corpus_judge_prompt.md` (mới)
- `backend/tests/test_full_corpus_eval.py` (mới, logic thuần)
- `reports/phase_7b_gate_1_evaluator_implementation_2026_10_24.md` (mới)
- Kết quả private: `data/evaluation/phase_7b/` (file mới, không ghi đè `subsets.json`)

## Vừa xong
- B2 xong, chờ review A: `reports/phase_7b_gate_1_evaluator_implementation_2026_10_24.md`;
  retrieval tất định; smoke 10 sạch, 0,0028 USD; dự báo Gate 2 ~0,077 USD.
- B1 xong, A đã đóng: `reports/phase_7b_gate_0_health_audit_2026_10_24.md` — nền
  full-corpus khớp tài liệu; test free 211/213 pass (2 fail do hằng số cũ); sự cố
  deselect (collection test tạm + 1 request OpenAI 400 ~0 USD + ghi đè CSV, đã khôi phục).
- Phase 7A2 đã User-closed 2026-10-24 (Gate 1–3). Report của B: gate 2 reindex,
  gate 3 cleanup, governance v2 cross review.

## Đã học / bẫy gặp
- Git của B là `none`, nên dùng `rm` thường, không dùng `git rm` (lệnh này stage vào index).
- `pkill -f "<pattern>"` chạy trong cùng shell sẽ kill luôn chính shell đó; dùng `kill <pid>`.
- `kill $!` sau `uv run … &` chỉ dừng tiến trình `uv`, server con vẫn chạy.
  Muốn kiểm health mà không phải dừng server: gọi in-process qua `create_app` +
  lifespan + `httpx.ASGITransport`.
- Auto-mode permission của B chặn `rm` và `kill`. Khi bị chặn: dừng, nhờ User
  chạy bằng `!` trong terminal B.
- pytest: rootdir là gốc repo, node id là `backend/tests/…`; `--deselect tests/…`
  không khớp. Chỉ liệt kê file test free, không dựa vào deselect.
- Test Foods cũ ghi đè `backend/evaluation/retrieval_results.csv` (tracked); conftest
  `ingested_collection` tạo collection tạm Qdrant.
- `select_cases([])` từng = mọi case → retry chạy lại cả Golden; đã sửa. Lệnh paid mới:
  thử trước không `--env-file` để thấy nó định gọi gì.
- User 2026-10-24: báo cáo trực tiếp với A; việc A giao = User giao.

## Việc dở / câu hỏi cho A
- Không.
