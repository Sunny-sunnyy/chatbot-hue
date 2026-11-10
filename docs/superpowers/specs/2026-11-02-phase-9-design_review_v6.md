# Review: Phase 9 — spec bản 6 (trợ lý dạng agent có công cụ)

Decision: **ready_for_user_confirmation** ở vòng 3 (bản 8 `82127aabcb5b`); vòng 1 bản 6 và vòng 2 bản 7: changes_requested — xem cuối file
Người kiểm: sub-agent review độc lập (Claude, ngữ cảnh mới, A giao)
Date: 13:49 02/11/2026 (`date`)
Canonical guide: `docs/superpowers/specs/2026-11-02-phase-9-design.md`
Implementation report: không có (việc chỉ tài liệu — spec chờ User duyệt)

## 1. Phạm vi đã review

- **File review:** spec bản 6, 383 dòng, sha256 12 ký tự **`fbb2853aa90c`** — [Chạy] `sha256sum … | cut -c1-12` khớp đề bài. Spec đang là bản sửa trong working tree (chưa commit), đúng sha.
- **Căn cứ đã đọc** (đúng bảng "Căn cứ để review" của spec):
  - [Đọc] `session_prompt/CURRENT_HANDOFF.md` mục "Phase 9 đổi hướng" + "Quyết định sau nghiên cứu" (bản working tree, chưa commit — dòng 103–121);
  - [Đọc] `data/nghien_cuu_phase_9_2026-11-01/agent/a_sa2.md` §3 (3a, 3b R1–R15, 3c, 3d); `a_sa1.md` §2.0–§2.5; `a_sa3.md` §2a–§2d, §3a;
  - [Đọc] `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` §3.1–§3.3;
  - [Đọc] code `HEAD`: `backend/llm/generator_openai_full_corpus.py:98-103, 133-144, 184-190`; `backend/llm/grounded_answer.py` (cả file); `backend/api/routes/chat.py:35-53, 223-400`; `backend/retrieval/full_corpus.py:419`; `backend/evaluation/full_corpus_eval.py:169`; `frontend/src/markdown.js:7-14`.
- **Ngoài căn cứ, chỉ để đối chiếu số spec dẫn:** `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md:99, 133-136, 141, 166-167` (số Đủ 3,50 / 4,92, câu theo ngày). Không đọc `STATUS_*.md`, tin nhắn của người viết, `*sealed*`, `.env`, nội dung kho.
- **Danh sách kiểm:** `skills/risk-gated-agent-review`, `skills/agent-design-review`, `skills/agent-security-review`, `skills/run-experiment` §1, §4.

## 2. Findings

Tóm tắt: **0 blocker · 10 major · 8 minor.** Phần lớn major sửa được bằng chữ trong spec (chốt cơ chế / sửa luật đo), không cần đổi hướng.

### M1 (major) — B7: luật kết luận ghi trước luôn ra "có giá trị"

- **Vị trí:** §5 B7, dòng 260–262.
- **Yêu cầu:** đề bài mục 4 — "so RAG cũ ↔ agent cuối Phase có kết luận ghi trước"; `run-experiment` §4 (kết luận phải có thể ra "kém hơn / chưa rõ").
- **Bằng chứng:** "có giá trị" khi không phạm sàn **và** (hơn mốc ở ≥ 1 nhóm chất lượng **hoặc** làm được ≥ 3 việc mới mà mốc 0 / n). Ba việc mới (trò chuyện, nhớ tên, hỏi lại) mốc RAG 1–8 **về cấu trúc không làm được** ⇒ vế "hoặc" đúng ngay khi B1 + B3 + B4 được giữ. Dòng 262 "không đạt ⇒ agent chỉ thêm tính năng" mâu thuẫn: "chỉ thêm tính năng" chính là điều kiện "đạt" ở dòng 261.
- **Tác động:** kết luận chính của luận văn được quyết trước khi đo; nhánh kết quả âm không bao giờ xảy ra.
- **Tiêu chí đóng:** tách hai kết luận ghi trước, báo cả hai, không gộp bằng "hoặc": (i) **"tốt hơn ở hỏi đáp"** = vượt nhiễu, CI 95 % > 0 ở nhóm chất lượng nào (ghi trước nhóm + cách sửa khi nhiều nhóm, vd Holm); (ii) **"thêm được việc mới"** = mỗi việc mới có ngưỡng chất lượng riêng (vd nhớ tên đúng ≥ x / y, hỏi lại đúng ≥ 8 / 10) chứ không chỉ "mốc 0 / n".

### M2 (major) — Cổng gọi web dựa vào ý định của model, code không thấy được

- **Vị trí:** §5 B6 dòng 237; §3 dòng 82.
- **Yêu cầu:** `agent-design-review` §2 ("không dựa vào cờ mô hình tự khai"); đề bài mục 2 (chia việc code ↔ model, làm được trên SDK).
- **Bằng chứng:** cổng code đòi "lượt chưa có câu trả lời từ kho (trợ lý **định** trả từ chối)". Khi `tra_web` là công cụ trong vòng lặp của SDK, lúc công cụ được gọi code chỉ thấy: tuyến, nhãn chủ đề do định tuyến đưa, số lần đã gọi. "Định từ chối" chỉ là việc model đã chọn gọi `tra_web` ⇒ cổng tự quy về "model muốn". a_sa3 §2d mục 4 nói cổng thật phải là "model trả câu từ chối chuẩn" rồi mới đi web (luồng P3, thêm một lượt).
- **Tác động:** cơ chế chính giữ "kho trước" không làm được như viết; tiền / độ trễ / mức tụt "web gọi nhầm ≤ 2 %" phụ thuộc cơ chế chưa chọn.
- **Tiêu chí đóng:** spec chọn một và ghi hệ quả: (a) `tra_web` **không** là công cụ của model — trợ lý trả `tu_choi` (đầu ra có cấu trúc) ⇒ code kiểm điều kiện (tuyến, chủ đề, không khẩn cấp) ⇒ code gọi Serper ⇒ một lần gọi model thứ hai viết mục web; hoặc (b) giữ là công cụ, cổng code chỉ gồm điều kiện code thấy được (liệt kê), và bỏ chữ "trợ lý định trả từ chối".

### M3 (major, bảo mật) — Nhớ hội thoại × tra web: hai đường rò

- **Vị trí:** §5 B3 dòng 191–193; §5 B6 dòng 232; §10 Q2 (a) dòng 352.
- **Yêu cầu:** a_sa2 R9 (lệnh sống qua nhiều lượt), R7 (dữ liệu cá nhân vào truy vấn web); `agent-security-review` mục 1, 5; quyết định User 13:29 "tên là dữ liệu cá nhân".
- **Bằng chứng:**
  1. B3 giữ "câu hỏi + **câu trả lời cuối**" và nói "không giữ chữ web". Nhưng Q2 (a) — phương án C khuyên — cho model viết mục "Từ web" **trong câu trả lời** ⇒ chữ suy từ web nằm trong câu trả lời cuối ⇒ quay lại prompt ở lượt sau qua lịch sử. Mâu thuẫn trong chính spec.
  2. Truy vấn `tra_web` do model viết, model thấy lịch sử có tên người dùng. Rào 2 chỉ bỏ số điện thoại / email. Ý "truy vấn chỉ dựa trên câu hỏi lượt này" của a_sa2 R7 bị bỏ. Tên ⇒ Serper / Google = đường ra mới cho dữ liệu cá nhân, spec không rào và không đo.
