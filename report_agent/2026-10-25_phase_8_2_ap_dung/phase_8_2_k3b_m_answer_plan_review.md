# Review: Phase 8.2 §10 K3b-m — phụ lục plan "lượt sinh + judge"

Decision: **changes_requested** (0 blocker / 1 major / 3 minor) — T1–T7 đúng nguyên văn K3 plan, cỡ mẫu và tiền tính lại khớp; nhưng T2 và T6 mâu thuẫn nhau
vì API trả 500 cho **mọi** lỗi citation
Người kiểm: C (Claude Opus 5.5, `hue-rag-5b`) · Việc: C53 (A giao 27/10)
Date: 2026-10-27 10:08 +0700 (`date`)
Canonical guide: K3 plan `0a6370204c7d` §3, §4; K3b plan bản 2 `57dad7150322` §2, §4 "Tầng trả lời"; spec 8.2 §10.2 (`cd910c4c4169`); `run-experiment` §1.6, §3
Plan được review: `phase_8_2_k3b_m_answer_plan.md` sha **`84d4aaf0ad04`** (C tính từ file lúc bắt đầu và lúc ghi review: không đổi)

## 1. Phạm vi đã review

Chỉ dựa trên "Căn cứ để review" của plan (WORKFLOW §9.1); không đọc STATUS_B. Đọc hết plan; K3 plan §3 (dòng 61) và §4 (dòng 66–112, có số dòng); K3b plan bản 2 §2,
§4 dòng 178–184; report K3b `origin/p82-k3b` §4.3–§4.4; spec §10.2; skill `run-experiment`. Để kiểm điểm (2) C mở thêm `backend/api/routes/chat.py` và
`backend/llm/citations.py` ở `811d25d` (code production mà T2 nói tới).

Tính lại bằng lệnh chỉ đọc, 0 USD: `/tmp/c53_check.py` từ `backend/` (`PYTHONPATH=. HF_HUB_OFFLINE=1 uv run python …`) đọc `data/phase_8_2/b1/judge/` (qua `b1.scored_rows`
của `811d25d`), `split.json`, `keep_realism`, `data/phase_8_2/k3b/{m_l1.merged,m_test}.jsonl`, `data/phase_8_2/k3/base_{dev,test}.jsonl`; context builder production đếm token.

**Ghi chú về M-1:** C thấy điểm này khi đọc `chat.py` trong lúc review; sau đó B (người viết) cũng tự báo cùng điểm qua tin nhắn. Finding dưới đây dựa trên code, không dựa
trên tin của B.

## 2. Findings

### M-1 (major) — T6 "citation v2 ≤ +2, khác no-citation" mâu thuẫn với T2 "lỗi kỹ thuật / 500 = 0" (và sàn chung spec §10.2)

- **Vị trí:** plan §2 bảng T2, T6 và đoạn "Hai chỗ phụ lục ghi rõ cách đếm" gạch T6.
- **Bằng chứng:** `backend/api/routes/chat.py:125-135` (`811d25d`) bắt **mọi** `CitationIntegrityError` của `select_cited_sources` và trả **HTTP 500**. `llm/citations.py`
  ném lỗi này ở ba chỗ: câu từ chối kèm citation (`:25`), không citation (`:29`), id citation lạ (`:33`). Lỗi citation v2 mà T6 đếm (`g2_generate.citation_error(…,
  single_source_policy=False)`) gọi đúng hàm đó ⇒ **mọi** lỗi v2, không riêng "no citation", đều là một câu người dùng nhận 500.
- **Tác động:** đọc đúng chữ, T2 (sàn 0) đã bao mọi lỗi T6 ⇒ T6 vô nghĩa; đọc theo đoạn "Hai chỗ ghi rõ", T6 cho phép tới 2 câu 500 ⇒ trái sàn chung spec §10.2
  ("0 câu lỗi kỹ thuật / 500"), mà spec đứng trên plan (`Session_Prompt.md` §2). Hai cách đọc cho kết luận khác nhau đúng ở trường hợp có 1–2 lỗi citation. Mốc B1 có
  **0** lỗi v2 (dev + test), nên sàn 0 có nghĩa.
