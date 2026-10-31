---
name: propose-options
description: Dùng mỗi khi cần User quyết định hoặc chọn hướng trong hue_rag — đưa phương án A/B/C, đề xuất cách làm, mở Phase mới, đổi kiến trúc/quy trình, chọn model/provider/dữ liệu/chi phí. Cũng dùng khi vấn đề còn mở cần bàn nhiều bước trước khi chốt (brainstorm Phase, thiết kế việc mới) — hỏi mỗi lần một câu có đáp án để chọn. Mỗi phương án bằng lời thường kèm đổi gì, tốn gì, khi nào sai, chọn khác mất gì, và một câu tự kiểm để User biết mình đã hiểu.
---

# Đề xuất để User chọn — A, B, C

Nguồn: skill cùng tên của dự án MekongAI (User 2026-10-24), chỉnh cho hue_rag.

## Vì sao

User muốn hiểu lý do, không chỉ chọn theo nhãn "khuyến nghị". Mỗi Phase của
hue_rag User đều brainstorm, tra cứu công nghệ/repo, thử nghiệm, so sánh rồi mới
dùng. Việc của agent: đề xuất, phản biện, giải thích cho tới khi User hiểu và tự
quyết được.

## 1. Có cần hỏi không

Chỉ hỏi khi câu trả lời đổi phạm vi, dữ liệu, tiền, thao tác phá hủy, kiến trúc
hoặc quyền (`session_prompt/Session_Prompt.md` §1). Chi tiết kỹ thuật trong phạm
vi đã duyệt: A tự quyết, nói ra lý do. Không hỏi lại điều đã chốt
(`Project_Status.md` §5).

- **Câu User hiểu được nhiều cách** (dữ liệu / code / quyết định / tài liệu; "đồng ý" áp cho một hay nhiều câu): nhắc lại
  một câu "ý bạn là … đúng không?" trước khi giao việc (25/10: hiểu "kiểm tra lại các phase" là rà dữ liệu, User muốn rà code).
- **Đề xuất có thứ tự việc** (merge trước, sửa trước…): đối chiếu spec / plan đã duyệt trước khi trình, ghi một dòng
  "khớp spec … §…" hoặc nói rõ là lệch (25/10: đề xuất merge B1 trước, trái spec 8.2 — B1 sau B0).
- **Khuyên bỏ / đóng một hướng chưa từng đo:** đối chiếu nguyên tắc "thử + so mốc trước khi chọn" (`Project_Status.md` §5, User 24/10 20:49);
  không có số chất lượng ⇒ đề xuất phép đo rẻ trước, hoặc ghi rõ "chưa đo, lý do bỏ chỉ là vận hành" (27/10: A khuyên đóng Qwen3-8B chưa đo, User hỏi lại — W28).

## 2. Mỗi phương án

| Phần | Viết gì |
|---|---|
| **Là gì** | một–hai câu lời thường; thuật ngữ thì kèm nghĩa |
| **Đổi gì** | với User (phải làm/hiểu gì) và với hệ thống (chạy khác thế nào) |
| **Tốn gì** | thời gian, tiền API, độ phức tạp code, bảo trì |
| **Khi nào sai** | điều kiện làm phương án hỏng hoặc không đáng |
| **Chọn khác thì mất gì** | so trên cùng tiêu chí |

Thêm phương án "không làm / giữ như cũ" khi đó là lựa chọn thật.

## 3. Khuyến nghị

- Nói **lý do**, và **thông tin nào nếu có sẽ làm đảo khuyến nghị**.
- Tách rõ: **đã đo / có trong code** ↔ **ước lượng** ↔ **giả thuyết**.
- Phản biện cả phương án mình khuyến nghị: khi nào nó thất bại.
- Kết bằng **một câu tự kiểm**: "nếu hiểu đúng thì trả lời được: …".
- Sau khi User chọn: nhắc lại ngắn lựa chọn đó nghĩa là gì, cái giá là gì. Câu trả
  lời cho thấy chưa hiểu thì giải thích lại bằng ví dụ đúng bài toán.

