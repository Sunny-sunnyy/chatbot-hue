# Implementation Report: Phase 9 B3 — nhớ hội thoại (cờ `nho_hoi_thoai` TẮT) + sửa lời dặn D6 (**dở — khoá phần đã thấy, chờ C chạy kín**)

Người làm: B (Claude Opus 5.5, `hue-rag-52`) · việc **B136** · bắt đầu 11:50 03/11/2026, bản này 13:19 03/11/2026 (kết phiên; giờ các mốc từ `date`).
Plan: `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` bản 2 sha `cd099ec0a00e` (A duyệt; commit `10ec9a2`). Bộ đo: C136 `report_agent/2026-11-02_phase_9_code/c136_bo_do_b3.md` (sha `3301f3c7b7e3` khi giao việc).
Nhánh **`p9-b3`** từ `10ec9a2`, worktree `/tmp/b_p9b3` (giữ). Commit: `e69c293` (code D1–D5, D9 (b) + test), `cb73e19` (review C145 m-1 / m-2), **`46008ed`** (D6 bản hẹp). Đã push. **Chưa merge.**
Report tracked, repo public: không chép câu Golden / câu chuỗi / kho; chỉ số đếm, `case_index`, mã chuỗi. Dữ liệu chạy: `data/phase_9/b3/` (private).

## 1. Phạm vi — đã làm / chưa làm

| Phần plan | Trạng thái |
|---|---|
| D1 kho cuộc trò chuyện RAM + cookie `conversation_id` (HttpOnly, SameSite=Strict, Path=/api, 30 phút, 500 cuộc) | xong + test |
| D2 giữ 3 lượt / ≤ 1.500 token, câu trả lời bỏ mã trích dẫn | xong + test |
| D3 lịch sử vào định tuyến + trò chuyện + trợ lý; câu dặn lịch sử chỉ khi có lịch sử | xong + test |
| D4 `POST /api/conversation/new`; log chỉ số đếm (`n_history_turns`, `history_tokens`), không mã cuộc / chữ | xong + test |
| D5 đếm token có lịch sử + phần đệm mục (`TOOL_PATH_OVERHEAD` 158, `ITEM_OVERHEAD` 36) | xong + test; số thật §4 Q8 |
| D6 lời dặn chống thêm lưu ý không nguồn (S20) | **bản hẹp giữ** sau 2 / 2 vòng (§4 Q2) |
| D9 (b) `generating` ngay trước `delta` đầu ở đường có công cụ | xong + test |
| harness `chuoi` (nho / doc_lap / tran, `--chi`, `--khong-in-chu`) | xong, chạy thật |
| Q1, Q2, Q8 pilot, chuỗi đã thấy (Q3–Q7 phần đã thấy) | **xong** (§4) |
| Khoá trước phần kín | **xong** (§5) |
| Phần kín 15 chuỗi (C chạy + chấm) | **chưa** — chờ C |
| Q10 cổng (uvicorn, cookie thật, ngắt `curl -m`) | **chưa** |
| Bước 8 giao diện (User chọn **Bản 1 — Huế hiện đại**, `data/giao_dien_v2/mau/1.html` `2952d57f3a92`, 13:11 03/11) | **chưa** |
| Mặc định `nho_hoi_thoai` | vẫn **false** (bật sau giao diện) |

## 2. Thay đổi chính (`git diff 10ec9a2..46008ed -- backend`, 11 file, +588 / −54)

| File | Thay đổi |
|---|---|
| `backend/api/conversations.py` (mới) | `stored_answer` (bỏ mã trích dẫn), `ConversationStore` (TTL, trần cuộc / lượt / token, `ensure` / `history` / `append` / `reset`) |
| `backend/api/app.py` | dựng `ConversationStore` sau tokenizer khi `nho_hoi_thoai` bật, không thì `None` |
| `backend/api/routes/chat.py` | cookie, `POST /api/conversation/new`, ghi lượt (outcome trong `REMEMBERED_OUTCOMES`) sau dòng log; lượt lỗi vẫn gửi cookie (C145 m-2); 2 trường log mới |
| `backend/llm/assistant.py` | `AnswerTrace.history`; cờ `nho_hoi_thoai` / `nho_cau_tra_loi`; lịch sử vào mọi lời gọi; `n_tool_items` cho ngân sách; D9 (b) |
| `backend/llm/generator_openai_full_corpus.py` | `with_history` (rỗng ⇒ đúng chuỗi B2), agent định tuyến / trợ lý có câu dặn lịch sử, mọi đường nhận `history=()` |
| `backend/llm/full_corpus_prompt.py` | D6 (bản hẹp, §4), `ROUTER_HISTORY_NOTE`, `ASSISTANT_HISTORY_NOTE` |
| `backend/retrieval/full_corpus_context.py` | `_token_count(…, history, n_tool_items)` + hằng phần đệm (nguồn: pilot B2 + C) |
| `backend/evaluation/full_corpus_eval.py` | lệnh `chuoi` (cùng một `ConversationStore`, ghi `usage_tru_builder`) |
| `backend/config/settings.yaml` | `nho_hoi_thoai: false`, `nho_cau_tra_loi: true` |
| tests | `test_b3_memory.py` (mới, 13 test), `test_b2_tool_loop.py` (thứ tự `generating`, ngân sách trừ phần đệm) |

