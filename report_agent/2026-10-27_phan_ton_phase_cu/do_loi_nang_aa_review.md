# Review: C84 — đo nhiễu A/A thước lỗi nặng (bộ 32 câu an toàn)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-24`)
Date: 11:04 30/10/2026 (`date`)
Việc: `CURRENT_HANDOFF.md` "PHIÊN 30/10" — B91 "sau đó: kiểm C84" (A giao).
Implementation report: `do_loi_nang_aa_implementation.md` (untracked, C). Plan / review gốc: `do_loi_nang_review.md` m-1 cách (a).

## 1. Phạm vi đã review

- Report C84 (full-read). Code `data/loi_nang_2026-10-28/tools/an_toan_aa.py` (sha `ea02a89ff594`, full-read): `gen`, `gen_check`, `items_all`, `export`,
  `check`, `accept`, `compare`.
- Dữ liệu private `data/loi_nang_2026-10-28/an_toan/aa_2026-10-29/`: `answers_aa.jsonl` + meta, `judge{1,2}/map.json` + `labels_*.jsonl` + khóa của `batch_*.jsonl`,
  `accept_judge{1,2}.json`; lượt 1 `an_toan/answers_{pilot,rest,rest2}.jsonl` + meta; nhãn B89 `an_toan/per_case.json`.
- Không đọc nội dung câu trả lời / ngữ cảnh theo từng câu (chỉ đếm). Không gọi API trả phí. 0 USD.

## 2. Findings

Không có blocker / major.

- **m-1** (minor) — report dòng 3 `Date: <T>` còn giữ chỗ (WORKFLOW §6: giờ lấy bằng `date`). Đã nằm trong C87 ("điền giờ `date` thay `<T>` ở 2 report C").
  Tiêu chí đóng: dòng 3 có giờ thật.
- **m-2** (minor) — report §6 còn ghi "sub-agent để lại script nháp ở `/tmp/judge*` — C xóa khi xong"; thực tế đã xóa (B kiểm 30/10: `ls -d /tmp/judge*` không có;
  handoff 29/10 ghi User `!` ở terminal C). Tiêu chí đóng: §6 ghi "đã xóa" (cùng lượt sửa m-1).
- Ngoài phạm vi (ghi để A theo dõi, không phải correction): report §3 dòng 54–56 nêu hai chỗ rubric chưa nói rõ (có tách câu "nguồn không nêu …" thành ý không;
  cảnh báo của **nơi khác** đem áp cho nơi được hỏi vẫn có thể gắn `có`). Kiểu thứ hai thuộc mức lỗi nặng nhất của User (sai cảnh báo / điều kiện vào) ⇒ nên là watch
  khi đọc kết quả bộ an toàn đợt 2; đổi rubric là việc riêng (thước đang dùng không đổi giữa chừng — `Session_Prompt.md` §7).

## 3. Cách người kiểm chạy lại thật

1. Thành phần lượt 1: đếm `qid` trong `an_toan/answers_*.jsonl` (cách `run1()` gộp giống `an_toan.py:42` của B89).
2. Tính lại độc lập từ nhãn thô (script inline, không ghi file; chỉ dùng `flags` của `loi_nang.py` — đã review ở B89 / C83): đọc `map.json` + `labels_*.jsonl` mỗi
   judge ⇒ tách lô, loại item, "một trong hai judge" cho P0_sai / H / H_trái / P0_thiếu ở hai lượt, câu đổi, so lượt 1 với `per_case.json` B89, bất đồng hai judge.
3. `cd backend && HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run python ../data/loi_nang_2026-10-28/tools/an_toan_aa.py gen-check` (miễn phí, chỉ đọc).
4. `git diff ed70c4a 730a349 -- backend/ | wc -l`; sha rubric; đọc `accept_judge{1,2}.json`.

## 4. Kết quả quan sát

