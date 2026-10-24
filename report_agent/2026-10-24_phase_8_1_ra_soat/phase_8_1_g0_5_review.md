# Review: Phase 8.1 G0.5 — tham số mặc định-như-cũ (B11)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor; thêm 1 điểm cần A quyết trước G1.3,
1 điểm trước G3)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a3`)
Date: 24/10/2026, 21:05–21:11 (giờ lấy bằng `date`)
Spec: `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §3.1, §5 G0.5, §6.1
Implementation report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_5_params_implementation.md`

## 1. Phạm vi đã review

- **Exact diff** của 3 file B11 (working tree, trên `5c9d172`):
  - `backend/llm/generator_openai_full_corpus.py`;
  - `backend/retrieval/full_corpus.py`;
  - `backend/ingestion/full_corpus_pipeline.py`.

  Đối chiếu với danh sách tham số spec §3.1 và mục việc B11.
- **Kiểm phạm vi:** B11 không đụng `backend/evaluation/` (C16), chunker, `settings.yaml`, loader.
- **Kiểm độc lập** các gate G0.5 (§3) và mốc `native_hybrid_rrf` mà B báo không tái lập.

## 2. Findings

**Không có blocker hoặc major.**

| Tiêu chí (spec §3.1 / B11) | Kết quả |
|---|---|
| Generator: `answer_instructions` (mặc định `ANSWER_SYSTEM_INSTRUCTIONS`), `reasoning_effort` (mặc định `None` ⇒ `ModelSettings(reasoning=None)`) ở `__init__` và `from_environment` | Đúng. Agent Representation B không đổi |
| Retrieval: `candidate_pool` (30), `rrf_k` (60), `search_params` (`None`) truyền vào cả hai `query_points` và RRF; factory nhận `collection_name`, `record_path`, `sparse_state_path` | Đúng. Mặc định giữ nguyên 30/30/60. Đổi tên collection bằng `dataclasses.replace` trên candidate, nên phần kiểm record, truy vấn và trace dùng cùng một tên |
| Pipeline: `collection_name`, `sparse_state_path`, `record_path`, `embedding_models` (chép settings, không sửa chunker) | Đúng. `record_path` ngoài danh sách §3.1 nhưng cần cho §3.2; B đã ghi lý do |
| Không đổi mặc định / không thêm key `settings.yaml` / không sửa loader / không abstraction | Đúng. Chỉ thêm tham số keyword và một helper `_repo_relative` cho thông báo lỗi |
| Comment tiếng Việt ghi *vì sao* | Có, ngắn |

**Minor:**

- **m1. Biến thể build quên `record_path` thì record rơi vào thư mục runtime.**
  `build_candidate(collection_name="hue_81_x")` mà không truyền `record_path` sẽ ghi record vào
  `data/full_corpus_builds/hue_81_x.json` (`build_record_path` lấy theo tên collection), không phải
  `data/phase_8_1/builds/` như spec §3.2. Record runtime không bị ghi đè (khác tên), nên không nguy
  hiểm, nhưng làm bẩn thư mục runtime.
  - Tiêu chí đóng: harness G3 luôn truyền `record_path` (và `sparse_state_path`); người review G3 kiểm
    điểm này.
  - Không đề xuất thêm validator.
  - Ghi chú: nếu harness quên `sparse_state_path` mà đổi chunk thì `_write_or_check_sparse_state` raise
    (fail-closed). Như vậy sparse state runtime an toàn.
- **m2. Hành vi `reasoning_effort=""`.** Chuỗi rỗng bị coi như "không gửi" (`if reasoning_effort`), không
  báo lỗi. Hiện không ảnh hưởng; ghi lại để harness truyền đúng `none`/`low`/`medium`/`high`.

**Cần A quyết** (không phải lỗi của B11):

1. **Mốc `native_hybrid_rrf` của 7B.** C chạy lại độc lập: khác mốc 7B ở đúng 6/158 câu như B báo
   (case 0, 10, 14, 16, 25, 162). Lượt của C **giống từng byte** lượt của B (`/tmp/b11/retrieval_native_after.jsonl`).
   Bằng chứng thêm của C:
   - Code retrieval/sparse/BM25 không đổi từ `b781af8` (12:33). Mốc native được ghi 14:39, sau đó, nên
     khác biệt **không do code**.
   - Nhánh dense giữ nguyên: `dense_bm25_rrf` vẫn giống byte.
   - Điểm hòa ở biên top-30 của nhánh sparse chỉ có ở 2/6 câu (case 25, 162; probe `/tmp/c18_ties.py`,
     chỉ đọc). Hòa không giải thích hết.
   - Giữa 14:39 và bây giờ, Qdrant đã tắt / bật lại (17:10) và 2 collection Foods bị xóa (B9).

   Giả thuyết (chưa chứng minh): trạng thái Qdrant đổi (segment/optimizer) làm đổi thứ tự trả về ở nhánh
   sparse. Đề xuất: dùng lượt chạy hôm nay làm mốc native cho G1.3 (đã có 2 lượt giống hệt nhau, của B
   và của C). Ghi "mốc 7B không tái lập, lý do chưa rõ" trong report G1. A duyệt.
2. **Trước G3: `build_candidate` chưa nhận danh sách chunk do harness xử lý tiếp** (B §5 mục 1). Spec
   §3.1 đặt logic chia đoạn mới trong harness, nên G3 cần một lối vào nhận `chunks`. C đồng ý với B: thêm
   tham số `chunks` (mặc định `None` = `chunk_full_corpus`) theo cùng luật mặc định-như-cũ + gate G0.5,
   trước khi làm G3.

Các mục "khâu còn dính" khác B ghi (top-10 hằng, settings đọc trong pipeline, client tạo bên trong, K1/B)
nên đưa vào danh sách G5 như A đã chốt.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `uv` trong `.venv`, `HF_HUB_OFFLINE=1`, Qdrant chỉ đọc, 0 USD. Working tree lúc chạy có cả
diff C16 (evaluator) lẫn B11. Bằng chứng là cho tổ hợp này; md5 3 file B11 lúc kiểm: `db49e803…`
(retrieval), `5ff3a792…` (generator), `943d0f21…` (pipeline).

```bash
uv run --env-file ../.env python -m pytest -p no:cacheprovider tests/test_full_corpus_{chunker,sparse,embedding,qdrant_ingestion,retrieval,context,eval}.py tests/test_{citations,bm25,golden_full_corpus,phase6_settings,static_ui,api_chat,openai_full_corpus_generator,phase6_live_smoke}.py -q
uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/c18_dense.jsonl            # + cmp mốc 7B
uv run python -m evaluation.full_corpus_eval retrieval --treatment native_hybrid_rrf --out /tmp/c18_native.jsonl   # + cmp lượt B và mốc 7B
PYTHONPATH=. uv run --env-file ../.env python /tmp/b11/param_check.py                      # /health + tham số mới
uv run python -I /tmp/c18_ties.py                                                         # hòa điểm sparse ở biên top-30
```

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Pytest 15 file | **PASS**: 195 passed, 0 failed (156,7 s) |
| `dense_bm25_rrf` 176 câu | **PASS**: giống từng byte mốc 7B (`cefb2d1a…`) |
| `native_hybrid_rrf` | Giống từng byte lượt B11; khác mốc 7B 6/158 (như B báo; xem §2 "Cần A quyết" 1) |
| `/health` in-process | **PASS**: 200, mọi thành phần `ready` |
| Tham số mới chạy thật | Đường tường minh = mặc định (cùng top-10); `pool=100, k=10, exact=True` cho counts dense 100 / bm25 100 / rrf 100 / final 10; generator mặc định `reasoning=None`, tùy chỉnh `Reasoning(effort='low')` + instructions truyền vào |
| `git diff --check` | sạch |

## 5. Giới hạn

- Không chạy `build_candidate` với tham số mới (ghi Qdrant, ngoài quyền review). Lần dùng thật đầu tiên
  là harness G3.
- Không chạy generator với `reasoning_effort` qua API (có phí). Chỉ kiểm cấu trúc `ModelSettings`.
- Nguyên nhân lệch mốc native chưa chứng minh.

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`** cho B11. A commit 3 file cùng gate G0. m1, m2 không cần vòng sửa. A quyết
mốc native (mục 1) trước G1.3, và lối vào `chunks` (mục 2) trước G3.