## 3. Cách đã chạy thật

Từ `/tmp/b_p9b3/backend`: `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag [--env-file /home/minhhieu/hue_rag/.env] …`.
Test: `pytest tests/test_b3_memory.py tests/test_b2_tool_loop.py tests/test_api_chat.py` ⇒ **33 / 33** (sau C145).
Q2: `full_corpus_eval generate` (176) + `data/phase_9/b2_chay/tools/sinh_an_toan.py` (32, có ngữ cảnh) ⇒ `do_cuoi.py` (DO_CUOI_DIR) + `an_toan_b2.py` + `data/phase_9/b3/tools/q2_golden.py`, `regen_thieu.py`; judge = sub-agent Claude mới mỗi lô.
Chuỗi: `full_corpus_eval chuoi data/phase_9/bo_do_b3/chuoi_da_thay.jsonl --ben nho|doc_lap|tran --out …` ⇒ `data/phase_9/b3/tools/cham_chuoi.py may|export|analyze` (sha `6bcd64e6bc1c`).

## 4. Kết quả quan sát

| Mã | Kết quả | Bằng chứng |
|---|---|---|
| **Q1** | **PASS** — nhớ tắt: định tuyến + trò chuyện giống byte B2; lần gọi trả lời / trợ lý khác B2 đúng một chỗ (câu D6) | `data/phase_9/b3/q1/` |
| **Q2 vòng 1** (D6 "Chỉ nêu điều có trong Bằng chứng; không thêm lời khuyên chung…") | **phạm sàn từ chối nhầm 7 > 5** (mới: case 20, 48 — không bị từ chối ở cả 2 lượt B2). Đủ tụt 6 / TB −0,070, Đúng tụt 4 / −0,047, F1–F4 0. S-AT: P0_sai mới S10 ⇒ sinh lại 0 / 3 ↔ mốc 0 / 3; thiếu mới so B2 S04 ⇒ 0 / 3 ↔ 0 / 3; S20 ép `tro_ly_hue` 0 / 3. **Đọc chữ (judge không bắt):** S04 giữ lời khuyên có nguồn 1 / 4 (B2 4 / 4), S10 mở "Có." rồi nói ngược 3 / 4 | `q2_judge*/` |
| **Q2 vòng 2** (D6 hẹp: chỉ chặn lời khuyên / lưu ý an toàn không có nguồn, giữ cái có nguồn; A quyết) | chạy thử nhanh (S20 ép, S04, S10, case 20 / 48 × 3) sạch ⇒ 208: **từ chối nhầm 4** · Đủ tụt 5, **TB +0,000** [−0,054; +0,062] · Đúng tụt 1, **TB +0,016** · F1–F4 0 · **P0_sai 0** (mốc 01/11: 2) · thiếu mới so B2 S09, S26 ⇒ sinh lại 3 / 3 ↔ 3 / 3, 0 / 3 ↔ 0 / 3 ⇒ không mới thật · cổng đối chứng judge 10 / 10, 5 / 5, 0 / 5 cả 6 bộ. **Đọc chữ:** S04 giữ 3 / 4, S10 "Không" 4 / 4, case 48 từ chối 1 / 4 (thử nhanh 1 / 3, 208 0 / 1). ⇒ **GIỮ D6 hẹp** (luật ghi trước); S20 hết "mới thật", B3 dùng 0 suất P0_sai | `q2v2*/` |
| **Q8** token thật − builder (lượt viết) | pilot nhớ 3 chuỗi: −140…0; chuỗi đã thấy (nho, 44 lượt viết): −140…**167**; tran max 300 ⇒ **< 512 mọi lượt**. Builder đếm **dư ~70 token mỗi lượt lịch sử** (phần đệm mục 36 đo trên mục công cụ; tin lịch sử nhẹ hơn) — an toàn, không sửa | `pilot_nho/`, `chuoi_r1/may.json` |
| **Q3** nhớ tên (đã thấy) | **6 / 6** | `chuoi_r1/may.json` |
| **Q4** hỏi tiếp — Completeness lượt sau có `golden` (20), nhớ ↔ câu gõ thật không lịch sử | **TB +0,65, CI 95 % [+0,15; +1,25] > 0** (6 thắng / 13 hoà / 1 thua — D02). Báo kèm: chỉ 9 lượt hỏi tiếp +1,22 [+0,22; +2,33]; nhớ ↔ trần `dung_mot_minh` +0,15 [−0,15; +0,60] | `chuoi_r1/q4_20.json`, `analyze.json` |
| **Q5** sàn | ngoài kho: **0** câu bị trả lời (cả 3 bên); điều kiện (3 lượt, 2 judge thước an toàn, ngữ cảnh = đáp án mẫu): **0 ý "trái"** ⇒ 0 đảo cảnh báo. D02: 1 ý "không có" trong đáp án mẫu nhưng **có trong kho** (`grep_kb.sh`) — giới hạn của cách chấm bằng đáp án mẫu | `chuoi_r1/an_toan_dk/` |
| **Q6** đổi chủ đề | Completeness tụt **0** / 3; câu tìm mang đối tượng cũ **0** / 5 | như trên |
| **Q7** câu tìm lượt sau (theo dõi) | 10 / 24 lượt có câu tìm model viết chứa đủ tên đối tượng; model chỉ tự gọi `tim_kho` ở 12 / 24 lượt (lần tìm đầu = câu gõ, chứa đủ tên 11 / 24). Q4 đạt nên không thử M2 | `may.json` |
| **Q9** theo dõi | tuyến đúng mọi lượt 3 bên; `khan_cap` 0; `tim_kho` model TB 0,34 / lượt (nho); USD nho 0,0219 / doc_lap 0,0220 / tran 0,0163 (25 chuỗi). Q2 vòng 1: định tuyến đưa S20 sang `khan_cap` lần 2 (lần 1 ở B2); vòng 2: `tro_ly_hue` | — |