- **Gốc:** cách đếm này mượn từ K3 plan (dòng 88 + 92, cùng có từ trước) và từ plan R1 bản 2 (C viết, B55 M-1 (4) chấp nhận). R1 đã dừng nên không ảnh hưởng kết quả
  nào; nhưng lỗi định nghĩa có từ plan của C.
- **Tiêu chí đóng:** định nghĩa T2 bằng máy = `row["error"] is not None` **hoặc** `row["citation_error"] is not None` (= mọi câu production trả 500 / 502), sàn **0**,
  kèm `file:dòng` của `chat.py`; T6 thành **theo dõi** (đếm theo dạng `:25` / `:29` / `:33` để biết vì sao), hoặc bỏ. Ghi rõ đây là sửa cho khớp spec §10.2, A duyệt cùng sha.

### m-1 — "trần 6 câu" của W1 chỉ là câu thắng ở tầng tìm, không phải trần thay đổi Completeness

- **Bằng chứng (C tính trên `b1/judge/`):** 6 câu khớp plan — 38 (C4), 48 / 67 / 167 (từ chối, C1), 70 (C3), 159 (C3); 156 đã 5; 17, 85 không tự nhiên; test: 20, 130 không tự
  nhiên, 95 đã 5. Nhưng luna đổi tập top-10 ở **mọi** câu có đoạn đúng (và gọi mới cho 121 câu không có đoạn đúng), nên Completeness có thể đổi ở cả **18** câu dev chính
  đang < 5 ở B1 (và giảm ở bất kỳ câu nào).
- **Tác động:** không đổi luật (W1 chỉ theo dõi); chỉ để người đọc không hiểu "6" là giới hạn trên của mọi thay đổi.
- **Tiêu chí đóng:** ghi "6 câu có lý do biết trước để tăng (đoạn đúng mới vào context); câu khác cũng có thể đổi theo cả hai chiều".

### m-2 — 120 có thể giữ làm sàn: ở K3b-m context câu này vẫn 0 fact

- **Vị trí:** T8 (120 / 168 theo dõi, theo K3 plan dòng 85).
- **Bằng chứng:** report K3b §4.4 + C kiểm: 120 `top10_gold_frac` 0 ở L1 và L2 (lý do spec §10.2 cho sàn "120, 168 vẫn từ chối" — context không có fact — vẫn đúng ở 120); 168
  lên 0,5 (một nửa fact vào context) nên theo dõi là đúng. R1 / R2 vấp đúng dạng "trả lời vòng" ở các câu loại này.
- **Tiêu chí đóng:** A chọn: (i) giữ như K3 plan (cả hai theo dõi), hoặc (ii) 120 thành sàn "vẫn từ chối" (chặt hơn, ghi trước). C nghiêng (ii); không bắt buộc.

### m-3 — gọi đồng thời 4 với hai lần gọi / câu: nên ghi trước cách xử lý 429 / timeout

- **Vị trí:** §3 "Song song: `CONCURRENCY` 4"; §5.3.
- **Bằng chứng / tác động:** mỗi câu gọi luna (~5 s) rồi sinh; K3 / K3b gọi luna **tuần tự**, B1 chỉ song song lượt sinh. `max_retries=0` ⇒ một 429 / timeout là lỗi kỹ thuật
  ⇒ T2 ⇒ "kém hơn" vì hạ tầng, không vì chất lượng. Plan đã nói đúng là "lỗi kỹ thuật" (không fallback) — chỉ thiếu một câu ghi trước rằng 429 / timeout cũng vậy, và
  ghi `e2e_ms` khi gọi đồng thời có độ trễ khác production một người dùng (§6 đã nêu phần sau).
- **Tiêu chí đóng:** thêm một câu ở §5.3: "429 / timeout = lỗi kỹ thuật, dừng, ghi nguyên văn; không chạy lại cả lượt mà không có A". Hoặc hạ concurrency khi rerank.

## 3. Kết quả quan sát — năm điểm A hỏi

