# Bàn giao hiện hành

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: ba6b694
Head commit: worktree
Risk level: low
Git authorization: commit_and_push (đã được người dùng cấp quyền trực tiếp)
Sub-agent authorization: none

---

## 1. Trạng thái hiện tại

- Triển khai xây dựng dữ liệu tri thức chuẩn hóa (curated answer-facing knowledge base) cho domain `festivals/` dưới `/home/minhhieu/hue_rag/knowledge-base-hue/festivals/`.
- Khuôn mẫu biên soạn chuẩn: `knowledge-base-hue/meta/festivals-template.md`.
- Danh mục 25 lễ hội cốt lõi đã phê duyệt và cập nhật: `knowledge-base-hue/festivals/hue_festivals_core_25.md` (đã bổ sung entity 0 *Lễ hội Ẩm thực Huế*, chuẩn hóa tên gọi entity 5 *Lễ hội Cầu ngư*).
- Đã hoàn thành 100% việc biên soạn, rà soát và kiểm chứng độc lập với các nguồn tư liệu chính thống cho toàn bộ 26 entity lễ hội cốt lõi:
  1. `knowledge-base-hue/festivals/festival/Lễ hội Ẩm thực Huế.md`
  2. `knowledge-base-hue/festivals/festival/Festival Huế.md`
  3. `knowledge-base-hue/festivals/festival/Festival Nghề truyền thống Huế.md`
  4. `knowledge-base-hue/festivals/festival/Lễ hội Áo dài Huế.md`
  5. `knowledge-base-hue/festivals/festival/Lễ hội Điện Huệ Nam.md`
  6. `knowledge-base-hue/festivals/festival/Lễ hội Cầu ngư.md`
  7. `knowledge-base-hue/festivals/festival/Lễ tế Nam Giao.md`
  8. `knowledge-base-hue/festivals/festival/Lễ tế Xã Tắc.md`
  9. `knowledge-base-hue/festivals/festival/Lễ Ban Sóc triều Nguyễn.md`
  10. `knowledge-base-hue/festivals/festival/Lễ hội Đền Huyền Trân Công chúa.md`
  11. `knowledge-base-hue/festivals/festival/Hội vật làng Sình.md`
  12. `knowledge-base-hue/festivals/festival/Hội vật làng Thủ Lễ.md`
  13. `knowledge-base-hue/festivals/festival/Lễ hội Đua ghe truyền thống Huế.md`
  14. `knowledge-base-hue/festivals/festival/Đại lễ Phật đản tại Huế.md`
  15. `knowledge-base-hue/festivals/festival/Lễ hội Quán Thế Âm tại Huế.md`
  16. `knowledge-base-hue/festivals/festival/Lễ hội Thanh Trà Huế.md`
  17. `knowledge-base-hue/festivals/festival/Chợ quê ngày hội – Cầu ngói Thanh Toàn.md`
  18. `knowledge-base-hue/festivals/festival/Lễ hội Hương xưa làng cổ – Phước Tích.md`
  19. `knowledge-base-hue/festivals/festival/Lễ hội Sóng nước Tam Giang.md`
  20. `knowledge-base-hue/festivals/festival/Ngày hội Sen Huế.md`
  21. `knowledge-base-hue/festivals/festival/Ngày hội Hoàng Mai Huế.md`
  22. `knowledge-base-hue/festivals/festival/Lễ hội làng Dương Nỗ.md`
  23. `knowledge-base-hue/festivals/festival/Lễ Thu tế làng An Truyền.md`
  24. `knowledge-base-hue/festivals/festival/Hội xuân Gia Lạc.md`
  25. `knowledge-base-hue/festivals/festival/Lễ giỗ Tổ nghề Kim hoàn.md`
  26. `knowledge-base-hue/festivals/festival/Lễ tế Bà Bún Vân Cù.md`
- Toàn bộ các file tuân thủ nghiêm ngặt nguyên tắc: chính xác, ranh giới entity rõ ràng, tri thức bền vững (temporal grounding), không suy diễn, không đưa giá vé chi tiết vào entity file, bám sát `knowledge-base-hue/meta/festivals-template.md`.
- Đã cập nhật bảng `knowledge-base-hue/festivals/hue_festivals_core_25.md` chuẩn xác.
- Người dùng yêu cầu không commit và push lẻ tẻ trong quá trình làm; gom hoàn thành xong hết toàn bộ 25 lễ hội mới commit và push một lần.

## 2. Nhiệm vụ tiếp theo

- Báo cáo người dùng về việc hoàn thành 100% toàn bộ danh mục 25 Lễ hội Cốt lõi tại Huế.
- Xin chỉ thị của người dùng về việc:
  1. Kiểm tra / tổng duyệt toàn bộ bộ tài liệu tri thức lễ hội;
  2. Phê duyệt thực hiện Git commit và push toàn bộ các file tri thức mới tạo;
  3. Kế hoạch tiếp theo (ingestion pipeline / evaluation / các domain tiếp theo).

## 3. Ranh giới hiện hành

Chưa authorize:
- Thay đổi chunker, embedding, vectorstore Qdrant, retrieval runtime hoặc code backend;
- Thay đổi các domain dữ liệu khác ngoài `festivals/`;
- Tự ý khởi tạo sub-agent.