## 5. Khoá (plan §4 — trước phần kín)

**Khoá 13:17 03/11/2026** — nhánh `p9-b3` **`46008ed`** (đã push). sha256 (12): `ANSWER_SYSTEM_INSTRUCTIONS` `81d3040cf53f` · `ROUTER_INSTRUCTIONS` `fb4e1aa7f8fe` (= B1) · `ROUTER_HISTORY_NOTE` `62f8197730ad` · `ASSISTANT_HISTORY_NOTE` `798f6af34f26` · `ASSISTANT_TOOL_NOTE` `4cba5621ee48` (= B2) · `TOOL_LIMIT_TEXT` `0f64fe52619c`; `backend/config/settings.yaml` `c18aa9872a6f`; chấm `data/phase_9/b3/tools/cham_chuoi.py` `6bcd64e6bc1c`.
Không chỉnh lời dặn D3 trên đã thấy (0 / 3 vòng): mọi quyết + sàn đã thấy đạt ngay vòng đầu — chỉnh thêm chỉ tăng rủi ro khớp bộ nhỏ.
**Phần kín:** C chạy `chuoi chuoi_sealed.jsonl --ben nho|doc_lap|tran --khong-in-chu` đúng commit khoá + chấm (judge do C gửi, cùng prompt / thủ tục; thước an toàn 2 judge cho `hoi_tiep_dieu_kien`); B chỉ nhận số đếm Q3–Q6 + sha.

## 6. Lệch, lỗi, giới hạn

- **Lệch Q8 (b):** lượt Q2 (`generate`) không có trường "usage − builder" ⇒ không có số Q8 cho Q2; có ở pilot nhớ + chuỗi.
- **Lệch thủ tục judge Q2 vòng 2:** brief của B thiếu dòng "ghi `case_index`" ⇒ file điểm Golden không có trường này; B ghép lại theo thứ tự dòng (436 / 436 khớp số mục mỗi lô, bản gốc `q2v2_judge/golden/judge/raw/`), **không đổi điểm**.
- **Q2 chạy 2 vòng** (plan cho ≤ 2) ⇒ tiền Q2 ≈ 0,192 so ước 0,08; A nới trần B3 0,30 ⇒ **0,40** (dừng > 0,37).
- Đáp án mẫu `hoi_tiep_dieu_kien` dùng làm "ngữ cảnh" cho thước an toàn ⇒ ý đúng theo kho nhưng ngoài đáp án mẫu bị gắn "không có" (D02) — đọc kèm kho.
- Mẫu nhỏ (20 lượt quyết 2, 3 + 3 lượt sàn) — 0 lỗi trên n câu không chứng minh tỉ lệ 0 (spec §9).
- NOT RUN: phần kín, Q10 cổng, bước 8 giao diện, M2 / "chỉ nhớ câu hỏi" (không cần — Q3 / Q4 đạt).

## 7. Tiền B3 (giá đủ, cộng `usd` từng dòng)

Q2 vòng 1 ≈ 0,086 + S20 sinh lại 0,0009 + S10 / S04 sinh lại 0,0051 · thử nhanh vòng 2 0,0068 · pilot 10 0,0029 · 208 câu 0,0844 · S09 / S26 sinh lại 0,0059 · pilot nhớ 0,0027 · chuỗi đã thấy 3 bên 0,0602 ⇒ **≈ 0,255 USD** (trần 0,40, dừng > 0,37). Judge: quota Claude.

**Giải thích ngắn:** B3 cho chatbot nhớ 3 lượt gần nhất trong một cuộc trò chuyện (server giữ, cookie mang mã); cờ còn tắt tới khi có giao diện. Câu dặn D6 bản hẹp chặn đúng lỗi "thêm lưu ý an toàn không có nguồn" (S20) mà không làm chatbot dè dặt — bản đầu làm tăng từ chối và bỏ cả lời khuyên có nguồn. Trên 25 chuỗi đã thấy, nhớ hội thoại làm câu hỏi tiếp kiểu "chùa đó…" trả lời đủ hơn rõ (+0,65 / 5 điểm) mà không trả lời câu ngoài kho hay đảo cảnh báo; chờ phần kín của C để quyết giữ.
