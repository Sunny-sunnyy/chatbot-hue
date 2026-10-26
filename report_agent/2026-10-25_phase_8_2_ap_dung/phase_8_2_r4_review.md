# Review: Phase 8.2 §10 R4 — thước "số trong câu trả lời có trong đoạn được trích"

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-23`)
Date: 2026-10-26 21:52 +0700 (`date`)
Canonical guide: spec 8.2 §10.3 dòng R4 (bản duyệt `09e8f3932ede`); `CURRENT_HANDOFF.md` dòng C39 (tiêu chí ghi trước: bắt 2 / 2, báo nhầm ≤ 1 / 3)
Implementation report: `phase_8_2_r4_implementation.md` (C, 21:46)

## 1. Phạm vi đã review

- Exact file mới (working tree chung, untracked): `backend/experiments/phase_8_2/r4_numbers.py`, `backend/experiments/phase_8_2/__init__.py`
  (rỗng), `backend/tests/test_r4_numbers.py`.
- `git status --short backend/` chỉ ra hai mục mới đó ⇒ **không đụng production**. Validator / chatbot không đổi.
- Đã chạy lại: test, `check_file` của C trên 4 file. Đã kiểm độc lập context dựng lại và các số bị cờ (§3).

## 2. Findings

**m-1 (minor) — tiêu chí "báo nhầm ≤ 1 / 3" được đo trên chính các ca đã dùng để thiết kế quy tắc.**
- Bằng chứng: hai quy tắc "bỏ số trong câu hỏi" và "tách khoảng số" sinh ra từ đúng ca 143 và 93 của C36 (C37 `de_xuat_khau_tra_loi_C.md:54`).
  Hai ca này sau đó nằm trong bộ kiểm thước.
- Tác động: "đạt" là kết quả **trên mẫu đã thấy**; nó chưa cho biết tỉ lệ báo nhầm trên câu mới. Report §4 đã cho số ngoài mẫu (B1 dev:
  thật 1 / 4) và kết luận đúng hướng: chỉ dùng làm danh sách đọc lại, không làm chỉ số tự động.
- Tiêu chí đóng: report ghi một dòng: "tiêu chí đạt trên 5 ca thiết kế; ngoài mẫu (B1 dev) precision khoảng 1 / 4". Không cần sửa code.

**m-2 (minor) — nhãn "số tự tính đúng" của 137 và 172 nên đọc lại.**
- Bằng chứng (B tính bằng máy, chỉ số đếm): ở 172 (cả G2.1a lẫn B1) và 137 (B1), số bị cờ **có trong một nguồn khác của 10 đoạn context nhưng
  không ở nguồn được trích**. Hình mẫu này giống ca 51 (trích lệch đoạn), không giống ca 30 (số không có ở đâu trong context). Số có thể trùng
  tình cờ, vì vậy đây chỉ là gợi ý.
- Tác động: precision ngoài mẫu có thể cao hơn 1 / 4 nếu 137 / 172 là trích lệch đoạn. Kết luận "chỉ để đọc lại" không đổi.
- Tiêu chí đóng: C đọc lại 137 / 172, nếu nhãn đổi thì sửa bảng §4. Hoặc ghi "chưa phân biệt được trích lệch với tự tính khi số có ở nguồn khác".

Không có finding về độ phức tạp:
- Code có 3 hàm thuần, 1 hàm chạy file và CLI; dùng lại chunker, context builder và `CITATION_PATTERN` của production.
- 6 test logic thuần, mỗi test giữ một hành vi cần: chuẩn hóa dạng số; tách khoảng số + bỏ nhãn citation; số có căn cứ; số chỉ ở nguồn không
  trích; số trong câu hỏi; câu không trích nguồn. Không thừa.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `HF_HUB_OFFLINE=1 uv run …`, 0 USD:
1. `python -m pytest tests/test_r4_numbers.py -q`.
2. Script tạm `/tmp/b47/probe.py` (đã xóa) gọi **đúng `r4_numbers.check_file`** của C trên `g2_context10`, `b1_dev`, `b1_test`, `t_context10`.
   B không chạy `main()`: hàm đó ghi đè `data/phase_8_2/r4/<tên>.jsonl` của C mà không chặn. Với mỗi file, script:
   - so kết quả cờ với file C đã lưu;
   - **kiểm độc lập context dựng lại:** sha của `build_answer_input(question.strip(), packed.text)` so với `user_prompt_sha` mà B41 T2 đã bắt
     từ đường production `811d25d` (`data/phase_8_2/b1/rebase_2610/t2_new.jsonl`). Phép kiểm này chặt hơn "một độ lệch token chung";
   - với mỗi số bị cờ: đếm số có trong một nguồn **bất kỳ** của 10 đoạn, so với số không có ở đâu.

## 4. Kết quả quan sát

| Kiểm | Kết quả | Đạt |
|---|---|---|
| Test | **6 passed** (8,3 s) | ✓ |
| Cờ trên `g2_context10` | `[30, 51, 155, 172]` — đúng report; **khớp file C đã lưu** cả 4 file | ✓ |
| 5 ca C36 | 155 cờ, 51 cờ (bắt 2 / 2); 30 cờ, 93 không, 143 không (nhầm 1 / 3) ⇒ **đạt tiêu chí ghi trước** (xem m-1) | ✓ |
| Context dựng lại = context model thấy | sha chuỗi gửi model trùng T2: **120 / 120** (G2.1a dev), **120 / 120** (B1 dev), **56 / 56** (B1 test), **56 / 56** (G2.1a test) ⇒ không chỉ đúng số token mà đúng từng byte | ✓ |
| Mốc B1 dev / test | cờ `[30, 137, 155, 172]` / `[114]` — đúng report | ✓ |
| Số bị cờ: có ở nguồn khác / không ở đâu | G2.1a dev — 30: 0 / 1; 51: 1 / 0; 155: 2 / 0; 172: 1 / 0. B1 dev — 30: 0 / 1; 137: 1 / 0; 155: 3 / 0; 172: 1 / 0 (m-2) | — |
| Không đụng production | chỉ 2 mục untracked mới trong `backend/` | ✓ |
| `__init__.py` rỗng trùng nhánh `p82-b1` | add / add cùng nội dung rỗng ⇒ git gộp sạch | ✓ |

## 5. Giới hạn

- B không đọc nội dung câu trả lời / nguồn (chỉ đếm bằng máy), nên m-2 là gợi ý theo hình mẫu, chưa phải nhãn.
- Không kiểm chế độ test theo từng câu (chỉ đếm, đúng luật).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Thước đúng như mô tả: context dựng lại khớp từng byte, tiêu chí ghi trước đạt, không đụng production, test vừa
đủ. Hai minor là chữ / nhãn trong report của C, không chặn dùng R4 làm chỉ số theo dõi cho R1–R3.