- **Tác động:** ca web độc lọt một lần có thể ảnh hưởng mọi lượt sau trong phiên; tên người dùng có thể đi tới bên thứ ba.
- **Tiêu chí đóng:** (1) ghi luật lưu: phần web của câu trả lời (mục "Từ web" / mã `[w n]`) **không** vào lịch sử — code cắt trước khi lưu — hoặc ghi rõ lựa chọn khác + lý do; thêm ca đo nhiều lượt "lượt 1 có web độc, lượt 2 câu thường" (a_sa2 R9) vào bộ B6; (2) truy vấn web: code dựng / kiểm từ câu hỏi lượt này (hoặc model viết nhưng không thấy lịch sử), và bộ B6 có ≥ 3 chuỗi "đã nêu tên rồi hỏi câu cần web" ⇒ đếm truy vấn chứa tên = 0 (đếm trên vết tại máy của lượt đo, không log chữ ở runtime).

### M4 (major) — B2: mốc V0 không phải bậc đã giữ; A/A đặt sai bậc; chưa có cỡ mẫu

- **Vị trí:** §5 B2 dòng 170–185; §4 dòng 103, 130; §9 dòng 329.
- **Yêu cầu:** `run-experiment` §1 mục 2 (một thay đổi mỗi biến thể), mục 6 (cỡ mẫu trước khi chạy, Holm khi nhiều biến thể), §3 (A/A cho khâu có LLM); §4 spec "mỗi bậc so với bậc trước đã giữ".
- **Bằng chứng:**
  1. Bậc đã giữ trước B2 là B1: `tro_ly_hue` = đường RAG 1–8, **chưa có công cụ** (dòng 154). V0 ở B2 = câu gốc **+ trợ lý được gọi `tim_kho` thêm ≤ 2 lần** (dòng 175). Vậy "bật vòng lặp công cụ" và "cách viết câu tìm" là hai biến, mà biến thứ nhất **không** được so với B1. Dòng 185 "kết quả âm ⇒ giữ V0, trợ lý không có `tim_kho` thêm" — cái được giữ thực chất là B1, không phải V0.
  2. "A/A mới cho đường agent ở bậc đầu" (dòng 130) và "A/A mới ở B1" (dòng 329): ở B1 chưa có vòng lặp công cụ; đường agent nhiễu hơn xuất hiện từ B2. Mức tụt S-G "câu tụt ≤ A/A + 3" từ B2 trở đi cần A/A của đường có công cụ.
  3. Tầng 1 "rẻ — chỉ lần gọi định tuyến" (dòng 177) không đúng cho V2 (câu tìm do trợ lý viết ⇒ phải chạy trợ lý) và không tính các lần `tim_kho` thêm của V0 / V1 / V3.
  4. Chỉ số quyết "Completeness câu nhiều nguồn CI 95 % > 0, test không ngược chiều" trên 18 câu (8 câu yếu) chia dev / test, 3 biến thể: spec không đếm số câu có thể đổi và số câu phải thắng; không nêu Holm.
- **Tác động:** có thể giữ vòng lặp công cụ mà không có bằng chứng nó hơn B1; ngưỡng mức tụt dùng nhiễu của đường khác; kết quả B2 rất dễ "chưa rõ" mà không ghi trước.
- **Tiêu chí đóng:** (1) thêm biến **V0'** = câu gốc, **không** `tim_kho` thêm (= B1) làm mốc; bước "bật `tim_kho` thêm" so V0' riêng hoặc ghi rõ là biến thứ hai; (2) A/A cho đường có công cụ chạy ở B2 (giữ A/A định tuyến ở B1 nếu cần), ghi số lượt; (3) ghi tầng 1 của V2 tốn gì; (4) ghi cỡ mẫu theo `run-experiment` §1 mục 6 (số câu có thể đổi trên mốc, số câu phải thắng, Holm) — thiếu thì ghi trước "kết quả có thể chưa rõ".

### M5 (major) — B1 gộp năm thay đổi, luật giữ / gỡ từng phần chưa có; mẫu số câu theo ngày lệch báo cáo

- **Vị trí:** §5 B1 dòng 152–166; §1 dòng 41.
- **Yêu cầu:** `run-experiment` §1 mục 2–3 (một thay đổi; mỗi chỉ số định nghĩa: tập nào, n bao nhiêu); §4 spec luật giữ / gỡ.
- **Bằng chứng:** B1 = định tuyến + trò chuyện + ngoài phạm vi + khẩn cấp + ngày + H4c, hai chỉ số quyết (định tuyến ≥ 90 %; từ chối nhầm câu theo ngày giảm ≥ 3 / 12). Không ghi: một phần đạt, phần kia không thì giữ gì (vd ngày đạt, định tuyến 85 %). Bộ tuyến ~60 câu không ghi phần đã thấy / kín bao nhiêu, mà quyết dùng "kín không ngược chiều". Câu theo ngày: spec "5 / 12", "12 câu cũ"; báo cáo ghi bộ **15** câu, mốc từ chối nhầm **6 / 14** (30/10) và **5** câu trong kho lượt 01/11 (`10_BAO_CAO_DANH_GIA.md:99, 141`; plan đo cuối §3.3). H4c không có tiêu chí nào.
- **Tác động:** kết quả B1 có thể không quyết được; ngưỡng "≥ 3 / 12" có thể tính trên mẫu số sai.
- **Tiêu chí đóng:** bảng giữ / gỡ cho từng phần B1 (định tuyến; ngày; H4c; khẩn cấp) — phần nào gỡ độc lập được bằng cờ; ghi chia đã thấy / kín của bộ tuyến; sửa mẫu số câu theo ngày theo đúng bộ đã đo (ghi nguồn); H4c có test code (dòng có đúng khi nguồn thuộc 3 thư mục, không có khi không).

### M6 (major) — Tiền ước bỏ sót lượt hồi quy bắt buộc ⇒ tổng ~0,8 USD thấp, Q4 dựa trên số này

