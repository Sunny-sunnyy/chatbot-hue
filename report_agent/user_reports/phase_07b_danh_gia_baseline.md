# Báo cáo cho bạn: Phase 7B — Thước đo chất lượng và điểm mốc

```text
Trạng thái: Đã đóng (User 24/10/2026)
Cập nhật lúc: 24-10-2026 +07
Người viết: A · Review: (B hoặc C)
```

## 1. Bạn nhận được gì

Một **bộ chấm tự động** cho chatbot Huế và **điểm mốc** của hệ thống hiện tại trên 176 câu hỏi
Golden. Từ nay, mỗi cải tiến ở Phase 8 đều được chấm cùng cách, cùng 176 câu, rồi so với mốc này để
biết có thật tốt hơn không.

Ví dụ: Phase 8 thử đưa 10 đoạn thay vì 5 vào ngữ cảnh → chạy lại bộ chấm → so từng câu với mốc.

## 2. Hệ thống chấm hoạt động thế nào

```text
176 câu Golden → chạy đúng đường API thật (tìm đoạn → 5 đoạn ngữ cảnh → gpt-6-luna trả lời)
  → chấm truy xuất (đoạn chứa keyword đáp án có lọt top-10 không)   — miễn phí
  → chấm câu trả lời: Claude so với đáp án mẫu, 3 điểm 1–5            — không tốn API
  → đếm từ chối đúng / từ chối nhầm, lỗi trích dẫn                     — miễn phí
```

- **Người chấm chính là Claude** (bạn chọn, để tiết kiệm). `gpt-6-luna` chấm phụ để so.
- Câu trả lời của bot vẫn do `gpt-6-luna` sinh — đó là thứ cần đo, không thay được.

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Điểm mốc (Đúng / Đủ / Trúng ý) | **4,43 / 4,28 / 4,45** | Khá tốt tổng thể |
| Câu một dữ kiện (75 câu) | 4,87 / 4,84 / 4,89 | Gần hoàn hảo |
| Câu có điều kiện (29) | 4,72 / 4,41 / 4,76 | Tốt |
| Câu so sánh (25) | 3,68 / 3,44 / 3,60 | Yếu |
| Câu ghép nhiều nguồn (29) | **3,28 / 3,00 / 3,41** | Yếu nhất |
| Câu ngoài kho (18) | 5 / 5 / 5 — từ chối đúng 18/18 | Không bịa |
| **Từ chối nhầm** | **22 / 158 câu** | Đây là toàn bộ 22 câu bị 1/1/1; bỏ chúng ra điểm còn 4,92 / 4,75 / 4,95 |
| Lỗi trích dẫn (người dùng thấy lỗi) | 4 / 176 | Hiếm |
| Chạy lại toàn bộ lần 2 | chênh trung bình ≤ 0,011 điểm | Thước đo rất ổn định |
| Claude chấm lại 30 câu | không câu nào lệch quá 1 điểm | Người chấm ổn định |
| Claude so với gpt-6-luna | trùng 89–96% số câu | Hai người chấm khác hãng đồng ý cao |

**Vì sao từ chối nhầm** (chẩn đoán 22 câu, không tốn tiền):

| Nguyên nhân | Số câu |
|---|---:|
| Đoạn chứa đáp án không nằm trong 5 đoạn ngữ cảnh | 8 |
| Có một vế, thiếu vế kia → bot từ chối cả câu | 10 |
| Có đủ bằng chứng mà vẫn từ chối | 4 |

12/22 câu có đáp án nằm ở hạng 6–10, bị cắt vì chỉ giữ 5 đoạn. Thử nhanh với 10 đoạn (0,005 USD):
10/22 câu hết từ chối — chưa chấm điểm, chỉ là dấu hiệu cho Phase 8.

## 4. Chi phí

Toàn bộ 7B + thử nhanh: **~0,087 USD (~2.200 đồng)** trên ngân sách 1 USD. Claude chấm dùng quota
Claude Code (~1,1M token), không tốn API.

## 5. Giới hạn — điều bạn nên biết

- **Chưa có người chấm tay** (bạn quyết bỏ). Hai người chấm máy đồng ý cao, nhưng nghiên cứu nói điều
  đó chưa chứng minh chúng đúng.
- 121/176 câu đã đạt tối đa → khó thấy cải tiến ở câu vốn đã tốt; cải tiến sẽ lộ chủ yếu ở 55 câu còn lại.
- Bộ câu Golden do LLM viết, người duyệt — không phải câu người dùng thật hỏi.
- Chỉ số truy xuất dựa trên keyword nên chỉ là "proxy", không phải đo hiểu nghĩa.

## 6. Hôm nay còn đúng không

| Kết quả / quyết định | Trạng thái |
|---|---|
| Bộ chấm `backend/evaluation/full_corpus_eval.py` + prompt judge `full_corpus_judge_prompt.md` | còn dùng (Phase 8 dùng lại) |
| Judge chính Claude, luna phụ | còn dùng |
| Điểm mốc trên | còn đúng tới khi Phase 8 đổi hệ thống |

## 7. Bước tiếp theo

**Phase 8 — đợt ổn định**: sửa từ chối nhầm (ngữ cảnh 10 đoạn, prompt cho trả lời phần có căn cứ),
chia đoạn bảng giá, BM25 tiếng Việt, reranker tiếng Việt… Mỗi thay đổi so với mốc theo cặp trên cùng
176 câu. Bạn sẽ quyết các lựa chọn lớn khi brainstorm.

Tài liệu kỹ thuật: spec `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`;
report `reports/phase_7b_*`; guide `guides/full_corpus_rag.md` mục "Cập nhật Phase 7B".