**(1) T1–T7 đúng nguyên văn K3 plan §4 — ĐẠT.** C đối chiếu theo số dòng: dòng 87 (OOS 0 / 18) = T1; 88 (lỗi kỹ thuật / 500, 176) = T2; 89 (Completeness 4 / 6) = T3; 90
(Accuracy 4 / 5) = T4; 91 (từ chối nhầm +1 / +1) = T5; 92 (citation v2 +2) = T6; 98 (`output_tokens` +20 %) = T7; 85 (120 / 168 theo dõi) = T8. "Luật giữ" = K3 plan
bước 3 (dòng 106). Phát lại thứ tự = K3 plan dòng 61 và K3b plan dòng 182. Ngưỡng A/A: dev C 1/86/1, A 1/86/1; test C 3/38/0, A 2/38/1 ⇒ max + 3 = 4 / 4 / 6 / 5 — khớp.

**(2) T5 / T6 có chồng nhau không — T5 không chồng; T6 chồng T2 (M-1).** T5 = câu chính B1 `refusal` false → K3b-m true: câu từ chối là câu chuẩn, không citation,
validator nhận (không lỗi) ⇒ không chồng T2 / T6. T6 ↔ T2 chồng hoàn toàn theo code production (M-1).

**(3) Cỡ mẫu trên mốc B1 — ĐẠT (kèm m-1).** 6 câu dev chính có chỗ tăng có lý do biết trước, test chính 0 — C tính lại khớp. Vì luật giữ chỉ đòi "không hỏng" (T1–T7) và W1
là theo dõi, ghi trước "chưa thấy lợi có thể xảy ra, không có nghĩa là không có lợi" là đủ. Đồng ý với A: W1 chỉ theo dõi — muốn biến W1 thành điều kiện thì trần 6 câu
cần ≥ 5 / 0 trên n 88 (C38), gần như chắc "chưa rõ".

