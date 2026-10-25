# Review: Phase 8.2 B1 plan (B23) — context 10 + NFC

Decision: **ready — A duyệt bản sha `1a5ac660bd5d`**
Người kiểm: A (Claude Opus 5.5, terminal `hue-rag-00`) · 2026-10-25 16:27 (`date`)
Bản được review: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_plan.md` sha256 `1a5ac660bd5d` · Spec 8.2 sha `dabae90b2b60`

## 1. Phạm vi đã review

Gói "Căn cứ để review" của plan (plan; spec §3.2, §4, §5 B1, §7; `backend/retrieval/full_corpus.py:462-470`;
`backend/api/routes/chat.py:47-75`; `backend/evaluation/full_corpus_eval.py:327-375`). Lệnh chỉ đọc: `ls backend/tests/`
(4 file test plan nêu đều có); `grep` client OpenAI trong `test_api_chat.py`, `test_full_corpus_retrieval.py`,
`test_full_corpus_context.py` — không thấy; mốc `cefb2d1ad609…` trong `data/phase_8_1/baseline/g0_6_manifest.json` (khớp T1).

## 2. Đối chiếu tiêu chí spec B1.2

| Spec B1.2 | Plan | Khớp |
|---|---|---|
| 158 câu byte `cefb2d1a…` | T1 | ✓ |
| 176 / 176 `top_chunk_ids`, `context_sources`, `input_tokens` = G2.1a | T2 | ✓ |
| G2.1a chấm lại cùng lượt mù; 0 OOS; 0 lỗi; Completeness CI chứa 0; A/A context 10 | T3 | ✓ |
| `/chat` tới 10 nguồn, có citation | T4 (+ số nguồn đóng gói đo ở T5) | ✓ |
| câu NFD cùng nguồn bản NFC | T5 + đối chứng trước sửa | ✓ |
| tiền ≤ trần, pilot 10 | §6 (0,037 ≤ 0,06; ước lại × 17,6; > 50% dừng) | ✓ |

## 3. Quyết định của A cho hai câu B hỏi

1. **Chỗ NFC:** đồng ý đầu `FullCorpusRetrievalService.search` qua hàm thuần `normalize_query` (một chỗ, đúng tầng đã đo hại).
   Giới hạn "câu đưa model vẫn là chuỗi gốc" ghi trong report B1 và báo cáo khâu; không thêm chỗ thứ hai khi chưa có số đo hại ở
   bước sinh.
2. **T5 "cùng nguồn":** đúng cách hiểu của B — 10 id `search` + nguồn đóng gói (tất định) quyết đạt / không đạt; `sources` của API
   phụ thuộc câu trả lời model ⇒ chỉ ghi.

## 4. Findings

Không có blocker / major.
- minor a: report B1 ghi model id judge và số câu đổi điểm A/A **theo dev bỏ unnatural** bên cạnh số 176 câu (số chính của 8.1 dùng
  tập đó; E1 / E2 sẽ cần nhiễu trên cùng tập). Không đổi tiêu chí T3.
- minor b: T4 dùng port 8000 — kiểm port trống trước (`ss -ltn`), máy có dự án khác chạy song song.

## 5. Kết luận

A duyệt plan sha `1a5ac660bd5d`; B sửa code và chạy theo plan. Report B1 do A review (C đang C32).
