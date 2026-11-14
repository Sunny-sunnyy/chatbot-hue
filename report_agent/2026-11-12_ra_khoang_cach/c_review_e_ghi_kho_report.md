# Review — report ghi kho 14/11 của E (`e_ghi_kho_diem_mong_di_lai_implementation.md`)

Người kiểm: C (`hue-rag-b4`) · 10:26 14/11/2026 (`date`) · skill `risk-gated-agent-review` · 0 USD (chỉ đọc file trong `data/` + 1 lần đọc Qdrant).
Không đọc `*sealed*`. Không in nội dung câu Golden / câu an toàn: mọi phép so chỉ in số đếm hoặc đúng / sai.

**Kết luận: ready_for_user_confirmation — 0 blocker, 0 major, 2 minor.** Mọi số ở bảng mục 4 mà C tính lại được đều khớp.

## Tính lại (độc lập, từ `data/sua_kho_2026-11-14_ghi_kho/`)
| Số trong report | C tính lại | Cách |
|---|---|---|
| K1: Đủ +0,031 (4 / 123 / 2), Đúng +0,039 (5 / 123 / 1), tụt 2 / 1, ngoài kho bị trả lời 0, lỗi kỹ thuật 0, trích dẫn mới 0 | khớp | `k1/golden/analyze.json` |
| T3: từ chối nhầm 3 ⇒ 5, thêm case 18 (nhiều nguồn) + 33 (so sánh) | khớp | đếm `refusal` trong `truoc.jsonl` ↔ `sau.jsonl` |
| 18 và 33: lần tìm đầu giống hệt trước, top-10 không có đoạn mới | khớp: top-10 giống hệt, 0 đoạn của 3 bài mới | so `top_chunk_ids` |
| Chạy lại: 18 từ chối 1 / 3, 33 từ chối 0 / 3 | khớp | `sau/chay_lai_18_33_lan{1,2,3}.jsonl` |
| K3: 8 / 158 câu đổi top-10, 5 câu có đoạn mới | khớp (case 15, 69, 117, 140, 154, 157, 168, 170) | so top-10 trước ↔ sau |
| Case 154 mất 1 / 2 trích dẫn nhãn | khớp: đoạn `#29` của bài lịch trình rời top-10; 3 đoạn bài đi lại vào (`#2` ở hạng 3) | nhãn `gold_v6` + top-10 |
| K2: ngoài kho bị trả lời = X03; gắn sai mới S10, S20; thiếu cảnh báo mới S03, S10, S11 | khớp | `k2/compare.json` |
| S-AT 4 lần trên kho mới: gắn sai S03 0 / 4 · S10 1 / 4 · S11 2 / 4 · S20 1 / 4; thiếu cảnh báo S03 / S10 / S11 mỗi câu 3 / 4 | khớp | nhãn `judge_1`, `judge_2`, `judge_regen_{1,2}`, "một trong hai người chấm" |
| B7 kho cũ: gắn sai S10 0 / 5, S11 0 / 2, S20 0 / 2; thiếu cảnh báo S03 2 / 2, S10 4 / 5, S11 1 / 2 | khớp | `data/phase_9/b7/an_toan/cham/compare.json` + `compare_regen.json` |
| Ngữ cảnh 4 câu S-AT không có đoạn mới / dòng đã sửa | khớp: 0 / 16 lượt | dò tiêu đề 3 bài mới + 3 cụm chữ đã sửa trong `context` |
| Tiền 0,2288 USD · USD / câu 0,000413 ⇒ 0,000433 | khớp | cộng mục 5; `analyze.json` |

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor | mục 4, dòng K3 | Report viết ý bị đẩy ra của case 154 "có **nguyên văn** trong đoạn #2 bài đi lại". C so theo dãy 4 từ liền nhau: chỉ 5 / 9 dãy của trích dẫn có trong đoạn #2. Số trong trích dẫn có mặt, nhưng không phải nguyên văn. Kết luận "giữ" vẫn đứng, vì K1 của câu này 5 / 5 ↔ 5 / 5. | đổi "có nguyên văn" ⇒ "có cùng ý (một phần chữ)" |
| m-2 | minor | mục 4, dòng K3 (repo public) | Cạnh `case_index` 154 có nêu **tên thông tin** mà câu hỏi nhắm tới (địa chỉ một nơi cụ thể). `Session_Prompt.md` §5 chỉ cho tả ở mức loại câu cạnh `case_index`. | bỏ cụm tên thông tin, giữ "đoạn bài lịch trình" |

## Rà tên / địa chỉ cơ sở trong report (repo public)
Không thấy tên quán / cơ sở kinh doanh hay địa chỉ lấy từ `data/`. Có nhắc tên đường của một bảo tàng công lập và tên Sở Du lịch: đây là thông tin công khai của cơ quan nhà nước, cùng loại với nội dung đã duyệt trong gói, nên C không coi là lỗi. Mã câu an toàn (X03, S03…) chỉ đi kèm loại câu, đúng luật.

## Chưa kiểm được
- Case 33 trên kho mới: lần tìm **thứ hai** do model tự gọi lấy thêm 2 đoạn. Log chỉ ghi số đoạn thêm, không ghi id đoạn, nên không biết 2 đoạn đó có thuộc bài mới không. Không đổi kết luận: chạy lại 3 lần đều trả lời.
- Ngữ cảnh câu an toàn ở trường `context` có thể chỉ gồm lần tìm đầu; C chưa đọc code harness để chắc.
