# Nhật ký 31/10/2026 (chiều) — áp khung AI FDE vào cách làm; sửa báo cáo bị cũ

**Cập nhật lần cuối: 17:40 31/10/2026.** Tiền paid trong buổi: 0 USD (~0 đồng).

## Tóm tắt
- Chiều nay **chỉ làm cách làm việc (AI FDE)**, chatbot **không đổi**.
- Một dự án khác của bạn dựng một **khung làm dự án theo khoá AI FDE** (khung cá nhân của bạn, ngoài repo). A đọc khung, đối chiếu với hue_rag, rồi áp những phần bạn duyệt: hook cảnh báo giờ ước, luật xét lại mọi luật đang thử, skill cho Session D, mấy phần nhỏ của skill mẫu, 2 skill cho agent (dùng từ Phase 9).
- Chạy vòng xét luật đầu tiên: **40 luật "đang thử" còn 7**, không gỡ luật nào.
- A gửi lại góp ý cho khung (lỗi hook, một con số sai, một mâu thuẫn trong mẫu). Khung đã lên **v2** phía dự án kia.
- **Bạn phát hiện báo cáo trong thư mục này bị cũ:** 4 báo cáo khâu còn ghi số trước khi sửa kho (205 file / 8.459 đoạn thay vì 204 / 8.424). A đã sửa cả 4.

## Thêm sau 17:00 (theo yêu cầu của bạn)
- **Rà lại cả 11 báo cáo** trong thư mục này cho đúng hiện trạng, **xoá phần không còn đúng** (khoảng 1.700 dòng xoá / 1.180 dòng thêm): số hiện hành,
  ~40 số dòng code lệch, các câu "bạn cần quyết" đã quyết; phương án đã thử giữ gọn kèm link. 2 người kiểm độc lập (một bên bắt 2 lỗi lớn, đã sửa).
- **Luật mới:** mọi thay đổi / thử nghiệm chạm hệ thống, kể cả không áp dụng, phải cập nhật báo cáo ở đây **ngay trong đợt**.
- **Phát hiện:** chạy lại kiểm Golden sau 2 đợt sửa kho ⇒ **1 câu** có từ khoá không còn nguyên văn trong kho — chờ bạn duyệt sửa (phiên sau).
- **Bàn xong khung báo cáo so sánh** (5 câu): một file, hai phần (theo khâu + theo Phase), đầy đủ số đo, nhãn độ tin; trước đó đo cuối + thử có giới hạn.
  Gom phần đã đóng: **dời sang phiên sau** (bạn quyết 17:39).

## Bạn cần làm gì
- Phiên sau: duyệt sửa 1 câu Golden lệch kho; chọn có mở B / C cho việc gom báo cáo so sánh không. A cũng hỏi lại 3 đề xuất cách làm còn chờ từ sáng nay (W35, I8, W36), và một đề xuất mới cho lỗi "suýt đưa chi tiết dự án khác lên repo public" (S60).
- Phiên sau quay lại dự án: spec streaming (câu Q1 + duyệt) ⇒ code.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Đối chiếu khung + khoá bản mới (ver4) | bản 30/10 vẫn đúng hướng; 4 chỗ cần xem lại đã ghi vào việc streaming / đóng gói | không phải làm lại việc cũ |
| Hook cảnh báo giờ ước lúc ghi | đã chạy, **bắt đúng 2 giờ ước A gõ** trước khi vào commit | lỗi lặp nhiều nhất của các agent nay bị nhắc ngay lúc viết |
| Vòng xét luật (lần đầu) | 40 ⇒ 7 luật đang thử; 1 memory cũ sửa | luật nào còn tác dụng thì rõ hơn, file mở phiên không phình |
| Skill mới | `teach-and-quiz` (Session D); `agent-design-review`, `agent-security-review` (Phase 9) | sẵn cho buổi học D và cho Phase 9 |
| Phase 9 | ghi rõ: **mở bằng nghiên cứu rộng** (đề tài, dự án, paper, ứng dụng thật), không khoá vào gợi ý lịch trình; Phase 1–8 = "RAG mức 1" | đúng ý bạn |
| Báo cáo bị cũ | sửa `BAO_CAO_LUU_TRU_QDRANT`, `BAO_CAO_CHIA_DOAN`, `BAO_CAO_TIM_KIEM`, `BAO_CAO_NEN_TANG` + mục lục | thư mục này lại khớp hiện trạng (204 file / 8.424 đoạn) |

## Giải thích ngắn (để bạn tự nói lại được)
Vấn đề: agent hay lặp vài lỗi cách làm (ghi giờ đoán, luật thử mãi không ai xét), và hai dự án tự học cùng bài học. Cách làm: dùng chung một khung theo khoá AI FDE; mỗi dự án chỉ lấy phần có lý do và kiểm lại bằng người kiểm khác. Kết quả: 5 luật / skill mới đang thử, vòng xét đầu tiên chạy được, khung chung sửa được 3 lỗi nhờ hue_rag. Giới hạn: phần lớn bằng chứng là "dùng rồi, chưa thấy lặp" (quan sát, chưa chứng minh); việc báo cáo cũ cho thấy luật "sửa đủ 5 chỗ" mấy ngày qua chưa được làm đủ.

## Đọc thêm
- `report_agent/2026-10-31_khung_fde/TONG_HOP.md` (kỹ thuật, giờ quyết định, commit)
- `BAO_CAO_LUU_TRU_QDRANT.md`, `BAO_CAO_CHIA_DOAN.md`, `BAO_CAO_TIM_KIEM.md` (vừa cập nhật)