- **Vị trí:** §4 dòng 114; §5 B1 164, B3 202, B4 213, B5 223, B6 249; §8 dòng 306–319; §10 Q4.
- **Yêu cầu:** đề bài mục 5 (tiền ước so trần); luật User: ước USD trước, trần phiên ≤ 1 USD.
- **Bằng chứng:** §4: "mỗi bậc chạy đủ 176 + 32 câu", câu rủi ro chạy 3 lượt. Thêm công cụ `hoi_lai` / `lich_trinh` / `tra_web` đổi prompt (mô tả công cụ) của **mọi** câu `tro_ly_hue` ⇒ phải chạy lại hồi quy. Nhưng B4 0,03 · B5 0,02 · B6 0,05 USD không đủ cho một lượt 208 câu. Ước của người kiểm (suy ra từ a_sa3 §2b, chưa đo): ~0,00034 USD / câu (P2) + định tuyến ~0,00007 ⇒ ~0,0004 USD / câu ⇒ một lượt 208 câu ≈ 0,08 USD, thêm 2 lượt cho 32 câu an toàn ≈ 0,03 ⇒ **≈ 0,1 USD / bậc chỉ cho hồi quy**. B1 tự tính: 278 câu × 2 lượt × 0,0003 = 0,17 (spec ghi 0,15). Tổng hợp lý ≈ **1,05–1,15 USD** trước khi tính câu web (P3 ≈ 0,00075 / câu).
- **Tác động:** Q4 (b) 0,8 USD chắc vỡ; Q4 (a) 1,2 USD chỉ dư ~5–15 %, không phải "dư 50 %" như dòng 371; User chọn trần trên số sai.
- **Tiêu chí đóng:** bảng §8 tính lại mỗi bậc gồm: bộ của bậc + hồi quy 176 + 32 (số lượt) + lượt lặp câu rủi ro + A/A; hoặc ghi luật khi nào được bỏ hồi quy (vd hash prompt không đổi). Q4 viết lại theo số mới.

### M7 (major, thiết kế agent) — Streaming + lõi chung khi có công cụ chưa được thiết kế

- **Vị trí:** §3 dòng 73–84, 123; §5 B0 dòng 147.
- **Yêu cầu:** `agent-design-review` (streaming khi có công cụ, chữ đầu hiện lúc nào); plan đo cuối §3.1 (Golden đo qua `answer_case` dựa trên việc route stream và bộ đánh giá **dùng chung lõi**).
- **Bằng chứng:**
  1. Hôm nay chữ hiện dần bằng cách lọc sự kiện `response.output_text.delta` rồi tách trường `answer` của JSON (`chat.py:368-371`, `AnswerTextStream`). Spec đổi đầu ra trợ lý thành `tra_loi | hoi_lai | tu_choi` và thêm lượt gọi công cụ (không có chữ) — không nói chữ được tách thế nào, lượt nào được stream.
  2. Mọi câu thêm một lần gọi định tuyến **trước** khi có chữ (không stream được); spec không ghi chữ đầu dự kiến cho từng tuyến (a_sa3 §2c có số cho P1 / P3).
  3. Spec không nói vòng lặp agent + định tuyến nằm ở đâu để `answer_case` (bộ đánh giá, `Runner.run`) và `/api/chat/stream` (`Runner.run_streamed`) đi **cùng** đường. Nếu chỉ route stream có agent, S-G đo đường khác người dùng thấy.
  4. Rút lại chữ khi trích dẫn hỏng (`chat.py:309-313`) hôm nay chỉ cho `[n]`; spec thêm `[w n]` nhưng không nói rút lại áp cả mã web.
  SDK 0.19.4 có đủ mảnh ([Chạy] đọc `.venv`: `run_streamed(..., error_handlers=…)` `agents/run.py:375-388`; `StopAtTools` `agent.py:143`; `parallel_tool_calls` `model_settings.py:113`; `tool_output_guardrails` `tool.py:484`) ⇒ làm được, nhưng spec phải chốt cách.
- **Tác động:** phần người dùng thấy và độ đúng của bộ đo đều phụ thuộc chỗ chưa chốt; dồn hết vào "kiểm ở B0" là để plan nhỏ quyết kiến trúc.
- **Tiêu chí đóng:** một đoạn ở §3: (a) định tuyến + agent nằm trong lõi chung (`grounded_answer` hoặc module mới) mà cả `answer_case` lẫn route stream gọi; (b) lượt nào stream, sự kiện trạng thái nào cho lượt công cụ; (c) cách tách chữ từ đầu ra nhiều kiểu (hoặc chỉ `tra_loi` được stream); (d) rút lại áp cho cả `[n]` và `[w n]`; (e) chữ đầu dự kiến mỗi tuyến (dẫn a_sa3 §2c).

### M8 (major) — Hai ý trong danh sách User chọn 13:29 bị thu hẹp không ghi lý do

- **Vị trí:** §2 dòng 62; §5 (không bậc nào); §5 B6 dòng 248.
- **Yêu cầu:** đề bài mục 1 (không tự thu hẹp); `CURRENT_HANDOFF.md` "Quyết định sau nghiên cứu" — mẫu khoá gồm "soát chữ web", "thẻ công cụ trên giao diện".
- **Bằng chứng:** "thẻ công cụ trên giao diện" chỉ xuất hiện ở bảng §2, không ở bậc nào (chỉ có dòng trạng thái "đang tìm…" ở §4 dòng 123). "Soát chữ web" thành **có điều kiện** ("có ≥ 1 ca độc lọt ⇒ thêm model thứ hai"); a_sa2 §3d còn nói "0 ca thì vẫn bật trước khi có người dùng thật / deploy" — spec bỏ vế này.
- **Tác động:** User đọc §2 tưởng hai việc này có trong Phase.
- **Tiêu chí đóng:** đặt "thẻ công cụ" vào một bậc (vd B2 cùng giao diện) hoặc ghi "lệch có lý do" + hỏi User; "soát chữ web": ghi rõ là lệch so quyết định 13:29, lý do (tiền / độ trễ), và giữ vế "bật trước khi deploy" ở "Giả định an toàn" §7.

### M9 (major) — Lịch: việc bắt buộc (nhớ) không được che; B2 không có hạn chót

