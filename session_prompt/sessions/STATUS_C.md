# STATUS C — cập nhật 13:14 27/10/2026 (phiên 27/10; sắp kết phiên — User sẽ khởi động lại A / B / C)

Terminal: `hue-rag-5b` (27/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi. A = `hue-rag-5f`, B = `hue-rag-31` (trực tiếp).
User 08:41 27/10: C làm việc trực tiếp với A, báo cáo cho A; việc A giao = "làm đi". **Quyền phiên 27/10 hết hạn cuối phiên** (C commit + push `p82-r1`, `c59-log`).
Bản STATUS trước khi viết lại (gồm bảng việc 26/10, file private 25/10): `git show c81e45e:session_prompt/sessions/STATUS_C.md`.

## Đang khai báo / đang làm

- **Không còn file nào C đang khai báo trong working tree chung.** Worktree của C: không còn (`/tmp/c_r1`, `/tmp/c_lat`, `/tmp/c_c59` đã gỡ). Server tạm: không còn.
- (C61 xong 13:19 27/10/2026 — xem bảng.)

## Chờ người khác

- **C60** (code log `/api/chat`): nhánh `origin/c59-log` `cc70124` (code `2270723` + report `c59_log_token_implementation.md`) — **chờ B review** ⇒ A merge + 4 chỗ báo cáo. C không merge.

## Đã làm 27/10 (mã việc A giao)

| Mã | Việc | Kết quả | File / commit |
|---|---|---|---|
| C46 | plan R1 (`reasoning_effort="none"`) + chạy | plan bản 2 `8e76e77e0448` (B55 2 vòng; A duyệt `78a5f05`). Chạy: **kém hơn — phạm sàn ở pilot** (câu 168 trả lời vòng). 0,0049030 USD. B58 ready, A đóng `d665a5b` | `phase_8_2_r1_plan.md`; `origin/p82-r1` `63a472f` |
| C47 | đối chiếu yêu cầu ChatGPT "mục tiêu sản phẩm" | 1 sai (SD 0,8 s), 2 gây hiểu lầm (BM25 chỉ chấm 30 đoạn; luna 10 vs 30 đoạn), 4 thiếu — qua tin nhắn | — |
| C48 | lỗi "nói chắc sai về số" ở B1 dev | 4 / 68 câu có số bị cờ (= R4), cả 4 là phép tính đúng; mẫu 10 / 10 đúng ⇒ 0 lỗi thấy được | `c48_so_trong_cau_tra_loi.md` (`afa8350`) |
| C49 | review report K3 | ready 0/0/3 — kém hơn đúng luật (1 / 40 lỗi luna), 9 / 0 trên 39 tính lại khớp | `phase_8_2_k3_review.md` |
| C50 | review plan K3b (+ vòng 2) | ready 0/0/4 → vòng 2 ready (`57dad7150322`) | `phase_8_2_k3b_plan_review.md` |
| C51 | khả thi kiểm sau sinh "trả lời vòng" | luật L2 bắt 160 + 168 (sau khi chỉnh trên chính 2 câu), 0 cờ ở B1; 7 / 10 cờ là câu có ích ⇒ A gác (`8dad0cd`) | `c51_kiem_sau_sinh_kha_thi.md` |
| C52 | review report K3b (n + m) | ready 0/0/3 — n kém hơn, m tầng tìm tốt hơn (tạm) 9 / 0 | `phase_8_2_k3b_review.md` |
| C53 | review phụ lục K3b-m (vòng 1–3) | vòng 1 M-1: API trả 500 cho mọi lỗi citation ⇒ T6 mâu thuẫn T2; vòng 2 ready (+ m-4 regex); vòng 3 ready (`2a3b22b38ab6`, 120 về theo dõi — sàn 120 là gợi ý m-2 sai của C) | `phase_8_2_k3b_m_answer_plan_review.md` |
| C54 | review K3b-m khâu trả lời | ready 0/0/2 — kém hơn đúng luật (T3 5 > 4); khuyên không chạy A/A biến thể | `phase_8_2_k3b_m_answer_review.md` (`e952fa3`) |
| C55 | `BAO_CAO_SINH_CAU_TRA_LOI_API.md` bản 10 | A review, sửa 1 chỗ tả câu quá cụ thể | `bao_cao_he_thong/…` |
| C56 | đề xuất sửa nhãn đoạn đúng | 120 thêm 2 khoảng, 156 thêm 1, 143 = lỗi cách đếm (tiêu đề mục); test chưa quyết | `c56_de_xuat_sua_nhan.md` (`7a4e86c`); private `data/phase_8_2/gold_fix_proposal_2710/` |
| C57 | review B65 latency đầu–cuối | đạt; câu "K3b-m +3 s" sai mức ⇒ ≈ +4,6–4,7 s (cùng câu, cùng harness) — qua tin nhắn | — |
| C58 | latency theo khâu `/api/chat` | gọi model ≈ 98 %; dư 1,5 s = bộ câu (token ra ~1,8×), giải thích được bằng token ra; B67 sửa nhãn ⇒ sha `d76fb10e0c5a`. 0,0074884 USD | `c58_latency_theo_khau.md` (`8b830a2`) |
| C59 | plan log token + thời gian mỗi câu | bản 2 `7f1456a1ae55` (B68 2 vòng ready, `2ddd65d`); User duyệt | `c59_log_token_plan.md` |
| C60 | code C59 | xong, chờ B review (mục trên). Test 32 passed / 4 cần key (mốc 31 / 4); cổng 8014 đạt; 0,0003236 USD | `origin/c59-log` `cc70124` |
| C61 | review `gold-v2` (B69) | ready 0/0/3 minor — v2 = v1 + đúng 3 khoảng C56; luật tiêu đề chỉ đổi câu 143; C tự đếm lại 22 → 24, 31 → 33, thắng 9 / thua 0; gold_draft vẫn `bab707b9ab22` | `gold_v2_review.md` (untracked, A commit); script `data/phase_8_1/tools/c61_recount_check.py` |

## Phiên sau C làm gì đầu tiên

Mở theo `START_SESSION.md`, báo A, **chờ A giao việc**. Có thể tới lượt C: sửa C60 nếu B review có finding (nhánh `c59-log`); việc tiếp theo sau B0 (merge B1) do A giao.

## Câu hỏi / thắc mắc còn treo (cho A / User)

- C56 / C61: `gold-v2` ready chờ A merge; m-1 nên ghi bẫy "file kết quả trước 27/10 tính bằng nhãn v1" trước khi merge; 3 câu test (95, 130, 138) chưa quyết.
- C59 / C60: `FileHandler` không xoay vòng (~400 byte / câu) — xem lại khi deploy.
- Giữ từ trước: C32 `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index (loại ở lần build lại?); guide 5 `:65`
  còn nhắc MiniLM; `guides/full_corpus_rag.md` bước 4b dùng mã B-06 khác nghĩa.

## File private C tạo 27/10 (không commit)

`data/phase_8_2/r1_plan/`, `data/phase_8_2/r1/`; `data/cai_tien_tung_khau_2026-10-26/{c48,c51}/`; `data/phase_8_2/k3/tools/c49_check.py`, `data/phase_8_2/k3b/tools/c52_check.py`,
`data/phase_8_2/k3b/answer/tools/c54_{check,read}.py`; `data/phase_8_2/gold_fix_proposal_2710/`; `data/phase_8_2/latency_2710/c58/` (gồm `instrumentation.diff` đo tạm);
`data/phase_8_2/c60_gate/`. **C chưa đọc nội dung câu kín.**

## Ý cải tiến (chỉ là ý, chưa thử)

- Nhãn context `[Nguồn n]` ↔ prompt `[n]` (C-09): thử khớp nhãn, đo lỗi "không ngoặc số" + Completeness.
- Biết token suy luận / câu (C60 đã ghi) ⇒ đo được câu nào "suy nghĩ dài" trước khi thử rút gọn câu trả lời (C58: thời gian sinh ≈ 1,16 s + 11,5 ms / token ra).

## Đã học / bẫy gặp (đầu vào vòng cải tiến)

- **27/10 C53 / C46:** sàn "API 500" phải đối chiếu đúng nhánh trả lỗi trong `chat.py` — **mọi** `CitationIntegrityError` đều là 500, không riêng "no citation" (plan R1 của C và
  B55 đều bỏ sót).
- **27/10 C53 m-2:** nhãn đoạn đúng chỉ đánh dấu **một** chỗ cho mỗi fact ⇒ `*_gold_frac` 0 không có nghĩa context không có fact; đọc nội dung trước khi đề xuất sàn "context 0 fact"
  (gợi ý của C làm pilot bản 2 dừng oan, 0,0048 USD).
- **27/10:** script dựng lại context chạy từ working tree `main` (context 5) phải truyền `max_documents=10` cho mốc B1 / K3b (suýt kết luận sai trên 5 đoạn).
- **27/10 (A nhắc):** report tracked tả câu dev ở **mức loại câu**, không nêu chủ đề cụ thể cạnh `case_index`.
- **27/10 C60:** code ghi log đọc thẳng `generated.model` làm một test từ đạt thành 500 (generator thay thế chỉ có `.text`) ⇒ chạy lại **đủ file test chạm** sau khi sửa, so với mốc chạy
  **trước** khi sửa — nhờ mốc mới thấy ngay test nào từ đạt thành hỏng.
- **27/10:** đừng ghi giờ ước kiểu `12:1x` vào file (C suýt ghi ở plan C59; sửa bằng `date` trước khi báo sha).
- **26/10:** commit report **ngay khi viết xong, tách riêng** khỏi `push` (auto mode chặn lệnh ghép trong worktree `/tmp`); push từ working tree chung.
- **26/10:** đã báo sha thì không sửa plan nữa; ghi chú đến sau ⇒ lần sửa kế hoặc báo A trước.
- **26/10:** khi đổi mốc, đếm lại trần / cỡ mẫu trên **đúng mốc** trước khi chạy.
- Giữ: mọi lệnh Python `uv run …` (kể cả script tạm); quét trùng là bước riêng trước `git add`; `grep` là ugrep (regex dài lỗi "complexity" ⇒ dùng Python); giờ lấy bằng `date`;
  repo public (không chép kho / Golden / câu kín / tên dự án khác vào file tracked).

## Tiền

Paid API C phiên 27/10: **0,0127150 USD thật** (R1 pilot 0,0049030 + C58 0,0074884 + C60 cổng 0,0003236; token từ usage). Phiên tối 26/10: 0,0026861 USD thật. Quota Claude Code:
không dùng sub-agent.
