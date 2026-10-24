# Prompt gửi Claude Code đang chạy ở dự án MekongAI

User copy nguyên khối dưới vào session Claude Code của `/home/minhhieu/MekongAI_Project/mekongai-template`.

```text
Bạn đang ở dự án MekongAI. Một dự án khác của tôi (hue_rag, chatbot RAG về Huế, cũng chạy
3 session Claude Code A/B/C: A điều phối, B/C thực thi) muốn học cách MekongAI tổ chức công việc
và báo cáo. Hãy viết MỘT file Markdown mô tả cách làm việc thực tế của MekongAI, dựa trên file
thật trong repo (session_prompt/, report_agent/, .claude/skills/), không dựa vào trí nhớ.

Chỉ đọc, không sửa file nào của MekongAI. Không chép secret, nội dung tài liệu khách hàng hay
dữ liệu riêng tư — chỉ mô tả cấu trúc, quy tắc và ví dụ tên file.

Cần mô tả (mỗi mục: quy tắc là gì, file nào quy định, ví dụ đường dẫn thật, vì sao làm vậy,
điều gì từng không ổn và đã sửa):

1. Mở session: đọc những file nào, theo thứ tự nào; prompt mở session dùng chung.
2. Vai và phối hợp: điều phối giao việc thế nào (GIAO_VIEC.md), session thực thi nhận việc,
   báo xong, hỏi — kênh nào (outbox, SendMessage, qua User); ai được commit.
3. Tổ chức report_agent/: đặt tên folder đợt (<YYYY-MM-DD>_<chủ_đề>), mở đợt mới khi nào, một
   đợt kéo dài nhiều ngày thì sao; folder con theo session/việc (a_…, b_…, c_…) dùng khi nào;
   các file trong đợt (KE_HOACH, GIAO_VIEC, STATUS_<X>, <X>_outbox, BAO_CAO_<X>,
   CHANGELOG_DRAFT_<X>, TONG_HOP, NGU_CANH_DOT, TIEU_CHI) — ai ghi, ghi đè hay chỉ thêm, khi nào.
4. Trạng thái và ngữ cảnh: STATUS_<X>, NGU_CANH_DOT, WORK_CONTEXT, CURRENT_HANDOFF (nếu có) —
   khác nhau thế nào, cập nhật lúc nào, giữ ngắn ra sao; cách session mới nối tiếp việc dở.
5. Báo cáo cho người dùng ở bao_cao_he_thong/ (vừa chuyển về đây cùng tôi):
   - LUONG_HOAT_DONG_HE_THONG.md: cấu trúc mục, dòng "Cập nhật lần cuối", khi nào và ai cập nhật,
     giữ ngắn thế nào khi hệ thống đổi nhiều lần;
   - BAO_CAO_<KHÂU>.md (vd. BAO_CAO_XU_LY_PDF.md, BAO_CAO_TIM_KIEM_PDF.md): chia theo khâu hay theo
     loại file, cấu trúc một file, đánh số "bản" ra sao, viết lại hay ghi thêm khi khâu đổi, cách
     ghi "đã thử và bỏ";
   - nhat_ky/<YYYY-MM-DD>_<chủ_đề>.md: khác BAO_CAO_* thế nào, ai viết, cuối ngày hay cuối đợt;
   - quy tắc văn phong (từ ngữ đời thường, tỉ giá USD, số đo kèm ý nghĩa, không mã nội bộ…).
6. Nghiên cứu ngoài (gửi ChatGPT): đặt yêu cầu và kết quả ở đâu, theo ngày/đợt thế nào.
7. Review chéo, đóng đợt, CHANGELOG, commit: quy trình ngắn.
8. Mẫu (templates/): liệt kê và mục đích từng mẫu.
9. Bài học: điều gì làm quy trình nặng / thừa và đã bỏ; điều gì giúp User đọc dễ nhất.

Cuối file: một bảng "nếu chỉ được giữ 5 quy tắc thì giữ gì".

Lưu kết quả vào:
/home/minhhieu/hue_rag/report_agent/2026-10-24_to_chuc_bao_cao/MO_TA_CACH_LAM_VIEC_MEKONGAI.md
(nếu không ghi được ra ngoài repo thì lưu trong MekongAI ở report_agent/ và báo tôi đường dẫn).
```
