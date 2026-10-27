# Review: C64 mục 3 — đề xuất nhãn "đoạn đúng" cho 3 câu nhóm kiểm (B74)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-2d`) · 14:38 27/10/2026 (`date`)
Bản được review: `c64_de_xuat_nhan_test.md` (C, 14:30) + private `data/phase_8_2/gold_fix_proposal_2710/{proposal_test_c64.jsonl, effect_test_c64.json, ghi_chu_c64.md}`.
Cách kiểm: như C61 kiểm C56 — so từng trường với `gold_v2.jsonl`, quote = văn bản file tại offset, chunk trúng, hiệu ứng tính lại bằng **hàm đếm B tự viết**
(chỉ dùng chung luật trúng `g1_retrieval.chunk_hits_quote` = thước đang dùng), không dùng `c64_build.py`. File này không chép câu hỏi, đáp án hay nội dung kho.
**Không sửa `gold_v2.jsonl`** (sha12 trước / sau: `2f5a347a71ff`). 0 USD.

## 1. Kiểm độc lập (script `data/phase_8_2/gold_fix_proposal_2710/b74/b74_check.py`, kết quả `b74/b74_check.json`)

| Kiểm | Kết quả |
|---|---|
| Chỉ đổi phần nói (so với `gold_v2`) | 130: `evidence` cũ là tiền tố của mới, **+1** khoảng; chữ fact giữ nguyên; chỉ fact 0 đổi `quote_ids` `[0]` → `[0, 2]`. 138: `evidence` **không đổi**; chữ fact giữ nguyên; chỉ fact 2 đổi `[0, 1]` → `[0, 1, 2, 3]`. Câu 95 không có dòng đề xuất (giữ) |
| quote = văn bản file tại `[start, end)` | 7 / 7 trích dẫn của 130, 138 đúng; mỗi trích dẫn xuất hiện **đúng 1 lần** trong file |
| Chunk trúng | mỗi trích dẫn trúng đúng 1 chunk; khoảng mới của 130 trúng chunk **có trong context B1** của câu đó |
| Hiệu ứng `context_gold_all` (test, 15 câu có nhãn) | context lấy từ lượt B1 thật `b1/b1_test.jsonl` (`top_chunk_ids[:context_sources]`): **7 → 9** (+130, +138), mất 0; `k3/base_test` (nguồn C dùng): 7 → 9; context hai nguồn giống nhau 15 / 15 câu; `k3b/m_test`: **10 → 11** (+138), mất 0 — **khớp report C** |

## 2. Đọc nội dung (private, B đọc dòng gốc + đoạn trong context)

- **130 (nhiều nguồn) — đồng ý thêm khoảng.** Câu chứa khoảng mới có chủ ngữ đúng là đối tượng của fact 0 và nói đúng ý fact đó (cùng ý với khoảng đã nhãn, khác chỗ
  trong cùng file). Khoảng cắt gọn, không kéo thêm ý khác.
- **138 (so sánh) — đồng ý gắn thêm trích dẫn 2, 3.** Trích dẫn 2 nằm dưới tiêu đề mục đúng đối tượng ("hợp phần này" = đối tượng của fact 0 — B đọc tiêu đề mục
  ngay trên); trích dẫn 3 **nói thẳng** ý so sánh của fact 2. Không thêm khoảng mới.
- **95 (so sánh) — đồng ý giữ.** B kiểm 10 chunk trong context B1: không chunk nào có chữ nói thẳng ý của fact 0; các chunk có "hai năm một lần" chỉ nêu mốc khởi
  đầu (suy ra được, không nói thẳng). Giữ nhãn chặt đúng cách C56 / gold v2 làm.

## 3. Findings

### m-1 — fact so sánh của 138 nhận "một trích dẫn bất kỳ"

- **Vị trí:** đề xuất 138, fact 2 `quote_ids` `[0, 1, 2, 3]`; luật đếm `g1_retrieval.gold_coverage` (fact trúng khi **một** trích dẫn bất kỳ trúng).
- **Bằng chứng / tác động:** chỉ trích dẫn 3 nói thẳng ý so sánh; trích dẫn 0, 1, 2 mỗi cái chỉ một số liệu. Với `context_gold_all` không sao (fact 0, 1 vẫn phải trúng
  riêng), nhưng `*_gold_frac` có thể tính fact 2 "trúng" khi context chỉ có một số liệu. Nhãn v2 gốc (`[0, 1]`) đã có cùng tính chất — đề xuất không tạo ra lỗi mới.
- **Tiêu chí đóng (không chặn):** hoặc chỉ gắn `[3]` cho fact 2 (chặt hơn; B tính lại: câu 138 vẫn đủ đoạn đúng ở cả context B1 và K3b-m ⇒ hiệu ứng
  `context_gold_all` **giữ nguyên** 7 → 9 / 10 → 11), hoặc giữ như C và ghi vào giới hạn. Liên quan quy ước chung "ý so sánh" C đã nêu ở §4 report C — việc của A / User.

## 4. Giới hạn

- 3 câu, một người kiểm (B) đọc lại; dựa vào đúng tập context đã lưu (B1, K3b-m test), không chạy lại tìm kiếm.
- Không kiểm phần ngoài phạm vi C ghi (câu trả lời mốc của 138 có `citation_error`).

## 5. Kết luận

ready. Áp vào file nhãn (bản mới, không ghi đè `gold_v2` / `gold_draft`) hay không: A / User quyết, như C56 → gold v2.
