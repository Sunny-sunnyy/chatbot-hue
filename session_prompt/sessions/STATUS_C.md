# STATUS C — cập nhật 14:15 27/10/2026 (đang C64)

Terminal: `hue-rag-86` (phiên mới 13:40 27/10; trước `hue-rag-5b`) · Agent: Claude Opus 5.5 · Vai: thực thi. B = `hue-rag-2d` (B tự báo), A = `hue-rag-51` (A xác nhận) — trực tiếp.
User 13:45 27/10/2026 (phiên mới, nhắc lại 08:41 27/10): C làm việc trực tiếp với A, báo cáo cho A; việc A giao = "làm đi". **Quyền phiên 27/10 hết hạn** (C commit + push `p82-r1`, `c59-log`; paid trong trần từng việc).
STATUS trước phiên này (bảng việc 26/10, file private 25/10): `git show c81e45e:session_prompt/sessions/STATUS_C.md`.

## Đang làm

- **C64** (A giao 14:15 27/10, `CURRENT_HANDOFF.md` → C64; 0 USD trừ cổng ≈ 0,0005; A cần biết mục chưa xong trước 16:15):
  1. review plan B3 (sha `9d60b16b63da`, chỉ dựa "Căn cứ để review"; không đọc STATUS_B / tin B; không mở câu kín) — đang làm;
  2. `dense_ms` làm tròn 1 chữ số + test ghim + cổng ổn định (B review);
  3. đề xuất nhãn 3 câu test 95, 130, 138 (cách C56) — private, không sửa `gold_v2.jsonl`.
- Xong trước trong phiên: C62 (`719417e`), review B71 (ready 0/0/2, `4a10ff6`), C63 (`data/tinh_nang_moi_2026-10-27/c63_can_cu.md`). Tiền phiên ≈ 0,000453 USD (log).

## Đang khai báo sửa (C64, từ 14:15 27/10/2026)

- `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan_review.md` (mới).
- `backend/api/routes/chat.py`, `backend/tests/test_api_chat.py` (mục 2 — làm sau review B3).
- `data/phase_8_2/gold_fix_proposal_2710/` (file mới cho 95 / 130 / 138; mục 3).

## Nhánh của C

- `p82-r1` (`origin/p82-r1` `63a472f`): harness `r1.py` (`d2646e6`) + report R1 — **hồ sơ, không merge** (R1 kém hơn).
- `c59-log` (`2270723` code + `cc70124` report): **đã merge `main` `5100b90`** (A, sau B70 ready). Nhánh cục bộ / remote còn, xóa hay giữ do A.
- (Nhánh cũ `p82-r2` của C — hồ sơ R2, 26/10.)

## Vừa xong (phiên 27/10, mã việc A giao)

