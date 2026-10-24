# Review: Phase 7A2 Gate 2 — Build 2 index và cutover runtime

Decision: approved with limitation (User 2026-10-24) — e5 index + cutover đạt; index 8B hoãn sang Phase 8
Reviewer: Claude Opus 5.5 (A)
Date: 2026-10-24
Spec: `docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md` (§5; amendment §2/§5.2/§8 ngày 2026-10-24)
Plan: `docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md` (Task 4–8)
Implementation report: `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md`

## 1. Phạm vi đã review

- Đọc đủ handoff `final_review` và implementation report.
- Diff gate: `git status`, `git diff --stat 5e8aff1`, đọc diff đầy đủ của
  `embedding/full_corpus.py`, `ingestion/full_corpus_pipeline.py`,
  `ingestion/source_state.py`, `retrieval/full_corpus.py`,
  `llm/phase6_live_smoke.py`, `vectorstore/qdrant.py`, `pyproject.toml`; quét
  dòng thêm trong tests. `git diff --check` sạch.
- Chạy lại read-only theo Review Contract (mục 3).

## 2. Findings

**F1 — major — index 8B trộn vector nhiều provider (acceptance §5.5 mục 2 FAIL).**
Build không pin provider (đúng spec bản 2026-10-23) nên OpenRouter phân 133
batch cho DeepInfra, Nebius, SiliconFlow. Mẫu 20 chunk: 10 cos ≈ 0,9999, 10 cos
0,9953–0,9974 so với Nebius; min 0,99535 < 0,999. Tác động: so sánh e5 vs 8B ở
Phase 7B/8 không đáng tin vì vector document và query không đồng nhất. Đây là
lỗ hổng thiết kế (survey chưa đo được DeepInfra do 429), không phải lỗi
Implementer. User chọn (b) ngày 2026-10-24: pin Nebius cho build và query, xóa
index 8B hiện tại, dùng lần build thứ 2. Đóng khi: build 8B mới chỉ có provider
`Nebius`, cos mẫu ≥ 0,999, retrieval smoke 8B chạy lại.

Không có finding khác. Deviation D1 (`{384, 4096}`), D2 (mẫu verify = chunk
đầu mỗi domain) đã chấp nhận. Sai lệch nhỏ (không quan sát RED, `HF_HUB_OFFLINE=1`,
`git rm` lỡ stage rồi restore) không ảnh hưởng nghiệm thu.

Ghi nhận ngoài phạm vi: notebook 04/06/08b còn tên cũ (sẽ gãy sau Gate 3) và
markdown notebook 03 còn mô tả 4 model — đưa vào đợt dọn sau Phase 7.

## 3. Reviewer chạy lại thật (read-only)

| Kiểm tra | Kết quả |
|---|---|
| `GET /collections/<7a2>` | e5: 8.459 point, green, dense 384 Cosine + sparse; 8B: 8.459, green, dense 4096 Cosine + sparse |
| Scroll toàn bộ payload | cả hai: 8.459 point, 0 payload sai 7 field, đủ 5 domain |
| Mẫu 50 point có vector | dense 384 / 4096, sparse không rỗng |
| Hai build record | schema `full_corpus_build:v3`, `complete`, 205 file / 8.459 chunk, `point_count` 8.459; sparse SHA `dbd5f7bc…` khớp file `full_corpus_sparse_state.json`; 8B providers `[DeepInfra, Nebius, SiliconFlow]` |
| Health (`uvicorn` port 8017, `.env`) | HTTP 200, `app/qdrant/retrieval/tokenizer/generator` đều ready |
| Grep hằng số/module đã xóa trong `backend/` | 0 |
| Dòng test thêm chứa mock/monkeypatch/fake/stub | 0 |

Không chạy lại paid call, không chạy lại focused suite (Implementer: 95 passed).

## 4. Giới hạn

- Không xác định được provider theo từng batch của build 8B cũ (runner chỉ ghi tập).
- e5 build, health, live smoke 5 call được giữ làm evidence cho Correction 1
  vì correction chỉ đổi nhánh OpenRouter.

## 5. Decision và bước tiếp theo

`changes_requested` → handoff `correction` (Correction 1) cho Implementer B.
Sau Correction 1: Reviewer review delta, User đóng Gate 2, rồi mở Gate 3.

## 6. Correction 1 và closure (2026-10-24)

Correction 1 (B): code pin Nebius (`order: [nebius]`, `allow_fallbacks: false`,
`data_collection: deny`; response provider khác `Nebius` thì raise, có test
thuần); xóa đúng index 8B cũ (8.459 point, record `ea4672c1…`); build lần 2/2
lỗi **HTTP 504** ở batch 20/133 (pin Nebius ~10–30 s/batch), trước khi tạo
collection. Focused suite 96 passed, `git diff --check` sạch.

A kiểm lại: Qdrant không có collection 8B, không có record 8B; collection e5,
record e5 và `full_corpus_sparse_state.json` còn nguyên; log build ghi
`RuntimeError: OpenRouter HTTP 504`; code gửi `OPENROUTER_PROVIDER_ROUTING`
trong mọi request.

**Quyết định User 2026-10-24:** hoãn index 8B sang Phase 8 (chunking có thể đổi ở
Phase 8 nên 8B sẽ phải build lại; khi đó thiết kế cách gọi chịu lỗi 504/429 —
batch nhỏ hơn, một lần thử lại — dựa trên hai lỗi đã quan sát). Đóng Gate 2 với
e5: acceptance §5.5 mục 1, 3, 4, 6 đạt; mục 2 và 5 chỉ đạt cho e5. F1 chuyển
thành giới hạn mở cho Phase 8. Code runner 8B (pin Nebius) giữ trong repo, chưa
có index.

Gate 2 `approved` (với giới hạn trên). Git: A commit/push.