## 4. Brainstorm — vấn đề còn mở, nhiều quyết định nối nhau

- Trước khi hỏi: đọc đủ ngữ cảnh (spec/report liên quan, kết quả tra cứu); không
  hỏi điều file đã trả lời. Cần thông tin ngoài: viết yêu cầu ChatGPT theo
  `Session_Prompt.md` §9, kiểm URL bằng WebFetch.
- Chia việc lớn thành chuỗi quyết định theo thứ tự phụ thuộc; **mỗi lần một câu**,
  câu hỏi có đáp án (AskUserQuestion, 2–4 đáp án), phần giải thích mỗi đáp án theo
  mục 2 viết ngay trước câu hỏi; luôn chừa đường cho User ghi ý khác.
- Sau mỗi lựa chọn: 2–3 dòng nghĩa là gì, cái giá là gì. Ý User sửa đề bài thì ghi
  lại và đi theo.
- User chưa hiểu: dừng chọn, giảng bằng ví dụ, đề nghị quyết sau nếu chưa cần ngay.
- Kết quả: **một** tài liệu thiết kế trong `docs/superpowers/specs/` (mục tiêu,
  quyết định kèm lý do/cái giá, phạm vi, bước, tiêu chí nghiệm thu, quyền, rủi ro)
  cho User duyệt một lần (`session_prompt/WORKFLOW.md` §9). Không tự chuyển sang
  làm khi User chưa duyệt.

## 4b. Đề xuất dựng thứ mới — khám phá 5 dòng trước (theo khung_fde v1, W40; khoá AI FDE W2D1·46, W3D1·85–86)

Đề xuất dựng tính năng / Phase / agent / công cụ mới (Phase 9, giao diện mới…) ⇒ viết trước 5 dòng; thiếu dòng nào thì nói là
thiếu và chưa đề xuất dựng: (1) **vấn đề + đo bằng gì** ("để …, đo bằng …"; "cần agent cho X" là giải pháp, chưa phải vấn đề);
(2) **ba ô**: đo được không · có dữ liệu / cách đánh giá chưa · giá trị là rẻ hơn, nhanh hơn hay làm khác đi; (3) **mốc đơn giản
nhất** cách mới phải hơn (pipeline đang chạy — `Project_Status.md`); (4) **tiêu chí thành công bằng số**, ghi lúc mở (đổi khâu
chatbot ⇒ mốc và tiêu chí theo `run-experiment`); (5) **phương án B** nếu thử dưới ngưỡng. 5 dòng vào mục mục tiêu / tiêu chí
nghiệm thu của **một** spec (§4, `WORKFLOW.md` §9.1), không thành tài liệu riêng. Trước khi viết spec: thử nhỏ trên dữ liệu thật
(đếm, xem mẫu, một lời gọi — không trả phí hoặc trong trần đã duyệt, `Session_Prompt.md` §9) và báo phát hiện. Không áp cho
sửa lỗi nhỏ đã rõ nguyên nhân.

## 4c. Việc lớn — giúp User tự nói lại được (theo khung_fde v1, W40)

Mở hướng mới, đổi kiến trúc, đóng Phase ⇒ cuối đề xuất thêm vài ý để User **nói được** bằng lời thường: hiểu vấn đề thế này (và
cái chưa chắc) → đã xem những hướng nào, vì sao chọn hướng này → định làm gì, kiểm bằng cách nào → cần xác nhận điểm nào. Lý do:
User được đánh giá ở chỗ tự giải thích lại được việc agent làm (đồ án tốt nghiệp; User 31/10). Muốn luyện ⇒ gợi ý buổi
Session D (`teach-and-quiz`).

## 5. Cách nói

Rõ, đơn giản, trúng trọng tâm. **Đủ quan trọng hơn ngắn.** Không dùng nhãn
"(Recommended)" thay cho lý do.