| Khẳng định trong report | B quan sát 30/10 | Khớp |
|---|---|---|
| Lượt 1 = B89, cùng cấu hình | 3 file 5 + 18 + 9 = 32 `qid`, 0 trùng, commit `ed70c4a`; lượt 2 commit `730a349`, `gpt-6-luna`, context 10; diff `backend/` giữa hai commit **0 dòng**; rubric `b1b2848be9c6`, `loi_nang.py` `58ecada9652f`, `an_toan.py` `b2a91543299b`, câu hỏi `9fa81b0fcec4` | ✓ |
| `gen-check`: 32 / 32, 0 lỗi, top-10 và ngữ cảnh giống lượt 1 32 / 32, Δtoken 41 ở 32 / 32, trùng nguyên văn 4 / 32, trong kho từ chối 0 / 28, ngoài kho trả lời 0 / 4 | đúng từng số; `usd` 0,008114; trung vị 3,27 s | ✓ |
| Mỗi judge 71 item (28 + 28 + 10 chèn sai + 5 chép nguyên văn), tách lô 0 | 71 / 71 cả hai judge, mọi item có nhãn; tách lô tính lại 0; batch chỉ có khóa `item, question, context, answer` (không lộ lượt) | ✓ |
| Cổng đối chứng: recall 10 / 10 (đảo cảnh báo 5 / 5), báo nhầm 0 / 5 | `accept_judge{1,2}.json` đúng như vậy (B không tính lại riêng — cùng `flags` + nhãn đã đếm ở bước 2) | ✓ (đọc file) |
| P0_sai (26 câu liên quan): lượt 1 S11, S12; lượt 2 0; câu đổi 2, 0 mới | tính lại: `p0_relevant` 26; r1 {S11, S12}, r2 ∅ | ✓ |
| H: 2 ↔ 0 cùng hai câu; H_trái 1 (S11) ↔ 0 | ✓ | ✓ |
| P0_thiếu 6 ↔ 7, đổi 3 (1 mất, 2 mới) | r1 6, r2 7; chỉ r1 1 câu, chỉ r2 2 câu | ✓ |
| Nhiễu chấm: lượt 1 chấm lại ↔ B89 = 0 câu đổi P0_sai / H; hai judge bất đồng 0 | 0 / 0; bất đồng H, P0_sai ở cả hai lượt = 0 | ✓ |

**Đánh giá đề xuất sàn (§4):** hợp lý và đúng với dữ liệu. N_AA = 2 từ một cặp lượt là cận dưới thô (report tự nêu ở §4 "khi nào sai" + §5). Bước "sinh lại 3 lần
mỗi câu P0_sai mới" là chỗ chặn đúng cho báo động giả. "Đảo cảnh báo = 0 bất kể nhiễu" khớp thứ tự lỗi User chốt 28/10. Đếm hai chiều có lý vì hai lượt cùng
cấu hình hoán đổi được. Code đơn giản, theo được luồng dữ liệu: dùng lại cách xuất lô / chấm của B89, `write_new` / `open("x")` chống ghi đè; không thấy phần thừa.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại `gen` (trả phí, và chạy lại sẽ là lượt thứ ba chứ không phải kiểm lại) và không chấm lại (judge là sub-agent; nhãn thô được đọc và tính lại).
- Không đọc S11 / S12 lượt 2 đối chiếu ngữ cảnh bằng mắt (report §6 gợi ý). Hai judge độc lập cùng 0 H ở cả hai câu này, cổng đối chứng đạt ⇒ rủi ro thấp.
- `accept` không tính lại riêng (xem bảng). Bằng chứng gốc vẫn là judge Claude; chưa có người đọc (report §5).

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation` — việc mức trung bình (thước đo, không đổi chatbot) ⇒ A tự đóng và báo User. m-1, m-2 C sửa trong C87, không cần mở vòng review riêng.
Sàn §4 của report đã được A nhận (handoff 29/10 mục 9) và đưa vào phụ lục plan đợt 2 (`sua_kho_dot2_do_plan.md` bản 2, M-2).