- **Vị trí:** §6 dòng 265–286.
- **Yêu cầu:** đề bài mục 5 (khả thi tới 20/12, luật cắt); quyết định User "nhớ hội thoại **bắt buộc**".
- **Bằng chứng:** B3 (bắt buộc) nằm sau B2 (thí nghiệm khó nhất, 4 biến × 2 tầng), và B3 cần câu tìm đứng một mình cho câu hỏi tiếp — đúng thứ B2 chọn (dòng 169). Luật cắt 1: B2 trễ ⇒ thu nhỏ **B5**, không giới hạn B2. Không luật nào cho B1 trễ (B1 là nền của mọi bậc). Mỗi bậc một tuần gồm plan ⇒ review ⇒ A duyệt ⇒ code ⇒ đo 208 câu + bộ riêng ⇒ judge mù ⇒ review nhánh ⇒ merge.
- **Tác động:** trễ ở B1 / B2 đẩy thẳng vào việc bắt buộc và vào B7 (không cắt, chỉ 5 ngày).
- **Tiêu chí đóng:** thêm (1) hạn chót B2: vd 25/11 chưa chọn ⇒ đóng B2 với phương án đang dẫn trên dev (hoặc V0') và sang B3; (2) luật cho B1 trễ (vd 16/11); (3) ghi "B3 không cắt" cạnh "B7 không cắt", hoặc ghi rõ B3 làm được trên B1 nếu B2 chưa xong.

### M10 (major, an toàn nội dung) — Tuyến trò chuyện không có kiểm cuối, nhưng spec nói "tuyến nào cũng qua kiểm cuối"

- **Vị trí:** §5 B1 dòng 155, 165; §3 dòng 77, 84.
- **Yêu cầu:** sàn "không bịa", "nói chắc sai"; `agent-security-review` mục 3 (giới hạn ở code, không ở lời dặn).
- **Bằng chứng:** dòng 165: "định tuyến bị lừa chỉ đổi tuyến, mà tuyến nào cũng qua kiểm cuối". Kiểm cuối (dòng 84) là kiểm trích dẫn theo sổ nguồn; tuyến `tro_chuyen` không có nguồn ⇒ câu trả lời 0 mã `[n]` qua kiểm một cách rỗng. Chặn "trò chuyện nói thông tin Huế" chỉ là lời dặn (dòng 155). Bộ tuyến có 5 câu "lẫn lộn", không có ca người dùng cố tình lái tuyến.
- **Tác động:** lỗi tệ nhất của dự án (nói chắc sai, không nguồn) có một đường đi không có rào code.
- **Tiêu chí đóng:** sửa câu dòng 165 cho đúng; thêm ~5 ca "lái tuyến" (chữ người dùng đòi coi là trò chuyện rồi hỏi thông tin Huế) vào bộ B1, sàn: 0 câu trả lời trò chuyện chứa thông tin Huế cụ thể (judge hoặc người đọc); hoặc một kiểm code rẻ cho đầu ra trò chuyện (vd có giờ / giá / số ⇒ đổi sang trợ lý) nếu đo thấy lọt.

### m1 (minor) — "code `backend/` không đổi từ `a80e12d`" không đúng chữ

- **Vị trí:** §1 dòng 47. **Bằng chứng:** [Chạy] `git diff --stat a80e12d HEAD -- backend/` ⇒ `backend/api/app.py` (thư mục giao diện build `frontend/dist`, B121) + `test_static_ui.py` đổi; đường trả lời không đổi. **Đóng:** viết "đường trả lời (`llm/`, `retrieval/`, `api/routes/chat.py`) không đổi từ `a80e12d`".

### m2 (minor) — Trùng tên Q1–Q4 và mã nội bộ không giải nghĩa

- **Vị trí:** §2 dòng 67 (Q1–Q4 bản 5) ↔ §10 (Q1–Q4 mới); §5, §8 dùng "Q1", "Q4" cho cả hai. Mã S64, W35, H4c, C106, F1–F4, "TRIPO 6b" không giải nghĩa ở chỗ dùng. **Yêu cầu:** luật User "không mã nội bộ khi không giải nghĩa". **Đóng:** đổi câu hỏi mới thành tên khác (vd P1–P4) hoặc luôn ghi "bản 5"; mỗi mã lần đầu kèm 3–5 chữ nghĩa.

### m3 (minor) — "Bộ đo mới ~100 câu" lệch tổng các bộ con

- **Vị trí:** §4 dòng 132 ↔ B1 158 (~60 + ~22), B3 197 (~40 chuỗi), B4 (15), B5 (5 cặp), B6 242 (~25 + ca độc). Tổng ≈ 170 mục. **Tác động:** công viết câu (người viết ≠ người code) trong tuần 02–08/11 bị đánh giá thấp. **Đóng:** một bảng số câu theo bộ, đã thấy / kín, ai viết, viết tuần nào.

### m4 (minor) — `hoi_lai` vừa là công cụ vừa là kiểu đầu ra

- **Vị trí:** §3 dòng 82–83 ("công cụ … `hoi_lai`" và "đầu ra có cấu trúc: tra_loi | hoi_lai | tu_choi"); B4 dòng 207 (`StopAtTools`). a_sa2 R15 khuyên là kiểu đầu ra; a_sa1 §2.2 khuyên công cụ + `StopAtTools`. **Đóng:** chọn một, ghi lý do.

### m5 (minor) — Căn cứ thiếu cho các ý "A giao"

- **Vị trí:** §2 dòng 68, §4 dòng 115. "S-OOS định nghĩa lại", "6 rào bắt buộc", "so RAG cũ ↔ agent" ghi "A giao C120", nhưng mục C120 trong `CURRENT_HANDOFF.md` không ghi các ý này (chỉ "giao qua tin nhắn"). Đề bài review của A có nêu chúng nên người kiểm coi là đúng ý A. **Đóng:** A ghi ba ý vào mục C120 của handoff (hoặc spec dẫn đúng nơi ghi).

### m6 (minor) — Câu hỏi User §10 chưa đủ hệ quả cho mọi phương án

- **Vị trí:** dòng 339–374. **Yêu cầu:** luật User + `propose-options`: mỗi phương án có hệ quả, khi nào sai, chọn khác mất gì, lý do khuyến nghị. **Bằng chứng:** Q1 (b), (c) không có "khi nào sai"; Q2 (b) không có "khi nào sai"; Q3 (a), (b) không có "khi nào sai" và (a) không nêu lý do khuyên; Q4 (c) không có hệ quả nào; Q4 (a) dựa trên số 0,8 (xem M6). **Đóng:** bổ sung các dòng thiếu; mỗi câu vẫn tick được một ô.

### m7 (minor, mức công) — Cắt bớt đo lặp không có vấn đề quan sát được

- **Vị trí:** §4 dòng 129 ("câu rủi ro chạy 3 lượt" — áp mọi bậc), §3 dòng 94–98 (ba nơi ghi số: `chat_metrics`, dòng kết quả đánh giá, vết tại máy), B3 dòng 201 (S-G / S-AT với nhớ tắt), B6 dòng 243 (benchmark Serper 20 truy vấn).
- **Đề xuất cắt cụ thể:** (1) 3 lượt chỉ cho câu rủi ro **ở bậc đổi đúng đường đó** (khẩn cấp ở B1, web ở B6) + B7; bậc khác 1 lượt + luật "ca mới ⇒ sinh lại 3 lần" sẵn có; (2) vết tại máy = thêm trường vào dòng kết quả đánh giá, không thêm nơi thứ ba; (3) B3: nhớ tắt mà hash prompt giống B2 ⇒ dùng lại số S-G / S-AT của B2, không chạy lại; (4) benchmark Serper chỉ chạy nếu Q3 (giới hạn tên miền) còn mở sau B122.

### m8 (minor, bảo mật) — `session_id` và log

- **Vị trí:** §3 dòng 73; B3 dòng 191. Spec không nói `session_id` có vào `chat_metrics` không. `session_id` nối các dòng log của một cuộc trò chuyện có tên người dùng. **Đóng:** ghi "không log `session_id`" (hoặc chỉ băm), và cách trình duyệt giữ mã (cookie HttpOnly / header) — một dòng.

### m9 (minor) — B5: chỉ số quyết gần như không thể trượt

- **Vị trí:** dòng 222. "User đọc mù 5 cặp kín (mốc ↔ agent)": mốc RAG 1–8 không có công cụ lịch trình nên câu trả lời khác hẳn dạng (khó "mù"), agent gần như chắc thắng. **Đóng:** ghi trước tiêu chí User chấm (đúng luật xếp, hợp người đi cùng, có nguồn) hoặc so với một bản không agent (code xếp + một lần gọi model) — chọn cái rẻ hơn.

## 3. Cách người kiểm chạy lại thật

Chỉ đọc / đếm, 0 USD, không gọi API:
- `sha256sum docs/superpowers/specs/2026-11-02-phase-9-design.md | cut -c1-12` ⇒ `fbb2853aa90c`.
- `grep -n -A2 '^name = "openai-agents"' uv.lock` ⇒ `0.19.4`; `.venv/.../openai_agents-0.19.4.dist-info`.
- `grep` trong `.venv/lib/python3.13/site-packages/agents/`: `error_handlers` (`run.py:218, 388`), `max_turns` (`run_error_handlers.py:53`), `StopAtTools` (`agent.py:143`), `parallel_tool_calls` (`model_settings.py:113`), `tool_output_guardrails` (`tool.py:484`).
- `git show HEAD:<file> | cat -n` cho các file code ở mục 1; `git diff --stat a80e12d HEAD -- backend/`.
- `git grep -n 4d5bbe9e0edc HEAD` (T1 = mốc kết quả tìm 158 câu — `06_BAO_CAO_TIM_KIEM.md:142`).
- `uv run python .githooks/overlap_scan.py docs/superpowers/specs/2026-11-02-phase-9-design.md` ⇒ `0 trùng` (script chỉ in số dòng + loại, không in nội dung).

## 4. Kết quả quan sát

- `file:dòng` spec dẫn **khớp** code HEAD: `_run_config` `tracing_disabled=True`, `trace_include_sensitive_data=False` (`generator_openai_full_corpus.py:98-103`); `Agent` không công cụ (`:133-144`); `max_turns=1` (`:188`); `METRIC_FIELDS` chỉ token, không USD (`chat.py:37-40`); `extra="forbid"` (`chat.py:52`); `retrieval_service.search` (`full_corpus.py:419`); `cost_usd` (`full_corpus_eval.py:169`); `markdown.js:10` cho `href`, mẫu trích dẫn chỉ `[n]` (`:14`).
- SDK 0.19.4 có mọi tính năng spec dựa vào (mục 3) ⇒ "chưa cần nâng bản" hợp lý; streaming khi có công cụ còn là việc thiết kế (M7), không phải thiếu SDK.
- Đúng quyết định User: agent mọi câu, RAG thành công cụ, SDK giữ, định tuyến có cấu trúc, câu tìm là thí nghiệm nhiều phương án, nhớ hỏi + đáp bắt buộc, tiền / tốc độ theo dõi + log USD bắt buộc, web sau 6 rào + cờ, Q1–Q4 bản 5 giữ — **có đủ**; lệch: M8.
- 6 rào a_sa2 §3c: đủ cả 6 trong B6 dòng 230–236; thiếu vế R7 "truy vấn chỉ dựa trên câu hỏi lượt này" và tương tác với nhớ (M3).
- Số Đủ 3,50 / 4,92 khớp `10_BAO_CAO_DANH_GIA.md:133-136`; số câu theo ngày lệch (M5).
- File spec: 0 dòng trùng Golden / kho / câu kín (quét máy); không thấy chi tiết dự án khác của User.

## 5. Giới hạn hoặc phần chưa chạy

- **NOT RUN** mọi lượt model / Serper / server (đề bài cấm API trả phí; review chỉ tài liệu). Số tiền ở M6 là **ước của người kiểm** từ a_sa3 §2b, chưa đo.
- Không kiểm được nhịp làm thật của các bậc trước (không đọc `STATUS_*.md` theo luật review) ⇒ M9 dựa trên khối việc mỗi tuần, không trên số giờ đã đo.
- Kết quả ChatGPT 02/11, B122 ngoài căn cứ / chưa xong ⇒ giá Serper, điều khoản Serper không kiểm.
- `CURRENT_HANDOFF.md` đọc bản working tree chưa commit; sau commit cần chắc dòng 103–121 không đổi.

## 6. Decision và bước tiếp theo

**`changes_requested`** — vòng 1 của bản 6.

Người viết (C) sửa trong một lượt M1–M10 theo "tiêu chí đóng"; minor m1–m9 sửa cùng lượt nếu rẻ, không mở vòng riêng. Ranh giới giữ nguyên: hướng agent, SDK 0.19.4, thứ tự bậc B0–B7, 6 rào, sàn S-AT / S-G. Kiểm lại vòng sau: đọc diff các mục bị sửa + tính lại bảng tiền §8 + quét `overlap_scan.py` lại. Spec chưa sẵn sàng để User duyệt sha.

---

# Vòng 2 — bản 7 `37e306ef40f7`

Decision vòng 2: **changes_requested** (3 major mới, ít việc; 10 major vòng 1 đóng hết)
Date: 14:00 02/11/2026 (`date`) · Người kiểm: như vòng 1.

## V2.1 Phạm vi + cổng

- [Chạy] `sha256sum … | cut -c1-12` ⇒ `37e306ef40f7`, 447 dòng — khớp tin A.
- [Chạy] `uv run python .githooks/overlap_scan.py <spec>` ⇒ `0 trùng`.
- [Đọc] spec bản 7 (cả file, kể cả bảng "Trả lời review"); `CURRENT_HANDOFF.md` mục C120 (dòng 122–130, working tree); căn cứ mới `data/nghien_cuu_phase_9_2026-11-01/agent/b123_sdk_probe.md`; `git show HEAD:backend/llm/generator_openai_full_corpus.py:60-95, 266-270` (cách đọc đầu ra cuối); `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` T3-10 (đối chiếu số Q3a).
- Cùng luật vòng 1: chỉ đọc, 0 USD, không `*sealed*`, không `.env`.

## V2.2 Finding vòng 1 — đóng / chưa

| Finding | Kết quả | Bằng chứng (dòng bản 7) |
|---|---|---|
| M1 B7 luôn "có giá trị" | **đóng** | 274–286: hai kết luận tách, (i) 3 nhóm + Holm, "0 nhóm ⇒ không tốt hơn"; (ii) ngưỡng từng việc. Còn vấn đề phía mốc ⇒ M11 mới |
| M2 cổng web theo ý model | **đóng** | 83–85, 94: điều kiện code thấy được (câu trả lời = câu từ chối chuẩn ∧ tuyến ∧ chưa gọi). Lệch quyết định User ⇒ M13 |
| M3 nhớ × web | **đóng** | 121 (cắt mục "Từ web"), 253 (truy vấn từ câu hỏi lượt này, không lịch sử), 260–264 (ca nhiều lượt + 0 truy vấn chứa tên) |
| M4 B2 | **đóng** | 202 (V0 = B1), 205 (tầng tìm chỉ tốn định tuyến), 208 (cỡ mẫu 12 câu + "chưa rõ ⇒ giữ V0"), 210 (A/A ở B2b) |
| M5 B1 | **đóng** | 186–193 bảng giữ / gỡ từng phần + cờ; 165 bộ tuyến 40 / 20; 42 + 191 mẫu số "12 câu quyết trong bộ 15" khớp plan đo cuối §3.3; 193 H4c có test |
| M6 tiền | **đóng** | 336–348: hồi quy mỗi bậc, A/A, câu rủi ro; tôi cộng lại bảng = 1,213 USD; P4 viết lại 403–411 |
| M7 streaming + lõi chung | **đóng** | 72 lõi chung `assistant.py` cho cả 3 nơi gọi; 103–107; B0 182 kiểm `answer_case` qua lõi chung. Khớp B123 §2: lần gọi công cụ không phát `output_text.delta` ⇒ bộ lọc ở `chat.py:368` dùng tiếp được |
| M8 thẻ công cụ / soát web | **đóng** | 104, 213 (thẻ công cụ ở B2b); 66 + 267 + 331 (soát web ghi "lệch có lý do", luôn bật trước deploy) |
| M9 lịch | **đóng** | 303–309: luật B1 16/11, hạn B2 25/11, B3 + B7 không cắt; 218 B3 làm được trên B1. Còn chỗ phụ thuộc ⇒ M12 |
| M10 trò chuyện | **đóng** | 190 sàn "0 câu trò chuyện chứa thông tin Huế" + 5 ca lái tuyến; 196–197 sửa câu sai |
| m1 | đóng | 45 |
| m2 | đóng | 27–28 bảng mã, P1–P4. Còn vài mã không giải nghĩa (Q3a, S64, F1–F4, N_AA) — không mở lại |
| m3 | đóng | 163–171 |
| m4 | đóng | 91–93 (chọn công cụ + lý do). Còn chỗ đầu ra cuối ⇒ m10 mới |
| m5 | đóng | handoff dòng 126–127 ghi ý A giao |
| m6 | đóng | 368–412: mọi phương án có "khi nào sai" |
| m7 | đóng | 126, 150–151, 159, 225, 268 |
| m8 | đóng | 71, 122, 182 |
| m9 | đóng | 245–246 |

## V2.3 Finding mới (phần sửa)

### M11 (major) — B7: bên RAG 1–8 "dùng lại mốc" không làm được với bộ mới, và lệch thời gian

- **Vị trí:** §8 dòng 347 ("bên RAG 1–8 dùng lại mốc"); §5 B7 dòng 273–275.
- **Yêu cầu:** kết luận (i) của B7 so RAG 1–8 ↔ agent trên **cùng bộ câu, cùng lượt mù**; plan đo cuối §3.1 (hai lượt cách ≥ 1 ngày ⇒ có thể trôi phía nhà cung cấp ⇒ thêm A/A cùng ngày).
- **Bằng chứng:** câu trả lời đã lưu của RAG 1–8 chỉ có cho Golden 176, bộ an toàn 32 và 15 câu theo ngày (lượt 01/11). Phần kín của các bộ mới (chuỗi hỏi tiếp, câu ngày mới…) **chưa bao giờ** chạy trên RAG 1–8 ⇒ nhóm "câu hỏi tiếp" của kết luận (i) không có bên mốc. Với nhóm có mốc, hai bên cách nhau ~7 tuần (01/11 ↔ 14–18/12), mà câu theo ngày tương đối thì đáp án đúng đổi theo ngày chạy.
- **Tác động:** kết luận chính của luận văn có thể so hai lượt sinh khác ngày, hoặc thiếu bên mốc ở một nhóm.
- **Tiêu chí đóng:** B7 sinh lại bên RAG 1–8 (worktree ở commit đầu Phase 9, vd `a80e12d` / tag) **cùng tuần** trên mọi bộ B7, hoặc ít nhất trên các nhóm của (i). Cộng tiền: ~380 câu × ~0,00025 ≈ 0,1 USD vào §8 và P4.

### M12 (major) — B2b bị gỡ / bị cắt thì B4, B5 dựng trên gì

- **Vị trí:** §5 B2b dòng 209–213; luật cắt 1 dòng 304; B4 231, B5 242.
- **Yêu cầu:** `run-experiment` §4 (luật giữ / gỡ rõ); §4 spec "mỗi bậc so bậc trước đã giữ".
- **Bằng chứng:** vòng công cụ (Runner nhiều lượt, `max_turns`, đếm trần, thẻ công cụ, A/A đường có công cụ) xuất hiện lần đầu ở B2b. Luật cắt 1 có thể bỏ B2b; B2b cũng có thể bị gỡ ("chưa rõ"). Nhưng `hoi_lai` (B4) và `lich_trinh` (B5) đều là **công cụ** ⇒ cần đúng vòng đó. Spec không nói: gỡ B2b là tắt riêng `tim_kho` hay tắt cả vòng công cụ; A/A đường có công cụ khi đó chạy ở đâu; thẻ công cụ làm ở đâu. B2b cũng chưa có dòng cỡ mẫu / "chưa rõ ⇒ …" như B2a (dòng 208).
- **Tác động:** B4 có thể vô tình gộp hai biến (bật vòng công cụ + `hoi_lai`), ngưỡng mức tụt không có nhiễu đúng đường.
- **Tiêu chí đóng:** 2–3 dòng: "gỡ B2b = tắt `tim_kho` thêm; vòng công cụ vẫn là hạ tầng"; nếu B2b bị cắt / gỡ thì A/A đường có công cụ + thẻ công cụ chuyển sang B4; B2b có dòng cỡ mẫu và luật "chưa rõ ⇒ …".

### M13 (major) — Ba chỗ bớt quyền tự quyết của model so lời User; chỉ một chỗ ghi lệch, hệ quả chưa đủ để User chọn

- **Vị trí:** §2 dòng 66; §3 dòng 80, 90, 94–96; §5 B2b dòng 209; §10.
- **Yêu cầu:** đề bài vòng 2 mục 3 (chỉ kiểm lý do + hệ quả có đủ để User chọn, không chấm đúng / sai); `propose-options` (hệ quả · khi nào sai · chọn khác mất gì); handoff 11:21 "model tự quyết gọi công cụ (tìm kho, ngày hôm nay, tra web khi kho không có…)".
- **Bằng chứng:**
  1. **Web** — đã ghi lệch (dòng 66), lý do có (94–96). **Thiếu hệ quả:** (a) câu kho chỉ trả lời được một phần không bao giờ đi web (cổng chỉ mở khi câu trả lời **đúng bằng** câu từ chối chuẩn); (b) câu bị từ chối nhầm (mốc 12 / 158) sẽ ra câu trả lời từ web thay vì kho; (c) người dùng thấy câu từ chối hiện dần rồi mới tới mục web (câu từ chối được stream trước khi code biết nó là câu từ chối); (d) câu hỏi tiếp tra web chỉ bằng câu hỏi lượt này ⇒ "còn giá vé ở đó?" ra truy vấn mất chủ ngữ. Phía "để model tự gọi" cũng chưa ghi được / mất gì cho User so.
  2. **Ngày hôm nay** — User nêu là công cụ model tự gọi; spec cho code đưa vào (dòng 90, có lý do a_sa1 §2.2) nhưng **không** ghi ở dòng "lệch có lý do".
  3. **Lần tìm đầu** — code luôn tìm trước (dòng 80); B2b ghi "chính là V2 User nêu" (dòng 209), nhưng V2 bản 6 là "không tìm trước, trợ lý tự gọi `tim_kho`". Phương án đó không còn được đo; spec không ghi bỏ + lý do (a_sa1 §2.1: thêm một lần gọi cho mọi câu).
- **Tác động:** A hỏi User về "web do code gọi" mà User không thấy đủ cái giá; hai chỗ còn lại User không biết là đã đổi.
- **Tiêu chí đóng:** dòng "lệch có lý do" ghi đủ cả ba chỗ. Chỗ web thành câu tick được với hệ quả (a)–(d) ở phía code gọi, và phía model gọi ghi được / mất (dẫn M2 vòng 1: cổng code không thấy được ý định). Để không quá 5 câu hỏi User (A giao, handoff dòng 127), **gộp vào P2** ("ai quyết gọi web + web hiện thế nào") thay vì thêm P5. Sửa dòng 209: bỏ "chính là V2", ghi "V2 thuần (không tìm trước) bỏ, lý do …".

### m10 (minor) — Chỗ "chốt khi có B123": B123 đã trả lời

Dòng 25 và 103 ghi B123 chưa xong. B123 (`b123_sdk_probe.md`, lần gọi model thật, 0,00023 USD) đã trả lời:
- **USD + ms từng lần gọi:** `RunHooks.on_llm_start` / `on_llm_end`, `response.usage` + `cost_usd` (B123 §1) ⇒ ghi vào dòng 127 làm cách log.
- **Chỉ stream câu cuối:** lần gọi công cụ không phát `output_text.delta` (B123 §2) ⇒ bộ lọc hiện có (`chat.py:368`) đủ. Lọc thêm theo mục `message` chỉ là phòng ca chưa thấy.
- **Định tuyến có cấu trúc chạy cùng stream + công cụ** (B123 §3). Bản 7 giữ đầu ra `{answer}` ⇒ **không** phải sửa `ANSWER_PREFIX` như B123 cảnh báo cho kiểu `RoutedAnswer`.
- **`tool_choice="required"`** tự trả về sau lần gọi đầu. Spec không dùng (code tìm trước) — ghi một dòng là đã xét.
- Chỗ B123 **không** trả lời: với `StopAtTools(["hoi_lai"])`, `final_output` là giá trị công cụ trả, không phải `AnswerOutput`. Còn `finish_answer_stream` hiện ép kiểu `AnswerOutput` (`generator_openai_full_corpus.py:269`, `parse_structured_output` ⇒ `GenerationError`). Câu "đầu ra cuối giữ kiểu `{answer}`" (dòng 92) vì thế không đúng ở lượt `hoi_lai` ⇒ ghi cách xử lý (nhánh riêng cho kết quả `hoi_lai`), để plan B4 khỏi bỏ sót.

### m11 (minor) — Cổng web mở cả khi "chạm trần" hoặc lỗi

Dòng 100: hết `max_turns` ⇒ trả **câu từ chối chuẩn**. Dòng 83: cổng web mở khi câu trả lời = câu từ chối chuẩn ⇒ lượt chạm trần / lỗi công cụ cũng đi web, trái "lỗi hạ tầng ≠ không có kết quả" (a_sa2 R8). **Đóng:** thêm điều kiện cổng `outcome` = từ chối bình thường (không `max_turns`, không lỗi công cụ).

### m12 (minor) — Đường web: chữ đầu và số đo

Theo dòng 106, câu từ chối được stream trước rồi mới tới mục "Từ web". Vậy "chữ đầu" ở đường web tới lúc ~2,9 s (chữ câu từ chối), không phải "≈ 5–6 s" như bảng dòng 115. Ngoài ra `chat_metrics.refusal` hôm nay = (câu trả lời == câu từ chối) (`chat.py:100`), nên câu có mục web vẫn ghi là từ chối. **Đóng:** ghi thước chữ đầu cho đường web (chữ câu từ chối hay chữ mục web), và trường log riêng "có mục web".

### m13 (minor) — Chỉ số quyết B2a

- Dòng 207: hai điều kiện nối bằng ";" — chưa rõ phải đạt cả hai hay một.
- "Holm cho ≤ 2 biến" đặt ở khâu trả lời, nhưng khâu này chỉ chạy **một** biến (dòng 206). Holm thuộc tầng tìm.
- Số "12 câu chưa đủ keyword (6 / 18 + 6 / 20)" không kiểm được bằng căn cứ: báo cáo T3-10 ghi riêng câu so sánh "chỉ 2 câu yếu ⇒ không phải hướng tìm", Đủ 4,35. Gộp 20 câu so sánh vào phép thử CI pha loãng nhóm yếu.
- **Đóng:** ghi "và" / "hoặc"; chuyển Holm về tầng tìm; dẫn nguồn số 12 (file:dòng); cân nhắc giữ Completeness trên 18 câu nhiều nguồn.

### m14 (minor) — B7 (ii): ngưỡng "trò chuyện" là sàn, không phải "làm được"

Dòng 280: "0 câu chứa thông tin Huế cụ thể" chỉ cho biết trò chuyện không hại, không cho biết nó làm được việc. **Đóng:** thêm một ngưỡng dương (vd câu chào / cảm ơn / hỏi về trợ lý được đáp tự nhiên, không từ chối ≥ x / y trên phần kín).

### m15 (minor) — Truy vấn web từ câu hỏi lượt này: tên trong cùng câu

Ca đo dòng 261 chỉ có "tên nêu ở lượt **trước**". Người dùng có thể nêu tên ngay trong câu cần web ("mình là X, …"). Code chỉ bỏ số điện thoại / email (dòng 253). **Đóng:** thêm 1–2 ca "tên trong cùng câu" vào bộ B6, hoặc ghi giới hạn này ở "Giả định an toàn".

### m16 (minor, mức công) — 447 dòng: chỗ cắt được (~40 dòng)

- §7 "Rào chính" (321–328) lặp lại §3 + rào B6 ⇒ một dòng trỏ.
- §9 bảng rủi ro (356–362): mọi dòng lặp cách giảm đã có ở §3 / §5 / §6 ⇒ giữ đoạn "Giới hạn".
- §1 "Agent dưới chính sách" (49–52) và §10 "Để bạn tự nói lại" (416–421) nói cùng ý ⇒ giữ một.
- Bảng "Trả lời review" (423–447): xoá sau khi User duyệt (git và file review giữ hồ sơ).
- B1 khẩn cấp "0 câu khẩn cấp vào model (3 lượt)" (192): luật code tất định ⇒ 1 lượt là đủ.

Không thấy cơ chế mới nào làm quá tay. Phần sửa bản 7 phần lớn là **cắt** (bỏ `tra_web` khỏi vòng công cụ, một nơi ghi số, 3 lượt chỉ ở đúng bậc).

## V2.4 Giới hạn

- NOT RUN mọi lượt model / Serper / server (cấm API trả phí). Số B123 là của B (lượt thật, n rất nhỏ); tôi chỉ đọc file, không chạy lại probe.
- Số "12 câu" (m13) không kiểm được: nguồn nằm ngoài căn cứ (file implementation R31).
- Handoff và spec đọc bản working tree chưa commit.

## V2.5 Decision vòng 2

**`changes_requested`** — vòng 2 / tối đa 4.

- Ba major mới đều sửa bằng chữ, không đổi kiến trúc:
  - M11: sinh lại bên RAG 1–8 cùng tuần ở B7 + tiền;
  - M12: 2–3 dòng nói rõ gỡ / cắt B2b thì sao;
  - M13: ghi đủ ba chỗ lệch + gộp vào P2.
- m10–m16 sửa cùng lượt nếu rẻ.
- Vòng 3 chỉ kiểm diff các mục đó + quét `overlap_scan.py`. Nếu chỉ còn minor ⇒ `ready_for_user_confirmation`.
- Ranh giới giữ nguyên như vòng 1.

---

# Vòng 3 — bản 8 `82127aabcb5b`

Decision vòng 3: **ready_for_user_confirmation** (0 blocker, 0 major; 2 minor mới không mở vòng)
Date: 14:18 02/11/2026 (`date`) · Người kiểm: như vòng 1–2.

## V3.1 Phạm vi + cổng

- [Chạy] `sha256sum … | cut -c1-12` ⇒ `82127aabcb5b`, 450 dòng — khớp tin A.
- [Chạy] `overlap_scan.py <spec>` ⇒ `0 trùng`.
- [Đọc] spec bản 8 cả file; `CURRENT_HANDOFF.md` dòng 133 ("User chọn M13", 14:12); `b122_tra_web.md` dòng 8–35, 88 (điều khoản + giá Serper, Brave); `b123_sdk_probe.md` (đã đọc vòng 2).
- Cùng luật: chỉ đọc, 0 USD, không `*sealed*` / `.env`. File `q3a…implementation.md` mà spec dẫn cho số "12 câu" nằm ngoài căn cứ ⇒ không mở, chỉ kiểm chữ khớp nhau (12 / 18 + 14 / 20 đủ keyword ⇒ 6 + 6 = 12 câu thiếu, khớp bản 7).

## V3.2 Finding vòng 2 — đóng / chưa

| Finding | Kết quả | Bằng chứng (dòng bản 8) |
|---|---|---|
| M11 bên RAG 1–8 ở B7 | **đóng** | 284 sinh lại cùng tuần, worktree tag `p9-moc`, nêu lý do; 351 +~0,095 USD (380 × 0,00025) |
| M12 B2b gỡ / cắt | **đóng** | 215–217 "vòng công cụ là hạ tầng", gỡ B2b = tắt `tim_kho` thêm, cắt / gỡ ⇒ A/A + thẻ công cụ sang B4; 219 cỡ mẫu + "chưa rõ ⇒ tắt" |
| M13 lựa chọn User | **đóng — ghi đúng lựa chọn** | handoff 133 ↔ spec 63: ngày luôn vào lời dặn · web do code gọi khi kho từ chối · lần tìm đầu là thí nghiệm có V2 thuần (spec 208, B2a); 64 ghi 4 hệ quả (a)–(d) + được / mất phía "model tự gọi"; 65 "sau Phase 9 thêm công cụ mới" |
| m10 B123 | đóng | 93–94 (nhánh riêng cho `hoi_lai` trước khi ép `AnswerOutput`), 103, 108, 130 |
| m11 cổng khi chạm trần | đóng | 83, 102 |
| m12 chữ đầu web + log | đóng | 118–120, 132 `has_web_section` |
| m13 B2a | đóng | 212 "và", Holm ở tầng tìm; 213 quyết trên 18 câu nhiều nguồn |
| m14 trò chuyện | đóng | 291 ngưỡng dương ≥ 9 / 10 |
| m15 tên trong cùng câu | đóng | 271 (theo dõi), 334 (giả định an toàn) |
| m16 mức công | đóng | 332, 358–360, 49, 432; 450 dòng ≈ trần ~450 A giao; phần thêm là lựa chọn User + P5 (có lý do) |

## V3.3 Phần mới + câu hỏi User

- **P5 / B122:** spec 258, 355, 410–419 khớp B122 (điều khoản Serper 29/05/2024 không nói về dùng cho người dùng cuối / hiển thị / lưu, tự nhận B2B; 2.500 lượt dùng thử; 1 USD / 1.000 lượt ở gói thấp nhất; Brave cấm lưu và cấm dùng kết quả để "đánh giá / benchmark" dịch vụ AI). Đặt web sau W35 và hỏi User là đúng luật.
- **P1–P5 tick được**, mỗi câu một ô chọn, có câu tự kiểm. Hệ quả + "khi nào sai" đủ ở P1–P3, P4 (a)(b), P5 (a). Còn thiếu nhỏ ⇒ m18.
- Không thấy blocker / major mới. Hai minor dưới đây sửa lúc viết plan bậc tương ứng, **không mở vòng 4**.

### m17 (minor) — B2a giữ V2 thuần thì A/A đường có công cụ ở đâu

Dòng 215–217: A/A đường có công cụ nằm ở B2b, hoặc B4 khi B2b bị cắt / gỡ. Nhưng nếu B2a giữ **V2** thì vòng công cụ đã chạy ở khâu trả lời của B2a, và B2b gộp vào V2. Mức tụt S-G ở khâu trả lời V2 ↔ V0 khi đó vẫn dùng N_AA của đường không công cụ. **Đóng (ở plan B2):** ghi "đo V2 ở khâu trả lời ⇒ A/A đường có công cụ chạy tại B2a".

### m18 (minor) — Vài phương án P4 / P5 còn thiếu dòng

- P4 (c) chưa có "khi nào sai"; P5 (b) chưa có "được"; P5 (c) chưa có "khi nào sai".
- P5 (a): phạm vi email hỏi Serper nên khớp lựa chọn P2. Nếu chọn P2 (a), model đọc đoạn trích rồi tóm tắt, không chỉ "hiện link + đoạn trích".
- **Đóng:** A bổ sung khi hỏi User (mỗi lần một câu); không cần bản 9 chỉ vì việc này.

## V3.4 Giới hạn

- NOT RUN mọi lượt model / Serper / server (cấm API trả phí). Số tiền ≈ 1,35 USD là ước, chưa đo; pilot 10 câu đầu B1 ước lại (spec 354).
- Không mở file nguồn của số "12 câu" (ngoài căn cứ). Spec + handoff đọc bản working tree chưa commit.

## V3.5 Decision vòng 3

**`ready_for_user_confirmation`** cho sha **`82127aabcb5b`**.

- Việc rủi ro cao ⇒ A trình User:
  - 5 câu P1–P5;
  - các dòng User chọn 14:12 (§2 dòng 63–65);
  - dòng "lệch có lý do" về soát chữ web (§2 dòng 66);
  - câu "kết quả web cố định qua model thật có hợp luật không mock" (B6 dòng 268).
- User duyệt sha ⇒ A giao B0.
- m17, m18 đưa vào plan B2 và lúc hỏi User. Spec giữ nguyên sha để User duyệt.
