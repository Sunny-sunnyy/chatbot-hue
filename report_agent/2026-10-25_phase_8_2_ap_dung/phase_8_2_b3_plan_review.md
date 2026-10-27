# Review: Phase 8.2 B3 — plan mốc cuối trên câu kín (B72)

Decision: **changes_requested** (0 blocker / 2 major / 4 minor) — vòng 1
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-86`)
Date: 14:18 27/10/2026 (`date`)
Plan: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md` bản 1, sha `9d60b16b63da` (C tính lại từ file lúc đọc và lúc ghi review)
Cách review: `WORKFLOW.md` §9.1 — chỉ dựa trên mục "Căn cứ để review" của plan (4 mục) + lệnh chỉ đọc. C **không** đọc `STATUS_B.md` hay tin nhắn
của B về plan, **không** mở nội dung câu kín (chỉ `ls` tên file trong `knowledge-base-hue/evaluation/phase_8_1/`).

## 1. Phạm vi đã review

- Plan: toàn bộ (210 dòng).
- Spec 8.2 (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`): §3 mục 7–8, §5 B3, §6 mục 4, §7, §10.2 (đủ cả mục, gồm "Sàn chung" và dòng
  "Test … = không làm hỏng"), §10.6 Q2.
- `skills/run-experiment/SKILL.md` §1 (khuôn, sàn / mức tụt, "hai dòng tiêu chí không đếm cùng một lỗi", cỡ mẫu).
- `Session_Prompt.md` §5 (câu kín, giữ mù); `backend/evaluation/full_corpus_eval.py:322-382` (`answer_case`, `run_generation`); `backend/api/routes/chat.py:181-189`.
- Lệnh chỉ đọc để kiểm khẳng định của plan: `git diff f26485b 576f84e -- backend/evaluation/full_corpus_eval.py backend/config/settings.yaml`;
  `git show f26485b:` cho `full_corpus_eval.py`, `retrieval/full_corpus.py`, `llm/citations.py`, `config/settings.yaml`; `git merge-base` với `1e4acd0`, `9e6d371`;
  tính lại phần ước tiền §6. Một tra cứu ngoài gói (để kiểm M-2): `grep "A đã thấy"` trong `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`.

## 2. Findings

### M-1 (major) — luật "câu API trả 500 (citation)" lệch "Sàn chung" của spec mà plan không nói vì sao

- **Vị trí:** plan §4 YAML dòng 117 (`câu API trả 500 (citation)` … `role: tolerance, max_worse: "+1 câu"`) và dòng 129–134 (kết luận "không làm hỏng" = 2 sàn +
  4 mức tụt).
- **Yêu cầu:** spec §10.2 dòng "Test … = **không làm hỏng** (sàn + mức tụt như luật tương ứng)"; "Sàn chung" cùng mục: "**0 câu lỗi kỹ thuật / 500**"; mức tụt
  luật (i): "lỗi citation (validator v2) tăng ≤ 2 câu". Skill `run-experiment` §1 mục 3: sàn / mức tụt đo hành vi production trỏ `file:dòng`, và hai dòng không đếm
  cùng một lỗi (27/10: mức tụt citation chồng sàn 500 qua 3 plan).
- **Bằng chứng:** spec tự có hai câu cho cùng loại lỗi (sàn 0 câu 500; mức tụt citation ≤ +2). Plan chọn cách thứ ba (+1 câu, không phải sàn) — chặt hơn spec
  mức tụt, lỏng hơn spec sàn — nhưng không ghi đang theo câu nào của spec và vì sao. `chat.py:181-189`: mọi `CitationIntegrityError` ⇒ 500, người dùng không thấy
  câu trả lời ⇒ đây là lỗi người dùng nhận, gần với "sàn 500" hơn.
- **Tác động:** nhánh cuối có đúng 1 câu 500 citation nhiều hơn ⇒ plan kết luận "không làm hỏng", đọc theo "Sàn chung" thì "làm hỏng". Tiêu chí quyết mơ hồ
  **trước** khi chạy là đúng loại lỗi mà §9.1 muốn bắt.
- **Tiêu chí đóng:** plan ghi rõ một luật cho 500 citation và câu spec nó theo (sàn 0 câu, hoặc mức tụt ± k câu kèm lý do "sàn chung chỉ áp đợt cải tiến" nếu A
  đồng ý); câu tương ứng ở §4 "Kết luận" sửa theo. Nếu cần A quyết, ghi thành câu hỏi §8 và A trả lời **trước** khi duyệt sha.

### M-2 (major) — bước "A ghi 3 số dòng câu A đã thấy" không làm được mà vẫn giữ mù

- **Vị trí:** plan §2 dòng 39–41 ("A chỉ làm hai việc: ghi 3 số dòng (1..36) của 3 câu A đã thấy … vào `a_seen_lines.json`"); §5 bước 1.
- **Yêu cầu:** `Session_Prompt.md` §5 "người điều phối không đọc nội dung"; spec §3 mục 7 (báo S36 + S33). S33 là **tập quyết** của plan (§4 dòng 97).
- **Bằng chứng:** `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md:42`: "A đã thấy 3 câu kín (**User trích**)" — A biết nội dung 3 câu, không có nguồn nào trong
  gói nói A biết **số dòng**. Muốn ra số dòng, A phải đối chiếu với `sealed_official.jsonl` = mở file câu kín. Plan không nói số dòng lấy từ đâu.
- **Tác động:** hoặc A vi phạm giữ mù để tạo S33, hoặc S33 không dựng được ⇒ tập quyết không có.
- **Tiêu chí đóng:** plan ghi nguồn có sẵn của 3 số dòng (nếu có, trỏ file), hoặc đổi cách: ví dụ A ghi lại 3 câu đã thấy (A đã biết nội dung) vào một file private,
  **người chạy** (được mở câu kín) khớp ra số dòng bằng script chỉ in số dòng, rồi ghi `a_seen_lines.json`. Cách nào cũng được, miễn A không mở file câu kín.

### m-1 — judge sub-agent trả lời về cho người chạy có thể chứa nội dung

- **Vị trí:** plan §2 dòng 45–48 (người chạy không đọc feedback judge; sub-agent chỉ `Read` prompt + lô, `Write` file điểm).
- **Bằng chứng / tác động:** tin trả lời cuối của sub-agent hiện thẳng trong ngữ cảnh người chạy; plan không giới hạn nội dung tin đó ⇒ có thể lộ câu / feedback.
- **Tiêu chí đóng:** brief judge ghi "tin trả lời cuối chỉ gồm: đường dẫn file điểm + số dòng đã chấm, không chép câu hỏi / câu trả lời / feedback".

### m-2 — nhiễu A/A chỉ lấy nhánh context 10; mức "≤ 3 câu tụt" chưa nói rõ là chặt hơn "A/A + 3"

- **Vị trí:** plan §4 YAML dòng 114–115; dòng 143–145.
- **Bằng chứng:** cột `noise` chỉ dùng A/A context 10 (B1 ↔ G2.1a: 1 câu tụt / 176); nhánh đầu là context 5, nhiễu plan ghi 16 / 176 câu đổi điểm (7B Run 1 ↔ 2)
  ⇒ quy về 33 câu ≈ 3 câu đổi (hai chiều). Spec §10.2: mức tụt = **A/A + 3**. Plan đặt tuyệt đối 3 — chặt hơn nếu tính cả nhiễu context 5.
- **Tác động:** không sai luật (chặt hơn được phép), nhưng tăng khả năng kết luận "làm hỏng" do nhiễu; người đọc report sau không biết đây là lựa chọn có chủ đích.
- **Tiêu chí đóng:** một câu ở §4: ngưỡng 3 là tuyệt đối, chọn chặt hơn A/A + 3 vì …; hoặc đổi thành "A/A + 3" với A/A ghi bằng số của cả hai nhánh.

### m-3 — danh sách khác nhau giữa `f26485b` và `576f84e` (plan §1) thiếu đổi import; vài dòng "Sàn chung" không áp mà không ghi

- **Bằng chứng:** `git merge-base --is-ancestor f26485b 1e4acd0` = đúng ⇒ nhánh đầu còn cách nạp module cũ (`full_corpus_eval.py` tự chèn `sys.path`, `retrieval/full_corpus.py`
  import `backend.core…` — gói 1b sửa chuyện module nạp hai lần). C kiểm: `answer_case` / `run_generation` đúng là giống nhau; `settings.yaml` đúng chỉ đổi đường file
  điều kiện (nhánh đầu đọc `config/full_corpus_conditions.json` có trong chính commit đó) + bỏ tham số Representation B; citation nhánh đầu đúng chỉ nhận `[n]`
  (`git show f26485b:backend/llm/citations.py:9`). T1 ở cả hai worktree (§5 bước 3) đã che phần tìm kiếm.
  "Sàn chung" §10.2 còn có "0 câu mất đoạn đúng khỏi context" và "câu 120, 168 vẫn từ chối" — không áp cho câu kín (không có nhãn đoạn đúng; không phải câu dev).
- **Tiêu chí đóng:** §1 thêm một dòng "import / module nạp (gói 1b) khác — T1 hai nhánh kiểm"; §4 một dòng "hai sàn chung kia không áp, vì …".

### m-4 — "không lọc độ tự nhiên" dựa trên giả định, trong khi có file nhãn

- **Vị trí:** plan §4 dòng 102–103.
- **Bằng chứng:** `knowledge-base-hue/evaluation/phase_8_1/sealed_realism.jsonl` tồn tại (C chỉ thấy tên file). Quyết định User 24/10 21:40 (số chính bỏ câu không
  tự nhiên; câu kín không tự nhiên thì thay) **không nằm trong gói căn cứ** ⇒ C không kiểm được giả định "mọi câu kín đều tự nhiên".
- **Tiêu chí đóng:** plan trỏ nguồn cho giả định (quyết định / report nói câu kín đã qua lọc tự nhiên), hoặc để script đếm số câu nhãn ≠ natural (chỉ in số đếm) —
  0 ⇒ giả định đúng; > 0 ⇒ báo cả hai số.

Ghi chú nhỏ (không cần vòng sửa): dòng 135 ghi "spec §10.2 Q2" — câu Q2 nằm ở §10.6 (§10.2 chỉ trỏ tới).

## 3. Cách người kiểm chạy lại thật

Không chạy harness (plan chưa có code; `b3.py` chưa tồn tại). Chỉ lệnh Git chỉ đọc ở §1 và tính lại tiền:
291.269 × 0,1 / 1M + 15.585 × 0,5 / 1M = 0,0369 USD / 176 câu ≈ 0,00021 USD / câu; 36 × (0,000133 + 0,00021) ≈ 0,0123; pilot 10 × 0,000343 ≈ 0,0034.

## 4. Kết quả quan sát

- Đúng: hai nhánh và cách dựng (§1, §3) khớp spec §3 mục 8 + §5 B3; ước tiền khớp (trên); trần 0,03 USD ≤ phần còn của trần 8.2; harness ghi từng dòng, từ chối ghi
  đè, ghi meta cả khi lỗi, không retry / fallback (skill §3); câu hỏi gửi **nguyên văn** (không qua NFC của bộ nạp Golden ở `full_corpus_eval.py`) ⇒ đo đúng việc
  NFC của chatbot cuối; hai dòng "lỗi kỹ thuật" (`error`) và "500 citation" (`citation_error`) không đếm cùng lỗi — khớp `full_corpus_eval.py:339-363`.
- Lệch: M-1, M-2 (quyết định / giữ mù); m-1 → m-4 (rõ ràng, nhiễu, giả định).

## 5. Giới hạn hoặc phần chưa chạy

- Không kiểm bảng cỡ mẫu spec §10.3 ("4 thắng / 0 thua ⇒ p 0,026") — ngoài gói căn cứ.
- Không đọc câu kín, `sealed_realism.jsonl`, `g0_6_manifest.json` (ngoài gói; manifest plan dùng cho số loại câu).

## 6. Decision và bước tiếp theo

`changes_requested`: B sửa M-1, M-2 (và các minor nếu muốn) thành **bản 2**, báo sha mới; C kiểm phần sửa (chỉ các mục trên + đường bị ảnh hưởng) trước khi A
duyệt sha. Câu hỏi §8 của plan (người chạy, nhánh thứ ba, A/A câu kín) là việc của A — C không có ý kiến chặn; với §8.3, nếu A giữ "không A/A" thì m-2 càng nên
ghi rõ.

## Vòng 2 — kiểm phần sửa (bản 2, sha `27e75be5ed44`)

Decision vòng 2: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor) — A duyệt sha `27e75be5ed44` được.
Date: 14:25 27/10/2026 (`date`). Cách làm giữ như vòng 1: chỉ gói "Căn cứ để review" + quyết định A ghi ở `CURRENT_HANDOFF.md` mục B72 (14:20); không đọc STATUS_B / tin
của B về nội dung plan; không mở câu kín. C tính lại sha từ file: `27e75be5ed44`. Ngoài gói chỉ mở `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md:92-95`
(plan mới trích để làm nguồn cho độ tự nhiên).

| Finding vòng 1 | Bản 2 | Kết quả |
|---|---|---|
| M-1 luật 500 citation | Theo quyết định A (khác tiêu chí đóng gốc của C, A có quyền chọn): câu 500 citation chấm Completeness = Accuracy = 1 ở **cả hai nhánh**, gộp vào TB + số câu tụt; số 500 chỉ theo dõi (dòng 125–128, 140–144); sàn = OOS 0 + lỗi kỹ thuật 0 sau **một** lần chạy lại đúng câu (124, 145–146); lý do không theo "Sàn chung" ghi rõ (143–144); kết luận "2 sàn + 3 mức tụt" khớp YAML (151). Không còn hai dòng đếm cùng lỗi. | **đóng** |
| M-2 số dòng câu A đã thấy | Người chạy B (được mở câu kín) khớp từ `sealed_user_feedback_private.md`, lệnh `match-seen` chỉ in số dòng + số khớp; A không đọc câu kín lẫn file ghi câu (42–47); không đủ 3 ⇒ chỉ S36 + ghi chú, kết luận theo S36 (47, 108). A không phải mở gì. | **đóng** |
| m-1 tin trả lời judge | Brief ghi "chỉ đường dẫn file điểm + số item" (55–56). | **đóng** |
| m-2 nhiễu A/A | A/A = 2 (context 5: 16/176 × 33 ≈ 3,0 hai chiều ⇒ 1,5 tụt; context 10: ≈ 0,19 — C tính lại khớp), mức tụt = A/A + 3 = 5 theo spec §10.2 (125–126, 165–166). | **đóng** |
| m-3 import 1b, sàn không áp | Dòng 33–34 (preflight in `__file__`), 147–148. | **đóng** |
| m-4 độ tự nhiên | Nguồn spec 8.1 G0.4 (C mở: dòng 92–95 đúng nói văn nói + User duyệt mẫu + có dấu đầy đủ); `preflight` đếm nhãn ≠ natural, chỉ in số đếm; > 0 ⇒ báo thêm tập bỏ câu không tự nhiên, kết luận vẫn S33 (111–114). | **đóng** |
| Ghi chú §10.6 Q2 | Dòng 154. | **đóng** |

### m-5 (mới, minor) — dòng đầu bản 2 vẫn ghi giờ bản 1

- **Vị trí:** dòng 3 `Date: 2026-10-27 14:10 +0700 (`date`) · Bản 2` — 14:10 là giờ bản 1 (A quyết M-1 / M-2 lúc 14:20, sau đó mới có bản 2).
- **Tác động:** không đổi tiêu chí; chỉ sai mốc giờ ghi (luật `WORKFLOW.md` §6 giờ bằng `date`). **Không cần sửa trước khi duyệt sha** — sửa thì là bản mới.
  Ghi đúng giờ bản 2 trong report B3 hoặc lần sửa sau.

### Hệ quả cần A biết (không phải finding)

Với n ≈ 30 câu trong phạm vi, **một** câu 500 citation mới ở nhánh cuối mà nhánh đầu chấm 5 = −4 điểm ⇒ TB ≈ −0,13 < −0,1 ⇒ "làm hỏng" chỉ từ dòng TB. Tức theo
quyết định M-1, thực tế mỗi câu 500 mới (trên câu nhánh đầu làm tốt) gần như là một sàn. Ngược lại, câu 500 ở nhánh đầu (bộ kiểm v1 chỉ nhận `[n]`) tính là thắng
cho nhánh cuối — đúng là "đo trên đường production lúc đó" như §1 ghi, nhưng phần thắng đó đến từ citation v2, không phải context 10 + NFC.