| Mã | Việc | Kết quả | File / commit |
|---|---|---|---|
| C46 | plan R1 (`reasoning_effort="none"`, luật (a)) + chạy | plan bản 2 `8e76e77e0448` (B55 2 vòng, A duyệt `78a5f05`). Chạy: **kém hơn — phạm sàn ở pilot** (câu 168 lẽ ra từ chối bị trả lời vòng; OOS 12 / 12 đúng; 0 API 500). B58 ready; A đóng `d665a5b` | `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md`; `origin/p82-r1` `63a472f` |
| C47 | đối chiếu yêu cầu ChatGPT "mục tiêu sản phẩm" (chỉ đọc) | 1 sai (SD 0,8 s), 2 gây hiểu lầm (BM25 chỉ chấm lại 30 đoạn dense; luna 10 vs 30 đoạn), 4 thiếu — gửi A bằng tin | — |
| C48 | lỗi "nói chắc sai về số" ở B1 dev | 68 câu có số, 4 câu bị cờ đều là phép tính đúng; mẫu 10 / 10 đúng ⇒ 0 lỗi thấy được | `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md` (`afa8350`) |
| C49 | review report K3 | ready 0/0/3 — kém hơn đúng luật (1 / 40 lỗi luna), 9 / 0 trên 39 tính lại khớp | `…/phase_8_2_k3_review.md` |
| C50 | review plan K3b (vòng 1 + 2) | ready 0/0/4 → vòng 2 ready (`57dad7150322`) | `…/phase_8_2_k3b_plan_review.md` |
| C51 | khả thi kiểm sau sinh "trả lời vòng" | luật L2 bắt 160 + 168 (sau khi chỉnh trên chính 2 câu), 0 cờ ở B1; 7 / 10 cờ là câu có ích ⇒ A gác (`8dad0cd`) | `…/c51_kiem_sau_sinh_kha_thi.md` |
| C52 | review report K3b (n + m) | ready 0/0/3 — n kém hơn, m tầng tìm tốt hơn (tạm) 9 / 0, 0 / 95 sai hợp đồng | `…/phase_8_2_k3b_review.md` |
| C53 | review phụ lục K3b-m khâu trả lời (vòng 1–3) | v1 changes_requested (M-1: `chat.py` trả 500 cho **mọi** lỗi citation ⇒ T6 mâu thuẫn T2); v2 ready + m-4 regex; v3 ready (`2a3b22b38ab6`, 120 về theo dõi) | `…/phase_8_2_k3b_m_answer_plan_review.md` |
| C54 | review K3b-m khâu trả lời | ready 0/0/2 — **kém hơn đúng luật** (T3: 5 câu tụt > 4); chỉ báo TB tăng; khuyên không chạy A/A biến thể | `…/phase_8_2_k3b_m_answer_review.md` (`e952fa3`) |
| C55 | `BAO_CAO_SINH_CAU_TRA_LOI_API.md` bản 10 | A review, sửa 1 chỗ tả câu quá cụ thể | `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md` |
| C56 | đề xuất sửa nhãn đoạn đúng | 120 thêm 2 khoảng, 156 thêm 1, 143 = lỗi cách đếm (tiêu đề mục); 3 câu test chưa quyết | `…/c56_de_xuat_sua_nhan.md` (`7a4e86c`); private `data/phase_8_2/gold_fix_proposal_2710/` |
| C57 | review B65 latency đầu–cuối (tin nhắn) | đạt; câu "K3b-m +3 s" sai mức ⇒ ≈ +4,6–4,7 s p50 (cùng câu, cùng harness) | — |
| C58 | latency theo khâu `/api/chat` | gọi model ≈ 98 %; dư 1,5 s = bộ câu (token ra ~1,8×); B67 sửa nhãn ⇒ `d76fb10e0c5a` | `…/c58_latency_theo_khau.md` (`8b830a2`) |
| C59 | plan log token + thời gian mỗi câu | bản 2 `7f1456a1ae55` (B68 2 vòng ready, `2ddd65d`); User duyệt | `…/c59_log_token_plan.md` |
| C60 | code C59 | B70 ready 0/0/2; **merge `main` `5100b90`**. Test 32 passed / 4 cần key (mốc 31 / 4); cổng 8014 đạt | `backend/api/routes/chat.py`, `backend/llm/generator_openai_full_corpus.py`, `backend/tests/test_api_chat.py`; `…/c59_log_token_implementation.md` |
| C61 | review `gold-v2` (B69) | ready 0/0/3 — v2 = v1 + đúng 3 khoảng C56; luật tiêu đề chỉ đổi câu 143; C tự đếm lại B1 22 → 24, K3b-m 31 → 33, thắng 9 / thua 0. A merge `a819789` | `…/gold_v2_review.md` (`454292a`) |

(`…` = `report_agent/2026-10-25_phase_8_2_ap_dung/` cho các review 8.2, `report_agent/2026-10-26_cai_tien_tung_khau/` cho C48, C51, C56, C58–C61.)

## Việc dở / câu hỏi cho A (hoặc User qua A)

- **Không có việc dở.** Phiên sau: mở theo `START_SESSION.md`, báo A, **chờ A giao việc** (bước kế của dự án: User đọc cặp mù B0 ⇒ merge B1 context 10 ⇒ đóng 8.2 ⇒ tính năng mới).
- C60 còn hai minor B70 (không sửa): m-1 test khóa danh sách trắng chỉ phủ trường gán **trước** điểm lỗi ngân sách context (trường lạ thêm ở phần sinh / citation chỉ cổng ổn định bắt);
  m-2 `dense_ms` chưa làm tròn 1 chữ số như các trường khác (vô hại) — A quyết có sửa không.
