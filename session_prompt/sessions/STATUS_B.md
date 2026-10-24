# STATUS B — cập nhật 2026-10-24

Terminal: `hue-rag-64` · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- B8 xong: 4 file trong `bao_cao_he_thong/` (NEN_TANG, CHIA_DOAN, EMBEDDING_TU_KHOA, LUU_TRU_QDRANT). Review A xong: `report_agent/2026-10-24_to_chuc_bao_cao/bao_cao_he_thong_A1_review.md` (changes_requested: 1 major, 6 minor).
  Nháp do 4 sub-agent viết ở `/tmp/b8/`, B kiểm file:dòng các lệch chính trước khi chép vào repo.

## Đang khai báo sửa
- `bao_cao_he_thong/BAO_CAO_{NEN_TANG,CHIA_DOAN,EMBEDDING_TU_KHOA,LUU_TRU_QDRANT}.md` (mới)

## Vừa xong
- B8 bước nhỏ: report Gate 4 §5 → User bỏ chấm tay, tiêu chí 5 PARTIAL (đóng). Phase 7B User-closed (`62c757d`).
- B6 C review `ready_for_user_confirmation`, A commit `c1f4f20`; B7 sửa m1–m3.
- B6 (Gate 4) xong, chờ review chéo: baseline Claude Run 1 A/C/R 4,426/4,284/4,455; nhiễu cả
  đường ≤0,011, 0 case lệch ≥2; 121 case 5/5/5, 22 case 1/1/1 = đúng 22 từ chối nhầm.
- B5 A đóng, commit `f80737a`.
- B5 (probe context 10): 0,00495 USD. Tổng paid B ~0,087 USD.
- B4 A đóng, commit `9514f75`.
- B4 chi tiết: `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`; nhiễu judge
  luna rất thấp (30/30 lệch ≤1); 22 từ chối nhầm = 8 retrieval miss / 10 một phần / 4 đủ keyword.
- B3 (Gate 2) A đóng, commit `28b14be`.
- B3 chi tiết: `reports/phase_7b_gate_2_runs_implementation_2026_10_24.md`;
  Run 1/2 176/176, judge luna 176+30 hợp lệ; Gate 2 0,0792 USD, tổng B 7B 0,0820 USD.
- B2 (Gate 1) A đóng, commit `ea5a1d5`.
- B2 chi tiết: `reports/phase_7b_gate_1_evaluator_implementation_2026_10_24.md`;
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
