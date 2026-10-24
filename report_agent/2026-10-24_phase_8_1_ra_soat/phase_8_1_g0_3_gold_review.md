# Review: Phase 8.1 G0.3 — đoạn đúng cho 55 câu khó (B14)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major; 8 minor — nên áp trước khi khóa file)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-b0`) + 3 sub-agent Claude (chỉ đọc, mỗi agent ~18 câu)
Date: 2026-10-24 21:20–21:29 +0700 (lấy bằng `date`)
Người làm: A (qua 4 sub-agent). Nháp: `data/phase_8_1/gold/gold_draft.jsonl` (private) + `batch_*.jsonl`, `selection.json`
Việc: `session_prompt/CURRENT_HANDOFF.md` "Việc của A" → G0.3 / B14; spec 8.1 §3.3, §5 G0.3, D6

Report này chỉ ghi số câu (`case_index`), loại lỗi, đường dẫn file; không chép câu hỏi, đáp án hay nội dung corpus.

## 1. Phạm vi đã review

- **Kiểm máy (B, độc lập với validator của A)** — `/tmp/b11/b14_mech.py`: 55 dòng, không trùng, khớp
  `selection.json`; nhóm khớp `split.json`; khóa câu khớp `question_key` của Golden; mỗi trích dẫn
  `text[start:end] == quote` trên `read_source_lf` (cùng cách đọc của chunker) và xuất hiện đúng 1 lần; `quote_ids`
  hợp lệ, mỗi fact ≥1 trích dẫn, trích dẫn không dùng; câu `multi_source`/`comparative` có ≥2 file; keyword đáp án
  (có trong đáp án mẫu, không có trong câu hỏi) có nằm trong trích dẫn.
- **Luật chọn câu (B):** dựng lại từ `run1_answers.jsonl` (từ chối nhầm) + `retrieval_dense_bm25_rrf_1.jsonl` (MRR).
- **Kiểm ngữ nghĩa (3 sub-agent, chỉ đọc):** với từng câu mở file nguồn ở offset; fact có thật sự được trích dẫn
  chứng minh; fact đủ/thừa so với câu hỏi và đáp án mẫu; với câu nhiều nguồn / so sánh / "liệt kê": grep 5 thư mục
  domain (có thử không dấu) tìm file khác cùng trả lời hoặc mâu thuẫn; nhãn `is_answerable`/`ambiguity`; đáp án mẫu
  có nói quá kho không. B tự kiểm lại các phát hiện kiểm được bằng máy (41, 51, 67, corpus Hải Vân).

## 2. Findings

Không có blocker hoặc major: **không fact nào sai** (số, tên, giờ, năm đều khớp offset), **không thiếu nguồn và không
có nguồn mâu thuẫn làm đổi đáp án** ở cả 55 câu; đáp án mẫu không nói quá kho (trừ một chữ ở 92). Nhãn
`is_answerable = full` cho cả 55 câu là hợp lý.

| # | Câu | Loại | Vấn đề | Đề xuất (A sửa nháp) |
|---|---|---|---|---|
| m1 | 16, 17, 18, 19, 20, 21, 22 | nhãn `ambiguity` không thống nhất | Câu "liệt kê đủ" đều phụ thuộc độ phủ kho, nhưng chỉ 18 (và 53) ghi "exhaustiveness relies on corpus coverage", còn lại "none" | Chọn một quy ước cho mọi câu "liệt kê đủ" (đề xuất: cùng một nhãn) |
| m2 | 21 | nhãn `ambiguity` | Cách hỏi có thể hiểu là trang phục Việt, trong khi đáp án trong kho là trang phục nước khác; có chỗ cho thuê trang phục Việt nhưng không phải quán (heritage-guides, file hướng dẫn vé) | Ghi `ambiguity` khác "none" + note; cân nhắc đưa vào mẫu User duyệt |
| m3 | 41, 67, 68 | trích dẫn hụt tên | Tên/định danh của fact nằm ngay trước đoạn trích (41: nhãn văn bia đứng trước `start` — B kiểm lại; 67: tên ở dòng tiêu đề ngay trước — B kiểm lại; 68: tên ở câu trước) | Mở rộng `start` để tên nằm trong trích dẫn. Tác động thấp: tên vẫn cùng đoạn/heading, nên metric theo đoạn đúng không đổi |
| m4 | 51 | trích dẫn thừa | 2 trích dẫn (id 2, 4) không fact nào dùng (B kiểm lại); trích dẫn id 2 ghi mốc năm khác các trích dẫn còn lại 1 năm — mâu thuẫn nhỏ trong kho, đáp án không phụ thuộc | Bỏ id 2, 4 (hoặc gắn vào fact nếu cần) |
| m5 | 95 (fact 3), 168 (fact 0) | fact thừa | Fact là tiền đề lấy từ câu hỏi, không phải phần đáp án | Bỏ hoặc đánh dấu không bắt buộc, để metric "đủ fact" không phạt câu trả lời đúng |
| m6 | 85, 154 | loại câu | Nhãn `multi_source` nhưng một file là đủ và hợp lệ (đã grep, không file nào khác nêu) | Không sửa Golden chính thức (ngoài phạm vi 8.1); ghi trong `note` và khi báo theo loại câu nói rõ 2 câu này |
| m7 | 33, 113 | nhãn `ambiguity` (nhỏ) | 33: con số sức chứa không gắn với cơ sở nào trong 2 cơ sở; 113: sự kiện có 2 đêm, trích dẫn chỉ nói đêm 1 | Thêm `note` (hoặc `ambiguity` "low") |
| m8 | 92 | đáp án mẫu nói hơi quá | Đáp án mẫu có chữ "chỉ" mà trích dẫn không có | Ghi `note`; không sửa Golden |