- C60: `FileHandler` không xoay vòng (~400 byte / câu) — xem lại khi deploy.
- C56 / C61: 3 câu test C56 (95, 130, 138) chưa ai đọc / quyết.
- Giữ từ trước: C32 `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index (loại ở lần build lại?); guide 5 `:65` còn nhắc
  MiniLM; `guides/full_corpus_rag.md` bước 4b dùng mã B-06 khác nghĩa.

## Đã học / bẫy gặp (đầu vào vòng cải tiến)

- **Sàn "API 500" phải đối chiếu đúng nhánh trả lỗi trong `chat.py`:** **mọi** `CitationIntegrityError` là 500 (`chat.py:127-135`), không riêng "no citation" — plan R1 của C
  và B55 đều bỏ sót (C53 M-1).
- **Nhãn đoạn đúng chỉ đánh dấu một chỗ cho mỗi fact** ⇒ `*_gold_frac` 0 không có nghĩa context không có fact; đọc nội dung trước khi đề xuất sàn "context 0 fact" (gợi ý m-2 C53
  của C làm pilot phụ lục bản 2 dừng oan, 0,0048 USD). Từ 27/10 (`a819789`) `GOLD_PATH` = `gold_v2.jsonl` + luật tiêu đề — số `*_gold_*` trước 27/10 tính bằng v1.
- **Script dựng lại context chạy từ working tree `main`** phải truyền `max_documents=10` khi so mốc B1 / K3b (main đang context 5) — suýt kết luận sai trên 5 đoạn.
- **Report tracked tả câu dev ở mức loại câu**, không nêu chủ đề cụ thể cạnh `case_index` (A nhắc; C rà lại và sửa 2 chỗ trong file của mình).
- **Chạy mốc test trước khi sửa, chạy lại đủ file test chạm sau khi sửa** — C60: code ghi log đọc thẳng `generated.model` làm một test từ đạt thành 500 (generator thay thế chỉ có
  `.text`); nhờ mốc mới thấy ngay. Log không được đổi phản hồi ⇒ đọc trường phụ bằng `getattr(…, None)`.
- **Thử ngược test bảo vệ** (thêm trường lạ ⇒ đỏ) — nhưng vị trí thử quyết định test phủ tới đâu (B70 m-1).
- **Không ghi giờ ước kiểu `12:1x`** vào file (C suýt ghi ở plan C59); lấy bằng `date` trước khi báo sha. `sed` với giờ có `/` hỏng — dùng Python để thay chuỗi.
- **Đo latency giữa hai bộ câu:** xen kẽ từng câu trong một lượt (cùng server, cùng phút) mới tách được bộ câu khỏi dao động theo giờ (C58).
- **Kiểm chéo số liệu bằng code tự viết**, không chạy lại script của người làm (C49, C52, C54, C61) — tái lập số đã lưu trước rồi mới tính số mới.
- 26/10 (giữ): commit report ngay khi viết, tách `push` thành lệnh riêng, push từ working tree chung; đã báo sha thì không sửa plan nữa; đổi mốc thì đếm lại trần trên đúng mốc.
- Giữ: mọi lệnh Python `uv run …`; quét trùng là bước riêng trước `git add`; `grep` là ugrep (regex dài lỗi "complexity" ⇒ dùng Python); repo public (không chép kho / Golden /
  câu kín / tên dự án khác vào file tracked — cổng 8011 đang bị tiến trình của một dự án khác chiếm, dùng 8014). **C chưa đọc nội dung câu kín.**

## File private C tạo phiên 27/10 (không commit)

`data/phase_8_2/r1_plan/`, `data/phase_8_2/r1/`; `data/cai_tien_tung_khau_2026-10-26/{c48,c51}/`; `data/phase_8_2/k3/tools/c49_check.py`;
`data/phase_8_2/k3b/tools/{c52_check.py, c53_check.py, c53_case120_context.py}`; `data/phase_8_2/k3b/answer/tools/c54_{check,read}.py`; `data/phase_8_2/gold_fix_proposal_2710/`;
`data/phase_8_2/latency_2710/c58/` (gồm `instrumentation.diff` đo tạm); `data/phase_8_2/c60_gate/`; `data/phase_8_1/tools/c61_recount_check.py`.

## Tiền paid phiên 27/10

- **Log (token từ usage provider, tính bằng `cost_usd`): 0,0127150 USD** = R1 pilot 0,0049030 (C46) + đo latency 0,0074884 (C58, token generator trả về) + cổng C60 0,0003236.
- **Ước: 0.** Judge / review: quota Claude Code, không dùng sub-agent.
- (Phiên tối 26/10: 0,0026861 USD log.)