**(4) Phát lại thứ tự L1 có chắc giống lượt đã đo không — ĐẠT với kiểm 55 / 55 đã ghi.**
- Phát lại = thứ tự luna đã lưu + `apply_contract` trên pool 30 dựng lại từ `service.search` production. Pool tất định (M2' K3b khớp K3 40 / 40, test 15 / 15) và cùng
  `limit` 30 (bẫy HNSW `Project_Status.md` §8 không chạm). Kiểm `top_chunk_ids` = file gốc ở **55 / 55**, lệch ⇒ dừng (§5.1) — đủ để chắc câu phát lại dùng đúng 10 đoạn
  đã đo; không cần gọi luna lại cho 55 câu đó.
- 121 câu gọi mới: không có đoạn đúng nên tầng tìm chưa từng đo chúng; một lần gọi mới là một mẫu, không có gì để "giống". Nhiễu luna ở các câu này đi thẳng vào T3–T5
  (A/A + 3 chỉ tính nhiễu khâu sinh) — đúng chiều thận trọng: người dùng thật cũng gặp nhiễu đó. §6 đã ghi giới hạn "chỉ một mẫu L1".

**(5) Tiền ước 0,107, trần 0,13 — ĐẠT.** 121 × 0,000586 = **0,0709**; sinh 120 × 0,000204 + 56 × 0,000221 = **0,0369**; cộng **0,1078**. Token context của 10 đoạn K3b-m gần bằng
mốc: C dựng lại bằng context builder production trên 55 câu phát lại — TB **918** so với **916** token (1,002×) ⇒ ước tiền sinh = B1 là hợp lý. Trần 0,13 = ước + 21 %; tổng
8.2 ≈ 0,137 + 0,13 ≈ 0,27 < 0,5. Đồng ý giữ 176 câu: bỏ 29 câu không tự nhiên chỉ tiết kiệm ≈ 0,023 nhưng đổi tập của T2 / T6.

## 4. Giới hạn

- Chưa có harness `k3b_answer.py` để review (plan §3 mô tả); `K3bService` / phát lại cần review cùng report.
- C không chạy lệnh có phí; số ước dựa trên usage thật của K3b-m và B1.

## 5. Decision và bước tiếp theo

**changes_requested** — B sửa M-1 (định nghĩa T2 = mọi câu production trả 500 / 502, sàn 0; T6 theo dõi), cân nhắc m-1..m-3, báo sha bản 2; C kiểm phần sửa. Các điểm
còn lại (T1, T3–T5, T7, phát lại + kiểm 55 / 55, cỡ mẫu, trần 0,13, giữ 176 câu, W1 theo dõi) đủ để A duyệt sau khi sửa.

## Vòng 2 — kiểm phần sửa (bản 2 sha `92a8a7eb4177`, C tính từ file; 10:14 27/10/2026 +0700, `date`)

Cách kiểm: `git diff HEAD -- phase_8_2_k3b_m_answer_plan.md` (bản 1 `84d4aaf0ad04` ở `fbd72af` → bản 2); thử regex W2 mới trên chuỗi tự viết và trên `b1_dev.jsonl`
(`uv run python` inline từ `backend/`, 0 USD). Quét trùng review: 0.

| Finding | Đóng? | Ghi chú |
|---|---|---|
| M-1 | **đóng** | T2 = `error` **hoặc** `citation_error` ≠ null, sàn 0, kèm `chat.py:124-135`, `citations.py:25,29,33` (thêm vào căn cứ mục 3); T6 → theo dõi theo dạng; luật giữ bỏ T6 khỏi mức tụt (T3–T5, T7); đoạn "nói thẳng" ghi lý do + cùng hiểu lầm ở R1 bản 2 |
| m-1 | **đóng** | W1: "6 câu có lý do biết trước; câu khác đổi được cả hai chiều (18 câu < 5)" |
| m-2 | **đóng** | A chọn: 120 = sàn "vẫn từ chối" (T8, luật giữ, dừng 3b); 168 theo dõi |
| m-3 | **đóng** | §5.3: 429 / timeout = lỗi kỹ thuật, dừng, ghi nguyên văn, không chạy lại khi chưa có A |

**Ngoài phạm vi — không đổi** (đối chiếu diff): T1, T3, T4, T5 (ngưỡng + cách đếm), T7, mốc B1, A/A, cách phát lại (L1 / `m_test`, kiểm 55 / 55), trần 0,13, 176 câu, judge cùng lượt
mù, các bước chạy. §8 ghi đúng bốn chốt của A.

### m-4 (mới, minor) — cách tách câu W2 bản 2 vẫn tách rời `[n]` khi có khoảng trắng trước nó (". [1]")

- **Bằng chứng (C thử):** regex `([.!?](?:\[(?:Nguồn )?\d+\])*)\s+` giữ được `.[2] Câu sau` (đúng như B kiểm trên 168 / 160), nhưng với `… được nêu. [1]` (dấu cách trước
  `[1]`, cuối dòng) thì `[1]` thành mẩu riêng và câu trước bị đếm là **không citation**. Trên `b1_dev`, **43 / 99** câu trả lời có mẩu chỉ-citation bị tách như vậy. Regex
  cũng chỉ nhận `[Nguồn n]` viết hoa, không có khoảng trắng trong ngoặc — khác `CITATION_PATTERN` của production (không phân biệt hoa thường, cho phép khoảng trắng).
- **Tác động:** W2 chỉ theo dõi ⇒ không đổi luật giữ; nhưng có thể đếm nhầm "câu không citation kiểu nguồn không có…" ở các câu kết bằng ". [n]" nếu câu đó có cụm phủ định
  (C51 gặp đúng dạng này ở B1 câu 25).
- **Tiêu chí đóng:** cho phép khoảng trắng trước / trong citation và gắn mẩu chỉ-citation vào câu trước, ví dụ `([.!?](?:\s*\[\s*(?:nguồn\s*)?\d+\s*\])*)(?:\s+|$)` với
  `re.IGNORECASE`, hoặc dùng lại hàm tách câu đã kiểm của C51 (`data/cai_tien_tung_khau_2026-10-26/c51/c51_scan.py` `sentences`); kiểm lại trên B1 câu 25. Sửa được ở
  harness mà không cần bản plan mới (W2 không vào luật), nhưng ghi trong report.

**Decision vòng 2: ready_for_user_confirmation** — A có thể ghi "duyệt bản sha `92a8a7eb4177`"; m-4 sửa trong harness trước khi chạy.