**Quan sát thêm (không phải lỗi của G0.3):**

- **Luật chọn câu tái lập đúng:** đủ 22 câu từ chối nhầm (15 thử / 7 kiểm); phần còn lại đúng là các câu nhiều
  nguồn / so sánh / có điều kiện có MRR thấp nhất trong từng nhóm. Ở nhóm thử, ngưỡng MRR rơi vào 1,0 (19 câu đồng
  hạng, seed chọn), nhưng chỉ 1/25 câu được chọn có MRR 1,0 — chấp nhận được.
- **Kiểm máy:** 0 lỗi offset, 0 lỗi khóa/nhóm/`quote_ids`. 7 câu (16, 17, 18, 19, 21, 22, 120) có keyword đáp án
  không nằm trong trích dẫn: sub-agent xác nhận đó là tên quán/địa danh nằm ở tiêu đề file/mục, nên không phải lỗi
  (cùng loại với m3 nhưng không cần sửa).
- **Corpus mâu thuẫn (ngoài G0.3, báo A — không tự sửa, đúng `Session_Prompt.md` §5):**
  `knowledge-base-hue/travel/places/Đèo Hải Vân.md:84` ghi Hải Vân Quan miễn phí từ 01/08/2024, trong khi
  `travel/tickets/Vé tham quan Hải Vân Quan.md` và file hướng dẫn mua vé ghi phí 70.000. Không ảnh hưởng đáp án câu
  169, nhưng có thể làm bot trả lời sai câu hỏi về phí Hải Vân Quan.

## 3. Cách người kiểm chạy lại thật

- `cd backend && HF_HUB_OFFLINE=1 uv run python /tmp/b11/b14_mech.py` (kiểm máy ở mục 1).
- Script nhỏ dựng lại luật chọn từ file 7B (mục 1).
- 3 sub-agent `general-purpose` chỉ đọc (19 + 18 + 18 câu), lệnh chính: đọc offset + `grep`/`rg` trên 5 thư mục domain.
- B kiểm lại bằng máy: 41 (nhãn đứng trước `start`), 51 (id trích dẫn không dùng = [2, 4]), 67 (tên trong 400 ký tự
  trước `start`), `grep` dòng 84 của `Đèo Hải Vân.md` và file vé Hải Vân Quan.

## 4. Kết quả quan sát

Như mục 2. Kiểm máy: **PASS** 0 lỗi cấu trúc. Kiểm ngữ nghĩa: 55/55 câu fact đúng, 0 thiếu nguồn, 0 mâu thuẫn
làm đổi đáp án; 8 minor. Tiền: **0 USD** (sub-agent dùng quota Claude Code).

## 5. Giới hạn hoặc phần chưa chạy

- Kiểm ngữ nghĩa do sub-agent làm; B chỉ kiểm lại các phát hiện kiểm được bằng máy (41, 51, 67, corpus). Phần
  "không thiếu nguồn" dựa trên grep — không chứng minh tuyệt đối với cách diễn đạt lạ.
- Không đọc `user_review_sample.md` chi tiết; gợi ý thêm câu 21 (m2) vào mẫu User duyệt nếu còn chỗ.

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation` sau khi A áp m1–m5 và m7 vào nháp (m6, m8 chỉ ghi `note`). Đây là nhãn agent: User
duyệt mẫu ~10 câu theo D6, rồi A khóa file. B không sửa file nháp.
