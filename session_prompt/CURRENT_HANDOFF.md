# Bàn giao hiện hành

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: ba6b694
Head commit: worktree
Risk level: low
Git authorization: commit_and_push
Sub-agent authorization: none

---

## 1. Trạng thái hiện tại

- Triển khai xây dựng dữ liệu tri thức chuẩn hóa (curated answer-facing knowledge base) cho domain `festivals/` dưới `/home/minhhieu/hue_rag/knowledge-base-hue/festivals/`.
- Khuôn mẫu biên soạn chuẩn: `knowledge-base-hue/meta/festivals-template.md`.
- Danh mục 25 lễ hội cốt lõi đã phê duyệt và cập nhật: `knowledge-base-hue/festivals/hue_festivals_core_25.md` (đã bổ sung entity 0 *Lễ hội Ẩm thực Huế*, chuẩn hóa tên gọi entity 5 *Lễ hội Cầu ngư*).
- Đã hoàn thành, rà soát và kiểm chứng độc lập với các nguồn tư liệu chính thống cho 10 entity lễ hội (từ Entity 0 đến Entity 9):
  1. `knowledge-base-hue/festivals/festival/0 Lễ hội Ẩm thực Huế.md`
  2. `knowledge-base-hue/festivals/festival/1 Festival Huế.md`
  3. `knowledge-base-hue/festivals/festival/2 Festival Nghề truyền thống Huế.md`
  4. `knowledge-base-hue/festivals/festival/3 Lễ hội Áo dài Huế.md`
  5. `knowledge-base-hue/festivals/festival/4 Lễ hội Điện Huệ Nam.md`
  6. `knowledge-base-hue/festivals/festival/5 Lễ hội Cầu ngư.md`
  7. `knowledge-base-hue/festivals/festival/6 Lễ tế Nam Giao.md`
  8. `knowledge-base-hue/festivals/festival/7 Lễ tế Xã Tắc.md`
  9. `knowledge-base-hue/festivals/festival/8 Lễ Ban Sóc triều Nguyễn.md`
  10. `knowledge-base-hue/festivals/festival/9 Lễ hội Đền Huyền Trân Công chúa.md`
- Người dùng đã xác nhận phê duyệt chất lượng và ủy quyền Git: `commit_and_push`.

## 2. Nhiệm vụ tiếp theo của Implementer

- Tiếp tục biên soạn dữ liệu các entity tiếp theo trong danh sách 25 lễ hội cốt lõi tại `knowledge-base-hue/festivals/festival/` theo khuôn mẫu `knowledge-base-hue/meta/festivals-template.md`.
- Entity tiếp theo:
  - Entity 10: `10 Hội vật làng Sình.md`
  - Entity 11: `11 Hội vật làng Thủ Lễ.md`
  - ... (tuần tự theo danh mục `hue_festivals_core_25.md`).
- Tiếp tục tuân thủ nghiêm ngặt nguyên tắc: chính xác, ranh giới entity rõ ràng, tri thức bền vững (bảo vệ temporal grounding), không suy diễn quan hệ nhân quả, không đưa giá vé chi tiết vào entity file.

## 3. Ranh giới hiện hành

Chưa authorize:
- Thay đổi chunker, embedding, vectorstore Qdrant, retrieval runtime hoặc code backend;
- Thay đổi các domain dữ liệu khác ngoài `festivals/`;
- Tự ý khởi tạo sub-agent.
