# Đề xuất cho dự án từ lần đọc lại khóa AI FDE — 25/10/2026

Nguồn: 5 sub-agent đọc lại 15 tóm tắt khóa AI FDE (ghi chú private `data/course_notes/v2/`), A tự kiểm các
khẳng định đánh dấu ✓ bằng file thật. **Đây là đề xuất, chưa phải quyết định**: mỗi mục quyết ở đúng gate / spec
của nó theo skill `run-experiment` và `propose-options`. Không đổi chatbot trong đợt này.

## 8.1 — trước khi chạy G4 / G2 (đưa vào kế hoạch B16 khi A duyệt)

1. **Cỡ mẫu G4.** Rerank chỉ xếp lại top-10 có thể cứu tối đa khoảng 6–8 câu (G1). Sub-agent tính tay: cần ≥ 4–5
   câu thắng, 0 câu thua, để CI 95% > 0 (thêm Holm khi nhiều biến thể). ⇒ ghi trước "kết quả có thể chưa rõ";
   cân nhắc G4-B (pool 100) là câu hỏi chính.
2. **Nhiễu G2 lấy từ 7B có sẵn (0 USD).** ✓ Run 1 ↔ Run 2: 16/176 câu đổi điểm, lỗi citation 4 → 6, từ chối nhầm
   22 = 22 (`reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md`). Tiêu chí "lỗi citation không tăng"
   của plan B16 sẽ bác cả biến thể vô hại ⇒ đổi thành mức tụt cho phép theo số câu, đã trừ nhiễu.
3. **Luật xử lý đầu ra lỗi của rerank luna** (hoán vị thiếu / lặp / bị cắt) ghi trước; không để "giữ thứ tự gốc"
   thành fallback che lỗi — đếm riêng số câu lỗi.
4. **Đo độ trễ đúng cách:** chạy từng câu một, không session nào khác dùng GPU, bỏ lần nạp model đầu, báo p50/p95
   cả luồng và từng khâu, cả CPU; một dòng "đang giữ GPU" trong `STATUS_<X>.md`.
5. **Reasoning effort:** thêm biến thể `none`; gọi baseline là "mặc định (không gửi)", không gọi "medium" khi
   chưa có bằng chứng.

## Thước đo — số theo dõi ở 8.1, tiêu chí ở 8.2 (không đổi thước giữa chừng)

6. **Bám nguồn bằng code.** ✓ Judge hiện tại bỏ qua citation và không trừ chi tiết thêm
   (`backend/evaluation/full_corpus_judge_prompt.md:13-16`) ⇒ không gì bắt được một con số bịa. Kiểm bằng code:
   số (giá / giờ / năm) trong câu có `[n]` phải xuất hiện trong đoạn `[n]`; chạy lại trên câu trả lời 7B/G2 đã lưu.
7. **Câu lỗi citation vẫn được 5 điểm.** ✓ (`reports/phase_7b_gate_4_…:111`). Người dùng thấy lỗi 500 nhưng
   điểm không phản ánh ⇒ báo riêng "điểm trên câu người dùng thật sự nhận được".
8. **`is_refusal` chỉ bắt câu trùng hệt câu từ chối chuẩn** (sub-agent đọc code, chưa kiểm lại) ⇒ câu từ chối một
   phần bị tính là đã trả lời; kiểm trước khi dùng cho G2.2.

## 8.2

9. **Gate dữ liệu.** Sổ mâu thuẫn trong kho (53 mục) chưa có cột trạng thái, chưa có mục Hải Vân (B14). Thêm
   trạng thái; dữ kiện dễ đổi (giá, giờ) có một nơi chuẩn; ghi "đối chiếu ngày" trong `## Nguồn dữ liệu` (không
   frontmatter — `Session_Prompt.md` §5). Mục "Nguồn dữ liệu" hiện thiếu ở nhiều file ngoài foods (đếm bằng grep,
   chưa kiểm lại).
10. **Build index 8B chạy tiếp được.** Code hiện dừng cả lần build khi một batch lỗi; một lần build ~133 batch có
    trả tiền, đã gặp 504 / 429. Đề xuất lưu vector theo batch, chỉ thử lại lỗi tạm thời, không đổi provider khi
    thử lại. **Trái luật "không resume" hiện hành** (`Session_Prompt.md` §7) ⇒ cần User duyệt trong spec 8.2.
11. Reranker chỉ thắng trên GPU ⇒ ghi hai kết luận: dùng được trên máy User; chưa chắc mang lên deploy rẻ.
12. Đầu 8.2: một sub-agent ngữ cảnh mới review cấu trúc toàn bộ diff 8.1; tách các "khâu dính" trước khi thêm cải tiến.

## Phase 9 (chỉ là danh sách kiểm, chưa phải spec)

13. Bắt đầu từ **phân loại lỗi còn lại sau 8.2**; G1 cho thấy nghẽn ở xếp hạng — vòng lặp agent không giải loại
    lỗi đó. Agent chỉ đáng khi còn nhiều câu nhiều nguồn thiếu đoạn đúng.
14. Baseline = pipeline cố định tốt nhất của 8.2. Agent nếu có: bọc pipeline thành một tool tìm kiếm chỉ đọc;
    kiểm citation, "context rỗng thì từ chối", trần số lần gọi model và trần tiền mỗi câu nằm trong code.
15. Dùng `openai-agents` đang có trước khi thêm framework mới. Quyết sớm chat một lượt hay nhiều lượt (đổi cả bộ đo).
    Memory dài hạn cần danh tính đã xác minh — để sau.

## Khi quyết định deploy / public

16. Giới hạn lượt gọi và trần tiền trong code (AWS không có trần cứng).
17. Giao diện: ✓ `frontend/app.js:72` dùng DOMPurify mặc định — sub-agent nói vẫn cho thẻ ảnh trỏ URL ngoài
    (kênh gửi dữ liệu ra ngoài tiềm ẩn); chặn trước khi public.
18. API trả nguyên văn đoạn corpus (`sources.excerpts`) trong khi corpus được coi là private ⇒ User cần quyết
    "private" nghĩa là gì với người dùng chatbot.

## Bàn giao / portfolio

19. README gốc cho repo public (đã lọc dữ liệu private); kịch bản demo vài lượt chọn trước, mỗi lượt thể hiện
    một cơ chế; User tự giải thích từng lượt (Session D); mục "giới hạn đã biết" ngắn.
